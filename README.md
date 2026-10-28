# dicht

**English summary.** `dicht` is a skill set for Claude Code that makes every build task (website, WordPress plugin or theme, API, app, MCP server, script, infrastructure) follow a fixed checklist with evidence per rule. It consists of a core skill and 13 sub-skills (web, WordPress, API, database, infra, git, AI/MCP, privacy, architecture, scripts, input formats, messaging, delivery checks), hooks that block dangerous commands and refuse code edits until the skill is loaded, an audit script per project type, and templates. The rules are written in Dutch. Install with `./installeer.sh`; see the sections below for hooks and usage. Owner-specific parts (research notes, evidence files, audits, private exceptions) are left out of this public export. License: MIT, with third-party quotations listed in `THIRD-PARTY.md`.

## Wat is dicht

Een harde werkwijze met bewijs voor elke bouw- of codetaak. Bij de start van een taak bepaalt Claude het projecttype (`website`, `wp-plugin`, `wp-thema`, `api`, `app`, `mcp`, `klantproject`), laadt de checklist van dat type en de sub-skills waarvan de trigger afgaat, en schrijft per regel-ID het bewijs in `bewijs/<jjjj-mm-dd>-<korte hash>.md`. Een taak is pas klaar als geen punt leeg of `niet gemeten` is. Zie `skills/dicht/SKILL.md`.

| Map | Wat |
|---|---|
| `skills/dicht/` | de kern: `SKILL.md`, checklists per projecttype, referenties (bewijsbestand, intake, kleine wijziging, uitzonderingen, vaste waarden) |
| `skills/dicht-*/` | de 13 sub-skills, elk met `SKILL.md` en de regels per thema in `references/` |
| `skills/dicht/hooks/` | de hooks voor Claude Code, de git pre-commit-hook en hun tests |
| `skills/dicht/audit/` | het auditscript per projecttype (alleen lezen) en de tests |
| `skills/dicht/tools/` | `regels_voor_wijziging.py`: kiest bij een wijziging de regels uit de diff en het profiel |
| `skills/dicht/sjablonen/` | gevalideerde sjablonen (nginx, Docker, systemd, scripts, CI, database, TypeScript, API, WordPress, bewijs, berichten) |
| `skills/dicht/installatie/` | `gitleaks-installeren.sh`: optionele tweede geheimscan |
| `commands/dicht-audit.md` | het commando `/dicht-audit` |

## Vereisten

- Claude Code, bash, git en Python 3 (getest met Python 3.10). De hooks, de audit en het hulpmiddel gebruiken de standaardbibliotheek; de audit gebruikt PyYAML als het er is, voor de controles op Compose-bestanden (zonder PyYAML is die uitkomst "onbekend").
- Optioneel: gitleaks voor de geheimscan (`skills/dicht/installatie/gitleaks-installeren.sh`, Linux x86_64, met een vaste checksum). Zonder gitleaks gebruikt de scan alleen de eigen patronen.
- Optioneel: Playwright voor Python met Chromium, voor de oplevercontrole `dicht-anti-vibe/scripts/vibe_meet.py` en de test daarvan (`pip install playwright` en `playwright install chromium`).

## Installeren

```
./installeer.sh                  # naar ~/.claude
python3 ~/.claude/skills/dicht/hooks/test_hooks.py | tail -1     # verwacht: 0 fout(en)
python3 ~/.claude/skills/dicht/audit/test_audit.py | tail -1     # verwacht: 0 fout(en)
```

Installeer naar `~/.claude`: de geheimscan, `gitleaks-installeren.sh` en `/dicht-audit` gaan van die plek uit (`DOEL=/pad ./installeer.sh` zet de skills elders neer, maar dan wijzen die drie nog naar `~/.claude`). Het script kopieert de kern, de sub-skills en het commando, overschrijft niets (staat er al een map `dicht*`, dan stopt het) en wijzigt geen instellingen. In `hooks/settings-voorbeeld.json` vult het de paden van de installatie in. Verwijderen: haal de mappen `~/.claude/skills/dicht*` en `~/.claude/commands/dicht-audit.md` weg, en eerst de hooks uit de instellingen.

## Gebruik

