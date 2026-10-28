# MSG E: WhatsApp Business

Compacte regels van `dicht-berichten`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/email-berichten-bots.md` (regelnummer in `regel-index.tsv`).

### MSG-35 Beantwoord het verificatieverzoek alleen bij het juiste token
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: META
- Regel: Laat de GET op het webhookadres de waarde van `hub.challenge` alleen teruggeven als `hub.mode` gelijk is aan `subscribe` en `hub.verify_token` in constante tijd gelijk is aan het eigen geheim uit de configuratie; geef anders 403 en geef `hub.challenge` terug als platte tekst.
- Bewijs: `curl -s -o /dev/null -w "%{http_code}" "https://<host>/webhook?hub.mode=subscribe&hub.verify_token=fout&hub.challenge=1"` geeft 403; met het juiste token geeft het 200, de waarde 1 en `Content-Type: text/plain`. Afgevinkt met de uitvoer. Vastgelegd risico (besluit van Marketing Maatwerk, 04-10-2026, OPEN-VRAGEN A32): de WhatsApp-spiegel leest via een gekoppeld apparaat met een niet-officiële client en valt buiten deze regels, die voor de officiële Cloud API gelden; hij blijft zoals hij is en staat als risico in het uitzonderingenregister (ARCH-30). Versturen via de spiegel wordt niet gebouwd.
- Norm: ASVS 5.0.0 V1.2.1 (L1) voor het teruggeven; zie AUTH-57.
- Zie ook: AUTH-58, AUTH-59, MSG-36, MSG-37, MSG-39, MSG-43, MSG-44, WP-82, API-40

### MSG-36 Controleer X-Hub-Signature-256 over de ruwe body met het app-geheim
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: META
- Regel: Bereken bij elke POST op het webhookadres een HMAC-SHA256 over de ruwe bytes van de body met het app-geheim, vergelijk die in constante tijd met de waarde na `sha256=` in `X-Hub-Signature-256`, en verwerk niets als de kop ontbreekt of niet klopt.
- Bewijs: Een test met drie verzoeken (geldige handtekening, geen kop, gewijzigde body): alleen het eerste wordt verwerkt, de andere geven 401 of 403; de test bevat een body met tekens buiten ASCII. De algemene regel en de ruwe body: AUTH-58. Afgevinkt met de testuitvoer.
- Norm: zie AUTH-58 voor de ASVS-eis.
- Zie ook: AUTH-58, AUTH-59, MSG-35, MSG-37, MSG-39, MSG-43, MSG-44, WP-82, API-40

### MSG-37 Ontdubbel op het bericht-ID; Meta biedt een melding tot 36 uur opnieuw aan
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: META
- Regel: Antwoord direct met 200, leg het bericht-ID vast met een unieke index voordat je iets doet, en verwerk een ID dat al bestaat niet opnieuw.
- Bewijs: Een test die dezelfde melding twee keer instuurt: er ontstaat één rij en één uitgaande actie. De handler antwoordt binnen een seconde (meting) en doet het werk daarna. Zie AUTH-59 en DB-68. Afgevinkt met de testuitvoer.
- Norm: zie AUTH-59 en DB-68.
- Zie ook: AUTH-58, AUTH-59, MSG-35, MSG-36, MSG-39, MSG-43, MSG-44, WP-82, API-40

### MSG-38 Dwing het 24-uursvenster af in code
hoog · hard · api | app | mcp | klantproject · tegenlezer: scherpen (04-10-2026) · bron niet gelezen: META
- Regel: Leg per gesprek het tijdstip van het laatste inkomende bericht vast (alleen uit een melding met geldige handtekening), laat de verzendfunctie een vrij bericht weigeren als dat langer dan 24 uur geleden is, en stuur daarbuiten alleen een vooraf goedgekeurd sjabloon.
- Bewijs: Een unit-test op de verzendfunctie: laatste inkomende bericht 23 uur geleden geeft verzenden, 25 uur geleden geeft een weigering met de reden `venster_dicht` zonder aanroep naar buiten; een sjabloonbericht gaat in beide gevallen door. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V2.3.2 (L2, grenzen van bedrijfslogica) naar de geest.
