// Tests bij afmelden.ts. Draaien: node --experimental-strip-types --test afmelden.test.ts
// Dekt: MSG-07, MSG-09
import assert from 'node:assert/strict';
import { randomBytes, randomUUID } from 'node:crypto';
import { test } from 'node:test';
import { leesAfmeldToken, maakAfmeldKoppen, maakAfmeldToken } from './afmelden.ts';

const geheim = randomBytes(32);
const ontvanger = randomUUID();
const lijst = randomUUID();

test('een geldig token geeft ontvanger en lijst terug', () => {
  const token = maakAfmeldToken(geheim, ontvanger, lijst);
  assert.deepEqual(leesAfmeldToken(geheim, token), { ontvangerId: ontvanger, lijstId: lijst });
});

test('een gewijzigd token, een andere ontvanger of een andere lijst wordt geweigerd', () => {
  const token = maakAfmeldToken(geheim, ontvanger, lijst);
  const [o, l, mac] = token.split('.') as [string, string, string];
  assert.equal(leesAfmeldToken(geheim, `${randomUUID()}.${l}.${mac}`), null);
  assert.equal(leesAfmeldToken(geheim, `${o}.${randomUUID()}.${mac}`), null);
  assert.equal(leesAfmeldToken(geheim, `${o}.${l}.${mac.slice(0, -2)}AA`), null);
  assert.equal(leesAfmeldToken(geheim, `${o}.${l}`), null);
  assert.equal(leesAfmeldToken(geheim, ''), null);
  assert.equal(leesAfmeldToken(randomBytes(32), token), null);
});

test('het token bevat geen e-mailadres en de koppen hebben precies een https-adres', () => {
  const token = maakAfmeldToken(geheim, ontvanger, lijst);
  assert.ok(!token.includes('@'));
  const koppen = maakAfmeldKoppen('https://mail.voorbeeld.nl', token);
  assert.equal(koppen['List-Unsubscribe'], `<https://mail.voorbeeld.nl/afmelden/${token}>`);
  assert.equal(koppen['List-Unsubscribe-Post'], 'List-Unsubscribe=One-Click');
  assert.throws(() => maakAfmeldKoppen('http://mail.voorbeeld.nl', token));
});

test('een te kort geheim wordt geweigerd', () => {
  assert.throws(() => maakAfmeldToken(randomBytes(8), ontvanger, lijst));
});
