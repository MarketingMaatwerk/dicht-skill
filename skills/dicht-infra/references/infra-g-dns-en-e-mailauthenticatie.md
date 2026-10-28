# INFRA G: DNS en e-mailauthenticatie

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-56 Publiceer precies één SPF-record dat eindigt op een harde weigering
hoog · hard · website | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elk domein één SPF-record dat alle echte verzendroutes noemt, hooguit tien DNS-opzoekingen kost en eindigt op `-all`; gebruik `~all` alleen tijdens een uitrol met een einddatum.
- Bewijs: `dig +short TXT <domein> | grep -c 'v=spf1'` geeft 1; het record eindigt op `-all`; een telling van `include`, `a`, `mx`, `ptr`, `exists` en `redirect` (ook genest) blijft op tien of lager; een echte mail per verzendroute toont `spf=pass` in `Authentication-Results`. Afgevinkt met de uitvoer en de headers.
- Norm: geen ASVS-eis; Forum Standaardisatie "pas toe of leg uit" voor overheden (niet nagelezen, Niet bevestigd punt 4).

### INFRA-57 Onderteken elke verzendroute met DKIM en meet het aan echte mail
hoog · hard · website | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet DKIM aan voor elke route die namens het domein verstuurt, met een RSA-sleutel van minstens 2048 bit, en bewijs het met de headers van een ontvangen bericht per route.
- Bewijs: Per verzendroute een ontvangen bericht met `DKIM-Signature` (`d=` gelijk aan het From-domein) en `dkim=pass` in `Authentication-Results`; `dig +short TXT <selector>._domainkey.<domein>` toont de sleutel. Lees de selector uit de zone of de header, raad hem niet. Afgevinkt met de headers per route.
- Norm: geen ASVS-eis.

### INFRA-58 Zet DMARC op elk domein en kies het eindbeleid per soort mail
hoog · hard · website | api | app | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Publiceer op elk domein een DMARC-record met een `rua`-adres dat gelezen wordt, begin op `p=none` (minstens een maand), en ga na het lezen van de rapporten naar `p=quarantine` (even lang). Ga alleen door naar `p=reject` op een domein of subdomein dat uitsluitend geautomatiseerde mail verstuurt (transactiemail, verzendlijnen) of dat niet mailt (INFRA-59), en onderteken daar elke mail met DKIM. Op een domein waar mensen vanaf mailen is `p=quarantine` het eindpunt: zo'n domein hoort volgens RFC 9989 geen `p=reject` te publiceren, omdat doorgestuurde mail en maillijsten erop breken.
- Bewijs: `dig +short TXT _dmarc.<domein>` toont het beleid; bij een extern `rua`-adres bestaat het autorisatierecord; er is een rapport van de laatste zeven dagen ontvangen; `p=reject` staat alleen op een domein of subdomein zonder menselijke afzenders, en de keuze per domein staat in de documentatie van het project. Afgevinkt met de uitvoer, een rapport en de vastgelegde keuze.
- Norm: geen ASVS-eis.
- Zie ook: INFRA-63, MSG-02, MSG-03, MSG-07, MSG-11, MSG-13, MSG-15

### INFRA-59 Sluit domeinen die niet mailen volledig af
middel · hard · website | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elk domein en subdomein dat nooit mail verstuurt `v=spf1 -all`, een DMARC-record met `p=reject` en een null MX (`MX 0 .`).
- Bewijs: Voor elk domein uit de domeinlijst van de klant dat niet mailt: `dig +short TXT <domein>`, `dig +short TXT _dmarc.<domein>` en `dig +short MX <domein>` tonen de drie records. Afgevinkt met de uitvoer per domein.
- Norm: geen ASVS-eis.

### INFRA-60 Dwing TLS voor inkomende mail af met MTA-STS en vraag rapporten met TLS-RPT
laag · richtlijn · website | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Publiceer voor domeinen met eigen mail een MTA-STS-beleid (eerst `mode: testing`, daarna `enforce`) en een TLS-RPT-record.
- Bewijs: `dig +short TXT _mta-sts.<domein>`, `dig +short TXT _smtp._tls.<domein>` en `curl -s https://mta-sts.<domein>/.well-known/mta-sts.txt` tonen record en beleid; de `mx`-regels komen overeen met `dig +short MX <domein>`. Afgevinkt met de uitvoer. Bij mail op gedeelde hosting: eerst nagaan of het certificaat van de mailserver de MX-naam dekt.
- Norm: ASVS 5.0.0 V12.3.1 (L2) naar de geest.

