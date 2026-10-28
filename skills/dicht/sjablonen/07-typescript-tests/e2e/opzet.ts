// Sjabloon: gedeelde testopzet. Een JavaScript-fout in de console of een mislukt verzoek naar de eigen host
//   laat de test falen.
// Dekt: ARCH-37
// Gebruik: importeer test en expect uit dit bestand in plaats van uit @playwright/test.
// Gevalideerd op 04-10-2026: typecontrole met tsc 6.0.3 en geladen door Playwright 1.63.0 (--list). Niet in een
//   browser gedraaid.
import { test as basis, expect } from '@playwright/test';

export const test = basis.extend<{ bewaakConsole: void }>({
  bewaakConsole: [
    async ({ page, baseURL }, use) => {
      const fouten: string[] = [];
      page.on('pageerror', (fout) => fouten.push(`pageerror: ${fout.message}`));
      page.on('console', (bericht) => {
        if (bericht.type() === 'error') fouten.push(`console: ${bericht.text()}`);
      });
      page.on('response', (antwoord) => {
        const eigenHost = baseURL !== undefined && antwoord.url().startsWith(baseURL);
        if (eigenHost && antwoord.status() >= 500) fouten.push(`${String(antwoord.status())} ${antwoord.url()}`);
      });
      page.on('requestfailed', (verzoek) => {
        const eigenHost = baseURL !== undefined && verzoek.url().startsWith(baseURL);
        if (eigenHost) fouten.push(`mislukt: ${verzoek.url()}`);
      });
      await use();
      expect(fouten, 'geen fouten in de console of op de eigen host').toEqual([]);
    },
    { auto: true },
  ],
});

export { expect };
