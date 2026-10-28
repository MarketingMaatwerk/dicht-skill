<!--
Sjabloon: threat model in vier vragen, in maximaal vijftien minuten, voor de eerste regel code.
Dekt: ARCH-80, ARCH-81 (wanneer herzien), ARCH-82 (misbruikgevallen bij geld of limieten)
De vorm is letterlijk die uit ARCH-80. Plek: docs/threat-model.md.
Aanpassen: de schets, de grenzen en de top vijf. Elke maatregel is een regel-ID uit de skill.
Herzien bij elke nieuwe ingang of grens (ARCH-81).
Controleren: het bestand bestaat voor de eerste commit met code; elke dreiging in de top vijf heeft een regel-ID
  en een bewijs; wat bewust is geaccepteerd staat in docs/uitzonderingen.md (ARCH-30).
Haal dit commentaarblok weg in het echte bestand.
-->
# Threat model <project> (<datum>, <wie>)

## 1. Waar werken we aan?

Schets: browser -> nginx -> API -> Postgres; API -> Mollie; mail-in -> worker -> model

- Gegevens: <welke, hoe gevoelig>
- Grenzen: internet|nginx, API|database, API|externe dienst, mail|model

## 2. Wat kan er misgaan?

Per grens de zes categorieen van STRIDE.

| Grens | Spoofing | Tampering | Repudiation | Information disclosure | Denial of service | Elevation of privilege |
|---|---|---|---|---|---|---|
| internet / nginx | | | | | | |
| API / database | | | | | | |
| API / externe dienst | | | | | | |
| mail / model | | | | | | |

## 3. Wat doen we eraan?

| # | Dreiging | Maatregel (regel-ID) | Bewijs |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

Misbruikgevallen bij een stroom met geld of limieten (ARCH-82):

## 4. Goed genoeg?

- Bewust geaccepteerd (ARCH-30, met ID uit docs/uitzonderingen.md):
- Wanneer herzien:
