# VIBE D: Snelheid

Compacte regels van `dicht-anti-vibe`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/anti-vibe.md` (regelnummer in `regel-index.tsv`).

### VIBE-18 Afbeeldingen zijn gecomprimeerd, passend en lazy onder de vouw
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elke afbeelding is gecomprimeerd (WebP of AVIF waar het kan) en niet meer dan twee keer zo breed als ze getoond wordt; afbeeldingen onder de vouw hebben `loading="lazy"`, de LCP-afbeelding niet.
- Bewijs: `vibe_meet.py` regel VIBE-18: geen afbeelding boven 300 kB overdracht, geen afbeelding met `naturalWidth` meer dan twee keer de getoonde breedte, elke afbeelding onder de vouw lazy en de LCP-afbeelding niet. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook ARCH-74 (Core Web Vitals).
- Bron: website.md Stap 9, O34 (afbeeldingen gecomprimeerd) en A8 (lazy, LCP niet); H paragraaf 2 punt 10 en paragraaf 3 (lazy loading, afbeeldingen comprimeren).

### VIBE-19 Scripts en stijlen: uitgesteld, geminificeerd, zonder source maps
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Niet-kritieke scripts staan op `defer` of `async`; eigen JS en CSS zijn geminificeerd (gecompileerde Tailwind, geen CDN-versie); in productie staan geen source maps.
- Bewijs: `vibe_meet.py` regel VIBE-19: geen `script src` in `head` zonder `defer`, `async` of `type="module"`, geen eigen JS of CSS die niet geminificeerd is (gemiddelde regel korter dan 200 tekens bij meer dan 2 kB), geen `sourceMappingURL` en geen `.map`-bestand dat 200 geeft, geen `cdn.tailwindcss.com`. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook WEB-58 (scripts zelf hosten of SRI).
- Bron: website.md Stap 9, O16 (geen source maps), O18 (gecomprimeerde of geminificeerde bundle) en A8 (defer of async, minificeren); Stap 8 (Tailwind, geen CDN in productie); H paragraaf 3 (minificeren, niet-kritieke scripts uitstellen).

### VIBE-20 Paginacache en compressie staan aan en zijn gemeten
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: De paginacache (LiteSpeed of gelijkwaardig) staat aan en geeft bij een tweede aanvraag een treffer; HTML, CSS en JS gaan gecomprimeerd over de lijn (gzip of brotli).
- Bewijs: `vibe_meet.py` regel VIBE-20: de tweede aanvraag van de homepage heeft een cachekop met `hit` (`x-litespeed-cache`, `x-cache`, `cf-cache-status`) en HTML, CSS en JS hebben `content-encoding` gzip of br. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O18 (gecomprimeerd) en A8 (paginacache aan en gemeten); H paragraaf 3 (server-side caching).

### VIBE-21 Geen ongebruikte plugins of afhankelijkheden; lange lijsten gepagineerd
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Op de site staan geen inactieve of ongebruikte plugins en in `package.json` of `composer.json` geen ongebruikte afhankelijkheden; een lijst van meer dan 24 items (berichten, portfolio, reviews) is gepagineerd of laadt in delen.
- Bewijs: `wp plugin list --status=inactive --format=count` is 0 en bij elke actieve plugin staat in het bewijsbestand waarvoor hij is; `grep` per afhankelijkheid in `package.json` op een import in de bron; per lijstsjabloon de paginering (`posts_per_page` of `paginate_links`). Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook WP-72 (plugins beoordelen, lijst kort).
- Bron: website.md Stap 9, A8 (ongebruikte plugins en dependencies verwijderd, lange lijsten gepagineerd); H paragraaf 3 (ongebruikte dependencies, lange lijsten pagineren).

### VIBE-22 Een Lighthouse-audit per hoofdpagina, met de scores vastgelegd
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Draai per hoofdpagina een Lighthouse-audit voor mobiel en leg de vier scores en LCP, CLS en TBT vast in het bewijsbestand.
- Bewijs: per hoofdpagina eerst ophalen, dan lezen (niet in één pijp): `curl -s -o psi.json "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<url>&strategy=mobile&category=performance&category=accessibility&category=best-practices&category=seo"` en `python3 -c "import json,sys; d=json.load(open(sys.argv[1]))['lighthouseResult']; a=d['audits']; print({k: v['score'] for k, v in d['categories'].items()}, a['largest-contentful-paint']['displayValue'], a['cumulative-layout-shift']['displayValue'], a['total-blocking-time']['displayValue'])" psi.json`; de uitvoer in het bewijsbestand. Geeft de API 429 (gedeelde daglimiet zonder sleutel), draai dan Lighthouse (mobiel) in Chrome DevTools en zet de scores met een schermafbeelding in het bewijsbestand. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook ARCH-74 (Core Web Vitals op het 75e percentiel).
- Bron: website.md Stap 9, A8 (Lighthouse-audit per hoofdpagina, mobiel); H paragraaf 3 (Lighthouse-audit).
