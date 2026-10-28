# Checklist wp-plugin

481 regels: 434 hard, 47 richtlijn. Gemaakt door `tools/bouw.py` uit het veld "Geldt voor"; niet met de hand wijzigen.
Elk punt: ID (ernst) titel, en wat telt als afgevinkt. Het volledige bewijs staat in de referentie van de sub-skill. Een punt dat in dit project niet speelt krijgt in het bewijsbestand `nvt` met een reden.

## Ontwerp: hard (49)

### dicht-api
- [ ] AUTH-64 (kritiek) Bescherm elke functie, ook via een andere methode of een ander pad. Afgevinkt als de matrix alle routes dekt.
- [ ] API-25 (hoog) Houd een inventaris bij en zet niets in productie wat er niet hoort. `app.printRoutes()` of de OpenAPI-uitvoer in CI wordt vergeleken met de vastgelegde lijst;
- [ ] BIZ-15 (hoog) Begrens terugbetalingen in je eigen boek voordat je Mollie aanroept. Test met 20 gelijktijdige gedeeltelijke terugbetalingen die samen meer zijn dan de betaling: de som in de eigen tabel blijft binnen het betaalde bedrag en de nagebootste 
- [ ] BIZ-18 (hoog) Pas 0 procent of verlegde btw alleen toe op bewijs dat de server zelf heeft gecontroleerd. Test: een bestelling met een btw-nummer dat de nagebootste VIES-dienst afkeurt, krijgt het gewone tarief;
- [ ] BIZ-35 (middel) Bind een eenmalig voordeel aan iets stabielers dan een e-mailadres. De documentatie noemt per voordeel de sleutel.

### dicht-database
- [ ] DB-83 (hoog) Elke tabel met persoonsgegevens heeft een bewaartermijn en een opruimjob. Afgevinkt als alle drie kloppen.

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

### dicht-wordpress
- [ ] WP-25 (kritiek) Lees een bestand of sjabloon nooit in op basis van invoer. Afgevinkt met grep en test.

### dicht-privacy
- [ ] PRIV-01 (hoog) Leg per project vast wie verantwoordelijke en wie verwerker is. Afgevinkt als elke tabel met persoonsgegevens uit de classificatie (DB-87) in precies één rij valt.
- [ ] PRIV-02 (hoog) Het verwerkingsregister bevat per activiteit de wettelijke velden. Afgevinkt met de uitvoer.
- [ ] PRIV-03 (hoog) Werk het register bij in dezelfde wijziging als de nieuwe gegevensstroom. Afgevinkt met de vergelijking.
- [ ] PRIV-07 (hoog) Geen verwerking zonder vastgelegde grondslag. Afgevinkt met de scriptuitvoer.
- [ ] PRIV-08 (middel) Vraag per veld alleen wat het doel nodig heeft. Afgevinkt met tabel en grep.
- [ ] PRIV-09 (middel) De standaardinstelling is de zuinigste. Afgevinkt met de testuitvoer.
- [ ] PRIV-10 (hoog) Toestemming is aantoonbaar, per doel en even makkelijk in te trekken. Afgevinkt met beide.
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

### dicht-architectuur
- [ ] ARCH-05 (hoog) Lever geen test-, voorbeeld- of ontwikkelcode mee naar productie. Afgevinkt met de drie uitvoeren.
- [ ] ARCH-29 (middel) Leg elke architectuurbeslissing vast als ADR. Afgevinkt als die bestanden bestaan en de status klopt.
- [ ] ARCH-30 (hoog) Leg elke uitzondering op een harde regel vast, ook een overgeslagen stap. Afgevinkt als het bestand bestaat en geen uitzondering over zijn einddatum heen is.
- [ ] ARCH-32 (middel) Leg hersteltermijnen vast en houd een schuldregister bij. Afgevinkt met de tellingen.
- [ ] ARCH-57 (middel) Houd per applicatie een loginventaris bij. Afgevinkt als lijst en werkelijkheid gelijk zijn.
- [ ] ARCH-80 (hoog) Maak bij elk nieuw project een threat model in vier vragen. Afgevinkt als het bestand compleet is.
- [ ] ARCH-81 (middel) Herzie het threat model bij elke nieuwe ingang of grens. Afgevinkt met de datumvergelijking.
- [ ] ARCH-83 (middel) Genereer de lijst van ingangen en vergelijk hem met het document. Afgevinkt met de testuitvoer.

### dicht-invoer
- [ ] INV-13 (hoog) Dwing per parameter één waarde en één type af. Afgevinkt met test en grep.
- [ ] INV-43 (hoog) Tel uitgepakte bytes en entries tijdens het uitpakken en pak niet genest uit. Afgevinkt met de testuitvoer.

## Ontwerp: richtlijnen (13)

### dicht-api
- [ ] BIZ-28 (middel) Sla periodes op als halfopen interval. `grep -rniE "23:59|between .* and" src` is leeg voor tijdvergelijkingen, of beoordeeld.

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
- [ ] PRIV-44 (middel) Meet zonder toestemming alleen wat geen of geringe gevolgen heeft, en dan zelf gehost. Afgevinkt met de drie.
- [ ] PRIV-63 (middel) ASVS dekt de AVG niet: gebruik de koppeltabel. Afgevinkt als elke rij een verwijzing heeft.
- [ ] PRIV-64 (laag) Herbeoordeel het niveau bij elke wijziging van functie of gegevens. Afgevinkt met de log.

### dicht-architectuur
- [ ] ARCH-82 (middel) Schrijf voor elke stroom met geld of limieten de misbruikgevallen op. Afgevinkt als elke stroom met geld een lijst heeft.

## Bouwen: hard (346)

