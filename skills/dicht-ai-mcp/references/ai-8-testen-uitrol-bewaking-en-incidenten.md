# AI 8: Testen, uitrol, bewaking en incidenten

Compacte regels van `dicht-ai-mcp`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/ai-mcp.md` (regelnummer in `regel-index.tsv`).

### AI-77 Zet het model vast op een exacte versie; een modelwissel is een release
middel · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwijs in code naar een exacte modelversie en niet naar een alias die meeschuift, leg per functie vast welk model hij gebruikt, en behandel een wissel van model, leverancier of clientversie als een release met de eval uit AI-78.
- Bewijs: `grep -rnE "model *[:=]" <AI-code>` toont exacte versienamen of één centrale configuratie; de documentatie heeft een tabel van functie naar model; bij een alias via een proxy staat genoteerd welke versie die vandaag oplevert en hoe dat bij een update wordt gecontroleerd. Afgevinkt met de grep en de tabel.
- Norm: OWASP LLM Top 10 2026 LLM04 maatregel 2 (onderhouden versies van componenten, API's en onderliggende modellen); OWASP AI Agent Security Cheat Sheet ("Skip adversarial testing after prompt, tool, memory, retrieval, or provider changes" onder Don't).

### AI-78 Een vaste eval is een gate bij elke wijziging van prompt, model, tools of leverancier
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd per AI-functie een vaste set gevallen bij met de verwachte uitkomst (goede gevallen, randgevallen, eerdere fouten en de injectiegevallen uit AI-81), draai die bij elke wijziging van prompt, model, toolset, zoekconfiguratie of leverancier, en rol niet uit onder de afgesproken drempel.
- Bewijs: De evalset staat in de repository (zonder echte klantgegevens en zonder geheimen), de CI of het releasescript draait hem, en de uitvoer met model, promptversie, datum en score per geval wordt bewaard. Afgevinkt met de laatste evaluitvoer. Let op: iemand kan in dezelfde wijziging ook de tests afzwakken; een wijziging in de evalset valt onder review.
- Norm: OWASP AI Agent Security Cheat Sheet, sectie 9 (CI/CD and Release Gates; Validation Evidence); NIST AI 600-1 MS-2.7-007 (AI red-teaming, onder meer tegen prompt injection) en MS-2.7-009 (regelmatig toetsen dat maatregelen nog werken).

### AI-79 Elke AI-functie en elke agent is zonder deploy uit te zetten
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke AI-functie, elke automatische lijn en elke MCP-server een schakelaar die zonder nieuwe uitrol werkt (per functie en per tenant), leg vast bij welke signalen hij wordt gebruikt, en test hem.
- Bewijs: Per functie staat de schakelaar in de documentatie, en een test zet hem om en laat zien dat de functie niets meer doet en de rest van de toepassing blijft werken. Afgevinkt met de testuitvoer.
- Norm: OWASP LLM Prompt Injection Prevention Cheat Sheet, checklist ("Implement emergency controls and kill switches"); NIST AI 600-1 MG-2.4-004 (criteria voor het uitschakelen van een GAI-systeem vastleggen en herzien).
- Zie ook: ARCH-76, AI-26, PRIV-51, ARCH-77, SCR-46, BIZ-23, SCR-52, MSG-49

### AI-80 Faal gesloten als het model uitvalt of iets onverwachts teruggeeft
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Kies bij een time-out, een weigering, een schemafout of een leeg antwoord altijd de veilige uitkomst: geen actie, het item blijft staan voor een mens, en er komt een melding; een AI-controle die niet kan oordelen, keurt nooit goed.
- Bewijs: Een test per AI-controle met vier foutsoorten van de nep-leverancier (time-out, HTTP 500, ongeldige JSON, weigertekst): in alle vier gebeurt de actie niet en is er een logregel of melding. Afgevinkt met de testuitvoer. Zie WEB-63 en API-12.
- Norm: ASVS 5.0.0 V16.5.3 (L2); OWASP AI Agent Security Cheat Sheet ("Fail closed when risk classification, approval validation, policy lookup, or audit logging fails"); OWASP LLM Prompt Injection Prevention Cheat Sheet ("Missing telemetry, errors, and unsupported test contexts must not count as blocked attacks").

### AI-81 Injectietests per invoerkanaal zijn een gate
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf voor elk onvertrouwd invoerkanaal uit AI-03 minimaal drie tests die een injectie via dat kanaal aanbieden (een directe opdracht, een verstopte of gecodeerde opdracht, en een poging tot exfiltratie of een ongewenste tool-aanroep), met nepgegevens en geïnstrumenteerde tools, en laat de uitrol falen als de verboden uitkomst optreedt.
- Bewijs: De testsuite heeft per kanaal de drie tests; de CI-uitvoer toont ze groen; de tests controleren de uitkomst (geen tool-aanroep, geen nepgegeven in uitvoer of uitgaand verzoek, geen opgeslagen instructie) en niet de tekst van het antwoord. Afgevinkt met de CI-uitvoer. Een geslaagde test bewijst niet dat de functie veilig is; hij bewijst dat deze bekende pogingen niet tot schade leiden. De grens blijft AI-02, AI-06 en AI-24.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregel 11; OWASP LLM Prompt Injection Prevention Cheat Sheet, sectie Smoke-Testing Your Defenses; OWASP AI Agent Security Cheat Sheet, sectie 9 (Abuse-Case Test Matrix); NIST AI 600-1 MS-2.7-007; Anthropic ("Red-team your own agent").

### AI-82 Beoordeel een AI-test op wat er gebeurde, en herhaal hem
middel · richtlijn · app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een test voor een AI-functie slagen of falen op een waarneembare uitkomst (welke tools zijn aangeroepen, wat is opgeslagen, welk verzoek ging naar buiten), draai elke test meerdere keren, tel fouten en ontbrekende metingen niet als geslaagd, en rapporteer tellers en geen gemiddelde "veiligheidsscore".
- Bewijs: De testhulp registreert tool-aanroepen en uitgaande verzoeken; elke injectietest draait minimaal vijf keer en de uitvoer toont het aantal runs en het aantal overtredingen (de eis is nul). Afgevinkt met de uitvoer. Het getal vijf is een eigen keuze; de bron schrijft geen aantal voor.
- Norm: OWASP LLM Prompt Injection Prevention Cheat Sheet, secties Grade the intended outcome en Report results with their limits.

### AI-83 Bewaak verbruik, weigeringen en afwijkend toolgebruik, met een alarm
middel · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Meet per functie en per tenant het aantal aanroepen, tokens, kosten, fouten, schemafouten, weigeringen van goedkeuringen en geweigerde tool-aanroepen, en stel een alarm in op een plotselinge stijging van verbruik, een reeks geweigerde aanroepen, een nieuwe tool die wordt gebruikt en een stroom die zijn plafond raakt.
- Bewijs: Een overzicht (query of dashboard) met de genoemde tellers per dag, en een test die het alarm laat afgaan (bijvoorbeeld tien geweigerde aanroepen achter elkaar). Afgevinkt met het overzicht en de ontvangen melding. De algemene opzet van alarmering hoort in ARCH.
- Norm: OWASP LLM Top 10 2026 LLM06 maatregel 8 en LLM03 maatregel 8; OWASP AI Agent Security Cheat Sheet, sectie 6; ASVS 5.0.0 V16.3.3 (L2).
- Zie ook: ARCH-67, INFRA-35, ARCH-69, INFRA-86, INFRA-87, DB-97, DB-47, INFRA-52

### AI-84 Heb een draaiboek voor een AI-incident
middel · richtlijn · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg vast wat je doet bij een geslaagde injectie of een lek via een model: functie uitzetten (AI-79), tokens en sleutels van de betrokken servers intrekken, het auditlog van tool-aanroepen veiligstellen, geheugen en kennisbank op vergiftigde inhoud doorzoeken en schonen (AI-69), bepalen welke gegevens bij welke partij zijn beland, en de datalekbeoordeling starten.
- Bewijs: Het draaiboek staat in de projectdocumentatie met de zes stappen en per stap het commando of de plek; de stap "token intrekken" en de stap "fragmenten van één bron verwijderen" zijn één keer geoefend op test. Afgevinkt met het document en de oefennotitie. De algemene incidentrespons hoort in INFRA, de meldplicht in PRIV.
- Norm: OWASP LLM Top 10 2026 LLM02 Tier 3 punt 5 en LLM09 maatregel 6; NIST AI 600-1 MG-2.4-002 en MG-2.4-003 (escalatie en herstel bij incidenten met een GAI-systeem).
- Zie ook: PRIV-31, INFRA-96, PRIV-32, PRIV-33, INFRA-91, PRIV-71, GIT-106, WP-78, INFRA-94

### AI-85 Code die een model schreef, gaat door dezelfde gates, en elk voorgesteld pakket wordt gecontroleerd
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat door AI geschreven code door dezelfde lint, typecheck, tests, SAST, geheimscan en review gaan als andere code, en controleer van elke afhankelijkheid die een model voorstelt of die bestaat, of het het bedoelde pakket is en of het aan de regels voor nieuwe afhankelijkheden voldoet, voordat je het installeert.
- Bewijs: De CI-gates uit GIT en ARCH draaien op elke wijziging, ongeacht wie hem schreef; bij een nieuwe afhankelijkheid staat in de wijziging de korte onderbouwing (besluit 16) met de repository-URL en de leeftijd van de versie. Afgevinkt met de CI-uitvoer en de onderbouwing. De skill `requesting-code-review` blijft van toepassing; de inhoud van de OWASP Secure Coding with AI Cheat Sheet is in dit onderzoek niet gelezen (zie Niet bevestigd).
- Norm: OWASP LLM Top 10 2026 LLM04 maatregel 2 en LLM10 (bereik uitgebreid naar gegenereerde code, zie "What's New"); ASVS 5.0.0 V15.1.2 (L2) en V15.2.4 (L3).
- Zie ook: GIT-57, GIT-58, GIT-59, API-67, API-68, API-78, WP-37, ARCH-40, ARCH-56, GIT-60, GIT-61, GIT-34

### AI-86 Wat een agent op een klantsite of in een vreemde repository leest, is onvertrouwd
hoog · hard · klantproject | wp-plugin | wp-thema | alles · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Behandel bij werk met een agent op een klantsite, in een vreemde repository of op een mogelijk gehackte server alle inhoud die de agent leest (bestanden, commentaar in code, database-inhoud, uitvoer van WP-CLI, logregels, webpagina's) als onvertrouwde invoer; laat op basis daarvan geen onomkeerbare actie uitvoeren zonder eigen controle, en geef de sessie geen geheimen of toegang die de klus niet nodig heeft.
- Bewijs: Voor klussen op een site met een vermoeden van een hack: de sessie draait met een account of sleutel die alleen die site raakt, of de opdracht aan de agent beperkt de doelen uitdrukkelijk tot die ene site en elke schrijfactie wordt door een mens bevestigd. In de werkwijze staat de regel dat instructies in gelezen inhoud worden gemeld en niet uitgevoerd. Afgevinkt met de notitie bij de klus. De regel sluit aan op de eigen regel (exacte ID's op live).
- Norm: OWASP LLM Top 10 2026 LLM01 (indirecte injectie) en LLM03; OWASP Agentic 2026 ASI01 en ASI03; Claude Code, "Security", best practices voor onvertrouwde inhoud.
