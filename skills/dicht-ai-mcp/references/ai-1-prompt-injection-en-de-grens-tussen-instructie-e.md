# AI 1: Prompt injection en de grens tussen instructie en gegevens

Compacte regels van `dicht-ai-mcp`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/ai-mcp.md` (regelnummer in `regel-index.tsv`).

### AI-01 Ontwerp op de aanname dat de injectie slaagt
kritiek · hard · app | mcp | api | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Leg per AI-functie vast wat er gebeurt als het model volledig door een aanvaller wordt bestuurd, en begrens tools, rechten en uitvoerkanalen zo dat die situatie geen schade buiten het gesprek kan aanrichten.
- Bewijs: In de projectdocumentatie staat per AI-functie een tabel met drie kolommen: welke onvertrouwde invoer het model leest, bij welke gegevens het kan, welke acties of uitvoerkanalen het heeft. Onder de tabel staat per functie in één zin wat een aanvaller maximaal bereikt. Afgevinkt als de tabel er is en de regels AI-02, AI-06 en AI-24 erop zijn toegepast.
- Norm: OWASP LLM Top 10 2026 LLM01 (inleiding van de maatregelen); OWASP Agentic 2026 ASI01; NIST AI 600-1 paragraaf 2.9 Information Security; ASVS 5.0.0 V15.1.5 (L3, gevaarlijke functionaliteit documenteren).
- Zie ook: SCR-51, SCR-49, SCR-50, AI-24, AI-25

### AI-02 Geen agent met onvertrouwde invoer, gevoelige data en een uitweg tegelijk
kritiek · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Laat een agent nooit zonder menselijke goedkeuring per actie tegelijk (A) onvertrouwde inhoud lezen, (B) bij gevoelige gegevens kunnen en (C) iets wijzigen of naar buiten communiceren; haal één van de drie weg of zet goedkeuring op C.
- Bewijs: De tabel uit AI-01 heeft per agent de kolommen A, B en C. Geen rij heeft drie keer "ja" zonder een verwijzing naar de goedkeuringsstap. Voor rijen met twee keer "ja" (A en B, of A en C) staat het restrisico in één zin genoteerd. Afgevinkt met de tabel.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregel 8 ("Rule of Two") en LLM03 Excessive Agency; OWASP Agentic 2026 ASI01 en ASI02.

### AI-03 Ken elke bron die in de context komt en geef hem een vertrouwensniveau
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak per AI-functie een lijst van alles wat in de context van het model terechtkomt (gebruikersinvoer, mailtekst, onderwerp, afzendernaam, bijlagen, webpagina's, zoekresultaten, RAG-fragmenten, tool-uitvoer, bestandsnamen, transcripties, geheugen) en markeer elke bron als vertrouwd (eigen code en configuratie) of onvertrouwd (al het andere).
- Bewijs: De bronnenlijst staat in de documentatie of als commentaar boven de promptopbouw, en elke onvertrouwde bron is in de code terug te vinden als afgebakend blok (AI-04). Controle: zoek in de promptcode naar elke variabele die in de prompt wordt gezet (`grep -n '\${' <promptbestand>`) en leg hem naast de lijst. Afgevinkt als geen variabele ontbreekt.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregel 6; NIST AI 600-1 paragraaf 2.9 (indirecte injectie via "data likely to be retrieved"); ASVS 5.0.0 V2.2.1 (L1).
- Zie ook: MSG-22, MSG-24, MSG-25, MSG-31, MSG-33

### AI-04 Lever onvertrouwde inhoud via een gescheiden, gelabeld kanaal
hoog · hard · app | mcp | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Zet onvertrouwde inhoud nooit in de systeemprompt; lever hem als afgebakend blok met vermelding van soort en herkomst, als JSON-gecodeerde waarde, en bij Claude in een `tool_result`-blok en niet in een gewoon `user`-tekstblok; zet je eigen instructies daar nooit tussen (die horen in een `user`-beurt na het `tool_result`).
- Bewijs: (1) `grep -n "system" <promptcode>` laat alleen vaste strings of vertrouwde configuratie in de systeemprompt zien. (2) Een unit-test die een mail met `</email>` en met een aanhalingsteken plus sluitaccolade instuurt en controleert dat het gebouwde bericht nog steeds één geldig JSON-object of één ongebroken blok is. Afgevinkt met grep en testuitvoer.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregel 6 (met de kanttekening dat een aanvaller die de markering kent hem kan nabootsen); ASVS 5.0.0 V1.1.2 (L2).

### AI-05 Zet het beleid in de systeemprompt, maar bouw er niets op
middel · richtlijn · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zeg in de systeemprompt met stellige toestaan- en verbieden-zinnen wat het model doet, dat inhoud uit tools, mail en documenten gegevens zijn en nooit opdrachten, en wat het doet als het instructies in die inhoud ziet; behandel dit als een laag die de kans verlaagt en nooit als de controle zelf.
- Bewijs: De systeemprompt bevat het beleid voor onvertrouwde inhoud (leesbaar in de code), en voor elke verbodszin in de prompt die een beveiligingsgrens beschrijft is in de code een afdwingende controle aan te wijzen (regelnummer). Afgevinkt met de lijst van verbodszin naar controle.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregel 1 en LLM08 Hidden Context Exposure maatregel 2.

### AI-06 Dwing autorisatie en beveiligingsbesluiten af in code, nooit in het model
kritiek · hard · app | mcp | api | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Laat het model nooit beslissen of iets mag; controleer rechten, tenant, bedragen, ontvangers en toestand in gewone code op het moment van uitvoeren, voor elke aanroep die het model voorstelt.
- Bewijs: Per tool een test die de tool rechtstreeks aanroept (zonder model) met een gebruiker zonder rechten en met een object van een andere tenant; beide geven een weigering. Afgevinkt als die test voor elke muterende tool in CI draait. Zie AUTH-62, AUTH-63 en AUTH-66.
- Norm: OWASP LLM Top 10 2026 LLM03 maatregel 7 (complete mediation) en LLM08 maatregel 3; ASVS 5.0.0 V8.3.1 (L1), V8.2.1 en V8.2.2 (L1); OWASP Agentic 2026 ASI03.

### AI-07 Verwijder onzichtbare tekens bij inname en bij weergave
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Strip uit elke onvertrouwde tekst die naar een model gaat, en uit elke modeluitvoer die je toont of doorgeeft, de Unicode-tagtekens (U+E0000 tot en met U+E007F), de variatiekiezers (U+FE00 tot en met U+FE0F) en de breedteloze tekens (U+200B, U+200C, U+200D, U+2060).
- Bewijs: Een unit-test die een tekst met een verborgen zin in tagtekens door de innamefunctie haalt en controleert dat de uitvoer geen codepunt uit de genoemde reeksen bevat; dezelfde test op de functie die modeluitvoer klaarmaakt voor weergave. Afgevinkt met de testuitvoer. Let op: emoji met een variatiekiezer verliezen hun kleurvariant; dat is aanvaard voor tekst die naar een model gaat.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregel 5 en LLM09 maatregel 2 (normaliseren voor het embedden).

### AI-08 Behandel elke modaliteit en elk afgeleid tekstveld als invoer
middel · richtlijn · app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Pas dezelfde regels (afbakenen, strippen, begrenzen) toe op tekst die uit een afbeelding, pdf, audio-opname of documentmetadata komt, en geef het model geen bestand van buiten zonder dat de toepassing ervan uitgaat dat er instructies in staan.
- Bewijs: De bronnenlijst uit AI-03 noemt elke modaliteit apart, en er is per modaliteit één injectietest in de testset van AI-81 (bijvoorbeeld een pdf met verborgen tekst, een transcript met een gesproken opdracht). Afgevinkt met de testuitvoer.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregel 3.

### AI-09 Een injectiefilter of bewakingsmodel is een extra laag, geen grens
middel · richtlijn · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik patroonfilters (zoals de skill `prompt-guard`) en een klein bewakingsmodel alleen als signaal en extra drempel, log elke beslissing ervan, en laat geen enkele regel uit dit document vervallen omdat er een filter voor staat.
- Bewijs: In het ontwerp staat het filter als laag naast, en niet in plaats van, AI-02, AI-06 en AI-24. De beslissingen van het filter worden gelogd (aantal doorgelaten, gemarkeerd, geblokkeerd per dag). Afgevinkt als beide aantoonbaar zijn. Als je het bewakingsmodel van Anthropic gebruikt: het patroon (klein model, gestructureerde uitvoer met één boolean, pas daarna de inhoud als `tool_result` doorgeven) staat in de Anthropic-documentatie.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregelen 3 en 11; OWASP LLM Prompt Injection Prevention Cheat Sheet, sectie Model-Based Guardrails (kanttekeningen).

### AI-10 Schrijven naar geheugen of duurzame context is een geprivilegieerde handeling
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Laat een model alleen feiten naar duurzaam geheugen schrijven (kennisbank, klantprofiel, notities, geheugenbestanden, instructiebestanden) via een pad dat de bron vastlegt, de inhoud begrenst en instructie-achtige inhoud tegenhoudt of ter goedkeuring voorlegt; en lees geheugen dat uit onvertrouwde bron is afgeleid terug als onvertrouwde gegevens.
- Bewijs: (1) Elk opgeslagen feit heeft een bronverwijzing (mail-id, document-id, gebruiker) en een tijdstip in de database. (2) Een test met een document dat een opdracht en een betaalgegeven bevat: het resultaat is geen opgeslagen instructie, en een gewijzigd betaal- of contactgegeven wordt niet zonder menselijke bevestiging overgenomen. (3) Bestanden die een agent als instructie leest (`CLAUDE.md`, skills, geheugenbestanden) zijn niet schrijfbaar voor een proces dat onvertrouwde inhoud verwerkt, of wijzigingen lopen via git en review. Afgevinkt met de testuitvoer en de bronkolom.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregel 9; OWASP Agentic 2026 ASI06 Memory and Context Poisoning; ASVS 5.0.0 V2.2.1 (L1).
