// Sjabloon: e2e-test met echte klikken, op wat de gebruiker ziet, met een toegankelijkheidsscan.
// Dekt: ARCH-36, ARCH-37, ARCH-38 (presentatie-as), ARCH-46, ARCH-48, ARCH-50
// Aanpassen: de route, de labels en de verwachte teksten. Het formulier hieronder is een voorbeeld.
// Regels in dit bestand:
//   - klikken, tikken en typen alleen via locator.click(), locator.tap(), locator.fill() of page.mouse (ARCH-36);
//     nooit dispatchEvent, een click() in page.evaluate of force: true
//   - elementen op rol, label of zichtbare tekst; geen waitForTimeout (ARCH-37)
//   - controleer dat het juiste element reageerde, niet alleen dat er iets gebeurde (ARCH-36)
//   - alleen verzonnen gegevens (ARCH-48); een test die echt mailt gebruikt een adres op het eigen domein in de
//     vorm ztest-<doel>-<willekeurig>@example.com (ARCH-50) en ruimt zijn records op met exacte id's
// Controleren:
//   grep -rnE "dispatchEvent|force:\s*true|\.evaluate\([^)]*\.click\(" e2e/     is leeg (ARCH-36)
//   grep -rn "waitForTimeout" e2e/                                               is leeg (ARCH-37)
//   de run toont beide projecten (1440 en 375) en nul overtredingen van axe (ARCH-38, ARCH-46)
// Gevalideerd op 04-10-2026: typecontrole met tsc 6.0.3 en playwright test --list (1.63.0) toont de vier tests
//   in beide projecten. Niet in een browser gedraaid.
import AxeBuilder from '@axe-core/playwright';
import { randomUUID } from 'node:crypto';
import { expect, test } from './opzet';

test.describe('contactformulier', () => {
  test('versturen toont de bevestiging', async ({ page }) => {
    await page.goto('/contact');

    await page.getByLabel('Naam').fill('Testpersoon Verzonnen');
    await page.getByLabel('E-mailadres').fill(`ztest-contact-${randomUUID()}@example.com`);
    await page.getByLabel('Bericht').fill('Dit is een testbericht.');
    await page.getByRole('button', { name: 'Versturen' }).click();

    // Het juiste element reageerde: de bevestiging met deze tekst is zichtbaar.
    await expect(page.getByRole('status')).toHaveText('Bedankt, je bericht is verstuurd.');
  });

  test('leeg versturen toont de foutmelding bij het veld', async ({ page }) => {
    await page.goto('/contact');
    await page.getByRole('button', { name: 'Versturen' }).click();
    await expect(page.getByLabel('Naam')).toHaveAttribute('aria-invalid', 'true');
  });

  test('geen zijwaartse overloop', async ({ page }) => {
    await page.goto('/contact');
    const overloop = await page.evaluate(
      () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
    );
    expect(overloop).toBe(false);
  });

  test('toegankelijkheidsscan zonder overtredingen', async ({ page }) => {
    await page.goto('/contact');
    const uitkomst = await new AxeBuilder({ page }).analyze();
    expect(uitkomst.violations).toEqual([]);
  });
});
