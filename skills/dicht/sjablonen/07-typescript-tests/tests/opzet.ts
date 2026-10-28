// Sjabloon: testopzet die uitgaand verkeer buiten 127.0.0.1 blokkeert.
// Dekt: ARCH-50
// Dekt gedeeltelijk: dit onderschept alleen fetch. Een bibliotheek die zelf een socket opent (node:http, pg,
//   nodemailer) valt erbuiten; bootst die na of geef ze een adres op 127.0.0.1.
// Controleren (ARCH-50): een test die een onbekende host aanroept faalt met de fout hieronder.
// Gevalideerd op 04-10-2026: typecontrole met tsc 6.0.3 en geladen door Vitest 5.0.3 (vitest list). Niet gedraaid.
import { beforeAll } from 'vitest';

const TOEGESTAAN = new Set(['127.0.0.1', 'localhost', '[::1]']);

beforeAll(() => {
  const echteFetch = globalThis.fetch;
  globalThis.fetch = (invoer, opties) => {
    const adres = invoer instanceof Request ? invoer.url : String(invoer);
    const host = new URL(adres).hostname;
    if (!TOEGESTAAN.has(host)) {
      throw new Error(`onverwachte uitgaande aanroep in een test: ${host} (ARCH-50)`);
    }
    return echteFetch(invoer, opties);
  };
});