### dicht-web
- [ ] WEB-01 (kritiek) Codeer uitvoer per context, als laatste stap. Afgevinkt als beide groen zijn.
- [ ] WEB-02 (hoog) Schrijf tekst naar de DOM met veilige sinks. Afgevinkt met de grep-uitvoer en een groene lint.
- [ ] WEB-03 (hoog) Sta HTML van gebruikers alleen toe via een onderhouden sanitizer. Afgevinkt met versie en testuitvoer.
- [ ] WEB-04 (hoog) Laat in URL-attributen alleen veilige schema's toe. Afgevinkt met de testuitvoer.
- [ ] WEB-06 (hoog) Geef data aan JavaScript door als gecodeerde data, niet als code. Afgevinkt met de test.
- [ ] WEB-07 (hoog) Behandel SVG, Markdown en eigen CSS van gebruikers als actieve inhoud. Afgevinkt met de drie testuitvoeren.
- [ ] WEB-09 (middel) Stuur bij elke respons het juiste Content-Type met charset en nosniff. Afgevinkt met de vier uitvoeren.
- [ ] WEB-13 (middel) Geen inline handlers, geen unsafe-eval. Afgevinkt met grep en header.
- [ ] WEB-17 (hoog) Zet HSTS op alle responsen. Afgevinkt met de uitvoer en de subdomeinlijst.
- [ ] WEB-19 (middel) Zet een expliciete Referrer-Policy. Afgevinkt met beide.
- [ ] WEB-22 (laag) Verberg versies en verwijder verouderde headers. Afgevinkt met de uitvoer.
- [ ] WEB-25 (hoog) Geef elke sessiecookie Secure, HttpOnly, SameSite en het __Host-voorvoegsel. Afgevinkt met de header en de consoletest.
- [ ] WEB-26 (hoog) Bewaar geen geheimen of persoonsgegevens in web storage. Afgevinkt met grep en schermafbeelding van de opslag.
- [ ] WEB-27 (middel) Ruim de browser op bij uitloggen. Afgevinkt met de test.
- [ ] WEB-29 (hoog) Wijzig nooit iets via GET. Afgevinkt met lijst en test.
- [ ] WEB-30 (kritiek) Verdedig elke wijzigende aanvraag met cookie-authenticatie tegen CSRF. Afgevinkt met de testuitvoer.
- [ ] WEB-33 (hoog) Sta met CORS alleen een vaste lijst van origins toe. Afgevinkt met de vier uitvoeren.
- [ ] WEB-36 (hoog) Controleer afzender en inhoud bij postMessage. Afgevinkt met grep en test.
- [ ] WEB-39 (hoog) Stuur alleen door naar bestemmingen uit een allowlist. Afgevinkt met de testuitvoer.
- [ ] WEB-40 (kritiek) Haal server-side alleen toegestane adressen op (SSRF). Afgevinkt met de testuitvoer.
- [ ] WEB-41 (hoog) Volg server-side geen redirects. Afgevinkt met test en grep.
- [ ] WEB-42 (hoog) Bouw absolute URL's uit de configuratie, nooit uit de Host-header. Afgevinkt met beide.
- [ ] WEB-43 (hoog) Begrens de grootte van elke upload en elke body. Afgevinkt met de test.
- [ ] WEB-44 (hoog) Sta alleen een allowlist van typen toe en controleer de inhoud. Afgevinkt met de testuitvoer.
- [ ] WEB-45 (hoog) Bepaal bestandsnaam en pad zelf. Afgevinkt met test en grep.
- [ ] WEB-46 (kritiek) Sla uploads op waar ze nooit als code worden uitgevoerd. Afgevinkt met de curl-uitvoer.
- [ ] WEB-47 (hoog) Lever bestanden van gebruikers uit als download of vanaf een aparte origin. Afgevinkt met de uitvoer.
- [ ] WEB-52 (hoog) Zet no-store op elke respons met persoonlijke of ingelogde inhoud. Afgevinkt met beide uitvoeren per route.
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
- [ ] AUTH-05 (hoog) Stop nooit meer dan het wachtwoord in bcrypt. Afgevinkt als de test groen is of bcrypt niet voorkomt.
- [ ] AUTH-06 (middel) Verifieer het wachtwoord ongewijzigd en werk wachtwoordmanagers niet tegen. [alleen: met login] Afgevinkt met een Playwright-test die een wachtwoord plakt.
- [ ] AUTH-09 (hoog) Geen hints, geen geheime vragen, geen standaardaccounts, geen blijvende startwachtwoorden. Afgevinkt als de lijst klopt met de afgesproken beheerders.
- [ ] AUTH-10 (kritiek) Begrens inlogpogingen per account en per bron. [alleen: met login] Afgevinkt als de test groen is en het document bestaat.
- [ ] AUTH-12 (middel) Verklap niet of een account bestaat. [alleen: met login] Afgevinkt als de test in CI staat.
- [ ] AUTH-13 (hoog) Ken en bewaak elk inlogpad. Afgevinkt als elk pad een test heeft.
- [ ] AUTH-14 (hoog) Log elke authenticatiegebeurtenis, zonder geheimen. Afgevinkt als beide kloppen.
- [ ] AUTH-16 (kritiek) MFA verplicht voor beheer en voor alles op niveau 2. [alleen: beheer] [bron niet gelezen: NEN] Afgevinkt als query en test kloppen.
- [ ] AUTH-25 (kritiek) Reset- en verificatietokens: willekeurig, gehasht, eenmalig, kort geldig. [alleen: met login] Afgevinkt als de drie tests groen zijn.
- [ ] AUTH-27 (kritiek) Stuur resetmails alleen naar het geverifieerde adres uit de database. [alleen: met login] Afgevinkt als de tests groen zijn.
- [ ] AUTH-28 (hoog) Na een reset: niet automatisch inloggen, sessies weg, melding. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-31 (middel) Houd tokens uit referers, logs en pagina's met scripts van derden. [alleen: met login] Afgevinkt als alle drie kloppen.
- [ ] AUTH-32 (kritiek) Sessie-id: willekeurig, ondoorzichtig, op de server gecontroleerd. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-33 (kritiek) Sessiecookie: `__Host-`, Secure, HttpOnly, SameSite, en nooit in webopslag. [alleen: met login] Afgevinkt als beide kloppen.
- [ ] AUTH-34 (hoog) Nieuw sessie-id bij inloggen en bij elke rechtenwijziging. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-35 (hoog) Leg een idle timeout en een absolute timeout vast en dwing ze op de server af. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-36 (kritiek) Uitloggen en blokkeren werken direct op de server. [alleen: met login] Afgevinkt als beide tests groen zijn.
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
- [ ] AUTH-82 (hoog) Beheerinterfaces: MFA, eigen pad, niet alleen een IP-filter. [alleen: met beheer] Afgevinkt als beide kloppen.
- [ ] API-01 (kritiek) Schema-validatie aan elke rand. Elke route heeft een schema voor body, query en params (Fastify `schema` of een zod-parse als eerste regel).
- [ ] API-02 (hoog) Weiger onbekende velden en bind nooit de hele body. `grep -rnE "\.set\((req|request)\.|\.values\((req|request)\." src` is leeg. Test: een PATCH met een extra veld `role` geeft 400 en wijzigt niets.
- [ ] API-03 (hoog) Geef elk veld een grens. Lint- of reviewcontrole: geen `z.string()` zonder `.max()` of formaat, geen `z.array()` zonder `.max()`. Test per route met een te lange waarde verwacht 400.
- [ ] API-06 (hoog) Valideer betekenis en samenhang, niet alleen vorm. Per flow een test met een op zichzelf geldige maar onderling onmogelijke combinatie;
- [ ] API-07 (middel) Decodeer één keer, vóór de validatie. `grep -rn "decodeURIComponent\|urldecode\|rawurldecode" src` toont alleen aanroepen vóór de schema-parse. Test met dubbel gecodeerde invoer.
- [ ] API-09 (hoog) Geef alleen de velden terug die de client nodig heeft. Elke route heeft een response-schema of een mapper.
- [ ] API-12 (kritiek) Faal dicht. Test per controle met een mock die gooit: de actie erna gebeurt niet. Review: elke `catch` zonder `throw` of `return` rond een controle is een bevinding.
- [ ] API-17 (hoog) Pagineer elke lijst met een maximum dat de server bepaalt. Elk lijstschema bevat `limit: z.coerce.number().int().min(1).max(100).default(25)`.
- [ ] API-20 (hoog) Begrens verzoeken per route-klasse en per identiteit. Test: N+1 verzoeken binnen het venster geven 429.
- [ ] API-27 (kritiek) Bereken prijs en totaal op de server uit een vertrouwde bron. Het bestelschema bevat geen bedragveld.
- [ ] API-28 (hoog) Reken met geld in hele centen of exacte decimalen, nooit met floats. Het schema gebruikt `integer` of `numeric` voor bedragen (zie DB).
- [ ] API-29 (hoog) Leg elke flow vast als statusmachine en sta alleen de bedoelde overgangen toe. Eén functie `overgang(van, naar)` met een tabel van toegestane paren; unit-tests voor elke verboden overgang. Test end-to-end: stap 3 aanroepen zonder stap 2 geeft 409.
- [ ] API-30 (kritiek) Maak controleren en handelen één atomaire stap. Een test vuurt 20 gelijktijdige verzoeken af op dezelfde bewerking en controleert dat het effect precies één keer optreedt.
- [ ] API-31 (hoog) Dwing "één keer" af met een unieke constraint. De migratie bevat de unieke index (zie DB).
- [ ] API-32 (kritiek) Zet een samengestelde bewerking in één transactie. De statusovergang en het aanmaken van de taak staan in dezelfde `db.transaction`. Test: een fout na de eerste schrijfactie laat de status ongewijzigd.
- [ ] API-34 (middel) Leg limieten per gebruiker en in totaal vast en dwing ze af. De limieten staan in de projectdocumentatie. Per limiet een test die de grens overschrijdt. Overschrijdingen worden gelogd (ASVS V16.3.3).
- [ ] API-35 (hoog) Weiger nul, negatief en extreem in aantallen en bedragen. Unit-tests op de prijsfunctie met 0, -1, 1.5, het maximum plus één en een stapel kortingen.
- [ ] API-36 (kritiek) Behandel de webhook als signaal en haal de status op bij Mollie. Test: een POST naar de webhook met het id van een betaling met status `open` leidt niet tot levering.
- [ ] API-37 (kritiek) Vergelijk bedrag, valuta en bestelling voordat je levert. De handler zoekt op `molliePaymentId` in de eigen tabel (geen bestel-id uit het verzoek of alleen uit `metadata`).
- [ ] API-38 (kritiek) Lever precies één keer, hoe vaak de webhook ook komt. Test met 20 gelijktijdige webhook-aanroepen voor één betaling: precies één leveringstaak, één mail, één vergoeding.
- [ ] API-39 (hoog) Antwoord 200 pas als de verwerking duurzaam vastligt. Test: laat de database-aanroep in de handler falen en controleer dat het antwoord 5xx is.
- [ ] API-40 (middel) Antwoord de webhook binnen 15 seconden en doe zwaar werk daarna. De handler bevat geen aanroepen naar andere diensten dan de Mollie-API en de eigen database.
- [ ] API-41 (hoog) Stuur een Idempotency-Key mee bij elke POST naar Mollie. `grep -rn "idempotencyKey\|Idempotency-Key" src` toont de sleutel bij elke muterende Mollie-aanroep.
- [ ] API-42 (hoog) Verwerk ook wat er na "betaald" gebeurt. Test met een nagebootst Mollie-antwoord waarin een chargeback of terugbetaling staat: er ontstaat een vastlegging en een taak.
- [ ] API-44 (hoog) Controleer de handtekening bij de nieuwe Mollie-webhooks. De route bewaart de ruwe body (in Fastify via een eigen content-type-parser met `parseAs: 'buffer'`).
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
- [ ] API-60 (hoog) Begrens en controleer uploads aan de API-kant. De registratie van `@fastify/multipart` toont alle vier de limieten.
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
- [ ] BIZ-09 (middel) Een slot in het geheugen van het proces is geen slot. `grep -rnE "new (Map|Set)\(|let [a-zA-Z]+ = (0|\[\]|\{\})" src` op moduleniveau: elke treffer is een cache zonder gevolgen voor de uitkomst, of is gedocumenteerd.
- [ ] BIZ-10 (hoog) Rond btw rekenkundig af op hele centen, volgens één vastgelegde methode. De gekozen methode staat in de projectdocumentatie.
- [ ] BIZ-12 (middel) Verdeel een bedrag zo dat de delen samen exact het totaal zijn. Eigenschappen-test (ARCH-42): voor willekeurige totalen en aantallen is de som van `verdeel()` gelijk aan het totaal en verschillen de delen hoogstens één cent.
- [ ] BIZ-13 (hoog) Leg prijs, korting, btw-tarief en totaal vast op de bestelling en reken ze later niet opnieuw uit. De bestelregel heeft eigen kolommen voor prijs, korting, tarief en totaal, alle `NOT NULL`.
- [ ] BIZ-14 (hoog) Bevries de bestelling zodra de betaling is aangemaakt. Test: maak een betaling aan, probeer daarna een regel toe te voegen, het aantal te wijzigen en een code toe te passen;
- [ ] BIZ-17 (laag) De valuta komt van de server en staat bij elk bedrag. Het bestelschema bevat geen valutaveld (API-02 weigert het).
- [ ] BIZ-19 (middel) Een bestelling van nul euro heeft een eigen overgang en gaat niet langs "betaald". De statusmachine heeft een overgang `concept -> gratis_toegekend` naast `wacht_op_betaling -> betaald`.
- [ ] BIZ-20 (hoog) Reserveer schaarse dingen met een vervaltijd en een maximum per account. De reserveringstabel heeft `verloopt_op NOT NULL`.
- [ ] BIZ-21 (middel) Boek verbruik van een quotum vóór de dure actie en geef het terug als de actie mislukt. Test: 50 gelijktijdige verzoeken bij één resterende eenheid geven precies één aanroep van de nagebootste dienst en 49 keer 429.
- [ ] BIZ-22 (hoog) "Betaald maar niet leverbaar" is een eigen toestand met een vaste afhandeling. De overgangstabel van API-29 bevat de toestand en de overgangen eruit.
- [ ] BIZ-24 (middel) Geloof bij een bericht over een toestand de actuele stand, niet de inhoud of de volgorde van het bericht. Test: bied de berichten van één betaling aan in omgekeerde volgorde en dubbel;
- [ ] BIZ-25 (middel) Controleer een termijn op het moment van gebruik en reken niet op de opruimjob. Test met een vaste klok: een rij met `verloopt_op` één seconde in het verleden wordt geweigerd terwijl de status nog "actief" is.
- [ ] BIZ-26 (hoog) Reken kalenderperiodes vanaf de ankerdatum, in SQL of met een kalenderbibliotheek. `grep -rnE "setMonth|setFullYear|setDate|86400|\* 30\b|\* 365\b" src` is leeg in code die periodes, vervaldatums of einddatums berekent, of elke treffer is beoordeeld.
- [ ] BIZ-27 (middel) Bepaal zakelijke datums in Europe/Amsterdam en sla ze op als datum. `grep -rnE "toISOString\(\)\.(slice|substring|split)" src` raakt geen zakelijke datum.
- [ ] BIZ-29 (middel) Tel dagen als kalenderdagen, niet als 24 uur. Test met een vaste klok rond 29-03-2026 en 25-10-2026: de termijn eindigt op de verwachte kalenderdag.
- [ ] BIZ-32 (middel) Maak codes met waarde niet raadbaar en begrens het proberen. Test: na het ingestelde aantal mislukte pogingen geeft de route 429 (API-20, API-22), ook voor een daarna correcte code binnen het venster.
- [ ] BIZ-33 (hoog) Sta standaard één code per bestelling toe en begrens de totale korting. Unit-tests op de prijsfunctie: twee codes, dezelfde code twee keer, een code plus een automatische actie;
- [ ] BIZ-34 (hoog) Reserveer een beperkte code bij het starten van de bestelling en tel hem definitief bij de betaling. Test: 20 gelijktijdige bestellingen met een code die één keer geldt;
- [ ] BIZ-37 (middel) Geef opzoekfuncties met zakelijke waarde een eigen limiet. Per opzoekfunctie staat de limiet in de documentatie (API-34) en is er een test die hem overschrijdt (429 met `Retry-After`).
- [ ] BIZ-40 (hoog) Een time-out is "onbekend", niet "mislukt". Het statusveld van elke uitgaande taak kent "onbekend".
- [ ] BIZ-44 (hoog) WordPress: houd geen teller, limiet of slot bij met opties of meta. `grep -rnE "update_option|update_post_meta|update_user_meta|set_transient" .` in de plugin: geen treffer schrijft een waarde die uit een eerdere `get_` is berekend en die

