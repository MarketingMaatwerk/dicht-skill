# API B: uitvoer en foutmodel

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/api-code.md` (regelnummer in `regel-index.tsv`).

### API-09 Geef alleen de velden terug die de client nodig heeft
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw elk antwoord op uit een expliciete lijst velden (response-schema in Fastify of een eigen mapper); geef nooit een databaserij of een object van een externe API ongefilterd terug.
- Bewijs: Elke route heeft een response-schema of een mapper. Test: het antwoord bevat precies de verwachte sleutels (snapshot op sleutelnamen). `grep -rn "select()" src` in route-bestanden wordt per treffer beoordeeld.
- Norm: ASVS 5.0.0 V15.3.1 (L1); OWASP API Top 10 2023 API3.

### API-10 Zet een eigen error handler; Fastify stuurt de foutmelding letterlijk door
hoog · hard · api | mcp | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Registreer `setErrorHandler` die voor elke fout die je niet zelf bewust gooit een vaste, algemene melding teruggeeft en de echte fout alleen logt.
- Bewijs: `grep -rn "setErrorHandler" src` geeft een treffer. Test: een route die `throw new Error('geheim pad /srv/x')` doet, geeft een antwoord waar die tekst niet in staat.
- Norm: ASVS 5.0.0 V16.5.1 (L2); OWASP API Top 10 2023 API8.
- Zie ook: WEB-62, API-11, API-79, WP-40, ARCH-72

### API-11 Eén foutformaat met stabiele codes
laag · richtlijn · api | mcp · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Geef fouten terug als `application/problem+json` (RFC 9457) met `type`, `title`, `status` en een eigen stabiele foutcode; zet er geen stack, query, bestandspad of interne id in.
- Bewijs: Een contracttest loopt alle foutpaden af en controleert het schema van het foutantwoord en de afwezigheid van `stack`, `sql`, `/home/`, `node_modules`.
- Norm: ASVS 5.0.0 V16.5.1 (L2); RFC 9457.
- Zie ook: WEB-62, API-10, API-79, WP-40, ARCH-72

### API-12 Faal dicht
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een fout in validatie, autorisatie, handtekeningcontrole, de controle van een limiet of quotum of een externe controle altijd eindigen in weigeren; schrijf geen `catch` die daarna gewoon doorgaat. Aanvulling uit WEB-63: Geldt ook voor anti-spam en betaalstatus.
- Bewijs: Test per controle met een mock die gooit: de actie erna gebeurt niet. Review: elke `catch` zonder `throw` of `return` rond een controle is een bevinding.
    Ook (uit WEB-63): Een test per controle waarin de afhankelijkheid een fout gooit of een time-out geeft; de aanvraag wordt geweigerd. `grep -rnE "catch *(\([^)]*\))? *\{ *(return true|ok *= *true|next\(\))" src/` is leeg. Afgevinkt met test en grep.
- Norm: ASVS 5.0.0 V16.5.3 (L2), V16.5.2 (L2). OWASP Top 10 2025 A10 (CWE-636), uit het samengevoegde ARCH-16.
- Dekt ook: WEB-63

### API-13 Laat het proces stoppen bij een onafgehandelde fout
hoog · hard · api | app | mcp · tegenlezer: scherpen (04-10-2026)
- Regel: Onderdruk `unhandledRejection` en `uncaughtException` niet; log de fout in een laatste handler, sluit af en laat systemd of Docker het proces herstarten.
- Bewijs: `grep -rn "unhandledRejection\|uncaughtException" src` toont alleen een handler die logt en `process.exit(1)` aanroept. De service-unit heeft `Restart=on-failure` of de container `restart: unless-stopped` (zie INFRA).
- Norm: ASVS 5.0.0 V16.5.4 (L3). Let op: V16.5.4 eist de laatste handler ook om te voorkomen dat een fout het hele proces omver haalt; Node noemt doordraaien na `uncaughtException` onveilig, dus hier vult de herstart door systemd of Docker dat doel in.

### API-14 → WEB-09
Samengevoegd: "Zet op elk antwoord het juiste Content-Type met charset" is gedekt door WEB-09. Gebruik die regel.

### API-15 → WEB-52
Samengevoegd: "Laat antwoorden met gevoelige gegevens niet cachen" is gedekt door WEB-52. Gebruik die regel.

### API-16 → WEB-55
Samengevoegd: "Geen geheimen of persoonsgegevens in de URL" is gedekt door WEB-55. Gebruik die regel.
