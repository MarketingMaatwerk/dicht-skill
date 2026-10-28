---
name: dicht-git
description: Regels met bewijs voor git en de toeleverketen (worktree, commit en merge, GitHub en Actions, gates, gelekte geheimen, afhankelijkheden in npm en Composer, Docker-images als afhankelijkheid, releases). Niet voor de inrichting van de server (dicht-infra).
---

# dicht-git: git, GitHub, CI en afhankelijkheden

Sub-skill van `dicht`. Bevat de 106 regels van domein GIT in tien thema's. De worktree-werkwijze van Marketing Maatwerk (één sessie, één worktree, één branch; commit na elke gevalideerde stap; deploy als bewuste merge in de live checkout) is thema A. Vaste waarden: hersteltermijnen 48 uur, 7 dagen, 30 dagen (GIT-77); minimale leeftijd van een versie 7 dagen (GIT-72).

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/git-a-werkwijze-met-git-en-worktrees.md` | GIT-01 t/m GIT-13 (13 actief) | Werkwijze met git en worktrees |
| `references/git-b-github-account-en-toegang.md` | GIT-14 t/m GIT-22 (9 actief) | GitHub-account en toegang |
| `references/git-c-repository-instellingen-en-branch-bescherming.md` | GIT-23 t/m GIT-31 (7 actief) | Repository-instellingen en branch-bescherming |
| `references/git-d-geheimen-in-git-en-herstel-na-een-lek.md` | GIT-32 t/m GIT-40 (8 actief) | Geheimen in git en herstel na een lek |
| `references/git-e-github-actions.md` | GIT-41 t/m GIT-56 (16 actief) | GitHub Actions |
| `references/git-f-gates-en-hulpmiddelen.md` | GIT-57 t/m GIT-68 (11 actief) | Gates en hulpmiddelen |
| `references/git-g-afhankelijkheden-in-npm.md` | GIT-69 t/m GIT-80 (12 actief) | Afhankelijkheden in npm |
| `references/git-h-composer-en-wordpress-plugins-van-derden.md` | GIT-81 t/m GIT-90 (9 actief) | Composer en WordPress-plugins van derden |
| `references/git-i-docker-images-als-afhankelijkheid.md` | GIT-91 t/m GIT-100 (10 actief) | Docker-images als afhankelijkheid |
| `references/git-j-releases-herkomst-sbom-en-licenties.md` | GIT-101 t/m GIT-106 (6 actief) | Releases, herkomst, SBOM en licenties |

## Wanneer niet

- Runtime-hardening van containers en geheimen op de server: `dicht-infra`.
- Wat de tests moeten bewijzen en de vorm van het bewijsbestand: `dicht-architectuur`. GIT-67 is samengevoegd met ARCH-53.
- WordPress-updates op een klantsite: `dicht-wordpress`, thema G.
- De Cyber Resilience Act achter SBOM en meldpunt: `dicht-privacy`, thema M. GIT-30 is samengevoegd met PRIV-72.
- Python-afhankelijkheden (venv, hashes, `pip-audit`), shellcheck en ruff als gate voor scripts: `dicht-scripts` (SCR-23, SCR-32, SCR-35).

## Verhouding tot bestaande skills

Deze regels gaan voor op vier punten:
- `secrets-management` gebruikt `actions/checkout@v4`, `hashicorp/vault-action@v2` en de images `vault:latest` en `trufflesecurity/trufflehog:latest`: verplaatsbare tags. Zie GIT-41 en GIT-91.
- `docker-expert` gebruikt `node:18-alpine` en `gcr.io/distroless/nodejs18-debian11`; Node 18 en 20 zijn einde levensduur en geen voorbeeld pint op digest. Zie GIT-91 en GIT-93.
- `cc-skill-security-review` en `owasp-security` noemen `npm audit` en `npm audit fix` als hele afhankelijkhedenbeleid. Zie GIT-69 tot en met GIT-80.
- Geen van de skills kent de worktree-werkwijze (thema A).
Voor reviews: `requesting-code-review` en `code-review-excellence`.
