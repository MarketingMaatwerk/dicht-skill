# INV F: SVG en afbeeldingen

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-27 Geef ImageMagick een dichte policy voordat het bestanden van buiten ziet
hoog · hard · wp-plugin | wp-thema | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat ImageMagick (ook via PHP Imagick en WordPress) alleen draaien met een policy die alleen de beeldformaten toelaat die nodig zijn (GIF, JPEG, PNG, WebP), die de coders voor PS, EPS, PDF, XPS, MVG, MSL, SVG en URL's weigert, indirect lezen via `@bestand` blokkeert en grenzen stelt aan breedte, hoogte, geheugen, schijf en tijd.
- Bewijs: `identify -list policy` (of `magick -list policy`) op de server en in de container toont de weigerregels en de grenzen; test: een bestand `test.jpg` met MVG- of PostScript-inhoud geeft een policy-fout en geen uitvoer. Op gedeelde hosting waar de policy niet te lezen of te wijzigen is: leg dat vast en gebruik GD of hercodeer buiten de hosting. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V5.2.2 (L1), V5.2.6 (L3), V15.2.5 (L3).
- Zie ook: INV-28, INV-29, INV-30, INV-32, WEB-49

### INV-28 Laat de grenzen van sharp staan en zet een tijdslimiet
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Verhoog `limitInputPixels` niet en zet het nooit op `false` of 0, gebruik `unlimited: true` nooit, laat `failOn` op `'warning'`, zet `.timeout({ seconds: n })` op elke bewerking van een bestand van buiten, lees geanimeerde bestanden alleen met een vast maximum aan `pages`, en houd sharp op de laatste versie.
- Bewijs: `grep -rnE "limitInputPixels|unlimited|failOn|animated|pages:" src` toont geen verruiming; elke `sharp(`-aanroep op een upload heeft `.timeout(`; `npm ls sharp` toont 0.35.4 of hoger; de test uit WEB-49 (30000 bij 30000 pixels) wordt geweigerd. Afgevinkt met grep, versie en test.
- Norm: ASVS 5.0.0 V5.2.6 (L3), V5.2.1 (L1), V15.2.1 (L1).
- Zie ook: INV-27, INV-29, INV-30, INV-32, WEB-49

### INV-29 Controleer in PHP de afmetingen vóór het decoderen en gebruik getimagesize niet als bewijs
middel · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Lees in PHP eerst breedte en hoogte uit de kop, weiger alles boven het vastgelegde maximum aan pixels, en decodeer dan pas met GD of Imagick; behandel `getimagesize()` nooit als controle dat het bestand een geldige afbeelding is, en zet bij Imagick grenzen met `Imagick::setResourceLimit()` als de policy van de server niet te beheren is.
- Bewijs: `grep -rnE "getimagesize\(|imagecreatefrom|readImage\(" --include=*.php .`: vóór elke decodering staat een grens op breedte maal hoogte; `getimagesize` is nergens de enige controle (in WordPress doet `wp_handle_upload` de typecontrole, Zie WP-22). Test: een afbeelding boven de grens wordt geweigerd zonder fatale fout in het log. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V5.2.6 (L3), V5.2.2 (L1).
- Zie ook: INV-28, INV-27, INV-30, INV-32, WEB-49

### INV-30 Bewaar geen locatiegegevens in foto's die anderen kunnen zien
middel · hard · website | wp-plugin | wp-thema | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Roep bij sharp nooit `keepMetadata()`, `keepExif()` of `withMetadata()` aan op een upload van een gebruiker, en verwijder op WordPress-sites waar bezoekers of klanten foto's uploaden de metadata ook uit het originele bestand.
- Bewijs: `grep -rnE "keepMetadata|keepExif|withMetadata|withExif" src` is leeg of verklaard; `exiftool -GPS* -SerialNumber <opgeslagen bestand>` op het origineel en op een verkleinde versie van een testfoto met GPS-gegevens is leeg. Afgevinkt met grep en de exiftool-uitvoer. Zie WEB-49 voor het hercoderen.
- Norm: AVG artikel 5 lid 1 onder c en artikel 25; ASVS 5.0.0 V5.2.2 (L1).
- Zie ook: INV-28, INV-27, INV-29, INV-32, WEB-49

