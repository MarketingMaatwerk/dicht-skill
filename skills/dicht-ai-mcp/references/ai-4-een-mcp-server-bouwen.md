# AI 4: Een MCP-server bouwen

Compacte regels van `dicht-ai-mcp`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/ai-mcp.md` (regelnummer in `regel-index.tsv`).

### AI-32 Elke MCP-server die niet uitsluitend lokaal via stdio draait, eist authenticatie op elke aanvraag
kritiek · hard · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer op elke HTTP-aanvraag aan een MCP-eindpunt een geldig token in de `Authorization`-header voordat je iets van de aanvraag verwerkt, en antwoord met 401 bij een ontbrekend, ongeldig of verlopen token.
- Bewijs: `curl -s -o /dev/null -w '%{http_code}' -X POST https://<host>/mcp -H 'Content-Type: application/json' -d '{}'` geeft 401; hetzelfde met een ingetrokken token geeft 401. Afgevinkt met beide uitvoeren. Zie AUTH-55.
- Norm: MCP-specificatie 2026-07-28, basic/authorization ("authorization MUST be included in every HTTP request from client to server"; "Invalid or expired tokens MUST receive a HTTP 401 response") en basic/transports/streamable-http ("Servers SHOULD implement proper authentication for all connections"); ASVS 5.0.0 V13.2.1 (L2).
- Zie ook: AUTH-49, AI-33, AI-34, AI-36

### AI-33 Accepteer alleen tokens die voor deze server zijn uitgegeven
kritiek · hard · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Valideer bij OAuth-tokens dat de server zelf het beoogde publiek is (de `aud`-claim of de uitkomst van introspectie bevat de canonieke URI van deze MCP-server) en weiger elk ander token, ook als handtekening en geldigheid kloppen.
- Bewijs: Een test biedt een geldig ondertekend token aan met een ander publiek (een andere `aud` of `resource`): de server antwoordt 401. Afgevinkt met de testuitvoer. Niet van toepassing bij ondoorzichtige eigen API-tokens die alleen deze server kent (AI-37); noteer dat dan. Zie AUTH-41 en AUTH-49.
- Norm: MCP-specificatie 2026-07-28, basic/authorization, Token Handling ("MCP servers MUST validate that access tokens were issued specifically for them as the intended audience") en security-considerations, Access Token Privilege Restriction; RFC 8707; ASVS 5.0.0 V10.3.1 (L2) en V9.2.3 (L2).
- Zie ook: AUTH-49, AI-34, AI-32, AI-36

### AI-34 Geef het token van de client nooit door aan een achterliggende API
kritiek · hard · mcp · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Gebruik voor aanroepen naar een achterliggende dienst een eigen credential van de MCP-server (of een apart token dat de server zelf als OAuth-client voor die gebruiker heeft verkregen) en stuur het token dat de MCP-client aanbood nooit door.
- Bewijs: `grep -rn "authorization" <servercode>` laat zien dat de binnenkomende header alleen wordt gelezen voor validatie en nergens in een uitgaande aanvraag wordt gezet; uitgaande aanroepen gebruiken een sleutel uit de configuratie of een per gebruiker opgeslagen token van de achterliggende dienst. Afgevinkt met de grep en de aanwijzing in de code.
- Norm: MCP-specificatie 2026-07-28, basic/authorization ("MCP servers MUST NOT accept or transit any other tokens") en security-considerations ("The MCP server MUST NOT pass through the token it received from the MCP client"); MCP Security Best Practices, Token Passthrough.
- Zie ook: AUTH-49, AI-33, AI-32, AI-36

### AI-35 Tokens staan in de Authorization-header, nooit in de URL
hoog · hard · mcp | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Accepteer een token alleen in de `Authorization: Bearer`-header en weiger een token in de queryreeks of het pad; maak geen MCP-URL's waarin een sleutel staat.
- Bewijs: Een aanvraag met een geldig token in de queryreeks en zonder header geeft 401; `grep -rn "query.*token\|searchParams.*token" <servercode>` vindt geen leespad voor tokens uit de URL. Afgevinkt met de curl-uitvoer en de grep. Zie WEB-55, API-16 en AUTH-55.
- Norm: MCP-specificatie 2026-07-28, basic/authorization, Token Requirements ("Access tokens MUST NOT be included in the URI query string"); ASVS 5.0.0 V14.2.1 (L1).
- Zie ook: AUTH-53, AUTH-54, AI-37, GIT-35, AUTH-55, WP-81

