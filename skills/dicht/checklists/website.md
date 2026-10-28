# Checklist website

459 regels: 398 hard, 61 richtlijn. Gemaakt door `tools/bouw.py` uit het veld "Geldt voor"; niet met de hand wijzigen.
Elk punt: ID (ernst) titel, en wat telt als afgevinkt. Het volledige bewijs staat in de referentie van de sub-skill. Een punt dat in dit project niet speelt krijgt in het bewijsbestand `nvt` met een reden.

## Ontwerp: hard (35)

### dicht-web
- [ ] WEB-59 (middel) Houd een lijst van derde partijen bij en stuur ze geen gevoelige data. Afgevinkt met de hostlijst.

### dicht-api
- [ ] AUTH-64 (kritiek) Bescherm elke functie, ook via een andere methode of een ander pad. Afgevinkt als de matrix alle routes dekt.

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

### dicht-privacy
- [ ] PRIV-01 (hoog) Leg per project vast wie verantwoordelijke en wie verwerker is. Afgevinkt als elke tabel met persoonsgegevens uit de classificatie (DB-87) in precies één rij valt.
- [ ] PRIV-02 (hoog) Het verwerkingsregister bevat per activiteit de wettelijke velden. Afgevinkt met de uitvoer.
- [ ] PRIV-03 (hoog) Werk het register bij in dezelfde wijziging als de nieuwe gegevensstroom. Afgevinkt met de vergelijking.
- [ ] PRIV-05 (hoog) De privacyverklaring klopt met wat de code doet. Afgevinkt met de testuitvoer en de laatste uitvoer van die vergelijking
- [ ] PRIV-07 (hoog) Geen verwerking zonder vastgelegde grondslag. Afgevinkt met de scriptuitvoer.
- [ ] PRIV-08 (middel) Vraag per veld alleen wat het doel nodig heeft. Afgevinkt met tabel en grep.
- [ ] PRIV-10 (hoog) Toestemming is aantoonbaar, per doel en even makkelijk in te trekken. Afgevinkt met beide.
- [ ] PRIV-21 (hoog) Elke gegevenssoort heeft een termijn met een reden, in het register en in de code. Afgevinkt met de vergelijking en de logregels.
- [ ] PRIV-23 (middel) Geef logs met persoonsgegevens een termijn die het doel dekt en niet meer. Afgevinkt met overzicht en configuratie.
- [ ] PRIV-37 (hoog) Doe bij elk nieuw project een DPIA-toets van vijf minuten en leg de uitkomst vast. Afgevinkt met de notitie.
- [ ] PRIV-59 (hoog) Leg per project het ASVS-niveau vast, per onderdeel. Afgevinkt als het bestand bestaat vóór de eerste regel code van een nieuw project en bij de oplevering van een bestaand project.
- [ ] PRIV-60 (middel) Maak een toepasbaarheidstabel en verklaar elk hoofdstuk dat vervalt. Afgevinkt met tabel en grep-uitvoer.
- [ ] PRIV-76 (hoog) Toets voor het eigen bedrijf en voor elke klant of de Cyberbeveiligingswet geldt. [bron niet gelezen: CBW] Afgevinkt als de notitie voor het eigen bedrijf bestaat en bij nieuwe klanten in de intake staat.

### dicht-architectuur
- [ ] ARCH-05 (hoog) Lever geen test-, voorbeeld- of ontwikkelcode mee naar productie. Afgevinkt met de drie uitvoeren.
- [ ] ARCH-30 (hoog) Leg elke uitzondering op een harde regel vast, ook een overgeslagen stap. Afgevinkt als het bestand bestaat en geen uitzondering over zijn einddatum heen is.
- [ ] ARCH-32 (middel) Leg hersteltermijnen vast en houd een schuldregister bij. Afgevinkt met de tellingen.
- [ ] ARCH-57 (middel) Houd per applicatie een loginventaris bij. Afgevinkt als lijst en werkelijkheid gelijk zijn.

### dicht-invoer
- [ ] INV-13 (hoog) Dwing per parameter één waarde en één type af. Afgevinkt met test en grep.

## Ontwerp: richtlijnen (12)

### dicht-infra
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
- [ ] PRIV-44 (middel) Meet zonder toestemming alleen wat geen of geringe gevolgen heeft, en dan zelf gehost. Afgevinkt met de drie.
- [ ] PRIV-63 (middel) ASVS dekt de AVG niet: gebruik de koppeltabel. Afgevinkt als elke rij een verwijzing heeft.
- [ ] PRIV-64 (laag) Herbeoordeel het niveau bij elke wijziging van functie of gegevens. Afgevinkt met de log.

