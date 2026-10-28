# AUTH I: Autorisatie per functie, object en veld

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/auth.md` (regelnummer in `regel-index.tsv`).

### AUTH-62 Weiger standaard en dwing af op de server, op één plek
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke route standaard dicht zijn tenzij er een expliciete toestemmingsregel bij staat, dwing autorisatie af in servercode via één gedeeld mechanisme (hook, middleware plus datalaag), en vertrouw nooit op verborgen knoppen of controles in de frontend.
- Bewijs: De server weigert te starten of een test faalt als een route geen expliciete `permission` of `public` heeft. Een test loopt alle geregistreerde routes af zonder sessie en verwacht 401 of 403, behalve op de lijst met publieke routes. Afgevinkt als die test in CI staat.
- Norm: ASVS 5.0.0 V8.2.1, V8.3.1 (L1); OWASP Top 10:2025 A01; OWASP API Security Top 10 2023 API5.
- Zie ook: WP-10, WP-09, WP-11, WP-12, WP-13, AUTH-64

### AUTH-63 Controleer bij elk object of het van deze gebruiker en deze tenant is
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem in elke query die een id uit de aanvraag gebruikt (pad, query, body, bestandsnaam) de eigenaar of tenant uit de sessie mee in de voorwaarde, en geef bij geen treffer 404.
- Bewijs: Per route met een id-parameter een integratietest: gebruiker B vraagt het object van gebruiker A op (lezen, wijzigen, verwijderen) en krijgt 404 of 403, en het object is ongewijzigd. Afgevinkt als elke route in de lijst een test heeft (zie AUTH-66).
- Norm: ASVS 5.0.0 V8.2.2 (L1); OWASP API Security Top 10 2023 API1; OWASP Top 10:2025 A01.

### AUTH-64 Bescherm elke functie, ook via een andere methode of een ander pad
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per functie vast welke rol of permissie hem mag aanroepen en dwing dat af op elke HTTP-methode en elke route die bij die functie uitkomt (REST, AJAX-handler, RPC, MCP-tool, CLI-brug); registreer alleen de methodes die je ondersteunt.
- Bewijs: De routetest uit AUTH-62 uitgebreid met rollen: voor elke route en methode wordt per rol de verwachte uitkomst (toegestaan of 403) uit een matrixbestand gelezen en getest. Afgevinkt als de matrix alle routes dekt.
- Norm: ASVS 5.0.0 V8.2.1 (L1), V8.1.1 (L1: regels gedocumenteerd), V4.1.4 (L3: alleen ondersteunde methodes); OWASP API Security Top 10 2023 API5.
- Zie ook: WP-10, WP-09, WP-11, WP-12, WP-13, AUTH-62, INV-62

### AUTH-65 Laat een gebruiker geen velden zetten die zijn rechten bepalen
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Accepteer bij aanmaken en wijzigen alleen een expliciete lijst velden per rol (schema met `strict`), en nooit `role`, `tenant_id`, `owner_id`, `is_admin`, `email_verified` of prijs- en statusvelden uit de body van een gewone gebruiker.
- Bewijs: Test per schrijfroute: een body met `role`, `tenantId` en `isAdmin` geeft 400 (strikt schema) of negeert de velden, en de database is ongewijzigd. Afgevinkt als de test groen is. Zie API voor schema-validatie in het algemeen.
- Norm: ASVS 5.0.0 V8.2.3 (L2), V8.1.2 (L2); OWASP API Security Top 10 2023 API3.
- Zie ook: API-02, INV-47, INV-46, WP-32, INV-13

### AUTH-66 Autorisatietests met twee gebruikers en twee tenants zijn een CI-gate
hoog · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Onderhoud een testset die voor elke route met gegevens ten minste dit probeert: niet ingelogd, ingelogd als andere gebruiker in dezelfde tenant, ingelogd in een andere tenant, en ingelogd met een te lage rol; laat de build falen als een nieuwe route niet in de set zit.
- Bewijs: CI-uitvoer toont de autorisatiematrix-test als verplichte stap; een test vergelijkt de lijst geregistreerde routes met de matrix en faalt bij een ontbrekende route. Afgevinkt als beide in CI staan.
- Norm: ASVS 5.0.0 V8.4.1 (L2); OWASP API Security Top 10 2023 API1.
- Zie ook: DB-22, AUTH-77, AI-53, ARCH-40

### AUTH-67 Vertrouw niet alleen op middleware, proxy of route-volgorde
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Herhaal de autorisatiecontrole op de plek waar de data wordt gelezen of geschreven (service- of datalaag, en RLS in de database), ook als een middleware, nginx-regel of framework-laag hem al doet.
- Bewijs: Codecheck van de datalaag: functies die tenant- of gebruikersdata lezen krijgen de context (`ctx.userId`, `ctx.tenantId`) als verplichte parameter. Test: de servicefunctie rechtstreeks aanroepen zonder context faalt bij het compileren (TypeScript) of geeft een fout. Afgevinkt als dat zo is.
- Norm: ASVS 5.0.0 V8.3.1 (L1); OWASP Top 10:2025 A01.

### AUTH-68 Onvoorspelbare id's zijn een extra laag, geen autorisatie
middel · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor naar buiten zichtbare id's willekeurige waarden (UUID v4 of een willekeurige string) in plaats van oplopende nummers, maar behandel een id nooit als geheim: de controle uit AUTH-63 blijft verplicht.
- Bewijs: Codecheck: geen route geeft data op basis van alleen een id zonder sessie, behalve bewust gedeelde links die voldoen aan AUTH-25 (willekeurig token van 128 bits, vervaldatum, intrekbaar). Afgevinkt als de lijst met zulke links gedocumenteerd is.
- Norm: ASVS 5.0.0 V8.2.2 (L1), V11.5.1 (L2: "UUIDs do not respect this condition" voor onraadbare geheimen).

### AUTH-69 Bestanden, exports en back-ups vallen onder dezelfde autorisatie
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Serveer uploads, exports, facturen en back-ups alleen via een route die de sessie en het eigendom controleert (of via een kortlevende ondertekende URL), en bewaar ze buiten de webroot.
- Bewijs: `curl -s -o /dev/null -w '%{http_code}' https://site/<pad-naar-upload-of-export>` zonder cookie geeft 401, 403 of 404 voor elk type bestand; een test vraagt een bestand van tenant A op met een sessie van tenant B. Afgevinkt als beide kloppen. Zie WEB (uploads) en WP (back-upmappen).
- Norm: ASVS 5.0.0 V8.2.2 (L1); OWASP Top 10:2025 A01.
- Zie ook: DB-23, AI-68, AI-71

### AUTH-70 Log geweigerde toegang en geef geen details prijs
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Log elke geweigerde autorisatie met gebruiker, tenant, route en object-id, geef de aanvrager alleen een generieke 403 of 404, en sla alarm bij een reeks weigeringen van één account.
- Bewijs: Test: een geweigerde aanvraag schrijft een logregel `event=authz_fail` met de vier velden en de respons bevat geen reden of bestaan van het object. Afgevinkt als de test groen is. Zie ARCH voor alarmering.
- Norm: ASVS 5.0.0 V16.3.2 (L2; L3: alle autorisatiebesluiten en toegang tot gevoelige data), V16.3.3 (L2); OWASP Top 10:2025 A09.
- Zie ook: ARCH-59, AUTH-14, ARCH-58, ARCH-63

### AUTH-71 → WP-10, WP-09, WP-13, WP-12
Samengevoegd: "WordPress: capability-controle op elke handler; een nonce is geen autorisatie" is gedekt door WP-10, WP-09, WP-13, WP-12. Gebruik die regel.
