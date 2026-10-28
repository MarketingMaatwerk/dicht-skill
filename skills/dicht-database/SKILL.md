---
name: dicht-database
description: Regels met bewijs voor PostgreSQL en Drizzle (schema, migratie, tabel, query, rollen, RLS en multi-tenant, SQL-injectie, transacties, back-up en herstel). Niet voor de MySQL-kant van WordPress (dicht-wordpress).
---

# dicht-database: PostgreSQL en datamanagement

Sub-skill van `dicht`. Bevat de 98 regels van domein DB in tien thema's. Stack: PostgreSQL 16 en 18 in Docker, Drizzle, postgres.js en node-postgres.

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/db-a-rollen-en-minimale-rechten.md` | DB-01 t/m DB-10 (10 actief) | rollen en minimale rechten |
| `references/db-b-rij-niveau-beveiliging-en-multi-tenant.md` | DB-11 t/m DB-24 (14 actief) | rij-niveau beveiliging en multi-tenant |
| `references/db-c-sql-injectie-en-querybouw.md` | DB-25 t/m DB-29 (5 actief) | SQL-injectie en querybouw |
| `references/db-d-migraties-zonder-risico.md` | DB-30 t/m DB-43 (14 actief) | migraties zonder risico |
| `references/db-e-back-up-en-herstel.md` | DB-44 t/m DB-57 (14 actief) | back-up en herstel |
| `references/db-f-verbinding-netwerk-en-authenticatie.md` | DB-58 t/m DB-65 (8 actief) | verbinding, netwerk en authenticatie |
| `references/db-g-data-integriteit-en-transacties.md` | DB-66 t/m DB-73 (6 actief) | data-integriteit en transacties |
| `references/db-h-schema-ontwerp.md` | DB-74 t/m DB-79 (6 actief) | schema-ontwerp |
| `references/db-i-versleuteling-bewaartermijnen-en-privacy.md` | DB-80 t/m DB-88 (9 actief) | versleuteling, bewaartermijnen en privacy |
| `references/db-j-auditing-monitoring-en-onderhoud.md` | DB-89 t/m DB-98 (10 actief) | auditing, monitoring en onderhoud |

## Wanneer niet

- `$wpdb`, tabelprefix en de databasegebruiker van een WordPress-site: `dicht-wordpress`.
- Bedrijfsregels rond races, idempotentie en Mollie: `dicht-api`, thema API-D en API-E. DB-66 en DB-67 zijn daarmee samengevoegd.
- Back-up van de host, offsite-opslag en geheimen op de server: `dicht-infra`, thema I en J.
- Wettelijke bewaartermijnen en wisverzoeken: `dicht-privacy`, thema D en E.

## Verhouding tot bestaande skills

- `postgresql-table-design`: goed voor types, indexen en constraints (DB-77 verwijst ernaar). Dun op beveiliging: de RLS-alinea noemt `FORCE`, eigenaar, `BYPASSRLS` en views niet; DB-11 tot en met DB-24 vullen dat aan. De skill noemt `pgcrypto` met `crypt()` voor wachtwoorden: gebruik dat niet, zie DB-81.
- `supabase-postgres-best-practices`: bruikbaar voor queryprestaties en verbindingen. De RLS-voorbeelden gebruiken een sessiebrede `set app.current_user_id`, wat met een pool tot kruisbesmetting leidt: DB-16 gaat voor. De voorbeelden met `auth.uid()` zijn Supabase-specifiek.
- `drizzle-orm`: noemt `generate` en `migrate`, maar niets over locks, terugweg of `sql.raw`: DB-25 tot en met DB-43.
- `secrets-management`: gaat over CI-geheimen. Databasegeheimen staan in DB-61 en DB-62.
