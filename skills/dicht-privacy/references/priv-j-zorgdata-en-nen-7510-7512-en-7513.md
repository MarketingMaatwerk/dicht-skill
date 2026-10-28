# PRIV J: zorgdata en NEN 7510, 7512 en 7513

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-52 Stel vast voor wie de zorgnormen wettelijk gelden, en wat de klant dus van jou gaat eisen
hoog · hard · app | api | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Leg bij elk project met gezondheidsgegevens vast wie de zorgaanbieder is, of jouw systeem een zorginformatiesysteem of een elektronisch uitwisselingssysteem is, en dat NEN 7510, 7512 en 7513 via die zorgaanbieder als eis op de leverancier terechtkomen; behandel de normen dan als ontwerpeis vanaf dag één.
- Bewijs: In de projectdocumentatie (voor een zorgsysteem `docs/PRIVACY-SECURITY.md`): de kwalificatie van het systeem, de naam van de norm en de uitgave waartegen gebouwd wordt, en per norm de plek in de code of het proces. Afgevinkt als de kwalificatie er staat en door de klant of een jurist is bevestigd. `[jurist]` voor de kwalificatie van het systeem.
- Norm: Besluit elektronische gegevensverwerking door zorgaanbieders artikel 3, 5 en 7; Wabvpz artikel 15j; AVG artikel 9 en 32.

### PRIV-53 Tweefactorauthenticatie voor iedereen die bij patiëntgegevens kan
kritiek · hard · app | api | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Laat geen enkele gebruiker, beheerder of ondersteuner patiëntgegevens inzien zonder authenticatie met ten minste twee factoren, ook niet op het interne netwerk en ook niet via een beheer- of supportroute.
- Bewijs: De test uit AUTH-16 voor elke rol en elke route, inclusief impersonatie (AUTH-79) en directe databasetoegang: zonder tweede factor geen patiëntgegevens. Afgevinkt met de testuitvoer. Technisch af te dwingen.
- Norm: AVG artikel 32; NEN 7510-2 (beheersmaatregel beveiligde authenticatie; de tekst van de uitgave 2024 is niet gelezen); ASVS 5.0.0 V6.3.3 (L2).
- Zie ook: AUTH-16, AUTH-82, WP-58, INFRA-98, GIT-14, INFRA-11

### PRIV-54 Log elke inzage in een dossier, en bouw de controle op die logging mee
kritiek · hard · app | api | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Leg bij elke toegang tot, elke zoekactie in en elke uitwisseling van persoonlijke gezondheidsinformatie vast wie, wanneer, welke cliënt en welke actie, en lever een functie waarmee de zorgaanbieder die logging systematisch kan beoordelen (afwijkingen signaleren, niet alleen op klacht zoeken).
- Bewijs: (1) Een test per leesroute (scherm, API, export, AI-functie, supporttoegang) die na een inzage precies één logregel vindt met gebruiker, cliënt, tijdstip en actie. (2) De app-rol kan de logtabel niet wijzigen of wissen (de controle uit AUTH-84). (3) Een rapport of signalering voor inzage zonder behandelrelatie bestaat en is gedemonstreerd. Afgevinkt met de drie. Welke velden NEN 7513:2024 precies eist, is niet uit de normtekst bevestigd: leg de veldenlijst naast de norm zodra die is geopend.
- Norm: Besluit elektronische gegevensverwerking door zorgaanbieders artikel 5; NEN 7513:2024; Wabvpz artikel 15e; ASVS 5.0.0 V16.3.2 (L3-deel: toegang tot gevoelige gegevens loggen).
- Zie ook: ARCH-64, AUTH-84, ARCH-65, INFRA-89, DB-91, AI-52

### PRIV-55 Bewaar de logging van zorgsystemen ten minste vijf jaar
hoog · hard · app | api | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Stel de bewaartermijn van de NEN 7513-logging in op ten minste vijf jaar vanaf het schrijven van de logregel, sluit die logging uit van kortere algemene logrotatie, en neem haar mee in de back-up.
- Bewijs: De configuratie van de opruimjob en de logrotatie laat een aparte termijn van minimaal vijf jaar zien voor de dossierlogging; de back-upinhoud bevat de logtabel. Afgevinkt met de configuratie. Technisch af te dwingen. De bovengrens (het besluit noemt in de toelichting de bewaartermijn van het dossier) is `[jurist]`.
- Norm: Besluit van de Minister voor Medische Zorg van 27 juni 2019 (Stcrt. 2019, 38007); AVG artikel 5 lid 1 onder e.
- Zie ook: ARCH-71, PRIV-23, INFRA-88, INFRA-33

### PRIV-56 Bouw tegen de actuele uitgave van de normen en leg vast welke
middel · richtlijn · app | api | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Noteer in het project tegen welke uitgave gebouwd wordt (op 04-10-2026: NEN 7510-1:2024, NEN 7510-2:2024+A1:2026, NEN 7512:2022 en NEN 7513:2024), haal de normtekst op via NEN Connect, en controleer in de verversroutine of er een nieuwe uitgave of een mededeling in de Staatscourant is.
- Bewijs: De uitgaven staan met datum in de projectdocumentatie; de normteksten zijn opgehaald (kosteloos volgens NEN, via NEN Connect) en de regels PRIV-53 tot en met PRIV-55 zijn ernaast gelegd. Afgevinkt met de notitie. De datum waarop de uitgaven van 2024 voor het besluit gelden, is niet gevonden (zie "Niet bevestigd").
- Norm: Besluit elektronische gegevensverwerking door zorgaanbieders artikel 7.

### PRIV-57 Gebruik het BSN alleen als de wet het voorschrijft
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem geen veld voor het burgerservicenummer op en sla geen BSN op uit documenten of vrije tekst, tenzij een wet het gebruik voor dit doel voorschrijft (in de zorg: de zorgaanbieder op grond van de Wabvpz); als leverancier verwerk je het alleen in opdracht van zo'n partij.
- Bewijs: `grep -rniE "\bbsn\b|burgerservice|sofi" src/ migrations/` geeft niets, of alleen velden met een verwijzing naar de wet en de opdrachtgever in de classificatie (DB-87) en versleuteling per kolom (DB-80). Afgevinkt met de grep. Technisch af te dwingen.
- Norm: UAVG artikel 46; Wabvpz artikel 4 en 8; AVG artikel 87.

### PRIV-58 Ruim een zorgdossier niet op met de gewone bewaartermijn
hoog · hard · app | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Sluit gegevens die deel zijn van een medisch dossier uit van de algemene opruimjob en geef ze de termijn van de zorgaanbieder: twintig jaar vanaf de laatste wijziging, tenzij de zorgaanbieder iets anders opdraagt.
- Bewijs: De tabel met bewaartermijnen (DB-83) onderscheidt per gegevenssoort "dossier" (termijn van de zorgaanbieder) van "werkgegeven" (korte eigen termijn, met de reden), en een test laat zien dat de opruimjob een dossierrecord overslaat en een verlopen werkgegeven wist. Afgevinkt met tabel en test. Wat tot het dossier hoort, bepaalt de zorgaanbieder: `[jurist]`.
- Norm: BW artikel 7:454 lid 3; AVG artikel 5 lid 1 onder e.
