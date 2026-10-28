# MSG B: Afmelden, bounces en klachten

Compacte regels van `dicht-berichten`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/email-berichten-bots.md` (regelnummer in `regel-index.tsv`).

### MSG-07 Bouw afmelden in één klik precies volgens RFC 8058
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in elke nieuwsbrief en elke reclamemail `List-Unsubscribe: <https://...>` met precies één HTTPS-adres en `List-Unsubscribe-Post: List-Unsubscribe=One-Click`, laat de DKIM-handtekening beide koppen dekken, en laat het adres een POST zonder cookie, login of CSRF-token verwerken.
- Bewijs: `curl -s -o /dev/null -w "%{http_code}" -X POST -d "List-Unsubscribe=One-Click" <adres uit een ontvangen testbericht>` geeft 200 zonder cookie; daarna staat het testadres op de afmeldlijst (query); `h=` in de handtekening bevat beide koppen. Afgevinkt met de uitvoer, de query en de koppen.
- Norm: Telecommunicatiewet artikel 11.7 (zie PRIV-48); geen ASVS-eis.
- Zie ook: INFRA-63, MSG-02, MSG-03, MSG-11, MSG-13, MSG-15, INFRA-58, PRIV-28, PRIV-48, MSG-08, MSG-09, MSG-49

### MSG-08 Meld niemand af op een GET
middel · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een GET op de afmeldlink alleen een pagina met een bevestigingsknop tonen; de afmelding zelf gebeurt uitsluitend op een POST.
- Bewijs: `curl -s <afmeldlink>` (GET) verandert de afmeldlijst niet (query voor en na); alleen de POST doet dat. Afgevinkt met de twee query's.
- Norm: geen ASVS-eis; dezelfde gedachte als "geen wijziging op GET" in WEB (CSRF).
- Zie ook: PRIV-28, PRIV-48, MSG-07, MSG-09, MSG-13, MSG-49

### MSG-09 Maak het afmeldadres onraadbaar en bind het aan één ontvanger en één lijst
hoog · hard · api | app | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Zet in het afmeldadres een willekeurig of ondertekend token dat ontvanger en lijst vastlegt, en nooit het e-mailadres of een oplopend nummer als enige gegeven; controleer het token op de server.
- Bewijs: Het token heeft minstens 128 bit willekeur of is een HMAC over ontvanger en lijst; een POST met een gewijzigd token geeft 404 of 400 en wijzigt niets; het antwoord is gelijk voor bestaande en onbestaande adressen. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V14.2.1 (L1, geen gevoelige gegevens in het adres) naar de geest.
- Zie ook: PRIV-28, PRIV-48, MSG-07, MSG-08, MSG-13, MSG-49

### MSG-10 → PRIV-28
Samengevoegd: "Verwerk een afmelding direct en controleer de lijst vlak voor het versturen" is gedekt door PRIV-28. Gebruik die regel.

### MSG-11 Lees een bounce als afleverrapport en stop na een blijvende fout
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Herken een bounce aan het MIME-type `multipart/report` met `report-type=delivery-status`, lees `Status` en `Action` uit het deel `message/delivery-status`, zet een adres met een statuscode die met 5 begint op de niet-meer-mailen-lijst, en probeer een code die met 4 begint hooguit een vast aantal keren opnieuw.
- Bewijs: Een test met drie opgeslagen voorbeeldberichten (een DSN met `Status: 5.1.1`, een DSN met `Status: 4.2.2`, een afwezigheidsmelding): de eerste zet het adres op de lijst, de tweede verhoogt een teller, de derde doet geen van beide. Afgevinkt met de testuitvoer.
- Norm: geen ASVS-eis.
- Zie ook: INFRA-63, MSG-02, MSG-03, MSG-07, MSG-13, MSG-15, INFRA-58

