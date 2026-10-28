# AI 3: Tools, agentrechten en menselijke goedkeuring

Compacte regels van `dicht-ai-mcp`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/ai-mcp.md` (regelnummer in `regel-index.tsv`).

### AI-19 Geef een agent alleen de tools die de taak nodig heeft
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Stel per agent en per taak de toolset samen uit een allowlist; een tool die de taak niet nodig heeft, wordt niet aangeboden, en een tool doet niet meer dan zijn naam zegt.
- Bewijs: Per agent staat de toolset in de code of de configuratie als expliciete lijst (geen "alle tools"), met per tool één regel reden. Een test start de agent en controleert dat de aangeboden toollijst gelijk is aan de allowlist. Afgevinkt met de lijst en de testuitvoer. Bij de eigen MCP-servers bestaat dit patroon al: de eigen CRM-server registreert voor Claude Desktop een aparte, beperktere set (`registerDesktopTools`, eigen ervaring; code niet opnieuw gelezen).
- Norm: OWASP LLM Top 10 2026 LLM03 maatregelen 1 en 2; OWASP Agentic 2026 ASI02; ASVS 5.0.0 V15.2.3 (L2, alleen benodigde functionaliteit in productie).

### AI-20 Bouw specifieke tools in plaats van open tools
hoog · richtlijn · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bied een model geen tool aan die een vrije shell-opdracht, vrije SQL, een vrije URL of een vrij bestandspad uitvoert als een specifieke tool met een strikt schema hetzelfde doel bereikt.
- Bewijs: De toollijst bevat geen tool met een vrij commando-, query-, URL- of padargument, of er staat per open tool een genoteerde reden plus de compenserende maatregel (alleen-lezen rol volgens DB-09, basismap volgens AI-46, goedkeuring volgens AI-24, en geen onvertrouwde invoer in dezelfde agent volgens AI-02). Afgevinkt met de lijst.
- Norm: OWASP LLM Top 10 2026 LLM03 maatregel 3; ASVS 5.0.0 V15.1.5 en V15.2.5 (L3, gevaarlijke functionaliteit apart beschermen).
- Zie ook: DB-09, AI-21

### AI-21 De identiteit achter een tool heeft minimale rechten in het achterliggende systeem
kritiek · hard · app | mcp | api | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Laat een tool met een eigen, minimale identiteit bij het achterliggende systeem komen: een databaserol met alleen de nodige tabellen en bewerkingen, een API-sleutel met alleen de nodige scopes, en nooit een beheerders- of servicerol die rij-niveau beveiliging omzeilt.
- Bewijs: Per tool is de gebruikte rol of sleutel benoemd. Voor databasetools: `\du` laat zien dat de rol geen `SUPERUSER` en geen `BYPASSRLS` heeft, en een test probeert met die rol een tabel buiten de scope te lezen en te wijzigen; beide falen. Afgevinkt met de uitvoer. Zie DB-01, DB-05, DB-09 en DB-14, en AUTH-56.
- Norm: OWASP LLM Top 10 2026 LLM03 maatregel 4; ASVS 5.0.0 V13.2.2 (L2) en V13.3.2 (L2); OWASP Agentic 2026 ASI03.
- Zie ook: INFRA-66, INFRA-10, AUTH-56, DB-02, INFRA-97, WP-45, WP-68, DB-09, AI-20

### AI-22 Voer tools uit in de context van de gebruiker en zijn tenant
kritiek · hard · app | mcp | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Leid de gebruiker en de tenant voor elke tool-aanroep af uit het geverifieerde token of de sessie, geef die context door in elke stap van een keten van tools of agents, en accepteer nooit een gebruikers- of tenant-id uit een toolargument of uit modeltekst.
- Bewijs: Geen enkel tool-schema bevat een veld voor tenant of gebruiker (`grep -n "tenant" <toolschema's>` laat alleen afleiding uit de context zien). De isolatietest uit AUTH-77 draait per tool met twee tenants: een id van tenant B geeft bij een token van tenant A een weigering of leeg resultaat. Afgevinkt met de testuitvoer. Zie AUTH-63, AUTH-72 en DB-17.
- Norm: OWASP LLM Top 10 2026 LLM03 maatregel 5; ASVS 5.0.0 V8.2.2 (L1), V8.4.1 (L2), V10.3.2 en V10.3.3 (L2); OWASP MCP Security Cheat Sheet (Confused Deputy).
- Zie ook: DB-13, AUTH-72, DB-17, AUTH-74, DB-12, DB-14, AUTH-73

### AI-23 Valideer elk toolargument als onvertrouwde invoer
hoog · hard · mcp | app | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke tool een strikt invoerschema (`additionalProperties: false`, grenzen en patronen per veld) en valideer daarnaast in de handler de betekenis: bestaat het object, hoort het bij deze tenant, is de toestand geschikt voor deze actie.
- Bewijs: Per tool een test met vier invoeren: een extra veld, een verkeerd type, een waarde die met `-` begint of `../` bevat, en een bestaand id van een andere tenant; alle vier worden geweigerd. Afgevinkt met de testuitvoer. Zie API-01, API-02, API-03 en API-06.
- Norm: MCP-specificatie 2026-07-28, server/tools, Security Considerations ("Servers MUST: Validate all tool inputs"); OWASP LLM Top 10 2026 LLM07 maatregel 3; ASVS 5.0.0 V2.2.1 (L1).
- Zie ook: API-01, AI-11, API-50, WP-13, ARCH-07

