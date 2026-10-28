# INV B: JSON, querystrings en formuliervelden

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-08 Parse JSON één keer en geef het geparste object door
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat precies één parser de JSON lezen, valideer het resultaat, en geef daarna het gevalideerde object door aan de volgende laag; stuur nooit de ruwe tekst door naar een tweede systeem dat hem opnieuw parset, en weiger op paden met rechten of geld een object met dubbele sleutels.
- Bewijs: `grep -rn "rawBody\|request.raw" src` toont de ruwe body alleen bij het controleren van een handtekening (webhooks) en nooit als uitgaande body. Test op routes met rol, prijs of tenant: een body met een dubbele sleutel geeft 400, of de waarde die de controle ziet is aantoonbaar de waarde die wordt opgeslagen. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V1.5.3 (L3).

### INV-09 Stuur gehele getallen buiten het veilige bereik als tekst
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet elk ID, bedrag in centen of ander geheel getal dat groter kan worden dan 2^53 - 1 als string in JSON, en valideer getallen die wel als getal binnenkomen met `Number.isSafeInteger`.
- Bewijs: `grep -rn "z.number()" src` toont bij elk ID en elk bedrag `.int()` met een bereik binnen `Number.MAX_SAFE_INTEGER`; kolommen van het type `bigint` worden in API-antwoorden als string gezet (test: een rij met ID 9007199254740993 komt ongewijzigd terug). In PHP: `json_decode` van externe ID's met `JSON_BIGINT_AS_STRING`. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V1.4.2 (L2), V2.2.1 (L1).

### INV-10 Begrens de diepte van geneste invoer vóór eigen recursie
middel · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elk schema voor vrije of recursieve structuren (boomstructuren, filters, JSON-kolommen, blokken van een editor) een maximale diepte en controleer die vóór een eigen recursieve functie de data doorloopt.
- Bewijs: Test per route met een vrije of recursieve structuur: een body met 10000 niveaus geeft 400 binnen de normale responstijd, geen 500. In PHP blijft de `depth` van `json_decode` op 512 of lager. Afgevinkt met de test.
- Norm: ASVS 5.0.0 V2.2.1 (L1), V15.2.2 (L2).
- Zie ook: INFRA-45, API-18, WEB-43, API-19, ARCH-13, INV-44, MSG-24

### INV-11 Laat json_decode in PHP een uitzondering gooien
middel · hard · wp-plugin | wp-thema | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Roep `json_decode()` altijd aan met `JSON_THROW_ON_ERROR` en valideer daarna de vorm; vergelijk het resultaat nooit met `null` om een fout te herkennen.
- Bewijs: `grep -rn "json_decode(" --include=*.php .` toont bij elke aanroep in eigen code `JSON_THROW_ON_ERROR`; PHPStan of een eigen regel bewaakt het. Test: een ongeldige body geeft 400. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V2.2.1 (L1).

### INV-12 Gebruik geen z.coerce op invoer zonder eerst de vorm te controleren
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet een getal of boolean uit een querystring, formulier of kop om met een expliciete vormcontrole (`z.string().regex(/^[0-9]{1,9}$/).transform(Number)` of een enum `'true' | 'false'`) en niet met `z.coerce.number()` of `z.coerce.boolean()`. Dit gaat over waarden die als tekst binnenkomen; een getal in een JSON-body valideer je als getal met `.int()` en een bereik (INV-09).
- Bewijs: `grep -rn "z.coerce" src` is leeg of elke treffer heeft een voorafgaande vormcontrole; tests per getalveld met `''`, `' '`, `'1e3'`, `'0x10'` en `'-0'` geven 400. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V15.3.5 (L2), V2.2.1 (L1).

### INV-13 Dwing per parameter één waarde en één type af
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per query-, formulier- en padparameter in het schema vast of het één tekstwaarde of een lijst is, weiger de andere vorm, en lees een parameter nooit uit meer dan één bron (query, body, cookie) tegelijk.
- Bewijs: Test per route: dezelfde parameter twee keer en de variant met `[]` geven 400 waar één waarde wordt verwacht. In PHP: `grep -rnE "\\$_(GET|POST|REQUEST|COOKIE)\[" .` toont bij elke lezing een typecontrole (`is_string`) of een WordPress-functie die dat doet (Zie WP-06); `$_REQUEST` komt niet voor. Afgevinkt met test en grep.
- Norm: ASVS 5.0.0 V15.3.7 (L2), V15.3.5 (L2).
- Zie ook: AUTH-65, API-02, INV-47, INV-46, WP-32

### INV-14 Controleer in PHP dat een groot formulier volledig is aangekomen
middel · richtlijn · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur bij formulieren met veel velden (instellingenpagina's, grote WooCommerce- of Elementor-formulieren) het aantal velden mee of sluit af met een controleveld, en weiger de opslag als het ontbreekt.
- Bewijs: Voor elk formulier met meer dan enkele honderden velden: een test die 1001 velden instuurt en laat zien dat de opslag wordt geweigerd of volledig is. `php -i | grep max_input_vars` is vastgelegd in de projectdocumentatie. Afgevinkt met test en waarde.
- Norm: ASVS 5.0.0 V2.2.1 (L1).

### INV-15 Geef elk content-type dat een route aanneemt een eigen schema
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zorg dat bij een route met `schema.body.content` elk content-type dat een parser kan opleveren ook als sleutel in die `content`-kaart staat, registreer geen parser met een regex of een vangnet zonder dat, en houd Fastify op 5.12.5 of hoger.
- Bewijs: `npm ls fastify` toont 5.12.5 of hoger; `grep -rn "addContentTypeParser" src` toont alleen exacte tekstwaarden, of bij elke regex een bijbehorende sleutel in elk `content`-schema; test per schrijfroute: de ongeldige body met `Content-Type: application/json\t`, ` application/json` en `text/plain` geeft 400 of 415. Afgevinkt met de drie uitvoeren. Zie API-05 en WEB-31.
- Norm: ASVS 5.0.0 V2.2.1 (L1), V15.2.1 (L1).
- Zie ook: API-05, WEB-31
