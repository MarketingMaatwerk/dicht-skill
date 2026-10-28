# INV A: XML

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-01 Zet in PHP geen parservlag die entiteiten of DTD's laadt
kritiek · hard · wp-plugin | wp-thema | api | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Geef aan `DOMDocument`, `simplexml_load_*` en `XMLReader` nooit `LIBXML_NOENT`, `LIBXML_DTDLOAD`, `LIBXML_DTDVALID`, `LIBXML_DTDATTR`, `LIBXML_XINCLUDE` of `LIBXML_PARSEHUGE` mee voor XML die van buiten komt.
- Bewijs: `grep -rnE "LIBXML_(NOENT|DTDLOAD|DTDVALID|DTDATTR|XINCLUDE|PARSEHUGE)" --include=*.php .` is leeg of elke treffer leest alleen een eigen, vast bestand. Test: een document met een externe entiteit naar `/etc/hostname` geeft uitvoer zonder de hostnaam. Afgevinkt met grep en testuitvoer.
- Norm: ASVS 5.0.0 V1.5.1 (L1); OWASP Top 10 2025 A02 (Security Misconfiguration, CWE-611).

### INV-02 Leg in PHP een entiteit-lader vast die niets laadt, en reken niet op de globale stand
hoog · hard · wp-plugin | wp-thema | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Roep in code die XML van buiten leest vóór het parsen `libxml_set_external_entity_loader(fn () => null)` aan, draai op een PHP-versie met de fix voor CVE-2023-3823, en gebruik `libxml_disable_entity_loader()` niet meer.
- Bewijs: `php -v` toont 8.1.22, 8.2.8 of hoger (Zie GIT-93 en WP-52 voor ondersteunde lijnen); `grep -rn "libxml_disable_entity_loader" .` is leeg in eigen code; `grep -rn "libxml_set_external_entity_loader" .` toont de callback bij elke plek die XML van buiten leest. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V1.5.1 (L1).

### INV-03 Zet in fast-xml-parser entiteiten uit voor XML van buiten en blijf op een gerepareerde versie
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak de parser voor XML van buiten aan met `processEntities: false` en houd fast-xml-parser op 5.10.1 of hoger (lijn 4: 4.5.7 of hoger).
- Bewijs: `npm ls fast-xml-parser` toont 5.10.1 of hoger (of 4.5.7 of hoger); `grep -rn "new XMLParser(" src` toont bij elke parser voor externe XML `processEntities: false`; een test met een document met duizend geneste entiteiten is binnen een seconde klaar en geeft de entiteit ongewijzigd terug. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V1.5.1 (L1), V15.2.1 (L1).

### INV-04 Behandel elk formaat met XML erin als XML
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Pas INV-01 tot en met INV-03 toe op elk formaat dat XML bevat: SVG, RSS en Atom, sitemaps, SOAP, SAML, XLSX, DOCX en ODT, WordPress-exportbestanden, en metadata in mediabestanden (XMP, iXML).
- Bewijs: Een lijst in de projectdocumentatie van elke plek waar zo'n formaat wordt ingelezen, met per plek de parser en zijn instelling; per plek een test met een bestand dat een DOCTYPE met entiteit bevat (voor XLSX: in `xl/workbook.xml` of `[Content_Types].xml`): geweigerd of zonder expansie verwerkt. Afgevinkt met de lijst en de testuitvoer.
- Norm: ASVS 5.0.0 V1.5.1 (L1), V5.2.2 (L1).

### INV-05 Voer geen XSLT van gebruikers uit en geef een stylesheet geen PHP-functies
hoog · hard · wp-plugin | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik alleen eigen, vaste XSLT-stylesheets, roep `XSLTProcessor::registerPHPFunctions()` nooit zonder een expliciete lijst van functies aan, en zet `setSecurityPrefs()` zo dat ook lezen van bestanden en netwerk verboden is.
- Bewijs: `grep -rn "registerPHPFunctions\|XSLTProcessor\|importStylesheet" --include=*.php .`: elke stylesheet komt uit de eigen code, `registerPHPFunctions` heeft een lijst of ontbreekt, en `setSecurityPrefs` staat erbij. Afgevinkt met de grep.
- Norm: ASVS 5.0.0 V1.3.5 (L2).

### INV-06 Bouw XML met een serializer, nooit met tekst aan elkaar
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel uitgaande XML (EPP naar een registry, SOAP, sitemaps, feeds, exportbestanden) samen met een bibliotheek die tekst en attributen zelf codeert, en zet invoer nooit in een commentaar, CDATA-blok of elementnaam.
- Bewijs: `grep -rnE "<\?xml|<[a-zA-Z:]+>\\$\{|<[a-zA-Z:]+>' *\." src` toont geen XML die met template strings of concatenatie is gebouwd. Test: een waarde `a</x><y>b` en een waarde `]]>` komen gecodeerd in het uitgaande bericht (vergelijk met een XML-parser: het aantal elementen is gelijk aan dat van een bericht met gewone tekst). Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V1.2.1 (L1).

### INV-07 Zet geen invoer in een XPath-expressie
middel · hard · wp-plugin | api | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Bouw een XPath-expressie nooit met invoer; selecteer met een vaste expressie en filter daarna in code, of laat alleen waarden toe die aan een strikte allowlist (letters, cijfers, vaste lengte) voldoen; op PHP 8.4 of hoger mag een tekstwaarde ook via `DOMXPath::quote()` in de expressie.
- Bewijs: `grep -rnE "->query\(|->evaluate\(|xpath\.select\(|\.evaluate\(" .` toont geen expressie met een variabele uit een aanvraag, tenzij die door `DOMXPath::quote()` gaat of aan de allowlist is getoetst. Afgevinkt met de grep.
- Norm: ASVS 5.0.0 V1.2.7 (L2).
