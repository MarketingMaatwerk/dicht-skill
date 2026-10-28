# WEB 3: Security headers

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-17 Zet HSTS op alle responsen
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur `Strict-Transport-Security` met een `max-age` van minstens één jaar (31536000) en `includeSubDomains` op alle HTTPS-responsen, nadat is vastgesteld dat elk subdomein HTTPS serveert.
- Bewijs: `curl -sI https://<host>/` en `curl -sI https://<host>/bestaat-niet` tonen beide de header met `max-age` van minstens 31536000 en `includeSubDomains`; een lijst van subdomeinen uit DNS is nagelopen op HTTPS. Afgevinkt met de uitvoer en de subdomeinlijst.
- Norm: ASVS 5.0.0 V3.4.1 (L1; alle subdomeinen vanaf L2); OWASP Top 10 2025 A02 en A04 Cryptographic Failures.
- Zie ook: WEB-23, WEB-22, WP-65, WEB-56, WP-43, INFRA-44, INFRA-55, INFRA-48, DB-60

### WEB-18 Vraag HSTS-preload alleen bewust aan
middel · richtlijn · website | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Voeg `preload` alleen toe en meld een domein alleen aan bij hstspreload.org als vaststaat dat alle huidige en toekomstige subdomeinen (ook mail, panelen en testomgevingen) HTTPS serveren, en leg het besluit vast; doe dit nooit op een klantdomein zonder akkoord van de klant.
- Bewijs: Voor aanmelding: de eisen van hstspreload.org zijn afgevinkt (geldig certificaat, redirect van HTTP naar HTTPS op dezelfde host, alle subdomeinen op HTTPS, `max-age` minstens 31536000, `includeSubDomains`, `preload`) en het akkoord staat genoteerd. Afgevinkt met de notitie.
- Norm: ASVS 5.0.0 V3.7.4 (L3).

### WEB-19 Zet een expliciete Referrer-Policy
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur `Referrer-Policy: strict-origin-when-cross-origin` op alle responsen, en `no-referrer` op pagina's waarvan het pad of de query een geheim bevat (resetlink, magic link, deelbare link).
- Bewijs: `curl -sI` toont de header op een gewone pagina en `no-referrer` op de resetpagina; de resetpagina laadt geen bronnen van derden (netwerklog van de browser). Afgevinkt met beide.
- Norm: ASVS 5.0.0 V3.4.5 (L2), V14.2.1 (L1).

### WEB-20 Schakel ongebruikte browserfuncties uit met Permissions-Policy
laag · richtlijn · website | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur `Permissions-Policy` met een lege allowlist voor elke functie die de site niet gebruikt, minimaal `geolocation=(), camera=(), microphone=()`, en geef een iframe alleen via `allow` wat het nodig heeft.
- Bewijs: `curl -sI` toont de header. Apps die de microfoon echt gebruiken (bijvoorbeeld voor notulen) geven die alleen aan de eigen origin: `microphone=(self)`. Afgevinkt met de header. Let op: MDN markeert de header als "limited availability" en experimenteel; niet elke browser dwingt hem af, dus dit is aanvullend.
- Norm: Geen eigen ASVS-eis; OWASP Top 10 2025 A02.

### WEB-21 Isoleer het venster en de bronnen: COOP en CORP
middel · richtlijn · website | app | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur op HTML-responsen `Cross-Origin-Opener-Policy: same-origin` (of `same-origin-allow-popups` als een betaal- of OAuth-popup dat vereist) en op bronnen die een ingelogde gebruiker toont `Cross-Origin-Resource-Policy: same-origin` of `same-site`.
- Bewijs: `curl -sI` op een HTML-pagina toont COOP; op een ingelogde afbeelding of download CORP. De betaalstroom (Mollie-redirect) en OAuth-login zijn daarna met echte klikken getest. Afgevinkt met headers en e2e-uitvoer. Zet `Cross-Origin-Embedder-Policy: require-corp` niet blind: het blokkeert elke bron van derden die niet meewerkt.
- Norm: ASVS 5.0.0 V3.4.8 (L3), V3.5.8 (L3); hard voor login, betaling en tenant-data volgens besluit 6.

### WEB-22 Verberg versies en verwijder verouderde headers
laag · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur geen `X-Powered-By` en geen versienummer in `Server`, zet `X-XSS-Protection` niet of op `0`, en verwijder `Public-Key-Pins` en `Expect-CT`.
- Bewijs: `curl -sI https://<host>/ | grep -iE "^(server|x-powered-by|x-xss-protection|public-key-pins|expect-ct)"` toont hooguit `Server: nginx` zonder versie. Afgevinkt met de uitvoer. `server_tokens` staat in nginx standaard op `on` en `expose_php` in PHP standaard op `1`, dus beide moeten bewust uit.
- Norm: ASVS 5.0.0 V13.4.6 (L3); OWASP Top 10 2025 A02.
- Zie ook: WEB-23, WEB-17, WP-65

### WEB-23 Controleer headers op elke locatie en elke statuscode (nginx-overerving)
hoog · hard · website | api | app | klantproject | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in nginx elke security header met `always`, en zorg dat een `location` met een eigen `add_header` de headers van het hogere niveau niet kwijtraakt: herhaal ze via een include of zet `add_header_inherit merge;`. Aanvulling uit INFRA-49: Zet de vaste headers in één snippet; `add_header_inherit merge;` werkt vanaf nginx 1.29.3, op oudere versies komt de snippet in elke `location` met een eigen `add_header`.
- Bewijs: Een script dat per host minimaal vijf URL's opvraagt (homepage, een statisch bestand, een API-route, een 404 en een 301) en per respons de verplichte headers telt; elke respons heeft ze allemaal. Afgevinkt met de tabel. Context: de live nginx is 1.29.8 (gemeten met `docker exec nginx nginx -v`), dus `add_header_inherit` is beschikbaar; in de huidige configuratie komt de directive niet voor (alleen gelezen, niets gewijzigd).
    Ook (uit INFRA-49): `nginx -T | grep -n 'add_header_inherit'` toont `merge` in het `http`-blok, of elke `location` met `add_header` bevat de `include`; de headermeting op vijf URL's uit WEB-23 is groen. Afgevinkt met beide.
- Norm: ASVS 5.0.0 V3.4.1 ("on all responses"), V3.4.4 ("all HTTP responses"), V3.4.6 ("every HTTP response"); OWASP Top 10 2025 A02.
- Dekt ook: INFRA-49
- Zie ook: WEB-17, WEB-22, WP-65

### WEB-24 Verbied insluiten met frame-ancestors
hoog · hard · website | wp-thema | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur op elke respons `Content-Security-Policy: frame-ancestors 'none'` (of `'self'` of een expliciete lijst als insluiten nodig is) en voeg `X-Frame-Options: DENY` of `SAMEORIGIN` alleen toe als aanvulling voor oude browsers.
- Bewijs: `curl -sI` toont `frame-ancestors` in de CSP-header (niet in een meta-tag, zie WEB-15) op een pagina, een 404 en een API-respons; een testpagina met `<iframe src="https://<host>/">` laat in de browser een geblokkeerd frame zien. Afgevinkt met header en schermafbeelding of consolemelding.
- Norm: ASVS 5.0.0 V3.4.6 (L2); OWASP Top 10 2025 A02.
