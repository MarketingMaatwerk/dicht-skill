# PRIV C: verwerkers, subverwerkers en doorgifte

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-14 Geen echte persoonsgegevens naar een leverancier zonder verwerkersovereenkomst
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Sluit met elke leverancier die namens jou persoonsgegevens verwerkt (hosting, mail, AI-model, spamfilter, boekhouding, back-upopslag) een verwerkersovereenkomst voordat de eerste echte gegevens erheen gaan, en leg in het register vast welk document het is, van welke datum en waar het te vinden is.
- Bewijs: Elke rij onder `subprocessors:` heeft de velden document, datum en vindplaats (URL of bestandspad); een script meldt rijen zonder datum. Afgevinkt met de scriptuitvoer. Technisch af te dwingen op het register; de inhoud van de overeenkomst (de acht onderdelen van artikel 28 lid 3) is `[jurist]`. Openstaand (besluit van Marketing Maatwerk, 04-10-2026, OPEN-VRAGEN A31): Discord en Slack staan nog niet onder `subprocessors:`; ze moeten erbij met document, datum en vindplaats, en met het doorgifte-instrument (PRIV-18; de juridische kant is J14).
- Norm: AVG artikel 28 lid 1, 3 en 9.
- Zie ook: AI-66, PRIV-83, PRIV-18, AI-72, PRIV-12, AI-65, PRIV-03

### PRIV-15 Bied als verwerker zelf een overeenkomst aan, met een subverwerkerlijst die je bijhoudt
hoog · hard · app | klantproject | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Lever bij elke dienst waarin je voor een klant persoonsgegevens verwerkt (hosting, onderhoud, een SaaS-tenant) een verwerkersovereenkomst mee met een actuele lijst van subverwerkers, en informeer klanten vóór je een subverwerker toevoegt of vervangt, met een termijn om bezwaar te maken.
- Bewijs: (1) Een publieke of bij de klant bekende subverwerkerlijst met datum. (2) Een vaste stap in de release: bij een wijziging van `subprocessors:` voor een product met klanten hoort een bericht aan die klanten (als concept voor Marketing Maatwerk, gouden regel) met de ingangsdatum. Afgevinkt met de lijst en, bij een wijziging, het bericht.
- Norm: AVG artikel 28 lid 2 en 4.

### PRIV-16 Gebruik gegevens van klanten van klanten nooit voor eigen doelen
hoog · hard · app | klantproject | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwerk gegevens die je als verwerker onder je hebt uitsluitend voor de dienst aan die klant: geen eigen analyses over tenants heen, geen hergebruik voor acquisitie, geen gebruik als test- of trainingsmateriaal, tenzij de overeenkomst het uitdrukkelijk toestaat.
- Bewijs: De rollen uit DB-02 en DB-14 laten zien dat geen beheer- of analysedienst tenantinhoud kan lezen buiten de supportroute van AUTH-79; `grep` in tests en fixtures op e-mailadressen buiten het eigen testdomein is leeg (eigen ervaring). Afgevinkt met beide. Technisch af te dwingen.
- Norm: AVG artikel 28 lid 3 onder a en lid 10, artikel 32 lid 4.

### PRIV-17 Einde van de opdracht: teruggeven of wissen, ook de kopieën
hoog · hard · klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak per dienst een afsluitprocedure die bij het einde van een klantrelatie de gegevens teruglevert in een bruikbaar formaat of wist, inclusief back-ups na hun termijn, lokale werkkopieën, testomgevingen, exports en afgeleide gegevens zoals embeddings.
- Bewijs: Een script of checklist `afsluiten-klant` dat per klant alle plekken afloopt (hosting, back-uplocaties, lokale mappen, testomgeving, CRM-bijlagen, vectoropslag), met een proefrun op een testklant waarna een zoekactie op de klantnaam en het domein niets meer vindt buiten de administratie (PRIV-90). Afgevinkt met de uitvoer van de proefrun. Let op: verwijderen op live systemen vraagt akkoord van Marketing Maatwerk.
- Norm: AVG artikel 28 lid 3 onder g; zie AI-70 en DB-84.

### PRIV-18 Leg per leverancier vast in welk land de gegevens komen en op grond waarvan
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Noteer per subverwerker het land van verwerking en, buiten de EER, het doorgifte-instrument (adequaatheidsbesluit met het bewijs van deelname, of standaardbepalingen), controleer voor een Amerikaanse leverancier of het gebruikte product onder het Data Privacy Framework valt, en kies bij gelijke geschiktheid een leverancier die in de EER verwerkt.
- Bewijs: Elke rij onder `subprocessors:` heeft `location` en, buiten de EER, `transfer_basis` met een link naar het bewijs (de vermelding op de deelnemerslijst of de bepalingen in de overeenkomst) en een datum van controle; de verversroutine per kwartaal controleert de stand van zaak C-703/25 P. Afgevinkt met het register. In het eigen register hebben de Amerikaanse rijen een `transfer_basis`, zonder link of controledatum.
- Norm: AVG artikel 44, 45 en 46, artikel 13 lid 1 onder f, artikel 30 lid 1 onder e.
- Zie ook: AI-66, PRIV-83, PRIV-14, AI-72, PRIV-12, AI-65, PRIV-03

### PRIV-19 Een script, lettertype of ingesloten dienst van een derde is ook een ontvanger
middel · hard · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Behandel elke host van een derde die de browser van de bezoeker aanroept (lettertypen, kaarten, video, captcha, analytics, chat) als ontvanger van ten minste het IP-adres: host het zelf, of neem de partij op in het register en de verklaring en laad haar pas na toestemming als de wet dat vraagt (PRIV-40).
- Bewijs: De hostlijst uit WEB-58 per paginatype, met per host: zelf gehost, in het register, of pas na toestemming. Afgevinkt als geen host buiten die drie valt. Technisch af te dwingen met de CSP (WEB-11) en de Playwright-hostlijst.
- Norm: AVG artikel 4 punt 1 en 9, artikel 13 lid 1 onder e; ASVS 5.0.0 V14.2.3 (L2).
- Zie ook: WEB-59, WEB-58, PRIV-46, PRIV-40

### PRIV-20 Toegang van de bouwer tot klantsystemen is persoonlijk, minimaal en gelogd
middel · hard · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Werk op klantsites en in klantsystemen met een eigen, herleidbaar account of sleutel, haal alleen de gegevens op die de klus nodig heeft, maak geen lokale kopie van een database met persoonsgegevens zonder einddatum, en noteer wat je hebt gedaan.
- Bewijs: Per klus een notitie op het klantprofiel (de notitieregel van het CRM) met wat is opgehaald; `find ~/klanten -name "*.sql*" -mtime +30` en dezelfde zoekactie op `.wpress` en `.zip` in werkmappen is leeg of verklaard. Afgevinkt met de zoekuitvoer.
- Norm: AVG artikel 28 lid 3 onder b, artikel 32 lid 4; zie AUTH-85 en INFRA voor sleutels.
