# BIZ A: vergrendelen en isolatie

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/bedrijfslogica-gelijktijdigheid.md` (regelnummer in `regel-index.tsv`).

### BIZ-01 Schrijf een teller of saldo als relatieve bewerking in SQL
hoog · hard · api | app | wp-plugin | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Verhoog of verlaag een teller, saldo, voorraad of gebruiksaantal met één statement dat op de huidige waarde in de database rekent (`SET gebruikt = gebruikt + 1 WHERE gebruikt < maximum`), en schrijf nooit een waarde terug die je eerder in de applicatie hebt gelezen en uitgerekend.
- Bewijs: `grep -rnE "\.set\(\{[^}]*(\+|-) *[0-9a-zA-Z_.]+" src` toont geen rekensom in JavaScript op een kolom die een teller of saldo is; elke treffer gebruikt `sql\`kolom + n\``. De kolom heeft een `CHECK (gebruikt >= 0 AND gebruikt <= maximum)` of `CHECK (saldo >= 0)` (DB-70). De test van API-30 (20 gelijktijdige verzoeken) eindigt op precies het maximum.
- Norm: ASVS 5.0.0 V2.3.4 (L2), V15.4.2 (L3); CWE-362.
- Zie ook: API-30, BIZ-02, BIZ-03, BIZ-04, BIZ-05, BIZ-06, BIZ-07, BIZ-09, BIZ-44, BIZ-50

### BIZ-02 Bewaak een regel over meerdere rijen met één slot op de ouder, niet met een slot op de rijen zelf
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Als een regel gaat over een aantal of een som van rijen (maximaal vijf gebruikers per tenant, maximaal drie open bestellingen per klant, de som van terugbetalingen is hoogstens het betaalde bedrag), neem dan eerst een slot op de ene rij waar de regel bij hoort (`SELECT ... FOR UPDATE` op de tenant, de klant of de betaling) en tel pas daarna, in dezelfde transactie; of draai de transactie als `SERIALIZABLE` met een herhaallus (DB-69).
- Bewijs: Per regel over meerdere rijen staat in de projectdocumentatie welk slot hem bewaakt. Test: 20 gelijktijdige verzoeken bij een stand van limiet min één leveren precies één toevoeging op (zie BIZ-50 voor de opzet). Codecontrole: elke `count(` of `sum(` gevolgd door een `insert` in dezelfde functie heeft een `.for('update')` op de ouder of `isolationLevel: 'serializable'`.
- Norm: ASVS 5.0.0 V2.3.4 (L2), V2.3.2 (L2), V15.4.2 (L3).
- Zie ook: API-30, BIZ-01, BIZ-03, BIZ-04, BIZ-05, BIZ-06, BIZ-07, BIZ-09, BIZ-44, BIZ-50

### BIZ-03 Gebruik advisory locks alleen op transactieniveau en met een vaste sleutelruimte
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor een applicatieslot `pg_advisory_xact_lock` binnen een transactie en nooit de sessievariant (`pg_advisory_lock`); leid de sleutel af uit een vaste naamruimte per doel plus het id, en leg die naamruimten op één plek vast.
- Bewijs: `grep -rnE "pg_(try_)?advisory_lock\(" src` is leeg (alleen `_xact_`-varianten). De naamruimten staan als constanten in één bestand. Controle op productie, alleen lezen: `SELECT count(*) FROM pg_locks WHERE locktype = 'advisory'` is nul als er geen verzoek loopt.
- Norm: ASVS 5.0.0 V15.4.3 (L3).
- Zie ook: API-30, BIZ-01, BIZ-02, BIZ-04, BIZ-05, BIZ-06, BIZ-07, BIZ-09, BIZ-44, BIZ-50

### BIZ-04 Leg "hoogstens één tegelijk actief" vast met een partiële unieke index
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg elke regel van de vorm "hoogstens één actieve X per Y" (één lopend abonnement per klant en pakket, één open betaling per bestelling, één lopende taak per domein, één standaardadres per contact) vast met een unieke index met een `WHERE`-voorwaarde op de status.
- Bewijs: `\d+ <tabel>` toont de partiële unieke index voor elke regel van deze vorm die in de documentatie staat. Test: twee gelijktijdige aanmaakverzoeken geven één rij en één nette weigering (409). Voeg de index op een gevulde tabel toe volgens DB-33 en DB-37.
- Norm: ASVS 5.0.0 V2.3.4 (L2), V2.3.2 (L2).
- Zie ook: API-30, BIZ-01, BIZ-02, BIZ-03, BIZ-05, BIZ-06, BIZ-07, BIZ-09, BIZ-44, BIZ-50

