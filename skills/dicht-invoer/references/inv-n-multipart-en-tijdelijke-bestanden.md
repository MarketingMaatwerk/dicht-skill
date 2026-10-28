# INV N: multipart en tijdelijke bestanden

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-65 Zet bij multipart elke limiet zelf, lees elke stream uit en weiger een afgekapt bestand
hoog · hard · api | app | mcp · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Stel bij `@fastify/multipart` `fileSize`, `files`, `fields`, `fieldSize` en `parts` expliciet in per route, laat `throwFileSizeLimit` aan (of controleer na het lezen `file.truncated` en gooi het bestand weg), lees of vernietig elke bestandsstream, en houd het pakket op 10.1.1 of hoger.
- Bewijs: `npm ls @fastify/multipart` toont 10.1.1 of hoger; de registratie toont de vijf limieten en geen `throwFileSizeLimit: false` zonder controle op `truncated`; tests: limiet plus één byte (413 en geen bestand op schijf), een aanvraag met 1000 kleine velden (geweigerd), en een upload die halverwege wordt afgebroken (geen achterblijvend bestand in de tijdelijke map). `client_max_body_size` in nginx begrenst het totaal (API-18). Afgevinkt met versie, grep en tests. Zie API-60.
- Norm: ASVS 5.0.0 V5.2.1 (L1), V5.2.4 (L3), V15.2.1 (L1).
- Zie ook: WEB-44, WEB-43, WEB-46, API-60, WP-22, WP-23, WP-24, INV-33, MSG-25

### INV-66 Geef busboy alle limieten mee, want de standaard is onbegrensd
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak busboy (rechtstreeks of via een pakket dat het doorgeeft) altijd aan met `limits` voor `fileSize`, `files`, `fields`, `fieldSize` en `parts`, luister naar het `limit`-signaal of controleer `truncated` aan het eind van de stream, en gebruik `info.filename` nooit als pad.
- Bewijs: `grep -rn "busboy(" src` toont bij elke aanroep `limits` met de vijf waarden; test: limiet plus één byte wordt afgebroken en opgeruimd. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V5.2.1 (L1), V5.3.2 (L1).

### INV-67 Behandel in PHP een lege aanvraag na een te grote upload als fout
middel · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer in eigen PHP-handlers buiten `wp_handle_upload()` eerst `$_FILES[...]['error'] === UPLOAD_ERR_OK`, en behandel een POST-aanvraag met een `Content-Length` groter dan nul maar lege `$_POST` en `$_FILES` als mislukt in plaats van als "niets gewijzigd".
- Bewijs: `grep -rn "\$_FILES" --include=*.php .`: bij elke lezing staat een controle op `error`; test: een aanvraag van 9 MB op elk formulier met een upload geeft een foutmelding en wijzigt niets (`wp option get` of de databaserij vóór en na). De waarden van `post_max_size`, `upload_max_filesize` en `max_file_uploads` op de hosting staan in de projectdocumentatie. Afgevinkt met grep en test. Zie WP-22.
- Norm: ASVS 5.0.0 V5.2.1 (L1), V2.2.1 (L1).

### INV-68 Maak tijdelijke bestanden in een eigen, verse map met een onvoorspelbare naam
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak per verwerking een map met `fs.mkdtemp()` (in PHP een bestand met `tempnam()` of `wp_tempnam()`) onder een map die alleen de dienst kan lezen, schrijf nooit naar een vaste naam in `/tmp`, en zet nooit een tijdelijk of tussenbestand onder de webroot.
- Bewijs: `grep -rnE "['\"\`]/tmp/|sys_get_temp_dir\(\) *\. *['\"]/[a-z]" src .` toont geen vaste naam; `stat -c '%a %U' <tijdelijke basismap>` toont 700 en de gebruiker van de dienst; de systemd-eenheid heeft `PrivateTmp=yes` (Zie de INFRA-regels over systemd); `find <webroot> -newer <markeerbestand van de teststart> \( -name "*.csv" -o -name "*.zip" -o -name "*.sql" -o -name "*.pdf" \)` is leeg na een export. Afgevinkt met de vier uitvoeren.
- Norm: ASVS 5.0.0 V5.3.2 (L1), V5.3.1 (L1); CWE-377.
- Zie ook: INV-69, SCR-14, SCR-31, SCR-04

### INV-69 Ruim tijdelijke bestanden op bij elke afloop en begrens de ruimte
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwijder tijdelijke bestanden in een `finally` (ook bij een fout, een time-out en een afgebroken verbinding), ruim bij de start van de dienst en periodiek alles op wat ouder is dan de langste verwerking, en zet de tijdelijke map op een bestandssysteem of met een quotum dat de database en de logs niet kan verdringen.
- Bewijs: Test: breek een upload en een export halverwege af (verbinding sluiten, proces een fout laten gooien) en toon dat de tijdelijke basismap daarna leeg is; `systemctl cat <dienst>` of de Compose-definitie toont een aparte, begrensde tijdelijke map (`tmpfs` met `size=`, of een eigen volume); een timer of opstartroutine verwijdert resten ouder dan de vastgelegde termijn. Afgevinkt met de testuitvoer en de configuratie. Zie PRIV-25 en API-71.
- Norm: ASVS 5.0.0 V5.2.4 (L3), V15.2.2 (L2); AVG artikel 5 lid 1 onder e.
- Zie ook: INV-68, SCR-14, SCR-31, SCR-04
