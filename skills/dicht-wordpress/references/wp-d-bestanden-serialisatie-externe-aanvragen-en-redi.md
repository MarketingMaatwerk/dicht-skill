# WP D: Bestanden, serialisatie, externe aanvragen en redirects

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-22 Verwerk uploads via wp_handle_upload met een eigen typenlijst
kritiek · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke upload door `wp_handle_upload()` of `media_handle_upload()` lopen na een capability- en nonce-controle, laat `test_type` aan staan, geef in `mimes` alleen de typen mee die de functie nodig heeft, en verplaats nooit zelf een bestand met `move_uploaded_file()` op basis van de naam uit de aanvraag.
- Bewijs: `grep -rnE "move_uploaded_file|file_put_contents\(.*\\$_FILES|'test_type' *=> *false" .` is leeg; een test die `shell.php`, `shell.php.jpg`, `foto.jpg` met PHP-inhoud en een bestand boven de limiet uploadt: alle vier geweigerd of onschadelijk opgeslagen (geen `.php` op schijf). Afgevinkt met grep, testuitvoer en een `find` op de uploadmap.
- Norm: ASVS 5.0.0 V5.2.1 (L1), V5.2.2 (L1), V5.3.2 (L1); OWASP Top 10 2025 A01 en A05.
- Zie ook: WEB-44, WEB-43, WEB-46, API-60, WP-23, WP-24, INV-33, INV-65, MSG-25

### WP-23 Zet geen ongefilterde uploads aan en laat SVG en HTML dicht
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Definieer `ALLOW_UNFILTERED_UPLOADS` nooit, voeg via het filter `upload_mimes` geen `svg`, `html`, `js` of `php` toe, en sta SVG alleen toe via een sanitizer die scripts en externe verwijzingen verwijdert.
- Bewijs: `grep -rn "ALLOW_UNFILTERED_UPLOADS\|upload_mimes" wp-config.php wp-content/` toont geen verruiming, of alleen een plugin die SVG saneert en op de pluginlijst staat (WP-72); Plugin Check meldt niets bij "No unfiltered uploads". Afgevinkt met de grep.
- Norm: ASVS 5.0.0 V5.2.2 (L1), V3.2.1 (L1).
- Zie ook: WEB-44, WEB-43, WEB-46, API-60, WP-22, WP-24, INV-33, INV-65, MSG-25, INV-31, INV-32, WEB-07, WEB-47

### WP-24 Laat de uploadmap geen PHP uitvoeren en meet dat op de echte server
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Blokkeer het uitvoeren van PHP in `wp-content/uploads` op serverniveau en bewijs met een anonieme aanvraag op de echte server dat het werkt.
- Bewijs: Op een testkopie: zet `wp-content/uploads/dicht-test.php` met `<?php echo 'UITGEVOERD';` neer, vraag hem anoniem op met `curl -s -o - -w '%{http_code}'` en zie 403 zonder de tekst `UITGEVOERD`; haal het bestand weg. Op een live klantsite alleen na akkoord. Afgevinkt met de curl-uitvoer en de datum.
- Norm: ASVS 5.0.0 V5.3.1 (L1).
- Zie ook: WEB-44, WEB-43, WEB-46, API-60, WP-22, WP-23, INV-33, INV-65, MSG-25

### WP-25 Lees een bestand of sjabloon nooit in op basis van invoer
kritiek · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Kies een sjabloon, weergave of taalbestand via een vaste lijst van namen en bouw het pad zelf; geef nooit een waarde uit de aanvraag, een shortcode-attribuut, een blokattribuut of postmeta door aan `include`, `require`, `locate_template()`, `load_template()` of `get_template_part()`.
- Bewijs: `grep -rnE "(include|require)(_once)?\s*\(?.*\\$|get_template_part\(.*\\$|locate_template\(.*\\$" .`: elke variabele komt uit een vaste lijst; een test met `../../../../wp-config` en een onbekende naam geeft de standaardweergave. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V5.3.2 (L1), V1.3.3 (L2); OWASP Top 10 2025 A05.
- Zie ook: API-54, AI-46, API-76, WEB-45, WP-29, INV-41, INV-34, SCR-15