### AI-24 Een mens keurt elke onomkeerbare of naar buiten zichtbare actie goed, op de exacte inhoud
kritiek · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat versturen, betalen, boeken, definitief maken, verwijderen, publiceren en rechten wijzigen pas uitvoeren nadat een mens de exacte actie heeft gezien (ontvanger, volledige tekst, bedrag, doelobject, geen samenvatting) en goedgekeurd; bind de goedkeuring aan precies die parameters en laat hem kort gelden.
- Bewijs: (1) Een lijst van alle acties in de klasse onomkeerbaar of naar buiten zichtbaar, met per actie waar de goedkeuring plaatsvindt. (2) Een test die een concept na goedkeuring wijzigt en daarna laat versturen: de verzending wordt geweigerd. (3) Een test die de verstuurfunctie zonder goedkeuringsrecord aanroept: geweigerd. Afgevinkt met de lijst en beide testuitvoeren. Uitzonderingen (automatische lijnen) vallen onder AI-26.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregel 7 en LLM03 maatregel 6; MCP-specificatie 2026-07-28, server/tools ("there SHOULD always be a human in the loop with the ability to deny tool invocations"); OWASP AI Agent Security Cheat Sheet, High-Impact Action Integrity Controls; ASVS 5.0.0 V2.3.5 (L3, goedkeuring voor stromen met hoge waarde).
- Zie ook: SCR-51, SCR-49, SCR-50, AI-01, AI-25

### AI-25 De goedkeuring wordt buiten het model afgedwongen en faalt gesloten
kritiek · hard · app | mcp · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Leg de goedkeuring vast in een systeem dat het model niet kan beschrijven (database, sessie van de mens), controleer hem in de uitvoerende code, en weiger de actie als de risicoklasse onbekend is, de goedkeuring ontbreekt of verlopen is, of het auditlog niet te schrijven is.
- Bewijs: (1) Er is geen tool waarmee het model zijn eigen actie kan goedkeuren, of die tool vereist een geheim dat alleen de mens heeft (sessie, tweede factor). (2) Een test die de uitvoerende functie aanroept terwijl de goedkeuringstabel onbereikbaar is: de actie wordt geweigerd. (3) Tools die niet in de risicoklassering staan, vallen in de klasse "goedkeuring nodig". Afgevinkt met de testuitvoer. Zie WEB-63 en API-12.
- Norm: OWASP AI Agent Security Cheat Sheet ("Fail closed when risk classification, approval validation, policy lookup, or audit logging fails"; "Ensure the confirmation UI cannot be bypassed by LLM-crafted responses" in de MCP Security Cheat Sheet); ASVS 5.0.0 V16.5.3 (L2); OWASP Agentic 2026 ASI09 Human-Agent Trust Exploitation.
- Zie ook: SCR-51, SCR-49, SCR-50, AI-01, AI-24

### AI-26 Een automatische lijn heeft een plafond, een noodstop, een automatische pauze en een vaste vangrail
hoog · hard · app | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Geef elke AI-stroom die zonder menselijke goedkeuring handelt een hard maximum per dag, een noodstop die zonder deploy werkt, een automatische pauze bij elke afwijking (reactie, bounce, fout, onzekere verzending), een vaste tekst of vaste vangrails die een deterministische controle afdwingt, en een vastgelegd besluit van de eigenaar met begin- en einddatum.
- Bewijs: Per automatische lijn: (1) het plafond staat in code en een test laat zien dat verzending N+1 wordt geweigerd; (2) de noodstop is één commando of schakelaar en een test laat zien dat de lijn daarna niets doet; (3) een test voor elke pauzegrond; (4) de vaste controle weigert een tekst zonder de verplichte onderdelen; (5) het besluit met datum staat in de documentatie. Afgevinkt met vijf bewijzen per lijn.
- Norm: OWASP LLM Top 10 2026 LLM03 maatregelen 7 (gegradeerde handhaving) en 9 (stroomonderbrekers) en LLM06 maatregel 9; OWASP Agentic 2026 ASI08 Cascading Failures; ASVS 5.0.0 V2.3.2 (L2) en V2.4.1 (L2).
- Zie ook: ARCH-76, AI-79, PRIV-51, ARCH-77, SCR-46, BIZ-23, SCR-52, MSG-49

