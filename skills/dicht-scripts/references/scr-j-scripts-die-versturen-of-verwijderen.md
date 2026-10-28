# SCR J: Scripts die versturen of verwijderen

Compacte regels van `dicht-scripts`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/scripts-automatisering.md` (regelnummer in `regel-index.tsv`).

### SCR-45 Leg de poging vast vóór het effect en behandel "onbekend" als "gebeurd"
hoog · hard · api | app | klantproject · eigen bron · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet per item een rij op `bezig` vóór de verzending, betaling of verwijdering, zet hem daarna op `verstuurd`, `mislukt` of `onzeker`, laat een volgende run een rij op `bezig` of `onzeker` nooit opnieuw proberen, en pauzeer de lijn tot een mens die rij heeft beoordeeld. Aanvulling uit MSG-14: Bij mail: geef elke mail vooraf een unieke sleutel (ontvanger, sjabloon, stap) en zet de status op `onzeker` zodra de verbinding wegvalt nadat de inhoud is aangeboden (RFC 1047); de beoordeling van een onzekere mail mag ook door een aparte controle gebeuren, nooit door automatisch opnieuw te sturen.
- Bewijs: Een test die het proces doodt tussen verzenden en vastleggen (een nep-mailserver die het bericht aanneemt en daarna de verbinding verbreekt): de volgende run verstuurt niets naar die ontvanger en zet de lijn op pauze met een melding. Afgevinkt met de testuitvoer.
    Ook (uit MSG-14): Een test die de verbinding verbreekt na het versturen van de inhoud: de rij krijgt `onzeker`, er volgt geen tweede poging en de lijn pauzeert (PRIV-51); een unieke index op de sleutel (ontvanger, sjabloon, stap) weigert een tweede rij (DB-68). Afgevinkt met de testuitvoer en het schema.
- Norm: ASVS 5.0.0 V2.3.3 (L2), V16.5.3 (L2, "preventing fail-open conditions such as processing a transaction despite errors").
- Eigen bron: geen primaire bron; de uitwerking (rij vooraf, `onzeker` telt mee, lijn pauzeren) komt uit de eigen verzendlijnen; ASVS V2.3.3 en V16.5.3 dragen alleen het principe; het maildeel uit het samengevoegde MSG-14 rust wel op RFC 1047 en RFC 5321. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Dekt ook: MSG-14
- Zie ook: BIZ-40, API-41, API-49, ARCH-18

### SCR-46 Controleer de schakelaar en het plafond vlak voor elke afzonderlijke actie, en faal gesloten
hoog · hard · api | app | klantproject · eigen bron · tegenlezer: bevestigd (04-10-2026)
- Regel: Lees de noodstop en de teller voor het plafond uit de gedeelde opslag direct vóór elke afzonderlijke verzending of verwijdering (niet één keer aan het begin van de run), tel pogingen en niet alleen successen, en doe niets als de schakelaar of de teller niet te lezen is.
- Bewijs: Drie tests per lijn: (1) de schakelaar gaat uit tijdens een run en het volgende item wordt niet verwerkt; (2) de opslag is onbereikbaar en er wordt niets verstuurd; (3) mislukte pogingen vullen het plafond. Afgevinkt met de testuitvoer. Dit zijn de tests die AI-26 en PRIV-51 al vragen, met deze drie gevallen erbij.
- Norm: ASVS 5.0.0 V16.5.3 (L2), V2.3.2 (L2), V2.4.1 (L2).
- Eigen bron: geen primaire bron; de uitwerking (schakelaar en plafond vlak voor elke actie) komt uit de eigen verzendlijnen; ASVS V16.5.3, V2.3.2 en V2.4.1 dragen alleen het principe. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Zie ook: ARCH-76, AI-79, AI-26, PRIV-51, ARCH-77, BIZ-23, SCR-52, MSG-49, AI-73, ARCH-28, SCR-47, BIZ-21

### SCR-47 Laat een leeg, mislukt of genegeerd filter nooit "alles" betekenen
kritiek · hard · alles · eigen bron · tegenlezer: bevestigd (04-10-2026)
- Regel: Tel vóór elke bulkactie het aantal geselecteerde items, vergelijk het met het aantal dat je verwacht, en stop bij nul, bij meer dan verwacht en bij elke waarschuwing van het selecterende hulpmiddel; bouw de selectie nooit met een filter waarvan je niet hebt getest dat een onzinwaarde nul items oplevert.
- Bewijs: In het script staat een telling met een vergelijking vóór de actie; een test met een onzinfilter levert nul items en een stop op; de proefrun (ARCH-28) toont het aantal. Afgevinkt met script en testuitvoer.
- Norm: ASVS 5.0.0 V2.3.2 (L2), V16.5.3 (L2); BRIEF besluit 19.
- Eigen bron: geen primaire bron; de eis komt uit een eigen incident (10-06-2026, eigen ervaring); ASVS V2.3.2 en V16.5.3 dragen alleen het principe. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Zie ook: BIZ-23, AI-73, ARCH-28, SCR-46, BIZ-21, SCR-15, ARCH-51

### SCR-52 Bewaak het tijdvenster in het script zelf, niet alleen in de planning
middel · hard · api | app | klantproject · eigen bron · tegenlezer: niet tegengelezen
- Regel: Laat een script dat alleen binnen een tijdvenster mag versturen, bellen of wijzigen dat venster zelf controleren, direct vóór elke afzonderlijke actie en met een expliciete tijdzone (SCR-40), en laat het buiten het venster niets doen; de cron-regel of timer bepaalt alleen wanneer het script start.
- Bewijs: Drie tests: (1) het script buiten het venster gestart (de klok als parameter of nagemaakt) doet niets en zegt in de uitvoer waarom; (2) op de rand: de laatste minuut binnen het venster wel, de eerste minuut erbuiten niet; (3) het venster sluit tijdens een run en het volgende item wordt niet verwerkt. De controle staat in de lus naast de schakelaar en het plafond (SCR-46). Afgevinkt met de testuitvoer.
- Norm: geen ASVS-eis die dit letterlijk vraagt; ASVS 5.0.0 V2.3.2 (L2, grenzen van bedrijfslogica) naar de geest.
- Eigen bron: geen primaire bron; de eis komt uit de werkwijze van de eigen verzendlijnen (commentaar in de crontab, de scripts zelf niet gelezen) en een eigen incident (08-09-2026, SCR-40); geen primaire bron gevonden. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Zie ook: ARCH-76, AI-79, AI-26, PRIV-51, ARCH-77, SCR-46, BIZ-23, MSG-49, DB-74, ARCH-12, INFRA-71, BIZ-26, BIZ-27, BIZ-28, BIZ-29, SCR-40

### SCR-53 Stop een proces op proces-id of poort, nooit op een breed patroon
hoog · hard · alles · tegenlezer: niet tegengelezen
- Regel: Stop een eigen proces (testinstance, hulpserver, lus) op het proces-id dat je bij de start hebt vastgelegd (`kill "$pid"`, een pidbestand met `pkill -F`) of op de poort waarop het luistert (`fuser -k <poort>/tcp`); gebruik `pkill`, `pkill -f` en `killall` nooit met een patroon dat ook op een ander proces van dezelfde gebruiker kan passen, zoals de naam van een runtime (`node`, `python`, `tsx`) of een relatief pad (`tsx src/server.ts`), en nooit zonder patroon (`pkill -u <gebruiker>`).
- Bewijs: (1) `grep -rnE '\b(pkill|killall)\b' --include='*.sh' --include='*.py' .` geeft alleen regels met een pidbestand (`-F`), een ouder (`-P`) of een patroon met het volledige pad van de eigen map. (2) De PreToolUse-hook `pretool_gevaarlijk.py` weigert een brede opdracht en een patroon dat op dat moment op een proces van een systemd-dienst past; afgevinkt met de uitvoer van `test_hooks.py` (de gevallen onder SCR-53). (3) Na het stoppen van een testinstance: `systemctl show <dienst> -p ActiveEnterTimestamp` van de diensten met dezelfde opdracht is niet veranderd.
- Norm: geen ASVS-eis die dit letterlijk vraagt; ASVS 5.0.0 V2.3.2 (L2, grenzen van bedrijfslogica) naar de geest.
