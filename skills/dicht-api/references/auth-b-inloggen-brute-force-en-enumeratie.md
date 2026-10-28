# AUTH B: Inloggen, brute force en enumeratie

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/auth.md` (regelnummer in `regel-index.tsv`).

### AUTH-10 Begrens inlogpogingen per account en per bron
kritiek · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Begrens mislukte inlogpogingen per account (oplopende vertraging, en nooit meer dan 100 opeenvolgende mislukte pogingen voordat de factor wordt uitgeschakeld) en daarnaast per IP-adres, en leg de gekozen drempels vast in de projectdocumentatie.
- Bewijs: Integratietest: de zesde foute poging op één account binnen het venster geeft 429 of een vertraging, ook vanaf een ander IP; een script met 30 accounts vanaf één IP loopt tegen de IP-limiet aan. Document `docs/auth.md` noemt de drempels. Afgevinkt als de test groen is en het document bestaat.
- Norm: ASVS 5.0.0 V6.3.1 (L1), V6.1.1 (L1: gedocumenteerd, inclusief voorkomen van kwaadaardige lockout); NIST SP 800-63B-4 §3.2.2 (SHALL maximaal 100 opeenvolgende mislukte pogingen per authenticator per account); OWASP Top 10:2025 A07.
- Zie ook: API-20, WEB-66, INFRA-46, API-22, WP-57, AI-45, AI-74, AUTH-12, WP-56, AUTH-13, WP-55

### AUTH-11 Voorkom dat een aanvaller accounts kan blokkeren
middel · richtlijn · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik oplopende vertraging of een extra uitdaging in plaats van een harde, langdurige blokkade na enkele pogingen, en geef de echte gebruiker altijd een weg terug (reset of tweede factor).
- Bewijs: Test: na het bereiken van de drempel kan de gebruiker via de resetmail binnen het venster weer inloggen. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V6.1.1 (L1: "prevent malicious account lockout").

### AUTH-12 Verklap niet of een account bestaat
middel · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef op login, wachtwoordreset en registratie hetzelfde antwoord, dezelfde statuscode en een vergelijkbare responstijd, ongeacht of het account bestaat.
- Bewijs: Test die 20 keer een bestaand en 20 keer een onbekend adres aanbiedt op login en reset: identieke body en status, en het verschil in mediaan-responstijd blijft onder een vastgelegde marge (bijvoorbeeld 50 ms). Afgevinkt als de test in CI staat.
- Norm: ASVS 5.0.0 V6.3.8 (L3; voor Marketing Maatwerk hard op login en reset omdat login een kritiek deel is).
- Zie ook: AUTH-10, WP-57, WP-56, AUTH-13, WP-55

### AUTH-13 Ken en bewaak elk inlogpad
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg alle manieren vast waarop iemand of iets zich kan authenticeren (formulier, API, magic link, OAuth, API-sleutel, MCP, XML-RPC, applicatiewachtwoord, CLI, supporttoegang) en dwing op elk pad dezelfde sterkte en dezelfde limieten af; schakel paden die je niet gebruikt uit.
- Bewijs: `docs/auth.md` bevat een tabel met alle paden, per pad de factor, de limiet en de test. Voor WordPress: `curl -s -o /dev/null -w '%{http_code}' -X POST https://site/xmlrpc.php` geeft 403 of 405 als XML-RPC niet nodig is. Afgevinkt als elk pad een test heeft.
- Norm: ASVS 5.0.0 V6.1.3, V6.3.4 (L2); OWASP API Security Top 10 2023 API2 ("ken alle mogelijke flows").
- Zie ook: AUTH-10, WP-57, AUTH-12, WP-56, WP-55, ARCH-83, API-25, WP-62

### AUTH-14 Log elke authenticatiegebeurtenis, zonder geheimen
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Log elke geslaagde en mislukte login, reset, factorwijziging en uitlog met tijd, account-id, bron en gebruikte factor; log nooit wachtwoorden, tokens, sessie-id's of OTP-codes (hooguit een hash of de eerste tekens).
- Bewijs: `grep -rniE "password|token|secret|authorization" logs/ | head` op een testomgeving na een volledige login-, reset- en API-ronde levert geen waarden op. Test: een mislukte login schrijft een regel met `event=authn_login_fail`. Afgevinkt als beide kloppen.
- Norm: ASVS 5.0.0 V16.3.1 (L2), V16.2.5 (L2: sessietokens alleen gehasht of gemaskeerd); OWASP Top 10:2025 A09.
- Zie ook: ARCH-62, API-66, DB-88, INFRA-88, AI-67, AI-52, GIT-39, ARCH-59, AUTH-70, ARCH-58, ARCH-63

### AUTH-15 Meld verdachte logins en wijzigingen aan de gebruiker
middel · richtlijn · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur de gebruiker een bericht bij een login vanaf een nieuw apparaat, bij een juist wachtwoord met mislukte tweede factor, en bij elke wijziging van wachtwoord, e-mailadres of MFA; stuur de melding van een e-mailwijziging naar het oude adres.
- Bewijs: Integratietest: e-mailwijziging levert een mail op het oude adres op. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V6.3.5, V6.3.7 (L3).
