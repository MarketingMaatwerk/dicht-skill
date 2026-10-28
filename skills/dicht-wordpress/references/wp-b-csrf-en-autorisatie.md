# WP B: CSRF en autorisatie

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-09 Controleer een nonce op elke handler die iets wijzigt, en kijk naar de uitkomst
kritiek · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke handler die iets wijzigt (formulier, `admin-post`, AJAX, link met actie) alleen `POST` accepteren, controleer een nonce met een actienaam die het object bevat (`check_admin_referer( 'verwijder-item_' . $id )`, `check_ajax_referer()` of `wp_verify_nonce()`), en stop als de nonce ontbreekt of onjuist is.
- Bewijs: (1) `phpcs --sniffs=WordPress.Security.NonceVerification .` is groen. (2) Per handler een test met een geldige sessie en (a) zonder nonce, (b) met een nonce van een andere actie: beide geven 403 en wijzigen niets. Afgevinkt met phpcs en de testuitvoer per handler.
- Norm: ASVS 5.0.0 V3.5.1 (L1), V3.5.3 (L1); OWASP Top 10 2025 A01.
- Zie ook: WEB-30, WP-15, WEB-32, WP-10, WP-11, WP-12, WP-13, AUTH-62, AUTH-64

### WP-10 Controleer de capability op het object, niet alleen op de rol
kritiek · hard · wp-plugin | wp-thema | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Controleer in elke handler met `current_user_can()` de capability die bij de handeling hoort, en geef bij een handeling op één object het ID mee: `current_user_can( 'edit_post', $post_id )`, `current_user_can( 'delete_user', $user_id )`. Aanvulling uit AUTH-71: Gebruik `__return_true` alleen voor bewust publieke routes; een nonce is alleen een verdediging tegen CSRF, geen autorisatie.
- Bewijs: Een test per handler met twee gebruikers (bijvoorbeeld twee auteurs, of een abonnee en een beheerder): gebruiker A probeert het object van gebruiker B te lezen, wijzigen en verwijderen en krijgt 403. De lijst van handlers komt uit `grep -rnE "wp_ajax_|admin_post_|register_rest_route|add_shortcode|add_action\( *'(init|admin_init|template_redirect)'" .` (een shortcode telt mee zodra hij een gevoelige actie uitvoert, zie AUTH-71). Afgevinkt als elke handler op de lijst een test heeft.
    Ook (uit AUTH-71): `grep -rn "register_rest_route" . | wc -l` is gelijk aan het aantal `permission_callback`-vermeldingen, en elke `__return_true` staat op de lijst met publieke routes. `grep -rn "wp_ajax_" .` en controleer dat elke handler `current_user_can` aanroept. Afgevinkt als beide kloppen. Zie WP voor de volledige uitwerking.
- Norm: ASVS 5.0.0 V8.2.1 (L1), V8.2.2 (L1), V8.3.1 (L1); OWASP Top 10 2025 A01 Broken Access Control.
- Dekt ook: AUTH-71
- Zie ook: WP-09, WP-11, WP-12, WP-13, AUTH-62, AUTH-64

### WP-11 Gebruik is_admin() en admin_init nooit als rechtencontrole
kritiek · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Behandel `is_admin()` alleen als "dit is een aanvraag naar wp-admin" en zet in elke functie op `admin_init` die iets doet zelf een capability-controle en een nonce.
- Bewijs: `grep -rn "is_admin()" .` en `grep -rn "'admin_init'" .`: bij elke treffer staat in de review of er daarna een `current_user_can()` volgt voordat er iets gebeurt. Een test die elke gevonden actie anoniem aanroept via `admin-ajax.php` en `admin-post.php` en nergens een effect ziet. Afgevinkt met de lijst en de testuitvoer.
- Norm: ASVS 5.0.0 V8.2.1 (L1), V8.3.1 (L1).
- Zie ook: WP-10, WP-09, WP-12, WP-13, AUTH-62, AUTH-64

