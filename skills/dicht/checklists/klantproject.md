# Checklist klantproject

817 regels: 722 hard, 95 richtlijn. Gemaakt door `tools/bouw.py` uit het veld "Geldt voor"; niet met de hand wijzigen.
Elk punt: ID (ernst) titel, en wat telt als afgevinkt. Het volledige bewijs staat in de referentie van de sub-skill. Een punt dat in dit project niet speelt krijgt in het bewijsbestand `nvt` met een reden.

## Ontwerp: hard (64)

### dicht-web
- [ ] WEB-59 (middel) Houd een lijst van derde partijen bij en stuur ze geen gevoelige data. Afgevinkt met de hostlijst.

### dicht-api
- [ ] AUTH-64 (kritiek) Bescherm elke functie, ook via een andere methode of een ander pad. Afgevinkt als de matrix alle routes dekt.
- [ ] AUTH-81 (hoog) Accountherstel via support vraagt bewijs op hetzelfde niveau als de inrichting. Afgevinkt als document en test bestaan.
- [ ] API-51 (middel) Leg vast met welke externe diensten de app praat. De lijst staat in de projectdocumentatie en komt overeen met `grep -rnoE "https://[a-z0-9.-]+" src | sort -u`.
- [ ] BIZ-04 (hoog) Leg "hoogstens één tegelijk actief" vast met een partiële unieke index. `\d+ <tabel>` toont de partiële unieke index voor elke regel van deze vorm die in de documentatie staat.
- [ ] BIZ-06 (hoog) Voorkom overlappende periodes en dubbele boekingen met een exclusion constraint. `\d+ <tabel>` toont de exclusion constraint.
- [ ] BIZ-15 (hoog) Begrens terugbetalingen in je eigen boek voordat je Mollie aanroept. Test met 20 gelijktijdige gedeeltelijke terugbetalingen die samen meer zijn dan de betaling: de som in de eigen tabel blijft binnen het betaalde bedrag en de nagebootste 
- [ ] BIZ-18 (hoog) Pas 0 procent of verlegde btw alleen toe op bewijs dat de server zelf heeft gecontroleerd. Test: een bestelling met een btw-nummer dat de nagebootste VIES-dienst afkeurt, krijgt het gewone tarief;
- [ ] BIZ-35 (middel) Bind een eenmalig voordeel aan iets stabielers dan een e-mailadres. De documentatie noemt per voordeel de sleutel.
- [ ] BIZ-46 (hoog) Wijs per feit één bron aan en sla elk extern id uniek op. De tabel staat in het architectuurdocument.

### dicht-database
- [ ] DB-83 (hoog) Elke tabel met persoonsgegevens heeft een bewaartermijn en een opruimjob. Afgevinkt als alle drie kloppen.
- [ ] DB-87 (middel) Classificeer gegevens per kolom. Afgevinkt als het script nul ontbrekende kolommen meldt.

### dicht-infra
- [ ] INFRA-73 (hoog) Houd per geheim één bron en een lijst van gebruikers bij. Afgevinkt met de lijst en de vergelijking.

### dicht-git
- [ ] GIT-05 (middel) Commit na elke gevalideerde stap, één onderwerp per commit. Afgevinkt met beide uitvoeren.
- [ ] GIT-14 (kritiek) Beveilig het GitHub-account met TOTP plus een passkey, zonder sms. Afgevinkt met een notitie met datum.
- [ ] GIT-15 (hoog) Gebruik tokens met een einddatum en de kleinste reikwijdte. Afgevinkt met de lijst.
- [ ] GIT-16 (hoog) Geef een server alleen een deploy key met leesrecht op één repo. Afgevinkt met de uitvoer.
- [ ] GIT-18 (middel) Onderteken commits en tags. Afgevinkt met de uitvoer.
- [ ] GIT-22 (hoog) Maak een repo alleen publiek na een scan van de hele geschiedenis. Afgevinkt met beide uitvoeren.
- [ ] GIT-23 (hoog) Stel vast wat het GitHub-plan toelaat voordat je erop rekent. Afgevinkt met die tabel.
- [ ] GIT-24 (hoog) Bescherm de standaardbranch: met een ruleset waar het plan die biedt, anders lokaal. Afgevinkt met de uitvoer.
- [ ] GIT-27 (hoog) Zet de Actions-instellingen van de repo dicht. Afgevinkt met de uitvoer.
- [ ] GIT-28 (hoog) Zet Dependabot-meldingen en beveiligingsupdates aan op elke repo. Afgevinkt met de uitvoer.
- [ ] GIT-57 (hoog) De gate bevat lint, typecheck, tests en de scans van dit domein. Afgevinkt met script en uitvoer.
- [ ] GIT-77 (hoog) Leg hersteltermijnen vast en houd je eraan. Afgevinkt met document en uitvoer.
- [ ] GIT-104 (middel) Controleer de licentie van elke afhankelijkheid. Afgevinkt met de uitvoer.
- [ ] GIT-106 (hoog) Heb een draaiboek voor een gekaapt pakket. Afgevinkt met draaiboek en de uitvoer van de oefening.

### dicht-wordpress
- [ ] WP-25 (kritiek) Lees een bestand of sjabloon nooit in op basis van invoer. Afgevinkt met grep en test.

### dicht-ai-mcp
- [ ] AI-01 (kritiek) Ontwerp op de aanname dat de injectie slaagt. [bron niet gelezen: AGENTIC] Afgevinkt als de tabel er is en de regels AI-02, AI-06 en AI-24 erop zijn toegepast.
- [ ] AI-17 (hoog) Ontvanger, afzender en bijlagen van een bericht komen uit code, niet uit het model. [bron niet gelezen: AGENTIC] Afgevinkt met de testuitvoer.
- [ ] AI-66 (hoog) Leg per modelleverancier vast onder welke voorwaarden de gegevens worden verwerkt. Afgevinkt met de tabel.

### dicht-privacy
- [ ] PRIV-01 (hoog) Leg per project vast wie verantwoordelijke en wie verwerker is. Afgevinkt als elke tabel met persoonsgegevens uit de classificatie (DB-87) in precies één rij valt.
- [ ] PRIV-02 (hoog) Het verwerkingsregister bevat per activiteit de wettelijke velden. Afgevinkt met de uitvoer.
- [ ] PRIV-03 (hoog) Werk het register bij in dezelfde wijziging als de nieuwe gegevensstroom. Afgevinkt met de vergelijking.
- [ ] PRIV-05 (hoog) De privacyverklaring klopt met wat de code doet. Afgevinkt met de testuitvoer en de laatste uitvoer van die vergelijking
- [ ] PRIV-07 (hoog) Geen verwerking zonder vastgelegde grondslag. Afgevinkt met de scriptuitvoer.
- [ ] PRIV-08 (middel) Vraag per veld alleen wat het doel nodig heeft. Afgevinkt met tabel en grep.
- [ ] PRIV-10 (hoog) Toestemming is aantoonbaar, per doel en even makkelijk in te trekken. Afgevinkt met beide.
- [ ] PRIV-11 (hoog) Gebruik gegevens niet voor een ander doel dan waarvoor ze zijn verzameld. Afgevinkt met de verwijzing.
- [ ] PRIV-12 (hoog) Houd bijzondere gegevens buiten systemen die er niet voor gebouwd zijn. Afgevinkt met de telling en de classificatie.
- [ ] PRIV-21 (hoog) Elke gegevenssoort heeft een termijn met een reden, in het register en in de code. Afgevinkt met de vergelijking en de logregels.
- [ ] PRIV-23 (middel) Geef logs met persoonsgegevens een termijn die het doel dekt en niet meer. Afgevinkt met overzicht en configuratie.
- [ ] PRIV-37 (hoog) Doe bij elk nieuw project een DPIA-toets van vijf minuten en leg de uitkomst vast. Afgevinkt met de notitie.
- [ ] PRIV-38 (hoog) Bij zorgdata is de DPIA een bouwdocument dat meeloopt met de code. Afgevinkt met de log van de laatste drie integratiewijzigingen.
- [ ] PRIV-59 (hoog) Leg per project het ASVS-niveau vast, per onderdeel. Afgevinkt als het bestand bestaat vóór de eerste regel code van een nieuw project en bij de oplevering van een bestaand project.
- [ ] PRIV-60 (middel) Maak een toepasbaarheidstabel en verklaar elk hoofdstuk dat vervalt. Afgevinkt met tabel en grep-uitvoer.
- [ ] PRIV-76 (hoog) Toets voor het eigen bedrijf en voor elke klant of de Cyberbeveiligingswet geldt. [bron niet gelezen: CBW] Afgevinkt als de notitie voor het eigen bedrijf bestaat en bij nieuwe klanten in de intake staat.
- [ ] PRIV-80 (middel) Stel vast of je aanbieder of gebruiksverantwoordelijke bent. [bron niet gelezen: AI-VO] Afgevinkt met de tabel.

### dicht-architectuur
- [ ] ARCH-01 (middel) Bouw een modulaire monoliet; een extra proces of dienst vraagt een vastgelegd besluit. [eigen bron] Afgevinkt als lijst en werkelijkheid gelijk zijn.
- [ ] ARCH-05 (hoog) Lever geen test-, voorbeeld- of ontwikkelcode mee naar productie. Afgevinkt met de drie uitvoeren.
- [ ] ARCH-06 (middel) Houd één architectuurdocument bij met vaste onderdelen. Afgevinkt als beide kloppen.
- [ ] ARCH-29 (middel) Leg elke architectuurbeslissing vast als ADR. Afgevinkt als die bestanden bestaan en de status klopt.
- [ ] ARCH-30 (hoog) Leg elke uitzondering op een harde regel vast, ook een overgeslagen stap. Afgevinkt als het bestand bestaat en geen uitzondering over zijn einddatum heen is.
- [ ] ARCH-31 (middel) Schrijf per dienst een runbook met de vijf handelingen en elk alarm. Afgevinkt met de vergelijking en de datum van de oefening.
- [ ] ARCH-32 (middel) Leg hersteltermijnen vast en houd een schuldregister bij. Afgevinkt met de tellingen.
- [ ] ARCH-57 (middel) Houd per applicatie een loginventaris bij. Afgevinkt als lijst en werkelijkheid gelijk zijn.
- [ ] ARCH-80 (hoog) Maak bij elk nieuw project een threat model in vier vragen. Afgevinkt als het bestand compleet is.
- [ ] ARCH-81 (middel) Herzie het threat model bij elke nieuwe ingang of grens. Afgevinkt met de datumvergelijking.

### dicht-scripts
Alleen als het project een script, een geplande taak of een lus bevat die in cron, een timer, een uitrol of een andere sessie draait; anders het hele blok `nvt` met die reden.
- [ ] SCR-39 (middel) Bepaal per taak wat er gebeurt met een gemiste run. Afgevinkt met de lijst en de uitvoer.

### dicht-invoer
- [ ] INV-13 (hoog) Dwing per parameter één waarde en één type af. Afgevinkt met test en grep.
- [ ] INV-43 (hoog) Tel uitgepakte bytes en entries tijdens het uitpakken en pak niet genest uit. Afgevinkt met de testuitvoer.

### dicht-berichten
- [ ] MSG-21 (laag) Geef bijlagen een veilige, gecodeerde bestandsnaam. Afgevinkt met de testuitvoer.
- [ ] MSG-33 (middel) Herken een automatisch antwoord aan de koppen, niet aan het onderwerp. Afgevinkt met de testuitvoer.
- [ ] MSG-38 (hoog) Dwing het 24-uursvenster af in code. [bron niet gelezen: META] Afgevinkt met de testuitvoer.

## Ontwerp: richtlijnen (17)

### dicht-api
- [ ] BIZ-28 (middel) Sla periodes op als halfopen interval. `grep -rniE "23:59|between .* and" src` is leeg voor tijdvergelijkingen, of beoordeeld.

### dicht-infra
- [ ] INFRA-08 (middel) Trek toegang in met een lijst, niet uit het hoofd. Afgevinkt met de lijst en de vergelijking.

