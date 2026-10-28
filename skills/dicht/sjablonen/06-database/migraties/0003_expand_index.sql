-- Sjabloon expand en contract, stap 1b: index op een gevulde tabel, in een eigen bestand buiten een transactie.
-- Dekt: DB-33
-- Dekt gedeeltelijk: of drizzle-kit migrate een bestand buiten een transactie kan draaien is in het onderzoek
--   niet bevestigd (DB-33). Draai dit bestand daarom met psql, met de migratierol:
--     psql -X -v ON_ERROR_STOP=1 -f 0003_expand_index.sql
-- Controleren (stap in het deployscript, DB-33):
--   SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;     geeft nul rijen
--   Een ongeldige index na een afgebroken run: DROP INDEX CONCURRENTLY en opnieuw.
-- terugweg: DROP INDEX CONCURRENTLY IF EXISTS orders_tenant_contact_idx;
-- Gevalideerd op 04-10-2026 tegen een wegwerp-PostgreSQL 18.6: de index is geldig; met psql -1 (in een
--   transactie) faalt het bestand, zoals bedoeld.

SET lock_timeout = '5s';

CREATE INDEX CONCURRENTLY IF NOT EXISTS orders_tenant_contact_idx ON orders (tenant_id, contact_id);
