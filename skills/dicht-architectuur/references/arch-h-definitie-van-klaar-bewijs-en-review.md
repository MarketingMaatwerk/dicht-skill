# ARCH H: Definitie van klaar, bewijs en review

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-52 Een bouwtaak is klaar als de checklist van het projecttype is afgevinkt met bewijs
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Meld een bouwtaak pas als klaar wanneer elk punt van de checklist voor het projecttype (de sectie Checklist per projecttype in elk domein) is afgevinkt met het genoemde bewijs, of een vastgelegde uitzondering heeft (ARCH-30); zeg anders letterlijk wat nog niet is getoetst en waarom.
- Bewijs: Het bewijsbestand (ARCH-53) bevat per checklistpunt de status (voldaan, niet van toepassing met reden, uitzondering met verwijzing) en het bewijs of de plek waar het staat. Afgevinkt als geen punt leeg is.
- Norm: BRIEF besluit 2; NIST SSDF PO.4.1 en PO.4.2 (criteria voor beveiligingscontroles vastleggen en de gegevens ervoor verzamelen).
- Zie ook: ARCH-53, WP-84, WP-86

### ARCH-53 Schrijf het bewijs in één bestand met een vaste vorm
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf bij elke oplevering en elke uitrol één bestand `bewijs/<jjjj-mm-dd>-<korte hash>.md` in de repository (buiten de webroot) met een vaste kop (project, projecttype, commit, datum, wie, versies van runtime en hulpmiddelen, uitzonderingen) en per checklistpunt de regel-ID, de status en de letterlijke uitvoer of een verwijzing naar een bestand ernaast, zonder geheimen en zonder persoonsgegevens.
- Bewijs: Het bestand van de laatste uitrol bestaat, de commit erin is gelijk aan de commit die draait (ARCH-24), elk punt van de checklist komt erin voor, en een geheimscan op de map `bewijs/` is schoon. Afgevinkt met die vier controles. De volledige opzet staat in Open vragen, punt 1.
    Ook (uit GIT-67): Het bewijsbestand van de laatste oplevering bestaat en bevat de commit-hash die live staat. Afgevinkt met het bestand.
- Norm: NIST SSDF PO.3.3; BRIEF besluit 2 en 17.
- Dekt ook: GIT-67
- Zie ook: ARCH-52, WP-84, WP-86

### ARCH-54 Laat elke wijziging aan een kritiek deel nakijken door een tweede paar ogen
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke wijziging aan een kritiek deel, aan het uitrolscript of aan de gate nakijken door een reviewer die de wijziging niet schreef (een mens, of een review-agent in een schone context die de code en de eis krijgt en niet de conclusie), met een vaste checklist, en leg de bevindingen en wat ermee is gedaan vast bij de wijziging.
- Bewijs: Bij de merge staat een reviewnotitie met: wie of wat reviewde, de checklist met per punt de uitkomst, de bevindingen met ernst, en per bevinding "opgelost in commit X" of "geaccepteerd, reden". Voor werk dat door een model is geschreven geldt hetzelfde (AI-85). Afgevinkt met de notitie. De checklist: (1) doet het wat gevraagd is en niet meer, (2) invoer gevalideerd en uitvoer gefilterd, (3) autorisatie en tenantgrens op de server, (4) fouten falen gesloten, (5) geen geheimen of persoonsgegevens in code of logs, (6) tests bewijzen het gedrag en de randen, (7) migratie verenigbaar met de vorige build, (8) logging en alarm voor het nieuwe pad, (9) niets ingewikkelder dan nodig.
- Norm: NIST SSDF PW.7.1 en PW.7.2.
- Zie ook: GIT-13

### ARCH-55 Tel elke onderdrukking en geef haar een reden
middel · hard · api | app | mcp | wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Sta `@ts-ignore` en `@ts-nocheck` niet toe, sta `@ts-expect-error`, `eslint-disable`, `phpcs:ignore` en `@phpstan-ignore` alleen toe met een reden op dezelfde regel, en laat het totaal en de omvang van de PHPStan-baseline alleen dalen.
- Bewijs: De lintconfiguratie bevat `@typescript-eslint/ban-ts-comment` (standaard: `ts-ignore` en `ts-nocheck` worden gemeld, `ts-expect-error` mag met een beschrijving); de tellingen uit ARCH-32 staan in het bewijsbestand en zijn niet hoger dan de vorige keer. Afgevinkt met configuratie en telling. Zie API-68 voor de lintset, WP-37 voor `phpcs:ignore`.
- Norm: BRIEF besluit 10.
- Zie ook: ARCH-30, GIT-65

### ARCH-56 Volg in PHP-code de weg van invoer naar gevaarlijke functies met taint-analyse
middel · richtlijn · wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai op eigen plugin- en themacode naast PHPStan ook Psalm met `--taint-analysis`, en beoordeel elke gemelde stroom van gebruikersinvoer naar uitvoer, query, bestandspad of commando.
- Bewijs: `vendor/bin/psalm --taint-analysis` geeft nul meldingen, of elke melding is beoordeeld en met reden onderdrukt; de uitvoer zit in het bewijspakket (WP-84). Afgevinkt met de uitvoer. Of de standaardbronnen en -putten van Psalm de WordPress-functies (`$wpdb`, `esc_html`, `wp_kses`) herkennen, is niet nagelezen (zie Niet bevestigd 5).
- Norm: NIST SSDF PW.7.2 voorbeeld 4 (statische analyse met beoordeling door een mens).
- Zie ook: GIT-57, GIT-58, GIT-59, API-67, API-68, API-78, WP-37, ARCH-40, GIT-60, GIT-61, GIT-34, AI-85
