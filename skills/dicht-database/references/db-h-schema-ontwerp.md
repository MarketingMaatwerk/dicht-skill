# DB H: schema-ontwerp

Compacte regels van `dicht-database`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/database.md` (regelnummer in `regel-index.tsv`).

### DB-74 Tijdstippen zijn timestamptz
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Sla elk tijdstip op als `timestamptz` en gebruik `timestamp` zonder tijdzone alleen voor een kalendermoment zonder zone (met commentaar waarom).
- Bewijs: `SELECT table_name, column_name FROM information_schema.columns WHERE data_type = 'timestamp without time zone' AND table_schema = 'public';` is leeg of elke rij is toegelicht. In Drizzle: `timestamp('...', { withTimezone: true })`.
- Norm: Geen ASVS-eis; correctheid.
- Zie ook: ARCH-12, INFRA-71, BIZ-26, BIZ-27, BIZ-28, BIZ-29, SCR-40, SCR-52

### DB-75 Geld is numeric of een geheel aantal centen
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Sla bedragen op als `numeric(p,s)` of als geheel aantal centen in `bigint`, met de valuta in een eigen kolom, en gebruik nooit `real`, `double precision` of het type `money`.
- Bewijs: `SELECT table_name, column_name, data_type FROM information_schema.columns WHERE data_type IN ('real','double precision','money') AND table_schema = 'public';` bevat geen bedragkolommen. Afgevinkt als dat zo is en er een test is die 0,1 + 0,2 op het rekenpad controleert.
- Norm: ASVS 5.0.0 2.3.2 (L2); L3 voor betaling volgens besluit 6.
- Zie ook: API-28, API-27, BIZ-10, BIZ-11, BIZ-12, BIZ-17

### DB-76 Kies sleutels bewust: wat naar buiten gaat is niet raadbaar en verraadt niets
middel · richtlijn · api | app | mcp | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Gebruik voor identifiers die in URL's, API's of exports verschijnen een UUID versie 4 (`gen_random_uuid()`), en gebruik UUID versie 7 of `bigint identity` alleen voor interne sleutels of waar het lekken van aanmaaktijd en volgorde geen bezwaar is. De functie `uuidv7()` bestaat pas vanaf PostgreSQL 18: op PostgreSQL 16 en 17 gebruik je voor interne sleutels `bigint identity`.
- Bewijs: Review van routes en API-schema's op het type van elk id dat naar buiten gaat. Op PostgreSQL 16 en 17: `grep -rn "uuidv7()" <migraties>` is leeg. Afgevinkt als externe id's UUID versie 4 zijn of de afwijking is toegelicht, en de autorisatietest uit domein AUTH bestaat.
- Norm: ASVS 5.0.0 8.2.2 (L1); OWASP API Security Top 10 2023 API1.

### DB-77 Volg voor types en namen de skill postgresql-table-design
laag · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `text` (met `CHECK` voor een lengtegrens) in plaats van `char(n)` of `varchar(n)`, `generated always as identity` in plaats van `serial`, namen in kleine letters met underscores, en `NOT IN` niet met een subquery.
- Bewijs: Lint op het schema of review; `grep -rn "NOT IN (" src/ drizzle/`. Afgevinkt als nieuwe tabellen de conventies volgen.
- Norm: Geen; correctheid en onderhoud.

### DB-78 Soft delete is een bewuste keuze met een einddatum
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `deleted_at` alleen waar herstel door de gebruiker nodig is, neem `deleted_at IS NULL` op in de policy of in een view zodat het filter niet vergeten kan worden, pas unieke indexen aan met `WHERE deleted_at IS NULL`, en verwijder zacht verwijderde rijen definitief na een vastgelegde termijn.
- Bewijs: Lijst van tabellen met `deleted_at`, per tabel de termijn en de opruimjob (DB-83); test dat een verwijderde rij niet terugkomt in lijst, zoekfunctie en export. Afgevinkt als beide bestaan.
- Norm: AVG artikel 5 lid 1 onder e en artikel 17; ASVS 5.0.0 14.2.7 (L3).
- Zie ook: PRIV-21, DB-83, DB-84, PRIV-24, PRIV-26, AI-70, PRIV-22

### DB-79 Elke database is UTF8
laag · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak databases aan met codering `UTF8` en gebruik nooit `SQL_ASCII`.
- Bewijs: `SELECT datname, pg_encoding_to_char(encoding) FROM pg_database;` toont overal `UTF8`.
- Norm: ASVS 5.0.0 1.2.4 (L1) indirect.
