# INV I: mass assignment in PHP en WordPress

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-46 Gebruik extract, variabele variabelen en parse_str niet op invoer
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Roep `extract()` nooit aan op `$_GET`, `$_POST`, `$_REQUEST`, `$_COOKIE`, `$_FILES`, shortcode-attributen of een gedecodeerde body, gebruik geen `$$naam` met een naam uit invoer, en lees elk veld bij naam.
- Bewijs: `grep -rnE "\bextract\(|\\$\\$[a-zA-Z_{]|parse_str\([^,)]+\)" --include=*.php .`: geen treffer in eigen code, of de bron is een array die de code zelf heeft opgebouwd en de aanroep gebruikt `EXTR_SKIP`. Afgevinkt met de nagelopen lijst.
- Norm: ASVS 5.0.0 V15.3.3 (L2).
- Zie ook: AUTH-65, API-02, INV-47, WP-32, INV-13

### INV-47 Geef WordPress-functies die gebruikers of berichten schrijven nooit de hele aanvraag
kritiek · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel de array voor `wp_insert_user()`, `wp_update_user()`, `wp_insert_post()`, `wp_update_post()` en elke lus over `update_user_meta()` of `update_post_meta()` veld voor veld samen uit een vaste lijst, en neem `role`, `ID`, `post_author`, `post_status`, `post_type` en metasleutels nooit over uit `$_POST` of een REST-body van een gewone gebruiker.
- Bewijs: `grep -rnE "wp_(insert|update)_(user|post)\(\s*\\$_(POST|REQUEST|GET)|update_(user|post)_meta\([^,]+,\s*\\$[a-z_]*key" --include=*.php .`: geen aanroep met een superglobal, en geen metasleutel uit invoer zonder allowlist; test: een registratie met `role=administrator` en met `meta[wp_capabilities][administrator]=1` levert een account met de laagste rol (`wp user get <id> --field=roles`). Afgevinkt met grep en test. Zie AUTH-65 en WP-32.
- Norm: ASVS 5.0.0 V15.3.3 (L2); OWASP API Top 10 2023 API3.
- Zie ook: AUTH-65, API-02, INV-46, WP-32, INV-13
