-- Sjabloon expand en contract, stap 2 van 3: na de backfill (backfill.sh) de constraints valideren.
-- Dekt: DB-34, DB-35, DB-32
-- Release 2: de code leest en schrijft de nieuwe vorm; de oude kolom wordt nog gevuld of genegeerd.
-- NOT NULL op een gevulde kolom gaat in vier stappen (DB-35): CHECK NOT VALID, valideren, SET NOT NULL,
--   CHECK weg. De eerste stap houdt het slot kort; het valideren leest de tabel zonder schrijvers te blokkeren.
-- Controleren: de SET NOT NULL-stap blijft op de kopie van productie binnen lock_timeout (DB-35, DB-39).
-- terugweg: ALTER TABLE orders ALTER COLUMN contact_id DROP NOT NULL;
-- Gevalideerd op 04-10-2026 tegen een wegwerp-PostgreSQL 18.6: voor de backfill faalt het bestand op de CHECK,
--   na de backfill slaagt het en is contact_id NOT NULL.

SET lock_timeout = '5s';
SET statement_timeout = '60s';

ALTER TABLE orders VALIDATE CONSTRAINT orders_contact_fk;

ALTER TABLE orders ADD CONSTRAINT orders_contact_id_niet_leeg CHECK (contact_id IS NOT NULL) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_contact_id_niet_leeg;
ALTER TABLE orders ALTER COLUMN contact_id SET NOT NULL;
ALTER TABLE orders DROP CONSTRAINT orders_contact_id_niet_leeg;
