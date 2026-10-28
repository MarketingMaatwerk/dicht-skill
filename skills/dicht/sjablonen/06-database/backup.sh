#!/usr/bin/env bash
# Sjabloon: dagelijkse, versleutelde back-up van een PostgreSQL in Docker, met de globale objecten.
# Dekt: DB-44, DB-45, DB-47 (alleen het stoppen bij een fout), DB-48, DB-50, DB-57, SCR-01, SCR-04, SCR-16, SCR-18
# Dekt gedeeltelijk:
#   - DB-47 vraagt ook een bewaking los van dit script (een bestand jonger dan 26 uur, niet kleiner dan de helft
#     van het vorige): zie controleer-backup.sh.
#   - DB-49 en INFRA-79 (een versleutelde kopie buiten de server) doet dit script niet: de spiegeling naar
#     offsite is een eigen stap.
#   - DB-57: BEWAAR_DAGEN heeft geen standaardwaarde, omdat de termijn per soort project verschilt; de gekozen
#     termijn staat ook in het register (policy-state.yaml).
# Bewaartermijn (besluit van Marketing Maatwerk, 05-10-2026): 14 dagen voor een website, 30 dagen voor een webshop en voor een
#   eigen systeem (CRM, registrar). Voorbeeld: BEWAAR_DAGEN=14 voor een website, BEWAAR_DAGEN=30 voor een webshop.
# Aanpassen: CONTAINER, BEHEERROL, de lijst DATABASES en DOEL.
# Versleuteling (DB-45): age met een publieke sleutel in AGE_ONTVANGER; de dump gaat via een pipe en staat nooit
#   leesbaar op schijf. De privesleutel staat niet op deze server.
# Herstellen (DB-45: het herstelcommando hoort in het script; DB-50):
#   age -d -i <privesleutel> <bestand>.dump.age | docker exec -i <wegwerpcontainer> pg_restore -U <rol> -d <db> --exit-on-error
#   age -d -i <privesleutel> <bestand>-globals.sql.age | docker exec -i <wegwerpcontainer> psql -X --set ON_ERROR_STOP=on -U <rol> -d postgres
#   daarna ANALYZE. Zie herstelproef.sh.
# Draaien: dagelijks via een timer of cron met een harde time-out en een foutmelding (03-systemd/).
# Controleren (DB-45): file <nieuwste back-up> toont een age-bestand en geen leesbare SQL of gzip.
# Niet tegen Docker of een server gedraaid; alleen bash -n en shellcheck 0.11.0 (zonder bevinding).
set -euo pipefail
umask 077
export PATH=/usr/local/bin:/usr/bin:/bin
trap 'echo "fout op regel $LINENO: $BASH_COMMAND" >&2' ERR

CONTAINER=voorbeeld-postgres
BEHEERROL=postgres
DATABASES=(voorbeeld)
DOEL=/var/backups/voorbeeld
AGE_ONTVANGER="${AGE_ONTVANGER:?zet AGE_ONTVANGER op de publieke age-sleutel}"
BEWAAR_DAGEN="${BEWAAR_DAGEN:?zet BEWAAR_DAGEN op 14 (website) of 30 (webshop of eigen systeem), zie de kop (DB-57)}"
[[ "$BEWAAR_DAGEN" =~ ^[0-9]+$ ]] || { echo "fout: BEWAAR_DAGEN is geen getal" >&2; exit 2; }

install -d -m 700 -- "$DOEL"
exec 9>"$DOEL/.backup.lock"
flock -n -E 75 9 || { rc=$?; [ "$rc" -eq 75 ] && { echo "draait al, overgeslagen"; exit 0; }; exit "$rc"; }

STEMPEL=$(date -u +%Y%m%dT%H%M%SZ)

# Dumpen vanuit de container zelf: dezelfde major als de server (DB-48). Custom-formaat (DB-50).
# Eerst naar een tijdelijke naam, dan mv: een half bestand telt nooit als back-up (SCR-17).
for db in "${DATABASES[@]}"; do
  [[ "$db" =~ ^[a-z_][a-z0-9_]*$ ]] || { echo "fout: ongeldige databasenaam: $db" >&2; exit 2; }
  uit="$DOEL/$db-$STEMPEL.dump.age"
  docker exec "$CONTAINER" pg_dump -U "$BEHEERROL" -Fc -- "$db" | age -r "$AGE_ONTVANGER" -o "$uit.deel"
  [ -s "$uit.deel" ] || { echo "fout: lege back-up voor $db" >&2; exit 1; }
  mv -f -- "$uit.deel" "$uit"
  echo "back-up: $uit ($(stat -c %s -- "$uit") bytes)"
done

# Rollen en rechten (DB-44).
uit="$DOEL/globals-$STEMPEL.sql.age"
docker exec "$CONTAINER" pg_dumpall -U "$BEHEERROL" --globals-only | age -r "$AGE_ONTVANGER" -o "$uit.deel"
[ -s "$uit.deel" ] || { echo "fout: lege back-up van de globale objecten" >&2; exit 1; }
mv -f -- "$uit.deel" "$uit"

# Bewaartermijn (DB-57): alleen eigen bestanden, in de eigen map, op naam en leeftijd.
find "${DOEL:?}" -maxdepth 1 -type f -name '*.age' -mtime +"$BEWAAR_DAGEN" -print -delete
find "${DOEL:?}" -maxdepth 1 -type f -name '*.deel' -mmin +120 -print -delete