### AI-36 Bouw je OAuth voor MCP, volg dan het profiel van de specificatie volledig
hoog · hard · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Als een MCP-server OAuth ondersteunt: publiceer Protected Resource Metadata (RFC 9728), geef bij 401 een `WWW-Authenticate`-header met `resource_metadata`, laat de autorisatieserver PKCE met `S256` eisen en `code_challenge_methods_supported` publiceren, vergelijk redirect-URI's exact, geef kortlevende access tokens uit, roteer refresh tokens voor publieke clients, en stuur de `iss`-parameter mee in het autorisatieantwoord.
- Bewijs: (1) `curl https://<host>/.well-known/oauth-protected-resource` geeft een document met `authorization_servers`. (2) De metadata van de autorisatieserver bevat `code_challenge_methods_supported` met `S256` en `authorization_response_iss_parameter_supported: true`. (3) Een autorisatieaanvraag zonder `code_challenge` wordt geweigerd; een redirect-URI die één teken afwijkt wordt geweigerd. Afgevinkt met de drie uitvoeren. De algemene OAuth-regels staan in AUTH-44 tot en met AUTH-52; gebruik een bestaande, onderhouden autorisatieserver en bouw er geen zelf, tenzij dat een onderbouwd besluit is.
- Norm: MCP-specificatie 2026-07-28, basic/authorization (Overview punten 1, 4 en 5; Authorization Response Validation) en security-considerations (Token Theft, Authorization Code Protection, Open Redirection); RFC 9728, RFC 8414, RFC 9207, RFC 8707; ASVS 5.0.0 V10.4.1 (L1) en V10.1.2 (L2).
- Zie ook: AUTH-49, AI-33, AI-34, AI-32

### AI-37 Statische MCP-tokens: als hash opgeslagen, per tenant, met scope, vervaldatum en intrekking
hoog · hard · mcp | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Als een MCP-server met eigen API-tokens werkt in plaats van OAuth: genereer ze volgens AUTH-53 (CSPRNG, minimaal 128 bits, standaard 256), toon ze één keer, sla alleen een hash op, koppel elk token aan één tenant en één gebruiker, geef het een scope en een vervaldatum, maak het direct intrekbaar, en leg de afwijking van het OAuth-profiel vast met de reden.
- Bewijs: (1) In de database staat alleen de hash (`\d api_tokens` toont geen kolom met het token zelf). (2) Een ingetrokken token geeft direct 401. (3) Het token heeft een scope- en vervalveld, en een test met een verlopen token geeft 401. Of die er zijn, is niet verder uitgezocht en hoort in de audit. Zie AUTH-53 en AUTH-54.
- Norm: MCP-specificatie 2026-07-28, basic/authorization, Protocol Requirements (autorisatie optioneel; HTTP "SHOULD conform"); MCP Security Best Practices, Scope Minimization; ASVS 5.0.0 V13.3.4 (L3, rotatie en verval van geheimen).
- Zie ook: AUTH-53, AUTH-54, GIT-35, AUTH-55, AI-35, WP-81

### AI-38 Valideer de Origin-header op elk HTTP-eindpunt van een MCP-server
hoog · hard · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer op elke binnenkomende aanvraag de `Origin`-header tegen een allowlist en antwoord met 403 als hij aanwezig en niet toegestaan is; weiger een aanvraag zonder `Origin` niet om die reden, en controleer daarnaast de `Host`-header tegen de verwachte hostnamen.
- Bewijs: `curl -s -o /dev/null -w '%{http_code}' -X POST https://<host>/mcp -H 'Origin: https://evil.example' -H 'Authorization: Bearer <geldig>' -H 'Content-Type: application/json' -d '{}'` geeft 403; dezelfde aanvraag zonder `Origin` wordt normaal verwerkt. Afgevinkt met beide uitvoeren. Zie WEB-33, WEB-34 en WEB-42.
- Norm: MCP-specificatie 2026-07-28, basic/transports/streamable-http, Security Warning punt 1 ("Servers MUST validate the Origin header on all incoming connections"; ongeldige Origin geeft 403); OWASP MCP Security Cheat Sheet, sectie 6.

