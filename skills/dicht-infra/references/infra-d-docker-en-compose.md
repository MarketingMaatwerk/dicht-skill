# INFRA D: Docker en Compose

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-26 Geef geen container toegang tot de Docker-socket
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Koppel `/var/run/docker.sock` nooit in een container en zet de Docker-API nooit open op een TCP-poort.
- Bewijs: `for c in $(docker ps -q); do docker inspect --format '{{.Name}} {{range .Mounts}}{{.Source}} {{end}}' $c; done | grep docker.sock` is leeg; `sudo ss -tlnp | grep -E ':(2375|2376)\b'` is leeg. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V13.2.2 (L2); OWASP Top 10 2025 A02.

### INFRA-27 Draai het proces in de container niet als root
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in elke eigen Dockerfile een `USER` met een vast, niet-nul UID, of zet `user:` in Compose, en controleer het op de draaiende container.
- Bewijs: `for c in $(docker ps -q); do docker exec $c id -u 2>/dev/null | sed "s|^|$(docker inspect --format '{{.Name}}' $c) |"; done` geeft voor elke eigen container een UID ongelijk aan 0; uitzonderingen (officiële database-images die zelf van root naar een eigen gebruiker wisselen) zijn genoteerd. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.2.2 (L2).

### INFRA-28 Laat alle capabilities vallen en geef alleen terug wat nodig is
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `cap_drop: [ALL]` op elke service en voeg met `cap_add` alleen de capabilities toe die de dienst aantoonbaar nodig heeft.
- Bewijs: `docker inspect --format '{{.Name}} {{.HostConfig.CapDrop}} {{.HostConfig.CapAdd}}' $(docker ps -q)` toont `[ALL]` bij elke eigen service en een verklaarde lijst bij `CapAdd`. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.2.2 (L2).

### INFRA-29 Verbied het verkrijgen van nieuwe rechten in de container
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `security_opt: ["no-new-privileges:true"]` op elke service.
- Bewijs: `docker inspect --format '{{.Name}} {{.HostConfig.SecurityOpt}}' $(docker ps -q)` toont `no-new-privileges` bij elke eigen service. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.2.2 (L2).

### INFRA-30 Maak het bestandssysteem van de container alleen-lezen
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `read_only: true` op elke service en geef schrijfbare plekken expliciet als `tmpfs` of als benoemd volume.
- Bewijs: `docker inspect --format '{{.Name}} {{.HostConfig.ReadonlyRootfs}}' $(docker ps -q)` toont `true` voor elke eigen service of een genoteerde reden; `docker exec <container> touch /app/x` geeft `Read-only file system`. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V13.2.2 (L2).

### INFRA-31 Geen privileged containers en geen namespaces van de host
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik nooit `privileged: true`, en gebruik `network_mode: host` of `pid: host` alleen met een geschreven onderbouwing en dan samen met INFRA-27 tot en met INFRA-30.
- Bewijs: `docker inspect --format '{{.Name}} priv={{.HostConfig.Privileged}} net={{.HostConfig.NetworkMode}} pid={{.HostConfig.PidMode}}' $(docker ps -q)` toont nergens `priv=true`; elke `net=host` heeft een notitie met reden en de aanvullende maatregelen. Afgevinkt met uitvoer en notities.
- Norm: ASVS 5.0.0 V13.2.2 (L2); OWASP Top 10 2025 A02.
- Zie ook: INV-40, INV-32, INV-35, INV-36, INFRA-32

### INFRA-32 Zet op elke container een limiet voor geheugen en processen
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke service een geheugenlimiet en een `pids_limit`, en een cpu-limiet voor diensten die werk van buiten uitvoeren.
- Bewijs: `docker inspect --format '{{.Name}} mem={{.HostConfig.Memory}} pids={{.HostConfig.PidsLimit}}' $(docker ps -q)` toont nergens `mem=0` of `pids=<nil>`; de som van de geheugenlimieten blijft onder het geheugen van de host. Afgevinkt met de uitvoer en de optelling.
- Norm: ASVS 5.0.0 V15.2.2 (L2).
- Zie ook: INV-40, INV-32, INV-35, INV-36, INFRA-31

