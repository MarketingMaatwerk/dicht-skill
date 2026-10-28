# WEB 2: Content Security Policy

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-11 Zet een strikte CSP op elke HTML-respons
hoog · hard · website | wp-thema | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur op elke HTML-respons een `Content-Security-Policy` met minimaal `object-src 'none'`, `base-uri 'none'` en een `script-src` op basis van nonces of hashes; gebruik een allowlist van hosts alleen als nonces aantoonbaar niet kunnen en leg dat vast.
- Bewijs: `curl -sI https://<host>/ | grep -i content-security-policy` toont het beleid met `object-src 'none'`, `base-uri 'none'` en een nonce of hash in `script-src`; de pagina werkt in een Playwright-test zonder CSP-fouten in de console. Voor kritieke delen (login, betaling): het beleid is per respons met nonce of hash (ASVS L3). Afgevinkt met header en consolelog.
- Norm: ASVS 5.0.0 V3.4.3 (L2, per respons met nonce of hash voor L3); OWASP Top 10 2025 A02 en A05.
- Zie ook: AI-14, PRIV-85, WEB-58

### WEB-12 Maak de nonce per respons, willekeurig en onvoorspelbaar
hoog · hard · website | wp-thema | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Genereer voor elke respons een nieuwe nonce van minimaal 128 bit uit een cryptografische bron, base64-gecodeerd, en cache nooit een HTML-respons met nonce in een gedeelde cache.
- Bewijs: Twee keer `curl -s https://<host>/ | grep -o "nonce-[A-Za-z0-9+/=]*"` geeft twee verschillende waarden van minstens 22 base64-tekens; op gecachte, statische pagina's wordt een hash-beleid gebruikt in plaats van een nonce. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V3.4.3 (L2 en L3).

### WEB-13 Geen inline handlers, geen unsafe-eval
middel · hard · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf geen inline event-handlers (`onclick=`), geen `javascript:`-links en geen inline scripts zonder nonce, en neem `'unsafe-eval'` niet op in het beleid.
- Bewijs: `grep -rnE " on[a-z]+=\"|href=\"javascript:" <templates>` is leeg; de CSP-header bevat geen `'unsafe-eval'` en `'unsafe-inline'` alleen als genegeerde terugval naast een nonce met `'strict-dynamic'`. Afgevinkt met grep en header.
- Norm: ASVS 5.0.0 V3.4.3 (L2), V1.3.2 (L1).

### WEB-14 Rol CSP uit via report-only en houd de rapportage aan
middel · richtlijn · website | wp-thema | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet een nieuw of strenger beleid eerst als `Content-Security-Policy-Report-Only` naast het geldende beleid, verzamel de meldingen via `report-to` (met `report-uri` als terugval), los ze op en schakel dan pas over op afdwingen; laat de rapportage daarna aanstaan.
- Bewijs: De report-only-header staat aantoonbaar minstens een week live (datum van de commit en van de overstap), het meldpunt ontvangt meldingen (logregel) en het meldpunt zelf heeft een limiet op grootte en frequentie (WEB-66). Afgevinkt met data en een voorbeeldmelding.
- Norm: ASVS 5.0.0 V3.4.7 (L3, daarom richtlijn).

### WEB-15 Lever CSP als HTTP-header, niet als meta-tag
middel · hard · website | wp-thema | klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur het beleid als responsheader; gebruik `<meta http-equiv>` alleen als je de header niet kunt zetten en zet dan framing-bescherming en rapportage op een andere manier.
- Bewijs: `curl -sI` toont de header; `curl -s <url> | grep -i 'http-equiv="Content-Security-Policy"'` is leeg of bewust en gedocumenteerd. Op gedeelde hosting (Enhance, LiteSpeed): de header komt uit `.htaccess` of uit PHP en is op een echte respons gemeten, niet aangenomen. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V3.4.3 en V3.4.6 (L2).

### WEB-16 Zet Trusted Types aan in eigen applicaties
middel · richtlijn · app · tegenlezer: bevestigd (04-10-2026)
- Regel: Voeg in eigen React- en TypeScript-applicaties `require-trusted-types-for 'script'` toe (eerst report-only) en laat HTML-sinks alleen waarden uit een benoemd beleid accepteren dat door de sanitizer loopt.
- Bewijs: De header staat (report-only of afdwingend) en de e2e-test draait zonder Trusted Types-meldingen. Afgevinkt met header en testlog. Let op de ondersteuning: MDN noemt de API "Baseline 2026, newly available" sinds februari 2026; oudere browsers negeren de regel, dus dit vervangt WEB-02 en WEB-03 niet.
- Norm: Geen eigen ASVS-eis; ondersteunt ASVS 5.0.0 V3.2.2 en V3.4.3.
