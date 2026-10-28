# ARCH F: Teststrategie

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-33 Leg per project vast welke testlaag wat bewijst
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf in `docs/TESTEN.md` per laag (unit, integratie, e2e, beveiliging, contract, property-based, fuzz, mutatie) wat die laag in dit project bewijst, met welke opdracht hij draait, hoe lang hij duurt en of hij in de gate of alleen vóór een oplevering draait; dek elke kernstroom met minstens één e2e-test en elke bedrijfsregel met tests op de laagste laag die hem kan bewijzen.
- Bewijs: Het bestand bestaat met de tabel; elke opdracht in de tabel draait en geeft exitcode 0; de lijst kernstromen (inloggen, bestellen en betalen, de belangrijkste schrijfactie, een export) heeft per stroom een e2e-test met naam. Afgevinkt met het bestand en de uitvoer.
- Norm: NIST SSDF PW.8.1; BRIEF besluit 11.

### ARCH-34 Begin elke bugfix met een test die de fout laat zien
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf bij elke fout eerst een test die faalt om precies die fout, maak hem daarna groen, en laat hem voor altijd in de suite staan; voor een beveiligingsfout geldt dit zonder uitzondering.
- Bewijs: De commit of de reeks commits van de fix bevat een test; de uitvoer van die test op de commit ervoor is rood en op de fix groen (beide in het bewijsbestand of de merge-notitie). Afgevinkt met de twee uitvoeren.
- Norm: NIST SSDF PW.8.2 voorbeeld 3; globale regel van Marketing Maatwerk ("schrijf eerst een test die de bug reproduceert").

### ARCH-35 Test code die de database raakt tegen een echte PostgreSQL
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai integratietests tegen een echte PostgreSQL van dezelfde hoofdversie als productie, met de echte migraties, de runtime-rol (niet de eigenaar of een superuser) en RLS aan; boots de database niet na met een mock of een andere engine.
- Bewijs: De testconfiguratie verbindt met een database waarvan `SELECT version()` dezelfde hoofdversie geeft als productie en `SELECT current_user, rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user` de runtime-rol toont met twee keer `f`. Afgevinkt met beide uitvoeren in de testlog.
- Norm: twaalf-factor X; NIST SSDF PW.8.2 voorbeeld 4.
- Zie ook: BIZ-50, BIZ-51, BIZ-52, ARCH-42

### ARCH-36 Bedien de pagina in e2e-tests met echte invoer
hoog · hard · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Klik, tik en typ in e2e-tests via de invoer van Playwright (`locator.click()`, `page.mouse.click(x, y)`, `locator.tap()`, `locator.fill()`), en gebruik nooit `dispatchEvent`, een `click()` vanuit `page.evaluate` of de optie `force: true` om een handeling te laten slagen.
- Bewijs: `grep -rnE "dispatchEvent|force:\s*true|\.evaluate\([^)]*\.click\(" e2e/ tests/` is leeg of elke treffer heeft een reden in een commentaarregel. Elke test controleert dat het juiste element reageerde (bijvoorbeeld de geopende titel), niet alleen dat er iets gebeurde. Afgevinkt met de grep.
- Norm: BRIEF besluit 11 ("end-to-end met echte klikken").

### ARCH-37 Schrijf e2e-tests op wat de gebruiker ziet, en laat een fout in de console de test breken
middel · richtlijn · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zoek elementen op rol, label of zichtbare tekst, gebruik de wachtende controles van Playwright (`await expect(locator).toBeVisible()`) in plaats van vaste wachttijden, test geen sites van derden, en laat elke test falen op een JavaScript-fout in de console of een mislukt verzoek naar de eigen host.
- Bewijs: `grep -rn "waitForTimeout" e2e/` is leeg; de testopzet heeft een gedeelde `page.on('pageerror')` en `page.on('console')` die bij een fout de test laat falen; de run meldt nul consolefouten. Afgevinkt met de grep en de run.
- Norm: BRIEF besluit 11.

### ARCH-38 Test elke functie langs vaste assen, niet alleen het gelukkige pad
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf voor elke functie die je oplevert tests langs minimaal deze assen: invoer (leeg, ongeldig, geldig, te lang, verkeerd type), autorisatie (niet ingelogd, eigenaar, iemand anders, verlopen of hergebruikt token), herhaling (twee keer dezelfde actie, vaker dan de limiet), toestand (geen, één, meerdere records), presentatie (1440 en 375 pixels breed, geen zijwaartse overloop), taal (elke taal van de site) en cache (een persoonlijke pagina geeft geen treffer uit de gedeelde cache).
- Bewijs: Per functie een tabel in de testbeschrijving of het bewijsbestand met per as de testnaam of "niet van toepassing, want ..."; de e2e-run toont beide schermbreedtes. Afgevinkt als geen as leeg is zonder reden. De asvolgorde komt uit de eigen regel van Marketing Maatwerk; de autorisatie-as is dezelfde als AUTH-66.
- Norm: ASVS 5.0.0 V2.2.1 (L1), V2.3.1 (L1), V8.2.2 (L1); BRIEF besluit 11.

