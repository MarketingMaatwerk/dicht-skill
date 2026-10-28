// Sjabloon: Playwright-configuratie.
// Dekt: ARCH-38 (de twee schermbreedtes), ARCH-39, ARCH-49, ARCH-12
// Aanpassen: baseURL (een testomgeving, nooit productie: ARCH-51) en het aantal herhalingen in CI
//   (ARCH-39: lokaal nul, in CI "hooguit een klein aantal"; het getal 1 hieronder is een eigen invulling).
// Controleren (ARCH-39): de suite slaagt met --workers=1 en in de parallelle stand; nul tests met status flaky.
// Gevalideerd op 04-10-2026 met Playwright 1.63.0 (wegwerpcontainer): playwright test --list toont beide
//   projecten (1440 en 375) met acht tests. Niet in een browser gedraaid.
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: process.env.E2E_BASE_URL,
    timezoneId: 'Europe/Amsterdam',
    trace: 'retain-on-failure',
  },
  projects: [
    // De twee breedtes uit ARCH-38: 1440 en 375 pixels. De hoogtes zijn een eigen invulling.
    { name: 'breed-1440', use: { viewport: { width: 1440, height: 900 } } },
    { name: 'smal-375', use: { viewport: { width: 375, height: 812 }, hasTouch: true } },
  ],
});
