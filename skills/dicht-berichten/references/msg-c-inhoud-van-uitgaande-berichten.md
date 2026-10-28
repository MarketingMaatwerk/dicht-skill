# MSG C: Inhoud van uitgaande berichten

Compacte regels van `dicht-berichten`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/email-berichten-bots.md` (regelnummer in `regel-index.tsv`).

### MSG-16 Geef invoer nooit door als afzender aan sendmail of mail()
kritiek · hard · website | wp-plugin | wp-thema | api | app | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Zet het envelopadres en de afzender van uitgaande mail vast in de configuratie, verstuur via SMTP (INFRA-64) en geef geen waarde uit een verzoek door aan de vijfde parameter van PHP `mail()`, aan `Sender` van PHPMailer of aan een `sendmail`-transport.
- Bewijs: `grep -rnE "mail\(.*,.*,.*,.*,|->Sender *=|sendmail: *true|isMail\(|isSendmail\(" <code>` toont geen waarde uit een verzoek en geen lokaal transport; een testinzending met `a@b.nl -OQueueDirectory=/tmp -X/tmp/x.php` als adres wordt geweigerd door de adresvalidatie. Afgevinkt met grep en de testuitvoer.
- Norm: ASVS 5.0.0 V1.2.5 (L1, OS-commando-injectie), V1.3.11 (L2).
- Zie ook: MSG-01, INFRA-64, MSG-12, MSG-02, WEB-68

### MSG-17 Codeer elke variabele in een HTML-mailsjabloon
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Codeer elke waarde die van een gebruiker of een externe bron komt voor HTML voordat hij in de HTML-versie van een mail belandt, begrens de lengte ervan, en zet in de platte-tekstversie geen waarde die op een link lijkt.
- Bewijs: Een unit-test per sjabloon met de naam `<a href="https://x.example">klik</a> https://x.example`: de HTML-versie bevat `&lt;a` en geen `<a href="https://x.example"`; de naam is afgekapt op de vastgelegde lengte; velden die in een aanhef komen weigeren `://` en `www.`. Afgevinkt met de testuitvoer. De ontvanger en de vrije tekst zelf: WEB-69.
- Norm: ASVS 5.0.0 V1.2.1 (L1, uitvoercodering passend bij de context).
- Zie ook: WEB-01, WP-01, WP-02, WP-03, WEB-06, INV-25, INV-35

### MSG-18 Beslis op het adres dat de parser teruggeeft, met één parser voor de hele keten
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Ontleed een e-mailadres één keer met de bibliotheek die ook verstuurt, vergelijk en bewaar alleen het ontlede `local@domein` in kleine letters, weiger een invoer die meer dan één adres, een weergavenaam, commentaar tussen haakjes of een aanhalingsteken bevat, en doe een domeincontrole nooit met een tekstvergelijking op de ruwe invoer.
- Bewijs: Een unit-test met `a@toegestaan.nl(x)@kwaad.example`, `"a@toegestaan.nl"@kwaad.example`, `a@toegestaan.nl, b@kwaad.example` en `Naam <a@kwaad.example>`: alle vier worden geweigerd op elk invoerveld voor een adres. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V2.1.1 (L1, validatieregels voor e-mailadressen vastgelegd), V1.3.11 (L2).
- Zie ook: INV-64, WEB-69, AUTH-47

### MSG-19 Laat links in mail alleen naar het eigen domein wijzen, zonder open doorstuurder
middel · hard · api | app | klantproject | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw elke link in een mail uit de basis-URL in de configuratie (WEB-42), laat hem wijzen naar het domein dat de ontvanger van je kent, en gebruik voor klikmeting geen doorstuuradres dat een willekeurig doel uit de querystring volgt.
- Bewijs: `grep -rnoE "https?://[^\"' >]+" <sjablonen>` toont alleen eigen domeinen of variabelen die uit de configuratie komen; `curl -sI "https://<klikdomein>/r?u=https://example.org"` geeft geen 30x naar example.org (het doel komt uit een tabel of het adres is ondertekend). Afgevinkt met grep en de uitvoer. Toestemming voor klik- en openmeting: PRIV-41.
- Norm: ASVS 5.0.0 V3.7.3 (L3, melding bij doorsturen naar buiten) naar de geest; zie WEB voor open redirects.
- Zie ook: WEB-42, MSG-20

### MSG-20 Vraag in een mail nooit om een wachtwoord of betaalgegevens, en zeg dat ook
middel · richtlijn · api | app | klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Vraag in geen enkel bericht om een wachtwoord, een code of nieuwe betaalgegevens, wijzig bankgegevens nooit per mail, en zet in de vaste voettekst van transactiemail wat de dienst nooit per mail vraagt.
- Bewijs: `grep -rniE "wachtwoord|password|iban|rekeningnummer" <sjablonen>` is per treffer verklaard (alleen "stel een wachtwoord in via deze link", nooit "stuur"); de voettekst van transactiemail bevat de vaste zin. Afgevinkt met grep en het sjabloon.
- Norm: geen ASVS-eis.
- Zie ook: WEB-42, MSG-19

### MSG-21 Geef bijlagen een veilige, gecodeerde bestandsnaam
laag · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bepaal de bestandsnaam van een bijlage in uitgaande mail zelf (vaste naam plus nummer), laat de bibliotheek hem coderen, en neem geen naam over uit een upload of een klantveld zonder hem terug te brengen tot letters, cijfers, punt en streepje.
- Bewijs: Een unit-test met een bedrijfsnaam vol aanhalingstekens, regeleinden en `../`: de bijlage heet `factuur-<nummer>.pdf`. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V5.4.2 (L2).