### AI-39 Een lokale MCP-server gebruikt stdio, of luistert alleen op 127.0.0.1 met authenticatie
hoog · hard · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een MCP-server die alleen voor de eigen machine is bedoeld via stdio praten; als HTTP nodig is, bind dan op `127.0.0.1` (niet op `0.0.0.0`), eis een token, zet de rebinding-bescherming van de SDK aan, en gebruik een SDK-versie waarin die bescherming bestaat.
- Bewijs: `ss -tlnp | grep <poort>` toont `127.0.0.1:<poort>` (of een unix-socket), of er staat een genoteerde reden waarom een ander adres nodig is plus de firewallregel; een aanvraag zonder token geeft 401. De SDK-versie in het lockfile is minimaal 1.24.0 (TypeScript) of 1.23.0 (Python). Afgevinkt met de drie uitvoeren.
- Norm: MCP-specificatie 2026-07-28, streamable-http, Security Warning punt 2 ("servers SHOULD bind only to localhost (127.0.0.1) rather than all network interfaces (0.0.0.0)"); MCP Security Best Practices, Local MCP Server Compromise ("Use the stdio transport to limit access to just the MCP client"; bij HTTP een token of een unix-socket).
- Zie ook: INFRA-13, DB-58, INFRA-14, INFRA-12, AI-75

### AI-40 Een MCP-proxy met één vaste client-id vraagt per client toestemming
hoog · hard · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Als je MCP-server als OAuth-proxy voor een dienst van derden werkt met één vaste client-id: toon een eigen toestemmingspagina per MCP-client voordat je doorstuurt naar de derde, bewaar die toestemming per gebruiker en client-id, vergelijk redirect-URI's exact, en zet de `state`-cookie pas nadat de gebruiker heeft goedgekeurd.
- Bewijs: Alleen van toepassing als de server deze proxyrol heeft; noteer anders "niet van toepassing". Als wel: een e2e-test met een tweede, nieuw geregistreerde client laat zien dat de toestemmingspagina van de MCP-server verschijnt voordat er wordt doorgestuurd; de pagina noemt de clientnaam, de scopes en de redirect-URI; de cookie heeft `__Host-`, `Secure`, `HttpOnly` en `SameSite=Lax`; de pagina stuurt `frame-ancestors 'none'`. Afgevinkt met de testuitvoer en de headers.
- Norm: MCP-specificatie 2026-07-28, security-considerations, Confused Deputy Problem ("MCP proxy servers using static client IDs MUST obtain user consent for each dynamically registered client"); MCP Security Best Practices, Confused Deputy Problem (Required Protections).

### AI-41 Een statushandle is een naam, geen sleutel
hoog · hard · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak handles voor toestand over meerdere aanroepen (een winkelmand-id, een workflow-id, een upload-id) willekeurig en ondoorzichtig, bind ze op de server aan de geverifieerde gebruiker, geef ze een beperkte levensduur, en controleer bij elke aanroep dat de handle van de aanroeper is.
- Bewijs: Een test maakt als gebruiker A een handle en gebruikt hem als gebruiker B: weigering. De handle is minimaal 128 bits willekeurig (zie API-61) en de opslagsleutel bevat het gebruikers-id uit het token. Afgevinkt met de testuitvoer. Zie AUTH-63 en AUTH-68.
- Norm: MCP Security Best Practices, State Handle Hijacking ("MCP servers MUST NOT treat possession of a state handle as authentication"); MCP-specificatie 2026-07-28, server/tools (ontwerp van handles: autorisatie, ondoorzichtigheid, levensduur); ASVS 5.0.0 V8.2.2 (L1).

### AI-42 Deel geen server- of transportinstantie tussen clients
hoog · hard · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak in een stateloze HTTP-server per aanvraag een eigen server- en transportobject (of gebruik een SDK-versie die hergebruik veilig maakt), en bewaar geen gegevens van een aanvraag in een variabele op moduleniveau.
- Bewijs: `npm ls @modelcontextprotocol/sdk` toont 1.26.0 of hoger (de laatste versie op 04-10-2026 is 1.32.0), en een test stuurt twintig gelijktijdige aanvragen met twee verschillende tokens en controleert dat elk antwoord alleen gegevens van de eigen tenant bevat. Afgevinkt met de versie en de testuitvoer.
- Norm: ASVS 5.0.0 V8.4.1 (L2); OWASP LLM Top 10 2026 LLM02 Sensitive Information Disclosure; MCP-specificatie 2026-07-28, changelog punt 1 (lijsten mogen niet per verbinding verschillen, toestand via expliciete handles).

