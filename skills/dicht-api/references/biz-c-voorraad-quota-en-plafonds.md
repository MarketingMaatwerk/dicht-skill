# BIZ C: voorraad, quota en plafonds

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/bedrijfslogica-gelijktijdigheid.md` (regelnummer in `regel-index.tsv`).

### BIZ-20 Reserveer schaarse dingen met een vervaltijd en een maximum per account
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd iets wat op kan (voorraad, een tijdslot, een eenmalige code, een plek in een actie) alleen vast met een reservering die een vervaltijd heeft, begrens het aantal openstaande reserveringen per account, per sessie en per bron, en tel een verlopen reservering niet meer mee op het moment van tellen (BIZ-25).
- Bewijs: De reserveringstabel heeft `verloopt_op NOT NULL`. De vervaltijd is niet korter dan de geldigheid van de betaling (anders betaalt iemand voor iets wat al is vrijgegeven; zie BIZ-22). Tests: een verlopen reservering telt niet mee, ook als de opruimjob niet heeft gedraaid; het maximum per account wordt geweigerd met 429; 20 gelijktijdige reserveringen op de laatste eenheid geven er één. In WooCommerce: de instelling "Hold stock (minutes)" is ingevuld (BIZ-45).
- Norm: ASVS 5.0.0 V2.3.4 (L2), V2.4.1 (L2); OWASP API Top 10 2023 API6.
- Zie ook: API-34, BIZ-21, BIZ-23, BIZ-37, BIZ-32, BIZ-38, AI-74, BIZ-25, BIZ-34

### BIZ-21 Boek verbruik van een quotum vóór de dure actie en geef het terug als de actie mislukt
middel · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf het verbruik van een quotum (aanroepen per tenant, mails per dag, domeinchecks per uur, opslag) af met de voorwaardelijke `UPDATE` van BIZ-01 voordat de actie start, en boek het terug als de actie niet is uitgevoerd; controleer nooit eerst, voer dan uit en tel achteraf.
- Bewijs: Test: 50 gelijktijdige verzoeken bij één resterende eenheid geven precies één aanroep van de nagebootste dienst en 49 keer 429. Test: een mislukte actie geeft de eenheid terug. De periode (dag, maand) is een kolom in de sleutel, zodat een nieuwe periode een nieuwe rij is en er geen resetjob nodig is.
- Norm: ASVS 5.0.0 V2.4.1 (L2), V2.3.2 (L2), V15.4.2 (L3). Zie API-34, AI-74.
- Zie ook: BIZ-23, AI-73, ARCH-28, SCR-46, SCR-47, API-34, BIZ-37, BIZ-32, BIZ-20, BIZ-38, AI-74

### BIZ-22 "Betaald maar niet leverbaar" is een eigen toestand met een vaste afhandeling
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem in elke statusmachine met een betaling en een levering door een externe partij de toestand "betaald, levering mislukt" op, met een vast vervolg: een begrensd aantal nieuwe pogingen (API-49, ARCH-19), daarna een taak voor Marketing Maatwerk en een terugbetaling of een alternatief volgens de bedrijfsregel, en een bericht aan de klant; controleer de beschikbaarheid opnieuw op het moment van leveren.
- Bewijs: De overgangstabel van API-29 bevat de toestand en de overgangen eruit. Test met een nagebootste leverancier die "niet beschikbaar" antwoordt: de bestelling komt in de toestand, er ontstaat een taak en een alarm (ARCH-69), en er wordt niet oneindig herhaald. Controlequery in de dagelijkse afstemming (BIZ-48): geen bestelling staat langer dan de afgesproken tijd op "betaald" zonder levering of zonder deze toestand.
- Norm: ASVS 5.0.0 V2.3.3 (L2), V2.3.1 (L1).
- Zie ook: API-42, BIZ-15, BIZ-16, BIZ-36, BIZ-47

### BIZ-23 Geef elke automatische stroom die geld kost of iets naar buiten stuurt een dagplafond dat stopt
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke geautomatiseerde handeling met kosten of een effect buiten het systeem (registraties bij de registry, hostingpakketten aanmaken, sms, mail, terugbetalingen, gratis bestellingen, uitkeringen) een plafond per tenant en een plafond in totaal per dag, in de database geteld volgens BIZ-21; bij het plafond stopt de stroom, komt er een alarm en gaat hij alleen met een bewuste handeling weer aan.
- Bewijs: Per stroom staat in de projectdocumentatie het plafond per tenant en in totaal, en wie hem weer aanzet. Test: de aanroep na het plafond wordt geweigerd, er gaat een alarm af en de volgende run blijft gestopt tot de schakelaar (ARCH-76) is omgezet. Het plafond is een getal in de configuratie dat bij de start wordt gevalideerd (ARCH-07) en niet nul of leeg kan zijn.
- Norm: ASVS 5.0.0 V2.1.3 (L2), V2.4.1 (L2), V2.3.2 (L2); OWASP API Top 10 2023 API6. Zie AI-73, ARCH-28, API-34.
- Zie ook: ARCH-76, AI-79, AI-26, PRIV-51, ARCH-77, SCR-46, SCR-52, MSG-49, AI-73, ARCH-28, SCR-47, BIZ-21, API-34, BIZ-37, BIZ-32, BIZ-20, BIZ-38, AI-74
