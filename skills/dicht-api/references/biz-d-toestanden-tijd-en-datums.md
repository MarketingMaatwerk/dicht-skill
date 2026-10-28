# BIZ D: toestanden, tijd en datums

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/bedrijfslogica-gelijktijdigheid.md` (regelnummer in `regel-index.tsv`).

### BIZ-24 Geloof bij een bericht over een toestand de actuele stand, niet de inhoud of de volgorde van het bericht
middel · hard · api | app | wp-plugin | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Behandel elk inkomend bericht over een toestand (webhook van Mollie, Moneybird, het hostingpaneel, een berichtendienst) als signaal dat er iets is veranderd: haal de actuele stand op bij de bron en verwerk die, en laat een bericht nooit een eindtoestand terugzetten naar een eerdere toestand.
- Bewijs: Test: bied de berichten van één betaling aan in omgekeerde volgorde en dubbel; de eindtoestand is gelijk aan de stand bij de bron. De overgangstabel bevat geen overgang uit een eindtoestand, behalve de benoemde (terugbetaald, teruggeboekt). Voor een bron zonder ophaalmogelijkheid: het bericht heeft een tijdstempel of volgnummer dat wordt opgeslagen, en een ouder bericht wordt genegeerd.
- Norm: ASVS 5.0.0 V2.3.1 (L1); OWASP API Top 10 2023 API10.
- Zie ook: API-36, API-37, API-38, API-44, WP-83, WP-82

### BIZ-25 Controleer een termijn op het moment van gebruik en reken niet op de opruimjob
middel · hard · api | app | wp-plugin | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem in elke query en elke overgang die van een termijn afhangt (reservering verlopen, proefperiode voorbij, code geldig tot, geld terug tot dag 14, uitnodiging geldig) de vergelijking met de klok van de database op, en gebruik daarvoor in een lange transactie `clock_timestamp()` in plaats van `now()`; een job die verlopen rijen een andere status geeft is opruimen, geen handhaving.
- Bewijs: Test met een vaste klok: een rij met `verloopt_op` één seconde in het verleden wordt geweigerd terwijl de status nog "actief" is. `grep` op de query's van elke termijn toont de tijdvergelijking. Geen enkel schema accepteert een tijdstip van de client als "nu".
- Norm: ASVS 5.0.0 V2.3.1 (L1), V2.2.2 (L1).
- Zie ook: BIZ-20, BIZ-34

### BIZ-26 Reken kalenderperiodes vanaf de ankerdatum, in SQL of met een kalenderbibliotheek
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bereken de n-de periode van een abonnement of termijn altijd als "ankerdatum plus n periodes" (`anker + n * interval '1 month'` in PostgreSQL), nooit als "vorige datum plus één periode", nooit met `Date.prototype.setMonth` en nooit met een vast aantal seconden of dagen per maand.
- Bewijs: `grep -rnE "setMonth|setFullYear|setDate|86400|\* 30\b|\* 365\b" src` is leeg in code die periodes, vervaldatums of einddatums berekent, of elke treffer is beoordeeld. Tests met ankerdatum 31 januari, 29 februari 2028 en 31 augustus over 13 periodes: elke periode begint op de ankerdag of op de laatste dag van een kortere maand, en er is precies één periode per maand. Op Node 22 bestaat `Temporal` niet (`typeof Temporal` geeft `undefined`, gemeten 04-10-2026); gebruik de database of een onderhouden bibliotheek.
- Norm: ASVS 5.0.0 V2.2.3 (L2).
- Zie ook: DB-74, ARCH-12, INFRA-71, BIZ-27, BIZ-28, BIZ-29, SCR-40, SCR-52

### BIZ-27 Bepaal zakelijke datums in Europe/Amsterdam en sla ze op als datum
middel · hard · api | app | wp-plugin | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leid elke datum met een zakelijke of fiscale betekenis (factuurdatum, betaaldatum voor de boekhouding, vervaldatum, einddatum van een contract, de dag van een daglimiet) af uit het tijdstip in de tijdzone `Europe/Amsterdam` en sla hem op als `date`; knip nooit de eerste tien tekens van een ISO-tijdstip in UTC af, en maak van een datum zonder tijd nooit een `Date` met `new Date('jjjj-mm-dd')` om er lokaal mee te rekenen.
- Bewijs: `grep -rnE "toISOString\(\)\.(slice|substring|split)" src` raakt geen zakelijke datum. Test met een vaste klok op 01-01 00:30 en 01-07 01:30 Nederlandse tijd: factuurdatum, periode en daglimiet vallen op de Nederlandse dag. De tijdzone staat als constante op één plek, niet als instelling van de server.
- Norm: ASVS 5.0.0 V2.2.3 (L2). Zie DB-74, ARCH-12.
- Zie ook: DB-74, ARCH-12, INFRA-71, BIZ-26, BIZ-28, BIZ-29, SCR-40, SCR-52

### BIZ-28 Sla periodes op als halfopen interval
middel · richtlijn · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg elke periode vast als begin (inbegrepen) en eind (niet inbegrepen) en vergelijk met `begin <= t AND t < eind`; sla een einddatum "tot en met de 31e" op als het begin van de 1e in Europe/Amsterdam, en toon hem aan de gebruiker als de 31e.
- Bewijs: `grep -rniE "23:59|between .* and" src` is leeg voor tijdvergelijkingen, of beoordeeld. Test: een gebeurtenis precies op de grens hoort bij precies één periode. Bereiktypes in PostgreSQL staan als `'[begin, eind)'`.
- Norm: geen ASVS-eis; ontwerpregel uit de PostgreSQL-documentatie.
- Zie ook: DB-74, ARCH-12, INFRA-71, BIZ-26, BIZ-27, BIZ-29, SCR-40, SCR-52

### BIZ-29 Tel dagen als kalenderdagen, niet als 24 uur
middel · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Reken een termijn in dagen ("geld terug binnen 14 dagen", "herinnering na 5 dagen", "bewaar 30 dagen") met kalenderdagen in Europe/Amsterdam (`+ interval '14 days'` op een `timestamptz` met de juiste tijdzone, of op een `date`), niet met `14 * 24 * 60 * 60 * 1000` milliseconden.
- Bewijs: Test met een vaste klok rond 29-03-2026 en 25-10-2026: de termijn eindigt op de verwachte kalenderdag. `grep -rnE "86_?400|24 \* 60|interval '[0-9]+ hours'" src` in termijncode is leeg of beoordeeld. Bij een transactiepooler of een sessie in UTC staat de tijdzone uitdrukkelijk in de query (`AT TIME ZONE`), niet in de sessie-instelling (DB-64).
- Norm: ASVS 5.0.0 V2.2.3 (L2).
- Zie ook: DB-74, ARCH-12, INFRA-71, BIZ-26, BIZ-27, BIZ-28, SCR-40, SCR-52

### BIZ-30 Leg elke periodieke incasso vast met een unieke sleutel op abonnement en periode voordat je incasseert
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak voor elke verlenging of termijn eerst een rij met een unieke sleutel op (abonnement, begin van de periode) en roep Mollie pas aan als die insert een rij opleverde; de idempotentiesleutel naar Mollie (API-41) is die van deze rij.
- Bewijs: `\d incassos` toont de unieke index. Test: de job twee keer achter elkaar en twee keer tegelijk draaien geeft één aanroep van de nagebootste Mollie-API per abonnement en periode. Test: een crash tussen de aanroep en het bijwerken leidt bij de volgende run tot navragen (BIZ-40), niet tot een nieuwe betaling.
- Norm: ASVS 5.0.0 V2.3.4 (L2), V2.3.3 (L2). Zie API-31, API-41, ARCH-18.
- Zie ook: API-31, BIZ-34, BIZ-35, BIZ-39, BIZ-41, BIZ-43, BIZ-46, API-33, DB-68

### BIZ-31 Laat een periodieke taak zijn werk afleiden uit de toestand, niet uit de datum van vandaag
middel · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke dagelijkse of periodieke taak selecteren op "alles wat aan de beurt is en nog niet is gedaan" (`vervalt_op <= nu AND gedaan_op IS NULL`), niet op "alles met de datum van vandaag"; een gemiste run wordt dan vanzelf ingehaald en een dubbele run doet niets.
- Bewijs: Test: sla in de test één run over (zet de klok twee dagen vooruit); de volgende run pakt beide dagen op. Test: twee runs achter elkaar geven hetzelfde eindresultaat als één. De taak logt hoeveel achterstallige rijen hij vond en alarmeert boven een drempel (inhalen van een week aan herinneringen in één keer is zelf een risico: begrens met BIZ-23).
- Norm: ASVS 5.0.0 V2.3.3 (L2). Zie ARCH-18 en het domein SCR voor overlappende runs en `Persistent=`.
- Zie ook: INFRA-69, SCR-18, SCR-38, SCR-39, SCR-37, SCR-36, SCR-41, INFRA-70