### INFRA-61 Zet DNSSEC aan en houd twee werkende nameservers
middel · richtlijn · website | klantproject | api | app · tegenlezer: scherpen (04-10-2026)
- Regel: Onderteken elke zone met DNSSEC, laat het DS-record bij het register plaatsen, en controleer dat elke opgegeven nameserver antwoordt.
- Bewijs: `dig +short DS <domein>` toont een record; `delv <domein>` of `dig +dnssec <domein> | grep -c RRSIG` bevestigt de ondertekening; `for ns in $(dig +short NS <domein>); do dig +short @$ns SOA <domein>; done` geeft per nameserver hetzelfde serienummer. Afgevinkt met de uitvoer.
- Norm: geen ASVS-eis.

### INFRA-62 Verwijder DNS-records voordat je de dienst erachter opheft
hoog · hard · website | klantproject | api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Haal bij het opheffen van een site, subdomein of externe dienst eerst het DNS-record weg en dan pas de dienst, en houd een lijst bij van alle domeinen en subdomeinen met waar ze naartoe wijzen.
- Bewijs: De lijst van records per zone (uit het panel of de API, niet geraden) met per record het doel en of dat doel nog van de klant is; voor elk CNAME: `dig +short <naam>` eindigt op een adres dat antwoordt met inhoud van de klant. Afgevinkt met de lijst en de datum.
- Norm: ASVS 5.0.0 V13.1.1 (L2, gedocumenteerde externe afhankelijkheden).

### INFRA-63 Voldoe aan de eisen van grote ontvangers voordat je in aantallen mailt
hoog · hard · api | app | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Verstuur geautomatiseerde of commerciële mail alleen vanaf een domein met SPF, DKIM en DMARC die uitlijnen met het From-adres, over TLS, met een afmeldmogelijkheid in één klik voor marketingmail, en houd het spampercentage in Postmaster Tools onder 0,10 procent en laat het nooit 0,30 procent of hoger worden. De bouw van afmelden in één klik, bounces en klachten staat in MSG-07 tot en met MSG-13.
- Bewijs: Headers van een ontvangen bericht per lijn (`spf=pass`, `dkim=pass`, `dmarc=pass`, `List-Unsubscribe` en `List-Unsubscribe-Post` bij marketingmail); het spampercentage uit Postmaster Tools met datum; de noodstop en het dagplafond van de lijn. Afgevinkt met de headers en het percentage. Of een bericht "marketing" is en welke grondslag geldt, hoort in PRIV.
- Norm: geen ASVS-eis.
- Zie ook: MSG-02, MSG-03, MSG-07, MSG-11, MSG-13, MSG-15, INFRA-58

### INFRA-64 Verstuur mail van een site of dienst via geauthenticeerde SMTP
middel · hard · website | wp-plugin | klantproject | api | app · eigen bron · tegenlezer: niet te bevestigen (04-10-2026)
- Regel: Laat elke site en elke dienst mail versturen via een SMTP-account met authenticatie en TLS, en niet via de lokale `sendmail` of PHP `mail()` van de hosting.
- Bewijs: Een testbericht vanaf elk formulier of elke dienst naar een testadres op het eigen domein; de headers tonen de SMTP-server als afzender en `dkim=pass`. Controleer aankomst via IMAP in alle mappen, ook de spammap (eigen ervaring). Afgevinkt met de headers.
- Norm: geen ASVS-eis.
- Eigen bron: geen primaire bron; bron is alleen eigen meting (eigen ervaring); de genoemde RFC's schrijven de route niet voor. Het deel "geen lokale sendmail of PHP mail()" heeft sinds batch 4 wel een primaire onderbouwing in MSG-16 (CVE-2016-10033). Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Zie ook: MSG-01, MSG-16, MSG-12, MSG-02, WEB-68

### INFRA-65 Publiceer een security.txt met een geldige vervaldatum
laag · richtlijn · website | api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elk eigen product en op de eigen site `/.well-known/security.txt` met minimaal `Contact` en `Expires`, en vernieuw de vervaldatum voordat hij verloopt.
- Bewijs: `curl -s https://<host>/.well-known/security.txt` toont `Contact:` en een `Expires:` in de toekomst. Afgevinkt met de uitvoer.
- Norm: geen ASVS-eis.
- Zie ook: PRIV-72
