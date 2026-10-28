# WP H: Blootstelling en inloggen

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-55 Zet XML-RPC dicht op de server, tenzij een dienst het nodig heeft
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Blokkeer `xmlrpc.php` op serverniveau (403) op elke site die geen Jetpack, mobiele app of andere XML-RPC-koppeling gebruikt, en begrens het streng waar het wel nodig is.
- Bewijs: `curl -s -o /dev/null -w '%{http_code}' -X POST -d '<methodCall><methodName>system.listMethods</methodName></methodCall>' https://site/xmlrpc.php` geeft 403. Op sites van Marketing Maatwerk doet het eigen formulierschild dit, behalve met Jetpack. Staat het open, dan is er een notitie welke dienst het nodig heeft en welke begrenzing geldt. Afgevinkt met de curl-uitvoer.
- Norm: ASVS 5.0.0 V6.3.4 (L2), V6.3.1 (L1), V15.2.3 (L2).
- Zie ook: AUTH-10, WP-57, AUTH-12, WP-56, AUTH-13

### WP-56 Geef geen gebruikersnamen weg
middel · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Sluit voor anonieme bezoekers `/wp-json/wp/v2/users`, de doorverwijzing van `?author=<nummer>` en het verschil in foutmeldingen bij inloggen en wachtwoord vergeten, en gebruik als inlognaam nooit `admin`, de domeinnaam of de weergavenaam.
- Bewijs: Anoniem: `curl -s -o /dev/null -w '%{http_code}' https://site/wp-json/wp/v2/users` geeft 401 of 403; `curl -sI 'https://site/?author=1'` geeft geen `Location` met een naam; een inlogpoging met een bestaande en een niet-bestaande naam geeft dezelfde melding; idem voor wachtwoord vergeten. `wp user list --role=administrator --field=user_login` bevat geen `admin`. Op sites van Marketing Maatwerk regelt het eigen formulierschild de eerste drie. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V6.3.8 (L3; hier hard omdat het weinig kost), V6.3.2 (L1).
- Zie ook: AUTH-10, WP-57, AUTH-12, AUTH-13, WP-55

### WP-57 Begrens inlogpogingen op elk inlogpad
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Begrens mislukte inlogpogingen per IP en per account op `wp-login.php`, op XML-RPC (als het open staat), op de REST API met basisauthenticatie en op elk eigen inlogformulier (WooCommerce "Mijn account", ledenportaal).
- Bewijs: Per inlogpad zes foute pogingen achter elkaar vanaf één adres: de zesde wordt geweigerd of vertraagd (op sites van Marketing Maatwerk: het eigen formulierschild, 5 fouten per 15 minuten per IP of account). Test vanaf een eigen adres en ruim de teller daarna op. Afgevinkt met de uitvoer per pad.
- Norm: ASVS 5.0.0 V6.3.1 (L1), V6.1.1 (L1), V6.3.4 (L2).
- Zie ook: API-20, WEB-66, INFRA-46, API-22, AUTH-10, AI-45, AI-74, AUTH-12, WP-56, AUTH-13, WP-55

### WP-58 Verplicht een tweede factor voor elke beheerder
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet voor elk account met de rol beheerder (en winkelbeheerder in WooCommerce) een tweede factor aan met een onderhouden plugin, en registreer per beheerder minstens twee middelen of herstelcodes.
- Bewijs: Voor elke gebruiker uit `wp user list --role=administrator --field=ID` is een tweede factor geregistreerd (bij de plugin Two-Factor: `wp user meta get <id> _two_factor_enabled_providers` is niet leeg); een inlog met alleen het wachtwoord komt niet in wp-admin. Afgevinkt met de uitvoer en één testinlog.
- Norm: ASVS 5.0.0 V6.3.3 (L2).
- Zie ook: AUTH-16, AUTH-82, INFRA-98, GIT-14, PRIV-53, INFRA-11

