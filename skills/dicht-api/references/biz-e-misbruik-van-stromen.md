# BIZ E: misbruik van stromen

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/bedrijfslogica-gelijktijdigheid.md` (regelnummer in `regel-index.tsv`).

### BIZ-32 Maak codes met waarde niet raadbaar en begrens het proberen
middel · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Genereer een code die op zichzelf waarde geeft (persoonlijke korting, cadeaubon, eenmalige actiecode) met een CSPRNG (API-61), begrens het aantal mislukte pogingen per sessie, per account en per IP op de route die codes controleert, en geef voor "bestaat niet", "verlopen" en "op" hetzelfde antwoord. Een bewust openbare code (een partnercode in een advertentie) krijgt in plaats daarvan een einddatum, een maximum aantal keer en een maximum korting.
- Bewijs: Test: na het ingestelde aantal mislukte pogingen geeft de route 429 (API-20, API-22), ook voor een daarna correcte code binnen het venster. Test: de drie foutgevallen geven dezelfde status en dezelfde body. De limiet en de vorm van de codes staan in de projectdocumentatie. Elke openbare code heeft `verloopt_op`, `maximum` en een kortingsgrens (`CHECK`).
- Norm: ASVS 5.0.0 V2.4.1 (L2); OWASP API Top 10 2023 API6. Zie AUTH-12 voor hetzelfde principe bij accounts.
- Zie ook: API-34, BIZ-21, BIZ-23, BIZ-37, BIZ-20, BIZ-38, AI-74

### BIZ-33 Sta standaard één code per bestelling toe en begrens de totale korting
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat per bestelling hoogstens één kortingscode toe tenzij stapelen uitdrukkelijk is ontworpen; pas kortingen toe in één vaste volgorde, en controleer na alle kortingen dat de totale korting onder het maximum blijft en het totaal boven het minimum (API-35), op de server en in de database.
- Bewijs: Unit-tests op de prijsfunctie: twee codes, dezelfde code twee keer, een code plus een automatische actie; de uitkomst is de vastgelegde regel en nooit onder het minimum. `CHECK (korting_centen <= maximum)` of `CHECK (kortingspercentage <= 65)` in de database (bij de registrar is 65 procent het maximum). In WooCommerce staat bij elke bon "Individual use only" aan, tenzij stapelen bedoeld is.
- Norm: ASVS 5.0.0 V2.3.2 (L2), V2.2.3 (L2); OWASP API Top 10 2023 API6.
- Zie ook: API-37, BIZ-13, BIZ-14, BIZ-17, BIZ-19, API-35, API-29

### BIZ-34 Reserveer een beperkte code bij het starten van de bestelling en tel hem definitief bij de betaling
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf het gebruik van een code met een limiet af volgens BIZ-01 op het moment dat de bestelling wordt bevroren (BIZ-14), als reservering met dezelfde vervaltijd als de betaling; maak hem definitief in de transactie die de bestelling op betaald zet, en geef hem vrij bij verlopen, annuleren of mislukken.
- Bewijs: Test: 20 gelijktijdige bestellingen met een code die één keer geldt; precies één krijgt de korting, de rest krijgt de volle prijs of een weigering, en geen enkele betaling wordt aangemaakt met een bedrag dat niet bij zijn bestelling past (BIZ-13). Test: een verlopen bestelling geeft de code terug. Controlequery (BIZ-51): voor elke code is het aantal definitieve plus niet-verlopen reserveringen hoogstens het maximum.
- Norm: ASVS 5.0.0 V2.3.4 (L2), V15.4.2 (L3); OWASP API Top 10 2023 API6.
- Zie ook: API-31, BIZ-30, BIZ-35, BIZ-39, BIZ-41, BIZ-43, BIZ-46, API-33, DB-68, BIZ-25, BIZ-20

### BIZ-35 Bind een eenmalig voordeel aan iets stabielers dan een e-mailadres
middel · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg voor elk voordeel dat één keer per klant geldt (proefperiode, welkomstkorting, gratis eerste periode) vast op welke sleutel "klant" wordt herkend, en gebruik daarvoor een genormaliseerd e-mailadres plus minstens één sterker kenmerk waar de stroom dat heeft (het betaalmiddel of de machtiging bij Mollie, het KvK-nummer, het domein waarvoor wordt besteld); bewaar die sleutel ook nadat het account is verwijderd, als hash (DB-81).
- Bewijs: De documentatie noemt per voordeel de sleutel. Unieke index op (voordeel, klantsleutel) met `NOT NULL` (BIZ-05). Tests: tweede aanmelding met hoofdletters of punten in een Gmail-adres, met hetzelfde betaalmiddel en na verwijderen van het eerste account: geen tweede voordeel. De bewaartermijn van de sleutel staat in het register (PRIV) en in de opruimjob (DB-83).
- Norm: ASVS 5.0.0 V2.3.2 (L2); OWASP API Top 10 2023 API6. Zie API-31.
- Zie ook: API-31, BIZ-30, BIZ-34, BIZ-39, BIZ-41, BIZ-43, BIZ-46, API-33, DB-68

### BIZ-36 Geen vergoeding voor een verwijzing naar jezelf
middel · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Ken een verwijsbonus of partnervergoeding alleen toe op een betaalde, niet teruggedraaide bestelling (BIZ-16) van een klant die aantoonbaar een ander is dan de eigenaar van de code: vergelijk klantsleutel (BIZ-35), betaalmiddel en organisatie, en zet twijfelgevallen op "ter beoordeling" in plaats van ze uit te keren. De vergoeding blijft voorlopig tot de termijn van BIZ-16 voorbij is: 14 dagen bij iDEAL, 56 dagen bij SEPA-incasso (besluit van Marketing Maatwerk, 04-10-2026).
- Bewijs: Tests: bestelling met de eigen code (zelfde klantsleutel, zelfde betaalmiddel, zelfde organisatie) geeft geen vergoeding; een vergoeding ontstaat pas bij de overgang naar betaald en niet bij aanmelden of bij het starten van de bestelling. Plafond per code per dag (BIZ-23). De dagelijkse controle meldt codes met een afwijkend patroon (veel bestellingen, veel terugbetalingen).
- Norm: ASVS 5.0.0 V2.3.2 (L2); OWASP API Top 10 2023 API6.
- Zie ook: API-42, BIZ-15, BIZ-16, BIZ-22, BIZ-47

### BIZ-37 Geef opzoekfuncties met zakelijke waarde een eigen limiet
middel · hard · api | app | wp-plugin | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke openbare functie die bij elke aanroep iets waardevols prijsgeeft of iets kost (domein beschikbaar, prijs voor deze klant, saldo van een cadeaubon, bestaat dit bedrijf al, postcodecontrole) een eigen limiet per bron en per dag, los van de algemene limiet, en begrens wat één antwoord teruggeeft.
- Bewijs: Per opzoekfunctie staat de limiet in de documentatie (API-34) en is er een test die hem overschrijdt (429 met `Retry-After`). Antwoorden op dezelfde vraag worden kort gecachet, met de tenant in de sleutel waar het antwoord per klant verschilt (DB-23). Een alarm gaat af als het aantal aanroepen naar de leverancier per uur boven de drempel komt.
- Norm: ASVS 5.0.0 V2.4.1 (L2); OWASP API Top 10 2023 API6, API4. Zie API-20, API-34.
- Zie ook: API-34, BIZ-21, BIZ-23, BIZ-32, BIZ-20, BIZ-38, AI-74

### BIZ-38 Meet op waardevolle stromen of het tempo menselijk is
laag · richtlijn · api | app | wp-plugin | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg bij stromen die waarde uitdelen (aanmelden met voordeel, bestellen in een actie, een bon verzilveren) op de server het tijdstip van elke stap vast en weiger of vertraag een afronding die sneller komt dan een mens kan, als extra laag boven de limieten van BIZ-23 en BIZ-32.
- Bewijs: Test: een afronding binnen de ingestelde ondergrens na de eerste stap wordt geweigerd of naar een extra controle gestuurd. De ondergrens staat in de documentatie. Het registratieformulier van de site van Marketing Maatwerk doet dit al met een tijdstempel; zie WEB voor formulieren.
- Norm: ASVS 5.0.0 V2.4.2 (L3); OWASP API Top 10 2023 API6.
- Zie ook: API-34, BIZ-21, BIZ-23, BIZ-37, BIZ-32, BIZ-20, AI-74
