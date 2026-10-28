# PRIV P: betalen (Mollie, kaartgegevens, bestelknop, bewaarplicht)

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-84 Laat kaartgegevens nooit door de eigen server of de eigen pagina-code lopen
kritiek · hard · website | wp-plugin | api | app | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: PCI
- Regel: Gebruik voor kaartbetalingen de betaalpagina van de betaalprovider (doorsturen) of diens ingesloten velden, en bouw geen formulier, log, veld of API-route waar een kaartnummer, vervaldatum of beveiligingscode doorheen gaat.
- Bewijs: `grep -rniE "cardnumber|card_number|cvv|cvc|pan\b" src/` geeft alleen aanroepen van de bibliotheek van de provider; de netwerklog van een testbetaling laat zien dat kaartgegevens alleen naar het domein van de provider gaan. Afgevinkt met beide. Technisch af te dwingen.
- Norm: PCI DSS v4.0.1 (SAQ A); ASVS 5.0.0 V14.2.6 (L3); zie AI-49.
- Zie ook: PRIV-85, WEB-58

### PRIV-85 Bescherm de pagina die de betaalvelden insluit tegen vreemde scripts
hoog · hard · website | wp-plugin | app | klantproject · tegenlezer: scherpen (04-10-2026) · bron niet gelezen: PCI
- Regel: Laad op een pagina die betaalvelden van de provider insluit (iframe of ingesloten velden) alleen scripts die je kent en nodig hebt, met een strikte CSP en SRI, en houd een lijst van die scripts met de reden bij; kies bij twijfel voor doorsturen naar de betaalpagina van de provider.
- Bewijs: De hostlijst van de afrekenpagina uit WEB-58 bevat alleen de eigen host en de betaalprovider; de CSP uit WEB-11 en WEB-12 staat afdwingend op die pagina; de lijst van scripts met reden staat in de projectdocumentatie. Afgevinkt met hostlijst, header en lijst. Technisch af te dwingen. Welke vragenlijst voor de klant geldt en wat Mollie daarover bevestigt: zie "Niet bevestigd".
- Norm: PCI DSS v4.0.1 eis 6.4.3 en 11.6.1 en de voorwaarde in SAQ A (januari 2025); ASVS 5.0.0 V3.4.3 (L2).
- Zie ook: WEB-11, AI-14, WEB-58, PRIV-84

### PRIV-86 Behandel de betaalprovider als zelfstandige verantwoordelijke, en noem hem toch in het register
middel · richtlijn · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet Mollie in het register en de privacyverklaring als ontvanger van betaalgegevens met de rol "zelfstandig verwerkingsverantwoordelijke", stuur alleen de gegevens mee die de betaling nodig heeft, en verwacht geen verwerkersovereenkomst voor betalingen.
- Bewijs: Het register noemt de rol; een test van de betaalaanroep laat zien dat `description` en `metadata` alleen een bestelnummer en interne sleutels bevatten. Afgevinkt met beide. De kwalificatie van de rol: `[jurist]`.
- Norm: AVG artikel 4 punt 7, artikel 5 lid 1 onder c, artikel 13 lid 1 onder e.

### PRIV-87 Bij een eerste betaling met machtiging: toon wat en hoe vaak, en bewaar het bewijs
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: SEPA
- Regel: Toon vóór een eerste betaling die een machtiging voor terugkerende incasso geeft het bedrag, de frequentie en wat er verandert bij opzegging, sla het mandaat (referentie en datum) en de getoonde tekstversie op bij de klant, en kondig een incasso aan voordat hij wordt afgeschreven.
- Bewijs: Een e2e-test van de bestelroute controleert dat bedrag en frequentie boven de betaalknop staan; de database heeft per abonnement de `mandateReference`, de `signatureDate` en de versie van de voorwaarden en de getoonde samenvatting. Afgevinkt met test en schema. De 8 weken en 13 maanden zijn alleen uit de Mollie-documentatie bevestigd, niet uit het SEPA-rulebook.
- Norm: SEPA Direct Debit (via de regels van de betaalprovider); AVG artikel 5 lid 2 voor het bewijs.

### PRIV-88 De bestelknop zegt dat er betaald moet worden, en de kerninformatie staat er direct boven
hoog · hard · website | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef de knop waarmee een consument bestelt een tekst waaruit de betalingsverplichting ondubbelzinnig blijkt ("bestelling met betalingsverplichting" of gelijkwaardig), toon onmiddellijk daarvoor de totale prijs, de duur en de minimale duur van de overeenkomst, en vermeld uiterlijk aan het begin van het bestelproces de leveringsbeperkingen en de betaalmiddelen.
- Bewijs: Een e2e-test leest de tekst van de bestelknop en controleert dat prijs, duur en minimale duur in hetzelfde scherm boven de knop staan; voor een zakelijke bestelstraat een test dat bestellen zonder geldig KvK-nummer niet lukt. Afgevinkt met de testuitvoer. Technisch af te dwingen. Of een eenmanszaak als klant consument is: `[jurist]`.
- Norm: BW artikel 6:230v lid 2 tot en met 4, artikel 6:230m lid 1.

