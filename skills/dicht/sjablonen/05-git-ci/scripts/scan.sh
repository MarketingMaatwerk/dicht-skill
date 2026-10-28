#!/usr/bin/env bash
# Sjabloon: de scans van de gate voor een Node-project.
# Dekt: GIT-34, GIT-56, GIT-59, GIT-60, GIT-61, SCR-01, SCR-23
# Aanpassen: haal zizmor en actionlint weg als de repo geen .github/ heeft; voeg voor een image
#   trivy image --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed "$IMG" toe (GIT-63) en voor PHP
#   composer audit --locked --no-dev en vendor/bin/psalm --taint-analysis (GIT-60, GIT-61).
# De gate faalt gesloten (GIT-59): een ontbrekend hulpmiddel is een fout. Nergens "|| true".
# De opdrachten zijn letterlijk die uit GIT-34, GIT-60 en GIT-61 en uit de voorbeeldpijplijn.
# Controleren: de uitvoer is zonder treffer en de exitcode 0; elke uitzondering staat in het register met een
#   einddatum van hooguit 90 dagen (GIT-65).
set -euo pipefail

for hulpmiddel in gitleaks osv-scanner semgrep; do
  command -v "$hulpmiddel" >/dev/null || { echo "fout: $hulpmiddel ontbreekt; de gate faalt gesloten" >&2; exit 1; }
done

# Geheimscan: hele geschiedenis en werkmap (GIT-34).
gitleaks git --redact --exit-code 1 .
gitleaks dir --redact --exit-code 1 .

# Afhankelijkheden: op het lockfile, productie, niveau hoog of kritiek (GIT-61).
npm audit --omit=dev --audit-level=high
osv-scanner scan source -r .

# SAST (GIT-60).
semgrep scan --config p/default --error --metrics=off .

# Workflow-lint (GIT-56), alleen als er workflows zijn.
if [ -d .github ]; then
  for hulpmiddel in zizmor actionlint; do
    command -v "$hulpmiddel" >/dev/null || { echo "fout: $hulpmiddel ontbreekt; de gate faalt gesloten" >&2; exit 1; }
  done
  zizmor .github/
  actionlint
fi
