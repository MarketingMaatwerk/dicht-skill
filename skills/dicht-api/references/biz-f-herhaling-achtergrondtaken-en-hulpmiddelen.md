# BIZ F: herhaling, achtergrondtaken en hulpmiddelen

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/bedrijfslogica-gelijktijdigheid.md` (regelnummer in `regel-index.tsv`).

### BIZ-39 Bind een idempotentiesleutel aan de eigenaar, de route en de inhoud, en ken de toestand "in behandeling"
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Sla een idempotentiesleutel (API-33) op met de tenant of gebruiker, de route en een hash van de body; geef bij dezelfde sleutel met een andere eigenaar, route of body een fout, geef bij een tweede verzoek terwijl het eerste nog loopt 409, en bewaar de sleutel langer dan de langste herhaling van de afzender.
- Bewijs: Tests: dezelfde sleutel van een andere tenant voert het verzoek gewoon uit als nieuw en geeft niets van de eerste terug; dezelfde sleutel met een andere body geeft 422 of 400; twee gelijktijdige verzoeken met dezelfde sleutel geven één uitvoering en één 409; een rij die langer dan de time-out op "bezig" staat wordt volgens BIZ-42 behandeld. De bewaartermijn staat in de documentatie en in de opruimjob.
- Norm: ASVS 5.0.0 V2.3.3 (L2), V15.4.2 (L3). Zie API-33, DB-68, AUTH-74.
- Zie ook: API-31, BIZ-30, BIZ-34, BIZ-35, BIZ-41, BIZ-43, BIZ-46, API-33, DB-68

### BIZ-40 Een time-out is "onbekend", niet "mislukt"
hoog · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke uitgaande handeling met een effect (betaling, terugbetaling, factuur, registratie, verzending) naast geslaagd en mislukt de uitkomst "onbekend" voor een time-out of een verbroken verbinding na het versturen; herhaal bij "onbekend" alleen met dezelfde idempotentiesleutel binnen de geldigheid ervan, en vraag anders eerst bij de ontvanger na of de handeling is uitgevoerd; blijft het onbekend, parkeer de taak dan voor een mens.
- Bewijs: Het statusveld van elke uitgaande taak kent "onbekend". Test met een nagebootste dienst die het verzoek uitvoert en daarna de verbinding verbreekt: er ontstaat geen tweede handeling. Test: een "onbekend" ouder dan de geldigheid van de sleutel leidt tot navragen, niet tot herhalen. De verzendlijnen van Marketing Maatwerk hebben deze regel al: na een onzekere verzending gaat de lijn alleen na akkoord weer aan.
- Norm: ASVS 5.0.0 V2.3.3 (L2), V16.5.2 (L2). Zie API-41, API-49, ARCH-18.
- Zie ook: SCR-45, API-41, API-49, ARCH-18

### BIZ-41 Voorkom dubbele facturen in Moneybird met een eigen claim, want Moneybird kent geen idempotentiesleutel
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg vóór het aanmaken van een factuur, creditfactuur of betaling in Moneybird een rij vast met een unieke sleutel op de zakelijke handeling (bestelling en soort document), zet een eigen referentie op het document waarmee je het kunt terugvinden, sla het Moneybird-id op in die rij, en zoek bij een onbekende uitkomst (BIZ-40) eerst op die referentie voordat je opnieuw aanmaakt.
- Bewijs: `\d documenten` toont de unieke index op (bestelling, soort) en een unieke index op het Moneybird-id. Test met een nagebootste Moneybird-API: de taak twee keer tegelijk en een crash na de POST geven samen één document. Het herstelpad voor een rij die op "aanmaken" blijft staan zoekt op de referentie en maakt niets nieuws als het document bestaat. De ontbrekende idempotentiesleutel is vastgesteld met `grep -ci idempot` op de OpenAPI-specificatie van Moneybird (nul treffers op 04-10-2026); controleer dat bij de verversronde opnieuw.
- Norm: ASVS 5.0.0 V2.3.3 (L2), V2.3.4 (L2). Zie API-31, API-38, BIZ-08.
- Zie ook: API-31, BIZ-30, BIZ-34, BIZ-35, BIZ-39, BIZ-43, BIZ-46, API-33, DB-68, BIZ-48, BIZ-49, API-43, BIZ-51

### BIZ-42 Geef een geclaimde taak een huurtermijn
middel · hard · api | app | mcp · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Als een worker een taak claimt door hem een status "bezig" te geven en de transactie af te sluiten, sla dan op tot wanneer de claim geldt, laat een verlopen claim door een andere worker opnieuw oppakken, en maak de taak bestand tegen die tweede uitvoering (ARCH-18); kies de termijn langer dan de langste normale uitvoering inclusief de time-outs van API-48.
- Bewijs: Test: claim een taak, laat de worker niets doen, zet de klok voorbij de termijn; een tweede worker pakt hem op en het effect treedt één keer op. Controlequery in de bewaking: geen taak staat langer dan de termijn op "bezig" (alarm, ARCH-69). Het aantal pogingen telt mee voor de dode-brievenbak (ARCH-19).
- Norm: ASVS 5.0.0 V15.4.3 (L3), V2.3.3 (L2). Zie DB-71, DB-73, ARCH-18, ARCH-19, ARCH-21.
- Zie ook: ARCH-19, API-23, DB-71, ARCH-18, ARCH-20

### BIZ-43 Maak een MCP-tool met een zakelijk effect idempotent op de zakelijke sleutel
middel · hard · mcp · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Laat een tool die iets aanmaakt of in gang zet (factuur uit een offerte, taak, concept, betaling registreren) dubbele uitvoering weigeren op basis van de zakelijke sleutel in de database (één factuur per offerte, één betaling per factuur en bedrag en datum), niet op basis van een sleutel die het model moet meesturen; zet `idempotentHint` alleen op `true` als dat ook echt zo is.
- Bewijs: Per tool met een effect: een test die hem twee keer achter elkaar en twee keer tegelijk aanroept met dezelfde argumenten en één resultaat in de database verwacht. De tooldefinitie: `idempotentHint: true` komt alleen voor bij tools met zo'n test. Zie AI-50: annotaties zijn een hint, geen beveiliging.
- Norm: ASVS 5.0.0 V2.3.3 (L2), V2.3.4 (L2). Zie API-31, API-33, AI-50, AI-52.
- Zie ook: API-31, BIZ-30, BIZ-34, BIZ-35, BIZ-39, BIZ-41, BIZ-46, API-33, DB-68, AI-50

### BIZ-44 WordPress: houd geen teller, limiet of slot bij met opties of meta
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor een teller, een saldo, een daglimiet of een slot in een plugin of thema nooit `get_option` gevolgd door `update_option`, `get_post_meta` gevolgd door `update_post_meta`, of `get_transient` gevolgd door `set_transient`; schrijf één SQL-statement dat zelf rekent en de grens bewaakt (`UPDATE ... SET n = n + 1 WHERE n < max` via `$wpdb->query` met `prepare`, en controleer het aantal geraakte rijen), of een eigen tabel met een unieke sleutel.
- Bewijs: `grep -rnE "update_option|update_post_meta|update_user_meta|set_transient" .` in de plugin: geen treffer schrijft een waarde die uit een eerdere `get_` is berekend en die een limiet, saldo, voorraad of slot voorstelt. Test in de wegwerpomgeving (ARCH-47): 30 gelijktijdige verzoeken met `curl --parallel` tegen de limiet van 20 geven precies 20 keer succes. Zie WP-16 voor `prepare`.
- Norm: ASVS 5.0.0 V2.3.4 (L2), V15.4.2 (L3); CWE-362.
- Zie ook: API-30, BIZ-01, BIZ-02, BIZ-03, BIZ-04, BIZ-05, BIZ-06, BIZ-07, BIZ-09, BIZ-50

### BIZ-45 WooCommerce: gebruik de ingebouwde voorraad- en bonlimieten en bouw ze niet na
middel · richtlijn · wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat voorraad, het vasthouden van voorraad voor onbetaalde bestellingen en limieten op kortingsbonnen door WooCommerce zelf afhandelen (voorraadbeheer aan, "Hold stock (minutes)" ingevuld, "Usage limit per coupon", "Usage limit per user" en "Individual use only" per bon), en schrijf geen eigen code die voorraad of bongebruik bijhoudt naast WooCommerce.
- Bewijs: `wp option get woocommerce_manage_stock` en `wp option get woocommerce_hold_stock_minutes` (alleen lezen) tonen "yes" en een getal. Elke bon met waarde heeft een limiet; een bon zonder limiet staat met reden in de documentatie. `grep -rnE "wc_update_product_stock|set_stock_quantity|_usage_count" .` in eigen code is leeg of beoordeeld.
- Norm: ASVS 5.0.0 V2.3.4 (L2), V2.3.2 (L2). Zie WP-83.