## Bouwen: hard (268)

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
- [ ] WEB-26 (hoog) Bewaar geen geheimen of persoonsgegevens in web storage. Afgevinkt met grep en schermafbeelding van de opslag.
- [ ] WEB-27 (middel) Ruim de browser op bij uitloggen. [alleen: met login] Afgevinkt met de test.
- [ ] WEB-29 (hoog) Wijzig nooit iets via GET. Afgevinkt met lijst en test.
- [ ] WEB-30 (kritiek) Verdedig elke wijzigende aanvraag met cookie-authenticatie tegen CSRF. Afgevinkt met de testuitvoer.
- [ ] WEB-36 (hoog) Controleer afzender en inhoud bij postMessage. Afgevinkt met grep en test.
- [ ] WEB-37 (middel) Zet niet-vertrouwde inhoud in een iframe met sandbox. Afgevinkt met grep en test.
- [ ] WEB-39 (hoog) Stuur alleen door naar bestemmingen uit een allowlist. Afgevinkt met de testuitvoer.
- [ ] WEB-42 (hoog) Bouw absolute URL's uit de configuratie, nooit uit de Host-header. Afgevinkt met beide.
- [ ] WEB-43 (hoog) Begrens de grootte van elke upload en elke body. Afgevinkt met de test.
- [ ] WEB-44 (hoog) Sta alleen een allowlist van typen toe en controleer de inhoud. Afgevinkt met de testuitvoer.
- [ ] WEB-45 (hoog) Bepaal bestandsnaam en pad zelf. Afgevinkt met test en grep.
- [ ] WEB-46 (kritiek) Sla uploads op waar ze nooit als code worden uitgevoerd. Afgevinkt met de curl-uitvoer.
- [ ] WEB-47 (hoog) Lever bestanden van gebruikers uit als download of vanaf een aparte origin. Afgevinkt met de uitvoer.
- [ ] WEB-48 (middel) Scan bestanden uit niet-vertrouwde bron op malware. Afgevinkt met de logregel.
- [ ] WEB-50 (hoog) Voorkom request smuggling tussen proxy en applicatie. Afgevinkt met versies en uitvoer.
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
- [ ] AUTH-01 (hoog) Minimale en maximale wachtwoordlengte. [alleen: met login] Afgevinkt als de test in CI draait en het schema op alle drie de plekken (registratie, wijzigen, reset) hetzelfde is.
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
- [ ] AUTH-62 (kritiek) Weiger standaard en dwing af op de server, op één plek. Afgevinkt als die test in CI staat.
- [ ] AUTH-63 (kritiek) Controleer bij elk object of het van deze gebruiker en deze tenant is. Afgevinkt als elke route in de lijst een test heeft (zie AUTH-66).
- [ ] AUTH-65 (kritiek) Laat een gebruiker geen velden zetten die zijn rechten bepalen. Afgevinkt als de test groen is.
- [ ] AUTH-67 (hoog) Vertrouw niet alleen op middleware, proxy of route-volgorde. Afgevinkt als dat zo is.
- [ ] AUTH-69 (hoog) Bestanden, exports en back-ups vallen onder dezelfde autorisatie. Afgevinkt als beide kloppen.
- [ ] AUTH-70 (middel) Log geweigerde toegang en geef geen details prijs. Afgevinkt als de test groen is.
- [ ] AUTH-82 (hoog) Beheerinterfaces: MFA, eigen pad, niet alleen een IP-filter. [alleen: met beheer] Afgevinkt als beide kloppen.
- [ ] API-01 (kritiek) Schema-validatie aan elke rand. Elke route heeft een schema voor body, query en params (Fastify `schema` of een zod-parse als eerste regel).
- [ ] API-07 (middel) Decodeer één keer, vóór de validatie. `grep -rn "decodeURIComponent\|urldecode\|rawurldecode" src` toont alleen aanroepen vóór de schema-parse. Test met dubbel gecodeerde invoer.
- [ ] API-12 (kritiek) Faal dicht. Test per controle met een mock die gooit: de actie erna gebeurt niet. Review: elke `catch` zonder `throw` of `return` rond een controle is een bevinding.
- [ ] API-20 (hoog) Begrens verzoeken per route-klasse en per identiteit. Test: N+1 verzoeken binnen het venster geven 429.
- [ ] API-48 (hoog) Geef elke uitgaande aanroep een time-out, een maximale omvang en geen redirects. `grep -rn "fetch(" src` toont bij elke aanroep een `signal`.
- [ ] API-49 (middel) Herhaal begrensd, met oplopende wachttijd, en alleen wat veilig te herhalen is. Eén gedeelde herhaalfunctie met een maximum;
- [ ] API-50 (hoog) Valideer antwoorden van externe diensten net zo streng als invoer van gebruikers. Elke client-module exporteert geparste types;
- [ ] API-53 (kritiek) Start processen zonder shell en met een argumentenlijst. `grep -rnE "\bexec\(|execSync\(|shell: *true" src` is leeg.
- [ ] API-54 (kritiek) Maak bestandspaden zelf en controleer dat ze binnen de basismap blijven. Test met `../`, `..%2f`, een absoluut pad en een naam met een nulbyte: alle geweigerd.
- [ ] API-55 (kritiek) Deserialiseer onvertrouwde data alleen als JSON met een schema. `grep -rnE "unserialize\(|maybe_unserialize\(" .` in PHP toont alleen data uit eigen opslag die niet door gebruikers te zetten is (zie WP voor `maybe_unserialize`).
- [ ] API-56 (kritiek) Voer nooit tekst als code uit. ESLint-regels `no-eval`, `no-implied-eval` en `no-new-func` staan aan en zijn groen. `grep -rnE "\beval\(|new Function\(|vm\.run" src` is leeg.
- [ ] API-57 (hoog) Houd reguliere expressies lineair en begrens de invoer ervoor. ESLint met `eslint-plugin-security` (`detect-unsafe-regex`, `detect-non-literal-regexp`) of `eslint-plugin-regexp` is groen.
- [ ] API-61 (kritiek) Maak onraadbare waarden met een CSPRNG en minimaal 128 bits. `grep -rnE "Math\.random|mt_rand|\brand\(|uniqid\(" src` is leeg in code die tokens, namen van privébestanden of codes maakt. Een UUID v4 mag als id, niet als geheim.
- [ ] API-63 (hoog) Kies bewust tussen hashen en versleutelen. `grep -rnE "createCipher\(|aes-...-(ecb|cbc)|md5|sha1" src` wordt per treffer beoordeeld.
- [ ] API-64 (hoog) Schrijf geen eigen cryptografie. Review: elke plek waar een handtekening of sleutel wordt gemaakt gebruikt HMAC of een bibliotheekfunctie.
- [ ] API-65 (kritiek) Houd geheimen uit code en build en valideer ze bij de start. Afgevinkt met de uitvoer van beide.
- [ ] API-66 (hoog) Log geen geheimen en geen persoonsgegevens. De logger-configuratie bevat `redact`.
- [ ] API-67 (hoog) Zet de strikte TypeScript-opties aan en maak de typecheck een gate. `tsc --showConfig` toont de zes opties.
- [ ] API-68 (hoog) Lint met type-informatie en laat de build erop falen. `eslint .
- [ ] API-69 (middel) Geen `any`, geen cast en geen `!` op data van buiten. De lint van API-68 is groen zonder `eslint-disable` voor `no-explicit-any` of `no-unsafe-*`.
- [ ] API-79 (hoog) Productie-instellingen van PHP tonen geen fouten. `php -i | grep -E "display_errors|expose_php|log_errors|exception_ignore_args"` of de PHP-instellingen in Enhance tonen deze waarden.
- [ ] API-81 (kritiek) Zet geen ontwikkelgereedschap en geen `vendor/` in de webroot. `curl -sI https://<site>/wp-content/plugins/<plugin>/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php`, `/.git/HEAD` en `/composer.json` geven 403 of 404.

