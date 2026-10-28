# PRIV G: DPIA en functionaris gegevensbescherming

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-37 Doe bij elk nieuw project een DPIA-toets van vijf minuten en leg de uitkomst vast
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Loop bij elk nieuw project en elke nieuwe verwerking de lijst van de AP en de drie gevallen van artikel 35 lid 3 langs en noteer "DPIA nodig: ja of nee, omdat"; bij ja gaat er geen echte verwerking live vóór de DPIA klaar is.
- Bewijs: In `docs/privacy.md`: de datum van de toets, de punten van de lijst die raken, en de conclusie. Voor de verwerker: de toets is ook nuttig, want de klant moet de DPIA doen en "de verwerker [moet] u ondersteunen bij het uitvoeren van de DPIA" (AP). Afgevinkt met de notitie. Of iets "grootschalig" is: `[jurist]`.
- Norm: AVG artikel 35 lid 1, 3 en 4; AP-lijst (Stcrt. 2019, 64418).
- Zie ook: ARCH-80, ARCH-81, PRIV-59, PRIV-01

### PRIV-38 Bij zorgdata is de DPIA een bouwdocument dat meeloopt met de code
hoog · hard · app | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd bij een project met gezondheidsgegevens de DPIA, het register en de lijst van subverwerkers bij in dezelfde wijziging als de code die een gegevensstroom toevoegt of verandert, en zet geen nieuwe stroom aan met echte gegevens vóór de documenten zijn bijgewerkt.
- Bewijs: De regel staat in de `CLAUDE.md` van het project; `git log` laat zien dat wijzigingen aan integraties samen met `docs/PRIVACY-SECURITY.md` of `SUBVERWERKERS.md` zijn gecommit. Afgevinkt met de log van de laatste drie integratiewijzigingen.
- Norm: AVG artikel 35 lid 1 en 3 onder b, artikel 36; zie AI-72.

### PRIV-39 Toets of een functionaris gegevensbescherming verplicht is
middel · richtlijn · app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per organisatie waarvoor je bouwt (ook als je verwerker bent) vast of ze hoofdzakelijk belast is met grootschalige verwerking van bijzondere gegevens of met stelselmatige observatie op grote schaal; zo ja, dan hoort er een functionaris te zijn en neem je zijn contactgegevens op in het register en de datalekprocedure.
- Bewijs: De toets staat in de projectdocumentatie met datum en conclusie. Afgevinkt met de notitie. `[jurist]` voor de conclusie; de grens van "grootschalig" is niet uit een primaire bron bevestigd.
- Norm: AVG artikel 37 lid 1 onder b en c.
