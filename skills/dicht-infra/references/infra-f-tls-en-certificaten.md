# INFRA F: TLS en certificaten

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-50 Vernieuw certificaten volledig automatisch
hoog · hard · api | app | mcp | website | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elk publiek certificaat uit en vernieuw het met een ACME-client die zonder menselijke handeling draait, en laat hem vernieuwen op aanwijzing van ARI of rond twee derde van de looptijd.
- Bewijs: `certbot certificates` (of het equivalent van de client) toont elk certificaat met vervaldatum; `certbot renew --dry-run` slaagt voor alle; een lijst van alle hostnamen in nginx (`nginx -T | grep ssl_certificate`) is vergeleken met die lijst. Afgevinkt als elke hostnaam een automatisch vernieuwd certificaat heeft.
- Norm: ASVS 5.0.0 V12.2.2 (L1).

### INFRA-51 Laat de webserver het vernieuwde certificaat ook laden
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Koppel aan de vernieuwing een actie die de webserver herlaadt, en bewijs met een meting dat het certificaat op de poort gelijk is aan het certificaat op schijf.
- Bewijs: Voor elke hostnaam: `echo | openssl s_client -connect <host>:443 -servername <host> 2>/dev/null | openssl x509 -noout -enddate` is gelijk aan `openssl x509 -noout -enddate -in <pad>/fullchain.pem`; de configuratie van de client toont de hook of het herlaadmechanisme. Afgevinkt met de vergelijking en het mechanisme.
- Norm: ASVS 5.0.0 V12.2.2 (L1).

### INFRA-52 Bewaak de vervaldatum van buitenaf
hoog · hard · api | app | mcp | website | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een bewaking buiten de server elk publiek certificaat dagelijks controleren en alarm slaan als de resterende looptijd onder een derde van de totale looptijd komt.
- Bewijs: De bewaking toont per hostnaam de vervaldatum en de drempel; een testmelding is aangekomen op het alarmkanaal (INFRA-87). Afgevinkt met schermafdruk of uitvoer en de testmelding.
- Norm: ASVS 5.0.0 V12.2.2 (L1).
- Zie ook: ARCH-67, INFRA-35, ARCH-69, INFRA-86, INFRA-87, DB-97, DB-47, AI-83

### INFRA-53 Leg met CAA vast wie certificaten mag uitgeven
middel · richtlijn · website | api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elk domein een CAA-record met alleen de eigen certificaatautoriteit, en voeg voor kritieke domeinen `accounturi` toe.
- Bewijs: `dig +short CAA <domein>` toont het record; controleer vooraf welke CA de hostingpartij gebruikt (Enhance en panelen geven zelf certificaten uit), anders mislukt hun vernieuwing. Afgevinkt met de uitvoer en een geslaagde vernieuwing daarna.
- Norm: geen ASVS-eis.

### INFRA-54 Bescherm de private sleutel van het certificaat
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef private sleutels alleen leesrecht voor root (modus 600), houd ze buiten git en buiten de webroot, en neem ze alleen versleuteld mee in een back-up.
- Bewijs: `sudo find <letsencrypt-pad> -name 'privkey*.pem' -printf '%m %u %p\n'` toont 600 en root; `git -C <repo> ls-files | grep -iE '\.(key|pem)$'` is leeg; de back-upconfiguratie versleutelt of sluit de map uit. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.3.1 (L2), V13.3.2 (L2).

### INFRA-55 Versleutel en controleer elke verbinding die de host verlaat
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik TLS met certificaatcontrole voor elke verbinding van of naar een andere machine (database, SMTP, IMAP, API, back-updoel, monitoring), en schakel certificaatcontrole nooit uit om een fout te omzeilen.
- Bewijs: `grep -rnE "rejectUnauthorized:\s*false|verify_peer['\"]?\s*=>\s*false|NODE_TLS_REJECT_UNAUTHORIZED|sslmode=(disable|allow|prefer|require)\b|CURLOPT_SSL_VERIFYPEER,\s*(0|false)|curl .*(-k|--insecure)" <code en scripts>` is leeg of elke treffer betreft loopback. Afgevinkt met de uitvoer. Voor de database: zie DB-60.
- Norm: ASVS 5.0.0 V12.3.1 (L2), V12.3.2 (L2), V12.3.3 (L2).
- Zie ook: WEB-56, WEB-17, WP-43, INFRA-44, INFRA-48, DB-60
