# Checklist mcp

740 regels: 628 hard, 112 richtlijn. Gemaakt door `tools/bouw.py` uit het veld "Geldt voor"; niet met de hand wijzigen.
Elk punt: ID (ernst) titel, en wat telt als afgevinkt. Het volledige bewijs staat in de referentie van de sub-skill. Een punt dat in dit project niet speelt krijgt in het bewijsbestand `nvt` met een reden.

## Ontwerp: hard (65)

### dicht-api
- [ ] AUTH-64 (kritiek) Bescherm elke functie, ook via een andere methode of een ander pad. Afgevinkt als de matrix alle routes dekt.
- [ ] AUTH-72 (kritiek) Haal de tenant uit de geverifieerde sessie, nooit uit de aanvraag. Afgevinkt als de test in de matrix van AUTH-66 zit.
- [ ] API-25 (hoog) Houd een inventaris bij en zet niets in productie wat er niet hoort. `app.printRoutes()` of de OpenAPI-uitvoer in CI wordt vergeleken met de vastgelegde lijst;
- [ ] API-51 (middel) Leg vast met welke externe diensten de app praat. De lijst staat in de projectdocumentatie en komt overeen met `grep -rnoE "https://[a-z0-9.-]+" src | sort -u`.
- [ ] BIZ-04 (hoog) Leg "hoogstens één tegelijk actief" vast met een partiële unieke index. `\d+ <tabel>` toont de partiële unieke index voor elke regel van deze vorm die in de documentatie staat.
- [ ] BIZ-06 (hoog) Voorkom overlappende periodes en dubbele boekingen met een exclusion constraint. `\d+ <tabel>` toont de exclusion constraint.
- [ ] BIZ-46 (hoog) Wijs per feit één bron aan en sla elk extern id uniek op. De tabel staat in het architectuurdocument.

### dicht-database
- [ ] DB-11 (hoog) Kies het tenantmodel bewust en leg het vast. Afgevinkt als het document bestaat en de test ernaar verwijst.
- [ ] DB-83 (hoog) Elke tabel met persoonsgegevens heeft een bewaartermijn en een opruimjob. Afgevinkt als alle drie kloppen.
- [ ] DB-87 (middel) Classificeer gegevens per kolom. Afgevinkt als het script nul ontbrekende kolommen meldt.

### dicht-infra
- [ ] INFRA-73 (hoog) Houd per geheim één bron en een lijst van gebruikers bij. Afgevinkt met de lijst en de vergelijking.

### dicht-git
- [ ] GIT-05 (middel) Commit na elke gevalideerde stap, één onderwerp per commit. Afgevinkt met beide uitvoeren.
- [ ] GIT-14 (kritiek) Beveilig het GitHub-account met TOTP plus een passkey, zonder sms. Afgevinkt met een notitie met datum.
- [ ] GIT-15 (hoog) Gebruik tokens met een einddatum en de kleinste reikwijdte. Afgevinkt met de lijst.
- [ ] GIT-18 (middel) Onderteken commits en tags. Afgevinkt met de uitvoer.
- [ ] GIT-22 (hoog) Maak een repo alleen publiek na een scan van de hele geschiedenis. Afgevinkt met beide uitvoeren.
- [ ] GIT-23 (hoog) Stel vast wat het GitHub-plan toelaat voordat je erop rekent. Afgevinkt met die tabel.
- [ ] GIT-24 (hoog) Bescherm de standaardbranch: met een ruleset waar het plan die biedt, anders lokaal. Afgevinkt met de uitvoer.
- [ ] GIT-26 (middel) Bescherm tags en maak releases onveranderlijk. Afgevinkt met de drie uitvoeren.
- [ ] GIT-27 (hoog) Zet de Actions-instellingen van de repo dicht. Afgevinkt met de uitvoer.
- [ ] GIT-28 (hoog) Zet Dependabot-meldingen en beveiligingsupdates aan op elke repo. Afgevinkt met de uitvoer.
- [ ] GIT-57 (hoog) De gate bevat lint, typecheck, tests en de scans van dit domein. Afgevinkt met script en uitvoer.
- [ ] GIT-77 (hoog) Leg hersteltermijnen vast en houd je eraan. Afgevinkt met document en uitvoer.
- [ ] GIT-104 (middel) Controleer de licentie van elke afhankelijkheid. Afgevinkt met de uitvoer.
- [ ] GIT-106 (hoog) Heb een draaiboek voor een gekaapt pakket. Afgevinkt met draaiboek en de uitvoer van de oefening.

### dicht-ai-mcp
- [ ] AI-01 (kritiek) Ontwerp op de aanname dat de injectie slaagt. [bron niet gelezen: AGENTIC] Afgevinkt als de tabel er is en de regels AI-02, AI-06 en AI-24 erop zijn toegepast.
- [ ] AI-17 (hoog) Ontvanger, afzender en bijlagen van een bericht komen uit code, niet uit het model. [bron niet gelezen: AGENTIC] Afgevinkt met de testuitvoer.
- [ ] AI-66 (hoog) Leg per modelleverancier vast onder welke voorwaarden de gegevens worden verwerkt. Afgevinkt met de tabel.

### dicht-privacy
- [ ] PRIV-01 (hoog) Leg per project vast wie verantwoordelijke en wie verwerker is. Afgevinkt als elke tabel met persoonsgegevens uit de classificatie (DB-87) in precies één rij valt.
- [ ] PRIV-02 (hoog) Het verwerkingsregister bevat per activiteit de wettelijke velden. Afgevinkt met de uitvoer.
- [ ] PRIV-03 (hoog) Werk het register bij in dezelfde wijziging als de nieuwe gegevensstroom. Afgevinkt met de vergelijking.
- [ ] PRIV-07 (hoog) Geen verwerking zonder vastgelegde grondslag. Afgevinkt met de scriptuitvoer.
- [ ] PRIV-09 (middel) De standaardinstelling is de zuinigste. Afgevinkt met de testuitvoer.
- [ ] PRIV-11 (hoog) Gebruik gegevens niet voor een ander doel dan waarvoor ze zijn verzameld. Afgevinkt met de verwijzing.
- [ ] PRIV-12 (hoog) Houd bijzondere gegevens buiten systemen die er niet voor gebouwd zijn. Afgevinkt met de telling en de classificatie.
- [ ] PRIV-13 (middel) Laat geen besluit met gevolgen voor een persoon volledig aan een automaat. Afgevinkt met lijst en test.
- [ ] PRIV-21 (hoog) Elke gegevenssoort heeft een termijn met een reden, in het register en in de code. Afgevinkt met de vergelijking en de logregels.
- [ ] PRIV-23 (middel) Geef logs met persoonsgegevens een termijn die het doel dekt en niet meer. Afgevinkt met overzicht en configuratie.
- [ ] PRIV-37 (hoog) Doe bij elk nieuw project een DPIA-toets van vijf minuten en leg de uitkomst vast. Afgevinkt met de notitie.
- [ ] PRIV-59 (hoog) Leg per project het ASVS-niveau vast, per onderdeel. Afgevinkt als het bestand bestaat vóór de eerste regel code van een nieuw project en bij de oplevering van een bestaand project.
- [ ] PRIV-60 (middel) Maak een toepasbaarheidstabel en verklaar elk hoofdstuk dat vervalt. Afgevinkt met tabel en grep-uitvoer.
- [ ] PRIV-61 (hoog) Deze L3-eisen zijn hard voor betaling, login en tenant-isolatie. Afgevinkt als alle elf een verwijzing en een bewijs hebben.
- [ ] PRIV-62 (middel) De documentatie-eisen van ASVS zijn zelf het bewijs: schrijf ze. Afgevinkt als ze bestaan en de autorisatietests (AUTH) naar de matrix verwijzen.
- [ ] PRIV-70 (hoog) Bepaal per leverbaar stuk software of het een product met digitale elementen is. Afgevinkt als de lijst bestaat.
- [ ] PRIV-74 (middel) Leg de ondersteuningsperiode vast en lever beveiligingsupdates kosteloos en apart. Afgevinkt met de drie.
- [ ] PRIV-76 (hoog) Toets voor het eigen bedrijf en voor elke klant of de Cyberbeveiligingswet geldt. [bron niet gelezen: CBW] Afgevinkt als de notitie voor het eigen bedrijf bestaat en bij nieuwe klanten in de intake staat.
- [ ] PRIV-80 (middel) Stel vast of je aanbieder of gebruiksverantwoordelijke bent. [bron niet gelezen: AI-VO] Afgevinkt met de tabel.

### dicht-architectuur
- [ ] ARCH-01 (middel) Bouw een modulaire monoliet; een extra proces of dienst vraagt een vastgelegd besluit. [eigen bron] Afgevinkt als lijst en werkelijkheid gelijk zijn.
- [ ] ARCH-02 (middel) Geef elke module één publieke ingang en dwing de grens af in de gate. Afgevinkt met de groene en de rode uitvoer.
- [ ] ARCH-05 (hoog) Lever geen test-, voorbeeld- of ontwikkelcode mee naar productie. Afgevinkt met de drie uitvoeren.
- [ ] ARCH-06 (middel) Houd één architectuurdocument bij met vaste onderdelen. Afgevinkt als beide kloppen.
- [ ] ARCH-15 (hoog) Laat de kern doorwerken als een externe dienst uitvalt. Afgevinkt met de testuitvoer per dienst.
- [ ] ARCH-29 (middel) Leg elke architectuurbeslissing vast als ADR. Afgevinkt als die bestanden bestaan en de status klopt.
- [ ] ARCH-30 (hoog) Leg elke uitzondering op een harde regel vast, ook een overgeslagen stap. Afgevinkt als het bestand bestaat en geen uitzondering over zijn einddatum heen is.
- [ ] ARCH-31 (middel) Schrijf per dienst een runbook met de vijf handelingen en elk alarm. Afgevinkt met de vergelijking en de datum van de oefening.
- [ ] ARCH-32 (middel) Leg hersteltermijnen vast en houd een schuldregister bij. Afgevinkt met de tellingen.
- [ ] ARCH-57 (middel) Houd per applicatie een loginventaris bij. Afgevinkt als lijst en werkelijkheid gelijk zijn.
- [ ] ARCH-80 (hoog) Maak bij elk nieuw project een threat model in vier vragen. Afgevinkt als het bestand compleet is.
- [ ] ARCH-81 (middel) Herzie het threat model bij elke nieuwe ingang of grens. Afgevinkt met de datumvergelijking.
- [ ] ARCH-83 (middel) Genereer de lijst van ingangen en vergelijk hem met het document. Afgevinkt met de testuitvoer.

### dicht-scripts
Alleen als het project een script, een geplande taak of een lus bevat die in cron, een timer, een uitrol of een andere sessie draait; anders het hele blok `nvt` met die reden.
- [ ] SCR-39 (middel) Bepaal per taak wat er gebeurt met een gemiste run. Afgevinkt met de lijst en de uitvoer.

### dicht-invoer
- [ ] INV-13 (hoog) Dwing per parameter één waarde en één type af. Afgevinkt met test en grep.
- [ ] INV-43 (hoog) Tel uitgepakte bytes en entries tijdens het uitpakken en pak niet genest uit. Afgevinkt met de testuitvoer.

### dicht-berichten
- [ ] MSG-29 (middel) Identificeer een bericht met map, UIDVALIDITY en UID. Afgevinkt met het schema en de testuitvoer.
- [ ] MSG-38 (hoog) Dwing het 24-uursvenster af in code. [bron niet gelezen: META] Afgevinkt met de testuitvoer.

## Ontwerp: richtlijnen (17)

### dicht-infra
- [ ] INFRA-08 (middel) Trek toegang in met een lijst, niet uit het hoofd. Afgevinkt met de lijst en de vergelijking.
- [ ] INFRA-105 (middel) Weet wat je zelf kunt opvangen en wat alleen de aanbieder of een CDN kan. Afgevinkt met document en proef.

