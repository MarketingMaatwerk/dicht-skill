---
name: dicht-anti-vibe
description: Oplevercontrole tegen gevibecodete sites, met bewijs per regel: links, knoppen, formulieren, mobiel menu, scroll, snelheid, SEO en verplichte pagina's. Gebruik bij voorkantwerk en oplevering van een site. Niet voor API of app zonder voorkant.
---

# dicht-anti-vibe: oplevercontrole van een website

Sub-skill van `dicht` (besluit van Marketing Maatwerk, 22-10-2026): 43 regels VIBE, de oplevercontrole uit het eigen websiteproces (stap 9), voor elke website, wp-thema en klantproject. Meten (alleen lezen): `/usr/bin/python3 ~/.claude/skills/dicht-anti-vibe/scripts/vibe_meet.py https://<site>`; formulieren en query's op de testomgeving.

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/vibe-a-inhoud-en-links.md` | VIBE-01 t/m VIBE-09 (9 actief) | Inhoud en links |
| `references/vibe-b-formulieren-knoppen-en-laden.md` | VIBE-10 t/m VIBE-14, VIBE-43 (6 actief) | Formulieren, knoppen en laden |
| `references/vibe-c-mobiel-en-layout.md` | VIBE-15 t/m VIBE-17, VIBE-37 t/m VIBE-42 (9 actief) | Mobiel en layout |
| `references/vibe-d-snelheid.md` | VIBE-18 t/m VIBE-22 (5 actief) | Snelheid |
| `references/vibe-e-vindbaarheid-en-verplichte-pagina-s.md` | VIBE-23 t/m VIBE-33 (11 actief) | Vindbaarheid en verplichte pagina's |
| `references/vibe-f-wordpress.md` | VIBE-34 t/m VIBE-35 (2 actief) | WordPress |
| `references/vibe-g-beheer-en-anti-spam-verwijzing.md` | VIBE-36 (1 actief) | Beheer en anti-spam (verwijzing) |

## Wanneer niet

- API, MCP of app zonder voorkant.
- Beveiliging van de voorkant: `dicht-web`. Beheer, anti-spam en WordPress-blootstelling: VIBE-36 verwijst.
- Keywords, GEO-tekst en de keuze van schema-typen: het eigen websiteproces (stap 9).

## Verhouding tot bestaande skills

`webapp-testing` (Playwright) en `performance` (sneller maken). Hier staat wat bij oplevering aantoonbaar moet kloppen.