- **Bouwtaak.** Vraag Claude Code om de skill `dicht` te laden en het projecttype te noemen; de skill zegt welke sub-skills erbij horen. Met de hooks aan (hieronder) gebeurt dat afgedwongen.
- **Profiel per project.** Een project krijgt `.dicht/profiel.json` in de repo-root volgens `skills/dicht/references/intake.md`. Controle: `python3 ~/.claude/skills/dicht/tools/regels_voor_wijziging.py --controleer-profiel`.
- **Kleine wijziging.** In de repo-root: `python3 ~/.claude/skills/dicht/tools/regels_voor_wijziging.py --bewijs` kiest de regels voor de diff en vult het bewijsbestand voor.
- **Audit.** `/dicht-audit <type>` in Claude Code, of rechtstreeks `~/.claude/skills/dicht/audit/audit-<type> --pad .`. De audit leest alleen en schrijft een bewijsbestand; exitcode 1 betekent dat een harde regel niet is voldaan, 2 een fout in het script.
- **Uitzonderingen.** De regels noemen Marketing Maatwerk waar de eigenaar beslist (akkoord, overrulen, uitzonderingen verlengen). In je eigen project lees je daar: de eigenaar van het project. Een uitzondering staat per regel, met datum, reden, verloopdatum en vervangende maatregel in `docs/uitzonderingen.md` (`skills/dicht/references/uitzonderingen.md`).

## Hooks

`skills/dicht/hooks/settings-voorbeeld.json` heeft twee blokken. Neem de inhoud over, niet de sleutels `globaal` en `per_project`, en voeg samen met wat er al staat.

| Blok | Waar | Hook | Wat |
|---|---|---|---|
| `globaal` | `~/.claude/settings.json` | `pretool_gevaarlijk.py` (PreToolUse) | weigert gevaarlijke opdrachten (recursief verwijderen buiten het project, geforceerd pushen, `--no-verify`, brede `kill`) met een melding wat wel kan; vraagt nooit om bevestiging |
| | | `pretool_geheimscan.py` (PreToolUse, Bash) | geheimscan op wat een `git commit` vastlegt |
| | | `pretool_verplicht.py` (PreToolUse) | weigert code schrijven in een bouwproject zolang de sessie `dicht` en de sub-skills voor dat bestand niet heeft geladen, of het project geen profiel heeft |
| | | `sessionstart_dicht.py` (SessionStart) | toont in een bouwproject het type, de checklist en de sub-skills van het profiel |
| | | `prompt_verplicht.py` (UserPromptSubmit) | herinnert aan de verplichting bij een bouwwoord, tot de skill is geladen |
| `per_project` | `<repo>/.claude/settings.json` | `stop_bewijs.py` (Stop) | blokkeert een klaar-melding na een codewijziging zolang het bewijsbestand onvolledig is |
| | | `prompt_overrule.py` (UserPromptSubmit) | noodrem: een prompt die begint met `DICHT OVERRULE: <reden>` zet de Stop-hook voor die sessie uit en legt dat vast in `.dicht/overrules.log` |

Elke hook start via een korte `sh`-regel: ontbreekt het script, dan geeft die een melding en blokkeert niets (Claude Code leest exitcode 2 als blokkeren, en `python3` met een pad dat niet bestaat geeft exitcode 2). De hooks weigeren alleen via hun JSON-uitvoer.

`pretool_verplicht.py` laat altijd vrij: tekst- en gegevensbestanden (zoals `.md`, `.txt`, `.csv`) en de mappen `/tmp`, `/dev`, `~/.claude/projects`, `~/docs` en `~/backups` (`VRIJE_MAPPEN` in `hooks/dicht_lib.py`).

De git-hook voor de geheimscan per repo: `ln -s ~/.claude/skills/dicht/hooks/git-pre-commit "$(git rev-parse --git-common-dir)/hooks/pre-commit"` (voeg samen als er al een `pre-commit` is).

## Wat is weggelaten

Dit is een publieke export van een privérepository. Weggelaten zijn: het onderzoek per regel (`research/`, de plek waar `regel-index.tsv` en de verwijzingen "Waarom, voorbeeld en bron" naar wijzen), de werkdocumenten (`OPEN-VRAGEN.md`, `ARCHITECTUUR.md`, de notities en tegenlezingen, de opdracht `BRIEF`), bewijsbestanden en audits van eigen projecten, de correcties op skills van anderen, en de eigen vrijstellingen in de geheimscan. Namen van eigen systemen zijn vervangen door algemene termen (zoals "het CRM"). De besluiten en datums in de regels zijn die van Marketing Maatwerk en gelden voor jouw project pas als je ze zelf overneemt. Van de synthese-notities staat alleen de tabel met broncodes erin (`skills/dicht/SYNTHESE-NOTITIES.md`). Verwijzingen naar weggelaten bestanden kunnen dus niet worden gevolgd.

`dicht-privacy` gaat over wat de wet van de bouw vraagt; het is geen juridisch advies.

## Licentie

MIT, zie `LICENSE`. Korte citaten uit normen en documentatie van derden vallen niet onder die licentie: zie `THIRD-PARTY.md`.
