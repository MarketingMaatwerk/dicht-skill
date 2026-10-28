# ARCH G: Testdata en geheimen in tests

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-48 Gebruik in tests alleen verzonnen gegevens
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw testgegevens met fabrieken of vaste bestanden met verzonnen namen, adressen en nummers, en zet nooit een export van productie, een echte mail of een echt klantdocument in de repository of de testmap.
- Bewijs: `git grep -nIE "@(gmail|hotmail|outlook|ziggo|kpnmail)\.|\b06[- ]?[0-9]{8}\b" -- test tests e2e fixtures` is leeg of elke treffer is aantoonbaar verzonnen; testadressen staan op het eigen domein (ARCH-50). Afgevinkt met de grep. Voor een kopie van productie in de proefmigratie geldt DB-85 (maskeren) en DB-39.
- Norm: ASVS 5.0.0 V14.2.4 (L2); NIST SSDF PO.5.1; AVG artikel 5 lid 1 onder c (zie PRIV).
- Zie ook: DB-85, INFRA-74, ARCH-50, ARCH-08, WEB-72

### ARCH-49 Geef tests eigen geheimen en houd inlogtoestanden uit git
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik in tests en in CI alleen sleutels van een test- of sandboxomgeving (Mollie-testsleutel, een eigen testdatabase met een eigen rol, een eigen testaccount), nooit een productiegeheim, en zet de map met opgeslagen inlogtoestanden van Playwright in `.gitignore`.
- Bewijs: `git check-ignore playwright/.auth` geeft het pad terug; `.env.test` staat in `.gitignore` en bevat alleen testsleutels (Mollie: voorvoegsel `test_`); de geheimscan over de hele geschiedenis is schoon (GIT-34). Afgevinkt met de drie controles.
- Norm: ASVS 5.0.0 V13.3.1 (L2); NIST SSDF PO.5.1.
- Zie ook: INFRA-72, API-65, GIT-32, GIT-95, DB-62, AI-28, WP-33, INFRA-76, WP-71, DB-61, AI-60

### ARCH-50 Laat tests geen echte mail, betaling of oproep naar buiten sturen
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Vervang in unit- en integratietests elke externe dienst door een nagebootste versie en laat een onverwachte uitgaande aanroep de test breken; gebruik in e2e-tests die echt mail versturen alleen adressen op het eigen domein in de vorm `ztest-<doel>-<willekeurig>@example.com`.
- Bewijs: De testopzet blokkeert uitgaand verkeer buiten `127.0.0.1` (een onderschepper die bij een onbekende host een fout gooit); `grep -rn "example\.com\|example\.org" test e2e` is leeg voor adressen waar echt naar gemaild wordt; na de e2e-run zijn de testrecords op exacte ID's verwijderd. Afgevinkt met de opzet en de grep.
- Norm: NIST SSDF PO.5.1.
- Zie ook: ARCH-48, DB-85, INFRA-74, ARCH-08, WEB-72

### ARCH-51 Beperk een test op productie tot lezen, of markeer en ruim op met exacte id's
hoog · hard · alles · eigen bron · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai op productie alleen een rooktest die leest, of een test die zijn eigen herkenbare records aanmaakt, de id's bij het aanmaken bewaart en precies die id's weer verwijdert; gebruik nooit een lijst met een filter als bron voor een verwijderlus.
- Bewijs: Het testscript bewaart de id's in een variabele of bestand en de opruimstap gebruikt alleen die (`wp post delete <id>`, `DELETE ... WHERE id = ANY($1)`); het aantal verwijderde rijen is gelijk aan het aantal aangemaakte. Afgevinkt met het script en de telling. Zie ARCH-28.
- Norm: ASVS 5.0.0 V15.2.3 (L2).
- Eigen bron: geen primaire bron; de eis is een les uit twee eigen incidenten (eigen ervaring); ASVS V15.2.3 gaat over iets anders. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Zie ook: ARCH-28, SCR-15, SCR-47
