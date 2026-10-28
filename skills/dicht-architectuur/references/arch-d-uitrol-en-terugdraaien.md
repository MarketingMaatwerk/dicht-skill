# ARCH D: Uitrol en terugdraaien

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-22 Rol uit met één script dat alle stappen doet
hoog · hard · api | app | mcp | wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak per dienst één uitrolscript dat in vaste volgorde de gate draait, bouwt, de vorige build bewaart, migreert, herstart, de health-controle doet en het bewijs wegschrijft; draai in de live checkout nooit een losse build, een losse herstart of een losse migratie.
- Bewijs: Het script staat in de repository (`deploy/publish.sh` of gelijkwaardig), begint met `set -euo pipefail`, en het bewijsbestand van de laatste uitrol (ARCH-53) toont elke stap met exitcode. Afgevinkt met script en bewijs.
- Norm: twaalf-factor V; NIST SSDF PO.3.3.
- Zie ook: ARCH-23, ARCH-24, GIT-02, GIT-03, DB-41, DB-42, INFRA-47

### ARCH-23 Controleer de gezondheid na de herstart en draai vanzelf terug
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat het uitrolscript na de herstart wachten tot de gereedheidscontrole (ARCH-67) binnen een vaste tijd slaagt, en laat het bij die mislukking én bij elke andere fout nadat de build is begonnen de vorige build terugzetten, opnieuw controleren en met een fout eindigen; of bouw in een aparte map en wissel pas na een geslaagde gate.
- Bewijs: Het script bevat de controle en de terugdraaifunctie, en een `trap ... ERR` (of een bouwmap die pas na de gate wordt gewisseld) dekt elke stap na de build; voor Docker `docker compose up -d --wait --wait-timeout <s>`; twee proeven op de testomgeving, één met een bewust kapotte build en één met een bewust falende stap tussen build en herstart, laten zien dat de vorige build blijft werken en het script met exitcode ongelijk aan nul eindigt. Afgevinkt met de uitvoer van beide proeven.
- Norm: twaalf-factor V (terugdraaien naar een vorige release).
- Zie ook: ARCH-22, ARCH-24, GIT-02, GIT-03, DB-41, DB-42, INFRA-47

### ARCH-24 Bewijs na elke uitrol dat wat draait gelijk is aan wat in git staat
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Vergelijk na elke uitrol het release-id dat de draaiende dienst meldt (ARCH-09) met de commit van de live checkout, en bij een image dat code kopieert ook de bestanden in de container met de repository.
- Bewijs: `test "$(curl -s 127.0.0.1:<poort>/health | jq -r .version)" = "$(git rev-parse --short HEAD)"`; voor Docker per bestand `docker exec <container> cat /app/<pad> | cmp - <pad>` over `git ls-files` met nul afwijkingen. Afgevinkt met de uitvoer in het bewijsbestand.
- Norm: twaalf-factor V.
- Zie ook: ARCH-22, ARCH-23, GIT-02, GIT-03, DB-41, DB-42, INFRA-47

### ARCH-25 Oefen het terugdraaien en houd migraties voorwaarts verenigbaar
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewaar bij elke uitrol de vorige build, beschrijf het terugdraaien in het runbook als één opdracht, oefen het minstens één keer per dienst en daarna bij elke wijziging van het uitrolscript, en zorg met expand en contract (DB-31) dat de vorige build op het nieuwe schema blijft werken.
- Bewijs: Het runbook bevat de terugdraai-opdracht; een gedateerd verslag van de laatste oefening op de testomgeving (build N naar N-1, health groen, kernroute werkt op het schema van N). Afgevinkt met runbook en verslag.
- Norm: twaalf-factor V; ASVS 5.0.0 V16.5.2 (L2).
- Zie ook: WP-63, WP-53, DB-40

### ARCH-26 Test de nieuwe versie als tweede exemplaar voordat je omschakelt
middel · richtlijn · api | app | mcp · eigen bron · tegenlezer: bevestigd (04-10-2026)
- Regel: Start de nieuwe versie vanuit de worktree als tweede exemplaar op een andere poort, tegen de testdatabase of een kopie, en draai daar de e2e-tests en de rooktest op voordat je in de live checkout merget en herstart.
- Bewijs: De uitvoer van de e2e-run noemt het adres van het tweede exemplaar en de commit; die commit is gelijk aan de commit die daarna is uitgerold. Afgevinkt met beide.
- Norm: twaalf-factor X.
- Eigen bron: geen primaire bron; bron is de eigen worktree-werkwijze plus een secundaire bron (Fowler). Opgenomen op besluit van Marketing Maatwerk (04-10-2026).

### ARCH-27 Rol een wijziging die veel sites of tenants raakt in stappen uit
hoog · hard · klantproject | wp-plugin | wp-thema | mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Rol een wijziging die in één keer meerdere klantsites, alle tenants of alle verzoeken raakt (een mu-plugin, een gedeelde nginx-regel, een firewallregel, een prompt of model, een gedeeld sjabloon) eerst uit op één eigen site of tenant, controleer het resultaat, en ga daarna in groepen verder.
- Bewijs: Het bewijsbestand toont de volgorde met tijdstippen (eerst de eigen site, dan de rest) en per stap de controle die is gedaan. Afgevinkt met die lijst.
- Norm: NIST SSDF PW.8.2.

### ARCH-28 Geef elk script dat veel wijzigt of verwijdert een proefstand, exacte doelen en een grens
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een script dat in bulk wijzigt of verwijdert standaard alleen tonen wat het zou doen, werken op een expliciete lijst van id's van één soort, stoppen boven een vooraf opgegeven aantal, en bij voorkeur eerst markeren als verwijderd in plaats van direct wissen.
- Bewijs: Het script heeft een proefstand als standaard (`--uitvoeren` is nodig om echt te wijzigen), valideert het type van elk id, heeft een maximum, en de uitvoer van de proefrun staat in het logboek vóór de echte run. Afgevinkt met script en beide uitvoeren. Op live geldt daarnaast de regel van Marketing Maatwerk: verwijderen vereist akkoord.
- Norm: ASVS 5.0.0 V2.3.5 (L3, goedkeuring door meer dan één persoon voor handelingen met grote gevolgen).
- Zie ook: BIZ-23, AI-73, SCR-46, SCR-47, BIZ-21, SCR-15, ARCH-51

### ARCH-87 Rol uit op een moment waarop je na een uur nog kunt nameten en terugdraaien
middel · richtlijn · api | app | mcp | klantproject | wp-plugin | wp-thema · eigen bron · tegenlezer: niet tegengelezen
- Regel: Rol een wijziging naar productie alleen uit als degene die uitrolt een uur later de nameting kan doen en zo nodig kan terugdraaien; niet vlak voor een periode waarin niemand kijkt (avond, vrije dag, afwezigheid).
- Bewijs: Het bewijsbestand van de uitrol noemt het tijdstip van de uitrol en, minstens een uur later, de nameting: voor een dienst de gereedheidscontrole (ARCH-67) en de foutmeldingen in het log sinds de uitrol (ARCH-68); voor WordPress de homepage met status 200 en het PHP-foutlog sinds de uitrol zonder nieuwe fouten; in beide gevallen één echte handeling van de hoofdfunctie (formulier versturen, testbestelling, inloggen) met de uitkomst. Afgevinkt met beide tijdstippen.
- Norm: geen externe norm; eigen werkwijze.
- Eigen bron: geen primaire bron; eigen werkwijze naar een tip uit een video van een derde; de termijn van een uur is een eigen keuze. Opgenomen op opdracht van Marketing Maatwerk via de eigen beheersessie (28-10-2026).