### dicht-database
- [ ] DB-25 (kritiek) Alleen geparametriseerde queries. Afgevinkt als de gate groen is en er een test bestaat die een aanhalingsteken in elk zoekveld stuurt.

### dicht-infra
- [ ] INFRA-42 (hoog) Draai een nginx-tak die nog fixes krijgt. Afgevinkt als de versie op een lopende tak staat en buiten elk kwetsbaar bereik valt.
- [ ] INFRA-43 (hoog) Weiger verbindingen voor onbekende hostnamen. Afgevinkt met beide uitvoeren, ook via IPv6.
- [ ] INFRA-44 (hoog) Zet protocollen en ciphers volgens Mozilla "intermediate". Afgevinkt met de drie uitvoeren.
- [ ] INFRA-45 (middel) Zet limieten en time-outs voor aanvragen expliciet. Afgevinkt met beide uitvoeren.
- [ ] INFRA-46 (hoog) Begrens aanvragen per bron in nginx en antwoord met 429. Afgevinkt met de configuratie en de lus per route.
- [ ] INFRA-47 (middel) Herlaad nginx alleen na een geslaagde test en controleer dat de nieuwe configuratie draait. Afgevinkt met de drie uitvoeren.
- [ ] INFRA-50 (hoog) Vernieuw certificaten volledig automatisch. Afgevinkt als elke hostnaam een automatisch vernieuwd certificaat heeft.
- [ ] INFRA-51 (hoog) Laat de webserver het vernieuwde certificaat ook laden. Afgevinkt met de vergelijking en het mechanisme.
- [ ] INFRA-54 (hoog) Bescherm de private sleutel van het certificaat. Afgevinkt met de uitvoer.
- [ ] INFRA-55 (hoog) Versleutel en controleer elke verbinding die de host verlaat. Afgevinkt met de uitvoer.
- [ ] INFRA-56 (hoog) Publiceer precies één SPF-record dat eindigt op een harde weigering. Afgevinkt met de uitvoer en de headers.
- [ ] INFRA-57 (hoog) Onderteken elke verzendroute met DKIM en meet het aan echte mail. Afgevinkt met de headers per route.
- [ ] INFRA-58 (hoog) Zet DMARC op elk domein en kies het eindbeleid per soort mail. Afgevinkt met de uitvoer, een rapport en de vastgelegde keuze.
- [ ] INFRA-59 (middel) Sluit domeinen die niet mailen volledig af. Afgevinkt met de uitvoer per domein.
- [ ] INFRA-62 (hoog) Verwijder DNS-records voordat je de dienst erachter opheft. Afgevinkt met de lijst en de datum.
- [ ] INFRA-64 (middel) Verstuur mail van een site of dienst via geauthenticeerde SMTP. [eigen bron] Afgevinkt met de headers.
- [ ] INFRA-72 (kritiek) Bewaar geheimen in bestanden met modus 600 buiten elke repository. Afgevinkt met de uitvoer.
- [ ] INFRA-76 (middel) Houd geheimen uit commandoregels, logs en shellgeschiedenis. Afgevinkt met de uitvoer.
- [ ] INFRA-77 (hoog) Geef elke dienst een eigen sleutel met de kleinste reikwijdte. Afgevinkt met de lijst.