### dicht-database
- [ ] DB-25 (kritiek) Alleen geparametriseerde queries. Afgevinkt als de gate groen is en er een test bestaat die een aanhalingsteken in elk zoekveld stuurt.

### dicht-infra
- [ ] INFRA-55 (hoog) Versleutel en controleer elke verbinding die de host verlaat. Afgevinkt met de uitvoer.
- [ ] INFRA-64 (middel) Verstuur mail van een site of dienst via geauthenticeerde SMTP. [eigen bron] Afgevinkt met de headers.
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
- [ ] GIT-65 (middel) Leg elke uitzondering vast met reden en einddatum. Afgevinkt met de bestanden.
- [ ] GIT-75 (hoog) Onderbouw elke nieuwe afhankelijkheid kort. Afgevinkt met de commit.
- [ ] GIT-78 (hoog) Controleer de naam van een pakket voordat je het installeert. Afgevinkt met die uitvoer.
- [ ] GIT-81 (hoog) Composer: lockfile committen, installeren zonder dev en zonder verrassingen. Afgevinkt met de drie.
- [ ] GIT-82 (hoog) Houd Composer zelf bij en laat de ingebouwde blokkades aan. Afgevinkt met de drie.
- [ ] GIT-83 (middel) Sta alleen benoemde Composer-plugins toe. Afgevinkt met de uitvoer.
- [ ] GIT-84 (hoog) Beoordeel een WordPress-plugin of thema van een ander vóór installatie. Afgevinkt met die notitie.
- [ ] GIT-89 (middel) Behandel meegeleverde bibliotheken in een plugin of thema als afhankelijkheden. Afgevinkt met de drie.
- [ ] GIT-90 (middel) Lever een plugin of thema als schoon pakket uit de repo. Afgevinkt met de drie.
- [ ] GIT-93 (hoog) Gebruik alleen runtimes die nog beveiligingsfixes krijgen. Afgevinkt met de uitvoer.
- [ ] GIT-101 (middel) Maak bij elke release een SBOM. [bron niet gelezen: WET] Afgevinkt met het bestand.
- [ ] GIT-102 (middel) Een release is een ondertekende tag op een gevalideerde commit. Afgevinkt met de drie.
- [ ] GIT-105 (middel) WordPress-plugins en thema's: GPL-compatibel, ook wat je meelevert. Afgevinkt met beide.

### dicht-wordpress
- [ ] WP-01 (kritiek) Escape elke uitvoer laat, met de functie die bij de context hoort. Afgevinkt met de phpcs-uitvoer en de testuitvoer.
- [ ] WP-02 (hoog) Gebruik esc_url voor elke URL, ook in een attribuut. `grep -rnE "(href|src|action)=\"<\?php echo esc_attr" .` is leeg;
- [ ] WP-03 (hoog) Geef data aan JavaScript door als JSON met JSON_HEX_TAG of via de script-API. Afgevinkt met grep en test.
- [ ] WP-04 (hoog) Sta HTML alleen toe via wp_kses met een eigen, korte allowlist. Afgevinkt met de testuitvoer.
- [ ] WP-06 (hoog) Lees invoer in drie stappen: unslash, valideren, dan pas gebruiken. Afgevinkt met beide uitvoeren.
- [ ] WP-07 (middel) Zet wp_slash om de waarde bij het opslaan van meta en berichten. Afgevinkt met de testuitvoer.
- [ ] WP-08 (middel) Laat geen PHP-bestand rechtstreeks uitvoeren. Afgevinkt met beide uitvoeren.
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
- [ ] WP-26 (kritiek) Deserialiseer nooit invoer; gebruik JSON. Afgevinkt met de nagelopen lijst.
- [ ] WP-27 (hoog) Stuur door met wp_safe_redirect en stop daarna. Afgevinkt met phpcs, grep en test.
- [ ] WP-28 (hoog) Haal een URL van een gebruiker alleen op met wp_safe_remote_get, met een grens. Afgevinkt met grep en test.
- [ ] WP-29 (middel) Schrijf bestanden alleen in een eigen map onder uploads, met een zelfgekozen naam. Afgevinkt met grep en curl.
- [ ] WP-30 (hoog) Behandel shortcode-attributen als invoer van een gebruiker met weinig rechten. Afgevinkt met de testuitvoer.
- [ ] WP-31 (hoog) Escape blokattributen in de render-callback. Afgevinkt met de testuitvoer.
- [ ] WP-32 (hoog) Registreer instellingen en meta met een sanitize- en een auth-callback. Afgevinkt met grep en curl.
- [ ] WP-34 (middel) Beheer een mu-plugin als code met een bron, een versie en een eigenaar. Afgevinkt met de uitvoer per site.
- [ ] WP-36 (middel) Laad niets uit de kern opnieuw en geen code van een externe server. Afgevinkt met de Plugin Check-uitvoer en grep.
- [ ] WP-83 (kritiek) Laat de betaalstatus van een bestelling alleen van de betaalprovider komen. Afgevinkt met grep en tests.

