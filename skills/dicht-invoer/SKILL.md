---
name: dicht-invoer
description: Regels met bewijs voor bestanden en formaten van buiten (XML, JSON, YAML, CSV, HTML en Markdown, SVG en afbeeldingen, PDF, archieven, import en export, Unicode, URL's en e-mailadressen). Niet voor de uploadroute zelf (dicht-web) of algemene API-validatie (dicht-api).
---

# dicht-invoer: invoer en bestandsformaten

Sub-skill van `dicht` (batch 4, besluit 26). Bevat de 69 regels van domein INV in veertien thema's. Begint waar de algemene regels al gelden (schema aan elke rand, uploadlimieten, SSRF-controle) en noemt per bibliotheek de standaardwaarde, de ondergrens van de versie en de aanval. Ondergrenzen op 04-10-2026: Fastify 5.12.5 (INV-15), `@fastify/multipart` 10.1.1 (INV-65), fast-xml-parser 5.10.1 of 4.5.7 (INV-03); werk ze bij binnen de hersteltermijnen van GIT-77.

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/inv-a-xml.md` | INV-01 t/m INV-07 (7 actief) | XML |
| `references/inv-b-json-querystrings-en-formuliervelden.md` | INV-08 t/m INV-15 (8 actief) | JSON, querystrings en formuliervelden |
| `references/inv-c-yaml-en-toml.md` | INV-16 t/m INV-18 (3 actief) | YAML en TOML |
| `references/inv-d-csv-en-spreadsheets.md` | INV-19 t/m INV-21 (2 actief) | CSV en spreadsheets |
| `references/inv-e-html-en-markdown-opschonen.md` | INV-22 t/m INV-26 (5 actief) | HTML en Markdown opschonen |
| `references/inv-f-svg-en-afbeeldingen.md` | INV-27 t/m INV-34 (8 actief) | SVG en afbeeldingen |
| `references/inv-g-pdf-maken-en-lezen.md` | INV-35 t/m INV-40 (6 actief) | PDF maken en lezen |
| `references/inv-h-archieven-en-compressie.md` | INV-41 t/m INV-45 (5 actief) | archieven en compressie |
| `references/inv-i-mass-assignment-in-php-en-wordpress.md` | INV-46 t/m INV-47 (2 actief) | mass assignment in PHP en WordPress |
| `references/inv-j-http-koppen-en-regeleinden.md` | INV-48 t/m INV-50 (3 actief) | HTTP-koppen en regeleinden |
| `references/inv-k-unicode.md` | INV-51 t/m INV-58 (8 actief) | Unicode |
| `references/inv-l-url-s-en-paden-ontleden.md` | INV-59 t/m INV-62 (4 actief) | URL's en paden ontleden |
| `references/inv-m-zoekpatronen-en-e-mailadressen.md` | INV-63 t/m INV-64 (2 actief) | zoekpatronen en e-mailadressen |
| `references/inv-n-multipart-en-tijdelijke-bestanden.md` | INV-65 t/m INV-69 (5 actief) | multipart en tijdelijke bestanden |

## Wanneer niet

- De basis van een upload (allowlist van typen, eigen naam, opslag buiten de webroot, uitleveren als download, malwarescan): `dicht-web`, WEB-43 tot en met WEB-49, en API-60.
- Schema-validatie, onbekende velden en decodeervolgorde in het algemeen: `dicht-api` (API-01, API-02, API-07). Mass assignment in TypeScript: API-02 en AUTH-65.
- SSRF en redirects: WEB-40, WEB-41, API-48. Koppen in uitgaande mail: WEB-68.
- `tarfile`, `zipfile`, `yaml.load` en pickle in Python: `dicht-scripts`.
- Mailparsers, MIME-bommen en HTML-mail in een webweergave: `dicht-berichten`.
- Onzichtbare tekens in invoer voor een model: `dicht-ai-mcp` (AI-07).

## Verhouding tot bestaande skills

`owasp-security`, `api-security-best-practices` en `nodejs-backend-patterns` blijven bruikbaar voor voorbeeldcode; ze noemen de bibliotheekstandaarden en versies uit dit domein niet (vastgesteld in de inleiding van het onderzoek).
