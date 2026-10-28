# SCR B: Bash, quoting en injectie

Compacte regels van `dicht-scripts`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/scripts-automatisering.md` (regelnummer in `regel-index.tsv`).

### SCR-06 Zet elke expansie tussen dubbele aanhalingstekens en bouw argumentlijsten als array
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf `"$var"`, `"$(opdracht)"` en `"${lijst[@]}"`; bouw een opdracht met wisselende argumenten als array (`args=(-a --delete); args+=("$bron")`), nooit als één tekst die je ongequote laat uiteenvallen.
- Bewijs: `shellcheck -i SC2086,SC2046,SC2068 $(git ls-files '*.sh')` geeft geen meldingen. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V1.2.5 (L1); CWE-78.

### SCR-07 Geen `eval` en geen `bash -c` met een waarde van buiten
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `eval`, `bash -c "$tekst"`, `sh -c "... $var ..."` en `source <(opdracht)` nooit met een waarde die uit een argument, een bestand, een database, een API of een model komt; gebruik een array of een `case` met vaste opdrachten.
- Bewijs: `/usr/bin/grep -nE '\beval\b|(ba)?sh -c ["'"'"'][^"'"'"']*\$|source <\(' $(git ls-files '*.sh')` is leeg of elke treffer gebruikt aantoonbaar alleen vaste tekst; `shellcheck -i SC2294` geeft geen meldingen. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V1.3.2 (L1, "avoids the use of eval() or other dynamic code execution features"), V1.2.5 (L1); CWE-78.
- Zie ook: API-53, AI-47, SCR-24, SCR-10

### SCR-08 Zet `--` voor elk argument van buiten en `./` voor elk patroon
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf `opdracht [opties] -- "$waarde"` bij elke waarde die je niet zelf hebt getypt, en `./*.txt` in plaats van `*.txt`; weiger een waarde die met `-` begint waar een naam of id wordt verwacht.
- Bewijs: `shellcheck -i SC2035 $(git ls-files '*.sh')` geeft geen meldingen; een test per script dat een naam van buiten krijgt, met de waarden `-rf`, `--help` en `--output=/tmp/x`: er wordt niets verwijderd en er ontstaat geen bestand. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V1.2.5 (L1); CWE-88.

### SCR-09 Verwerk bestandsnamen met een NUL-scheiding, nooit door `ls` te lezen
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Loop over bestanden met `find ... -print0 | xargs -0 ...`, `find ... -exec ... {} +` of `while IFS= read -r -d '' f; do ...; done < <(find ... -print0)`; lees regels altijd met `read -r`.
- Bewijs: `shellcheck -i SC2012,SC2162,SC2044,SC2045 $(git ls-files '*.sh')` geeft geen meldingen; `/usr/bin/grep -nE '\| *xargs( |$)' $(git ls-files '*.sh') | /usr/bin/grep -v -- '-0'` is leeg. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V5.3.2 (L1); past ruim.

### SCR-10 Behandel de opdracht achter `ssh` als tekst voor een tweede shell
hoog · hard · klantproject | api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef een waarde van buiten nooit los mee achter `ssh host opdracht`; stuur het script via standaardinvoer (`ssh host 'bash -s' -- < script.sh` met de waarden als gequote argumenten via `printf '%q'`), en zet in elk onbeheerd script `-o BatchMode=yes -o ConnectTimeout=10` en nooit `StrictHostKeyChecking=no`.
- Bewijs: `/usr/bin/grep -rnE 'StrictHostKeyChecking[= ](no|off)' . ~/.ssh/config` is leeg; elke `ssh`-aanroep in een onbeheerd script heeft `BatchMode=yes` en `ConnectTimeout` (in de aanroep of in `~/.ssh/config` voor die host); `shellcheck -i SC2029` is nagelopen; een test met een id dat `;` bevat wordt geweigerd. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V1.2.5 (L1), V12.3.1 (L2, noemt SSH letterlijk); CWE-78.
- Zie ook: API-53, AI-47, SCR-24, SCR-07

### SCR-11 Geef waarden aan psql door als variabele, nooit in de tekst van de query
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur SQL vanuit Bash via standaardinvoer of `-f` met `-v naam="$waarde"` en `:'naam'` in de query, en zet `-v ON_ERROR_STOP=1`; plak een shellvariabele nooit in de tekst achter `-c`.
- Bewijs: `/usr/bin/grep -nE 'psql[^|]*-c +"[^"]*\$' $(git ls-files '*.sh')` is leeg, of elke treffer gebruikt aantoonbaar alleen een waarde die het script zelf maakt (een tijdstempel uit `date`, een vast getal) en dat staat in een commentaarregel; elke psql-aanroep die schrijft heeft `ON_ERROR_STOP=1`. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V1.2.4 (L1, "database queries ... use parameterized queries"); CWE-89.
- Zie ook: DB-25, DB-26, DB-27, WP-16, WP-18, WP-19, DB-28, SCR-30, INV-63

### SCR-12 Zet het eindwoord van een here-document tussen aanhalingstekens als de inhoud data is
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf `<<'EOF'` voor elke here-document waarvan de inhoud letterlijk moet aankomen (een prompt, SQL, een configuratiebestand, een script voor een andere host), en gebruik alleen `<<EOF` als je de expansie bewust wilt.
- Bewijs: `/usr/bin/grep -nE '<<-? ?[A-Z_]+$' $(git ls-files '*.sh')` toont alleen here-documents waarin de expansie bedoeld is (per treffer nagelopen); `shellcheck -i SC2087` geeft geen meldingen. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V1.2.5 (L1); past ruim.

### SCR-13 Een env-bestand dat je met `.` inleest is code
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Lees een `.env` alleen met `.` of `source` in als het bestand van hetzelfde account is, modus 600 heeft en niet door een applicatie of een formulier wordt geschreven; gebruik in een unit `EnvironmentFile=` en lees in alle andere gevallen regel voor regel als data.
- Bewijs: Voor elk bestand achter `/usr/bin/grep -rnE '^\s*(\.|source) +\S*\.env' $(git ls-files '*.sh')`: `stat -c '%a %U' <bestand>` toont 600 en het account van het script, en `/usr/bin/grep -rn "<bestandsnaam>" src/` toont geen code die erin schrijft. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.3.2 (L2), V1.3.2 (L1).
- Zie ook: INFRA-76, SCR-19, SCR-20, SCR-05, SCR-16, SCR-50, MSG-41, AI-28
