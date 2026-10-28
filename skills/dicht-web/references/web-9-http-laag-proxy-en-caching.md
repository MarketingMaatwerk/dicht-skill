# WEB 9: HTTP-laag, proxy en caching

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-50 Voorkom request smuggling tussen proxy en applicatie
hoog · hard · api | app | website | mcp · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Laat de proxy en de applicatie dubbelzinnige aanvragen weigeren (zowel `Transfer-Encoding` als `Content-Length`, ongeldige headers), houd nginx en Node.js op een ondersteunde versie met alle beveiligingsfixes, en zet geen eigen HTTP-parser of tweede proxy tussen nginx en de applicatie zonder dit te testen.
- Bewijs: (1) `node --version` en de nginx-versie staan op een ondersteunde release (controleer tegen de releasepagina's, zie INFRA en GIT). (2) Een aanvraag met beide headers (`printf 'POST / HTTP/1.1\r\nHost: <host>\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\n' | openssl s_client -quiet -connect <host>:443`) geeft 400 of sluit de verbinding. Afgevinkt met versies en uitvoer. Alleen uitvoeren op een eigen testomgeving.
- Norm: ASVS 5.0.0 V4.2.1 (L2), V4.2.2 tot en met V4.2.4 (L3); OWASP Top 10 2025 A02 en A03.

### WEB-51 Vertrouw proxy-headers alleen van de eigen proxy
hoog · hard · api | app | website | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat de reverse proxy `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Forwarded-Host`, `X-Real-IP` en elke interne header (`X-User-Id`, `X-Tenant`, frameworkheaders) overschrijven of verwijderen op binnenkomende aanvragen, stel in de applicatie precies in welke proxy vertrouwd wordt (Fastify `trustProxy` met het adres van de proxy, nooit blind `true` op een poort die van buiten bereikbaar is), en bind de applicatie aan `127.0.0.1` of een intern Docker-netwerk. Aanvulling uit API-21: Een CIDR-blok van de eigen proxy mag ook.
- Bewijs: (1) Twee aanvragen met verschillende `X-Forwarded-For` leveren in het applicatielog hetzelfde, echte client-IP op. (2) De applicatiepoort is van buiten niet bereikbaar: `curl http://<publiek-ip>:<poort>/` faalt en `ss -tlnp` toont `127.0.0.1` of een Docker-netwerk. (3) De limiettest uit WEB-66 slaagt ook met wisselende `X-Forwarded-For`. Afgevinkt met de drie uitvoeren.
    Ook (uit API-21): `grep -rn "trustProxy" src` toont een lijst adressen. Test: een verzoek rechtstreeks op de servicepoort met `X-Forwarded-For: 1.2.3.4` logt niet `1.2.3.4` als `req.ip`. In nginx staat `proxy_set_header X-Real-IP $remote_addr`.
- Norm: ASVS 5.0.0 V4.1.3 (L2), V15.3.4 (L2); OWASP Top 10 2025 A01 en A02.
- Dekt ook: API-21

### WEB-52 Zet no-store op elke respons met persoonlijke of ingelogde inhoud
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur `Cache-Control: no-store` op elke respons die afhangt van wie er is ingelogd of die persoonsgegevens, tokens of bestelgegevens bevat, en sluit die routes expliciet uit van elke paginacache (nginx `proxy_cache`, WP Super Cache, LiteSpeed Cache, CDN). Aanvulling uit API-15: Geldt ook voor gegevens van één account en voor antwoorden van een MCP-server.
- Bewijs: `curl -sI` met een geldige sessiecookie op elke ingelogde route toont `Cache-Control: no-store`; daarna dezelfde URL zonder cookie opvragen geeft geen inhoud van de ingelogde gebruiker en geen cache-hit-header (`X-Cache`, `X-LiteSpeed-Cache: hit`, `X-Cache-Status`). Afgevinkt met beide uitvoeren per route.
    Ook (uit API-15): `curl -sI` op elke accountroute toont `cache-control: no-store`. Een hook op de plugin met accountroutes zet de header standaard.
- Norm: ASVS 5.0.0 V14.3.2 (L2), V14.2.2 (L2); OWASP Top 10 2025 A02 en A04.
- Dekt ook: API-15

### WEB-53 Sluit web cache deception uit
hoog · hard · website | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat de cache alleen opslaan wat de applicatie met `Cache-Control` als cachebaar aanmerkt, laat cacheregels op extensie of pad die header nooit overschrijven, en laat de applicatie 404 geven op een onbekend pad in plaats van de inhoud van een bovenliggende route.
- Bewijs: Ingelogd `https://<host>/<privéroute>/x.css`, `/<privéroute>;x.css` en `/<privéroute>%2fx.css` opvragen: de respons is 404, of bevat `Cache-Control: no-store` en wordt bij een tweede aanvraag zonder cookie niet uit de cache geserveerd. `grep -n proxy_ignore_headers` in de nginx-configuratie is leeg of verklaard. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V14.2.5 (L3; hard omdat het ingelogde data raakt, besluit 6).

### WEB-54 Laat niets uit de aanvraag in een gecachte respons belanden dat niet in de cachesleutel zit
hoog · hard · website | app | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik in een cachebare respons geen waarde uit een header, cookie of parameter die geen deel is van de cachesleutel; verwijder headers die de applicatie niet nodig heeft bij de proxy, weiger een GET met body, en stuur `Vary` mee voor elke header waar de respons wel van afhangt.
- Bewijs: Vraag een cachebare pagina op met `X-Forwarded-Host: evil.example`, `X-Forwarded-Scheme: http` en `X-Original-URL: /x`, en daarna zonder die headers: de tweede respons bevat geen spoor van de eerste. De nginx-cachesleutel is nagelezen (standaard `$scheme$proxy_host$request_uri`). Afgevinkt met de twee uitvoeren. De drie testheaders zijn praktijkkennis.
- Norm: ASVS 5.0.0 V14.2.2 (L2), V4.1.3 (L2); OWASP Top 10 2025 A02.

### WEB-55 Zet geen gevoelige gegevens in de URL
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur sessietokens, API-sleutels, wachtwoorden en persoonsgegevens alleen in de body of in een header; een eenmalig token in een maillink (reset, bevestiging) is de enige uitzondering en vervalt direct na gebruik (zie AUTH). Aanvulling uit API-16: Dus nooit in pad of query.
- Bewijs: `grep -rnE "\?(.*&)?(token|key|api_key|password|secret|sessie|email)=" src/` en de routetabel nagelopen; een steekproef uit het toegangslog bevat geen tokens of e-mailadressen in de querystring. Afgevinkt met grep en logsteekproef.
    Ook (uit API-16): `grep -rnE "token=|key=|apikey=|password=" src` in URL-opbouw is leeg. Steekproef in `access.log`: geen tokens of e-mailadressen in het pad. Uitzondering: eenmalige links per mail (zie AUTH voor levensduur en eenmalig gebruik).
- Norm: ASVS 5.0.0 V14.2.1 (L1); OWASP Top 10 2025 A04; AVG artikel 32 (logs zonder persoonsgegevens, zie PRIV).
- Dekt ook: API-16

### WEB-56 Serveer alles over HTTPS; laat een API niet stil doorsturen
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak elke publieke dienst alleen via HTTPS met een publiek vertrouwd certificaat bereikbaar; stuur op poort 80 alleen pagina's voor mensen door naar HTTPS, en laat een API of webhook-eindpunt op HTTP een fout geven in plaats van een redirect.
- Bewijs: `curl -sI http://<site>/` geeft 301 naar `https://` op dezelfde host; `curl -si http://<api-host>/v1/…` geeft geen 301 maar een fout (of de poort is dicht); `curl -sI https://<host>/` slaagt zonder `-k`. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V12.2.1 en V12.2.2 (L1), V4.1.2 (L2); OWASP Top 10 2025 A04.
- Zie ook: WEB-17, WP-43, INFRA-44, INFRA-55, INFRA-48, DB-60

### WEB-57 Sta alleen de HTTP-methoden toe die de route gebruikt
laag · richtlijn · api | app | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat per route alleen de gebruikte methoden toe, geef 405 op de rest, en zorg dat `TRACE` in productie niet werkt.
- Bewijs: `curl -si -X TRACE https://<host>/` geeft 405 of 400; `curl -si -X PUT` op een route die alleen POST kent geeft 404 of 405. In nginx kan `limit_except` per `location` de methoden beperken. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.4.4 (L2), V4.1.4 (L3).
