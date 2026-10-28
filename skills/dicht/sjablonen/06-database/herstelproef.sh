#!/usr/bin/env bash
# Sjabloon: herstelproef van de nieuwste back-up in een lege wegwerpcontainer, met rijtellingen en logboek.
# Dekt: DB-46, DB-50, INFRA-82 (alleen de database, niet de lege machine), SCR-01, SCR-04, SCR-14, SCR-15
# Dekt gedeeltelijk: INFRA-82 vraagt een herstelproef op een lege machine; dit script herstelt op dezelfde host.
# Aanpassen: DB, DOEL, IMAGE (dezelfde major als productie, op digest: GIT-91, DB-48) en KERNTABELLEN.
# Draaien: door een mens, minstens elk kwartaal en na elke wijziging van backup.sh of een major upgrade (DB-46).
#   De privesleutel van age staat niet op deze server (DB-45): geef het pad naar een tijdelijk aangekoppelde
#   sleutel mee in AGE_SLEUTEL en haal hem daarna weer weg.
#   Het script maakt alleen een eigen wegwerpcontainer en raakt productie niet aan (alleen lezen in DOEL).
# Uitvoer: een regel voor docs/herstelproeven.md met datum, bestand, hersteltijd en rijtellingen. Zet de
#   tellingen van productie ernaast en wie het deed (DB-46). Afgevinkt als de laatste regel per database jonger
#   is dan 92 dagen en de tellingen kloppen.
# Niet tegen Docker of een server gedraaid; alleen bash -n en shellcheck 0.11.0 (zonder bevinding).
set -euo pipefail
umask 077
trap 'echo "fout op regel $LINENO: $BASH_COMMAND" >&2' ERR

DB=voorbeeld
DOEL=/var/backups/voorbeeld
IMAGE='postgres:<major.minor>@sha256:<digest>'
KERNTABELLEN=(tenants contacts orders)
AGE_SLEUTEL="${AGE_SLEUTEL:?zet AGE_SLEUTEL op het pad van de privesleutel}"
PROEF="herstelproef-$DB-$$"

NIEUWSTE=$(find "$DOEL" -maxdepth 1 -type f -name "$DB-*.dump.age" -printf '%T@ %p\n' | sort -rn | head -n 1 | cut -d' ' -f2-)
[ -n "$NIEUWSTE" ] || { echo "fout: geen back-up van $DB in $DOEL" >&2; exit 1; }
GLOBALS=$(find "$DOEL" -maxdepth 1 -type f -name 'globals-*.sql.age' -printf '%T@ %p\n' | sort -rn | head -n 1 | cut -d' ' -f2-)
[ -n "$GLOBALS" ] || { echo "fout: geen back-up van de globale objecten in $DOEL" >&2; exit 1; }

WERK=$(mktemp -d)
opruimen() {
  docker rm -f -- "$PROEF" >/dev/null 2>&1 || true   # alleen de eigen wegwerpcontainer, op exacte naam
  rm -rf -- "${WERK:?}"
}
trap opruimen EXIT

head -c 32 /dev/urandom | base64 > "$WERK/pw"
# Geen gepubliceerde poort, geen netwerk: de proef praat alleen via docker exec (INFRA-13).
docker run -d --name "$PROEF" --network none \
  -e POSTGRES_PASSWORD_FILE=/run/pw -v "$WERK/pw:/run/pw:ro" "$IMAGE" >/dev/null

for _ in $(seq 1 30); do
  docker exec "$PROEF" pg_isready -U postgres >/dev/null 2>&1 && break
  sleep 2
done
docker exec "$PROEF" pg_isready -U postgres >/dev/null || { echo "fout: wegwerpserver start niet" >&2; exit 1; }

START=$(date +%s)
# Eerst de rollen, dan de database; stoppen bij de eerste fout (DB-50).
age -d -i "$AGE_SLEUTEL" -- "$GLOBALS" | docker exec -i "$PROEF" psql -X --set ON_ERROR_STOP=on -U postgres -d postgres >/dev/null
docker exec "$PROEF" createdb -U postgres -- "$DB"
age -d -i "$AGE_SLEUTEL" -- "$NIEUWSTE" | docker exec -i "$PROEF" pg_restore -U postgres -d "$DB" --exit-on-error
docker exec "$PROEF" psql -X --set ON_ERROR_STOP=on -U postgres -d "$DB" -c 'ANALYZE' >/dev/null
DUUR=$(( $(date +%s) - START ))

tellingen=""
for tabel in "${KERNTABELLEN[@]}"; do
  [[ "$tabel" =~ ^[a-z_][a-z0-9_]*$ ]] || { echo "fout: ongeldige tabelnaam: $tabel" >&2; exit 2; }
  # De tabelnaam komt uit de vaste lijst hierboven en is op vorm gecontroleerd (SCR-11, DB-27).
  n=$(docker exec "$PROEF" psql -X -At --set ON_ERROR_STOP=on -U postgres -d "$DB" -c "SELECT count(*) FROM \"$tabel\"")
  tellingen+="$tabel=$n "
done

printf '| %s | %s | %s | %ss | %s| <tellingen productie> | <wie> |\n' \
  "$(date -u +%F)" "$DB" "$(basename -- "$NIEUWSTE")" "$DUUR" "$tellingen"
