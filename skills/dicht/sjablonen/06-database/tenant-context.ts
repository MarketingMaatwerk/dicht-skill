// Sjabloon: tenantcontext per transactie voor Drizzle met PostgreSQL en RLS.
// Dekt: DB-16, DB-17, AUTH-72, AUTH-74, AUTH-75
// Aanpassen: de import van je eigen db-instantie en het type van tenantId.
// Gebruik: elke query op een tenant-tabel loopt via metTenant(). De tenant komt uit de geverifieerde sessie
//   op de server, nooit uit de aanvraag (AUTH-72, DB-17).
// Waarom zo: set_config(..., true) geldt alleen binnen de transactie. Een sessiebrede SET lekt via de pool
//   naar het volgende verzoek (DB-16).
// Controleren (DB-16):
//   grep -rnE "SET (SESSION )?app\.|set_config\([^)]*false" src/     geeft nul treffers
//   een test met twee verzoeken van verschillende tenants over een pool van een verbinding slaagt
// Gevalideerd op 04-10-2026 in een wegwerpcontainer: tsc --noEmit met de tsconfig uit 07-typescript-tests
//   (TypeScript 6.0.3) en eslint --max-warnings 0 met eslint.config.mjs (typescript-eslint 8.71.0), beide groen.
//   Niet tegen een database gedraaid.
import { sql } from 'drizzle-orm';
import type { NodePgDatabase } from 'drizzle-orm/node-postgres';

type Tx = Parameters<Parameters<NodePgDatabase['transaction']>[0]>[0];

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export async function metTenant<T>(
  db: NodePgDatabase,
  tenantId: string,
  werk: (tx: Tx) => Promise<T>,
): Promise<T> {
  // Faal gesloten: geen tenant, geen query (DB-17). Geen standaardwaarde.
  if (!UUID.test(tenantId)) {
    throw new Error('tenantcontext ontbreekt of is ongeldig');
  }
  return db.transaction(async (tx) => {
    // De waarde gaat als parameter mee, niet als tekst in de query (DB-25).
    await tx.execute(sql`select set_config('app.tenant_id', ${tenantId}, true)`);
    return werk(tx);
  });
}
