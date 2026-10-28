// Sjabloon: cross-tenant regressietest per tabel, tegen een echte PostgreSQL met de runtime-rol.
// Dekt: DB-22, AUTH-77 (het tabeldeel), AUTH-74, ARCH-35, DB-14, DB-17
// Dekt gedeeltelijk:
//   - AUTH-77 en AUTH-66 vragen dezelfde proef ook per route (niet ingelogd, andere gebruiker in dezelfde
//     tenant, andere tenant, te lage rol) met een vergelijking tegen de lijst geregistreerde routes. Dat deel
//     hangt van de applicatie af en staat hier niet.
//   - DB-22 vraagt de proef ook voor elke view en elke SECURITY DEFINER-functie; voeg die toe aan TABELLEN of
//     als eigen test.
// Aanpassen: TABELLEN (per tenant-tabel de kolommen voor een minimale rij) en de naam van de tenanttabel.
// Draaien: TEST_DATABASE_URL wijst naar een testdatabase met de echte migraties en verbindt als de runtime-rol,
//   niet als eigenaar of superuser (ARCH-35). Eigen testgeheimen, nooit die van productie (ARCH-49).
//   De test draait in een transactie en rolt terug; er blijft niets achter.
// Controleren: de test is een verplichte stap in de gate en voor elke uitrol (AUTH-77, ARCH-40); een nieuwe
//   tabel met tenant_id die niet in TABELLEN staat maakt de metatest rood.
// Gevalideerd op 04-10-2026: typecontrole met tsc 6.0.3 en vitest list (Vitest 5.0.3). Niet tegen een server
//   gedraaid; de policy zelf is wel getest met 06-database/migraties/0001 tegen PostgreSQL 18.6.
import { randomUUID } from 'node:crypto';
import pg from 'pg';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';

// Per tenant-tabel: de kolommen (naast id en tenant_id) voor een minimale geldige rij.
const TABELLEN: Record<string, Record<string, unknown>> = {
  contacts: { naam: 'Testpersoon Verzonnen' },
  meetings: { titel: 'Testafspraak' },
};
const NAAM = /^[a-z_][a-z0-9_]*$/;

const url = process.env.TEST_DATABASE_URL;
if (url === undefined) throw new Error('TEST_DATABASE_URL ontbreekt');
const pool = new pg.Pool({ connectionString: url, max: 1 });
let client: pg.PoolClient;

async function zetTenant(tenantId: string): Promise<void> {
  await client.query("select set_config('app.tenant_id', $1, true)", [tenantId]);
}

async function voegToe(tabel: string, tenantId: string): Promise<string> {
  const extra = TABELLEN[tabel];
  if (extra === undefined || !NAAM.test(tabel)) throw new Error(`onbekende tabel: ${tabel}`);
  const kolommen = ['id', 'tenant_id', ...Object.keys(extra)];
  if (!kolommen.every((k) => NAAM.test(k))) throw new Error('ongeldige kolomnaam');
  const id = randomUUID();
  const plaatsen = kolommen.map((_, i) => `$${String(i + 1)}`).join(', ');
  // Tabel- en kolomnamen komen uit de vaste lijst hierboven; de waarden gaan als parameter mee (DB-25, DB-27).
  await client.query(`insert into "${tabel}" (${kolommen.map((k) => `"${k}"`).join(', ')}) values (${plaatsen})`, [
    id,
    tenantId,
    ...Object.values(extra),
  ]);
  return id;
}

beforeAll(async () => {
  client = await pool.connect();
});
afterAll(async () => {
  client.release();
  await pool.end();
});

describe('opzet', () => {
  it('draait met de runtime-rol: geen superuser, geen BYPASSRLS (ARCH-35, DB-14)', async () => {
    const r = await client.query<{ rolsuper: boolean; rolbypassrls: boolean }>(
      'select rolsuper, rolbypassrls from pg_roles where rolname = current_user',
    );
    expect(r.rows).toEqual([{ rolsuper: false, rolbypassrls: false }]);
  });

  it('elke tabel met tenant_id staat in de test (DB-22, AUTH-77)', async () => {
    const r = await client.query<{ table_name: string }>(
      "select table_name from information_schema.columns where column_name = 'tenant_id' and table_schema = 'public' order by 1",
    );
    expect(r.rows.map((rij) => rij.table_name)).toEqual(Object.keys(TABELLEN).sort());
  });

  it('elke tenant-tabel heeft RLS aan en afgedwongen (DB-13)', async () => {
    const r = await client.query<{ relname: string }>(
      'select relname from pg_class where relname = any($1) and not (relrowsecurity and relforcerowsecurity)',
      [Object.keys(TABELLEN)],
    );
    expect(r.rows).toEqual([]);
  });
});

describe.each(Object.keys(TABELLEN))('tenant-isolatie: %s', (tabel) => {
  it('tenant A kan rijen van tenant B niet lezen, wijzigen, verwijderen of invoegen', async () => {
    const a = randomUUID();
    const b = randomUUID();
    await client.query('begin');
    try {
      // Twee tenants zaaien, elk onder de eigen context.
      for (const tenant of [a, b]) {
        await zetTenant(tenant);
        await client.query('insert into tenants (id, naam) values ($1, $2)', [tenant, 'Testtenant']);
      }
      await zetTenant(b);
      const rijVanB = await voegToe(tabel, b);

      await zetTenant(a);
      const lezen = await client.query(`select 1 from "${tabel}" where id = $1`, [rijVanB]);
      expect(lezen.rowCount).toBe(0);
      const wijzigen = await client.query(`update "${tabel}" set tenant_id = tenant_id where id = $1`, [rijVanB]);
      expect(wijzigen.rowCount).toBe(0);
      const verwijderen = await client.query(`delete from "${tabel}" where id = $1`, [rijVanB]);
      expect(verwijderen.rowCount).toBe(0);

      // Invoegen in tenant B vanuit context A: geweigerd door WITH CHECK. Een fout breekt de transactie af,
      // daarom een savepoint.
      await client.query('savepoint invoegen');
      await expect(voegToe(tabel, b)).rejects.toThrow(/row-level security/);
      await client.query('rollback to savepoint invoegen');

      // De rij van B bestaat nog, gezien vanuit B.
      await zetTenant(b);
      const nog = await client.query(`select 1 from "${tabel}" where id = $1`, [rijVanB]);
      expect(nog.rowCount).toBe(1);
    } finally {
      await client.query('rollback');
    }
  });

  it('zonder tenantcontext faalt de query (DB-17)', async () => {
    await client.query('begin');
    try {
      await expect(client.query(`select 1 from "${tabel}" limit 1`)).rejects.toThrow();
    } finally {
      await client.query('rollback');
    }
  });
});
