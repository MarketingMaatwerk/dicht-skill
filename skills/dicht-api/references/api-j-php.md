# API J: PHP

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/api-code.md` (regelnummer in `regel-index.tsv`).

### API-75 Strikte types en strikte vergelijking in elk PHP-bestand
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Begin elk eigen PHP-bestand met `declare(strict_types=1);`, vergelijk altijd met `===` en `!==`, geef `in_array` en `array_search` de derde parameter `true`, en vergelijk geheimen met `hash_equals` (API-62).
- Bewijs: `grep -rL "declare(strict_types=1)" --include=*.php <eigen mappen>` is leeg. PHPStan met `phpstan-strict-rules` of een PHPCS-regel op `==` is groen.
- Norm: ASVS 5.0.0 V15.3.5 (L2).

### API-76 Laad nooit een bestand op basis van invoer
kritiek · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `include` en `require` alleen met vaste paden of met een sleutel die via een vaste tabel naar een pad wordt vertaald, en laat `allow_url_include` uit.
- Bewijs: `grep -rnE "(include|require)(_once)? *\(?.*\\$(_GET|_POST|_REQUEST|_COOKIE)" .` is leeg. `php -i | grep allow_url_include` toont Off.
- Norm: ASVS 5.0.0 V5.3.2 (L1).
- Zie ook: API-54, AI-46, WP-25, WEB-45, WP-29, INV-41, INV-34, SCR-15

### API-77 Lees superglobals op één plek en nooit `$_REQUEST`
middel · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Lees `$_GET`, `$_POST`, `$_COOKIE`, `$_SERVER` en `$_FILES` alleen aan de rand van de code, valideer daar naar een getypeerde waarde, en gebruik `$_REQUEST` niet.
- Bewijs: `grep -rn "\$_REQUEST" .` in eigen code is leeg. `grep -rnE "\\$_(GET|POST|COOKIE|SERVER|FILES)" .` toont alleen treffers in de invoerlaag. Zie WP voor `wp_unslash` en `sanitize_*`.
- Norm: ASVS 5.0.0 V15.3.7 (L2), V4.1.3 (L2).

### API-78 Statische analyse op PHP als gate
middel · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai PHPStan op eigen plugin- en themacode op minimaal niveau 8 (nieuw werk: `max`; in PHPStan 2.x is dat niveau 10) en laat de build falen op een melding; leg bestaande meldingen bij oud werk vast in een baseline.
- Bewijs: `vendor/bin/phpstan analyse --level 8` (met `szepeviktor/phpstan-wordpress` voor WordPress-stubs) is groen in CI. `phpstan.neon` staat in de repository.
- Norm: besluit 10 van Marketing Maatwerk; ASVS 5.0.0 V15.3.5 (L2).
- Zie ook: GIT-57, GIT-58, GIT-59, API-67, API-68, WP-37, ARCH-40, ARCH-56, GIT-60, GIT-61, GIT-34, AI-85

### API-79 Productie-instellingen van PHP tonen geen fouten
hoog · hard · website | wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in productie `display_errors = Off`, `display_startup_errors = Off`, `log_errors = On`, `expose_php = Off`, `html_errors = Off` en `zend.exception_ignore_args = On`.
- Bewijs: `php -i | grep -E "display_errors|expose_php|log_errors|exception_ignore_args"` of de PHP-instellingen in Enhance tonen deze waarden. `curl -sI` toont geen `X-Powered-By`. Zie WP voor `WP_DEBUG_DISPLAY`.
- Norm: ASVS 5.0.0 V13.4.2 (L2), V13.4.6 (L3), V16.5.1 (L2).
- Zie ook: WEB-62, API-10, API-11, WP-40, ARCH-72

### API-80 → GIT-93, WP-52
Samengevoegd: "Draai op een ondersteunde PHP-versie" is gedekt door GIT-93, WP-52. Gebruik die regel.

### API-81 Zet geen ontwikkelgereedschap en geen `vendor/` in de webroot
kritiek · hard · website | wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Installeer op productie met `composer install --no-dev`, houd `vendor/`, tests, `.git`, `composer.json` en losse hulpscripts buiten de webroot of blokkeer ze in de webserver, en lever een plugin zonder ontwikkelbestanden.
- Bewijs: `curl -sI https://<site>/wp-content/plugins/<plugin>/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php`, `/.git/HEAD` en `/composer.json` geven 403 of 404. Het releasepakket van de plugin bevat geen `tests/`, `node_modules/` of dev-afhankelijkheden.
- Norm: ASVS 5.0.0 V13.4.1 (L1), V15.2.3 (L2), V13.4.7 (L3).
- Zie ook: WEB-64, ARCH-05, WP-63, WP-41, API-25
