# ARCH I: Logging, audit-log, health-checks en alarmering

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-57 Houd per applicatie een loginventaris bij
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per applicatie in één tabel vast welke gebeurtenissen worden gelogd, in welk formaat, waar de regels terechtkomen, wie ze mag lezen, hoe lang ze bewaard blijven en waarvoor ze worden gebruikt, en laat de applicatie nergens anders naartoe loggen dan naar wat in die tabel staat.
- Bewijs: De tabel staat in `docs/ARCHITECTURE.md` of `docs/LOGGING.md`; `find <app-map> /var/log -name "*.log" -newer <referentie>` en `docker inspect --format '{{.HostConfig.LogConfig}}'` tonen alleen bestemmingen uit de tabel. Afgevinkt als lijst en werkelijkheid gelijk zijn. De servertabel uit INFRA-88 en deze tabel verwijzen naar elkaar.
- Norm: ASVS 5.0.0 V16.1.1 (L2), V16.2.3 (L2).

### ARCH-58 Log gestructureerd, één regel per gebeurtenis, met vaste velden
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf elke logregel als één JSON-object met minimaal: tijd in UTC (ISO 8601), niveau, naam en release-id van de applicatie, de gebeurtenisnaam (ARCH-59), het correlatie-id (ARCH-60), de route en methode, de uitkomst (statuscode of resultaat), de duur, en waar bekend het tenant-id en het gebruikers-id als interne sleutel (geen naam of e-mailadres).
- Bewijs: Een steekproef van honderd regels uit de testrun is regel voor regel geldige JSON (`jq -e . >/dev/null`) en elke regel met een `route` heeft de verplichte velden (`jq -e 'select(.route) | .time and .level and .event and .req_id'`). Afgevinkt met de uitvoer. Log de route als patroon (`/orders/:id`), niet de volledige URL met parameters (WEB-55, ASVS V14.2.1).
- Norm: ASVS 5.0.0 V16.2.1 (L2), V16.2.2 (L2), V16.2.4 (L2).
- Zie ook: ARCH-59, AUTH-14, AUTH-70, ARCH-63

### ARCH-59 Gebruik één vaste woordenlijst voor beveiligingsgebeurtenissen
middel · richtlijn · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef beveiligingsgebeurtenissen in alle projecten dezelfde namen, bij voorkeur die van de OWASP Logging Vocabulary (`authn_login_success`, `authn_login_fail`, `authn_login_lock`, `authz_fail`, `authz_admin`, `input_validation_fail`, `excess_rate_limit_exceeded`, `sensitive_read`, `sensitive_delete`, `malicious_direct_reference`, en voor MCP `mcp_prompt_injection`), en leg eigen toevoegingen vast in de loginventaris.
- Bewijs: `grep -rhoE "event: ?'[a-z_]+'" src | sort -u` (of gelijkwaardig) geeft alleen namen die in de inventaris staan; een test per gebeurtenis bewijst dat hij wordt geschreven. Afgevinkt met de lijst.
- Norm: ASVS 5.0.0 V16.2.4 (L2), V16.3.1 tot en met V16.3.3 (L2).
- Zie ook: AUTH-14, AUTH-70, ARCH-58, ARCH-63

### ARCH-60 Geef elk verzoek een correlatie-id en neem het overal mee
middel · hard · api | app | mcp · tegenlezer: scherpen (04-10-2026)
- Regel: Maak per binnenkomend verzoek een willekeurig id aan, zet het in elke logregel van dat verzoek, geef het mee aan taken in de wachtrij en aan uitgaande aanroepen, en gebruik het als referentienummer in de foutmelding aan de gebruiker; neem een id uit een kopregel alleen over van de eigen proxy.
- Bewijs: Een test doet één verzoek dat een taak aanmaakt en een fout geeft; het id in de foutrespons is terug te vinden in de logregels van de route en van de worker. Een verzoek van buiten met een eigen `X-Request-Id` krijgt een ander id in de logs. Afgevinkt met de testuitvoer. Zie WEB-62 voor het referentienummer.
- Norm: ASVS 5.0.0 V16.2.1 (L2).

