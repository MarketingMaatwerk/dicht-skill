# AUTH K: Beheerders, impersonatie, support en audit

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/auth.md` (regelnummer in `regel-index.tsv`).

### AUTH-79 Impersonatie: apart, zichtbaar, beperkt, gelogd
hoog · hard · api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw "inloggen als klant" alleen als aparte functie voor een eigen permissie, met een verplichte reden, een eigen sessie die de echte beheerder én de klant vastlegt, een korte maximale duur, een zichtbare balk in de interface, een verbod op het wijzigen van inloggegevens en betaalgegevens, en een auditregel voor het begin, het einde en elke schrijfactie.
- Bewijs: Tests: een beheerder zonder de permissie krijgt 403; tijdens impersonatie geeft het wijzigen van wachtwoord, e-mail, MFA of API-sleutels 403; de auditlog bevat `actor_id` en `subject_id`; de sessie verloopt na de ingestelde duur. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V8.3.3 (L3: besluiten op basis van de oorspronkelijke aanvrager), V16.3.1, V16.3.2 (L2), V6.4.6 (L3: beheerders mogen het wachtwoord van een gebruiker niet kennen of kiezen), V8.4.2 (L3).

### AUTH-80 Beheerders starten een reset, ze kiezen geen wachtwoord
middel · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef beheerders en support alleen de mogelijkheid om het resetproces voor een gebruiker te starten (de gebruiker krijgt zelf de link), niet om een wachtwoord in te stellen of in te zien.
- Bewijs: Codecheck: de beheer-API heeft geen route die een wachtwoord als invoer accepteert voor een andere gebruiker. Test: `POST /admin/users/:id/password` bestaat niet of geeft 404. Afgevinkt als dat zo is.
- Norm: ASVS 5.0.0 V6.4.6 (L3).

### AUTH-81 Accountherstel via support vraagt bewijs op hetzelfde niveau als de inrichting
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per product een herstelprocedure vast voor "ik kan niet meer inloggen" die niet leunt op wat een beller weet of op een verzoek vanaf een nieuw e-mailadres; eis een herstelcode, een nog werkende factor, of een controle via een vooraf vastgelegd kanaal, en stuur een melding naar alle bekende adressen van het account.
- Bewijs: `docs/auth.md` bevat de herstelprocedure met de toegestane bewijzen; het beheerscherm voor het wijzigen van een e-mailadres door support schrijft een auditregel en verstuurt de melding (test). Afgevinkt als document en test bestaan.
- Norm: ASVS 5.0.0 V6.4.4 (L2: bij verlies van een factor identiteitsbewijs op hetzelfde niveau als bij inschrijving), V6.4.3 (L2); NIST SP 800-63B-4 §4.2 (herstel van niet-geïdentificeerde accounts SHALL via bewaarde herstelcode, toegestuurde herstelcode of herstelcontact; meldingen bij herstel).

### AUTH-82 Beheerinterfaces: MFA, eigen pad, niet alleen een IP-filter
hoog · hard · alles (met beheer) · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet beheer- en supportfuncties achter een eigen permissie met verplichte MFA (AUTH-16) en korte sessies (AUTH-35); gebruik een IP-allowlist of VPN alleen als extra laag en nooit als enige controle.
- Bewijs: `curl -s -o /dev/null -w '%{http_code}' https://app/admin` vanaf buiten geeft een loginpagina of 401, geen 200 met inhoud; test: een beheerder zonder MFA komt er niet in. Afgevinkt als beide kloppen. Zie INFRA voor netwerkafscherming.
- Norm: ASVS 5.0.0 V8.4.2 (L3: meerdere lagen; netwerklocatie niet de enige factor), V6.3.3 (L2).
- Zie ook: AUTH-16, WP-58, INFRA-98, GIT-14, PRIV-53, INFRA-11

### AUTH-83 Scheid taken bij handelingen met grote gevolgen
middel · richtlijn · api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Eis voor handelingen met grote of onomkeerbare gevolgen (tenant verwijderen, alle data exporteren, uitbetaalgegevens wijzigen, een beheerder toevoegen) een tweede bevestiging: een tweede persoon waar die er is, anders herauthenticatie plus een wachttijd met melding en annuleermogelijkheid.
- Bewijs: Test per handeling uit de lijst: zonder tweede bevestiging of binnen de wachttijd wordt hij niet uitgevoerd en gaat er een melding uit. Afgevinkt als de lijst in `docs/auth.md` staat en elke handeling een test heeft.
- Norm: ASVS 5.0.0 V2.3.5 (L3: goedkeuring door meerdere gebruikers voor bedrijfsprocessen met hoge waarde), V7.5.3 (L3).

### AUTH-84 Auditlog van gevoelige acties
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Schrijf voor elke gevoelige actie (inloggen, factor- of rolwijziging, aanmaken of intrekken van sleutels, impersonatie, export, verwijdering, wijziging van tenant-instellingen, toegang door support) een auditregel met wie, namens wie, wat, welk object, welke tenant, wanneer en vanaf waar, in een opslag waar de applicatierol alleen kan toevoegen.
- Bewijs: `SELECT has_table_privilege('<app-rol>', 'audit_log', 'UPDATE'), has_table_privilege('<app-rol>', 'audit_log', 'DELETE')` geeft `f, f`. Test: elke actie uit de lijst levert precies één auditregel met alle velden. Afgevinkt als beide kloppen. Zie ARCH (logging) en PRIV (bewaartermijn, NEN 7513).
- Norm: ASVS 5.0.0 V16.3.1, V16.3.2, V16.3.3 (L2); OWASP Top 10:2025 A09; NEN 7513 voor zorgdata (niet nagelezen in deze sessie, zie PRIV). Wettelijke basis: zie PRIV-54, PRIV-55 (logging van inzage in zorgdossiers en de bewaartermijn daarvan).
- Zie ook: ARCH-64, ARCH-65, INFRA-89, PRIV-54, DB-91, AI-52

### AUTH-85 Offboarding: toegang van mensen en systemen direct weg
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Beëindig bij het uitschakelen of verwijderen van een account direct alle sessies, refresh tokens, API-sleutels en passkeys van dat account, en controleer per kwartaal de lijst met beheerders, serviceaccounts en sleutels op ongebruikte of onbekende vermeldingen.
- Bewijs: Test: na het uitschakelen van een gebruiker geven diens sessie, refresh token en API-sleutel 401. Kwartaalcontrole: `SELECT ... WHERE last_used_at < now() - interval '90 days'` voor sleutels en beheerders, met datum en uitkomst genoteerd in het projectdossier. Afgevinkt als de test groen is en de laatste controle minder dan een kwartaal oud is.
- Norm: ASVS 5.0.0 V7.4.2 (L1), V6.5.6 (L3: elke factor intrekbaar), V10.4.9 (L2).
