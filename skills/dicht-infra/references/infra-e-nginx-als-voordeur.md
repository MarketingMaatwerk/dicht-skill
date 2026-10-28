# INFRA E: nginx als voordeur

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-42 Draai een nginx-tak die nog fixes krijgt
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Pin de nginx-image op de huidige stable- of mainline-tak, en stap over zodra nginx.org een nieuwe tak als stable aanwijst.
- Bewijs: `docker exec <nginx> nginx -v` naast https://nginx.org/en/download.html; per advisory van het lopende jaar een regel "geraakt of niet, en waarom". Afgevinkt als de versie op een lopende tak staat en buiten elk kwetsbaar bereik valt.
- Norm: ASVS 5.0.0 V15.2.1 (L1); OWASP Top 10 2025 A03.
- Zie ook: GIT-93, API-72, WP-52, DB-93, INFRA-22, AI-54, SCR-33

### INFRA-43 Weiger verbindingen voor onbekende hostnamen
hoog · hard · api | app | mcp | website · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Maak één standaard-serverblok voor poort 443 met `ssl_reject_handshake on` en één voor poort 80 met `return 444`, beide met `default_server`, voor IPv4 en IPv6.
- Bewijs: `echo | openssl s_client -connect <ip>:443 -servername bestaat-niet.invalid 2>&1 | grep -iE 'alert|subject='` toont een handshake-fout en geen certificaat; `curl -s -o /dev/null -w '%{http_code}' -H 'Host: bestaat-niet.invalid' http://<ip>/` geeft `000`. Afgevinkt met beide uitvoeren, ook via IPv6.
- Norm: geen directe ASVS-eis (V13.4.6, L3, gaat over versie-informatie van backend-componenten, niet over hostnamen in een certificaat); onderbouwing van WEB-42.

### INFRA-44 Zet protocollen en ciphers volgens Mozilla "intermediate"
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in het `http`-blok `ssl_protocols TLSv1.2 TLSv1.3` en de zes cipher-suites van het Mozilla-profiel intermediate (versie 6.0), en gebruik het profiel modern (alleen TLS 1.3) voor diensten waar je alle clients kent.
- Bewijs: `nginx -T | grep -E '^\s*ssl_(protocols|ciphers|prefer_server_ciphers)'` toont precies deze regels en geen afwijkende; `openssl s_client -connect <host>:443 -tls1_1 </dev/null` mislukt; een scan met `testssl.sh` of internet.nl toont geen zwakke suites. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V12.1.1 (L1), V12.1.2 (L2; L3 eist uitsluitend suites met forward secrecy).
- Zie ook: WEB-56, WEB-17, WP-43, INFRA-55, INFRA-48, DB-60

### INFRA-45 Zet limieten en time-outs voor aanvragen expliciet
middel · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat `client_max_body_size` in het `http`-blok op 1m of lager staan en verhoog het alleen in de `location` van een uploadroute, en zet `client_header_timeout`, `client_body_timeout` en `send_timeout` op hooguit 30 seconden tenzij een route meer nodig heeft.
- Bewijs: `nginx -T | grep -nE 'client_max_body_size|client_(header|body)_timeout|send_timeout'` toont de hoge waarden alleen binnen een `location`; `curl -s -o /dev/null -w '%{http_code}' -X POST --data-binary @groot.bin https://<host>/api/login` geeft 413. Afgevinkt met beide uitvoeren. Zie ook WEB-43.
- Norm: ASVS 5.0.0 V15.2.2 (L2).
- Zie ook: API-18, WEB-43, API-19, ARCH-13, INV-44, INV-10, MSG-24

### INFRA-46 Begrens aanvragen per bron in nginx en antwoord met 429
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak per soort route (inloggen, formulieren, webhooks, zoekfuncties, algemeen) een `limit_req_zone` met de sleutel `$binary_remote_addr`, pas hem toe met een bewuste `burst`, en zet `limit_req_status 429`.
- Bewijs: `nginx -T | grep -nE 'limit_req'` toont zones en toepassingen; per beschermde route een lus (`for i in $(seq 1 30); do curl -s -o /dev/null -w '%{http_code}\n' ...; done | sort | uniq -c`) die 429 laat zien. Achter een extra proxy of CDN geldt WEB-51: de sleutel moet het echte clientadres zijn. Afgevinkt met de configuratie en de lus per route.
- Norm: ASVS 5.0.0 V15.2.2 (L2); OWASP API Security Top 10 2023 API4 (Unrestricted Resource Consumption).
- Zie ook: API-20, WEB-66, API-22, AUTH-10, WP-57, AI-45, AI-74

### INFRA-47 Herlaad nginx alleen na een geslaagde test en controleer dat de nieuwe configuratie draait
middel · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai vóór elke herlaadactie `nginx -t`, kijk welke configuratiebestanden sinds de vorige herlaadactie zijn gewijzigd, en controleer daarna met een aanvraag dat de wijziging actief is.
- Bewijs: De uitvoer van `nginx -t`; `find conf.d -newermt '<tijd laatste herlaadactie>'` toont alleen het eigen bestand; na de herlaadactie een `curl` die het nieuwe gedrag laat zien. Afgevinkt met de drie uitvoeren.
- Norm: geen ASVS-eis; voorwaarde voor betrouwbaar bewijs bij alle nginx-regels.
- Zie ook: ARCH-22, ARCH-23, ARCH-24, GIT-02, GIT-03, DB-41, DB-42

### INFRA-48 Controleer het certificaat van een upstream buiten de host
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet bij elke `proxy_pass https://...` naar een andere machine `proxy_ssl_verify on` met `proxy_ssl_trusted_certificate` en `proxy_ssl_server_name on`.
- Bewijs: `nginx -T | grep -nE 'proxy_pass https|proxy_ssl_'` toont bij elke externe upstream de drie regels. Afgevinkt met de uitvoer. Upstreams op loopback of op het eigen Docker-netwerk vallen hierbuiten.
- Norm: ASVS 5.0.0 V12.3.2 (L2), V12.3.4 (L2).
- Zie ook: WEB-56, WEB-17, WP-43, INFRA-44, INFRA-55, DB-60

### INFRA-49 → WEB-23
Samengevoegd: "Zet security headers op één plek en laat ze overerven" is gedekt door WEB-23. Gebruik die regel.
