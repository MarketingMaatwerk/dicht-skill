# ARCH C: Fouten en veerkracht

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-13 Stel time-outs af van binnen naar buiten
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per verzoekpad één tabel vast met de time-out van elke laag (browser of client, nginx, applicatie, database, externe dienst) en zorg dat elke binnenste laag eerder opgeeft dan de laag eromheen.
- Bewijs: De tabel staat in `docs/ARCHITECTURE.md` met per laag de waarde en de vindplaats (`nginx -T | grep -E "proxy_(read|send|connect)_timeout"`, de Fastify-opties, `SHOW statement_timeout` voor de app-rol, de time-out van de HTTP-client). Afgevinkt als elke binnenste waarde kleiner is dan de buitenste. De waarden zelf zijn een eigen keuze per project.
- Norm: ASVS 5.0.0 V13.1.3 (L3), V15.1.3 (L2).
- Zie ook: INFRA-45, API-18, WEB-43, API-19, INV-44, INV-10, MSG-24, API-48, API-49, ARCH-14, AI-76, DB-65, SCR-21, SCR-25, SCR-26, SCR-43, MSG-42

### ARCH-14 Herhaal op één laag
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Kies per keten één laag die een mislukte aanroep herhaalt (meestal de laag het dichtst bij de externe dienst) en laat de lagen erboven de fout doorgeven zonder zelf te herhalen.
- Bewijs: `grep -rnE "retry|retries|attempt" src` toont herhaallogica op één laag per keten (de gedeelde functie uit API-49); de browsercode en de wachtrij herhalen niet dezelfde aanroep nog eens. Afgevinkt met de grep en een korte toelichting per keten.
- Norm: ASVS 5.0.0 V13.1.3 (L3).
- Zie ook: API-48, API-49, ARCH-13, AI-76, DB-65, API-19, SCR-21, SCR-25, SCR-26, SCR-43, MSG-42

### ARCH-15 Laat de kern doorwerken als een externe dienst uitvalt
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bepaal per externe dienst (betaalprovider, mail, AI-leverancier, boekhouding, registrar) wat de applicatie doet als die niet antwoordt: een nette melding, een taak in de wachtrij of een uitgeschakelde functie; laat inloggen en de kernschermen daar nooit op wachten.
- Bewijs: Per externe dienst een test die de dienst onbereikbaar maakt (verkeerd adres of een nagebootste time-out) en bewijst dat (1) de inlog en een kernroute binnen de normale tijd 200 geven en (2) de afhankelijke functie een nette fout of een wachtstatus geeft. Afgevinkt met de testuitvoer per dienst.
- Norm: ASVS 5.0.0 V16.5.2 (L2); OWASP Top 10 2025 A10.

### ARCH-16 → API-32, API-12
Samengevoegd: "Laat een bewerking helemaal slagen of helemaal terugdraaien" is gedekt door API-32, API-12. Gebruik die regel.

### ARCH-17 Maak het afsluiten korter dan het geduld van de procesmanager
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat de dienst op SIGTERM stoppen met aannemen, lopende verzoeken afmaken en verbindingen sluiten, met een eigen uiterste tijd die korter is dan de tijd waarna de procesmanager SIGKILL stuurt. Aanvulling uit API-73: Vang ook `SIGINT` af, roep `app.close()` aan, laat lopende taken afmaken binnen een grens en sluit daarna de databasepool.
- Bewijs: De waarden naast elkaar: de eigen afsluittijd (bijvoorbeeld `close-with-grace` met `delay`, standaard 10000 ms) tegenover `systemctl show <unit> -p TimeoutStopUSec` (standaard 90 seconden) of `stop_grace_period` in Compose (standaard 10 seconden). Een proef: start een traag verzoek, stuur SIGTERM, en zie dat het verzoek een antwoord krijgt en het proces daarna met code 0 stopt. Afgevinkt met de waarden en de proef. Zie API-73 voor de code.
    Ook (uit API-73): De code bevat de signaalafhandeling. Test: een herstart tijdens een traag verzoek levert een volledig antwoord of een 503 op, geen afgebroken verbinding. Fastify geeft na `close()` standaard 503 op nieuwe verzoeken (`return503OnClosing`).
