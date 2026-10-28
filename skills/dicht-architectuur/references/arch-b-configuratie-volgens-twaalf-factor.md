# ARCH B: Configuratie volgens twaalf-factor

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-07 Lees configuratie uit de omgeving en valideer haar bij het opstarten
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Lees alles wat per omgeving verschilt uit omgevingsvariabelen, valideer het bij het opstarten tegen één schema, en laat het proces met een duidelijke fout stoppen als een waarde ontbreekt of ongeldig is; lees `process.env` nergens anders.
- Bewijs: (1) `grep -rn "process\.env" src | grep -v "src/config"` is leeg. (2) Een test start de applicatie met één verplichte variabele weggelaten en verwacht een exitcode ongelijk aan nul binnen enkele seconden. Afgevinkt met grep en test. De lakmoesproef van twaalf-factor geldt: de repository kan openbaar worden zonder dat er een geheim in staat (GIT-32).
- Norm: ASVS 5.0.0 V13.3.1 (L2); twaalf-factor III.
- Zie ook: API-01, AI-11, AI-23, API-50, WP-13

### ARCH-08 Laat beveiliging niet afhangen van de naam van de omgeving
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Schakel geen beveiligingscontrole in of uit op basis van `NODE_ENV`, `WP_ENV` of een vergelijkbare omgevingsnaam; gebruik per gedrag een eigen instelling waarvan de standaard de veilige stand is.
- Bewijs: `grep -rnE "NODE_ENV|WP_ENV|APP_ENV" src` toont alleen regels die logniveau, foutweergave of ontwikkelhulpmiddelen kiezen, geen controle op toegang, handtekening, CSRF, CORS of rate limiting. Een test start de applicatie zonder de variabele en bewijst dat een beveiligde route nog steeds weigert. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V13.4.2 (L2); twaalf-factor III (variabelen zijn los van elkaar, niet gegroepeerd per omgeving).
- Zie ook: ARCH-48, DB-85, INFRA-74, ARCH-50, WEB-72

### ARCH-09 Geef elke release een id en laat de dienst het zelf melden
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Scheid bouwen, uitbrengen en draaien, geef elke release een uniek id (de commit-hash, eventueel met tijdstempel), bak dat id in de build, en laat de draaiende dienst het melden via het interne health-adres en in de eerste logregel na het opstarten.
- Bewijs: `curl -s http://127.0.0.1:<poort>/health` (of `docker exec`) geeft een `version` die gelijk is aan `git rev-parse --short HEAD` van de live checkout. Afgevinkt als de twee waarden in het bewijsbestand (ARCH-53) staan en gelijk zijn. Zie ARCH-24 voor de controle na elke uitrol.
- Norm: twaalf-factor V; ASVS 5.0.0 V13.4.6 (L3): toon de versie niet aan het publiek (ARCH-67).

### ARCH-10 Houd ontwikkeling, test en productie gelijk in versies en soort diensten
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik in ontwikkeling, test en productie dezelfde hoofdversie van de runtime (Node, PHP), dezelfde database met dezelfde hoofdversie en dezelfde webserver; vervang een dienst in tests niet door een lichtere variant.
- Bewijs: De versies staan vast op één plek (`.nvmrc` of `engines`, `composer.json` `config.platform.php`, de image-tag van Postgres) en komen overeen met productie: `node -v`, `php -v` en `SELECT version()` op beide omgevingen in het bewijsbestand. Afgevinkt als de hoofdversies gelijk zijn.
- Norm: twaalf-factor X; NIST SSDF PW.8.2 voorbeeld 4.

### ARCH-11 Zet beheertaken in de repository en draai ze tegen dezelfde release
middel · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf elke eenmalige ingreep in gegevens (herstelscript, bijvullen, opschonen) als een bestand in de repository dat door review gaat, en draai het met dezelfde code en configuratie als de draaiende release; typ geen losse SQL of `wp eval` op productie.
- Bewijs: De map `scripts/` of `migrations/` bevat het script met datum en doel; de commit staat vóór de uitvoering; de uitvoer staat in het bewijsbestand of het logboek. Afgevinkt met commit en uitvoer.
- Norm: twaalf-factor XII.

### ARCH-12 Draai de dienst en de tests in UTC en sla tijd op met tijdzone
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet voor elke dienst en voor de testopdracht expliciet `TZ=UTC`, schrijf logtijden in UTC of met een expliciete afwijking, en reken alleen bij het tonen om naar lokale tijd.
- Bewijs: `systemctl show <unit> -p Environment` of de Compose-definitie toont `TZ=UTC`; het testscript in `package.json` zet `TZ=UTC`; een logregel heeft een tijd die op `Z` eindigt. Afgevinkt met de drie waarnemingen. Zie DB-77 voor kolomtypes.
- Norm: ASVS 5.0.0 V16.2.2 (L2).
- Zie ook: DB-74, INFRA-71, BIZ-26, BIZ-27, BIZ-28, BIZ-29, SCR-40, SCR-52
