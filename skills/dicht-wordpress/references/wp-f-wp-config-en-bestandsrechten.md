# WP F: wp-config en bestandsrechten

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-38 Geef elke installatie eigen sleutels en salts en wissel ze na elk incident
kritiek · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in `wp-config.php` acht unieke, willekeurige waarden voor de `*_KEY`- en `*_SALT`-constanten, kopieer ze nooit van een andere site of uit een sjabloon, en vervang ze na elk vermoeden van een lek, na een gelekte back-up en bij het overnemen van een site.
- Bewijs: `grep -c "put your unique phrase here" wp-config.php` geeft 0; de hash van de acht regels verschilt per site (`grep -E "_(KEY|SALT)'" wp-config.php | sha256sum` naast elkaar voor alle sites van één klant en voor staging en live). Na een incident: `wp config shuffle-salts` uitgevoerd en de datum genoteerd. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V11.5.1 (L2), V13.3.1 (L2), V7.4.1 (L1) voor het beëindigen van sessies.
- Zie ook: GIT-36, INFRA-93, WP-79, GIT-54, INFRA-75

### WP-39 Zet de bestandseditor in wp-admin uit
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Definieer `DISALLOW_FILE_EDIT` als `true` op elke site, en gebruik `DISALLOW_FILE_MODS` alleen op sites waar updates aantoonbaar via een andere weg lopen.
- Bewijs: `wp config get DISALLOW_FILE_EDIT` geeft `1` of `true`; `wp eval 'var_dump( wp_is_file_mod_allowed( "automatic_updater" ) );'` geeft `true` tenzij het updateproces buiten WordPress is vastgelegd. Op sites van Marketing Maatwerk zet het eigen formulierschild de constante. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V15.2.3 (L2), V13.4.2 (L2).

### WP-40 Zet debug uit in productie en maak het foutlog onbereikbaar
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op productie `WP_DEBUG` op `false`, of als loggen nodig is `WP_DEBUG_DISPLAY` op `false` en `WP_DEBUG_LOG` op een pad buiten de webroot, zorg dat `display_errors` in PHP uit staat, en laat `wp-content/debug.log` niet bestaan of niet opvraagbaar zijn.
- Bewijs: `curl -s -o /dev/null -w '%{http_code}' https://site/wp-content/debug.log` geeft 403 of 404 (en een vergelijkbare niet-bestaande naam geeft dezelfde code, zie WP-64); `wp config get WP_DEBUG` is leeg of `false`; een opzettelijke fout op een testkopie toont de bezoeker geen PHP-melding. Site Health meldt geen waarschuwing over het debuglog. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.4.2 (L2), V16.5.1 (L2), V16.4.2 (L2).
- Zie ook: WEB-62, API-10, API-11, API-79, ARCH-72

### WP-41 Maak wp-config.php onleesbaar voor anderen en laat er geen kopieën van slingeren
kritiek · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `wp-config.php` op rechten 400, 440 of 600, blokkeer het opvragen ervan op serverniveau, en laat in de webroot geen kopie staan met een andere naam of extensie (`wp-config.php.bak`, `.old`, `.save`, `.txt`, `~`, `.swp`).
- Bewijs: `stat -c '%a %U' wp-config.php` toont 400, 440 of 600 en de eigenaar van het account; `ls -la | grep -i "wp-config"` toont alleen het ene bestand; een lus met curl over de varianten `.bak .old .save .orig .txt ~ .swp` geeft overal 404 of 403. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.4.7 (L3, hier hard vanwege de inhoud), V13.3.2 (L2).
- Zie ook: WEB-64, API-81, ARCH-05, WP-63, API-25

### WP-42 Houd bestanden op 644 en mappen op 755, met het account als eigenaar
middel · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet mappen op 755 en bestanden op 644 (of strenger), laat alles eigendom zijn van het hostingaccount, en gebruik nergens 777 of 666.
- Bewijs: `find . -type d -perm -o+w` en `find . -type f -perm -o+w` zijn leeg; `find . ! -user <account>` is leeg. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.3.2 (L2) naar analogie; CIS-achtige basisregel, zie INFRA.

### WP-43 Dwing HTTPS af voor de hele site en voor wp-admin
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `siteurl` en `home` op `https://`, definieer `FORCE_SSL_ADMIN` als `true`, en stuur elke HTTP-aanvraag met één 301 door naar HTTPS.
- Bewijs: `wp option get siteurl` en `wp option get home` beginnen met `https://`; `wp config get FORCE_SSL_ADMIN` is waar; `curl -sI http://site/wp-login.php` geeft 301 naar https. Meet www en het hoofddomein 10 tot 20 keer met een volledige GET (zie WP-65). Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V12.2.1 (L1), V3.4.1 (L1).
- Zie ook: WEB-56, WEB-17, INFRA-44, INFRA-55, INFRA-48, DB-60

### WP-44 Reken niet op een ander tabelprefix
laag · richtlijn · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Kies bij een nieuwe installatie een eigen prefix als dat niets kost, maar wijzig het prefix van een bestaande site niet als beveiligingsmaatregel en tel het nooit mee als verdediging.
- Bewijs: Geen. Bij een nieuwe site: het prefix staat in de overdracht. Afgevinkt zonder verdere actie.
- Norm: geen.

### WP-45 Geef elke site een eigen database en een eigen databasegebruiker
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke WordPress-site verbinden met een eigen databasegebruiker die alleen rechten heeft op de database van die site, en laat staging en live nooit dezelfde database of gebruiker delen.
- Bewijs: Per site `wp config get DB_USER` en `DB_NAME`: geen twee sites met dezelfde waarde; `SHOW GRANTS FOR CURRENT_USER` (via `wp db query`) toont alleen rechten op de eigen database en geen `GRANT OPTION`, `FILE` of `SUPER`. Afgevinkt met de uitvoer per site.
- Norm: ASVS 5.0.0 V13.2.2 (L2).
- Zie ook: INFRA-66, INFRA-10, AUTH-56, DB-02, INFRA-97, WP-68, AI-21

### WP-46 Overweeg DISALLOW_UNFILTERED_HTML op sites met meer beheerders of redacteuren
middel · richtlijn · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Definieer `DISALLOW_UNFILTERED_HTML` als `true` op sites waar meer mensen dan de eigenaar de rol beheerder of redacteur hebben en niemand scripts in berichten hoeft te plakken.
- Bewijs: `wp config get DISALLOW_UNFILTERED_HTML` is waar, of er staat een notitie waarom niet (bijvoorbeeld een paginabouwer of ingesloten scripts die het nodig hebben; test dit eerst op een kopie). Afgevinkt met de uitvoer of de notitie.
- Norm: ASVS 5.0.0 V1.3.1 (L1).