### dicht-git
- [ ] GIT-17 (middel) SSH-sleutels: ed25519, met wachtwoordzin, één per machine. Afgevinkt met beide.
- [ ] GIT-19 (laag) Zet vigilant mode pas aan als alles ondertekend is. Afgevinkt met een schermafbeelding of de API-uitvoer `gh api repos/<o>/<r>/commits/<sha> --jq .
- [ ] GIT-20 (middel) Geef anderen toegang via een organisatie of een deploy key, niet als collaborator. Afgevinkt met de lijst.
- [ ] GIT-21 (middel) Loop per kwartaal sessies, sleutels, tokens en apps na. Afgevinkt met de notitie.
- [ ] GIT-25 (laag) Kies één mergestrategie en zet de regels die ermee botsen niet aan. Afgevinkt met de ruleset-uitvoer.
- [ ] GIT-29 (laag) Wijs een eigenaar aan voor workflows en CODEOWNERS zelf. Afgevinkt met de drie.
- [ ] GIT-68 (laag) Leg de versies van hulpmiddelen vast en ververs ze per kwartaal. Afgevinkt met de lijst.

### dicht-wordpress
- [ ] WP-44 (laag) Reken niet op een ander tabelprefix. Afgevinkt zonder verdere actie.

### dicht-privacy
- [ ] PRIV-04 (middel) Houd als verwerker een eigen register per klant bij. Afgevinkt als elke actieve hosting- of onderhoudsklant een rij heeft.
- [ ] PRIV-06 (middel) Bewaar het bewijs van elke privacykeuze bij het project. Afgevinkt als het bestand bestaat en de laatste wijziging in git niet ouder is dan de laatste wijziging aan de gegevensstroom.
- [ ] PRIV-39 (middel) Toets of een functionaris gegevensbescherming verplicht is. Afgevinkt met de notitie.
- [ ] PRIV-44 (middel) Meet zonder toestemming alleen wat geen of geringe gevolgen heeft, en dan zelf gehost. Afgevinkt met de drie.
- [ ] PRIV-63 (middel) ASVS dekt de AVG niet: gebruik de koppeltabel. Afgevinkt als elke rij een verwijzing heeft.
- [ ] PRIV-64 (laag) Herbeoordeel het niveau bij elke wijziging van functie of gegevens. Afgevinkt met de log.
- [ ] PRIV-78 (middel) Reken erop dat een klant onder de wet zijn eisen aan jou doorlegt. Afgevinkt als de map bestaat en de stukken een datum hebben.

## Bouwen: hard (512)

### dicht-web
- [ ] WEB-01 (kritiek) Codeer uitvoer per context, als laatste stap. Afgevinkt als beide groen zijn.
- [ ] WEB-02 (hoog) Schrijf tekst naar de DOM met veilige sinks. Afgevinkt met de grep-uitvoer en een groene lint.
- [ ] WEB-03 (hoog) Sta HTML van gebruikers alleen toe via een onderhouden sanitizer. Afgevinkt met versie en testuitvoer.
- [ ] WEB-04 (hoog) Laat in URL-attributen alleen veilige schema's toe. Afgevinkt met de testuitvoer.
- [ ] WEB-06 (hoog) Geef data aan JavaScript door als gecodeerde data, niet als code. Afgevinkt met de test.
- [ ] WEB-07 (hoog) Behandel SVG, Markdown en eigen CSS van gebruikers als actieve inhoud. Afgevinkt met de drie testuitvoeren.
- [ ] WEB-08 (kritiek) Bouw nooit een template uit invoer. Afgevinkt met de test.
- [ ] WEB-09 (middel) Stuur bij elke respons het juiste Content-Type met charset en nosniff. Afgevinkt met de vier uitvoeren.
- [ ] WEB-11 (hoog) Zet een strikte CSP op elke HTML-respons. Afgevinkt met header en consolelog.
- [ ] WEB-12 (hoog) Maak de nonce per respons, willekeurig en onvoorspelbaar. Afgevinkt met beide uitvoeren.
- [ ] WEB-13 (middel) Geen inline handlers, geen unsafe-eval. Afgevinkt met grep en header.
- [ ] WEB-15 (middel) Lever CSP als HTTP-header, niet als meta-tag. Afgevinkt met de uitvoer.
- [ ] WEB-17 (hoog) Zet HSTS op alle responsen. Afgevinkt met de uitvoer en de subdomeinlijst.
- [ ] WEB-19 (middel) Zet een expliciete Referrer-Policy. Afgevinkt met beide.
- [ ] WEB-22 (laag) Verberg versies en verwijder verouderde headers. Afgevinkt met de uitvoer.
- [ ] WEB-23 (hoog) Controleer headers op elke locatie en elke statuscode (nginx-overerving). Afgevinkt met de tabel.
- [ ] WEB-24 (hoog) Verbied insluiten met frame-ancestors. Afgevinkt met header en schermafbeelding of consolemelding.
- [ ] WEB-25 (hoog) Geef elke sessiecookie Secure, HttpOnly, SameSite en het __Host-voorvoegsel. Afgevinkt met de header en de consoletest.
- [ ] WEB-29 (hoog) Wijzig nooit iets via GET. Afgevinkt met lijst en test.
- [ ] WEB-30 (kritiek) Verdedig elke wijzigende aanvraag met cookie-authenticatie tegen CSRF. Afgevinkt met de testuitvoer.
- [ ] WEB-39 (hoog) Stuur alleen door naar bestemmingen uit een allowlist. Afgevinkt met de testuitvoer.
- [ ] WEB-40 (kritiek) Haal server-side alleen toegestane adressen op (SSRF). Afgevinkt met de testuitvoer.
- [ ] WEB-42 (hoog) Bouw absolute URL's uit de configuratie, nooit uit de Host-header. Afgevinkt met beide.
- [ ] WEB-43 (hoog) Begrens de grootte van elke upload en elke body. Afgevinkt met de test.
- [ ] WEB-44 (hoog) Sta alleen een allowlist van typen toe en controleer de inhoud. Afgevinkt met de testuitvoer.
- [ ] WEB-45 (hoog) Bepaal bestandsnaam en pad zelf. Afgevinkt met test en grep.
- [ ] WEB-46 (kritiek) Sla uploads op waar ze nooit als code worden uitgevoerd. Afgevinkt met de curl-uitvoer.
- [ ] WEB-47 (hoog) Lever bestanden van gebruikers uit als download of vanaf een aparte origin. Afgevinkt met de uitvoer.
- [ ] WEB-48 (middel) Scan bestanden uit niet-vertrouwde bron op malware. Afgevinkt met de logregel.
- [ ] WEB-51 (hoog) Vertrouw proxy-headers alleen van de eigen proxy. Afgevinkt met de drie uitvoeren.
- [ ] WEB-52 (hoog) Zet no-store op elke respons met persoonlijke of ingelogde inhoud. Afgevinkt met beide uitvoeren per route.
- [ ] WEB-53 (hoog) Sluit web cache deception uit. Afgevinkt met de uitvoer.
- [ ] WEB-54 (hoog) Laat niets uit de aanvraag in een gecachte respons belanden dat niet in de cachesleutel zit. Afgevinkt met de twee uitvoeren.
- [ ] WEB-55 (hoog) Zet geen gevoelige gegevens in de URL. Afgevinkt met grep en logsteekproef.
- [ ] WEB-56 (hoog) Serveer alles over HTTPS; laat een API niet stil doorsturen. Afgevinkt met de drie uitvoeren.
- [ ] WEB-58 (hoog) Host scripts, stijlen en lettertypen zelf, of pin ze met SRI. Afgevinkt met de hostlijst en de grep.
- [ ] WEB-62 (hoog) Toon een generieke foutpagina; debug uit in productie. Afgevinkt met respons en logregel.
- [ ] WEB-64 (hoog) Zet niets in de webroot dat er niet hoort. Afgevinkt met de uitvoer.
- [ ] WEB-66 (hoog) Begrens het aantal aanvragen op elke route die iets kost of iets verstuurt. Afgevinkt met de uitvoer.
- [ ] WEB-67 (hoog) Bescherm elk publiek formulier op de server tegen bots. Afgevinkt met de testuitvoer.
- [ ] WEB-68 (hoog) Voorkom header-injectie in uitgaande mail. Afgevinkt met de testuitvoer en de headers van de ontvangen mail.
- [ ] WEB-69 (middel) Laat een formulier nooit naar een adres uit de invoer mailen zonder grens. Afgevinkt met de code en de test.

### dicht-api
- [ ] AUTH-01 (hoog) Minimale en maximale wachtwoordlengte. Afgevinkt als de test in CI draait en het schema op alle drie de plekken (registratie, wijzigen, reset) hetzelfde is.
- [ ] AUTH-03 (hoog) Controleer nieuwe wachtwoorden tegen een blocklist. Afgevinkt als beide tests groen zijn.
- [ ] AUTH-04 (kritiek) Sla wachtwoorden op met Argon2id. Afgevinkt als beide kloppen en de parameters uit configuratie komen.
- [ ] AUTH-05 (hoog) Stop nooit meer dan het wachtwoord in bcrypt. Afgevinkt als de test groen is of bcrypt niet voorkomt.
- [ ] AUTH-06 (middel) Verifieer het wachtwoord ongewijzigd en werk wachtwoordmanagers niet tegen. [alleen: met login] Afgevinkt met een Playwright-test die een wachtwoord plakt.
- [ ] AUTH-08 (hoog) Wachtwoord wijzigen vraagt het huidige wachtwoord. Afgevinkt als de test groen is en de meldingsmail in de test-mailbox staat.
- [ ] AUTH-09 (hoog) Geen hints, geen geheime vragen, geen standaardaccounts, geen blijvende startwachtwoorden. Afgevinkt als de lijst klopt met de afgesproken beheerders.
- [ ] AUTH-10 (kritiek) Begrens inlogpogingen per account en per bron. [alleen: met login] Afgevinkt als de test groen is en het document bestaat.
- [ ] AUTH-12 (middel) Verklap niet of een account bestaat. [alleen: met login] Afgevinkt als de test in CI staat.
- [ ] AUTH-13 (hoog) Ken en bewaak elk inlogpad. Afgevinkt als elk pad een test heeft.
- [ ] AUTH-14 (hoog) Log elke authenticatiegebeurtenis, zonder geheimen. Afgevinkt als beide kloppen.
- [ ] AUTH-16 (kritiek) MFA verplicht voor beheer en voor alles op niveau 2. [bron niet gelezen: NEN] Afgevinkt als query en test kloppen.
- [ ] AUTH-17 (hoog) TOTP: eenmalig, kort geldig, begrensd. Afgevinkt als de tests groen zijn.
- [ ] AUTH-18 (middel) E-mail en sms zijn geen volwaardige tweede factor. Afgevinkt als de test groen is.
- [ ] AUTH-19 (hoog) Herstelcodes: sterk, gehasht, eenmalig. Afgevinkt als beide kloppen.
- [ ] AUTH-20 (kritiek) Reset en herstel mogen MFA niet omzeilen. Afgevinkt als beide tests groen zijn.
- [ ] AUTH-21 (kritiek) Passkeys: verifieer op de server volgens WebAuthn, met een bibliotheek. Afgevinkt als de drie tests groen zijn.
- [ ] AUTH-22 (middel) Passkeys: sla het juiste op en lek niets via de user handle. Afgevinkt als beide kloppen.
- [ ] AUTH-23 (hoog) Passkeys: eis gebruikersverificatie als de passkey de enige stap is, en laat de terugval niet zwakker zijn. Afgevinkt als beide kloppen.
- [ ] AUTH-25 (kritiek) Reset- en verificatietokens: willekeurig, gehasht, eenmalig, kort geldig. [alleen: met login] Afgevinkt als de drie tests groen zijn.
- [ ] AUTH-27 (kritiek) Stuur resetmails alleen naar het geverifieerde adres uit de database. [alleen: met login] Afgevinkt als de tests groen zijn.
- [ ] AUTH-28 (hoog) Na een reset: niet automatisch inloggen, sessies weg, melding. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-29 (hoog) Verifieer een e-mailadres voordat het iets betekent, en bescherm de wijziging ervan. Afgevinkt als de tests groen zijn.
- [ ] AUTH-30 (hoog) Magic links: dezelfde eisen als een reset, gebonden aan de browser, niet voor kritieke delen. Afgevinkt als de tests groen zijn.
- [ ] AUTH-31 (middel) Houd tokens uit referers, logs en pagina's met scripts van derden. [alleen: met login] Afgevinkt als alle drie kloppen.
- [ ] AUTH-32 (kritiek) Sessie-id: willekeurig, ondoorzichtig, op de server gecontroleerd. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-33 (kritiek) Sessiecookie: `__Host-`, Secure, HttpOnly, SameSite, en nooit in webopslag. [alleen: met login] Afgevinkt als beide kloppen.
- [ ] AUTH-34 (hoog) Nieuw sessie-id bij inloggen en bij elke rechtenwijziging. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-35 (hoog) Leg een idle timeout en een absolute timeout vast en dwing ze op de server af. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-36 (kritiek) Uitloggen en blokkeren werken direct op de server. [alleen: met login] Afgevinkt als beide tests groen zijn.
- [ ] AUTH-37 (middel) Geef gebruiker en beheerder zicht op en controle over actieve sessies. Afgevinkt als beide groen zijn.
- [ ] AUTH-38 (hoog) Vraag opnieuw om authenticatie voor gevoelige handelingen. Afgevinkt als elke handeling uit de lijst een test heeft.
- [ ] AUTH-39 (kritiek) Leg het algoritme vast bij verificatie. Afgevinkt als de tests groen zijn.
- [ ] AUTH-40 (kritiek) Haal verificatiesleutels uit je eigen configuratie, niet uit het token. Afgevinkt als de test groen is.
- [ ] AUTH-41 (kritiek) Valideer geldigheid, uitgever, publiek en type van elk token. Afgevinkt als de vier tests groen zijn.
- [ ] AUTH-42 (hoog) Symmetrische tokensleutels: willekeurig en minimaal zo lang als de hash. Afgevinkt als beide kloppen.
- [ ] AUTH-44 (kritiek) Alleen de authorization code flow met PKCE (S256). Afgevinkt als dit klopt.
- [ ] AUTH-45 (kritiek) Redirect-URI's exact vergelijken. Afgevinkt als de tests groen zijn of een schermafdruk van de registratie in het dossier zit.
- [ ] AUTH-46 (hoog) Bind `state`, PKCE en `nonce` aan de browsersessie die de flow startte. Afgevinkt als de tests groen zijn.
- [ ] AUTH-47 (kritiek) Koppel externe identiteiten op uitgever plus `sub`, nooit op e-mail. Afgevinkt als de test groen is.
- [ ] AUTH-48 (hoog) Valideer het ID-token volledig. Afgevinkt als de tests groen zijn.
- [ ] AUTH-50 (hoog) Refresh tokens: roteren met hergebruikdetectie, eindig en intrekbaar. Afgevinkt als de tests groen zijn.
- [ ] AUTH-51 (hoog) Houd tokens en clientgeheimen bij de backend en vraag minimale scopes. Afgevinkt als beide kloppen.
- [ ] AUTH-56 (hoog) Diensten onderling: eigen identiteit per dienst met minimale rechten. Afgevinkt als dat klopt.
- [ ] AUTH-57 (hoog) Vergelijk geheimen in constante tijd. Afgevinkt als beide kloppen.
- [ ] AUTH-58 (kritiek) Inkomende webhooks: handtekening over de ruwe body controleren. Afgevinkt als de drie tests groen zijn.
- [ ] AUTH-59 (hoog) Inkomende webhooks: bescherm tegen herhaling en dubbele verwerking. Afgevinkt als beide tests groen zijn.
- [ ] AUTH-62 (kritiek) Weiger standaard en dwing af op de server, op één plek. Afgevinkt als die test in CI staat.
- [ ] AUTH-63 (kritiek) Controleer bij elk object of het van deze gebruiker en deze tenant is. Afgevinkt als elke route in de lijst een test heeft (zie AUTH-66).
- [ ] AUTH-65 (kritiek) Laat een gebruiker geen velden zetten die zijn rechten bepalen. Afgevinkt als de test groen is.
- [ ] AUTH-66 (hoog) Autorisatietests met twee gebruikers en twee tenants zijn een CI-gate. Afgevinkt als beide in CI staan.
- [ ] AUTH-67 (hoog) Vertrouw niet alleen op middleware, proxy of route-volgorde. Afgevinkt als dat zo is.
- [ ] AUTH-69 (hoog) Bestanden, exports en back-ups vallen onder dezelfde autorisatie. Afgevinkt als beide kloppen.
- [ ] AUTH-70 (middel) Log geweigerde toegang en geef geen details prijs. Afgevinkt als de test groen is.
- [ ] AUTH-80 (middel) Beheerders starten een reset, ze kiezen geen wachtwoord. Afgevinkt als dat zo is.
- [ ] AUTH-82 (hoog) Beheerinterfaces: MFA, eigen pad, niet alleen een IP-filter. [alleen: met beheer] Afgevinkt als beide kloppen.
- [ ] AUTH-84 (hoog) Auditlog van gevoelige acties. [bron niet gelezen: NEN] Afgevinkt als beide kloppen.
- [ ] API-01 (kritiek) Schema-validatie aan elke rand. Elke route heeft een schema voor body, query en params (Fastify `schema` of een zod-parse als eerste regel).
- [ ] API-07 (middel) Decodeer één keer, vóór de validatie. `grep -rn "decodeURIComponent\|urldecode\|rawurldecode" src` toont alleen aanroepen vóór de schema-parse. Test met dubbel gecodeerde invoer.
- [ ] API-12 (kritiek) Faal dicht. Test per controle met een mock die gooit: de actie erna gebeurt niet. Review: elke `catch` zonder `throw` of `return` rond een controle is een bevinding.
- [ ] API-27 (kritiek) Bereken prijs en totaal op de server uit een vertrouwde bron. Het bestelschema bevat geen bedragveld.
- [ ] API-30 (kritiek) Maak controleren en handelen één atomaire stap. Een test vuurt 20 gelijktijdige verzoeken af op dezelfde bewerking en controleert dat het effect precies één keer optreedt.
- [ ] API-32 (kritiek) Zet een samengestelde bewerking in één transactie. De statusovergang en het aanmaken van de taak staan in dezelfde `db.transaction`. Test: een fout na de eerste schrijfactie laat de status ongewijzigd.
- [ ] API-36 (kritiek) Behandel de webhook als signaal en haal de status op bij Mollie. Test: een POST naar de webhook met het id van een betaling met status `open` leidt niet tot levering.
- [ ] API-37 (kritiek) Vergelijk bedrag, valuta en bestelling voordat je levert. De handler zoekt op `molliePaymentId` in de eigen tabel (geen bestel-id uit het verzoek of alleen uit `metadata`).
- [ ] API-38 (kritiek) Lever precies één keer, hoe vaak de webhook ook komt. Test met 20 gelijktijdige webhook-aanroepen voor één betaling: precies één leveringstaak, één mail, één vergoeding.
- [ ] API-39 (hoog) Antwoord 200 pas als de verwerking duurzaam vastligt. Test: laat de database-aanroep in de handler falen en controleer dat het antwoord 5xx is.
- [ ] API-40 (middel) Antwoord de webhook binnen 15 seconden en doe zwaar werk daarna. De handler bevat geen aanroepen naar andere diensten dan de Mollie-API en de eigen database.
- [ ] API-41 (hoog) Stuur een Idempotency-Key mee bij elke POST naar Mollie. `grep -rn "idempotencyKey\|Idempotency-Key" src` toont de sleutel bij elke muterende Mollie-aanroep.
- [ ] API-42 (hoog) Verwerk ook wat er na "betaald" gebeurt. Test met een nagebootst Mollie-antwoord waarin een chargeback of terugbetaling staat: er ontstaat een vastlegging en een taak.
- [ ] API-82 (hoog) Productie betaalt met de live-sleutel, en de eerste echte betaling bewijst het. Afgevinkt met beide.
- [ ] API-48 (hoog) Geef elke uitgaande aanroep een time-out, een maximale omvang en geen redirects. `grep -rn "fetch(" src` toont bij elke aanroep een `signal`.
- [ ] API-49 (middel) Herhaal begrensd, met oplopende wachttijd, en alleen wat veilig te herhalen is. Eén gedeelde herhaalfunctie met een maximum;
- [ ] API-50 (hoog) Valideer antwoorden van externe diensten net zo streng als invoer van gebruikers. Elke client-module exporteert geparste types;
- [ ] API-53 (kritiek) Start processen zonder shell en met een argumentenlijst. `grep -rnE "\bexec\(|execSync\(|shell: *true" src` is leeg.
- [ ] API-54 (kritiek) Maak bestandspaden zelf en controleer dat ze binnen de basismap blijven. Test met `../`, `..%2f`, een absoluut pad en een naam met een nulbyte: alle geweigerd.
- [ ] API-55 (kritiek) Deserialiseer onvertrouwde data alleen als JSON met een schema. `grep -rnE "unserialize\(|maybe_unserialize\(" .` in PHP toont alleen data uit eigen opslag die niet door gebruikers te zetten is (zie WP voor `maybe_unserialize`).
- [ ] API-56 (kritiek) Voer nooit tekst als code uit. ESLint-regels `no-eval`, `no-implied-eval` en `no-new-func` staan aan en zijn groen. `grep -rnE "\beval\(|new Function\(|vm\.run" src` is leeg.
- [ ] API-57 (hoog) Houd reguliere expressies lineair en begrens de invoer ervoor. ESLint met `eslint-plugin-security` (`detect-unsafe-regex`, `detect-non-literal-regexp`) of `eslint-plugin-regexp` is groen.
- [ ] API-59 (middel) Maak exports veilig tegen formule-injectie. Unit-test op de exportfunctie met elk van de zes begintekens. Eén gedeelde exportfunctie, geen losse `join(',')`.
- [ ] API-61 (kritiek) Maak onraadbare waarden met een CSPRNG en minimaal 128 bits. `grep -rnE "Math\.random|mt_rand|\brand\(|uniqid\(" src` is leeg in code die tokens, namen van privébestanden of codes maakt. Een UUID v4 mag als id, niet als geheim.
- [ ] API-63 (hoog) Kies bewust tussen hashen en versleutelen. `grep -rnE "createCipher\(|aes-...-(ecb|cbc)|md5|sha1" src` wordt per treffer beoordeeld.
- [ ] API-64 (hoog) Schrijf geen eigen cryptografie. Review: elke plek waar een handtekening of sleutel wordt gemaakt gebruikt HMAC of een bibliotheekfunctie.
- [ ] API-65 (kritiek) Houd geheimen uit code en build en valideer ze bij de start. Afgevinkt met de uitvoer van beide.
- [ ] API-66 (hoog) Log geen geheimen en geen persoonsgegevens. De logger-configuratie bevat `redact`.
- [ ] API-75 (hoog) Strikte types en strikte vergelijking in elk PHP-bestand. `grep -rL "declare(strict_types=1)" --include=*.php <eigen mappen>` is leeg. PHPStan met `phpstan-strict-rules` of een PHPCS-regel op `==` is groen.
- [ ] API-76 (kritiek) Laad nooit een bestand op basis van invoer. `grep -rnE "(include|require)(_once)? *\(?.*\\$(_GET|_POST|_REQUEST|_COOKIE)" .` is leeg. `php -i | grep allow_url_include` toont Off.
- [ ] API-77 (middel) Lees superglobals op één plek en nooit `$_REQUEST`. `grep -rn "\$_REQUEST" .` in eigen code is leeg.
- [ ] API-78 (middel) Statische analyse op PHP als gate. `vendor/bin/phpstan analyse --level 8` (met `szepeviktor/phpstan-wordpress` voor WordPress-stubs) is groen in CI. `phpstan.neon` staat in de repository.
- [ ] API-79 (hoog) Productie-instellingen van PHP tonen geen fouten. `php -i | grep -E "display_errors|expose_php|log_errors|exception_ignore_args"` of de PHP-instellingen in Enhance tonen deze waarden.
- [ ] API-81 (kritiek) Zet geen ontwikkelgereedschap en geen `vendor/` in de webroot. `curl -sI https://<site>/wp-content/plugins/<plugin>/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php`, `/.git/HEAD` en `/composer.json` geven 403 of 404.
- [ ] BIZ-01 (hoog) Schrijf een teller of saldo als relatieve bewerking in SQL. `grep -rnE "\.set\(\{[^}]*(\+|-) *[0-9a-zA-Z_.]+" src` toont geen rekensom in JavaScript op een kolom die een teller of saldo is;
- [ ] BIZ-02 (hoog) Bewaak een regel over meerdere rijen met één slot op de ouder, niet met een slot op de rijen zelf. Per regel over meerdere rijen staat in de projectdocumentatie welk slot hem bewaakt.
- [ ] BIZ-05 (middel) Een unieke sleutel met een kolom die NULL kan zijn, houdt geen duplicaten tegen. Query op het schema: elke kolom in een unieke index is `NOT NULL` of de index heeft `indnullsnotdistinct = true` (`SELECT indexrelid::regclass, indnullsnotdistinct FROM p
- [ ] BIZ-08 (middel) Laat factuurnummers en andere doorlopende reeksen niet uit een sequence komen. `grep -rnE "serial|generatedAlwaysAsIdentity|nextval" src` raakt geen kolom die als factuur-, order- of bonnummer naar buiten gaat.
- [ ] BIZ-10 (hoog) Rond btw rekenkundig af op hele centen, volgens één vastgelegde methode. De gekozen methode staat in de projectdocumentatie.
- [ ] BIZ-11 (hoog) Maak van een numeric uit de database geen JavaScript-getal om mee te rekenen. `grep -rnE "Number\(|parseFloat\(|toFixed\(|Math\.round\(" src` in prijs-, korting-, btw- en betaalcode: elke treffer werkt op gehele centen of is weergave;
- [ ] BIZ-12 (middel) Verdeel een bedrag zo dat de delen samen exact het totaal zijn. Eigenschappen-test (ARCH-42): voor willekeurige totalen en aantallen is de som van `verdeel()` gelijk aan het totaal en verschillen de delen hoogstens één cent.
- [ ] BIZ-13 (hoog) Leg prijs, korting, btw-tarief en totaal vast op de bestelling en reken ze later niet opnieuw uit. De bestelregel heeft eigen kolommen voor prijs, korting, tarief en totaal, alle `NOT NULL`.
- [ ] BIZ-14 (hoog) Bevries de bestelling zodra de betaling is aangemaakt. Test: maak een betaling aan, probeer daarna een regel toe te voegen, het aantal te wijzigen en een code toe te passen;
- [ ] BIZ-16 (middel) Keer een vergoeding of tegoed dat aan een betaling hangt pas uit na de terugboektermijn. De termijn per betaalwijze staat in de projectdocumentatie (iDEAL: 14 dagen, de eigen geld-terugtermijn;
- [ ] BIZ-19 (middel) Een bestelling van nul euro heeft een eigen overgang en gaat niet langs "betaald". De statusmachine heeft een overgang `concept -> gratis_toegekend` naast `wacht_op_betaling -> betaald`.
- [ ] BIZ-20 (hoog) Reserveer schaarse dingen met een vervaltijd en een maximum per account. De reserveringstabel heeft `verloopt_op NOT NULL`.
- [ ] BIZ-22 (hoog) "Betaald maar niet leverbaar" is een eigen toestand met een vaste afhandeling. De overgangstabel van API-29 bevat de toestand en de overgangen eruit.
- [ ] BIZ-23 (hoog) Geef elke automatische stroom die geld kost of iets naar buiten stuurt een dagplafond dat stopt. Per stroom staat in de projectdocumentatie het plafond per tenant en in totaal, en wie hem weer aanzet.
- [ ] BIZ-24 (middel) Geloof bij een bericht over een toestand de actuele stand, niet de inhoud of de volgorde van het bericht. Test: bied de berichten van één betaling aan in omgekeerde volgorde en dubbel;
- [ ] BIZ-25 (middel) Controleer een termijn op het moment van gebruik en reken niet op de opruimjob. Test met een vaste klok: een rij met `verloopt_op` één seconde in het verleden wordt geweigerd terwijl de status nog "actief" is.
- [ ] BIZ-26 (hoog) Reken kalenderperiodes vanaf de ankerdatum, in SQL of met een kalenderbibliotheek. `grep -rnE "setMonth|setFullYear|setDate|86400|\* 30\b|\* 365\b" src` is leeg in code die periodes, vervaldatums of einddatums berekent, of elke treffer is beoordeeld.
- [ ] BIZ-27 (middel) Bepaal zakelijke datums in Europe/Amsterdam en sla ze op als datum. `grep -rnE "toISOString\(\)\.(slice|substring|split)" src` raakt geen zakelijke datum.
- [ ] BIZ-29 (middel) Tel dagen als kalenderdagen, niet als 24 uur. Test met een vaste klok rond 29-03-2026 en 25-10-2026: de termijn eindigt op de verwachte kalenderdag.
- [ ] BIZ-30 (hoog) Leg elke periodieke incasso vast met een unieke sleutel op abonnement en periode voordat je incasseert. `\d incassos` toont de unieke index.
- [ ] BIZ-32 (middel) Maak codes met waarde niet raadbaar en begrens het proberen. Test: na het ingestelde aantal mislukte pogingen geeft de route 429 (API-20, API-22), ook voor een daarna correcte code binnen het venster.
- [ ] BIZ-33 (hoog) Sta standaard één code per bestelling toe en begrens de totale korting. Unit-tests op de prijsfunctie: twee codes, dezelfde code twee keer, een code plus een automatische actie;
- [ ] BIZ-34 (hoog) Reserveer een beperkte code bij het starten van de bestelling en tel hem definitief bij de betaling. Test: 20 gelijktijdige bestellingen met een code die één keer geldt;
- [ ] BIZ-36 (middel) Geen vergoeding voor een verwijzing naar jezelf. Tests: bestelling met de eigen code (zelfde klantsleutel, zelfde betaalmiddel, zelfde organisatie) geeft geen vergoeding;
- [ ] BIZ-37 (middel) Geef opzoekfuncties met zakelijke waarde een eigen limiet. Per opzoekfunctie staat de limiet in de documentatie (API-34) en is er een test die hem overschrijdt (429 met `Retry-After`).
- [ ] BIZ-40 (hoog) Een time-out is "onbekend", niet "mislukt". Het statusveld van elke uitgaande taak kent "onbekend".
- [ ] BIZ-41 (hoog) Voorkom dubbele facturen in Moneybird met een eigen claim, want Moneybird kent geen idempotentiesleutel. `\d documenten` toont de unieke index op (bestelling, soort) en een unieke index op het Moneybird-id.
- [ ] BIZ-44 (hoog) WordPress: houd geen teller, limiet of slot bij met opties of meta. `grep -rnE "update_option|update_post_meta|update_user_meta|set_transient" .` in de plugin: geen treffer schrijft een waarde die uit een eerdere `get_` is berekend en die
- [ ] BIZ-49 (middel) Laat de afstemming melden en alleen via de gewone verwerking herstellen. `grep -rnE "update|insert|delete" ` in de afstemmingsmodule toont alleen schrijven naar de eigen rapportage- of taaktabel.

### dicht-database
- [ ] DB-01 (kritiek) Geen superuser als applicatierol. Afgevinkt als de rol van elke dienst op alle vijf kolommen `f` heeft.
- [ ] DB-02 (hoog) Eén loginrol per dienst en per omgeving. Afgevinkt als elke dienst een eigen rol toont en geen rol in twee omgevingen bestaat met hetzelfde wachtwoord (controle in de geheimenopslag).
- [ ] DB-03 (hoog) Scheid de eigenaar (migratierol) van de runtime-rol. Afgevinkt als geen tabel de runtime-rol als eigenaar heeft en de migratierol niet in een runtime-`DATABASE_URL` voorkomt.
- [ ] DB-04 (hoog) Trek de standaardrechten van PUBLIC in. [bron niet gelezen: CIS] Afgevinkt als in `datacl` geen regel `=Tc/.
- [ ] DB-05 (hoog) Verleen rechten per tabel en per bewerking, nooit GRANT ALL. Afgevinkt als geen `TRUNCATE`, `REFERENCES` of `TRIGGER` voorkomt en audit-tabellen alleen `INSERT` en `SELECT` hebben.
- [ ] DB-06 (kritiek) Geen gevaarlijke rolattributen of voorgedefinieerde rollen voor applicaties. Afgevinkt als applicatierollen in geen van beide voorkomen.
- [ ] DB-07 (middel) Trek EXECUTE op functies in van PUBLIC. Afgevinkt als de query voor eigen functies nul rijen geeft (een lege `proacl` betekent de standaard, dus PUBLIC mag uitvoeren).
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
- [ ] DB-58 (kritiek) De database is niet bereikbaar vanaf internet. [bron niet gelezen: CIS] Afgevinkt als beide kloppen.
- [ ] DB-59 (hoog) Geen trust over TCP, alleen scram-sha-256. [bron niet gelezen: CIS] Afgevinkt als alle drie kloppen.
- [ ] DB-60 (hoog) TLS met certificaatcontrole zodra de verbinding de host verlaat. Afgevinkt als beide kloppen.
- [ ] DB-61 (middel) Zet en wissel wachtwoorden zonder dat ze in een log belanden. Afgevinkt als beide groen zijn.
- [ ] DB-62 (hoog) De verbindingsstring is een geheim. Afgevinkt als alle drie kloppen.
- [ ] DB-63 (middel) Begrens de pool per dienst en houd de som onder max_connections. Afgevinkt als de som onder `SHOW max_connections` blijft.
- [ ] DB-65 (hoog) Zet time-outs per rol. Afgevinkt als elke applicatierol de drie instellingen heeft.
- [ ] DB-68 (hoog) Verwerk webhooks en opdrachten idempotent met een unieke sleutel. Afgevinkt als beide kloppen.
- [ ] DB-70 (hoog) Leg regels vast in de database: NOT NULL, CHECK, UNIQUE en foreign keys. Afgevinkt als de test voor de kerntabellen bestaat.
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
- [ ] INFRA-07 (hoog) Geef elke sleutel één doel en beperk automatiseringssleutels. Afgevinkt als elke automatiseringssleutel `restrict` heeft of de uitzondering is genoteerd.
- [ ] INFRA-11 (hoog) Zet beheerschermen niet open op internet. Afgevinkt met de lijst en de uitvoer.
- [ ] INFRA-50 (hoog) Vernieuw certificaten volledig automatisch. Afgevinkt als elke hostnaam een automatisch vernieuwd certificaat heeft.
- [ ] INFRA-55 (hoog) Versleutel en controleer elke verbinding die de host verlaat. Afgevinkt met de uitvoer.
- [ ] INFRA-56 (hoog) Publiceer precies één SPF-record dat eindigt op een harde weigering. Afgevinkt met de uitvoer en de headers.
- [ ] INFRA-57 (hoog) Onderteken elke verzendroute met DKIM en meet het aan echte mail. Afgevinkt met de headers per route.
- [ ] INFRA-58 (hoog) Zet DMARC op elk domein en kies het eindbeleid per soort mail. Afgevinkt met de uitvoer, een rapport en de vastgelegde keuze.
- [ ] INFRA-59 (middel) Sluit domeinen die niet mailen volledig af. Afgevinkt met de uitvoer per domein.
- [ ] INFRA-62 (hoog) Verwijder DNS-records voordat je de dienst erachter opheft. Afgevinkt met de lijst en de datum.
- [ ] INFRA-63 (hoog) Voldoe aan de eisen van grote ontvangers voordat je in aantallen mailt. Afgevinkt met de headers en het percentage.
- [ ] INFRA-64 (middel) Verstuur mail van een site of dienst via geauthenticeerde SMTP. [eigen bron] Afgevinkt met de headers.
- [ ] INFRA-69 (hoog) Laat elke geplande taak een fout melden en voorkom dubbel draaien. Afgevinkt met de lijst en de proefmelding.
- [ ] INFRA-72 (kritiek) Bewaar geheimen in bestanden met modus 600 buiten elke repository. Afgevinkt met de uitvoer.
- [ ] INFRA-76 (middel) Houd geheimen uit commandoregels, logs en shellgeschiedenis. Afgevinkt met de uitvoer.
- [ ] INFRA-77 (hoog) Geef elke dienst een eigen sleutel met de kleinste reikwijdte. Afgevinkt met de lijst.

### dicht-git
- [ ] GIT-01 (hoog) Eén sessie, één worktree, één branch. Afgevinkt met beide uitvoeren.
- [ ] GIT-03 (hoog) Valideer voordat je commit, merget of herstart. Afgevinkt met beide.
- [ ] GIT-04 (hoog) Stage alleen expliciete paden en lees wat je commit. Afgevinkt met de lijst.
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
- [ ] GIT-64 (middel) Draai een passieve ZAP-scan tegen de testomgeving. Afgevinkt met het rapport.
- [ ] GIT-65 (middel) Leg elke uitzondering vast met reden en einddatum. Afgevinkt met de bestanden.
- [ ] GIT-75 (hoog) Onderbouw elke nieuwe afhankelijkheid kort. Afgevinkt met de commit.
- [ ] GIT-78 (hoog) Controleer de naam van een pakket voordat je het installeert. Afgevinkt met die uitvoer.
- [ ] GIT-81 (hoog) Composer: lockfile committen, installeren zonder dev en zonder verrassingen. Afgevinkt met de drie.
- [ ] GIT-82 (hoog) Houd Composer zelf bij en laat de ingebouwde blokkades aan. Afgevinkt met de drie.
- [ ] GIT-83 (middel) Sta alleen benoemde Composer-plugins toe. Afgevinkt met de uitvoer.
- [ ] GIT-84 (hoog) Beoordeel een WordPress-plugin of thema van een ander vóór installatie. Afgevinkt met die notitie.
- [ ] GIT-93 (hoog) Gebruik alleen runtimes die nog beveiligingsfixes krijgen. Afgevinkt met de uitvoer.

### dicht-wordpress
- [ ] WP-01 (kritiek) Escape elke uitvoer laat, met de functie die bij de context hoort. Afgevinkt met de phpcs-uitvoer en de testuitvoer.
- [ ] WP-02 (hoog) Gebruik esc_url voor elke URL, ook in een attribuut. `grep -rnE "(href|src|action)=\"<\?php echo esc_attr" .` is leeg;
- [ ] WP-03 (hoog) Geef data aan JavaScript door als JSON met JSON_HEX_TAG of via de script-API. Afgevinkt met grep en test.
- [ ] WP-04 (hoog) Sta HTML alleen toe via wp_kses met een eigen, korte allowlist. Afgevinkt met de testuitvoer.
- [ ] WP-06 (hoog) Lees invoer in drie stappen: unslash, valideren, dan pas gebruiken. Afgevinkt met beide uitvoeren.
- [ ] WP-07 (middel) Zet wp_slash om de waarde bij het opslaan van meta en berichten. Afgevinkt met de testuitvoer.
- [ ] WP-09 (kritiek) Controleer een nonce op elke handler die iets wijzigt, en kijk naar de uitkomst. Afgevinkt met phpcs en de testuitvoer per handler.
- [ ] WP-10 (kritiek) Controleer de capability op het object, niet alleen op de rol. Afgevinkt als elke handler op de lijst een test heeft.
- [ ] WP-11 (kritiek) Gebruik is_admin() en admin_init nooit als rechtencontrole. Afgevinkt met de lijst en de testuitvoer.
- [ ] WP-12 (hoog) Registreer wp_ajax_nopriv alleen voor bewust publieke acties. Afgevinkt met de grep en de lijst.
- [ ] WP-13 (kritiek) Geef elke REST-route een permission_callback en een schema voor de argumenten. Afgevinkt met de drie uitvoeren.
- [ ] WP-14 (hoog) Gebruik voor REST de ingebouwde authenticatie en stuur de nonce als header. Afgevinkt met grep en de testaanvraag.
- [ ] WP-15 (middel) Reken bij anonieme bezoekers niet op de nonce. Afgevinkt met de testuitvoer.
- [ ] WP-16 (kritiek) Bouw elke query met een variabele via $wpdb->prepare, met kale placeholders. Afgevinkt met phpcs en testuitvoer.
- [ ] WP-17 (middel) Geef LIKE-patronen door als argument met esc_like. Afgevinkt met grep en test.
- [ ] WP-18 (hoog) Kies sorteerkolom en richting uit een vaste lijst. Afgevinkt met grep en test.
- [ ] WP-19 (hoog) Bouw een IN-lijst met gegenereerde placeholders. Afgevinkt met grep en een test met een lege en een gemanipuleerde lijst.
- [ ] WP-20 (hoog) Valideer ook wat je aan WP_Query en andere kernfuncties geeft. Afgevinkt met de nagelopen lijst.
- [ ] WP-22 (kritiek) Verwerk uploads via wp_handle_upload met een eigen typenlijst. Afgevinkt met grep, testuitvoer en een `find` op de uploadmap.
- [ ] WP-23 (hoog) Zet geen ongefilterde uploads aan en laat SVG en HTML dicht. Afgevinkt met de grep.
- [ ] WP-24 (hoog) Laat de uploadmap geen PHP uitvoeren en meet dat op de echte server. Afgevinkt met de curl-uitvoer en de datum.
- [ ] WP-26 (kritiek) Deserialiseer nooit invoer; gebruik JSON. Afgevinkt met de nagelopen lijst.
- [ ] WP-27 (hoog) Stuur door met wp_safe_redirect en stop daarna. Afgevinkt met phpcs, grep en test.
- [ ] WP-28 (hoog) Haal een URL van een gebruiker alleen op met wp_safe_remote_get, met een grens. Afgevinkt met grep en test.
- [ ] WP-29 (middel) Schrijf bestanden alleen in een eigen map onder uploads, met een zelfgekozen naam. Afgevinkt met grep en curl.
- [ ] WP-30 (hoog) Behandel shortcode-attributen als invoer van een gebruiker met weinig rechten. Afgevinkt met de testuitvoer.
- [ ] WP-32 (hoog) Registreer instellingen en meta met een sanitize- en een auth-callback. Afgevinkt met grep en curl.
- [ ] WP-34 (middel) Beheer een mu-plugin als code met een bron, een versie en een eigenaar. Afgevinkt met de uitvoer per site.
- [ ] WP-38 (kritiek) Geef elke installatie eigen sleutels en salts en wissel ze na elk incident. Afgevinkt met de uitvoer.
- [ ] WP-39 (hoog) Zet de bestandseditor in wp-admin uit. Afgevinkt met de uitvoer.
- [ ] WP-40 (hoog) Zet debug uit in productie en maak het foutlog onbereikbaar. Afgevinkt met de uitvoer.
- [ ] WP-41 (kritiek) Maak wp-config.php onleesbaar voor anderen en laat er geen kopieën van slingeren. Afgevinkt met de uitvoer.
- [ ] WP-42 (middel) Houd bestanden op 644 en mappen op 755, met het account als eigenaar. Afgevinkt met de uitvoer.
- [ ] WP-43 (hoog) Dwing HTTPS af voor de hele site en voor wp-admin. Afgevinkt met de uitvoer.
- [ ] WP-45 (hoog) Geef elke site een eigen database en een eigen databasegebruiker. Afgevinkt met de uitvoer per site.
- [ ] WP-68 (hoog) Draai WP-CLI als het account van de site, nooit als root. Afgevinkt met de grep.
- [ ] WP-69 (hoog) Onderzoek een verdachte site zonder zijn code te laden. Afgevinkt met het verslag.
- [ ] WP-71 (middel) Zet geen wachtwoorden of sleutels op de commandoregel. Afgevinkt met de grep.
- [ ] WP-81 (hoog) Geef WooCommerce REST-sleutels het minste recht en gebruik ze alleen over HTTPS. Afgevinkt met de lijst en de grep.
- [ ] WP-82 (hoog) Controleer de handtekening van een WooCommerce-webhook over de ruwe body. Afgevinkt met de testuitvoer.
- [ ] WP-83 (kritiek) Laat de betaalstatus van een bestelling alleen van de betaalprovider komen. Afgevinkt met grep en tests.

### dicht-ai-mcp
- [ ] AI-02 (kritiek) Geen agent met onvertrouwde invoer, gevoelige data en een uitweg tegelijk. [bron niet gelezen: AGENTIC] Afgevinkt met de tabel.
- [ ] AI-03 (hoog) Ken elke bron die in de context komt en geef hem een vertrouwensniveau. Afgevinkt als geen variabele ontbreekt.
- [ ] AI-04 (hoog) Lever onvertrouwde inhoud via een gescheiden, gelabeld kanaal. Afgevinkt met grep en testuitvoer.
- [ ] AI-06 (kritiek) Dwing autorisatie en beveiligingsbesluiten af in code, nooit in het model. [bron niet gelezen: AGENTIC] Afgevinkt als die test voor elke muterende tool in CI draait.
- [ ] AI-07 (hoog) Verwijder onzichtbare tekens bij inname en bij weergave. Afgevinkt met de testuitvoer.
- [ ] AI-10 (hoog) Schrijven naar geheugen of duurzame context is een geprivilegieerde handeling. [bron niet gelezen: AGENTIC] Afgevinkt met de testuitvoer en de bronkolom.
- [ ] AI-11 (hoog) Valideer modeluitvoer tegen een strikt schema in code. Afgevinkt met de testuitvoer.
- [ ] AI-12 (kritiek) Voer modeluitvoer nooit uit als code, query, commando of pad. [bron niet gelezen: AGENTIC] Afgevinkt met de grep-uitvoer en een verklaring per treffer.
- [ ] AI-13 (hoog) Render modeluitvoer als onvertrouwde inhoud. Afgevinkt met de testuitvoer en de header.
- [ ] AI-14 (kritiek) Laat gerenderde modeluitvoer geen verzoeken naar buiten doen. Afgevinkt met het netwerklog en de header.
- [ ] AI-15 (middel) Controleer elke link uit een model en open er nooit automatisch een. Afgevinkt met de testuitvoer en de grep.
- [ ] AI-18 (hoog) Feiten waar iemand op vertrouwt komen uit een bron, niet uit het model. Afgevinkt met de testuitvoer.
- [ ] AI-19 (hoog) Geef een agent alleen de tools die de taak nodig heeft. [bron niet gelezen: AGENTIC] Afgevinkt met de lijst en de testuitvoer.
- [ ] AI-21 (kritiek) De identiteit achter een tool heeft minimale rechten in het achterliggende systeem. [bron niet gelezen: AGENTIC] Afgevinkt met de uitvoer.
- [ ] AI-24 (kritiek) Een mens keurt elke onomkeerbare of naar buiten zichtbare actie goed, op de exacte inhoud. Afgevinkt met de lijst en beide testuitvoeren.
- [ ] AI-26 (hoog) Een automatische lijn heeft een plafond, een noodstop, een automatische pauze en een vaste vangrail. [bron niet gelezen: AGENTIC] Afgevinkt met vijf bewijzen per lijn.
- [ ] AI-28 (kritiek) Geheimen blijven in code en komen nooit in de context van het model. Afgevinkt met grep en testuitvoer.
- [ ] AI-31 (hoog) Begrens elke agentrun in stappen, tijd en kosten. Afgevinkt met de testuitvoer en de waarden.
- [ ] AI-55 (hoog) Beoordeel elke MCP-server voordat hij wordt aangesloten. [bron niet gelezen: AGENTIC] Afgevinkt met de lijst.
- [ ] AI-56 (hoog) Zet elke MCP-server vast op een versie. Afgevinkt met de grep-uitvoer.
- [ ] AI-57 (hoog) Controleer naam en uitgever letter voor letter. Afgevinkt met beide gegevens.
- [ ] AI-59 (hoog) Agentconfiguratie in een repository is code en wordt als code beoordeeld. [bron niet gelezen: AGENTIC] Afgevinkt met de uitvoer en een notitie.
- [ ] AI-60 (hoog) Tokens voor MCP-servers staan niet in platte tekst in bestanden die gedeeld, gevolgd of geback-upt worden. Afgevinkt met de drie uitvoeren.
- [ ] AI-61 (hoog) Elke server krijgt een eigen credential met de kleinste scope. Afgevinkt met de lijst.
- [ ] AI-62 (hoog) Lees een skill of plugin van een ander volledig, inclusief scripts, en zet netwerkaanroepen uit. [bron niet gelezen: AGENTIC] Afgevinkt met de grep-uitvoer en de notitie.
- [ ] AI-63 (hoog) Houd AI-gereedschap actueel en gebruik geen overbodige tussenlagen. Afgevinkt met de versies en de rooktest.
- [ ] AI-65 (hoog) Stuur alleen de velden naar een model die de taak nodig heeft. Afgevinkt met de testuitvoer.
- [ ] AI-67 (hoog) Behandel logs van prompts en antwoorden als de brongegevens zelf. Afgevinkt met de grep-uitvoer en de opruimjob.
- [ ] AI-72 (hoog) Bijzondere en zorggegevens gaan niet naar een model zonder vastgelegd besluit. [bron niet gelezen: NEN] Afgevinkt met de tabel en de testuitvoer.
- [ ] AI-73 (hoog) Zet een hard uitgavenplafond dat stopt, niet alleen waarschuwt. Afgevinkt met beide.
- [ ] AI-74 (hoog) Begrens per gebruiker de invoer, de uitvoer en het aantal aanroepen. Afgevinkt met de testuitvoer.
- [ ] AI-75 (kritiek) Een modelproxy of inferentie-eindpunt is nooit zonder authenticatie bereikbaar. Afgevinkt met de drie uitvoeren.

### dicht-privacy
- [ ] PRIV-14 (hoog) Geen echte persoonsgegevens naar een leverancier zonder verwerkersovereenkomst. Afgevinkt met de scriptuitvoer.
- [ ] PRIV-15 (hoog) Bied als verwerker zelf een overeenkomst aan, met een subverwerkerlijst die je bijhoudt. Afgevinkt met de lijst en, bij een wijziging, het bericht.
- [ ] PRIV-16 (hoog) Gebruik gegevens van klanten van klanten nooit voor eigen doelen. Afgevinkt met beide.
- [ ] PRIV-17 (hoog) Einde van de opdracht: teruggeven of wissen, ook de kopieën. Afgevinkt met de uitvoer van de proefrun.
- [ ] PRIV-18 (hoog) Leg per leverancier vast in welk land de gegevens komen en op grond waarvan. Afgevinkt met het register.
- [ ] PRIV-19 (middel) Een script, lettertype of ingesloten dienst van een derde is ook een ontvanger. Afgevinkt als geen host buiten die drie valt.
- [ ] PRIV-20 (middel) Toegang van de bouwer tot klantsystemen is persoonlijk, minimaal en gelogd. Afgevinkt met de zoekuitvoer.
- [ ] PRIV-22 (middel) Formulierinzendingen en bestellingen in WordPress krijgen een ingestelde termijn. Afgevinkt met instelling en telling.
- [ ] PRIV-25 (middel) Geef elke tijdelijke kopie een einddatum op het moment dat je hem maakt. Afgevinkt met de drie.
- [ ] PRIV-40 (hoog) Plaats of lees niets op het apparaat vóór toestemming, behalve wat strikt nodig is. Afgevinkt met de testuitvoer per paginatype.
- [ ] PRIV-41 (hoog) De regel geldt voor elke techniek, niet alleen voor cookies. Afgevinkt met de drie.
- [ ] PRIV-42 (hoog) Weigeren is even makkelijk als accepteren, en niets staat vooraf aan. Afgevinkt met de testuitvoer.
- [ ] PRIV-43 (hoog) De toestemmingsstatus stuurt de code, niet alleen de banner. Afgevinkt met de drie uitvoeren.
- [ ] PRIV-46 (middel) Laad ingesloten inhoud van derden pas na een klik. Afgevinkt met de testuitvoer.
- [ ] PRIV-49 (middel) Mail aan eigen klanten mag alleen voor eigen gelijksoortige producten en met afmelding vanaf het begin. Afgevinkt met test en query.
- [ ] PRIV-52 (hoog) Stel vast voor wie de zorgnormen wettelijk gelden, en wat de klant dus van jou gaat eisen. [bron niet gelezen: NEN] Afgevinkt als de kwalificatie er staat en door de klant of een jurist is bevestigd.
- [ ] PRIV-53 (kritiek) Tweefactorauthenticatie voor iedereen die bij patiëntgegevens kan. [bron niet gelezen: NEN] Afgevinkt met de testuitvoer.
- [ ] PRIV-54 (kritiek) Log elke inzage in een dossier, en bouw de controle op die logging mee. [bron niet gelezen: NEN] Afgevinkt met de drie.
- [ ] PRIV-55 (hoog) Bewaar de logging van zorgsystemen ten minste vijf jaar. [bron niet gelezen: NEN] Afgevinkt met de configuratie.
- [ ] PRIV-57 (hoog) Gebruik het BSN alleen als de wet het voorschrijft. Afgevinkt met de grep.
- [ ] PRIV-58 (hoog) Ruim een zorgdossier niet op met de gewone bewaartermijn. Afgevinkt met tabel en test.
- [ ] PRIV-65 (hoog) Stel per webwinkel of dienst vast of de toegankelijkheidswet geldt. Afgevinkt als het er staat.
- [ ] PRIV-66 (hoog) Bouw elke nieuwe site op WCAG 2.2 niveau AA. Afgevinkt met beide; een scan alleen vindt maar een deel van de criteria.
- [ ] PRIV-67 (hoog) Maak inloggen, beveiligingsstappen en betalen toegankelijk. Afgevinkt met de testuitvoer.
- [ ] PRIV-68 (middel) Lever een toegankelijkheidsverklaring mee en houd haar actueel. Afgevinkt met de URL en de testuitvoer.
- [ ] PRIV-79 (hoog) Zeg bij de eerste interactie dat iemand met een AI-systeem te maken heeft. Afgevinkt met de testuitvoer.
- [ ] PRIV-82 (middel) Maak bekend dat een deepfake of een ongecontroleerde publieke tekst door AI is gemaakt. Afgevinkt met de testuitvoer.
- [ ] PRIV-83 (hoog) Laat persoonsgegevens alleen naar een AI-dienst gaan die in het register staat. Afgevinkt met de grep en het register.
- [ ] PRIV-84 (kritiek) Laat kaartgegevens nooit door de eigen server of de eigen pagina-code lopen. [bron niet gelezen: PCI] Afgevinkt met beide.
- [ ] PRIV-85 (hoog) Bescherm de pagina die de betaalvelden insluit tegen vreemde scripts. [bron niet gelezen: PCI] Afgevinkt met hostlijst, header en lijst.
- [ ] PRIV-87 (hoog) Bij een eerste betaling met machtiging: toon wat en hoe vaak, en bewaar het bewijs. [bron niet gelezen: SEPA] Afgevinkt met test en schema.
- [ ] PRIV-88 (hoog) De bestelknop zegt dat er betaald moet worden, en de kerninformatie staat er direct boven. Afgevinkt met de testuitvoer.
- [ ] PRIV-89 (hoog) Bouw de herroepingsfunctie in elke webwinkel voor consumenten. Afgevinkt met de testuitvoer.
- [ ] PRIV-90 (middel) Bewaar de administratie zeven jaar, en alleen de administratie. Afgevinkt met tabel en test.

### dicht-architectuur
- [ ] ARCH-10 (middel) Houd ontwikkeling, test en productie gelijk in versies en soort diensten. Afgevinkt als de hoofdversies gelijk zijn.
- [ ] ARCH-33 (middel) Leg per project vast welke testlaag wat bewijst. Afgevinkt met het bestand en de uitvoer.
- [ ] ARCH-34 (hoog) Begin elke bugfix met een test die de fout laat zien. Afgevinkt met de twee uitvoeren.
- [ ] ARCH-36 (hoog) Bedien de pagina in e2e-tests met echte invoer. Afgevinkt met de grep.
- [ ] ARCH-38 (hoog) Test elke functie langs vaste assen, niet alleen het gelukkige pad. Afgevinkt als geen as leeg is zonder reden.
- [ ] ARCH-47 (hoog) Test een WordPress-plugin of thema in een wegwerpomgeving met twee rollen. Afgevinkt met de drie uitvoeren.
- [ ] ARCH-48 (hoog) Gebruik in tests alleen verzonnen gegevens. Afgevinkt met de grep.
- [ ] ARCH-49 (hoog) Geef tests eigen geheimen en houd inlogtoestanden uit git. Afgevinkt met de drie controles.
- [ ] ARCH-50 (hoog) Laat tests geen echte mail, betaling of oproep naar buiten sturen. Afgevinkt met de opzet en de grep.
- [ ] ARCH-51 (hoog) Beperk een test op productie tot lezen, of markeer en ruim op met exacte id's. [eigen bron] Afgevinkt met het script en de telling.
- [ ] ARCH-69 (hoog) Alarmeer op symptomen, met een drempel en een actie. Afgevinkt met de tabel en de proefmeldingen.
- [ ] ARCH-71 (middel) Deel logs in drie soorten in en geef elke soort een eigen termijn. [bron niet gelezen: NEN] Afgevinkt met inventaris en meting.

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
- [ ] SCR-10 (hoog) Behandel de opdracht achter `ssh` als tekst voor een tweede shell. Afgevinkt met de uitvoer.
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
- [ ] SCR-35 (middel) Maak een beveiligingslint een gate voor Python-scripts. Afgevinkt met de drie uitvoeren.
- [ ] SCR-37 (middel) Zet de omgeving die een cron-taak nodig heeft in het script zelf. Afgevinkt met de uitvoer van de proefrun.
- [ ] SCR-38 (hoog) Geef elke geplande run een harde time-out. Afgevinkt met de drie uitvoeren.
- [ ] SCR-40 (middel) Plan niets tussen 02:00 en 03:00 en reken in het script met een vaste tijdzone. Afgevinkt met de uitvoer.
- [ ] SCR-43 (middel) Laat een lus bij een fout trager gaan, nooit sneller. Afgevinkt met de testuitvoer.
- [ ] SCR-44 (hoog) Laat een taak die zichzelf opnieuw inplant eerst controleren of er al een exemplaar loopt. [eigen bron] Afgevinkt met de testuitvoer.
- [ ] SCR-45 (hoog) Leg de poging vast vóór het effect en behandel "onbekend" als "gebeurd". [eigen bron] Afgevinkt met de testuitvoer.
- [ ] SCR-46 (hoog) Controleer de schakelaar en het plafond vlak voor elke afzonderlijke actie, en faal gesloten. [eigen bron] Afgevinkt met de testuitvoer.
- [ ] SCR-47 (kritiek) Laat een leeg, mislukt of genegeerd filter nooit "alles" betekenen. [eigen bron] Afgevinkt met script en testuitvoer.
- [ ] SCR-52 (middel) Bewaak het tijdvenster in het script zelf, niet alleen in de planning. [eigen bron] Afgevinkt met de testuitvoer.
- [ ] SCR-53 (hoog) Stop een proces op proces-id of poort, nooit op een breed patroon. (1) `grep -rnE '\b(pkill|killall)\b' --include='*.sh' --include='*.py' .` geeft alleen regels met een pidbestand (`-F`), een ouder (`-P`) of een patroon met het volledige
- [ ] SCR-48 (middel) Stuur tekst naar een tmux-venster als letterlijke tekst en de Enter apart. Afgevinkt met beide uitvoeren.
- [ ] SCR-49 (hoog) Typ pas als het scherm in de verwachte toestand staat, en stop bij elk onbekend scherm. [eigen bron] Afgevinkt met de testuitvoer.
- [ ] SCR-50 (hoog) Geef een prompt met gegevens door via standaardinvoer of een bestand, nooit als argument. Afgevinkt met de drie uitvoeren.
- [ ] SCR-51 (hoog) Wie bij de tmux-socket of de lokale aansturing kan, bestuurt de agent. Afgevinkt met de drie controles.

### dicht-invoer
- [ ] INV-01 (kritiek) Zet in PHP geen parservlag die entiteiten of DTD's laadt. Afgevinkt met grep en testuitvoer.
- [ ] INV-02 (hoog) Leg in PHP een entiteit-lader vast die niets laadt, en reken niet op de globale stand. Afgevinkt met de drie uitvoeren.
- [ ] INV-03 (hoog) Zet in fast-xml-parser entiteiten uit voor XML van buiten en blijf op een gerepareerde versie. Afgevinkt met de drie uitvoeren.
- [ ] INV-04 (hoog) Behandel elk formaat met XML erin als XML. Afgevinkt met de lijst en de testuitvoer.
- [ ] INV-05 (hoog) Voer geen XSLT van gebruikers uit en geef een stylesheet geen PHP-functies. Afgevinkt met de grep.
- [ ] INV-06 (hoog) Bouw XML met een serializer, nooit met tekst aan elkaar. Afgevinkt met grep en test.
- [ ] INV-07 (middel) Zet geen invoer in een XPath-expressie. Afgevinkt met de grep.
- [ ] INV-08 (hoog) Parse JSON één keer en geef het geparste object door. Afgevinkt met grep en test.
- [ ] INV-09 (hoog) Stuur gehele getallen buiten het veilige bereik als tekst. Afgevinkt met grep en test.
- [ ] INV-10 (middel) Begrens de diepte van geneste invoer vóór eigen recursie. Afgevinkt met de test.
- [ ] INV-11 (middel) Laat json_decode in PHP een uitzondering gooien. Afgevinkt met grep en test.
- [ ] INV-12 (middel) Gebruik geen z.coerce op invoer zonder eerst de vorm te controleren. Afgevinkt met grep en test.
- [ ] INV-16 (hoog) Lees YAML alleen met een veilige lader zonder eigen types. Afgevinkt met beide uitvoeren.
- [ ] INV-17 (middel) Begrens aliassen en samenvoegingen in YAML van buiten. Afgevinkt met grep en test.
- [ ] INV-20 (middel) Lees een CSV-import strikt: UTF-8, vast scheidingsteken, limieten en een schema per rij. Afgevinkt met de testuitvoer.
- [ ] INV-21 (hoog) Gebruik het pakket xlsx niet vanaf npm. Afgevinkt met de uitvoer.
- [ ] INV-22 (hoog) Saneer als laatste stap en verander de uitvoer daarna niet meer. Afgevinkt met grep en test.
- [ ] INV-23 (hoog) Draai DOMPurify op de server alleen met een actuele jsdom. Afgevinkt met de uitvoer.
- [ ] INV-24 (hoog) Reken niet op de Markdown-renderer voor veiligheid. Afgevinkt met grep en test.
- [ ] INV-25 (hoog) Gebruik strip_tags en reguliere expressies niet als sanitizer. Afgevinkt met de nagelopen lijst.
- [ ] INV-27 (hoog) Geef ImageMagick een dichte policy voordat het bestanden van buiten ziet. Afgevinkt met de uitvoer.
- [ ] INV-28 (hoog) Laat de grenzen van sharp staan en zet een tijdslimiet. Afgevinkt met grep, versie en test.
- [ ] INV-29 (middel) Controleer in PHP de afmetingen vóór het decoderen en gebruik getimagesize niet als bewijs. Afgevinkt met grep en test.
- [ ] INV-30 (middel) Bewaar geen locatiegegevens in foto's die anderen kunnen zien. Afgevinkt met grep en de exiftool-uitvoer.
- [ ] INV-31 (hoog) Toon SVG van anderen alleen via een img-element. Afgevinkt met grep en curl.
- [ ] INV-32 (hoog) Zet SVG van anderen niet op de server om naar een rasterbeeld zonder afscherming. Afgevinkt met de testuitvoer, of met de vaststelling dat SVG-invoer wordt geweigerd.
- [ ] INV-33 (hoog) Behandel magic bytes als een hint en parse het bestand volledig. Afgevinkt met de testuitvoer.
- [ ] INV-34 (hoog) Geef PHP-bestandsfuncties nooit een pad met een schema uit invoer. Afgevinkt met grep en test.
- [ ] INV-35 (kritiek) Behandel HTML voor een PDF als code die in een browser op de server draait. Afgevinkt met test en grep.
- [ ] INV-36 (hoog) Start Chrome nooit met --no-sandbox. Afgevinkt met de drie uitvoeren.
- [ ] INV-37 (hoog) Gebruik wkhtmltopdf niet meer. Afgevinkt met beide uitvoeren.
- [ ] INV-38 (hoog) Houd dompdf dicht: geen externe bronnen, geen PHP in het document, een smalle chroot. Afgevinkt met de drie uitvoeren.
- [ ] INV-39 (hoog) Lees PDF's met pdf.js alleen vanaf 4.2.67 en met isEvalSupported uit. Afgevinkt met de drie uitvoeren.
- [ ] INV-41 (kritiek) Controleer elke naam in een archief voordat er een byte wordt geschreven. Afgevinkt met test, grep en versies.
- [ ] INV-42 (hoog) Weiger symlinks en hardlinks in een archief. Afgevinkt met de testuitvoer.
- [ ] INV-44 (middel) Begrens gedecomprimeerde omvang van aanvragen en antwoorden. Afgevinkt met grep en test.
- [ ] INV-45 (middel) Pak in WordPress uit met unzip_file en niet met een eigen ZipArchive-lus. Afgevinkt met grep en test.
- [ ] INV-46 (hoog) Gebruik extract, variabele variabelen en parse_str niet op invoer. Afgevinkt met de nagelopen lijst.
- [ ] INV-47 (kritiek) Geef WordPress-functies die gebruikers of berichten schrijven nooit de hele aanvraag. Afgevinkt met grep en test.
- [ ] INV-48 (middel) Weiger regeleinden en tekens buiten ASCII voordat een waarde in een antwoordkop komt. Afgevinkt met de uitvoer.
- [ ] INV-49 (hoog) Bouw uitgaande aanvragen met URL-objecten en vaste kopwaarden. Afgevinkt met grep en test.
- [ ] INV-50 (hoog) Gebruik in nginx geen $uri in een redirect, een kop of een doorgegeven adres. Afgevinkt met beide uitvoeren.
- [ ] INV-51 (hoog) Maak identifiers canoniek met één functie die bij herhaling niets meer verandert. Afgevinkt met grep, index en tests.
- [ ] INV-52 (middel) Vergelijk hoofdletterongevoelig via kleine letters, nooit via hoofdletters of de taalinstelling. Afgevinkt met grep en test.
- [ ] INV-53 (hoog) Sla domeinnamen op en vergelijk ze als A-label. Afgevinkt met query en test.
- [ ] INV-55 (hoog) Laat de build falen op bidi-stuurtekens in broncode. Afgevinkt met de uitvoer van een run met en zonder testbestand.
- [ ] INV-56 (middel) Weiger stuurtekens in velden van één regel. Afgevinkt met de test.
- [ ] INV-57 (middel) Weiger het NUL-teken en ongeldige Unicode aan de rand. Afgevinkt met de test.
- [ ] INV-58 (middel) Meet lengte in de eenheid van de opslag en kap nooit stil af. Afgevinkt met test, grep en de query.
- [ ] INV-59 (hoog) Ontleed een URL met één WHATWG-parser en gebruik daarna het ontlede object. Afgevinkt met grep en test.
- [ ] INV-60 (hoog) Neem in PHP geen beveiligingsbeslissing op parse_url. Afgevinkt met de nagelopen lijst.
- [ ] INV-61 (hoog) Controleer IP-adressen met de standaardbibliotheek, niet met het pakket ip. Afgevinkt met grep, `npm ls` en test.
- [ ] INV-62 (middel) Laat proxy en applicatie een pad op dezelfde manier lezen. Afgevinkt met grep en de curl-uitvoer.
- [ ] INV-63 (laag) Ontdoe zoektekst van LIKE-jokertekens. Afgevinkt met grep en test.
- [ ] INV-64 (hoog) Accepteer e-mailadressen alleen in de eenvoudige vorm en beslis niets op het domein van een onbevestigd adres. Afgevinkt met test en grep.
- [ ] INV-67 (middel) Behandel in PHP een lege aanvraag na een te grote upload als fout. Afgevinkt met grep en test.
- [ ] INV-68 (middel) Maak tijdelijke bestanden in een eigen, verse map met een onvoorspelbare naam. Afgevinkt met de vier uitvoeren.

### dicht-berichten
- [ ] MSG-01 (hoog) Zet in From alleen een adres op een eigen domein; de inzender hoort in Reply-To. Afgevinkt met grep en de ontvangen koppen.
- [ ] MSG-02 (hoog) Scheid transactiemail van reclame en koude mail op afzenderadres en domein. Afgevinkt met de tabel en de koppen.
- [ ] MSG-03 (middel) Onderteken zonder lengtelimiet en dek de koppen die de ontvanger ziet. Afgevinkt met de koppen per route.
- [ ] MSG-04 (middel) Bouw elk bericht met een bibliotheek, met één Message-ID, één Date en één From. Afgevinkt met de testuitvoer en de telling.
- [ ] MSG-05 (hoog) Controleer het certificaat op elke SMTP- en IMAP-verbinding. Afgevinkt met grep en de testuitvoer.
- [ ] MSG-06 (hoog) Houd de mailbibliotheek binnen de hersteltermijnen, juist bij meerdere tenants. Afgevinkt met de uitvoer en de datum.
- [ ] MSG-07 (hoog) Bouw afmelden in één klik precies volgens RFC 8058. Afgevinkt met de uitvoer, de query en de koppen.
- [ ] MSG-08 (middel) Meld niemand af op een GET. Afgevinkt met de twee query's.
- [ ] MSG-09 (hoog) Maak het afmeldadres onraadbaar en bind het aan één ontvanger en één lijst. Afgevinkt met de testuitvoer.
- [ ] MSG-11 (hoog) Lees een bounce als afleverrapport en stop na een blijvende fout. Afgevinkt met de testuitvoer.
- [ ] MSG-12 (middel) Geef elke stroom een afzender op de envelop die gelezen wordt. Afgevinkt met de kop en de logregel.
- [ ] MSG-49 (hoog) Ontdubbel ontvangers over alle verzendlijnen op genormaliseerd adres en domein. [eigen bron] Afgevinkt met de lijst en de testuitvoer.
- [ ] MSG-16 (kritiek) Geef invoer nooit door als afzender aan sendmail of mail(). Afgevinkt met grep en de testuitvoer.
- [ ] MSG-17 (hoog) Codeer elke variabele in een HTML-mailsjabloon. Afgevinkt met de testuitvoer.
- [ ] MSG-18 (hoog) Beslis op het adres dat de parser teruggeeft, met één parser voor de hele keten. Afgevinkt met de testuitvoer.
- [ ] MSG-19 (middel) Laat links in mail alleen naar het eigen domein wijzen, zonder open doorstuurder. Afgevinkt met grep en de uitvoer.
- [ ] MSG-22 (kritiek) Vertrouw From niet: beslis op het oordeel van je eigen ontvangende server. Afgevinkt met de testuitvoer.
- [ ] MSG-23 (kritiek) Toon HTML-mail alleen opgeschoond, in een sandbox zonder scripts en zonder verzoeken naar buiten. Afgevinkt met de testuitvoer en grep.
- [ ] MSG-24 (hoog) Begrens wat de parser van één bericht mag kosten. Afgevinkt met de testuitvoer.
- [ ] MSG-25 (hoog) Behandel een bijlage als een upload van een onbekende en pak niets automatisch uit. Afgevinkt met de testuitvoer en grep.
- [ ] MSG-26 (hoog) Zet geen invoer met een regeleinde in een IMAP- of SMTP-opdracht. Afgevinkt met de testuitvoer en grep.
- [ ] MSG-31 (hoog) Antwoord nooit automatisch op een automatisch bericht. Afgevinkt met de testuitvoer.
- [ ] MSG-32 (middel) Markeer elk automatisch verstuurd bericht. Afgevinkt met de koppen per stroom.
- [ ] MSG-35 (middel) Beantwoord het verificatieverzoek alleen bij het juiste token. [bron niet gelezen: META] Afgevinkt met de uitvoer.
- [ ] MSG-36 (kritiek) Controleer X-Hub-Signature-256 over de ruwe body met het app-geheim. [bron niet gelezen: META] Afgevinkt met de testuitvoer.
- [ ] MSG-37 (hoog) Ontdubbel op het bericht-ID; Meta biedt een melding tot 36 uur opnieuw aan. [bron niet gelezen: META] Afgevinkt met de testuitvoer.
- [ ] MSG-40 (middel) Zet bij elk bericht met inhoud van buiten uit wie er genoemd mag worden. Afgevinkt met de testuitvoer en grep.
- [ ] MSG-41 (hoog) Behandel een webhookadres en een bot-token als geheim. Afgevinkt met de uitvoer en het overzicht.
- [ ] MSG-42 (middel) Volg 429 en Retry-After, en blijf onder de grens voor ongeldige verzoeken. Afgevinkt met de testuitvoer.
- [ ] MSG-48 (middel) Zet geen gevoelige inhoud in een melding. Afgevinkt met de voorbeelden.

## Bouwen: richtlijnen (61)

### dicht-web
- [ ] WEB-14 (middel) Rol CSP uit via report-only en houd de rapportage aan. Afgevinkt met data en een voorbeeldmelding.
- [ ] WEB-18 (middel) Vraag HSTS-preload alleen bewust aan. Afgevinkt met de notitie.
- [ ] WEB-20 (laag) Schakel ongebruikte browserfuncties uit met Permissions-Policy. Afgevinkt met de header.
- [ ] WEB-28 (middel) Geef elke applicatie een eigen hostnaam. Afgevinkt met de lijst.
- [ ] WEB-70 (middel) Houd botbescherming en login toegankelijk. Afgevinkt met grep en test.

### dicht-api
- [ ] AUTH-07 (middel) Bewaar de hashparameters en herhash bij inloggen. Afgevinkt als de test groen is.
- [ ] AUTH-11 (middel) Voorkom dat een aanvaller accounts kan blokkeren. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-15 (middel) Meld verdachte logins en wijzigingen aan de gebruiker. Afgevinkt als de test groen is.
- [ ] AUTH-24 (middel) Begrens pushverzoeken en toegestuurde codes. Afgevinkt als de test groen is.
- [ ] AUTH-43 (hoog) Zet geen rechten in een langlevend token. Afgevinkt als de test groen is.
- [ ] AUTH-68 (middel) Onvoorspelbare id's zijn een extra laag, geen autorisatie. Afgevinkt als de lijst met zulke links gedocumenteerd is.
- [ ] API-45 (laag) Gebruik geen IP-lijst als controle op Mollie-webhooks. Geen allowlist voor Mollie in nginx of de firewall, of alleen als extra laag naast API-36.
- [ ] BIZ-45 (middel) WooCommerce: gebruik de ingebouwde voorraad- en bonlimieten en bouw ze niet na. `wp option get woocommerce_manage_stock` en `wp option get woocommerce_hold_stock_minutes` (alleen lezen) tonen "yes" en een getal.

### dicht-database
- [ ] DB-08 (middel) Zet search_path vast per rol. Afgevinkt als elke loginrol een expliciet `search_path` heeft en DB-04 is afgevinkt.
- [ ] DB-10 (laag) Begrens elke rol met een verbindingslimiet. Afgevinkt als geen applicatierol `-1` heeft en de som onder `max_connections` blijft.
- [ ] DB-28 (hoog) Geen dynamische SQL in databasefuncties. Afgevinkt als de lijst leeg is of elke treffer is beoordeeld.
- [ ] DB-35 (middel) Zet NOT NULL op een gevulde kolom via een gevalideerde CHECK. Afgevinkt als de `SET NOT NULL`-stap op de kopie binnen de `lock_timeout` blijft.
- [ ] DB-37 (middel) Voeg een unieke of primaire sleutel toe via een vooraf gebouwde index. Afgevinkt als beide stappen apart staan.
- [ ] DB-76 (middel) Kies sleutels bewust: wat naar buiten gaat is niet raadbaar en verraadt niets. Afgevinkt als externe id's UUID versie 4 zijn of de afwijking is toegelicht, en de autorisatietest uit domein AUTH bestaat.
- [ ] DB-77 (laag) Volg voor types en namen de skill postgresql-table-design. Afgevinkt als nieuwe tabellen de conventies volgen.
- [ ] DB-82 (middel) Weet wat schijfversleuteling wel en niet doet. Afgevinkt als de documentatie klopt met de werkelijkheid en met de teksten richting klanten.

### dicht-infra
- [ ] INFRA-09 (middel) Hergebruik één SSH-verbinding bij geautomatiseerd werk. Afgevinkt met het script of de opdrachttekst.
- [ ] INFRA-53 (middel) Leg met CAA vast wie certificaten mag uitgeven. Afgevinkt met de uitvoer en een geslaagde vernieuwing daarna.
- [ ] INFRA-60 (laag) Dwing TLS voor inkomende mail af met MTA-STS en vraag rapporten met TLS-RPT. Afgevinkt met de uitvoer.
- [ ] INFRA-61 (middel) Zet DNSSEC aan en houd twee werkende nameservers. Afgevinkt met de uitvoer.

### dicht-git
- [ ] GIT-08 (laag) Ruim worktrees en branches op zodra het werk gemerged is. Afgevinkt met beide uitvoeren.
- [ ] GIT-13 (middel) Laat elke wijziging lezen voordat hij live gaat. Afgevinkt met die notitie.
- [ ] GIT-37 (middel) Herschrijf de geschiedenis alleen als intrekken niet genoeg is. Afgevinkt met de vier.
- [ ] GIT-42 (hoog) Gebruik zo min mogelijk acties van derden en kijk wat ze zelf aanroepen. Afgevinkt met die lijst.
- [ ] GIT-49 (hoog) Geef CI geen sleutel tot productie. Afgevinkt met de uitvoer.
- [ ] GIT-55 (middel) Laat een bot niet zelf mergen zonder de gate en de wachttijd. Afgevinkt met de instelling en de regel.
- [ ] GIT-88 (hoog) Beveiligingsupdates direct, de rest na een wachttijd. Afgevinkt met beleid en logboek.

### dicht-wordpress
- [ ] WP-33 (middel) Bewaar geheimen in wp-config of de omgeving, niet in een optie die iedereen kan lezen. Afgevinkt met de drie uitvoeren.
- [ ] WP-35 (laag) Maak geplande taken herhaalbaar en reken niet op het tijdstip. Afgevinkt met de uitvoer.
- [ ] WP-46 (middel) Overweeg DISALLOW_UNFILTERED_HTML op sites met meer beheerders of redacteuren. Afgevinkt met de uitvoer of de notitie.
- [ ] WP-70 (middel) Weet dat wp eval een andere context heeft dan wp-admin. Afgevinkt met het script.
- [ ] WP-80 (middel) Gebruik multisite alleen voor sites van één eigenaar en beperk de superbeheerder. Afgevinkt met de uitvoer.

### dicht-ai-mcp
- [ ] AI-05 (middel) Zet het beleid in de systeemprompt, maar bouw er niets op. Afgevinkt met de lijst van verbodszin naar controle.
- [ ] AI-08 (middel) Behandel elke modaliteit en elk afgeleid tekstveld als invoer. Afgevinkt met de testuitvoer.
- [ ] AI-09 (middel) Een injectiefilter of bewakingsmodel is een extra laag, geen grens. Afgevinkt als beide aantoonbaar zijn.
- [ ] AI-20 (hoog) Bouw specifieke tools in plaats van open tools. Afgevinkt met de lijst.
- [ ] AI-27 (hoog) Een agent die commando's of code uitvoert, draait in een afgeschermde omgeving. [bron niet gelezen: AGENTIC] Voor elke agent die commando's uitvoert, is vastgelegd welke isolatie geldt (sandbox aan, container, aparte gebruiker) en welke mappen en hosts bereikbaar zijn.
- [ ] AI-58 (hoog) Lees de toolbeschrijvingen en merk het op als ze veranderen. [bron niet gelezen: AGENTIC] Afgevinkt met het opgeslagen bestand en de hash.

### dicht-privacy
- [ ] PRIV-24 (middel) Leg vast hoe een wisverzoek zich verhoudt tot back-ups. Afgevinkt met de passage en de teststap.
- [ ] PRIV-56 (middel) Bouw tegen de actuele uitgave van de normen en leg vast welke. [bron niet gelezen: NEN] Afgevinkt met de notitie.
- [ ] PRIV-69 (laag) Ken de uitzonderingen voor inhoud, en gebruik ze niet voor nieuwe inhoud. Afgevinkt met de lijst en een steekproef.
- [ ] PRIV-86 (middel) Behandel de betaalprovider als zelfstandige verantwoordelijke, en noem hem toch in het register. Afgevinkt met beide.

### dicht-architectuur
- [ ] ARCH-11 (middel) Zet beheertaken in de repository en draai ze tegen dezelfde release. Afgevinkt met commit en uitvoer.
- [ ] ARCH-37 (middel) Schrijf e2e-tests op wat de gebruiker ziet, en laat een fout in de console de test breken. Afgevinkt met de grep en de run.
- [ ] ARCH-39 (middel) Houd tests onafhankelijk en behandel een wankele test als een fout. Afgevinkt met de uitvoer.
- [ ] ARCH-46 (middel) Neem een toegankelijkheidsscan op in de e2e-tests. Afgevinkt met beide.

### dicht-scripts
Alleen als het project een script, een geplande taak of een lus bevat die in cron, een timer, een uitrol of een andere sessie draait; anders het hele blok `nvt` met die reden.
- [ ] SCR-17 (middel) Schrijf een bestand dat een ander proces leest atomair. Afgevinkt met de testuitvoer.

### dicht-invoer
- [ ] INV-14 (middel) Controleer in PHP dat een groot formulier volledig is aangekomen. Afgevinkt met test en waarde.
- [ ] INV-18 (middel) Valideer geparste YAML en TOML met een schema en reken niet op het geraden type. Afgevinkt met de test.
- [ ] INV-26 (middel) Beperk de sanitizer tot HTML als SVG en MathML niet nodig zijn. Afgevinkt met de grep.
- [ ] INV-40 (middel) Verwerk PDF's, Office-bestanden en beeld van buiten in een apart proces met grenzen. Afgevinkt met de test.
- [ ] INV-54 (middel) Weiger of markeer namen met gemengde schriftsoorten waar de naam vertrouwen draagt. Afgevinkt met de test, of met een vastgelegde reden waarom het voor dit project niet speelt.

### dicht-berichten
- [ ] MSG-13 (middel) Behandel een klacht als een afmelding. Afgevinkt met de aanmelding en de testuitvoer.
- [ ] MSG-15 (middel) Bouw volume geleidelijk op en verlaag het bij uitstel of weigering. Afgevinkt met de configuratie en een dagtelling.
- [ ] MSG-20 (middel) Vraag in een mail nooit om een wachtwoord of betaalgegevens, en zeg dat ook. Afgevinkt met grep en het sjabloon.
- [ ] MSG-34 (middel) Stuur een automatisch antwoord hooguit één keer per afzender per zeven dagen, naar het envelopadres. Afgevinkt met de testuitvoer.

## Vóór oplevering: hard (76)

### dicht-web
- [ ] WEB-71 (hoog) Gebruik robots.txt nooit als afscherming. Afgevinkt met de drie uitvoeren.
- [ ] WEB-72 (middel) Zet test-, staging- en demo-omgevingen achter een login en op noindex. Afgevinkt met de uitvoer.

### dicht-api
- [ ] BIZ-51 (middel) Leg per geldstroom de invarianten vast als query en draai ze in de test en dagelijks. Het bestand met invarianten staat in de repository naast het threat model (ARCH-82).
- [ ] BIZ-52 (middel) Test geld en tijd met een vaste tabel van grensgevallen. De tabel staat als geparametriseerde test in de repository (`it.each`).

### dicht-git
- [ ] GIT-87 (hoog) Controleer core en plugins tegen de controlesommen van wordpress.org. Afgevinkt met de uitvoer.

### dicht-wordpress
- [ ] WP-55 (hoog) Zet XML-RPC dicht op de server, tenzij een dienst het nodig heeft. Afgevinkt met de curl-uitvoer.
- [ ] WP-56 (middel) Geef geen gebruikersnamen weg. Afgevinkt met de uitvoer.
- [ ] WP-57 (hoog) Begrens inlogpogingen op elk inlogpad. Afgevinkt met de uitvoer per pad.
- [ ] WP-58 (hoog) Verplicht een tweede factor voor elke beheerder. Afgevinkt met de uitvoer en één testinlog.
- [ ] WP-59 (middel) Houd het aantal beheerders klein en ruim accounts op. Afgevinkt met de uitvoer en de datum.
- [ ] WP-60 (middel) Beheer applicatiewachtwoorden per koppeling en trek ongebruikte in. Afgevinkt met de uitvoer.
- [ ] WP-62 (hoog) Vraag bij elke oplevering de bekende WordPress-paden zelf op. Afgevinkt met beide uitvoeren.
- [ ] WP-63 (kritiek) Laat een back-up nooit in de webroot staan. Afgevinkt met beide uitvoeren.
- [ ] WP-64 (hoog) Bewijs elke blokkade met een anonieme aanvraag op de echte server. Afgevinkt met die uitvoer.
- [ ] WP-65 (middel) Zet eigen regels buiten het blok dat WordPress beheert. Afgevinkt met de uitvoer.
- [ ] WP-66 (kritiek) Sluit ingelogde en persoonlijke pagina's uit van de paginacache en meet het. Afgevinkt met de uitvoer van de drie metingen.
- [ ] WP-67 (middel) Laat een gecachte pagina geen verlopen nonce uitleveren. Afgevinkt met de testuitvoer.
- [ ] WP-85 (hoog) Doe een nulmeting voordat je een bestaande site in beheer neemt. [eigen bron] Afgevinkt met de notitie.
- [ ] WP-86 (middel) Sluit elke klus op een klantsite af met een korte controle en een notitie. [eigen bron] Afgevinkt met de uitvoer en de notitie.

### dicht-ai-mcp
- [ ] AI-77 (middel) Zet het model vast op een exacte versie; een modelwissel is een release. Afgevinkt met de grep en de tabel.
- [ ] AI-78 (hoog) Een vaste eval is een gate bij elke wijziging van prompt, model, tools of leverancier. Afgevinkt met de laatste evaluitvoer.
- [ ] AI-79 (hoog) Elke AI-functie en elke agent is zonder deploy uit te zetten. Afgevinkt met de testuitvoer.
- [ ] AI-80 (hoog) Faal gesloten als het model uitvalt of iets onverwachts teruggeeft. Afgevinkt met de testuitvoer.
- [ ] AI-81 (hoog) Injectietests per invoerkanaal zijn een gate. Afgevinkt met de CI-uitvoer.
- [ ] AI-83 (middel) Bewaak verbruik, weigeringen en afwijkend toolgebruik, met een alarm. Afgevinkt met het overzicht en de ontvangen melding.
- [ ] AI-85 (hoog) Code die een model schreef, gaat door dezelfde gates, en elk voorgesteld pakket wordt gecontroleerd. Afgevinkt met de CI-uitvoer en de onderbouwing.
- [ ] AI-86 (hoog) Wat een agent op een klantsite of in een vreemde repository leest, is onvertrouwd. [bron niet gelezen: AGENTIC] Afgevinkt met de notitie bij de klus.

### dicht-privacy
- [ ] PRIV-45 (middel) De cookielijst in de verklaring is de gemeten lijst. Afgevinkt met de vergelijking.

### dicht-architectuur
- [ ] ARCH-27 (hoog) Rol een wijziging die veel sites of tenants raakt in stappen uit. Afgevinkt met die lijst.
- [ ] ARCH-28 (kritiek) Geef elk script dat veel wijzigt of verwijdert een proefstand, exacte doelen en een grens. Afgevinkt met script en beide uitvoeren.
- [ ] ARCH-52 (hoog) Een bouwtaak is klaar als de checklist van het projecttype is afgevinkt met bewijs. Afgevinkt als geen punt leeg is.
- [ ] ARCH-53 (middel) Schrijf het bewijs in één bestand met een vaste vorm. Afgevinkt met die vier controles.
- [ ] ARCH-54 (hoog) Laat elke wijziging aan een kritiek deel nakijken door een tweede paar ogen. Afgevinkt met de notitie.
- [ ] ARCH-74 (middel) Houd de Core Web Vitals op het 75e percentiel binnen de drempels. Afgevinkt met de labrapporten bij oplevering en de velddata bij de eerste controle daarna.
- [ ] ARCH-84 (middel) Bouw per projecttype één auditscript dat het bewijs verzamelt. Afgevinkt met de uitvoer van de proef.
- [ ] ARCH-85 (hoog) Laat een auditscript alleen lezen, begrensd en zonder geheimen in de uitvoer. [eigen bron] Afgevinkt met de drie controles.
- [ ] ARCH-86 (middel) Lever de audit van een bestaand project op als lijst van bevindingen, niet als herstel. Afgevinkt met rapport en status.

### dicht-anti-vibe
- [ ] VIBE-01 (hoog) Geen placeholdertekst, voorbeeldinhoud of tool-URL in productie. Afgevinkt met de uitvoer.
- [ ] VIBE-02 (hoog) Geen nepcijfers, neplogo's, nepbadges of nepreviews. Afgevinkt met die lijst.
- [ ] VIBE-03 (hoog) Elke link werkt. Afgevinkt met de uitvoer.
- [ ] VIBE-04 (middel) Social-links werken, of het icoon staat er niet. Afgevinkt met de uitvoer.
- [ ] VIBE-05 (laag) Het copyright-jaar is actueel en wordt berekend. Afgevinkt met beide uitvoeren.
- [ ] VIBE-06 (middel) Echte SVG-iconen, geen emoji als icoon. Afgevinkt met de uitvoer.
- [ ] VIBE-07 (hoog) Logo, telefoonnummer en e-mailadres zijn klikbaar. Afgevinkt met de uitvoer.
- [ ] VIBE-08 (middel) De inhoud uit de intake staat erop. Afgevinkt met beide.
- [ ] VIBE-09 (middel) Geen lege of losse pagina's; een logische linkstructuur. Afgevinkt met de uitvoer.
- [ ] VIBE-10 (hoog) Elke knop en CTA doet iets. Afgevinkt met de uitvoer.
- [ ] VIBE-11 (hoog) Elk formulier toont na verzenden een melding op de pagina. Afgevinkt met de testuitvoer.
- [ ] VIBE-12 (hoog) Elk formulier toont een foutmelding per veld. Afgevinkt met de testuitvoer.
- [ ] VIBE-14 (hoog) Geen fouten in de console. Afgevinkt met de uitvoer.
- [ ] VIBE-43 (middel) Een veld voor een eenmalige code heeft autocomplete="one-time-code". Afgevinkt met de uitvoer of de grep.
- [ ] VIBE-15 (hoog) Geen horizontale scroll op 320, 360 en 390 px. Afgevinkt met de uitvoer.
- [ ] VIBE-16 (hoog) Het mobiele menu werkt, ook met het toetsenbord. Afgevinkt met de uitvoer.
- [ ] VIBE-17 (middel) De testronde scrollt elke pagina echt door, op elk formaat. Afgevinkt met de uitvoer en de bekeken beelden.
- [ ] VIBE-37 (middel) Klikdoelen zijn minstens 24 bij 24 px, of hebben genoeg ruimte. Afgevinkt met de uitvoer.
- [ ] VIBE-38 (middel) Een submenu blijft open als de muis er recht naartoe gaat. Afgevinkt met de uitvoer.
- [ ] VIBE-40 (middel) viewport-fit=cover alleen samen met safe-area-insets. Afgevinkt met beide.
- [ ] VIBE-18 (middel) Afbeeldingen zijn gecomprimeerd, passend en lazy onder de vouw. Afgevinkt met de uitvoer.
- [ ] VIBE-19 (middel) Scripts en stijlen: uitgesteld, geminificeerd, zonder source maps. Afgevinkt met de uitvoer.
- [ ] VIBE-20 (middel) Paginacache en compressie staan aan en zijn gemeten. Afgevinkt met de uitvoer.
- [ ] VIBE-21 (middel) Geen ongebruikte plugins of afhankelijkheden; lange lijsten gepagineerd. Afgevinkt met de uitvoer.
- [ ] VIBE-22 (middel) Een Lighthouse-audit per hoofdpagina, met de scores vastgelegd. Afgevinkt met de uitvoer.
- [ ] VIBE-23 (hoog) De HTML-bron toont de echte inhoud. Afgevinkt met de uitvoer.
- [ ] VIBE-24 (hoog) Elke pagina heeft een eigen titel en beschrijving en precies één H1. Afgevinkt met de uitvoer.
- [ ] VIBE-25 (middel) Canonical en og:image op elke pagina. Afgevinkt met de uitvoer.
- [ ] VIBE-26 (middel) Het lang-attribuut klopt met de taal van de pagina. Afgevinkt met beide.
- [ ] VIBE-27 (middel) Elke afbeelding heeft een alt-attribuut. Afgevinkt met de uitvoer.
- [ ] VIBE-28 (middel) Structured data staat erop en is geldig. Afgevinkt met beide.
- [ ] VIBE-29 (middel) sitemap.xml, robots.txt en llms.txt kloppen. Afgevinkt met de uitvoer.
- [ ] VIBE-30 (laag) Er is een favicon, en het hoort bij het thema. Afgevinkt met beide.
- [ ] VIBE-31 (middel) Een eigen 404-pagina die 404 geeft. Afgevinkt met de uitvoer.
- [ ] VIBE-32 (hoog) De verplichte pagina's staan erop. Afgevinkt met de uitvoer en die regels.
- [ ] VIBE-33 (middel) Analytics meet en Search Console verifieert de site. Afgevinkt met beide.
- [ ] VIBE-34 (middel) Standaardinhoud en versiebestanden zijn weg. [alleen: wordpress] Afgevinkt met beide.
- [ ] VIBE-35 (middel) Geen query in een lus in eigen thema- of mu-plugin-code. [alleen: wordpress] Afgevinkt met de getallen.
- [ ] VIBE-36 (hoog) Loop beheer, anti-spam en blootstelling na volgens de regels die er al zijn. Afgevinkt met alle drie.

## Vóór oplevering: richtlijnen (8)

### dicht-wordpress
- [ ] WP-61 (middel) Zet de REST API niet uit; beperk wat anoniem zichtbaar is. Afgevinkt met de lijst en de testinzendingen.

### dicht-ai-mcp
- [ ] AI-84 (middel) Heb een draaiboek voor een AI-incident. Afgevinkt met het document en de oefennotitie.

### dicht-privacy
- [ ] PRIV-91 (middel) Loop bij een voorkant voor bezoekers de juridische checkvragen langs en laat elke twijfel controleren. [eigen bron] Afgevinkt met die lijst.

### dicht-architectuur
- [ ] ARCH-87 (middel) Rol uit op een moment waarop je na een uur nog kunt nameten en terugdraaien. [eigen bron] Afgevinkt met beide tijdstippen.

### dicht-anti-vibe
- [ ] VIBE-13 (laag) Laden toont een skeleton, geen spinner. Afgevinkt met beide.
- [ ] VIBE-39 (laag) Een submenu blijft open op de schuine weg ernaartoe. Afgevinkt met de uitvoer.
- [ ] VIBE-41 (laag) Cijfers in een tabel zijn even breed. Afgevinkt met de uitvoer.
- [ ] VIBE-42 (laag) Koppen over meer regels zijn gebalanceerd. Afgevinkt met de uitvoer.

## Na oplevering en beheer: hard (70)

### dicht-api
- [ ] AUTH-02 (middel) Geen samenstellingsregels en geen verplichte periodieke wissel. [alleen: met login] Afgevinkt met de test uit AUTH-01 (wachtwoord van 15 kleine letters wordt geaccepteerd).
- [ ] AUTH-85 (hoog) Offboarding: toegang van mensen en systemen direct weg. Afgevinkt als de test groen is en de laatste controle minder dan een kwartaal oud is.
- [ ] API-43 (hoog) Stem dagelijks af wat de webhook kan hebben gemist. De taak bestaat (cron of worker), heeft een droge modus, logt hoeveel betalingen hij alsnog verwerkte en alarmeert bij meer dan nul.
- [ ] BIZ-31 (middel) Laat een periodieke taak zijn werk afleiden uit de toestand, niet uit de datum van vandaag. Test: sla in de test één run over (zet de klok twee dagen vooruit);
- [ ] BIZ-47 (hoog) Opzeggen, terugbetalen en stoppen raken elk systeem dat de klant kent. Test met nagebootste diensten: na `beeindig()` staan er taken voor Mollie, Moneybird en de leverancier, elk idempotent (BIZ-41) en met de uitkomst "onbekend" afgehandeld 
- [ ] BIZ-48 (hoog) Stem elke dag in drie richtingen af en alarmeer op elk verschil. De taak bestaat, draait dagelijks, en schrijft per controle het aantal vergeleken en het aantal afwijkende rijen.

### dicht-database
- [ ] DB-44 (kritiek) Maak dagelijks een automatische back-up van elke database en van de globale objecten. [bron niet gelezen: NEN] Afgevinkt als elke database een bestand van minder dan 26 uur oud heeft en er een globals-bestand is.
- [ ] DB-45 (hoog) Versleutel elke back-up voordat hij op schijf staat. Afgevinkt als geen enkele back-up leesbaar is zonder sleutel.
- [ ] DB-46 (kritiek) Doe een herstelproef met datum, minstens elk kwartaal. [bron niet gelezen: NEN] Afgevinkt als de laatste regel per database jonger is dan 92 dagen en de tellingen kloppen.
- [ ] DB-47 (hoog) Een mislukte of ontbrekende back-up geeft alarm. Afgevinkt als een proef (back-up een dag overslaan in een testomgeving, of de controle draaien tegen een lege map) een melding geeft.
- [ ] DB-48 (hoog) Dump met een pg_dump van dezelfde major als de server. Afgevinkt als dat zo is.
- [ ] DB-49 (hoog) Bewaar een versleutelde kopie buiten de server. Afgevinkt als beide kloppen.
- [ ] DB-53 (hoog) Elke database heeft een herstelplan met RPO en RTO. [bron niet gelezen: NEN] Afgevinkt als alle vier waar zijn.
- [ ] DB-54 (middel) Herstel alleen dumps uit een vertrouwde bron. Afgevinkt als het runbook de stap bevat en de client de actuele minor heeft (DB-92).
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
- [ ] INFRA-24 (hoog) Volg de advisories van wat je draait en leg termijnen vast. Afgevinkt met de lijst en de termijnen.
- [ ] INFRA-52 (hoog) Bewaak de vervaldatum van buitenaf. Afgevinkt met schermafdruk of uitvoer en de testmelding.
- [ ] INFRA-75 (hoog) Oefen het vervangen van een geheim voordat het nodig is. Afgevinkt met de lijst.
- [ ] INFRA-79 (kritiek) Bewaar drie kopieën op twee soorten opslag, waarvan één buiten de server. Afgevinkt als elke dataset een kopie buiten de server heeft die jonger is dan het afgesproken verlies (INFRA-84).
- [ ] INFRA-82 (kritiek) Doe elk kwartaal een herstelproef op een lege machine. Afgevinkt als het verslag jonger is dan drie maanden.
- [ ] INFRA-84 (middel) Leg per dienst vast hoeveel verlies en uitval aanvaardbaar is. [bron niet gelezen: WET] Afgevinkt met de tabel.
- [ ] INFRA-86 (hoog) Bewaak de bereikbaarheid vanaf een plek buiten de server. Afgevinkt met de lijst en de proefmelding.
- [ ] INFRA-91 (hoog) Schrijf het draaiboek voordat er iets gebeurt. Afgevinkt met het document en de datum.
- [ ] INFRA-92 (hoog) Isoleer eerst en bewaar bewijs voordat je opruimt. Afgevinkt met het verslag.
- [ ] INFRA-93 (kritiek) Vervang na een inbraak elk geheim dat de getroffen omgeving kon lezen. Afgevinkt met de lijst.
- [ ] INFRA-94 (hoog) Herbouw vanaf een schone bron; ruim alleen op met volledige controle. Afgevinkt met het verslag.
- [ ] INFRA-96 (kritiek) Beoordeel bij elk incident met persoonsgegevens direct de meldplicht. [bron niet gelezen: WET] Afgevinkt met het verslag.
- [ ] INFRA-97 (hoog) Geef elke site een eigen systeemgebruiker en een eigen database. Afgevinkt met de lijst en de proef.
- [ ] INFRA-98 (kritiek) Bescherm het panel met een tweede factor en beperk API-tokens. Afgevinkt met de lijst en de proef.
- [ ] INFRA-99 (hoog) Weet voor elke ingreep welke back-up je terugweg is. [eigen bron] Afgevinkt met de uitvoer.
- [ ] INFRA-100 (hoog) Controleer elke beheerde site dagelijks op wijzigingen en bekende sporen. [eigen bron] Afgevinkt met de vergelijking, het log en de proef.
- [ ] INFRA-101 (hoog) Test elke afscherming op de webserver die er echt draait. [eigen bron] Afgevinkt met de uitvoer.
- [ ] INFRA-103 (middel) Ruim op wat een project op de hosting achterlaat. Afgevinkt met de uitvoer.
- [ ] INFRA-104 (hoog) Meet dat updates op een klantsite echt worden toegepast. [eigen bron] Afgevinkt met de uitvoer.

### dicht-git
- [ ] GIT-09 (hoog) Elke repo met waarde heeft een kopie buiten de server. Afgevinkt met uitvoer en datum.
- [ ] GIT-76 (middel) Laat Dependabot versies bijwerken, gegroepeerd en met wachttijd. Afgevinkt met bestand en uitvoer.
- [ ] GIT-86 (hoog) Houd per site een inventaris bij en vervang wat gesloten of verlaten is. Afgevinkt met de uitvoer.

### dicht-wordpress
- [ ] WP-47 (kritiek) Laat beveiligingsupdates van de kern automatisch installeren en controleer dat het gebeurt. Afgevinkt met de uitvoer per site.
- [ ] WP-48 (hoog) Controleer dat niets updates tegenhoudt of verbergt. Afgevinkt met de vier uitvoeren.
- [ ] WP-49 (hoog) Leg termijnen vast voor updates van plugins en thema's en houd je eraan. Afgevinkt met de uitvoer en de datum van de laatste run.
- [ ] WP-50 (middel) Lees het getroffen versiebereik voordat je ingrijpt. Afgevinkt met de notitie in de taak.
- [ ] WP-51 (hoog) Verwijder plugins en thema's die niet in gebruik zijn. Afgevinkt met de uitvoer.
- [ ] WP-52 (hoog) Draai op een PHP-versie die nog beveiligingsupdates krijgt. Afgevinkt met beide waarden.
- [ ] WP-53 (middel) Zorg vóór elke update voor een terugweg. Afgevinkt met tijdstip en uitvoer.
- [ ] WP-73 (kritiek) Haal plugins en thema's alleen van de maker of van wordpress.org. Afgevinkt met de lijst en de uitvoer.
- [ ] WP-74 (hoog) Houd Elementor en andere paginabouwers strak bij en beperk wie ermee mag werken. Afgevinkt met de uitvoer.
- [ ] WP-75 (hoog) Behandel een plugin voor beheer op afstand als een beheerderssleutel. Afgevinkt met de uitvoer.
- [ ] WP-76 (hoog) Gebruik geen plugins die code uit de database uitvoeren of bestanden beheren. Afgevinkt met de pluginlijst.
- [ ] WP-77 (hoog) Zoek malware met meer dan één signaal. Afgevinkt met de uitvoer en de lijst van verklaringen.
- [ ] WP-78 (kritiek) Herstel een gehackte site in een vaste volgorde. Afgevinkt met het verslag.
- [ ] WP-79 (kritiek) Wissel na een inbraak elke sleutel die de site kende. Afgevinkt met de lijst.

### dicht-privacy
- [ ] PRIV-26 (hoog) Een inzageverzoek is binnen een maand te beantwoorden met een getest script. Afgevinkt met de testuitvoer.
- [ ] PRIV-27 (hoog) Controleer de identiteit van een verzoeker zonder kopie van een identiteitsbewijs. Afgevinkt met procedure en test.
- [ ] PRIV-28 (hoog) Bezwaar tegen direct marketing werkt direct en blijvend. Afgevinkt met de testuitvoer.
- [ ] PRIV-30 (middel) Geef als verwerker de klant het gereedschap om verzoeken af te handelen. Afgevinkt met grep en test.
- [ ] PRIV-31 (kritiek) Meld een datalek binnen 72 uur na kennisname, ook als het onderzoek nog loopt. Afgevinkt als het document bestaat en één keer is doorgelopen met een oefengeval.
- [ ] PRIV-32 (kritiek) Informeer als verwerker de klant direct, en leg de termijn vast in de overeenkomst. Afgevinkt met de drie.
- [ ] PRIV-33 (hoog) Registreer elk datalek, ook als je het niet meldt. Afgevinkt als het bestand bestaat (ook als het leeg is) en in het draaiboek genoemd wordt.
- [ ] PRIV-34 (hoog) Zorg dat je kunt vaststellen of er toegang is geweest. Afgevinkt met overzicht en proef.
- [ ] PRIV-35 (hoog) Informeer betrokkenen bij een hoog risico, en weet wanneer versleuteling dat voorkomt. Afgevinkt met beide.

### dicht-invoer
- [ ] INV-69 (middel) Ruim tijdelijke bestanden op bij elke afloop en begrens de ruimte. Afgevinkt met de testuitvoer en de configuratie.

## Na oplevering en beheer: richtlijnen (9)

### dicht-database
- [ ] DB-50 (middel) Gebruik het custom-formaat en herstel met stop-bij-fout. Afgevinkt als de proef zonder fouten eindigt.
- [ ] DB-56 (middel) Zet data-checksums aan bij een nieuw cluster. Afgevinkt als dat zo is voor nieuwe clusters; voor bestaande clusters is het een verbeterpunt bij de volgende major upgrade.
- [ ] DB-90 (middel) Log trage queries, lock-wachttijden en verbindingen. Afgevinkt als ze zijn ingesteld en het log binnen de bewaartermijn van INFRA valt.

### dicht-infra
- [ ] INFRA-25 (middel) Haal weg wat niet nodig is. Afgevinkt met de vergelijking.
- [ ] INFRA-85 (middel) Reken een snapshot van de hostingpartij niet als de enige back-up. Afgevinkt met beide.
- [ ] INFRA-95 (middel) Leg tijdens het incident vast wat je doet en evalueer daarna. Afgevinkt met het verslag.
- [ ] INFRA-102 (middel) Weet vooraf wie de logs en de firewall van de hosting beheert. [eigen bron] Afgevinkt met de tabel.

### dicht-wordpress
- [ ] WP-54 (middel) Volg beveiligingsnieuws automatisch en laat het op de eigen sites toetsen. Afgevinkt met de logregels.

### dicht-privacy
- [ ] PRIV-36 (laag) Spreek vooraf af of de verwerker namens de klant mag melden. Afgevinkt met het document.