### dicht-git
- [ ] GIT-01 (hoog) Eén sessie, één worktree, één branch. Afgevinkt met beide uitvoeren.
- [ ] GIT-02 (hoog) De live checkout staat op main en verandert alleen door een merge. Afgevinkt met de drie uitvoeren.
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
- [ ] GIT-69 (hoog) Commit het lockfile en installeer alleen met npm ci. Afgevinkt met de drie.
- [ ] GIT-70 (middel) Lees de diff van het lockfile. Afgevinkt met beide.
- [ ] GIT-71 (hoog) Draai geen install-scripts van afhankelijkheden. Afgevinkt met de uitvoer.
- [ ] GIT-72 (hoog) Installeer geen versie die jonger is dan zeven dagen. Afgevinkt met de drie.
- [ ] GIT-73 (middel) Geen afhankelijkheden uit git of van een losse URL. Afgevinkt met beide, of met elke treffer naast zijn regel in het uitzonderingenregister (ARCH-30) met commit-SHA of hash, reden en einddatum; de bekende uitzondering is SheetJS van de eigen bron van de maker (INV-21).
- [ ] GIT-75 (hoog) Onderbouw elke nieuwe afhankelijkheid kort. Afgevinkt met de commit.
- [ ] GIT-78 (hoog) Controleer de naam van een pakket voordat je het installeert. Afgevinkt met die uitvoer.
- [ ] GIT-80 (middel) Houd productie klein: geen dev-pakketten, geen ongebruikte pakketten. Afgevinkt met beide.
- [ ] GIT-84 (hoog) Beoordeel een WordPress-plugin of thema van een ander vóór installatie. Afgevinkt met die notitie.
- [ ] GIT-91 (hoog) Zet elke image vast op tag plus digest. [bron niet gelezen: CIS] Afgevinkt met de uitvoer.
- [ ] GIT-93 (hoog) Gebruik alleen runtimes die nog beveiligingsfixes krijgen. Afgevinkt met de uitvoer.
- [ ] GIT-95 (kritiek) Geen geheim in een image, een laag of de bouwcontext. [bron niet gelezen: CIS] Afgevinkt met de vier.
- [ ] GIT-96 (hoog) Haal in een Dockerfile niets op zonder controlesom. [bron niet gelezen: CIS] Afgevinkt met de uitvoer.
- [ ] GIT-97 (middel) Weet welke image draait. Afgevinkt met de notitie.

### dicht-wordpress
- [ ] WP-24 (hoog) Laat de uploadmap geen PHP uitvoeren en meet dat op de echte server. Afgevinkt met de curl-uitvoer en de datum.
- [ ] WP-38 (kritiek) Geef elke installatie eigen sleutels en salts en wissel ze na elk incident. Afgevinkt met de uitvoer.
- [ ] WP-39 (hoog) Zet de bestandseditor in wp-admin uit. Afgevinkt met de uitvoer.
- [ ] WP-40 (hoog) Zet debug uit in productie en maak het foutlog onbereikbaar. Afgevinkt met de uitvoer.
- [ ] WP-41 (kritiek) Maak wp-config.php onleesbaar voor anderen en laat er geen kopieën van slingeren. Afgevinkt met de uitvoer.
- [ ] WP-42 (middel) Houd bestanden op 644 en mappen op 755, met het account als eigenaar. Afgevinkt met de uitvoer.
- [ ] WP-43 (hoog) Dwing HTTPS af voor de hele site en voor wp-admin. Afgevinkt met de uitvoer.
- [ ] WP-45 (hoog) Geef elke site een eigen database en een eigen databasegebruiker. Afgevinkt met de uitvoer per site.

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
- [ ] AI-74 (hoog) Begrens per gebruiker de invoer, de uitvoer en het aantal aanroepen. Afgevinkt met de testuitvoer.

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
- [ ] PRIV-57 (hoog) Gebruik het BSN alleen als de wet het voorschrijft. Afgevinkt met de grep.
- [ ] PRIV-65 (hoog) Stel per webwinkel of dienst vast of de toegankelijkheidswet geldt. Afgevinkt als het er staat.
- [ ] PRIV-66 (hoog) Bouw elke nieuwe site op WCAG 2.2 niveau AA. Afgevinkt met beide; een scan alleen vindt maar een deel van de criteria.
- [ ] PRIV-67 (hoog) Maak inloggen, beveiligingsstappen en betalen toegankelijk. Afgevinkt met de testuitvoer.
- [ ] PRIV-68 (middel) Lever een toegankelijkheidsverklaring mee en houd haar actueel. Afgevinkt met de URL en de testuitvoer.
- [ ] PRIV-79 (hoog) Zeg bij de eerste interactie dat iemand met een AI-systeem te maken heeft. Afgevinkt met de testuitvoer.
- [ ] PRIV-82 (middel) Maak bekend dat een deepfake of een ongecontroleerde publieke tekst door AI is gemaakt. Afgevinkt met de testuitvoer.
- [ ] PRIV-84 (kritiek) Laat kaartgegevens nooit door de eigen server of de eigen pagina-code lopen. [bron niet gelezen: PCI] Afgevinkt met beide.
- [ ] PRIV-85 (hoog) Bescherm de pagina die de betaalvelden insluit tegen vreemde scripts. [bron niet gelezen: PCI] Afgevinkt met hostlijst, header en lijst.
- [ ] PRIV-88 (hoog) De bestelknop zegt dat er betaald moet worden, en de kerninformatie staat er direct boven. Afgevinkt met de testuitvoer.
- [ ] PRIV-89 (hoog) Bouw de herroepingsfunctie in elke webwinkel voor consumenten. Afgevinkt met de testuitvoer.

