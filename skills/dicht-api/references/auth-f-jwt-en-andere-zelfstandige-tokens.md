# AUTH F: JWT en andere zelfstandige tokens

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/auth.md` (regelnummer in `regel-index.tsv`).

### AUTH-39 Leg het algoritme vast bij verificatie
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef bij elke tokenverificatie een vaste lijst met toegestane algoritmen mee (bij voorkeur één, en nooit `none`), en meng geen symmetrische en asymmetrische algoritmen voor dezelfde sleutel.
- Bewijs: `grep -rn "\.verify(" src/` en controleer dat elke aanroep `algorithms` meegeeft. Tests: een token met `alg: none` en een token met HS256 getekend met de publieke sleutel worden geweigerd. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V9.1.1, V9.1.2 (L1); RFC 8725 §3.1, §3.2; OWASP API Security Top 10 2023 API2.

### AUTH-40 Haal verificatiesleutels uit je eigen configuratie, niet uit het token
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Verifieer tokens met sleutels uit vooraf ingestelde, vertrouwde bronnen per uitgever; volg `jku`, `x5u` of `jwk` uit de header niet zonder allowlist en gebruik `kid` alleen als opzoeksleutel in een vaste verzameling, nooit in een pad, URL of query.
- Bewijs: Codecheck: de JWKS-URL of sleutel staat in configuratie; geen gebruik van headerwaarden in `fetch`, `readFile` of SQL. Test: een token met een vreemde `jku` en een geldige handtekening van de aanvallerssleutel wordt geweigerd. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V9.1.3 (L1); RFC 8725 §3.10.

### AUTH-41 Valideer geldigheid, uitgever, publiek en type van elk token
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer bij elk token `exp` en `nbf`, de exacte `iss`, dat `aud` jouw dienst is, en dat het token van het verwachte soort is (een toegangstoken voor autorisatie, een ID-token alleen als bewijs van inloggen); weiger tokens zonder deze claims.
- Bewijs: Tests: verlopen token, token met andere `aud`, token met andere `iss` en een ID-token op een API-route geven elk 401. Afgevinkt als de vier tests groen zijn.
- Norm: ASVS 5.0.0 V9.2.1 (L1), V9.2.2, V9.2.3 (L2); RFC 8725 §3.8, §3.9, §3.11, §3.12.

### AUTH-42 Symmetrische tokensleutels: willekeurig en minimaal zo lang als de hash
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor HS256 een sleutel van minimaal 256 bits uit een CSPRNG, nooit een door een mens gekozen woord of zin, en gebruik een aparte sleutel per omgeving en per doel.
- Bewijs: Controle zonder de waarde te tonen: `printf %s "$JWT_SECRET" | wc -c` geeft 43 of meer (base64url van 32 bytes) en de waarde staat niet in de repository (`gitleaks detect`). Afgevinkt als beide kloppen. Zie GIT en INFRA voor geheimenbeheer.
- Norm: RFC 7518 §3.2 ("A key of the same size as the hash output ... or larger MUST be used"); RFC 8725 §3.5 (door mensen te onthouden wachtwoorden MUST NOT direct als HMAC-sleutel); ASVS 5.0.0 V11.5.1 (L2), V13.3.1 (L2).

### AUTH-43 Zet geen rechten in een langlevend token
hoog · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat rollen, tenant-lidmaatschap en blokkades bij elk verzoek uit de database of een korte cache komen, of houd tokens met rechten erin zo kort geldig dat een intrekking binnen de vastgelegde termijn (bijvoorbeeld 5 minuten) effect heeft.
- Bewijs: Integratietest: rol verlagen en direct daarna (of na de vastgelegde termijn) met het oude token een beheeractie doen geeft 403. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V8.3.2 (L3: wijzigingen in autorisatiewaarden werken direct, anders compenserende maatregelen).
