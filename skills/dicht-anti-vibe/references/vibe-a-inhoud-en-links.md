# VIBE A: Inhoud en links

Compacte regels van `dicht-anti-vibe`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/anti-vibe.md` (regelnummer in `regel-index.tsv`).

### VIBE-01 Geen placeholdertekst, voorbeeldinhoud of tool-URL in productie
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: In de gerenderde HTML van elke pagina staat geen "lorem ipsum", "Your text here", "Coming soon", "Binnenkort", voorbeeldnamen, voorbeeldprijzen of een link of bron naar een tool- of testdomein (`example.com`, `localhost`, een ander `testomgeving.example`-adres, `placeholder`-diensten, `vercel.app`, `netlify.app`).
- Bewijs: `vibe_meet.py` regel VIBE-01 is `goed` (zoekt in de tekst en in elke `href` en `src` van elke gemeten pagina). Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O1 (placeholder- of tool-URL) en A7 (geen placeholdertekst); H paragraaf 2 punt 14.

### VIBE-02 Geen nepcijfers, neplogo's, nepbadges of nepreviews
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elk cijfer over bezoekers, klanten of resultaten, elk "trusted by"-logo, elke badge en elke review op de site is echt en heeft een bron in de intake (Stap 2) of een mail van de klant. Geen bron: weghalen.
- Bewijs: `vibe_meet.py` regel VIBE-02 noemt de kandidaten (getallen met "+", "klanten", "reviews", "trusted by", sterrenrijen); in het bewijsbestand staat per kandidaat de bron (intake of mail met datum) of dat hij is weggehaald. Afgevinkt met die lijst.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O23 (reviews echt), O30 (geen nep bezoekers- of klantaantallen) en O31 (geen nep trusted-by-logo's, nepmetrics of badges); Stap 8 boilerplate (reviews uit Stap 2, geen placeholders).

### VIBE-03 Elke link werkt
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Crawl alle interne en externe links van elke pagina: geen enkele geeft 4xx of 5xx, geen link wijst naar `#` of een lege `href`, en geen navigatielink is dood. Leg het aantal gecontroleerde links vast.
- Bewijs: `vibe_meet.py` regel VIBE-03 is `goed` en noemt het aantal gecontroleerde links (intern en extern). Een externe site die bots weigert (403, 429, 999) staat als `niet gemeten` met de URL; open die met de hand of in Playwright. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, A1 (kapotte links) en O28 (geen dode interne navigatielinks); H paragraaf 2 punt 2 en 7.

### VIBE-04 Social-links werken, of het icoon staat er niet
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elk social-icoon linkt naar het echte profiel van de klant (gevonden in Stap 1). Geen kanaal gevonden: icoon weglaten, nooit een `#`-link of een link naar de homepage van het platform.
- Bewijs: `vibe_meet.py` regel VIBE-04: elke link naar facebook, instagram, linkedin, x/twitter, youtube of tiktok heeft een pad na de domeinnaam en geeft geen 404; platforms die bots weigeren staan als `niet gemeten` en worden met de hand geopend. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O29; Stap 8 S4 (social links).

### VIBE-05 Het copyright-jaar is actueel en wordt berekend
laag · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Het jaar in de footer is het huidige jaar en komt uit code (`<?php echo esc_html( wp_date( 'Y' ) ); ?>` of `new Date().getFullYear()`), nooit vast in een sjabloon of in de database.
- Bewijs: `vibe_meet.py` regel VIBE-05 vindt het huidige jaar naast het copyrightteken; en `grep -rnE "(&copy;|©)[^<]{0,20}20[0-9]{2}" <thema>/` geeft niets (een vast jaar in de broncode). Afgevinkt met beide uitvoeren.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O33; Stap 8 S3; H paragraaf 2 punt 9.

### VIBE-06 Echte SVG-iconen, geen emoji als icoon
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Iconen in knoppen, menu, lijsten, kaarten en kopjes zijn SVG (Lucide of het officiële merkicoon), nooit een emoji.
- Bewijs: `vibe_meet.py` regel VIBE-06 vindt geen emoji (Unicode-blokken 1F300 tot 1FAFF en 2600 tot 27BF) in de tekst van `button`, `a`, `nav`, `li`, `h1` tot en met `h4`, `header` en `footer`. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O32; Stap 8 S5 (iconen).

### VIBE-07 Logo, telefoonnummer en e-mailadres zijn klikbaar
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Het logo linkt naar de homepage; elk telefoonnummer is een `tel:`-link (of een bewust gekozen WhatsApp-link `https://wa.me/`) en elk e-mailadres een `mailto:`-link, overal waar ze zichtbaar staan (header, contact, footer, tekst). Telefoon en e-mailadres staan zichtbaar in footer of contactsectie, niet alleen een formulier.
- Bewijs: `vibe_meet.py` regel VIBE-07: het logo in `header` linkt naar `/`, elke tekst die op een telefoonnummer of e-mailadres lijkt staat in een `a[href^="tel:"]` of `a[href^="mailto:"]`, en elke pagina heeft minstens één van beide. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, A5 (klikbaar); Stap 8 S2 (contactgegevens zichtbaar); H paragraaf 2 punt 17, 18 en 19.

### VIBE-08 De inhoud uit de intake staat erop
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: De reactietijd-belofte uit Stap 2 staat zichtbaar bij contact of CTA; er staan minstens 5 FAQ's; de teamfoto staat erop als de klant er een aanleverde; bij een fysieke locatie staan een kaart en een routebeschrijving. Een kaart van Google laadt pas na een klik of toestemming (PRIV-46).
- Bewijs: `vibe_meet.py` regel VIBE-08 telt de FAQ's (FAQPage in JSON-LD, anders `details` of de FAQ-sectie) en meldt of een Maps-iframe al bij laden verschijnt; in het bewijsbestand staat per punt de plek op de site (URL en sectie) of `nvt` met reden (geen teamfoto aangeleverd, geen fysieke locatie). Afgevinkt met beide.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook PRIV-46.
- Bron: website.md Stap 9, O22 (reactietijd-belofte), O24 (Maps en route), O26 (teamfoto), O27 (minimaal 5 FAQ's).

### VIBE-09 Geen lege of losse pagina's; een logische linkstructuur
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elk menu-item wijst naar een pagina met echte inhoud; er is geen pagina in de sitemap waar geen enkele interne link naartoe gaat; pagina's en secties linken logisch naar elkaar. Breadcrumbs staan er waar de site meer dan twee niveaus heeft.
- Bewijs: `vibe_meet.py` regel VIBE-09: elke menu-pagina heeft minstens 80 woorden tekst in `main`, en elke URL uit de sitemap wordt vanaf minstens één gemeten pagina gelinkt. Breadcrumbs: in het bewijsbestand de URL waar ze staan of `nvt` (site met twee niveaus of minder). Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O19 (breadcrumbs), O20 (interne linkstructuur) en A3 (geen menu-item of pagina die ongebruikt of leeg is); H paragraaf 2 punt 15.