### dicht-architectuur
- [ ] ARCH-10 (middel) Houd ontwikkeling, test en productie gelijk in versies en soort diensten. Afgevinkt als de hoofdversies gelijk zijn.
- [ ] ARCH-33 (middel) Leg per project vast welke testlaag wat bewijst. Afgevinkt met het bestand en de uitvoer.
- [ ] ARCH-34 (hoog) Begin elke bugfix met een test die de fout laat zien. Afgevinkt met de twee uitvoeren.
- [ ] ARCH-36 (hoog) Bedien de pagina in e2e-tests met echte invoer. Afgevinkt met de grep.
- [ ] ARCH-38 (hoog) Test elke functie langs vaste assen, niet alleen het gelukkige pad. Afgevinkt als geen as leeg is zonder reden.
- [ ] ARCH-48 (hoog) Gebruik in tests alleen verzonnen gegevens. Afgevinkt met de grep.
- [ ] ARCH-49 (hoog) Geef tests eigen geheimen en houd inlogtoestanden uit git. Afgevinkt met de drie controles.
- [ ] ARCH-50 (hoog) Laat tests geen echte mail, betaling of oproep naar buiten sturen. Afgevinkt met de opzet en de grep.
- [ ] ARCH-51 (hoog) Beperk een test op productie tot lezen, of markeer en ruim op met exacte id's. [eigen bron] Afgevinkt met het script en de telling.
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
- [ ] INV-04 (hoog) Behandel elk formaat met XML erin als XML. Afgevinkt met de lijst en de testuitvoer.
- [ ] INV-22 (hoog) Saneer als laatste stap en verander de uitvoer daarna niet meer. Afgevinkt met grep en test.
- [ ] INV-24 (hoog) Reken niet op de Markdown-renderer voor veiligheid. Afgevinkt met grep en test.
- [ ] INV-25 (hoog) Gebruik strip_tags en reguliere expressies niet als sanitizer. Afgevinkt met de nagelopen lijst.
- [ ] INV-30 (middel) Bewaar geen locatiegegevens in foto's die anderen kunnen zien. Afgevinkt met grep en de exiftool-uitvoer.
- [ ] INV-31 (hoog) Toon SVG van anderen alleen via een img-element. Afgevinkt met grep en curl.
- [ ] INV-33 (hoog) Behandel magic bytes als een hint en parse het bestand volledig. Afgevinkt met de testuitvoer.
- [ ] INV-37 (hoog) Gebruik wkhtmltopdf niet meer. Afgevinkt met beide uitvoeren.
- [ ] INV-48 (middel) Weiger regeleinden en tekens buiten ASCII voordat een waarde in een antwoordkop komt. Afgevinkt met de uitvoer.
- [ ] INV-50 (hoog) Gebruik in nginx geen $uri in een redirect, een kop of een doorgegeven adres. Afgevinkt met beide uitvoeren.
- [ ] INV-55 (hoog) Laat de build falen op bidi-stuurtekens in broncode. Afgevinkt met de uitvoer van een run met en zonder testbestand.
- [ ] INV-56 (middel) Weiger stuurtekens in velden van één regel. Afgevinkt met de test.
- [ ] INV-58 (middel) Meet lengte in de eenheid van de opslag en kap nooit stil af. Afgevinkt met test, grep en de query.
- [ ] INV-59 (hoog) Ontleed een URL met één WHATWG-parser en gebruik daarna het ontlede object. Afgevinkt met grep en test.
- [ ] INV-62 (middel) Laat proxy en applicatie een pad op dezelfde manier lezen. Afgevinkt met grep en de curl-uitvoer.
- [ ] INV-64 (hoog) Accepteer e-mailadressen alleen in de eenvoudige vorm en beslis niets op het domein van een onbevestigd adres. Afgevinkt met test en grep.
- [ ] INV-68 (middel) Maak tijdelijke bestanden in een eigen, verse map met een onvoorspelbare naam. Afgevinkt met de vier uitvoeren.

### dicht-berichten
- [ ] MSG-01 (hoog) Zet in From alleen een adres op een eigen domein; de inzender hoort in Reply-To. Afgevinkt met grep en de ontvangen koppen.
- [ ] MSG-04 (middel) Bouw elk bericht met een bibliotheek, met één Message-ID, één Date en één From. Afgevinkt met de testuitvoer en de telling.
- [ ] MSG-16 (kritiek) Geef invoer nooit door als afzender aan sendmail of mail(). Afgevinkt met grep en de testuitvoer.
- [ ] MSG-17 (hoog) Codeer elke variabele in een HTML-mailsjabloon. Afgevinkt met de testuitvoer.
- [ ] MSG-18 (hoog) Beslis op het adres dat de parser teruggeeft, met één parser voor de hele keten. Afgevinkt met de testuitvoer.
- [ ] MSG-32 (middel) Markeer elk automatisch verstuurd bericht. Afgevinkt met de koppen per stroom.
- [ ] MSG-41 (hoog) Behandel een webhookadres en een bot-token als geheim. Afgevinkt met de uitvoer en het overzicht.
- [ ] MSG-46 (middel) Behandel een push-abonnement als geheim van één gebruiker en als onvertrouwd adres. Afgevinkt met de testuitvoer.
- [ ] MSG-47 (laag) Verwijder een abonnement bij 404 of 410 en houd de VAPID-sleutel op de server. Afgevinkt met de testuitvoer en grep.
- [ ] MSG-48 (middel) Zet geen gevoelige inhoud in een melding. Afgevinkt met de voorbeelden.

