# INV C: YAML en TOML

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-16 Lees YAML alleen met een veilige lader zonder eigen types
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik js-yaml 4 of hoger (of het pakket `yaml`) met het standaardschema, installeer `js-yaml-js-types` niet en geef geen `customTags` of eigen schema mee voor YAML die niet uit de eigen repository komt.
- Bewijs: `npm ls js-yaml js-yaml-js-types yaml` toont js-yaml 4 of hoger en geen `js-yaml-js-types`; `grep -rnE "customTags|DEFAULT_FULL_SCHEMA|js-yaml-js-types|schema:" src` is leeg of verklaard. Afgevinkt met beide uitvoeren. Voor Python: domein SCR.
- Norm: ASVS 5.0.0 V1.5.2 (L2).
- Zie ook: API-55, WP-26, SCR-27, SCR-28, INV-17

### INV-17 Begrens aliassen en samenvoegingen in YAML van buiten
middel · hard · api | app | mcp | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Laat bij het pakket `yaml` `maxAliasCount` op de standaard van 100 of lager, zet bij js-yaml (5.2.0 of hoger; in lijn 3 en 4 bestaat de optie niet) de optie `maxAliases` op een eindige waarde, en begrens de bestandsgrootte vóór het parsen.
- Bewijs: `grep -rnE "maxAliasCount|maxAliases" src` toont geen verhoging naar -1 en bij js-yaml een eindige waarde, met `npm ls js-yaml` op 5.2.0 of hoger; een test met een alias-bom wordt geweigerd met een fout en het proces blijft onder zijn geheugenlimiet. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V15.2.2 (L2).
- Zie ook: API-55, WP-26, SCR-27, SCR-28, INV-16

### INV-18 Valideer geparste YAML en TOML met een schema en reken niet op het geraden type
middel · richtlijn · alles · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Haal elk YAML- of TOML-configuratiebestand na het parsen door een schema (Zie ARCH-07), zet tekstwaarden die op een getal, datum of boolean lijken tussen aanhalingstekens, en leg vast welke YAML-versie de parser gebruikt.
- Bewijs: Het schema voor elk configuratiebestand staat in de repository en de start faalt bij een verkeerd type (test met `no` op de plek van een tekstwaarde). Afgevinkt met de test.
- Norm: ASVS 5.0.0 V1.5.3 (L3), V2.2.1 (L1).