- Norm: twaalf-factor IX.
- Dekt ook: API-73

### ARCH-18 Ga ervan uit dat een taak meer dan één keer draait
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf elke taak in een wachtrij zo dat twee keer uitvoeren hetzelfde resultaat geeft als één keer (unieke sleutel per effect), en laat een worker die stopt zijn lopende taak teruggeven aan de rij.
- Bewijs: Per soort taak een test die dezelfde taak twee keer aanbiedt en precies één effect telt (één rij, één uitgaand bericht in de nagebootste dienst). Afgevinkt met de testuitvoer. Zie DB-68 (unieke sleutel) en DB-71 (`FOR UPDATE SKIP LOCKED`).
- Norm: twaalf-factor IX; ASVS 5.0.0 V2.3.3 (L2).
- Zie ook: API-30, API-31, API-33, API-38, DB-68, AUTH-59, ARCH-19, API-23, DB-71, ARCH-20, BIZ-42, BIZ-40, SCR-45, API-41, API-49

### ARCH-19 Geef elke wachtrij een maximum aantal pogingen, een dode-brievenbak en een alarm
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Begrens het aantal pogingen per taak, zet een taak die het maximum bereikt in een aparte dode-brievenbak met de laatste fout, sla alarm zodra daar iets in komt of zodra de rij langer wordt dan een vastgelegde drempel, en beschrijf hoe je een taak opnieuw aanbiedt.
- Bewijs: De wachtrijconfiguratie toont het maximum en de wachttijd; een test laat een taak altijd falen en vindt hem daarna in de dode-brievenbak met de foutmelding; een proefmelding van het alarm met datum; het runbook (ARCH-31) beschrijft het opnieuw aanbieden. Afgevinkt met de vier onderdelen.
- Norm: ASVS 5.0.0 V15.1.3 (L2), V15.2.2 (L2).
- Zie ook: API-23, DB-71, ARCH-18, ARCH-20, BIZ-42

### ARCH-20 Leg de wijziging en de opdracht voor het externe effect vast in dezelfde transactie
hoog · richtlijn · api | app | mcp · tegenlezer: scherpen (04-10-2026)
- Regel: Als een handeling zowel de database wijzigt als een extern effect heeft (mail, webhook, betaling, registratie), schrijf dan de opdracht voor dat effect als rij in dezelfde transactie als de wijziging, en laat een worker die rij daarna uitvoeren.
- Bewijs: Voor elke handeling met een extern effect toont de code dat de taak binnen dezelfde transactie wordt ingevoegd (`tx.insert(jobs)` of de wachtrij-API met de transactie), en een test die het proces stopt na de commit bewijst dat de worker het effect alsnog uitvoert. Afgevinkt met codeverwijzing en test.
- Norm: ASVS 5.0.0 V2.3.3 (L2).
- Zie ook: ARCH-19, API-23, DB-71, ARCH-18, BIZ-42

### ARCH-21 Zorg dat een plotselinge stop geen halve toestand achterlaat
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Ontwerp elk proces zo dat het op elk moment hard gestopt kan worden: geen toestand die alleen in het geheugen bestaat, geen bestand dat half geschreven blijft staan, en een taak die "bezig" is komt na een time-out vanzelf terug.
- Bewijs: Een proef op de testomgeving: start een taak en een verzoek, stop het proces met `kill -9`, start het opnieuw en controleer dat de taak binnen de verlooptijd opnieuw draait en dat er geen half bestand of halve rij is. Afgevinkt met het verslag van de proef. Schrijf bestanden via een tijdelijke naam en een `rename`.
- Norm: twaalf-factor IX.
