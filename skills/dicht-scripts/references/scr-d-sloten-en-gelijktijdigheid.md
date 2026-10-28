# SCR D: Sloten en gelijktijdigheid

Compacte regels van `dicht-scripts`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/scripts-automatisering.md` (regelnummer in `regel-index.tsv`).

### SCR-18 Neem een slot op een eigen slotbestand buiten `/tmp`, met een eigen exitcode voor "draait al"
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Vergrendel met `flock -n -E 75 <slotbestand>` op een bestand in een map die alleen het eigen account kan schrijven (`$XDG_RUNTIME_DIR`, `/run/lock/<dienst>/` of de statusmap van de dienst), nooit in `/tmp`, en behandel exitcode 75 als "sla over" en niet als fout.
- Bewijs: `/usr/bin/grep -rnE 'flock[^|;]*/tmp/' $(git ls-files '*.sh') <(crontab -l)` is leeg; een proef waarin de taak twee keer tegelijk start laat de tweede eindigen met de melding "draait al" en de eerste ongestoord doorlopen. Afgevinkt met de uitvoer van beide.
- Norm: ASVS 5.0.0 V15.4.1 (L3) en V15.4.3 (L3, "locking logic stays within the code responsible for managing the resource"); past ruim.
- Zie ook: INFRA-69, SCR-38, SCR-39, SCR-37, SCR-36, SCR-41, INFRA-70, BIZ-31
