// Sjabloon: verificatie van inkomende webhooks van Slack, Discord en Meta (WhatsApp Business), over de ruwe body.
// Dekt: MSG-43, MSG-39, MSG-36, MSG-35, AUTH-58, AUTH-57
// Dekt gedeeltelijk:
//   - Herhaling en dubbele verwerking (AUTH-59, MSG-37, MSG-44): leg het bericht-ID of event_id vast met een
//     unieke index voordat je iets doet (zie 08-api/migraties/idempotentie.sql en DB-68). Dat zit niet in deze
//     functies.
//   - Tijdig antwoorden (MSG-44: Slack binnen drie seconden) hoort in de handler: bevestigen, dan het werk in
//     een wachtrij.
// De ruwe body: elke functie krijgt de bytes zoals ze binnenkwamen, niet een opnieuw geserialiseerd object
//   (AUTH-58). In Fastify: een eigen content-type-parser met parseAs: 'buffer' op de webhookroute.
// Elke functie faalt gesloten (API-12): ontbreekt een kop of klopt er iets niet, dan is de uitkomst false en
//   verwerkt de handler niets (Slack en Meta: 401 of 403; Discord: 401).
// Aanpassen: niets aan de functies; de geheimen komen uit de configuratie van de dienst, nooit uit de code.
//   De vijf minuten voor Slack komen uit MSG-43.
// Controleren: node --experimental-strip-types --test webhook-verificatie.test.ts (de tests bij dit bestand).
import { createHmac, createPublicKey, timingSafeEqual, verify } from 'node:crypto';

function gelijk(a: Buffer, b: Buffer): boolean {
  return a.length === b.length && timingSafeEqual(a, b);
}

// Slack (MSG-43): v0= plus HMAC-SHA256 van "v0:<tijdstempel>:<ruwe body>" met het signing secret; een verzoek
// dat meer dan vijf minuten afwijkt wordt geweigerd. Het oude verificatietoken in de body gebruik je niet.
export function controleerSlack(
  signingSecret: string,
  ruweBody: Buffer,
  handtekening: string | undefined,
  tijdstempel: string | undefined,
  nuInSeconden: number = Math.floor(Date.now() / 1000),
): boolean {
  if (handtekening === undefined || tijdstempel === undefined || !/^\d{1,12}$/.test(tijdstempel)) return false;
  if (Math.abs(nuInSeconden - Number(tijdstempel)) > 5 * 60) return false;
  const mac = createHmac('sha256', signingSecret).update(`v0:${tijdstempel}:`).update(ruweBody).digest('hex');
  return gelijk(Buffer.from(`v0=${mac}`), Buffer.from(handtekening));
}

// Discord (MSG-39): Ed25519-handtekening uit X-Signature-Ed25519 over X-Signature-Timestamp plus de ruwe body,
// met de publieke sleutel van de app (hex, 32 bytes). Klopt hij niet: 401.
export function controleerDiscord(
  publiekeSleutelHex: string,
  ruweBody: Buffer,
  handtekeningHex: string | undefined,
  tijdstempel: string | undefined,
): boolean {
  if (handtekeningHex === undefined || tijdstempel === undefined) return false;
  if (!/^[0-9a-f]{64}$/i.test(publiekeSleutelHex) || !/^[0-9a-f]{128}$/i.test(handtekeningHex)) return false;
  // Een kale Ed25519-sleutel van 32 bytes in de DER-vorm (SubjectPublicKeyInfo) die node verwacht.
  const sleutel = createPublicKey({
    key: Buffer.concat([Buffer.from('302a300506032b6570032100', 'hex'), Buffer.from(publiekeSleutelHex, 'hex')]),
    format: 'der',
    type: 'spki',
  });
  return verify(null, Buffer.concat([Buffer.from(tijdstempel), ruweBody]), sleutel, Buffer.from(handtekeningHex, 'hex'));
}

// Meta, WhatsApp Business (MSG-36): HMAC-SHA256 over de ruwe bytes met het app-geheim, vergeleken met de waarde
// na "sha256=" in X-Hub-Signature-256.
export function controleerMeta(appGeheim: string, ruweBody: Buffer, kop: string | undefined): boolean {
  if (kop === undefined || !kop.startsWith('sha256=')) return false;
  const mac = createHmac('sha256', appGeheim).update(ruweBody).digest('hex');
  return gelijk(Buffer.from(mac), Buffer.from(kop.slice('sha256='.length)));
}

// Meta, het verificatieverzoek (MSG-35): geef hub.challenge alleen terug bij hub.mode=subscribe en het juiste
// token (in constante tijd). De handler stuurt de waarde als text/plain, anders 403.
export function metaChallenge(
  eigenToken: string,
  query: { 'hub.mode'?: string; 'hub.verify_token'?: string; 'hub.challenge'?: string },
): string | null {
  const token = query['hub.verify_token'];
  const challenge = query['hub.challenge'];
  if (query['hub.mode'] !== 'subscribe' || token === undefined || challenge === undefined) return null;
  return gelijk(Buffer.from(token), Buffer.from(eigenToken)) ? challenge : null;
}
