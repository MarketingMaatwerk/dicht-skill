# GIT C: Repository-instellingen en branch-bescherming

Compacte regels van `dicht-git`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/git-supplychain.md` (regelnummer in `regel-index.tsv`).

### GIT-23 Stel vast wat het GitHub-plan toelaat voordat je erop rekent
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per repo op GitHub vast welke beschermingen het plan biedt, en vervang wat ontbreekt door een lokale controle uit dit document in plaats van aan te nemen dat GitHub het doet.
- Bewijs: Het plan staat genoteerd (Settings, Billing and licensing) en per repo is de tabel ingevuld met wat aan staat of welk alternatief draait. Afgevinkt met die tabel. Vastgelegd (besluit van Marketing Maatwerk, 04-10-2026, OPEN-VRAGEN A14): het plan van `MarketingMaatwerk` is Free en blijft Free. Voor elke privé-repo geldt dus de kolom Free: geen rulesets, geen beschermde branches, geen CODEOWNERS en geen environments, en het alternatief uit de laatste kolom draait. Het plan is door Marketing Maatwerk genoemd en niet met het token uitgelezen. Wat lokaal niet af te dwingen is (GIT-24), staat als beperking in het uitzonderingenregister (ARCH-30).
- Norm: OWASP CI/CD CICD-SEC-7 Insecure System Configuration; NIST SSDF PO.3.1.

### GIT-24 Bescherm de standaardbranch: met een ruleset waar het plan die biedt, anders lokaal
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke repo op GitHub waar het plan het toelaat (een publieke repo, of een betaald plan) een actieve ruleset op de standaardbranch met: force-push geblokkeerd, verwijderen geblokkeerd, ondertekende commits verplicht, een pull request verplicht, de gate-checks verplicht, en een lege bypass-lijst. Op een privé-repo op het Free-plan bestaat geen ruleset en geen beschermde branch (GIT-23; besluit van Marketing Maatwerk, 04-10-2026: het plan is en blijft Free); dwing daar lokaal af, in elke clone waaruit gepusht wordt: een `pre-push`-hook die een push naar de standaardbranch afbreekt als hij niet fast-forward is, de branch verwijdert of een commit zonder geldige handtekening bevat, en die de gate draait (GIT-58); ondertekende commits en tags (GIT-18); en een merge naar de standaardbranch met `git merge --verify-signatures`. CI mag dezelfde gate draaien, maar is daar een signaal en geen slot: zonder branch-bescherming houdt een rode run geen push of merge tegen.
- Bewijs: Met een ruleset: `gh api repos/<o>/<r>/rulesets --jq '.[]|{name,enforcement,target}'` toont een ruleset met `enforcement: active`; `gh api repos/<o>/<r>/rulesets/<id>` toont de regels `non_fast_forward`, `deletion`, `required_signatures`, `pull_request` en `required_status_checks` en een lege `bypass_actors`. Afgevinkt met de uitvoer. De veldnamen in dit bewijs staan in de OpenAPI-beschrijving van de REST-API (`github/rest-api-description`, gelezen 04-10-2026). Zonder ruleset (privé-repo op Free): (1) `ls -l "$(git rev-parse --git-common-dir)/hooks/pre-push"` toont een uitvoerbare hook (worktrees delen de hooks van de gezamenlijke git-map), of `git config core.hooksPath` wijst naar de map waar hij staat; (2) in een proefclone met een lokale kale remote breekt de hook drie pushes naar de standaardbranch af: een push die niet fast-forward is, het verwijderen van de branch en een push met een commit zonder handtekening; (3) `git config commit.gpgsign` en `git config merge.verifySignatures` geven `true`; (4) de beperking staat in het uitzonderingenregister (ARCH-30) met een herzieningsdatum. Afgevinkt met de vier. Niet bevestigd: dat deze lokale afdwinging een ruleset vervangt staat in geen primaire bron; de bronnen dragen alleen de mechanismen (de hook kan een push afbreken, `--no-verify` slaat hem over, `--verify-signatures` kijkt alleen naar de laatste commit van de branch die je merget). De hook zoals hier beschreven is niet gebouwd en niet getest; het sjabloon met lefthook draait in `pre-push` alleen de gate.
- Norm: NIST SSDF PS.1.1; OWASP CI/CD CICD-SEC-1 en CICD-SEC-5; besluit 15, voor privé-repo's beperkt door het besluit van 04-10-2026 (OPEN-VRAGEN A14).

### GIT-25 Kies één mergestrategie en zet de regels die ermee botsen niet aan
laag · richtlijn · alles · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Gebruik overal een merge-commit (`--no-ff`, GIT-02) en zet "Require linear history" dus niet aan. Niet bevestigd, dus alleen als voorzorg: onderteken alle commits op de feature-branch als "Require signed commits" aan staat.
- Bewijs: De ruleset bevat geen `required_linear_history`; een test-PR met een merge-commit gaat door. Afgevinkt met de ruleset-uitvoer.
- Norm: geen eigen eis.

### GIT-26 Bescherm tags en maak releases onveranderlijk
middel · hard · wp-plugin | wp-thema | mcp | api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke repo waaruit je iets levert (plugin, thema, image, pakket) een tag-ruleset op `v*` die bijwerken en verwijderen blokkeert, en zet "Enable release immutability" aan. Op een privé-repo op het Free-plan bestaat geen tag-ruleset (GIT-23; besluit van Marketing Maatwerk, 04-10-2026: het plan is en blijft Free): leg dat daar vast als beperking in het uitzonderingenregister (ARCH-30); wat overblijft is de ondertekende tag van GIT-102.
- Bewijs: De ruleset-uitvoer toont een ruleset met `target: tag`; `git push --force origin v<bestaand>` wordt geweigerd; `gh release verify <tag>` slaagt op de laatste release. Afgevinkt met de drie uitvoeren. Klassieke tag protection rules bestaan sinds 30-08-2024 niet meer. Of onveranderlijke releases op een privé-repo van een persoonlijk account werken, is niet bevestigd (punt 4).
- Norm: NIST SSDF PS.2.1 en PS.3.1; OWASP CI/CD CICD-SEC-9 Improper Artifact Integrity Validation; OWASP Top 10 2025 A08.

### GIT-27 Zet de Actions-instellingen van de repo dicht
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet per repo onder Settings, Actions: workflow-rechten op alleen lezen, "Allow GitHub Actions to create and approve pull requests" uit, toegestane acties beperkt tot een lijst, en "Require actions to be pinned to a full-length commit SHA" aan; schakel Actions helemaal uit op een repo zonder workflows.
- Bewijs: `gh api repos/<o>/<r>/actions/permissions` en `gh api repos/<o>/<r>/actions/permissions/workflow` tonen `default_workflow_permissions: read` en `can_approve_pull_request_reviews: false`; een testworkflow met `uses: actions/checkout@v7` faalt op de pin-eis. Afgevinkt met de uitvoer. De API-paden en veldnamen (ook `sha_pinning_required`) staan in de OpenAPI-beschrijving van de REST-API (`github/rest-api-description`, gelezen 04-10-2026). Of de pin-eis op elk plan werkt, staat nergens in de documentatie (punt 5).
- Norm: OWASP CI/CD CICD-SEC-5 Insufficient PBAC en CICD-SEC-7; NIST SSDF PO.3.2.

### GIT-28 Zet Dependabot-meldingen en beveiligingsupdates aan op elke repo
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke repo op GitHub, ook privé, de dependency graph, Dependabot alerts en Dependabot security updates aan, en archiveer een repo niet zolang de code ergens draait.
- Bewijs: `gh api repos/<o>/<r>/vulnerability-alerts -i` geeft 204; `gh api repos/<o>/<r>/automated-security-fixes` toont `enabled: true`. Afgevinkt met de uitvoer. De API-paden staan in de OpenAPI-beschrijving van de REST-API (`github/rest-api-description`, gelezen 04-10-2026; `GET .../vulnerability-alerts` antwoordt met 204 of 404). Docker en docker-compose krijgen van Dependabot geen beveiligingsupdates, alleen versie-updates: de image-scan van GIT-63 vult dat gat.
- Norm: ASVS 5.0.0 V15.2.1 (L1); OWASP Top 10 2025 A03; NIST SSDF RV.1.1.
- Zie ook: GIT-52, GIT-76

### GIT-29 Wijs een eigenaar aan voor workflows en CODEOWNERS zelf
laag · richtlijn · klantproject | alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet, zodra er meer dan één persoon schrijfrecht heeft en het plan code owners biedt (een publieke repo, of een betaald plan), een `.github/CODEOWNERS` neer met jou als eigenaar van `/.github/` en van `CODEOWNERS` zelf, en zet "Require review from Code Owners" aan. Op een privé-repo op het Free-plan bestaan code owners en die regel niet (GIT-23; besluit van Marketing Maatwerk, 04-10-2026: het plan is en blijft Free): geef daar niemand schrijfrecht als collaborator (GIT-20) en lees elke wijziging aan `.github/` zelf na vóór de merge (GIT-13).
- Bewijs: Het bestand bestaat met de twee regels; de ruleset toont de code-owner-eis; een test-PR van een tweede account op `.github/workflows/` kan niet zonder jouw goedkeuring gemerged worden. Afgevinkt met de drie. Op een privé-repo op Free: het bewijs van GIT-20 (geen collaborator met schrijfrecht) en de notitie van GIT-13 bij elke wijziging aan `.github/`. Voor een solist heeft de regel geen effect: de enige eigenaar is de auteur. Daarom richtlijn.
- Norm: NIST SSDF PS.1.1 (voorbeeld 4); OWASP CI/CD CICD-SEC-1.

### GIT-30 → PRIV-72
Samengevoegd: "Geef een meldpunt voor kwetsbaarheden bij alles wat je aan anderen levert" is gedekt door PRIV-72. Gebruik die regel.

### GIT-31 → WEB-64
Samengevoegd: "Lever nooit een .git-map mee naar productie" is gedekt door WEB-64. Gebruik die regel.
