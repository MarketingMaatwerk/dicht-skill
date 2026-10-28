# BIZ G: afstemming tussen systemen

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/bedrijfslogica-gelijktijdigheid.md` (regelnummer in `regel-index.tsv`).

### BIZ-46 Wijs per feit één bron aan en sla elk extern id uniek op
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per project vast welk systeem de waarheid is voor elk feit (bij Marketing Maatwerk: is er betaald: Mollie; welke factuur met welk nummer: Moneybird; waar heeft de klant recht op: de eigen database; bestaat de dienst: het hostingpaneel of de registry), sla het id van het andere systeem op in een kolom met een unieke constraint, en neem een beslissing over een feit altijd op de stand van zijn bron.
- Bewijs: De tabel staat in het architectuurdocument. `SELECT indexdef FROM pg_indexes` toont een unieke index op elk extern id. Codecontrole: geen leverbeslissing leest alleen de eigen status zonder dat die door API-36 uit de bron is bijgewerkt.
- Norm: ASVS 5.0.0 V2.2.3 (L2), V2.3.3 (L2); OWASP API Top 10 2023 API10. Zie API-36, API-37, API-50.
- Zie ook: API-31, BIZ-30, BIZ-34, BIZ-35, BIZ-39, BIZ-41, BIZ-43, API-33, DB-68, BIZ-48, BIZ-49, API-43, BIZ-51

### BIZ-47 Opzeggen, terugbetalen en stoppen raken elk systeem dat de klant kent
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf voor elke beëindiging (opzegging, terugbetaling, chargeback, niet-betaalde verlenging) één functie die alle gevolgen als taken vastlegt: de incasso of het abonnement bij Mollie stoppen, de periodieke factuur in Moneybird uitzetten, de dienst bij de leverancier stoppen of laten aflopen, de vergoeding intrekken (BIZ-16), en bewijs met een test dat er na de einddatum niets meer wordt geïncasseerd of gefactureerd.
- Bewijs: Test met nagebootste diensten: na `beeindig()` staan er taken voor Mollie, Moneybird en de leverancier, elk idempotent (BIZ-41) en met de uitkomst "onbekend" afgehandeld (BIZ-40). Test met de klok na de einddatum: de verlengingsjob (BIZ-30) en de factuurjob slaan de klant over. De dagelijkse afstemming (BIZ-48) meldt een actieve incasso of periodieke factuur bij een beëindigde klant. Bij Marketing Maatwerk bestaat hiervoor al een timer die periodieke facturen uitzet; die hoort in deze test.
- Norm: ASVS 5.0.0 V2.3.3 (L2), V2.3.1 (L1). Zie API-32, API-42, ARCH-20.
- Zie ook: API-42, BIZ-15, BIZ-16, BIZ-22, BIZ-36

### BIZ-48 Stem elke dag in drie richtingen af en alarmeer op elk verschil
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een dagelijkse taak, die alleen leest, de eigen database vergelijken met Mollie en Moneybird en elk verschil melden: bij Mollie betaald zonder eigen bestelling of levering; eigen levering zonder betaling bij Mollie; betaling zonder factuur of met meer dan één factuur; een bedrag dat in centen afwijkt; een terugbetaling of chargeback bij Mollie die de eigen database niet kent; een beëindigde klant met een lopende incasso (BIZ-47).
- Bewijs: De taak bestaat, draait dagelijks, en schrijft per controle het aantal vergeleken en het aantal afwijkende rijen. Nul afwijkingen wordt ook gelogd (een taak die niets meldt en een taak die niet draait zien er anders hetzelfde uit; zie ARCH-69). Test: zet in de testdatabase een bestelling op betaald zonder betaling in de nagebootste Mollie-API; de taak meldt hem. De vergelijking gebruikt centen (BIZ-11) en de Nederlandse datum (BIZ-27).
- Norm: ASVS 5.0.0 V2.2.3 (L2), V2.3.2 (L2). Zie API-43, ARCH-85.
- Zie ook: BIZ-49, API-43, BIZ-46, BIZ-51, BIZ-41

### BIZ-49 Laat de afstemming melden en alleen via de gewone verwerking herstellen
middel · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een afstemmings- of hersteltaak nooit zelf statussen zetten, bedragen aanpassen, facturen maken of geld terugsturen; hij mag alleen de bestaande idempotente verwerkingsfunctie opnieuw aanroepen voor een gemist signaal (API-43), en maakt voor elk verschil in geld een taak voor een mens.
- Bewijs: `grep -rnE "update|insert|delete" ` in de afstemmingsmodule toont alleen schrijven naar de eigen rapportage- of taaktabel. De taak draait met een databaserol zonder schrijfrechten op de kerntabellen (DB-05) of heeft een proefstand die standaard aan staat (ARCH-28). Test: een gemiste betaling wordt hersteld via dezelfde functie als de webhook en levert één keer.
- Norm: ASVS 5.0.0 V2.3.1 (L1), V2.3.3 (L2). Zie API-43, ARCH-28, ARCH-86.
- Zie ook: BIZ-48, API-43, BIZ-46, BIZ-51, BIZ-41
