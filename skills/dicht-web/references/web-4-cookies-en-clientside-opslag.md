# WEB 4: Cookies en clientside opslag

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-25 Geef elke sessiecookie Secure, HttpOnly, SameSite en het __Host-voorvoegsel
hoog · hard · website | wp-plugin | api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet elke cookie met `Secure`, zet sessie- en tokencookies ook met `HttpOnly` en een bewust gekozen `SameSite` (`Lax` of `Strict`), en noem ze met het voorvoegsel `__Host-` (dus zonder `Domain`, met `Path=/`), tenzij de cookie bewust met andere hosts wordt gedeeld; dan `__Secure-`.
- Bewijs: `curl -sI` op de login-respons: elke `Set-Cookie` heeft `Secure`; de sessiecookie heeft `HttpOnly`, `SameSite` en begint met `__Host-`. In de browser geeft `document.cookie` de sessiecookie niet terug. Afgevinkt met de header en de consoletest. Een cookie met `SameSite=None` heeft een genoteerde reden en altijd `Secure`.
- Norm: ASVS 5.0.0 V3.3.1 (L1), V3.3.2, V3.3.3, V3.3.4 (L2); OWASP Top 10 2025 A07 Authentication Failures.
- Zie ook: AUTH-33, WEB-26

### WEB-26 Bewaar geen geheimen of persoonsgegevens in web storage
hoog · hard · website | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet geen sessie-ID, JWT, refresh-token, API-sleutel of gevoelige klantdata in `localStorage`, `sessionStorage` of IndexedDB; bewaar een sessie in een `HttpOnly`-cookie.
- Bewijs: `grep -rnE "(local|session)Storage\.setItem|indexedDB\.open" src/` en per resultaat genoteerd wat erin gaat; in een ingelogde browser bevat `Object.keys(localStorage)` geen token of persoonsgegeven. Afgevinkt met grep en schermafbeelding van de opslag.
- Norm: ASVS 5.0.0 V14.3.3 (L2; sessietokens zijn daar formeel uitgezonderd, de OWASP Session Management Cheat Sheet raadt ook die af in web storage, en dat volg ik); OWASP Top 10 2025 A07.
- Zie ook: AUTH-33, WEB-25

### WEB-27 Ruim de browser op bij uitloggen
middel · hard · app | website (met login) | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Wis bij uitloggen en bij het verlopen van de sessie alle gegevens van de gebruiker uit de browser: stuur `Clear-Site-Data: "cache", "cookies", "storage"` op de uitlogrespons en wis de applicatietoestand ook in de clientcode.
- Bewijs: E2e-test: inloggen, een pagina met klantdata openen, uitloggen, terugknop indrukken en de pagina opnieuw opvragen; er is geen klantdata zichtbaar en de opslag is leeg. `curl -sI` op de uitlogroute toont `Clear-Site-Data`. Afgevinkt met de test.
- Norm: ASVS 5.0.0 V14.3.1 (L1), V14.3.2 (L2).

### WEB-28 Geef elke applicatie een eigen hostnaam
middel · richtlijn · website | app | api | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Host aparte applicaties, inhoud van gebruikers en test- of demo-omgevingen elk op een eigen hostnaam en nooit als pad onder de origin van een applicatie met login.
- Bewijs: Een lijst van hostnamen per project met per hostnaam één applicatie; geüploade bestanden van gebruikers staan op een aparte host of worden als download geserveerd (WEB-47). Afgevinkt met de lijst.
- Norm: ASVS 5.0.0 V3.5.4 (L2).
