# GIT A: Werkwijze met git en worktrees

Compacte regels van `dicht-git`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/git-supplychain.md` (regelnummer in `regel-index.tsv`).

### GIT-01 Eén sessie, één worktree, één branch
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak voor elke bouwtaak een eigen worktree op een eigen branch (`git worktree add ~/dev/infra-<project> -b feature/<project> main`) en ontwikkel nooit in de checkout waar de diensten vanaf draaien.
- Bewijs: `git worktree list` toont het pad van de sessie op `feature/<project>`; `git -C <live checkout> branch --show-current` geeft `main`. Afgevinkt met beide uitvoeren. Git helpt mee: `git worktree add` weigert een branch die al in een andere worktree is uitgecheckt.
- Norm: NIST SSDF PO.5.1 (omgevingen scheiden); OWASP CI/CD CICD-SEC-1 Insufficient Flow Control Mechanisms.

### GIT-02 De live checkout staat op main en verandert alleen door een merge
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Voer in de live checkout alleen `git merge --no-ff feature/<project>` uit op `main`, gevolgd door de herstart van de betrokken dienst, en nooit `checkout`, `reset`, `rebase` of losse bewerkingen.
- Bewijs: Vóór de merge is `git -C <live> status --porcelain --untracked-files=no` leeg; na de merge toont `git log -1 --format='%h %p %s'` een commit met twee ouders; de health-check van de dienst is groen. Afgevinkt met de drie uitvoeren. Let op: `--no-ff` gaat niet samen met de GitHub-regel "Require linear history" (GIT-25).
- Norm: NIST SSDF PS.1.1; OWASP CI/CD CICD-SEC-1.
- Zie ook: ARCH-22, ARCH-23, ARCH-24, GIT-03, DB-41, DB-42, INFRA-47

### GIT-03 Valideer voordat je commit, merget of herstart
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai vóór elke commit de gate van het project (GIT-58) en controleer vóór elke herstart dat de code op schijf start: afhankelijkheden geïnstalleerd, imports vindbaar, typecheck of `php -l` groen.
- Bewijs: De uitvoer van de gate met exitcode 0 en datum staat in de sessie; na een herstart geeft een echte route 200. Afgevinkt met beide.
- Norm: NIST SSDF PO.3.1 en PO.3.3 (gereedschap dat bewijs levert).
- Zie ook: ARCH-22, ARCH-23, ARCH-24, GIT-02, DB-41, DB-42, INFRA-47

### GIT-04 Stage alleen expliciete paden en lees wat je commit
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `git add <pad>` per bestand, nooit `git add -A`, `git add .` of `git commit -a`, en lees vóór de commit `git diff --cached --name-only` en bij twijfel de diff zelf.
- Bewijs: De lijst van `git diff --cached --name-only` bevat alleen bestanden van deze taak en geen pad dat matcht op `\.env|\.pem$|\.key$|\.sql|\.bak|dump|backup`. Afgevinkt met de lijst. Een pre-commit-hook met een geheimscan (GIT-33) is het vangnet.
- Norm: ASVS 5.0.0 V13.3.1 (L2); OWASP CI/CD CICD-SEC-6 Insufficient Credential Hygiene.

### GIT-05 Commit na elke gevalideerde stap, één onderwerp per commit
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg elke werkende eenheid direct vast in een eigen commit met een boodschap die zegt wat er verandert en waarom, en laat aan het eind van een sessie niets gevalideerds ongecommit achter.
- Bewijs: `git status --porcelain` in de worktree is leeg bij het afsluiten, of de rest is benoemd als werk van een andere sessie; `git log --oneline main..HEAD` toont per stap één regel. Afgevinkt met beide uitvoeren.
- Norm: NIST SSDF PS.1.1 (voorbeeld 2: wijzigingen herleidbaar per account).

### GIT-06 Installeer afhankelijkheden in de worktree zelf
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai in elke nieuwe worktree een eigen `npm ci --include=dev` (per pakketmap) en maak nooit een symlink naar de `node_modules` van de hoofdcheckout.
- Bewijs: `readlink -f node_modules/@<scope>/<pakket>` geeft een pad binnen de worktree; `npx tsc --version` en de testrunner starten. Afgevinkt met beide uitvoeren.
- Norm: NIST SSDF PO.5.1.

### GIT-07 Draai opdrachten in verschillende worktrees na elkaar
middel · hard · alles · eigen bron · tegenlezer: niet te bevestigen (04-10-2026)
- Regel: Voer opdrachten die in verschillende worktrees schrijven of committen nooit parallel uit, gebruik `git -C <pad>` in plaats van `cd`, en controleer na elke commit met `git log --oneline -1 <branch>` waar hij staat.
- Bewijs: De uitvoer van `git log --oneline -1 <branch>` na de commit toont de eigen boodschap op de bedoelde branch. Afgevinkt met die regel.
- Norm: geen eigen eis; ondersteunt NIST SSDF PS.1.1.
- Eigen bron: geen primaire bron; bron is alleen eigen ervaring (eigen ervaring). Opgenomen op besluit van Marketing Maatwerk (04-10-2026).

### GIT-08 Ruim worktrees en branches op zodra het werk gemerged is
laag · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwijder na de deploy de worktree met `git worktree remove <pad>` en de branch met `git branch -d feature/<project>`, en loop per maand de lijst van worktrees na.
- Bewijs: `git worktree list` bevat alleen lopend werk; `git branch --merged main` toont geen oude feature-branches. Afgevinkt met beide uitvoeren. `git worktree remove` weigert een worktree met ongecommit werk; gebruik `--force` alleen na het lezen van `git status` in die worktree.
- Norm: ASVS 5.0.0 V15.2.3 (L2, geen overbodige code in productie) als afgeleide.

### GIT-09 Elke repo met waarde heeft een kopie buiten de server
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zorg dat elke repo waar een dienst of klant van afhangt een kopie buiten de server heeft: een privé-remote, of een dagelijkse `git bundle create <bestand> --all` die versleuteld in de offsite back-up gaat, en doe per kwartaal een herstelproef. Vaste keuze (besluit van Marketing Maatwerk, 04-10-2026): een repo met geheimen of klantgegevens, ook als die alleen in de geschiedenis staan, krijgt de dagelijkse versleutelde bundle in de offsite back-up en geen remote; elke andere repo krijgt een privé-remote op GitHub.
- Bewijs: `git remote -v` toont een remote waarvan `git ls-remote` de laatste commit van `main` geeft, of er is een bundle van vandaag in de offsite back-up; de laatste herstelproef (clone uit remote of bundle, `git log -1` gelijk aan de bron) heeft een datum binnen drie maanden. Afgevinkt met uitvoer en datum.
- Norm: NIST SSDF PS.3.1 (elke release veilig archiveren); zie INFRA voor 3-2-1 en versleuteling.
- Zie ook: DB-44, DB-45, DB-49, INFRA-79, INFRA-81, INFRA-83, DB-57

### GIT-10 Zet .gitignore neer vóór de eerste commit en weet wat het niet doet
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Begin elke repo met een `.gitignore` die `.env`, `.env.*` (met uitzondering van `.env.example`), sleutels (`*.pem`, `*.key`), dumps (`*.sql`, `*.sql.gz`), back-ups (`*.bak*`, `*.wpress`), `node_modules`, `vendor` en uploads uitsluit, en haal een bestand dat al gevolgd wordt weg met `git rm --cached`.
- Bewijs: `git ls-files | grep -iE '(^|/)\.env($|\.)|\.pem$|\.key$|\.sql(\.gz)?$|\.wpress$|\.bak'` toont hooguit `.env.example`; `git check-ignore -v .env` noemt de regel die hem uitsluit. Afgevinkt met beide uitvoeren. Gebruik `/usr/bin/grep`: de `grep` in de Claude-shell slaat genegeerde bestanden over (eigen ervaring).
- Norm: ASVS 5.0.0 V13.3.1 (L2); OWASP CI/CD CICD-SEC-6.

### GIT-11 Maak geen repo van een map waarin tokens en shellgeschiedenis staan
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Volg in git nooit een thuismap of configuratiemap met tokenbestanden, shellgeschiedenis of een sleutelbestand naast het versleutelde bestand waar het bij hoort; versiebeheer voor configuratie gaat via een aparte repo met een allowlist van bestanden.
- Bewijs: `git -C ~ ls-files | /usr/bin/grep -iE 'bash_history|hosts\.yml|\.keyfile|id_(rsa|ed25519)$|credentials'` is leeg, of de home-repo is vervangen door een repo met een allowlist. Afgevinkt met de uitvoer. Herstel hoort bij de audit en vraagt akkoord: het raakt de geschiedenis (GIT-37).
- Norm: ASVS 5.0.0 V13.3.1 (L2); NIST SSDF PO.5.2 (ontwikkelomgeving beveiligen).

### GIT-12 Houd git zelf bij en clone niets onvertrouwds met submodules
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd git op een versie met de beveiligingsfixes van de distributie, clone een repo van een onbekende partij nooit met `--recurse-submodules`, en zet `safe.directory` nooit op `*`.
- Bewijs: `git --version` plus de pakketversie; op Ubuntu: `zcat /usr/share/doc/git/changelog.Debian.gz | grep -m1 CVE-2025-48384` geeft een treffer; `git config --global --get-all safe.directory` bevat geen `*`. Afgevinkt met de drie uitvoeren. Het kale versienummer 2.34.1 zegt dus niets; upstream is 2.56.0 (28-09-2026).
- Norm: NIST SSDF PO.3.2 en PO.5.2; ASVS 5.0.0 V15.2.1 (L1).

### GIT-13 Laat elke wijziging lezen voordat hij live gaat
middel · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Lees vóór de merge de volledige diff `git diff main...feature/<project>` zelf na, en laat bij een wijziging aan login, betaling, tenant-isolatie, een migratie of een workflow een tweede lezer meekijken (de skill `requesting-code-review` of een tweede model met alleen de diff).
- Bewijs: In de sessie of de PR staat de beoordeling van de diff met de bevindingen en wat ermee gedaan is; bij de genoemde kritieke delen staat de uitvoer van de tweede lezer. Afgevinkt met die notitie.
- Norm: NIST SSDF PS.1.1 (voorbeeld 4); OWASP CI/CD CICD-SEC-1; ASVS-niveau L3 voor de kritieke delen volgens besluit 6.
- Zie ook: ARCH-54
