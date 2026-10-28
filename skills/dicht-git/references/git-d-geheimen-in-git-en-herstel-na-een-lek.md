# GIT D: Geheimen in git en herstel na een lek

Compacte regels van `dicht-git`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/git-supplychain.md` (regelnummer in `regel-index.tsv`).

### GIT-32 Geen geheim in code, configuratie, tests of commitberichten
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet nooit een wachtwoord, token, sleutel of verbindingsreeks met wachtwoord in een gevolgd bestand, ook niet in een test, een voorbeeld, een migratie of een commitbericht; lever een `.env.example` met alleen namen en nepwaarden.
- Bewijs: De geheimscan van GIT-33 en GIT-34 is schoon; `git grep -nE "(postgres|mysql)://[^:@/ ]+:[^@ ]+@" -- . ':!*.example'` is leeg; `.env.example` bevat geen waarde die in `.env` staat (`comm -12 <(cut -d= -f2- .env | sort -u) <(cut -d= -f2- .env.example | sort -u)` toont alleen lege of onschuldige waarden, zonder de uitvoer te bewaren). Afgevinkt met de drie. Zie DB-61 voor migratiebestanden en API-65 voor geheimen in code.
- Norm: ASVS 5.0.0 V13.3.1 (L2); OWASP CI/CD CICD-SEC-6; OWASP Top 10 2025 A02 en A04.
- Zie ook: INFRA-72, API-65, GIT-95, DB-62, AI-28, WP-33, INFRA-76, WP-71, DB-61, AI-60, ARCH-49

### GIT-33 Scan op geheimen vóór elke commit, lokaal
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Installeer in elke repo een pre-commit-hook die de gestagede wijziging met gitleaks of betterleaks scant en de commit weigert bij een treffer.
- Bewijs: Een testcommit met een nepsleutel in het formaat van een echte (bijvoorbeeld een regel `aws_secret_access_key = <40 willekeurige tekens>`) wordt geweigerd; daarna is de test weggehaald. Afgevinkt met de uitvoer van de geweigerde commit. Een hook is te omzeilen met `--no-verify` of `SKIP=gitleaks`; daarom is GIT-34 ook verplicht. Let op: gitleaks 8.30.1 krijgt volgens de README alleen nog beveiligingspatches; de opvolger betterleaks (1.9.0, MIT, zelfde auteur) heeft in versie 2 een andere opdrachtregel. Zie open vraag 3.
- Norm: ASVS 5.0.0 V13.3.1 (L2); NIST SSDF PO.3.1; OWASP CI/CD CICD-SEC-6; besluit 15.

### GIT-34 Scan de hele geschiedenis in de gate
hoog · hard · alles · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Draai in de gate (lokaal en in CI) een geheimscan over de volledige geschiedenis en over de werkmap, en laat de gate falen bij een treffer.
- Bewijs: De uitvoer van de scan met exitcode 0 en datum; elke uitzondering staat met reden in `.gitleaksignore`. Afgevinkt met de uitvoer. In CI: haal de volledige geschiedenis op (`fetch-depth: 0`), anders scant de gate één commit. trufflehog controleert een gevonden sleutel bij de leverancier; een ingetrokken sleutel valt dan onder "unverified" en wordt met deze vlaggen niet gemeld. Gebruik altijd `--redact`, anders staat het geheim in het CI-log.
- Norm: ASVS 5.0.0 V13.3.1 (L2); OWASP CI/CD CICD-SEC-6; besluit 11 en 15.
- Zie ook: GIT-57, GIT-58, GIT-59, API-67, API-68, API-78, WP-37, ARCH-40, ARCH-56, GIT-60, GIT-61, AI-85

### GIT-35 Geef eigen sleutels een herkenbaar voorvoegsel en een eigen scanregel
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke sleutel die een eigen product uitgeeft beginnen met een vast voorvoegsel (AUTH-53) en neem voor dat voorvoegsel een regel op in de configuratie van de geheimscan.
- Bewijs: Een testbestand met een nepsleutel met het eigen voorvoegsel laat de scan falen. Afgevinkt met de uitvoer. Een eigen regel staat in `.gitleaks.toml` als een blok `[[rules]]` (README van gitleaks, gelezen 04-10-2026).
- Norm: ASVS 5.0.0 V13.3.1 (L2); zie AUTH-53.
- Zie ook: AUTH-53, AUTH-54, AI-37, AUTH-55, AI-35, WP-81

### GIT-36 Een gelekt geheim is gecompromitteerd: trek het eerst in
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Trek een geheim dat in een commit, log, image, chat of ticket heeft gestaan direct in bij de uitgever en vervang het overal, vóór je iets aan de geschiedenis doet, en doe dat voor alle geheimen tegelijk die via dezelfde weg bereikbaar waren.
- Bewijs: Per geheim een regel: wat, waar het stond, tijdstip van intrekken, bewijs dat de oude waarde niet meer werkt (een aanroep met de oude waarde geeft 401), en waar de nieuwe waarde is gezet. Afgevinkt met die lijst. Zoek alle plekken met `/usr/bin/grep -r` en een patroonbestand (`-f`), zodat het geheim niet in de opdrachtregel staat en `.env`-bestanden niet worden overgeslagen.
- Norm: ASVS 5.0.0 V13.3.4 (L3); OWASP CI/CD CICD-SEC-6; AVG artikel 33 als het geheim toegang tot persoonsgegevens gaf (zie PRIV).
- Zie ook: INFRA-93, WP-79, GIT-54, INFRA-75, WP-38

### GIT-37 Herschrijf de geschiedenis alleen als intrekken niet genoeg is
middel · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Herschrijf de geschiedenis alleen voor iets wat je niet kunt intrekken (klantgegevens, een privésleutel van een certificaat dat nog geldig is, een dump) en doe het dan met `git filter-repo --sensitive-data-removal` (versie 2.47 of hoger) volgens de stappen van GitHub, met akkoord van Marketing Maatwerk.
- Bewijs: Het besluit met reden staat genoteerd; na afloop geeft `git log --all -S'<kenmerk>' --oneline` niets, de ruleset staat weer aan (GIT-24), alle worktrees en clones zijn opnieuw opgezet, en bij een repo op GitHub is het verzoek aan Support verstuurd. Afgevinkt met de vier. Lokaal blijven verwijderde objecten bereikbaar tot de reflog verloopt (standaard 90 dagen, onbereikbare vermeldingen 30) en `git gc` ze opruimt.
- Norm: AVG artikel 5 lid 1 onder e en f voor persoonsgegevens (zie PRIV); NIST SSDF PS.1.1.

### GIT-38 Verwijderd is niet weg: reken met forks, clones en SHA's
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Behandel alles wat ooit naar een gedeelde of publieke repo is gepusht als gelezen, ook als de commit, branch, fork of repo daarna is verwijderd.
- Bewijs: Bij een lek in een repo met forks of collaborators staat in de incidentnotitie dat GIT-36 is uitgevoerd ongeacht het verwijderen. Afgevinkt met die notitie.
- Norm: OWASP CI/CD CICD-SEC-6.

### GIT-39 Houd geheimen uit CI-logs
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewaar geheimen in CI alleen als geheim van de repo of het environment, nooit als platte tekst in een workflow, nooit als JSON- of YAML-blok in één geheim, en registreer elke afgeleide waarde (base64, URL-gecodeerd) met `::add-mask::`.
- Bewijs: `grep -rnE "(password|token|secret|key) *: *['\"]?[A-Za-z0-9/+_-]{16,}" .github/workflows/` is leeg; `zizmor` meldt geen `secrets-outside-env` of `overprovisioned-secrets` (GIT-56). Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V13.3.1 (L2); OWASP CI/CD CICD-SEC-6 en CICD-SEC-10.
- Zie ook: ARCH-62, API-66, DB-88, INFRA-88, AUTH-14, AI-67, AI-52

### GIT-40 → INFRA-75, INFRA-73
Samengevoegd: "Oefen de lekprocedure één keer per jaar" is gedekt door INFRA-75, INFRA-73. Gebruik die regel.
