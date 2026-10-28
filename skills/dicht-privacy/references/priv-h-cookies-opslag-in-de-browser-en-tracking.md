# PRIV H: cookies, opslag in de browser en tracking

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-40 Plaats of lees niets op het apparaat vóór toestemming, behalve wat strikt nodig is
hoog · hard · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laad geen script, pixel of ingesloten dienst die informatie op het apparaat van de bezoeker opslaat of uitleest voordat de bezoeker toestemming gaf, tenzij de opslag strikt noodzakelijk is voor de gevraagde dienst (sessie, winkelwagen, de cookiekeuze zelf, beveiliging) of valt onder de uitzondering voor meting met geringe gevolgen (PRIV-44).
- Bewijs: Een Playwright-test met een schone browser laadt elk paginatype zonder op de banner te klikken en legt vast: alle cookies, alle sleutels in localStorage en sessionStorage, en alle aangeroepen hosts. De lijst bevat alleen wat in het register onder `necessary` staat en hosts uit de eigen lijst. Afgevinkt met de testuitvoer per paginatype. Technisch af te dwingen als gate.
- Norm: Telecommunicatiewet artikel 11.7a lid 1 en 3; AVG artikel 6 lid 1 onder a.
- Zie ook: PRIV-19, WEB-59, WEB-58, PRIV-46

### PRIV-41 De regel geldt voor elke techniek, niet alleen voor cookies
hoog · hard · website | wp-plugin | app | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Pas PRIV-40 ook toe op localStorage en sessionStorage zodra de inhoud wordt uitgelezen of verstuurd, op trackingpixels in pagina's en in e-mail, op volgparameters in links, en op fingerprinting.
- Bewijs: De test uit PRIV-40 legt ook web storage vast; `grep -rnE "localStorage|sessionStorage|navigator\.(plugins|hardwareConcurrency)|canvas.*toDataURL" src/` is verklaard per treffer; in mailsjablonen `grep -rniE "<img[^>]+(width=.?1|height=.?1|track|open)"` is leeg of valt onder een vastgelegde toestemming. Afgevinkt met de drie. Technisch af te dwingen. Zie WEB-26 voor wat niet in web storage hoort.
- Norm: Telecommunicatiewet artikel 11.7a lid 1 en 2; Richtlijn 2002/58/EG artikel 5 lid 3.

### PRIV-42 Weigeren is even makkelijk als accepteren, en niets staat vooraf aan
hoog · hard · website | wp-thema | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw de cookiebanner met de knoppen voor weigeren en accepteren op dezelfde laag en even zichtbaar, zonder vooraf aangevinkte keuzes, en met een altijd bereikbare plek om de keuze te wijzigen of in te trekken.
- Bewijs: Een e2e-test telt de klikken: weigeren kost niet meer klikken dan accepteren en beide knoppen staan in de eerste laag; na weigeren zijn er geen andere cookies of opslag dan onder `necessary`; een link "cookie-instellingen" staat op elke pagina en heropent de keuze. Afgevinkt met de testuitvoer. Technisch af te dwingen. De banner valt ook onder de toegankelijkheidseisen (PRIV-66).
- Norm: AVG artikel 4 punt 11, artikel 7 lid 3; Telecommunicatiewet artikel 11.7a.

### PRIV-43 De toestemmingsstatus stuurt de code, niet alleen de banner
hoog · hard · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elk script en elke ingesloten dienst die toestemming nodig heeft pas laden via één centrale functie die de opgeslagen keuze leest, en laat het intrekken van de keuze de bijbehorende cookies en opslag verwijderen en het script stoppen.
- Bewijs: De test uit PRIV-40 in drie standen (geen keuze, geweigerd, geaccepteerd en daarna ingetrokken): alleen in de stand "geaccepteerd" verschijnen de niet-noodzakelijke cookies en hosts, en na intrekken zijn ze weg. Afgevinkt met de drie uitvoeren. Technisch af te dwingen.
- Norm: AVG artikel 7 lid 1 en 3; Telecommunicatiewet artikel 11.7a lid 1.

### PRIV-44 Meet zonder toestemming alleen wat geen of geringe gevolgen heeft, en dan zelf gehost
middel · richtlijn · website | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Kies voor meting zonder toestemming een eigen of zelf gehoste oplossing die geen bezoeker herkent over bezoeken heen, geen IP-adres bewaart, niets met derden deelt en alleen de kwaliteit of het effect van de eigen dienst meet; alles wat daarboven gaat (sessieverloop, herkenning, A/B per bezoeker) vraagt toestemming.
- Bewijs: De beschrijving van de meting in het register noemt per laag wat wordt vastgelegd; de test uit PRIV-40 laat zien dat laag 1 niets opslaat op het apparaat; `grep` in de metingscode toont dat het IP-adres niet wordt weggeschreven. Afgevinkt met de drie. Of een concrete meting onder de uitzondering valt: `[jurist]`, en let op de bewaartermijn van 13 maanden voor de cookie in laag 2 tegenover de uitspraak van de AP over een half jaar.
- Norm: Telecommunicatiewet artikel 11.7a lid 3 onder b.

### PRIV-45 De cookielijst in de verklaring is de gemeten lijst
middel · hard · website | wp-thema | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Genereer de lijst van cookies en opslagsleutels in de cookieverklaring uit een meting van de site (naam, doel, partij, bewaartermijn) en herhaal die meting bij elke oplevering en na elke update van plugins of thema.
- Bewijs: De uitvoer van de test uit PRIV-40 in de stand "geaccepteerd" wordt vergeleken met `cookies:` in het register; elk verschil is een fout. Afgevinkt met de vergelijking. Technisch af te dwingen.
- Norm: Telecommunicatiewet artikel 11.7a lid 1 onder a; AVG artikel 13.

### PRIV-46 Laad ingesloten inhoud van derden pas na een klik
middel · hard · website | wp-thema | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Toon voor video's, kaarten, agenda-widgets, chat en sociale inbeddingen eerst een eigen plaatje met een knop, en laad de inhoud van de derde pas na de klik of na toestemming voor die categorie.
- Bewijs: De test uit PRIV-40 op pagina's met inbeddingen: vóór de klik geen host van de derde in de netwerklog. Afgevinkt met de testuitvoer. Technisch af te dwingen; de CSP `frame-src` kan het afdwingen op pagina's zonder inbedding.
- Norm: Telecommunicatiewet artikel 11.7a lid 1; zie WEB-58 en WEB-59.
- Zie ook: PRIV-19, WEB-59, WEB-58, PRIV-40
