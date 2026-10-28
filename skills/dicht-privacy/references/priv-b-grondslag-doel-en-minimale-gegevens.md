# PRIV B: grondslag, doel en minimale gegevens

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-07 Geen verwerking zonder vastgelegde grondslag
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Kies vóór de bouw voor elk doel één van de zes grondslagen uit artikel 6 lid 1 en leg hem vast in het register; bouw niets dat persoonsgegevens verzamelt waarvoor dat veld leeg is.
- Bewijs: `legal_basis` is gevuld bij elke activiteit (de controle uit PRIV-02); bij sub f staat een verwijzing naar de belangenafweging (in het eigen register het veld `lia_document`). Afgevinkt met de scriptuitvoer. De keuze zelf is `[jurist]` bij twijfel, met name bij gerechtvaardigd belang.
- Norm: AVG artikel 5 lid 1 onder a, artikel 6 lid 1.

### PRIV-08 Vraag per veld alleen wat het doel nodig heeft
middel · hard · website | wp-plugin | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Onderbouw elk formulierveld en elke kolom met persoonsgegevens met het doel waarvoor het nodig is, maak velden die niet nodig zijn optioneel of verwijder ze, en sla afgeleide of meegestuurde gegevens (IP-adres, user agent, volledige payload van een webhook) alleen op als er een doel voor is.
- Bewijs: Een tabel per formulier: veld, verplicht of optioneel, doel. `grep -rnE "REMOTE_ADDR|user_agent|req\.ip" src/` laat alleen plekken zien met een genoteerd doel. Afgevinkt met tabel en grep. Technisch deels af te dwingen: een schema-test die faalt als een formulier een veld krijgt dat niet in de tabel staat.
- Norm: AVG artikel 5 lid 1 onder c, artikel 25 lid 2; ASVS 5.0.0 V14.2.6 (L3).

### PRIV-09 De standaardinstelling is de zuinigste
middel · hard · app | api | wp-plugin | mcp · tegenlezer: scherpen (04-10-2026)
- Regel: Zet elke instelling die gegevens deelt, zichtbaar maakt of langer bewaart standaard uit: profielen en lijsten zijn privé tot iemand ze deelt, optionele meting staat uit tot toestemming, en een nieuwe gebruiker of koppeling krijgt de minste rechten.
- Bewijs: Een test die een nieuw account of nieuwe tenant aanmaakt en controleert dat elke deel- en zichtbaarheidsinstelling op de zuinigste waarde staat en dat geen eigen gegevens zonder login opvraagbaar zijn. Afgevinkt met de testuitvoer. Technisch af te dwingen.
- Norm: AVG artikel 25 lid 2; ASVS 5.0.0 V8.2.2 (L1).

### PRIV-10 Toestemming is aantoonbaar, per doel en even makkelijk in te trekken
hoog · hard · website | app | api | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg bij elke toestemming vast wie, wanneer, voor welk doel en op basis van welke tekstversie toestemming gaf, vraag toestemming per doel met een vakje dat niet vooraf is aangevinkt, en bouw het intrekken op dezelfde plek en met evenveel stappen als het geven.
- Bewijs: (1) `grep -rnE "checked|defaultChecked" ` op toestemmingsvakjes geeft niets. (2) Een e2e-test geeft toestemming, trekt haar in via de pagina zelf en controleert de rij in de tabel en dat de verwerking stopt. Afgevinkt met beide. Technisch af te dwingen.
- Norm: AVG artikel 4 punt 11, artikel 7 lid 1, 3 en 4.

### PRIV-11 Gebruik gegevens niet voor een ander doel dan waarvoor ze zijn verzameld
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Koppel elke nieuwe toepassing van bestaande persoonsgegevens (een mailing aan bestellers, een AI-samenvatting van klantmail, een export voor analyse) aan het oorspronkelijke doel in het register, en bouw haar pas na een vastgelegde toets op verenigbaarheid of een nieuwe grondslag.
- Bewijs: Bij elke nieuwe functie die bestaande persoonsgegevens leest, staat in de PR of het opleverbericht welke activiteit uit het register hij bedient; een nieuwe activiteit is toegevoegd als die er niet was (PRIV-03). Afgevinkt met de verwijzing. Niet technisch af te dwingen; wel te ondersteunen met aparte databaserollen per dienst (DB-02), zodat een dienst niet bij gegevens voor een ander doel kan.
- Norm: AVG artikel 5 lid 1 onder b, artikel 6 lid 4.

### PRIV-12 Houd bijzondere gegevens buiten systemen die er niet voor gebouwd zijn
hoog · hard · app | api | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwerk geen gegevens over gezondheid, ras, geloof, politieke opvatting, vakbond, seksuele gerichtheid, genetica of biometrie tenzij een uitzondering van artikel 9 lid 2 is vastgelegd, en waarschuw bij vrije tekstvelden, notities en uploads dat ze er niet voor bedoeld zijn.
- Bewijs: (1) Het register heeft per activiteit `special_categories` (in het eigen bestand gevuld bij 22 van de 30 activiteiten; de rest invullen). (2) Bij elk vrij tekstveld dat bij een persoon hoort, staat een korte hulptekst, en de classificatie uit DB-87 markeert het veld als "kan bijzondere gegevens bevatten", met de gevolgen voor logs, exports en modelaanroepen. Afgevinkt met de telling en de classificatie.
- Norm: AVG artikel 9 lid 1 en 2; ASVS 5.0.0 V14.1.1 en V14.1.2 (L2).
- Zie ook: AI-66, PRIV-83, PRIV-14, PRIV-18, AI-72, AI-65, PRIV-03

### PRIV-13 Laat geen besluit met gevolgen voor een persoon volledig aan een automaat
middel · hard · app | api | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw bij elke automatische beoordeling die iemand een dienst weigert, een prijs bepaalt of hem anders "in aanmerkelijke mate treft" een stap in waarin een mens beslist of kan herzien, en leg vast welke beoordelingen er zijn.
- Bewijs: Een lijst van automatische beoordelingen met per stuk: wat is het gevolg, wie kan het herzien, hoe vraagt de betrokkene dat aan. Een test laat zien dat een afwijzing een taak of melding voor een mens oplevert. Afgevinkt met lijst en test. Of een gevolg "aanmerkelijk" is: `[jurist]`.
- Norm: AVG artikel 22 lid 1 tot en met 3, artikel 15 lid 1 onder h; zie ook AI-24.