### PRIV-89 Bouw de herroepingsfunctie in elke webwinkel voor consumenten
hoog · hard · website | wp-plugin | app | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Geef elke online-interface waar consumenten een overeenkomst op afstand sluiten een duidelijk zichtbare, steeds beschikbare functie om de overeenkomst te ontbinden: een knop, een formulier met naam, de overeenkomst en het adres voor de bevestiging, een tweede bevestigingsknop, en direct een ontvangstbevestiging op een duurzame gegevensdrager met inhoud, datum en tijdstip.
- Bewijs: Een e2e-test doorloopt de functie zonder in te loggen tot en met de ontvangstbevestiging per mail en controleert datum en tijd in de bevestiging; de link staat in de voettekst op elke pagina. Afgevinkt met de testuitvoer. Technisch af te dwingen. Uitzonderingen op het herroepingsrecht zelf (maatwerk, digitale inhoud, diensten die al zijn uitgevoerd): `[jurist]`.
- Norm: BW artikel 6:230oa lid 1 tot en met 5, artikel 6:230m lid 1 onder h; Richtlijn (EU) 2023/2673.

### PRIV-90 Bewaar de administratie zeven jaar, en alleen de administratie
middel · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Markeer in het gegevensmodel welke gegevens bij de fiscale administratie horen (facturen, betalingen, overeenkomsten en de berichten daarover) en bewaar die zeven jaar; geef al het andere van dezelfde klant een eigen, kortere termijn en laat de opruimjob dat onderscheid maken.
- Bewijs: De tabel met termijnen (DB-83) heeft per gegevenssoort de kolom "administratie ja of nee"; de test van de opruimjob laat zien dat na de korte termijn alleen de administratie overblijft. Afgevinkt met tabel en test. Technisch af te dwingen. Wat precies tot de administratie hoort (de Belastingdienst noemt ook "berichten" en "software en databestanden"): `[jurist]` of de boekhouder.
- Norm: AWR artikel 52 lid 4; AVG artikel 5 lid 1 onder e, artikel 6 lid 1 onder c, artikel 17 lid 3 onder b.

### PRIV-91 Loop bij een voorkant voor bezoekers de juridische checkvragen langs en laat elke twijfel controleren
middel · richtlijn · website | wp-thema | app | klantproject · eigen bron · tegenlezer: niet tegengelezen
- Regel: Beantwoord bij elke oplevering van een site, webwinkel of app met bezoekers uit Nederland of de EU deze checkvragen, en laat elk antwoord waarover twijfel is juridisch controleren (niet 100% zeker, laat juridisch controleren; dit is geen juridisch advies). (1) Getuigenissen en reviews: voor een website geldt VIBE-02 (hard); voor een app: is elk getuigenis echt en terug te voeren op een echte klant? (2) Tijdsdruk en schaarste: klopt elke afteltimer en elke melding als "nog maar 2", en begint geen timer opnieuw? (3) Opzeggen: kan een abonnement even makkelijk worden opgezegd als afgesloten (zelfde kanaal, niet meer stappen)? (4) Automatisch verlengen: krijgt de klant bericht vóór een verlenging (bij een incasso met machtiging zie PRIV-87)? (5) Prijs: is de prijs voor iedereen gelijk, of hangt hij af van gegevens over de bezoeker, en staat dat er dan bij? (6) Claims: is er onderbouwing voor elke claim over wat het product of een AI-functie doet? (7) Inhoud van gebruikers: kan een bezoeker illegale inhoud melden en laten weghalen als bezoekers iets kunnen plaatsen? (8) Leeftijd: richt de dienst zich op minderjarigen of trekt hij ze aan, en is bepaald wat dat vraagt? (9) Beeld en tekst van anderen: is er een licentie of toestemming voor elke foto, video, illustratie, lettertype en tekst die niet van de klant is? (10) AI-gesprekken: kan een chatbot een gesprek over gezondheid, psychische nood of een crisis krijgen, en is er dan een vaste doorverwijzing naar hulp en zijn er gebruiksregels voor de AI-functie?
- Bewijs: In het bewijsbestand staat per vraag het antwoord (ja, nee, of nvt met reden) en bij elk antwoord met twijfel aan wie het is voorgelegd en wanneer, of letterlijk "niet juridisch gecontroleerd". Elke open twijfel staat als open punt in het opleverbericht aan de klant. Afgevinkt met die lijst.
- Norm: geen gelezen norm of wettekst; checkvragen, niet 100% zeker, laat juridisch controleren. Wat al een eigen regel heeft of hetzelfde onderwerp raakt, staat daar: nepreviews en nepcijfers VIBE-02, AI-melding PRIV-79, weigerknop cookies PRIV-42, tracking pas na toestemming PRIV-40 en PRIV-43, ongevraagde mail PRIV-47 tot en met PRIV-49, afmelden PRIV-48, bijzondere gegevens (ook gezondheid en biometrie) PRIV-12, risicobeoordeling PRIV-37, toegankelijkheid PRIV-66 en VIBE-27, melden van een uitgebuite kwetsbaarheid PRIV-71, bestelknop PRIV-88, herroeping PRIV-89, incasso met machtiging PRIV-87, opzeggen in elk systeem BIZ-47, licenties van afhankelijkheden en meegeleverde plugins GIT-104 en GIT-105.
- Eigen bron: geen primaire bron; checkvragen uit video's van een derde (niet nagecheckt); geen norm of wettekst gelezen, laat juridisch controleren. Opgenomen op opdracht van Marketing Maatwerk via de eigen beheersessie (28-10-2026).
