// Sjabloon: configuratie uit de omgeving, bij het opstarten gevalideerd tegen een schema.
// Dekt: ARCH-07, API-01 (omgevingsvariabelen), API-65, ARCH-08
// Aanpassen: de lijst variabelen. Geen standaardwaarden voor geheimen of limieten: ontbreekt er een, dan start
//   het proces niet. Lees process.env nergens anders (ARCH-07).
// De limieten per route-klasse hebben geen waarde in het onderzoek (API-20): kies ze per project en leg ze vast.
// Controleren: grep -rn "process\.env" src toont alleen dit bestand; starten zonder MOLLIE_API_KEY stopt met
//   een duidelijke fout.
// Gevalideerd op 04-10-2026 in een wegwerpcontainer: tsc --noEmit met de tsconfig uit 07-typescript-tests
//   (TypeScript 6.0.3) en eslint --max-warnings 0 met eslint.config.mjs (typescript-eslint 8.71.0), beide groen.
//   Niet gedraaid als dienst.
import { z } from 'zod';

const Env = z.object({
  NODE_ENV: z.enum(['production', 'test', 'development']),
  RELEASE: z.string().min(1), // het release-id uit de build (ARCH-09)
  HOST: z.literal('127.0.0.1').or(z.literal('0.0.0.0')), // 0.0.0.0 alleen in een container op een intern netwerk (INFRA-13)
  PORT: z.coerce.number().int().min(1024).max(65535),
  PROXY_ADRES: z.string().min(1), // het adres van de eigen nginx, voor trustProxy (WEB-51)
  DATABASE_URL: z.url(),
  MOLLIE_API_KEY: z.string().regex(/^(test|live)_[A-Za-z0-9]{30,}$/),
  RATE_LIMIT_ALGEMEEN_PER_MINUUT: z.coerce.number().int().min(1),
  RATE_LIMIT_BESTELLEN_PER_MINUUT: z.coerce.number().int().min(1),
});

export const env = Env.parse(process.env);
export type Env = z.infer<typeof Env>;