### ARCH-61 Schrijf logs naar de standaarduitvoer en laat de omgeving ze opslaan
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat de applicatie haar logregels naar stdout schrijven en laat systemd, Docker of de hosting de opslag, de rotatie en het doorsturen regelen; open en roteer vanuit de applicatie zelf geen logbestanden.
- Bewijs: `grep -rnE "createWriteStream|appendFile|error_log\(.*, ?3" src` toont geen logbestemming; `journalctl -u <unit> -n 5 -o cat` of `docker logs --tail 5` toont de JSON-regels. Afgevinkt met beide. WordPress op gedeelde hosting is de uitzondering: daar geldt WP-40.
- Norm: twaalf-factor XI.

### ARCH-62 Log alleen benoemde velden en scan de testlogs in de gate
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef aan de logger alleen velden mee die je bij naam kiest, nooit een heel verzoek, een hele gebruiker, een hele fout van een externe dienst of de inhoud van een formulier, en laat de gate de logs van de testrun doorzoeken op de nepgeheimen en neppersoonsgegevens die de tests gebruiken.
- Bewijs: De testsuite gebruikt herkenbare nepwaarden (bijvoorbeeld het wachtwoord `Zx-nep-geheim-9431` en het adres `ztest-log@example.com`); de gate bewaart de loguitvoer van de run en `grep -cE "Zx-nep-geheim-9431|ztest-log@|Bearer [A-Za-z0-9._-]{20,}" testlog.jsonl` geeft 0. Afgevinkt met de uitvoer. Zie AI-67 voor logs van prompts.
- Norm: ASVS 5.0.0 V16.2.5 (L2), V14.2.4 (L2); AVG artikel 5 lid 1 onder c (zie PRIV).
- Zie ook: API-66, DB-88, INFRA-88, AUTH-14, AI-67, AI-52, GIT-39

### ARCH-63 Log ook mislukte validatie, limieten, onverwachte fouten en starten en stoppen
middel · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf naast inlog- en autorisatiegebeurtenissen (AUTH-14, AUTH-70) een logregel voor: geweigerde invoer, een bereikte snelheids- of bedrijfslimiet, een mislukte handtekening- of tokencontrole, elke onverwachte fout, een mislukte TLS-verbinding naar een achterliggende dienst, het starten en stoppen van de applicatie, en een wijziging van configuratie of schakelaars.
- Bewijs: Per soort gebeurtenis een test die hem uitlokt en de logregel met de juiste `event` terugvindt; de lijst staat in de loginventaris (ARCH-57). Afgevinkt met de testuitvoer. Een waarde die niet in een vaste keuzelijst voorkomt (`input_validation_discrete_fail`) kan alleen door manipulatie ontstaan en verdient een eigen alarm.
- Norm: ASVS 5.0.0 V16.3.3 (L2), V16.3.4 (L2); OWASP Top 10 2025 A09.
- Zie ook: ARCH-59, AUTH-14, AUTH-70, ARCH-58

### ARCH-64 Schrijf de auditregel in dezelfde transactie als de handeling
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Houd het audit-log apart van het gewone applicatielog, in een eigen tabel waar de applicatierol alleen kan invoegen (AUTH-84), schrijf de regel in dezelfde databasetransactie als de handeling die hij beschrijft, en laat de handeling mislukken als de auditregel niet geschreven kan worden.
- Bewijs: (1) De rechtencontrole uit AUTH-84 geeft `f, f`. (2) Een test laat het invoegen in `audit_log` mislukken en bewijst dat de handeling is teruggedraaid. (3) Een test per gevoelige handeling telt precies één auditregel. Afgevinkt met de drie uitvoeren. `details` bevat geen inhoud van het object, alleen welke velden zijn gewijzigd. De vorm is uitgewerkt in Open vragen, punt 4.
- Norm: ASVS 5.0.0 V16.3.2 (L2, voor L3 ook elke toegang tot gevoelige gegevens), V16.4.2 (L2), V2.3.3 (L2); NEN 7513 voor zorgdata (zie PRIV).
- Zie ook: AUTH-84, ARCH-65, INFRA-89, PRIV-54, DB-91, AI-52

