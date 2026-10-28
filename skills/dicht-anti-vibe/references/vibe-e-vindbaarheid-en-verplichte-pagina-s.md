# VIBE E: Vindbaarheid en verplichte pagina's

Compacte regels van `dicht-anti-vibe`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/anti-vibe.md` (regelnummer in `regel-index.tsv`).

### VIBE-23 De HTML-bron toont de echte inhoud
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: De HTML die de server stuurt (zonder JavaScript) bevat de kop, de tekst en de links van de pagina; geen lege schil die pas in de browser gevuld wordt.
- Bewijs: `vibe_meet.py` regel VIBE-23: per pagina bevat de ruwe HTML (zonder browser opgehaald) de H1 van de gerenderde pagina en minstens 80 woorden tekst. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O2 (view-source toont echte content).

### VIBE-24 Elke pagina heeft een eigen titel en beschrijving en precies één H1
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elke pagina heeft een `title` en een `meta name="description"` die op geen andere pagina voorkomen, en precies één `h1`.
- Bewijs: `vibe_meet.py` regel VIBE-24 (uniek over alle gemeten pagina's, aantal `h1` per pagina). Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O4 (unieke title), O5 (unieke meta description) en O8 (precies één H1); H paragraaf 2 punt 5 en 6.

### VIBE-25 Canonical en og:image op elke pagina
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elke pagina heeft een absolute `link rel="canonical"` naar haar eigen indexeerbare URL en een `og:image` die 200 geeft.
- Bewijs: `vibe_meet.py` regel VIBE-25 (aanwezig, absoluut, zelfde host, canonical en og:image geven 200). Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O6 (og:image) en O9 (canonical tags).

### VIBE-26 Het lang-attribuut klopt met de taal van de pagina
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: `html lang` is de taal van de inhoud (`nl-NL` of `nl` voor een Nederlandse site). Op WordPress staat de sitetaal op `nl_NL`.
- Bewijs: `vibe_meet.py --taal nl` regel VIBE-26; op WordPress `wp option get WPLANG` geeft `nl_NL` (of `wp language core list --status=active`). Afgevinkt met beide.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook PRIV-66 (WCAG 2.2 AA).
- Bron: website.md Stap 9, O14 (correcte lang-attributen) en W1 (sitetaal op nl_NL).

### VIBE-27 Elke afbeelding heeft een alt-attribuut
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elke `img` heeft een `alt`: een beschrijving bij een inhoudelijke afbeelding, leeg (`alt=""`) alleen bij een puur decoratieve.
- Bewijs: `vibe_meet.py` regel VIBE-27 (geen `img` zonder `alt`; het aantal lege alts staat erbij om na te lopen). Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook PRIV-66 (WCAG 2.2 AA).
- Bron: website.md Stap 9, O15 (alt-teksten op alle afbeeldingen).

### VIBE-28 Structured data staat erop en is geldig
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elke pagina heeft JSON-LD die als JSON te lezen is; de homepage heeft Organization of LocalBusiness en WebSite. Welke typen verder, en de laatste controle met de Rich Results Test en de Schema.org-validator, staan in het eigen websiteproces (stap 9).
- Bewijs: `vibe_meet.py` regel VIBE-28 (elk JSON-LD-blok leesbaar, de typen op de homepage); daarna de Rich Results Test per paginatype zonder fouten (schermafbeelding of link in het bewijsbestand). Afgevinkt met beide.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O7 (structured data aanwezig); de blokken "Structured data" en "Laatste check" van Stap 9 blijven in website.md.

### VIBE-29 sitemap.xml, robots.txt en llms.txt kloppen
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: `sitemap.xml` geeft 200 en bevat alleen indexeerbare pagina's die 200 geven (op WordPress gefilterd met `wp_sitemaps_add_provider` en `wp_sitemaps_taxonomies`: geen lege berichten-, categorie- of auteurspagina's); `robots.txt` geeft 200, noemt de sitemap en blokkeert AI-crawlers niet (tenzij bewust en vastgelegd); `llms.txt` geeft direct 200, geen 301.
- Bewijs: `vibe_meet.py` regel VIBE-29 (status van de drie bestanden zonder redirects te volgen, elke sitemap-URL 200 en zonder `noindex`, geen `Disallow: /` voor GPTBot, ClaudeBot, PerplexityBot, Google-Extended of CCBot). Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook WEB-71 (robots.txt is geen afscherming).
- Bron: website.md Stap 9, O10 (llms.txt), O11 (AI-crawlers niet geblokkeerd), O13 (sitemap.xml), W3 (sitemap beperken) en W5 (llms.txt 200, geen 301); verplichte pagina's P1 (sitemap.xml, robots.txt, llms.txt).

### VIBE-30 Er is een favicon, en het hoort bij het thema
laag · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elke pagina verwijst naar een favicon dat 200 geeft. Op WordPress staat het in het thema, niet in de mediabibliotheek (`site_icon` is 0), zodat het met het merk meeverhuist.
- Bewijs: `vibe_meet.py` regel VIBE-30; op WordPress `wp option get site_icon` geeft 0 en `grep -rn 'rel="icon"' <thema>/` vindt de verwijzing. Afgevinkt met beide.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O12 (favicon) en W4 (favicon in het thema); H paragraaf 2 punt 4.

### VIBE-31 Een eigen 404-pagina die 404 geeft
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Een niet-bestaande URL geeft status 404 en een eigen pagina in de huisstijl met een weg terug (link naar home of het menu).
- Bewijs: `vibe_meet.py` regel VIBE-31 (een willekeurige URL geeft 404, de pagina heeft het menu of een link naar `/`). Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O3 (werkende 404-pagina) en P1 (404); H paragraaf 2 punt 8.

### VIBE-32 De verplichte pagina's staan erop
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: De site heeft een privacyverklaring, een cookieverklaring met een werkende cookie-toestemming, algemene voorwaarden en een toegankelijkheidsverklaring, elk vanuit de footer bereikbaar en met 200.
- Bewijs: `vibe_meet.py` regel VIBE-32 (linkteksten privacy, cookie, voorwaarden en toegankelijkheid in de footer, elk 200). De werking van de toestemming toets je met PRIV-42 en PRIV-43; de inhoud van de verklaringen met PRIV-05 en PRIV-68. Afgevinkt met de uitvoer en die regels.
- Norm: Geen externe norm voor de lijst zelf; de inhoud volgt PRIV-05, PRIV-42, PRIV-43 en PRIV-68.
- Bron: website.md Stap 9, P1 (verplichte pagina's en elementen).

### VIBE-33 Analytics meet en Search Console verifieert de site
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: GA4 (een eigen property per project) stuurt na toestemming een meting; zonder toestemming stuurt het niets. Search Console is gekoppeld en de eigendom is geverifieerd.
- Bewijs: `vibe_meet.py` regel VIBE-33: zonder klik op de banner gaat er geen aanvraag naar `google-analytics.com/g/collect`, na een klik op "accepteren" wel, met het meet-ID erbij (alleen in de eigen browser; op de site verandert niets). Search Console: de property staat in de lijst van de GSC-hulpmiddelen met de eigendom geverifieerd. Afgevinkt met beide.
- Norm: Geen externe norm voor de koppeling; de toestemming volgt PRIV-40 en PRIV-43.
- Bron: website.md Stap 9, O25 (GA4 actief en meet data) en O35 (Search Console gekoppeld); Stap 8 (Google Analytics en Search Console).