### dicht-ai-mcp
- [ ] AI-12 (kritiek) Voer modeluitvoer nooit uit als code, query, commando of pad. [bron niet gelezen: AGENTIC] Afgevinkt met de grep-uitvoer en een verklaring per treffer.
- [ ] AI-13 (hoog) Render modeluitvoer als onvertrouwde inhoud. Afgevinkt met de testuitvoer en de header.
- [ ] AI-28 (kritiek) Geheimen blijven in code en komen nooit in de context van het model. Afgevinkt met grep en testuitvoer.
- [ ] AI-55 (hoog) Beoordeel elke MCP-server voordat hij wordt aangesloten. [bron niet gelezen: AGENTIC] Afgevinkt met de lijst.
- [ ] AI-56 (hoog) Zet elke MCP-server vast op een versie. Afgevinkt met de grep-uitvoer.
- [ ] AI-57 (hoog) Controleer naam en uitgever letter voor letter. Afgevinkt met beide gegevens.
- [ ] AI-59 (hoog) Agentconfiguratie in een repository is code en wordt als code beoordeeld. [bron niet gelezen: AGENTIC] Afgevinkt met de uitvoer en een notitie.
- [ ] AI-60 (hoog) Tokens voor MCP-servers staan niet in platte tekst in bestanden die gedeeld, gevolgd of geback-upt worden. Afgevinkt met de drie uitvoeren.
- [ ] AI-61 (hoog) Elke server krijgt een eigen credential met de kleinste scope. Afgevinkt met de lijst.
- [ ] AI-62 (hoog) Lees een skill of plugin van een ander volledig, inclusief scripts, en zet netwerkaanroepen uit. [bron niet gelezen: AGENTIC] Afgevinkt met de grep-uitvoer en de notitie.
- [ ] AI-63 (hoog) Houd AI-gereedschap actueel en gebruik geen overbodige tussenlagen. Afgevinkt met de versies en de rooktest.

### dicht-privacy
- [ ] PRIV-14 (hoog) Geen echte persoonsgegevens naar een leverancier zonder verwerkersovereenkomst. Afgevinkt met de scriptuitvoer.
- [ ] PRIV-18 (hoog) Leg per leverancier vast in welk land de gegevens komen en op grond waarvan. Afgevinkt met het register.
- [ ] PRIV-19 (middel) Een script, lettertype of ingesloten dienst van een derde is ook een ontvanger. Afgevinkt als geen host buiten die drie valt.
- [ ] PRIV-22 (middel) Formulierinzendingen en bestellingen in WordPress krijgen een ingestelde termijn. Afgevinkt met instelling en telling.
- [ ] PRIV-25 (middel) Geef elke tijdelijke kopie een einddatum op het moment dat je hem maakt. Afgevinkt met de drie.
- [ ] PRIV-40 (hoog) Plaats of lees niets op het apparaat vóór toestemming, behalve wat strikt nodig is. Afgevinkt met de testuitvoer per paginatype.
- [ ] PRIV-41 (hoog) De regel geldt voor elke techniek, niet alleen voor cookies. Afgevinkt met de drie.
- [ ] PRIV-42 (hoog) Weigeren is even makkelijk als accepteren, en niets staat vooraf aan. Afgevinkt met de testuitvoer.
- [ ] PRIV-43 (hoog) De toestemmingsstatus stuurt de code, niet alleen de banner. Afgevinkt met de drie uitvoeren.
- [ ] PRIV-46 (middel) Laad ingesloten inhoud van derden pas na een klik. Afgevinkt met de testuitvoer.
- [ ] PRIV-49 (middel) Mail aan eigen klanten mag alleen voor eigen gelijksoortige producten en met afmelding vanaf het begin. Afgevinkt met test en query.
- [ ] PRIV-57 (hoog) Gebruik het BSN alleen als de wet het voorschrijft. Afgevinkt met de grep.
- [ ] PRIV-65 (hoog) Stel per webwinkel of dienst vast of de toegankelijkheidswet geldt. Afgevinkt als het er staat.
- [ ] PRIV-66 (hoog) Bouw elke nieuwe site op WCAG 2.2 niveau AA. Afgevinkt met beide; een scan alleen vindt maar een deel van de criteria.
- [ ] PRIV-67 (hoog) Maak inloggen, beveiligingsstappen en betalen toegankelijk. Afgevinkt met de testuitvoer.
- [ ] PRIV-71 (hoog) Meld een actief uitgebuite kwetsbaarheid in je product binnen 24 uur. Afgevinkt met het document.
- [ ] PRIV-72 (middel) Geef elk product een meldpunt en een beleid voor het melden van kwetsbaarheden. Afgevinkt als de drie bestaan en een testbericht aankomt.
- [ ] PRIV-73 (hoog) Lever zonder bekende uitbuitbare kwetsbaarheden en met een veilige standaardconfiguratie. Afgevinkt met beide.
- [ ] PRIV-84 (kritiek) Laat kaartgegevens nooit door de eigen server of de eigen pagina-code lopen. [bron niet gelezen: PCI] Afgevinkt met beide.
- [ ] PRIV-85 (hoog) Bescherm de pagina die de betaalvelden insluit tegen vreemde scripts. [bron niet gelezen: PCI] Afgevinkt met hostlijst, header en lijst.
- [ ] PRIV-87 (hoog) Bij een eerste betaling met machtiging: toon wat en hoe vaak, en bewaar het bewijs. [bron niet gelezen: SEPA] Afgevinkt met test en schema.
- [ ] PRIV-88 (hoog) De bestelknop zegt dat er betaald moet worden, en de kerninformatie staat er direct boven. Afgevinkt met de testuitvoer.
- [ ] PRIV-89 (hoog) Bouw de herroepingsfunctie in elke webwinkel voor consumenten. Afgevinkt met de testuitvoer.
- [ ] PRIV-90 (middel) Bewaar de administratie zeven jaar, en alleen de administratie. Afgevinkt met tabel en test.

