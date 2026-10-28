# PRIV N: NIS2 en de Cyberbeveiligingswet

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-76 Toets voor het eigen bedrijf en voor elke klant of de Cyberbeveiligingswet geldt
hoog · hard · klantproject | alles · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CBW
- Regel: Leg voor het eigen bedrijf en per klant vast of de organisatie in een sector uit bijlage 1 of 2 valt en middelgroot of groter is, en of er een activiteit is waarvoor de wet ongeacht de omvang geldt (domeinnaamregistratie, vertrouwensdiensten, openbare elektronische communicatie).
- Bewijs: Een notitie per organisatie met: sector, omvang (werknemers, omzet), bijzondere activiteiten, conclusie en datum. Afgevinkt als de notitie voor het eigen bedrijf bestaat en bij nieuwe klanten in de intake staat. `[jurist]` voor de conclusie; de aanwijzingsartikelen 9 tot en met 11 en bijlage 2 zijn in dit onderzoek niet volledig gelezen.
- Norm: Richtlijn (EU) 2022/2555 artikel 2 lid 1, 2 en 4; Cyberbeveiligingswet artikel 4, 8 en 12 en bijlage 1.

### PRIV-77 Wie domeinnamen doorverkoopt, valt ongeacht omvang onder de wet: registreer en houd houdergegevens op orde
hoog · hard · api | app · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: CBW
- Regel: Behandel de eigen domeinverkoop als "domeinnaamregistratiedienst": meld je aan bij het nationale register, houd per domein de naam, het e-mailadres en het telefoonnummer van de houder en het beheercontact nauwkeurig en volledig bij met een verificatiestap, publiceer het beleid daarvoor, en beantwoord een rechtmatig verzoek om registratiegegevens binnen 72 uur.
- Bewijs: (1) De uitkomst van de toets, bevestigd door een jurist of de toezichthouder, met datum. (2) Als de plicht geldt: het bewijs van aanmelding, een query die per domein in `registrar.domains` de vier gegevens toont zonder lege velden, een test dat een bestelling zonder bevestigd e-mailadres niet tot registratie leidt, de URL van het gepubliceerde beleid, en een vaste procedure voor toegangsverzoeken met de termijn van 72 uur. Afgevinkt met de toets, en bij "ja" met de vijf onderdelen. `[jurist]`: dit is de belangrijkste open vraag van dit domein.
- Norm: Richtlijn (EU) 2022/2555 artikel 2 lid 4, artikel 6 punt 22, artikel 28; Cyberbeveiligingswet artikel 1 (definitie), 4 lid 4, 43, 44, 49, 50, 88 tot en met 90.

### PRIV-78 Reken erop dat een klant onder de wet zijn eisen aan jou doorlegt
middel · richtlijn · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd voor elke klant die onder de Cyberbeveiligingswet valt het bewijs uit deze skill per project beschikbaar (updatebeleid, toegangsbeheer, back-up en herstelproef, incidentprocedure met termijnen, lijst van onderaannemers), zodat je een leveranciersvragenlijst kunt beantwoorden zonder iets te hoeven bouwen.
- Bewijs: Een map per klantproject met de bewijsstukken uit de checklist (GIT-67 bewaart de uitvoer van de gates). Afgevinkt als de map bestaat en de stukken een datum hebben.
- Norm: Richtlijn (EU) 2022/2555 artikel 21 lid 2 onder d.
