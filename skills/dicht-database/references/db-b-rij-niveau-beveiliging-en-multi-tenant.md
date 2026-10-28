# DB B: rij-niveau beveiliging en multi-tenant

Compacte regels van `dicht-database`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/database.md` (regelnummer in `regel-index.tsv`).

### DB-11 Kies het tenantmodel bewust en leg het vast
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg voor elk multi-tenant systeem in een ADR vast welk isolatiemodel geldt (gedeelde tabellen met `tenant_id` en RLS, schema per tenant, of database per tenant) en waarom.
- Bewijs: ADR in de repository met de keuze, de afweging en de verwijzing naar de isolatietest uit DB-22. Afgevinkt als het document bestaat en de test ernaar verwijst.
- Norm: ASVS 5.0.0 8.1.1 (L1), 8.4.1 (L2).

### DB-12 Elke tenant-tabel heeft een verplichte tenant_id
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke tabel met tenantgegevens een kolom `tenant_id` die `NOT NULL` is, een foreign key naar de tenanttabel heeft en vooraan staat in een index; leid de tenant nooit alleen af via een join.
- Bewijs: Query die alle tabellen in het applicatieschema toont zonder kolom `tenant_id`, naast een expliciete lijst van globale tabellen. Afgevinkt als het verschil leeg is en `is_nullable = 'NO'` voor elke `tenant_id`.
- Norm: ASVS 5.0.0 8.4.1 (L2), 8.2.2 (L1).
- Zie ook: DB-13, AUTH-72, DB-17, AUTH-74, DB-14, AUTH-73, AI-22

### DB-13 Zet RLS aan en dwing hem af op elke tenant-tabel
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Voer op elke tenant-tabel zowel `ENABLE ROW LEVEL SECURITY` als `FORCE ROW LEVEL SECURITY` uit, in dezelfde migratie die de tabel aanmaakt.
- Bewijs: `SELECT relname, relrowsecurity, relforcerowsecurity FROM pg_class WHERE relkind = 'r' AND relnamespace = 'public'::regnamespace;`. Afgevinkt als elke tenant-tabel op beide kolommen `t` heeft.
- Norm: ASVS 5.0.0 8.4.1 (L2); L3 voor tenant-isolatie volgens besluit 6.
- Zie ook: AUTH-72, DB-17, AUTH-74, DB-12, DB-14, AUTH-73, AI-22

### DB-14 De runtime-rol mag RLS niet kunnen omzeilen
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zorg dat de rol waarmee de applicatie verbindt geen superuser is, geen `BYPASSRLS` heeft en geen eigenaar van tenant-tabellen is.
- Bewijs: De query uit DB-01 voor de runtime-rol, plus de test uit DB-22 die met exact de productierol (naam en attributen) draait. Afgevinkt als `rolsuper = f`, `rolbypassrls = f` en de test slaagt.
- Norm: ASVS 5.0.0 8.4.1 (L2).
- Zie ook: DB-13, AUTH-72, DB-17, AUTH-74, DB-12, AUTH-73, AI-22

### DB-15 Schrijf policies met USING en WITH CHECK, en gebruik restrictief voor de tenantgrens
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Definieer de tenantgrens als een `AS RESTRICTIVE`-policy `FOR ALL` met zowel `USING` als `WITH CHECK`, naast minstens één permissieve policy.
- Bewijs: `SELECT tablename, policyname, permissive, cmd, qual, with_check FROM pg_policies;`. Afgevinkt als elke tenant-tabel een `RESTRICTIVE`-policy met gevulde `qual` en `with_check` heeft, en de test uit DB-22 ook een `INSERT` en `UPDATE` naar een andere tenant weigert.
- Norm: ASVS 5.0.0 8.4.1 (L2), 8.2.2 (L1).

### DB-16 Zet de tenantcontext per transactie, nooit per sessie
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet de tenant met `SELECT set_config('app.tenant_id', $1, true)` of `SET LOCAL` binnen de transactie van het verzoek, en voer elke tenantquery binnen die transactie uit.
- Bewijs: `grep -rnE "SET (SESSION )?app\.|set_config\([^)]*false" src/` geeft nul treffers; een test die twee verzoeken van verschillende tenants achter elkaar over een pool van één verbinding stuurt. Afgevinkt als de grep leeg is en de test slaagt.
    Ook (uit AUTH-75): `grep -rnE "SET +app\.|set_config\(" src/` toont alleen `SET LOCAL` of `set_config(..., true)` binnen een transactie. Test met een pool van grootte 1: aanvraag als tenant A en daarna, zonder context te zetten, een query: die geeft nul rijen of een fout. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 8.4.1 (L2).
- Dekt ook: AUTH-75

### DB-17 Tenantcontext komt uit de geverifieerde sessie en faalt gesloten
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Leid de tenant af uit de server-geverifieerde identiteit en het actuele lidmaatschap, gebruik in policies `current_setting('app.tenant_id')` zonder `missing_ok`, en zet nooit een standaardwaarde voor die instelling.
- Bewijs: Test: verzoek met geldige sessie van tenant A en het tenant-id van B geeft 403 of 404; een query zonder context geeft een databasefout. `SELECT qual FROM pg_policies` bevat nergens `current_setting(..., true)`. Afgevinkt als alle drie kloppen.
- Norm: ASVS 5.0.0 8.4.1 (L2), 8.3.1 (L1), 8.2.2 (L1); OWASP API Security Top 10 2023 API1.
- Zie ook: DB-13, AUTH-72, AUTH-74, DB-12, DB-14, AUTH-73, AI-22

### DB-18 Views over tenant-tabellen krijgen security_invoker
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak elke view die tenant-tabellen leest aan met `WITH (security_invoker = true)`.
- Bewijs: `SELECT c.relname, c.reloptions FROM pg_class c WHERE c.relkind = 'v' AND c.relnamespace = 'public'::regnamespace;`. Afgevinkt als elke view over tenant-tabellen `security_invoker=true` toont en in de isolatietest van DB-22 is opgenomen. Vereist PostgreSQL 15 of hoger (bevestigd in de release notes van 15: "Previously, view accesses were always treated as being done by the view's owner. That's still the default").
- Norm: ASVS 5.0.0 8.4.1 (L2).

### DB-19 SECURITY DEFINER-functies zijn uitzonderingen met drie verplichte maatregelen
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf een `SECURITY DEFINER`-functie alleen met `SET search_path = <vertrouwd schema>, pg_temp`, met `REVOKE ALL ... FROM PUBLIC` en een gerichte `GRANT EXECUTE` in dezelfde transactie, en met een eigen controle op tenant en gebruiker in de functie zelf.
- Bewijs: `SELECT proname, proconfig, proacl FROM pg_proc WHERE prosecdef;`. Afgevinkt als elke rij een `search_path` in `proconfig` heeft dat op `pg_temp` eindigt, `proacl` geen PUBLIC bevat, en elke functie in de isolatietest van DB-22 zit.
- Norm: ASVS 5.0.0 8.4.1 (L2), 8.3.3 (L3).

### DB-20 Neem tenant_id op in unieke sleutels en samengestelde foreign keys
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak unieke constraints op tenantgegevens altijd samengesteld met `tenant_id`, en laat foreign keys tussen tenant-tabellen verwijzen naar `(tenant_id, id)`.
- Bewijs: Query op `pg_constraint` die unieke constraints en foreign keys op tenant-tabellen toont zonder `tenant_id` in de kolomlijst. Afgevinkt als die lijst leeg is of elke uitzondering is toegelicht.
- Norm: ASVS 5.0.0 8.4.1 (L2).

### DB-21 Geen TRUNCATE of REFERENCES voor de runtime-rol
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Verleen de runtime-rol nooit `TRUNCATE` of `REFERENCES` op tenant-tabellen.
- Bewijs: De query uit DB-05. Afgevinkt als `TRUNCATE` en `REFERENCES` niet voorkomen voor de runtime-rol.
- Norm: ASVS 5.0.0 8.4.1 (L2).

### DB-22 Een cross-tenant regressietest per tabel, view en functie is een gate
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd een geautomatiseerde test bij die voor elke tenant-tabel, elke view en elke `SECURITY DEFINER`-functie bewijst dat tenant A de rijen van tenant B niet kan lezen, invoegen, wijzigen of verwijderen, en laat de build falen als een tenant-tabel in de test ontbreekt.
- Bewijs: CI-uitvoer van de isolatietest plus de metatest. Afgevinkt als beide groen zijn en de test in de verplichte CI-stappen staat.
- Norm: ASVS 5.0.0 8.4.1 (L2); L3 voor tenant-isolatie volgens besluit 6.
- Zie ook: AUTH-77, AUTH-66, AI-53, ARCH-40

### DB-23 Tenant-id hoort ook in caches, wachtrijen, bestanden en exports
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem het tenant-id op in elke cachesleutel, elk wachtrijbericht, elk bestandspad en elke export waarvan de inhoud per tenant verschilt, en zet in een worker de context opnieuw volgens DB-16 voordat hij de database raakt. Aanvulling uit AUTH-76: Laat een worker nooit met een bevoorrechte verbinding alles verwerken.
- Bewijs: Codereview op cachesleutels en wachtrijschema's (schema-validatie eist `tenantId`); test die voor twee tenants dezelfde cachebare route opvraagt. Afgevinkt als de test verschillende uitkomsten geeft en het schema `tenantId` verplicht stelt.
    Ook (uit AUTH-76): `grep -rnE "cache\.(get|set)\(|redis\.(get|set)\(" src/` en controleer dat elke sleutel via een helper `tenantKey(ctx, ...)` loopt; test: export van tenant A is met een sessie van tenant B niet op te halen; test: een worker verwerkt een bericht zonder `tenantId` niet. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 8.4.1 (L2), 14.2.2 (L2).
- Dekt ook: AUTH-76
- Zie ook: AI-68, AI-71, AUTH-69

### DB-24 Back-up- en beheerrollen die RLS omzeilen zijn apart en niet bereikbaar voor de app
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor `pg_dump` en beheer een aparte rol met `BYPASSRLS` of superuser die alleen lokaal vanaf de host verbindt, en gebruik nooit `--enable-row-security` voor een volledige back-up.
- Bewijs: Het back-upcommando in het script, de rol in `pg_hba.conf` of de compose-configuratie, en de herstelproef uit DB-46 met rijtellingen per tenant-tabel. Afgevinkt als de proef dezelfde tellingen geeft als productie.
- Norm: AVG artikel 32 lid 1 onder c.
