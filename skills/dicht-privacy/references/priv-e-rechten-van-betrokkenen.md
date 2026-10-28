# PRIV E: rechten van betrokkenen

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-26 Een inzageverzoek is binnen een maand te beantwoorden met een getest script
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd per systeem een export bij die alle gegevens van één persoon verzamelt uit alle tabellen, bestanden, logs met een identificator en afgeleide gegevens, in een leesbaar formaat, samen met de vaste informatie over doelen, ontvangers, termijnen en herkomst.
- Bewijs: Dezelfde test als DB-84, maar lezend: een testpersoon met gegevens in elke relevante tabel, het script draait, en de uitvoer bevat elk geplant gegeven. Afgevinkt met de testuitvoer. Technisch af te dwingen. De uitzonderingen (rechten van anderen, interne notities): `[jurist]`.
- Norm: AVG artikel 12 lid 3, artikel 15 lid 1 en 3.
- Zie ook: PRIV-21, DB-83, DB-84, PRIV-24, DB-78, AI-70, PRIV-22

### PRIV-27 Controleer de identiteit van een verzoeker zonder kopie van een identiteitsbewijs
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel de identiteit van iemand die een verzoek doet vast met wat je al hebt: laat een ingelogde gebruiker het verzoek in zijn account doen, of stuur een bevestigingslink naar het bekende e-mailadres; vraag geen kopie van een identiteitsbewijs als standaard.
- Bewijs: De procedure in `docs/privacy.md` beschrijft de twee routes; een test laat zien dat de export alleen start na login of na het volgen van een eenmalige link naar het geregistreerde adres (eigenschappen van die link: AUTH, resettokens). Afgevinkt met procedure en test.
- Norm: AVG artikel 12 lid 2 en 6, artikel 5 lid 1 onder c.

### PRIV-28 Bezwaar tegen direct marketing werkt direct en blijvend
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwerk een afmelding of bezwaar tegen marketing meteen en zonder voorwaarden, zet het adres op een lijst die blijft bestaan, en controleer die lijst vóór elke verzending, ook in andere kanalen en producten van hetzelfde bedrijf. Aanvulling uit MSG-10: Schrijf de afmelding in dezelfde aanroep naar de afmeldlijst en laat de verzendfunctie de lijst raadplegen op het moment van versturen, niet bij het klaarzetten; Google en Yahoo noemen 48 uur als uiterste grens.
- Bewijs: Een test per verzendlijn: zet een testadres op de lijst en probeer te verzenden via elke lijn; geen enkele verzendt. `grep` laat zien dat elke verzendfunctie dezelfde controle aanroept. Afgevinkt met de testuitvoer. Technisch af te dwingen.
    Ook (uit MSG-10): Een test: zet een bericht klaar, meld het adres af, laat de verzendfunctie lopen; er wordt niets verstuurd en de uitkomst is `afgemeld`. Afgevinkt met de testuitvoer. De lijst zelf en de blijvende werking: PRIV-28.
- Norm: AVG artikel 21 lid 2 en 3; Telecommunicatiewet artikel 11.7.
- Dekt ook: MSG-10
- Zie ook: PRIV-48, MSG-07, MSG-08, MSG-09, MSG-13, MSG-49

### PRIV-29 Lever gegevens die een klant zelf aanleverde ook machineleesbaar terug
laag · richtlijn · app | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Bied in elke toepassing waarin gebruikers op basis van toestemming of een overeenkomst gegevens invoeren een export in een gangbaar machineleesbaar formaat (CSV of JSON) voor hun eigen gegevens.
- Bewijs: Een e2e-test die als gebruiker de export start en het bestand inleest; de export is veilig tegen formule-injectie (WEB-65, API-59) en valt onder dezelfde autorisatie als de gegevens (AUTH-69). Afgevinkt met de testuitvoer.
- Norm: AVG artikel 20 lid 1.

### PRIV-30 Geef als verwerker de klant het gereedschap om verzoeken af te handelen
middel · hard · wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur een verzoek van een betrokkene dat bij jou als verwerker binnenkomt door naar de klant en beantwoord het niet zelf, en lever in elk product de functies waarmee de klant kan inzien, corrigeren, exporteren en wissen per persoon.
- Bewijs: Voor een WP-plugin: `grep -rn "wp_privacy_personal_data_exporters\|wp_privacy_personal_data_erasers"` vindt beide filters, en een test met een testgebruiker laat zien dat export en wissing de eigen tabel meenemen. Voor een SaaS: de functies bestaan per contact en per tenant en zijn getest. Afgevinkt met grep en test. Technisch af te dwingen.
- Norm: AVG artikel 28 lid 3 onder e.
