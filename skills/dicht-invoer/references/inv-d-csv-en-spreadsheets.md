# INV D: CSV en spreadsheets

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-19 → API-59
Samengevoegd: "Neutraliseer formules ook midden in een veld en na een regeleinde" is gedekt door API-59. Gebruik die regel.

### INV-20 Lees een CSV-import strikt: UTF-8, vast scheidingsteken, limieten en een schema per rij
middel · hard · api | app | wp-plugin | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Decodeer een importbestand met `new TextDecoder('utf-8', { fatal: true })`, verwijder een BOM aan het begin, leg het scheidingsteken vast (of laat de gebruiker kiezen) in plaats van te raden, stel een maximum aan rijen, kolommen en celgrootte in, en valideer elke rij met een schema voordat er iets wordt opgeslagen.
- Bewijs: Tests op de importfunctie met vier bestanden: Windows-1252 met een é (geweigerd met een duidelijke melding), UTF-8 met BOM (eerste kolom wordt herkend), limiet plus één rij (geweigerd), en een rij met een ongeldig veld (hele import geweigerd of die rij gemeld, volgens de documentatie van de functie). Afgevinkt met de testuitvoer. Zie ARCH-43 voor het fuzzen van de parser en API-59 voor de export.
- Norm: ASVS 5.0.0 V2.2.1 (L1), V5.2.1 (L1), V1.1.1 (L2).
- Zie ook: API-59

### INV-21 Gebruik het pakket xlsx niet vanaf npm
hoog · hard · api | app | mcp | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Lees geen spreadsheets van buiten met `xlsx` uit het npm-register (0.18.5); kies een onderhouden bibliotheek uit het register, of leg met een uitzondering vast dat SheetJS 0.20.3 of hoger van de eigen bron van de maker komt, met vastgezette integriteit in het lockfile, een reden en een einddatum (de voorwaarden van GIT-73). Beslis het per project (besluit van Marketing Maatwerk, 04-10-2026): de uitzondering op GIT-73 voor SheetJS van het CDN van de maker is toegestaan, met hash, reden en einddatum in het register (ARCH-30).
- Bewijs: `npm ls xlsx` is leeg, of toont 0.20.3 of hoger met een `resolved`-URL naar `cdn.sheetjs.com` en een `integrity`-waarde, plus een vastgelegde uitzondering op GIT-73. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V15.2.1 (L1), V15.2.4 (L3).
- Zie ook: GIT-73
