#!/usr/bin/env bash
# Sjabloon: de gate voor shell- en Python-scripts in een repository.
# Dekt: SCR-23, SCR-35, SCR-32 (alleen pip-audit)
# Aanpassen: niets, behalve het pad van requirements.txt. De versies van shellcheck (nu v0.11.0, SCR-23), ruff
#   en pip-audit zet je vast in het project (GIT-62, GIT-68); dit script installeert niets.
# De gate faalt gesloten (GIT-59): ontbreekt een hulpmiddel, dan is de uitkomst een fout, geen overslaan.
# Controleren: de uitvoer is leeg en de exitcode 0; shellcheck --version en ruff --version tonen de vastgezette versie.
set -euo pipefail

for hulpmiddel in shellcheck ruff; do
  command -v "$hulpmiddel" >/dev/null || { echo "fout: $hulpmiddel ontbreekt; de gate faalt gesloten" >&2; exit 1; }
done

# Shell: syntaxcontrole en shellcheck (SCR-23).
git ls-files -z '*.sh' | xargs -0 -r -n1 bash -n
git ls-files -z '*.sh' | xargs -0 -r shellcheck --severity=warning

# Python: beveiligingslint (SCR-35).
git ls-files -z '*.py' | xargs -0 -r ruff check --select S,RUF006

# Afhankelijkheden met hashes: audit (SCR-32). Alleen als het project een requirements.txt heeft.
if [ -f requirements.txt ]; then
  command -v pip-audit >/dev/null || { echo "fout: pip-audit ontbreekt" >&2; exit 1; }
  pip-audit -r requirements.txt
fi

# Elke onderdrukking heeft een reden (SCR-23, SCR-35): toon ze voor de reviewer.
git ls-files -z '*.sh' | xargs -0 -r grep -n 'shellcheck disable' || true
git ls-files -z '*.py' | xargs -0 -r grep -n 'noqa: S' || true
