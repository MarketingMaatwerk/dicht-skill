# WEB 7: Redirects en server-side aanvragen

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-39 Stuur alleen door naar bestemmingen uit een allowlist
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leid een doorstuuradres nooit rechtstreeks af uit invoer (`?next=`, `?redirect_to=`, `?return=`): gebruik een sleutel die de server naar een vaste URL vertaalt, of sta alleen een relatief pad toe dat met één `/` begint en niet met `//` of `/\`, of vergelijk de host na parsen met een allowlist.
- Bewijs: Test per route met een doorstuurparameter met de waarden `https://evil.example`, `//evil.example`, `/\evil.example` en `https:evil.example`; de `Location` blijft op de eigen host. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V3.7.2 (L2); OWASP Top 10 2025 A01.
- Zie ook: WP-27, AUTH-45

### WEB-40 Haal server-side alleen toegestane adressen op (SSRF)
kritiek · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat de server alleen een URL ophalen die door een gebruiker, een klant, een mail of een model is aangeleverd na deze controles: schema is `https` (of `http` als het moet), poort staat op een allowlist, de hostnaam is opgezocht en álle gevonden adressen (A en AAAA) vallen buiten loopback, privé, link-local (`169.254.0.0/16`, `fe80::/10`), unique local (`fc00::/7`) en het eigen servernetwerk, en de verbinding gaat naar precies het gecontroleerde adres. Waar de bestemmingen bekend zijn: een allowlist van hosts in plaats van deze blocklist.
- Bewijs: Unit-tests op de ophaalfunctie met `http://127.0.0.1/`, `http://[::1]/`, `http://169.254.169.254/`, `http://2130706433/` (decimaal), `http://[::ffff:127.0.0.1]/` en een testdomein dat naar `127.0.0.1` wijst: alle zes worden geweigerd. Daarnaast op netwerkniveau: de container die ophaalt heeft geen route naar interne diensten (zie INFRA). Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V1.3.6 (L2); OWASP Top 10 2025 A01 (CWE-918); OWASP Top 10 2021 A10.
- Zie ook: WEB-41, API-48, API-47, AI-48, WP-28, INFRA-18, INV-59, INV-61, MSG-27, MSG-46

### WEB-41 Volg server-side geen redirects
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet bij elke uitgaande aanvraag naar een door anderen aangeleverde URL het volgen van redirects uit, of controleer elke `Location` opnieuw volgens WEB-40 met een maximum van enkele stappen.
- Bewijs: Test met een lokale testserver die 302 naar `http://127.0.0.1/` geeft; de ophaalfunctie weigert. `grep -rn "fetch(\|axios\|got(\|undici" src/` en per uitgaande aanroep naar externe invoer staat de redirect-instelling. Afgevinkt met test en grep.
- Norm: ASVS 5.0.0 V15.3.2 (L2).
- Zie ook: WEB-40, API-48, API-47, AI-48, WP-28, INFRA-18, INV-59, INV-61, MSG-27, MSG-46

### WEB-42 Bouw absolute URL's uit de configuratie, nooit uit de Host-header
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel links in mails (reset, bevestiging, factuur), canonieke URL's, redirects en OAuth-callbacks samen uit een basis-URL in de configuratie en nooit uit `Host`, `X-Forwarded-Host` of `X-Forwarded-Proto` van de aanvraag; laat de webserver onbekende hostnamen weigeren met een standaard-serverblok. Aanvulling uit AUTH-26: Geldt ook voor uitnodigingslinks; ook niet uit `SERVER_NAME`.
- Bewijs: `curl -s -H 'Host: evil.example' https://<ip>/` en `curl -s -H 'X-Forwarded-Host: evil.example' https://<host>/` geven een respons zonder `evil.example`; `grep -rnE "headers\.host|x-forwarded-host|HTTP_HOST|SERVER_NAME" src/` is leeg of verklaard. Afgevinkt met beide. `ssl_reject_handshake` bestaat sinds nginx 1.19.4 en staat standaard uit.
    Ook (uit AUTH-26): `grep -rnE "req\.(hostname|headers\.host)|HTTP_HOST|SERVER_NAME" src/` levert geen treffer in mail- of linkcode. Test: resetverzoek met `Host: evil.example` levert een mail met de geconfigureerde basis-URL. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V4.1.3 (L2); OWASP Top 10 2025 A05 en A02.
- Dekt ook: AUTH-26
- Zie ook: MSG-19, MSG-20
