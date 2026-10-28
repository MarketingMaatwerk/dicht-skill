-- Sjabloon expand en contract, stap 3 van 3: verwijderen.
-- Dekt: DB-31, DB-32, DB-40
-- Release 3: pas nadat een release heeft gedraaid waarin niets de oude kolom meer leest of schrijft (DB-31).
-- De regel hieronder met "contract:" is verplicht; de CI-controle uit DB-31 eist hem bij elke DROP of RENAME.
-- contract: expand in 0002_expand.sql (release <id>), omgezet in release <id>
-- terugweg: dump van de kolom voor het verwijderen: <pad>, sha256 <controlesom>; herstelproef <datum> (DB-40)
-- Controleren: grep -rn "klant_naam" src/ is leeg in de release die nu draait.
-- Gevalideerd op 04-10-2026 tegen een wegwerp-PostgreSQL 18.6: de kolom is weg.

SET lock_timeout = '5s';
SET statement_timeout = '60s';

ALTER TABLE orders DROP COLUMN klant_naam;
