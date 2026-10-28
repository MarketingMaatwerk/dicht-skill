# WP N: WooCommerce

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-81 Geef WooCommerce REST-sleutels het minste recht en gebruik ze alleen over HTTPS
hoog · hard · klantproject | api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak per koppeling een eigen REST-sleutel op een eigen gebruiker, met het recht "lezen" tenzij schrijven nodig is, stuur de sleutel als Basic-authenticatie in de header over HTTPS en nooit als `consumer_key` en `consumer_secret` in de URL, en trek de sleutel in zodra de koppeling stopt.
- Bewijs: In WooCommerce > Instellingen > Geavanceerd > REST API staat per sleutel een beschrijving, een gebruiker en het recht; geen sleutel "lezen/schrijven" zonder notitie. `grep -rn "consumer_secret=" ` in eigen code en in de configuratie van de koppeling is leeg. Voor een eigen app of MCP-server die de winkel aanroept: de sleutel staat in de geheimenopslag (API-65). Afgevinkt met de lijst en de grep.
- Norm: ASVS 5.0.0 V14.2.1 (L1), V13.2.2 (L2), V8.2.1 (L1).
- Zie ook: AUTH-53, AUTH-54, AI-37, GIT-35, AUTH-55, AI-35

### WP-82 Controleer de handtekening van een WooCommerce-webhook over de ruwe body
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel bij elke WooCommerce-webhook een geheim in van minstens 128 bits, bereken bij ontvangst `base64( HMAC-SHA256( ruwe body, geheim ) )`, vergelijk dat in constante tijd met de header `X-WC-Webhook-Signature`, en verwerk dubbele en oude afleveringen idempotent.
- Bewijs: Drie tests op de ontvanger: een geldige aflevering wordt verwerkt; dezelfde body met één gewijzigd teken geeft 401; dezelfde geldige aflevering twee keer leidt tot één verwerking. Let op: WooCommerce zet een webhook uit na meer dan vijf opeenvolgende mislukte afleveringen (alles behalve 2xx, 301 en 302 telt als mislukt), dus bewaak of de webhook nog actief is. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V13.2.1 (L2), V11.5.1 (L2).
- Zie ook: API-36, API-37, API-38, API-44, WP-83, BIZ-24, AUTH-58, AUTH-59, MSG-35, MSG-36, MSG-37, MSG-39, MSG-43, MSG-44, API-40

### WP-83 Laat de betaalstatus van een bestelling alleen van de betaalprovider komen
kritiek · hard · klantproject | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet een bestelling in eigen WooCommerce-code alleen op betaald op basis van de status die je bij de betaalprovider ophaalt, nooit op basis van de terugkeer-URL, een parameter in de aanvraag of een eigen AJAX-actie, en reken het bedrag altijd op de server uit.
- Bewijs: `grep -rnE "payment_complete\(|update_status\( *'(processing|completed)'" .` in eigen code: elke aanroep volgt op een status die bij de provider is opgehaald; een test die de terugkeer-URL aanroept voor een onbetaalde bestelling laat de status ongemoeid; een test met een gemanipuleerd bedrag in de aanvraag levert het serverbedrag op. Afgevinkt met grep en tests.
- Norm: ASVS 5.0.0 V2.3.1 (L1), V2.2.2 (L1), V8.3.1 (L1). Niveau L3 voor betaling (besluit 6).
- Zie ook: API-36, API-37, API-38, API-44, WP-82, BIZ-24
