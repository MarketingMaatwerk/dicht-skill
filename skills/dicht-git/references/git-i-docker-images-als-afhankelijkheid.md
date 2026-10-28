# GIT I: Docker-images als afhankelijkheid

Compacte regels van `dicht-git`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/git-supplychain.md` (regelnummer in `regel-index.tsv`).

### GIT-91 Zet elke image vast op tag plus digest
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CIS
- Regel: Schrijf in elke `FROM` en elke `image:` in een Compose-bestand de versie-tag gevolgd door `@sha256:<digest>`; gebruik nooit `latest` en nooit een tag alleen. Aanvulling uit INFRA-36: Pin op een versie die nog onderhouden wordt.
- Bewijs: `/usr/bin/grep -rnE "^FROM |^\s*image:" Dockerfile* docker-compose*.yml compose*.yml | /usr/bin/grep -v "@sha256:"` toont alleen bouwfasen (`FROM <fase>`) en eigen images. Afgevinkt met de uitvoer. Gebruik de digest van de index (alle platformen), niet die van één platform. Zie DB-98 voor de Postgres-image.
    Ook (uit INFRA-36): `docker ps --format '{{.Image}}' | grep -E ':latest$|^[^:]+$'` is leeg; `docker images --format '{{.Repository}}:{{.Tag}} {{.CreatedSince}}'` toont geen gebruikte image ouder dan de afgesproken termijn; per image staat in de lijst van INFRA-24 welke tak hij volgt. Het vastzetten op een digest hoort in GIT. Afgevinkt met de uitvoer.
- Norm: CIS Docker Benchmark 4.2 (alleen vertrouwde basisimages; nummering uit 1.6.0) (CIS-nummer niet bevestigd: de benchmark staat achter een registratie en is niet gelezen); OWASP Top 10 2025 A08; OWASP CI/CD CICD-SEC-9.
- Dekt ook: INFRA-36
- Zie ook: GIT-92, GIT-63, GIT-94, INFRA-37, GIT-96, AI-56

### GIT-92 Laat een bot de digests bijwerken en bouw wekelijks opnieuw
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CIS
- Regel: Neem `docker` en `docker-compose` op in `dependabot.yml` (of Renovate met `docker:pinDigests`), en bouw en scan elke eigen image minstens wekelijks opnieuw, ook zonder codewijziging.
- Bewijs: `dependabot.yml` bevat beide ecosystemen; `docker image inspect <image> --format '{{.Created}}'` is niet ouder dan zeven dagen voor draaiende eigen images, of de scan van GIT-63 is groen. Afgevinkt met beide. Dependabot geeft voor Docker alleen versie-updates, geen beveiligingsupdates. Renovate-valkuil: digest-updates van GHCR, Quay en ECR blijven met de standaardinstelling van `minimumReleaseAge` oneindig hangen, omdat die registries geen tijdstempel geven.
- Norm: CIS Docker Benchmark 4.4 (CIS-nummer niet bevestigd: de benchmark staat achter een registratie en is niet gelezen); ASVS 5.0.0 V15.2.1 (L1).
- Zie ook: GIT-91, GIT-63, GIT-94, INFRA-37, GIT-96, AI-56

### GIT-93 Gebruik alleen runtimes die nog beveiligingsfixes krijgen
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw op een Node-versie in actieve of onderhouds-LTS en een PHP-versie die nog beveiligingsfixes krijgt, en plan de overstap minstens drie maanden vóór de einddatum.
- Bewijs: `node --version` en `php -v` in de draaiende container of op de server tonen een versie uit de tabel die niet binnen drie maanden afloopt; anders staat de overstap gepland met datum. Afgevinkt met de uitvoer. PHP 8.2 op klantsites loopt eind 2026 af: zie WP en INFRA.
    Ook (uit API-80): `php -v` per site. Sites op 8.2 staan dus voor het einde van 2026 op de lijst om te verhuizen.
- Norm: ASVS 5.0.0 V15.2.1 (L1); OWASP Top 10 2025 A03 (niet-onderhouden componenten).
- Dekt ook: API-80
- Zie ook: API-72, WP-52, DB-93, INFRA-22, INFRA-42, AI-54, SCR-33

### GIT-94 Kies een basisimage van een bekende uitgever en zo klein als werkt
middel · richtlijn · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CIS
- Regel: Gebruik als basis een Docker Official Image, een Docker Hardened Image of distroless, in de kleinste variant waarmee de applicatie werkt, en gebruik geen image van een onbekend Docker Hub-account zonder de onderbouwing van GIT-75.
- Bewijs: Per image in Dockerfiles en Compose-bestanden staat de uitgever vast (`docker.io/library/...` voor Official Images, `dhi.io` of het eigen register voor Hardened Images, `gcr.io/distroless/...`), of er is een onderbouwing. Afgevinkt met de lijst. Docker Hardened Images zijn sinds 17-12-2025 gratis onder Apache 2.0; SLA-patches en FIPS-varianten zijn betaald. Alpine gebruikt musl in plaats van glibc; niet elke native module werkt daar. De registernaam van Hardened Images is niet nagelezen (niet bevestigd, punt 10).
- Norm: CIS Docker Benchmark 4.2 en 4.3 (CIS-nummer niet bevestigd: de benchmark staat achter een registratie en is niet gelezen); NIST SSDF PW.4.1.
- Zie ook: GIT-91, GIT-92, GIT-63, INFRA-37, GIT-96, AI-56

### GIT-95 Geen geheim in een image, een laag of de bouwcontext
kritiek · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CIS
- Regel: Geef een geheim tijdens de build alleen mee met `RUN --mount=type=secret`, nooit via `ARG`, `ENV` of `COPY`, en zet `.env`, `.git`, sleutels en dumps in `.dockerignore`. Aanvulling uit INFRA-34: Geef geheimen tijdens het draaien bij voorkeur als bestand (Compose `secrets`) in plaats van als omgevingsvariabele, zodat ze niet in `docker inspect` staan.
- Bewijs: `docker history --no-trunc <image> | /usr/bin/grep -iE "token|secret|password|key="` is leeg; `trivy image --scanners secret <image>` is schoon; `.dockerignore` bevat `.env*` en `.git`; `docker build --check` meldt geen `SecretsUsedInArgOrEnv`. Afgevinkt met de vier. Let op: `--provenance=mode=max` legt de waarden van build-argumenten vast in de attestatie. De vlag `--scanners secret` bij `trivy image` is niet letterlijk nagelezen (niet bevestigd, punt 10).
    Ook (uit INFRA-34): `docker history --no-trunc <image> | grep -iE 'token|secret|password|key='` is leeg; `grep -nE '^\s*(ARG|ENV)\s+\S*(TOKEN|SECRET|PASSWORD|KEY)' Dockerfile` is leeg; een `.dockerignore` sluit `.env`, `.git` en sleutelbestanden uit. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V13.3.1 (L2: niet in build-artefacten); CIS Docker Benchmark 4.10 (CIS-nummer niet bevestigd: de benchmark staat achter een registratie en is niet gelezen); OWASP Docker Security Cheat Sheet regel 12.
- Dekt ook: INFRA-34
- Zie ook: INFRA-72, API-65, GIT-32, DB-62, AI-28, WP-33, INFRA-76, WP-71, DB-61, AI-60, ARCH-49

### GIT-96 Haal in een Dockerfile niets op zonder controlesom
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CIS
- Regel: Gebruik in een Dockerfile geen `curl … | sh` en geen `ADD <url>` zonder `--checksum=sha256:…`; installeer pakketten via de pakketbeheerder van de image of kopieer een binary uit een image op digest.
- Bewijs: `/usr/bin/grep -nE "curl[^|]*\| *(ba)?sh|wget[^|]*\| *(ba)?sh|^ADD +https?://" Dockerfile*` is leeg of elke `ADD` heeft `--checksum`. Afgevinkt met de uitvoer. `ADD --checksum` vraagt Dockerfile-syntaxis 1.6 of hoger. De build checks van Docker kennen hier geen regel voor.
- Norm: CIS Docker Benchmark 4.9 en 4.11 (CIS-nummer niet bevestigd: de benchmark staat achter een registratie en is niet gelezen); OWASP Top 10 2025 A08.
- Zie ook: GIT-91, GIT-92, GIT-63, GIT-94, INFRA-37, AI-56

### GIT-97 Weet welke image draait
middel · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Rol een eigen image uit onder een tag met de commit-hash, en leg bij elke deploy de digest van elke draaiende image vast.
- Bewijs: `docker compose images` en `docker inspect --format '{{.Image}} {{.Config.Image}}' <container>` staan met datum in de deploy-notitie en de tag bevat een commit-hash die in `git log` voorkomt. Afgevinkt met de notitie.
- Norm: NIST SSDF PS.3.1 en PS.3.2; OWASP CI/CD CICD-SEC-10.

### GIT-98 Bouw met herkomstgegevens en een SBOM waar de image naar een register gaat
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw een image die je naar een register pusht met `--provenance=mode=max --sbom=true`, nadat GIT-95 is afgevinkt.
- Bewijs: `docker buildx imagetools inspect <image> --format '{{ json .SBOM }}'` en `'{{ json .Provenance }}'` geven inhoud. Afgevinkt met de uitvoer. Attestaties hangen aan een image-index en vragen de containerd image store of een `docker-container`-builder; voor een image die alleen lokaal op de server wordt gebouwd en gedraaid, volstaat GIT-101.
- Norm: SLSA 1.2 Build L1 (herkomst bestaat); ASVS 5.0.0 V15.1.2 (L2).
- Zie ook: GIT-101, PRIV-75

### GIT-99 Reken niet op Docker Content Trust
laag · richtlijn · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CIS
- Regel: Zet `DOCKER_CONTENT_TRUST=1` niet aan en bouw er niets op; controleer de handtekening van een image van een derde met cosign waar de uitgever die publiceert, en vertrouw voor de rest op de digest (GIT-91).
- Bewijs: `echo "${DOCKER_CONTENT_TRUST:-leeg}"` geeft `leeg` of `0` op bouw- en draaimachines; voor een image met gepubliceerde handtekening staat de uitvoer van `cosign verify --certificate-identity-regexp … --certificate-oidc-issuer … <image>` in de notitie. Afgevinkt met beide waar van toepassing.
- Norm: CIS Docker Benchmark 4.5 (bewust afgeweken, met reden) en 4.12 (CIS-nummer niet bevestigd: de benchmark staat achter een registratie en is niet gelezen); OWASP Top 10 2025 A08.

### GIT-100 Houd het register en de toegang ertoe klein
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet eigen images in een privé-register (GHCR), geef de server een token dat alleen `read:packages` heeft, en log in op Docker Hub met een eigen account in plaats van anoniem te pullen.
- Bewijs: `gh api user/packages?package_type=container --jq '.[]|{name,visibility}'` toont `private` voor eigen images; het token op de server heeft alleen leesrecht. Afgevinkt met de uitvoer. Het API-pad en de scopenaam zijn niet vandaag nagelezen (niet bevestigd, punt 6). Docker Hub: 100 pulls per 6 uur per adres zonder inloggen, 200 met een gratis account.
- Norm: ASVS 5.0.0 V13.3.2 (L2); OWASP CI/CD CICD-SEC-2.
