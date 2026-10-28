# DB I: versleuteling, bewaartermijnen en privacy

Compacte regels van `dicht-database`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/database.md` (regelnummer in `regel-index.tsv`).

### DB-80 Versleutel geheimen en bijzondere gegevens per kolom in de applicatie
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Versleutel kolommen met tokens van derden (OAuth-refresh-tokens, IMAP- en SMTP-wachtwoorden, API-sleutels die je moet kunnen teruglezen) en bijzondere persoonsgegevens in de applicatie met AES-256-GCM via de standaardbibliotheek, met een sleutel die buiten de database en buiten de back-up van de database staat, en sla een sleutelversie op bij elke waarde.
- Bewijs: Lijst van kolommen met geheimen (uit de classificatie van DB-87); `SELECT <kolom> FROM ... LIMIT 1` toont geen leesbare waarde; de sleutel staat niet in de database, niet in de dump en niet in git; test voor versleutelen, ontsleutelen en een gewijzigde ciphertext die faalt. Afgevinkt als alle vier kloppen.
- Norm: ASVS 5.0.0 11.3.2 (L1), 11.3.3 (L2), 11.2.1 (L2), 14.2.4 (L2), 13.3.1 (L2); AVG artikel 32 lid 1 onder a.

### DB-81 Wat je alleen hoeft te vergelijken, hash je; en niet met pgcrypto
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Sla wachtwoorden, eigen API-sleutels, sessietokens en resettokens op als hash volgens domein AUTH (berekend in de applicatie), nooit versleuteld en nooit met `crypt()` uit pgcrypto in een query.
- Bewijs: `grep -rniE "crypt\(|pgp_sym_encrypt" src/ drizzle/` is leeg of toegelicht; het schema bevat voor tokens alleen hashkolommen. Afgevinkt als dat zo is.
- Norm: ASVS 5.0.0 hoofdstukken V6 en V7 (zie domein AUTH); 16.2.5 (L2).
- Zie ook: AUTH-04, AUTH-05, AUTH-07

### DB-82 Weet wat schijfversleuteling wel en niet doet
middel · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet versleuteling van het volume of de schijf aan waar de leverancier dat biedt, en reken het nooit mee als bescherming tegen een aanval op de draaiende server.
- Bewijs: Vastgelegd per server: is het volume versleuteld (ja of nee, bron: leverancier of `lsblk -f`), en welke kolommen zijn daarnaast volgens DB-80 versleuteld. Afgevinkt als de documentatie klopt met de werkelijkheid en met de teksten richting klanten.
- Norm: AVG artikel 32 lid 1 onder a; ASVS 5.0.0 14.1.2 (L2).

### DB-83 Elke tabel met persoonsgegevens heeft een bewaartermijn en een opruimjob
hoog · hard · api | app | mcp | klantproject | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per tabel met persoonsgegevens de bewaartermijn en de datumkolom vast waarop die telt, en laat een geplande, idempotente job rijen ouder dan die termijn in batches verwijderen of anonimiseren, met een logregel van het aantal.
- Bewijs: Tabel in de documentatie (tabel, termijn, kolom, job) die overeenkomt met `policy-state.yaml`; per tabel `SELECT min(<datumkolom>) FROM <tabel>` is niet ouder dan de termijn plus één jobinterval; de job staat in cron of systemd en logt. Afgevinkt als alle drie kloppen.
- Norm: AVG artikel 5 lid 1 onder e en artikel 25; ASVS 5.0.0 14.2.7 (L3), 14.2.4 (L2). Wettelijke basis: zie PRIV-21, PRIV-90, PRIV-58 (bewaartermijn per gegevenssoort; administratie en zorgdossier hebben een eigen termijn).
- Zie ook: PRIV-21, DB-84, PRIV-24, PRIV-26, DB-78, AI-70, PRIV-22

### DB-84 Een verwijderverzoek is een getest script
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd per systeem een script of functie bij die alle gegevens van één persoon of tenant verwijdert of anonimiseert over alle tabellen, zoekindexen, bestanden en vectoropslag, en leg vast hoe verwijderverzoeken na een herstel uit back-up opnieuw worden toegepast.
- Bewijs: Test die een persoon met gegevens in elke relevante tabel aanmaakt, het script draait en daarna met een zoekopdracht op e-mail en naam over alle tekstkolommen nul treffers vindt; een lijst van uitgevoerde verzoeken (zonder de gegevens zelf) voor herhaling na herstel. Afgevinkt als beide bestaan.
- Norm: AVG artikel 17; ASVS 5.0.0 14.2.4 (L2). Wettelijke basis: zie PRIV-24, PRIV-26 (wisverzoek, de verhouding tot back-ups en het geteste script).
- Zie ook: PRIV-21, DB-83, PRIV-24, PRIV-26, DB-78, AI-70, PRIV-22

### DB-85 Geen echte persoonsgegevens in ontwikkeling en accept zonder maskering
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Vul ontwikkel-, test- en acceptdatabases met gegenereerde gegevens of met een productiekopie die door een maskeerscript is gehaald (namen, e-mail, telefoon, adressen, vrije tekst, tokens), en geef die omgevingen nooit productiegeheimen.
- Bewijs: Het vulscript bevat de maskeerstap; `SELECT count(*) FROM contacts WHERE email NOT LIKE '%@<eigen testdomein>'` is nul in accept; tokens en wachtwoordkolommen zijn leeg of vervangen. Afgevinkt als dat zo is. Eigen regel van Marketing Maatwerk sluit hierop aan: testadressen op het eigen domein.
- Norm: AVG artikel 5 lid 1 onder c en f, artikel 25 en artikel 32 lid 1 onder a; ASVS 5.0.0 14.2.4 (L2).
- Zie ook: ARCH-48, INFRA-74, ARCH-50, ARCH-08, WEB-72

### DB-86 Pseudonimiseren is niet anonimiseren
middel · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026) · bron niet gelezen: EDPB
- Regel: Behandel gehashte of vervangen identifiers (gehasht e-mailadres, klantnummer in plaats van naam) als persoonsgegevens, bewaar de sleutel of koppeltabel gescheiden met eigen toegangsrechten, en noem iets pas anoniem als herleiden ook met aanvullende gegevens niet meer kan.
- Bewijs: In de dataclassificatie (DB-87) staat per afgeleide kolom of hij gepseudonimiseerd of anoniem is, met onderbouwing; gepseudonimiseerde tabellen hebben een bewaartermijn (DB-83). Afgevinkt als dat is vastgelegd.
- Norm: AVG artikel 4 lid 5, overweging 26, artikel 32 lid 1 onder a. Wettelijke basis: zie PRIV-12 (de EDPB-richtsnoeren 01/2025 over pseudonimisering zijn nog niet definitief gevonden (zie OPEN-VRAGEN.md)).

### DB-87 Classificeer gegevens per kolom
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd per project een lijst bij van tabellen en kolommen met hun klasse (publiek, intern, persoonsgegeven, bijzonder of gevoelig, geheim) en de maatregelen per klasse (versleuteling, logging, bewaartermijn, wie mag lezen).
- Bewijs: Het document bestaat, dekt elke tabel (vergelijk met `information_schema.tables`) en is bijgewerkt in dezelfde PR als de laatste schemawijziging. In Drizzle kan dit als commentaar of metadata naast de kolomdefinitie, met een script dat ontbrekende classificaties meldt. Afgevinkt als het script nul ontbrekende kolommen meldt.
- Norm: ASVS 5.0.0 14.1.1 en 14.1.2 (L2); AVG artikel 30 (verwerkingsregister, zie PRIV).

### DB-88 Het databaselog bevat geen persoonsgegevens of geheimen
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat `log_statement` op `none` of `ddl`, zet `log_parameter_max_length = 0` als je trage queries logt, laat `log_parameter_max_length_on_error` op 0, en behandel het serverlog als gevoelig (rechten, bewaartermijn).
- Bewijs: `SHOW log_statement; SHOW log_parameter_max_length; SHOW log_parameter_max_length_on_error;` en een steekproef `docker logs <db> | grep -cE '@|Bearer|password'`. Afgevinkt als de instellingen kloppen en de steekproef nul geeft.
- Norm: ASVS 5.0.0 16.2.5 (L2), 14.2.4 (L2); AVG artikel 5 lid 1 onder c.
- Zie ook: ARCH-62, API-66, INFRA-88, AUTH-14, AI-67, AI-52, GIT-39