### AI-43 Toolnamen en toolbeschrijvingen zijn publiek, eerlijk en zonder verborgen sturing
middel · richtlijn · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf een toolbeschrijving die precies zegt wat de tool doet en welke gevolgen hij heeft, zet er geen geheimen, interne paden of instructies over andere tools of andere servers in, houd namen binnen de aanbevolen tekens (letters, cijfers, `_`, `-`, `.`, 1 tot 128 tekens) en uniek binnen de server, en geef de toollijst in een vaste volgorde terug.
- Bewijs: Lees de uitvoer van `tools/list` (bijvoorbeeld met de MCP Inspector, versie 0.14.1 of hoger) en controleer: geen geheimen, geen zinnen die naar andere servers of tools verwijzen als opdracht, namen binnen het patroon, en twee keer achter elkaar dezelfde volgorde. Afgevinkt met de opgeslagen lijst.
- Norm: MCP-specificatie 2026-07-28, server/tools (Tool Names; "Servers SHOULD return tools in a deterministic order"); OWASP MCP Security Cheat Sheet, secties 2 en 8.

### AI-44 Een toolresultaat is gelabelde, minimale en opgeschoonde data
hoog · hard · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef in een toolresultaat alleen de velden terug die de taak nodig heeft, als gestructureerde data met een aanduiding van soort en herkomst, zonder ruwe HTML, zonder onzichtbare tekens (AI-07), met een maximale lengte, en zet er geen eigen instructies voor het model tussen.
- Bewijs: Per tool die inhoud van buiten teruggeeft (mail, notities, webpagina's, documenten): het resultaat is een JSON-object met een bronveld, de tekst is begrensd, en een test met een mail vol HTML, een tagteken-injectie en 200 kB tekst geeft een resultaat zonder tags, zonder onzichtbare tekens en binnen de limiet. Afgevinkt met de testuitvoer.
- Norm: MCP-specificatie 2026-07-28, server/tools, Security Considerations ("Servers MUST: Sanitize tool outputs"); OWASP MCP Security Cheat Sheet, sectie 12; ASVS 5.0.0 V14.2.6 (L3, minimaal benodigde gevoelige gegevens teruggeven).

### AI-45 Begrens tool-aanroepen per token en per tenant
hoog · hard · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op het MCP-eindpunt een limiet per token en per tenant op het aantal aanroepen per minuut en per dag, met strengere limieten voor tools die iets versturen, iets kosten of veel gegevens teruggeven, en antwoord bij overschrijding met een fout en zonder gedeeltelijke uitvoering.
- Bewijs: Een lus van N+1 aanroepen met één token geeft bij de laatste een limietfout (HTTP 429 of een JSON-RPC-fout); de limieten per toolklasse staan in de configuratie. Afgevinkt met de lusuitvoer en de waarden. Zie API-20, API-22 en WEB-66.
- Norm: MCP-specificatie 2026-07-28, server/tools, Security Considerations ("Servers MUST: Rate limit tool invocations"); ASVS 5.0.0 V2.4.1 (L2); OWASP LLM Top 10 2026 LLM03 maatregel 9.
- Zie ook: API-20, WEB-66, INFRA-46, API-22, AUTH-10, WP-57, AI-74

### AI-46 Paden en URI's in tools en resources blijven binnen de basismap, ook na het volgen van symlinks
hoog · hard · mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Los elk pad uit een toolargument of resource-URI volledig op (inclusief symlinks) en vergelijk het daarna met de opgeloste basismap op een padgrens; vergelijk nooit op een tekstueel voorvoegsel en vertrouw nooit op een basismap die alleen bij het starten is ingesteld.
- Bewijs: Een test met vier invoeren: `../x`, een absoluut pad buiten de map, een zustermap met hetzelfde voorvoegsel, en een symlink in de map die naar buiten wijst; alle vier geweigerd. Afgevinkt met de testuitvoer. Zie API-54 en WEB-45.
- Norm: MCP-specificatie 2026-07-28, server/resources, Security Considerations ("Servers MUST validate all resource URIs"; "Servers MUST sanitize file paths to prevent directory traversal attacks"); ASVS 5.0.0 V5.3.2 (L1).
- Zie ook: API-54, WP-25, API-76, WEB-45, WP-29, INV-41, INV-34, SCR-15

### AI-47 Een tool start nooit een shell met toolargumenten
kritiek · hard · mcp | app · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: AGENTIC
- Regel: Roep in een tool externe programma's alleen aan zonder shell en met een argumentenlijst, zet `--` voor argumenten die van het model komen, weiger waarden die met `-` beginnen waar een naam of verwijzing wordt verwacht, en gebruik voor HTTP een bibliotheek in plaats van `curl` via de shell.
- Bewijs: `grep -rnE "exec\(|execSync\(|shell: *true|child_process" <servercode>` geeft alleen `execFile` of `spawn` zonder shell met een vaste programmanaam; een test met de argumenten `; id`, `$(id)` en `--output=/tmp/x` laat zien dat er geen commando wordt uitgevoerd en geen bestand ontstaat. Afgevinkt met grep en testuitvoer. Zie API-53.
- Norm: ASVS 5.0.0 V1.2.5 (L1); OWASP Agentic 2026 ASI05; OWASP MCP Security Cheat Sheet, sectie 5 ("Never pass raw shell commands or unsanitized file paths").
- Zie ook: API-53, SCR-24, SCR-07, SCR-10

### AI-48 Een tool die een URL ophaalt, valt onder de SSRF-regels
hoog · hard · mcp | app | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een tool alleen URL's ophalen na de controles uit WEB-40 en WEB-41 (alleen `https`, het opgeloste adres niet privé, niet loopback, niet link-local, geen automatische redirects, limiet op grootte en tijd), en gebruik waar het kan een allowlist van hosts in plaats van een vrije URL.
- Bewijs: De unit-tests uit WEB-40 (zes adressen, waaronder `127.0.0.1`, `169.254.169.254`, een privé-adres, een redirect naar intern en een IPv6-loopback) draaien op elke tool en elke functie die een URL uit modeluitvoer, een mail of een toolargument ophaalt. Afgevinkt met de testuitvoer.
- Norm: MCP Security Best Practices, Server-Side Request Forgery; ASVS 5.0.0 V1.3.6 (L2) en V13.2.4 (L2); OWASP MCP Security Cheat Sheet, sectie 5.
- Zie ook: WEB-40, WEB-41, API-48, API-47, WP-28, INFRA-18, INV-59, INV-61, MSG-27, MSG-46

### AI-49 Vraag nooit een wachtwoord, sleutel of betaalgegeven via het model
hoog · hard · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Vraag geheimen en betaalgegevens nooit op via een toolargument of een formulier-elicitation; stuur de gebruiker daarvoor naar een eigen HTTPS-pagina (URL-modus), zet in die URL geen persoonsgegevens en geen vooraf ingelogde toegang, bind de aanvraag aan de geverifieerde gebruiker, en geef het verkregen geheim nooit terug aan de client.
- Bewijs: `grep -niE "password|wachtwoord|secret|api.?key|token|iban|kaart" <toolschema's>` vindt geen invoerveld voor een geheim; koppelingen die een geheim nodig hebben, lopen via de app of een URL-elicitation. Afgevinkt met de grep en, indien van toepassing, een e2e-test van de URL-stroom.
- Norm: MCP-specificatie 2026-07-28, client/elicitation ("Servers MUST NOT use form mode elicitation to request sensitive information such as passwords, API keys, access tokens, or payment credentials"; URL's zonder gevoelige gegevens en niet vooraf geauthenticeerd; "The MCP server MUST NOT transmit credentials obtained through URL mode elicitation to the MCP client").

### AI-50 Vul tool-annotaties eerlijk in en bouw er geen beveiliging op
laag · richtlijn · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke tool de annotaties `readOnlyHint`, `destructiveHint`, `idempotentHint` en `openWorldHint` die bij zijn werkelijke gedrag passen, en behandel annotaties aan de serverkant en aan de clientkant als hulp voor de gebruiker en nooit als controle.
- Bewijs: Een tabel van tools met hun annotaties naast het werkelijke gedrag (leest, schrijft, verwijdert, praat met buiten); geen muterende tool heeft `readOnlyHint: true`. Afgevinkt met de tabel.
- Norm: MCP-specificatie 2026-07-28, server/tools ("clients MUST consider tool annotations to be untrusted unless they come from trusted servers") en het schema (de vier annotatienamen komen in `schema.mdx` voor).
- Zie ook: BIZ-43

### AI-51 Minimale scopes, stapsgewijs verhoogd, zonder jokers
middel · richtlijn · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Publiceer bij OAuth in `scopes_supported` alleen de kleinste set voor basisgebruik, vraag hogere scopes pas op het moment dat een geprivilegieerde tool wordt aangeroepen (403 met `insufficient_scope` en de benodigde scope), gebruik geen scope als `*`, `all` of `admin` voor gewoon gebruik, en controleer rechten in de serverlogica ook als de scope klopt.
- Bewijs: Het Protected Resource Metadata-document bevat alleen de basisscopes; een aanroep van een schrijftool met een basistoken geeft 403 met `WWW-Authenticate: Bearer error="insufficient_scope", scope="..."`. Afgevinkt met de curl-uitvoer. Voor statische tokens geldt AI-29 en AI-37.
- Norm: MCP Security Best Practices, Scope Minimization; MCP-specificatie 2026-07-28, basic/authorization (Scope Selection Strategy en Scope Challenge Handling); ASVS 5.0.0 V10.3.2 (L2).

### AI-52 Log elke tool-aanroep met wie, wat en uitkomst, zonder geheimen
hoog · hard · mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf voor elke tool-aanroep een auditregel met tijdstip, tenant, gebruiker, token-id, toolnaam, het doelobject, de uitkomst en een correlatie-id; log parameters zonder geheimen en zonder volledige persoonsgegevens, en maak het log onbereikbaar voor de tools zelf.
- Bewijs: Na één aanroep van elke toolklasse staat er per aanroep een auditregel met de genoemde velden (query op de audittabel); een aanroep met een nepgeheim in een argument laat in het log een gemaskeerde waarde zien; er is geen tool die de audittabel kan wijzigen. Afgevinkt met de query-uitvoer. Zie AUTH-84 en API-66.
- Norm: MCP-specificatie 2026-07-28, server/tools (clients "SHOULD: Log tool usage for audit purposes"); OWASP MCP Security Cheat Sheet, sectie 10; OWASP LLM Top 10 2026 LLM03 maatregel 8; ASVS 5.0.0 V16.2.1 (L2), V16.2.5 (L2) en V16.3.2 (L2).
- Zie ook: ARCH-62, API-66, DB-88, INFRA-88, AUTH-14, AI-67, GIT-39, ARCH-64, AUTH-84, ARCH-65, INFRA-89, PRIV-54, DB-91

### AI-53 Elke tool heeft een isolatietest met twee tenants
kritiek · hard · mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf voor elke tool van een multi-tenant MCP-server een test die met het token van tenant A een object van tenant B leest, wijzigt en zoekt, en laat de uitrol falen als één ervan iets van B teruggeeft of wijzigt.
- Bewijs: De testsuite bevat per tool minimaal één kruistest; de CI-uitvoer toont het aantal tools en het aantal kruistests, en die zijn gelijk. Afgevinkt met de CI-uitvoer. Zie AUTH-66, AUTH-77 en DB-22. Bij het CRM is het model database-per-tenant (eigen ervaring); de test controleert daar dat een token nooit de pool van een andere tenant kan kiezen.
- Norm: ASVS 5.0.0 V8.4.1 (L2) en V8.2.2 (L1); OWASP LLM Top 10 2026 LLM02; OWASP API Security Top 10 2023 API1 (BOLA, uitgewerkt in AUTH en API).
- Zie ook: DB-22, AUTH-77, AUTH-66, ARCH-40

### AI-54 Blijf op een ondersteunde protocolrevisie en bouw geen afgeraden onderdelen
middel · richtlijn · mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw nieuwe servers op de huidige revisie van de specificatie (2026-07-28) met een actuele officiële SDK, gebruik Streamable HTTP of stdio, en bouw niets nieuws op HTTP+SSE, dynamische clientregistratie, Sampling, Roots of protocol-logging.
- Bewijs: Het lockfile toont de SDK-versie; de server antwoordt op `server/discover` met de ondersteunde revisies; `grep -rn "SSEServerTransport\|sampling/createMessage\|roots/list" <servercode>` is leeg of verklaard. Afgevinkt met de drie uitvoeren.
- Norm: MCP-specificatie 2026-07-28, changelog (Major changes 1 tot en met 3; Deprecated 1, 2 en 4) en het register van afgeraden onderdelen; ASVS 5.0.0 V15.2.1 (L1).
- Zie ook: GIT-93, API-72, WP-52, DB-93, INFRA-22, INFRA-42, SCR-33