### INV-31 Toon SVG van anderen alleen via een img-element
hoog · hard · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een SVG die niet uit de eigen repository komt alleen zien via `<img src>` of als CSS-achtergrond, zet hem nooit inline in de pagina, niet in `<object>`, `<embed>` of `<iframe>`, en lever het bestand zelf uit volgens WEB-47 zodat rechtstreeks openen geen script uitvoert.
- Bewijs: `grep -rnE "file_get_contents\([^)]*\.svg|innerHTML[^;]*svg|<object[^>]*\.svg|<embed[^>]*\.svg" .` toont alleen SVG's uit de eigen repository; `curl -sI` op een geüploade SVG toont `Content-Disposition: attachment` of `Content-Security-Policy` met `sandbox` (WEB-47). Afgevinkt met grep en curl. Zie WEB-07 en WP-23 voor het saneren of weigeren van SVG-uploads.
- Norm: ASVS 5.0.0 V1.3.4 (L2), V3.2.1 (L1).
- Zie ook: INV-32, WEB-07, WP-23, WEB-47

### INV-32 Zet SVG van anderen niet op de server om naar een rasterbeeld zonder afscherming
hoog · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Rasteriseer een SVG van een gebruiker (met sharp, ImageMagick, Inkscape of een headless browser) alleen in een proces zonder netwerk en zonder leesrechten buiten een lege werkmap, en anders niet.
- Bewijs: Per plek waar SVG wordt gerasteriseerd: de SVG staat alleen in een verse map uit INV-68, het proces heeft geen netwerk (container zonder netwerk of `PrivateNetwork=`, Zie INFRA) en een test met `<image href="file:///etc/hostname">` en `<image href="http://127.0.0.1:1/">` geeft een beeld zonder die inhoud en zonder uitgaande verbinding. Afgevinkt met de testuitvoer, of met de vaststelling dat SVG-invoer wordt geweigerd.
- Norm: ASVS 5.0.0 V1.3.4 (L2), V15.2.5 (L3).
- Zie ook: INV-28, INV-27, INV-29, INV-30, WEB-49, INV-31, WEB-07, WP-23, WEB-47, INV-40, INV-35, INV-36, INFRA-31, INFRA-32

### INV-33 Behandel magic bytes als een hint en parse het bestand volledig
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik herkenning op de eerste bytes (`file-type`, `finfo`) alleen om vroeg te weigeren, en bewijs het type door het bestand volledig te parsen of opnieuw te coderen met de bibliotheek voor dat type; behandel elk formaat zonder magic bytes (SVG, HTML, CSV, tekst, JSON) als tekst die via de parser voor dat formaat moet.
- Bewijs: Per uploadfunctie staat vast welke bibliotheek het bestand volledig leest of hercodeert (sharp of GD voor beeld, de PDF-lezer uit INV-40, de CSV-parser uit INV-20); test: een GIF-kop met PHP-inhoud en een JPEG-kop gevolgd door HTML worden geweigerd of komen hercodeerd terug zonder de extra inhoud (`grep -c "<?php"` op het opgeslagen bestand is 0). Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V5.2.2 (L1).
- Zie ook: WEB-44, WEB-43, WEB-46, API-60, WP-22, WP-23, WP-24, INV-65, MSG-25

### INV-34 Geef PHP-bestandsfuncties nooit een pad met een schema uit invoer
hoog · hard · wp-plugin | wp-thema | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Weiger in PHP elke waarde met `://` (en dus `phar://`, `php://`, `data://`, `http://`, `ftp://`) voordat die bij `file_get_contents`, `fopen`, `file_exists`, `getimagesize`, `copy`, `include` of een bibliotheek die daarop leunt terechtkomt, en haal URL's alleen op via de functies uit WP-28 of WEB-40.
- Bewijs: `grep -rnE "(file_get_contents|fopen|file_exists|is_file|getimagesize|copy|readfile)\(\s*\\$_(GET|POST|REQUEST|COOKIE)" --include=*.php .` is leeg; elke bestandsfunctie met een variabel pad krijgt een pad dat de code zelf heeft samengesteld (API-54, WP-25); test: de waarden `phar://x`, `php://filter/resource=wp-config.php` en `http://127.0.0.1/` worden geweigerd. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V5.3.2 (L1), V1.3.6 (L2).
- Zie ook: API-54, AI-46, WP-25, API-76, WEB-45, WP-29, INV-41, SCR-15, INV-60, WP-27, WP-28
