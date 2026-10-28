# GIT E: GitHub Actions

Compacte regels van `dicht-git`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/git-supplychain.md` (regelnummer in `regel-index.tsv`).

### GIT-41 Zet elke actie vast op een volledige commit-SHA
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwijs in `uses:` naar elke actie, ook die van GitHub zelf, met de volledige commit-SHA van 40 tekens en zet de versie als commentaar op dezelfde regel; gebruik nooit een tag of branch.
- Bewijs: `/usr/bin/grep -rnE "uses: +[^#]+@" .github/ | /usr/bin/grep -vE "@[0-9a-f]{40}( |$)|uses: +\./"` is leeg; `zizmor` meldt geen `unpinned-uses` (GIT-56); de repo-instelling van GIT-27 staat aan. Afgevinkt met de drie. Controleer bij het kiezen van een SHA dat hij uit de repo van de actie komt en niet uit een fork (zizmor: `impostor-commit`). De SHA hierboven is op 04-10-2026 opgehaald en als commit-object gecontroleerd; zie de tabel onder GIT-68.
- Norm: OWASP CI/CD CICD-SEC-3 Dependency Chain Abuse en CICD-SEC-8 Ungoverned Usage of 3rd Party Services; OWASP Top 10 2025 A03; NIST SSDF PO.3.2.

### GIT-42 Gebruik zo min mogelijk acties van derden en kijk wat ze zelf aanroepen
hoog · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Vervang een actie van een derde door een `run:`-stap met een gepind hulpmiddel waar dat in een paar regels kan, en lees van elke overgebleven actie de `action.yml` op de gepinde commit: gebruikt hij zelf acties op een tag, dan telt jouw pin niet.
- Bewijs: Per actie van een derde een notitie: waarom nodig, de gelezen `action.yml` op de gepinde commit, en dat `/usr/bin/grep -n "uses:" action.yml` alleen SHA's of niets toont. Afgevinkt met die lijst.
- Norm: OWASP CI/CD CICD-SEC-3 en CICD-SEC-8; NIST SSDF PW.4.1.

### GIT-43 Geef het workflow-token standaard geen rechten
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet bovenaan elke workflow `permissions: {}` of `permissions: contents: read` en geef per job alleen de rechten die die job nodig heeft.
- Bewijs: Elke workflow heeft een `permissions`-sleutel op het hoogste niveau (`/usr/bin/grep -L "^permissions:" .github/workflows/*.yml` is leeg); `zizmor` meldt geen `excessive-permissions`. Afgevinkt met beide. Wie één recht noemt, zet alle niet genoemde rechten op `none`.
- Norm: OWASP CI/CD CICD-SEC-5 Insufficient PBAC; NIST SSDF PS.1.1.

### GIT-44 Zet nooit een expressie met invoer van buiten in een run-stap
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `${{ github.event.* }}`, `${{ github.head_ref }}` en andere waarden die een buitenstaander bepaalt (titel, tekst, branchnaam, commitbericht, auteur) nooit rechtstreeks in `run:`, maar zet ze in `env:` en lees ze als shellvariabele tussen dubbele aanhalingstekens.
- Bewijs: `/usr/bin/grep -rnE "run:.*\$\{\{ *(github\.(event|head_ref)|inputs\.)" .github/` is leeg en `zizmor` meldt geen `template-injection` (die vindt ook meerregelige `run`-blokken, de grep niet). Afgevinkt met beide.
- Norm: OWASP CI/CD CICD-SEC-4 Poisoned Pipeline Execution; OWASP Top 10 2025 A05 Injection.

### GIT-45 Draai nooit code uit een pull request in een workflow met rechten
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `pull_request_target`, `workflow_run` en `issue_comment` niet, tenzij de workflow de code uit de pull request nergens uitcheckt, bouwt of uitvoert; test code van een PR alleen onder `pull_request`.
- Bewijs: `/usr/bin/grep -rnE "pull_request_target|workflow_run|issue_comment" .github/workflows/` is leeg, of per treffer staat vast dat er geen checkout van PR-code volgt; `zizmor` meldt geen `dangerous-triggers`. Afgevinkt met beide. `actions/checkout` weigert sinds v7 (18-06-2026, teruggezet naar v2 tot en met v6 op 20-07-2026) fork-code bij deze triggers, maar `git fetch`, `gh pr checkout` en gedownloade artefacten vallen daar buiten. Sinds 08-12-2025 komt het workflowbestand bij `pull_request_target` altijd van de standaardbranch.
- Norm: OWASP CI/CD CICD-SEC-4; OWASP Top 10 2025 A08.

### GIT-46 Laat het token niet op de runner achter en upload geen verborgen bestanden
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet bij elke `actions/checkout` `persist-credentials: false`, tenzij de job daarna zelf moet pushen, en upload nooit de hele werkmap als artefact.
- Bewijs: `zizmor` meldt geen `artipacked`; `/usr/bin/grep -rn -A3 "actions/checkout@" .github/workflows/` toont bij elke checkout de instelling. Afgevinkt met beide. De standaardwaarde is in v7.0.1 nog steeds `true`; sinds v6 staat het token onder `$RUNNER_TEMP` in plaats van in `.git/config`.
- Norm: OWASP CI/CD CICD-SEC-6.

### GIT-47 Gebruik geen cache in een job die publiceert of uitrolt
middel · hard · alles · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Laat een release- of deploy-job zonder `actions/cache` en zonder de cache-optie van setup-acties bouwen, en sla nooit iets gevoeligs in een cache op.
- Bewijs: De release- en deploy-workflows bevatten geen `actions/cache` en geen `cache:`-optie; `zizmor` meldt geen `cache-poisoning`. Afgevinkt met beide. Sinds 26-06-2026 mogen onvertrouwde triggers de cache van de standaardbranch alleen lezen; een mislukte cache-opslag laat de job dan zonder melding slagen.
- Norm: OWASP CI/CD CICD-SEC-9 Improper Artifact Integrity Validation; OWASP Top 10 2025 A08.

### GIT-48 Geef een geheim alleen aan de stap die het nodig heeft
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet een geheim in `env:` van precies één stap, nooit op workflow- of jobniveau, en gebruik nooit `secrets: inherit` of `toJSON(secrets)`.
- Bewijs: `/usr/bin/grep -rnE "secrets: *inherit|toJSON\(secrets\)" .github/` is leeg; in elke workflow staat `secrets.` alleen onder `env:` of `with:` van een stap (`zizmor`: `secrets-inherit`, `overprovisioned-secrets`). Afgevinkt met beide.
- Norm: ASVS 5.0.0 V13.3.2 (L2); OWASP CI/CD CICD-SEC-6.

### GIT-49 Geef CI geen sleutel tot productie
hoog · richtlijn · api | app | mcp | website | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd de uitrol als bewuste stap op de server zelf (GIT-02): de server haalt code op met een deploy key met leesrecht (GIT-16). Moet CI toch uitrollen, zet het geheim dan in een environment dat alleen vanaf de standaardbranch bereikbaar is, met een sleutel die op de server alleen het uitrolscript mag starten.
- Bewijs: `gh secret list` en `gh secret list --env <naam>` tonen geen sleutel of wachtwoord van een productieserver op repo-niveau; of: het environment heeft een branchbeperking en de sleutel staat in `authorized_keys` met een vaste opdracht. Afgevinkt met de uitvoer. Environments op privé-repo's vragen GitHub Pro; verplichte reviewers en een wachttijd zijn er op Free, Pro en Team alleen voor publieke repo's. De beperking met een vaste opdracht in `authorized_keys` staat in INFRA-07 (`restrict`, `from=` en `command=`, daar bevestigd tegen sshd(8)). Besluit van Marketing Maatwerk (04-10-2026): het plan is en blijft Free, dus op een privé-repo bestaat geen environment en geldt alleen de eerste vorm (uitrol op de server zelf).
- Norm: OWASP CI/CD CICD-SEC-5 en CICD-SEC-6; OWASP Top 10 2025 A03 ("your CI/CD pipeline has weaker security than the systems it builds and deploys").

### GIT-50 Publiceer met kortlevende identiteit in plaats van een token
middel · richtlijn · mcp | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Publiceer een npm-pakket alleen via trusted publishing (OIDC, npm 11.5.1 of hoger) vanuit één vaste workflow, en gebruik voor cloud-diensten OIDC in plaats van een opgeslagen sleutel.
- Bewijs: Het pakket heeft op npmjs.com een trusted publisher en geen publicatietoken in de geheimen; `npm view <pakket> dist.attestations` toont een attestatie (alleen bij een publieke bronrepo). Afgevinkt met beide. Klassieke npm-tokens zijn sinds 09-12-2025 ingetrokken; schrijftokens gelden standaard 7 en hooguit 90 dagen. Voor Marketing Maatwerk nu alleen relevant als hij een pakket gaat publiceren.
- Norm: OWASP CI/CD CICD-SEC-6; SLSA 1.2 Build L2.

### GIT-51 Zet geen self-hosted runner op een server met productie of klantdata
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik de runners van GitHub; registreer nooit een runner op de server waar diensten, databases of klantsites draaien, en gebruik een eigen runner alleen als wegwerpmachine die na één job verdwijnt.
- Bewijs: `gh api repos/<o>/<r>/actions/runners --jq .total_count` geeft 0; op de server draait geen proces `Runner.Listener` (`pgrep -fa Runner.Listener` is leeg). Afgevinkt met beide. Het API-pad `/repos/{owner}/{repo}/actions/runners` met het veld `total_count` staat in de OpenAPI-beschrijving van de REST-API (`github/rest-api-description`, gelezen 04-10-2026).
- Norm: OWASP CI/CD CICD-SEC-7; NIST SSDF PO.5.1.

### GIT-52 Laat Dependabot de gepinde acties bijwerken, met wachttijd
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem in `.github/dependabot.yml` het ecosysteem `github-actions` op met `directory: "/"` en een `cooldown` van minstens 7 dagen, en controleer bekende lekken in acties met zizmor.
- Bewijs: Het bestand bevat het blok; er is een Dependabot-PR voor acties gezien of `zizmor` meldt geen `known-vulnerable-actions` en geen `dependabot-cooldown`. Afgevinkt met bestand en uitvoer. Voor `github-actions`, `docker` en `docker-compose` werkt alleen `default-days`, niet de semver-varianten.
- Norm: ASVS 5.0.0 V15.2.1 (L1); OWASP CI/CD CICD-SEC-3.
- Zie ook: GIT-28, GIT-76

### GIT-53 Maak verplichte checks die niet stil kunnen slagen
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak één job `gate` verplicht die met `if: always()` en `needs:` op alle controlejobs wacht en faalt als er één niet `success` is; gebruik geen `continue-on-error` in een controlejob en geen `paths`-filter op een workflow met een verplichte check.
- Bewijs: Een test-PR waarin één controlejob bewust faalt, kan niet gemerged worden; `/usr/bin/grep -rn "continue-on-error: *true" .github/workflows/` is leeg. Afgevinkt met de geblokkeerde PR en de grep. Het codevoorbeeld is niet uitgevoerd (niet bevestigd, punt 9).
- Norm: OWASP CI/CD CICD-SEC-1; besluit 2 en 10.

### GIT-54 Na een incident met een actie of pakket: alles roteren wat de job kon zien
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Draaide een workflow in het venster van een gekaapte actie of een kwaadaardige pakketversie, behandel dan elk geheim van die repo en elk token op die runner als gelekt (GIT-36), controleer de repo op nieuwe workflows, runners, deploy keys en publieke kopieën, en lees de workflowlogs van die periode.
- Bewijs: De incidentnotitie bevat: het venster uit de advisory naast de eigen runs (`gh run list --created <datum>`), de lijst geroteerde geheimen, en de uitvoer van `git log --since=<datum> -- .github/`, `gh repo list --visibility public` en de deploy keys. Afgevinkt met die notitie.
- Norm: OWASP CI/CD CICD-SEC-10; NIST SSDF RV.1.1; AVG artikel 33 als persoonsgegevens bereikbaar waren (zie PRIV).
- Zie ook: GIT-36, INFRA-93, WP-79, INFRA-75, WP-38

### GIT-55 Laat een bot niet zelf mergen zonder de gate en de wachttijd
middel · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Merge een update-PR van Dependabot of Renovate alleen na een groene gate, en automatisch alleen voor patch-updates van al bestaande afhankelijkheden na de wachttijd van GIT-72; een nieuwe afhankelijkheid, een major en elke wijziging aan `.github/` leest een mens.
- Bewijs: De repo-instelling "Allow GitHub Actions to create and approve pull requests" staat uit (GIT-27); een eventuele automerge-regel noemt alleen `patch` en verwijst naar de verplichte gate. Afgevinkt met de instelling en de regel.
- Norm: OWASP CI/CD CICD-SEC-1; OWASP Top 10 2025 A03.

### GIT-56 Controleer elke workflow met zizmor en actionlint
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai in de gate `zizmor` en `actionlint` over `.github/` en laat de gate falen bij een bevinding.
- Bewijs: De uitvoer van beide hulpmiddelen met exitcode 0 en datum. Afgevinkt met de uitvoer. Versies op 04-10-2026: zizmor 1.30.1 (MIT, 09-09-2026), actionlint 1.7.12 (MIT, 30-03-2026). De precieze opdrachtregels zijn niet vandaag nagelezen (niet bevestigd, punt 10).
- Norm: NIST SSDF PO.3.1 en PW.7 (niet gelezen, zie niet bevestigd punt 11); OWASP CI/CD CICD-SEC-4 en CICD-SEC-7.
