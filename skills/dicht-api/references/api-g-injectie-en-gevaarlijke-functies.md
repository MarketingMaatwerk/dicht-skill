# API G: injectie en gevaarlijke functies

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/api-code.md` (regelnummer in `regel-index.tsv`).

### API-52 → DB-25, DB-26, DB-27, WP-16
Samengevoegd: "Bouw SQL alleen met parameters, ook met een ORM" is gedekt door DB-25, DB-26, DB-27, WP-16. Gebruik die regel.

### API-53 Start processen zonder shell en met een argumentenlijst
kritiek · hard · alles · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Gebruik `execFile` of `spawn` met een vaste opdracht en een array van argumenten, nooit `exec` of `shell: true` met invoer; zet `--` voor argumenten die van buiten komen; in PHP: `proc_open` met een array, geen `shell_exec`, `system`, `exec`, `passthru` of backticks met invoer.
- Bewijs: `grep -rnE "\bexec\(|execSync\(|shell: *true" src` is leeg. In PHP: `grep -rnE "shell_exec|system\(|passthru|popen"` plus een zoekactie op backticks. Test met een waarde die `;` en een waarde die met `-` begint.
- Norm: ASVS 5.0.0 V1.2.5 (L1); OWASP Top 10 2025 A05 Injection (in de uitgave 2021: A03).
- Zie ook: AI-47, SCR-24, SCR-07, SCR-10

### API-54 Maak bestandspaden zelf en controleer dat ze binnen de basismap blijven
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor opslag een zelf gegenereerde naam (id of willekeurige waarde); moet een naam van buiten toch in een pad, los het pad dan op met `path.resolve` en weiger het als het niet met de basismap plus scheidingsteken begint; negeer padinformatie uit archieven.
- Bewijs: Test met `../`, `..%2f`, een absoluut pad en een naam met een nulbyte: alle geweigerd. `grep -rnE "(readFile|createReadStream|writeFile|unlink|sendFile)\(" src` toont geen pad dat rechtstreeks uit een verzoek komt.
- Norm: ASVS 5.0.0 V5.3.2 (L1), V5.3.3 (L3).
- Zie ook: AI-46, WP-25, API-76, WEB-45, WP-29, INV-41, INV-34, SCR-15

### API-55 Deserialiseer onvertrouwde data alleen als JSON met een schema
kritiek · hard · alles · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Gebruik voor data van buiten alleen `JSON.parse` gevolgd door een schema; gebruik nooit `unserialize()` in PHP op invoer (ook niet met `allowed_classes`), nooit `node-serialize`, YAML met eigen types of `eval` als parser.
- Bewijs: `grep -rnE "unserialize\(|maybe_unserialize\(" .` in PHP toont alleen data uit eigen opslag die niet door gebruikers te zetten is (zie WP voor `maybe_unserialize`). `npm ls node-serialize serialize-javascript` wordt beoordeeld. Opgeslagen geserialiseerde data die buiten de server komt, heeft een HMAC.
- Norm: ASVS 5.0.0 V1.5.2 (L2); OWASP Top 10 2025 A08 Software or Data Integrity Failures (zelfde nummer in 2021).
- Zie ook: WP-26, SCR-27, SCR-28, INV-16, INV-17

### API-56 Voer nooit tekst als code uit
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik geen `eval`, `new Function`, `vm.runIn*`, `setTimeout` met een string, of in PHP `eval`, `assert` met een string, `create_function` of `preg_replace` met `/e`, en bouw geen sjablonen uit invoer. Aanvulling uit WEB-05: Ook geen `setInterval` met een string en geen event-handler via `setAttribute('on...', ...)`.
- Bewijs: ESLint-regels `no-eval`, `no-implied-eval` en `no-new-func` staan aan en zijn groen. `grep -rnE "\beval\(|new Function\(|vm\.run" src` is leeg.
    Ook (uit WEB-05): `grep -rnE "\beval\(|new Function\(|set(Timeout|Interval)\( *['\"\`]" src/` is leeg; ESLint `no-eval`, `no-implied-eval` en `no-new-func` staan op error; de CSP bevat geen `'unsafe-eval'` (WEB-13). Afgevinkt met grep, lint en de header.
- Norm: ASVS 5.0.0 V1.3.2 (L1), V1.3.7 (L2).
- Dekt ook: WEB-05
- Zie ook: AI-12, WEB-08

### API-57 Houd reguliere expressies lineair en begrens de invoer ervoor
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf geen regex met geneste of overlappende herhaling (`(a+)+`, `(.*)*`, `(a|a)*`), begrens de lengte van de invoer voordat de regex draait, en bouw nooit een regex uit invoer zonder die te escapen.
- Bewijs: ESLint met `eslint-plugin-security` (`detect-unsafe-regex`, `detect-non-literal-regexp`) of `eslint-plugin-regexp` is groen. `grep -rn "new RegExp(" src` toont alleen constanten of geëscapete invoer. Fastify houdt `allowUnsafeRegex` op `false` en `maxParamLength` op 100 (standaard).
- Norm: ASVS 5.0.0 V1.3.12 (L3), V1.2.9 (L2).

### API-58 Voorkom prototype pollution
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Voeg invoer nooit recursief samen met een bestaand object, gebruik `Map` of `Object.create(null)` voor structuren met sleutels van buiten, controleer eigenschappen met `Object.hasOwn`, en laat `onProtoPoisoning` en `onConstructorPoisoning` van Fastify op `'error'` staan.
- Bewijs: `grep -rnE "merge\(|defaultsDeep|extend\(true|Object\.assign\([^,]+, *(req|request)" src` wordt per treffer beoordeeld. `grep -rn "onProtoPoisoning\|onConstructorPoisoning" src` is leeg (standaard blijft staan). Test: een body met `{"__proto__":{"x":1}}` geeft 400.
- Norm: ASVS 5.0.0 V15.3.6 (L2).

### API-59 Maak exports veilig tegen formule-injectie
middel · hard · api | app | wp-plugin | klantproject | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet bij een CSV- of spreadsheet-export een enkel aanhalingsteken voor elke celwaarde die begint met `=`, `+`, `-`, `@`, tab of een nulteken, en volg de aanhalingsregels van RFC 4180. Aanvulling uit INV-19: Behandel ook waarden die beginnen met een regeleinde (CR of LF) of met de volle-breedte tekens `＝`, `＋`, `－` en `＠`, zet elk veld tussen dubbele aanhalingstekens met verdubbeling van aanhalingstekens in de waarde, en test met een waarde die een scheidingsteken en daarna een formule bevat.
- Bewijs: Unit-test op de exportfunctie met elk van de zes begintekens. Eén gedeelde exportfunctie, geen losse `join(',')`.
    Ook (uit WEB-65): Een unit-test op de exportfunctie met waarden die beginnen met elk van de zes tekens; in de uitvoer staat er een `'` voor. Afgevinkt met de testuitvoer.
    Ook (uit INV-19): Unit-test op de gedeelde exportfunctie met de waarden `=1+2";=1+2`, `\r=1+2`, `＝1+2` en `x,=1+2`: na inlezen met een CSV-parser begint geen enkele cel met een formuleteken. Voor exports die mensen in Excel openen staat in de projectdocumentatie welke variant is gekozen (aanhalingsteken of tab) en dat de export daarna niet meer machinaal wordt ingelezen. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V1.2.10 (L3); RFC 4180 secties 2.6 en 2.7.
- Dekt ook: WEB-65, INV-19
- Zie ook: INV-20

### API-60 Begrens en controleer uploads aan de API-kant
hoog · hard · api | app | wp-plugin | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke uploadroute expliciete limieten (`fileSize`, `files`, `fields`, `parts`), controleer extensie en inhoud (magic bytes) tegen een lijst van toegestane types, sla op onder een eigen naam buiten de webroot, en verwerk de upload als stream.
- Bewijs: De registratie van `@fastify/multipart` toont alle vier de limieten. Tests: te groot bestand (413), verkeerd type met goede extensie, te veel bestanden. De opslagmap wordt niet door nginx geserveerd of heeft uitvoering uit.
- Norm: ASVS 5.0.0 V5.2.1 (L1), V5.2.2 (L1), V5.3.1 (L1), V5.3.2 (L1), V5.2.4 (L3).
- Zie ook: WEB-44, WEB-43, WEB-46, WP-22, WP-23, WP-24, INV-33, INV-65, MSG-25
