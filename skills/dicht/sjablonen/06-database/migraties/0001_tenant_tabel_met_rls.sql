-- Sjabloon: migratie die een tenant-tabel aanmaakt, met rechten en RLS in dezelfde migratie.
-- Dekt: DB-12, DB-13, DB-15, DB-17, DB-20, DB-32, DB-43, DB-74, DB-30, AUTH-74
-- Aanpassen: de tabelnaam, de kolommen, de app-rol en het type van tenant_id (hier uuid, gelijk aan de cast
--   in de policy). De permissieve policy "leden" is het minimum uit DB-15; maak hem strenger als rollen binnen
--   een tenant verschillen.
-- Draaien: met de migratierol, als aparte deploystap (DB-41), met drizzle-kit migrate; nooit drizzle-kit push
--   tegen productie of accept (DB-30).
-- De policy gebruikt current_setting('app.tenant_id') zonder missing_ok en zonder standaardwaarde: zonder
--   tenantcontext faalt elke query (DB-17). De context zet de applicatie per transactie (tenant-context.ts, DB-16).
-- Controleren:
--   SELECT relname, relrowsecurity, relforcerowsecurity FROM pg_class WHERE relname = 'meetings';   t en t (DB-13)
--   de cross-tenant test (07-typescript-tests/tenant-isolatie.test.ts) slaagt met de app-rol (DB-22)
-- terugweg: DROP TABLE meetings;  (alleen zolang de tabel leeg is; daarna een dump met controlesom, DB-40)
-- Gevalideerd op 04-10-2026 tegen een wegwerp-PostgreSQL 18.6, met de rollen uit rollen.sql: zonder context
--   faalt elke query (ook op een hergebruikte verbinding en ook voor de eigenaar), tenant B ziet, wijzigt en
--   verwijdert niets van tenant A, een rij voor een andere tenant en een contact van een andere tenant worden
--   geweigerd.

SET lock_timeout = '5s';
SET statement_timeout = '60s';

CREATE TABLE meetings (
  id          uuid        NOT NULL DEFAULT gen_random_uuid(),
  tenant_id   uuid        NOT NULL REFERENCES tenants (id),
  contact_id  uuid,
  titel       text        NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (id),
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, contact_id) REFERENCES contacts (tenant_id, id)
);
-- tenant_id vooraan in een index (DB-12).
CREATE INDEX meetings_tenant_created_idx ON meetings (tenant_id, created_at);

-- RLS aan en afgedwongen, ook voor de eigenaar (DB-13).
ALTER TABLE meetings ENABLE ROW LEVEL SECURITY;
ALTER TABLE meetings FORCE ROW LEVEL SECURITY;

-- De tenantgrens als restrictieve policy met USING en WITH CHECK, naast een permissieve (DB-15).
CREATE POLICY tenant_grens ON meetings AS RESTRICTIVE FOR ALL
  USING (tenant_id = current_setting('app.tenant_id')::uuid)
  WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
CREATE POLICY leden ON meetings AS PERMISSIVE FOR ALL
  USING (true) WITH CHECK (true);

-- Rechten per bewerking in dezelfde migratie (DB-43, DB-05). Geen TRUNCATE, geen REFERENCES (DB-21).
-- Eerst alles intrekken, ook van de app-rol: de standaardrechten uit rollen.sql geven hem al vier bewerkingen
-- en een GRANT van minder trekt niets in. Zo geldt precies wat hieronder staat.
REVOKE ALL ON meetings FROM PUBLIC, voorbeeld_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON meetings TO voorbeeld_app;
