# MSG F: Discord en Slack

Compacte regels van `dicht-berichten`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/email-berichten-bots.md` (regelnummer in `regel-index.tsv`).

### MSG-39 Controleer bij Discord-interacties de Ed25519-handtekening en antwoord anders met 401
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer bij elk verzoek op het interactie-eindpunt de handtekening uit `X-Signature-Ed25519` over `X-Signature-Timestamp` plus de ruwe body met de publieke sleutel van de app, en antwoord met 401 als hij niet klopt.
- Bewijs: `curl -s -o /dev/null -w "%{http_code}" -X POST -H "X-Signature-Ed25519: 00" -H "X-Signature-Timestamp: 1" -d '{"type":1}' https://<host>/<interactiepad>` geeft 401; een test met een geldige handtekening over een gewijzigde body geeft 401. Afgevinkt met de uitvoer.
- Norm: zie AUTH-58.
- Zie ook: AUTH-58, AUTH-59, MSG-35, MSG-36, MSG-37, MSG-43, MSG-44, WP-82, API-40

### MSG-40 Zet bij elk bericht met inhoud van buiten uit wie er genoemd mag worden
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur met elk Discord-bericht dat tekst van buiten bevat (onderwerp van een mail, naam van een klant, logregel) `allowed_mentions` met een lege `parse`-lijst mee, en codeer in Slack de tekens `&`, `<` en `>` in zulke tekst.
- Bewijs: Een test die een bericht met `@everyone`, `<@&123>` en `<!channel>` door de meldfunctie stuurt: de Discord-aanroep bevat `"allowed_mentions":{"parse":[]}` en de Slack-tekst bevat `&lt;!channel&gt;`. `grep -rn "allowed_mentions" <meldcode>` toont het veld op elke plek waar een bericht wordt gepost. Afgevinkt met de testuitvoer en grep.
- Norm: ASVS 5.0.0 V1.2.1 (L1, codering passend bij de context) naar de geest.

### MSG-41 Behandel een webhookadres en een bot-token als geheim
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewaar het adres van een inkomende webhook (Discord, Slack) en elk bot-token alleen in het geheimenbestand van de dienst, nooit in code, logs, foutmeldingen of een commit, geef elke dienst zijn eigen webhook of token, en trek het in bij een vermoeden van lekken.
- Bewijs: `gitleaks detect` of `grep -rnE "discord(app)?\.com/api/webhooks/|hooks\.slack\.com/services/|xox[baprs]-" <repo en logs>` is leeg; het geheimenbestand heeft rechten 600; een overzicht noemt per token welke diensten het lezen. Afgevinkt met de uitvoer en het overzicht. Zie GIT-32, INFRA-07.
- Norm: ASVS 5.0.0 V13.3.1 (L2).
- Zie ook: INFRA-76, SCR-19, SCR-20, SCR-05, SCR-13, SCR-16, SCR-50, AI-28

### MSG-42 Volg 429 en Retry-After, en blijf onder de grens voor ongeldige verzoeken
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke aanroep naar Discord of Slack bij een 429 wachten zolang `Retry-After` (of `retry_after`) aangeeft, zet geen vaste limieten in de code, stop met aanroepen zodra een token 401 of 403 geeft, en geef een meldfunctie een eigen plafond per tijdvak.
- Bewijs: Een test met een nagebootste 429 met `Retry-After: 2`: de volgende aanroep komt niet eerder dan na 2 seconden; een nagebootste 401 leidt tot stoppen en één foutregel, niet tot herhalen; de meldfunctie heeft een plafond (bijvoorbeeld één bericht per taak per 10 minuten) dat in een test wordt geraakt. Afgevinkt met de testuitvoer. Zie API-49.
- Norm: zie API-49 (begrensd herhalen).
- Zie ook: API-48, API-49, ARCH-13, ARCH-14, AI-76, DB-65, API-19, SCR-21, SCR-25, SCR-26, SCR-43

### MSG-43 Controleer bij Slack de handtekening en weiger een verzoek ouder dan vijf minuten
kritiek · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bereken bij elk verzoek van Slack `v0=` plus de HMAC-SHA256 van `v0:<tijdstempel>:<ruwe body>` met het signing secret, vergelijk in constante tijd met `X-Slack-Signature`, weiger als `X-Slack-Request-Timestamp` meer dan vijf minuten afwijkt, en gebruik het oude verificatietoken in de body niet.
- Bewijs: Een test met vier verzoeken (geldig, verkeerde handtekening, geldig maar tijdstempel van tien minuten oud, geen koppen): alleen het eerste wordt verwerkt; `grep -rn "body.token\|payload.token" <code>` is leeg. Afgevinkt met de testuitvoer en grep. Zie AUTH-58, AUTH-59.
- Norm: zie AUTH-58 en AUTH-59.
- Zie ook: AUTH-58, AUTH-59, MSG-35, MSG-36, MSG-37, MSG-39, MSG-44, WP-82, API-40

### MSG-44 Antwoord Slack binnen drie seconden en ontdubbel op event_id
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bevestig een event met een 2xx binnen drie seconden, zet het werk in een wachtrij, en leg `event_id` vast met een unieke index zodat een herhaalde aflevering niets opnieuw doet.
- Bewijs: Een test die hetzelfde event twee keer instuurt (de tweede met `x-slack-retry-num: 1`): er is één verwerking; de responstijd van de handler in de test blijft onder een seconde. Afgevinkt met de testuitvoer.
- Norm: zie DB-68, API-40.
- Zie ook: AUTH-58, AUTH-59, MSG-35, MSG-36, MSG-37, MSG-39, MSG-43, WP-82, API-40

### MSG-45 Vraag bij Discord alleen de intents die de bot nodig heeft
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef een Discord-bot alleen de gateway-intents en kanaalrechten die zijn taak vraagt; een bot die alleen meldingen plaatst, krijgt geen leesrecht op berichtinhoud en verbindt niet met de gateway.
- Bewijs: De instellingen van de app in het ontwikkelaarsportaal (schermafdruk met datum): geen bevoorrechte intents aan tenzij verklaard; de rol van de bot in de server heeft alleen "berichten versturen" in de bedoelde kanalen. Afgevinkt met de schermafdruk. Zie AI-19, AI-21.
- Norm: ASVS 5.0.0 V13.2.2 (L2, minimale rechten tussen onderdelen) naar de geest.
