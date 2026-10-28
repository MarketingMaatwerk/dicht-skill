# PRIV O: AI-verordening (het minimum voor AI-functies)

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-79 Zeg bij de eerste interactie dat iemand met een AI-systeem te maken heeft
hoog · hard · website | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke chatbot, spraakassistent of andere functie waarmee een mens rechtstreeks met een AI-systeem communiceert, uiterlijk bij de eerste interactie duidelijk en toegankelijk melden dat het een AI-systeem is.
- Bewijs: Een e2e-test opent de functie en vindt de melding in het eerste scherm of bericht, leesbaar voor een schermlezer. Afgevinkt met de testuitvoer. Technisch af te dwingen.
- Norm: Verordening (EU) 2024/1689 artikel 50 lid 1 en 5, artikel 113.

### PRIV-80 Stel vast of je aanbieder of gebruiksverantwoordelijke bent
middel · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AI-VO
- Regel: Leg per AI-functie vast of je het systeem onder eigen naam aanbiedt (aanbieder) of een systeem van een ander onder eigen verantwoordelijkheid gebruikt (gebruiksverantwoordelijke), en of de functie in een hoogrisicotoepassing of een verboden praktijk kan vallen.
- Bewijs: Een tabel per AI-functie: rol, doel, of mensen er rechtstreeks mee communiceren, of de uitvoer naar buiten gaat, en de conclusie over hoog risico met datum. Afgevinkt met de tabel. `[jurist]` voor de rol en voor de vraag of een zorgproduct een hoogrisicosysteem is; de artikelen 5 en 6 en bijlage III zijn in dit onderzoek niet gelezen.
- Norm: Verordening (EU) 2024/1689 artikel 3 (definities aanbieder en gebruiksverantwoordelijke); Verordening (EU) 2026/1744.

### PRIV-81 Markeer gegenereerde tekst, beeld, audio en video machineleesbaar als je aanbieder bent
middel · richtlijn · app | mcp · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AI-VO
- Regel: Zorg als aanbieder van een systeem dat synthetische inhoud maakt dat de uitvoer machineleesbaar gemarkeerd is als kunstmatig gegenereerd, door de markering van de onderliggende leverancier te behouden of zelf metadata toe te voegen, en verwijder zulke markeringen niet in de eigen verwerking.
- Bewijs: Een test die een gegenereerde afbeelding door de eigen verwerking haalt en daarna de markering nog terugvindt; voor tekst een vastgelegde keuze met reden. Afgevinkt met de testuitvoer. Welke technieken als voldoende gelden (de praktijkcode) is niet gelezen: zie "Niet bevestigd".
- Norm: Verordening (EU) 2024/1689 artikel 50 lid 2; Verordening (EU) 2026/1744 (overgang in artikel 111 lid 4).

### PRIV-82 Maak bekend dat een deepfake of een ongecontroleerde publieke tekst door AI is gemaakt
middel · hard · website | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Vermeld bij beeld, audio of video die een deepfake vormt dat de inhoud kunstmatig is gemaakt of bewerkt, en bij AI-tekst die wordt gepubliceerd om het publiek te informeren over zaken van algemeen belang hetzelfde, tenzij een mens de tekst heeft gecontroleerd en iemand de redactionele verantwoordelijkheid draagt.
- Bewijs: De publicatiestroom heeft een goedkeuringsstap met naam en tijdstip per item (AI-24); een test laat zien dat een item zonder goedkeuring niet gepubliceerd wordt. Afgevinkt met de testuitvoer. Of een tekst "van algemeen belang" is: `[jurist]`.
- Norm: Verordening (EU) 2024/1689 artikel 50 lid 4.

### PRIV-83 Laat persoonsgegevens alleen naar een AI-dienst gaan die in het register staat
hoog · hard · app | mcp | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor werk met persoonsgegevens van klanten alleen AI-diensten die als subverwerker zijn vastgelegd met overeenkomst, bewaartermijn en regio (AI-66), en voer zulke gegevens niet in bij een chatdienst of abonnement dat daar niet onder valt.
- Bewijs: Per AI-aanroep in de code is te herleiden welke dienst en welk account hij gebruikt (`grep` op de basis-URL's en sleutelnamen) en die dienst staat onder `subprocessors:` met een overeenkomst (PRIV-14). Afgevinkt met de grep en het register. `[jurist]`: de vraag van AI-66 over de proxy blijft open en staat onder "Open vragen".
- Norm: AVG artikel 28 en 32, artikel 4 punt 12 (inbreuk); zie AI-66, AI-67 en AI-72.
- Zie ook: AI-66, PRIV-14, PRIV-18, AI-72, PRIV-12, AI-65, PRIV-03
