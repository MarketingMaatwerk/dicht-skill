# WEB 12: Automatisering, formulieren en e-mail

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-66 Begrens het aantal aanvragen op elke route die iets kost of iets verstuurt
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet een limiet per client op elke route die mail verstuurt, een account of bestelling aanmaakt, inlogt, zoekt, exporteert, een betaald model of een externe API aanroept, of meldingen ontvangt (CSP-rapporten, webhooks); geef 429 bij overschrijding en bepaal de client op het echte IP-adres (WEB-51) of het account.
- Bewijs: `for i in $(seq 1 30); do curl -s -o /dev/null -w "%{http_code}\n" -X POST https://<host>/<route>; done | sort | uniq -c` laat na de limiet 429 zien; dezelfde lus met een wisselende `X-Forwarded-For` ook. De limieten per route staan in de documentatie. Ligt de limiet in nginx, dan geeft die bij overschrijding standaard 503: zet `limit_req_status 429;` (INFRA-46). Afgevinkt met de uitvoer. Alleen op een testomgeving of met een testmailadres op het eigen domein.
- Norm: ASVS 5.0.0 V2.4.1 (L2), V2.1.3 (L2), V15.2.2 (L2); OWASP Top 10 2025 A06; OWASP API Security Top 10 2023 API4 (zie API).
- Zie ook: API-20, INFRA-46, API-22, AUTH-10, WP-57, AI-45, AI-74

### WEB-67 Bescherm elk publiek formulier op de server tegen bots
hoog · hard · website | wp-plugin | wp-thema | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elk publiek formulier (contact, offerte, inschrijving, registratie, reactie, wachtwoord vergeten) minstens twee controles die op de server worden uitgevoerd, naast de limiet uit WEB-66, en laat de inzending bij een mislukte controle niet tot een mail of een record leiden.
- Bewijs: Per formulier een test met `curl` die (a) het lokveld vult, (b) binnen één seconde na het laden post, (c) het bewijsveld weglaat; alle drie worden geweigerd en leveren geen mail op. Voor WordPress-sites van Marketing Maatwerk is dit een eigen mu-plugin (lokveld, ondertekend tijdstempel met minimaal 3 seconden, rekenbewijs, 5 per uur per IP, dagmaximum); het bewijs is de teller `wp option get mmfs_teller --format=json` plus de drie tests. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V2.4.1 (L2), V2.2.2 (L1), V2.4.2 (L3, realistische menselijke timing).

### WEB-68 Voorkom header-injectie in uitgaande mail
hoog · hard · website | wp-plugin | wp-thema | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Weiger elke waarde met een regeleinde (`\r` of `\n`) die in een mailheader belandt (naam, afzender, antwoordadres, onderwerp), stel headers samen via een bibliotheek of als array en nooit via tekstaaneenschakeling, en valideer e-mailadressen vóór gebruik.
- Bewijs: Test per formulier met `%0d%0aBcc:%20test@<eigen-domein>` in elk veld dat in een header komt: de inzending wordt geweigerd of de mail heeft geen extra ontvanger (controleer de ontvangen headers). Afgevinkt met de testuitvoer en de headers van de ontvangen mail.
- Norm: ASVS 5.0.0 V1.3.11 (L2); OWASP Top 10 2025 A05.
- Zie ook: INV-48, INV-56, INV-49, INV-50, MSG-04, MSG-26, MSG-01, MSG-16, INFRA-64, MSG-12, MSG-02

### WEB-69 Laat een formulier nooit naar een adres uit de invoer mailen zonder grens
middel · hard · website | wp-plugin | wp-thema | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet de ontvanger van formuliermail vast in de configuratie; stuur een bevestiging naar het ingevulde adres alleen met een vaste tekst zonder vrije invoer van de inzender, onder de limiet van WEB-66 en een dagmaximum.
- Bewijs: Codecontrole: de ontvanger komt uit de configuratie; de bevestigingsmail bevat geen veld uit de inzending behalve hooguit de naam, gecodeerd en in lengte begrensd; het dagmaximum is getest. Afgevinkt met de code en de test.
- Norm: ASVS 5.0.0 V2.4.1 (L2), V1.3.11 (L2), V2.3.2 (L2).
- Zie ook: INV-64, MSG-18, AUTH-47

### WEB-70 Houd botbescherming en login toegankelijk
middel · richtlijn · website | wp-thema | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik geen puzzel, rekensom of overtypcode die de bezoeker zelf moet oplossen als enige weg door een login of formulier, blokkeer plakken en wachtwoordmanagers niet in inlogvelden, en kies botbescherming die zonder handeling van de bezoeker werkt (lokveld, tijdcontrole, rekenbewijs door de browser).
- Bewijs: `grep -rniE "onpaste|autocomplete=\"off\"" <templates>` is leeg op inlog- en wachtwoordvelden; inloggen lukt in een e2e-test met alleen toetsenbord en geplakte gegevens; het formulier heeft geen puzzel zonder alternatief. Afgevinkt met grep en test.
- Norm: WCAG 2.2 succescriterium 3.3.8 Accessible Authentication (Minimum), niveau AA; ASVS 5.0.0 V2.4.1 (L2). Wettelijke basis: zie PRIV-67 (toegankelijkheid van inloggen, beveiligingsstappen en betalen).
- Zie ook: PRIV-66, PRIV-67, ARCH-46
