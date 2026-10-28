# WEB 13: Indexatie en service workers

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-71 Gebruik robots.txt nooit als afscherming
hoog · hard · website | wp-thema | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Scherm privépagina's af met authenticatie; wil je een publieke pagina uit de zoekresultaten houden, stuur dan `X-Robots-Tag: noindex` of een `<meta name="robots" content="noindex">` en blokkeer die pagina juist niet in robots.txt. Zet geen geheime paden in robots.txt.
- Bewijs: `curl -s https://<host>/robots.txt` bevat geen pad naar iets vertrouwelijks; elke privéroute geeft zonder sessie 401, 403 of een redirect naar de login; pagina's die niet geïndexeerd mogen worden geven `X-Robots-Tag: noindex` (`curl -sI`) en zijn niet geblokkeerd in robots.txt. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V13.4.5 (L2); OWASP Top 10 2025 A01 en A02.

### WEB-72 Zet test-, staging- en demo-omgevingen achter een login en op noindex
middel · hard · website | wp-thema | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak elke omgeving die niet voor het publiek is alleen bereikbaar met authenticatie (basic auth of een IP-allowlist op de webserver), stuur daar `X-Robots-Tag: noindex, nofollow` op alle responsen, en gebruik er geen kopie van echte klantdata.
- Bewijs: `curl -sI https://<test-host>/` geeft 401 of 403 zonder inloggegevens en toont `X-Robots-Tag: noindex, nofollow`; een zoekopdracht `site:<test-host>` geeft geen resultaten. Afgevinkt met de uitvoer. Voor demo's die publiek moeten zijn (showcases): alleen `noindex`, geen klantdata, en een genoteerd besluit.
- Norm: ASVS 5.0.0 V13.4.5 (L2), V15.2.3 (L2); AVG artikel 32 (geen echte persoonsgegevens in test, zie PRIV).
- Zie ook: ARCH-48, DB-85, INFRA-74, ARCH-50, ARCH-08

### WEB-73 Houd een service worker klein in bereik en laat hem geen privédata cachen
middel · hard · app | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Registreer een service worker alleen met het kleinste bereik dat nodig is, verruim het bereik niet met `Service-Worker-Allowed`, cache alleen statische bestanden van de eigen origin, en sla nooit responsen van ingelogde of persoonlijke routes op in de Cache API.
- Bewijs: In de code van de worker: de lijst van te cachen paden is een allowlist van statische bestanden; `grep -n "cache.put\|cache.addAll\|respondWith" sw.js` nagelopen; na uitloggen in een e2e-test is `caches.keys()` leeg of zonder API-inhoud (WEB-27 stuurt `Clear-Site-Data: "storage"`, dat ook service worker-registraties verwijdert). `curl -sI <sw-url>` toont geen `Service-Worker-Allowed`. Afgevinkt met code en test.
- Norm: ASVS 5.0.0 V14.3.1 (L1), V14.3.3 (L2).

### WEB-74 Zorg dat je een service worker kunt terugtrekken
laag · richtlijn · app · tegenlezer: bevestigd (04-10-2026)
- Regel: Lever het bestand van de service worker uit zonder lange cache (`Cache-Control: no-cache`), houd de URL stabiel, en heb een geteste noodversie klaar die alle caches wist en zichzelf afmeldt.
- Bewijs: `curl -sI <sw-url>` toont `Cache-Control: no-cache` of `max-age=0`; een e2e-test installeert de worker, zet de noodversie live en stelt vast dat de registratie en de caches weg zijn. Afgevinkt met header en test.
- Norm: Geen eigen ASVS-eis; ondersteunt ASVS 5.0.0 V14.3.1.
