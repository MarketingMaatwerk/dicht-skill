# WP I: Serverlaag van klantsites: .htaccess, LiteSpeed en cache

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-64 Bewijs elke blokkade met een anonieme aanvraag op de echte server
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Beschouw een regel in `.htaccess` pas als werkend wanneer een anonieme aanvraag op de productieserver het verwachte antwoord geeft, vergelijk dat antwoord met een niet-bestaand pad in dezelfde map, en zet blokkades als `RewriteRule ... - [F,L]` bovenaan de `.htaccess` in de webroot in plaats van als `Require all denied` in een submap.
- Bewijs: Per blokkade twee regels curl-uitvoer: het geblokkeerde pad (403) en een verzonnen naam in dezelfde map (404, of ook 403 als de hele map dicht is), met datum en servernaam. Afgevinkt met die uitvoer. Een scan of een blik in het bestand telt niet.
- Norm: ASVS 5.0.0 V13.4.7 (L3), V13.4.3 (L2).

### WP-65 Zet eigen regels buiten het blok dat WordPress beheert
middel · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Plaats eigen regels in `.htaccess` (headers, blokkades, doorverwijzingen) boven `# BEGIN WordPress` en buiten de blokken van cacheplugins, en zet vaste doorverwijzingen van www en HTTP vóór de regels van een paginacache.
- Bewijs: `grep -n "BEGIN\|END" .htaccess` laat zien dat eigen regels vóór het eerste `BEGIN` staan; 10 tot 20 keer `curl -s -o /dev/null -w '%{http_code} %{num_redirects}\n' -L https://www.<domein>/` geeft steeds dezelfde uitkomst met één doorverwijzing. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V3.4.1 (L1) voor headers die moeten blijven staan.
- Zie ook: WEB-23, WEB-17, WEB-22

### WP-66 Sluit ingelogde en persoonlijke pagina's uit van de paginacache en meet het
kritiek · hard · klantproject | website | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Zorg dat de paginacache (LiteSpeed Cache, WP Super Cache of een andere) nooit een pagina opslaat of uitlevert die afhangt van wie er kijkt: winkelwagen, afrekenen, mijn account, ledenpagina's, pagina's met een eigen sessie- of inlogcookie en REST-antwoorden met gegevens van een gebruiker; voeg eigen cookies toe aan de uitzonderingen van de cacheplugin.
- Bewijs: Per persoonlijke URL: (1) twee verschillende ingelogde testgebruikers krijgen elk hun eigen inhoud, ook bij 10 aanvragen om en om; (2) een anonieme aanvraag direct daarna krijgt geen inhoud van een gebruiker; (3) de respons heeft `Cache-Control: no-store` of een cache-header die "miss" of "no-cache" aangeeft (bij LiteSpeed de header `x-litespeed-cache`). In LiteSpeed Cache staan de eigen cookies bij "Do Not Cache Cookies" en de eigen paden bij "Do Not Cache URIs". Afgevinkt met de uitvoer van de drie metingen.
- Norm: ASVS 5.0.0 V14.2.2 (L2), V14.3.2 (L2); OWASP Top 10 2025 A01.

### WP-67 Laat een gecachte pagina geen verlopen nonce uitleveren
middel · hard · klantproject | wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd de levensduur van een gecachte pagina met een formulier korter dan 12 uur, of haal de nonce op het moment van gebruik op via een niet-gecachte aanvraag, of laat de cacheplugin de nonce per bezoeker invullen; los een verlopen nonce nooit op door de controle te verwijderen.
- Bewijs: Een test die de pagina uit de cache haalt nadat hij er langer dan de ingestelde levensduur in staat (of met de klok van de testomgeving vooruit) en het formulier met succes verstuurt; `grep -rn "nonce" .` toont geen uitgecommentarieerde controles. Voor formulieren achter het eigen formulierschild geldt de eigen ondertekende tijdstempel (maximaal 7 dagen). Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V3.5.1 (L1).
