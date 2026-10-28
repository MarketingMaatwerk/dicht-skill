#!/usr/bin/env bash
# Installeert de skill dicht (kern, sub-skills, hooks, audit, sjablonen en het commando /dicht-audit) in de
# map van Claude Code. Doel: $DOEL, standaard ~/.claude. Wijzigt geen instellingen en overschrijft niets:
# staat er al een map dicht of dicht-*, of het commando, dan stopt het zonder iets te schrijven.
set -euo pipefail
trap 'echo "fout op regel $LINENO" >&2' ERR

BRON="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DOEL="${DOEL:-$HOME/.claude}"

[[ -f "$BRON/skills/dicht/SKILL.md" ]] || { echo "bron niet gevonden in $BRON" >&2; exit 1; }
command -v python3 >/dev/null || { echo "python3 ontbreekt (nodig voor de hooks en de audit)" >&2; exit 1; }

bestaat=()
for m in "$BRON"/skills/dicht*/; do
  naam="$(basename -- "$m")"
  [[ -e "$DOEL/skills/$naam" ]] && bestaat+=("$DOEL/skills/$naam")
done
[[ -e "$DOEL/commands/dicht-audit.md" ]] && bestaat+=("$DOEL/commands/dicht-audit.md")
if (( ${#bestaat[@]} )); then
  printf 'bestaat al, niets geschreven: %s\n' "${bestaat[@]}" >&2
  exit 1
fi

mkdir -p -- "$DOEL/skills" "$DOEL/commands"
for m in "$BRON"/skills/dicht*/; do
  cp -R -- "${m%/}" "$DOEL/skills/"
done
cp -- "$BRON/commands/dicht-audit.md" "$DOEL/commands/"

# Het voorbeeld van de hookinstellingen krijgt de echte paden van deze installatie.
voorbeeld="$DOEL/skills/dicht/hooks/settings-voorbeeld.json"
inhoud="$(<"$voorbeeld")"
printf '%s\n' "${inhoud//\/home\/gebruiker\/.claude/$DOEL}" > "$voorbeeld"

echo "geinstalleerd in $DOEL/skills: $(find "$DOEL/skills" -maxdepth 1 -name 'dicht*' | wc -l) skills"
echo "controle: python3 $DOEL/skills/dicht/hooks/test_hooks.py && python3 $DOEL/skills/dicht/audit/test_audit.py"
echo "hooks aanzetten: zie README.md, sectie Hooks (voorbeeld in $voorbeeld)"
