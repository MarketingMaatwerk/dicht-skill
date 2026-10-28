# DB D: migraties zonder risico

Compacte regels van `dicht-database`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/database.md` (regelnummer in `regel-index.tsv`).

### DB-30 Migraties zijn gereviewde SQL-bestanden in git
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Wijzig het productieschema alleen via migratiebestanden die met `drizzle-kit generate` (of met de hand) zijn gemaakt, in git staan, zijn gelezen en met `drizzle-kit migrate` worden toegepast; gebruik `drizzle-kit push` nooit tegen productie of accept.
- Bewijs: Map met migraties in git; `SELECT * FROM drizzle.__drizzle_migrations ORDER BY 1 DESC LIMIT 5;` komt overeen met de bestanden; `grep -rn "drizzle-kit push" package.json scripts/ deploy/` toont alleen ontwikkelscripts. Afgevinkt als alle drie kloppen.
- Norm: Besluit 13 van Marketing Maatwerk; ASVS 5.0.0 geen directe eis.

### DB-31 Expand en contract: verwijder of hernoem nooit in dezelfde release
hoog · hard · api | app | mcp | klantproject · eigen bron · tegenlezer: bevestigd (04-10-2026)
- Regel: Splits elke brekende schemawijziging in drie releases: eerst toevoegen (nieuwe kolom of tabel, oude blijft werken), dan de code omzetten en gegevens overzetten, en pas na een release waarin niets de oude vorm meer leest of schrijft verwijderen.
- Bewijs: CI-controle die in nieuwe migratiebestanden `DROP COLUMN`, `DROP TABLE`, `RENAME` en `ALTER COLUMN ... TYPE` aanwijst en een regel `-- contract: <verwijzing naar de expand-release>` eist. Afgevinkt als de controle groen is en de verwijzing klopt.
- Norm: Besluit 13 van Marketing Maatwerk; ASVS 5.0.0 geen directe eis.
- Eigen bron: geen primaire bron; de eis is besluit 13; de primaire bron draagt alleen het gedrag van `DROP COLUMN` en `RENAME`, Fowler is secundair. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).

### DB-32 Zet lock_timeout in elke migratie
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Begin elke migratie die DDL bevat met `SET lock_timeout = '5s'` (en een passende `statement_timeout`), en laat de migratie bij een time-out falen en later opnieuw proberen.
- Bewijs: CI-controle dat elk migratiebestand met DDL `lock_timeout` zet, of `SELECT rolconfig FROM pg_roles WHERE rolname = '<migratierol>'` toont de instelling. Afgevinkt als een van beide waar is.
- Norm: ASVS 5.0.0 15.2.2 (L2, beschikbaarheid); besluit 13.

### DB-33 Bouw indexen op gevulde tabellen met CONCURRENTLY en controleer op ongeldige indexen
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak een index op een bestaande tabel met `CREATE INDEX CONCURRENTLY` in een eigen migratie buiten een transactie, en controleer daarna op ongeldige indexen.
- Bewijs: `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;` geeft nul rijen na elke migratie (als stap in het deployscript). Afgevinkt als de controle in het script staat en leeg is. Of `drizzle-kit migrate` een bestand buiten een transactie kan draaien is niet bevestigd, zie Niet bevestigd; draai zulke bestanden desnoods met `psql`.
- Norm: Besluit 13; ASVS 5.0.0 15.2.2 (L2).

### DB-34 Voeg foreign keys en CHECK-constraints toe als NOT VALID en valideer apart
hoog · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Voeg op een gevulde tabel een foreign key of `CHECK` toe met `NOT VALID` en voer `VALIDATE CONSTRAINT` uit in een aparte stap.
- Bewijs: Review van het migratiebestand; `SELECT conname FROM pg_constraint WHERE NOT convalidated;` is leeg na de tweede stap. Afgevinkt als beide stappen bestaan en de query leeg is.
- Norm: Besluit 13.

### DB-35 Zet NOT NULL op een gevulde kolom via een gevalideerde CHECK
middel · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Voeg eerst `CHECK (kolom IS NOT NULL) NOT VALID` toe, valideer die, voer dan `SET NOT NULL` uit en verwijder de `CHECK`.
- Bewijs: Review van het migratiebestand op de vier stappen; tijdmeting op de kopie uit DB-39. Afgevinkt als de `SET NOT NULL`-stap op de kopie binnen de `lock_timeout` blijft.
- Norm: Besluit 13.

### DB-36 Voorkom een herschrijving van de hele tabel
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Voeg op een gevulde tabel geen kolom toe met een volatiele standaardwaarde (`clock_timestamp()`, `gen_random_uuid()`), geen opgeslagen gegenereerde kolom en geen identity-kolom, en wijzig geen kolomtype, tenzij de tijd op een kopie is gemeten en een onderhoudsvenster is afgesproken.
- Bewijs: CI-controle op migratiebestanden voor `ALTER COLUMN ... TYPE`, `GENERATED`, en `DEFAULT` met een functieaanroep op bestaande tabellen; tijdmeting uit DB-39. Afgevinkt als er geen treffer is of de meting en het venster zijn vastgelegd.
- Norm: Besluit 13.

### DB-37 Voeg een unieke of primaire sleutel toe via een vooraf gebouwde index
middel · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw de unieke index eerst met `CREATE UNIQUE INDEX CONCURRENTLY` en koppel hem daarna met `ADD CONSTRAINT ... UNIQUE USING INDEX` (of `PRIMARY KEY USING INDEX`).
- Bewijs: Review van het migratiebestand; controle op ongeldige indexen uit DB-33. Afgevinkt als beide stappen apart staan.
- Norm: Besluit 13.

### DB-38 Vul gegevens bij in kleine batches, los van de schemamigratie
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Voer een backfill of bulkwijziging uit als een herhaalbaar script dat per batch (bijvoorbeeld 1.000 tot 10.000 rijen) een eigen korte transactie gebruikt, en nooit als één `UPDATE` over de hele tabel in de schemamigratie.
- Bewijs: Het backfill-script staat in git, is idempotent (een tweede run wijzigt nul rijen) en logt de voortgang. Afgevinkt als de tweede run nul rijen meldt.
- Norm: Besluit 13.

### DB-39 Test elke migratie op een recente kopie van productie
hoog · hard · api | app | mcp | klantproject · eigen bron · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai elke migratie eerst op een herstelde, recente kopie van de productiedatabase (met gemaskeerde persoonsgegevens volgens DB-85), meet de duur per statement en draai daarna de testsuite tegen dat schema.
- Bewijs: Logregel van de proefmigratie met datum, omvang van de kopie en duur per bestand, plus de testuitvoer. Afgevinkt als de log bestaat, van na de laatste wijziging van het bestand is, en geen statement langer dan de `lock_timeout` een blokkerende lock hield.
- Norm: Besluit 13; AVG artikel 32 lid 1 onder d (regelmatig testen).
- Eigen bron: geen primaire bron; de eis is besluit 13 en een eigen les (eigen ervaring); de primaire bron draagt alleen het herstel van een dump. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).

### DB-40 Leg de terugweg vast voordat je migreert
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf bij elke migratie vooraf op hoe je terug kunt (de omgekeerde SQL, of "niet nodig: alleen toevoegend"), en maak vlak voor een migratie die gegevens verwijdert of omzet een back-up waarvan je het herstel hebt geprobeerd.
- Bewijs: In de PR of het migratiebestand staat een regel `-- terugweg:`; bij destructieve migraties het pad en de controlesom van de dump en de uitkomst van de herstelproef. Afgevinkt als beide aanwezig zijn.
- Norm: Besluit 13; AVG artikel 32 lid 1 onder c.
- Zie ook: WP-63, WP-53, ARCH-25

### DB-41 Eén migratieloper, als aparte deploystap met de migratierol
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai migraties als aparte stap in de deploy met de migratierol (DB-03), niet vanuit de applicatie bij het opstarten, en zorg dat nooit twee lopers tegelijk draaien.
- Bewijs: Het deployscript toont de migratiestap met een eigen `DATABASE_URL`; `grep -rn "migrate(" src/` toont geen aanroep in de opstartcode van de applicatie. Afgevinkt als beide kloppen. Wie toch bij het opstarten migreert, neemt eerst `pg_advisory_xact_lock` op een vaste sleutel.
- Norm: ASVS 5.0.0 13.2.2 (L2).
- Zie ook: ARCH-22, ARCH-23, ARCH-24, GIT-02, GIT-03, DB-42, INFRA-47

### DB-42 Controleer na elke uitrol dat schema en code overeenkomen
middel · hard · api | app | mcp | klantproject · eigen bron · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat de deploy na de migratiestap controleren dat de laatst toegepaste migratie in de database gelijk is aan de laatste migratie in de uitgerolde code, in elke omgeving.
- Bewijs: Health-check of deploystap die de hoogste rij uit `drizzle.__drizzle_migrations` vergelijkt met het journaal in de build. Afgevinkt als de controle bestaat en de deploy stopt bij een verschil.
- Norm: Besluit 13.
- Eigen bron: geen primaire bron; de eis is besluit 13 en een eigen les (eigen ervaring); de primaire bron draagt alleen het mechanisme van `drizzle-kit migrate`. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Zie ook: ARCH-22, ARCH-23, ARCH-24, GIT-02, GIT-03, DB-41, INFRA-47

### DB-43 Zet rechten en RLS in dezelfde migratie als de tabel
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat de migratie die een tabel, view of functie aanmaakt in dezelfde transactie ook de `REVOKE`, de `GRANT`, `ENABLE` en `FORCE ROW LEVEL SECURITY` en de policies bevatten.
- Bewijs: CI-controle: elk migratiebestand met `CREATE TABLE` voor een tenant-tabel bevat ook `ENABLE ROW LEVEL SECURITY`, `FORCE ROW LEVEL SECURITY` en `CREATE POLICY`. Afgevinkt als de controle groen is en de metatest uit DB-22 slaagt.
- Norm: ASVS 5.0.0 8.4.1 (L2).
