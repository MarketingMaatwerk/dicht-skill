# API D: bedrijfslogica, races en idempotentie

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/api-code.md` (regelnummer in `regel-index.tsv`).

### API-27 Bereken prijs en totaal op de server uit een vertrouwde bron
kritiek · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem van de client alleen wat hij kiest (product-id, aantal, termijn, kortingscode) en bereken prijs, korting, btw en totaal op de server uit de eigen prijslijst; neem nooit een bedrag over uit het verzoek.
- Bewijs: Het bestelschema bevat geen bedragveld. Test: een verzoek met een extra `prijs` of `amount` geeft 400 (zie API-02). Het bedrag dat naar Mollie gaat komt aantoonbaar uit de servercode (unit-test op de prijsfunctie).
- Norm: ASVS 5.0.0 V2.2.2 (L1), V2.3.2 (L2); OWASP API Top 10 2023 API6.
- Zie ook: DB-75, API-28, BIZ-10, BIZ-11, BIZ-12, BIZ-17

### API-28 Reken met geld in hele centen of exacte decimalen, nooit met floats
hoog · hard · api | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Sla bedragen op en reken ermee als geheel getal in centen (of `numeric` in PostgreSQL), en zet pas bij de aanroep naar Mollie om naar een string met precies twee decimalen.
- Bewijs: Het schema gebruikt `integer` of `numeric` voor bedragen (zie DB). `grep -rnE "parseFloat|toFixed" src` in prijs- en betaalcode wordt per treffer beoordeeld. Unit-test met bedragen die bij floats fout gaan. Een `numeric` komt als tekst uit de driver: beoordeel ook `Number(` en `Math.round(` op bedragen; de grep en de testwaarden staan in BIZ-11.
- Norm: ASVS 5.0.0 V2.2.1 (L1), V1.4.2 (L2).
- Zie ook: DB-75, API-27, BIZ-10, BIZ-11, BIZ-12, BIZ-17

### API-29 Leg elke flow vast als statusmachine en sta alleen de bedoelde overgangen toe
hoog · hard · api | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elk proces met stappen (bestelling, betaling, levering, opzegging, terugbetaling) een statusveld op de server met een vaste lijst van toegestane overgangen, en weiger elk verzoek dat een stap overslaat of een afgeronde stap herhaalt.
- Bewijs: Eén functie `overgang(van, naar)` met een tabel van toegestane paren; unit-tests voor elke verboden overgang. Test end-to-end: stap 3 aanroepen zonder stap 2 geeft 409.
- Norm: ASVS 5.0.0 V2.3.1 (L1).
- Zie ook: API-37, BIZ-13, BIZ-14, BIZ-17, BIZ-19, BIZ-33, API-35

### API-30 Maak controleren en handelen één atomaire stap
kritiek · hard · api | app | wp-plugin | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf elke bewerking van de vorm "controleer, dan wijzig" als één atomaire databasebewerking: een voorwaardelijke `UPDATE ... WHERE <voorwaarde> RETURNING`, een rij-lock (`SELECT ... FOR UPDATE`) in een transactie, of een unieke constraint; controleer het aantal geraakte rijen. Aanvulling uit DB-67: Nooit met een losse `SELECT` gevolgd door een `INSERT` of `UPDATE`.
- Bewijs: Een test vuurt 20 gelijktijdige verzoeken af op dezelfde bewerking en controleert dat het effect precies één keer optreedt. Zonder die test is de regel niet afgevinkt voor betaling, tegoed, kortingscode en levering. Dezelfde 20 verzoeken gelden voor de databasekant (DB-67).
    Ook (uit DB-67): Test die dezelfde handeling met 20 gelijktijdige verzoeken afvuurt (gelijk aan API-30; hier stond tien, het strengste geldt) en precies één succes verwacht. Afgevinkt als die test bestaat voor elke beperkte resource (codes, voorraad, saldo, uniek slot).
- Norm: ASVS 5.0.0 V15.4.2 (L3), V2.3.4 (L2), V2.3.3 (L2).
- Dekt ook: DB-67
- Zie ook: API-31, API-33, API-38, DB-68, ARCH-18, AUTH-59, BIZ-01, BIZ-02, BIZ-03, BIZ-04, BIZ-05, BIZ-06, BIZ-07, BIZ-09, BIZ-44, BIZ-50

### API-31 Dwing "één keer" af met een unieke constraint
hoog · hard · api | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg alles wat maar één keer mag gebeuren (kortingscode per klant, partnervergoeding per betaling, welkomstmail per bestelling, proefperiode per account) vast met een unieke index en laat de database het duplicaat weigeren.
- Bewijs: De migratie bevat de unieke index (zie DB). De code vangt de unieke-constraintfout (PostgreSQL-code 23505) af als "al gedaan". Test met gelijktijdige verzoeken zoals bij API-30.
- Norm: ASVS 5.0.0 V2.3.4 (L2), V2.3.2 (L2).
- Zie ook: API-30, API-33, API-38, DB-68, ARCH-18, AUTH-59, BIZ-30, BIZ-34, BIZ-35, BIZ-39, BIZ-41, BIZ-43, BIZ-46

### API-32 Zet een samengestelde bewerking in één transactie
kritiek · hard · api | app | wp-plugin | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Voer bewerkingen die samen moeten slagen of samen moeten mislukken uit in één databasetransactie, en leg een externe actie die erbij hoort (mail, aanroep naar een API) vast als taak in dezelfde transactie in plaats van hem erbinnen uit te voeren.
- Bewijs: De statusovergang en het aanmaken van de taak staan in dezelfde `db.transaction`. Test: een fout na de eerste schrijfactie laat de status ongewijzigd.
    Ook (uit DB-66): Integratietest die in de tweede stap een fout injecteert en controleert dat de eerste stap is teruggedraaid. Afgevinkt als die test bestaat voor elke meerstapshandeling met geld of rechten.
    Ook (uit ARCH-16): Per kritieke handeling een test die een fout injecteert halverwege (de tweede schrijfactie gooit) en daarna controleert dat er geen rij is achtergebleven, en een test die de controle zelf laat falen en een weigering verwacht. Afgevinkt met de testuitvoer. Zie WEB-63 voor hetzelfde principe aan de webkant.
- Norm: ASVS 5.0.0 V2.3.3 (L2).
- Dekt ook: DB-66, ARCH-16

### API-33 Maak eigen muterende routes met een extern effect idempotent
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een POST die geld, een bestelling, een mail of een externe actie veroorzaakt een idempotentiesleutel accepteren (header `Idempotency-Key`), sla sleutel en resultaat op en geef bij herhaling het opgeslagen resultaat terug.
- Bewijs: Test: twee identieke POST's met dezelfde sleutel geven hetzelfde antwoord en één rij. Dezelfde sleutel met een andere body geeft een fout (Mollie zelf geeft dan 400). Let op: de IETF-concepttekst voor deze header (draft-ietf-httpapi-idempotency-key-header-07) is op 18-04-2026 verlopen; de header is een gangbare afspraak, geen standaard.
- Norm: ASVS 5.0.0 V2.3.3 (L2); OWASP API Top 10 2023 API6.
- Zie ook: API-30, API-31, API-38, DB-68, ARCH-18, AUTH-59, BIZ-30, BIZ-34, BIZ-35, BIZ-39, BIZ-41, BIZ-43, BIZ-46

### API-34 Leg limieten per gebruiker en in totaal vast en dwing ze af
middel · hard · api | app | wp-plugin | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Beschrijf per gevoelige flow de zakelijke grenzen (maximaal aantal bestellingen per uur per account, maximaal aantal mails per dag, maximaal aantal proefaccounts per e-mailadres of IP, maximaal aantal AI-aanroepen per tenant) en dwing ze af in de code.
- Bewijs: De limieten staan in de projectdocumentatie. Per limiet een test die de grens overschrijdt. Overschrijdingen worden gelogd (ASVS V16.3.3).
- Norm: ASVS 5.0.0 V2.1.3 (L2), V2.3.2 (L2), V2.4.1 (L2); OWASP API Top 10 2023 API6.
- Zie ook: BIZ-21, BIZ-23, BIZ-37, BIZ-32, BIZ-20, BIZ-38, AI-74

### API-35 Weiger nul, negatief en extreem in aantallen en bedragen
hoog · hard · api | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elk aantal en elk bedrag een ondergrens en een bovengrens in het schema (aantal minimaal 1, geheel getal, met een maximum) en controleer na het rekenen dat het totaal groter is dan nul en binnen het verwachte bereik ligt.
- Bewijs: Unit-tests op de prijsfunctie met 0, -1, 1.5, het maximum plus één en een stapel kortingen. De functie gooit bij een totaal van nul of minder, tenzij gratis expliciet is toegestaan.
- Norm: ASVS 5.0.0 V2.2.1 (L1), V1.4.2 (L2), V2.3.2 (L2).
- Zie ook: API-37, BIZ-13, BIZ-14, BIZ-17, BIZ-19, BIZ-33, API-29
