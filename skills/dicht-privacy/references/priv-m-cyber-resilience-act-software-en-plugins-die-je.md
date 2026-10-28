# PRIV M: Cyber Resilience Act (software en plugins die je levert)

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-70 Bepaal per leverbaar stuk software of het een product met digitale elementen is
hoog · hard · wp-plugin | wp-thema | mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg voor elke plugin, elk thema, elke bibliotheek, elke MCP-server en elke app die je aan anderen verstrekt vast: wordt het in het kader van een handelsactiviteit op de markt aangeboden (verkocht, in licentie gegeven, of gratis verspreid als onderdeel van je bedrijf), of is het maatwerk voor één klant, of is het een dienst die alleen op jouw server draait.
- Bewijs: Een lijst van alles wat je aan anderen levert met per stuk: soort (product, maatwerk, dienst), aan wie, en de conclusie met datum. Afgevinkt als de lijst bestaat. De kwalificatie (met name van maatwerk voor één klant en van een plugin die alleen binnen een onderhoudscontract wordt geleverd) is `[jurist]`.
- Norm: Verordening (EU) 2024/2847 artikel 2 lid 1, artikel 3 (definities product met digitale elementen, gegevensverwerking op afstand, op de markt aanbieden), overweging over websites en clouddiensten, artikel 71.

### PRIV-71 Meld een actief uitgebuite kwetsbaarheid in je product binnen 24 uur
hoog · hard · wp-plugin | wp-thema | mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem voor elk product uit PRIV-70 in het incidentdraaiboek op: een vroegtijdige waarschuwing binnen 24 uur nadat je weet van een actief uitgebuite kwetsbaarheid of een ernstig incident, een melding binnen 72 uur, en een eindverslag uiterlijk 14 dagen nadat een oplossing beschikbaar is (bij een ernstig incident binnen een maand), via het centrale meldingsplatform.
- Bewijs: Het draaiboek (INFRA-95, `docs/incident.md`) bevat de drie termijnen, het meldkanaal en de lijst van producten waarvoor ze gelden. Afgevinkt met het document. Welke CSIRT de coördinator is en of het platform in gebruik is: zie "Niet bevestigd".
- Norm: Verordening (EU) 2024/2847 artikel 14 lid 1 tot en met 4, artikel 71 lid 2.
- Zie ook: PRIV-31, INFRA-96, PRIV-32, PRIV-33, INFRA-91, AI-84, GIT-106, WP-78, INFRA-94

### PRIV-72 Geef elk product een meldpunt en een beleid voor het melden van kwetsbaarheden
middel · hard · wp-plugin | wp-thema | mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Publiceer bij elk product dat je levert een contactadres voor kwetsbaarheden en een kort beleid voor gecoördineerde openbaarmaking (wat je verwacht, wat de melder mag verwachten, binnen welke termijn je reageert). Aanvulling uit GIT-30: Lever het meldpunt als `SECURITY.md` met meldadres en ondersteunde versies, en zet op een publieke repo private vulnerability reporting aan.
- Bewijs: `SECURITY.md` in de repository en `/.well-known/security.txt` op de productsite (GIT-30, INFRA-65), en het adres in de readme van het pakket. Afgevinkt als de drie bestaan en een testbericht aankomt. Technisch af te dwingen.
    Ook (uit GIT-30): Het bestand bestaat en het adres komt aan (testmail naar een adres op het eigen domein). Afgevinkt met de ontvangen mail. Private vulnerability reporting bestaat alleen voor publieke repo's.
- Norm: Verordening (EU) 2024/2847 bijlage I deel II punt 5 en 6.
- Dekt ook: GIT-30
- Zie ook: INFRA-65

### PRIV-73 Lever zonder bekende uitbuitbare kwetsbaarheden en met een veilige standaardconfiguratie
hoog · hard · wp-plugin | wp-thema | mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef geen versie van een product vrij met een bekende uitbuitbare kwetsbaarheid in de eigen code of in een afhankelijkheid, en lever met een configuratie die standaard veilig is (geen standaardwachtwoord, optionele functies uit, minste rechten).
- Bewijs: De uitvoer van de afhankelijkheden-audit op het lockfile bij de release (GIT-61, bewaard volgens GIT-67), zonder open bevinding die uitbuitbaar is; een installatietest op een schone omgeving die laat zien dat geen functie open staat zonder instelling. Afgevinkt met beide. Technisch af te dwingen.
- Norm: Verordening (EU) 2024/2847 bijlage I deel I punt 2 onder a, b en j; ASVS 5.0.0 V15.2.1 (L1).
- Zie ook: GIT-77, INFRA-24, ARCH-32, WP-49, GIT-88, DB-92, GIT-61, MSG-06, SCR-32

### PRIV-74 Leg de ondersteuningsperiode vast en lever beveiligingsupdates kosteloos en apart
middel · hard · wp-plugin | wp-thema | mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Bepaal en publiceer per product hoe lang je beveiligingsupdates levert (ten minste vijf jaar, of de verwachte gebruiksduur als die korter is), lever ze kosteloos, waar haalbaar los van functie-updates, en met automatisch bijwerken als standaard waar het product dat ondersteunt.
- Bewijs: De readme of productpagina noemt de einddatum van de ondersteuning; de releasegeschiedenis toont een beveiligingsrelease zonder functiewijziging; het updatekanaal werkt op een testsite (voor WordPress: een eigen updatebron of de officiële bibliotheek, zie WP voor updates). Afgevinkt met de drie.
- Norm: Verordening (EU) 2024/2847 artikel 13 lid 8 en 9, bijlage I deel I punt 2 onder c, deel II punt 2, 7 en 8.

### PRIV-75 Maak bij elke release een SBOM en bewaar de risicobeoordeling
middel · richtlijn · wp-plugin | wp-thema | mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak per release van een product een softwarestuklijst in een gangbaar machineleesbaar formaat met ten minste de directe afhankelijkheden, en houd een korte gedocumenteerde beoordeling van de cyberbeveiligingsrisico's bij die je bij elke grote wijziging bijwerkt.
- Bewijs: De SBOM uit GIT-101 staat bij de release; `docs/threat-model.md` (de korte dreigingsanalyse uit ARCH) heeft een datum die niet ouder is dan de laatste hoofdversie. Afgevinkt met beide. Technisch af te dwingen voor de SBOM.
- Norm: Verordening (EU) 2024/2847 artikel 13 lid 3 en 4, bijlage I deel II punt 1.
- Zie ook: GIT-101, GIT-98
