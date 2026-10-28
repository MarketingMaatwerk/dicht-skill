# WP C: Database

Compacte regels van `dicht-wordpress`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/wordpress.md` (regelnummer in `regel-index.tsv`).

### WP-16 Bouw elke query met een variabele via $wpdb->prepare, met kale placeholders
kritiek · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet elke waarde in een SQL-query via `$wpdb->prepare()` met `%d`, `%f` of `%s` zonder aanhalingstekens eromheen, gebruik `%i` voor een tabel- of kolomnaam (sinds WordPress 6.2), en gebruik waar het kan `$wpdb->insert()`, `update()` en `delete()` of de WordPress-API (`WP_Query`, meta, opties) in plaats van eigen SQL.
- Bewijs: `phpcs --sniffs=WordPress.DB.PreparedSQL,WordPress.DB.PreparedSQLPlaceholders .` is groen zonder `phpcs:ignore` op regels met invoer; een test die per parameter `'` en `1 OR 1=1` instuurt en geen databasefout en geen extra rijen terugkrijgt. Afgevinkt met phpcs en testuitvoer.
- Norm: ASVS 5.0.0 V1.2.4 (L1); OWASP Top 10 2025 A05 Injection.
- Zie ook: DB-25, DB-26, DB-27, WP-18, WP-19, DB-28, SCR-11, SCR-30, INV-63

### WP-17 Geef LIKE-patronen door als argument met esc_like
middel · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw een LIKE-patroon in PHP met `$wpdb->esc_like()` om de zoekterm, zet de jokertekens er daar omheen en geef het geheel als `%s` aan `prepare()`.
- Bewijs: `grep -rn "LIKE" --include=*.php .` toont alleen `LIKE %s` met een variabele die uit `esc_like()` komt; een test met de zoektermen `%` en `_` geeft alleen rijen die dat teken letterlijk bevatten. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V1.2.4 (L1).

### WP-18 Kies sorteerkolom en richting uit een vaste lijst
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Vertaal een sorteerveld en een sorteerrichting uit de aanvraag via een allowlist naar een vaste kolomnaam en naar `ASC` of `DESC`, en zet nooit de invoer zelf in `ORDER BY`.
- Bewijs: `grep -rnE "ORDER BY .*\\$" --include=*.php .`: elke variabele komt aantoonbaar uit een allowlist; een test met `orderby=id;SELECT SLEEP(5)` geeft de standaardsortering en geen vertraging. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V1.2.4 (L1), V2.2.1 (L1).
- Zie ook: DB-25, DB-26, DB-27, WP-16, WP-19, DB-28, SCR-11, SCR-30, INV-63

### WP-19 Bouw een IN-lijst met gegenereerde placeholders
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak voor `IN ( ... )` evenveel `%d` of `%s` als er waarden zijn en geef de waarden als argumenten aan `prepare()`; zet nooit een samengevoegde string in de query.
- Bewijs: `grep -rnE "IN \(\s*(\{?\\$|'?\s*\.)" --include=*.php .` is leeg of elke treffer bevat alleen de placeholder-string; een lege lijst wordt vóór de query afgevangen (anders ontstaat `IN ()`, een SQL-fout). Afgevinkt met grep en een test met een lege en een gemanipuleerde lijst.
- Norm: ASVS 5.0.0 V1.2.4 (L1).
- Zie ook: DB-25, DB-26, DB-27, WP-16, WP-18, DB-28, SCR-11, SCR-30, INV-63

### WP-20 Valideer ook wat je aan WP_Query en andere kernfuncties geeft
hoog · hard · wp-plugin | wp-thema | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef invoer nooit ongecontroleerd door als argument aan `WP_Query`, `get_posts()`, `get_users()` of `WP_Meta_Query`: zet getallen om met `absint()`, kies sleutels en vergelijkingsoperatoren uit een vaste lijst, en geef nooit een hele array uit de aanvraag door.
- Bewijs: `grep -rnE "(WP_Query|get_posts|get_users|WP_User_Query)\(" .`: bij elke aanroep is elk argument een vaste waarde, een gecast getal of een waarde uit een allowlist. Afgevinkt met de nagelopen lijst.
- Norm: ASVS 5.0.0 V1.2.4 (L1), V2.2.1 (L1), V15.3.3 (L2).

### WP-21 Geef eigen tabellen en opties een prefix en ruim ze op bij verwijderen
laag · richtlijn · wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Noem eigen tabellen `{$wpdb->prefix}<plugin>_<naam>`, geef opties, hooks, functies en klassen een eigen voorvoegsel of namespace, en verwijder eigen tabellen, opties en geplande taken in `uninstall.php`.
- Bewijs: `grep -rn "wp_" --include=*.php . | grep -E "FROM|INTO|UPDATE|JOIN"` toont geen hardgecodeerd prefix; een test op een schone installatie: installeren, gebruiken, verwijderen, daarna `wp db tables` en `wp option list --search='<prefix>*'` zijn leeg. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V14.1.1 (L2) voor het kennen van de opgeslagen gegevens. Zie DB-83.