### ARCH-39 Houd tests onafhankelijk en behandel een wankele test als een fout
middel · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke test zijn eigen gegevens aanmaken en opruimen zodat hij los en in willekeurige volgorde slaagt, zet het aantal herhalingen lokaal op nul, en behandel een test die pas na een herhaling slaagt als een openstaande fout met een eigenaar, niet als groen.
- Bewijs: De e2e-suite slaagt met `--workers=1` en in de standaard parallelle stand; de configuratie heeft `retries: 0` lokaal en hooguit een klein aantal in CI; de run meldt nul tests met de status "flaky", of elke wankele test staat in het schuldregister (ARCH-32). Afgevinkt met de uitvoer.
- Norm: NIST SSDF PW.8.2.

### ARCH-40 Draai de beveiligingstests in de gate en nog een keer vlak voor de uitrol
kritiek · hard · api | app | mcp · tegenlezer: scherpen (04-10-2026)
- Regel: Neem de autorisatiematrix (AUTH-66), de isolatietests met twee tenants (AUTH-77, DB-22, AI-53), de payloadtests (WEB-01, WP-01) en de foutpadtests (API-11) op als gewone tests in de gate, laat het uitrolscript de isolatietest en de bijbehorende metatest opnieuw draaien tegen de te starten build, en laat de uitrol stoppen bij een fout.
- Bewijs: De gate-opdracht (GIT-58) bevat de vier testgroepen; het uitrolscript bevat de isolatietest vóór de herstart; de metatest vergelijkt de tabellen met `tenant_id` en de geregistreerde routes met wat getest wordt en faalt bij een ontbrekende; het overslaan is alleen mogelijk als vastgelegde uitzondering (ARCH-30). Afgevinkt met de uitvoer van de laatste uitrol.
- Norm: ASVS 5.0.0 V8.4.1 (L2), V8.2.2 (L1); NIST SSDF PW.8.2 voorbeeld 1 en 2.
- Zie ook: DB-22, AUTH-77, AUTH-66, AI-53, GIT-57, GIT-58, GIT-59, API-67, API-68, API-78, WP-37, ARCH-56, GIT-60, GIT-61, GIT-34, AI-85

### ARCH-41 Bewijs met een contracttest dat elke respons aan zijn schema voldoet
middel · richtlijn · api | mcp | app · tegenlezer: scherpen (04-10-2026)
- Regel: Leg het contract van elke route, elke webhook en elke MCP-tool vast als schema (zod of OpenAPI, één bron volgens API-08), en draai een test die voor elke route de echte respons, ook de foutrespons, tegen dat schema valideert en faalt op een onbekend veld.
- Bewijs: Een test loopt de geregistreerde routes af en valideert status, kopregels en inhoud tegen het schema; de test faalt als een route geen schema heeft. Voor een OpenAPI-document kan Schemathesis de invoer genereren en de respons toetsen. Afgevinkt met de testuitvoer en het aantal routes.
- Norm: ASVS 5.0.0 V15.3.1 (L1, alleen de benodigde velden teruggeven).

### ARCH-42 Test kritieke logica met eigenschappen in plaats van alleen voorbeelden
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf voor elke kritieke rekenregel, parser en statusmachine (prijs en btw, kortingen, tegoed, de betaalstatus, een tenantfilter, een eigen codering of ontleding) minstens één property-based test die een eigenschap bewijst voor willekeurige invoer, en leg de seed van een gevonden fout vast als vaste regressietest.
- Bewijs: De lijst van kritieke modules in `docs/TESTEN.md` noemt per module de property-based test; de run toont dat ze draaien; een eerder gevonden tegenvoorbeeld staat als vaste test met de seed in het commentaar. Afgevinkt met lijst en uitvoer.
- Norm: BRIEF besluit 11; ASVS 5.0.0 V2.3.2 (L2).
- Zie ook: BIZ-50, BIZ-51, BIZ-52, ARCH-35