### dicht-git
- [ ] GIT-17 (middel) SSH-sleutels: ed25519, met wachtwoordzin, één per machine. Afgevinkt met beide.
- [ ] GIT-19 (laag) Zet vigilant mode pas aan als alles ondertekend is. Afgevinkt met een schermafbeelding of de API-uitvoer `gh api repos/<o>/<r>/commits/<sha> --jq .
- [ ] GIT-20 (middel) Geef anderen toegang via een organisatie of een deploy key, niet als collaborator. Afgevinkt met de lijst.
- [ ] GIT-21 (middel) Loop per kwartaal sessies, sleutels, tokens en apps na. Afgevinkt met de notitie.
- [ ] GIT-25 (laag) Kies één mergestrategie en zet de regels die ermee botsen niet aan. Afgevinkt met de ruleset-uitvoer.
- [ ] GIT-29 (laag) Wijs een eigenaar aan voor workflows en CODEOWNERS zelf. Afgevinkt met de drie.
- [ ] GIT-68 (laag) Leg de versies van hulpmiddelen vast en ververs ze per kwartaal. Afgevinkt met de lijst.

### dicht-privacy
- [ ] PRIV-06 (middel) Bewaar het bewijs van elke privacykeuze bij het project. Afgevinkt als het bestand bestaat en de laatste wijziging in git niet ouder is dan de laatste wijziging aan de gegevensstroom.
- [ ] PRIV-63 (middel) ASVS dekt de AVG niet: gebruik de koppeltabel. Afgevinkt als elke rij een verwijzing heeft.
- [ ] PRIV-64 (laag) Herbeoordeel het niveau bij elke wijziging van functie of gegevens. Afgevinkt met de log.

### dicht-architectuur
- [ ] ARCH-03 (laag) Laat afhankelijkheden één kant op lopen en sta geen cirkels toe. Afgevinkt met de uitvoer.
- [ ] ARCH-04 (hoog) Zet gevaarlijke functionaliteit apart en geef haar minder rechten. Afgevinkt als de lijst bestaat en elk onderdeel een inperking heeft of een genoteerde reden waarom niet.
- [ ] ARCH-13 (middel) Stel time-outs af van binnen naar buiten. Afgevinkt als elke binnenste waarde kleiner is dan de buitenste.
- [ ] ARCH-14 (middel) Herhaal op één laag. Afgevinkt met de grep en een korte toelichting per keten.
- [ ] ARCH-66 (middel) Bepaal wat er gebeurt als loggen mislukt. Afgevinkt met het verslag van de proef.

## Bouwen: hard (486)

### dicht-web
- [ ] WEB-01 (kritiek) Codeer uitvoer per context, als laatste stap. Afgevinkt als beide groen zijn.
- [ ] WEB-03 (hoog) Sta HTML van gebruikers alleen toe via een onderhouden sanitizer. Afgevinkt met versie en testuitvoer.
- [ ] WEB-04 (hoog) Laat in URL-attributen alleen veilige schema's toe. Afgevinkt met de testuitvoer.
- [ ] WEB-08 (kritiek) Bouw nooit een template uit invoer. Afgevinkt met de test.
- [ ] WEB-09 (middel) Stuur bij elke respons het juiste Content-Type met charset en nosniff. Afgevinkt met de vier uitvoeren.
- [ ] WEB-17 (hoog) Zet HSTS op alle responsen. Afgevinkt met de uitvoer en de subdomeinlijst.
- [ ] WEB-19 (middel) Zet een expliciete Referrer-Policy. Afgevinkt met beide.
- [ ] WEB-22 (laag) Verberg versies en verwijder verouderde headers. Afgevinkt met de uitvoer.
- [ ] WEB-23 (hoog) Controleer headers op elke locatie en elke statuscode (nginx-overerving). Afgevinkt met de tabel.
- [ ] WEB-25 (hoog) Geef elke sessiecookie Secure, HttpOnly, SameSite en het __Host-voorvoegsel. Afgevinkt met de header en de consoletest.
- [ ] WEB-29 (hoog) Wijzig nooit iets via GET. Afgevinkt met lijst en test.
- [ ] WEB-31 (hoog) Laat een JSON-API alleen application/json toe. Afgevinkt met test en grep.
- [ ] WEB-33 (hoog) Sta met CORS alleen een vaste lijst van origins toe. Afgevinkt met de vier uitvoeren.
- [ ] WEB-34 (hoog) Controleer de Origin bij de WebSocket-handshake. Afgevinkt met de test.
- [ ] WEB-37 (middel) Zet niet-vertrouwde inhoud in een iframe met sandbox. Afgevinkt met grep en test.
- [ ] WEB-39 (hoog) Stuur alleen door naar bestemmingen uit een allowlist. Afgevinkt met de testuitvoer.
- [ ] WEB-40 (kritiek) Haal server-side alleen toegestane adressen op (SSRF). Afgevinkt met de testuitvoer.
- [ ] WEB-41 (hoog) Volg server-side geen redirects. Afgevinkt met test en grep.
- [ ] WEB-42 (hoog) Bouw absolute URL's uit de configuratie, nooit uit de Host-header. Afgevinkt met beide.
- [ ] WEB-43 (hoog) Begrens de grootte van elke upload en elke body. Afgevinkt met de test.
- [ ] WEB-45 (hoog) Bepaal bestandsnaam en pad zelf. Afgevinkt met test en grep.
- [ ] WEB-50 (hoog) Voorkom request smuggling tussen proxy en applicatie. Afgevinkt met versies en uitvoer.
- [ ] WEB-51 (hoog) Vertrouw proxy-headers alleen van de eigen proxy. Afgevinkt met de drie uitvoeren.
- [ ] WEB-52 (hoog) Zet no-store op elke respons met persoonlijke of ingelogde inhoud. Afgevinkt met beide uitvoeren per route.
- [ ] WEB-55 (hoog) Zet geen gevoelige gegevens in de URL. Afgevinkt met grep en logsteekproef.
- [ ] WEB-56 (hoog) Serveer alles over HTTPS; laat een API niet stil doorsturen. Afgevinkt met de drie uitvoeren.
- [ ] WEB-62 (hoog) Toon een generieke foutpagina; debug uit in productie. Afgevinkt met respons en logregel.
- [ ] WEB-66 (hoog) Begrens het aantal aanvragen op elke route die iets kost of iets verstuurt. Afgevinkt met de uitvoer.

### dicht-api
- [ ] AUTH-06 (middel) Verifieer het wachtwoord ongewijzigd en werk wachtwoordmanagers niet tegen. [alleen: met login] Afgevinkt met een Playwright-test die een wachtwoord plakt.
- [ ] AUTH-09 (hoog) Geen hints, geen geheime vragen, geen standaardaccounts, geen blijvende startwachtwoorden. Afgevinkt als de lijst klopt met de afgesproken beheerders.
- [ ] AUTH-10 (kritiek) Begrens inlogpogingen per account en per bron. [alleen: met login] Afgevinkt als de test groen is en het document bestaat.
- [ ] AUTH-12 (middel) Verklap niet of een account bestaat. [alleen: met login] Afgevinkt als de test in CI staat.
- [ ] AUTH-13 (hoog) Ken en bewaak elk inlogpad. Afgevinkt als elk pad een test heeft.
- [ ] AUTH-14 (hoog) Log elke authenticatiegebeurtenis, zonder geheimen. Afgevinkt als beide kloppen.
- [ ] AUTH-25 (kritiek) Reset- en verificatietokens: willekeurig, gehasht, eenmalig, kort geldig. [alleen: met login] Afgevinkt als de drie tests groen zijn.
- [ ] AUTH-27 (kritiek) Stuur resetmails alleen naar het geverifieerde adres uit de database. [alleen: met login] Afgevinkt als de tests groen zijn.
- [ ] AUTH-28 (hoog) Na een reset: niet automatisch inloggen, sessies weg, melding. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-31 (middel) Houd tokens uit referers, logs en pagina's met scripts van derden. [alleen: met login] Afgevinkt als alle drie kloppen.
- [ ] AUTH-32 (kritiek) Sessie-id: willekeurig, ondoorzichtig, op de server gecontroleerd. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-33 (kritiek) Sessiecookie: `__Host-`, Secure, HttpOnly, SameSite, en nooit in webopslag. [alleen: met login] Afgevinkt als beide kloppen.
- [ ] AUTH-34 (hoog) Nieuw sessie-id bij inloggen en bij elke rechtenwijziging. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-35 (hoog) Leg een idle timeout en een absolute timeout vast en dwing ze op de server af. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-36 (kritiek) Uitloggen en blokkeren werken direct op de server. [alleen: met login] Afgevinkt als beide tests groen zijn.
- [ ] AUTH-39 (kritiek) Leg het algoritme vast bij verificatie. Afgevinkt als de tests groen zijn.
- [ ] AUTH-40 (kritiek) Haal verificatiesleutels uit je eigen configuratie, niet uit het token. Afgevinkt als de test groen is.
- [ ] AUTH-41 (kritiek) Valideer geldigheid, uitgever, publiek en type van elk token. Afgevinkt als de vier tests groen zijn.
- [ ] AUTH-42 (hoog) Symmetrische tokensleutels: willekeurig en minimaal zo lang als de hash. Afgevinkt als beide kloppen.
- [ ] AUTH-44 (kritiek) Alleen de authorization code flow met PKCE (S256). Afgevinkt als dit klopt.
- [ ] AUTH-45 (kritiek) Redirect-URI's exact vergelijken. Afgevinkt als de tests groen zijn of een schermafdruk van de registratie in het dossier zit.
- [ ] AUTH-46 (hoog) Bind `state`, PKCE en `nonce` aan de browsersessie die de flow startte. Afgevinkt als de tests groen zijn.
- [ ] AUTH-49 (kritiek) Als resource server: alleen tokens voor jou, en scopes afdwingen. Afgevinkt als de tests groen zijn.
- [ ] AUTH-50 (hoog) Refresh tokens: roteren met hergebruikdetectie, eindig en intrekbaar. Afgevinkt als de tests groen zijn.
- [ ] AUTH-51 (hoog) Houd tokens en clientgeheimen bij de backend en vraag minimale scopes. Afgevinkt als beide kloppen.
- [ ] AUTH-52 (hoog) Als je zelf autorisatieserver bent: codes eenmalig en kort, toestemming expliciet. Afgevinkt als de tests groen zijn.
- [ ] AUTH-53 (kritiek) API-sleutels: willekeurig, herkenbaar, alleen als hash opgeslagen, één keer getoond. Afgevinkt als alle drie kloppen.
- [ ] AUTH-54 (hoog) API-sleutels: scopes, eigenaar, vervaldatum, rotatie zonder storing. Afgevinkt als de tests groen zijn.
- [ ] AUTH-55 (hoog) Een API-sleutel is geen gebruikerslogin, en hoort in een header. Afgevinkt als de test groen is.
- [ ] AUTH-56 (hoog) Diensten onderling: eigen identiteit per dienst met minimale rechten. Afgevinkt als dat klopt.
- [ ] AUTH-57 (hoog) Vergelijk geheimen in constante tijd. Afgevinkt als beide kloppen.
- [ ] AUTH-58 (kritiek) Inkomende webhooks: handtekening over de ruwe body controleren. Afgevinkt als de drie tests groen zijn.
- [ ] AUTH-62 (kritiek) Weiger standaard en dwing af op de server, op één plek. Afgevinkt als die test in CI staat.
- [ ] AUTH-63 (kritiek) Controleer bij elk object of het van deze gebruiker en deze tenant is. Afgevinkt als elke route in de lijst een test heeft (zie AUTH-66).
- [ ] AUTH-65 (kritiek) Laat een gebruiker geen velden zetten die zijn rechten bepalen. Afgevinkt als de test groen is.
- [ ] AUTH-66 (hoog) Autorisatietests met twee gebruikers en twee tenants zijn een CI-gate. Afgevinkt als beide in CI staan.
- [ ] AUTH-67 (hoog) Vertrouw niet alleen op middleware, proxy of route-volgorde. Afgevinkt als dat zo is.
- [ ] AUTH-69 (hoog) Bestanden, exports en back-ups vallen onder dezelfde autorisatie. Afgevinkt als beide kloppen.
- [ ] AUTH-70 (middel) Log geweigerde toegang en geef geen details prijs. Afgevinkt als de test groen is.
- [ ] AUTH-73 (kritiek) Rollen gelden per tenant, niet globaal. Afgevinkt als de test groen is.
- [ ] AUTH-74 (kritiek) Tenant-filter in elke query plus rij-niveau beveiliging als vangnet. Afgevinkt als beide kloppen.
- [ ] AUTH-82 (hoog) Beheerinterfaces: MFA, eigen pad, niet alleen een IP-filter. [alleen: met beheer] Afgevinkt als beide kloppen.
- [ ] AUTH-84 (hoog) Auditlog van gevoelige acties. [bron niet gelezen: NEN] Afgevinkt als beide kloppen.
- [ ] API-01 (kritiek) Schema-validatie aan elke rand. Elke route heeft een schema voor body, query en params (Fastify `schema` of een zod-parse als eerste regel).
- [ ] API-02 (hoog) Weiger onbekende velden en bind nooit de hele body. `grep -rnE "\.set\((req|request)\.|\.values\((req|request)\." src` is leeg. Test: een PATCH met een extra veld `role` geeft 400 en wijzigt niets.
- [ ] API-03 (hoog) Geef elk veld een grens. Lint- of reviewcontrole: geen `z.string()` zonder `.max()` of formaat, geen `z.array()` zonder `.max()`. Test per route met een te lange waarde verwacht 400.
- [ ] API-04 (middel) Ken de Ajv-standaarden van Fastify en laat `allErrors` uit. `grep -rn "allErrors" src` is leeg of `false`.
- [ ] API-05 (hoog) Accepteer alleen de content-types die je verwacht. `npm ls fastify` toont 5.12.5 of hoger (de ondergrens van INV-15: na CVE-2025-32442, gerepareerd in 5.3.2, volgden in 2026 nog vijf advisories over de body-validatie, de 
- [ ] API-07 (middel) Decodeer één keer, vóór de validatie. `grep -rn "decodeURIComponent\|urldecode\|rawurldecode" src` toont alleen aanroepen vóór de schema-parse. Test met dubbel gecodeerde invoer.
- [ ] API-09 (hoog) Geef alleen de velden terug die de client nodig heeft. Elke route heeft een response-schema of een mapper.
- [ ] API-10 (hoog) Zet een eigen error handler; Fastify stuurt de foutmelding letterlijk door. `grep -rn "setErrorHandler" src` geeft een treffer. Test: een route die `throw new Error('geheim pad /srv/x')` doet, geeft een antwoord waar die tekst niet in staat.
- [ ] API-12 (kritiek) Faal dicht. Test per controle met een mock die gooit: de actie erna gebeurt niet. Review: elke `catch` zonder `throw` of `return` rond een controle is een bevinding.
- [ ] API-13 (hoog) Laat het proces stoppen bij een onafgehandelde fout. `grep -rn "unhandledRejection\|uncaughtException" src` toont alleen een handler die logt en `process.exit(1)` aanroept.
- [ ] API-17 (hoog) Pagineer elke lijst met een maximum dat de server bepaalt. Elk lijstschema bevat `limit: z.coerce.number().int().min(1).max(100).default(25)`.
- [ ] API-18 (middel) Kies de body-limiet bewust en houd nginx gelijk. `grep -rn "bodyLimit" src` toont alleen route-specifieke verhogingen met een reden.
- [ ] API-19 (hoog) Zet time-outs op de server; de standaard is geen time-out. De service luistert op `127.0.0.1` of een intern Docker-netwerk (`ss -ltnp`), niet rechtstreeks op een publiek adres, of `requestTimeout` staat ingesteld.
- [ ] API-20 (hoog) Begrens verzoeken per route-klasse en per identiteit. Test: N+1 verzoeken binnen het venster geven 429.
- [ ] API-23 (middel) Zet duur werk in een wachtrij en begrens het per gebruiker. De lijst van dure functies staat in de projectdocumentatie met per functie de limiet.
- [ ] API-30 (kritiek) Maak controleren en handelen één atomaire stap. Een test vuurt 20 gelijktijdige verzoeken af op dezelfde bewerking en controleert dat het effect precies één keer optreedt.
- [ ] API-32 (kritiek) Zet een samengestelde bewerking in één transactie. De statusovergang en het aanmaken van de taak staan in dezelfde `db.transaction`. Test: een fout na de eerste schrijfactie laat de status ongewijzigd.
- [ ] API-33 (hoog) Maak eigen muterende routes met een extern effect idempotent. Test: twee identieke POST's met dezelfde sleutel geven hetzelfde antwoord en één rij.
- [ ] API-34 (middel) Leg limieten per gebruiker en in totaal vast en dwing ze af. De limieten staan in de projectdocumentatie. Per limiet een test die de grens overschrijdt. Overschrijdingen worden gelogd (ASVS V16.3.3).
- [ ] API-47 (hoog) Onderteken uitgaande webhooks en bescherm de bezorger tegen SSRF. Tests met `http://`, `https://127.0.0.1`, `https://[::1]`, een privé-adres, en een host die doorverwijst naar een intern adres: alle geweigerd.
- [ ] API-48 (hoog) Geef elke uitgaande aanroep een time-out, een maximale omvang en geen redirects. `grep -rn "fetch(" src` toont bij elke aanroep een `signal`.
- [ ] API-49 (middel) Herhaal begrensd, met oplopende wachttijd, en alleen wat veilig te herhalen is. Eén gedeelde herhaalfunctie met een maximum;
- [ ] API-50 (hoog) Valideer antwoorden van externe diensten net zo streng als invoer van gebruikers. Elke client-module exporteert geparste types;
- [ ] API-53 (kritiek) Start processen zonder shell en met een argumentenlijst. `grep -rnE "\bexec\(|execSync\(|shell: *true" src` is leeg.
- [ ] API-54 (kritiek) Maak bestandspaden zelf en controleer dat ze binnen de basismap blijven. Test met `../`, `..%2f`, een absoluut pad en een naam met een nulbyte: alle geweigerd.
- [ ] API-55 (kritiek) Deserialiseer onvertrouwde data alleen als JSON met een schema. `grep -rnE "unserialize\(|maybe_unserialize\(" .` in PHP toont alleen data uit eigen opslag die niet door gebruikers te zetten is (zie WP voor `maybe_unserialize`).
- [ ] API-56 (kritiek) Voer nooit tekst als code uit. ESLint-regels `no-eval`, `no-implied-eval` en `no-new-func` staan aan en zijn groen. `grep -rnE "\beval\(|new Function\(|vm\.run" src` is leeg.
- [ ] API-57 (hoog) Houd reguliere expressies lineair en begrens de invoer ervoor. ESLint met `eslint-plugin-security` (`detect-unsafe-regex`, `detect-non-literal-regexp`) of `eslint-plugin-regexp` is groen.
- [ ] API-58 (hoog) Voorkom prototype pollution. `grep -rnE "merge\(|defaultsDeep|extend\(true|Object\.assign\([^,]+, *(req|request)" src` wordt per treffer beoordeeld.
- [ ] API-59 (middel) Maak exports veilig tegen formule-injectie. Unit-test op de exportfunctie met elk van de zes begintekens. Eén gedeelde exportfunctie, geen losse `join(',')`.
- [ ] API-60 (hoog) Begrens en controleer uploads aan de API-kant. De registratie van `@fastify/multipart` toont alle vier de limieten.
- [ ] API-61 (kritiek) Maak onraadbare waarden met een CSPRNG en minimaal 128 bits. `grep -rnE "Math\.random|mt_rand|\brand\(|uniqid\(" src` is leeg in code die tokens, namen van privébestanden of codes maakt. Een UUID v4 mag als id, niet als geheim.
- [ ] API-63 (hoog) Kies bewust tussen hashen en versleutelen. `grep -rnE "createCipher\(|aes-...-(ecb|cbc)|md5|sha1" src` wordt per treffer beoordeeld.
- [ ] API-64 (hoog) Schrijf geen eigen cryptografie. Review: elke plek waar een handtekening of sleutel wordt gemaakt gebruikt HMAC of een bibliotheekfunctie.
- [ ] API-65 (kritiek) Houd geheimen uit code en build en valideer ze bij de start. Afgevinkt met de uitvoer van beide.
- [ ] API-66 (hoog) Log geen geheimen en geen persoonsgegevens. De logger-configuratie bevat `redact`.
- [ ] API-67 (hoog) Zet de strikte TypeScript-opties aan en maak de typecheck een gate. `tsc --showConfig` toont de zes opties.
- [ ] API-68 (hoog) Lint met type-informatie en laat de build erop falen. `eslint .
- [ ] API-69 (middel) Geen `any`, geen cast en geen `!` op data van buiten. De lint van API-68 is groen zonder `eslint-disable` voor `no-explicit-any` of `no-unsafe-*`.
- [ ] API-70 (hoog) Handel elke promise af. `no-floating-promises` en `no-misused-promises` staan aan (API-68). Achtergrondtaken hebben een eigen `try/catch` die logt en alarmeert.
- [ ] API-72 (hoog) Draai op een ondersteunde Node-versie. `node -v` op de server en in het image toont 22.x (ondersteund tot 30-04-2027) of 24.x (tot 30-04-2028). `package.json` heeft `"engines": { "node": ">=22" }`.
- [ ] API-74 (hoog) Geen debugmodus, inspector of experimentele functies in productie. `systemctl cat <dienst>` en de `CMD` van het image tonen geen `--inspect` of `watch`.
- [ ] BIZ-01 (hoog) Schrijf een teller of saldo als relatieve bewerking in SQL. `grep -rnE "\.set\(\{[^}]*(\+|-) *[0-9a-zA-Z_.]+" src` toont geen rekensom in JavaScript op een kolom die een teller of saldo is;
- [ ] BIZ-02 (hoog) Bewaak een regel over meerdere rijen met één slot op de ouder, niet met een slot op de rijen zelf. Per regel over meerdere rijen staat in de projectdocumentatie welk slot hem bewaakt.
- [ ] BIZ-03 (middel) Gebruik advisory locks alleen op transactieniveau en met een vaste sleutelruimte. `grep -rnE "pg_(try_)?advisory_lock\(" src` is leeg (alleen `_xact_`-varianten).
- [ ] BIZ-05 (middel) Een unieke sleutel met een kolom die NULL kan zijn, houdt geen duplicaten tegen. Query op het schema: elke kolom in een unieke index is `NOT NULL` of de index heeft `indnullsnotdistinct = true` (`SELECT indexrelid::regclass, indnullsnotdistinct FROM p
- [ ] BIZ-07 (middel) Weiger een bewerking op verouderde gegevens met een versienummer. Elke tabel die via een formulier of een tool wordt bewerkt heeft een versiekolom (of gebruikt `updated_at` als voorwaarde).
- [ ] BIZ-09 (middel) Een slot in het geheugen van het proces is geen slot. `grep -rnE "new (Map|Set)\(|let [a-zA-Z]+ = (0|\[\]|\{\})" src` op moduleniveau: elke treffer is een cache zonder gevolgen voor de uitkomst, of is gedocumenteerd.
- [ ] BIZ-11 (hoog) Maak van een numeric uit de database geen JavaScript-getal om mee te rekenen. `grep -rnE "Number\(|parseFloat\(|toFixed\(|Math\.round\(" src` in prijs-, korting-, btw- en betaalcode: elke treffer werkt op gehele centen of is weergave;
- [ ] BIZ-21 (middel) Boek verbruik van een quotum vóór de dure actie en geef het terug als de actie mislukt. Test: 50 gelijktijdige verzoeken bij één resterende eenheid geven precies één aanroep van de nagebootste dienst en 49 keer 429.
- [ ] BIZ-23 (hoog) Geef elke automatische stroom die geld kost of iets naar buiten stuurt een dagplafond dat stopt. Per stroom staat in de projectdocumentatie het plafond per tenant en in totaal, en wie hem weer aanzet.
- [ ] BIZ-24 (middel) Geloof bij een bericht over een toestand de actuele stand, niet de inhoud of de volgorde van het bericht. Test: bied de berichten van één betaling aan in omgekeerde volgorde en dubbel;
- [ ] BIZ-25 (middel) Controleer een termijn op het moment van gebruik en reken niet op de opruimjob. Test met een vaste klok: een rij met `verloopt_op` één seconde in het verleden wordt geweigerd terwijl de status nog "actief" is.
- [ ] BIZ-27 (middel) Bepaal zakelijke datums in Europe/Amsterdam en sla ze op als datum. `grep -rnE "toISOString\(\)\.(slice|substring|split)" src` raakt geen zakelijke datum.
- [ ] BIZ-37 (middel) Geef opzoekfuncties met zakelijke waarde een eigen limiet. Per opzoekfunctie staat de limiet in de documentatie (API-34) en is er een test die hem overschrijdt (429 met `Retry-After`).
- [ ] BIZ-39 (middel) Bind een idempotentiesleutel aan de eigenaar, de route en de inhoud, en ken de toestand "in behandeling". Tests: dezelfde sleutel van een andere tenant voert het verzoek gewoon uit als nieuw en geeft niets van de eerste terug;
- [ ] BIZ-40 (hoog) Een time-out is "onbekend", niet "mislukt". Het statusveld van elke uitgaande taak kent "onbekend".
- [ ] BIZ-41 (hoog) Voorkom dubbele facturen in Moneybird met een eigen claim, want Moneybird kent geen idempotentiesleutel. `\d documenten` toont de unieke index op (bestelling, soort) en een unieke index op het Moneybird-id.
- [ ] BIZ-42 (middel) Geef een geclaimde taak een huurtermijn. Test: claim een taak, laat de worker niets doen, zet de klok voorbij de termijn;
- [ ] BIZ-43 (middel) Maak een MCP-tool met een zakelijk effect idempotent op de zakelijke sleutel. Per tool met een effect: een test die hem twee keer achter elkaar en twee keer tegelijk aanroept met dezelfde argumenten en één resultaat in de database verwacht.

