# BIZ H: tests voor grenzen, tijd en gelijktijdigheid

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/bedrijfslogica-gelijktijdigheid.md` (regelnummer in `regel-index.tsv`).

### BIZ-50 Bewijs een race met echte gelijktijdigheid tegen een echte PostgreSQL
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf de race-tests van API-30 en van dit domein zo dat de verzoeken aantoonbaar tegelijk lopen: tegen een echte PostgreSQL (ARCH-35), met een verbindingspool die minstens zo groot is als het aantal gelijktijdige verzoeken, via de HTTP-laag of losse verbindingen in plaats van één gedeelde transactie, en met een controle dat de test faalt als je de bescherming weghaalt.
- Bewijs: De testopzet gebruikt een pool van minstens 20 en geen omhullende transactie voor deze tests. Mutatiecontrole met de hand of via ARCH-44: haal de `WHERE`-voorwaarde, het slot of de unieke index weg en de test faalt; dat is één keer aangetoond en genoteerd in het bewijsbestand. De test draait in de gate (ARCH-40).
- Norm: ASVS 5.0.0 V15.4.2 (L3), V2.3.4 (L2). Zie API-30, ARCH-35, ARCH-44.
- Zie ook: API-30, BIZ-01, BIZ-02, BIZ-03, BIZ-04, BIZ-05, BIZ-06, BIZ-07, BIZ-09, BIZ-44, BIZ-51, BIZ-52, ARCH-35, ARCH-42

### BIZ-51 Leg per geldstroom de invarianten vast als query en draai ze in de test en dagelijks
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf voor elke stroom met geld, voorraad of limieten de regels die altijd moeten gelden op als query's die nul rijen horen te geven (saldo nooit negatief; som van de regels is het totaal; som van terugbetalingen hoogstens het betaalde bedrag; hoogstens één actief abonnement; gebruik van een code hoogstens het maximum; geen levering zonder betaling), draai ze na elke race- en eigenschappen-test en dagelijks op productie, alleen lezen.
- Bewijs: Het bestand met invarianten staat in de repository naast het threat model (ARCH-82). De testhulp `controleerInvarianten()` wordt aangeroepen aan het eind van elke test in de geld- en limietmodules. De dagelijkse taak (samen met BIZ-48) logt per invariant het aantal rijen en alarmeert boven nul. Waar het kan staat dezelfde regel ook als `CHECK`, unieke index of exclusion constraint (DB-70, BIZ-04, BIZ-06).
- Norm: ASVS 5.0.0 V2.3.2 (L2), V2.2.3 (L2). Zie ARCH-42, ARCH-82.
- Zie ook: BIZ-48, BIZ-49, API-43, BIZ-46, BIZ-41, BIZ-50, BIZ-52, ARCH-35, ARCH-42

### BIZ-52 Test geld en tijd met een vaste tabel van grensgevallen
middel · hard · api | app | wp-plugin | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem in de tests van elke prijs-, btw-, termijn- en periodefunctie de vaste tabel hieronder op, met een vaste klok, en vul hem aan met de grenzen van het eigen project.
- Bewijs: De tabel staat als geparametriseerde test in de repository (`it.each`). De klok in de tests is vast (`vi.useFakeTimers` met `setSystemTime`, of een klok die wordt meegegeven) en de database-tijd in de test komt uit een parameter in plaats van `now()` waar de test dat nodig heeft. Voor betaling, login en tenant-isolatie geldt daarbovenop de mutatiedrempel van 80 procent (ARCH-44, besluit 21).
- Norm: ASVS 5.0.0 V2.2.1 (L1), V2.2.3 (L2). Zie ARCH-38, ARCH-42, ARCH-44.
- Zie ook: BIZ-50, BIZ-51, ARCH-35, ARCH-42
