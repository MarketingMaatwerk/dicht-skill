---
name: dicht-web
description: Regels met bewijs voor alles wat een browser raakt (XSS en output-encoding, CSP en headers, cookies, CSRF, CORS, redirects en SSRF, uploads, formulieren, caching, scripts van derden). Niet voor WordPress-functies (dicht-wordpress) of inloggen (dicht-api).
---

# dicht-web: browser en webapplicatie

Sub-skill van `dicht`. Bevat de 74 regels van domein WEB in dertien thema's. Norm: OWASP ASVS 5.0.0 (hoofdstukken V1 tot en met V5 en V14) en de OWASP Cheat Sheet Series.

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/web-1-output-encoding-en-xss.md` | WEB-01 t/m WEB-10 (9 actief) | Output-encoding en XSS |
| `references/web-2-content-security-policy.md` | WEB-11 t/m WEB-16 (6 actief) | Content Security Policy |
| `references/web-3-security-headers.md` | WEB-17 t/m WEB-24 (8 actief) | Security headers |
| `references/web-4-cookies-en-clientside-opslag.md` | WEB-25 t/m WEB-28 (4 actief) | Cookies en clientside opslag |
| `references/web-5-csrf-en-cors.md` | WEB-29 t/m WEB-35 (7 actief) | CSRF en CORS |
| `references/web-6-framing-berichten-en-vensters.md` | WEB-36 t/m WEB-38 (3 actief) | Framing, berichten en vensters |
| `references/web-7-redirects-en-server-side-aanvragen.md` | WEB-39 t/m WEB-42 (4 actief) | Redirects en server-side aanvragen |
| `references/web-8-bestandsupload-en-download.md` | WEB-43 t/m WEB-49 (7 actief) | Bestandsupload en -download |
| `references/web-9-http-laag-proxy-en-caching.md` | WEB-50 t/m WEB-57 (8 actief) | HTTP-laag, proxy en caching |
| `references/web-10-scripts-en-bronnen-van-derden.md` | WEB-58 t/m WEB-59 (2 actief) | Scripts en bronnen van derden |
| `references/web-11-invoer-fouten-en-blootstelling.md` | WEB-60 t/m WEB-65 (2 actief) | Invoer, fouten en blootstelling |
| `references/web-12-automatisering-formulieren-en-e-mail.md` | WEB-66 t/m WEB-70 (5 actief) | Automatisering, formulieren en e-mail |
| `references/web-13-indexatie-en-service-workers.md` | WEB-71 t/m WEB-74 (4 actief) | Indexatie en service workers |

## Wanneer niet

- WordPress-vertaling van escapen, nonces en `wp_kses`: `dicht-wordpress`.
- Inloggen, sessies, tokens en rechten: `dicht-api` (thema's AUTH).
- Schema-validatie, foutmodel, rate limiting in de applicatie: `dicht-api` (thema's API). De duplicaten uit WEB verwijzen daar al naar.
- TLS-instellingen, nginx-limieten en firewall: `dicht-infra`.
- Cookietoestemming en derden als ontvanger: `dicht-privacy`.
- Wat er na de upload met het bestand gebeurt (XML, CSV, afbeelding, PDF, archief, SVG, Markdown) en hoe je URL's en Unicode ontleedt: `dicht-invoer`. WEB-44 verwijst naar INV-33.
- Mail die een formulier of de applicatie verstuurt, voorbij de koppen (WEB-68, WEB-69): `dicht-berichten`.

## Verhouding tot bestaande skills

`owasp-security` blijft bruikbaar voor uitleg en voorbeeldcode, maar is op drie punten onjuist of verouderd. Daar gaan deze regels voor:
- De helmet-CSP daar gebruikt `'strict-dynamic'` zonder nonce of hash en `styleSrc 'unsafe-inline'`. Zonder nonce of hash is dat geen werkend beleid: WEB-11 en WEB-12.
- De SSRF-controle daar toetst de hostnaam met reguliere expressies en volgt redirects: WEB-40 en WEB-41.
- Hij mist `frame-ancestors` als opvolger van `X-Frame-Options`, cookie-prefixes, Fetch Metadata, cache-regels en upload-opslag: WEB-24, WEB-25, WEB-30, WEB-52 tot en met WEB-54, WEB-43 tot en met WEB-49.
Voor UI en prestaties: `ui-ux-pro-max` en `performance`; voor e2e-tests: `webapp-testing`.
