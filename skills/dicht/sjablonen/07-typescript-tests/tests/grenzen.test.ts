// Sjabloon: de vaste tabel van grensgevallen voor geld en tijd, als geparametriseerde test (negatieve tests).
// Dekt: BIZ-52, API-35, BIZ-10, BIZ-11, BIZ-12, BIZ-26, ARCH-38 (invoer-as), ARCH-34
// Dekt gedeeltelijk: BIZ-52 bevat ook de rijen korting (BIZ-33), zomertijd (BIZ-29), jaarwissel (BIZ-27), grens
//   van een periode (BIZ-28) en verlopen (BIZ-25). Die hangen aan functies van het eigen project en staan
//   hieronder als it.todo, zodat ze in de testuitvoer zichtbaar openstaan.
// Aanpassen: de import. De vijf functies zijn die van het eigen project; de namen en vormen hieronder zijn een
//   voorbeeld. Bedragen zijn hele centen (API-28, DB-75). Vul de tabel aan met de grenzen van het project.
//   De invoer en de verwachte uitkomst van elke rij komen letterlijk uit de tabel in BIZ-52.
// Vaste klok (BIZ-52): vi.useFakeTimers met setSystemTime in tests die van "nu" afhangen.
// Controleren: de test draait in de gate; voor betaling, login en tenant-isolatie geldt daarbovenop de
//   mutatiedrempel van 80 procent (ARCH-44, besluit 21, stryker.config.json).
// Gevalideerd op 04-10-2026 met Vitest 5.0.3 (wegwerpcontainer): vitest list toont de tests. Niet gedraaid: de
//   vijf functies zijn van het eigen project.
import { describe, expect, it } from 'vitest';
import { berekenTotaal, naarCenten, plusMaanden, rondAfOpCenten, verdeel } from '../src/modules/billing';

describe('btw afronden (BIZ-10)', () => {
  // btw-bedrag 20,124 en 20,125 worden 20,12 en 20,13. Invoer in duizendsten van een euro.
  it.each([
    [20124n, 2012n],
    [20125n, 2013n],
  ])('%s duizendsten wordt %s centen', (duizendsten, centen) => {
    expect(rondAfOpCenten(duizendsten)).toBe(centen);
  });
});

describe('geen floats (BIZ-11)', () => {
  // 1,005 en 2,675 afronden op centen geeft 1,01 en 2,68; 19,99 maal 100 is 1999.
  // naarCenten leest de tekst als decimaal getal, zonder tussenstap via een JavaScript-getal.
  it.each([
    ['1.005', 101n],
    ['2.675', 268n],
    ['19.99', 1999n],
  ])('%s wordt %s centen', (tekst, centen) => {
    expect(naarCenten(tekst)).toBe(centen);
  });
});

describe('verdelen (BIZ-12)', () => {
  // 100,00 over 3 is 33,34 + 33,33 + 33,33; 0,05 over 3 is 0,02 + 0,02 + 0,01. De delen zijn samen het totaal.
  it.each([
    [10000n, 3, [3334n, 3333n, 3333n]],
    [5n, 3, [2n, 2n, 1n]],
  ])('%s centen over %s', (totaal, aantal, delen) => {
    expect(verdeel(totaal, aantal)).toEqual(delen);
    expect(verdeel(totaal, aantal).reduce((som, deel) => som + deel, 0n)).toBe(totaal);
  });
});

describe('grenzen van aantallen (API-35)', () => {
  // aantal 0, -1, 1,5 en maximum plus een worden geweigerd.
  const MAXIMUM = 100; // het maximum uit het schema van het eigen project
  it.each([0, -1, 1.5, MAXIMUM + 1])('aantal %s wordt geweigerd', (aantal) => {
    expect(() => berekenTotaal({ prijsInCenten: 999n, aantal })).toThrow();
  });

  it('een totaal van nul wordt geweigerd; gratis loopt alleen via het eigen pad (BIZ-19)', () => {
    expect(() => berekenTotaal({ prijsInCenten: 0n, aantal: 1 })).toThrow();
  });
});

describe('kalenderperiodes vanaf de ankerdatum (BIZ-26)', () => {
  it.each([
    ['2026-01-31', 1, '2026-02-28'],
    ['2026-01-31', 2, '2026-03-31'],
    ['2028-02-29', 12, '2029-02-28'],
  ])('anker %s plus %s maanden is %s', (anker, maanden, verwacht) => {
    expect(plusMaanden(anker, maanden)).toBe(verwacht);
  });
});

describe('nog in te vullen uit de tabel van BIZ-52', () => {
  it.todo('btw methode: drie regels van 0,99 tegen 21 procent, overal dezelfde methode (BIZ-10)');
  it.todo('korting: twee codes, dezelfde code twee keer, 100 procent (BIZ-33)');
  it.todo('zomertijd: termijn van 14 dagen over 29-03-2026 en over 25-10-2026 (BIZ-29)');
  it.todo('jaarwissel: betaling op 01-01 om 00:30 Nederlandse tijd krijgt factuurdatum 01-01 (BIZ-27)');
  it.todo('grens van een periode: een gebeurtenis precies op het eind hoort bij de volgende periode (BIZ-28)');
  it.todo('verlopen: verloopt_op een seconde geleden met status actief wordt geweigerd (BIZ-25)');
});
