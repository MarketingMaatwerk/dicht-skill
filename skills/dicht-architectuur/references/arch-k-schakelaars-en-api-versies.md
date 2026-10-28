# ARCH K: Schakelaars en API-versies

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-76 Geef elke risicovolle functie een schakelaar die zonder uitrol werkt
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke functie die zelfstandig iets naar buiten doet of geld raakt (een automatische verzendlijn, een betaalstroom, een koppeling met een externe dienst, een AI-functie, een nieuwe import) een schakelaar die zonder nieuwe uitrol werkt, test dat de rest van de applicatie blijft werken als hij uit staat, en beschrijf in het runbook wanneer je hem gebruikt.
- Bewijs: Per functie staat de schakelaar in `docs/ARCHITECTURE.md`; een test zet hem om en bewijst dat de functie niets meer doet (nul uitgaande aanroepen) en dat inloggen en de kernroutes blijven werken. Afgevinkt met de testuitvoer. Zie AI-79 voor AI-functies.
- Norm: ASVS 5.0.0 V16.5.2 (L2).
- Zie ook: AI-79, AI-26, PRIV-51, ARCH-77, SCR-46, BIZ-23, SCR-52, MSG-49

### ARCH-77 Houd schakelaars veilig, uniek en tijdelijk
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een ontbrekende of onleesbare schakelaar de veilige stand geven (functie uit), dwing hem af op de server, hergebruik nooit de naam van een oude schakelaar voor iets nieuws, verwijder een schakelaar en de dode code erachter zodra de functie definitief aan of uit staat, en houd een lijst bij met per schakelaar de eigenaar en de einddatum.
- Bewijs: De lijst van schakelaars staat in de repository; `grep -rn "<naam>" src` voor elke schakelaar die langer dan de einddatum bestaat is beoordeeld; een test start de applicatie zonder de configuratie van een schakelaar en bewijst dat de functie uit staat; een test als gewone gebruiker bewijst dat een schakelaar die in de browser wordt omgezet de server niet beïnvloedt. Afgevinkt met lijst en tests.
- Norm: ASVS 5.0.0 V8.3.1 (L1), V15.2.3 (L2), V16.5.3 (L2).
- Zie ook: ARCH-76, AI-79, AI-26, PRIV-51, SCR-46, BIZ-23, SCR-52, MSG-49

### ARCH-78 Kondig een brekende wijziging van een API aan met Deprecation en Sunset
middel · richtlijn · api | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Breng een wijziging die bestaande clients breekt uit als nieuwe versie naast de oude, stuur op de oude versie de kopregel `Deprecation` (een datum als `@<unix-tijd>`) en zodra de einddatum vaststaat ook `Sunset` (een HTTP-datum), en zet de einddatum niet vóór de datum van afkeuring. Aanvulling uit API-26: Zet de versie in het pad (`/v1/`) en breek binnen een versie niets; `Deprecation` is RFC 9745, `Sunset` is RFC 8594.
- Bewijs: `curl -sI <oude route>` toont beide kopregels; de einddatum staat in de documentatie; de logs tellen per client hoeveel aanroepen nog op de oude versie binnenkomen, en dat aantal is nul vóór het uitzetten. Afgevinkt met kopregels en telling. Voor MCP-tools geldt hetzelfde: een gewijzigde naam of een gewijzigd invoerschema is een brekende wijziging (AI-56, AI-77).
    Ook (uit API-26): Publieke routes beginnen met een versie. Een uit te faseren route geeft beide headers; de einddatum staat in de inventaris van API-25.
- Norm: RFC 9745 (Standards Track); RFC 8594 (Informational).
- Dekt ook: API-26

### ARCH-79 Breid een API uit door toe te voegen, niet door te wijzigen
laag · richtlijn · api | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Voeg binnen een versie alleen optionele velden en nieuwe routes toe; wijzig de betekenis, het type of de verplichting van een bestaand veld niet en verwijder niets, en laat de contracttest (ARCH-41) op de vorige versie van het schema blijven slagen.
- Bewijs: De contracttest draait tegen het opgeslagen schema van de vorige uitgave en slaagt; een verschil tussen de twee schema's toont alleen toevoegingen. Afgevinkt met de uitvoer. Dezelfde volgorde als expand en contract in de database (DB-31).
- Norm: ASVS 5.0.0 V15.3.1 (L1) blijft gelden voor nieuwe velden.
