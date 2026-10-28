-- Sjabloon: tabellen voor idempotente routes en webhooks.
-- Dekt: BIZ-39, API-33, DB-68, API-31, API-38, ARCH-20
-- De tabel idempotentie is letterlijk die uit BIZ-39. De tabel taken is een minimale outbox met de unieke
--   sleutel uit API-38 (betaling of bestelling plus taaksoort). betalingen.mollie_payment_id is uniek (BIZ-46).
-- Aanpassen: de app-rol, en de kolommen van taken en betalingen naar het eigen model. RLS en rechten horen in
--   dezelfde migratie (DB-43); zie 06-database/migraties/0001_tenant_tabel_met_rls.sql voor het patroon.
-- terugweg: DROP TABLE idempotentie, taken;  (alleen zolang ze leeg zijn)
-- Gevalideerd op 04-10-2026 tegen een wegwerp-PostgreSQL 18.6: een dubbele sleutel en een dubbele taak worden
--   geweigerd, een onbekende status ook, en de app-rol kan niet verwijderen uit taken.
-- Let op: deze twee tabellen hebben in dit sjabloon geen RLS; idempotentie heeft een tenant_id en krijgt in een
--   project met tenants het patroon uit 0001 (DB-13, DB-43).

SET lock_timeout = '5s';
SET statement_timeout = '60s';

CREATE TABLE idempotentie (
  tenant_id uuid NOT NULL, route text NOT NULL, sleutel text NOT NULL,
  body_hash bytea NOT NULL, status text NOT NULL CHECK (status IN ('bezig', 'klaar')),
  antwoord jsonb, aangemaakt_op timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (tenant_id, route, sleutel));

CREATE TABLE taken (
  id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  bestelling_id uuid NOT NULL,
  soort         text NOT NULL,
  status        text NOT NULL DEFAULT 'nieuw',
  aangemaakt_op timestamptz NOT NULL DEFAULT now(),
  UNIQUE (bestelling_id, soort)
);

-- Elk extern id uniek (BIZ-46): een tweede rij voor dezelfde Mollie-betaling kan niet bestaan.
-- ALTER TABLE betalingen ADD CONSTRAINT betalingen_mollie_payment_id_uniek UNIQUE (mollie_payment_id);

-- Eerst alles intrekken, ook van de app-rol: de standaardrechten uit 06-database/rollen.sql geven hem anders
-- op elke nieuwe tabel SELECT, INSERT, UPDATE en DELETE, en een GRANT van minder trekt niets in (DB-05, DB-43).
REVOKE ALL ON idempotentie, taken FROM PUBLIC, voorbeeld_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON idempotentie TO voorbeeld_app;
GRANT SELECT, INSERT, UPDATE ON taken TO voorbeeld_app;
