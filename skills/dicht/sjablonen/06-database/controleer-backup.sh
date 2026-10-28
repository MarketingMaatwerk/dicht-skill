#!/usr/bin/env bash
# Sjabloon: bewaking van de back-up, los van het back-upscript.
# Dekt: DB-47, INFRA-87 (alleen het back-updeel), ARCH-85
# Aanpassen: DOEL en DATABASES, gelijk aan backup.sh. De grenzen (26 uur, de helft van het vorige bestand) komen
#   letterlijk uit DB-47.
# Draaien: als eigen geplande taak met OnFailure naar het alarmkanaal (03-systemd/); exitcode 1 is alarm.
# Alleen lezen: het script wijzigt niets (ARCH-85).
# Controleren (DB-47): draai het tegen een lege map: het geeft een melding en exitcode 1.
set -euo pipefail

DOEL=/var/backups/voorbeeld
DATABASES=(voorbeeld)
MAX_MINUTEN=$((26 * 60))

fout=0
for db in "${DATABASES[@]}"; do
  mapfile -t bestanden < <(find "$DOEL" -maxdepth 1 -type f -name "$db-*.dump.age" -printf '%T@ %s %p\n' | sort -rn | head -n 2)
  if [ "${#bestanden[@]}" -eq 0 ]; then
    echo "ALARM: geen back-up van $db in $DOEL"; fout=1; continue
  fi
  read -r tijd grootte pad <<< "${bestanden[0]}"
  leeftijd=$(( ($(date +%s) - ${tijd%.*}) / 60 ))
  if [ "$leeftijd" -gt "$MAX_MINUTEN" ]; then
    echo "ALARM: nieuwste back-up van $db is $leeftijd minuten oud: $pad"; fout=1
  fi
  if [ "${#bestanden[@]}" -eq 2 ]; then
    read -r _ vorige _ <<< "${bestanden[1]}"
    if [ "$((grootte * 2))" -lt "$vorige" ]; then
      echo "ALARM: back-up van $db is kleiner dan de helft van de vorige ($grootte tegen $vorige bytes)"; fout=1
    fi
  fi
done
exit "$fout"