### dicht-architectuur
- [ ] ARCH-08 (hoog) Laat beveiliging niet afhangen van de naam van de omgeving. Afgevinkt met grep en test.
- [ ] ARCH-10 (middel) Houd ontwikkeling, test en productie gelijk in versies en soort diensten. Afgevinkt als de hoofdversies gelijk zijn.
- [ ] ARCH-33 (middel) Leg per project vast welke testlaag wat bewijst. Afgevinkt met het bestand en de uitvoer.
- [ ] ARCH-34 (hoog) Begin elke bugfix met een test die de fout laat zien. Afgevinkt met de twee uitvoeren.
- [ ] ARCH-36 (hoog) Bedien de pagina in e2e-tests met echte invoer. Afgevinkt met de grep.
- [ ] ARCH-38 (hoog) Test elke functie langs vaste assen, niet alleen het gelukkige pad. Afgevinkt als geen as leeg is zonder reden.
- [ ] ARCH-42 (hoog) Test kritieke logica met eigenschappen in plaats van alleen voorbeelden. Afgevinkt met lijst en uitvoer.
- [ ] ARCH-47 (hoog) Test een WordPress-plugin of thema in een wegwerpomgeving met twee rollen. Afgevinkt met de drie uitvoeren.
- [ ] ARCH-48 (hoog) Gebruik in tests alleen verzonnen gegevens. Afgevinkt met de grep.
- [ ] ARCH-49 (hoog) Geef tests eigen geheimen en houd inlogtoestanden uit git. Afgevinkt met de drie controles.
- [ ] ARCH-50 (hoog) Laat tests geen echte mail, betaling of oproep naar buiten sturen. Afgevinkt met de opzet en de grep.
- [ ] ARCH-51 (hoog) Beperk een test op productie tot lezen, of markeer en ruim op met exacte id's. [eigen bron] Afgevinkt met het script en de telling.
- [ ] ARCH-62 (hoog) Log alleen benoemde velden en scan de testlogs in de gate. Afgevinkt met de uitvoer.
- [ ] ARCH-63 (middel) Log ook mislukte validatie, limieten, onverwachte fouten en starten en stoppen. Afgevinkt met de testuitvoer.
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
- [ ] SCR-12 (middel) Zet het eindwoord van een here-document tussen aanhalingstekens als de inhoud data is. Afgevinkt met de uitvoer.
- [ ] SCR-14 (hoog) Maak tijdelijke bestanden met mktemp en ruim ze op met een trap. Afgevinkt met de uitvoer.
- [ ] SCR-15 (kritiek) Bewaak elk pad dat je recursief verwijdert of overschrijft. Afgevinkt met de drie uitvoeren.
- [ ] SCR-16 (middel) Zet umask 077 in elk script dat geheimen, persoonsgegevens of logs schrijft. Afgevinkt met beide uitvoeren.
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
- [ ] SCR-31 (middel) Maak tijdelijke bestanden in Python met het tempfile-pakket. Afgevinkt met de uitvoer.
- [ ] SCR-32 (hoog) Draai elk Python-script in een eigen virtuele omgeving met vastgezette afhankelijkheden en hashes. Afgevinkt met de drie uitvoeren.
- [ ] SCR-33 (hoog) Draai scripts op een Python-versie die nog beveiligingsupdates krijgt. Afgevinkt met de uitvoer en de notitie.
- [ ] SCR-35 (middel) Maak een beveiligingslint een gate voor Python-scripts. Afgevinkt met de drie uitvoeren.
- [ ] SCR-47 (kritiek) Laat een leeg, mislukt of genegeerd filter nooit "alles" betekenen. [eigen bron] Afgevinkt met script en testuitvoer.
- [ ] SCR-53 (hoog) Stop een proces op proces-id of poort, nooit op een breed patroon. (1) `grep -rnE '\b(pkill|killall)\b' --include='*.sh' --include='*.py' .` geeft alleen regels met een pidbestand (`-F`), een ouder (`-P`) of een patroon met het volledige

### dicht-invoer
- [ ] INV-01 (kritiek) Zet in PHP geen parservlag die entiteiten of DTD's laadt. Afgevinkt met grep en testuitvoer.
- [ ] INV-02 (hoog) Leg in PHP een entiteit-lader vast die niets laadt, en reken niet op de globale stand. Afgevinkt met de drie uitvoeren.
- [ ] INV-04 (hoog) Behandel elk formaat met XML erin als XML. Afgevinkt met de lijst en de testuitvoer.
- [ ] INV-05 (hoog) Voer geen XSLT van gebruikers uit en geef een stylesheet geen PHP-functies. Afgevinkt met de grep.
- [ ] INV-06 (hoog) Bouw XML met een serializer, nooit met tekst aan elkaar. Afgevinkt met grep en test.
- [ ] INV-07 (middel) Zet geen invoer in een XPath-expressie. Afgevinkt met de grep.
- [ ] INV-10 (middel) Begrens de diepte van geneste invoer vóór eigen recursie. Afgevinkt met de test.
- [ ] INV-11 (middel) Laat json_decode in PHP een uitzondering gooien. Afgevinkt met grep en test.
- [ ] INV-20 (middel) Lees een CSV-import strikt: UTF-8, vast scheidingsteken, limieten en een schema per rij. Afgevinkt met de testuitvoer.
- [ ] INV-22 (hoog) Saneer als laatste stap en verander de uitvoer daarna niet meer. Afgevinkt met grep en test.
- [ ] INV-24 (hoog) Reken niet op de Markdown-renderer voor veiligheid. Afgevinkt met grep en test.
- [ ] INV-25 (hoog) Gebruik strip_tags en reguliere expressies niet als sanitizer. Afgevinkt met de nagelopen lijst.
- [ ] INV-27 (hoog) Geef ImageMagick een dichte policy voordat het bestanden van buiten ziet. Afgevinkt met de uitvoer.
- [ ] INV-29 (middel) Controleer in PHP de afmetingen vóór het decoderen en gebruik getimagesize niet als bewijs. Afgevinkt met grep en test.
- [ ] INV-30 (middel) Bewaar geen locatiegegevens in foto's die anderen kunnen zien. Afgevinkt met grep en de exiftool-uitvoer.
- [ ] INV-31 (hoog) Toon SVG van anderen alleen via een img-element. Afgevinkt met grep en curl.
- [ ] INV-32 (hoog) Zet SVG van anderen niet op de server om naar een rasterbeeld zonder afscherming. Afgevinkt met de testuitvoer, of met de vaststelling dat SVG-invoer wordt geweigerd.
- [ ] INV-33 (hoog) Behandel magic bytes als een hint en parse het bestand volledig. Afgevinkt met de testuitvoer.
- [ ] INV-34 (hoog) Geef PHP-bestandsfuncties nooit een pad met een schema uit invoer. Afgevinkt met grep en test.
- [ ] INV-35 (kritiek) Behandel HTML voor een PDF als code die in een browser op de server draait. Afgevinkt met test en grep.
- [ ] INV-37 (hoog) Gebruik wkhtmltopdf niet meer. Afgevinkt met beide uitvoeren.
- [ ] INV-38 (hoog) Houd dompdf dicht: geen externe bronnen, geen PHP in het document, een smalle chroot. Afgevinkt met de drie uitvoeren.
- [ ] INV-41 (kritiek) Controleer elke naam in een archief voordat er een byte wordt geschreven. Afgevinkt met test, grep en versies.
- [ ] INV-42 (hoog) Weiger symlinks en hardlinks in een archief. Afgevinkt met de testuitvoer.
- [ ] INV-45 (middel) Pak in WordPress uit met unzip_file en niet met een eigen ZipArchive-lus. Afgevinkt met grep en test.
- [ ] INV-46 (hoog) Gebruik extract, variabele variabelen en parse_str niet op invoer. Afgevinkt met de nagelopen lijst.
- [ ] INV-47 (kritiek) Geef WordPress-functies die gebruikers of berichten schrijven nooit de hele aanvraag. Afgevinkt met grep en test.
- [ ] INV-49 (hoog) Bouw uitgaande aanvragen met URL-objecten en vaste kopwaarden. Afgevinkt met grep en test.
- [ ] INV-51 (hoog) Maak identifiers canoniek met één functie die bij herhaling niets meer verandert. Afgevinkt met grep, index en tests.
- [ ] INV-52 (middel) Vergelijk hoofdletterongevoelig via kleine letters, nooit via hoofdletters of de taalinstelling. Afgevinkt met grep en test.
- [ ] INV-55 (hoog) Laat de build falen op bidi-stuurtekens in broncode. Afgevinkt met de uitvoer van een run met en zonder testbestand.
- [ ] INV-56 (middel) Weiger stuurtekens in velden van één regel. Afgevinkt met de test.
- [ ] INV-58 (middel) Meet lengte in de eenheid van de opslag en kap nooit stil af. Afgevinkt met test, grep en de query.
- [ ] INV-59 (hoog) Ontleed een URL met één WHATWG-parser en gebruik daarna het ontlede object. Afgevinkt met grep en test.
- [ ] INV-60 (hoog) Neem in PHP geen beveiligingsbeslissing op parse_url. Afgevinkt met de nagelopen lijst.
- [ ] INV-63 (laag) Ontdoe zoektekst van LIKE-jokertekens. Afgevinkt met grep en test.
- [ ] INV-64 (hoog) Accepteer e-mailadressen alleen in de eenvoudige vorm en beslis niets op het domein van een onbevestigd adres. Afgevinkt met test en grep.
- [ ] INV-67 (middel) Behandel in PHP een lege aanvraag na een te grote upload als fout. Afgevinkt met grep en test.
- [ ] INV-68 (middel) Maak tijdelijke bestanden in een eigen, verse map met een onvoorspelbare naam. Afgevinkt met de vier uitvoeren.

