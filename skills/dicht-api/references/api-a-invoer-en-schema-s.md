# API A: invoer en schema's

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/api-code.md` (regelnummer in `regel-index.tsv`).

### API-01 Schema-validatie aan elke rand
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Valideer elke invoer die het proces binnenkomt (body, query, params, headers die je gebruikt, webhook-payload, antwoord van een externe API, wachtrijbericht, omgevingsvariabelen bij de start) met een schema voordat de code er iets mee doet. Aanvulling uit WEB-60: Ook cookies en bestandsmetadata; het schema legt type, lengte, bereik en toegestane waarden vast en weigert wat niet past; validatie in de browser is alleen gemak.
- Bewijs: Elke route heeft een schema voor body, query en params (Fastify `schema` of een zod-parse als eerste regel). Controle: `grep -rn "req.body\|request.body\|request.query\|request.params" src` levert geen gebruik op buiten een parse. Een test per route stuurt een verkeerd type en verwacht 400.
    Ook (uit WEB-60): Elke route heeft een schema (Fastify: `schema` of zod bij de route; WordPress: `sanitize_*` plus een eigen controle, REST: `args` met `validate_callback`); een test per route met een te lang veld, een verkeerd type en een extra veld geeft 400. Afgevinkt met de routelijst en de testuitvoer. De uitwerking (zod, strikte objecten, mass assignment) staat in API.
- Norm: ASVS 5.0.0 V2.2.1 (L1, vanaf L2 voor alle invoer), V2.2.2 (L1); OWASP API Top 10 2023 API8 en API10.
- Dekt ook: WEB-60
- Zie ook: AI-11, AI-23, API-50, WP-13, ARCH-07

### API-02 Weiger onbekende velden en bind nooit de hele body
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik strikte objecten (`z.strictObject` of `additionalProperties: false`) en geef nooit het request-object zelf door aan `insert`, `update` of `set`; noem elk veld dat geschreven mag worden.
- Bewijs: `grep -rnE "\.set\((req|request)\.|\.values\((req|request)\." src` is leeg. Test: een PATCH met een extra veld `role` geeft 400 en wijzigt niets.
- Norm: ASVS 5.0.0 V15.3.3 (L2); OWASP API Top 10 2023 API3.
- Zie ook: AUTH-65, INV-47, INV-46, WP-32, INV-13

### API-03 Geef elk veld een grens
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke string een maximale lengte, op elke array een maximaal aantal items, op elk getal een bereik, en op elke vrije sleutel-waarde-structuur een maximum aan sleutels.
- Bewijs: Lint- of reviewcontrole: geen `z.string()` zonder `.max()` of formaat, geen `z.array()` zonder `.max()`. Test per route met een te lange waarde verwacht 400.
- Norm: ASVS 5.0.0 V2.2.1 (L1), V1.3.3 (L2); OWASP API Top 10 2023 API4.

### API-04 Ken de Ajv-standaarden van Fastify en laat `allErrors` uit
middel · hard · api | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat `allErrors` op `false` staan en houd er rekening mee dat Fastify invoer aanpast: `coerceTypes: 'array'`, `useDefaults: true` en `removeAdditional: true` zijn de standaard.
- Bewijs: `grep -rn "allErrors" src` is leeg of `false`. Elk body-schema heeft `additionalProperties: false`. Wie zod gebruikt in de handler in plaats van het Fastify-schema: zie API-08 voor de keuze.
- Norm: ASVS 5.0.0 V2.2.1 (L1); OWASP API Top 10 2023 API4 en API8.

### API-05 Accepteer alleen de content-types die je verwacht
hoog · hard · api | mcp · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Registreer alleen de content-type-parsers die een route nodig heeft, weiger de rest met 415, en houd Fastify op de laatste 5.x.
- Bewijs: `npm ls fastify` toont 5.12.5 of hoger (de ondergrens van INV-15: na CVE-2025-32442, gerepareerd in 5.3.2, volgden in 2026 nog vijf advisories over de body-validatie, de laatste gerepareerd in 5.12.5; op 04-10-2026 is 5.12.5 ook de laatste versie). Test: dezelfde ongeldige body met `Content-Type: Application/JSON` en met `text/plain` geeft 400 of 415, nooit 200.
- Norm: ASVS 5.0.0 V2.2.1 (L1); OWASP API Top 10 2023 API8.
- Zie ook: INV-15, WEB-31

### API-06 Valideer betekenis en samenhang, niet alleen vorm
hoog · hard · api | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer na de vormvalidatie de combinaties: hoort deze optie bij dit pakket, ligt de einddatum na de begindatum, past de kortingscode bij dit product en deze klant.
- Bewijs: Per flow een test met een op zichzelf geldige maar onderling onmogelijke combinatie; verwacht 400 of 422. De regels staan beschreven bij het schema (commentaar of documentatie).
- Norm: ASVS 5.0.0 V2.2.3 (L2), V2.1.2 (L2).

### API-07 Decodeer één keer, vóór de validatie
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Breng invoer één keer naar de canonieke vorm (URL-decoderen, Unicode-normalisatie, trimmen, kleine letters voor e-mail en domeinnaam) en valideer daarna; decodeer nooit opnieuw na de validatie. Aanvulling uit WEB-61: Normaliseer ook paden.
- Bewijs: `grep -rn "decodeURIComponent\|urldecode\|rawurldecode" src` toont alleen aanroepen vóór de schema-parse. Test met dubbel gecodeerde invoer.
    Ook (uit WEB-61): `grep -rnE "decodeURIComponent|urldecode|rawurldecode|html_entity_decode|stripslashes" src/` en per resultaat aangetoond dat het vóór de validatie en maar één keer gebeurt; een test met dubbel gecodeerde `../` wordt geweigerd. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V1.1.1 (L2); V1.5.3 (L3) voor consistente parsers.
- Dekt ook: WEB-61
- Zie ook: INV-51, INV-52, INV-53, INV-54, INV-57, INV-58

### API-08 Eén bron voor type en validatie
middel · richtlijn · api | app | mcp · tegenlezer: scherpen (04-10-2026)
- Regel: Leid het TypeScript-type af uit het schema (`z.infer`) en schrijf nooit een los interface naast een schema; kies per project één plek voor validatie (Fastify-schema of zod in de handler) en houd je eraan.
- Bewijs: `grep -rnE "as [A-Z][A-Za-z]+(\[\])?[;,)]" src` op regels met `req.` of `JSON.parse` is leeg. Elk request-type is een `z.infer`.
- Norm: ASVS 5.0.0 V15.3.5 (L2).
