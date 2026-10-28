#!/usr/bin/env bash
# Sjabloon expand en contract, tussen stap 1 en 2: gegevens bijvullen in kleine batches.
# Dekt: DB-38, SCR-01, SCR-11
# Aanpassen: de UPDATE (hier: contact_id opzoeken bij klant_naam) en BATCH. De regel noemt 1.000 tot 10.000
#   rijen per batch; 1000 is de ondergrens daarvan.
# Draaien: met de migratierol; de verbinding komt uit PGSERVICE of PGPASSFILE, nooit uit een argument (SCR-19).
#   Los van de schemamigratie, elke batch in een eigen korte transactie (DB-38).
# Controleren (DB-38): een tweede run meldt 0 rijen (idempotent).
# Gevalideerd op 04-10-2026 tegen een wegwerp-PostgreSQL 18.6: 2500 rijen in batches van 1000, 1000, 500 en 0;
#   een tweede run meldt 0 rijen.
set -euo pipefail

BATCH=1000
totaal=0
while true; do
  # Elke psql-aanroep is een eigen transactie. De waarde gaat als psql-variabele mee (SCR-11).
  n=$(psql -X -At -v ON_ERROR_STOP=1 -v batch="$BATCH" <<'SQL'
WITH doel AS (
  SELECT o.id, c.id AS contact_id
  FROM orders o
  JOIN contacts c ON c.tenant_id = o.tenant_id AND c.naam = o.klant_naam
  WHERE o.contact_id IS NULL
  LIMIT :batch
  FOR UPDATE OF o SKIP LOCKED
), bijgewerkt AS (
  UPDATE orders o SET contact_id = doel.contact_id FROM doel WHERE o.id = doel.id RETURNING 1
)
SELECT count(*) FROM bijgewerkt;
SQL
  )
  totaal=$((totaal + n))
  echo "batch: $n rijen, totaal $totaal"
  [ "$n" -gt 0 ] || break
  sleep 1
done
echo "klaar: $totaal rijen bijgewerkt"
