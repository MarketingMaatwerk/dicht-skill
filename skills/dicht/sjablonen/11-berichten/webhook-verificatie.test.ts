// Tests bij webhook-verificatie.ts. Draaien: node --experimental-strip-types --test webhook-verificatie.test.ts
// Dekt: MSG-43, MSG-39, MSG-36, MSG-35
// De gevallen volgen het bewijs uit de regels: vier verzoeken voor Slack, drie voor Meta met tekens buiten ASCII.
import assert from 'node:assert/strict';
import { createHmac, generateKeyPairSync, sign } from 'node:crypto';
import { test } from 'node:test';
import { controleerDiscord, controleerMeta, controleerSlack, metaChallenge } from './webhook-verificatie.ts';

const body = Buffer.from('{"tekst":"café € 5","type":1}', 'utf8');

test('Slack: geldig, verkeerde handtekening, tien minuten oud, geen koppen (MSG-43)', () => {
  const geheim = 'testgeheim-alleen-voor-deze-test';
  const nu = 1_800_000_000;
  const teken = (ts: number) => `v0=${createHmac('sha256', geheim).update(`v0:${String(ts)}:`).update(body).digest('hex')}`;
  assert.equal(controleerSlack(geheim, body, teken(nu), String(nu), nu), true);
  assert.equal(controleerSlack(geheim, body, `v0=${'0'.repeat(64)}`, String(nu), nu), false);
  assert.equal(controleerSlack(geheim, body, teken(nu - 600), String(nu - 600), nu), false);
  assert.equal(controleerSlack(geheim, body, undefined, undefined, nu), false);
  assert.equal(controleerSlack(geheim, Buffer.from('{"type":2}'), teken(nu), String(nu), nu), false);
});

test('Discord: geldig, gewijzigde body, onzin in de kop (MSG-39)', () => {
  const { publicKey, privateKey } = generateKeyPairSync('ed25519');
  const sleutelHex = publicKey.export({ format: 'der', type: 'spki' }).subarray(-32).toString('hex');
  const ts = '1800000000';
  const handtekening = sign(null, Buffer.concat([Buffer.from(ts), body]), privateKey).toString('hex');
  assert.equal(controleerDiscord(sleutelHex, body, handtekening, ts), true);
  assert.equal(controleerDiscord(sleutelHex, Buffer.from('{"type":1}'), handtekening, ts), false);
  assert.equal(controleerDiscord(sleutelHex, body, handtekening, '1'), false);
  assert.equal(controleerDiscord(sleutelHex, body, '00', '1'), false);
  assert.equal(controleerDiscord(sleutelHex, body, undefined, undefined), false);
});

test('Meta: geldige handtekening, geen kop, gewijzigde body (MSG-36)', () => {
  const geheim = 'testgeheim-alleen-voor-deze-test';
  const kop = `sha256=${createHmac('sha256', geheim).update(body).digest('hex')}`;
  assert.equal(controleerMeta(geheim, body, kop), true);
  assert.equal(controleerMeta(geheim, body, undefined), false);
  assert.equal(controleerMeta(geheim, Buffer.from('{"tekst":"cafe"}'), kop), false);
});

test('Meta: de challenge alleen bij het juiste token (MSG-35)', () => {
  assert.equal(metaChallenge('goed', { 'hub.mode': 'subscribe', 'hub.verify_token': 'goed', 'hub.challenge': '1' }), '1');
  assert.equal(metaChallenge('goed', { 'hub.mode': 'subscribe', 'hub.verify_token': 'fout', 'hub.challenge': '1' }), null);
  assert.equal(metaChallenge('goed', { 'hub.mode': 'iets', 'hub.verify_token': 'goed', 'hub.challenge': '1' }), null);
  assert.equal(metaChallenge('goed', {}), null);
});