### BIZ-05 Een unieke sleutel met een kolom die NULL kan zijn, houdt geen duplicaten tegen
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak elke kolom in een unieke sleutel die "één keer" moet afdwingen `NOT NULL`, of zet `NULLS NOT DISTINCT` op de constraint.
- Bewijs: Query op het schema: elke kolom in een unieke index is `NOT NULL` of de index heeft `indnullsnotdistinct = true` (`SELECT indexrelid::regclass, indnullsnotdistinct FROM pg_index WHERE indisunique`). Test: twee inserts met NULL in de sleutelkolom geven bij de tweede een fout.
- Norm: ASVS 5.0.0 V2.3.2 (L2).
- Zie ook: API-30, BIZ-01, BIZ-02, BIZ-03, BIZ-04, BIZ-06, BIZ-07, BIZ-09, BIZ-44, BIZ-50

### BIZ-06 Voorkom overlappende periodes en dubbele boekingen met een exclusion constraint
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg elke regel "geen twee tegelijk in dezelfde periode" (afspraak in een agenda, reservering van een tijdslot, twee abonnementsperiodes voor dezelfde dienst, twee prijsregels die tegelijk gelden) vast met een `EXCLUDE`-constraint op een bereiktype, niet met een zoekopdracht vooraf.
- Bewijs: `\d+ <tabel>` toont de exclusion constraint. Test: twee gelijktijdige boekingen van hetzelfde uur geven één rij en één fout met SQLSTATE `23P01`, die de code vertaalt naar 409. Aangrenzende periodes (eind van de een is begin van de ander) worden allebei geaccepteerd.
- Norm: ASVS 5.0.0 V2.3.4 (L2).
- Zie ook: API-30, BIZ-01, BIZ-02, BIZ-03, BIZ-04, BIZ-05, BIZ-07, BIZ-09, BIZ-44, BIZ-50

### BIZ-07 Weiger een bewerking op verouderde gegevens met een versienummer
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elk record dat door meer dan één partij kan worden bewerkt (mens en mens, mens en agent, mens en synchronisatie) een versiekolom, laat de wijziging de versie meesturen die hij heeft gelezen, schrijf met `WHERE id = $1 AND versie = $2` en `SET versie = versie + 1`, en antwoord bij nul rijen met 409 of 412 in plaats van te overschrijven.
- Bewijs: Elke tabel die via een formulier of een tool wordt bewerkt heeft een versiekolom (of gebruikt `updated_at` als voorwaarde). Test: lees twee keer, schrijf twee keer; de tweede schrijfactie geeft 409 en de eerste wijziging staat er nog. Voor een MCP-tool: de tool geeft de versie terug bij lezen en eist hem bij schrijven.
- Norm: ASVS 5.0.0 V2.3.3 (L2); RFC 9110 paragraaf 13.1.1; RFC 6585 paragraaf 3.
- Zie ook: API-30, BIZ-01, BIZ-02, BIZ-03, BIZ-04, BIZ-05, BIZ-06, BIZ-09, BIZ-44, BIZ-50

### BIZ-08 Laat factuurnummers en andere doorlopende reeksen niet uit een sequence komen
middel · hard · api | app | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Laat één systeem de factuurnummers uitgeven (bij Marketing Maatwerk: Moneybird) en neem dat nummer over; bouw je zelf een doorlopende reeks, gebruik dan een tellerrij die je in dezelfde transactie als de factuur met `UPDATE ... SET laatste = laatste + 1 RETURNING laatste` ophoogt, en geen `serial`, `identity` of `nextval`.
- Bewijs: `grep -rnE "serial|generatedAlwaysAsIdentity|nextval" src` raakt geen kolom die als factuur-, order- of bonnummer naar buiten gaat. Controlequery op productie, alleen lezen: het aantal facturen in een reeks is gelijk aan hoogste min laagste nummer plus één, en elk nummer komt één keer voor. Of dat gaten verboden zijn hangt van de situatie af: laat de boekhouder dat bevestigen (dit is geen fiscaal advies).
- Norm: Wet op de omzetbelasting 1968 artikel 35a lid 1 onder b; ASVS 5.0.0 V2.3.2 (L2).

### BIZ-09 Een slot in het geheugen van het proces is geen slot
middel · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewaak een bedrijfsregel nooit met een variabele, een `Map`, een `Set` of een mutex in het geheugen van het Node-proces; gebruik de database (BIZ-01 tot en met BIZ-06). Reken er ook binnen één proces op dat tussen elke `await` een ander verzoek dezelfde gegevens kan lezen.
- Bewijs: `grep -rnE "new (Map|Set)\(|let [a-zA-Z]+ = (0|\[\]|\{\})" src` op moduleniveau: elke treffer is een cache zonder gevolgen voor de uitkomst, of is gedocumenteerd. Dag- en maandlimieten staan in de database. De race-test draait tegen twee processen of tegen de echte dienst, niet tegen één geïmporteerde functie.
- Norm: ASVS 5.0.0 V15.4.1 (L3), V15.4.2 (L3).
- Zie ook: API-30, BIZ-01, BIZ-02, BIZ-03, BIZ-04, BIZ-05, BIZ-06, BIZ-07, BIZ-44, BIZ-50
