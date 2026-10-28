// Sjabloon: handler voor de klassieke Mollie-webhook. De payload is alleen een signaal: de status komt uit de
//   Mollie-API, de verwerking is idempotent en een herhaling is veilig.
// Dekt: API-36, API-37, API-38, API-39, API-40, API-45, API-30, API-01, API-05, API-12, DB-68, ARCH-20, AUTH-60
// Dekt gedeeltelijk:
//   - API-44 (handtekening van de next-gen webhooks, X-Mollie-Signature) staat hier niet: dit is de klassieke
//     webhook, waar navragen bij de API de echtheidscontrole is (API-36). Gebruik voor next-gen de officiele
//     bibliotheek.
//   - API-42 (wat er na "betaald" gebeurt: terugbetaling, chargeback) en API-43 (dagelijkse afstemming) zijn
//     eigen stukken.
//   - API-40: de 15 seconden bewaak je met de time-out van de Mollie-client en van de database; zwaar werk doet
//     de worker die de taak oppakt.
// Aanpassen: de tabel- en kolomnamen, en de taak die de worker oppakt. De tabellen staan in
//   migraties/idempotentie.sql. Het Mollie-id sla je zelf op bij het aanmaken van de betaling (API-37), met
//   een Idempotency-Key per zakelijke actie (API-41).
// Tenant: de webhook heeft geen sessie. De rol waarmee deze handler de betaling opzoekt moet dat over tenants
//   heen mogen (een eigen, smalle rol of functie: DB-19, DB-24); werk dat uit per project.
// Controleren:
//   een POST met het id van een betaling met status open leidt niet tot levering (API-36)
//   een betaling met een ander bedrag of een andere valuta wordt niet geleverd en geeft een alarm (API-37)
//   20 gelijktijdige aanroepen voor een betaling geven precies een leveringstaak (API-38, API-30)
//   de database laten falen geeft 5xx; een onbekend id geeft 200 zonder Mollie-aanroep (API-39)
// Gevalideerd op 04-10-2026 in een wegwerpcontainer: tsc --noEmit met de tsconfig uit 07-typescript-tests
//   (TypeScript 6.0.3) en eslint --max-warnings 0 met eslint.config.mjs (typescript-eslint 8.71.0), beide groen.
//   Niet gedraaid als dienst en niet tegen Mollie.
import formbody from '@fastify/formbody';
import { createMollieClient, PaymentStatus } from '@mollie/api-client';
import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import { env } from '../env.js';
import { pool } from '../db.js';

const mollie = createMollieClient({ apiKey: env.MOLLIE_API_KEY });

// De enige invoer die telt: het id (API-36). Strikt, met een grens (API-02, API-03).
const Body = z.strictObject({ id: z.string().regex(/^tr_[A-Za-z0-9]{1,60}$/) });

// "10.00" naar 1000, zonder tussenstap via een float (API-28, BIZ-11).
function naarCenten(waarde: string): number {
  const m = /^(\d{1,9})\.(\d{2})$/.exec(waarde);
  if (m === null) throw new Error('onverwacht bedrag van Mollie');
  return Number(m[1]) * 100 + Number(m[2]);
}

export async function mollieWebhookRoutes(app: FastifyInstance): Promise<void> {
  // Alleen dit type inhoud, alleen binnen deze plugin (API-05).
  await app.register(formbody);

  app.post('/webhooks/mollie', async (req, reply) => {
    const { id } = Body.parse(req.body);

    // Zoek op het Mollie-id dat je zelf hebt opgeslagen, niet op iets uit het verzoek of uit metadata (API-37).
    const eigen = await pool.query<{ bestelling_id: string; bedrag_in_centen: number; valuta: string; status: string }>(
      'select bestelling_id, bedrag_in_centen, valuta, status from betalingen where mollie_payment_id = $1',
      [id],
    );
    const betaling = eigen.rows[0];
    if (betaling === undefined) {
      return reply.status(200).send(); // onbekend id: 200, zonder Mollie-aanroep (API-39)
    }

    // De status komt alleen uit het antwoord van de API, met de eigen sleutel (API-36). Een fout hier gooit:
    // de handler antwoordt 5xx en Mollie probeert opnieuw (API-39, API-12).
    const bijMollie = await mollie.payments.get(id);

    if (bijMollie.status !== PaymentStatus.paid) {
      req.log.info({ event: 'betaling_status', status: bijMollie.status }, 'niet betaald, geen levering');
      return reply.status(200).send();
    }

    // Bedrag en valuta vergelijken met wat de bestelling verwacht, voor de levering (API-37).
    if (naarCenten(bijMollie.amount.value) !== betaling.bedrag_in_centen || bijMollie.amount.currency !== betaling.valuta) {
      req.log.error({ event: 'betaling_afwijkend_bedrag', bestelling_id: betaling.bestelling_id }, 'ALARM: bedrag of valuta wijkt af');
      return reply.status(200).send(); // niet leveren; herhalen lost dit niet op, een mens kijkt ernaar
    }

    // Een winnaar: de overgang naar betaald is atomair en de leveringstaak ligt in dezelfde transactie vast
    // (API-30, API-38, ARCH-20). Elke volgende aanroep voor dezelfde betaling doet niets.
    const client = await pool.connect();
    try {
      await client.query('begin');
      const gewonnen = await client.query(
        "update betalingen set status = 'paid', betaald_op = now() where mollie_payment_id = $1 and status <> 'paid' returning bestelling_id",
        [id],
      );
      if (gewonnen.rowCount === 1) {
        // Unieke sleutel op (bestelling_id, soort) als vangnet (API-31, DB-68).
        await client.query(
          "insert into taken (bestelling_id, soort) values ($1, 'leveren') on conflict (bestelling_id, soort) do nothing",
          [betaling.bestelling_id],
        );
        req.log.info({ event: 'betaling_betaald', bestelling_id: betaling.bestelling_id }, 'leveringstaak aangemaakt');
      }
      await client.query('commit');
    } catch (fout) {
      await client.query('rollback');
      throw fout; // 5xx: Mollie probeert opnieuw (API-39)
    } finally {
      client.release();
    }

    // 200 pas nu de statuswijziging en de taak duurzaam vastliggen (API-39). Het zware werk doet de worker (API-40).
    return reply.status(200).send();
  });
}