### WP-12 Registreer wp_ajax_nopriv alleen voor bewust publieke acties
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Registreer een AJAX-actie alleen op `wp_ajax_nopriv_{actie}` als een anonieme bezoeker hem hoort te gebruiken, en houd een lijst van die acties bij met per actie wat hij leest of schrijft en welke begrenzing erop staat.
- Bewijs: `grep -rn "wp_ajax_nopriv_" .` komt overeen met de lijst in de documentatie van de plugin; elke actie op de lijst heeft invoervalidatie (WP-06), een begrenzing (WEB-66) en geeft geen gegevens van andere gebruikers terug. Afgevinkt met de grep en de lijst.
- Norm: ASVS 5.0.0 V8.2.1 (L1), V2.4.1 (L2).
- Zie ook: WP-10, WP-09, WP-11, WP-13, AUTH-62, AUTH-64

### WP-13 Geef elke REST-route een permission_callback en een schema voor de argumenten
kritiek · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Registreer elke route met een `permission_callback` die `current_user_can()` op de juiste capability en het juiste object controleert, gebruik `__return_true` alleen voor een route die op de lijst van publieke routes staat, beschrijf elk argument in `args` met `type`, `required`, `validate_callback` en `sanitize_callback`, en geef een `WP_REST_Response` of `WP_Error` terug.
- Bewijs: (1) Het aantal `register_rest_route`-aanroepen is gelijk aan het aantal `permission_callback`-vermeldingen en elke `__return_true` staat op de lijst met publieke routes (zie WP-10 en WP-12). (2) Met `WP_DEBUG` aan op de testomgeving bevat `debug.log` na het laden van `/wp-json/` geen melding "missing the required permission_callback argument". (3) Per route een test: anoniem, als abonnee en als eigenaar van een ander object geeft 401 of 403; een verkeerd type en een extra veld geven 400 of worden genegeerd. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V8.2.1, V8.2.2 (L1), V2.2.1 (L1), V15.3.3 (L2); OWASP API Security Top 10 2023 API1 en API5.
- Zie ook: API-01, AI-11, AI-23, API-50, ARCH-07, WP-10, WP-09, WP-11, WP-12, AUTH-62, AUTH-64

### WP-14 Gebruik voor REST de ingebouwde authenticatie en stuur de nonce als header
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat scripts in de browser de REST API aanroepen met de cookie van WordPress plus de header `X-WP-Nonce` met een nonce voor de actie `wp_rest`, laat systemen van buiten inloggen met een applicatiewachtwoord over HTTPS, en bouw geen eigen token- of sleutelcontrole in een `permission_callback` zonder dat die aan AUTH-53 tot en met AUTH-57 voldoet.
- Bewijs: `grep -rn "X-WP-Nonce\|wp_create_nonce( 'wp_rest' )" .` toont de nonce in elke eigen fetch-aanroep; een aanvraag met geldige cookie en zonder `X-WP-Nonce` naar een wijzigende eigen route geeft 401 of 403. Je hoeft de nonce niet zelf te controleren in de callback: dat doet `rest_cookie_check_errors()`. Afgevinkt met grep en de testaanvraag.
- Norm: ASVS 5.0.0 V3.5.1 (L1), V14.2.1 (L1).

### WP-15 Reken bij anonieme bezoekers niet op de nonce
middel · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bescherm een formulier of actie voor niet-ingelogde bezoekers met een eigen, per bezoeker verschillend token of met de lagen uit WEB-67, en niet alleen met een WordPress-nonce.
- Bewijs: Voor sites van Marketing Maatwerk: het formulier staat achter het eigen formulierschild (ondertekend tijdstempel, lokveld, rekenbewijs, limiet per IP) en de drie negatieve tests uit WEB-67 slagen. Voor eigen bouw zonder die mu-plugin: een test die dezelfde nonce vanaf een tweede "bezoeker" (andere cookiepot) opnieuw gebruikt en wordt geweigerd. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V3.5.1 (L1), V2.4.1 (L2).
- Zie ook: WEB-30, WP-09, WEB-32
