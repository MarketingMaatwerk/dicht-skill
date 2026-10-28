---
name: dicht-api
description: Regels met bewijs voor backend-code en API-routes (validatie, login, sessies, tokens, JWT, OAuth, rollen, tenants, webhooks, betalingen met Mollie, geld en btw, prijzen, facturen, voorraad, quota, gelijktijdigheid). Niet voor query's en migraties (dicht-database).
---

# dicht-api: API, backend-code, authenticatie, autorisatie en bedrijfslogica

Sub-skill van `dicht`. Bevat drie domeinen: API (82 regels, tien thema's, bestanden `api-*.md`), AUTH (85 regels, elf thema's, bestanden `auth-*.md`) en BIZ (bedrijfslogica en gelijktijdigheid, 52 regels, acht thema's, bestanden `biz-*.md`; batch 4). BIZ bouwt voort op API-27 tot en met API-45 en zegt welk middel bij welk soort bedrijfsregel hoort; een taak met geld, voorraad, tellers of termijnen laadt het thema uit `biz-*.md` naast het thema uit `api-*.md`. Norm: OWASP API Security Top 10 2023, ASVS 5.0.0 (V2, V6 tot en met V11, V15), NIST SP 800-63B, RFC 9700. Kritieke delen (betaling, login, tenant-isolatie) volgen niveau 3.

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/auth-a-wachtwoorden.md` | AUTH-01 t/m AUTH-09 (9 actief) | Wachtwoorden |
| `references/auth-b-inloggen-brute-force-en-enumeratie.md` | AUTH-10 t/m AUTH-15 (6 actief) | Inloggen, brute force en enumeratie |
| `references/auth-c-mfa-en-passkeys.md` | AUTH-16 t/m AUTH-24 (9 actief) | MFA en passkeys |
| `references/auth-d-wachtwoordreset-e-mailverificatie-en-magic-links.md` | AUTH-25 t/m AUTH-31 (6 actief) | Wachtwoordreset, e-mailverificatie en magic links |
| `references/auth-e-sessies.md` | AUTH-32 t/m AUTH-38 (7 actief) | Sessies |
| `references/auth-f-jwt-en-andere-zelfstandige-tokens.md` | AUTH-39 t/m AUTH-43 (5 actief) | JWT en andere zelfstandige tokens |
| `references/auth-g-oauth-2-0-en-openid-connect.md` | AUTH-44 t/m AUTH-52 (9 actief) | OAuth 2.0 en OpenID Connect |
| `references/auth-h-api-sleutels-service-tokens-en-webhooks.md` | AUTH-53 t/m AUTH-61 (8 actief) | API-sleutels, service-tokens en webhooks |
| `references/auth-i-autorisatie-per-functie-object-en-veld.md` | AUTH-62 t/m AUTH-71 (9 actief) | Autorisatie per functie, object en veld |
| `references/auth-j-multi-tenant-isolatie.md` | AUTH-72 t/m AUTH-78 (5 actief) | Multi-tenant isolatie |
| `references/auth-k-beheerders-impersonatie-support-en-audit.md` | AUTH-79 t/m AUTH-85 (7 actief) | Beheerders, impersonatie, support en audit |
| `references/api-a-invoer-en-schema-s.md` | API-01 t/m API-08 (8 actief) | invoer en schema's |
| `references/api-b-uitvoer-en-foutmodel.md` | API-09 t/m API-16 (5 actief) | uitvoer en foutmodel |
| `references/api-c-limieten-paginering-en-resourceverbruik.md` | API-17 t/m API-26 (8 actief) | limieten, paginering en resourceverbruik |
| `references/api-d-bedrijfslogica-races-en-idempotentie.md` | API-27 t/m API-35 (9 actief) | bedrijfslogica, races en idempotentie |
| `references/api-e-betaalstromen-met-mollie.md` | API-36 t/m API-45, API-82 (11 actief) | betaalstromen met Mollie |
| `references/api-f-webhooks-en-externe-aanroepen.md` | API-46 t/m API-51 (5 actief) | webhooks en externe aanroepen |
| `references/api-g-injectie-en-gevaarlijke-functies.md` | API-52 t/m API-60 (8 actief) | injectie en gevaarlijke functies |
| `references/api-h-cryptografie-en-geheimen-in-code.md` | API-61 t/m API-66 (5 actief) | cryptografie en geheimen in code |
| `references/api-i-typescript-en-node.md` | API-67 t/m API-74 (7 actief) | TypeScript en Node |
| `references/api-j-php.md` | API-75 t/m API-81 (6 actief) | PHP |
| `references/biz-a-vergrendelen-en-isolatie.md` | BIZ-01 t/m BIZ-09 (9 actief) | vergrendelen en isolatie |
| `references/biz-b-geld-btw-en-afronding.md` | BIZ-10 t/m BIZ-19 (10 actief) | geld, btw en afronding |
| `references/biz-c-voorraad-quota-en-plafonds.md` | BIZ-20 t/m BIZ-23 (4 actief) | voorraad, quota en plafonds |
| `references/biz-d-toestanden-tijd-en-datums.md` | BIZ-24 t/m BIZ-31 (8 actief) | toestanden, tijd en datums |
| `references/biz-e-misbruik-van-stromen.md` | BIZ-32 t/m BIZ-38 (7 actief) | misbruik van stromen |
| `references/biz-f-herhaling-achtergrondtaken-en-hulpmiddelen.md` | BIZ-39 t/m BIZ-45 (7 actief) | herhaling, achtergrondtaken en hulpmiddelen |
| `references/biz-g-afstemming-tussen-systemen.md` | BIZ-46 t/m BIZ-49 (4 actief) | afstemming tussen systemen |
| `references/biz-h-tests-voor-grenzen-tijd-en-gelijktijdigheid.md` | BIZ-50 t/m BIZ-52 (3 actief) | tests voor grenzen, tijd en gelijktijdigheid |

## Wanneer niet

- De databasekant van transacties, RLS en SQL: `dicht-database`. API-52 is samengevoegd met DB-25 tot en met DB-27.
- Overlappende cronruns, sloten in scripts en verzendlijnen als script: `dicht-scripts`. Limieten op uitgaande mail en het 24-uursvenster: `dicht-berichten`.
- Bedragen, datums en ID's ontleden uit CSV of andere invoer: `dicht-invoer`.
- SSRF in detail, uploads, caching en headers: `dicht-web`.
- WordPress-handlers (nonce, capability, REST-route): `dicht-wordpress`. AUTH-71 is daarmee samengevoegd.
- MCP-tokens en tool-rechten: `dicht-ai-mcp`.
- Wachtrijen, herhalen, afsluiten en logformaat als architectuur: `dicht-architectuur`.

## Verhouding tot bestaande skills

`api-security-best-practices`, `nodejs-backend-patterns`, `owasp-security`, `cc-skill-security-review` en `typescript-advanced-types` blijven bruikbaar voor voorbeeldcode. Niet overnemen, deze regels gaan voor:
- `owasp-security` (regel 243 tot 247): wachtwoordschema met 8 tekens plus verplichte hoofdletter, cijfer en speciaal teken. In strijd met AUTH-01 en AUTH-02.
- `owasp-security` (regel 84 tot 97) en `api-security-best-practices` (regel 463): bcrypt als eerste keuze. Zie AUTH-04 en AUTH-05.
- `owasp-security` (regel 331 tot 344) en `api-security-best-practices` (regel 135 tot 153): JWT als sessie met een refresh token van 7 dagen zonder rotatie of intrekking, en `jwt.verify` zonder algoritmelijst. Zie AUTH-33, AUTH-36, AUTH-39 en AUTH-50.
- `cc-skill-security-review` (regel 155 tot 170): autorisatie op `role !== 'admin'` zonder tenant. Zie AUTH-73.
- `api-security-best-practices` gebruikt `express-rate-limit` en Helmet; de stack is Fastify (`@fastify/rate-limit`, `@fastify/helmet`).
- `nodejs-backend-patterns` mist de Fastify-standaarden (API-04, API-10, API-19, API-21) en bevat MongoDB-voorbeelden die niet bij de stack horen.
- `owasp-security` is gebaseerd op de OWASP Top 10 2021.
- Geen van de vier dekt Mollie-webhooks (thema API-E), races en idempotentie (thema API-D) of PHP type juggling (API-75).
