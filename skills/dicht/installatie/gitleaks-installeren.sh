#!/usr/bin/env bash
# Zet gitleaks neer als losse binary voor de geheimscan van de skill "dicht" (besluit van Marketing Maatwerk, 04-10-2026; GIT-33, GIT-62).
# Voorbereid in verwerking 5 en daar NIET uitgevoerd. Uitvoeren na akkoord van Marketing Maatwerk (README.md).
#
# Wat het doet: haalt één vaste versie op, vergelijkt het archief met de sha256 die hieronder vastligt, pakt alleen
# de binary uit, zet hem in ~/.claude/skills/dicht/bin/ en legt de sha256 van de binary vast in gitleaks.sha256.
# geheimscan.py draait de binary alleen als die sha256 nog klopt.
#
# De sha256 hieronder is op 04-10-2026 gelezen uit gitleaks_8.30.1_checksums.txt van de uitgave op GitHub en
# nagerekend op het gedownloade archief (zelfde waarde). Een nieuwe versie: pas VERSIE en SHA256 samen aan,
# na het lezen van de uitgave (GIT-72: geen versie jonger dan zeven dagen).
# Terugweg: rm -- "$HOME/.claude/skills/dicht/bin/gitleaks" "$HOME/.claude/skills/dicht/bin/gitleaks.sha256"
set -euo pipefail

VERSIE="8.30.1"
ARCHIEF="gitleaks_${VERSIE}_linux_x64.tar.gz"
SHA256="551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"
DOEL="${DICHT_BIN:-$HOME/.claude/skills/dicht/bin}"

[[ "$(uname -s)-$(uname -m)" == "Linux-x86_64" ]] || { echo "alleen voor Linux x86_64" >&2; exit 1; }
tmp="$(mktemp -d)"
trap 'rm -rf -- "${tmp:?}"' EXIT

curl --fail --silent --show-error --location --proto '=https' --tlsv1.2 --max-time 120 \
  --output "$tmp/$ARCHIEF" "https://github.com/gitleaks/gitleaks/releases/download/v${VERSIE}/${ARCHIEF}"
echo "${SHA256}  ${tmp}/${ARCHIEF}" | sha256sum --check --strict -
tar -xzf "$tmp/$ARCHIEF" -C "$tmp" gitleaks
mkdir -p -- "$DOEL"
install -m 0755 -- "$tmp/gitleaks" "$DOEL/gitleaks"
( cd -- "$DOEL" && sha256sum gitleaks > gitleaks.sha256 )
"$DOEL/gitleaks" version
echo "gitleaks ${VERSIE} staat in ${DOEL}; de geheimscan gebruikt hem vanaf nu."
