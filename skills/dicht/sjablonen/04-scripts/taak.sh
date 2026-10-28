#!/usr/bin/env bash
# Sjabloon: Bash-skelet voor een geplande taak (cron of timer).
# Dekt: SCR-01, SCR-02, SCR-03, SCR-04, SCR-05, SCR-06, SCR-08, SCR-14, SCR-16, SCR-17, SCR-18, SCR-19, SCR-20,
#       SCR-21, SCR-37, SCR-40, INFRA-69 (alleen het slot), INFRA-70
# Aanpassen: NAAM, WERKMAP, de staatsmap en de stappen onder "het werk". Laat weg wat de taak niet nodig heeft
#   (het curl-voorbeeld, het atomair schrijven), maar niet de kop tot en met het slot.
# Draaien: uit cron of een timer met een harde time-out eromheen (SCR-38, zie 03-systemd/).
# Exitcodes: 0 gelukt of overgeslagen omdat er al een run loopt; elke andere code is een fout die gemeld wordt.
# Controleren (SCR-23): bash -n taak.sh; shellcheck --severity=warning taak.sh; een tweede start tijdens een
#   run meldt "draait al, overgeslagen".

# Strikte modus (SCR-01). Geen set -x: dit script raakt een geheim aan (SCR-05).
set -euo pipefail
shopt -s inherit_errexit          # SCR-03
umask 077                         # SCR-16: alles wat dit script aanmaakt is alleen voor het eigen account

# De omgeving zet het script zelf; cron heeft geen inlogprofiel (SCR-37).
export PATH=/usr/local/bin:/usr/bin:/bin
NAAM=voorbeeld-taak
WERKMAP=/opt/voorbeeld
STAAT="${XDG_STATE_HOME:-$HOME/.local/state}/$NAAM"
cd "$WERKMAP" || exit 1

# Meld de regel bij een fout (SCR-04).
trap 'echo "fout op regel $LINENO: $BASH_COMMAND" >&2' ERR

# Slot op een eigen bestand buiten /tmp; 75 betekent "draait al" en is geen fout (SCR-18).
install -d -m 700 -- "$STAAT"
exec 9>"$STAAT/taak.lock"
flock -n -E 75 9 || { rc=$?; [ "$rc" -eq 75 ] && { echo "draait al, overgeslagen"; exit 0; }; exit "$rc"; }

# Tijdelijke map met mktemp, opruimen in een EXIT-trap direct na het aanmaken (SCR-04, SCR-14).
WERK=$(mktemp -d)
trap 'rm -rf -- "$WERK"' EXIT

# Een datum waar het script op beslist: tijdzone expliciet (SCR-40).
VANDAAG=$(TZ=Europe/Amsterdam date +%F)

# --- het werk -------------------------------------------------------------------------------------------

# Een stap die niet mag mislukken controleer je expliciet zodra hij in een voorwaarde of keten staat (SCR-02).
haal_op() {
  local doel="$1"
  # Het geheim staat in een bestand met modus 600 en gaat als kopregel-bestand naar curl, nooit als argument
  # (SCR-19) en nooit als export voor het hele script (SCR-20). Onder systemd: $CREDENTIALS_DIRECTORY/<naam>.
  local kop="${CREDENTIALS_DIRECTORY:-$HOME/.config/$NAAM}/auth-header"
  [ -r "$kop" ] || { echo "fout: $kop niet leesbaar" >&2; return 1; }
  # --fail, time-outs, alleen HTTPS, geen -k (SCR-21).
  curl --silent --show-error --fail --proto '=https' \
       --connect-timeout 10 --max-time 30 --retry 2 \
       -H @"$kop" --output "$doel" -- "https://api.example.nl/v1/voorbeeld?datum=$VANDAAG"
}
haal_op "$WERK/uit.json" || { echo "fout: ophalen mislukt, niets gewijzigd" >&2; exit 1; }

# Declareren en toewijzen apart, zodat een mislukte opdracht niet wordt gemaskeerd (SCR-03).
aantal=""
aantal=$(wc -c < "$WERK/uit.json")
[ "$aantal" -gt 0 ] || { echo "fout: leeg antwoord" >&2; exit 1; }

# Argumenten als array, elke expansie tussen aanhalingstekens, -- voor waarden van buiten (SCR-06, SCR-08).
opties=(--archive)
rsync "${opties[@]}" -- "$WERK/uit.json" "$STAAT/laatste.json"

# Een bestand dat een ander proces leest schrijf je atomair: tijdelijk bestand in dezelfde map, dan mv (SCR-17).
# TMP=$(mktemp /srv/site/.voorbeeld.XXXXXX)
# trap 'rm -f -- "$TMP"; rm -rf -- "$WERK"' EXIT
# genereer > "$TMP"; chmod 644 "$TMP"; mv -f -- "$TMP" /srv/site/voorbeeld.json

echo "klaar: $NAAM $VANDAAG ($aantal bytes)"
