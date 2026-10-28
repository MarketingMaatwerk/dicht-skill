# AI 5: MCP-servers, skills en plugins van anderen gebruiken

Compacte regels van `dicht-ai-mcp`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/ai-mcp.md` (regelnummer in `regel-index.tsv`).

### AI-55 Beoordeel elke MCP-server voordat hij wordt aangesloten
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Sluit een MCP-server van een ander pas aan na een korte, vastgelegde beoordeling: wie is de uitgever, waar staat de broncode, wat doet hij op de machine en op het netwerk, welke tools en scopes vraagt hij, wanneer was de laatste release, en welke bekende kwetsbaarheden zijn er.
- Bewijs: Per aangesloten server staat in het project of in de eigen beheerdocumentatie een regel met uitgever, bron-URL, versie, datum van beoordeling, gevraagde rechten en de reden om hem te gebruiken (besluit 16 uit de brief: korte onderbouwing per nieuwe dependency). `claude mcp list` of de lijst in de configuratie bevat geen server zonder zo'n regel. Afgevinkt met de lijst.
- Norm: OWASP LLM Top 10 2026 LLM04 Supply Chain maatregel 1 en LLM01 maatregel 10; OWASP Agentic 2026 ASI04; OWASP MCP Security Cheat Sheet, sectie 9; ASVS 5.0.0 V15.1.2 (L2).

### AI-56 Zet elke MCP-server vast op een versie
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Start een MCP-server nooit met `npx -y <pakket>@latest`, `npx -y <pakket>` zonder versie, `uvx <pakket>` zonder versie of een container zonder digest; installeer een vaste versie via een lockfile of pin op een exacte versie of digest, en werk bij als een bewuste stap.
- Bewijs: `grep -nE "@latest|npx[^@]*\"-y\", *\"[^@\"]+\"" ~/.claude.json .mcp.json` geeft geen treffer; elke server heeft een exacte versie of digest. Afgevinkt met de grep-uitvoer. De minimale leeftijd van een versie en de controle van de lockfile horen in GIT.
- Norm: OWASP LLM Top 10 2026 LLM01 maatregel 10 en LLM04; OWASP MCP Security Cheat Sheet, sectie 9 ("Verify package integrity with checksums or code signing"); ASVS 5.0.0 V15.2.4 (L3).
- Zie ook: GIT-91, GIT-92, GIT-63, GIT-94, INFRA-37, GIT-96

### AI-57 Controleer naam en uitgever letter voor letter
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem de pakketnaam van een MCP-server, skill of plugin over van de officiële pagina van de uitgever en vergelijk hem letter voor letter met wat je installeert; installeer niets op basis van een naam die een model, een chatbericht of een zoekresultaat voorstelt.
- Bewijs: In de beoordeling uit AI-55 staat de bron-URL van de uitgever waar de naam vandaan komt, en `npm view <pakket> repository.url` (of het equivalent) wijst naar dezelfde repository. Afgevinkt met beide gegevens.
- Norm: OWASP LLM Top 10 2026 LLM04 maatregel 2 ("verify that AI-suggested dependencies exist and are the intended package before adopting them"); OWASP MCP Security Cheat Sheet, sectie 9.

### AI-58 Lees de toolbeschrijvingen en merk het op als ze veranderen
hoog · richtlijn · alles · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Lees bij het aansluiten de volledige beschrijving en het volledige schema van elke tool (ook parameternamen en standaardwaarden), wijs servers af met instructies die niets met de tool te maken hebben, bewaar een hash van de toollijst en beoordeel opnieuw als die verandert.
- Bewijs: Per server ligt de uitvoer van `tools/list` vast met datum en hash (bijvoorbeeld `sha256sum` over de opgeslagen JSON); bij een nieuwe versie wordt de hash vergeleken en het verschil gelezen. Afgevinkt met het opgeslagen bestand en de hash. De OWASP Cheat Sheet noemt het hulpmiddel `mcp-scan` hiervoor; dat is in dit onderzoek niet beoordeeld (zie Niet bevestigd).
- Norm: OWASP MCP Security Cheat Sheet, secties 2 en 11 ("Pin tool definitions using cryptographic hashes and alert on any changes"; "Re-prompt for consent when tool definitions change"); MCP-specificatie 2026-07-28, index (beschrijvingen van toolgedrag gelden als onvertrouwd tenzij van een vertrouwde server); OWASP Agentic 2026 ASI04.

### AI-59 Agentconfiguratie in een repository is code en wordt als code beoordeeld
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Behandel `.mcp.json`, `.claude/settings.json`, hooks, skills, slash-commando's, `CLAUDE.md` en vergelijkbare bestanden in een repository als uitvoerbare code: beoordeel elke wijziging in review, open een onbekende repository niet met een agent voordat je die bestanden hebt gelezen, en start in een onbekende map nooit een sessie zonder vertrouwensvraag.
- Bewijs: (1) In de eigen repositories vallen deze paden onder de reviewregel (CODEOWNERS of een afspraak in de werkwijze; uitwerking in GIT). (2) Voor een repo of archief van buiten: `find . -name '.mcp.json' -o -path '*/.claude/*' -o -name 'CLAUDE.md' -o -name 'AGENTS.md'` is uitgevoerd en de treffers zijn gelezen voordat een agent de map opent. Afgevinkt met de uitvoer en een notitie.
- Norm: OWASP Agentic 2026 ASI04 en ASI05; OWASP LLM Top 10 2026 LLM04; MCP Security Best Practices, Local MCP Server Compromise (kwaadaardig startcommando in een clientconfiguratie).

### AI-60 Tokens voor MCP-servers staan niet in platte tekst in bestanden die gedeeld, gevolgd of geback-upt worden
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet een token voor een MCP-server niet in een bestand dat in git staat of onversleuteld in een back-up belandt; gebruik de beveiligde opslag van de client, een omgevingsvariabele uit een geheimenbeheer, of een bestand met rechten `0600` dat buiten git en buiten gedeelde back-ups blijft.
- Bewijs: `git ls-files | grep -E "\.claude\.json|\.mcp\.json|mcp.*\.json"` gevolgd door `git grep -nE "Authorization|Bearer|API_KEY" -- <die bestanden>` geeft geen echte waarde; `stat -c '%a' ~/.claude.json` geeft `600`. Afgevinkt met de drie uitvoeren. Bij een treffer: token intrekken en nieuw uitgeven, daarna pas opruimen (de werkwijze voor een gelekt geheim hoort in GIT).
- Norm: OWASP MCP Security Cheat Sheet, sectie 6 ("Never store OAuth tokens in plaintext in MCP config files or application settings"); MCP-specificatie 2026-07-28, security-considerations, Token Theft ("Clients and servers MUST implement secure token storage"); ASVS 5.0.0 V13.3.1 (L2).
- Zie ook: INFRA-72, API-65, GIT-32, GIT-95, DB-62, AI-28, WP-33, INFRA-76, WP-71, DB-61, ARCH-49

### AI-61 Elke server krijgt een eigen credential met de kleinste scope
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke MCP-server en elke client een eigen token, deel nooit één token tussen servers, machines of mensen, vraag bij een dienst van derden de smalste scope (alleen-lezen waar het kan), en geef voorkeur aan kortlevende tokens boven persoonlijke tokens zonder einddatum.
- Bewijs: De tokenlijst van elke eigen server toont één token per client met een herkenbare naam en een laatst-gebruikt-datum; voor diensten van derden staat per koppeling de gekozen scope genoteerd. Afgevinkt met de lijst. Zie AUTH-54 en AUTH-56.
- Norm: OWASP MCP Security Cheat Sheet, sectie 1 ("Use scoped, per-server credentials; never share tokens across servers"; "Prefer ephemeral, short-lived tokens over long-lived PATs"); ASVS 5.0.0 V13.2.2 (L2).

### AI-62 Lees een skill of plugin van een ander volledig, inclusief scripts, en zet netwerkaanroepen uit
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Installeer een skill, plugin of hook van een ander pas nadat je de hele inhoud hebt gelezen (de instructietekst, alle scripts, alle afhankelijkheden), zoek naar netwerkadressen en ingebouwde sleutels, zet elke aanroep naar buiten uit die niet nodig is, en leg versie en bron vast.
- Bewijs: Per skill of plugin van een ander: `grep -rnE "https?://|urlopen|requests\.|fetch\(|curl |wget " <map>` is uitgevoerd en elke treffer is verklaard of uitgezet (voor prompt-guard: `PG_API_ENABLED=false`); bron, versie en datum van lezen staan genoteerd. Afgevinkt met de grep-uitvoer en de notitie.
- Norm: OWASP LLM Top 10 2026 LLM04 maatregel 1 en LLM01 maatregel 10; OWASP Agentic 2026 ASI04; ASVS 5.0.0 V13.2.4 (L2, allowlist van externe systemen) en V15.1.2 (L2).

### AI-63 Houd AI-gereedschap actueel en gebruik geen overbodige tussenlagen
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai agent-clients, SDK's en MCP-hulpmiddelen op een versie waarin de bekende kwetsbaarheden zijn opgelost, test na elke update dat de eigen koppelingen nog werken, en gebruik geen brugpakket (zoals `mcp-remote`) als de client de server rechtstreeks kan aansluiten.
- Bewijs: `claude --version` is minimaal 1.0.111; `npm ls -g mcp-remote @modelcontextprotocol/inspector` is leeg of toont minimaal 0.1.16 en 0.14.1; `grep -n "mcp-remote" ~/.claude.json <clientconfiguraties>` is leeg. Na een update draait de rooktest van de eigen koppelingen. Afgevinkt met de versies en de rooktest.
- Norm: OWASP LLM Top 10 2026 LLM04 maatregel 2 (patchbeleid, ook voor ontwikkelomgevingen); ASVS 5.0.0 V15.2.1 (L1).

### AI-64 Bouw je zelf een MCP-client, vertrouw dan niets wat een server teruggeeft
hoog · hard · app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Als je een eigen MCP-client of agent-host bouwt: sta voor autorisatie-URL's alleen `https` toe (en `http` alleen naar loopback tijdens ontwikkeling), open URL's nooit via een shell, pas op alle URL's uit serverantwoorden de SSRF-controles toe, toon bij het toevoegen van een lokale server het volledige commando en vraag om toestemming, toon toolinvoer voor uitvoering, en valideer toolresultaten voordat ze naar het model gaan.
- Bewijs: Alleen van toepassing als je een client bouwt; noteer anders "niet van toepassing". Als wel: unit-tests met een autorisatie-URL met `javascript:`, met `file:` en met `$(id)`; een test met `resource_metadata` naar een intern adres; een e2e-test die laat zien dat het volledige startcommando van een lokale server wordt getoond voor goedkeuring. Afgevinkt met de testuitvoer.
- Norm: MCP Security Best Practices, secties OAuth Authorization URL Validation ("MUST only allow http:// and https:// schemes"; "MUST NOT use shell commands to open URLs"), SSRF en Local MCP Server Compromise ("Show the exact command that will be executed, without truncation"); MCP-specificatie 2026-07-28, server/tools (clients tonen invoer, valideren resultaten, zetten time-outs).