### ARCH-43 Fuzz elke parser van niet-vertrouwde invoer en de API als geheel
middel · richtlijn · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai voor elke eigen parser of omzetter van niet-vertrouwde invoer (mail en MIME, csv-import, eigen bestandsformaten, webhook-inhoud, sjablonen) een fuzzer met een tijdslimiet, en draai voor elke API met een schema een op het schema gebaseerde fuzzer tegen de testomgeving; voor kritieke delen is dit hard.
- Bewijs: Per parser een fuzzdoel in de repository en de uitvoer van een run van vaste duur zonder crash of time-out; gevonden invoer staat als regressietest in de suite; voor de API het rapport van de schemafuzzer met nul antwoorden in de 500-reeks. Afgevinkt met de uitvoeren en de datum. De duur per run is een eigen keuze (voorstel: tien minuten vóór een oplevering).
- Norm: NIST SSDF PW.8.2 voorbeeld 5; BRIEF besluit 11.

### ARCH-44 Meet met mutatietests of de tests van kritieke modules iets bewijzen
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: scherpen (04-10-2026)
- Regel: Draai op de kritieke modules een mutatietest (StrykerJS voor TypeScript, Infection voor PHP) met een drempel van minstens 80 procent gedode mutanten waaronder de opdracht faalt (besluit 21), vóór elke oplevering die zo'n module raakt; draai hem op gewijzigde regels om de duur te beperken.
- Bewijs: De configuratie noemt de kritieke modules en een `break`-drempel (Stryker: onder `break` eindigt de opdracht met exitcode 1; de standaard is `null`, dus zonder instelling faalt er nooit iets); voor PHP `infection --min-msi=<n>`, met `--git-diff-lines` voor alleen gewijzigde regels. Het rapport met de score zit in het bewijsbestand. Afgevinkt met configuratie en rapport. De hoogte van de drempel is vastgelegd in besluit 21 van de brief: minstens 80 procent gedode mutanten. Vaste waarde: Stryker `thresholds.break: 80`, Infection `--min-msi=80`.
- Norm: BRIEF besluit 11.

### ARCH-45 Zet een dekkingsdrempel die niet mag dalen en lees hem niet als kwaliteit
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Meet de dekking in de gate en zet drempels voor regels, takken en functies op het huidige niveau, zodat een wijziging de dekking niet kan verlagen; gebruik dekking om ongeteste code te vinden, niet als bewijs dat de tests goed zijn.
- Bewijs: `vitest.config.ts` bevat `coverage.thresholds` met getallen voor `lines`, `branches` en `functions`; de gate draait met dekking en faalt eronder (een proef met een tijdelijk verhoogde drempel maakt de gate rood). Afgevinkt met configuratie en uitvoer.
- Norm: BRIEF besluit 10.

### ARCH-46 Neem een toegankelijkheidsscan op in de e2e-tests
middel · richtlijn · website | wp-thema | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai in de e2e-suite op elk paginatype en op elke toestand met een formulier of dialoog een scan met `@axe-core/playwright`, laat de test falen op een overtreding, en doe daarnaast een handmatige controle met toetsenbord en schermlezer op de kernstromen. Voor een nieuwe website, webshop of app is dezelfde scan in de gate hard (PRIV-66); deze regel is richtlijn voor de rest.
- Bewijs: De e2e-run bevat de scans en toont nul overtredingen, of elke uitzondering staat met reden in de test; het verslag van de handmatige controle (datum, stromen, bevindingen) zit bij de oplevering. Afgevinkt met beide. Zie WEB-70 en PRIV voor de eisen.
- Norm: WCAG (versie en niveau: zie PRIV).
- Zie ook: PRIV-66, PRIV-67, WEB-70

### ARCH-47 Test een WordPress-plugin of thema in een wegwerpomgeving met twee rollen
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Test een eigen plugin, thema of mu-plugin in een lokale wegwerpinstallatie (`wp-env`, of een testsite op de hosting die de serverlaag van de klant heeft), met PHPUnit voor de logica en Playwright voor de schermen, en doorloop elke beheer- en AJAX-handeling als beheerder en als een rol zonder het vereiste recht.
- Bewijs: `.wp-env.json` staat in de repository met vaste versies van WordPress en PHP; de e2e-run toont per handeling twee uitkomsten (beheerder slaagt, lage rol krijgt een weigering); `wp-env run cli <opdracht>` (of gelijkwaardig) draait PHPUnit in de omgeving. De serverlaag (LiteSpeed, `.htaccess`, cache) wordt apart op de echte server getoetst (WP-64, INFRA-101). Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V8.2.1 (L1); twaalf-factor X.
