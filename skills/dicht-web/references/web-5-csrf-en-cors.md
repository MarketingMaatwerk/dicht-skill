# WEB 5: CSRF en CORS

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-29 Wijzig nooit iets via GET
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke actie die iets wijzigt, verstuurt, verwijdert of betaalt alleen toe via POST, PUT, PATCH of DELETE; een GET-route mag alleen lezen. Dat geldt ook voor links in mails (afmelden, bevestigen): de link opent een pagina, de actie zelf is een POST.
- Bewijs: Een lijst van alle GET-routes (in Fastify via de routetabel, in WordPress alle `admin-post`, `init`- en `template_redirect`-handlers die `$_GET` lezen) met per route "alleen lezen: ja". Een test die elke GET-route twee keer aanroept en controleert dat de database gelijk blijft. Afgevinkt met lijst en test.
- Norm: ASVS 5.0.0 V3.5.3 (L1); OWASP Top 10 2025 A01 (CWE-352).

### WEB-30 Verdedig elke wijzigende aanvraag met cookie-authenticatie tegen CSRF
kritiek · hard · website | wp-plugin | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer bij elke wijzigende aanvraag die op een cookie vertrouwt een anti-CSRF-bewijs op de server: een synchronizer-token of een ondertekende double-submit-cookie, of een Fetch Metadata-controle (`Sec-Fetch-Site`) met verplichte terugval op een exacte vergelijking van `Origin` (of anders `Referer`) met de eigen origin; weiger de aanvraag als geen van beide headers er is.
- Bewijs: Een integratietest per wijzigende route met een geldige sessiecookie en (a) zonder token en met `Sec-Fetch-Site: cross-site`, (b) met `Origin: https://evil.example`, (c) met `Origin: https://<eigen-host>.evil.example`, (d) zonder `Origin`, `Referer` en `Sec-Fetch-Site`; alle vier geven 403. Afgevinkt met de testuitvoer. In WordPress is het bewijs een nonce-controle per handler: zie WP.
- Norm: ASVS 5.0.0 V3.5.1 (L1), V3.3.2 (L2); OWASP Top 10 2025 A01 (CWE-352).
- Zie ook: WP-09, WP-15, WEB-32

### WEB-31 Laat een JSON-API alleen application/json toe
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Weiger op elke wijzigende API-route een body met `Content-Type` `text/plain`, `application/x-www-form-urlencoded` of `multipart/form-data`, tenzij de route daar bewust voor gemaakt is en dan een CSRF-token eist; vertrouw niet op de CORS-preflight als enige CSRF-bescherming zonder dit af te dwingen.
- Bewijs: Test per wijzigende route: `curl -X POST -H 'Content-Type: text/plain' --data '{"a":1}'` geeft 415 of 400; de Fastify-versie in het lockfile is 5.12.5 of hoger (de ondergrens van INV-15; CVE-2022-41919 zelf is gerepareerd in 4.10.2); er is geen eigen `addContentTypeParser` voor `text/plain` of `*` op deze routes (`grep -rn addContentTypeParser`). Afgevinkt met test en grep.
- Norm: ASVS 5.0.0 V3.5.2 (L1); OWASP Top 10 2025 A01.
- Zie ook: INV-15, API-05

### WEB-32 Bescherm ook het inlogformulier tegen CSRF
middel · richtlijn · website | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef het inlogformulier en het registratieformulier dezelfde CSRF-bescherming als ingelogde formulieren (pre-sessie met token of de controle uit WEB-30) en maak na het inloggen altijd een nieuwe sessie aan.
- Bewijs: De test uit WEB-30 draait ook op `/login` en `/registreren`; de sessie-ID vóór en na inloggen verschilt. Afgevinkt met de test. De sessierotatie zelf hoort bij AUTH.
- Norm: ASVS 5.0.0 V3.5.1 (L1).
- Zie ook: WEB-30, WP-09, WP-15

### WEB-33 Sta met CORS alleen een vaste lijst van origins toe
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet geen CORS-headers tenzij een andere origin de API echt nodig heeft; vergelijk dan de `Origin` exact met een allowlist uit de configuratie, stuur `Vary: Origin` mee, sta `null` nooit toe en combineer `Access-Control-Allow-Credentials: true` nooit met een gespiegelde of wildcard-origin.
- Bewijs: `curl -sI -H 'Origin: https://evil.example' <api>` en dezelfde aanroep met `Origin: null` en met `Origin: https://app.voorbeeld.nl.evil.example`: geen van de drie krijgt `Access-Control-Allow-Origin` terug; een toegestane origin krijgt de header met `Vary: Origin`. Afgevinkt met de vier uitvoeren.
- Norm: ASVS 5.0.0 V3.4.2 (L1); OWASP Top 10 2025 A01 en A02.

### WEB-34 Controleer de Origin bij de WebSocket-handshake
hoog · hard · app | api | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Vergelijk bij elke WebSocket-handshake de `Origin` met de allowlist, gebruik alleen `wss://` en bind de verbinding aan de bestaande, geauthenticeerde sessie.
- Bewijs: Een test die de handshake doet met een geldige cookie en `Origin: https://evil.example` krijgt 403 of een gesloten verbinding; zonder cookie ook. Afgevinkt met de test.
- Norm: ASVS 5.0.0 V4.4.1 (L1), V4.4.2, V4.4.3, V4.4.4 (L2).

### WEB-35 Geen JSONP en geen data met autorisatie in scriptbestanden
laag · richtlijn · api | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Bied geen JSONP-eindpunt aan en lever gegevens waarvoor autorisatie nodig is nooit als JavaScript-bestand; gebruik JSON met het juiste `Content-Type`.
- Bewijs: `grep -rniE "callback=|jsonp" src/` is leeg; geen route geeft `application/javascript` met gebruikersdata terug. Afgevinkt met de grep.
- Norm: ASVS 5.0.0 V3.5.6 en V3.5.7 (L3).
