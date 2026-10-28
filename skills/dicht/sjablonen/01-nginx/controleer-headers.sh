#!/usr/bin/env bash
# Sjabloon: meet de verplichte headers op vijf soorten URL's (bewijs voor WEB-23).
# Dekt: WEB-23, WEB-09, WEB-17, WEB-19, WEB-22, WEB-24, INFRA-49
# Gebruik: controleer-headers.sh https://voorbeeld.nl / /assets/app.css /api/health /bestaat-niet /oud-pad
#   Geef minimaal vijf paden: de homepage, een statisch bestand, een API-route, een 404 en een 301.
# Aanpassen: de lijst VERPLICHT als het project meer of andere headers eist.
# Alleen lezen: het script doet GET-aanvragen en wijzigt niets (ARCH-85).
# Uitvoer: een tabel per URL; exitcode 1 als ergens een header ontbreekt of een versie zichtbaar is.
set -euo pipefail

BASIS="${1:?gebruik: controleer-headers.sh https://<host> <pad> <pad> <pad> <pad> <pad>}"
shift
[ "$#" -ge 5 ] || { echo "fout: geef minimaal vijf paden (WEB-23)" >&2; exit 2; }
case "$BASIS" in https://*) ;; *) echo "fout: alleen https" >&2; exit 2 ;; esac

VERPLICHT=(
  strict-transport-security
  x-content-type-options
  referrer-policy
  content-security-policy
)

WERK=$(mktemp -d)
trap 'rm -rf -- "$WERK"' EXIT

fout=0
for pad in "$@"; do
  koppen="$WERK/koppen"
  status=$(curl --silent --show-error --proto '=https' --connect-timeout 10 --max-time 30 \
                --output /dev/null --dump-header "$koppen" --write-out '%{http_code}' -- "$BASIS$pad") \
    || { echo "fout: geen antwoord op $pad" >&2; fout=1; continue; }
  printf '%s %s\n' "$status" "$pad"
  for kop in "${VERPLICHT[@]}"; do
    if grep -qi -- "^$kop:" "$koppen"; then
      printf '  ok        %s\n' "$kop"
    else
      printf '  ONTBREEKT %s\n' "$kop"; fout=1
    fi
  done
  # WEB-24: frame-ancestors in de CSP-header.
  if ! grep -i -- '^content-security-policy:' "$koppen" | grep -qi -- 'frame-ancestors'; then
    printf '  ONTBREEKT frame-ancestors in de CSP\n'; fout=1
  fi
  # WEB-22: geen versie in Server, geen X-Powered-By.
  if grep -qiE -- '^server: .*[0-9]' "$koppen" || grep -qi -- '^x-powered-by:' "$koppen"; then
    printf '  FOUT      versie of X-Powered-By zichtbaar\n'; fout=1
  fi
done
exit "$fout"
