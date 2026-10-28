# DB J: auditing, monitoring en onderhoud

Compacte regels van `dicht-database`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/database.md` (regelnummer in `regel-index.tsv`).

### DB-89 Zet pg_stat_statements aan
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laad `pg_stat_statements` via `shared_preload_libraries` in elke productiedatabase en bekijk bij elke release de tien zwaarste queries op totale tijd.
- Bewijs: `SHOW shared_preload_libraries;` bevat `pg_stat_statements` en `SELECT count(*) FROM pg_stat_statements;` werkt. Afgevinkt als beide kloppen. Let op: laden vraagt een herstart van de database, dus plan het. De querytekst van andere gebruikers is alleen zichtbaar voor superusers en `pg_read_all_stats`.
- Norm: ASVS 5.0.0 15.1.3 (L2).

### DB-90 Log trage queries, lock-wachttijden en verbindingen
middel · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `log_min_duration_statement` op een drempel (richtwaarde 500 ms) met parameters uit (DB-88), `log_lock_waits = on`, en `log_connections` aan.
- Bewijs: `SHOW log_min_duration_statement; SHOW log_lock_waits; SHOW log_connections;`. Afgevinkt als ze zijn ingesteld en het log binnen de bewaartermijn van INFRA valt.
- Norm: ASVS 5.0.0 16.3.1 (L2), 16.2.1 (L2).

### DB-91 Audit van DDL en rolwijzigingen; volledige audit bij zorgdata
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Leg wijzigingen aan schema, rollen en rechten vast (minimaal `log_statement = 'ddl'`, of pgaudit met `pgaudit.log = 'ddl, role'`), en gebruik voor zorgdata of L3-onderdelen pgaudit met objectaudit op de gevoelige tabellen, met het log naar een plek waar de databasebeheerder het niet kan wijzigen.
- Bewijs: `SHOW log_statement;` of `SHOW pgaudit.log;` en een proef: maak een rol aan en vind de regel terug in het log. Afgevinkt als de proef slaagt. Beperkingen: pgaudit kan superusers niet betrouwbaar auditen, `pgaudit.log_parameter` kan gevoelige waarden loggen (laat uit), en het volume kan groot worden. De pgaudit-versie moet bij de major passen (16.x bij PostgreSQL 16, 18.x bij 18).
- Norm: ASVS 5.0.0 16.3.3 (L2), 16.4.2 en 16.4.3 (L2); NEN 7513 voor zorgdata (niet gelezen, zie Niet bevestigd).
- Zie ook: ARCH-64, AUTH-84, ARCH-65, INFRA-89, PRIV-54, AI-52

### DB-92 Draai de actuele minor van je major
hoog · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Werk elke PostgreSQL-server en elke `pg_dump`- en `psql`-client bij naar de actuele minor binnen 14 dagen na uitgave, en binnen 48 uur als de uitgave een kritieke of actief misbruikte kwetsbaarheid (CISA KEV) dicht die in jouw gebruik bereikbaar is, en binnen 7 dagen bij ernst hoog (besluit 22).
- Bewijs: `SELECT version();` per server naast de tabel op https://www.postgresql.org/support/versioning/. Afgevinkt als de minor gelijk is aan de actuele. Lees bij elke minor de release notes: 16.15 vraagt bijvoorbeeld om `output_plugin_libraries` te zetten bij logische decodering met eigen plugins en eventueel herindexeren bij `btree_gist` of `ltree`. De 14 dagen voor een gewone minor is een eigen keuze; de 48 uur en 7 dagen zijn besluit 22.
- Norm: ASVS 5.0.0 15.1.1 (L1: leg hersteltermijnen vast) en 15.2.1 (L1: geen componenten buiten die termijnen); OWASP Top 10 2025 A03 Software Supply Chain Failures (in de uitgave 2021: A06).
- Zie ook: GIT-77, INFRA-24, ARCH-32, WP-49, GIT-88, GIT-61, PRIV-73, MSG-06, SCR-32

### DB-93 Blijf op een ondersteunde major en plan de upgrade een jaar vooruit
middel · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Start nieuwe projecten op de nieuwste major die je extensies ondersteunen, en plan voor elke bestaande database de major upgrade ruim voor het einde van de ondersteuning.
- Bewijs: Tabel per database met major en einddatum. Afgevinkt als geen productiedatabase binnen 12 maanden van zijn einddatum zit zonder upgradeplan. De host-client 14.24 op de server valt op 12-11-2026 uit ondersteuning.
- Norm: OWASP Top 10 2025 A03 Software Supply Chain Failures (in de uitgave 2021: A06).
- Zie ook: GIT-93, API-72, WP-52, INFRA-22, INFRA-42, AI-54, SCR-33

### DB-94 Laat autovacuum aan en bewaak wat hem tegenhoudt
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet autovacuum nooit uit, en bewaak lange transacties, achtergebleven replication slots, voorbereide transacties en de leeftijd van transactie-id's.
- Bewijs: `SHOW autovacuum;` is `on`; `SELECT datname, age(datfrozenxid) FROM pg_database;` blijft ruim onder 2 miljard (alarm bij een eigen drempel, bijvoorbeeld 500 miljoen); `SELECT slot_name, active FROM pg_replication_slots;` toont geen inactieve slots; `SELECT * FROM pg_prepared_xacts;` is leeg. Afgevinkt als alle vier kloppen en in de monitoring zitten (DB-97).
- Norm: ASVS 5.0.0 15.2.2 (L2, beschikbaarheid).

### DB-95 Indexeer foreign keys en lees het plan van elke nieuwe zware query
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak een index op elke foreign-key-kolom en op `tenant_id` (als eerste kolom van een samengestelde index), en bekijk voor elke nieuwe query op een tabel boven de 100.000 rijen het plan met `EXPLAIN (ANALYZE, BUFFERS)` op een kopie met productieomvang.
- Bewijs: Query op `pg_constraint` en `pg_index` die foreign keys zonder dekkende index toont, is leeg; bij de PR van een nieuwe zware query staat het plan. Afgevinkt als beide kloppen. De grens van 100.000 rijen is een eigen richtwaarde.
- Norm: ASVS 5.0.0 15.2.2 (L2).

### DB-96 Houd extensies op een allowlist
middel · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Installeer alleen extensies die het project gebruikt, leg per extensie vast waarom, en installeer geen onvertrouwde procedurele talen (`plperlu`, `plpython3u`). Een project met een exclusion constraint op een gewone kolom plus een bereik (BIZ-06) zet `btree_gist` op de lijst.
- Bewijs: `SELECT extname, extversion FROM pg_extension;` naast de vastgelegde lijst. Afgevinkt als ze gelijk zijn.
- Norm: OWASP Top 10 2025 A02 Security Misconfiguration en A03 Software Supply Chain Failures (in de uitgave 2021: A05 en A06).

### DB-97 Bewaak de database en alarmeer op vijf signalen
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewaak en alarmeer minimaal op: bereikbaarheid (`pg_isready` of een health-check met een echte query), vrije schijfruimte van het datavolume, aantal verbindingen ten opzichte van `max_connections`, leeftijd van de laatste back-up (DB-47), en langlopende of vastzittende transacties.
- Bewijs: De monitorconfiguratie toont de vijf controles met drempels en het alarmkanaal; een proef per controle (drempel tijdelijk omlaag) geeft een melding. Afgevinkt als de proeven zijn gedaan en gedateerd.
- Norm: ASVS 5.0.0 16.3.4 (L2); AVG artikel 32 lid 1 onder b.
- Zie ook: ARCH-67, INFRA-35, ARCH-69, INFRA-86, INFRA-87, DB-47, AI-83, INFRA-52

### DB-98 Database in Docker: versie vastzetten, app-rol via initialisatie, gegevens op een volume
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet het image vast op major en minor (bij voorkeur op digest, zie GIT), geef het beheerwachtwoord mee als `POSTGRES_PASSWORD_FILE`, maak de app- en migratierol aan in een initialisatiescript, en zet de gegevens op een benoemd volume dat in de back-up zit.
- Bewijs: Het compose-bestand toont een tag met minor of digest, een `_FILE`-geheim, een volume en een healthcheck; rollen in een bestaande database worden via een migratie of beheerscript aangemaakt, niet alleen via het initialisatiescript. Afgevinkt als dat zo is.
- Norm: ASVS 5.0.0 13.3.1 (L2), 13.2.3 (L2).
