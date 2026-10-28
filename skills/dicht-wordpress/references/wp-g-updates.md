# WP G: Updates

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-47 Laat beveiligingsupdates van de kern automatisch installeren en controleer dat het gebeurt
kritiek · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat op elke site automatische updates voor kleine kernversies aan staan (`WP_AUTO_UPDATE_CORE` niet gedefinieerd of `'minor'` of `true`), en controleer per site de draaiende versie tegen `https://api.wordpress.org/core/stable-check/1.0/`.
- Bewijs: `v=$(wp core version); curl -s https://api.wordpress.org/core/stable-check/1.0/ | jq -r --arg v "$v" '.[$v]'` geeft `latest` of, voor een oudere tak, `outdated`; `insecure` is een blokkade. `wp eval 'var_dump( apply_filters( "automatic_updater_disabled", defined( "AUTOMATIC_UPDATER_DISABLED" ) && AUTOMATIC_UPDATER_DISABLED ) );'` geeft `false`. Op 04-10-2026 is 7.1.2 `latest` en zijn 7.0.6, 6.9.9 en 6.8.10 `outdated`. Afgevinkt met de uitvoer per site.
- Norm: ASVS 5.0.0 V15.2.1 (L1), V15.1.1 (L1); OWASP Top 10 2025 A03 Software Supply Chain Failures.

### WP-48 Controleer dat niets updates tegenhoudt of verbergt
hoog · hard · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel bij elke site die je in beheer neemt en bij elke controle vast dat geen mu-plugin, beheerplugin, constante, filter of versiebeheermap de automatische updater uitzet of beschikbare updates verbergt.
- Bewijs: (1) `ls wp-content/mu-plugins/` bevat geen `automation-by-installatron.php`. (2) `wp core check-update` en `wp --skip-plugins --skip-themes core check-update` geven dezelfde uitkomst; idem voor `wp plugin list --update=available`. (3) `wp eval 'var_dump( ( new WP_Automatic_Updater() )->is_disabled() );'` geeft `false` (op een testkopie: het bestand met de klasse moet geladen zijn, zie WP-70). (4) Site Health toont de test voor achtergrondupdates (`background_updates`) en die is groen. Afgevinkt met de vier uitvoeren.
- Norm: ASVS 5.0.0 V15.2.1 (L1).

### WP-49 Leg termijnen vast voor updates van plugins en thema's en houd je eraan
hoog · hard · klantproject | website · tegenlezer: scherpen (04-10-2026)
- Regel: Installeer een beveiligingsupdate van een plugin of thema binnen 48 uur als het lek kritiek is, actief wordt misbruikt (CISA KEV) of zonder inloggen te misbruiken is, binnen 7 dagen bij ernst hoog en binnen 30 dagen bij ernst middel (besluit 22); is er geen fix, zet de plugin dan uit of scherm de kwetsbare functie af tot er een is.
- Bewijs: `wp plugin list --update=available --format=json` en `wp theme list --update=available` zijn leeg of elke regel heeft een datum en reden; voor sites in beheer bij Marketing Maatwerk: de nachtrun van de site-security-scanner meldt "success" én de controle uit WP-48 is gedaan. De termijnen staan in het onderhoudscontract of de werkafspraak. Afgevinkt met de uitvoer en de datum van de laatste run.
- Norm: ASVS 5.0.0 V15.1.1 (L1), V15.2.1 (L1).
- Zie ook: GIT-77, INFRA-24, ARCH-32, GIT-88, DB-92, GIT-61, PRIV-73, MSG-06, SCR-32

### WP-50 Lees het getroffen versiebereik voordat je ingrijpt
middel · hard · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel bij elke melding van een lek het getroffen versiebereik vast uit de bron (NVD, het advies van de maker, Patchstack) en vergelijk dat met de geïnstalleerde versie, voordat je een site als kwetsbaar meldt of er een taak van maakt.
- Bewijs: Bij elke beveiligingstaak staat het getroffen bereik met de bron en de geïnstalleerde versie; voor de kern de uitkomst van stable-check (WP-47). Afgevinkt met de notitie in de taak.
- Norm: ASVS 5.0.0 V15.1.1 (L1).

### WP-51 Verwijder plugins en thema's die niet in gebruik zijn
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Verwijder elke inactieve plugin en elk thema dat niet het actieve thema, het bovenliggende thema of één standaardthema als terugval is; uitzetten is niet genoeg.
- Bewijs: `wp plugin list --status=inactive --field=name` is leeg; `wp theme list --status=inactive --field=name` toont hooguit het bovenliggende thema en één standaardthema. Op een live klantsite: eerst akkoord, eerst controleren of er gegevens van de plugin bewaard moeten blijven. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V15.2.3 (L2).
- Zie ook: GIT-84, WP-73, GIT-86, GIT-87, WP-74, WP-75, WP-76, GIT-89

### WP-52 Draai op een PHP-versie die nog beveiligingsupdates krijgt
hoog · hard · klantproject | website | wp-plugin | wp-thema · tegenlezer: scherpen (04-10-2026)
- Regel: Zet elke site op een PHP-versie met beveiligingsondersteuning (op 04-10-2026: 8.2 tot en met 31-12-2026, 8.3 tot en met 31-12-2027, 8.4 tot en met 31-12-2028, 8.5 tot en met 31-12-2029) en plan de overstap van 8.2 vóór het einde van 2026.
- Bewijs: `wp eval 'echo PHP_VERSION;'` (dit is de versie van de opdrachtregel) én de versie die de webserver gebruikt, gelezen in Site Health of het hostingpaneel: beide staan op php.net als "Active support" of "Security fixes only". Afgevinkt met beide waarden.
- Norm: ASVS 5.0.0 V15.2.1 (L1).
- Zie ook: GIT-93, API-72, DB-93, INFRA-22, INFRA-42, AI-54, SCR-33

### WP-53 Zorg vóór elke update voor een terugweg
middel · hard · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer vóór een handmatige update van de kern, een grote pluginupdate of een PHP-wissel dat er een back-up van vandaag is die je kunt terugzetten, en test na de update de voorpagina, de inlog en het belangrijkste formulier of de afrekenstap.
- Bewijs: Het tijdstip van de laatste back-up (op Enhance via de API `/websites/{ws}/backups` of het paneel) ligt binnen 24 uur vóór de update; na de update drie curl-controles met status 200 en een echte testinzending op een eigen testadres. Afgevinkt met tijdstip en uitvoer. Voor de herstelproef zelf: zie INFRA en DB-46.
- Norm: ASVS 5.0.0 V15.1.1 (L1).
- Zie ook: WP-63, DB-40, ARCH-25

### WP-54 Volg beveiligingsnieuws automatisch en laat het op de eigen sites toetsen
middel · richtlijn · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd een geautomatiseerde bewaking in stand die de beveiligingsmeldingen van WordPress, Patchstack en vergelijkbare bronnen leest, per melding de eigen sites op versie of spoor controleert, en alleen bij een echte treffer een taak maakt.
- Bewijs: De laatste run van de eigen updatebewaking en van de nachtelijke scan is van vandaag; een site die niet is gecontroleerd is verklaard; een uitgezonderd domein is een besluit met datum. Afgevinkt met de logregels.
- Norm: ASVS 5.0.0 V15.1.1 (L1), V15.1.2 (L2).