## Bouwen: richtlijnen (40)

### dicht-web
- [ ] WEB-10 (laag) Voorkom DOM clobbering. Afgevinkt met de grep en de configuratie.
- [ ] WEB-14 (middel) Rol CSP uit via report-only en houd de rapportage aan. Afgevinkt met data en een voorbeeldmelding.
- [ ] WEB-18 (middel) Vraag HSTS-preload alleen bewust aan. Afgevinkt met de notitie.
- [ ] WEB-20 (laag) Schakel ongebruikte browserfuncties uit met Permissions-Policy. Afgevinkt met de header.
- [ ] WEB-21 (middel) Isoleer het venster en de bronnen: COOP en CORP. Afgevinkt met headers en e2e-uitvoer.
- [ ] WEB-28 (middel) Geef elke applicatie een eigen hostnaam. Afgevinkt met de lijst.
- [ ] WEB-32 (middel) Bescherm ook het inlogformulier tegen CSRF. Afgevinkt met de test.
- [ ] WEB-38 (laag) Open externe links zonder verwijzing naar het eigen venster. Afgevinkt met de grep.
- [ ] WEB-49 (middel) Herschrijf afbeeldingen en wantrouw archieven. Afgevinkt met de testuitvoer.
- [ ] WEB-57 (laag) Sta alleen de HTTP-methoden toe die de route gebruikt. Afgevinkt met de uitvoer.
- [ ] WEB-70 (middel) Houd botbescherming en login toegankelijk. Afgevinkt met grep en test.

### dicht-api
- [ ] AUTH-11 (middel) Voorkom dat een aanvaller accounts kan blokkeren. [alleen: met login] Afgevinkt als de test groen is.
- [ ] AUTH-68 (middel) Onvoorspelbare id's zijn een extra laag, geen autorisatie. Afgevinkt als de lijst met zulke links gedocumenteerd is.
- [ ] BIZ-38 (laag) Meet op waardevolle stromen of het tempo menselijk is. Test: een afronding binnen de ingestelde ondergrens na de eerste stap wordt geweigerd of naar een extra controle gestuurd.

### dicht-infra
- [ ] INFRA-53 (middel) Leg met CAA vast wie certificaten mag uitgeven. Afgevinkt met de uitvoer en een geslaagde vernieuwing daarna.
- [ ] INFRA-60 (laag) Dwing TLS voor inkomende mail af met MTA-STS en vraag rapporten met TLS-RPT. Afgevinkt met de uitvoer.
- [ ] INFRA-61 (middel) Zet DNSSEC aan en houd twee werkende nameservers. Afgevinkt met de uitvoer.
- [ ] INFRA-65 (laag) Publiceer een security.txt met een geldige vervaldatum. Afgevinkt met de uitvoer.

### dicht-git
- [ ] GIT-08 (laag) Ruim worktrees en branches op zodra het werk gemerged is. Afgevinkt met beide uitvoeren.
- [ ] GIT-13 (middel) Laat elke wijziging lezen voordat hij live gaat. Afgevinkt met die notitie.
- [ ] GIT-37 (middel) Herschrijf de geschiedenis alleen als intrekken niet genoeg is. Afgevinkt met de vier.
- [ ] GIT-42 (hoog) Gebruik zo min mogelijk acties van derden en kijk wat ze zelf aanroepen. Afgevinkt met die lijst.
- [ ] GIT-49 (hoog) Geef CI geen sleutel tot productie. Afgevinkt met de uitvoer.
- [ ] GIT-55 (middel) Laat een bot niet zelf mergen zonder de gate en de wachttijd. Afgevinkt met de instelling en de regel.
- [ ] GIT-66 (middel) Controleer Dockerfiles en Compose-bestanden statisch. [bron niet gelezen: CIS] Afgevinkt met beide.
- [ ] GIT-74 (middel) Gebruik een pakketbeheerder met veilige standaarden. Afgevinkt met beide.
- [ ] GIT-88 (hoog) Beveiligingsupdates direct, de rest na een wachttijd. Afgevinkt met beleid en logboek.
- [ ] GIT-94 (middel) Kies een basisimage van een bekende uitgever en zo klein als werkt. [bron niet gelezen: CIS] Afgevinkt met de lijst.
- [ ] GIT-99 (laag) Reken niet op Docker Content Trust. [bron niet gelezen: CIS] Afgevinkt met beide waar van toepassing.

### dicht-ai-mcp
- [ ] AI-58 (hoog) Lees de toolbeschrijvingen en merk het op als ze veranderen. [bron niet gelezen: AGENTIC] Afgevinkt met het opgeslagen bestand en de hash.

### dicht-privacy
- [ ] PRIV-69 (laag) Ken de uitzonderingen voor inhoud, en gebruik ze niet voor nieuwe inhoud. Afgevinkt met de lijst en een steekproef.

