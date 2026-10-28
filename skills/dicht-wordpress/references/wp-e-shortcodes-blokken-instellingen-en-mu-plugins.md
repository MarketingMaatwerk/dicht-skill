# WP E: Shortcodes, blokken, instellingen en mu-plugins

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-30 Behandel shortcode-attributen als invoer van een gebruiker met weinig rechten
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Haal attributen door `shortcode_atts()` met vaste standaardwaarden, valideer elke waarde, escape elke waarde bij uitvoer en geef de HTML terug met `return`.
- Bewijs: Per shortcode een test die als gebruiker met de rol bijdrager een bericht opslaat met `" onmouseover="alert(1)` en `javascript:alert(1)` in elk attribuut, en in de weergave geen handler en geen `javascript:` terugziet. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V1.2.1 (L1), V1.2.2 (L1).

### WP-31 Escape blokattributen in de render-callback
hoog · hard · wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Behandel `$attributes` en `$content` in de `render_callback` of `render.php` van een dynamisch blok als invoer: valideer tegen het schema in `block.json`, escape bij uitvoer en bouw de wrapper met `get_block_wrapper_attributes()`.
- Bewijs: Per dynamisch blok een test die via de REST API (`POST /wp/v2/posts` als auteur) een bericht opslaat met gemanipuleerde attributen in de blokcommentaar en in de weergave geen handler, script of onverwachte tag ziet. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V1.2.1 (L1), V2.2.2 (L1).

### WP-32 Registreer instellingen en meta met een sanitize- en een auth-callback
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Registreer elke optie met `register_setting()` en een `sanitize_callback`, registreer meta met `register_meta()` of `register_post_meta()` met `sanitize_callback` en `auth_callback`, en zet `show_in_rest` alleen aan voor waarden die elke lezer van het bericht mag zien.
- Bewijs: `grep -rn "register_setting\|register_meta\|register_post_meta" .`: elke aanroep heeft een `sanitize_callback`; elke `show_in_rest` staat op een lijst met de reden; `curl -s https://site/wp-json/wp/v2/<type>/<id> | jq .meta` toont anoniem geen interne velden. Plugin Check meldt niets bij "Setting sanitization". Afgevinkt met grep en curl.
- Norm: ASVS 5.0.0 V2.2.1 (L1), V8.2.3 (L2), V15.3.1 (L1).
- Zie ook: AUTH-65, API-02, INV-47, INV-46, INV-13

### WP-33 Bewaar geheimen in wp-config of de omgeving, niet in een optie die iedereen kan lezen
middel · richtlijn · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet API-sleutels van eigen bouw als constante in `wp-config.php` of als omgevingsvariabele, toon een opgeslagen sleutel nooit terug in een instellingenscherm, en zet nooit een sleutel in een bestand van de plugin of het thema.
- Bewijs: `gitleaks detect` op de plugin- of themamap is schoon (zie GIT); `wp option list --search='*key*' --fields=option_name` en `--search='*secret*'` tonen geen sleutels van eigen bouw; het instellingenscherm toont een bestaande sleutel als "ingesteld" en niet als waarde. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V13.3.1 (L2).
- Zie ook: INFRA-72, API-65, GIT-32, GIT-95, DB-62, AI-28, INFRA-76, WP-71, DB-61, AI-60, ARCH-49

### WP-34 Beheer een mu-plugin als code met een bron, een versie en een eigenaar
middel · hard · klantproject | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in `wp-content/mu-plugins` alleen bestanden die uit een eigen repository komen, met een versie in de kop, als één los PHP-bestand per functie, en vergelijk bij elke controle de bestanden op de server met de bron.
- Bewijs: `ls -la wp-content/mu-plugins/` per site komt overeen met de lijst in de klantbron; `diff` of `sha256sum` van elk bestand tegen de repository is leeg of gelijk. Afgevinkt met de uitvoer per site.
- Norm: ASVS 5.0.0 V15.2.3 (L2), V15.1.2 (L2).

### WP-35 Maak geplande taken herhaalbaar en reken niet op het tijdstip
laag · richtlijn · wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf elke WP-Cron-taak zo dat hij twee keer of te laat mag draaien zonder schade, en zet op sites waar taken ertoe doen (updates, opruimen, betalingen nalopen) `DISABLE_WP_CRON` aan met een echte cron die `wp cron event run --due-now` aanroept.
- Bewijs: `wp cron event list --fields=hook,next_run_relative` toont geen taken die ver over tijd zijn; Site Health meldt geen fout bij geplande gebeurtenissen. Afgevinkt met de uitvoer.
- Norm: geen ASVS-eis; hoort bij de betrouwbaarheid van WP-47.

### WP-36 Laad niets uit de kern opnieuw en geen code van een externe server
middel · hard · wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik de bibliotheken die WordPress meelevert (jQuery, PHPMailer, SimplePie) in plaats van een eigen kopie, laad geen uitvoerbare code van een server van derden, en bouw geen eigen updatemechanisme in een plugin.
- Bewijs: Plugin Check meldt niets bij "Offloading files", "Plugin updater" en bij bibliotheken die al in de kern zitten; `grep -rnE "wp_enqueue_(script|style)\(.*https?://" .` toont geen externe host zonder besluit en SRI (WEB-58). Afgevinkt met de Plugin Check-uitvoer en grep.
- Norm: ASVS 5.0.0 V15.2.4 (L3), V15.1.2 (L2).

### WP-37 Maak PHPCS met de WordPress-regels, Plugin Check en PHPStan een gate
hoog · hard · wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat bij elke eigen plugin en elk eigen thema in CI en vóór elke oplevering PHPCS draaien met `WordPress-Extra` (in elk geval de sniffs onder `WordPress.Security` en `WordPress.DB`), Plugin Check, en PHPStan met de WordPress-stubs, en lever niet op bij een fout.
- Bewijs: De uitvoer van `vendor/bin/phpcs` (nul fouten), `wp plugin check <slug>` op een testinstallatie (geen fouten in de categorie beveiliging) en `vendor/bin/phpstan analyse` (zie API-78) zit bij de oplevering; het aantal `phpcs:ignore`-regels is geteld en elke regel heeft een reden. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V15.1.1 (L1) en de eisen achter de afzonderlijke sniffs.
- Zie ook: GIT-57, GIT-58, GIT-59, API-67, API-68, API-78, ARCH-40, ARCH-56, GIT-60, GIT-61, GIT-34, AI-85
