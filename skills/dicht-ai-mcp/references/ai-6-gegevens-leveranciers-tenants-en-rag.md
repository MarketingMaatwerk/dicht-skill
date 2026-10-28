# AI 6: Gegevens, leveranciers, tenants en RAG

Compacte regels van `dicht-ai-mcp`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/ai-mcp.md` (regelnummer in `regel-index.tsv`).

### AI-65 Stuur alleen de velden naar een model die de taak nodig heeft
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw de context per taak op uit een allowlist van velden, kort lange teksten in, laat identificerende gegevens weg die de taak niet nodig heeft, en zet geen automatische "volledig profiel"-bijlage aan zonder reden per sjabloon.
- Bewijs: Per modelaanroep staat in de code welke velden meegaan (een expliciete lijst, geen `JSON.stringify(record)`), en een test controleert dat een veld buiten de lijst (bijvoorbeeld een IBAN of geboortedatum in het record) niet in de verstuurde prompt voorkomt. Afgevinkt met de testuitvoer. Zie API-09.
- Norm: OWASP LLM Top 10 2026 LLM02 Sensitive Information Disclosure, Tier 1 punt 2 ("Minimize context: send only task-required fields to external providers"); ASVS 5.0.0 V14.2.3 (L2) en V14.2.6 (L3); AVG artikel 5 lid 1 onder c (dataminimalisatie; artikelnummer niet vandaag nagelezen, zie Niet bevestigd).
- Zie ook: AI-66, PRIV-83, PRIV-14, PRIV-18, AI-72, PRIV-12, PRIV-03

### AI-66 Leg per modelleverancier vast onder welke voorwaarden de gegevens worden verwerkt
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg voor elke modelleverancier en elk account vast: onder welke voorwaarden het account valt (zakelijk of consument), of er een verwerkersovereenkomst is, hoe lang invoer en uitvoer worden bewaard, of ze voor training worden gebruikt, in welke regio wordt verwerkt, en welke soorten gegevens je er dus wel en niet naartoe mag sturen; en werk `policy-state.yaml` bij voordat de eerste echte klantgegevens gaan.
- Bewijs: Een tabel per leverancier en account met de zes punten, elk met bron-URL en datum, en de bijbehorende regel in `policy-state.yaml`. Vandaag bevestigd uit de bron: Anthropic verwijdert invoer en uitvoer van API-gebruikers standaard binnen 30 dagen, met uitzonderingen (onder meer tot 2 jaar bij een melding van overtreding van het gebruiksbeleid en tot 7 jaar voor classificatiescores; pagina bijgewerkt 01-07-2026), en gebruikt invoer en uitvoer van commerciële producten standaard niet voor training (pagina bijgewerkt 18-08-2026). Voor Mistral kon ik de eigen pagina vandaag niet openen (zie Niet bevestigd). Afgevinkt met de tabel.
- Norm: OWASP LLM Top 10 2026 LLM02 Tier 1 punt 7 ("technically enforce no-train/no-retain rather than policy text alone") en LLM04 maatregel 1 (voorwaarden en privacybeleid van leveranciers beoordelen); NIST AI 600-1 GV-6.1-004 (contracten en SLA's met derden); AVG artikel 28 (verwerker; uitwerking en controle in PRIV).
- Zie ook: PRIV-83, PRIV-14, PRIV-18, AI-72, PRIV-12, AI-65, PRIV-03

### AI-67 Behandel logs van prompts en antwoorden als de brongegevens zelf
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Log van een modelaanroep standaard alleen metagegevens (tijdstip, tenant, functie, model, tokens, duur, uitkomst, correlatie-id); log volledige prompts, antwoorden en redeneersporen alleen als dat nodig is, dan met dezelfde toegangsbeperking en bewaartermijn als de brongegevens, en nooit naar een externe log- of traceerdienst zonder besluit.
- Bewijs: `grep -rnE "console\.log|logger\.(info|debug)" <AI-code>` laat geen regel zien die een volledige prompt of een volledig antwoord logt, of die regel staat achter een schakelaar die in productie uit staat; de logtabel of het logbestand met inhoud heeft een opruimjob met een termijn. Afgevinkt met de grep-uitvoer en de opruimjob. Zie API-66, DB-83 en DB-88.
- Norm: OWASP LLM Top 10 2026 LLM02 Tier 1 punt 7 en Tier 2 punt 4; ASVS 5.0.0 V16.2.5 (L2), V14.2.4 (L2) en V14.2.7 (L3).
- Zie ook: ARCH-62, API-66, DB-88, INFRA-88, AUTH-14, AI-52, GIT-39

### AI-68 Zoek in een vectorindex altijd met het tenant- en rechtenfilter in de query zelf
kritiek · hard · app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Dwing bij elke zoekopdracht in embeddings het tenantfilter en het rechtenfilter af in de indexquery op de server, afgeleid uit de geverifieerde sessie; filter nooit pas na het ophalen en accepteer nooit een tenant of scope uit de aanvraag.
- Bewijs: De isolatietest uit AI-53 bevat een zoekvraag: tenant A zoekt op een unieke zin die alleen in een document van tenant B staat en krijgt nul resultaten. Bij een gedeelde index is het filter in de SQL of de indexaanroep aan te wijzen; bij een index per tenant (zoals het CRM met een database per tenant en pgvector, volgens eigen ervaring) is aan te wijzen dat de verbinding uit het token wordt gekozen. Afgevinkt met de testuitvoer. Zie AUTH-74, DB-13 en DB-16.
- Norm: OWASP LLM Top 10 2026 LLM09 Vector and Embedding Weaknesses maatregel 1 en LLM02 Tier 1 punt 3 ("Authorize before retrieval"); ASVS 5.0.0 V8.4.1 (L2).
- Zie ook: DB-23, AI-71, AUTH-69

### AI-69 Leg bij elk fragment in de kennisbank de herkomst vast en houd vertrouwensniveaus gescheiden
hoog · hard · app | mcp · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Sla bij elk fragment de bron, het tijdstip van inname, het vertrouwensniveau en de versie van de innamepijplijn op, normaliseer de tekst voor het embedden (AI-07, verborgen tekst weg), zet inhoud van buiten (web, mail van onbekenden, bijlagen) niet in dezelfde index als eigen, geverifieerde kennis zonder harde scheiding, en geef fragmenten uit onvertrouwde bron als onvertrouwde gegevens aan het model.
- Bewijs: De fragmenttabel heeft kolommen voor bron, tijdstip en vertrouwensniveau (`\d <tabel>`); een query haalt alle fragmenten van één bron op en verwijdert ze in één stap (geoefend op een testbron); een test met een document met witte of onzichtbare tekst laat zien dat die niet in het opgeslagen fragment staat. Afgevinkt met de drie uitvoeren.
- Norm: OWASP LLM Top 10 2026 LLM09 maatregelen 2 en 3 en LLM05 Data and Model Poisoning; OWASP Agentic 2026 ASI06.

### AI-70 Embeddings en afgeleide gegevens verdwijnen samen met de bron
middel · hard · app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwijder bij het verwijderen van een document, mail of contact ook de bijbehorende fragmenten, embeddings, samenvattingen, afgeleide feiten en cache-items binnen een vastgelegde termijn, controleer dat periodiek, en behandel back-ups van de vectoropslag met dezelfde gevoeligheid als de bron.
- Bewijs: Het verwijderscript uit DB-84 noemt de fragment- en feitentabellen, en een test verwijdert een bron en telt daarna nul fragmenten, nul afgeleide feiten en nul zoekresultaten voor een unieke zin uit die bron. Afgevinkt met de testuitvoer. Zie DB-83, DB-84 en DB-57.
- Norm: OWASP LLM Top 10 2026 LLM09 maatregelen 5 en 6; ASVS 5.0.0 V14.2.7 (L3); AVG artikel 17 (recht op gegevenswissing; uitwerking in PRIV).
- Zie ook: PRIV-21, DB-83, DB-84, PRIV-24, PRIV-26, DB-78, PRIV-22

### AI-71 Geen gedeelde context, cache of geheugen tussen tenants of gebruikers
kritiek · hard · app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd gespreksgeschiedenis, agentgeheugen, promptvoorvoegsels met gegevens, antwoordcaches en tussenresultaten per tenant en per gebruiker gescheiden; zet de tenant in elke cachesleutel, bewaar geen gegevens van een aanvraag in een variabele die meerdere aanvragen delen, en zet in een gedeelde systeemprompt nooit gegevens van één klant.
- Bewijs: `grep -rn "cache" <AI-code>` laat bij elke sleutel de tenant zien; een test stelt als tenant A en daarna als tenant B dezelfde vraag en controleert dat het tweede antwoord niets uit de gegevens van A bevat; er staat geen klantgegeven in een constante of een module-variabele. Afgevinkt met grep en testuitvoer. Zie AUTH-76 en DB-23.
- Norm: OWASP AI Agent Security Cheat Sheet, sectie 3 ("Implement memory isolation between users/sessions"); OWASP LLM Top 10 2026 LLM02 Tier 2 punt 5; ASVS 5.0.0 V8.4.1 (L2) en V14.2.2 (L2).
- Zie ook: DB-23, AI-68, AUTH-69

### AI-72 Bijzondere en zorggegevens gaan niet naar een model zonder vastgelegd besluit
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Stuur gezondheidsgegevens, andere bijzondere persoonsgegevens, inloggegevens en betaalgegevens pas naar een model nadat per gegevenssoort en per leverancier is vastgelegd dat het mag, onder welke overeenkomst en met welke bewaartermijn; zonder dat besluit houdt code ze uit de context.
- Bewijs: De gegevensclassificatie uit DB-87 heeft per klasse een kolom "mag naar model: ja, nee, onder voorwaarde" met verwijzing naar het besluit; een test met een record dat een veld uit een verboden klasse bevat, laat zien dat het veld niet in de prompt staat. Afgevinkt met de tabel en de testuitvoer. De juridische toets (grondslag, DPIA, NEN 7510) hoort in PRIV.
- Norm: OWASP LLM Top 10 2026 LLM02 Tier 1 punten 1 en 2; ASVS 5.0.0 V14.1.1 en V14.1.2 (L2); AVG artikel 9 en NEN 7510 (uitwerking en controle in PRIV; niet vandaag nagelezen).
- Zie ook: AI-66, PRIV-83, PRIV-14, PRIV-18, PRIV-12, AI-65, PRIV-03
