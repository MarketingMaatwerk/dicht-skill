# INV M: zoekpatronen en e-mailadressen

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-63 Ontdoe zoektekst van LIKE-jokertekens
laag · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in elke zoekterm die in een `LIKE`- of `ILIKE`-patroon belandt een backslash voor `%`, `_` en `\`, en eis een minimale lengte voor zoektermen op grote tabellen.
- Bewijs: `grep -rnE "i?like\(" src` toont bij elke aanroep met invoer de escape-functie; test: de zoekterm `%` geeft nul resultaten (of alleen namen met een procentteken), niet de hele tabel. Afgevinkt met grep en test. Voor WordPress: `esc_like()` (Zie de WP-regels over `$wpdb`).
- Norm: ASVS 5.0.0 V1.2.4 (L1), V15.2.2 (L2).
- Zie ook: DB-25, DB-26, DB-27, WP-16, WP-18, WP-19, DB-28, SCR-11, SCR-30

### INV-64 Accepteer e-mailadressen alleen in de eenvoudige vorm en beslis niets op het domein van een onbevestigd adres
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat alleen adressen toe van de vorm `lokaal@domein` zonder aanhalingstekens, haakjes, spaties, komma's, een tweede `@` of de reeks `=?`, maak het domein canoniek volgens INV-53, en ken rechten, tenant of korting pas toe op basis van het domein nadat het adres is bevestigd (Zie AUTH voor e-mailverificatie) en zoals de mailserver het heeft afgeleverd.
- Bewijs: Unit-test op het gedeelde e-mailschema met `"a@kwaad.nl"@goed.nl`, `a(x)@goed.nl`, `=?x?q?=41?=@goed.nl`, `a@b.nl,c@d.nl`, `a @goed.nl` en `a@goed.nl\n`: alle geweigerd. `grep -rnE "endsWith\('@|split\('@'\)" src`: elke treffer werkt op een bevestigd, canoniek adres. Afgevinkt met test en grep. Zie WEB-69 en AUTH-47.
- Norm: ASVS 5.0.0 V1.5.3 (L3), V2.2.1 (L1), V2.1.1 (L1).
- Zie ook: MSG-18, WEB-69, AUTH-47
