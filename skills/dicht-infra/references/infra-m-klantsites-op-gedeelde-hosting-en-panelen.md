# INFRA M: Klantsites op gedeelde hosting en panelen

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-97 Geef elke site een eigen systeemgebruiker en een eigen database
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet elke klantsite onder een eigen systeemaccount met een eigen databasegebruiker, en zet nooit twee sites van verschillende klanten onder één account.
- Bewijs: Per site de systeemgebruiker (uit de panel-API of `stat -c %U <webroot>`) en de databasegebruiker uit de configuratie; geen twee sites delen een van beide; `ls` van een andere site vanuit het account mislukt. Afgevinkt met de lijst en de proef.
- Norm: ASVS 5.0.0 V13.2.2 (L2).
- Zie ook: INFRA-66, INFRA-10, AUTH-56, DB-02, WP-45, WP-68, AI-21

### INFRA-98 Bescherm het panel met een tweede factor en beperk API-tokens
kritiek · hard · klantproject | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet een tweede factor op elk account van het hostingpanel, de registrar en het DNS-beheer, geef API-tokens de kleinste rol, en beperk ze tot de IP-adressen van de eigen server.
- Bewijs: Per account een bevestiging van de tweede factor; per token de rol en de IP-beperking; een aanroep met het token vanaf een ander adres geeft een weigering (bij Enhance: 401 `admin_lockdown_restriction`). Afgevinkt met de lijst en de proef.
- Norm: ASVS 5.0.0 V13.2.1 (L2), V13.3.2 (L2); voor de tweede factor: zie AUTH.
- Zie ook: AUTH-16, AUTH-82, WP-58, GIT-14, PRIV-53, INFRA-11

### INFRA-99 Weet voor elke ingreep welke back-up je terugweg is
hoog · hard · klantproject | website · eigen bron · tegenlezer: niet te bevestigen (04-10-2026)
- Regel: Controleer vóór elke risicovolle wijziging op een klantsite dat er een geslaagde back-up van bestanden en database bestaat van vóór de wijziging, en noteer welke.
- Bewijs: De uitvoer van de back-uplijst van het panel (bij Enhance: `GET /api/orgs/{org}/websites/{ws}/backups` met `homeDirStatus` en `mysqlDbsStatus`) met de gekozen snapshot en het tijdstip, genoteerd bij de wijziging. Afgevinkt met de uitvoer.
- Norm: geen ASVS-eis.
- Eigen bron: geen primaire bron; bron is alleen eigen meting (eigen ervaring). Opgenomen op besluit van Marketing Maatwerk (04-10-2026).

### INFRA-100 Controleer elke beheerde site dagelijks op wijzigingen en bekende sporen
hoog · hard · klantproject · eigen bron · tegenlezer: niet te bevestigen (04-10-2026)
- Regel: Laat voor elke site met hosting of onderhoud een dagelijkse controle draaien op: kernbestanden tegen checksums, nieuwe PHP-bestanden op plekken waar alleen data hoort, onbekende beheerdersaccounts, automatisch geladen bestanden, en publiek bereikbare back-up- en dumpbestanden; en maak alleen bij een nieuwe treffer een taak.
- Bewijs: De lijst van beheerde sites uit de panel-API (niet uit een eigen lijst die kan achterlopen) naast de lijst van gescande sites: ze zijn gelijk of het verschil is een besluit; het log van de laatste nachtrun; een proef met een onschuldig testbestand dat de controle vindt. Afgevinkt met de vergelijking, het log en de proef.
- Norm: ASVS 5.0.0 V13.4.1 (L1) en V13.4.7 (L3) voor de publieke bestanden; OWASP Top 10 2025 A08 Software or Data Integrity Failures (categorie niet vandaag nagelezen, zie WEB voor de Top 10).
- Eigen bron: geen primaire bron; bron is alleen eigen meting (eigen ervaring). Opgenomen op besluit van Marketing Maatwerk (04-10-2026).

### INFRA-101 Test elke afscherming op de webserver die er echt draait
hoog · hard · klantproject | website · eigen bron · tegenlezer: niet te bevestigen (04-10-2026)
- Regel: Stel per site vast welke webserver hem serveert (met `dig` en de `server`-header van het echte adres) en bewijs elke blokkade, redirect en header met een aanvraag van buiten, meerdere keren.
- Bewijs: Per site: `dig +short <domein>`, de `server`-header, en per afscherming een `curl` van buiten met de verwachte statuscode, vergeleken met een niet-bestaand pad (dat 404 hoort te geven). Afgevinkt met de uitvoer. Zie WEB-23 en WEB-64.
- Norm: ASVS 5.0.0 V13.4.3 (L2), V13.4.7 (L3).
- Eigen bron: geen primaire bron; bron is alleen eigen meting (drie geheugenbestanden); documentatie van LiteSpeed over `.htaccess` is niet gevonden. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).

### INFRA-102 Weet vooraf wie de logs en de firewall van de hosting beheert
middel · richtlijn · klantproject · eigen bron · tegenlezer: scherpen (04-10-2026)
- Regel: Leg per hostingomgeving vast welke logs je zelf kunt inzien, welke alleen de hostingpartij heeft, hoe lang ze bewaard worden en hoe je ze opvraagt, en doe hetzelfde voor firewall en IP-blokkades.
- Bewijs: Een tabel per omgeving (eigen VPS, elke hostingnode, externe hosts) met logs, bewaartermijn, firewall en contactweg. Afgevinkt met de tabel.
- Norm: ASVS 5.0.0 V16.1.1 (L2).
- Eigen bron: geen primaire bron; het deel over firewall en IP-blokkades heeft alleen een eigen meting als bron (eigen ervaring); het logdeel rust op ASVS 5.0.0 V16.1.1. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).

### INFRA-103 Ruim op wat een project op de hosting achterlaat
middel · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwijder bij oplevering en bij elke controle: oude staging- en testinstallaties, ongebruikte FTP- en SSH-accounts, tijdelijke hulpprogramma's en scripts, losse CLI-installaties, en back-up- of migratiebestanden in de webroot.
- Bewijs: Per site: `find <webroot> -maxdepth 3 \( -name '*.wpress' -o -name '*.sql' -o -name '*.zip' -o -name '*.bak' -o -name 'wp-cli.phar' \)` met elk resultaat verklaard; de lijst van accounts en sleutels uit het panel (INFRA-08); de lijst van domeinen zonder staging-resten. Op een live klantsite alleen verwijderen na akkoord. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V15.2.3 (L2), V13.4.1 (L1).

### INFRA-104 Meet dat updates op een klantsite echt worden toegepast
hoog · hard · klantproject · eigen bron · tegenlezer: niet te bevestigen (04-10-2026)
- Regel: Controleer per beheerde site de werkelijke versie van kern, plugins en thema's tegen de nieuwste, buiten het updatemechanisme van de site zelf om.
- Bewijs: Per site de versie van de kern naast het antwoord van de officiële versiecontrole, en de pluginlijst met versies, gemeten met de verbergende plugin uitgeschakeld voor dat commando. Afgevinkt met de uitvoer. De uitwerking (commando's en updatebeleid) staat in WP.
- Norm: ASVS 5.0.0 V15.2.1 (L1).
- Eigen bron: geen primaire bron; bron is alleen eigen meting (eigen ervaring). Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
