# WEB 11: Invoer, fouten en blootstelling

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-60 → API-01
Samengevoegd: "Valideer elke invoer op de server tegen een schema" is gedekt door API-01. Gebruik die regel.

### WEB-61 → API-07
Samengevoegd: "Decodeer één keer, valideer daarna" is gedekt door API-07. Gebruik die regel.

### WEB-62 Toon een generieke foutpagina; debug uit in productie
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef bij een onverwachte fout een generieke melding met een referentienummer en log de details alleen op de server; zet in productie elke debugmodus uit (`WP_DEBUG_DISPLAY` uit, `display_errors` uit, geen stacktraces in API-responsen, geen source maps met broncode voor het publiek).
- Bewijs: Forceer per applicatie een fout (ongeldige JSON, een niet-bestaande ID, een te lange waarde) en bekijk de respons: geen stacktrace, geen query, geen pad; het referentienummer is terug te vinden in het serverlog. `curl -s https://<host>/wp-content/debug.log` geeft 403 of 404. Afgevinkt met respons en logregel.
- Norm: ASVS 5.0.0 V16.5.1 (L2), V13.4.2 (L2), V16.5.4 (L3); OWASP Top 10 2025 A10 Mishandling of Exceptional Conditions en A02.
- Zie ook: API-10, API-11, API-79, WP-40, ARCH-72

### WEB-63 → API-12
Samengevoegd: "Faal gesloten" is gedekt door API-12. Gebruik die regel.

### WEB-64 Zet niets in de webroot dat er niet hoort
hoog · hard · website | wp-plugin | wp-thema | app | klantproject | api · tegenlezer: bevestigd (04-10-2026)
- Regel: Zorg dat `.git`, `.env`, back-ups (`.sql`, `.zip`, `.wpress`, `.bak`), logbestanden, editorbestanden, testscripts en interne documentatie niet via de webserver op te vragen zijn, en zet mapweergave uit. Aanvulling uit GIT-31: Neem `.git` op in `.dockerignore`.
- Bewijs: `for p in .git/config .env wp-config.php.bak backup.zip dump.sql wp-content/debug.log wp-content/ai1wm-backups/ phpinfo.php; do curl -s -o /dev/null -w "%{http_code} $p\n" https://<host>/$p; done` geeft overal 403 of 404; een map zonder index geeft geen lijst. Afgevinkt met de uitvoer.
    Ook (uit GIT-31): `curl -s -o /dev/null -w '%{http_code}' https://<host>/.git/HEAD` en dezelfde aanvraag op het themapad geven 403 of 404; `docker run --rm <image> ls -a /app | grep -c '^\.git$'` geeft 0. Afgevinkt met de uitvoeren. Zie WEB-64 voor de volledige padenlus.
- Norm: ASVS 5.0.0 V13.4.1 (L1), V13.4.3 en V13.4.5 (L2), V13.4.7 (L3), V15.2.3 (L2); OWASP Top 10 2025 A02.
- Dekt ook: GIT-31
- Zie ook: API-81, ARCH-05, WP-63, WP-41, API-25

### WEB-65 → API-59
Samengevoegd: "Maak exports veilig voor spreadsheets" is gedekt door API-59. Gebruik die regel.