### WP-59 Houd het aantal beheerders klein en ruim accounts op
middel · hard · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef alleen de rol beheerder aan wie plugins moet kunnen installeren, geef de klant voor dagelijks werk de rol redacteur of winkelbeheerder, verwijder accounts van vertrokken medewerkers en vorige bureaus, en loop de lijst na bij elke overdracht en elk kwartaal.
- Bewijs: `wp user list --role=administrator --fields=ID,user_login,user_email,user_registered` komt overeen met de afgesproken lijst in het CRM; geen adressen op `.invalid`, `.internal` of onbekende domeinen; geen account van een vorig bureau. Afgevinkt met de uitvoer en de datum.
- Norm: ASVS 5.0.0 V8.1.1 (L1), V8.2.1 (L1), V7.4.2 (L1).

### WP-60 Beheer applicatiewachtwoorden per koppeling en trek ongebruikte in
middel · hard · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak per koppeling een eigen applicatiewachtwoord op een account met de laagste rol die volstaat, noteer waarvoor het is, trek het in zodra de koppeling stopt, en zet de functie uit op sites die hem niet gebruiken.
- Bewijs: Voor elke beheerder: `wp user application-password list <id> --fields=uuid,name,created,last_used,last_ip` is leeg of elke regel hoort bij een bekende koppeling en is recent gebruikt. Na een incident: alle regels verwijderd met `wp user application-password delete <id> <uuid>`. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V6.3.4 (L2), V13.2.1 (L2).

### WP-61 Zet de REST API niet uit; beperk wat anoniem zichtbaar is
middel · richtlijn · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat de REST API aan staan en beperk anonieme toegang gericht: sluit de routes die gegevens prijsgeven (gebruikers, eigen routes met interne data) en laat de rest werken.
- Bewijs: `curl -s https://site/wp-json/ | jq -r '.namespaces[]'` geeft de lijst van namespaces; voor elke namespace van eigen bouw is anoniem getest welke routes antwoorden (WP-13); na elke beperking is een testinzending van elk formulier gedaan. Afgevinkt met de lijst en de testinzendingen.
- Norm: ASVS 5.0.0 V13.4.5 (L2), V15.3.1 (L1).

### WP-62 Vraag bij elke oplevering de bekende WordPress-paden zelf op
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer anoniem dat deze paden niets prijsgeven: `wp-content/debug.log`, kopieën van `wp-config.php`, `.git/config`, `.env`, databasedumps (`*.sql`, `*.sql.gz`), zip- en tar-bestanden in de webroot, `wp-content/uploads/` als mapweergave, `wp-content/ai1wm-backups/`, `wp-content/updraft/`, `wp-content/backups*`, `wp-admin/install.php` en `phpinfo.php` of `info.php`.
- Bewijs: Een lus met `curl -s -o /dev/null -w '%{http_code} %{size_download}'` over de lijst, per site, met ernaast dezelfde aanvraag voor een niet-bestaande naam in dezelfde map (om een 200 van een nette foutpagina of een 403 van een blokkade te kunnen onderscheiden, zie WP-64); op de server `find . -maxdepth 3 \( -name '*.sql*' -o -name '*.zip' -o -name '*.tar*' -o -name '*.wpress' -o -name '*.bak' \)`. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V13.4.1 (L1), V13.4.3 (L2), V13.4.7 (L3), V15.2.3 (L2).
- Zie ook: ARCH-83, API-25, AUTH-13

### WP-63 Laat een back-up nooit in de webroot staan
kritiek · hard · klantproject | website · tegenlezer: scherpen (04-10-2026)
- Regel: Bewaar back-ups buiten de webroot of bij de hoster, verwijder na elke migratie het `.wpress`-, zip- of sql-bestand van de server, en controleer anoniem dat de back-upmap van elke back-up- of migratieplugin geen bestand uitlevert.
- Bewijs: Op de server: `find wp-content -maxdepth 4 -name '*.wpress'` is leeg. Anoniem: een bestaand of opzettelijk geplaatst testbestand in de map geeft 403. Let op: met de blokkade geeft ook een verwijderd bestand 403 en geen 404; "weg" bewijs je dus op de server. Afgevinkt met beide uitvoeren. Verwijderen op een live klantsite alleen na akkoord en na controle dat er een back-up bij de hoster is.
- Norm: ASVS 5.0.0 V13.4.7 (L3; hier hard), V14.2.2 (L2), V15.2.3 (L2); AVG artikel 32 (zie PRIV).
- Zie ook: WEB-64, API-81, ARCH-05, WP-41, API-25, WP-53, DB-40, ARCH-25
