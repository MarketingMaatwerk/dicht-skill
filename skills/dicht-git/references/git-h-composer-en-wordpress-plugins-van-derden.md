# GIT H: Composer en WordPress-plugins van derden

Compacte regels van `dicht-git`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/git-supplychain.md` (regelnummer in `regel-index.tsv`).

### GIT-81 Composer: lockfile committen, installeren zonder dev en zonder verrassingen
hoog · hard · wp-plugin | wp-thema | klantproject | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Commit `composer.lock`, draai `composer validate` vóór elke commit van `composer.json`, en installeer voor productie met `composer install --no-dev` vanaf het lockfile; draai `composer update` alleen bewust en per pakket.
- Bewijs: `git ls-files composer.lock` geeft het bestand; `composer validate` is groen; het bouwscript of de Dockerfile bevat `composer install --no-dev`. Afgevinkt met de drie. Sinds 07-07-2026 zijn stabiele versies op Packagist onveranderlijk.
- Norm: ASVS 5.0.0 V15.2.1 (L1) en V15.2.4 (L3); OWASP Top 10 2025 A03.

### GIT-82 Houd Composer zelf bij en laat de ingebouwde blokkades aan
hoog · hard · wp-plugin | wp-thema | klantproject | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik Composer 2.10.3 of nieuwer, laat de standaardblokkade van onveilige en kwaadaardige versies aan staan (`policy.advisories.block` en `policy.malware.block`), en draai `composer audit --locked` in de gate.
- Bewijs: `composer --version` geeft 2.10.3 of hoger; `composer config policy` en `composer config audit` tonen geen uitgeschakelde blokkade; `composer audit --locked --no-dev` geeft exitcode 0. Afgevinkt met de drie. Gebruik de oude `audit.*`-sleutels en de nieuwe `policy.*`-sleutels niet door elkaar. `roave/security-advisories` is sinds 2.9 overbodig. Een wachttijd voor nieuwe versies staat sinds 01-10-2026 in de ontwikkeltak van Composer, maar zit niet in 2.10.3; gebruik tot die tijd de cooldown van Dependabot (GIT-76). De opdracht `composer config policy` is niet getest (niet bevestigd, punt 10).
- Norm: ASVS 5.0.0 V15.2.1 (L1); OWASP Top 10 2025 A03; NIST SSDF PO.3.2.

### GIT-83 Sta alleen benoemde Composer-plugins toe
middel · hard · wp-plugin | wp-thema | klantproject | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd `config.allow-plugins` in `composer.json` een expliciete lijst van pakketnamen, zet nooit `true` of een jokerteken, en installeer in CI met `--no-plugins --no-scripts` waar de build dat toelaat.
- Bewijs: `composer config allow-plugins` toont alleen benoemde pakketten met `true`. Afgevinkt met de uitvoer.
- Norm: OWASP CI/CD CICD-SEC-3.

### GIT-84 Beoordeel een WordPress-plugin of thema van een ander vóór installatie
hoog · hard · klantproject | website | wp-thema | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Installeer een plugin of thema van een derde pas na een korte beoordeling: status op wordpress.org (niet gesloten), laatste update en ondersteuning van de laatste drie WordPress-versies, aantal installaties, de lekkenhistorie (Patchstack of WPScan) en hoe snel die zijn opgelost, wie de eigenaar is en of die recent is gewisseld, en of het doel niet met bestaande middelen of twintig regels eigen code kan. Aanvulling uit WP-72: Leg per site vast welke plugin waarvoor dient en houd de lijst kort.
- Bewijs: Een notitie per nieuwe plugin met de zes punten en de datum, vastgelegd in het klantdossier (het CRM) of de repo. Afgevinkt met die notitie. Dit is de WordPress-vorm van GIT-75. Het updatebeleid en wat het breekt: WP.
    Ook (uit WP-72): `wp plugin list --fields=name,status,version,update --format=csv` per site, met in het CRM of de klantmap per plugin één regel "waarvoor"; een plugin die al langer dan een jaar geen update kreeg of die van wordpress.org is gehaald, heeft een besluit (vervangen of weg). De controle op bekende lekken loopt via WP-54. Afgevinkt met de lijst.
- Norm: NIST SSDF PW.4.1 en PW.4.4 (voorbeeld 4: nog actief onderhouden); ASVS 5.0.0 V15.1.2 (L2) en V15.2.1 (L1) (uit het samengevoegde WP-72), V15.1.4 (L3); OWASP Top 10 2025 A03.
- Dekt ook: WP-72
- Zie ook: WP-73, GIT-86, WP-51, GIT-87, WP-74, WP-75, WP-76, GIT-89

### GIT-85 → WP-73
Samengevoegd: "Haal plugins en thema's alleen bij de maker of wordpress.org" is gedekt door WP-73. Gebruik die regel.

### GIT-86 Houd per site een inventaris bij en vervang wat gesloten of verlaten is
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai per site minstens maandelijks `wp plugin list --fields=name,status,version,update,auto_update,wporg_status,wporg_last_updated` en `wp theme list`, vervang elke plugin die op wordpress.org gesloten is of langer dan een jaar niet is bijgewerkt, en verwijder wat inactief is.
- Bewijs: De uitvoer per site met datum; geen regel met een gesloten `wporg_status`; elke regel met een lege `wporg_status` (niet van wordpress.org) heeft een bron volgens GIT-85; geen inactieve plugins. Afgevinkt met de uitvoer. Wat de site zelf toont bij een gesloten plugin is niet bevestigd (punt 14); vertrouw daarom op deze opdracht en niet op het dashboard.
- Norm: ASVS 5.0.0 V15.1.2 (L2) en V15.2.3 (L2); OWASP Top 10 2025 A03 ("Monitor for libraries and components that are unmaintained").
- Zie ook: GIT-84, WP-73, WP-51, GIT-87, WP-74, WP-75, WP-76, GIT-89

### GIT-87 Controleer core en plugins tegen de controlesommen van wordpress.org
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai bij elke oplevering en bij elke verdenking `wp core verify-checksums` en `wp plugin verify-checksums --all`, en verklaar elke afwijking.
- Bewijs: De uitvoer van beide opdrachten zonder afwijkingen, of met een verklaring per bestand. Afgevinkt met de uitvoer. De controle werkt alleen voor wat op wordpress.org staat: premium-plugins en eigen plugins vallen erbuiten en vragen een vergelijking met het originele pakket of de eigen repo (`git status` in de pluginmap). `wp core verify-checksums` laadt WordPress niet.
- Norm: OWASP Top 10 2025 A08 Software or Data Integrity Failures; NIST SSDF PS.2.1.
- Zie ook: GIT-84, WP-73, GIT-86, WP-51, WP-74, WP-75, WP-76, GIT-89

### GIT-88 Beveiligingsupdates direct, de rest na een wachttijd
hoog · richtlijn · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Installeer een update die een lek dicht binnen de termijn van GIT-77 (kritiek binnen 48 uur), en laat een gewone update minstens 24 uur liggen en test hem eerst op een kopie bij sites met een winkel of maatwerk.
- Bewijs: Per site staat vast welk updatebeleid geldt (automatisch voor beveiliging, handmatig of vertraagd voor de rest) en het logboek van de laatste maand toont geen beveiligingsupdate die langer dan de termijn heeft gewacht. Afgevinkt met beleid en logboek. Of de wachttijd van wordpress.org nog geldt en of hij ook handmatige updates raakt, is niet bevestigd (punt 14). Uitwerking en wat automatische updates breekt (Installatron, InfiniteWP): WP.
- Norm: ASVS 5.0.0 V15.1.1 en V15.2.1 (L1); OWASP Top 10 2025 A03 ("Avoid deploying updates to all systems simultaneously").
- Zie ook: GIT-77, INFRA-24, ARCH-32, WP-49, DB-92, GIT-61, PRIV-73, MSG-06, SCR-32

### GIT-89 Behandel meegeleverde bibliotheken in een plugin of thema als afhankelijkheden
middel · hard · wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Beheer elke bibliotheek die een eigen plugin of thema meelevert (PHP via Composer, JavaScript via npm of als los bestand) met een lockfile of een lijst met naam, versie, bron en licentie, en scan de map met `osv-scanner` of `trivy fs`.
- Bewijs: De lijst of het lockfile bestaat; `/usr/bin/find . -name "*.min.js" -not -path "*/node_modules/*"` toont geen bestand zonder vermelding; de scan is groen. Afgevinkt met de drie. Bij levering via wordpress.org moeten ook meegeleverde bibliotheken GPL-compatibel zijn (GIT-105).
- Norm: ASVS 5.0.0 V15.1.2 (L2); OWASP Top 10 2025 A03 (alle componenten bijhouden, ook client-side).
- Zie ook: GIT-84, WP-73, GIT-86, WP-51, GIT-87, WP-74, WP-75, WP-76

### GIT-90 Lever een plugin of thema als schoon pakket uit de repo
middel · hard · wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw het zip-bestand van een plugin of thema met een script vanuit een getagde commit, met `composer install --no-dev` en zonder `.git`, tests, `node_modules`, `.env` en ontwikkelbestanden, en bewaar de SHA-256 van het pakket bij de release.
- Bewijs: `unzip -l <pakket>.zip | /usr/bin/grep -E "\.git/|node_modules/|tests?/|\.env|composer\.(json|lock)$"` toont alleen wat bewust mee moet; `sha256sum <pakket>.zip` staat in de release-notitie; de tag bestaat. Afgevinkt met de drie. `.gitattributes` met `export-ignore` en `git archive` zijn een gangbare manier; niet vandaag nagelezen (niet bevestigd, punt 10).
- Norm: ASVS 5.0.0 V15.2.3 (L2) en V13.4.1 (L1); NIST SSDF PS.2.1 en PS.3.1.
