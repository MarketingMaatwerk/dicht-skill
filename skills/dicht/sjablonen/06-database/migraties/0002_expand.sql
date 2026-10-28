-- Sjabloon expand en contract, stap 1 van 3: toevoegen. De oude vorm blijft werken.
-- Voorbeeld: de kolom orders.klant_naam (tekst) wordt vervangen door orders.contact_id (verwijzing).
-- Dekt: DB-31, DB-32, DB-34, DB-36 (geen herschrijving: kolom zonder standaardwaarde), DB-40, DB-30
-- Aanpassen: tabel, kolommen en constraintnamen.
-- Release 1 (dit bestand): nieuwe kolom, nullable, zonder standaardwaarde; foreign key als NOT VALID.
--   De code van release 1 schrijft naar beide vormen en leest nog de oude.
-- Controleren: getest op een recente kopie van productie (DB-39); de migratie blijft binnen lock_timeout.
-- terugweg: ALTER TABLE orders DROP COLUMN contact_id;  (er is nog niets dat alleen de nieuwe kolom leest)
-- Gevalideerd op 04-10-2026 tegen een wegwerp-PostgreSQL 18.6 (2500 rijen), in de volgorde 0002 tot en met 0005.

SET lock_timeout = '5s';
SET statement_timeout = '60s';

ALTER TABLE orders ADD COLUMN contact_id uuid;

ALTER TABLE orders ADD CONSTRAINT orders_contact_fk
  FOREIGN KEY (tenant_id, contact_id) REFERENCES contacts (tenant_id, id) NOT VALID;
