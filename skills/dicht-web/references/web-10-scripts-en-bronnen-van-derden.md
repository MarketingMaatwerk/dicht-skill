# WEB 10: Scripts en bronnen van derden

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-58 Host scripts, stijlen en lettertypen zelf, of pin ze met SRI
hoog · hard · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Lever JavaScript, CSS en lettertypen vanaf de eigen origin; laad een bron van een externe host alleen als hij statisch en van een vaste versie is, met `integrity` (sha384 of sha512) en `crossorigin="anonymous"`, en leg voor elke uitzondering (betaalscript, kaart, analytics) een besluit vast.
- Bewijs: Een Playwright-run die per paginatype alle geladen hosts logt; elke host buiten de eigen origin staat in de lijst van besluiten, en elke externe `<script>` en `<link rel="stylesheet">` in de HTML heeft `integrity` (`curl -s <url> | grep -oE '<script[^>]+src="https?://[^"]+"[^>]*>' | grep -v integrity` is leeg op de uitzonderingen na). Afgevinkt met de hostlijst en de grep.
- Norm: ASVS 5.0.0 V3.6.1 (L3; hard omdat de aanval alle bezoekers raakt en de maatregel goedkoop is); OWASP Top 10 2025 A03 Software Supply Chain Failures en A08 Software or Data Integrity Failures.
- Zie ook: WEB-11, AI-14, PRIV-85, PRIV-19, WEB-59, PRIV-46, PRIV-40, PRIV-84

### WEB-59 Houd een lijst van derde partijen bij en stuur ze geen gevoelige data
middel · hard · website | wp-thema | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per project vast welke externe hosts de browser aanroept en waarom, laad geen tracker of script van derden op pagina's met login, betaling, wachtwoordherstel of gezondheidsgegevens, en geef geen persoonsgegevens mee in URL's of gebeurtenissen naar derden.
- Bewijs: De hostlijst uit WEB-58 per paginatype; de pagina's voor login, afrekenen, reset en account laden nul hosts van derden behalve de genoteerde betaalprovider; de CSP `connect-src` en `script-src` passen bij de lijst. Bij een nieuwe derde partij is `policy-state.yaml` bijgewerkt (regel van Marketing Maatwerk, zie PRIV). Afgevinkt met de hostlijst.
- Norm: ASVS 5.0.0 V14.2.3 (L2); AVG artikel 28 en 32 (zie PRIV); OWASP Top 10 2025 A03. Wettelijke basis: zie PRIV-19, PRIV-46 (een derde in de browser is een ontvanger).
- Zie ook: PRIV-19, WEB-58, PRIV-46, PRIV-40