### INFRA-33 Begrens de containerlogs
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in `/etc/docker/daemon.json` de logdriver `local`, of `json-file` met `max-size` en `max-file`, en maak bestaande containers daarna opnieuw aan.
- Bewijs: `docker info --format '{{.LoggingDriver}}'` en `cat /etc/docker/daemon.json`; `docker inspect --format '{{.Name}} {{.HostConfig.LogConfig}}' $(docker ps -q)` toont bij elke container een limiet; `sudo du -sh /var/lib/docker/containers/*/*-json.log | sort -h | tail -3` toont geen bestand boven de limiet. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V16.1.1 (L2, logbeleid met bewaartermijn).
- Zie ook: ARCH-71, PRIV-23, PRIV-55, INFRA-88

### INFRA-34 → GIT-95
Samengevoegd: "Houd geheimen uit de image, uit de buildgeschiedenis en uit `docker inspect`" is gedekt door GIT-95. Gebruik die regel.

### INFRA-35 Geef elke service een healthcheck en een herstartbeleid
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke service een `healthcheck` die de echte functie test en `restart: unless-stopped` of `on-failure` met een maximum.
- Bewijs: `docker ps --format '{{.Names}}\t{{.Status}}'` toont `(healthy)` bij elke eigen service; `docker inspect --format '{{.Name}} {{.HostConfig.RestartPolicy.Name}}' $(docker ps -aq)` toont nergens `no`. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V16.5.2 (L2).
- Zie ook: ARCH-67, ARCH-69, INFRA-86, INFRA-87, DB-97, DB-47, AI-83, INFRA-52

### INFRA-36 → GIT-91, GIT-92
Samengevoegd: "Pin images op een versie en vernieuw ze volgens schema" is gedekt door GIT-91, GIT-92. Gebruik die regel.

### INFRA-37 Bouw kleine images zonder bouwgereedschap
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw in meerdere stappen en kopieer alleen het resultaat en de productie-afhankelijkheden naar een minimale basisimage; laat compilers, pakketbeheer-caches, tests en `.git` achter.
- Bewijs: `docker images <image>` (grootte) en `docker run --rm <image> sh -c 'which gcc make git curl wget'` (leeg of mislukt); de Dockerfile heeft een `FROM ... AS build` en een aparte eindstap. Afgevinkt met de uitvoer. Voor de opbouw zelf: zie de skill `docker-expert`.
- Norm: ASVS 5.0.0 V15.2.3 (L2).
- Zie ook: GIT-91, GIT-92, GIT-63, GIT-94, GIT-96, AI-56

### INFRA-38 → GIT-63
Samengevoegd: "Scan draaiende images op bekende lekken" is gedekt door GIT-63. Gebruik die regel.

### INFRA-39 Koppel mappen, geen losse bestanden, en koppel alleen-lezen waar het kan
middel · richtlijn · api | app | mcp · tegenlezer: scherpen (04-10-2026)
- Regel: Koppel configuratie als map en met `:ro`, en koppel nooit een los bestand dat je later met een editor wilt wijzigen.
- Bewijs: `docker inspect --format '{{range .Mounts}}{{.Source}} -> {{.Destination}} rw={{.RW}}{{"\n"}}{{end}}' <container>` toont mappen, en `rw=false` voor configuratie; na een wijziging toont `docker exec <container> cat <pad>` de nieuwe inhoud. Afgevinkt met de uitvoer.
- Norm: geen ASVS-eis; voorwaarde voor betrouwbaar bewijs bij INFRA-42 tot en met INFRA-49.

### INFRA-40 Geef elk Compose-project een eigen naam en gebruik `--remove-orphans` nooit op gedeelde projecten
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in elk Compose-bestand een expliciete projectnaam (`name:`) en draai `docker compose up --remove-orphans` alleen als je zeker weet dat geen ander Compose-bestand dezelfde projectnaam gebruikt.
- Bewijs: `docker compose ls` toont per stack een eigen naam; `grep -rn 'remove-orphans' <deployscripts>` is leeg of elke treffer heeft een notitie. Afgevinkt met de uitvoer.
- Norm: geen; beschikbaarheid.

### INFRA-41 Overweeg gebruikersnaamruimten voor diensten met een hoog risico
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai diensten die niet-vertrouwde invoer zwaar verwerken (browsers voor screenshots, mediaconversie, code van derden) met `userns-remap` of in rootless Docker.
- Bewijs: `docker info --format '{{.SecurityOptions}}'` toont `name=userns` of `name=rootless`, of er is een notitie waarom niet. Afgevinkt met uitvoer of notitie.
- Norm: ASVS 5.0.0 V15.2.5 (L3, extra bescherming rond gevaarlijke functionaliteit).
