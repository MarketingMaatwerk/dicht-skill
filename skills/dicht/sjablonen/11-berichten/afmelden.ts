// Sjabloon: afmelden in een klik volgens RFC 8058: de twee koppen en het ondertekende token.
// Dekt: MSG-07, MSG-09, AUTH-57
// Dekt gedeeltelijk:
//   - MSG-07 eist dat de DKIM-handtekening beide koppen dekt (h= met list-unsubscribe en list-unsubscribe-post,
//     MSG-03). Dat regel je bij de verzendroute, niet in deze code.
//   - Het voorbeeld in MSG-07 heeft naast het HTTPS-adres ook een mailto-adres; de regel zelf vraagt precies een
//     HTTPS-adres. Dit sjabloon zet alleen het HTTPS-adres.
// Het token is een HMAC-SHA256 over ontvanger en lijst (MSG-09): het legt beide vast, is niet te raden en staat
//   nergens opgeslagen. De id's zijn onraadbare sleutels (UUID), nooit het e-mailadres of een oplopend nummer.
// Aanpassen: BASIS (uit de configuratie, nooit uit de Host-header: WEB-42) en waar het geheim vandaan komt
//   (minstens 32 bytes willekeur, uit de geheimen van de dienst: AUTH-42).
// Imports: dit bestand en de tests gebruiken de extensie .ts, zodat node ze zonder bouwstap kan draaien. Bouw je
//   met tsc (module NodeNext), schrijf dan .js of zet allowImportingTsExtensions aan.
// Controleren: node --experimental-strip-types --test afmelden.test.ts (de tests bij dit bestand slagen).
import { createHmac, timingSafeEqual } from 'node:crypto';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

function handtekening(geheim: Buffer, ontvangerId: string, lijstId: string): Buffer {
  return createHmac('sha256', geheim).update(`${ontvangerId}.${lijstId}`).digest();
}

function eisGeheim(geheim: Buffer): void {
  if (geheim.length < 32) throw new Error('het afmeldgeheim is korter dan 32 bytes');
}

export function maakAfmeldToken(geheim: Buffer, ontvangerId: string, lijstId: string): string {
  eisGeheim(geheim);
  if (!UUID.test(ontvangerId) || !UUID.test(lijstId)) throw new Error('ongeldig id');
  return `${ontvangerId}.${lijstId}.${handtekening(geheim, ontvangerId, lijstId).toString('base64url')}`;
}

// Geeft ontvanger en lijst terug, of null bij elk token dat niet klopt. Vergelijkt in constante tijd.
export function leesAfmeldToken(geheim: Buffer, token: string): { ontvangerId: string; lijstId: string } | null {
  eisGeheim(geheim);
  const delen = token.split('.');
  if (delen.length !== 3) return null;
  const [ontvangerId, lijstId, mac] = delen as [string, string, string];
  if (!UUID.test(ontvangerId) || !UUID.test(lijstId)) return null;
  const verwacht = handtekening(geheim, ontvangerId, lijstId);
  const gekregen = Buffer.from(mac, 'base64url');
  if (gekregen.length !== verwacht.length || !timingSafeEqual(gekregen, verwacht)) return null;
  return { ontvangerId, lijstId };
}

// De twee koppen voor elke nieuwsbrief en elke reclamemail (MSG-07).
export function maakAfmeldKoppen(basis: string, token: string): Record<string, string> {
  const adres = new URL(`/afmelden/${token}`, basis);
  if (adres.protocol !== 'https:') throw new Error('het afmeldadres moet https zijn');
  return {
    'List-Unsubscribe': `<${adres.href}>`,
    'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click',
  };
}
