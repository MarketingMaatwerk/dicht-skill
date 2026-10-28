# GIT F: Gates en hulpmiddelen

Compacte regels van `dicht-git`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/git-supplychain.md` (regelnummer in `regel-index.tsv`).

### GIT-57 De gate bevat lint, typecheck, tests en de scans van dit domein
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per repo één gate vast die in deze volgorde draait: formatteren en lint, typecheck of statische analyse, unit- en integratietests, geheimscan (GIT-34), afhankelijkheden-audit (GIT-61), SAST (GIT-60), en waar van toepassing workflow-lint (GIT-56), Dockerfile- en image-scan (GIT-63, GIT-66).
- Bewijs: Het gate-script of de workflow bevat elke stap, en de laatste uitvoer toont ze allemaal met exitcode 0. Afgevinkt met script en uitvoer. Wat er precies getest wordt en met welke lintregels: ARCH, API-67, API-68 en API-78.
- Norm: NIST SSDF PO.3.1 en PO.3.3; besluit 10 en 11.
- Zie ook: GIT-58, GIT-59, API-67, API-68, API-78, WP-37, ARCH-40, ARCH-56, GIT-60, GIT-61, GIT-34, AI-85, SCR-23, SCR-35, INV-55

### GIT-58 Eén gate-opdracht, lokaal en in CI dezelfde
hoog · hard · alles · eigen bron · tegenlezer: scherpen (04-10-2026)
- Regel: Maak de gate aanroepbaar met één opdracht (`npm run check`, `composer check` of `make check`), draai die in de worktree vóór elke merge naar `main`, en laat een eventuele CI-workflow precies dezelfde opdracht aanroepen.
- Bewijs: De opdracht bestaat en geeft exitcode 0 in de worktree; in de merge-notitie staat de uitvoer met de commit-hash waarop hij draaide (`git rev-parse HEAD` gelijk aan de te mergen commit). Afgevinkt met beide. Een hook is te omzeilen met `--no-verify`; de hook is een geheugensteun, het bewijs is de uitvoer.
- Norm: OWASP CI/CD CICD-SEC-1; NIST SSDF PO.3.3.
- Eigen bron: geen primaire bron; de regel is een eigen werkwijze; NIST SSDF PO.3.3 en de git-documentatie dragen alleen het kader. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Zie ook: GIT-57, GIT-59, API-67, API-68, API-78, WP-37, ARCH-40, ARCH-56, GIT-60, GIT-61, GIT-34, AI-85

### GIT-59 De gate faalt gesloten
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat de gate falen als een hulpmiddel ontbreekt, niet start, een time-out krijgt of niets heeft gescand; gebruik in een gate nooit `|| true`, `continue-on-error`, `--no-fail` of een ontbrekende exitcode-vlag.
- Bewijs: Een proef met een bewust kwetsbaar testgeval per scanner (een oude image, een nepsleutel, een pakket met een bekend lek) maakt de gate rood. Afgevinkt met de rode uitvoer per scanner. Zie WEB-63 voor hetzelfde principe in de applicatie.
- Norm: OWASP CI/CD CICD-SEC-1; OWASP Top 10 2025 A10 Mishandling of Exceptional Conditions.
- Zie ook: GIT-57, GIT-58, API-67, API-68, API-78, WP-37, ARCH-40, ARCH-56, GIT-60, GIT-61, GIT-34, AI-85

### GIT-60 Statische analyse op beveiliging in de gate
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai in de gate Semgrep Community Edition of Opengrep met `--error` over de broncode, en voor PHP daarnaast PHPStan en Psalm met `--taint-analysis`; reken niet op CodeQL voor een privé-repo.
- Bewijs: De uitvoer met exitcode 0, of een lijst bevindingen die elk zijn opgelost of als uitzondering vastgelegd (GIT-65). Afgevinkt met de uitvoer. Beperkingen om te kennen: Semgrep CE analyseert volgens de eigen README alleen binnen één functie of bestand en "will miss many true positives". De regels uit de registry vallen onder de Semgrep Rules License: alleen voor eigen intern gebruik, niet doorleveren of als dienst aanbieden (open vraag 4). Versies: Semgrep 1.179.0 (LGPL-2.1), Opengrep 1.30.0 (LGPL-2.1), PHPStan 2.2.16, Psalm 6.19.1.
- Norm: NIST SSDF RV.1.2; besluit 11; ASVS 5.0.0 V1 (injectie) als doel van de scan.
- Zie ook: GIT-57, GIT-58, GIT-59, API-67, API-68, API-78, WP-37, ARCH-40, ARCH-56, GIT-61, GIT-34, AI-85

### GIT-61 Afhankelijkheden-audit als gate, op het lockfile
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat de gate falen op een bekende kwetsbaarheid van niveau hoog of kritiek in productie-afhankelijkheden, gemeten op het lockfile: `npm audit --omit=dev --audit-level=high`, `composer audit --locked --no-dev`, en `osv-scanner scan source -r .` als tweede bron.
- Bewijs: De uitvoer van de opdrachten met exitcode 0, of per bevinding een uitzondering met einddatum (GIT-65). Afgevinkt met de uitvoer. Draai ook `npm audit signatures` om registry-handtekeningen en attestaties te controleren. Let op: de wachttijd van GIT-72 kan een fix tegenhouden; npm houdt het pakket dan op de kwetsbare versie en eindigt met een fout. Sinds Composer 2.10 is de exitcode van `composer audit` altijd 0 of 1. OSV-Scanner 2.6.0 (Apache-2.0); de exitcode bij bevindingen is niet nagelezen (niet bevestigd, punt 10).
- Norm: ASVS 5.0.0 V15.2.1 (L1); OWASP Top 10 2025 A03; NIST SSDF PW.4.4 (voorbeeld 2) en RV.1.1; besluit 16.
- Zie ook: GIT-77, INFRA-24, ARCH-32, WP-49, GIT-88, DB-92, PRIV-73, MSG-06, SCR-32, GIT-57, GIT-58, GIT-59, API-67, API-68, API-78, WP-37, ARCH-40, ARCH-56, GIT-60, GIT-34, AI-85

### GIT-62 Zet de scanners zelf vast en haal ze niet op met curl naar sh
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Installeer elk hulpmiddel van de gate op een vaste versie met een gecontroleerde checksum, of draai het als image op digest; gebruik nooit `curl … | sh`, `:latest` of een setup-actie op een tag.
- Bewijs: In het gate-script en de workflows staat bij elk hulpmiddel een versie plus digest of checksum; `/usr/bin/grep -rnE "curl[^|]*\| *(ba)?sh|:latest" scripts/ .github/ Makefile` is leeg. Afgevinkt met de grep en het script. De versies staan in de tabel onder GIT-68.
- Norm: OWASP CI/CD CICD-SEC-3 en CICD-SEC-8; NIST SSDF PO.3.2.
- Zie ook: SCR-22

### GIT-63 Scan elke image die je uitrolt
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CIS
- Regel: Scan elke eigen image en elke image van derden in een Compose-bestand vóór uitrol en daarna wekelijks met `trivy image --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed`, en bouw opnieuw zodra er een fix is.
- Bewijs: De scanuitvoer per image met exitcode 0 en datum binnen zeven dagen; uitzonderingen staan in `.trivyignore` met einddatum (GIT-65). Afgevinkt met de uitvoer. Trivy 0.75.0 (Apache-2.0, 01-10-2026); alternatief Grype 0.120.0 met `--fail-on high --only-fixed` (exitcode 2). Docker Scout is gratis voor één repo op het Personal-plan.
    Ook (uit INFRA-38): `trivy image --severity HIGH,CRITICAL --ignore-unfixed <image>` per gebruikte image, met datum; het resultaat is leeg of elke regel heeft een besluit. Afgevinkt met het rapport.
- Norm: CIS Docker Benchmark 4.4 (images scannen en opnieuw bouwen; nummering uit versie 1.6.0) (CIS-nummer niet bevestigd: de benchmark staat achter een registratie en is niet gelezen); OWASP Docker Security Cheat Sheet regel 9; ASVS 5.0.0 V15.2.1 (L1).
- Dekt ook: INFRA-38
- Zie ook: GIT-91, GIT-92, GIT-94, INFRA-37, GIT-96, AI-56

### GIT-64 Draai een passieve ZAP-scan tegen de testomgeving
middel · hard · website | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai vóór de oplevering van een website, API of app de ZAP baseline-scan tegen de eigen testomgeving en los elke FAIL op; draai nooit een actieve scan tegen productie of een klantsite zonder akkoord.
- Bewijs: Het rapport met exitcode 0, of 2 met elke waarschuwing beoordeeld in het regelbestand. Afgevinkt met het rapport. ZAP 2.17.0 (Apache-2.0, 15-12-2025), nu "ZAP by Checkmarx". De tag `stable` is verplaatsbaar: pin op digest (GIT-62).
- Norm: besluit 11 (DAST); OWASP Top 10 2025 A02.

### GIT-65 Leg elke uitzondering vast met reden en einddatum
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Negeer een bevinding alleen via het negeerbestand van het hulpmiddel in de repo (`.trivyignore`, `.gitleaksignore`, een Semgrep-commentaar, een npm-`overrides`-notitie), met een reden, een naam en een einddatum van hooguit 90 dagen.
- Bewijs: Elke regel in een negeerbestand heeft een commentaar met reden en datum; `/usr/bin/grep -c "exp:" .trivyignore` is gelijk aan het aantal CVE-regels. Afgevinkt met de bestanden. Het CVE-nummer in het voorbeeld is verzonnen.
- Norm: ASVS 5.0.0 V15.1.1 (L1, termijnen vastleggen); besluit 2.
- Zie ook: ARCH-30, ARCH-55

### GIT-66 Controleer Dockerfiles en Compose-bestanden statisch
middel · richtlijn · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CIS
- Regel: Draai `docker build --check` met `# check=error=true` in de Dockerfile en hadolint over elke Dockerfile, en `zizmor` over workflows die images bouwen.
- Bewijs: De uitvoer van `docker build --check .` zonder bevindingen en hadolint met `--failure-threshold warning` groen. Afgevinkt met beide. Build checks vragen Buildx 0.15 of hoger hadolint 2.15.1 (GPL-3.0, 31-07-2026).
- Norm: CIS Docker Benchmark sectie 4 (CIS-nummer niet bevestigd: de benchmark staat achter een registratie en is niet gelezen).

