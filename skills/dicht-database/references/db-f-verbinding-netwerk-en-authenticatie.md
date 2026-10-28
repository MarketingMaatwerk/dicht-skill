# DB F: verbinding, netwerk en authenticatie

Compacte regels van `dicht-database`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/database.md` (regelnummer in `regel-index.tsv`).

### DB-58 De database is niet bereikbaar vanaf internet
kritiek · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026) · bron niet gelezen: CIS
- Regel: Publiceer de databasepoort nooit zonder host-adres; gebruik een intern Docker-netwerk zonder `ports`, of bind expliciet aan `127.0.0.1`.
- Bewijs: `docker ps --format '{{.Names}}\t{{.Ports}}'` toont voor databasecontainers alleen `127.0.0.1:` of geen gepubliceerde poort, en een poortscan van buiten (`nmap -p 5432-5445 <publiek IP>`) toont ze gesloten. Afgevinkt als beide kloppen.
- Norm: ASVS 5.0.0 13.2.4 (L2); OWASP Top 10 2025 A02 Security Misconfiguration (in de uitgave 2021: A05); CIS Docker Benchmark (nummer niet bevestigd).
- Zie ook: INFRA-13, INFRA-14, INFRA-12, AI-75, AI-39

### DB-59 Geen trust over TCP, alleen scram-sha-256
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CIS
- Regel: Gebruik voor elke TCP-regel in `pg_hba.conf` de methode `scram-sha-256`, zet nooit `POSTGRES_HOST_AUTH_METHOD=trust`, en gebruik geen `md5` of `password`.
- Bewijs: `SELECT type, database, user_name, address, auth_method FROM pg_hba_file_rules;` toont voor `host`-regels alleen `scram-sha-256`; `SHOW password_encryption;` geeft `scram-sha-256`; `SELECT rolname FROM pg_authid WHERE rolpassword LIKE 'md5%';` is leeg. Afgevinkt als alle drie kloppen.
- Norm: ASVS 5.0.0 13.2.1 en 13.2.3 (L2); CIS PostgreSQL Benchmark (nummer niet bevestigd).

### DB-60 TLS met certificaatcontrole zodra de verbinding de host verlaat
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor elke databaseverbinding die niet over de loopback of een Unix-socket op dezelfde host loopt `sslmode=verify-full` met een vast CA-certificaat, dwing aan de serverkant `hostssl` af, en zet nooit `rejectUnauthorized: false`.
- Bewijs: `grep -rn "rejectUnauthorized: false\|sslmode=\(disable\|allow\|prefer\|require\)" .` is leeg voor niet-lokale verbindingen; `SELECT ssl, client_addr FROM pg_stat_ssl JOIN pg_stat_activity USING (pid);` toont `t` voor elke niet-lokale verbinding. Afgevinkt als beide kloppen. Voor verbindingen binnen dezelfde host (loopback of intern Docker-netwerk) is dit een vastgelegde uitzondering onder L2; voor zorgdata (L3) niet.
- Norm: ASVS 5.0.0 12.3.1 en 12.3.2 (L2), 12.1.1 (L1).
- Zie ook: WEB-56, WEB-17, WP-43, INFRA-44, INFRA-55, INFRA-48

### DB-61 Zet en wissel wachtwoorden zonder dat ze in een log belanden
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet rolwachtwoorden met `\password` in `psql` of via een geheimbestand (`POSTGRES_PASSWORD_FILE`), nooit met een `ALTER ROLE ... PASSWORD '...'` in een migratie, script of shell-commando.
- Bewijs: `grep -rniE "password\s+'" drizzle/ migrations/ scripts/` is leeg; de geheimscan in CI (domein GIT) dekt migratiebestanden. Afgevinkt als beide groen zijn.
- Norm: ASVS 5.0.0 13.3.1 (L2), 16.2.5 (L2).
- Zie ook: INFRA-72, API-65, GIT-32, GIT-95, DB-62, AI-28, WP-33, INFRA-76, WP-71, AI-60, ARCH-49

### DB-62 De verbindingsstring is een geheim
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewaar `DATABASE_URL` alleen in de geheimenopslag of een `.env` buiten git en buiten de webroot met rechten 600, log hem nooit (ook niet bij een verbindingsfout) en toon hem nooit in een foutpagina of health-check.
- Bewijs: Geheimscan (gitleaks of trufflehog, zie GIT) op repository en logmap; `grep -rn "postgres://\|postgresql://" logs/` is leeg; `stat -c %a .env` geeft 600. Afgevinkt als alle drie kloppen.
- Norm: ASVS 5.0.0 13.3.1 en 13.3.2 (L2), 16.2.5 (L2), 16.5.1 (L2).
- Zie ook: INFRA-72, API-65, GIT-32, GIT-95, AI-28, WP-33, INFRA-76, WP-71, DB-61, AI-60, ARCH-49

### DB-63 Begrens de pool per dienst en houd de som onder max_connections
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel in elke dienst de poolgrootte expliciet in, maak één pool per proces (niet per verzoek of per module), en houd de som van alle pools plus beheerruimte onder `max_connections`.
- Bewijs: Overzicht (tabel in de documentatie) van dienst, poolgrootte en rol; `SELECT usename, count(*) FROM pg_stat_activity GROUP BY 1;` onder belasting blijft per rol onder de ingestelde grootte. Afgevinkt als de som onder `SHOW max_connections` blijft.
- Norm: ASVS 5.0.0 13.1.2 (L3), 15.2.2 (L2).

### DB-64 Met een pooler in transactiemodus bestaat er geen sessiestatus
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik achter PgBouncer in transactiemodus geen sessiebrede `SET`, geen `LISTEN`, geen sessie-advisory-locks en geen SQL-`PREPARE`; gebruik `SET LOCAL` en transactie-advisory-locks, en zet prepared statements van de driver uit of configureer `max_prepared_statements`.
- Bewijs: `SHOW pool_mode` in PgBouncer naast de grep uit DB-16 en `grep -rn "pg_advisory_lock\|LISTEN " src/`. Afgevinkt als bij transactiemodus geen sessiefuncties worden gebruikt. Niet van toepassing zolang er geen pooler tussen zit.
- Norm: ASVS 5.0.0 8.4.1 (L2).

### DB-65 Zet time-outs per rol
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet voor elke applicatierol met `ALTER ROLE ... SET` een `statement_timeout` (richtwaarde 30 seconden voor een API, langer voor workers), een `idle_in_transaction_session_timeout` (richtwaarde 60 seconden) en een `lock_timeout` (richtwaarde 5 tot 10 seconden).
- Bewijs: `SELECT rolname, rolconfig FROM pg_roles WHERE rolcanlogin;`. Afgevinkt als elke applicatierol de drie instellingen heeft. De getallen zijn richtwaarden van mij, geen norm; leg afwijkingen per dienst vast.
- Norm: ASVS 5.0.0 15.2.2 (L2), 15.1.3 (L2).
- Zie ook: API-48, API-49, ARCH-13, ARCH-14, AI-76, API-19, SCR-21, SCR-25, SCR-26, SCR-43, MSG-42
