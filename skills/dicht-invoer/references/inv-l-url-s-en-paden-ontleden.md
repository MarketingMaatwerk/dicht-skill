# INV L: URL's en paden ontleden

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-59 Ontleed een URL met één WHATWG-parser en gebruik daarna het ontlede object
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Ontleed elke URL van buiten met `new URL()` (in een `try`), neem beslissingen op `protocol`, `hostname` en `port` van dat object, geef hetzelfde object door aan de aanvraag, en gebruik nooit `url.parse()`, een reguliere expressie, `startsWith()` of `includes()` op de tekst.
- Bewijs: `grep -rnE "url\.parse\(|require\('url'\)\.parse|\.startsWith\('https?://|/\^https\?:" src` is leeg; unit-test op de controlefunctie met de zes URL's hierboven: alle zes geweigerd of naar de juiste host herleid. Afgevinkt met grep en test. Zie WEB-40 voor de adrescontrole en WEB-04 voor schema's in links.
- Norm: ASVS 5.0.0 V1.5.3 (L3), V1.3.6 (L2), V1.2.2 (L1).
- Zie ook: WEB-40, WEB-41, API-48, API-47, AI-48, WP-28, INFRA-18, INV-61, MSG-27, MSG-46

### INV-60 Neem in PHP geen beveiligingsbeslissing op parse_url
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `parse_url()` niet om te bepalen of een URL is toegestaan; gebruik in WordPress de functies uit WP-27 en WP-28, op PHP 8.5 of hoger de klasse `Uri\WhatWg\Url`, en laat in alle andere gevallen alleen een vaste lijst van volledige URL's of een ID toe.
- Bewijs: `grep -rn "parse_url(\|wp_parse_url(" --include=*.php .`: geen treffer waarvan het resultaat bepaalt of een aanvraag of redirect mag; die beslissing loopt via `wp_safe_remote_get`, `wp_safe_redirect` of een vaste lijst. Afgevinkt met de nagelopen lijst.
- Norm: ASVS 5.0.0 V1.5.3 (L3), V1.3.6 (L2).
- Zie ook: WP-27, WP-28, INV-34

### INV-61 Controleer IP-adressen met de standaardbibliotheek, niet met het pakket ip
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor de adrescontrole uit WEB-40 `net.BlockList` uit Node (of `ipaddr.js`) op het adres dat de DNS-opzoeking teruggeeft, en gebruik het npm-pakket `ip` (functies `isPublic` en `isPrivate`) en `netmask` 1.0.6 of lager nergens in een beveiligingscontrole.
- Bewijs: `grep -rnE "from 'ip'|require\('ip'\)|isPublic\(|isPrivate\(" src` is leeg; `npm ls ip netmask` toont geen gebruik in eigen code (een indirecte afhankelijkheid is beoordeeld en vastgelegd); de zes tests uit WEB-40 plus `127.1` en `::ffff:127.0.0.1` zijn groen. Afgevinkt met grep, `npm ls` en test.
- Norm: ASVS 5.0.0 V1.3.6 (L2), V15.2.1 (L1).
- Zie ook: WEB-40, WEB-41, API-48, API-47, AI-48, WP-28, INFRA-18, INV-59, MSG-27, MSG-46

### INV-62 Laat proxy en applicatie een pad op dezelfde manier lezen
middel · hard · api | app | mcp | website | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg toegangsregels in de applicatie en niet alleen op een padpatroon in nginx, laat de routeropties van Fastify (`caseSensitive`, `ignoreDuplicateSlashes`, `ignoreTrailingSlash`, `useSemicolonDelimiter`) op hun standaard, en test elke regel in nginx die een pad afschermt met de varianten van dat pad.
- Bewijs: `grep -rnE "caseSensitive|ignoreDuplicateSlashes|ignoreTrailingSlash|useSemicolonDelimiter" src` is leeg of verklaard; per afgeschermd pad in `nginx -T` een test met `/Pad`, `//pad`, `/pad/`, `/pad;x=1`, `/%70ad` en `/x/../pad`: geen variant geeft de inhoud zonder toegang; de applicatie eist zelf autorisatie op die routes (AUTH-64). Afgevinkt met grep en de curl-uitvoer.
- Norm: ASVS 5.0.0 V1.5.3 (L3).
- Zie ook: AUTH-64