### WP-26 Deserialiseer nooit invoer; gebruik JSON
kritiek · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Roep `unserialize()` en `maybe_unserialize()` nooit aan op een waarde uit een aanvraag, cookie, importbestand, externe API of een veld dat een gebruiker kan vullen, en wissel gegevens uit als JSON met een controle op de vorm.
- Bewijs: `grep -rnE "\b(maybe_)?unserialize\(" .`: elke treffer leest een waarde die de code zelf heeft geschreven en die een gebruiker niet kan vullen; waar dat niet aantoonbaar is, staat `unserialize( $x, array( 'allowed_classes' => false ) )`. Let op import- en exportfuncties en op postmeta die via REST of een formulier schrijfbaar is. Afgevinkt met de nagelopen lijst.
- Norm: ASVS 5.0.0 V1.5.2 (L2); OWASP Top 10 2025 A08 Software or Data Integrity Failures.
- Zie ook: API-55, SCR-27, SCR-28, INV-16, INV-17

### WP-27 Stuur door met wp_safe_redirect en stop daarna
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `wp_safe_redirect()` voor elke doorverwijzing waarvan het doel uit de aanvraag of de database kan komen, en laat er altijd `exit;` op volgen.
- Bewijs: `phpcs --sniffs=WordPress.Security.SafeRedirect .` is groen; `grep -rn -A1 "wp_safe_redirect\|wp_redirect" .` toont na elke aanroep `exit;` of `die;`; een test met `terug=https://evil.example` komt uit op de eigen site. Onbekende hosts vallen terug op `admin_url()`; extra hosts sta je toe met het filter `allowed_redirect_hosts`. Afgevinkt met phpcs, grep en test.
- Norm: ASVS 5.0.0 V1.2.2 (L1), V8.3.1 (L1) voor het doorlopen na een weigering.
- Zie ook: WEB-39, AUTH-45, INV-60, WP-28, INV-34

### WP-28 Haal een URL van een gebruiker alleen op met wp_safe_remote_get, met een grens
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `wp_safe_remote_get()` en `wp_safe_remote_post()` voor elk adres dat niet vast in de code staat, zet `timeout` en `limit_response_size`, controleer `is_wp_error()` en de statuscode, en gebruik voor uitgaande aanroepen nooit `curl_*` of `file_get_contents()` op een URL.
- Bewijs: `grep -rnE "wp_remote_(get|post|request|head)\(|curl_init|file_get_contents\( *['\"]?https?" .`: elke aanroep met een variabel adres gebruikt de `wp_safe_`-variant; een test met `http://127.0.0.1/`, `http://10.0.0.1/` en `http://gebruiker:wachtwoord@voorbeeld.nl/` geeft een fout en geen aanvraag. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V1.3.6 (L2), V15.3.2 (L2).
- Zie ook: WEB-40, WEB-41, API-48, API-47, AI-48, INFRA-18, INV-59, INV-61, MSG-27, MSG-46, INV-60, WP-27, INV-34

### WP-29 Schrijf bestanden alleen in een eigen map onder uploads, met een zelfgekozen naam
middel · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf gegenereerde bestanden (exports, caches, logs) alleen in een eigen submap van `wp_upload_dir()['basedir']`, met een naam die de code zelf maakt, en zet gevoelige bestanden daar niet neer zonder een blokkade die anoniem is gemeten.
- Bewijs: `grep -rnE "file_put_contents|fopen\(|fwrite\(" .`: elk pad is opgebouwd uit `wp_upload_dir()` plus een vaste submap plus een naam met minstens 128 bits willekeur (`wp_generate_password( 32, false )` of `bin2hex( random_bytes( 16 ) )`), of de map is aantoonbaar dicht (curl geeft 403). Plugin Check meldt bij `Write_File_Check` niets onverklaards. Afgevinkt met grep en curl.
- Norm: ASVS 5.0.0 V5.3.2 (L1), V11.5.1 (L2).
- Zie ook: API-54, AI-46, WP-25, API-76, WEB-45, INV-41, INV-34, SCR-15
