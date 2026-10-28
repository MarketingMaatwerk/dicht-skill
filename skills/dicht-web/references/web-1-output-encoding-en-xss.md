# WEB 1: Output-encoding en XSS

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-01 Codeer uitvoer per context, als laatste stap
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Codeer elke niet-vertrouwde waarde op het moment van uitvoer met de encoder die bij de context hoort (HTML-tekst, HTML-attribuut, JavaScript, CSS, URL) en nooit eerder of generiek bij de invoer.
- Bewijs: (1) Zoek in de code naar rauwe uitvoer: `grep -rnE "echo \$_(GET|POST|REQUEST)|<\?= *\$" --include=*.php` en in React `grep -rn dangerouslySetInnerHTML`. Elk resultaat is verklaard of weg. (2) Een test die per invoerveld de waarde `"'><svg onload=alert(1)>` instuurt en in de respons controleert dat de tekens gecodeerd terugkomen. Afgevinkt als beide groen zijn.
- Norm: ASVS 5.0.0 V1.2.1 (L1), V1.1.2 (L2); OWASP Top 10 2025 A05 Injection.
- Zie ook: WP-01, WP-02, WP-03, WEB-06, MSG-17, INV-25, INV-35

### WEB-02 Schrijf tekst naar de DOM met veilige sinks
hoog · hard · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `textContent`, `createTextNode` of `setAttribute` op een niet-uitvoerend attribuut om tekst in de pagina te zetten, en gebruik `innerHTML`, `outerHTML`, `insertAdjacentHTML` en `document.write` alleen met de uitvoer van een sanitizer (WEB-03).
- Bewijs: `grep -rnE "innerHTML|outerHTML|insertAdjacentHTML|document\.write|dangerouslySetInnerHTML|v-html" src/` geeft alleen regels met een sanitizer-aanroep of een vaste string; een ESLint-regel die deze sinks verbiedt staat aan in de gate. Afgevinkt met de grep-uitvoer en een groene lint.
- Norm: ASVS 5.0.0 V3.2.2 (L1); OWASP Top 10 2025 A05.

### WEB-03 Sta HTML van gebruikers alleen toe via een onderhouden sanitizer
hoog · hard · website | wp-plugin | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Haal elke HTML die van een gebruiker, een mail, een model of een externe bron komt door een bekende sanitizer (DOMPurify in de browser of Node, `wp_kses` in WordPress) met een allowlist van tags en attributen, en houd die bibliotheek op de laatste versie.
- Bewijs: (1) De versie van de sanitizer in het lockfile is niet lager dan de laatste versie met een beveiligingsfix (`npm ls dompurify`, vergelijk met de advisories). (2) Een test met drie payloads (`<img src=x onerror=...>`, `<svg><script>`, `<a href="javascript:...">`) geeft uitvoer zonder handler, script of `javascript:`. Afgevinkt met versie en testuitvoer.
- Norm: ASVS 5.0.0 V1.3.1 (L1); OWASP Top 10 2025 A05 en A03 Software Supply Chain Failures.
- Zie ook: WP-04, AI-13, WEB-07, INV-22, INV-23, INV-24, INV-26, MSG-23

### WEB-04 Laat in URL-attributen alleen veilige schema's toe
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer elke niet-vertrouwde URL die in `href`, `src`, `action`, `formaction` of een CSS-`url()` komt tegen een allowlist van schema's (`https:`, eventueel `mailto:` en `tel:`) voordat je hem codeert en plaatst.
- Bewijs: Een unit-test per veld dat een URL toont, met `javascript:`, `data:text/html,...` en `JaVaScRiPt:` als invoer; alle drie worden geweigerd. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V1.2.2 (L1); OWASP Top 10 2025 A05.

### WEB-05 → API-56
Samengevoegd: "Voer nooit tekst uit als code" is gedekt door API-56. Gebruik die regel.

