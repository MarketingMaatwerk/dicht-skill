# SCR G: Python-scripts

Compacte regels van `dicht-scripts`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/scripts-automatisering.md` (regelnummer in `regel-index.tsv`).

### SCR-24 Start processen vanuit Python met een lijst en zonder shell
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Roep `subprocess.run([...])` aan met een lijst van argumenten en zonder `shell=True`; gebruik nooit `os.system`, `os.popen` of `shell=True` met een waarde van buiten, en zet `"--"` voor argumenten van buiten.
- Bewijs: `/usr/bin/grep -rnE 'shell *= *True|os\.system\(|os\.popen\(|commands\.getoutput' --include='*.py' .` is leeg; `ruff check --select S602,S604,S605` geeft geen meldingen. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V1.2.5 (L1); CWE-78.
- Zie ook: API-53, AI-47, SCR-07, SCR-10

### SCR-25 Geef elke subprocess-aanroep een time-out en controleer de exitcode
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke `subprocess.run`, `check_output` en `check_call` een `timeout=` en `check=True` (of lees `returncode` op de volgende regel), en vang `TimeoutExpired` en `CalledProcessError` op de plek waar je er iets mee doet.
- Bewijs: `ruff check --select PLW1510` (subprocess-run-without-check) geeft geen meldingen; voor de time-out bestaat geen ruff-regel die ik heb kunnen vinden, dus: een script dat met `ast` elke aanroep van `subprocess.run|check_output|check_call` zonder sleutelwoord `timeout` meldt, met lege uitvoer. Plus een test met een opdracht die niet eindigt (`["sleep", "999"]` als vervanger): de aanroep eindigt binnen de ingestelde tijd met `TimeoutExpired`. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V15.2.2 (L2), V16.5.3 (L2).
- Zie ook: API-48, API-49, ARCH-13, ARCH-14, AI-76, DB-65, API-19, SCR-21, SCR-26, SCR-43, MSG-42

### SCR-26 Geef elke HTTP-aanroep in Python een time-out en laat de certificaatcontrole aan
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `timeout=` op elke `requests`-, `httpx`- en `urllib.request.urlopen`-aanroep (voor requests bij voorkeur als paar `(verbinden, lezen)`), gebruik nooit `verify=False` of een eigen `ssl`-context zonder controle, en roep `raise_for_status()` aan of controleer de statuscode.
- Bewijs: `ruff check --select S113,S501` geeft geen meldingen; `/usr/bin/grep -rnE 'urlopen\(' --include='*.py' . | /usr/bin/grep -v timeout` is leeg; `/usr/bin/grep -rnE 'verify *= *False|_create_unverified_context|CERT_NONE' --include='*.py' .` is leeg. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V12.3.2 (L2), V15.2.2 (L2).
- Zie ook: API-48, API-49, ARCH-13, ARCH-14, AI-76, DB-65, API-19, SCR-21, SCR-25, SCR-43, MSG-42

### SCR-27 Laad nooit pickle, shelve of marshal uit een bron die een ander kan schrijven
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `pickle`, `shelve`, `marshal`, `dill` en `joblib.load` alleen voor bestanden die het script zelf schreef in een map met modus 700; gebruik voor alles wat van een netwerk, een wachtrij, een cache, een upload of een gedeelde map komt JSON met een schema.
- Bewijs: `ruff check --select S301,S302,S403` (pickle, marshal en de import van pickle) geeft geen meldingen, en `/usr/bin/grep -rnE '\b(pickle|cPickle|shelve|marshal|dill)\.(load|loads|open)|joblib\.load' --include='*.py' .` is leeg of elke treffer leest een bestand uit een map met modus 700 dat het script zelf schreef. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V1.5.2 (L2, "Deserialization mechanisms that are explicitly defined as insecure must not be used with untrusted input"); CWE-502.
- Zie ook: API-55, WP-26, SCR-28, INV-16, INV-17

### SCR-28 Lees YAML met `yaml.safe_load`
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `yaml.safe_load` en `yaml.safe_load_all` (of `Loader=yaml.SafeLoader`), nooit `yaml.load` met `Loader`, `FullLoader` of `UnsafeLoader`, en nooit `yaml.unsafe_load`.
- Bewijs: `ruff check --select S506` geeft geen meldingen; `/usr/bin/grep -rnE 'yaml\.(load|load_all|unsafe_load|full_load)\(' --include='*.py' . | /usr/bin/grep -v SafeLoader` is leeg; `python3 -c "import yaml; print(yaml.__version__)"` toont 5.4 of hoger. Afgevinkt met de drie uitvoeren. Gemeten op 04-10-2026: PyYAML 6.0.3 lokaal, 0 treffers voor `yaml.load(`.
- Norm: ASVS 5.0.0 V1.5.2 (L2); CWE-502.
- Zie ook: API-55, WP-26, SCR-27, INV-16, INV-17

### SCR-29 Pak een archief alleen uit met een filter en een grens
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Roep `tarfile.extractall` en `extract` altijd aan met `filter="data"`, controleer bij de start `hasattr(tarfile, "data_filter")`, pak een zip uit na een telling van het aantal leden en de som van `file_size` tegen een maximum, en pak altijd uit in een lege, eigen map.
- Bewijs: `ruff check --select S202` geeft geen meldingen; `/usr/bin/grep -rnE '\.extractall\(|\.extract\(' --include='*.py' . | /usr/bin/grep -v 'filter='` toont alleen zip-aanroepen met een voorafgaande grenscontrole; een test met een archief dat `../../x` bevat eindigt met een fout en schrijft niets buiten de doelmap. Afgevinkt met de drie uitvoeren. Getoetst op 04-10-2026: Python 3.10.12 op de eigen server heeft `tarfile.data_filter` (`hasattr` geeft `True`).
- Norm: ASVS 5.0.0 V5.3.3 (L3, zip slip), V5.2.3 (L2, maximale uitgepakte omvang), V5.2.5 (L3, koppelingen).
- Zie ook: INV-41, INV-42, INV-43, INV-45, WEB-49

### SCR-30 Geef waarden aan SQL door als parameter, nooit met een f-string
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf elke query in Python met plaatshouders en een aparte parameterlijst (`cur.execute("... WHERE id = %s", (id,))`); gebruik f-strings, `%`, `+` en `.format` nooit om een waarde in SQL te zetten, en haal een tabel- of kolomnaam uit een vaste lijst.
- Bewijs: `ruff check --select S608` geeft geen meldingen, of elke melding is een query met alleen vaste tekst en een constante uit de code; `/usr/bin/grep -rnE '(execute|sql)\(\s*f["'"'"']' --include='*.py' .` is nagelopen. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V1.2.4 (L1); CWE-89.
- Zie ook: DB-25, DB-26, DB-27, WP-16, WP-18, WP-19, DB-28, SCR-11, INV-63

### SCR-31 Maak tijdelijke bestanden in Python met het tempfile-pakket
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `tempfile.TemporaryDirectory()`, `NamedTemporaryFile()` of `mkstemp()` en nooit `tempfile.mktemp()` of een vast pad onder `/tmp`; schrijf status die een run moet overleven naar een eigen map met modus 700.
- Bewijs: `ruff check --select S306,S108` geeft geen meldingen. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V15.4.2 (L3); CWE-377.
- Zie ook: INV-68, INV-69, SCR-14, SCR-04

### SCR-32 Draai elk Python-script in een eigen virtuele omgeving met vastgezette afhankelijkheden en hashes
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elk Python-project dat afhankelijkheden buiten de standaardbibliotheek gebruikt een eigen `venv`, een vastgezet bestand met `--hash=sha256:` per pakket, installeer met `pip install --require-hashes -r requirements.txt` (of `uv sync --locked`), roep in cron en units de interpreter uit die omgeving aan met een absoluut pad, en draai `pip-audit` als gate.
- Bewijs: In de repository staan een vastgezet bestand met hashes (`/usr/bin/grep -c -- '--hash=sha256:' requirements.txt` is groter dan nul en gelijk aan of groter dan het aantal pakketten) of een `uv.lock`; `crontab -l` en `systemctl cat` tonen een interpreter uit de `.venv`; de uitvoer van `pip-audit` is leeg of elke melding valt binnen de hersteltermijn van GIT-77. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V15.1.2 (L2, inventaris van onderdelen), V15.2.1 (L1, binnen de hersteltermijnen), V15.2.4 (L3). BRIEF besluit 16 en 22.
- Zie ook: GIT-77, INFRA-24, ARCH-32, WP-49, GIT-88, DB-92, GIT-61, PRIV-73, MSG-06, GIT-69, GIT-72

### SCR-33 Draai scripts op een Python-versie die nog beveiligingsupdates krijgt
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor elk nieuw script een Python-versie met de status `bugfix` of `security` (op 04-10-2026: 3.11 tot en met 3.14), leg per bestaand script vast welke interpreter het gebruikt, en plan de overstap vóór de einddatum van die versie.
- Bewijs: `python3 --version` en de interpreter in elke cron- en unit-regel naast de tabel op devguide.python.org/versions: de versie heeft status `bugfix` of `security`, of er ligt een genoteerde uitzondering met de termijn van de distributie en een datum voor de overstap (ARCH-30). Afgevinkt met de uitvoer en de notitie.
- Norm: ASVS 5.0.0 V15.2.1 (L1), V15.1.1 (L1).
- Zie ook: GIT-93, API-72, WP-52, DB-93, INFRA-22, INFRA-42, AI-54

### SCR-34 Houd asyncio-taken vast, blokkeer de lus niet en begrens elk wachten
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewaar elke taak van `asyncio.create_task` in een verzameling (of gebruik `asyncio.TaskGroup`), roep geen blokkerende functie aan in een coroutine (`time.sleep`, `requests`, `subprocess.run`: gebruik `asyncio.sleep`, een asynchrone client of `asyncio.to_thread`), en zet om elke `await` op iets buiten het proces een `asyncio.timeout()`.
- Bewijs: `ruff check --select RUF006` geeft geen meldingen; een run met `PYTHONASYNCIODEBUG=1` (of `asyncio.run(main(), debug=True)`) in de test toont geen waarschuwing over een nooit geawaite coroutine of een trage callback. Afgevinkt met beide uitvoeren. Voor blokkerende HTTP-aanroepen in een coroutine bestaat de ruff-regel ASYNC210 (blocking-http-call-in-async-function); de overige regels van de groep `ASYNC` zijn niet per stuk nagelezen.
- Norm: ASVS 5.0.0 V15.4.1 (L3), V15.2.2 (L2); past ruim. Zie API-70 voor promises in Node.

### SCR-35 Maak een beveiligingslint een gate voor Python-scripts
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai `ruff check --select S,RUF006` (of `bandit -r`) op een vastgezette versie over elk Python-bestand vóór elke commit en in CI, en sta een onderdrukking alleen toe als `# noqa: Sxxx` met de reden erbij.
- Bewijs: De gate-uitvoer is leeg; `ruff --version` toont de vastgezette versie; `/usr/bin/grep -rn 'noqa: S' --include='*.py' .` toont bij elke treffer een reden. Afgevinkt met de drie uitvoeren.
- Norm: BRIEF besluit 10 (lint als gate) en besluit 11 (SAST); ASVS 5.0.0 V15.2.5 (L3), past ruim.
- Zie ook: GIT-57, SCR-23, INV-55

### SCR-36 Start een Python-script uit cron in geïsoleerde modus
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Roep een Python-script in cron en in een unit aan met `python -I script.py` (of op 3.11 en hoger minimaal `-P`), tenzij het script bewust modules uit zijn eigen map laadt; zorg dan dat die map alleen voor het eigen account schrijfbaar is.
- Bewijs: `crontab -l | /usr/bin/grep -nE 'python3? ' | /usr/bin/grep -v -- ' -I'` is leeg of elke treffer is verklaard; `stat -c '%a %U %G %n'` van de scriptmap toont geen schrijfrecht voor groep of anderen (INFRA-70). Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.2.2 (L2); CWE-426.
- Zie ook: INFRA-69, SCR-18, SCR-38, SCR-39, SCR-37, SCR-41, INFRA-70, BIZ-31
