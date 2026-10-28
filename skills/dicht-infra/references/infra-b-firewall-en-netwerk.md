# INFRA B: Firewall en netwerk

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-12 Weiger inkomend verkeer standaard en bewijs het van buiten
kritiek · hard · api | app | mcp · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Zet de hostfirewall op standaard weigeren voor inkomend verkeer, open alleen de poorten die een publieke dienst nodig heeft, en controleer het resultaat met een poortscan vanaf een andere machine.
- Bewijs: `sudo ufw status verbose` toont `Default: deny (incoming)`; een scan vanaf een andere host (`nmap -Pn -p- <ipv4>` en `nmap -6 -Pn -p- <ipv6>`) toont alleen de bedoelde poorten. Afgevinkt met beide uitvoeren en de datum.
- Norm: ASVS 5.0.0 V13.4.5 (L2). V13.2.4 (L2) gaat over de allowlist voor uitgaande verbindingen en dekt deze regel niet.
- Zie ook: INFRA-13, DB-58, INFRA-14, AI-75, AI-39

### INFRA-13 Publiceer containerpoorten alleen op loopback
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf elke poortpublicatie in Compose als `127.0.0.1:<poort>:<poort>`, behalve voor de reverse proxy op 80 en 443, en publiceer een poort helemaal niet als alleen andere containers hem nodig hebben.
- Bewijs: `docker ps --format '{{.Names}}\t{{.Ports}}'` toont `0.0.0.0` of `[::]` alleen bij de proxy; `grep -nE '^\s*-\s*"?[0-9]+:[0-9]+' docker-compose.yml` is leeg. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V13.4.5 (L2); OWASP Top 10 2025 A02 Security Misconfiguration.
- Zie ook: DB-58, INFRA-14, INFRA-12, AI-75, AI-39

### INFRA-14 Laat hostdiensten niet op alle adressen luisteren
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bind elke dienst die buiten Docker op de host draait aan `127.0.0.1` of aan het adres van de Docker-bridge, en nooit aan `0.0.0.0` of `::`.
- Bewijs: `sudo ss -tulnp | awk '$5 !~ /^(127\.|\[::1\]|172\.)/'` toont alleen sshd en de proxy (en bewust publieke diensten, met reden). Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.4.5 (L2); OWASP Top 10 2025 A02.
- Zie ook: INFRA-13, DB-58, INFRA-12, AI-75, AI-39

### INFRA-15 Zet een tweede firewall buiten de host
middel · richtlijn · api | app | mcp · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Zet bij de hostingprovider een netwerkfirewall voor de server met dezelfde korte lijst van publieke poorten.
- Bewijs: Schermafdruk of API-uitvoer van de firewallregels bij de provider, met de datum, en de vergelijking met de lijst uit INFRA-12. Afgevinkt als beide lijsten gelijk zijn.
- Norm: geen ASVS-eis voor inkomend verkeer. ASVS 5.0.0 V13.2.4 (L2) noemt de firewall als laag ("firewall, or a combination of different layers"), maar voor de allowlist van uitgaande verbindingen; hier alleen naar analogie.

### INFRA-16 Neem IPv6 mee in elke controle
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Voer elke firewall-, poort- en bindcontrole uit voor IPv4 en voor IPv6.
- Bewijs: De scan uit INFRA-12 is voor beide adresfamilies gedaan; `sudo ufw status` toont de `(v6)`-regels; `curl -6 -sI https://<host>/<beheerpad>` geeft dezelfde weigering als `curl -4`. Afgevinkt met de uitvoer voor beide.
- Norm: ASVS 5.0.0 V13.4.5 (L2).

### INFRA-17 Geef elke applicatie een eigen netwerk
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet elke applicatie met haar eigen database in een eigen Compose-netwerk, en koppel alleen de container die verkeer van de proxy krijgt aan het gedeelde proxynetwerk.
- Bewijs: `docker network inspect <netwerk> --format '{{range .Containers}}{{.Name}} {{end}}'` per netwerk; elke database staat alleen op het netwerk van zijn eigen applicatie. Een proef: `docker exec <vreemde container> nc -zv <db-host> 5432` mislukt. Afgevinkt met de lijst en de proef.
- Norm: ASVS 5.0.0 V13.2.2 (L2), V13.2.4 (L2).

### INFRA-18 Beperk uitgaand verkeer van containers die adressen van buiten ophalen
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet een container die URL's uit invoer ophaalt (screenshots, scrapers, webhooks, MCP-tools) in een netwerk zonder route naar de interne diensten, en leg vast met welke externe systemen elke applicatie mag praten.
- Bewijs: Het document met externe verbindingen per applicatie bestaat (ASVS V13.1.1); `docker exec <ophaalcontainer> nc -zv <interne dienst> <poort>` mislukt. Afgevinkt met document en proef.
- Norm: ASVS 5.0.0 V13.1.1 (L2), V13.2.4 (L2), V13.2.5 (L2).
- Zie ook: WEB-40, WEB-41, API-48, API-47, AI-48, WP-28, INV-59, INV-61, MSG-27, MSG-46

### INFRA-19 Leg de kernelinstellingen voor het netwerk vast
laag · richtlijn · api | app | mcp · tegenlezer: scherpen (04-10-2026) · bron niet gelezen: CIS
- Regel: Zet in `/etc/sysctl.d/` minimaal `net.ipv4.conf.all.accept_redirects=0`, `net.ipv4.conf.all.send_redirects=0`, `net.ipv4.conf.all.accept_source_route=0`, `net.ipv4.tcp_syncookies=1`, `kernel.dmesg_restrict=1` en `kernel.kptr_restrict=1`, en controleer ze na elke herstart.
- Bewijs: `sysctl net.ipv4.conf.all.accept_redirects net.ipv4.conf.all.send_redirects net.ipv4.conf.all.accept_source_route net.ipv4.tcp_syncookies kernel.dmesg_restrict kernel.kptr_restrict` geeft `0 0 0 1 1 1`. `send_redirects` staat voor een interface aan zodra `all` of de interface zelf op 1 staat: zet daarom ook `net.ipv4.conf.default.send_redirects=0` en controleer met `sysctl -a 2>/dev/null | grep '\.send_redirects'` dat elke interface 0 geeft. Afgevinkt met de uitvoer. Let op: `net.ipv4.ip_forward=1` hoort bij Docker en is geen afwijking.
- Norm: geen ASVS-eis; CIS Ubuntu Linux Benchmark heeft hier regels voor, nummers niet bevestigd (Niet bevestigd punt 1).
