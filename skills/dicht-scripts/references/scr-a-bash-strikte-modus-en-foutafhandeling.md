# SCR A: Bash, strikte modus en foutafhandeling

Compacte regels van `dicht-scripts`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/scripts-automatisering.md` (regelnummer in `regel-index.tsv`).

### SCR-01 Begin elk Bash-script met de strikte modus
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in elk Bash-script als eerste regels `#!/usr/bin/env bash` (of `#!/bin/bash`) en `set -euo pipefail`, en noteer in een commentaarregel waarom als je één van de drie weglaat.
- Bewijs: `for f in $(git ls-files '*.sh'); do sed -n '1,8p' "$f" | /usr/bin/grep -qE '^set -euo pipefail|^set -eu -o pipefail' || echo "ONTBREEKT $f"; done` is leeg, of elk gemeld bestand heeft een commentaarregel met de reden. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V16.5.3 (L2, "fails gracefully and securely ... preventing fail-open conditions"); past ruim.

### SCR-02 Reken niet op `set -e` binnen een voorwaarde, een functie in een voorwaarde of een `&&`-keten
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer de uitkomst van elke stap die niet mag mislukken expliciet (`opdracht || { echo "fout: ..." >&2; exit 1; }`) zodra hij in een `if`, `while`, `&&`, `||` of achter `!` staat, of in een functie die zo wordt aangeroepen.
- Bewijs: Een test per uitrol- of back-upscript waarin één middenstap met opzet faalt (bijvoorbeeld een niet-bestaande map): het script eindigt met een exitcode ongelijk aan nul en de stappen erna zijn aantoonbaar niet uitgevoerd. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V16.5.3 (L2); past ruim.

### SCR-03 Declareer en wijs apart toe, zodat een mislukte opdracht niet wordt gemaskeerd
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf `local x; x=$(opdracht)` en `export X; X=$(opdracht)` op twee regels, en zet `shopt -s inherit_errexit` in scripts die op de uitkomst van een command substitution leunen.
- Bewijs: `shellcheck -i SC2155 $(git ls-files '*.sh')` geeft geen meldingen. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V16.5.3 (L2); past ruim.

### SCR-04 Ruim op met een EXIT-trap en meld de regel bij een fout
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet opruimen (tijdelijke bestanden, sloten, een onderhoudsvlag) in `trap '...' EXIT` direct na het aanmaken, tussen enkele aanhalingstekens, en voeg in scripts die onbeheerd draaien `trap 'echo "fout op regel $LINENO: $BASH_COMMAND" >&2' ERR` toe.
- Bewijs: `for f in $(/usr/bin/grep -lE 'mktemp|\.lock|onderhoud' $(git ls-files '*.sh')); do /usr/bin/grep -q "trap '" "$f" || echo "GEEN TRAP $f"; done` is leeg; `shellcheck -i SC2064` geeft geen meldingen. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V16.3.4 (L2, "logs unexpected errors"); past ruim.
- Zie ook: INV-68, INV-69, SCR-14, SCR-31

### SCR-05 Laat `set -x` uit in alles wat een geheim aanraakt
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in een script dat een geheim leest of doorgeeft geen `set -x` en geen `bash -x` in de cron- of unit-regel; moet je debuggen, zet de trace dan uit rond de regels met het geheim (`{ set +x; } 2>/dev/null`).
- Bewijs: `/usr/bin/grep -nE '^\s*set -[a-z]*x|bash -x' $(git ls-files '*.sh') <(crontab -l)` is leeg, of elke treffer staat in een script dat geen geheim leest. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V16.2.5 (L2).
- Zie ook: INFRA-76, SCR-19, SCR-20, SCR-13, SCR-16, SCR-50, MSG-41, AI-28
