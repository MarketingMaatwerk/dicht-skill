# DB A: rollen en minimale rechten

Compacte regels van `dicht-database`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/database.md` (regelnummer in `regel-index.tsv`).

### DB-01 Geen superuser als applicatierol
kritiek · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Laat geen enkele applicatie, worker, MCP-server of script in productie verbinden als superuser of als de rol uit `POSTGRES_USER`.
- Bewijs: `SELECT rolname, rolsuper, rolbypassrls, rolcreaterole, rolcreatedb, rolreplication FROM pg_roles WHERE rolcanlogin;` plus de gebruikersnaam uit de `DATABASE_URL` van elke dienst. Afgevinkt als de rol van elke dienst op alle vijf kolommen `f` heeft.
- Norm: ASVS 5.0.0 13.2.2 (L2); OWASP Top 10 2025 A01 Broken Access Control en A02 Security Misconfiguration (in de uitgave 2021: A01 en A05).

### DB-02 Eén loginrol per dienst en per omgeving
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke dienst (API, worker, MCP-server, rapportage, back-up, migratie) een eigen loginrol met een eigen wachtwoord, en gebruik nooit dezelfde rol in productie, accept en ontwikkeling.
- Bewijs: Lijst van diensten naast `SELECT usename, count(*) FROM pg_stat_activity GROUP BY 1;`. Afgevinkt als elke dienst een eigen rol toont en geen rol in twee omgevingen bestaat met hetzelfde wachtwoord (controle in de geheimenopslag).
- Norm: ASVS 5.0.0 13.2.1 en 13.2.2 (L2).
- Zie ook: INFRA-66, INFRA-10, AUTH-56, INFRA-97, WP-45, WP-68, AI-21

### DB-03 Scheid de eigenaar (migratierol) van de runtime-rol
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een aparte migratierol eigenaar zijn van schema's en tabellen en voer alleen daarmee DDL uit; geef de runtime-rol nooit eigendom.
- Bewijs: `SELECT schemaname, tablename, tableowner FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');`. Afgevinkt als geen tabel de runtime-rol als eigenaar heeft en de migratierol niet in een runtime-`DATABASE_URL` voorkomt.
- Norm: ASVS 5.0.0 13.2.2 (L2).

### DB-04 Trek de standaardrechten van PUBLIC in
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CIS
- Regel: Voer per database `REVOKE ALL ON DATABASE <db> FROM PUBLIC` en `REVOKE CREATE ON SCHEMA public FROM PUBLIC` uit en verleen `CONNECT` en `USAGE` alleen aan de rollen die ze nodig hebben.
- Bewijs: `SELECT datname, datacl FROM pg_database;` en `\dn+`. Afgevinkt als in `datacl` geen regel `=Tc/...` (PUBLIC) staat en `public` geen `C` voor PUBLIC toont.
- Norm: ASVS 5.0.0 13.2.2 (L2); CIS PostgreSQL Benchmark (regelnummer niet bevestigd, zie Niet bevestigd).

### DB-05 Verleen rechten per tabel en per bewerking, nooit GRANT ALL
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef de runtime-rol alleen `SELECT`, `INSERT`, `UPDATE` en `DELETE` op de tabellen die hij gebruikt, laat `DELETE` weg waar de dienst niet verwijdert, en leg toekomstige tabellen vast met `ALTER DEFAULT PRIVILEGES FOR ROLE <migratierol>`.
- Bewijs: `SELECT grantee, table_name, string_agg(privilege_type, ',') FROM information_schema.role_table_grants WHERE grantee = '<rol>' GROUP BY 1,2;`. Afgevinkt als geen `TRUNCATE`, `REFERENCES` of `TRIGGER` voorkomt en audit-tabellen alleen `INSERT` en `SELECT` hebben.
- Norm: ASVS 5.0.0 13.2.2 (L2).

### DB-06 Geen gevaarlijke rolattributen of voorgedefinieerde rollen voor applicaties
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef een applicatierol nooit `CREATEROLE`, `CREATEDB`, `REPLICATION` of `BYPASSRLS`, en nooit lidmaatschap van `pg_read_server_files`, `pg_write_server_files`, `pg_execute_server_program`, `pg_read_all_data` of `pg_write_all_data`.
- Bewijs: `SELECT r.rolname, m.rolname AS lid_van FROM pg_auth_members a JOIN pg_roles r ON r.oid = a.member JOIN pg_roles m ON m.oid = a.roleid WHERE m.rolname LIKE 'pg\_%';` plus de query uit DB-01. Afgevinkt als applicatierollen in geen van beide voorkomen. Uitzondering die mag: een monitoringrol met `pg_monitor`.
- Norm: ASVS 5.0.0 13.2.2 (L2).

### DB-07 Trek EXECUTE op functies in van PUBLIC
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Voer voor de migratierol `ALTER DEFAULT PRIVILEGES FOR ROLE <migratierol> REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC` uit (zonder `IN SCHEMA`) en verleen `EXECUTE` per functie.
- Bewijs: `SELECT proname, proacl FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace WHERE n.nspname NOT IN ('pg_catalog','information_schema') AND (proacl IS NULL OR proacl::text LIKE '%=X/%');`. Afgevinkt als de query voor eigen functies nul rijen geeft (een lege `proacl` betekent de standaard, dus PUBLIC mag uitvoeren).
- Norm: ASVS 5.0.0 13.2.2 (L2).

### DB-08 Zet search_path vast per rol
middel · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet voor elke loginrol `ALTER ROLE <rol> SET search_path = <eigen schema's>` zonder schema's waarin andere rollen mogen schrijven, en kwalificeer objecten in functies met hun schema.
- Bewijs: `SELECT rolname, rolconfig FROM pg_roles WHERE rolcanlogin;` en `\dn+`. Afgevinkt als elke loginrol een expliciet `search_path` heeft en DB-04 is afgevinkt.
- Norm: ASVS 5.0.0 13.2.2 (L2).

### DB-09 Vrije query-tools draaien onder een alleen-lezen rol
hoog · hard · mcp | api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elk hulpmiddel dat vrije SQL uitvoert (een MCP-tool zoals `query_database`, een rapportagescherm, een AI-agent) verbinden met een eigen rol die alleen `SELECT` heeft op een allowlist van tabellen of views, met `statement_timeout` en zonder toegang tot tabellen met geheimen.
- Bewijs: Test in CI of handmatig: verbind als de tool-rol en voer `INSERT`, `UPDATE`, `DELETE`, `CREATE TABLE` en een `SELECT` op een geheimentabel uit. Afgevinkt als alle vijf een rechtenfout geven en `SELECT rolconfig FROM pg_roles WHERE rolname = '<rol>'` een `statement_timeout` toont.
- Norm: ASVS 5.0.0 13.2.2 (L2), 15.2.2 (L2); OWASP Top 10 for LLM Applications (excessive agency, uitwerking in domein AI).
- Zie ook: AI-20, AI-21

### DB-10 Begrens elke rol met een verbindingslimiet
laag · richtlijn · api | app | mcp | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Zet per loginrol `CONNECTION LIMIT` op de poolgrootte van die dienst plus een kleine marge.
- Bewijs: `SELECT rolname, rolconnlimit FROM pg_roles WHERE rolcanlogin;`. Afgevinkt als geen applicatierol `-1` heeft en de som onder `max_connections` blijft.
- Norm: ASVS 5.0.0 13.1.2 (L3).
