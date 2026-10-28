// Sjabloon: een muterende route met schema-validatie, een response-schema en een idempotentiesleutel.
// Dekt: API-01, API-02, API-03, API-09, API-27, API-33, API-35, BIZ-39, API-20, AUTH-72, API-12
// Dekt gedeeltelijk:
//   - BIZ-39: "bewaar de sleutel langer dan de langste herhaling van de afzender" vraagt een opruimjob met een
//     termijn; die staat hier niet. Een proces dat stopt tussen claim en afronding laat de rij op "bezig" staan
//     (de client krijgt dan 409 tot iemand de rij beoordeelt); een huurtermijn daarvoor is BIZ-42.
//   - AUTH: vereisSessie is een lege plek die gesloten faalt (API-12). Vul hem in volgens de AUTH-regels; de
//     tenant komt uit de geverifieerde sessie, nooit uit de aanvraag (AUTH-72).
// Aanpassen: het schema, de prijslijst en maakBestelling. De prijs berekent de server uit een vertrouwde bron
//   (API-27); de client stuurt alleen wat hij wil, niet wat het kost.
// De tabel staat in migraties/idempotentie.sql (letterlijk uit BIZ-39).
// Controleren (API-33, BIZ-39): twee identieke POST's met dezelfde sleutel geven hetzelfde antwoord en een rij;
//   dezelfde sleutel met een andere body geeft een fout; een tweede verzoek terwijl het eerste loopt geeft 409.
// Gevalideerd op 04-10-2026 in een wegwerpcontainer: tsc --noEmit met de tsconfig uit 07-typescript-tests
//   (TypeScript 6.0.3) en eslint --max-warnings 0 met eslint.config.mjs (typescript-eslint 8.71.0), beide groen.
//   Niet gedraaid als dienst.
import type { FastifyInstance, FastifyRequest } from 'fastify';
import { createHash } from 'node:crypto';
import { z } from 'zod';
import { env } from '../env.js';
import { AppError } from '../fouten.js';
import { pool } from '../db.js';

const PAKKETTEN = ['basis', 'plus'] as const;
const PRIJS_IN_CENTEN: Record<(typeof PAKKETTEN)[number], number> = { basis: 0, plus: 0 }; // vul in uit de vertrouwde bron (API-27)

// Strikt object: onbekende velden worden geweigerd; elk veld heeft een grens (API-02, API-03, API-35).
const Body = z.strictObject({
  pakket: z.enum(PAKKETTEN),
  aantal: z.number().int().min(1).max(10),
});
const Sleutel = z.uuid();

// Alleen deze velden gaan terug naar de client (API-09).
const Antwoord = {
  type: 'object',
  additionalProperties: false,
  required: ['bestelling_id', 'totaal_in_centen', 'valuta'],
  properties: {
    bestelling_id: { type: 'string' },
    totaal_in_centen: { type: 'integer' },
    valuta: { type: 'string' },
  },
} as const;
interface AntwoordType {
  bestelling_id: string;
  totaal_in_centen: number;
  valuta: 'EUR';
}

// Lege plek: sessiecontrole. Faalt gesloten tot hij is ingevuld (API-12).
function vereisSessie(req: FastifyRequest): { tenantId: string; userId: string } {
  req.log.warn({ event: 'sessiecontrole_niet_ingevuld' }, 'vereisSessie is nog een lege plek: elke aanvraag krijgt 401');
  throw new AppError(401, 'niet_ingelogd', 'Niet ingelogd');
}

const ROUTE = 'POST /api/bestellingen';

export function bestellenRoutes(app: FastifyInstance): void {
  app.post(
    '/api/bestellingen',
    {
      schema: { response: { 201: Antwoord, 200: Antwoord } },
      config: { rateLimit: { max: env.RATE_LIMIT_BESTELLEN_PER_MINUUT, timeWindow: '1 minute' } },
    },
    async (req, reply) => {
      const sessie = vereisSessie(req);
      const body = Body.parse(req.body);
      const sleutel = Sleutel.parse(req.headers['idempotency-key']);
      const bodyHash = createHash('sha256').update(JSON.stringify(body)).digest();

      // Claim de sleutel, gebonden aan tenant, route en inhoud (BIZ-39). Eigen statement, direct vastgelegd,
      // zodat een tweede verzoek de toestand "bezig" ziet.
      const claim = await pool.query(
        `insert into idempotentie (tenant_id, route, sleutel, body_hash, status)
         values ($1, $2, $3, $4, 'bezig') on conflict do nothing returning 1`,
        [sessie.tenantId, ROUTE, sleutel, bodyHash],
      );
      if (claim.rowCount !== 1) {
        const bestaand = await pool.query<{ body_hash: Buffer; status: string; antwoord: AntwoordType | null }>(
          'select body_hash, status, antwoord from idempotentie where tenant_id = $1 and route = $2 and sleutel = $3',
          [sessie.tenantId, ROUTE, sleutel],
        );
        const rij = bestaand.rows[0];
        if (rij === undefined || !rij.body_hash.equals(bodyHash)) {
          throw new AppError(400, 'idempotentie_andere_inhoud', 'Deze sleutel is al gebruikt voor een ander verzoek');
        }
        if (rij.status !== 'klaar' || rij.antwoord === null) {
          throw new AppError(409, 'idempotentie_bezig', 'Verzoek loopt al');
        }
        return reply.status(200).send(rij.antwoord); // herhaling: het opgeslagen resultaat (API-33)
      }

      // Het werk en het afronden van de sleutel in een transactie (API-32).
      const client = await pool.connect();
      try {
        await client.query('begin');
        await client.query("select set_config('app.tenant_id', $1, true)", [sessie.tenantId]); // DB-16
        const totaal = PRIJS_IN_CENTEN[body.pakket] * body.aantal; // hele centen, op de server (API-27, API-28)
        if (!Number.isSafeInteger(totaal) || totaal <= 0) {
          throw new AppError(400, 'ongeldig_totaal', 'Ongeldige invoer'); // API-35; gratis heeft een eigen pad (BIZ-19)
        }
        const nieuw = await client.query<{ id: string }>(
          `insert into bestellingen (tenant_id, user_id, pakket, aantal, totaal_in_centen, valuta)
           values ($1, $2, $3, $4, $5, 'EUR') returning id`,
          [sessie.tenantId, sessie.userId, body.pakket, body.aantal, totaal],
        );
        const id = nieuw.rows[0]?.id;
        if (id === undefined) throw new Error('bestelling niet aangemaakt');
        const antwoord: AntwoordType = { bestelling_id: id, totaal_in_centen: totaal, valuta: 'EUR' };
        await client.query(
          `update idempotentie set status = 'klaar', antwoord = $4
           where tenant_id = $1 and route = $2 and sleutel = $3`,
          [sessie.tenantId, ROUTE, sleutel, JSON.stringify(antwoord)],
        );
        await client.query('commit');
        req.log.info({ event: 'bestelling_aangemaakt', tenant_id: sessie.tenantId, user_id: sessie.userId }, 'bestelling');
        return await reply.status(201).send(antwoord);
      } catch (fout) {
        await client.query('rollback');
        // Het werk is teruggedraaid: geef de sleutel vrij, zodat de client veilig kan herhalen.
        await pool.query('delete from idempotentie where tenant_id = $1 and route = $2 and sleutel = $3 and status = $4', [
          sessie.tenantId,
          ROUTE,
          sleutel,
          'bezig',
        ]);
        throw fout;
      } finally {
        client.release();
      }
    },
  );
}
