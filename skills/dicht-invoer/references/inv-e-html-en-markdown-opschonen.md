# INV E: HTML en Markdown opschonen

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-22 Saneer als laatste stap en verander de uitvoer daarna niet meer
hoog · hard · website | wp-plugin | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat de sanitizer (Zie WEB-03) de laatste bewerking zijn vóór opslag of weergave: geen zoek-en-vervang, sjabloonvervanging, afkappen, automatisch linken of een tweede HTML-bibliotheek op de gesaneerde uitvoer.
- Bewijs: `grep -rnE "sanitize\([^)]*\)\s*\.(replace|slice|substring|concat)|wp_kses[a-z_]*\([^;]*\)\s*\." src .` is leeg; codereview bevestigt per sanitizer-aanroep dat de uitvoer rechtstreeks naar opslag of de sink gaat. Test: de drie payloads uit WEB-03 door de hele keten (dus tot en met de weergave), niet alleen door de sanitizer. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V1.1.2 (L2), V1.3.1 (L1).
- Zie ook: WEB-03, WP-04, AI-13, WEB-07, INV-23, INV-24, INV-26, MSG-23

### INV-23 Draai DOMPurify op de server alleen met een actuele jsdom
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik DOMPurify in Node alleen met de laatste versie van jsdom, nooit met happy-dom of een andere DOM, en werk beide pakketten samen bij.
- Bewijs: `npm ls dompurify jsdom happy-dom linkedom` toont dompurify en jsdom op de laatste versie (op 04-10-2026: 3.4.16 en 30.1.2) en geen andere DOM in de productie-afhankelijkheden van de sanitizer; Dependabot of Renovate volgt beide. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V1.3.1 (L1), V15.2.1 (L1).
- Zie ook: WEB-03, WP-04, AI-13, WEB-07, INV-22, INV-24, INV-26, MSG-23

### INV-24 Reken niet op de Markdown-renderer voor veiligheid
hoog · hard · website | app | mcp | wp-plugin | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Haal de uitvoer van `marked` altijd door de sanitizer, zet bij markdown-it de optie `html` niet aan, en geef Markdown uit een model, een mail of een klant dezelfde behandeling als HTML van een gebruiker.
- Bewijs: `grep -rnE "marked(\.parse)?\(|markdownit\(|new MarkdownIt\(" src` toont bij elke aanroep van marked een sanitizer eromheen en bij markdown-it geen `html: true`; de Markdown-test uit WEB-07 slaagt. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V1.3.5 (L2), V1.3.1 (L1).
- Zie ook: WEB-03, WP-04, AI-13, WEB-07, INV-22, INV-23, INV-26, MSG-23

### INV-25 Gebruik strip_tags en reguliere expressies niet als sanitizer
hoog · hard · wp-plugin | wp-thema | website | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `strip_tags()`, `preg_replace()` of een eigen filter nooit als bescherming tegen XSS; codeer bij uitvoer (Zie WEB-01, WP-01) of saneer met `wp_kses` of DOMPurify.
- Bewijs: `grep -rnE "strip_tags\(|preg_replace\([^)]*(script|<)" --include=*.php .`: elke treffer staat niet tussen invoer en een HTML-uitvoer, of er volgt een `esc_*`- of `wp_kses`-aanroep op. Afgevinkt met de nagelopen lijst.
- Norm: ASVS 5.0.0 V1.3.1 (L1).
- Zie ook: WEB-01, WP-01, WP-02, WP-03, WEB-06, MSG-17, INV-35

### INV-26 Beperk de sanitizer tot HTML als SVG en MathML niet nodig zijn
middel · richtlijn · website | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Roep DOMPurify aan met `USE_PROFILES: { html: true }` voor inhoud waarin geen SVG of MathML hoort (mail, notities, opmerkingen, modeluitvoer).
- Bewijs: `grep -rn "DOMPurify.sanitize(" src` toont bij elke aanroep een configuratie met `USE_PROFILES` of een eigen korte `ALLOWED_TAGS`; uitzonderingen zijn verklaard. Afgevinkt met de grep.
- Norm: ASVS 5.0.0 V1.3.1 (L1), V1.3.4 (L2).
- Zie ook: WEB-03, WP-04, AI-13, WEB-07, INV-22, INV-23, INV-24, MSG-23
