---
name: dicht-scripts
description: Regels met bewijs voor Bash- en Python-scripts (strikte modus, quoting, tijdelijke bestanden, sloten, geheimen, shellcheck en ruff, cron en timers, monitors en lussen, scripts die versturen of verwijderen of een terminal of AI-sessie aansturen). Niet voor Node of PHP (dicht-api).
---

# dicht-scripts: scripts en automatisering

Sub-skill van `dicht` (batch 4, besluit 26). Bevat de 51 regels van domein SCR in elf thema's. Geldt zodra een script in cron, in een timer, in een uitrol of in een andere sessie draait; een script van drie regels dat je één keer met de hand draait valt erbuiten. Vijf regels (SCR-44 tot en met SCR-47 en SCR-49) dragen de markering `eigen bron`: de uitwerking komt uit eigen incidenten en de eigen verzendlijnen.

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/scr-a-bash-strikte-modus-en-foutafhandeling.md` | SCR-01 t/m SCR-05 (5 actief) | Bash, strikte modus en foutafhandeling |
| `references/scr-b-bash-quoting-en-injectie.md` | SCR-06 t/m SCR-13 (8 actief) | Bash, quoting en injectie |
| `references/scr-c-bestanden-tijdelijke-bestanden-verwijderen-en-re.md` | SCR-14 t/m SCR-17 (4 actief) | Bestanden, tijdelijke bestanden, verwijderen en rechten |
| `references/scr-d-sloten-en-gelijktijdigheid.md` | SCR-18 (1 actief) | Sloten en gelijktijdigheid |
| `references/scr-e-geheimen-in-scripts.md` | SCR-19 t/m SCR-20 (2 actief) | Geheimen in scripts |
| `references/scr-f-code-en-data-van-buiten-en-de-gate-voor-scripts.md` | SCR-21 t/m SCR-23 (3 actief) | Code en data van buiten, en de gate voor scripts |
| `references/scr-g-python-scripts.md` | SCR-24 t/m SCR-36 (13 actief) | Python-scripts |
| `references/scr-h-cron-en-systemd-timers.md` | SCR-37 t/m SCR-41 (5 actief) | Cron en systemd-timers |
| `references/scr-i-lange-lussen-en-monitors.md` | SCR-42 t/m SCR-44 (3 actief) | Lange lussen en monitors |
| `references/scr-j-scripts-die-versturen-of-verwijderen.md` | SCR-45 t/m SCR-47, SCR-52 t/m SCR-53 (5 actief) | Scripts die versturen of verwijderen |
| `references/scr-k-scripts-die-een-terminal-of-een-ai-agent-aanstur.md` | SCR-48 t/m SCR-51 (4 actief) | Scripts die een terminal of een AI-agent aansturen |

## Wanneer niet

- Node en PHP: processen zonder shell (API-53), SQL met parameters (DB-25), deserialisatie (API-55): `dicht-api` en `dicht-database`. Hier staat alleen de Bash- en Python-kant.
- De sandbox van een unit, rechten op scripts en het slot met foutmelding per geplande taak (INFRA-67, INFRA-69, INFRA-70): `dicht-infra`, thema H.
- Archieven, YAML en afbeeldingen als formaat (grenzen, symlinks, bommen): `dicht-invoer`. Hier staan de Python-aanroepen.
- Prompt-injectie, agentrechten en menselijke goedkeuring: `dicht-ai-mcp`. Hier staat het mechaniek van aansturen via tmux en standaardinvoer.
- Bounces, afmelden en afzenderreputatie van een verzendlijn: `dicht-berichten`. Dubbele incasso en inhalen als bedrijfsregel: `dicht-api`, thema's BIZ.

## Verhouding tot bestaande skills

Geen van de bestaande skills gaat over shell- of Python-scripts als productiecode: een zoekopdracht in de `SKILL.md` van elke skill op `shellcheck`, `set -euo`, `crontab` en `subprocess` gaf op 04-10-2026 geen treffers (alleen de `SKILL.md`-bestanden zijn doorzocht, niet hun bijlagen). `secrets-management` gaat over CI-geheimen, niet over geheimen in argumenten en omgeving (SCR-19, SCR-20).
