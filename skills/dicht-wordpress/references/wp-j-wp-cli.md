# WP J: WP-CLI

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-68 Draai WP-CLI als het account van de site, nooit als root
hoog · hard · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Voer WP-CLI uit als de gebruiker van het hostingaccount en gebruik `--allow-root` nooit op een server met meer dan één site of met andere diensten.
- Bewijs: `id -un` vóór het commando is het siteaccount; `grep -rn "allow-root" ` in eigen scripts (scanner, deploy, cron) is leeg. Afgevinkt met de grep.
- Norm: ASVS 5.0.0 V13.2.2 (L2).
- Zie ook: INFRA-66, INFRA-10, AUTH-56, DB-02, INFRA-97, WP-45, AI-21

### WP-69 Onderzoek een verdachte site zonder zijn code te laden
hoog · hard · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik op een site die mogelijk besmet is eerst commando's die WordPress niet laden (`wp core verify-checksums`, `find`, `grep`, `stat`), en laad WordPress daarna alleen met `--skip-plugins --skip-themes`, in het besef dat mu-plugins en drop-ins dan nog steeds laden.
- Bewijs: In het incidentverslag staan de eerste commando's met tijdstip: `wp core verify-checksums` (laadt WordPress niet), `ls -la wp-content/*.php wp-content/mu-plugins/`, en pas daarna commando's met `--skip-plugins --skip-themes`. Afgevinkt met het verslag.
- Norm: ASVS 5.0.0 V15.2.5 (L3) naar analogie; hoort bij incidentrespons (INFRA).

### WP-70 Weet dat wp eval een andere context heeft dan wp-admin
middel · richtlijn · klantproject | wp-plugin | wp-thema · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Reken er in `wp eval` en eigen WP-CLI-commando's op dat `is_admin()` onwaar is en dat er geen ingelogde gebruiker is; laad bestanden die achter `is_admin()` zitten zelf of gebruik `--context=admin`, en controleer bij een foutmelding eerst met curl of de site zelf nog werkt.
- Bewijs: In deploy- en controlescripts staat bij elke `wp eval` die beheercode aanroept `--context=admin` of een `require_once`; na elke deploy staat er een curl-controle op de voorpagina en wp-login naast de WP-CLI-controle. Afgevinkt met het script.
- Norm: geen ASVS-eis; voorkomt foute conclusies bij verificatie.

### WP-71 Zet geen wachtwoorden of sleutels op de commandoregel
middel · hard · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef een wachtwoord of sleutel nooit mee als argument aan WP-CLI (`wp user create ... --user_pass=...`, `wp config set ...`, `wp option update ...`); laat WordPress een resetlink sturen of lees de waarde uit een bestand of standaardinvoer.
- Bewijs: `grep -nE "user_pass=|config set .*(KEY|SECRET|PASS)" ~/.bash_history` op de server en in eigen scripts is leeg; nieuwe accounts zijn aangemaakt zonder wachtwoord in het commando en met `wp user reset-password <login>` of de standaardmail. Afgevinkt met de grep.
- Norm: ASVS 5.0.0 V13.3.1 (L2), V6.4.1 (L1).
- Zie ook: INFRA-72, API-65, GIT-32, GIT-95, DB-62, AI-28, WP-33, INFRA-76, DB-61, AI-60, ARCH-49
