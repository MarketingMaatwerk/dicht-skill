# AUTH G: OAuth 2.0 en OpenID Connect

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/auth.md` (regelnummer in `regel-index.tsv`).

### AUTH-44 Alleen de authorization code flow met PKCE (S256)
kritiek · hard · api | app | mcp | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Gebruik voor elke OAuth- of OIDC-koppeling de authorization code flow met PKCE en `code_challenge_method=S256` en een `code_verifier` met 256 bits entropie; gebruik nooit de implicit flow of de password grant, en weiger als autorisatieserver `plain`.
- Bewijs: Codecheck of netwerklog van een inlogronde: de autorisatie-URL bevat `response_type=code`, `code_challenge` en `code_challenge_method=S256`; nergens `response_type=token` of `grant_type=password`. Als autorisatieserver: test dat een verzoek zonder `code_challenge` en een tokenverzoek zonder `code_verifier` worden geweigerd. Afgevinkt als dit klopt.
- Norm: RFC 9700 §2.1.1 (publieke clients MUST PKCE; servers MUST PKCE ondersteunen), §2.1.2 (implicit SHOULD NOT), §2.4 (password grant MUST NOT); RFC 7636 §4.1, §4.2, §7.1; ASVS 5.0.0 V10.4.4 (L1), V10.4.6 (L2), V10.2.1 (L2).

### AUTH-45 Redirect-URI's exact vergelijken
kritiek · hard · api | app | mcp | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Registreer per client volledige redirect-URI's en vergelijk ze als exacte string (alleen de poort van `localhost` mag afwijken bij native clients); sta geen wildcards, geen deelpaden en geen `http` toe, en heb zelf geen open redirect op het geregistreerde domein.
- Bewijs: Als autorisatieserver: tests met een extra pad, een extra subdomein, een andere schrijfwijze en een extra queryparameter geven elk een fout zonder redirect. Als client: in de console van de aanbieder staan alleen volledige productie- en test-URI's. Afgevinkt als de tests groen zijn of een schermafdruk van de registratie in het dossier zit.
- Norm: RFC 9700 §2.1 (MUST exact string matching; MUST NOT open redirectors), §2.6 (geen `http` behalve loopback bij native clients); ASVS 5.0.0 V10.4.1 (L1).
- Zie ook: WEB-39, WP-27

### AUTH-46 Bind `state`, PKCE en `nonce` aan de browsersessie die de flow startte
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Genereer per autorisatieverzoek onraadbare waarden voor `state`, `code_verifier` en (bij OIDC) `nonce`, bewaar ze server-side bij de sessie van de browser die de flow startte, controleer ze in de callback en gooi ze daarna weg; controleer bij meerdere aanbieders ook de `iss` van het antwoord.
- Bewijs: Tests: callback zonder `state`, met een `state` uit een andere sessie en met een hergebruikte `state` geven elk een fout; bij OIDC faalt een ID-token met een andere `nonce`. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V10.1.2, V10.2.1, V10.2.2, V10.5.1 (L2); RFC 9700 §2.1 (CSRF MUST voorkomen; mix-up via `iss`, RFC 9207).

### AUTH-47 Koppel externe identiteiten op uitgever plus `sub`, nooit op e-mail
kritiek · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Sla bij "inloggen met Google of Microsoft" de combinatie van uitgever (`iss`, bij Microsoft ook `tid`) en `sub` (of `oid`) op als sleutel voor het account; koppel nooit automatisch aan een bestaand account op basis van de claim `email`, en neem geen autorisatiebesluit op `email`, `preferred_username` of `upn`.
- Bewijs: `\d external_identities` toont een unieke index op `(issuer, subject)`. Test: een externe login met een bekend e-mailadres maar een onbekende `(iss, sub)` maakt geen sessie voor het bestaande account zonder dat de gebruiker eerst op de bestaande manier inlogt. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V6.8.1, V10.3.3, V10.5.2 (L2).
- Zie ook: INV-64, MSG-18, WEB-69

### AUTH-48 Valideer het ID-token volledig
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer van elk ID-token de handtekening (AUTH-39, AUTH-40), dat `iss` exact de ingestelde uitgever is, dat `aud` gelijk is aan je eigen `client_id`, de `nonce` (AUTH-46) en `exp`; gebruik een onderhouden OIDC-bibliotheek en zet de uitgever in configuratie.
- Bewijs: Tests met de bibliotheek: ID-token met een andere `aud`, een andere `iss` en zonder handtekening worden geweigerd. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V6.8.2, V10.5.1, V10.5.3, V10.5.4 (L2).

### AUTH-49 Als resource server: alleen tokens voor jou, en scopes afdwingen
kritiek · hard · api | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Accepteer als API of MCP-server alleen toegangstokens waarvan het publiek (`aud` of de resource-indicator) jouw dienst is, dwing `scope` en `sub` af bij elk besluit, stuur een ontvangen token nooit door naar een andere dienst, en neem tokens alleen aan in de `Authorization`-header.
- Bewijs: Tests: token met een andere `aud` geeft 401; token zonder de vereiste scope geeft 403; token in de querystring wordt genegeerd. Codecheck: uitgaande aanroepen gebruiken een eigen token, niet `req.headers.authorization`. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V10.3.1, V10.3.2 (L2), V14.2.1 (L1); RFC 9700 §2.3; MCP-specificatie 2026-07-28, Authorization ("MCP servers MUST validate that access tokens were issued specifically for them"; "MUST NOT accept or transit any other tokens"; tokens "MUST NOT be included in the URI query string").
- Zie ook: AI-33, AI-34, AI-32, AI-36

### AUTH-50 Refresh tokens: roteren met hergebruikdetectie, eindig en intrekbaar
hoog · hard · api | app | mcp | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Vervang een refresh token bij elk gebruik door een nieuw, trek bij aanbieding van een al gebruikt token de hele reeks in, geef elke reeks een absolute einddatum, sla refresh tokens alleen gehasht op, en laat gebruiker en beheerder ze kunnen intrekken.
- Bewijs: Tests: token R1 inwisselen geeft R2; R1 opnieuw aanbieden geeft een fout en maakt ook R2 ongeldig; na de absolute einddatum faalt elke verversing. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V10.4.5 (L1; rotatie toegestaan op L1 en L2), V10.4.8, V10.4.9 (L2); RFC 9700 §2.2.2 (publieke clients MUST sender-constrained of rotatie), §4.14.

### AUTH-51 Houd tokens en clientgeheimen bij de backend en vraag minimale scopes
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat bij een browserapplicatie de backend de tokens bewaren en de browser alleen een sessiecookie krijgen (backend-for-frontend), zet een `client_secret` nooit in frontendcode of een app-bundel, en vraag alleen de scopes die de functie nodig heeft.
- Bewijs: `grep -rn "client_secret\|CLIENT_SECRET" frontend/ dist/` levert niets op. De autorisatie-URL bevat alleen de gedocumenteerde scopes (lijst in `docs/auth.md`). Afgevinkt als beide kloppen.
- Norm: ASVS 5.0.0 V10.1.1 (L2), V10.4.11 (L2), V10.2.3 (L3).

### AUTH-52 Als je zelf autorisatieserver bent: codes eenmalig en kort, toestemming expliciet
hoog · hard · api | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een autorisatiecode één keer en maximaal 10 minuten gelden (1 minuut voor kritieke delen), trek bij hergebruik van een code alle daarmee uitgegeven tokens in, sta per client alleen de benodigde grants toe, vraag de gebruiker per client om toestemming met een duidelijke omschrijving, en laat hem die toestemming kunnen inzien en intrekken.
- Bewijs: Tests: code tweemaal inwisselen faalt de tweede keer en maakt het eerste token ongeldig; code na 10 minuten faalt; een onbekende client krijgt een toestemmingsscherm. Gebruik bij voorkeur een bestaande, onderhouden autorisatieserver in plaats van eigen bouw; leg die keuze vast. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V10.4.2, V10.4.3, V10.4.4 (L1), V10.4.7, V10.7.1, V10.7.2, V10.7.3 (L2); MCP-specificatie 2026-07-28, Security Considerations, Confused Deputy Problem ("MCP proxy servers using static client IDs MUST obtain user consent for each dynamically registered client"; ongewijzigd ten opzichte van 2025-06-18).
