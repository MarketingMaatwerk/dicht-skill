# WP M: Multisite

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-80 Gebruik multisite alleen voor sites van één eigenaar en beperk de superbeheerder
middel · richtlijn · klantproject | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet sites van verschillende klanten nooit in één multisite-netwerk, geef de rol superbeheerder aan zo min mogelijk accounts, en test eigen plugins op multisite voordat je ze netwerkbreed activeert.
- Bewijs: `wp super-admin list` komt overeen met de afgesproken lijst; `wp plugin list --status=active-network` is beoordeeld volgens WP-72; een test met twee sites in het netwerk laat zien dat een beheerder van site A geen gegevens van site B kan lezen of wijzigen via de eigen plugin. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V8.2.2 (L1). Zie AUTH-72 tot en met AUTH-78 voor isolatie tussen tenants.