### dicht-berichten
- [ ] MSG-01 (hoog) Zet in From alleen een adres op een eigen domein; de inzender hoort in Reply-To. Afgevinkt met grep en de ontvangen koppen.
- [ ] MSG-04 (middel) Bouw elk bericht met een bibliotheek, met één Message-ID, één Date en één From. Afgevinkt met de testuitvoer en de telling.
- [ ] MSG-06 (hoog) Houd de mailbibliotheek binnen de hersteltermijnen, juist bij meerdere tenants. Afgevinkt met de uitvoer en de datum.
- [ ] MSG-16 (kritiek) Geef invoer nooit door als afzender aan sendmail of mail(). Afgevinkt met grep en de testuitvoer.
- [ ] MSG-17 (hoog) Codeer elke variabele in een HTML-mailsjabloon. Afgevinkt met de testuitvoer.
- [ ] MSG-18 (hoog) Beslis op het adres dat de parser teruggeeft, met één parser voor de hele keten. Afgevinkt met de testuitvoer.
- [ ] MSG-19 (middel) Laat links in mail alleen naar het eigen domein wijzen, zonder open doorstuurder. Afgevinkt met grep en de uitvoer.
- [ ] MSG-31 (hoog) Antwoord nooit automatisch op een automatisch bericht. Afgevinkt met de testuitvoer.
- [ ] MSG-32 (middel) Markeer elk automatisch verstuurd bericht. Afgevinkt met de koppen per stroom.
- [ ] MSG-41 (hoog) Behandel een webhookadres en een bot-token als geheim. Afgevinkt met de uitvoer en het overzicht.
- [ ] MSG-48 (middel) Zet geen gevoelige inhoud in een melding. Afgevinkt met de voorbeelden.

## Bouwen: richtlijnen (31)

### dicht-web
- [ ] WEB-32 (middel) Bescherm ook het inlogformulier tegen CSRF. Afgevinkt met de test.
- [ ] WEB-35 (laag) Geen JSONP en geen data met autorisatie in scriptbestanden. Afgevinkt met de grep.
- [ ] WEB-49 (middel) Herschrijf afbeeldingen en wantrouw archieven. Afgevinkt met de testuitvoer.

### dicht-api
- [ ] AUTH-11 (middel) Voorkom dat een aanvaller accounts kan blokkeren. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-68 (middel) Onvoorspelbare id's zijn een extra laag, geen autorisatie. Afgevinkt als de lijst met zulke links gedocumenteerd is.
- [ ] API-45 (laag) Gebruik geen IP-lijst als controle op Mollie-webhooks. Geen allowlist voor Mollie in nginx of de firewall, of alleen als extra laag naast API-36.
- [ ] BIZ-38 (laag) Meet op waardevolle stromen of het tempo menselijk is. Test: een afronding binnen de ingestelde ondergrens na de eerste stap wordt geweigerd of naar een extra controle gestuurd.
- [ ] BIZ-45 (middel) WooCommerce: gebruik de ingebouwde voorraad- en bonlimieten en bouw ze niet na. `wp option get woocommerce_manage_stock` en `wp option get woocommerce_hold_stock_minutes` (alleen lezen) tonen "yes" en een getal.

### dicht-git
- [ ] GIT-08 (laag) Ruim worktrees en branches op zodra het werk gemerged is. Afgevinkt met beide uitvoeren.
- [ ] GIT-13 (middel) Laat elke wijziging lezen voordat hij live gaat. Afgevinkt met die notitie.
- [ ] GIT-37 (middel) Herschrijf de geschiedenis alleen als intrekken niet genoeg is. Afgevinkt met de vier.
- [ ] GIT-42 (hoog) Gebruik zo min mogelijk acties van derden en kijk wat ze zelf aanroepen. Afgevinkt met die lijst.
- [ ] GIT-55 (middel) Laat een bot niet zelf mergen zonder de gate en de wachttijd. Afgevinkt met de instelling en de regel.
- [ ] GIT-103 (laag) Leg herkomst vast met wat het plan toelaat. Afgevinkt met uitvoer of document.

### dicht-wordpress
- [ ] WP-05 (middel) Escape ook vertaalde teksten. Afgevinkt met de phpcs-uitvoer van WP-01.
- [ ] WP-21 (laag) Geef eigen tabellen en opties een prefix en ruim ze op bij verwijderen. Afgevinkt met de testuitvoer.
- [ ] WP-33 (middel) Bewaar geheimen in wp-config of de omgeving, niet in een optie die iedereen kan lezen. Afgevinkt met de drie uitvoeren.
- [ ] WP-35 (laag) Maak geplande taken herhaalbaar en reken niet op het tijdstip. Afgevinkt met de uitvoer.
- [ ] WP-70 (middel) Weet dat wp eval een andere context heeft dan wp-admin. Afgevinkt met het script.
- [ ] WP-80 (middel) Gebruik multisite alleen voor sites van één eigenaar en beperk de superbeheerder. Afgevinkt met de uitvoer.

### dicht-ai-mcp
- [ ] AI-58 (hoog) Lees de toolbeschrijvingen en merk het op als ze veranderen. [bron niet gelezen: AGENTIC] Afgevinkt met het opgeslagen bestand en de hash.

### dicht-privacy
- [ ] PRIV-75 (middel) Maak bij elke release een SBOM en bewaar de risicobeoordeling. Afgevinkt met beide.
- [ ] PRIV-86 (middel) Behandel de betaalprovider als zelfstandige verantwoordelijke, en noem hem toch in het register. Afgevinkt met beide.

