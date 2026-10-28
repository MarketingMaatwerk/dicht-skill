# WP K: Plugins van derden, Elementor en beheer op afstand

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-72 → GIT-84
Samengevoegd: "Beoordeel elke plugin voordat hij op een site komt en houd de lijst kort" is gedekt door GIT-84. Gebruik die regel.

### WP-73 Haal plugins en thema's alleen van de maker of van wordpress.org
kritiek · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Installeer plugins en thema's alleen vanaf wordpress.org of rechtstreeks van de maker met een geldige licentie, nooit een "nulled" of doorverkochte kopie, en houd premiumplugins net zo bij als gratis plugins. Aanvulling uit GIT-85: De licentie staat op naam van de klant of van Marketing Maatwerk.
- Bewijs: Voor elke plugin die niet op wordpress.org staat: de bron, de licentiehouder en de vervaldatum staan in het CRM; `wp plugin verify-checksums --all` is groen voor alle plugins van wordpress.org (voor premiumplugins bestaat die controle niet, daar telt de versie van de maker). Afgevinkt met de lijst en de uitvoer.
    Ook (uit GIT-85): Per plugin die niet van wordpress.org komt, staat in het dossier de leverancier, het licentienummer of account, en de downloadbron. Afgevinkt met die lijst. Een primaire bron over nulled plugins is niet gevonden; de regel steunt op de werking van `verify-checksums` (GIT-87) en ASVS V15.1.2.
- Norm: ASVS 5.0.0 V15.1.2 (L2), V15.2.4 (L3).
- Dekt ook: GIT-85
- Zie ook: GIT-84, GIT-86, WP-51, GIT-87, WP-74, WP-75, WP-76, GIT-89

### WP-74 Houd Elementor en andere paginabouwers strak bij en beperk wie ermee mag werken
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Behandel Elementor, Elementor Pro en elke uitbreiding erop als kritieke afhankelijkheid: updates binnen de termijn van WP-49, zo min mogelijk uitbreidingen van derden, en toegang tot de editor alleen voor rollen die dat nodig hebben.
- Bewijs: `wp plugin list --fields=name,version,update | grep -i elementor` toont geen openstaande update (op 04-10-2026 is Elementor 4.3.3 de versie op wordpress.org); de lijst van uitbreidingen is beoordeeld volgens WP-72. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V15.2.1 (L1), V15.1.4 (L3).
- Zie ook: GIT-84, WP-73, GIT-86, WP-51, GIT-87, WP-75, WP-76, GIT-89

### WP-75 Behandel een plugin voor beheer op afstand als een beheerderssleutel
hoog · hard · klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat op een site hooguit één hulpmiddel voor beheer op afstand staan dat je zelf beheert, verwijder de client van elk vorig bureau of elke vorige hoster (InfiniteWP, MainWP, ManageWP, Installatron en vergelijkbaar), en controleer na verwijderen dat updates weer zichtbaar zijn.
- Bewijs: `wp plugin list --field=name | grep -iE "iwp-client|mainwp|worker|installatron"` en `ls wp-content/mu-plugins/` tonen alleen wat bewust is gekozen; in het CRM staat welke partij welk hulpmiddel beheert. Verwijderen op een live site na akkoord, en na afstemming met de partij die het gebruikt. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V6.3.4 (L2), V15.2.3 (L2).
- Zie ook: GIT-84, WP-73, GIT-86, WP-51, GIT-87, WP-74, WP-76, GIT-89

### WP-76 Gebruik geen plugins die code uit de database uitvoeren of bestanden beheren
hoog · hard · klantproject | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Installeer geen plugins die PHP uit een instellingenveld uitvoeren (codefragmenten, "PHP in widgets") en geen bestandsbeheerders in wp-admin; zet eigen code in een mu-plugin of het thema in de repository.
- Bewijs: De pluginlijst bevat geen bestandsbeheerder en geen plugin voor PHP-fragmenten; waar een fragmentenplugin om een reden blijft, staat het uitvoeren van PHP uit en staat de reden genoteerd. Afgevinkt met de pluginlijst.
- Norm: ASVS 5.0.0 V1.3.2 (L1), V15.2.3 (L2).
- Zie ook: GIT-84, WP-73, GIT-86, WP-51, GIT-87, WP-74, WP-75, GIT-89
