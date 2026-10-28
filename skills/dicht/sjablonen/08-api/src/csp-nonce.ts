// Sjabloon: strikte CSP met een nonce per respons, voor HTML die de applicatie zelf rendert.
// Dekt: WEB-11, WEB-12, WEB-13, WEB-15, WEB-24
// Dekt gedeeltelijk: WEB-14 (eerst report-only, met een meldpunt) staat hier niet; zet het beleid eerst als
//   Content-Security-Policy-Report-Only en schakel daarna om.
// Het beleid is letterlijk het strikte beleid uit WEB-11: script-src met nonce en strict-dynamic, met https: en
//   'unsafe-inline' als terugval die browsers met strict-dynamic negeren; object-src en base-uri op 'none'.
// De nonce komt uit @fastify/helmet met enableCSPNonces (WEB-12): reply.cspNonce.script en reply.cspNonce.style.
// Aanpassen: style-src. Het onderzoek noemt geen waarde voor style-src; 'self' hieronder is een eigen invulling.
//   Controleer in de header wat helmet er precies van maakt.
// Naast het beleid uit nginx (01-nginx/snippets/security-headers.conf): een browser past beide toe.
// Een HTML-respons met een nonce komt nooit in een gedeelde cache (WEB-12): no-store.
// Controleren (WEB-11, WEB-12):
//   curl -sI https://<host>/ | grep -i content-security-policy
//   twee keer curl -s https://<host>/ | grep -o "nonce-[A-Za-z0-9+/=]*" geeft twee verschillende waarden van
//     minstens 22 tekens
//   de pagina werkt in een Playwright-test zonder CSP-fouten in de console
// Gevalideerd op 04-10-2026 in een wegwerpcontainer: tsc --noEmit met de tsconfig uit 07-typescript-tests
//   (TypeScript 6.0.3) en eslint --max-warnings 0 met eslint.config.mjs (typescript-eslint 8.71.0), beide groen.
//   Niet gedraaid als dienst.
import helmet from '@fastify/helmet';
import type { FastifyInstance } from 'fastify';

export async function cspMetNonce(app: FastifyInstance): Promise<void> {
  await app.register(helmet, {
    enableCSPNonces: true,
    contentSecurityPolicy: {
      useDefaults: false,
      directives: {
        'script-src': ["'strict-dynamic'", 'https:', "'unsafe-inline'"], // helmet voegt de nonce toe
        'style-src': ["'self'"],
        'object-src': ["'none'"],
        'base-uri': ["'none'"],
        'frame-ancestors': ["'none'"],
      },
    },
  });

  app.get('/', (_req, reply) => {
    const nonce = reply.cspNonce.script;
    void reply.header('Cache-Control', 'no-store').type('text/html; charset=utf-8');
    // Geen inline handlers (WEB-13); elk script-element krijgt de nonce.
    return `<!doctype html>
<html lang="nl">
<head><meta charset="utf-8"><title>Voorbeeld</title></head>
<body>
<h1>Voorbeeld</h1>
<script nonce="${nonce}" src="/assets/app.js"></script>
</body>
</html>`;
  });
}
