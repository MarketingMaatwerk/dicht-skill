// Sjabloon: Vitest-configuratie.
// Dekt: ARCH-45, ARCH-50 (via tests/opzet.ts), ARCH-12 (samen met TZ=UTC in het testscript)
// Aanpassen: de drempels. ARCH-45 vraagt drempels "op het huidige niveau": meet eerst de dekking en vul die
//   getallen in. De nullen hieronder zijn een lege plek, geen keuze; met nul faalt er nooit iets.
// Het testscript in package.json zet de tijdzone: "test": "TZ=UTC vitest run" (ARCH-12).
// Controleren (ARCH-45): een proef met een tijdelijk verhoogde drempel maakt de gate rood.
// Gevalideerd op 04-10-2026 met Vitest 5.0.3 (wegwerpcontainer): de configuratie laadt en vitest list toont de
//   tests. De tests zelf zijn niet gedraaid (ze vragen de functies en de database van het eigen project).
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['tests/**/*.test.ts', 'src/**/*.test.ts'],
    setupFiles: ['tests/opzet.ts'],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts'],
      thresholds: { lines: 0, branches: 0, functions: 0 },
    },
  },
});