### dicht-database
- [ ] DB-01 (kritiek) Geen superuser als applicatierol. Afgevinkt als de rol van elke dienst op alle vijf kolommen `f` heeft.
- [ ] DB-02 (hoog) Eén loginrol per dienst en per omgeving. Afgevinkt als elke dienst een eigen rol toont en geen rol in twee omgevingen bestaat met hetzelfde wachtwoord (controle in de geheimenopslag).
- [ ] DB-03 (hoog) Scheid de eigenaar (migratierol) van de runtime-rol. Afgevinkt als geen tabel de runtime-rol als eigenaar heeft en de migratierol niet in een runtime-`DATABASE_URL` voorkomt.
- [ ] DB-04 (hoog) Trek de standaardrechten van PUBLIC in. [bron niet gelezen: CIS] Afgevinkt als in `datacl` geen regel `=Tc/.
- [ ] DB-05 (hoog) Verleen rechten per tabel en per bewerking, nooit GRANT ALL. Afgevinkt als geen `TRUNCATE`, `REFERENCES` of `TRIGGER` voorkomt en audit-tabellen alleen `INSERT` en `SELECT` hebben.
- [ ] DB-06 (kritiek) Geen gevaarlijke rolattributen of voorgedefinieerde rollen voor applicaties. Afgevinkt als applicatierollen in geen van beide voorkomen.
- [ ] DB-07 (middel) Trek EXECUTE op functies in van PUBLIC. Afgevinkt als de query voor eigen functies nul rijen geeft (een lege `proacl` betekent de standaard, dus PUBLIC mag uitvoeren).
- [ ] DB-09 (hoog) Vrije query-tools draaien onder een alleen-lezen rol. Afgevinkt als alle vijf een rechtenfout geven en `SELECT rolconfig FROM pg_roles WHERE rolname = '<rol>'` een `statement_timeout` toont.
- [ ] DB-12 (hoog) Elke tenant-tabel heeft een verplichte tenant_id. Afgevinkt als het verschil leeg is en `is_nullable = 'NO'` voor elke `tenant_id`.
- [ ] DB-13 (kritiek) Zet RLS aan en dwing hem af op elke tenant-tabel. Afgevinkt als elke tenant-tabel op beide kolommen `t` heeft.
- [ ] DB-14 (kritiek) De runtime-rol mag RLS niet kunnen omzeilen. Afgevinkt als `rolsuper = f`, `rolbypassrls = f` en de test slaagt.
- [ ] DB-15 (hoog) Schrijf policies met USING en WITH CHECK, en gebruik restrictief voor de tenantgrens. Afgevinkt als elke tenant-tabel een `RESTRICTIVE`-policy met gevulde `qual` en `with_check` heeft, en de test uit DB-22 ook een `INSERT` en `UPDATE` naar een andere tenant weigert.
- [ ] DB-16 (kritiek) Zet de tenantcontext per transactie, nooit per sessie. Afgevinkt als de grep leeg is en de test slaagt.
- [ ] DB-17 (kritiek) Tenantcontext komt uit de geverifieerde sessie en faalt gesloten. Afgevinkt als alle drie kloppen.
- [ ] DB-18 (hoog) Views over tenant-tabellen krijgen security_invoker. Afgevinkt als elke view over tenant-tabellen `security_invoker=true` toont en in de isolatietest van DB-22 is opgenomen.
- [ ] DB-19 (hoog) SECURITY DEFINER-functies zijn uitzonderingen met drie verplichte maatregelen. Afgevinkt als elke rij een `search_path` in `proconfig` heeft dat op `pg_temp` eindigt, `proacl` geen PUBLIC bevat, en elke functie in de isolatietest van DB-22 zit.
- [ ] DB-20 (middel) Neem tenant_id op in unieke sleutels en samengestelde foreign keys. Afgevinkt als die lijst leeg is of elke uitzondering is toegelicht.
- [ ] DB-21 (middel) Geen TRUNCATE of REFERENCES voor de runtime-rol. Afgevinkt als `TRUNCATE` en `REFERENCES` niet voorkomen voor de runtime-rol.
- [ ] DB-22 (kritiek) Een cross-tenant regressietest per tabel, view en functie is een gate. Afgevinkt als beide groen zijn en de test in de verplichte CI-stappen staat.
- [ ] DB-23 (hoog) Tenant-id hoort ook in caches, wachtrijen, bestanden en exports. Afgevinkt als de test verschillende uitkomsten geeft en het schema `tenantId` verplicht stelt.
- [ ] DB-24 (middel) Back-up- en beheerrollen die RLS omzeilen zijn apart en niet bereikbaar voor de app. Afgevinkt als de proef dezelfde tellingen geeft als productie.
- [ ] DB-25 (kritiek) Alleen geparametriseerde queries. Afgevinkt als de gate groen is en er een test bestaat die een aanhalingsteken in elk zoekveld stuurt.
- [ ] DB-26 (kritiek) sql.raw en sql.unsafe nooit met invoer. Afgevinkt als elke treffer alleen constanten bevat en de reden erbij staat.
- [ ] DB-27 (hoog) Tabelnamen, kolomnamen en sorteerrichting via een allowlist. Afgevinkt als geen treffer invoer bevat en de test slaagt.
- [ ] DB-29 (hoog) Draai drizzle-orm 0.45.2 of hoger. Afgevinkt als elke kopie 0.
- [ ] DB-30 (hoog) Migraties zijn gereviewde SQL-bestanden in git. Afgevinkt als alle drie kloppen.
- [ ] DB-31 (hoog) Expand en contract: verwijder of hernoem nooit in dezelfde release. [eigen bron] Afgevinkt als de controle groen is en de verwijzing klopt.
- [ ] DB-32 (hoog) Zet lock_timeout in elke migratie. Afgevinkt als een van beide waar is.
- [ ] DB-33 (hoog) Bouw indexen op gevulde tabellen met CONCURRENTLY en controleer op ongeldige indexen. Afgevinkt als de controle in het script staat en leeg is.
- [ ] DB-34 (hoog) Voeg foreign keys en CHECK-constraints toe als NOT VALID en valideer apart. Afgevinkt als beide stappen bestaan en de query leeg is.
- [ ] DB-36 (hoog) Voorkom een herschrijving van de hele tabel. Afgevinkt als er geen treffer is of de meting en het venster zijn vastgelegd.
- [ ] DB-38 (middel) Vul gegevens bij in kleine batches, los van de schemamigratie. Afgevinkt als de tweede run nul rijen meldt.
- [ ] DB-39 (hoog) Test elke migratie op een recente kopie van productie. [eigen bron] Afgevinkt als de log bestaat, van na de laatste wijziging van het bestand is, en geen statement langer dan de `lock_timeout` een blokkerende lock hield.
- [ ] DB-40 (hoog) Leg de terugweg vast voordat je migreert. Afgevinkt als beide aanwezig zijn.
- [ ] DB-41 (middel) Eén migratieloper, als aparte deploystap met de migratierol. Afgevinkt als beide kloppen.
- [ ] DB-42 (middel) Controleer na elke uitrol dat schema en code overeenkomen. [eigen bron] Afgevinkt als de controle bestaat en de deploy stopt bij een verschil.
- [ ] DB-43 (hoog) Zet rechten en RLS in dezelfde migratie als de tabel. Afgevinkt als de controle groen is en de metatest uit DB-22 slaagt.
- [ ] DB-58 (kritiek) De database is niet bereikbaar vanaf internet. [bron niet gelezen: CIS] Afgevinkt als beide kloppen.
- [ ] DB-59 (hoog) Geen trust over TCP, alleen scram-sha-256. [bron niet gelezen: CIS] Afgevinkt als alle drie kloppen.
- [ ] DB-60 (hoog) TLS met certificaatcontrole zodra de verbinding de host verlaat. Afgevinkt als beide kloppen.
- [ ] DB-61 (middel) Zet en wissel wachtwoorden zonder dat ze in een log belanden. Afgevinkt als beide groen zijn.
- [ ] DB-62 (hoog) De verbindingsstring is een geheim. Afgevinkt als alle drie kloppen.
- [ ] DB-63 (middel) Begrens de pool per dienst en houd de som onder max_connections. Afgevinkt als de som onder `SHOW max_connections` blijft.
- [ ] DB-64 (middel) Met een pooler in transactiemodus bestaat er geen sessiestatus. Afgevinkt als bij transactiemodus geen sessiefuncties worden gebruikt.
- [ ] DB-65 (hoog) Zet time-outs per rol. Afgevinkt als elke applicatierol de drie instellingen heeft.
- [ ] DB-68 (hoog) Verwerk webhooks en opdrachten idempotent met een unieke sleutel. Afgevinkt als beide kloppen.
- [ ] DB-69 (middel) Wie een strenger isolatieniveau kiest, bouwt de herhaling erbij. Afgevinkt als elke treffer een lus heeft, of er geen treffers zijn.
- [ ] DB-70 (hoog) Leg regels vast in de database: NOT NULL, CHECK, UNIQUE en foreign keys. Afgevinkt als de test voor de kerntabellen bestaat.
- [ ] DB-73 (middel) Houd transacties kort: geen netwerkaanroepen binnen een transactie. Afgevinkt als beide kloppen en DB-65 als vangnet is ingesteld.
- [ ] DB-74 (middel) Tijdstippen zijn timestamptz. `SELECT table_name, column_name FROM information_schema.columns WHERE data_type = 'timestamp without time zone' AND table_schema = 'public';` is leeg of elke rij is toege
- [ ] DB-75 (hoog) Geld is numeric of een geheel aantal centen. Afgevinkt als dat zo is en er een test is die 0,1 + 0,2 op het rekenpad controleert.
- [ ] DB-78 (middel) Soft delete is een bewuste keuze met een einddatum. Afgevinkt als beide bestaan.
- [ ] DB-79 (laag) Elke database is UTF8. `SELECT datname, pg_encoding_to_char(encoding) FROM pg_database;` toont overal `UTF8`.
- [ ] DB-80 (hoog) Versleutel geheimen en bijzondere gegevens per kolom in de applicatie. Afgevinkt als alle vier kloppen.
- [ ] DB-81 (hoog) Wat je alleen hoeft te vergelijken, hash je; en niet met pgcrypto. Afgevinkt als dat zo is.
- [ ] DB-84 (middel) Een verwijderverzoek is een getest script. Afgevinkt als beide bestaan.
- [ ] DB-85 (hoog) Geen echte persoonsgegevens in ontwikkeling en accept zonder maskering. Afgevinkt als dat zo is.
- [ ] DB-86 (middel) Pseudonimiseren is niet anonimiseren. [bron niet gelezen: EDPB] Afgevinkt als dat is vastgelegd.
- [ ] DB-88 (hoog) Het databaselog bevat geen persoonsgegevens of geheimen. Afgevinkt als de instellingen kloppen en de steekproef nul geeft.

### dicht-infra
- [ ] INFRA-01 (kritiek) Laat SSH alleen sleutels toe. Afgevinkt met beide uitvoeren.
- [ ] INFRA-02 (hoog) Verbied inloggen als root. Afgevinkt met beide uitvoeren.
- [ ] INFRA-03 (hoog) Lees de effectieve configuratie, niet het bestand. Afgevinkt als de waarden uit `sshd -T` kloppen.
- [ ] INFRA-06 (hoog) Demp raadpogingen en houd OpenSSH bij. Afgevinkt met de drie uitvoeren.
- [ ] INFRA-07 (hoog) Geef elke sleutel één doel en beperk automatiseringssleutels. Afgevinkt als elke automatiseringssleutel `restrict` heeft of de uitzondering is genoteerd.
- [ ] INFRA-10 (hoog) Behandel de docker-groep en wachtwoordloze sudo als root. Afgevinkt met de uitvoer per dienst, of met een genoteerde uitzondering.
- [ ] INFRA-11 (hoog) Zet beheerschermen niet open op internet. Afgevinkt met de lijst en de uitvoer.
- [ ] INFRA-12 (kritiek) Weiger inkomend verkeer standaard en bewijs het van buiten. Afgevinkt met beide uitvoeren en de datum.
- [ ] INFRA-13 (kritiek) Publiceer containerpoorten alleen op loopback. Afgevinkt met beide uitvoeren.
- [ ] INFRA-14 (hoog) Laat hostdiensten niet op alle adressen luisteren. Afgevinkt met de uitvoer.
- [ ] INFRA-16 (hoog) Neem IPv6 mee in elke controle. Afgevinkt met de uitvoer voor beide.
- [ ] INFRA-17 (hoog) Geef elke applicatie een eigen netwerk. Afgevinkt met de lijst en de proef.
- [ ] INFRA-26 (kritiek) Geef geen container toegang tot de Docker-socket. Afgevinkt met beide uitvoeren.
- [ ] INFRA-27 (hoog) Draai het proces in de container niet als root. Afgevinkt met de uitvoer.
- [ ] INFRA-28 (hoog) Laat alle capabilities vallen en geef alleen terug wat nodig is. Afgevinkt met de uitvoer.
- [ ] INFRA-29 (hoog) Verbied het verkrijgen van nieuwe rechten in de container. Afgevinkt met de uitvoer.
- [ ] INFRA-31 (kritiek) Geen privileged containers en geen namespaces van de host. Afgevinkt met uitvoer en notities.
- [ ] INFRA-32 (middel) Zet op elke container een limiet voor geheugen en processen. Afgevinkt met de uitvoer en de optelling.
- [ ] INFRA-33 (middel) Begrens de containerlogs. Afgevinkt met de uitvoer.
- [ ] INFRA-40 (middel) Geef elk Compose-project een eigen naam en gebruik `--remove-orphans` nooit op gedeelde projecten. Afgevinkt met de uitvoer.
- [ ] INFRA-42 (hoog) Draai een nginx-tak die nog fixes krijgt. Afgevinkt als de versie op een lopende tak staat en buiten elk kwetsbaar bereik valt.
- [ ] INFRA-43 (hoog) Weiger verbindingen voor onbekende hostnamen. Afgevinkt met beide uitvoeren, ook via IPv6.
- [ ] INFRA-44 (hoog) Zet protocollen en ciphers volgens Mozilla "intermediate". Afgevinkt met de drie uitvoeren.
- [ ] INFRA-45 (middel) Zet limieten en time-outs voor aanvragen expliciet. Afgevinkt met beide uitvoeren.
- [ ] INFRA-46 (hoog) Begrens aanvragen per bron in nginx en antwoord met 429. Afgevinkt met de configuratie en de lus per route.
- [ ] INFRA-47 (middel) Herlaad nginx alleen na een geslaagde test en controleer dat de nieuwe configuratie draait. Afgevinkt met de drie uitvoeren.
- [ ] INFRA-48 (hoog) Controleer het certificaat van een upstream buiten de host. Afgevinkt met de uitvoer.
- [ ] INFRA-50 (hoog) Vernieuw certificaten volledig automatisch. Afgevinkt als elke hostnaam een automatisch vernieuwd certificaat heeft.
- [ ] INFRA-51 (hoog) Laat de webserver het vernieuwde certificaat ook laden. Afgevinkt met de vergelijking en het mechanisme.
- [ ] INFRA-54 (hoog) Bescherm de private sleutel van het certificaat. Afgevinkt met de uitvoer.
- [ ] INFRA-55 (hoog) Versleutel en controleer elke verbinding die de host verlaat. Afgevinkt met de uitvoer.
- [ ] INFRA-66 (hoog) Geef elke dienst een eigen systeemaccount. Afgevinkt met de uitvoer.
- [ ] INFRA-67 (middel) Zet de sandbox van systemd aan op elke eigen dienst. Afgevinkt met de uitvoer en de test.
- [ ] INFRA-69 (hoog) Laat elke geplande taak een fout melden en voorkom dubbel draaien. Afgevinkt met de lijst en de proefmelding.
- [ ] INFRA-70 (middel) Bescherm de scripts die door cron en timers worden uitgevoerd. Afgevinkt met de uitvoer.
- [ ] INFRA-72 (kritiek) Bewaar geheimen in bestanden met modus 600 buiten elke repository. Afgevinkt met de uitvoer.
- [ ] INFRA-74 (hoog) Geef elke omgeving eigen geheimen en eigen data. Afgevinkt met de vergelijking.
- [ ] INFRA-76 (middel) Houd geheimen uit commandoregels, logs en shellgeschiedenis. Afgevinkt met de uitvoer.
- [ ] INFRA-77 (hoog) Geef elke dienst een eigen sleutel met de kleinste reikwijdte. Afgevinkt met de lijst.
- [ ] INFRA-78 (hoog) Zorg dat je zonder de server bij de geheimen kunt. Afgevinkt met het verslag van de proef.

### dicht-git
- [ ] GIT-01 (hoog) Eén sessie, één worktree, één branch. Afgevinkt met beide uitvoeren.
- [ ] GIT-02 (hoog) De live checkout staat op main en verandert alleen door een merge. Afgevinkt met de drie uitvoeren.
- [ ] GIT-03 (hoog) Valideer voordat je commit, merget of herstart. Afgevinkt met beide.
- [ ] GIT-04 (hoog) Stage alleen expliciete paden en lees wat je commit. Afgevinkt met de lijst.
- [ ] GIT-06 (hoog) Installeer afhankelijkheden in de worktree zelf. Afgevinkt met beide uitvoeren.
- [ ] GIT-07 (middel) Draai opdrachten in verschillende worktrees na elkaar. [eigen bron] Afgevinkt met die regel.
- [ ] GIT-10 (hoog) Zet .gitignore neer vóór de eerste commit en weet wat het niet doet. Afgevinkt met beide uitvoeren.
- [ ] GIT-11 (hoog) Maak geen repo van een map waarin tokens en shellgeschiedenis staan. Afgevinkt met de uitvoer.
- [ ] GIT-12 (middel) Houd git zelf bij en clone niets onvertrouwds met submodules. Afgevinkt met de drie uitvoeren.
- [ ] GIT-32 (kritiek) Geen geheim in code, configuratie, tests of commitberichten. Afgevinkt met de drie.
- [ ] GIT-33 (hoog) Scan op geheimen vóór elke commit, lokaal. Afgevinkt met de uitvoer van de geweigerde commit.
- [ ] GIT-34 (hoog) Scan de hele geschiedenis in de gate. Afgevinkt met de uitvoer.
- [ ] GIT-36 (kritiek) Een gelekt geheim is gecompromitteerd: trek het eerst in. Afgevinkt met die lijst.
- [ ] GIT-38 (middel) Verwijderd is niet weg: reken met forks, clones en SHA's. Afgevinkt met die notitie.
- [ ] GIT-39 (hoog) Houd geheimen uit CI-logs. Afgevinkt met beide uitvoeren.
- [ ] GIT-41 (kritiek) Zet elke actie vast op een volledige commit-SHA. Afgevinkt met de drie.
- [ ] GIT-43 (hoog) Geef het workflow-token standaard geen rechten. Afgevinkt met beide.
- [ ] GIT-44 (kritiek) Zet nooit een expressie met invoer van buiten in een run-stap. Afgevinkt met beide.
- [ ] GIT-45 (kritiek) Draai nooit code uit een pull request in een workflow met rechten. Afgevinkt met beide.
- [ ] GIT-46 (middel) Laat het token niet op de runner achter en upload geen verborgen bestanden. Afgevinkt met beide.
- [ ] GIT-47 (middel) Gebruik geen cache in een job die publiceert of uitrolt. Afgevinkt met beide.
- [ ] GIT-48 (hoog) Geef een geheim alleen aan de stap die het nodig heeft. Afgevinkt met beide.
- [ ] GIT-51 (hoog) Zet geen self-hosted runner op een server met productie of klantdata. Afgevinkt met beide.
- [ ] GIT-52 (middel) Laat Dependabot de gepinde acties bijwerken, met wachttijd. Afgevinkt met bestand en uitvoer.
- [ ] GIT-53 (hoog) Maak verplichte checks die niet stil kunnen slagen. Afgevinkt met de geblokkeerde PR en de grep.
- [ ] GIT-54 (hoog) Na een incident met een actie of pakket: alles roteren wat de job kon zien. Afgevinkt met die notitie.
- [ ] GIT-56 (hoog) Controleer elke workflow met zizmor en actionlint. Afgevinkt met de uitvoer.
- [ ] GIT-58 (hoog) Eén gate-opdracht, lokaal en in CI dezelfde. [eigen bron] Afgevinkt met beide.
- [ ] GIT-59 (hoog) De gate faalt gesloten. Afgevinkt met de rode uitvoer per scanner.
- [ ] GIT-60 (hoog) Statische analyse op beveiliging in de gate. Afgevinkt met de uitvoer.
- [ ] GIT-61 (hoog) Afhankelijkheden-audit als gate, op het lockfile. Afgevinkt met de uitvoer.
- [ ] GIT-62 (hoog) Zet de scanners zelf vast en haal ze niet op met curl naar sh. Afgevinkt met de grep en het script.
- [ ] GIT-65 (middel) Leg elke uitzondering vast met reden en einddatum. Afgevinkt met de bestanden.
- [ ] GIT-69 (hoog) Commit het lockfile en installeer alleen met npm ci. Afgevinkt met de drie.
- [ ] GIT-70 (middel) Lees de diff van het lockfile. Afgevinkt met beide.
- [ ] GIT-71 (hoog) Draai geen install-scripts van afhankelijkheden. Afgevinkt met de uitvoer.
- [ ] GIT-72 (hoog) Installeer geen versie die jonger is dan zeven dagen. Afgevinkt met de drie.
- [ ] GIT-73 (middel) Geen afhankelijkheden uit git of van een losse URL. Afgevinkt met beide, of met elke treffer naast zijn regel in het uitzonderingenregister (ARCH-30) met commit-SHA of hash, reden en einddatum; de bekende uitzondering is SheetJS van de eigen bron van de maker (INV-21).
- [ ] GIT-75 (hoog) Onderbouw elke nieuwe afhankelijkheid kort. Afgevinkt met de commit.
- [ ] GIT-78 (hoog) Controleer de naam van een pakket voordat je het installeert. Afgevinkt met die uitvoer.
- [ ] GIT-80 (middel) Houd productie klein: geen dev-pakketten, geen ongebruikte pakketten. Afgevinkt met beide.
- [ ] GIT-91 (hoog) Zet elke image vast op tag plus digest. [bron niet gelezen: CIS] Afgevinkt met de uitvoer.
- [ ] GIT-93 (hoog) Gebruik alleen runtimes die nog beveiligingsfixes krijgen. Afgevinkt met de uitvoer.
- [ ] GIT-95 (kritiek) Geen geheim in een image, een laag of de bouwcontext. [bron niet gelezen: CIS] Afgevinkt met de vier.
- [ ] GIT-96 (hoog) Haal in een Dockerfile niets op zonder controlesom. [bron niet gelezen: CIS] Afgevinkt met de uitvoer.
- [ ] GIT-97 (middel) Weet welke image draait. Afgevinkt met de notitie.
- [ ] GIT-101 (middel) Maak bij elke release een SBOM. [bron niet gelezen: WET] Afgevinkt met het bestand.
- [ ] GIT-102 (middel) Een release is een ondertekende tag op een gevalideerde commit. Afgevinkt met de drie.

### dicht-wordpress
- [ ] WP-81 (hoog) Geef WooCommerce REST-sleutels het minste recht en gebruik ze alleen over HTTPS. Afgevinkt met de lijst en de grep.
- [ ] WP-82 (hoog) Controleer de handtekening van een WooCommerce-webhook over de ruwe body. Afgevinkt met de testuitvoer.

### dicht-ai-mcp
- [ ] AI-02 (kritiek) Geen agent met onvertrouwde invoer, gevoelige data en een uitweg tegelijk. [bron niet gelezen: AGENTIC] Afgevinkt met de tabel.
- [ ] AI-03 (hoog) Ken elke bron die in de context komt en geef hem een vertrouwensniveau. Afgevinkt als geen variabele ontbreekt.
- [ ] AI-04 (hoog) Lever onvertrouwde inhoud via een gescheiden, gelabeld kanaal. Afgevinkt met grep en testuitvoer.
- [ ] AI-06 (kritiek) Dwing autorisatie en beveiligingsbesluiten af in code, nooit in het model. [bron niet gelezen: AGENTIC] Afgevinkt als die test voor elke muterende tool in CI draait.
- [ ] AI-07 (hoog) Verwijder onzichtbare tekens bij inname en bij weergave. Afgevinkt met de testuitvoer.
- [ ] AI-10 (hoog) Schrijven naar geheugen of duurzame context is een geprivilegieerde handeling. [bron niet gelezen: AGENTIC] Afgevinkt met de testuitvoer en de bronkolom.
- [ ] AI-11 (hoog) Valideer modeluitvoer tegen een strikt schema in code. Afgevinkt met de testuitvoer.
- [ ] AI-12 (kritiek) Voer modeluitvoer nooit uit als code, query, commando of pad. [bron niet gelezen: AGENTIC] Afgevinkt met de grep-uitvoer en een verklaring per treffer.
- [ ] AI-15 (middel) Controleer elke link uit een model en open er nooit automatisch een. Afgevinkt met de testuitvoer en de grep.
- [ ] AI-18 (hoog) Feiten waar iemand op vertrouwt komen uit een bron, niet uit het model. Afgevinkt met de testuitvoer.
- [ ] AI-19 (hoog) Geef een agent alleen de tools die de taak nodig heeft. [bron niet gelezen: AGENTIC] Afgevinkt met de lijst en de testuitvoer.
- [ ] AI-21 (kritiek) De identiteit achter een tool heeft minimale rechten in het achterliggende systeem. [bron niet gelezen: AGENTIC] Afgevinkt met de uitvoer.
- [ ] AI-22 (kritiek) Voer tools uit in de context van de gebruiker en zijn tenant. Afgevinkt met de testuitvoer.
- [ ] AI-23 (hoog) Valideer elk toolargument als onvertrouwde invoer. Afgevinkt met de testuitvoer.
- [ ] AI-24 (kritiek) Een mens keurt elke onomkeerbare of naar buiten zichtbare actie goed, op de exacte inhoud. Afgevinkt met de lijst en beide testuitvoeren.
- [ ] AI-25 (kritiek) De goedkeuring wordt buiten het model afgedwongen en faalt gesloten. [bron niet gelezen: AGENTIC] Afgevinkt met de testuitvoer.
- [ ] AI-28 (kritiek) Geheimen blijven in code en komen nooit in de context van het model. Afgevinkt met grep en testuitvoer.
- [ ] AI-31 (hoog) Begrens elke agentrun in stappen, tijd en kosten. Afgevinkt met de testuitvoer en de waarden.
- [ ] AI-32 (kritiek) Elke MCP-server die niet uitsluitend lokaal via stdio draait, eist authenticatie op elke aanvraag. Afgevinkt met beide uitvoeren.
- [ ] AI-33 (kritiek) Accepteer alleen tokens die voor deze server zijn uitgegeven. Afgevinkt met de testuitvoer.
- [ ] AI-34 (kritiek) Geef het token van de client nooit door aan een achterliggende API. Afgevinkt met de grep en de aanwijzing in de code.
- [ ] AI-35 (hoog) Tokens staan in de Authorization-header, nooit in de URL. Afgevinkt met de curl-uitvoer en de grep.
- [ ] AI-36 (hoog) Bouw je OAuth voor MCP, volg dan het profiel van de specificatie volledig. Afgevinkt met de drie uitvoeren.
- [ ] AI-37 (hoog) Statische MCP-tokens: als hash opgeslagen, per tenant, met scope, vervaldatum en intrekking. (1) In de database staat alleen de hash (`\d api_tokens` toont geen kolom met het token zelf).
- [ ] AI-38 (hoog) Valideer de Origin-header op elk HTTP-eindpunt van een MCP-server. Afgevinkt met beide uitvoeren.
- [ ] AI-39 (hoog) Een lokale MCP-server gebruikt stdio, of luistert alleen op 127.0.0.1 met authenticatie. Afgevinkt met de drie uitvoeren.
- [ ] AI-40 (hoog) Een MCP-proxy met één vaste client-id vraagt per client toestemming. Afgevinkt met de testuitvoer en de headers.
- [ ] AI-41 (hoog) Een statushandle is een naam, geen sleutel. Afgevinkt met de testuitvoer.
- [ ] AI-42 (hoog) Deel geen server- of transportinstantie tussen clients. Afgevinkt met de versie en de testuitvoer.
- [ ] AI-44 (hoog) Een toolresultaat is gelabelde, minimale en opgeschoonde data. Afgevinkt met de testuitvoer.
- [ ] AI-45 (hoog) Begrens tool-aanroepen per token en per tenant. Afgevinkt met de lusuitvoer en de waarden.
- [ ] AI-46 (hoog) Paden en URI's in tools en resources blijven binnen de basismap, ook na het volgen van symlinks. Afgevinkt met de testuitvoer.
- [ ] AI-47 (kritiek) Een tool start nooit een shell met toolargumenten. [bron niet gelezen: AGENTIC] Afgevinkt met grep en testuitvoer.
- [ ] AI-48 (hoog) Een tool die een URL ophaalt, valt onder de SSRF-regels. Afgevinkt met de testuitvoer.
- [ ] AI-49 (hoog) Vraag nooit een wachtwoord, sleutel of betaalgegeven via het model. Afgevinkt met de grep en, indien van toepassing, een e2e-test van de URL-stroom.
- [ ] AI-52 (hoog) Log elke tool-aanroep met wie, wat en uitkomst, zonder geheimen. Afgevinkt met de query-uitvoer.
- [ ] AI-53 (kritiek) Elke tool heeft een isolatietest met twee tenants. Afgevinkt met de CI-uitvoer.
- [ ] AI-55 (hoog) Beoordeel elke MCP-server voordat hij wordt aangesloten. [bron niet gelezen: AGENTIC] Afgevinkt met de lijst.
- [ ] AI-56 (hoog) Zet elke MCP-server vast op een versie. Afgevinkt met de grep-uitvoer.
- [ ] AI-57 (hoog) Controleer naam en uitgever letter voor letter. Afgevinkt met beide gegevens.
- [ ] AI-59 (hoog) Agentconfiguratie in een repository is code en wordt als code beoordeeld. [bron niet gelezen: AGENTIC] Afgevinkt met de uitvoer en een notitie.
- [ ] AI-60 (hoog) Tokens voor MCP-servers staan niet in platte tekst in bestanden die gedeeld, gevolgd of geback-upt worden. Afgevinkt met de drie uitvoeren.
- [ ] AI-61 (hoog) Elke server krijgt een eigen credential met de kleinste scope. Afgevinkt met de lijst.
- [ ] AI-62 (hoog) Lees een skill of plugin van een ander volledig, inclusief scripts, en zet netwerkaanroepen uit. [bron niet gelezen: AGENTIC] Afgevinkt met de grep-uitvoer en de notitie.
- [ ] AI-63 (hoog) Houd AI-gereedschap actueel en gebruik geen overbodige tussenlagen. Afgevinkt met de versies en de rooktest.
- [ ] AI-64 (hoog) Bouw je zelf een MCP-client, vertrouw dan niets wat een server teruggeeft. Afgevinkt met de testuitvoer.
- [ ] AI-65 (hoog) Stuur alleen de velden naar een model die de taak nodig heeft. Afgevinkt met de testuitvoer.
- [ ] AI-67 (hoog) Behandel logs van prompts en antwoorden als de brongegevens zelf. Afgevinkt met de grep-uitvoer en de opruimjob.
- [ ] AI-68 (kritiek) Zoek in een vectorindex altijd met het tenant- en rechtenfilter in de query zelf. Afgevinkt met de testuitvoer.
- [ ] AI-69 (hoog) Leg bij elk fragment in de kennisbank de herkomst vast en houd vertrouwensniveaus gescheiden. [bron niet gelezen: AGENTIC] Afgevinkt met de drie uitvoeren.
- [ ] AI-71 (kritiek) Geen gedeelde context, cache of geheugen tussen tenants of gebruikers. Afgevinkt met grep en testuitvoer.
- [ ] AI-72 (hoog) Bijzondere en zorggegevens gaan niet naar een model zonder vastgelegd besluit. [bron niet gelezen: NEN] Afgevinkt met de tabel en de testuitvoer.
- [ ] AI-73 (hoog) Zet een hard uitgavenplafond dat stopt, niet alleen waarschuwt. Afgevinkt met beide.
- [ ] AI-74 (hoog) Begrens per gebruiker de invoer, de uitvoer en het aantal aanroepen. Afgevinkt met de testuitvoer.
- [ ] AI-75 (kritiek) Een modelproxy of inferentie-eindpunt is nooit zonder authenticatie bereikbaar. Afgevinkt met de drie uitvoeren.
- [ ] AI-76 (middel) Geef elke modelaanroep een time-out en een begrensde herhaling. Afgevinkt met de testuitvoer.

### dicht-privacy
- [ ] PRIV-14 (hoog) Geen echte persoonsgegevens naar een leverancier zonder verwerkersovereenkomst. Afgevinkt met de scriptuitvoer.
- [ ] PRIV-15 (hoog) Bied als verwerker zelf een overeenkomst aan, met een subverwerkerlijst die je bijhoudt. Afgevinkt met de lijst en, bij een wijziging, het bericht.
- [ ] PRIV-16 (hoog) Gebruik gegevens van klanten van klanten nooit voor eigen doelen. Afgevinkt met beide.
- [ ] PRIV-18 (hoog) Leg per leverancier vast in welk land de gegevens komen en op grond waarvan. Afgevinkt met het register.
- [ ] PRIV-25 (middel) Geef elke tijdelijke kopie een einddatum op het moment dat je hem maakt. Afgevinkt met de drie.
- [ ] PRIV-57 (hoog) Gebruik het BSN alleen als de wet het voorschrijft. Afgevinkt met de grep.
- [ ] PRIV-71 (hoog) Meld een actief uitgebuite kwetsbaarheid in je product binnen 24 uur. Afgevinkt met het document.
- [ ] PRIV-72 (middel) Geef elk product een meldpunt en een beleid voor het melden van kwetsbaarheden. Afgevinkt als de drie bestaan en een testbericht aankomt.
- [ ] PRIV-73 (hoog) Lever zonder bekende uitbuitbare kwetsbaarheden en met een veilige standaardconfiguratie. Afgevinkt met beide.
- [ ] PRIV-79 (hoog) Zeg bij de eerste interactie dat iemand met een AI-systeem te maken heeft. Afgevinkt met de testuitvoer.
- [ ] PRIV-83 (hoog) Laat persoonsgegevens alleen naar een AI-dienst gaan die in het register staat. Afgevinkt met de grep en het register.

### dicht-architectuur
- [ ] ARCH-07 (hoog) Lees configuratie uit de omgeving en valideer haar bij het opstarten. Afgevinkt met grep en test.
- [ ] ARCH-08 (hoog) Laat beveiliging niet afhangen van de naam van de omgeving. Afgevinkt met grep en test.
- [ ] ARCH-09 (hoog) Geef elke release een id en laat de dienst het zelf melden. Afgevinkt als de twee waarden in het bewijsbestand (ARCH-53) staan en gelijk zijn.
- [ ] ARCH-10 (middel) Houd ontwikkeling, test en productie gelijk in versies en soort diensten. Afgevinkt als de hoofdversies gelijk zijn.
- [ ] ARCH-12 (middel) Draai de dienst en de tests in UTC en sla tijd op met tijdzone. Afgevinkt met de drie waarnemingen.
- [ ] ARCH-17 (middel) Maak het afsluiten korter dan het geduld van de procesmanager. Afgevinkt met de waarden en de proef.
- [ ] ARCH-18 (hoog) Ga ervan uit dat een taak meer dan één keer draait. Afgevinkt met de testuitvoer.
- [ ] ARCH-19 (hoog) Geef elke wachtrij een maximum aantal pogingen, een dode-brievenbak en een alarm. Afgevinkt met de vier onderdelen.
- [ ] ARCH-33 (middel) Leg per project vast welke testlaag wat bewijst. Afgevinkt met het bestand en de uitvoer.
- [ ] ARCH-34 (hoog) Begin elke bugfix met een test die de fout laat zien. Afgevinkt met de twee uitvoeren.
- [ ] ARCH-35 (hoog) Test code die de database raakt tegen een echte PostgreSQL. Afgevinkt met beide uitvoeren in de testlog.
- [ ] ARCH-38 (hoog) Test elke functie langs vaste assen, niet alleen het gelukkige pad. Afgevinkt als geen as leeg is zonder reden.
- [ ] ARCH-40 (kritiek) Draai de beveiligingstests in de gate en nog een keer vlak voor de uitrol. Afgevinkt met de uitvoer van de laatste uitrol.
- [ ] ARCH-42 (hoog) Test kritieke logica met eigenschappen in plaats van alleen voorbeelden. Afgevinkt met lijst en uitvoer.
- [ ] ARCH-48 (hoog) Gebruik in tests alleen verzonnen gegevens. Afgevinkt met de grep.
- [ ] ARCH-49 (hoog) Geef tests eigen geheimen en houd inlogtoestanden uit git. Afgevinkt met de drie controles.
- [ ] ARCH-50 (hoog) Laat tests geen echte mail, betaling of oproep naar buiten sturen. Afgevinkt met de opzet en de grep.
- [ ] ARCH-51 (hoog) Beperk een test op productie tot lezen, of markeer en ruim op met exacte id's. [eigen bron] Afgevinkt met het script en de telling.
- [ ] ARCH-58 (hoog) Log gestructureerd, één regel per gebeurtenis, met vaste velden. Afgevinkt met de uitvoer.
- [ ] ARCH-60 (middel) Geef elk verzoek een correlatie-id en neem het overal mee. Afgevinkt met de testuitvoer.
- [ ] ARCH-62 (hoog) Log alleen benoemde velden en scan de testlogs in de gate. Afgevinkt met de uitvoer.
- [ ] ARCH-63 (middel) Log ook mislukte validatie, limieten, onverwachte fouten en starten en stoppen. Afgevinkt met de testuitvoer.
- [ ] ARCH-64 (hoog) Schrijf de auditregel in dezelfde transactie als de handeling. [bron niet gelezen: NEN] Afgevinkt met de drie uitvoeren.
- [ ] ARCH-67 (hoog) Maak twee health-adressen: leeft het proces, en kan het werken. Afgevinkt met de vier waarnemingen.
- [ ] ARCH-69 (hoog) Alarmeer op symptomen, met een drempel en een actie. Afgevinkt met de tabel en de proefmeldingen.
- [ ] ARCH-71 (middel) Deel logs in drie soorten in en geef elke soort een eigen termijn. [bron niet gelezen: NEN] Afgevinkt met inventaris en meting.
- [ ] ARCH-76 (hoog) Geef elke risicovolle functie een schakelaar die zonder uitrol werkt. Afgevinkt met de testuitvoer.
- [ ] ARCH-77 (hoog) Houd schakelaars veilig, uniek en tijdelijk. Afgevinkt met lijst en tests.

### dicht-scripts
Alleen als het project een script, een geplande taak of een lus bevat die in cron, een timer, een uitrol of een andere sessie draait; anders het hele blok `nvt` met die reden.
- [ ] SCR-01 (hoog) Begin elk Bash-script met de strikte modus. Afgevinkt met de uitvoer.
- [ ] SCR-02 (hoog) Reken niet op `set -e` binnen een voorwaarde, een functie in een voorwaarde of een `&&`-keten. Afgevinkt met de testuitvoer.
- [ ] SCR-03 (middel) Declareer en wijs apart toe, zodat een mislukte opdracht niet wordt gemaskeerd. Afgevinkt met de uitvoer.
- [ ] SCR-04 (middel) Ruim op met een EXIT-trap en meld de regel bij een fout. Afgevinkt met beide uitvoeren.
- [ ] SCR-05 (middel) Laat `set -x` uit in alles wat een geheim aanraakt. Afgevinkt met de uitvoer.
- [ ] SCR-06 (hoog) Zet elke expansie tussen dubbele aanhalingstekens en bouw argumentlijsten als array. Afgevinkt met de uitvoer.
- [ ] SCR-07 (kritiek) Geen `eval` en geen `bash -c` met een waarde van buiten. Afgevinkt met de uitvoer.
- [ ] SCR-08 (hoog) Zet `--` voor elk argument van buiten en `./` voor elk patroon. Afgevinkt met de uitvoer.
- [ ] SCR-09 (middel) Verwerk bestandsnamen met een NUL-scheiding, nooit door `ls` te lezen. Afgevinkt met beide uitvoeren.
- [ ] SCR-11 (hoog) Geef waarden aan psql door als variabele, nooit in de tekst van de query. Afgevinkt met de uitvoer.
- [ ] SCR-12 (middel) Zet het eindwoord van een here-document tussen aanhalingstekens als de inhoud data is. Afgevinkt met de uitvoer.
- [ ] SCR-13 (middel) Een env-bestand dat je met `.` inleest is code. Afgevinkt met de uitvoer.
- [ ] SCR-14 (hoog) Maak tijdelijke bestanden met mktemp en ruim ze op met een trap. Afgevinkt met de uitvoer.
- [ ] SCR-15 (kritiek) Bewaak elk pad dat je recursief verwijdert of overschrijft. Afgevinkt met de drie uitvoeren.
- [ ] SCR-16 (middel) Zet umask 077 in elk script dat geheimen, persoonsgegevens of logs schrijft. Afgevinkt met beide uitvoeren.
- [ ] SCR-18 (middel) Neem een slot op een eigen slotbestand buiten `/tmp`, met een eigen exitcode voor "draait al". Afgevinkt met de uitvoer van beide.
- [ ] SCR-19 (hoog) Geef een geheim door via een bestand of standaardinvoer, nooit als argument. Afgevinkt met beide uitvoeren.
- [ ] SCR-20 (middel) Zet een geheim alleen in de omgeving van het ene proces dat het nodig heeft. Afgevinkt met de lijst en de uitvoer.
- [ ] SCR-21 (hoog) Geef elke `curl` in een script `--fail`, een time-out en alleen HTTPS. Afgevinkt met de uitvoer.
- [ ] SCR-22 (hoog) Voer nooit iets uit dat je in dezelfde regel ophaalt. Afgevinkt met de uitvoer.
- [ ] SCR-23 (middel) Maak shellcheck en een syntaxcontrole een gate voor elk shellscript. Afgevinkt met de drie uitvoeren.
- [ ] SCR-24 (kritiek) Start processen vanuit Python met een lijst en zonder shell. Afgevinkt met beide uitvoeren.
- [ ] SCR-25 (hoog) Geef elke subprocess-aanroep een time-out en controleer de exitcode. Afgevinkt met beide uitvoeren.
- [ ] SCR-26 (hoog) Geef elke HTTP-aanroep in Python een time-out en laat de certificaatcontrole aan. Afgevinkt met de uitvoer.
- [ ] SCR-27 (kritiek) Laad nooit pickle, shelve of marshal uit een bron die een ander kan schrijven. Afgevinkt met de uitvoer.
- [ ] SCR-28 (kritiek) Lees YAML met `yaml.safe_load`. Afgevinkt met de drie uitvoeren.
- [ ] SCR-29 (hoog) Pak een archief alleen uit met een filter en een grens. Afgevinkt met de drie uitvoeren.
- [ ] SCR-30 (kritiek) Geef waarden aan SQL door als parameter, nooit met een f-string. Afgevinkt met de uitvoer.
- [ ] SCR-31 (middel) Maak tijdelijke bestanden in Python met het tempfile-pakket. Afgevinkt met de uitvoer.
- [ ] SCR-32 (hoog) Draai elk Python-script in een eigen virtuele omgeving met vastgezette afhankelijkheden en hashes. Afgevinkt met de drie uitvoeren.
- [ ] SCR-33 (hoog) Draai scripts op een Python-versie die nog beveiligingsupdates krijgt. Afgevinkt met de uitvoer en de notitie.
- [ ] SCR-34 (middel) Houd asyncio-taken vast, blokkeer de lus niet en begrens elk wachten. Afgevinkt met beide uitvoeren.
- [ ] SCR-35 (middel) Maak een beveiligingslint een gate voor Python-scripts. Afgevinkt met de drie uitvoeren.
- [ ] SCR-37 (middel) Zet de omgeving die een cron-taak nodig heeft in het script zelf. Afgevinkt met de uitvoer van de proefrun.
- [ ] SCR-38 (hoog) Geef elke geplande run een harde time-out. Afgevinkt met de drie uitvoeren.
- [ ] SCR-40 (middel) Plan niets tussen 02:00 en 03:00 en reken in het script met een vaste tijdzone. Afgevinkt met de uitvoer.
- [ ] SCR-42 (middel) Draai een lus die moet blijven lopen onder een procesbeheerder met een trage herstart en een alarm. Afgevinkt met de drie uitvoeren.
- [ ] SCR-43 (middel) Laat een lus bij een fout trager gaan, nooit sneller. Afgevinkt met de testuitvoer.
- [ ] SCR-44 (hoog) Laat een taak die zichzelf opnieuw inplant eerst controleren of er al een exemplaar loopt. [eigen bron] Afgevinkt met de testuitvoer.
- [ ] SCR-47 (kritiek) Laat een leeg, mislukt of genegeerd filter nooit "alles" betekenen. [eigen bron] Afgevinkt met script en testuitvoer.
- [ ] SCR-53 (hoog) Stop een proces op proces-id of poort, nooit op een breed patroon. (1) `grep -rnE '\b(pkill|killall)\b' --include='*.sh' --include='*.py' .` geeft alleen regels met een pidbestand (`-F`), een ouder (`-P`) of een patroon met het volledige
- [ ] SCR-48 (middel) Stuur tekst naar een tmux-venster als letterlijke tekst en de Enter apart. Afgevinkt met beide uitvoeren.
- [ ] SCR-49 (hoog) Typ pas als het scherm in de verwachte toestand staat, en stop bij elk onbekend scherm. [eigen bron] Afgevinkt met de testuitvoer.
- [ ] SCR-50 (hoog) Geef een prompt met gegevens door via standaardinvoer of een bestand, nooit als argument. Afgevinkt met de drie uitvoeren.
- [ ] SCR-51 (hoog) Wie bij de tmux-socket of de lokale aansturing kan, bestuurt de agent. Afgevinkt met de drie controles.

### dicht-invoer
- [ ] INV-03 (hoog) Zet in fast-xml-parser entiteiten uit voor XML van buiten en blijf op een gerepareerde versie. Afgevinkt met de drie uitvoeren.
- [ ] INV-04 (hoog) Behandel elk formaat met XML erin als XML. Afgevinkt met de lijst en de testuitvoer.
- [ ] INV-08 (hoog) Parse JSON één keer en geef het geparste object door. Afgevinkt met grep en test.
- [ ] INV-09 (hoog) Stuur gehele getallen buiten het veilige bereik als tekst. Afgevinkt met grep en test.
- [ ] INV-10 (middel) Begrens de diepte van geneste invoer vóór eigen recursie. Afgevinkt met de test.
- [ ] INV-12 (middel) Gebruik geen z.coerce op invoer zonder eerst de vorm te controleren. Afgevinkt met grep en test.
- [ ] INV-15 (hoog) Geef elk content-type dat een route aanneemt een eigen schema. Afgevinkt met de drie uitvoeren.
- [ ] INV-16 (hoog) Lees YAML alleen met een veilige lader zonder eigen types. Afgevinkt met beide uitvoeren.
- [ ] INV-17 (middel) Begrens aliassen en samenvoegingen in YAML van buiten. Afgevinkt met grep en test.
- [ ] INV-20 (middel) Lees een CSV-import strikt: UTF-8, vast scheidingsteken, limieten en een schema per rij. Afgevinkt met de testuitvoer.
- [ ] INV-21 (hoog) Gebruik het pakket xlsx niet vanaf npm. Afgevinkt met de uitvoer.
- [ ] INV-22 (hoog) Saneer als laatste stap en verander de uitvoer daarna niet meer. Afgevinkt met grep en test.
- [ ] INV-23 (hoog) Draai DOMPurify op de server alleen met een actuele jsdom. Afgevinkt met de uitvoer.
- [ ] INV-24 (hoog) Reken niet op de Markdown-renderer voor veiligheid. Afgevinkt met grep en test.
- [ ] INV-28 (hoog) Laat de grenzen van sharp staan en zet een tijdslimiet. Afgevinkt met grep, versie en test.
- [ ] INV-32 (hoog) Zet SVG van anderen niet op de server om naar een rasterbeeld zonder afscherming. Afgevinkt met de testuitvoer, of met de vaststelling dat SVG-invoer wordt geweigerd.
- [ ] INV-33 (hoog) Behandel magic bytes als een hint en parse het bestand volledig. Afgevinkt met de testuitvoer.
- [ ] INV-35 (kritiek) Behandel HTML voor een PDF als code die in een browser op de server draait. Afgevinkt met test en grep.
- [ ] INV-36 (hoog) Start Chrome nooit met --no-sandbox. Afgevinkt met de drie uitvoeren.
- [ ] INV-37 (hoog) Gebruik wkhtmltopdf niet meer. Afgevinkt met beide uitvoeren.
- [ ] INV-39 (hoog) Lees PDF's met pdf.js alleen vanaf 4.2.67 en met isEvalSupported uit. Afgevinkt met de drie uitvoeren.
- [ ] INV-41 (kritiek) Controleer elke naam in een archief voordat er een byte wordt geschreven. Afgevinkt met test, grep en versies.
- [ ] INV-42 (hoog) Weiger symlinks en hardlinks in een archief. Afgevinkt met de testuitvoer.
- [ ] INV-44 (middel) Begrens gedecomprimeerde omvang van aanvragen en antwoorden. Afgevinkt met grep en test.
- [ ] INV-48 (middel) Weiger regeleinden en tekens buiten ASCII voordat een waarde in een antwoordkop komt. Afgevinkt met de uitvoer.
- [ ] INV-49 (hoog) Bouw uitgaande aanvragen met URL-objecten en vaste kopwaarden. Afgevinkt met grep en test.
- [ ] INV-51 (hoog) Maak identifiers canoniek met één functie die bij herhaling niets meer verandert. Afgevinkt met grep, index en tests.
- [ ] INV-52 (middel) Vergelijk hoofdletterongevoelig via kleine letters, nooit via hoofdletters of de taalinstelling. Afgevinkt met grep en test.
- [ ] INV-53 (hoog) Sla domeinnamen op en vergelijk ze als A-label. Afgevinkt met query en test.
- [ ] INV-55 (hoog) Laat de build falen op bidi-stuurtekens in broncode. Afgevinkt met de uitvoer van een run met en zonder testbestand.
- [ ] INV-56 (middel) Weiger stuurtekens in velden van één regel. Afgevinkt met de test.
- [ ] INV-57 (middel) Weiger het NUL-teken en ongeldige Unicode aan de rand. Afgevinkt met de test.
- [ ] INV-58 (middel) Meet lengte in de eenheid van de opslag en kap nooit stil af. Afgevinkt met test, grep en de query.
- [ ] INV-59 (hoog) Ontleed een URL met één WHATWG-parser en gebruik daarna het ontlede object. Afgevinkt met grep en test.
- [ ] INV-61 (hoog) Controleer IP-adressen met de standaardbibliotheek, niet met het pakket ip. Afgevinkt met grep, `npm ls` en test.
- [ ] INV-62 (middel) Laat proxy en applicatie een pad op dezelfde manier lezen. Afgevinkt met grep en de curl-uitvoer.
- [ ] INV-63 (laag) Ontdoe zoektekst van LIKE-jokertekens. Afgevinkt met grep en test.
- [ ] INV-64 (hoog) Accepteer e-mailadressen alleen in de eenvoudige vorm en beslis niets op het domein van een onbevestigd adres. Afgevinkt met test en grep.
- [ ] INV-65 (hoog) Zet bij multipart elke limiet zelf, lees elke stream uit en weiger een afgekapt bestand. Afgevinkt met versie, grep en tests.
- [ ] INV-66 (hoog) Geef busboy alle limieten mee, want de standaard is onbegrensd. Afgevinkt met grep en test.
- [ ] INV-68 (middel) Maak tijdelijke bestanden in een eigen, verse map met een onvoorspelbare naam. Afgevinkt met de vier uitvoeren.

### dicht-berichten
- [ ] MSG-04 (middel) Bouw elk bericht met een bibliotheek, met één Message-ID, één Date en één From. Afgevinkt met de testuitvoer en de telling.
- [ ] MSG-05 (hoog) Controleer het certificaat op elke SMTP- en IMAP-verbinding. Afgevinkt met grep en de testuitvoer.
- [ ] MSG-06 (hoog) Houd de mailbibliotheek binnen de hersteltermijnen, juist bij meerdere tenants. Afgevinkt met de uitvoer en de datum.
- [ ] MSG-17 (hoog) Codeer elke variabele in een HTML-mailsjabloon. Afgevinkt met de testuitvoer.
- [ ] MSG-18 (hoog) Beslis op het adres dat de parser teruggeeft, met één parser voor de hele keten. Afgevinkt met de testuitvoer.
- [ ] MSG-22 (kritiek) Vertrouw From niet: beslis op het oordeel van je eigen ontvangende server. Afgevinkt met de testuitvoer.
- [ ] MSG-23 (kritiek) Toon HTML-mail alleen opgeschoond, in een sandbox zonder scripts en zonder verzoeken naar buiten. Afgevinkt met de testuitvoer en grep.
- [ ] MSG-24 (hoog) Begrens wat de parser van één bericht mag kosten. Afgevinkt met de testuitvoer.
- [ ] MSG-25 (hoog) Behandel een bijlage als een upload van een onbekende en pak niets automatisch uit. Afgevinkt met de testuitvoer en grep.
- [ ] MSG-26 (hoog) Zet geen invoer met een regeleinde in een IMAP- of SMTP-opdracht. Afgevinkt met de testuitvoer en grep.
- [ ] MSG-27 (hoog) Een mailserver die de gebruiker opgeeft, is een uitgaand verzoek naar een onbekend adres. Afgevinkt met de testuitvoer.
- [ ] MSG-28 (hoog) Koppel mailboxen van klanten met OAuth waar de aanbieder dat eist, en bewaar een wachtwoord versleuteld en zo kort mogelijk. Afgevinkt met de query en de configuratie.
- [ ] MSG-30 (middel) Vernieuw IDLE binnen 29 minuten en haal na elke herverbinding in wat is gemist. Afgevinkt met de testuitvoer en de health-check.
- [ ] MSG-31 (hoog) Antwoord nooit automatisch op een automatisch bericht. Afgevinkt met de testuitvoer.
- [ ] MSG-32 (middel) Markeer elk automatisch verstuurd bericht. Afgevinkt met de koppen per stroom.
- [ ] MSG-35 (middel) Beantwoord het verificatieverzoek alleen bij het juiste token. [bron niet gelezen: META] Afgevinkt met de uitvoer.
- [ ] MSG-36 (kritiek) Controleer X-Hub-Signature-256 over de ruwe body met het app-geheim. [bron niet gelezen: META] Afgevinkt met de testuitvoer.
- [ ] MSG-37 (hoog) Ontdubbel op het bericht-ID; Meta biedt een melding tot 36 uur opnieuw aan. [bron niet gelezen: META] Afgevinkt met de testuitvoer.
- [ ] MSG-39 (kritiek) Controleer bij Discord-interacties de Ed25519-handtekening en antwoord anders met 401. Afgevinkt met de uitvoer.
- [ ] MSG-40 (middel) Zet bij elk bericht met inhoud van buiten uit wie er genoemd mag worden. Afgevinkt met de testuitvoer en grep.
- [ ] MSG-41 (hoog) Behandel een webhookadres en een bot-token als geheim. Afgevinkt met de uitvoer en het overzicht.
- [ ] MSG-42 (middel) Volg 429 en Retry-After, en blijf onder de grens voor ongeldige verzoeken. Afgevinkt met de testuitvoer.
- [ ] MSG-43 (kritiek) Controleer bij Slack de handtekening en weiger een verzoek ouder dan vijf minuten. Afgevinkt met de testuitvoer en grep.
- [ ] MSG-44 (middel) Antwoord Slack binnen drie seconden en ontdubbel op event_id. Afgevinkt met de testuitvoer.
- [ ] MSG-48 (middel) Zet geen gevoelige inhoud in een melding. Afgevinkt met de voorbeelden.

## Bouwen: richtlijnen (82)

### dicht-api
- [ ] AUTH-11 (middel) Voorkom dat een aanvaller accounts kan blokkeren. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-43 (hoog) Zet geen rechten in een langlevend token. Afgevinkt als de test groen is.
- [ ] AUTH-68 (middel) Onvoorspelbare id's zijn een extra laag, geen autorisatie. Afgevinkt als de lijst met zulke links gedocumenteerd is.
- [ ] AUTH-78 (laag) Laat foutmeldingen en unieke sleutels niets over andere tenants verraden. Afgevinkt als dat voor elke tabel met `tenant_id` geldt.
- [ ] API-08 (middel) Eén bron voor type en validatie. `grep -rnE "as [A-Z][A-Za-z]+(\[\])?[;,)]" src` op regels met `req.` of `JSON.parse` is leeg. Elk request-type is een `z.infer`.
- [ ] API-11 (laag) Eén foutformaat met stabiele codes. Een contracttest loopt alle foutpaden af en controleert het schema van het foutantwoord en de afwezigheid van `stack`, `sql`, `/home/`, `node_modules`.
- [ ] API-22 (laag) Antwoord op een overschreden limiet met 429 en Retry-After. Test: het 429-antwoord bevat `retry-after`.
- [ ] API-71 (middel) Koppel streams met `pipeline`. `grep -rn "\.pipe(" src` is leeg of onderbouwd. Test: een afgebroken upload laat geen tijdelijk bestand achter.

### dicht-database
- [ ] DB-08 (middel) Zet search_path vast per rol. Afgevinkt als elke loginrol een expliciet `search_path` heeft en DB-04 is afgevinkt.
- [ ] DB-10 (laag) Begrens elke rol met een verbindingslimiet. Afgevinkt als geen applicatierol `-1` heeft en de som onder `max_connections` blijft.
- [ ] DB-28 (hoog) Geen dynamische SQL in databasefuncties. Afgevinkt als de lijst leeg is of elke treffer is beoordeeld.
- [ ] DB-35 (middel) Zet NOT NULL op een gevulde kolom via een gevalideerde CHECK. Afgevinkt als de `SET NOT NULL`-stap op de kopie binnen de `lock_timeout` blijft.
- [ ] DB-37 (middel) Voeg een unieke of primaire sleutel toe via een vooraf gebouwde index. Afgevinkt als beide stappen apart staan.
- [ ] DB-71 (middel) Wachtrijtabellen lezen met FOR UPDATE SKIP LOCKED. Afgevinkt als die test bestaat voor elke tabel die als wachtrij dient.
- [ ] DB-72 (laag) Neem locks in een vaste volgorde. Afgevinkt als het serverlog over 30 dagen geen "deadlock detected" bevat of elke melding is verklaard.
- [ ] DB-76 (middel) Kies sleutels bewust: wat naar buiten gaat is niet raadbaar en verraadt niets. Afgevinkt als externe id's UUID versie 4 zijn of de afwijking is toegelicht, en de autorisatietest uit domein AUTH bestaat.
- [ ] DB-77 (laag) Volg voor types en namen de skill postgresql-table-design. Afgevinkt als nieuwe tabellen de conventies volgen.
- [ ] DB-82 (middel) Weet wat schijfversleuteling wel en niet doet. Afgevinkt als de documentatie klopt met de werkelijkheid en met de teksten richting klanten.

### dicht-infra
- [ ] INFRA-04 (middel) Beperk wie mag inloggen. Afgevinkt met beide uitvoeren.
- [ ] INFRA-05 (middel) Zet doorsturen uit dat je niet gebruikt. Afgevinkt met de uitvoer.
- [ ] INFRA-09 (middel) Hergebruik één SSH-verbinding bij geautomatiseerd werk. Afgevinkt met het script of de opdrachttekst.
- [ ] INFRA-15 (middel) Zet een tweede firewall buiten de host. Afgevinkt als beide lijsten gelijk zijn.
- [ ] INFRA-18 (middel) Beperk uitgaand verkeer van containers die adressen van buiten ophalen. Afgevinkt met document en proef.
- [ ] INFRA-19 (laag) Leg de kernelinstellingen voor het netwerk vast. [bron niet gelezen: CIS] Afgevinkt met de uitvoer.
- [ ] INFRA-30 (middel) Maak het bestandssysteem van de container alleen-lezen. Afgevinkt met beide uitvoeren.
- [ ] INFRA-35 (middel) Geef elke service een healthcheck en een herstartbeleid. Afgevinkt met de uitvoer.
- [ ] INFRA-37 (middel) Bouw kleine images zonder bouwgereedschap. Afgevinkt met de uitvoer.
- [ ] INFRA-39 (middel) Koppel mappen, geen losse bestanden, en koppel alleen-lezen waar het kan. Afgevinkt met de uitvoer.
- [ ] INFRA-41 (laag) Overweeg gebruikersnaamruimten voor diensten met een hoog risico. Afgevinkt met uitvoer of notitie.
- [ ] INFRA-53 (middel) Leg met CAA vast wie certificaten mag uitgeven. Afgevinkt met de uitvoer en een geslaagde vernieuwing daarna.
- [ ] INFRA-68 (laag) Geef een dienst een herstartbeleid en een geheugenlimiet. Afgevinkt met de uitvoer.
- [ ] INFRA-71 (laag) Synchroniseer de klok en wees expliciet over de tijdzone. Afgevinkt met de uitvoer.

### dicht-git
- [ ] GIT-08 (laag) Ruim worktrees en branches op zodra het werk gemerged is. Afgevinkt met beide uitvoeren.
- [ ] GIT-13 (middel) Laat elke wijziging lezen voordat hij live gaat. Afgevinkt met die notitie.
- [ ] GIT-35 (middel) Geef eigen sleutels een herkenbaar voorvoegsel en een eigen scanregel. Afgevinkt met de uitvoer.
- [ ] GIT-37 (middel) Herschrijf de geschiedenis alleen als intrekken niet genoeg is. Afgevinkt met de vier.
- [ ] GIT-42 (hoog) Gebruik zo min mogelijk acties van derden en kijk wat ze zelf aanroepen. Afgevinkt met die lijst.
- [ ] GIT-49 (hoog) Geef CI geen sleutel tot productie. Afgevinkt met de uitvoer.
- [ ] GIT-50 (middel) Publiceer met kortlevende identiteit in plaats van een token. Afgevinkt met beide.
- [ ] GIT-55 (middel) Laat een bot niet zelf mergen zonder de gate en de wachttijd. Afgevinkt met de instelling en de regel.
- [ ] GIT-66 (middel) Controleer Dockerfiles en Compose-bestanden statisch. [bron niet gelezen: CIS] Afgevinkt met beide.
- [ ] GIT-74 (middel) Gebruik een pakketbeheerder met veilige standaarden. Afgevinkt met beide.
- [ ] GIT-79 (middel) Geef interne pakketten een scope en een vaste registry. Afgevinkt met beide.
- [ ] GIT-94 (middel) Kies een basisimage van een bekende uitgever en zo klein als werkt. [bron niet gelezen: CIS] Afgevinkt met de lijst.
- [ ] GIT-98 (laag) Bouw met herkomstgegevens en een SBOM waar de image naar een register gaat. Afgevinkt met de uitvoer.
- [ ] GIT-99 (laag) Reken niet op Docker Content Trust. [bron niet gelezen: CIS] Afgevinkt met beide waar van toepassing.
- [ ] GIT-100 (middel) Houd het register en de toegang ertoe klein. Afgevinkt met de uitvoer.
- [ ] GIT-103 (laag) Leg herkomst vast met wat het plan toelaat. Afgevinkt met uitvoer of document.

### dicht-ai-mcp
- [ ] AI-05 (middel) Zet het beleid in de systeemprompt, maar bouw er niets op. Afgevinkt met de lijst van verbodszin naar controle.
- [ ] AI-09 (middel) Een injectiefilter of bewakingsmodel is een extra laag, geen grens. Afgevinkt als beide aantoonbaar zijn.
- [ ] AI-16 (middel) Haal stuurtekens uit modeluitvoer voor terminal en logs. Afgevinkt met de testuitvoer.
- [ ] AI-20 (hoog) Bouw specifieke tools in plaats van open tools. Afgevinkt met de lijst.
- [ ] AI-27 (hoog) Een agent die commando's of code uitvoert, draait in een afgeschermde omgeving. [bron niet gelezen: AGENTIC] Voor elke agent die commando's uitvoert, is vastgelegd welke isolatie geldt (sandbox aan, container, aparte gebruiker) en welke mappen en hosts bereikbaar zijn.
- [ ] AI-29 (middel) Scheid lezen, klaarzetten en uitvoeren in aparte toolsets en scopes. [bron niet gelezen: AGENTIC] Afgevinkt met de testuitvoer.
- [ ] AI-30 (middel) Een keten van agents geeft geen rechten en geen vertrouwen door. [bron niet gelezen: AGENTIC] Afgevinkt met de testuitvoer.
- [ ] AI-43 (middel) Toolnamen en toolbeschrijvingen zijn publiek, eerlijk en zonder verborgen sturing. Afgevinkt met de opgeslagen lijst.
- [ ] AI-50 (laag) Vul tool-annotaties eerlijk in en bouw er geen beveiliging op. Afgevinkt met de tabel.
- [ ] AI-51 (middel) Minimale scopes, stapsgewijs verhoogd, zonder jokers. Afgevinkt met de curl-uitvoer.
- [ ] AI-54 (middel) Blijf op een ondersteunde protocolrevisie en bouw geen afgeraden onderdelen. Afgevinkt met de drie uitvoeren.
- [ ] AI-58 (hoog) Lees de toolbeschrijvingen en merk het op als ze veranderen. [bron niet gelezen: AGENTIC] Afgevinkt met het opgeslagen bestand en de hash.

### dicht-privacy
- [ ] PRIV-75 (middel) Maak bij elke release een SBOM en bewaar de risicobeoordeling. Afgevinkt met beide.
- [ ] PRIV-81 (middel) Markeer gegenereerde tekst, beeld, audio en video machineleesbaar als je aanbieder bent. [bron niet gelezen: AI-VO] Afgevinkt met de testuitvoer.

### dicht-architectuur
- [ ] ARCH-11 (middel) Zet beheertaken in de repository en draai ze tegen dezelfde release. Afgevinkt met commit en uitvoer.
- [ ] ARCH-20 (hoog) Leg de wijziging en de opdracht voor het externe effect vast in dezelfde transactie. Afgevinkt met codeverwijzing en test.
- [ ] ARCH-21 (middel) Zorg dat een plotselinge stop geen halve toestand achterlaat. Afgevinkt met het verslag van de proef.
- [ ] ARCH-39 (middel) Houd tests onafhankelijk en behandel een wankele test als een fout. Afgevinkt met de uitvoer.
- [ ] ARCH-41 (middel) Bewijs met een contracttest dat elke respons aan zijn schema voldoet. Afgevinkt met de testuitvoer en het aantal routes.
- [ ] ARCH-43 (middel) Fuzz elke parser van niet-vertrouwde invoer en de API als geheel. Afgevinkt met de uitvoeren en de datum.
- [ ] ARCH-45 (laag) Zet een dekkingsdrempel die niet mag dalen en lees hem niet als kwaliteit. Afgevinkt met configuratie en uitvoer.
- [ ] ARCH-59 (middel) Gebruik één vaste woordenlijst voor beveiligingsgebeurtenissen. Afgevinkt met de lijst.
- [ ] ARCH-61 (laag) Schrijf logs naar de standaarduitvoer en laat de omgeving ze opslaan. Afgevinkt met beide.
- [ ] ARCH-68 (middel) Meet per dienst vier signalen. Afgevinkt met de uitvoer.
- [ ] ARCH-70 (laag) Geef verzoeken over procesgrenzen een standaard spoorkop mee. Afgevinkt met de logregels.
- [ ] ARCH-78 (middel) Kondig een brekende wijziging van een API aan met Deprecation en Sunset. Afgevinkt met kopregels en telling.
- [ ] ARCH-79 (laag) Breid een API uit door toe te voegen, niet door te wijzigen. Afgevinkt met de uitvoer.

### dicht-scripts
Alleen als het project een script, een geplande taak of een lus bevat die in cron, een timer, een uitrol of een andere sessie draait; anders het hele blok `nvt` met die reden.
- [ ] SCR-36 (laag) Start een Python-script uit cron in geïsoleerde modus. Afgevinkt met de uitvoer.
- [ ] SCR-41 (laag) Kies voor een nieuwe geplande taak een systemd-timer boven cron. Afgevinkt met de uitvoer of de notitie.

### dicht-invoer
- [ ] INV-18 (middel) Valideer geparste YAML en TOML met een schema en reken niet op het geraden type. Afgevinkt met de test.
- [ ] INV-26 (middel) Beperk de sanitizer tot HTML als SVG en MathML niet nodig zijn. Afgevinkt met de grep.
- [ ] INV-40 (middel) Verwerk PDF's, Office-bestanden en beeld van buiten in een apart proces met grenzen. Afgevinkt met de test.
- [ ] INV-54 (middel) Weiger of markeer namen met gemengde schriftsoorten waar de naam vertrouwen draagt. Afgevinkt met de test, of met een vastgelegde reden waarom het voor dit project niet speelt.

### dicht-berichten
- [ ] MSG-45 (laag) Vraag bij Discord alleen de intents die de bot nodig heeft. Afgevinkt met de schermafdruk.

## Vóór oplevering: hard (27)

### dicht-api
- [ ] AUTH-77 (kritiek) Een isolatietest per tabel en per route, die vóór elke uitrol draait. Afgevinkt als beide in de pijplijn staan.
- [ ] BIZ-50 (hoog) Bewijs een race met echte gelijktijdigheid tegen een echte PostgreSQL. De testopzet gebruikt een pool van minstens 20 en geen omhullende transactie voor deze tests.
- [ ] BIZ-51 (middel) Leg per geldstroom de invarianten vast als query en draai ze in de test en dagelijks. Het bestand met invarianten staat in de repository naast het threat model (ARCH-82).
- [ ] BIZ-52 (middel) Test geld en tijd met een vaste tabel van grensgevallen. De tabel staat als geparametriseerde test in de repository (`it.each`).

### dicht-git
- [ ] GIT-63 (hoog) Scan elke image die je uitrolt. [bron niet gelezen: CIS] Afgevinkt met de uitvoer.

### dicht-ai-mcp
- [ ] AI-77 (middel) Zet het model vast op een exacte versie; een modelwissel is een release. Afgevinkt met de grep en de tabel.
- [ ] AI-78 (hoog) Een vaste eval is een gate bij elke wijziging van prompt, model, tools of leverancier. Afgevinkt met de laatste evaluitvoer.
- [ ] AI-79 (hoog) Elke AI-functie en elke agent is zonder deploy uit te zetten. Afgevinkt met de testuitvoer.
- [ ] AI-80 (hoog) Faal gesloten als het model uitvalt of iets onverwachts teruggeeft. Afgevinkt met de testuitvoer.
- [ ] AI-81 (hoog) Injectietests per invoerkanaal zijn een gate. Afgevinkt met de CI-uitvoer.
- [ ] AI-83 (middel) Bewaak verbruik, weigeringen en afwijkend toolgebruik, met een alarm. Afgevinkt met het overzicht en de ontvangen melding.
- [ ] AI-85 (hoog) Code die een model schreef, gaat door dezelfde gates, en elk voorgesteld pakket wordt gecontroleerd. Afgevinkt met de CI-uitvoer en de onderbouwing.
- [ ] AI-86 (hoog) Wat een agent op een klantsite of in een vreemde repository leest, is onvertrouwd. [bron niet gelezen: AGENTIC] Afgevinkt met de notitie bij de klus.

### dicht-architectuur
- [ ] ARCH-22 (hoog) Rol uit met één script dat alle stappen doet. Afgevinkt met script en bewijs.
- [ ] ARCH-23 (hoog) Controleer de gezondheid na de herstart en draai vanzelf terug. Afgevinkt met de uitvoer van beide proeven.
- [ ] ARCH-24 (hoog) Bewijs na elke uitrol dat wat draait gelijk is aan wat in git staat. Afgevinkt met de uitvoer in het bewijsbestand.
- [ ] ARCH-25 (hoog) Oefen het terugdraaien en houd migraties voorwaarts verenigbaar. Afgevinkt met runbook en verslag.
- [ ] ARCH-27 (hoog) Rol een wijziging die veel sites of tenants raakt in stappen uit. Afgevinkt met die lijst.
- [ ] ARCH-28 (kritiek) Geef elk script dat veel wijzigt of verwijdert een proefstand, exacte doelen en een grens. Afgevinkt met script en beide uitvoeren.
- [ ] ARCH-44 (hoog) Meet met mutatietests of de tests van kritieke modules iets bewijzen. Afgevinkt met configuratie en rapport.
- [ ] ARCH-52 (hoog) Een bouwtaak is klaar als de checklist van het projecttype is afgevinkt met bewijs. Afgevinkt als geen punt leeg is.
- [ ] ARCH-53 (middel) Schrijf het bewijs in één bestand met een vaste vorm. Afgevinkt met die vier controles.
- [ ] ARCH-54 (hoog) Laat elke wijziging aan een kritiek deel nakijken door een tweede paar ogen. Afgevinkt met de notitie.
- [ ] ARCH-55 (middel) Tel elke onderdrukking en geef haar een reden. Afgevinkt met configuratie en telling.
- [ ] ARCH-84 (middel) Bouw per projecttype één auditscript dat het bewijs verzamelt. Afgevinkt met de uitvoer van de proef.
- [ ] ARCH-85 (hoog) Laat een auditscript alleen lezen, begrensd en zonder geheimen in de uitvoer. [eigen bron] Afgevinkt met de drie controles.
- [ ] ARCH-86 (middel) Lever de audit van een bestaand project op als lijst van bevindingen, niet als herstel. Afgevinkt met rapport en status.

## Vóór oplevering: richtlijnen (5)

### dicht-ai-mcp
- [ ] AI-82 (middel) Beoordeel een AI-test op wat er gebeurde, en herhaal hem. Afgevinkt met de uitvoer.
- [ ] AI-84 (middel) Heb een draaiboek voor een AI-incident. Afgevinkt met het document en de oefennotitie.

### dicht-architectuur
- [ ] ARCH-26 (middel) Test de nieuwe versie als tweede exemplaar voordat je omschakelt. [eigen bron] Afgevinkt met beide.
- [ ] ARCH-87 (middel) Rol uit op een moment waarop je na een uur nog kunt nameten en terugdraaien. [eigen bron] Afgevinkt met beide tijdstippen.
- [ ] ARCH-73 (middel) Leg per dienst een prestatie- en beschikbaarheidsdoel vast en meet het. Afgevinkt met de drie onderdelen.

## Na oplevering en beheer: hard (50)

### dicht-api
- [ ] AUTH-02 (middel) Geen samenstellingsregels en geen verplichte periodieke wissel. [alleen: met login] Afgevinkt met de test uit AUTH-01 (wachtwoord van 15 kleine letters wordt geaccepteerd).
- [ ] AUTH-85 (hoog) Offboarding: toegang van mensen en systemen direct weg. Afgevinkt als de test groen is en de laatste controle minder dan een kwartaal oud is.

### dicht-database
- [ ] DB-44 (kritiek) Maak dagelijks een automatische back-up van elke database en van de globale objecten. [bron niet gelezen: NEN] Afgevinkt als elke database een bestand van minder dan 26 uur oud heeft en er een globals-bestand is.
- [ ] DB-45 (hoog) Versleutel elke back-up voordat hij op schijf staat. Afgevinkt als geen enkele back-up leesbaar is zonder sleutel.
- [ ] DB-46 (kritiek) Doe een herstelproef met datum, minstens elk kwartaal. [bron niet gelezen: NEN] Afgevinkt als de laatste regel per database jonger is dan 92 dagen en de tellingen kloppen.
- [ ] DB-47 (hoog) Een mislukte of ontbrekende back-up geeft alarm. Afgevinkt als een proef (back-up een dag overslaan in een testomgeving, of de controle draaien tegen een lege map) een melding geeft.
- [ ] DB-48 (hoog) Dump met een pg_dump van dezelfde major als de server. Afgevinkt als dat zo is.
- [ ] DB-49 (hoog) Bewaar een versleutelde kopie buiten de server. Afgevinkt als beide kloppen.
- [ ] DB-53 (hoog) Elke database heeft een herstelplan met RPO en RTO. [bron niet gelezen: NEN] Afgevinkt als alle vier waar zijn.
- [ ] DB-55 (middel) Neem configuratie en geheimen mee in het herstel. Afgevinkt als dat lukt zonder iets van de oude server te kopiëren.
- [ ] DB-57 (middel) Back-ups hebben zelf een bewaartermijn. Afgevinkt als de oudste aanwezige back-up niet ouder is dan de vastgelegde termijn en het runbook beschrijft dat verwijderverzoeken na een herstel opnieuw worden toegepast (DB-84).
- [ ] DB-89 (middel) Zet pg_stat_statements aan. Afgevinkt als beide kloppen.
- [ ] DB-92 (hoog) Draai de actuele minor van je major. Afgevinkt als de minor gelijk is aan de actuele.
- [ ] DB-93 (middel) Blijf op een ondersteunde major en plan de upgrade een jaar vooruit. Afgevinkt als geen productiedatabase binnen 12 maanden van zijn einddatum zit zonder upgradeplan.
- [ ] DB-94 (middel) Laat autovacuum aan en bewaak wat hem tegenhoudt. Afgevinkt als alle vier kloppen en in de monitoring zitten (DB-97).
- [ ] DB-95 (middel) Indexeer foreign keys en lees het plan van elke nieuwe zware query. Afgevinkt als beide kloppen.
- [ ] DB-96 (middel) Houd extensies op een allowlist. Afgevinkt als ze gelijk zijn.
- [ ] DB-97 (hoog) Bewaak de database en alarmeer op vijf signalen. Afgevinkt als de proeven zijn gedaan en gedateerd.
- [ ] DB-98 (middel) Database in Docker: versie vastzetten, app-rol via initialisatie, gegevens op een volume. Afgevinkt als dat zo is.

### dicht-infra
- [ ] INFRA-20 (hoog) Laat beveiligingsupdates van het besturingssysteem automatisch installeren. Afgevinkt met de drie uitvoeren.
- [ ] INFRA-21 (hoog) Herstart binnen een week na een update die erom vraagt. Afgevinkt met de uitvoer.
- [ ] INFRA-22 (hoog) Draai een besturingssysteem dat nog beveiligingsupdates krijgt. Afgevinkt als de einddatum meer dan drie maanden weg is of de upgrade is ingepland met datum.
- [ ] INFRA-23 (hoog) Geef software van buiten de distributie een eigen updateroute. Afgevinkt met de uitvoer en de datum van de laatste ronde.
- [ ] INFRA-24 (hoog) Volg de advisories van wat je draait en leg termijnen vast. Afgevinkt met de lijst en de termijnen.
- [ ] INFRA-52 (hoog) Bewaak de vervaldatum van buitenaf. Afgevinkt met schermafdruk of uitvoer en de testmelding.
- [ ] INFRA-75 (hoog) Oefen het vervangen van een geheim voordat het nodig is. Afgevinkt met de lijst.
- [ ] INFRA-79 (kritiek) Bewaar drie kopieën op twee soorten opslag, waarvan één buiten de server. Afgevinkt als elke dataset een kopie buiten de server heeft die jonger is dan het afgesproken verlies (INFRA-84).
- [ ] INFRA-81 (hoog) Maak de externe kopie onwisbaar vanaf de server. Afgevinkt met de uitvoer van de proef.
- [ ] INFRA-82 (kritiek) Doe elk kwartaal een herstelproef op een lege machine. Afgevinkt als het verslag jonger is dan drie maanden.
- [ ] INFRA-83 (hoog) Neem de configuratie van de server mee in de back-up. Afgevinkt met de lijst en de diffs.
- [ ] INFRA-84 (middel) Leg per dienst vast hoeveel verlies en uitval aanvaardbaar is. [bron niet gelezen: WET] Afgevinkt met de tabel.
- [ ] INFRA-86 (hoog) Bewaak de bereikbaarheid vanaf een plek buiten de server. Afgevinkt met de lijst en de proefmelding.
- [ ] INFRA-87 (hoog) Sla alarm op schijf, geheugen, herstarts, certificaten, back-ups en geplande taken. Afgevinkt met de tabel en de testmeldingen.
- [ ] INFRA-88 (middel) Roteer logs, geef ze een bewaartermijn en houd geheimen en persoonsgegevens eruit. [bron niet gelezen: NEN] Afgevinkt met het overzicht en de steekproef.
- [ ] INFRA-89 (middel) Bescherm logs tegen wijzigen en bewaar een kopie buiten de server. Afgevinkt met de rechten en deze drie controles.
- [ ] INFRA-91 (hoog) Schrijf het draaiboek voordat er iets gebeurt. Afgevinkt met het document en de datum.
- [ ] INFRA-92 (hoog) Isoleer eerst en bewaar bewijs voordat je opruimt. Afgevinkt met het verslag.
- [ ] INFRA-93 (kritiek) Vervang na een inbraak elk geheim dat de getroffen omgeving kon lezen. Afgevinkt met de lijst.
- [ ] INFRA-94 (hoog) Herbouw vanaf een schone bron; ruim alleen op met volledige controle. Afgevinkt met het verslag.
- [ ] INFRA-96 (kritiek) Beoordeel bij elk incident met persoonsgegevens direct de meldplicht. [bron niet gelezen: WET] Afgevinkt met het verslag.

### dicht-git
- [ ] GIT-09 (hoog) Elke repo met waarde heeft een kopie buiten de server. Afgevinkt met uitvoer en datum.
- [ ] GIT-76 (middel) Laat Dependabot versies bijwerken, gegroepeerd en met wachttijd. Afgevinkt met bestand en uitvoer.
- [ ] GIT-92 (hoog) Laat een bot de digests bijwerken en bouw wekelijks opnieuw. [bron niet gelezen: CIS] Afgevinkt met beide.

### dicht-ai-mcp
- [ ] AI-70 (middel) Embeddings en afgeleide gegevens verdwijnen samen met de bron. Afgevinkt met de testuitvoer.

### dicht-privacy
- [ ] PRIV-26 (hoog) Een inzageverzoek is binnen een maand te beantwoorden met een getest script. Afgevinkt met de testuitvoer.
- [ ] PRIV-31 (kritiek) Meld een datalek binnen 72 uur na kennisname, ook als het onderzoek nog loopt. Afgevinkt als het document bestaat en één keer is doorgelopen met een oefengeval.
- [ ] PRIV-33 (hoog) Registreer elk datalek, ook als je het niet meldt. Afgevinkt als het bestand bestaat (ook als het leeg is) en in het draaiboek genoemd wordt.
- [ ] PRIV-34 (hoog) Zorg dat je kunt vaststellen of er toegang is geweest. Afgevinkt met overzicht en proef.
- [ ] PRIV-35 (hoog) Informeer betrokkenen bij een hoog risico, en weet wanneer versleuteling dat voorkomt. Afgevinkt met beide.

### dicht-invoer
- [ ] INV-69 (middel) Ruim tijdelijke bestanden op bij elke afloop en begrens de ruimte. Afgevinkt met de testuitvoer en de configuratie.

## Na oplevering en beheer: richtlijnen (8)

### dicht-database
- [ ] DB-50 (middel) Gebruik het custom-formaat en herstel met stop-bij-fout. Afgevinkt als de proef zonder fouten eindigt.
- [ ] DB-56 (middel) Zet data-checksums aan bij een nieuw cluster. Afgevinkt als dat zo is voor nieuwe clusters; voor bestaande clusters is het een verbeterpunt bij de volgende major upgrade.
- [ ] DB-90 (middel) Log trage queries, lock-wachttijden en verbindingen. Afgevinkt als ze zijn ingesteld en het log binnen de bewaartermijn van INFRA valt.
- [ ] DB-91 (middel) Audit van DDL en rolwijzigingen; volledige audit bij zorgdata. [bron niet gelezen: NEN] Afgevinkt als de proef slaagt.

### dicht-infra
- [ ] INFRA-25 (middel) Haal weg wat niet nodig is. Afgevinkt met de vergelijking.
- [ ] INFRA-90 (laag) Bekijk inlogpogingen en rechtenverhoging periodiek. Afgevinkt met de uitvoer en de datum.
- [ ] INFRA-95 (middel) Leg tijdens het incident vast wat je doet en evalueer daarna. Afgevinkt met het verslag.

### dicht-architectuur
- [ ] ARCH-65 (middel) Maak wijzigen van het audit-log zichtbaar. Afgevinkt met de proefmelding.
