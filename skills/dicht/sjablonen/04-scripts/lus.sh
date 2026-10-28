#!/usr/bin/env bash
# Sjabloon: Bash-skelet voor een lus die moet blijven lopen (monitor).
# Dekt: SCR-43, SCR-01, SCR-04
# Dekt gedeeltelijk: SCR-42 vraagt dat de lus onder systemd draait (zie 03-systemd/voorbeeld.service met
#   Restart=on-failure, RestartSec, StartLimit en OnFailure); dit bestand is alleen de lus zelf.
# Aanpassen: stap(), en de getallen. 60, 900, 30 en 15 zijn de voorbeeldwaarden uit SCR-43; MAX_FOUTEN noemt de
#   regel niet ("een melding als hetzelfde blijft falen"): zet hem zelf.
# Controleren: laat stap() falen: de pauze verdubbelt tot het maximum en na MAX_FOUTEN stopt de lus met een
#   exitcode ongelijk aan nul, zodat OnFailure meldt. bash -n lus.sh; shellcheck --severity=warning lus.sh.
set -euo pipefail
trap 'echo "fout op regel $LINENO: $BASH_COMMAND" >&2' ERR

MAX_FOUTEN="${MAX_FOUTEN:?zet MAX_FOUTEN (geen standaardwaarde)}"

stap() {
  /bin/true   # vervang door het echte werk
}

pauze=60
fouten=0
while true; do
  # Een time-out per stap (SCR-43). timeout kan geen functie starten: zet hem in stap() om de echte opdracht,
  # bijvoorbeeld: timeout 30 curl ...
  if stap; then
    pauze=60; fouten=0
  else
    fouten=$((fouten + 1))
    pauze=$(( pauze * 2 > 900 ? 900 : pauze * 2 ))
    echo "stap mislukt ($fouten op rij), volgende poging over ${pauze}s" >&2
    if [ "$fouten" -ge "$MAX_FOUTEN" ]; then
      echo "fout: $fouten keer op rij mislukt, lus stopt zodat de procesbeheerder meldt" >&2
      exit 1
    fi
  fi
  sleep $(( pauze + RANDOM % 15 ))   # een pauze in elk pad, met een kleine spreiding
done
