// Sjabloon: Fastify-skelet met validatie aan elke rand, foutafhandeling zonder details, rate limit, twee
//   health-adressen en netjes afsluiten.
// Dekt: API-10, API-11, API-12, API-13, API-18, API-19, API-20, API-22, API-66, API-74, ARCH-09, ARCH-17,
//       ARCH-58 (de velden die de logger zelf levert), ARCH-60, ARCH-62, ARCH-67, WEB-51, WEB-62, API-05
// Dekt gedeeltelijk:
//   - API-20: @fastify/rate-limit telt standaard in het geheugen van een proces; bij meer dan een proces of na
//     een herstart telt het niet door, dan is Redis of een tabel nodig. De limieten zelf komen uit env.ts.
//   - AUTH: de sessiecontrole in vereisSessie is een lege plek die gesloten faalt; zie de AUTH-regels.
//   - ARCH-58: route, methode, status en duur logt Fastify per verzoek; tenant_id en user_id voeg je toe waar
//     de sessie bekend is.
// Aanpassen: de routes, de sessiecontrole, de query in /health/ready (met de runtime-rol, ARCH-67).
// Getallen: requestTimeout 120 seconden is het voorbeeld uit de documentatie (API-19); bodyLimit is de
//   standaard van 1 MiB, gelijk aan client_max_body_size in nginx (API-18); 10 seconden afsluittijd is de
//   standaard van close-with-grace uit ARCH-17 en moet korter zijn dan TimeoutStopSec van de unit.
// Controleren:
//   een onverwachte fout geeft 500 met alleen de algemene titel en het req_id (API-10)
//   N+1 verzoeken binnen het venster geven 429 met Retry-After (API-20, API-22)
//   dezelfde body met Content-Type text/plain geeft 415 of 400, nooit 200 (API-05)
//   een traag verzoek, dan SIGTERM: het verzoek krijgt antwoord en het proces stopt met code 0 (ARCH-17)
// Gevalideerd op 04-10-2026 in een wegwerpcontainer: tsc --noEmit met de tsconfig uit 07-typescript-tests
//   (TypeScript 6.0.3) en eslint --max-warnings 0 met eslint.config.mjs (typescript-eslint 8.71.0), beide groen.
//   Niet gedraaid als dienst.
import rateLimit from '@fastify/rate-limit';
import Fastify, { type FastifyReply, type FastifyRequest } from 'fastify';
import { randomUUID } from 'node:crypto';
import { ZodError } from 'zod';
import { pool } from './db.js';
import { env } from './env.js';
import { ALGEMEEN, AppError, type Problem } from './fouten.js';
import { bestellenRoutes } from './routes/bestellen.js';
import { mollieWebhookRoutes } from './routes/mollie-webhook.js';

const app = Fastify({
  bodyLimit: 1_048_576,
  requestTimeout: 120_000,
  trustProxy: env.PROXY_ADRES, // alleen de eigen proxy, nooit blind true (WEB-51)
  requestIdHeader: false, // geen id overnemen van de client (ARCH-60)
  genReqId: () => randomUUID(),
  logger: {
    // Geen geheimen in het log (API-66). Log nooit een hele body of een heel object (ARCH-62).
    redact: ['req.headers.authorization', 'req.headers.cookie', 'req.headers["x-mollie-signature"]', '*.password', '*.token'],
    base: { app: 'voorbeeld-api', release: env.RELEASE },
  },
});

function probleem(status: number, reqId: string): Problem {
  return { type: 'about:blank', title: ALGEMEEN[status] ?? 'Er ging iets mis', status, code: `http_${String(status)}`, req_id: reqId };
}

// Een eigen error handler: Fastify stuurt anders de foutmelding letterlijk door (API-10).
app.setErrorHandler((err: unknown, req: FastifyRequest, reply: FastifyReply) => {
  void reply.type('application/problem+json');
  if (err instanceof AppError) {
    return reply.status(err.status).send(err.toProblem(req.id));
  }
  if (err instanceof ZodError) {
    req.log.info({ event: 'input_validation_fail' }, 'ongeldige invoer');
    return reply.status(400).send(probleem(400, req.id));
  }
  const status = typeof err === 'object' && err !== null && 'statusCode' in err ? Number(err.statusCode) : 500;
  if (status >= 400 && status < 500) {
    return reply.status(status).send(probleem(status, req.id));
  }
  req.log.error({ err, event: 'sys_unexpected_error' }, 'onverwachte fout');
  return reply.status(500).send(probleem(500, req.id));
});

app.setNotFoundHandler((req, reply) => reply.status(404).type('application/problem+json').send(probleem(404, req.id)));

// Limiet op elke publieke route; strengere grenzen per route in de route zelf (API-20). De plugin antwoordt
// met 429 en Retry-After (API-22).
await app.register(rateLimit, { max: env.RATE_LIMIT_ALGEMEEN_PER_MINUUT, timeWindow: '1 minute' });

// Leeft het proces: geen afhankelijkheden, voor het herstartbeleid (ARCH-67).
app.get('/health/live', { config: { rateLimit: false } }, () => ({ status: 'ok' }));

// Kan het werken: een query met de runtime-rol, voor de uitrol en de bewaking (ARCH-67). Meldt het release-id
// (ARCH-09). Alleen intern bereikbaar maken, of zonder details laten.
app.get('/health/ready', { config: { rateLimit: false } }, async () => {
  await pool.query('select 1');
  return { status: 'ok', version: env.RELEASE };
});

await app.register(bestellenRoutes);
await app.register(mollieWebhookRoutes);

// Niet onderdrukken: loggen, afsluiten, en de procesmanager laten herstarten (API-13).
process.on('unhandledRejection', (reden) => {
  app.log.fatal({ err: reden, event: 'sys_crash' }, 'onafgehandelde fout');
  process.exit(1);
});
process.on('uncaughtException', (fout) => {
  app.log.fatal({ err: fout, event: 'sys_crash' }, 'onafgehandelde fout');
  process.exit(1);
});

// Netjes afsluiten, met een eigen uiterste tijd die korter is dan het geduld van de procesmanager (ARCH-17).
const AFSLUIT_MS = 10_000;
for (const signaal of ['SIGTERM', 'SIGINT'] as const) {
  process.once(signaal, () => {
    app.log.info({ event: 'sys_shutdown' }, 'afsluiten');
    const nood = setTimeout(() => process.exit(1), AFSLUIT_MS);
    nood.unref();
    app
      .close()
      .then(() => pool.end())
      .then(() => process.exit(0))
      .catch(() => process.exit(1));
  });
}

await app.listen({ host: env.HOST, port: env.PORT });
app.log.info({ event: 'sys_startup', release: env.RELEASE }, 'gestart'); // de eerste logregel meldt de release (ARCH-09)
