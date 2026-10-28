# API C: limieten, paginering en resourceverbruik

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/api-code.md` (regelnummer in `regel-index.tsv`).

### API-17 Pagineer elke lijst met een maximum dat de server bepaalt
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Geef op elke lijstroute een `limit` met een standaardwaarde en een harde bovengrens in het schema (bijvoorbeeld standaard 25, maximaal 100) en geef nooit een onbegrensde lijst terug.
- Bewijs: Elk lijstschema bevat `limit: z.coerce.number().int().min(1).max(100).default(25)`. Test: `limit=100000` geeft 400. `grep -rn "\.from(" src` in routes zonder `.limit(` wordt per treffer beoordeeld.
- Norm: OWASP API Top 10 2023 API4; ASVS 5.0.0 V2.4.1 (L2).

### API-18 Kies de body-limiet bewust en houd nginx gelijk
middel · hard · api | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat `bodyLimit` op de standaard van 1 MiB of lager, verhoog hem alleen per route waar dat nodig is, en zet `client_max_body_size` in nginx op dezelfde waarde.
- Bewijs: `grep -rn "bodyLimit" src` toont alleen route-specifieke verhogingen met een reden. `nginx -T | grep client_max_body_size` komt overeen. Test: een body van 2 MiB op een gewone route geeft 413.
- Norm: ASVS 5.0.0 V5.2.1 (L1); OWASP API Top 10 2023 API4.
- Zie ook: INFRA-45, WEB-43, API-19, ARCH-13, INV-44, INV-10, MSG-24

### API-19 Zet time-outs op de server; de standaard is geen time-out
hoog · hard · api | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai een Fastify-service altijd achter nginx, of zet `requestTimeout` op een waarde boven nul (de documentatie noemt 120 seconden als voorbeeld); zet daarnaast een time-out op elke databasequery en elke externe aanroep.
- Bewijs: De service luistert op `127.0.0.1` of een intern Docker-netwerk (`ss -ltnp`), niet rechtstreeks op een publiek adres, of `requestTimeout` staat ingesteld. In PostgreSQL staat `statement_timeout` voor de app-rol (zie DB).
- Norm: ASVS 5.0.0 V15.2.2 (L2), V13.1.3 (L3); OWASP API Top 10 2023 API4.
- Zie ook: INFRA-45, API-18, WEB-43, ARCH-13, INV-44, INV-10, MSG-24, API-48, API-49, ARCH-14, AI-76, DB-65, SCR-21, SCR-25, SCR-26, SCR-43, MSG-42

### API-20 Begrens verzoeken per route-klasse en per identiteit
hoog · hard · api | app | mcp | wp-plugin | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet rate limiting op elke publieke route, met strengere grenzen voor dure of gevoelige routes (inloggen, wachtwoordreset, bestellen, domeincheck, mail versturen, AI-aanroepen), en gebruik als sleutel het account of de API-sleutel waar die er is en anders het IP-adres.
- Bewijs: Test: N+1 verzoeken binnen het venster geven 429. Let op: `@fastify/rate-limit` gebruikt standaard een geheugenopslag per proces (standaard `max` 1000 per minuut); bij meer dan één proces of na een herstart telt het niet door, dan is Redis of een tabel nodig. Een eigen teller in het geheugen heeft dezelfde beperking.
- Norm: ASVS 5.0.0 V2.4.1 (L2); OWASP API Top 10 2023 API4 en API6.
- Zie ook: WEB-66, INFRA-46, API-22, AUTH-10, WP-57, AI-45, AI-74

### API-21 → WEB-51
Samengevoegd: "Vertrouw alleen je eigen proxy voor het client-adres" is gedekt door WEB-51. Gebruik die regel.

### API-22 Antwoord op een overschreden limiet met 429 en Retry-After
laag · richtlijn · api | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef bij een overschreden limiet status 429 met een `Retry-After`-header en een algemeen foutbericht.
- Bewijs: Test: het 429-antwoord bevat `retry-after`. De `RateLimit`-headers zijn nog een IETF-concept (draft-ietf-httpapi-ratelimit-headers-11, actief tot 24-11-2026) en dus optioneel.
- Norm: RFC 6585 sectie 4.
- Zie ook: API-20, WEB-66, INFRA-46, AUTH-10, WP-57, AI-45, AI-74

### API-23 Zet duur werk in een wachtrij en begrens het per gebruiker
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Voer werk dat langer duurt dan de time-out van de client of veel CPU, geheugen of externe aanroepen kost (export, import, mailmigratie, AI-aanroep, pdf) uit via een wachtrij met een maximum aan gelijktijdige taken per gebruiker en in totaal.
- Bewijs: De lijst van dure functies staat in de projectdocumentatie met per functie de limiet. Test: de (max+1)-ste gelijktijdige taak van dezelfde gebruiker wordt geweigerd of in de rij gezet.
- Norm: ASVS 5.0.0 V15.1.3 (L2), V15.2.2 (L2).
- Zie ook: ARCH-19, DB-71, ARCH-18, ARCH-20, BIZ-42

### API-24 GraphQL alleen met diepte- en kostengrens en zonder introspectie
hoog · hard · api · tegenlezer: bevestigd (04-10-2026)
- Regel: Kies REST tenzij er een onderbouwde reden is voor GraphQL; als je GraphQL gebruikt, zet dan een maximale diepte, een maximaal aantal velden of een kostenberekening, begrens batching, en zet introspectie uit in productie.
- Bewijs: Configuratie toont de limieten. Test: een query dieper dan het maximum en een introspectiequery worden geweigerd.
- Norm: ASVS 5.0.0 V4.3.1 (L2), V4.3.2 (L2).

### API-25 Houd een inventaris bij en zet niets in productie wat er niet hoort
hoog · hard · api | mcp | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg elke route vast (methode, pad, wie mag, limiet) en zorg dat testroutes, debugroutes, voorbeeldcode, oude versies en documentatie-endpoints in productie niet bereikbaar zijn.
- Bewijs: `app.printRoutes()` of de OpenAPI-uitvoer in CI wordt vergeleken met de vastgelegde lijst; een verschil laat de build falen. `grep -rnE "/debug|/test|/tmp" src` op routes is leeg. Docs-endpoint (`/docs`, `/documentation`) geeft 404 of vraagt om inloggen.
- Norm: OWASP API Top 10 2023 API9; ASVS 5.0.0 V13.4.5 (L2), V15.2.3 (L2), V4.1.4 (L3).
- Zie ook: WEB-64, API-81, ARCH-05, WP-63, WP-41, ARCH-83, AUTH-13, WP-62

### API-26 → ARCH-78, ARCH-79
Samengevoegd: "Versioneer een publieke API en faseer zichtbaar uit" is gedekt door ARCH-78, ARCH-79. Gebruik die regel.
