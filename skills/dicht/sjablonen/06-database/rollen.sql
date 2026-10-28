-- Sjabloon: rollen en minimale rechten voor een database van een dienst.
-- Dekt: DB-01, DB-02, DB-03, DB-04, DB-05, DB-06, DB-07, DB-08, DB-10 (als commentaar), DB-14, DB-21, DB-61, DB-65, SCR-11
-- Aanpassen: de drie namen in het \set-blok. De time-outs zijn de richtwaarden uit DB-65 (30s voor een API,
--   langer voor een worker). CONNECTION LIMIT heeft geen waarde in de bron: zet hem op de poolgrootte van de
--   dienst plus een kleine marge (DB-10).
-- Draaien: eenmalig, als beheerder, per omgeving met eigen rolnamen en eigen wachtwoorden (DB-02):
--   psql -X -v ON_ERROR_STOP=1 -d <database> -f rollen.sql
-- Wachtwoorden: nooit in dit bestand, een migratie of een shell-opdracht (DB-61). Zet ze daarna interactief:
--   \password <app-rol>     en     \password <migratierol>
-- Controleren:
--   SELECT rolname, rolsuper, rolcreatedb, rolcreaterole, rolbypassrls, rolreplication FROM pg_roles
--     WHERE rolname IN (:'app', :'migrator');                          overal f (DB-01, DB-06, DB-14)
--   SELECT tableowner, count(*) FROM pg_tables WHERE schemaname = 'public' GROUP BY 1;   alleen de migratierol (DB-03)
--   \dp                                                                 geen TRUNCATE of REFERENCES voor de app-rol (DB-21)
--   SELECT has_database_privilege('public', current_database(), 'CONNECT');   f (DB-04)
-- Gevalideerd op 04-10-2026 tegen een wegwerp-PostgreSQL 18.6: het script draait zonder fout en de vier
--   controles hierboven geven de genoemde uitkomst; de app-rol kan geen tabel maken, niet TRUNCATE en geen
--   functie van de migratierol uitvoeren. Een tweede run faalt op "role already exists" (eenmalig script).

\set db voorbeeld
\set app voorbeeld_app
\set migrator voorbeeld_migrator

-- Aparte rollen zonder gevaarlijke attributen (DB-01, DB-06). De migratierol is eigenaar en doet DDL (DB-03);
-- de app-rol is de runtime-rol en is nooit eigenaar (DB-14).
CREATE ROLE :"migrator" LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS NOREPLICATION;
CREATE ROLE :"app"      LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS NOREPLICATION;
-- ALTER ROLE :"app" CONNECTION LIMIT <poolgrootte plus marge>;   -- DB-10

-- Standaardrechten van PUBLIC intrekken (DB-04).
REVOKE ALL ON DATABASE :"db" FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT CONNECT ON DATABASE :"db" TO :"app", :"migrator";
GRANT USAGE ON SCHEMA public TO :"app";
GRANT USAGE, CREATE ON SCHEMA public TO :"migrator";

-- Rechten per bewerking op toekomstige tabellen van de migratierol, nooit GRANT ALL (DB-05).
-- Geen TRUNCATE en geen REFERENCES voor de runtime-rol (DB-21).
ALTER DEFAULT PRIVILEGES FOR ROLE :"migrator" IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO :"app";
ALTER DEFAULT PRIVILEGES FOR ROLE :"migrator" IN SCHEMA public
  GRANT USAGE ON SEQUENCES TO :"app";
-- Waar de dienst niet wijzigt of verwijdert, trek je het per tabel in, in de migratie van die tabel (DB-05, DB-43):
--   REVOKE DELETE, UPDATE ON audit_log FROM <app-rol>;

-- EXECUTE op functies niet aan PUBLIC, zonder IN SCHEMA (DB-07). Verleen EXECUTE daarna per functie.
ALTER DEFAULT PRIVILEGES FOR ROLE :"migrator" REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;

-- Vast search_path per rol (DB-08).
ALTER ROLE :"app"      SET search_path = public;
ALTER ROLE :"migrator" SET search_path = public;

-- Time-outs per rol (DB-65, richtwaarden uit de regel).
ALTER ROLE :"app" SET statement_timeout = '30s';
ALTER ROLE :"app" SET idle_in_transaction_session_timeout = '60s';
ALTER ROLE :"app" SET lock_timeout = '10s';
