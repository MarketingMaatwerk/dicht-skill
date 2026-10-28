// Sjabloon: de ene verbindingspool van de dienst.
// Dekt: DB-63 (een pool per dienst), DB-65 (time-out, naast die op de rol), DB-62
// Aanpassen: max. Het onderzoek noemt geen getal: kies de poolgrootte zo dat de som over alle diensten onder
//   max_connections blijft (DB-63) en zet CONNECTION LIMIT van de rol op de pool plus een kleine marge (DB-10).
//   Zonder max geldt de standaard van de pg-bibliotheek.
// De verbindingsstring is een geheim (DB-62): hij komt uit env.ts en wordt nooit gelogd.
// Gevalideerd op 04-10-2026 in een wegwerpcontainer: tsc --noEmit met de tsconfig uit 07-typescript-tests
//   (TypeScript 6.0.3) en eslint --max-warnings 0 met eslint.config.mjs (typescript-eslint 8.71.0), beide groen.
//   Niet gedraaid als dienst.
import pg from 'pg';
import { env } from './env.js';

export const pool = new pg.Pool({
  connectionString: env.DATABASE_URL,
  statement_timeout: 30_000, // richtwaarde uit DB-65 voor een API
});