### dicht-architectuur
- [ ] ARCH-11 (middel) Zet beheertaken in de repository en draai ze tegen dezelfde release. Afgevinkt met commit en uitvoer.
- [ ] ARCH-37 (middel) Schrijf e2e-tests op wat de gebruiker ziet, en laat een fout in de console de test breken. Afgevinkt met de grep en de run.
- [ ] ARCH-39 (middel) Houd tests onafhankelijk en behandel een wankele test als een fout. Afgevinkt met de uitvoer.
- [ ] ARCH-46 (middel) Neem een toegankelijkheidsscan op in de e2e-tests. Afgevinkt met beide.
- [ ] ARCH-72 (middel) Toon een eigen foutpagina als de applicatie achter nginx niet antwoordt. Afgevinkt met beide.

### dicht-scripts
Alleen als het project een script, een geplande taak of een lus bevat die in cron, een timer, een uitrol of een andere sessie draait; anders het hele blok `nvt` met die reden.
- [ ] SCR-17 (middel) Schrijf een bestand dat een ander proces leest atomair. Afgevinkt met de testuitvoer.

### dicht-invoer
- [ ] INV-18 (middel) Valideer geparste YAML en TOML met een schema en reken niet op het geraden type. Afgevinkt met de test.
- [ ] INV-26 (middel) Beperk de sanitizer tot HTML als SVG en MathML niet nodig zijn. Afgevinkt met de grep.

### dicht-berichten
- [ ] MSG-20 (middel) Vraag in een mail nooit om een wachtwoord of betaalgegevens, en zeg dat ook. Afgevinkt met grep en het sjabloon.

## Vóór oplevering: hard (64)

### dicht-web
- [ ] WEB-71 (hoog) Gebruik robots.txt nooit als afscherming. Afgevinkt met de drie uitvoeren.
- [ ] WEB-72 (middel) Zet test-, staging- en demo-omgevingen achter een login en op noindex. Afgevinkt met de uitvoer.
- [ ] WEB-73 (middel) Houd een service worker klein in bereik en laat hem geen privédata cachen. Afgevinkt met code en test.

### dicht-git
- [ ] GIT-63 (hoog) Scan elke image die je uitrolt. [bron niet gelezen: CIS] Afgevinkt met de uitvoer.
- [ ] GIT-87 (hoog) Controleer core en plugins tegen de controlesommen van wordpress.org. Afgevinkt met de uitvoer.

### dicht-wordpress
- [ ] WP-55 (hoog) Zet XML-RPC dicht op de server, tenzij een dienst het nodig heeft. Afgevinkt met de curl-uitvoer.
- [ ] WP-56 (middel) Geef geen gebruikersnamen weg. Afgevinkt met de uitvoer.
- [ ] WP-57 (hoog) Begrens inlogpogingen op elk inlogpad. Afgevinkt met de uitvoer per pad.
- [ ] WP-58 (hoog) Verplicht een tweede factor voor elke beheerder. Afgevinkt met de uitvoer en één testinlog.
- [ ] WP-62 (hoog) Vraag bij elke oplevering de bekende WordPress-paden zelf op. Afgevinkt met beide uitvoeren.
- [ ] WP-63 (kritiek) Laat een back-up nooit in de webroot staan. Afgevinkt met beide uitvoeren.
- [ ] WP-64 (hoog) Bewijs elke blokkade met een anonieme aanvraag op de echte server. Afgevinkt met die uitvoer.
- [ ] WP-65 (middel) Zet eigen regels buiten het blok dat WordPress beheert. Afgevinkt met de uitvoer.
- [ ] WP-66 (kritiek) Sluit ingelogde en persoonlijke pagina's uit van de paginacache en meet het. Afgevinkt met de uitvoer van de drie metingen.

### dicht-ai-mcp
- [ ] AI-85 (hoog) Code die een model schreef, gaat door dezelfde gates, en elk voorgesteld pakket wordt gecontroleerd. Afgevinkt met de CI-uitvoer en de onderbouwing.
- [ ] AI-86 (hoog) Wat een agent op een klantsite of in een vreemde repository leest, is onvertrouwd. [bron niet gelezen: AGENTIC] Afgevinkt met de notitie bij de klus.

### dicht-privacy
- [ ] PRIV-45 (middel) De cookielijst in de verklaring is de gemeten lijst. Afgevinkt met de vergelijking.

### dicht-architectuur
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

### dicht-privacy
- [ ] PRIV-91 (middel) Loop bij een voorkant voor bezoekers de juridische checkvragen langs en laat elke twijfel controleren. [eigen bron] Afgevinkt met die lijst.

### dicht-architectuur
- [ ] ARCH-73 (middel) Leg per dienst een prestatie- en beschikbaarheidsdoel vast en meet het. Afgevinkt met de drie onderdelen.
- [ ] ARCH-75 (laag) Leg het prestatiebudget vast als controle die kan falen. Afgevinkt met beide uitvoeren.

### dicht-anti-vibe
- [ ] VIBE-13 (laag) Laden toont een skeleton, geen spinner. Afgevinkt met beide.
- [ ] VIBE-39 (laag) Een submenu blijft open op de schuine weg ernaartoe. Afgevinkt met de uitvoer.
- [ ] VIBE-41 (laag) Cijfers in een tabel zijn even breed. Afgevinkt met de uitvoer.
- [ ] VIBE-42 (laag) Koppen over meer regels zijn gebalanceerd. Afgevinkt met de uitvoer.

## Na oplevering en beheer: hard (31)

