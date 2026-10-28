# AUTH J: Multi-tenant isolatie

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/auth.md` (regelnummer in `regel-index.tsv`).

### AUTH-72 Haal de tenant uit de geverifieerde sessie, nooit uit de aanvraag
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bepaal de actieve tenant op de server uit de sessie en het actuele lidmaatschap van de gebruiker; behandel een tenant-id uit URL, header, body of subdomein alleen als keuze en controleer bij elk verzoek dat de gebruiker lid is van die tenant.
- Bewijs: Test: een geldige sessie van tenant A met `X-Tenant-Id` of padparameter van tenant B geeft 403 of 404 op elke route. Codecheck: `ctx.tenantId` wordt op één plek gezet, na controle van lidmaatschap. Afgevinkt als de test in de matrix van AUTH-66 zit.
- Norm: ASVS 5.0.0 V8.4.1 (L2; voor Marketing Maatwerk L3-behandeling: tenant-isolatie is een kritiek deel).
- Zie ook: DB-13, DB-17, AUTH-74, DB-12, DB-14, AUTH-73, AI-22

### AUTH-73 Rollen gelden per tenant, niet globaal
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Sla rollen op als koppeling tussen gebruiker en tenant en beantwoord "is deze gebruiker beheerder" altijd voor een specifieke tenant; houd platformbeheer strikt apart in een eigen rol en een eigen pad.
- Bewijs: `\d memberships` toont `(user_id, tenant_id, role)`; `grep -rnE "isAdmin|role *=== *'admin'" src/` levert geen controle op zonder tenant in dezelfde voorwaarde. Test: beheerder van tenant A krijgt 403 of 404 op beheerroutes van tenant B. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V8.4.1 (L2), V8.2.1 (L1).
- Zie ook: DB-13, AUTH-72, DB-17, AUTH-74, DB-12, DB-14, AI-22

### AUTH-74 Tenant-filter in elke query plus rij-niveau beveiliging als vangnet
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke tabel met klantdata een `tenant_id NOT NULL`, laat alle queries via gedeelde helpers lopen die de tenant verplicht meenemen, en zet daarnaast rij-niveau beveiliging aan met `FORCE ROW LEVEL SECURITY`, voor een applicatierol die geen eigenaar van de tabel is en geen `SUPERUSER` of `BYPASSRLS` heeft.
- Bewijs: `SELECT relname, relrowsecurity, relforcerowsecurity FROM pg_class WHERE relkind='r' AND relnamespace='public'::regnamespace` toont `t, t` voor elke tabel met `tenant_id`; `SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user` als applicatierol geeft `f, f`. Afgevinkt als beide kloppen. Zie DB voor de uitwerking.
- Norm: ASVS 5.0.0 V8.4.1 (L2), V8.3.1 (L1).
- Zie ook: DB-13, AUTH-72, DB-17, DB-12, DB-14, AUTH-73, AI-22

### AUTH-75 → DB-16
Samengevoegd: "Zet de tenant-context per transactie, niet per verbinding" is gedekt door DB-16. Gebruik die regel.

### AUTH-76 → DB-23
Samengevoegd: "Tenant in elke cachesleutel, elk bestandspad en elk wachtrijbericht" is gedekt door DB-23. Gebruik die regel.

### AUTH-77 Een isolatietest per tabel en per route, die vóór elke uitrol draait
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd een regressietest bij die voor elke tabel met `tenant_id` en elke route met klantdata twee tenants aanmaakt en bewijst dat lezen, wijzigen en verwijderen over de grens wordt geweigerd; breid hem uit bij elke nieuwe tabel of route en draai hem vóór elke uitrol.
- Bewijs: CI of het uitrolscript draait de isolatietest en stopt bij een fout. Een controle vergelijkt `SELECT table_name FROM information_schema.columns WHERE column_name='tenant_id'` met de tabellen in de test en faalt bij een ontbrekende tabel. Afgevinkt als beide in de pijplijn staan.
- Norm: ASVS 5.0.0 V8.4.1 (L2).
- Zie ook: DB-22, AUTH-66, AI-53, ARCH-40

### AUTH-78 Laat foutmeldingen en unieke sleutels niets over andere tenants verraden
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak unieke constraints per tenant (`UNIQUE (tenant_id, email)`), en geef bij een botsing of een ontbrekend object dezelfde generieke melding, zodat een tenant niet kan afleiden wat er bij een andere tenant bestaat.
- Bewijs: `\d+ <tabel>` toont dat unieke indexen op klantdata met `tenant_id` beginnen. Afgevinkt als dat voor elke tabel met `tenant_id` geldt.
- Norm: ASVS 5.0.0 V8.4.1 (L2).
