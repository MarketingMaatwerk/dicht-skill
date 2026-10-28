#!/usr/bin/env bash
# Sjabloon: bewijs van elke blokkade met een anonieme aanvraag, naast een verzonnen naam in dezelfde map.
# Dekt: WP-64, WP-62, WP-24, WP-41, WP-55, WP-63, WEB-64, INFRA-101, ARCH-85
# Gebruik: controleer-blokkades.sh https://<site>
# Aanpassen: de lijst PADEN (pad en de verzonnen naam ernaast).
# Alleen lezen: het script doet anonieme GET-aanvragen en wijzigt niets (ARCH-85). Het plaatst geen testbestand;
#   "weg" bewijs je op de server (WP-63), want met een blokkade geeft ook een verwijderd bestand 403.
# Uitvoer: per blokkade twee regels (het pad en de verzonnen naam), met datum en servernaam, zoals WP-64 vraagt.
#   Exitcode 1 als een geblokkeerd pad iets anders dan 403 of 404 geeft.
# Lezen van de uitkomst (WP-64): 403 naast 404 betekent dat de regel werkt; 403 naast 403 dat de hele map dicht
#   is; 404 naast 404 zegt niets over de regel (het bestand bestaat niet en er is geen blokkade aangetoond).
set -euo pipefail

SITE="${1:?gebruik: controleer-blokkades.sh https://<site>}"
case "$SITE" in https://*) ;; *) echo "fout: alleen https" >&2; exit 2 ;; esac

# pad|verzonnen naam in dezelfde map
PADEN=(
  "wp-config.php.bak|wp-zzverzonnen.php.txt"
  "wp-content/uploads/zzverzonnen.php|wp-content/uploads/zzverzonnen.txt"
  "xmlrpc.php|zzverzonnen.php"
  "wp-content/ai1wm-backups/zzverzonnen.wpress|wp-content/zzverzonnen/zzverzonnen.txt"
  ".git/config|zzverzonnen/config"
  ".env|zzverzonnen.env.txt"
  "dump.sql|zzverzonnen.txt"
  "wp-content/debug.log|wp-content/zzverzonnen.txt"
)

status() {
  curl --silent --show-error --proto '=https' --connect-timeout 10 --max-time 30 \
       --output /dev/null --write-out '%{http_code} %{size_download}' -- "$1"
}

echo "datum: $(date -u +%FT%TZ)"
echo "server: $(curl --silent --show-error --head --proto '=https' --connect-timeout 10 --max-time 30 -- "$SITE/" | grep -i '^server:' | tr -d '\r' || true)"

fout=0
for regel in "${PADEN[@]}"; do
  pad="${regel%%|*}"
  naast="${regel##*|}"
  a=$(status "$SITE/$pad")
  b=$(status "$SITE/$naast")
  printf '%s  /%s\n%s  /%s (verzonnen)\n\n' "$a" "$pad" "$b" "$naast"
  case "${a%% *}" in 403|404) ;; *) fout=1; echo "FOUT: /$pad geeft ${a%% *}" ;; esac
done
exit "$fout"