### MSG-12 Geef elke stroom een afzender op de envelop die gelezen wordt
middel · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Verstuur elk bericht met een geldig envelopadres (`MAIL FROM`) op het eigen domein dat uitkomt bij de bounceverwerker van die stroom, en gebruik de lege afzender `<>` alleen voor afleverrapporten.
- Bewijs: De kop `Return-Path` van een ontvangen bericht per stroom toont het bedoelde adres; een testmail naar een niet-bestaand adres op het eigen domein levert binnen een uur een verwerkte bounce op in het logboek van die stroom. Afgevinkt met de kop en de logregel.
- Norm: geen ASVS-eis.
- Zie ook: MSG-01, MSG-16, INFRA-64, MSG-02, WEB-68

### MSG-13 Behandel een klacht als een afmelding
middel · richtlijn · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Meld het DKIM-domein van elke verzendstroom aan voor de klachtenlus van ontvangers die er een bieden, en zet het adres uit een binnengekomen klachtrapport direct op de afmeldlijst.
- Bewijs: De aanmelding bij de klachtenlus per domein (schermafdruk of bevestigingsmail met datum); een test met een opgeslagen rapport van het type `message/feedback-report` zet het adres op de lijst. Afgevinkt met de aanmelding en de testuitvoer.
- Norm: geen ASVS-eis.
- Zie ook: INFRA-63, MSG-02, MSG-03, MSG-07, MSG-11, MSG-15, INFRA-58, PRIV-28, PRIV-48, MSG-08, MSG-09, MSG-49

### MSG-14 → SCR-45
Samengevoegd: "Herhaal een onzekere verzending niet blind" is gedekt door SCR-45. Gebruik die regel.

### MSG-15 Bouw volume geleidelijk op en verlaag het bij uitstel of weigering
middel · richtlijn · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Verhoog het dagvolume van een nieuwe stroom of een nieuw afzenderdomein in stappen, en verlaag het zodra de ontvangende servers tijdelijke fouten (4xx) of weigeringen gaan geven, tot het foutpercentage weer daalt.
- Bewijs: Het dagplafond per stroom staat in de configuratie met de datum van de laatste verhoging; het logboek telt per dag verstuurd, uitgesteld (4xx) en geweigerd (5xx); er is een drempel waarbij de lijn pauzeert. Afgevinkt met de configuratie en een dagtelling.
- Norm: geen ASVS-eis.
- Zie ook: INFRA-63, MSG-02, MSG-03, MSG-07, MSG-11, MSG-13, INFRA-58

### MSG-49 Ontdubbel ontvangers over alle verzendlijnen op genormaliseerd adres en domein
hoog · hard · api | app | klantproject · eigen bron · tegenlezer: niet tegengelezen
- Regel: Controleer vóór de eerste mail aan een nieuwe ontvanger of het adres of het domein al voorkomt bij een eerder benaderde ontvanger in welke verzendlijn dan ook of in het CRM; vergelijk op het genormaliseerde adres (kleine letters, zonder spaties eromheen) en het genormaliseerde domein (kleine letters, zonder `www.`, zonder streepjes en punten vóór de extensie); verstuur niet bij een treffer maar zet de ontvanger ter beoordeling, en verstuur ook niet als één van de bronnen niet te raadplegen is.
- Bewijs: De lijst van bronnen (elke verzendlijn, het CRM, en de afmeldlijst van PRIV-28) staat in de projectdocumentatie. Tests: (1) een adres dat alleen in hoofdletters verschilt van een eerder benaderd adres uit een andere lijn wordt niet gemaild; (2) een domein dat alleen in een streepje verschilt wordt niet gemaild en staat ter beoordeling; (3) is een bron onbereikbaar, dan wordt er niets verstuurd (SCR-46). Afgevinkt met de lijst en de testuitvoer.
- Norm: geen ASVS-eis die dit letterlijk vraagt; ASVS 5.0.0 V2.3.2 (L2, grenzen van bedrijfslogica) naar de geest.
- Eigen bron: geen primaire bron; de eis komt uit een eigen incident (04-08-2026, eigen ervaring); geen primaire bron gevonden. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Zie ook: ARCH-76, AI-79, AI-26, PRIV-51, ARCH-77, SCR-46, BIZ-23, SCR-52, PRIV-28, PRIV-48, MSG-07, MSG-08, MSG-09, MSG-13
