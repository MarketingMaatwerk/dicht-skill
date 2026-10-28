# MSG G: Web push

Compacte regels van `dicht-berichten`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/email-berichten-bots.md` (regelnummer in `regel-index.tsv`).

### MSG-46 Behandel een push-abonnement als geheim van één gebruiker en als onvertrouwd adres
middel · hard · app | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Sla een push-abonnement (adres en sleutels) alleen op bij de ingelogde gebruiker die het aanlevert, toon het nooit aan anderen, en stuur alleen naar een adres met `https` op een host uit een vaste lijst van push-diensten van browsers.
- Bewijs: Een test die een abonnement met een adres buiten de lijst aanbiedt en een validatiefout verwacht; een test met twee gebruikers toont dat de een het abonnement van de ander niet kan lezen of overschrijven (AUTH-63). De lijst van toegestane hosts staat in de configuratie. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V1.3.6 (L2), V13.2.4 (L2).
- Zie ook: WEB-40, WEB-41, API-48, API-47, AI-48, WP-28, INFRA-18, INV-59, INV-61, MSG-27

### MSG-47 Verwijder een abonnement bij 404 of 410 en houd de VAPID-sleutel op de server
laag · hard · app | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwijder een push-abonnement zodra de push-dienst 404 of 410 antwoordt, bewaar de private VAPID-sleutel alleen in het geheimenbestand van de server, en geef het VAPID-token een `exp` van hooguit 24 uur.
- Bewijs: Een test met een nagebootste 410: de rij is weg; `grep -rn "VAPID" <frontend>` toont alleen de publieke sleutel; de code die het token maakt, zet `exp` op hooguit 24 uur. Afgevinkt met de testuitvoer en grep.
- Norm: ASVS 5.0.0 V13.3.1 (L2).

### MSG-48 Zet geen gevoelige inhoud in een melding
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in een pushmelding, een Discord- of Slack-melding en de onderwerpregel van een notificatiemail alleen dat er iets is en waar, niet de inhoud zelf: geen codes, geen tokens, geen berichttekst van een klant, geen persoonsgegevens buiten wat nodig is om de melding te begrijpen.
- Bewijs: Per meldstroom een voorbeeld van een echte melding: hij bevat een soort, een verwijzing (taak-ID, naam van het kanaal) en hooguit een naam; `grep` op de meldcode toont geen velden als `body`, `tekst`, `token` of `code` in het bericht. Discord en Slack zijn subverwerker (besluit van Marketing Maatwerk, 04-10-2026: in de meldingen staan bedrijfs- en contactnamen) en moeten nog onder `subprocessors:` in `policy-state.yaml` (PRIV-03, PRIV-14); dat is niet gedaan. Wat er feitelijk in de meldingen staat is niet gemeten; dat gebeurt in de sessie die het register bijwerkt (OPEN-VRAGEN A20 en A31). Afgevinkt met de voorbeelden.
- Norm: AVG artikel 5 lid 1 onder c en artikel 32 (zoals uitgewerkt in PRIV; hier niet opnieuw nagelezen); ASVS 5.0.0 V14.1.1 (L2, gevoelige gegevens geclassificeerd) naar de geest.
