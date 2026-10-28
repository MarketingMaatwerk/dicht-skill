# API F: webhooks en externe aanroepen

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/api-code.md` (regelnummer in `regel-index.tsv`).

### API-46 → AUTH-58, AUTH-59
Samengevoegd: "Controleer inkomende webhooks op handtekening, versheid en herhaling" is gedekt door AUTH-58, AUTH-59. Gebruik die regel.

### API-47 Onderteken uitgaande webhooks en bescherm de bezorger tegen SSRF
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Als je zelf webhooks verstuurt naar adressen die een klant opgeeft: accepteer alleen `https://`, weiger elk adres dat na DNS-resolutie niet publiek bereikbaar is (controleer het IP waarmee je echt verbindt), volg geen redirects, onderteken id, tijdstempel en body met een geheim per ontvanger, en herhaal met oplopende tussenpozen tot een maximum.
- Bewijs: Tests met `http://`, `https://127.0.0.1`, `https://[::1]`, een privé-adres, en een host die doorverwijst naar een intern adres: alle geweigerd. Zie WEB voor de volledige SSRF-regel.
- Norm: ASVS 5.0.0 V1.3.6 (L2), V15.3.2 (L2), V13.2.4 (L2); OWASP API Top 10 2023 API7.
- Zie ook: WEB-40, WEB-41, API-48, AI-48, WP-28, INFRA-18, INV-59, INV-61, MSG-27, MSG-46, AUTH-61

### API-48 Geef elke uitgaande aanroep een time-out, een maximale omvang en geen redirects
hoog · hard · alles · tegenlezer: scherpen (04-10-2026)
- Regel: Zet op elke `fetch` en elke HTTP-client een time-out (`signal: AbortSignal.timeout(ms)`), `redirect: 'error'` of `'manual'` tenzij doorverwijzen bedoeld is, een grens op de omvang van het antwoord, en laat certificaatcontrole altijd aan.
- Bewijs: `grep -rn "fetch(" src` toont bij elke aanroep een `signal`. `grep -rn "rejectUnauthorized: false\|NODE_TLS_REJECT_UNAUTHORIZED" .` is leeg. Test met een nepserver die niet antwoordt: de aanroep faalt binnen de ingestelde tijd.
- Norm: ASVS 5.0.0 V15.3.2 (L2), V12.3.2 (L2), V13.1.3 (L3).
- Zie ook: WEB-40, WEB-41, API-47, AI-48, WP-28, INFRA-18, INV-59, INV-61, MSG-27, MSG-46, API-49, ARCH-13, ARCH-14, AI-76, DB-65, API-19, SCR-21, SCR-25, SCR-26, SCR-43, MSG-42

### API-49 Herhaal begrensd, met oplopende wachttijd, en alleen wat veilig te herhalen is
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Herhaal een mislukte externe aanroep alleen bij een tijdelijke fout (time-out, 429, 502, 503, 504), een beperkt aantal keren, met exponentieel oplopende wachttijd plus willekeurige spreiding, en alleen als de aanroep idempotent is of een idempotentiesleutel meestuurt.
- Bewijs: Eén gedeelde herhaalfunctie met een maximum; `grep -rn "while (true)\|for (;;)" src` rond netwerkcode is leeg. Test: een 400 wordt niet herhaald, een 503 maximaal N keer. Na het maximum gaat de taak naar een foutstatus met een alarm, niet stil verloren.
- Norm: ASVS 5.0.0 V13.1.3 (L3), V16.5.2 (L2).
- Zie ook: API-48, ARCH-13, ARCH-14, AI-76, DB-65, API-19, SCR-21, SCR-25, SCR-26, SCR-43, MSG-42, BIZ-40, SCR-45, API-41, ARCH-18

### API-50 Valideer antwoorden van externe diensten net zo streng als invoer van gebruikers
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Haal het antwoord van elke externe API (Mollie, Enhance, registrar, Moneybird, modelleverancier, een andere eigen dienst) door een schema voordat je het gebruikt, opslaat of doorgeeft.
- Bewijs: Elke client-module exporteert geparste types; `grep -rn "await .*\.json()" src` toont steeds een `.parse(` erachter. Test: een antwoord met een ontbrekend of verkeerd getypeerd veld geeft een nette fout en geen halve verwerking.
- Norm: OWASP API Top 10 2023 API10; ASVS 5.0.0 V2.2.1 (L1).
- Zie ook: API-01, AI-11, AI-23, WP-13, ARCH-07

### API-51 Leg vast met welke externe diensten de app praat
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd per dienst een lijst bij van de externe hosts waarmee hij verbinding maakt en laat uitgaand verkeer naar andere bestemmingen niet toe waar dat technisch kan (allowlist in de client, of op de firewall).
- Bewijs: De lijst staat in de projectdocumentatie en komt overeen met `grep -rnoE "https://[a-z0-9.-]+" src | sort -u`. Een nieuwe host die persoonsgegevens ontvangt, leidt tot een update van `policy-state.yaml` (regel van Marketing Maatwerk; zie PRIV).
- Norm: ASVS 5.0.0 V13.1.1 (L2), V13.2.4 (L2).
