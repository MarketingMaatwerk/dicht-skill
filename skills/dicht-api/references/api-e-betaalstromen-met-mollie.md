# API E: betaalstromen met Mollie

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/api-code.md` (regelnummer in `regel-index.tsv`).

### API-36 Behandel de webhook als signaal en haal de status op bij Mollie
kritiek · hard · api | wp-plugin | klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik uit de klassieke Mollie-webhook alleen het `id`, haal daarmee de betaling op via de Mollie-API met je eigen sleutel, en baseer elke beslissing op dat antwoord; lever nooit op basis van de terugkeer van de klant op de `redirectUrl` of op basis van velden in het verzoek.
- Bewijs: Test: een POST naar de webhook met het id van een betaling met status `open` leidt niet tot levering. Codecontrole: in de webhook-handler komt de status alleen uit het antwoord van `payments.get`. De bedankpagina toont alleen de status en start geen levering, of doet dezelfde navraag via dezelfde idempotente functie.
    Ook (uit AUTH-60): Tests met een nagebootste Mollie-API: een webhook met een onbekend `id` verandert niets; een betaling met een ander bedrag of een andere valuta dan de bestelling verandert niets; de bestelling wordt gevonden via het Mollie-id dat je zelf bij het aanmaken hebt opgeslagen, niet via `metadata` uit het antwoord (API-37); de route antwoordt binnen 15 seconden met 200. Afgevinkt als de tests groen zijn.
- Norm: OWASP API Top 10 2023 API10; ASVS 5.0.0 V2.3.1 (L1).
- Dekt ook: AUTH-60
- Zie ook: API-37, API-38, API-44, WP-83, WP-82, BIZ-24

### API-37 Vergelijk bedrag, valuta en bestelling voordat je levert
kritiek · hard · api | wp-plugin | klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Zoek de betaling op in je eigen database aan de hand van het Mollie-id dat je zelf bij het aanmaken hebt opgeslagen, en controleer dat status, bedrag en valuta van het Mollie-antwoord overeenkomen met wat jouw bestelling verwacht voordat je levert.
- Bewijs: De handler zoekt op `molliePaymentId` in de eigen tabel (geen bestel-id uit het verzoek of alleen uit `metadata`). Unit-test: een betaling met een ander bedrag of een andere valuta dan de bestelling wordt niet geleverd en geeft een alarm.
- Norm: ASVS 5.0.0 V2.2.3 (L2); OWASP API Top 10 2023 API10.
- Zie ook: API-36, API-38, API-44, WP-83, WP-82, BIZ-24, BIZ-13, BIZ-14, BIZ-17, BIZ-19, BIZ-33, API-35, API-29

### API-38 Lever precies één keer, hoe vaak de webhook ook komt
kritiek · hard · api | wp-plugin | klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak de overgang naar "betaald" atomair (API-30) en hang de levering aan de ene winnaar van die overgang; elke volgende aanroep voor dezelfde betaling doet niets.
- Bewijs: Test met 20 gelijktijdige webhook-aanroepen voor één betaling: precies één leveringstaak, één mail, één vergoeding. Een unieke index op (betaling, taaksoort) als vangnet (API-31).
- Norm: ASVS 5.0.0 V2.3.4 (L2), V15.4.2 (L3).
- Zie ook: API-30, API-31, API-33, DB-68, ARCH-18, AUTH-59, API-36, API-37, API-44, WP-83, WP-82, BIZ-24

### API-39 Antwoord 200 pas als de verwerking duurzaam vastligt
hoog · hard · api | wp-plugin | klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef de Mollie-webhook status 200 nadat de statuswijziging en de leveringstaak in de database staan; geef bij een eigen fout (database weg, Mollie-API onbereikbaar) een 5xx zodat Mollie opnieuw probeert; geef bij een onbekend id wel 200.
- Bewijs: Test: laat de database-aanroep in de handler falen en controleer dat het antwoord 5xx is. Test: een onbekend id geeft 200 zonder Mollie-aanroep. Zie ook API-43 voor het vangnet.
- Norm: ASVS 5.0.0 V16.5.3 (L2).

### API-40 Antwoord de webhook binnen 15 seconden en doe zwaar werk daarna
middel · hard · api | wp-plugin | klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Beperk de webhook-handler tot navragen, status vastleggen en een taak aanmaken; voer registratie, hosting aanmaken, mail en facturatie uit in een worker.
- Bewijs: De handler bevat geen aanroepen naar andere diensten dan de Mollie-API en de eigen database. Meting: de p99 van de webhook-route ligt ruim onder 15 seconden (log van `responseTime`).
- Norm: ASVS 5.0.0 V15.1.3 (L2).
- Zie ook: AUTH-58, AUTH-59, MSG-35, MSG-36, MSG-37, MSG-39, MSG-43, MSG-44, WP-82

### API-41 Stuur een Idempotency-Key mee bij elke POST naar Mollie
hoog · hard · api | wp-plugin | klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Genereer per zakelijke actie (deze betaling voor deze bestelling, deze terugbetaling) één UUID v4, sla hem op bij de bestelling, en stuur hem als `Idempotency-Key` mee bij het aanmaken van een betaling, terugbetaling, klant of abonnement; gebruik bij een herhaling dezelfde sleutel.
- Bewijs: `grep -rn "idempotencyKey\|Idempotency-Key" src` toont de sleutel bij elke muterende Mollie-aanroep. Let op de beperking: Mollie bewaart sleutels 1 uur, dus een herhaling na een uur is weer een nieuw verzoek; controleer na een uur eerst of de betaling al bestaat. Dezelfde sleutel met andere parameters geeft 400.
- Norm: ASVS 5.0.0 V2.3.3 (L2).
- Zie ook: BIZ-40, SCR-45, API-49, ARCH-18

### API-42 Verwerk ook wat er na "betaald" gebeurt
hoog · hard · api | wp-plugin | klantproject | app · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Haal bij elke webhook de betaling opnieuw op en verwerk terugbetalingen en chargebacks: leg ze vast, draai de levering of de vergoeding terug volgens de bedrijfsregel en maak een taak voor Marketing Maatwerk.
- Bewijs: Test met een nagebootst Mollie-antwoord waarin een chargeback of terugbetaling staat: er ontstaat een vastlegging en een taak. De vroege `return` bij "al betaald" staat pas na deze controle.
- Norm: ASVS 5.0.0 V2.3.1 (L1).
- Zie ook: BIZ-15, BIZ-16, BIZ-22, BIZ-36, BIZ-47

### API-43 Stem dagelijks af wat de webhook kan hebben gemist
hoog · hard · api | wp-plugin | klantproject | app · tegenlezer: scherpen (04-10-2026)
- Regel: Laat een dagelijkse taak alle eigen betalingen in een niet-definitieve status (`open`, `pending`, `authorized`) die ouder zijn dan de vervaltermijn opnieuw ophalen bij Mollie en door dezelfde verwerkingsfunctie halen. Hard voor elk project met Mollie (besluit van Marketing Maatwerk, 04-10-2026).
- Bewijs: De taak bestaat (cron of worker), heeft een droge modus, logt hoeveel betalingen hij alsnog verwerkte en alarmeert bij meer dan nul. De definitieve statussen volgens Mollie zijn `paid`, `expired`, `failed` en `canceled`; `banktransfer` verloopt standaard pas na 12 dagen, plus één of twee dagen als de twaalfde dag in het weekend valt.
- Norm: ASVS 5.0.0 V16.5.2 (L2).
- Zie ook: BIZ-48, BIZ-49, BIZ-46, BIZ-51, BIZ-41

### API-44 Controleer de handtekening bij de nieuwe Mollie-webhooks
hoog · hard · api | wp-plugin | app · tegenlezer: scherpen (04-10-2026)
- Regel: Controleer bij next-gen webhooks van Mollie de header `X-Mollie-Signature` (HMAC-SHA256 over de ongewijzigde body met het signing secret) in constante tijd voordat je de payload gebruikt, bij voorkeur met de officiële Mollie-bibliotheek; accepteer het bericht als één van de meegestuurde handtekeningen klopt, want na het wisselen van het secret stuurt Mollie 24 uur lang twee `X-Mollie-Signature`-headers.
- Bewijs: De route bewaart de ruwe body (in Fastify via een eigen content-type-parser met `parseAs: 'buffer'`). Test: een gewijzigde body of een ontbrekende header geeft 401; een bericht met twee handtekeningen waarvan één klopt wordt geaccepteerd. De handtekening bevat geen tijdstempel, dus herhaling vang je af met het gebeurtenis-id (API-46). Zie API-46 en API-62.
- Norm: ASVS 5.0.0 V4.1.5 (L3); OWASP API Top 10 2023 API10.
- Zie ook: API-36, API-37, API-38, WP-83, WP-82, BIZ-24

### API-45 Gebruik geen IP-lijst als controle op Mollie-webhooks
laag · richtlijn · api | wp-plugin | klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw de echtheidscontrole op navragen bij de API (API-36) of op de handtekening (API-44), niet op een lijst met IP-adressen van Mollie.
- Bewijs: Geen allowlist voor Mollie in nginx of de firewall, of alleen als extra laag naast API-36.
- Norm: geen ASVS-eis; leveranciersrichtlijn.

### API-82 Productie betaalt met de live-sleutel, en de eerste echte betaling bewijst het
hoog · hard · api | wp-plugin | klantproject | app · tegenlezer: niet tegengelezen
- Regel: Zet bij de livegang van een betaalkoppeling de productie op de Live API key van Mollie (of zet de testmodus van de betaalplugin uit), en controleer met de eerste echte betaling na de livegang dat die in live-modus binnenkomt. In productie staat nooit een Test API key of een aangezette testmodus; buiten productie juist wel (INFRA-74).
- Bewijs: (1) Bij de livegang doet de bouwer zelf één echte betaling met een klein bedrag (bijvoorbeeld via iDEAL) en betaalt die terug; in het Mollie-dashboard staat die betaling in live-modus (betaal-ID en datum, of een schermafbeelding). (2) De sha256 van de sleutel in productie (zonder regeleinde) is gelijk aan die van de Live API key uit het Mollie-dashboard, of bij WooCommerce staat de testmodus van de Mollie-plugin uit (schermafbeelding van de instelling). Afgevinkt met beide.
- Norm: geen ASVS-eis; leveranciersrichtlijn.
