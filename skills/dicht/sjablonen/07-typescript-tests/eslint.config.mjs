// Sjabloon: ESLint met type-informatie (flat config).
// Dekt: API-68, API-69, API-70, ARCH-55, ARCH-02 (variant zonder extra hulpmiddel), ARCH-36 en ARCH-37 (als lint)
// Aanpassen:
//   - de set: strictTypeChecked voor nieuw werk, minimaal recommendedTypeChecked voor bestaand werk (API-68).
//     De strict-sets zijn volgens typescript-eslint niet stabiel onder semver: pin de versie in package.json.
//   - het patroon voor modulegrenzen als de modules niet onder src/modules/ staan (ARCH-02).
// Draaien in de gate: eslint . --max-warnings 0 (API-68).
// Controleren:
//   eslint . --max-warnings 0 is groen
//   grep -rn "eslint-disable\|@ts-ignore\|@ts-expect-error" src     elke treffer heeft een reden (API-69, ARCH-55)
//   een proef met een verboden import maakt de lint rood (ARCH-02)
// Gevalideerd op 04-10-2026 met eslint 10.12.0 en typescript-eslint 8.71.0 (wegwerpcontainer, heap 420 MB): het
//   API-skelet uit 08-api is groen; een proef met een diepe import, any en een losse promise wordt rood.
//   De e2e-regels zijn niet gedraaid (e2e/ valt buiten de tsconfig van het sjabloon).
import tseslint from 'typescript-eslint';

export default tseslint.config(
  { ignores: ['dist/', 'coverage/', 'reports/', 'playwright-report/'] },
  ...tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      // Elke promise afgehandeld (API-70). Staan al in de set; hier expliciet als fout.
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/no-misused-promises': 'error',

      // Geen any, geen ! op data van buiten (API-69).
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-non-null-assertion': 'error',

      // Onderdrukkingen: ts-ignore en ts-nocheck niet, ts-expect-error alleen met een reden (ARCH-55).
      '@typescript-eslint/ban-ts-comment': [
        'error',
        { 'ts-ignore': true, 'ts-nocheck': true, 'ts-expect-error': 'allow-with-description' },
      ],

      // Modulegrens: alleen de publieke ingang van een andere module (ARCH-02).
      'no-restricted-imports': [
        'error',
        { patterns: [{ group: ['**/modules/*/*'], message: 'Importeer alleen de ingang van een module (ARCH-02).' }] },
      ],
    },
  },
  {
    // E2e-tests: echte invoer en geen vaste wachttijden (ARCH-36, ARCH-37).
    files: ['e2e/**/*.ts'],
    rules: {
      'no-restricted-syntax': [
        'error',
        { selector: "CallExpression[callee.property.name='dispatchEvent']", message: 'Gebruik echte invoer van Playwright (ARCH-36).' },
        { selector: "CallExpression[callee.property.name='waitForTimeout']", message: 'Gebruik een wachtende controle (ARCH-37).' },
        { selector: "Property[key.name='force'][value.value=true]", message: 'Geen force: true (ARCH-36).' },
      ],
    },
  },
);
