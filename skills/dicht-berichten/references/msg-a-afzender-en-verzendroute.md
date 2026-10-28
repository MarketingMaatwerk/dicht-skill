# MSG A: Afzender en verzendroute

Compacte regels van `dicht-berichten`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/email-berichten-bots.md` (regelnummer in `regel-index.tsv`).

### MSG-01 Zet in From alleen een adres op een eigen domein; de inzender hoort in Reply-To
hoog · hard · website | wp-plugin | wp-thema | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik als From-adres van elke mail die de toepassing verstuurt een vast adres uit de configuratie op een domein dat je zelf ondertekent, en zet het adres van een bezoeker of klant alleen in `Reply-To`, na validatie.
- Bewijs: `grep -rnE "From:.*\\$|setFrom\\(|from:" <mailcode>` laat alleen waarden uit de configuratie zien; een testinzending met een adres op een extern domein komt aan met `dmarc=pass` in `Authentication-Results` en met het ingevulde adres in `Reply-To`. Afgevinkt met grep en de ontvangen koppen.
- Norm: geen ASVS-eis.
- Zie ook: MSG-16, INFRA-64, MSG-12, MSG-02, WEB-68

### MSG-02 Scheid transactiemail van reclame en koude mail op afzenderadres en domein
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke soort mail (transactie, nieuwsbrief, koude mail) een eigen From-adres, verstuur reclame en koude mail vanaf een eigen subdomein met een eigen DKIM-domein, en zet nooit reclame in een transactiebericht.
- Bewijs: Een tabel per verzendstroom met From-adres, DKIM-domein (`d=`) en soort; per stroom de koppen van een ontvangen bericht waarin `d=` overeenkomt met de tabel; `grep` op de transactiesjablonen toont geen aanbiedingsblok. Afgevinkt met de tabel en de koppen.
- Norm: geen ASVS-eis.
- Zie ook: MSG-01, MSG-16, INFRA-64, MSG-12, WEB-68, INFRA-63, MSG-03, MSG-07, MSG-11, MSG-13, MSG-15, INFRA-58

### MSG-03 Onderteken zonder lengtelimiet en dek de koppen die de ontvanger ziet
middel · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Onderteken met DKIM zonder de `l=`-tag en neem minstens `From`, `To`, `Subject`, `Date`, `Message-ID`, `Reply-To` en, als ze er zijn, `List-Unsubscribe` en `List-Unsubscribe-Post` op in `h=`.
- Bewijs: In een ontvangen bericht per verzendroute: `grep -i '^DKIM-Signature' -A6 bericht.eml` toont geen `l=` en een `h=` met de genoemde koppen. Afgevinkt met de koppen per route.
- Norm: geen ASVS-eis.
- Zie ook: INFRA-63, MSG-02, MSG-07, MSG-11, MSG-13, MSG-15, INFRA-58

### MSG-04 Bouw elk bericht met een bibliotheek, met één Message-ID, één Date en één From
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel berichten samen met de mailbibliotheek van de taal (nooit met tekstaaneenschakeling), geef elk bericht een unieke `Message-ID` op het eigen domein en een `Date`, en laat de bibliotheek weigeren als een kop een regeleinde bevat.
- Bewijs: Een unit-test die een onderwerp en een naam met `\r\nBcc: x@<eigen-domein>` aan de bouwfunctie geeft en een fout of een bericht zonder extra kop verwacht; in een ontvangen bericht `grep -ciE '^(From|To|Subject|Date|Message-ID):'` geeft per kop 1. In Python: `grep -rn "verify_generated_headers" <code>` toont geen `False`. Afgevinkt met de testuitvoer en de telling.
- Norm: ASVS 5.0.0 V1.3.11 (L2).
- Zie ook: INV-48, WEB-68, INV-56, INV-49, INV-50, MSG-26

### MSG-05 Controleer het certificaat op elke SMTP- en IMAP-verbinding
hoog · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Verbind met een mailserver alleen over TLS, bij voorkeur op de poort met directe TLS (993 voor IMAP, 465 voor verzending) en op 587 alleen met verplichte STARTTLS (de verbinding breekt af als TLS niet lukt), en geef de client expliciet een context die certificaat en hostnaam controleert; zet de controle nooit uit om een fout weg te krijgen.
- Bewijs: `grep -rnE "IMAP4_SSL\(|SMTP_SSL\(|starttls\(" <code>` toont bij elke aanroep een context uit `ssl.create_default_context()`; `grep -rnE "rejectUnauthorized: *false|CERT_NONE|check_hostname *= *False|verify=False" <code>` is leeg; een test tegen een server met een zelfondertekend certificaat eindigt in een fout. Afgevinkt met grep en de testuitvoer.
- Norm: ASVS 5.0.0 V12.3.1 (L2), V12.3.2 (L2).

### MSG-06 Houd de mailbibliotheek binnen de hersteltermijnen, juist bij meerdere tenants
hoog · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Behandel de bibliotheek die mail verstuurt of ontleedt als kritieke afhankelijkheid: volg de adviezen ervan en werk bij binnen de vaste termijnen (kritiek of actief misbruikt 48 uur, hoog 7 dagen, middel 30 dagen).
- Bewijs: `npm ls nodemailer mailparser imapflow` of `composer show phpmailer/phpmailer` toont de versies; `npm audit --omit=dev` of `osv-scanner` meldt geen open advies voor deze pakketten boven de termijn. Afgevinkt met de uitvoer en de datum. Zie GIT voor de audit als poort.
- Norm: ASVS 5.0.0 V15.2.1 (L1, onderdelen binnen de vastgelegde hersteltermijnen); besluit 22 van Marketing Maatwerk (hersteltermijnen).
- Zie ook: GIT-77, INFRA-24, ARCH-32, WP-49, GIT-88, DB-92, GIT-61, PRIV-73, SCR-32
