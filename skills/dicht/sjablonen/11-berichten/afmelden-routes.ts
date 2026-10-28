// Sjabloon: de twee routes voor afmelden. GET toont alleen een bevestigingsknop, POST meldt af.
// Dekt: MSG-07, MSG-08, MSG-09, MSG-10 (direct verwerken), WEB-29, API-12
// Dekt gedeeltelijk: MSG-10 vraagt ook dat de verzendcode de afmeldlijst vlak voor het versturen controleert;
//   dat hoort in de verzendcode (zie het patroon in 04-scripts/skelet.py: controle vlak voor elke actie).
// Aanpassen: de tabel afmeldingen (unieke sleutel op ontvanger_id en lijst_id), de teksten en waar het geheim
//   vandaan komt. De POST werkt zonder cookie, login of CSRF-token (MSG-07): het token is de autorisatie.
//   Zet een limiet op de route (WEB-66).
// Het antwoord is gelijk voor een bestaande en een onbestaande ontvanger (MSG-09); een ongeldig token geeft 404.
// Controleren (MSG-07, MSG-08, MSG-09):
//   curl -s -o /dev/null -w "%{http_code}" -X POST -d "List-Unsubscribe=One-Click" <adres uit een testbericht>
//     geeft 200 zonder cookie; daarna staat het testadres op de afmeldlijst (query)
//   curl -s <afmeldlink> (GET) verandert de afmeldlijst niet (query voor en na)
//   een POST met een gewijzigd token geeft 404 en wijzigt niets
// Gevalideerd op 04-10-2026 in een wegwerpcontainer: tsc --noEmit (strikt, TypeScript 6.0.3, met
//   allowImportingTsExtensions) is groen. Niet gedraaid met een draaiende Fastify.
import formbody from '@fastify/formbody';
import type { FastifyInstance } from 'fastify';
import type pg from 'pg';
import { z } from 'zod';
import { leesAfmeldToken } from './afmelden.ts';

const Params = z.strictObject({ token: z.string().min(1).max(200) });

export async function afmeldRoutes(app: FastifyInstance, opties: { pool: pg.Pool; geheim: Buffer }): Promise<void> {
  await app.register(formbody);

  // GET: alleen een pagina met een knop. Een mailscanner die de link volgt meldt niemand af (MSG-08).
  app.get('/afmelden/:token', (req, reply) => {
    const { token } = Params.parse(req.params);
    if (leesAfmeldToken(opties.geheim, token) === null) {
      return reply.status(404).type('text/html; charset=utf-8').send('<!doctype html><title>Niet gevonden</title><p>Deze link is niet geldig.</p>');
    }
    // Het token bestaat alleen uit UUID-tekens, punten en base64url en is hierboven gecontroleerd; er komt
    // geen andere invoer in de pagina.
    return reply
      .header('Cache-Control', 'no-store')
      .header('Referrer-Policy', 'no-referrer') // een geheim in het pad (WEB-19)
      .type('text/html; charset=utf-8')
      .send(`<!doctype html>
<html lang="nl">
<head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Afmelden</title></head>
<body>
<h1>Afmelden</h1>
<form method="post" action="/afmelden/${token}">
<button type="submit">Ja, meld mij af</button>
</form>
</body>
</html>`);
  });

  // POST: de afmelding zelf, ook voor de one-click van de mailclient (body: List-Unsubscribe=One-Click).
  app.post('/afmelden/:token', async (req, reply) => {
    const { token } = Params.parse(req.params);
    const gelezen = leesAfmeldToken(opties.geheim, token);
    if (gelezen === null) {
      return reply.status(404).send();
    }
    // Direct verwerken (MSG-10), idempotent: een tweede POST doet niets. Geen controle of de ontvanger
    // bestaat: het antwoord is voor iedereen gelijk (MSG-09).
    await opties.pool.query(
      'insert into afmeldingen (ontvanger_id, lijst_id) values ($1, $2) on conflict (ontvanger_id, lijst_id) do nothing',
      [gelezen.ontvangerId, gelezen.lijstId],
    );
    req.log.info({ event: 'afmelding' }, 'afgemeld');
    return reply.status(200).type('text/plain; charset=utf-8').send('Je bent afgemeld.');
  });
}
