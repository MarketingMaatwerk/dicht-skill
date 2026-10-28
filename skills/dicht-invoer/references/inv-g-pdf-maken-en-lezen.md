# INV G: PDF maken en lezen

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-35 Behandel HTML voor een PDF als code die in een browser op de server draait
kritiek · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Codeer elke waarde van buiten in het HTML-sjabloon van een PDF (Zie WEB-01), zet JavaScript in de pagina uit met `page.setJavaScriptEnabled(false)`, blokkeer met `page.setRequestInterception(true)` elke aanvraag die niet naar een eigen, vaste bron gaat, en laad het sjabloon met `page.setContent()` in plaats van via een URL uit invoer.
- Bewijs: Test met een veldwaarde `<iframe src="http://127.0.0.1:1/"></iframe><script>document.title='X'</script><img src="http://127.0.0.1:1/x">`: de PDF toont de tekst letterlijk en een lokale testserver op die poort ziet geen aanvraag. `grep -rn "setJavaScriptEnabled\|setRequestInterception\|page.goto(" src` toont de instellingen bij elke PDF-functie. Afgevinkt met test en grep.
- Norm: ASVS 5.0.0 V1.3.6 (L2), V1.2.1 (L1), V15.2.5 (L3).
- Zie ook: WEB-01, WP-01, WP-02, WP-03, WEB-06, MSG-17, INV-25, INV-40, INV-32, INV-36, INFRA-31, INFRA-32

### INV-36 Start Chrome nooit met --no-sandbox
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai headless Chrome als een eigen gebruiker zonder rootrechten, met de sandbox aan, in een container of systemd-eenheid met minimale rechten, en gebruik `--no-sandbox` of `--disable-setuid-sandbox` nooit op inhoud die niet volledig van jezelf is.
- Bewijs: `grep -rn "no-sandbox\|disable-setuid-sandbox" .` is leeg; `ps -o user= -C chrome` (of in de container `whoami`) toont een gewone gebruiker; de Dockerfile maakt die gebruiker aan zoals in de Puppeteer-documentatie. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V15.2.5 (L3). Zie INFRA-31 en INFRA-32 voor de container zelf.
- Zie ook: INV-40, INV-32, INV-35, INFRA-31, INFRA-32

### INV-37 Gebruik wkhtmltopdf niet meer
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw geen nieuwe functie op wkhtmltopdf of op een pakket dat het aanroept, en vervang het in bestaand werk waar het HTML met invoer van buiten rendert.
- Bewijs: `which wkhtmltopdf wkhtmltoimage` is leeg op server en in images; `grep -rni "wkhtmlto" package.json composer.json Dockerfile* vendor/composer/installed.json` is leeg. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V15.2.1 (L1).

### INV-38 Houd dompdf dicht: geen externe bronnen, geen PHP in het document, een smalle chroot
hoog · hard · wp-plugin | klantproject | api · tegenlezer: scherpen (04-10-2026)
- Regel: Laat bij dompdf `isRemoteEnabled` en `isPhpEnabled` uit, zet `chroot` op alleen de map met de eigen sjablonen en lettertypen, geef gebruikers geen invloed op de opties, codeer alle invoer in de HTML, en houd dompdf op 3.1.6 of hoger; pas dezelfde lijn toe op mPDF en op plugins die een van beide meeleveren (factuur- en pakbonplugins voor WooCommerce).
- Bewijs: `composer show dompdf/dompdf` (of de versie in de map `vendor` van de plugin) toont 3.1.6 of hoger; `grep -rnE "isRemoteEnabled|isPhpEnabled|chroot|enable_remote" .` toont de waarden hierboven; test: een factuurveld met `<img src="/etc/hostname">` en `<link rel="stylesheet" href="http://127.0.0.1:1/x.css">` levert een PDF zonder die inhoud en zonder uitgaande aanvraag. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V1.3.6 (L2), V15.2.1 (L1).

### INV-39 Lees PDF's met pdf.js alleen vanaf 4.2.67 en met isEvalSupported uit
hoog · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Houd `pdfjs-dist` (ook als onderdeel van een ander pakket) op 4.2.67 of hoger en niet op 5.6.83 tot en met 6.2.107 (dus 6.2.108 of hoger op lijn 5 en 6), geef bij `getDocument()` altijd `isEvalSupported: false` mee en zet `enableScripting` uit.
- Bewijs: `npm ls pdfjs-dist` toont overal 4.2.67 of hoger en geen versie van 5.6.83 tot en met 6.2.107, ook genest; `grep -rn "getDocument(" src` toont `isEvalSupported: false`; `grep -rn "enableScripting" src` toont `false` waar de viewer wordt gebruikt. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V15.2.1 (L1), V1.3.2 (L1).

### INV-40 Verwerk PDF's, Office-bestanden en beeld van buiten in een apart proces met grenzen
middel · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat het uitlezen of omzetten van een bestand van buiten (PDF naar tekst, Office naar tekst, beeldbewerking, OCR) lopen in een worker of kindproces met een time-out, een geheugenlimiet en zonder netwerk, zodat een vastlopende of gekraakte parser de hoofddienst niet meeneemt.
- Bewijs: De verwerking draait aantoonbaar buiten het hoofdproces (`worker_threads`, `child_process` of een eigen container) met een time-out in de code en een geheugenlimiet (`resourceLimits`, `MemoryMax=` of de containerlimiet, Zie INFRA-32); test: een bestand dat de parser laat hangen wordt na de time-out afgebroken en de health-check van de dienst blijft groen. Afgevinkt met de test.
- Norm: ASVS 5.0.0 V15.2.2 (L2), V15.2.5 (L3).
- Zie ook: INV-32, INV-35, INV-36, INFRA-31, INFRA-32
