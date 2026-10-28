# INV K: Unicode

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-51 Maak identifiers canoniek met één functie die bij herhaling niets meer verandert
hoog · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Breng elke identifier waarop je vergelijkt (gebruikersnaam, e-mailadres, slug, subdomein, kortingscode, tenantnaam) met één gedeelde functie naar een canonieke vorm, gebruik die functie bij registratie, inloggen, reset en zoeken, leg de unieke index op de canonieke vorm, en bewijs met een test dat de functie idempotent is: `f(f(x)) === f(x)`.
- Bewijs: Eén functie in de code (`grep -rn "normalize(" src` toont alleen die plek); een unieke index op de kolom met de canonieke vorm (`\d <tabel>`); de idempotentietest en een test die `ᴮᴵᴳᴮᴵᴿᴰ` registreert terwijl `bigbird` bestaat (geweigerd als bestaand) zijn groen. Voor identifiers die geen Unicode nodig hebben (slug, subdomein, code): een schema met alleen `[a-z0-9-]`. Afgevinkt met grep, index en tests. Zie API-07 voor de volgorde decoderen en dan valideren.
- Norm: ASVS 5.0.0 V1.1.1 (L2), V1.5.3 (L3).
- Zie ook: API-07, INV-52, INV-53, INV-54, INV-57, INV-58

### INV-52 Vergelijk hoofdletterongevoelig via kleine letters, nooit via hoofdletters of de taalinstelling
middel · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor hoofdletterongevoelig vergelijken alleen de canonieke functie uit INV-51 (kleine letters, zonder taalinstelling), nooit `toUpperCase()`, `toLocaleLowerCase()` of `toLocaleUpperCase()`, en in PHP `mb_strtolower($s, 'UTF-8')` in plaats van `strtolower()` zodra de waarde meer dan ASCII kan bevatten.
- Bewijs: `grep -rnE "toUpperCase\(\)|toLocale(Lower|Upper)Case\(" src` toont geen gebruik in een vergelijking of sleutel; `grep -rn "strtolower(\|strtoupper(" --include=*.php .` toont alleen waarden die bewezen ASCII zijn; test: `ı`, `ß`, U+212A en `ﬁ` in een e-mailadres of gebruikersnaam worden geweigerd of vallen niet samen met een bestaand ASCII-account. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V1.1.1 (L2), V15.3.5 (L2).
- Zie ook: API-07, INV-51, INV-53, INV-54, INV-57, INV-58

### INV-53 Sla domeinnamen op en vergelijk ze als A-label
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet elke domeinnaam uit invoer (bestelling, DNS-record, allowlist, e-maildomein, redirect-doel) om met `url.domainToASCII()` (of in PHP `idn_to_ascii()`), weiger een leeg resultaat, sla de A-label-vorm in kleine letters op en vergelijk alleen die vorm; toon in beheerschermen en bevestigingsmails de A-label naast de leesbare vorm zodra de naam tekens buiten ASCII bevat.
- Bewijs: De kolom met domeinnamen bevat alleen waarden die aan `^[a-z0-9.-]+$` voldoen (`SELECT count(*) FROM <tabel> WHERE <kolom> !~ '^[a-z0-9.-]+$'` is 0); test: `аpple.com` wordt opgeslagen als `xn--pple-43d.com` en valt niet samen met `apple.com`; `xn--iñvalid.com` wordt geweigerd. Afgevinkt met query en test.
- Norm: ASVS 5.0.0 V1.1.1 (L2), V1.5.3 (L3).
- Zie ook: API-07, INV-51, INV-52, INV-54, INV-57, INV-58

