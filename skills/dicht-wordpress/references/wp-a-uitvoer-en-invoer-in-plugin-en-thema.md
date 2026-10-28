# WP A: Uitvoer en invoer in plugin en thema

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-01 Escape elke uitvoer laat, met de functie die bij de context hoort
kritiek · hard · wp-plugin | wp-thema | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Escape elke dynamische waarde op de regel waar hij wordt uitgevoerd: `esc_html()` voor tekst in een element, `esc_attr()` voor een attribuut, `esc_url()` voor een URL, `esc_textarea()` in een textarea, en `wp_kses()` of `wp_kses_post()` als er HTML in mag staan.
- Bewijs: `vendor/bin/phpcs --standard=WordPress-Extra --sniffs=WordPress.Security.EscapeOutput .` geeft nul fouten; elke `phpcs:ignore` voor deze sniff heeft een reden op dezelfde regel. Daarnaast een test die in elk veld `"'><svg onload=alert(1)>` opslaat en de waarde gecodeerd terugziet in de HTML van de voorkant en van wp-admin. Afgevinkt met de phpcs-uitvoer en de testuitvoer.
- Norm: ASVS 5.0.0 V1.2.1 (L1); OWASP Top 10 2025 A05 Injection.
- Zie ook: WEB-01, WP-02, WP-03, WEB-06, MSG-17, INV-25, INV-35

### WP-02 Gebruik esc_url voor elke URL, ook in een attribuut
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Haal elke URL in `href`, `src`, `action` en `formaction` door `esc_url()`, sla URL's op met `esc_url_raw()`, en gebruik nooit `esc_attr()` als vervanging.
- Bewijs: `grep -rnE "(href|src|action)=\"<\?php echo esc_attr" .` is leeg; een test met `javascript:alert(1)` in elk URL-veld geeft een lege of onschadelijke `href`. Let op: de standaardlijst van `wp_allowed_protocols()` bevat naast `http` en `https` ook onder meer `ftp`, `mailto`, `tel`, `sms`, `telnet` en `gopher`; geef voor een veld dat alleen een weblink mag zijn de tweede parameter mee: `esc_url( $url, array( 'https' ) )`.
- Norm: ASVS 5.0.0 V1.2.2 (L1).
- Zie ook: WEB-01, WP-01, WP-03, WEB-06, MSG-17, INV-25, INV-35

### WP-03 Geef data aan JavaScript door als JSON met JSON_HEX_TAG of via de script-API
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef serverdata door met `wp_localize_script()`, of met `wp_add_inline_script()` en `wp_json_encode( $data, JSON_HEX_TAG | JSON_HEX_AMP )`, en gebruik `esc_js()` alleen voor een tekst tussen enkele aanhalingstekens in een inline handler.
- Bewijs: `grep -rn "wp_json_encode\|json_encode" . | grep -v HEX_TAG` toont alleen aanroepen die niet in HTML of een scriptblok belanden (REST-antwoorden, opslag); een test met `</script><svg onload=alert(1)>` in een doorgegeven veld laat in de paginabron geen sluitende scripttag in het datablok zien. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V1.2.3 (L1).
- Zie ook: WEB-01, WP-01, WP-02, WEB-06, MSG-17, INV-25, INV-35

### WP-04 Sta HTML alleen toe via wp_kses met een eigen, korte allowlist
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Toon HTML uit een niet-vertrouwde bron (formulier, import, mail, model, externe API) alleen via `wp_kses()` met een eigen lijst van tags en attributen, en gebruik `wp_kses_post()` alleen voor inhoud die dezelfde vrijheid mag hebben als een bericht.
- Bewijs: Per uitvoerpunt met `wp_kses*` staat in de code of de review welke bron de waarde heeft en waarom die lijst past; een test met `<img src=x onerror=alert(1)>`, `<a href="javascript:alert(1)">` en `<style>` geeft uitvoer zonder handler, zonder `javascript:` en zonder `style`. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V1.3.1 (L1).
- Zie ook: WEB-03, AI-13, WEB-07, INV-22, INV-23, INV-24, INV-26, MSG-23

### WP-05 Escape ook vertaalde teksten
middel · richtlijn · wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `esc_html__()`, `esc_html_e()`, `esc_attr__()` en `esc_attr_e()` in plaats van `__()` en `_e()` op elke plek waar de vertaling in HTML terechtkomt.
- Bewijs: De sniff `WordPress.Security.EscapeOutput` meldt ongeëscapete `__()` en `_e()` als fout; phpcs is groen. Afgevinkt met de phpcs-uitvoer van WP-01.
- Norm: ASVS 5.0.0 V1.2.1 (L1).

### WP-06 Lees invoer in drie stappen: unslash, valideren, dan pas gebruiken
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Haal elke waarde uit `$_GET`, `$_POST`, `$_COOKIE` en `$_SERVER` eerst door `wp_unslash()`, valideer hem daarna tegen een vaste lijst of een formaat met strikte vergelijking, en gebruik een `sanitize_*`-functie alleen waar valideren niet kan.
- Bewijs: `phpcs --sniffs=WordPress.Security.ValidatedSanitizedInput .` is groen (de sniff meldt ontbrekende `isset`, ontbrekende `wp_unslash` en ontbrekende sanitizing afzonderlijk); `grep -rn "in_array(" . | grep -v "true )"` toont geen vergelijking met invoer. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V2.2.1 (L1), V2.2.2 (L1), V15.3.5 (L2).

### WP-07 Zet wp_slash om de waarde bij het opslaan van meta en berichten
middel · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef een waarde met backslashes (JSON, reguliere expressies, Windows-paden, meerregelige tekst) aan `add_post_meta()`, `update_post_meta()`, de overige meta-functies en `wp_insert_post()` door via `wp_slash()`.
- Bewijs: Een test die een waarde met een regeleinde, een aanhalingsteken en een backslash opslaat en byte voor byte gelijk terugleest. `update_option()` haalt geen `wp_unslash()` over de waarde (in `wp-includes/option.php` komt de functie niet voor); gebruik daar dus geen `wp_slash()`. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V2.2.1 (L1) voor de integriteit van opgeslagen invoer.

### WP-08 Laat geen PHP-bestand rechtstreeks uitvoeren
middel · hard · wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Begin elk PHP-bestand van een plugin of thema dat code uitvoert met `if ( ! defined( 'ABSPATH' ) ) { exit; }`.
- Bewijs: `for f in $(git ls-files '*.php'); do grep -L "ABSPATH" "$f"; done` toont alleen bestanden met uitsluitend klasse- of functiedefinities, en die lijst is nagekeken; Plugin Check (WP-37) meldt geen "direct file access". Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V15.2.3 (L2).
