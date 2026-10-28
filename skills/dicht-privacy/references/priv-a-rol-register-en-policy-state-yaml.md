# PRIV A: rol, register en policy-state.yaml

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-01 Leg per project vast wie verantwoordelijke en wie verwerker is
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg vóór de bouw per gegevensstroom vast wie doel en middelen bepaalt (de verwerkingsverantwoordelijke) en wie namens die partij verwerkt (de verwerker), en schrijf dat in de projectdocumentatie.
- Bewijs: Een tabel in de projectdocumentatie met per gegevensstroom: betrokkenen, gegevens, verantwoordelijke, verwerker, subverwerkers. Afgevinkt als elke tabel met persoonsgegevens uit de classificatie (DB-87) in precies één rij valt. Niet technisch af te dwingen; de tabel is het bewijs. [jurist] bij twijfel over gezamenlijke verantwoordelijkheid.
- Norm: AVG artikel 4 punt 7 en 8, artikel 24, artikel 28 lid 10.
- Zie ook: ARCH-80, ARCH-81, PRIV-37, PRIV-59

### PRIV-02 Het verwerkingsregister bevat per activiteit de wettelijke velden
hoog · hard · alles · tegenlezer: scherpen (04-10-2026)
- Regel: Zorg dat elke activiteit in `policy-state.yaml` (of het register van het project) de velden van artikel 30 lid 1 heeft: doel, categorieën van betrokkenen en van gegevens, ontvangers en subverwerkers, doorgifte buiten de EER met het land, de bewaartermijn, en een verwijzing naar de beveiligingsmaatregelen; zet de naam en de contactgegevens van de verwerkingsverantwoordelijke (artikel 30 lid 1 onder a) één keer bovenaan het register.
- Bewijs: Een script dat het YAML-bestand laadt en per activiteit controleert dat de zeven velden bestaan en niet leeg zijn; de uitvoer is leeg. Afgevinkt met de uitvoer. Technisch af te dwingen als gate in de repo van het register.
- Norm: AVG artikel 30 lid 1 en lid 5; ASVS 5.0.0 V14.1.1 (L2).

### PRIV-03 Werk het register bij in dezelfde wijziging als de nieuwe gegevensstroom
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Voeg bij elke wijziging die een nieuwe ontvanger van persoonsgegevens, een nieuw gegevensveld, een nieuw doel of een andere bewaartermijn invoert, de bijbehorende wijziging van `policy-state.yaml` toe voordat de code live gaat, en noem die in het opleverbericht.
- Bewijs: (1) De lijst van externe hosts uit API-51 en WEB-59 (`grep -rnoE "https://[a-z0-9.-]+" src | sort -u`, en de hostlijst uit Playwright) is vergeleken met `subprocessors:`; elk verschil is verklaard. (2) De kopregel "Laatste handmatige update" in `policy-state.yaml` heeft de datum van de oplevering, of het opleverbericht zegt "geen nieuwe gegevensstroom". Afgevinkt met de vergelijking. Technisch af te dwingen als controle in de oplevering. Openstaand (besluit van Marketing Maatwerk, 04-10-2026, OPEN-VRAGEN A31): Discord en Slack ontvangen meldingen met bedrijfs- en contactnamen en moeten nog als subverwerker in `policy-state.yaml`; dat gebeurt in een eigen sessie met akkoord per wijziging (A20). De inhoud van de meldingen is niet gemeten.
- Norm: AVG artikel 5 lid 2, artikel 30; ASVS 5.0.0 V14.2.3 (L2).
- Zie ook: AI-66, PRIV-83, PRIV-14, PRIV-18, AI-72, PRIV-12, AI-65

### PRIV-04 Houd als verwerker een eigen register per klant bij
middel · richtlijn · klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd voor elke klant voor wie je verwerker bent (hosting, onderhoud, tenant in een SaaS) bij welke categorieën verwerkingen je uitvoert, welke subverwerkers je inzet, of er doorgifte buiten de EER is, en welke beveiliging geldt.
- Bewijs: Een overzicht per klant (in het CRM of een bestand) met: dienst, soorten gegevens op de site of in de tenant, subverwerkers, datum verwerkersovereenkomst. Afgevinkt als elke actieve hosting- of onderhoudsklant een rij heeft. Niet technisch af te dwingen; een telling klanten tegen rijen is het bewijs.
- Norm: AVG artikel 30 lid 2.

### PRIV-05 De privacyverklaring klopt met wat de code doet
hoog · hard · website | app | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer bij elke oplevering die gegevens verzamelt dat de privacyverklaring de identiteit van de verantwoordelijke, het doel en de grondslag, de ontvangers, doorgifte buiten de EER, de bewaartermijn en de rechten van de betrokkene noemt voor precies deze verwerking, en dat de verklaring bereikbaar is op het moment van verzamelen.
- Bewijs: (1) Bij elk formulier staat een link naar de verklaring of een korte regel onder de knop; een e2e-test vindt de link. (2) Een vergelijking van `data_types`, `subprocessors` en `retention` uit het register met de tekst van de verklaring; de automatische vergelijking meldt geen verschil. Afgevinkt met de testuitvoer en de laatste uitvoer van die vergelijking.
- Norm: AVG artikel 12 lid 1, artikel 13 lid 1 en 2, artikel 5 lid 1 onder a.

### PRIV-06 Bewaar het bewijs van elke privacykeuze bij het project
middel · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg elke keuze met een privacykant (grondslag, termijn, leverancier, afgewezen alternatief, uitzondering op een regel uit dit domein) vast met datum en wie besloot, op een vaste plek in de repo of het register.
- Bewijs: Een bestand `docs/privacy.md` of de `note:` in het register bevat per keuze een datum en een reden; de overrule-uitzonderingen uit besluit 2 van de brief staan er ook. Afgevinkt als het bestand bestaat en de laatste wijziging in git niet ouder is dan de laatste wijziging aan de gegevensstroom.
- Norm: AVG artikel 5 lid 2, artikel 24 lid 1.