### dicht-architectuur
- [ ] ARCH-11 (middel) Zet beheertaken in de repository en draai ze tegen dezelfde release. Afgevinkt met commit en uitvoer.
- [ ] ARCH-37 (middel) Schrijf e2e-tests op wat de gebruiker ziet, en laat een fout in de console de test breken. Afgevinkt met de grep en de run.
- [ ] ARCH-39 (middel) Houd tests onafhankelijk en behandel een wankele test als een fout. Afgevinkt met de uitvoer.
- [ ] ARCH-43 (middel) Fuzz elke parser van niet-vertrouwde invoer en de API als geheel. Afgevinkt met de uitvoeren en de datum.
- [ ] ARCH-59 (middel) Gebruik één vaste woordenlijst voor beveiligingsgebeurtenissen. Afgevinkt met de lijst.

### dicht-invoer
- [ ] INV-14 (middel) Controleer in PHP dat een groot formulier volledig is aangekomen. Afgevinkt met test en waarde.
- [ ] INV-18 (middel) Valideer geparste YAML en TOML met een schema en reken niet op het geraden type. Afgevinkt met de test.

### dicht-berichten
- [ ] MSG-34 (middel) Stuur een automatisch antwoord hooguit één keer per afzender per zeven dagen, naar het envelopadres. Afgevinkt met de testuitvoer.

## Vóór oplevering: hard (20)

### dicht-api
- [ ] BIZ-50 (hoog) Bewijs een race met echte gelijktijdigheid tegen een echte PostgreSQL. De testopzet gebruikt een pool van minstens 20 en geen omhullende transactie voor deze tests.
- [ ] BIZ-52 (middel) Test geld en tijd met een vaste tabel van grensgevallen. De tabel staat als geparametriseerde test in de repository (`it.each`).

### dicht-wordpress
- [ ] WP-37 (hoog) Maak PHPCS met de WordPress-regels, Plugin Check en PHPStan een gate. Afgevinkt met de drie uitvoeren.
- [ ] WP-66 (kritiek) Sluit ingelogde en persoonlijke pagina's uit van de paginacache en meet het. Afgevinkt met de uitvoer van de drie metingen.
- [ ] WP-67 (middel) Laat een gecachte pagina geen verlopen nonce uitleveren. Afgevinkt met de testuitvoer.
- [ ] WP-84 (hoog) Lever een eigen plugin of thema op met een vast bewijspakket. Afgevinkt als het bestand bestaat en compleet is.

### dicht-ai-mcp
- [ ] AI-85 (hoog) Code die een model schreef, gaat door dezelfde gates, en elk voorgesteld pakket wordt gecontroleerd. Afgevinkt met de CI-uitvoer en de onderbouwing.
- [ ] AI-86 (hoog) Wat een agent op een klantsite of in een vreemde repository leest, is onvertrouwd. [bron niet gelezen: AGENTIC] Afgevinkt met de notitie bij de klus.

### dicht-privacy
- [ ] PRIV-45 (middel) De cookielijst in de verklaring is de gemeten lijst. Afgevinkt met de vergelijking.

### dicht-architectuur
- [ ] ARCH-22 (hoog) Rol uit met één script dat alle stappen doet. Afgevinkt met script en bewijs.
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

## Vóór oplevering: richtlijnen (2)

### dicht-architectuur
- [ ] ARCH-87 (middel) Rol uit op een moment waarop je na een uur nog kunt nameten en terugdraaien. [eigen bron] Afgevinkt met beide tijdstippen.
- [ ] ARCH-56 (middel) Volg in PHP-code de weg van invoer naar gevaarlijke functies met taint-analyse. Afgevinkt met de uitvoer.

## Na oplevering en beheer: hard (19)

### dicht-api
- [ ] AUTH-02 (middel) Geen samenstellingsregels en geen verplichte periodieke wissel. [alleen: met login] Afgevinkt met de test uit AUTH-01 (wachtwoord van 15 kleine letters wordt geaccepteerd).
- [ ] AUTH-85 (hoog) Offboarding: toegang van mensen en systemen direct weg. Afgevinkt als de test groen is en de laatste controle minder dan een kwartaal oud is.
- [ ] API-43 (hoog) Stem dagelijks af wat de webhook kan hebben gemist. De taak bestaat (cron of worker), heeft een droge modus, logt hoeveel betalingen hij alsnog verwerkte en alarmeert bij meer dan nul.
- [ ] BIZ-31 (middel) Laat een periodieke taak zijn werk afleiden uit de toestand, niet uit de datum van vandaag. Test: sla in de test één run over (zet de klok twee dagen vooruit);

### dicht-infra
- [ ] INFRA-75 (hoog) Oefen het vervangen van een geheim voordat het nodig is. Afgevinkt met de lijst.
- [ ] INFRA-91 (hoog) Schrijf het draaiboek voordat er iets gebeurt. Afgevinkt met het document en de datum.
- [ ] INFRA-92 (hoog) Isoleer eerst en bewaar bewijs voordat je opruimt. Afgevinkt met het verslag.
- [ ] INFRA-93 (kritiek) Vervang na een inbraak elk geheim dat de getroffen omgeving kon lezen. Afgevinkt met de lijst.
- [ ] INFRA-94 (hoog) Herbouw vanaf een schone bron; ruim alleen op met volledige controle. Afgevinkt met het verslag.
- [ ] INFRA-96 (kritiek) Beoordeel bij elk incident met persoonsgegevens direct de meldplicht. [bron niet gelezen: WET] Afgevinkt met het verslag.

### dicht-git
- [ ] GIT-09 (hoog) Elke repo met waarde heeft een kopie buiten de server. Afgevinkt met uitvoer en datum.
- [ ] GIT-76 (middel) Laat Dependabot versies bijwerken, gegroepeerd en met wachttijd. Afgevinkt met bestand en uitvoer.

### dicht-wordpress
- [ ] WP-52 (hoog) Draai op een PHP-versie die nog beveiligingsupdates krijgt. Afgevinkt met beide waarden.

### dicht-privacy
- [ ] PRIV-30 (middel) Geef als verwerker de klant het gereedschap om verzoeken af te handelen. Afgevinkt met grep en test.
- [ ] PRIV-31 (kritiek) Meld een datalek binnen 72 uur na kennisname, ook als het onderzoek nog loopt. Afgevinkt als het document bestaat en één keer is doorgelopen met een oefengeval.
- [ ] PRIV-33 (hoog) Registreer elk datalek, ook als je het niet meldt. Afgevinkt als het bestand bestaat (ook als het leeg is) en in het draaiboek genoemd wordt.
- [ ] PRIV-34 (hoog) Zorg dat je kunt vaststellen of er toegang is geweest. Afgevinkt met overzicht en proef.
- [ ] PRIV-35 (hoog) Informeer betrokkenen bij een hoog risico, en weet wanneer versleuteling dat voorkomt. Afgevinkt met beide.

### dicht-invoer
- [ ] INV-69 (middel) Ruim tijdelijke bestanden op bij elke afloop en begrens de ruimte. Afgevinkt met de testuitvoer en de configuratie.

## Na oplevering en beheer: richtlijnen (1)

### dicht-infra
- [ ] INFRA-95 (middel) Leg tijdens het incident vast wat je doet en evalueer daarna. Afgevinkt met het verslag.