### AI-27 Een agent die commando's of code uitvoert, draait in een afgeschermde omgeving
hoog · richtlijn · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Laat een agent die shell-commando's, scripts of gegenereerde code uitvoert draaien met isolatie van bestandssysteem en netwerk (sandbox, container of aparte gebruiker), met alleen de mappen en hosts die de taak nodig heeft, en zonder toegang tot geheimen van andere projecten; en verwerk in een sessie zonder die isolatie geen onvertrouwde inhoud.
- Bewijs: Voor elke agent die commando's uitvoert, is vastgelegd welke isolatie geldt (sandbox aan, container, aparte gebruiker) en welke mappen en hosts bereikbaar zijn. Voor Claude Code: `permissions.defaultMode`, de `deny`-regels en `sandbox` in `~/.claude/settings.json` zijn bewust gekozen en genoteerd. Voor elke andere sessie geldt de regel en hoort de stand in de audit.
- Norm: OWASP LLM Top 10 2026 LLM06 maatregel 4 (sandbox) en LLM03; OWASP Agentic 2026 ASI05; ASVS 5.0.0 V15.2.5 (L3); MCP Security Best Practices, sectie Local MCP Server Compromise.

### AI-28 Geheimen blijven in code en komen nooit in de context van het model
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd API-sleutels, tokens, wachtwoorden en verbindingsstrings in de uitvoerende code en zet ze nooit in een systeemprompt, een toolbeschrijving, een toolresultaat, een voorbeeld of een bestand dat de agent als context leest; de tool gebruikt het geheim, het model ziet het niet.
- Bewijs: (1) `grep -rnE "(sk-|Bearer |password|secret|api[_-]?key)" <promptbestanden en toolbeschrijvingen>` geeft geen echte waarde. (2) Een test plaatst een nepgeheim met een herkenbare markering in de omgeving van de tool en controleert dat het in geen enkel toolresultaat en geen enkele modelaanroep voorkomt. (3) Tools die inloggegevens nodig hebben, lezen die uit de configuratie en hebben geen argument voor een sleutel. Afgevinkt met grep en testuitvoer. Zie API-65 en API-66.
- Norm: OWASP LLM Top 10 2026 LLM08 maatregel 1 en LLM01 maatregel 4 ("Hold credentials and state-change capability in application code, not the model"); ASVS 5.0.0 V13.3.1 (L2); MCP-specificatie 2026-07-28, client/elicitation (gevoelige gegevens niet via het model).
- Zie ook: INFRA-72, API-65, GIT-32, GIT-95, DB-62, WP-33, INFRA-76, WP-71, DB-61, AI-60, ARCH-49, SCR-19, SCR-20, SCR-05, SCR-13, SCR-16, SCR-50, MSG-41

### AI-29 Scheid lezen, klaarzetten en uitvoeren in aparte toolsets en scopes
middel · richtlijn · mcp | app · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Deel tools in drie klassen in (lezen, klaarzetten als concept, uitvoeren), geef elke klasse een eigen scope op het token, en geef een agent die onvertrouwde inhoud verwerkt nooit de klasse uitvoeren.
- Bewijs: Elk token heeft een scopelijst; een test met een leestoken roept een schrijftool en een uitvoertool aan en krijgt een weigering (bij OAuth: 403 met `insufficient_scope`). Afgevinkt met de testuitvoer. Zie AUTH-54 en AI-51.
- Norm: MCP Security Best Practices, sectie Scope Minimization; OWASP Agentic 2026 ASI03; ASVS 5.0.0 V8.2.1 (L1).

### AI-30 Een keten van agents geeft geen rechten en geen vertrouwen door
middel · richtlijn · app | mcp · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Geef een subagent alleen de tools en gegevens voor zijn deeltaak, behandel wat hij teruggeeft als onvertrouwde gegevens als hij onvertrouwde inhoud heeft gelezen, en laat een agent nooit op verzoek van een andere agent een actie uitvoeren die buiten zijn eigen grens valt.
- Bewijs: In het ontwerp staat per agent in de keten zijn toolset en of hij onvertrouwde inhoud leest. Een test laat een subagent een document met een injectie samenvatten en controleert dat de bovenliggende agent de gevraagde actie niet uitvoert. Afgevinkt met de testuitvoer.
- Norm: OWASP Agentic 2026 ASI07 Insecure Inter-Agent Communication en ASI08; OWASP LLM Top 10 2026 LLM03 maatregel 5 (gebruikerscontext behouden over ketens).

### AI-31 Begrens elke agentrun in stappen, tijd en kosten
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke agentrun en elke lus met een model een maximum aantal stappen, een maximale diepte van geneste aanroepen, een tijdslimiet en een kostenplafond per run, en stop de run hard als één ervan wordt bereikt.
- Bewijs: De limieten staan als constanten of configuratie in de code, en een test met een nep-tool die altijd "probeer opnieuw" teruggeeft, eindigt met een limietfout binnen de ingestelde grens. Afgevinkt met de testuitvoer en de waarden.
- Norm: OWASP LLM Top 10 2026 LLM06 Unbounded Consumption maatregel 9 ("Enforce step limits, recursion depth limits, time limits, and per-run cost ceilings"); ASVS 5.0.0 V15.2.2 (L2) en V2.4.1 (L2).