### ARCH-65 Maak wijzigen van het audit-log zichtbaar
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur de auditregels ook naar een plek die de applicatie en haar databaserol niet kunnen wijzigen (de kopie buiten de server uit INFRA-89), en vergelijk periodiek het aantal regels en de hoogste id tussen bron en kopie; voor kritieke delen en zorgdata is dit hard. De dagelijkse versleutelde kopie zelf is hard voor elk project (INFRA-89, besluit 23); de periodieke vergelijking blijft richtlijn buiten kritieke delen en zorgdata.
- Bewijs: Een geplande taak vergelijkt bron en kopie en meldt een verschil op het alarmkanaal; een proef waarbij op de testomgeving één regel wordt verwijderd (met de eigenaarrol) geeft een melding. Afgevinkt met de proefmelding. Een ketting van hashes per regel is een alternatief; daarvoor is geen primaire bron met een uitgewerkt ontwerp gelezen (zie Niet bevestigd 6).
- Norm: ASVS 5.0.0 V16.4.2 (L2), V16.4.3 (L2).
- Zie ook: ARCH-64, AUTH-84, INFRA-89, PRIV-54, DB-91, AI-52

### ARCH-66 Bepaal wat er gebeurt als loggen mislukt
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg vast en test wat de applicatie doet als de logbestemming vol of onbereikbaar is: gewone logregels mogen verloren gaan zonder dat verzoeken mislukken, auditregels niet (ARCH-64), en invoer van gebruikers mag de logs niet kunnen vullen tot de schijf vol is.
- Bewijs: Een proef op de testomgeving met een volle of alleen-lezen logbestemming: de kernroute blijft antwoorden en er komt een alarm (INFRA-87, schijf). De lengte van gelogde invoervelden is begrensd in de logger. Afgevinkt met het verslag van de proef.
- Norm: ASVS 5.0.0 V16.4.1 (L2).

### ARCH-67 Maak twee health-adressen: leeft het proces, en kan het werken
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke dienst een adres dat alleen zegt dat het proces leeft (geen afhankelijkheden) en een adres dat de echte functie toetst (een query op de database met de runtime-rol, de migratieversie volgens DB-42, de wachtrij); gebruik het eerste voor het herstartbeleid en het tweede voor de uitrol en de bewaking, en maak beide alleen intern bereikbaar of zonder details.
- Bewijs: `curl -s 127.0.0.1:<poort>/health` en `/ready` geven 200; met de database gestopt op de testomgeving blijft `/health` 200 en geeft `/ready` 503; van buiten geeft `curl -s https://<host>/ready` een 404 of alleen een status zonder versie en zonder namen van onderdelen. De Docker-healthcheck heeft een ingestelde `interval`, `timeout`, `retries` en `start_period`. Afgevinkt met de vier waarnemingen.
- Norm: ASVS 5.0.0 V13.4.5 (L2), V13.4.6 (L3).
- Zie ook: INFRA-35, ARCH-69, INFRA-86, INFRA-87, DB-97, DB-47, AI-83, INFRA-52

### ARCH-68 Meet per dienst vier signalen
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Meet per dienst de responstijd (p50 en p95, geslaagd en mislukt apart), het aantal verzoeken, het aandeel fouten (5xx en mislukte taken) en de verzadiging (verbindingen in de pool, lengte van de wachtrij, geheugen), en maak die cijfers per dag opvraagbaar.
- Bewijs: Een opdracht of overzicht dat de vier cijfers voor de laatste 24 uur toont. De goedkoopste weg is de gestructureerde logs uit ARCH-58: `jq -s 'map(select(.route)) | group_by(.route) | map({route: .[0].route, n: length, fouten: (map(select(.status>=500))|length)})'`. Afgevinkt met de uitvoer. Een aparte metriekenstapel is niet verplicht; als je er een kiest, zijn in OpenTelemetry voor JavaScript sporen en metrieken stabiel en logs nog in ontwikkeling.
- Norm: ASVS 5.0.0 V15.1.3 (L2).

