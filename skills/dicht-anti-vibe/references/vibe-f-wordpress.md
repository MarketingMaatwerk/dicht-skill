# VIBE F: WordPress

Compacte regels van `dicht-anti-vibe`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/anti-vibe.md` (regelnummer in `regel-index.tsv`).

### VIBE-34 Standaardinhoud en versiebestanden zijn weg
middel · hard · website (WordPress) | wp-thema | klantproject (WordPress) · tegenlezer: niet tegengelezen
- Regel: Het bericht "Hello world!", de pagina "Sample Page" en de standaard-privacypagina zijn weg, en `readme.html` en `license.txt` staan niet in de webroot.
- Bewijs: `vibe_meet.py` regel VIBE-34 (`/hello-world/`, `/sample-page/`, `/readme.html` en `/license.txt` geven geen 200); `wp post list --post_type=post,page --name=hello-world,sample-page,privacy-policy --format=count` is 0. Afgevinkt met beide.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook WP-62 (bekende WordPress-paden bij elke oplevering).
- Bron: website.md Stap 9, W2 (standaardcontent weg).

### VIBE-35 Geen query in een lus in eigen thema- of mu-plugin-code
middel · hard · website (WordPress) | wp-thema | klantproject (WordPress) · tegenlezer: niet tegengelezen
- Regel: Eigen thema- en mu-plugin-code doet geen databasequery per item in een lus (N+1); haal in één query op (`WP_Query` met `post__in`, `update_meta_cache`, een `IN`-lijst met `$wpdb->prepare`). Tel de query's per paginaweergave en leg het aantal vast.
- Bewijs: op de testomgeving met Query Monitor of `define( 'SAVEQUERIES', true )`: het aantal query's per hoofdpagina in het bewijsbestand, en geen herhaalde query met alleen een ander ID. Niet op een live site (de instelling wijzigt de site). Afgevinkt met de getallen.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook WP-19 (`$wpdb->prepare`).
- Bron: website.md Stap 9, A9 (eigen queries, N+1); H paragraaf 3 (N+1-queries, dure queries cachen).
