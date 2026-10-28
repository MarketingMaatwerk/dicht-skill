# AUTH H: API-sleutels, service-tokens en webhooks

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/auth.md` (regelnummer in `regel-index.tsv`).

### AUTH-53 API-sleutels: willekeurig, herkenbaar, alleen als hash opgeslagen, één keer getoond
kritiek · hard · api | mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Genereer API-sleutels met een CSPRNG met minimaal 128 bits (standaard 256), geef ze een herkenbare prefix per product en soort (bijvoorbeeld `crm_live_`), sla alleen de SHA-256-hash plus de eerste tekens voor herkenning op, en toon de volledige sleutel één keer bij het aanmaken.
- Bewijs: `SELECT * FROM api_keys LIMIT 1` toont een hash en een prefix, geen bruikbare sleutel. De sleutel is na het aanmaakscherm niet meer op te vragen (test: `GET /api-keys/:id` bevat geen sleutel). Een gitleaks- of GitHub-patroon voor de prefix staat in de repository (zie GIT). Afgevinkt als alle drie kloppen.
- Norm: ASVS 5.0.0 V11.5.1 (L2: CSPRNG, minimaal 128 bits), V6.5.2 (L2, naar analogie: bij 112 bits of meer volstaat een standaardhash), V13.3.1 (L2).
- Zie ook: AUTH-54, AI-37, GIT-35, AUTH-55, AI-35, WP-81

### AUTH-54 API-sleutels: scopes, eigenaar, vervaldatum, rotatie zonder storing
hoog · hard · api | mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Koppel elke sleutel aan één tenant en één doel met alleen de benodigde scopes, geef hem een vervaldatum en een veld `last_used_at`, maak het mogelijk een tweede sleutel naast de eerste te hebben tijdens rotatie, en trek een sleutel direct in bij een vermoeden van lekken.
- Bewijs: `\d api_keys` toont `tenant_id`, `scopes`, `expires_at`, `last_used_at`, `revoked_at`. Tests: een sleutel met scope `contacts:read` krijgt 403 op een schrijfroute; een verlopen of ingetrokken sleutel krijgt 401. `docs/auth.md` beschrijft de rotatieprocedure. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V13.3.4 (L3: geheimen verlopen en roteren volgens documentatie), V13.3.2 (L2: minimale rechten), V8.2.1 (L1).
- Zie ook: AUTH-53, AI-37, GIT-35, AUTH-55, AI-35, WP-81

### AUTH-55 Een API-sleutel is geen gebruikerslogin, en hoort in een header
hoog · hard · api | mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik API-sleutels alleen om een systeem of integratie te identificeren, nooit als sessie van een mens in een browser, en neem ze alleen aan in de `Authorization`-header (of een vaste eigen header), nooit in de URL.
- Bewijs: `grep -rnE "api_?key=|token=" nginx-logvoorbeeld src/` levert geen sleutels in URL's op; test: een sleutel in de querystring wordt genegeerd (401). Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V7.2.2 (L1: geen statische geheimen als sessie), V14.2.1 (L1: geen API-sleutel of sessietoken in URL of querystring); OWASP API Security Top 10 2023 API2 ("API keys should not be used for user authentication").
- Zie ook: AUTH-53, AUTH-54, AI-37, GIT-35, AI-35, WP-81

### AUTH-56 Diensten onderling: eigen identiteit per dienst met minimale rechten
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke dienst, worker en cronjob een eigen account of token met alleen de rechten die hij nodig heeft (eigen databasegebruiker, eigen API-token), deel geen beheerdersgeheim tussen diensten en gebruik geen standaardwachtwoorden.
- Bewijs: `\du` in PostgreSQL toont per dienst een eigen rol zonder `SUPERUSER` en zonder `BYPASSRLS`; `grep -rn "POSTGRES_USER\|DATABASE_URL" docker/*/` toont per dienst een andere gebruiker. Afgevinkt als dat klopt. Zie DB en INFRA.
- Norm: ASVS 5.0.0 V13.2.1, V13.2.2, V13.2.3 (L2).
- Zie ook: INFRA-66, INFRA-10, DB-02, INFRA-97, WP-45, WP-68, AI-21

### AUTH-57 Vergelijk geheimen in constante tijd
hoog · hard · alles · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Vergelijk tokens, handtekeningen en sleutels met `crypto.timingSafeEqual` (Node, op buffers van gelijke lengte) of `hash_equals` (PHP), nooit met `==`, `===` of `strcmp`; zoek sleutels op via hun hash in plaats van ze te vergelijken. Aanvulling uit API-62: Geldt ook voor hashes.
- Bewijs: `grep -rnE "(signature|token|secret|hmac)\w* *(===?|!==?)" src/` levert geen treffers op. Test: een handtekening met een afwijkende lengte geeft 401, geen 500. Afgevinkt als beide kloppen.
    Ook (uit API-62): `grep -rnE "(token|secret|sig|signature|hmac|sleutel|apikey)[A-Za-z]* *(===|==|!==|!=) " src` is leeg. Unit-test met een bijna-juiste waarde.
- Norm: ASVS 5.0.0 V11.2.4 (L3: "all cryptographic operations are constant-time, with no 'short-circuit' operations in comparisons, calculations, or returns"; hard voor alles volgens OPEN-VRAGEN A7); OWASP Top 10:2025 A04 (Cryptographic Failures).
- Dekt ook: API-62

### AUTH-58 Inkomende webhooks: handtekening over de ruwe body controleren
kritiek · hard · api | app | wp-plugin | klantproject | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer van elke inkomende webhook de HMAC-handtekening over de ongewijzigde ruwe request-body met het gedeelde geheim, vóór het parsen en vóór enige verwerking, en weiger alles zonder geldige handtekening met 401. Aanvulling uit API-46: Vergelijk de handtekening in constante tijd (AUTH-57); geldt ook voor een MCP-server die webhooks ontvangt.
- Bewijs: Tests: geldige handtekening geeft 2xx; dezelfde body met één gewijzigd teken geeft 401; ontbrekende header geeft 401. Afgevinkt als de drie tests groen zijn.
    Ook (uit API-46): Tests: ontbrekende handtekening, verkeerde handtekening, oude tijdstempel en een herhaald gebeurtenis-id. De eerste drie geven 401 zonder uitleg, de vierde geeft 200 zonder effect. Alleen POST is toegestaan op de route.
- Norm: ASVS 5.0.0 V4.1.5 (L3: handtekening per bericht voor zeer gevoelige transacties; voor Marketing Maatwerk hard omdat betaling een kritiek deel is); OWASP API Security Top 10 2023 API2.
- Dekt ook: API-46
- Zie ook: AUTH-59, MSG-35, MSG-36, MSG-37, MSG-39, MSG-43, MSG-44, WP-82, API-40

### AUTH-59 Inkomende webhooks: bescherm tegen herhaling en dubbele verwerking
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Weiger webhooks waarvan de ondertekende tijdstempel meer dan 5 minuten afwijkt, sla het unieke gebeurtenis-id op en verwerk elk id hooguit één keer, ga er niet van uit dat gebeurtenissen op volgorde aankomen, en antwoord snel met 2xx terwijl het echte werk in een wachtrij gebeurt. Bedient één afhandeling meerdere bronnen, houd dan de kortste antwoordtermijn aan: Meta direct (MSG-37), Slack drie seconden (MSG-44), Mollie 15 seconden (API-40).
- Bewijs: Tests: dezelfde geldige webhook tweemaal geeft één verwerking (unieke index op `event_id`); een webhook met een tijdstempel van 10 minuten oud geeft 4xx. Afgevinkt als beide tests groen zijn. Zie API voor idempotentie in betaalstromen.
- Norm: ASVS 5.0.0 V2.3.3 (L2: een bedrijfshandeling slaagt in zijn geheel of wordt teruggedraaid); OWASP API Security Top 10 2023 API10 (Unsafe Consumption of APIs).
- Zie ook: API-30, API-31, API-33, API-38, DB-68, ARCH-18, AUTH-58, MSG-35, MSG-36, MSG-37, MSG-39, MSG-43, MSG-44, WP-82, API-40

### AUTH-60 → API-36, API-37, API-44
Samengevoegd: "Mollie: vertrouw de webhook niet, haal de status op" is gedekt door API-36, API-37, API-44. Gebruik die regel.

### AUTH-61 Uitgaande webhooks: per ontvanger een geheim, ondertekenen, kunnen roteren
middel · hard · api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Onderteken elke uitgaande webhook met HMAC-SHA256 over id, tijdstempel en body met een geheim per ontvanger van minimaal 24 bytes, stuur een uniek id en een tijdstempel mee, en ondersteun twee geldige geheimen tegelijk tijdens rotatie.
- Bewijs: Test: een uitgaand bericht bevat de drie headers en de handtekening is met het geheim van die ontvanger te verifiëren; na rotatie zijn tijdelijk twee handtekeningen aanwezig. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V4.1.5 (L3).
- Zie ook: API-47
