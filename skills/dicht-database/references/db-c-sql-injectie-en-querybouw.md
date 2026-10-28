# DB C: SQL-injectie en querybouw

Compacte regels van `dicht-database`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/database.md` (regelnummer in `regel-index.tsv`).

### DB-25 Alleen geparametriseerde queries
kritiek · hard · alles · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Geef elke waarde die niet letterlijk in de broncode staat als parameter mee (Drizzle query builder, de `sql`-template van Drizzle, of de tagged template van postgres.js) en bouw nooit SQL met stringconcatenatie of gewone template strings.
- Bewijs: Semgrep- of ESLint-regel die stringconcatenatie en template strings in `execute`, `query`, `unsafe` en `raw` afkeurt, als CI-gate. Afgevinkt als de gate groen is en er een test bestaat die een aanhalingsteken in elk zoekveld stuurt.
    Ook (uit API-52): `grep -rn "sql.raw\|\.unsafe(" src` is leeg of elke treffer bevat alleen constanten. Semgrep-regel op string-samenvoeging in queries. In PHP: `grep -rnE "(query|get_results|get_var)\(\s*\"[^\"]*\\$"`; zie WP voor `$wpdb->prepare`.
- Norm: ASVS 5.0.0 1.2.4 (L1); OWASP Top 10 2025 A05 Injection (in de uitgave 2021: A03).
- Dekt ook: API-52
- Zie ook: DB-26, DB-27, WP-16, WP-18, WP-19, DB-28, SCR-11, SCR-30, INV-63

### DB-26 sql.raw en sql.unsafe nooit met invoer
kritiek · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Gebruik `sql.raw()` (Drizzle) en `sql.unsafe()` (postgres.js) alleen met tekst die volledig uit constanten in de code bestaat, en zet bij elk gebruik een commentaar met de reden.
- Bewijs: `grep -rnE "sql\.raw\(|\.unsafe\(" src/` met per treffer een beoordeling; lintregel die een variabele als argument afkeurt. Afgevinkt als elke treffer alleen constanten bevat en de reden erbij staat.
- Norm: ASVS 5.0.0 1.2.4 (L1); OWASP Top 10 2025 A05 Injection (in de uitgave 2021: A03).
- Zie ook: DB-25, DB-27, WP-16, WP-18, WP-19, DB-28, SCR-11, SCR-30, INV-63

### DB-27 Tabelnamen, kolomnamen en sorteerrichting via een allowlist
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Vertaal elke door de gebruiker gekozen kolom, tabel of sorteerrichting via een vaste tabel in de code naar een Drizzle-kolomobject of een constante, en geef invoer nooit door aan `sql.identifier()`, `.as()` of een identifier-helper.
- Bewijs: `grep -rnE "sql\.identifier\(|\.as\(" src/` met beoordeling; test die een onbekende sorteerkolom stuurt en de standaard terugkrijgt. Afgevinkt als geen treffer invoer bevat en de test slaagt.
- Norm: ASVS 5.0.0 1.2.4 (L1).
- Zie ook: DB-25, DB-26, WP-16, WP-18, WP-19, DB-28, SCR-11, SCR-30, INV-63

### DB-28 Geen dynamische SQL in databasefuncties
hoog · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf databasefuncties met statische SQL en parameters; vermijd `EXECUTE` met samengestelde tekst.
- Bewijs: `SELECT proname FROM pg_proc WHERE prosrc ~* '\mexecute\M' AND pronamespace NOT IN ('pg_catalog'::regnamespace, 'information_schema'::regnamespace);` met beoordeling per treffer. Afgevinkt als de lijst leeg is of elke treffer is beoordeeld.
- Norm: ASVS 5.0.0 1.2.4 (L1).
- Zie ook: DB-25, DB-26, DB-27, WP-16, WP-18, WP-19, SCR-11, SCR-30, INV-63

### DB-29 Draai drizzle-orm 0.45.2 of hoger
hoog · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Gebruik in elk nieuw project `drizzle-orm` 0.45.2 of hoger (of 1.0.0-beta.20 of hoger) en plan voor bestaande projecten de upgrade in.
- Bewijs: `npm ls drizzle-orm` per dienst en de dependency-audit in CI (zie domein GIT). Afgevinkt als elke kopie 0.45.2 of hoger is, of als een vastgelegde uitzondering met DB-27 als compenserende maatregel bestaat.
- Norm: ASVS 5.0.0 15.2.1 (L1) en 15.1.1 (L1); OWASP Top 10 2025 A03 Software Supply Chain Failures (in de uitgave 2021: A06).