### ARCH-69 Alarmeer op symptomen, met een drempel en een actie
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel per dienst alarmen in op wat de gebruiker merkt en wat op een aanval wijst: gereedheidscontrole mislukt, aandeel 5xx boven de drempel, p95 boven de drempel, een taak in de dode-brievenbak, de wachtrij boven de drempel, een piek in `authn_login_fail`, elke `authz_fail` over de tenantgrens, en een uitblijvende geplande taak; geef elk alarm een drempel, een kanaal, een actie in het runbook en een geteste proefmelding.
- Bewijs: Een tabel met per alarm: signaal, drempel, venster, kanaal, runbook-kop, datum van de laatste proefmelding. Voorstel voor de beginwaarden, als eigen keuze: 5xx boven 2 procent over 5 minuten; p95 boven twee keer het doel uit ARCH-72 over 10 minuten; meer dan 20 `authn_login_fail` per 5 minuten in totaal of meer dan 5 per account; elke taak in de dode-brievenbak; elke `authz_fail` met een ander tenant-id. Afgevinkt met de tabel en de proefmeldingen. Het kanaal is onafhankelijk van wat het bewaakt (INFRA-86).
- Norm: ASVS 5.0.0 V16.3.1 tot en met V16.3.3 (L2), V16.4.3 (L2); OWASP Top 10 2025 A09.
- Zie ook: ARCH-67, INFRA-35, INFRA-86, INFRA-87, DB-97, DB-47, AI-83, INFRA-52

### ARCH-70 Geef verzoeken over procesgrenzen een standaard spoorkop mee
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zodra een verzoek meer dan één eigen proces raakt (API en worker, API en MCP-server), geef het correlatie-id door in de W3C-kop `traceparent` en log het spoor-id in elk proces; zet er geen persoonsgegevens in en vertrouw een `traceparent` van buiten niet voor beslissingen.
- Bewijs: Een test volgt één verzoek door twee processen en vindt hetzelfde spoor-id (32 hexadecimale tekens) in beide logs. Afgevinkt met de logregels. Volledige tracing met tijdsduren per stap is voor een monoliet met één worker niet nodig.
- Norm: geen ASVS-eis; ASVS 5.0.0 V16.2.4 (L2) voor het correleren.

### ARCH-71 Deel logs in drie soorten in en geef elke soort een eigen termijn
middel · hard · alles · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Onderscheid applicatielogs (foutopsporing), beveiligingslogs (inloggen, toegang, weigeringen, beheer) en het audit-log (wie deed wat met welke gegevens), en leg per soort een bewaartermijn vast die automatisch wordt afgedwongen; bewaar niets korter en niets langer dan die termijn. De termijn per soort volgt uit het doel (PRIV-23); de logging van zorgsystemen bewaar je ten minste vijf jaar (PRIV-55).
- Bewijs: De loginventaris (ARCH-57) noemt per soort de termijn en het mechanisme (logrotate, `journald` `MaxRetentionSec`, een opruimtaak op de audittabel); de oudste regel per soort is niet ouder dan de termijn. Afgevinkt met inventaris en meting. Voorstel voor de synthese en PRIV: applicatielogs 30 dagen, beveiligingslogs minimaal 6 maanden, audit-log volgens de wettelijke en contractuele termijn van het project.
- Norm: ASVS 5.0.0 V16.1.1 (L2), V14.2.4 (L2); AVG artikel 5 lid 1 onder e (opslagbeperking, zie PRIV).
- Zie ook: PRIV-23, PRIV-55, INFRA-88, INFRA-33

### ARCH-72 Toon een eigen foutpagina als de applicatie achter nginx niet antwoordt
middel · richtlijn · website | api | app · tegenlezer: scherpen (04-10-2026)
- Regel: Stel in nginx voor 502, 503 en 504 een statische eigen foutpagina in, en laat nginx foutantwoorden van de applicatie alleen onderscheppen op HTML-routes, niet op de API waar de client het foutformaat uit API-11 verwacht.
- Bewijs: Op de testomgeving met de applicatie gestopt geeft `curl -s -o /dev/null -w "%{http_code}" https://<host>/` 502 of 503 en toont de inhoud de eigen pagina zonder servernaam of versie; `curl -s https://<host>/api/...` geeft bij een fout van de applicatie zelf nog steeds `application/problem+json`. Afgevinkt met beide. Herladen van nginx volgens INFRA-47.
- Norm: ASVS 5.0.0 V16.5.1 (L2), V13.4.6 (L3).
- Zie ook: WEB-62, API-10, API-11, API-79, WP-40