### GIT-67 → ARCH-53
Samengevoegd: "Bewaar de uitvoer van de gate als bewijs bij de oplevering" is gedekt door ARCH-53. Gebruik die regel.

### GIT-68 Leg de versies van hulpmiddelen vast en ververs ze per kwartaal
laag · richtlijn · alles · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Houd per project één lijst bij met elk hulpmiddel van de gate, de vastgezette versie en de datum, en loop die lijst elk kwartaal na tegen de releases en de advisories van het hulpmiddel zelf. Neem ook de testhulpmiddelen uit ARCH op (stand 04-10-2026): Playwright 1.63.0, Vitest 5.0.3, StrykerJS 10.0.0, fast-check 4.10.2, dependency-cruiser 18.5.0, Lighthouse CI 0.15.1, `@axe-core/playwright` 4.13.0, Jazzer.js 4.0.0, Infection 0.35.6, Psalm 6.19.1, PHPStan 2.2.16 en `@wordpress/env` 11.16.0; elk is een nieuwe afhankelijkheid en vraagt de onderbouwing van GIT-75.
- Bewijs: De lijst bestaat en de datum van de laatste controle ligt binnen drie maanden. Afgevinkt met de lijst.
- Norm: NIST SSDF PO.3.2; OWASP Top 10 2025 A03 ("Update your CI/CD, IDE, and any other developer tooling regularly"); besluit 18.
