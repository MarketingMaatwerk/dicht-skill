# INV H: archieven en compressie

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-41 Controleer elke naam in een archief voordat er een byte wordt geschreven
kritiek · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Valideer bij het uitpakken elke entrynaam (geen absoluut pad, geen `..`-segment, geen backslash, geen schijfletter), los het doelpad op en vergelijk het met de uitpakmap volgens API-54, en gebruik daarvoor de controle van de bibliotheek waar die bestaat: `yauzl` met `decodeStrings: true` (de standaard) en `tar` zonder `preservePaths`.
- Bewijs: Test per uitpakfunctie met een archief met de entries `../x`, `/tmp/x`, `a/../../x` en `..\\x`: er ontstaat geen bestand buiten de uitpakmap (`find` vóór en na) en de functie meldt een fout. `grep -rn "preservePaths\|decodeStrings" src` toont geen verruiming. `npm ls adm-zip unzipper tar yauzl` toont actuele versies. Afgevinkt met test, grep en versies.
- Norm: ASVS 5.0.0 V5.3.3 (L3), V5.3.2 (L1).
- Zie ook: API-54, AI-46, WP-25, API-76, WEB-45, WP-29, INV-34, SCR-15, INV-42, INV-43, INV-45, SCR-29, WEB-49

### INV-42 Weiger symlinks en hardlinks in een archief
hoog · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Pak uit een archief van buiten alleen gewone bestanden en mappen uit: geef `tar` een `filter` die elk entry met type `SymbolicLink` of `Link` weigert, en schrijf bij zip nooit een symlink weg op basis van de bestandsmodus in het archief.
- Bewijs: Test met een tar en een zip die een symlink naar `/etc` en daarna een bestand via die symlink bevatten: de uitpakfunctie weigert of slaat de link over en `find <doel> -type l` is leeg na afloop. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V5.2.5 (L3).
- Zie ook: INV-41, INV-43, INV-45, SCR-29, WEB-49

### INV-43 Tel uitgepakte bytes en entries tijdens het uitpakken en pak niet genest uit
hoog · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per uitpakfunctie een maximum vast voor het totaal aan uitgepakte bytes, de grootte per bestand en het aantal entries, tel de bytes mee terwijl de stream loopt en breek af bij overschrijding, en pak een archief in een archief nooit automatisch uit.
- Bewijs: De grenzen staan in de projectdocumentatie (ASVS V5.1.1 vraagt de maximale uitgepakte grootte per uploadfunctie). Tests: een archief dat uitgepakt boven de grens komt, een archief met meer entries dan toegestaan en een zip in een zip: de eerste twee worden afgebroken en opgeruimd, de binnenste zip blijft een bestand. `df` vóór en na de test laat geen blijvende groei zien. Afgevinkt met de testuitvoer. Zie WEB-49.
- Norm: ASVS 5.0.0 V5.2.3 (L2), V5.1.1 (L2), V5.2.4 (L3).
- Zie ook: INV-41, INV-42, INV-45, SCR-29, WEB-49

### INV-44 Begrens gedecomprimeerde omvang van aanvragen en antwoorden
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Accepteer geen aanvraag met `Content-Encoding` tenzij de route daarvoor gemaakt is, geef elke eigen decompressie met `node:zlib` een `maxOutputLength`, en tel bij het lezen van een antwoord van een externe dienst de bytes na decompressie in plaats van op `Content-Length` te vertrouwen.
- Bewijs: `grep -rnE "gunzip|inflate|brotliDecompress|unzipSync" src` toont bij elke aanroep `maxOutputLength`; `grep -rnE "\.(text|json|arrayBuffer)\(\)" src` toont bij antwoorden van adressen die anderen opgeven een tellende lezer; test: een aanvraag met `Content-Encoding: gzip` geeft 415 of 400 op routes die het niet verwachten, en een antwoord dat uitgepakt boven de grens komt wordt afgebroken. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V5.2.3 (L2), V15.2.2 (L2).
- Zie ook: INFRA-45, API-18, WEB-43, API-19, ARCH-13, INV-10, MSG-24

### INV-45 Pak in WordPress uit met unzip_file en niet met een eigen ZipArchive-lus
middel · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik in een plugin of thema `unzip_file()` (na `WP_Filesystem()`) om een archief uit te pakken, naar een eigen map uit WP-29, en controleer daarna zelf type en aantal van de uitgepakte bestanden.
- Bewijs: `grep -rnE "ZipArchive|PharData|extractTo\(|gzopen\(" --include=*.php .` is leeg in eigen code of verklaard; na het uitpakken loopt de code de bestanden langs tegen een allowlist van extensies en verwijdert de rest; test met een zip met `../x.php` en `shell.php`: geen van beide bestaat na afloop als uitvoerbaar bestand. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V5.3.3 (L3), V5.2.3 (L2), V5.3.1 (L1).
- Zie ook: INV-41, INV-42, INV-43, SCR-29, WEB-49
