---
name: dicht-architectuur
description: Regels met bewijs voor opbouw en kwaliteit (modulegrenzen, configuratie, foutafhandeling, uitrol en terugdraaien, teststrategie, logging, bewaking en alarmering, threat model, bewijsbestand). Gebruik bij elk nieuw project, tests, een uitrolscript en elke oplevering.
---

# dicht-architectuur: architectuur, testen en observability

Sub-skill van `dicht` en kern-aanvulling: de kern verwijst er bij elk nieuw project en elke oplevering naar. Bevat de 87 regels van domein ARCH in dertien thema's. Vaste waarden: mutatietests op kritieke delen minstens 80 procent gedood (ARCH-44); modulaire monoliet als standaard (ARCH-01).

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/arch-a-architectuur-en-modulegrenzen.md` | ARCH-01 t/m ARCH-06 (6 actief) | Architectuur en modulegrenzen |
| `references/arch-b-configuratie-volgens-twaalf-factor.md` | ARCH-07 t/m ARCH-12 (6 actief) | Configuratie volgens twaalf-factor |
| `references/arch-c-fouten-en-veerkracht.md` | ARCH-13 t/m ARCH-21 (8 actief) | Fouten en veerkracht |
| `references/arch-d-uitrol-en-terugdraaien.md` | ARCH-22 t/m ARCH-28, ARCH-87 (8 actief) | Uitrol en terugdraaien |
| `references/arch-e-beslissingen-uitzonderingen-en-schuld-vastleggen.md` | ARCH-29 t/m ARCH-32 (4 actief) | Beslissingen, uitzonderingen en schuld vastleggen |
| `references/arch-f-teststrategie.md` | ARCH-33 t/m ARCH-47 (15 actief) | Teststrategie |
| `references/arch-g-testdata-en-geheimen-in-tests.md` | ARCH-48 t/m ARCH-51 (4 actief) | Testdata en geheimen in tests |
| `references/arch-h-definitie-van-klaar-bewijs-en-review.md` | ARCH-52 t/m ARCH-56 (5 actief) | Definitie van klaar, bewijs en review |
| `references/arch-i-logging-audit-log-health-checks-en-alarmering.md` | ARCH-57 t/m ARCH-72 (16 actief) | Logging, audit-log, health-checks en alarmering |
| `references/arch-j-prestatie-en-beschikbaarheid.md` | ARCH-73 t/m ARCH-75 (3 actief) | Prestatie en beschikbaarheid |
| `references/arch-k-schakelaars-en-api-versies.md` | ARCH-76 t/m ARCH-79 (4 actief) | Schakelaars en API-versies |
| `references/arch-l-threat-modeling-in-vijftien-minuten.md` | ARCH-80 t/m ARCH-83 (4 actief) | Threat modeling in vijftien minuten |
| `references/arch-m-auditscripts-en-de-audit-per-project.md` | ARCH-84 t/m ARCH-86 (3 actief) | Auditscripts en de audit per project |

## Wanneer niet

- Welke scans in de gate zitten en hoe CI is ingericht: `dicht-git`, thema E en F.
- De inhoud van een beveiligingsregel zelf: de sub-skill van dat domein. Deze sub-skill zegt hoe je hem test, uitrolt en bewijst.
- De auditscripts zelf bestaan nog niet (stap 4 van het plan); ARCH-84 beschrijft wat ze moeten doen.

## Verhouding tot bestaande skills

- `javascript-testing-patterns`: patronen voor unit- en integratietests, maar geen mutatietests en geen property-based tests, en het databasevoorbeeld maakt zijn eigen tabel in plaats van de echte migraties en de runtime-rol te gebruiken: ARCH-35 en ARCH-42 tot en met ARCH-45 vullen aan.
- `webapp-testing`: de Playwright-werkwijze. ARCH-36 tot en met ARCH-39 leggen vast wat een e2e-test moet bewijzen en dat echte invoer verplicht is.
- `nodejs-backend-patterns`: gelaagde opbouw en een globale foutafhandelaar. ARCH-01 tot en met ARCH-03 maken de modulegrens afdwingbaar; ARCH-13 tot en met ARCH-21 voegen veerkracht toe.
- `code-review-excellence` en `requesting-code-review`: hoe je reviewt. ARCH-54 legt vast wanneer het moet en wat het bewijs is.
- `performance`: de optimalisaties en een LCP-doel; INP en CLS op het 75e percentiel staan er niet in. ARCH-74 en ARCH-75 leggen de drie drempels vast als controle die kan falen.