### dicht-api
- [ ] AUTH-02 (middel) Geen samenstellingsregels en geen verplichte periodieke wissel. [alleen: met login] Afgevinkt met de test uit AUTH-01 (wachtwoord van 15 kleine letters wordt geaccepteerd).
- [ ] AUTH-85 (hoog) Offboarding: toegang van mensen en systemen direct weg. Afgevinkt als de test groen is en de laatste controle minder dan een kwartaal oud is.

### dicht-infra
- [ ] INFRA-52 (hoog) Bewaak de vervaldatum van buitenaf. Afgevinkt met schermafdruk of uitvoer en de testmelding.
- [ ] INFRA-75 (hoog) Oefen het vervangen van een geheim voordat het nodig is. Afgevinkt met de lijst.
- [ ] INFRA-86 (hoog) Bewaak de bereikbaarheid vanaf een plek buiten de server. Afgevinkt met de lijst en de proefmelding.
- [ ] INFRA-88 (middel) Roteer logs, geef ze een bewaartermijn en houd geheimen en persoonsgegevens eruit. [bron niet gelezen: NEN] Afgevinkt met het overzicht en de steekproef.
- [ ] INFRA-91 (hoog) Schrijf het draaiboek voordat er iets gebeurt. Afgevinkt met het document en de datum.
- [ ] INFRA-92 (hoog) Isoleer eerst en bewaar bewijs voordat je opruimt. Afgevinkt met het verslag.
- [ ] INFRA-93 (kritiek) Vervang na een inbraak elk geheim dat de getroffen omgeving kon lezen. Afgevinkt met de lijst.
- [ ] INFRA-94 (hoog) Herbouw vanaf een schone bron; ruim alleen op met volledige controle. Afgevinkt met het verslag.
- [ ] INFRA-96 (kritiek) Beoordeel bij elk incident met persoonsgegevens direct de meldplicht. [bron niet gelezen: WET] Afgevinkt met het verslag.
- [ ] INFRA-97 (hoog) Geef elke site een eigen systeemgebruiker en een eigen database. Afgevinkt met de lijst en de proef.
- [ ] INFRA-99 (hoog) Weet voor elke ingreep welke back-up je terugweg is. [eigen bron] Afgevinkt met de uitvoer.
- [ ] INFRA-101 (hoog) Test elke afscherming op de webserver die er echt draait. [eigen bron] Afgevinkt met de uitvoer.
- [ ] INFRA-103 (middel) Ruim op wat een project op de hosting achterlaat. Afgevinkt met de uitvoer.

### dicht-git
- [ ] GIT-09 (hoog) Elke repo met waarde heeft een kopie buiten de server. Afgevinkt met uitvoer en datum.
- [ ] GIT-76 (middel) Laat Dependabot versies bijwerken, gegroepeerd en met wachttijd. Afgevinkt met bestand en uitvoer.
- [ ] GIT-86 (hoog) Houd per site een inventaris bij en vervang wat gesloten of verlaten is. Afgevinkt met de uitvoer.
- [ ] GIT-92 (hoog) Laat een bot de digests bijwerken en bouw wekelijks opnieuw. [bron niet gelezen: CIS] Afgevinkt met beide.

### dicht-wordpress
- [ ] WP-47 (kritiek) Laat beveiligingsupdates van de kern automatisch installeren en controleer dat het gebeurt. Afgevinkt met de uitvoer per site.
- [ ] WP-49 (hoog) Leg termijnen vast voor updates van plugins en thema's en houd je eraan. Afgevinkt met de uitvoer en de datum van de laatste run.
- [ ] WP-51 (hoog) Verwijder plugins en thema's die niet in gebruik zijn. Afgevinkt met de uitvoer.
- [ ] WP-52 (hoog) Draai op een PHP-versie die nog beveiligingsupdates krijgt. Afgevinkt met beide waarden.
- [ ] WP-73 (kritiek) Haal plugins en thema's alleen van de maker of van wordpress.org. Afgevinkt met de lijst en de uitvoer.
- [ ] WP-74 (hoog) Houd Elementor en andere paginabouwers strak bij en beperk wie ermee mag werken. Afgevinkt met de uitvoer.
- [ ] WP-76 (hoog) Gebruik geen plugins die code uit de database uitvoeren of bestanden beheren. Afgevinkt met de pluginlijst.

### dicht-privacy
- [ ] PRIV-31 (kritiek) Meld een datalek binnen 72 uur na kennisname, ook als het onderzoek nog loopt. Afgevinkt als het document bestaat en één keer is doorgelopen met een oefengeval.
- [ ] PRIV-33 (hoog) Registreer elk datalek, ook als je het niet meldt. Afgevinkt als het bestand bestaat (ook als het leeg is) en in het draaiboek genoemd wordt.
- [ ] PRIV-34 (hoog) Zorg dat je kunt vaststellen of er toegang is geweest. Afgevinkt met overzicht en proef.
- [ ] PRIV-35 (hoog) Informeer betrokkenen bij een hoog risico, en weet wanneer versleuteling dat voorkomt. Afgevinkt met beide.

### dicht-invoer
- [ ] INV-69 (middel) Ruim tijdelijke bestanden op bij elke afloop en begrens de ruimte. Afgevinkt met de testuitvoer en de configuratie.

## Na oplevering en beheer: richtlijnen (1)

### dicht-infra
- [ ] INFRA-95 (middel) Leg tijdens het incident vast wat je doet en evalueer daarna. Afgevinkt met het verslag.
