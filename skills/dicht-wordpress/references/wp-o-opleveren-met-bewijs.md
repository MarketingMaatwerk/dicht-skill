# WP O: Opleveren met bewijs

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-84 Lever een eigen plugin of thema op met een vast bewijspakket
hoog · hard · wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Voeg bij elke oplevering van een eigen plugin, thema of mu-plugin een bewijsbestand toe met: de uitvoer van PHPCS, Plugin Check en PHPStan (WP-37), de lijst van handlers met per handler nonce, capability en test (WP-09, WP-10, WP-13), de uitkomst van de payloadtests (WP-01, WP-16, WP-22), de lijst van publieke routes en `nopriv`-acties (WP-12, WP-13), en de geteste versies van WordPress en PHP.
- Bewijs: Het bewijsbestand in de vorm van ARCH-53 (`bewijs/<jjjj-mm-dd>-<korte hash>.md`) staat in de repository bij de tag van de oplevering, met datum en de versies; elke uitvoer is van die commit. Afgevinkt als het bestand bestaat en compleet is.
- Norm: ASVS 5.0.0 V15.1.1 (L1), V8.1.1 (L1).
- Zie ook: ARCH-52, ARCH-53, WP-86

### WP-85 Doe een nulmeting voordat je een bestaande site in beheer neemt
hoog · hard · klantproject · eigen bron · tegenlezer: scherpen (04-10-2026)
- Regel: Voer bij elke site die je overneemt of waar je onderhoud op gaat doen eerst een nulmeting uit: versies en stable-check (WP-47), updateblokkades (WP-48), beheerders en applicatiewachtwoorden (WP-59, WP-60), mu-plugins en drop-ins (WP-34), de malwarecontrole (WP-77), bekende paden en back-ups (WP-62, WP-63), plugins van derden en beheer op afstand (WP-72, WP-75), en leg de uitkomst vast in het CRM.
- Bewijs: Een notitie in het CRM op het bedrijfsprofiel met de datum van de nulmeting, de bevindingen en de openstaande punten; de uitvoer staat in de klantmap. Afgevinkt met de notitie.
- Norm: ASVS 5.0.0 V15.1.2 (L2), V15.2.1 (L1).
- Eigen bron: geen primaire bron; de werkwijze komt uit eigen incidenten (eigen ervaring); ASVS V15.1.2 en V15.2.1 dragen alleen het doel. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).

### WP-86 Sluit elke klus op een klantsite af met een korte controle en een notitie
middel · hard · klantproject · eigen bron · tegenlezer: scherpen (04-10-2026)
- Regel: Controleer na elke wijziging op een klantsite dat de voorpagina, de inlog en het belangrijkste formulier of de afrekenstap werken, dat er geen testbestanden, testaccounts of tijdelijke mu-plugins zijn achtergebleven, en noteer in het CRM wat er is gewijzigd.
- Bewijs: `ls wp-content/mu-plugins/` en `find . -maxdepth 2 -newermt '<begin van de klus>' -name '*.php'` tonen alleen bedoelde bestanden; `wp user list --role=administrator` is ongewijzigd; drie curl-controles met 200; de notitie in het CRM. Afgevinkt met de uitvoer en de notitie.
- Norm: ASVS 5.0.0 V15.2.3 (L2).
- Eigen bron: geen primaire bron; de werkwijze komt uit eigen praktijk (eigen ervaring); ASVS V15.2.3 draagt alleen het doel. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Zie ook: ARCH-52, ARCH-53, WP-84