### WEB-06 Geef data aan JavaScript door als gecodeerde data, niet als code
hoog · hard · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Zet serverdata voor de browser in een `data-`attribuut (HTML-gecodeerd) of in een `<script type="application/json">`-blok waarin `<`, `>` en `&` als `\u003C`, `\u003E` en `\u0026` staan, en lees het met `JSON.parse`; schrijf nooit een waarde rechtstreeks in een uitvoerend scriptblok.
- Bewijs: Een test die een veld met `</script><svg onload=alert(1)>` vult en in de HTML-bron controleert dat de reeks `</script>` niet in het datablok voorkomt. In WordPress: data gaat via `wp_add_inline_script` met `wp_json_encode` of via `wp_localize_script`. Afgevinkt met de test.
- Norm: ASVS 5.0.0 V1.2.3 (L1); OWASP Top 10 2025 A05.
- Zie ook: WEB-01, WP-01, WP-02, WP-03, MSG-17, INV-25, INV-35

### WEB-07 Behandel SVG, Markdown en eigen CSS van gebruikers als actieve inhoud
hoog · hard · website | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Weiger SVG-uploads van gebruikers of sanitize ze tot alleen tekentags zonder `script`, `foreignObject` en event-attributen, haal gerenderde Markdown na het renderen door de sanitizer van WEB-03, en sta geen vrij CSS van gebruikers toe.
- Bewijs: (1) Upload-test: een SVG met `onload` en `<script>` wordt geweigerd of komt geschoond terug. (2) Markdown-test: `[x](javascript:alert(1))` en `<img src=x onerror=alert(1)>` leveren geen uitvoerbare uitvoer. (3) Geüploade bestanden komen van een aparte origin of met `Content-Disposition: attachment` (WEB-47). Afgevinkt met de drie testuitvoeren.
- Norm: ASVS 5.0.0 V1.3.4 (L2), V1.3.5 (L2); OWASP Top 10 2025 A05.
- Zie ook: WEB-03, WP-04, AI-13, INV-22, INV-23, INV-24, INV-26, MSG-23, INV-31, INV-32, WP-23, WEB-47

### WEB-08 Bouw nooit een template uit invoer
kritiek · hard · website | api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef gebruikersinvoer alleen als data aan een template mee en stel de templatetekst zelf nooit samen uit invoer; waar klanten eigen sjablonen mogen maken (mailsjablonen in een CRM), gebruik een logica-loze engine met een allowlist van variabelen.
- Bewijs: (1) Codecontrole: geen render-aanroep waarvan het eerste argument uit invoer of de database komt, tenzij de engine logica-loos is en de variabelen uit een allowlist komen. (2) Test: de waarden `{{7*7}}`, `${7*7}` en `<%= 7*7 %>` in elk veld dat in een sjabloon belandt, komen letterlijk terug en nooit als `49`. Afgevinkt met de test.
- Norm: ASVS 5.0.0 V1.3.7 (L2); OWASP Top 10 2025 A05.
- Zie ook: API-56, AI-12

### WEB-09 Stuur bij elke respons het juiste Content-Type met charset en nosniff
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke respons met een body een `Content-Type` dat klopt met de inhoud, met `charset=utf-8` voor tekstsoorten, en zet `X-Content-Type-Options: nosniff` op alle responsen. Aanvulling uit API-14: Stuur JSON nooit als `text/html`.
- Bewijs: `curl -sI https://<host>/<pad>` op een pagina, een API-route, een foutpagina (404, 500) en een statisch bestand: elk heeft het juiste `Content-Type` met charset en `X-Content-Type-Options: nosniff`. Afgevinkt met de vier uitvoeren.
    Ook (uit API-14): `curl -sI` op drie routes (succes, 400, 404) toont `content-type: application/json; charset=utf-8` of `application/problem+json`. `X-Content-Type-Options: nosniff` staat in nginx (zie WEB).
- Norm: ASVS 5.0.0 V4.1.1 (L1), V3.4.4 (L2); OWASP Top 10 2025 A02 Security Misconfiguration.
- Dekt ook: API-14

### WEB-10 Voorkom DOM clobbering
laag · richtlijn · website | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Declareer variabelen expliciet, lees geen configuratie uit `window.<naam>` of `document.<naam>`, en laat de sanitizer `id` en `name` niet toe op door gebruikers geleverde HTML.
- Bewijs: Codecontrole op `window.` en `document.` gevolgd door een eigen naam; de sanitizer-configuratie laat `id` en `name` niet toe. Afgevinkt met de grep en de configuratie.
- Norm: ASVS 5.0.0 V3.2.3 (L3).
