---
name: dicht
description: Harde werkwijze met bewijs voor elke bouw- of codetaak (website, WordPress-plugin of -thema, API, app, MCP-server, script, configuratie, infrastructuur, klantproject). Bepaalt het projecttype, laadt checklist en sub-skills, eist bewijs per regel. Niet bij alleen tekst, mail of offertes.
---

# dicht

Alles wat we bouwen is veilig, correct en aantoonbaar gecontroleerd. Hard met bewijs: een bouwtaak is pas klaar als de checklist van het projecttype is afgevinkt (ARCH-52).

## Werkwijze

1. **Bepaal het projecttype** (één of meer, zie tabel) en noem het hardop. Twijfel: vraag het.
2. **Laad de checklist** `checklists/<type>.md` (groot: lees per fase) en elke sub-skill waarvan de trigger afgaat. Nieuw project: altijd ook `dicht-privacy` en `dicht-architectuur`: leg het ASVS-niveau vast (PRIV-59), maak het threat model (ARCH-80) en werk het register bij (PRIV-03).
3. **Bouw per fase** (ontwerp, bouwen, vóór oplevering, beheer). Lees bij elk punt de regel in de referentie van de sub-skill: daar staat het volledige bewijs.
4. **Draai de poorten** (hieronder). Een rode poort wordt opgelost, niet overgeslagen.
5. **Schrijf het bewijs** in `bewijs/<jjjj-mm-dd>-<korte hash>.md` volgens `references/bewijsbestand.md`: per regel-ID de status (`voldaan`, `nvt` met reden, `uitzondering`, `niet gemeten`) en de letterlijke uitvoer of een pad.
6. **Meld pas klaar** als geen punt leeg of `niet gemeten` is. Anders: zeg letterlijk wat niet is getoetst en waarom.

## Wijziging aan een bestaand project

Draai `tools/regels_voor_wijziging.py --bewijs`: het kiest uit de diff en `.dicht/profiel.json` (repo-root, `references/intake.md`) de regels en vult het bewijsbestand voor. Bewijs alleen die, elk met bewijs of `nvt` met reden; uitzonderingen gelden onverkort. Nieuw project, oplevering of geen profiel: de hele checklist. Zie `references/kleine-wijziging.md`.

## Overrulen

Alleen Marketing Maatwerk kan een harde regel overrulen, expliciet en per regel. Leg het vast in `docs/uitzonderingen.md` volgens `references/uitzonderingen.md`: regel-ID, datum, reden, verloopdatum, vervangende maatregel. Een overgeslagen stap (`--no-verify`, `SKIP_TESTS`, een uitgezette scan) is ook een uitzondering (ARCH-30). Verlopen is niet afgevinkt.

## Projecttypes

| Type | Wat |
|---|---|
| `website` | statische site of WordPress-site zonder eigen code |
| `wp-plugin` | eigen plugin of mu-plugin |
| `wp-thema` | eigen thema of maatwerk in een thema |
| `api` | HTTP-API of backend-dienst (Fastify, PHP) |
| `app` | applicatie met login en gegevens (CRM, portaal, bestelstraat) |
| `mcp` | MCP-server of agent met tools |
| `klantproject` | werk op een site of systeem van een klant |

## Poorten

Eén opdracht, lokaal en in CI dezelfde, die gesloten faalt (GIT-57, GIT-58, GIT-59):

1. lint en opmaak
2. typecheck of statische analyse (`tsc --noEmit`, PHPStan, PHPCS)
3. tests: unit en integratie; e2e met echte klikken (Playwright)
4. scans: geheimscan, afhankelijkheden-audit, SAST; waar het speelt workflow-lint, Dockerfile- en image-scan

Vóór een oplevering daarbij: isolatie- en autorisatietests (ARCH-40), mutatietest op kritieke delen (ARCH-44), passieve ZAP-scan (GIT-64), voor websites toegankelijkheid en Core Web Vitals (ARCH-46, ARCH-74).

## Sub-skills en triggers

| Sub-skill | Laad bij |
|---|---|
| `dicht-web` | HTML-uitvoer, headers, CSP, cookies, formulieren, uploads, CORS, redirects, caching |
| `dicht-wordpress` | plugin, thema, WooCommerce, Elementor, werk op een WordPress-site |
| `dicht-api` | API-route, backend-code, login, sessie, token, OAuth, rollen, tenant, webhook, Mollie, geld, btw, voorraad, quotum |
| `dicht-database` | schema, migratie, RLS, rollen, query, back-up, Drizzle |
| `dicht-infra` | VPS, Docker, nginx, TLS, DNS, mail, systemd, geheimen, deploy, incident |
| `dicht-git` | repo, worktree, CI, Actions, nieuwe dependency, image, release, publicatie |
| `dicht-ai-mcp` | modelaanroep, prompt, agent, tool, MCP, RAG |
| `dicht-privacy` | persoonsgegevens, cookies, mail aan derden, zorgdata, betalen, toegankelijkheid |
| `dicht-architectuur` | nieuw project, tests, uitrol, logging, bewaking, bewijs |
| `dicht-scripts` | Bash- of Python-script, cron, timer, monitor, lus, bulkactie, aansturen van een sessie |
| `dicht-invoer` | bestand of formaat inlezen, omzetten of maken (XML, JSON, YAML, CSV, HTML, SVG, beeld, PDF, archief), Unicode, URL's |
| `dicht-berichten` | mail versturen of lezen, verzendlijn, afmelden, WhatsApp, Discord, Slack, push |
| `dicht-anti-vibe` | voorkant (thema, sjabloon, CSS, JS, HTML) en oplevering van een website, wp-thema of klantproject |

## Vaste waarden en voorrang

De besluiten van Marketing Maatwerk als getallen: `references/vaste-waarden.md`. Kritieke delen (betaling, login, tenant-isolatie) volgen ASVS 5.0.0 niveau 3, de rest niveau 2. Bij tegenspraak met een oudere skill wint `dicht`. Waarom, voorbeeld en bron per regel-ID: `research/`, via `regel-index.tsv`.
