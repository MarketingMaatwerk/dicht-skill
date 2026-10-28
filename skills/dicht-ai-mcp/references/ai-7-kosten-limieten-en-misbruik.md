# AI 7: Kosten, limieten en misbruik

Compacte regels van `dicht-ai-mcp`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/ai-mcp.md` (regelnummer in `regel-index.tsv`).

### AI-73 Zet een hard uitgavenplafond dat stopt, niet alleen waarschuwt
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel per API-sleutel, per tenant en per account bij de leverancier een maximum per dag en per maand in dat verdere aanroepen blokkeert, en bouw in de eigen code een tweede plafond per tenant dat onafhankelijk van de leverancier telt.
- Bewijs: De instelling bij de leverancier (schermafbeelding of API-uitvoer met het ingestelde maximum) en een test van het eigen plafond: na het bereiken van de grens voor een testtenant weigert de volgende aanroep met een nette fout. Afgevinkt met beide. Zie API-34.
- Norm: OWASP LLM Top 10 2026 LLM06 Unbounded Consumption maatregel 2 (Hard Spending Caps); ASVS 5.0.0 V2.4.1 (L2) en V2.1.3 (L2).
- Zie ook: BIZ-23, ARCH-28, SCR-46, SCR-47, BIZ-21

### AI-74 Begrens per gebruiker de invoer, de uitvoer en het aantal aanroepen
hoog · hard · app | mcp | website | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke AI-functie een maximum op de invoergrootte (geweigerd voordat het model wordt aangeroepen), een maximum op de uitvoer (`max_tokens`), en een limiet per gebruiker en per tenant in aanroepen en in tokens per minuut en per dag; geef een publieke AI-functie zonder login bovendien de botbescherming uit WEB-67.
- Bewijs: Een test met een invoer boven de grens geeft een weigering zonder modelaanroep (de teller van aanroepen blijft gelijk); `max_tokens` staat in elke aanroep; een lus boven de gebruikerslimiet geeft 429. Afgevinkt met de testuitvoer. Zie API-03, API-20 en WEB-66.
- Norm: OWASP LLM Top 10 2026 LLM06 maatregelen 1 en 3; ASVS 5.0.0 V2.4.1 (L2) en V15.2.2 (L2).
- Zie ook: API-20, WEB-66, INFRA-46, API-22, AUTH-10, WP-57, AI-45, API-34, BIZ-21, BIZ-23, BIZ-37, BIZ-32, BIZ-20, BIZ-38

### AI-75 Een modelproxy of inferentie-eindpunt is nooit zonder authenticatie bereikbaar
kritiek · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke eigen modelproxy, lokale modelserver en elk inferentie-eindpunt alleen luisteren op het adres dat nodig is, eis een sleutel per aanroepende dienst, en log per dienst het verbruik; een open poort op `0.0.0.0` met alleen een firewallregel is geen authenticatie.
- Bewijs: `ss -tlnp | grep -E ':(3456|11434) '` toont het bedoelde adres; een aanroep zonder sleutel geeft 401; per dienst is er een eigen sleutel en een verbruiksregel in het log. Afgevinkt met de drie uitvoeren. Zie AUTH-56 en API-25.
- Norm: OWASP LLM Top 10 2026 LLM06 maatregel 10 ("enforce authentication on all inference endpoints"); ASVS 5.0.0 V13.2.1 (L2).
- Zie ook: INFRA-13, DB-58, INFRA-14, INFRA-12, AI-39

### AI-76 Geef elke modelaanroep een time-out en een begrensde herhaling
middel · hard · app | mcp | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke modelaanroep een time-out, herhaal alleen bij tijdelijke fouten met oplopende wachttijd en een maximum aantal pogingen, herhaal nooit een stap die al een extern effect had, en doe de aanroep buiten een databasetransactie.
- Bewijs: De aanroepfunctie heeft een time-out en een maximum aantal pogingen in de code; een test met een nep-leverancier die eerst een time-out en dan een antwoord geeft, laat één resultaat en één effect zien. Afgevinkt met de testuitvoer. Zie API-48, API-49, API-33 en DB-73.
- Norm: ASVS 5.0.0 V16.5.2 (L2) en V15.2.2 (L2); OWASP LLM Top 10 2026 LLM06 maatregel 5 (graceful degradation); MCP-specificatie 2026-07-28, server/tools (clients zetten time-outs op tool-aanroepen).
- Zie ook: API-48, API-49, ARCH-13, ARCH-14, DB-65, API-19, SCR-21, SCR-25, SCR-26, SCR-43, MSG-42
