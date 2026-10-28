---
name: dicht-wordpress
description: Regels met bewijs voor WordPress (plugins, thema's en mu-plugins met escapen, nonces, capabilities, $wpdb->prepare en REST-routes, wp-config, updates, LiteSpeed, WP-CLI, WooCommerce, werk op een klantsite). Niet voor PHP zonder WordPress (dicht-api).
---

# dicht-wordpress: WordPress, PHP, WooCommerce en Elementor

Sub-skill van `dicht`. Bevat de 86 regels van domein WP in vijftien thema's. Komt bovenop `dicht-web` (browser), `dicht-api` (PHP in het algemeen, thema API-J) en `dicht-git` (plugins van derden, Composer).

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/wp-a-uitvoer-en-invoer-in-plugin-en-thema.md` | WP-01 t/m WP-08 (8 actief) | Uitvoer en invoer in plugin en thema |
| `references/wp-b-csrf-en-autorisatie.md` | WP-09 t/m WP-15 (7 actief) | CSRF en autorisatie |
| `references/wp-c-database.md` | WP-16 t/m WP-21 (6 actief) | Database |
| `references/wp-d-bestanden-serialisatie-externe-aanvragen-en-redi.md` | WP-22 t/m WP-29 (8 actief) | Bestanden, serialisatie, externe aanvragen en redirects |
| `references/wp-e-shortcodes-blokken-instellingen-en-mu-plugins.md` | WP-30 t/m WP-37 (8 actief) | Shortcodes, blokken, instellingen en mu-plugins |
| `references/wp-f-wp-config-en-bestandsrechten.md` | WP-38 t/m WP-46 (9 actief) | wp-config en bestandsrechten |
| `references/wp-g-updates.md` | WP-47 t/m WP-54 (8 actief) | Updates |
| `references/wp-h-blootstelling-en-inloggen.md` | WP-55 t/m WP-63 (9 actief) | Blootstelling en inloggen |
| `references/wp-i-serverlaag-van-klantsites-htaccess-litespeed-en.md` | WP-64 t/m WP-67 (4 actief) | Serverlaag van klantsites: .htaccess, LiteSpeed en cache |
| `references/wp-j-wp-cli.md` | WP-68 t/m WP-71 (4 actief) | WP-CLI |
| `references/wp-k-plugins-van-derden-elementor-en-beheer-op-afstan.md` | WP-72 t/m WP-76 (4 actief) | Plugins van derden, Elementor en beheer op afstand |
| `references/wp-l-malware-vinden-en-herstellen.md` | WP-77 t/m WP-79 (3 actief) | Malware vinden en herstellen |
| `references/wp-m-multisite.md` | WP-80 (1 actief) | Multisite |
| `references/wp-n-woocommerce.md` | WP-81 t/m WP-83 (3 actief) | WooCommerce |
| `references/wp-o-opleveren-met-bewijs.md` | WP-84 t/m WP-86 (3 actief) | Opleveren met bewijs |

## Wanneer niet

- Algemene PHP-valkuilen (type juggling, include, `unserialize`, productie-instellingen): `dicht-api`, thema API-J.
- Hosting, panel, accounts per site en back-ups van de host: `dicht-infra`, thema M en J.
- Beoordeling van een plugin van derden en Composer: `dicht-git`, thema H. WP-72 is daarmee samengevoegd (GIT-84).
- Bewaartermijnen, herroeping en privacy in WooCommerce: `dicht-privacy`.

## Verhouding tot bestaande skills

`wordpress-pro` geeft goede codevoorbeelden voor escapen, nonces en `$wpdb->prepare`, maar is op deze punten dun of onjuist. Daar gaan deze regels voor:
- Het voorbeeld `echo '<script>var config = ' . wp_json_encode($config) . ';</script>';` is onveilig zonder `JSON_HEX_TAG`: WP-03.
- Het voorbeeld met `WHERE post_id IN ({$ids})` binnen `prepare()` zet een variabele rechtstreeks in de query: WP-19.
- "Use nonces for form submissions" zonder de zin dat een nonce geen autorisatie is: WP-10.
- Hij noemt nergens `permission_callback`, `wp_unslash`, `wp_safe_redirect`, `%i`, `unserialize`, XML-RPC, automatische updates of malwareherstel: WP-13, WP-06, WP-27, WP-16, WP-26, WP-55, WP-47, WP-78.