### INV-54 Weiger of markeer namen met gemengde schriftsoorten waar de naam vertrouwen draagt
middel · richtlijn · app | api | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat in namen die anderen als herkenning gebruiken (weergavenaam van een tenant, afzendernaam, gebruikersnaam in een gedeelde omgeving) geen mengsel van schriftsoorten toe (Latijn met Cyrillisch of Grieks), of toon er een duidelijke markering bij.
- Bewijs: Een test op het schema voor zulke namen: een naam met Latijnse en Cyrillische letters door elkaar wordt geweigerd of krijgt de markering; in JavaScript te controleren met `/\p{Script=Cyrillic}/u` en `/\p{Script=Latin}/u` op dezelfde waarde. Afgevinkt met de test, of met een vastgelegde reden waarom het voor dit project niet speelt.
- Norm: ASVS 5.0.0 V2.2.1 (L1).
- Zie ook: API-07, INV-51, INV-52, INV-53, INV-57, INV-58

### INV-55 Laat de build falen op bidi-stuurtekens in broncode
hoog · hard · alles · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Zoek in elke repository vóór een merge naar de tekens U+202A tot en met U+202E en U+2066 tot en met U+2069 in broncode, configuratie en scripts, en laat de controle falen bij een treffer buiten een lijst van bewust toegestane bestanden (vertalingen).
- Bewijs: De stap staat in de CI of de hook en een testbestand met U+202E laat hem falen (getest op 04-10-2026: `grep -P` met deze klasse vindt het teken in een testbestand). Afgevinkt met de uitvoer van een run met en zonder testbestand. Zie GIT voor de plek van de gate.
- Norm: ASVS 5.0.0 V15.2.4 (L3) voor code van derden; OWASP Top 10 2025 A08 (Software or Data Integrity Failures).
- Zie ook: GIT-57, SCR-23, SCR-35

### INV-56 Weiger stuurtekens in velden van één regel
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Weiger in elk veld van één regel (naam, onderwerp, bestandsnaam, referentie, adresregel) alle stuurtekens (`\p{Cc}`, dus ook CR, LF, tab en NUL) en de bidi-stuurtekens uit INV-55; sta in meerregelige velden alleen `\n` en `\t` toe.
- Bewijs: Het gedeelde schema voor velden van één regel bevat de klasse; test met `a\r\nb`, `a\u0000b`, `a‮b` en `a\tb`: alle vier geweigerd. Afgevinkt met de test. Voor invoer die naar een model gaat: Zie AI-07.
- Norm: ASVS 5.0.0 V1.3.3 (L2), V16.4.1 (L2), V2.2.1 (L1).
- Zie ook: INV-48, WEB-68, INV-49, INV-50, MSG-04, MSG-26

### INV-57 Weiger het NUL-teken en ongeldige Unicode aan de rand
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Weiger in elk tekstveld U+0000 en tekst met losse surrogaten (`!s.isWellFormed()`), en decodeer bytes van buiten met `fatal: true` (INV-20).
- Bewijs: Test per schrijfroute (of één test op het gedeelde schema plus een lint-regel dat elk tekstveld dat schema gebruikt): `"a\u0000b"` en `"ab\uD83D"` geven 400, niet 500. Afgevinkt met de test.
- Norm: ASVS 5.0.0 V2.2.1 (L1), V1.3.3 (L2).
- Zie ook: API-07, INV-51, INV-52, INV-53, INV-54, INV-58

### INV-58 Meet lengte in de eenheid van de opslag en kap nooit stil af
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Druk elke lengtegrens uit in de eenheid die de opslag of de ontvanger gebruikt (tekens voor PostgreSQL `varchar(n)`, bytes voor een kop of een extern veld), weiger te lange invoer in plaats van hem af te kappen, en kap tekst voor weergave alleen af op een grafeemgrens met `Intl.Segmenter`.
- Bewijs: Het schema weigert te lange waarden (test: grens plus één geeft 400, en de opgeslagen waarde is nooit korter dan de ingestuurde); `grep -rnE "\.(slice|substring|substr)\(0," src` toont geen afkappen van invoer vóór opslag; voor MySQL en MariaDB (WordPress): `SELECT @@sql_mode` bevat `STRICT_TRANS_TABLES` en de tabellen zijn `utf8mb4`. Afgevinkt met test, grep en de query. Zie DB-79.
- Norm: ASVS 5.0.0 V1.3.3 (L2), V2.2.1 (L1).
- Zie ook: API-07, INV-51, INV-52, INV-53, INV-54, INV-57
