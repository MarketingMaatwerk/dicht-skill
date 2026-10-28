# BIZ B: geld, btw en afronding

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/bedrijfslogica-gelijktijdigheid.md` (regelnummer in `regel-index.tsv`).

### BIZ-10 Rond btw rekenkundig af op hele centen, volgens één vastgelegde methode
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Rond het btw-bedrag af op hele centen met de rekenkundige methode (derde decimaal 5 of hoger naar boven), kies per project één van de twee toegestane methodes (per regel of op het totaal), leg die keuze vast en gebruik overal dezelfde, ook in het bedrag dat naar Mollie gaat en in de factuur in Moneybird.
- Bewijs: De gekozen methode staat in de projectdocumentatie. Unit-test met de tabel uit BIZ-52 (onder meer 20,124 wordt 20,12 en 20,125 wordt 20,13, het voorbeeld van de Belastingdienst). Integratietest of handmatige controle met datum: voor drie bestellingen met meerdere regels is het totaal in de eigen database, bij Mollie en op de Moneybird-factuur tot op de cent gelijk.
- Norm: Belastingdienst, btw-bedrag afronden; ASVS 5.0.0 V2.2.3 (L2).
- Zie ook: DB-75, API-28, API-27, BIZ-11, BIZ-12, BIZ-17

### BIZ-11 Maak van een numeric uit de database geen JavaScript-getal om mee te rekenen
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet een `numeric` uit PostgreSQL (die als tekst binnenkomt) met een eigen parser om naar gehele centen of reken in SQL; gebruik nooit `Number()`, `parseFloat`, `Math.round(x * 100)` of `toFixed` om een geldbedrag te berekenen of af te ronden. `toFixed` mag alleen op een geheel aantal centen dat je door 100 deelt voor weergave.
- Bewijs: `grep -rnE "Number\(|parseFloat\(|toFixed\(|Math\.round\(" src` in prijs-, korting-, btw- en betaalcode: elke treffer werkt op gehele centen of is weergave; geen enkele staat op een bedrag met decimalen. Unit-test op de prijsfunctie met 1,005, 2,675 en 19,99. Kolommen voor bedragen: `integer` centen, of `numeric(12,2)` met rekenwerk in SQL.
- Norm: ASVS 5.0.0 V2.2.1 (L1), V1.4.2 (L2).
- Zie ook: DB-75, API-28, API-27, BIZ-10, BIZ-12, BIZ-17

### BIZ-12 Verdeel een bedrag zo dat de delen samen exact het totaal zijn
middel · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Verdeel een bedrag over delen (termijnen, een korting over regels, een vergoeding over partners, exclusief en btw uit een bedrag inclusief) door in gehele centen naar beneden af te ronden en de resterende centen één voor één aan vaste delen toe te wijzen, en controleer in de code dat de som van de delen gelijk is aan het totaal.
- Bewijs: Eigenschappen-test (ARCH-42): voor willekeurige totalen en aantallen is de som van `verdeel()` gelijk aan het totaal en verschillen de delen hoogstens één cent. In de database: een `CHECK` of een controlequery dat de som van de regels gelijk is aan het totaal van de bestelling (BIZ-51).
- Norm: ASVS 5.0.0 V2.2.3 (L2).
- Zie ook: DB-75, API-28, API-27, BIZ-10, BIZ-11, BIZ-17

### BIZ-13 Leg prijs, korting, btw-tarief en totaal vast op de bestelling en reken ze later niet opnieuw uit
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Sla op het moment van bestellen per regel de eenheidsprijs, de korting, het btw-tarief, het btw-bedrag en het totaal op, en gebruik voor de betaling, de factuur, de terugbetaling en de vergoeding die opgeslagen waarden; lees daarvoor nooit opnieuw de actuele prijslijst, de actuele kortingsregel of het actuele btw-tarief uit de configuratie.
- Bewijs: De bestelregel heeft eigen kolommen voor prijs, korting, tarief en totaal, alle `NOT NULL`. `grep` in de webhook-, factuur- en terugbetaalcode toont geen aanroep van de prijsfunctie of de prijslijst. Test: wijzig de prijslijst en het tarief na het aanmaken van een bestelling; betaling, factuur en terugbetaling gebruiken de oude bedragen. Het btw-tarief is een kolom op de regel, geen constante uit de omgeving die bij het factureren wordt gelezen.
- Norm: ASVS 5.0.0 V2.2.3 (L2), V2.3.3 (L2).
- Zie ook: API-37, BIZ-14, BIZ-17, BIZ-19, BIZ-33, API-35, API-29

### BIZ-14 Bevries de bestelling zodra de betaling is aangemaakt
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Sta na het aanmaken van de betaling geen wijziging meer toe aan de inhoud van de bestelling (regels, aantallen, code, adres dat het tarief bepaalt); een wijziging annuleert de openstaande betaling en maakt een nieuwe bestelling of een nieuwe betaling met een nieuw bedrag.
- Bewijs: Test: maak een betaling aan, probeer daarna een regel toe te voegen, het aantal te wijzigen en een code toe te passen; alle drie geven 409. Test met gelijktijdigheid: "betaling starten" en "regel toevoegen" tegelijk afgevuurd leveren nooit een bestelling op waarvan de som van de regels afwijkt van het bedrag van de betaling (controlequery van BIZ-51).
- Norm: ASVS 5.0.0 V2.3.1 (L1), V15.4.2 (L3); OWASP API Top 10 2023 API6.
- Zie ook: API-37, BIZ-13, BIZ-17, BIZ-19, BIZ-33, API-35, API-29

### BIZ-15 Begrens terugbetalingen in je eigen boek voordat je Mollie aanroept
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg elke terugbetaling eerst vast als rij in de eigen database, onder een slot op de betaling (BIZ-02) en met de controle dat de som van alle terugbetalingen hoogstens het betaalde bedrag is; roep daarna Mollie aan met de idempotentiesleutel van die rij (API-41), en betaal alleen terug via de Mollie-API naar de oorspronkelijke betaling, nooit naar een rekeningnummer dat iemand opgeeft.
- Bewijs: Test met 20 gelijktijdige gedeeltelijke terugbetalingen die samen meer zijn dan de betaling: de som in de eigen tabel blijft binnen het betaalde bedrag en de nagebootste Mollie-API krijgt niet meer aanroepen dan er rijen zijn. `grep -rniE "iban|rekeningnummer" src` in terugbetaalcode is leeg. De regel wanneer terugbetalen mag (bij Marketing Maatwerk: tot de bouw begint en uiterlijk 14 dagen) is een voorwaarde op de status en de datum in dezelfde transactie, met een test voor dag 14 en dag 15.
- Norm: ASVS 5.0.0 V2.3.2 (L2), V2.3.4 (L2); OWASP API Top 10 2023 API6.
- Zie ook: API-42, BIZ-16, BIZ-22, BIZ-36, BIZ-47

### BIZ-16 Keer een vergoeding of tegoed dat aan een betaling hangt pas uit na de terugboektermijn
middel · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet een partnervergoeding, verwijsbonus of tegoed bij de betaling op "voorlopig" en maak hem pas uitkeerbaar als de termijn voor terugbetalen en terugboeken van die betaalwijze voorbij is; trek hem in bij een terugbetaling of chargeback (API-42). Vaste termijnen (besluit van Marketing Maatwerk, 04-10-2026): 14 dagen bij iDEAL en 56 dagen bij SEPA-incasso.
- Bewijs: De termijn per betaalwijze staat in de projectdocumentatie (iDEAL: 14 dagen, de eigen geld-terugtermijn; SEPA-incasso: 56 dagen; besluit van Marketing Maatwerk, 04-10-2026). Test: een vergoeding binnen de termijn is niet uitkeerbaar; een terugbetaling of chargeback zet hem op ingetrokken, ook als hij al uitkeerbaar was, en maakt dan een taak voor Marketing Maatwerk. De dagelijkse controle (bij de registrar: de partnercontrole van 08:50) meldt elke intrekking.
- Norm: ASVS 5.0.0 V2.3.2 (L2); OWASP API Top 10 2023 API6.
- Zie ook: API-42, BIZ-15, BIZ-22, BIZ-36, BIZ-47

### BIZ-17 De valuta komt van de server en staat bij elk bedrag
laag · hard · api | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet de valuta vast in de servercode (bij Marketing Maatwerk: `EUR`), sla hem op naast elk bedrag dat de database verlaat, neem hem nooit over uit het verzoek en weiger elke optelling of vergelijking van bedragen met een verschillende valuta.
- Bewijs: Het bestelschema bevat geen valutaveld (API-02 weigert het). `grep -rn "currency" src` toont alleen de constante en de vergelijking van API-37. Mollie verwacht het bedrag als object met een ISO 4217-code en het exacte bedrag als tekst; de omzetting van centen naar die tekst staat op één plek.
- Norm: ASVS 5.0.0 V2.2.2 (L1), V2.2.3 (L2).
- Zie ook: DB-75, API-28, API-27, BIZ-10, BIZ-11, BIZ-12, API-37, BIZ-13, BIZ-14, BIZ-19, BIZ-33, API-35, API-29

### BIZ-18 Pas 0 procent of verlegde btw alleen toe op bewijs dat de server zelf heeft gecontroleerd
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bepaal het btw-tarief op de server; pas een verlegging of een nultarief voor een zakelijke klant in een ander EU-land alleen toe nadat de server het btw-identificatienummer heeft gecontroleerd bij de dienst van de Europese Commissie (VIES), bewaar de uitkomst met datum bij de bestelling, en reken bij een mislukte of onbereikbare controle het gewone tarief.
- Bewijs: Test: een bestelling met een btw-nummer dat de nagebootste VIES-dienst afkeurt, krijgt het gewone tarief; een time-out van de dienst ook (faal dicht, API-12). De bestelling bewaart nummer, uitkomst en tijdstip van de controle. Of en wanneer verlegging mag is fiscaal: laat de boekhouder de regel bevestigen voordat hij live gaat. Verkoopt het project alleen aan Nederlandse klanten, dan is de regel afgevinkt met de vaststelling dat er geen nultarief in de code zit.
- Norm: ASVS 5.0.0 V2.2.2 (L1), V2.2.3 (L2).

### BIZ-19 Een bestelling van nul euro heeft een eigen overgang en gaat niet langs "betaald"
middel · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Als een bestelling na korting nul euro kan worden, geef die uitkomst dan een eigen, benoemde overgang in de statusmachine (API-29) met een eigen controle (welke code, wie mag dit, hoe vaak), en lever nooit via het pad dat "betaald" veronderstelt zonder dat er een betaling is.
- Bewijs: De statusmachine heeft een overgang `concept -> gratis_toegekend` naast `wacht_op_betaling -> betaald`. Test: een bestelling met totaal nul zonder een code die uitdrukkelijk gratis toestaat, geeft een fout. Een gratis bestelling telt mee in de limieten van BIZ-34 en BIZ-23 en maakt een regel in het audit-log (AUTH-84). Het maximum-kortingspercentage (bij de registrar: 65 procent) is een `CHECK` in de database.
- Norm: ASVS 5.0.0 V2.3.1 (L1), V2.3.2 (L2).
- Zie ook: API-37, BIZ-13, BIZ-14, BIZ-17, BIZ-33, API-35, API-29
