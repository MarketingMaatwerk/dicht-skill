<!--
Sjabloon: bewijsbestand, een per oplevering en per uitrol.
Dekt: ARCH-52, ARCH-53, ARCH-30 (de verwijzing naar het register), ARCH-24, GIT-68, GIT-67
Bron van de vorm: skill/dicht/references/bewijsbestand.md en ARCHITECTUUR.md paragraaf 5.
Plek en naam: bewijs/<jjjj-mm-dd>-<korte hash>.md in de repository van het project; grote uitvoer in een map met
  dezelfde naam ernaast. Buiten de webroot; bij een WordPress-plugin of -thema niet in het zip-bestand.
Aanpassen: de kop, en per sub-skill een tabel met elk punt uit de checklist van het projecttype
  (skill/dicht/checklists/<type>.md). De rijen hieronder zijn voorbeelden van de vier statussen; vervang ze.
Regels:
  - Een bestand wordt nooit achteraf gewijzigd; een herstel krijgt een nieuw bestand.
  - Geen geheimen, geen persoonsgegevens, geen volledige logregels van productie. De geheimscan draait ook op bewijs/.
  - Status is voldaan, nvt, uitzondering of niet gemeten. nvt zonder reden telt als niet afgevinkt.
    niet gemeten is nooit voldaan: een taak met een leeg punt of een niet gemeten is niet klaar.
  - Bewijs is de letterlijke uitvoer van een regel, of een pad naar een bestand.
Controleren: python3 controleer-bewijs.py bewijs/<bestand>.md [docs/uitzonderingen.md] geeft exitcode 0; de commit
  in de kop is gelijk aan de commit die draait (ARCH-24); een geheimscan op bewijs/ is schoon.
Haal dit commentaarblok weg in het echte bestand.
-->
---
project: <naam>
type: <website | wp-plugin | wp-thema | api | app | mcp | klantproject>
commit: <korte hash>
datum: <UTC, ISO 8601>
door: <wie>
akkoord: <wie en wanneer, verplicht als er uitzonderingen zijn>
runtime: <versies van Node, PHP, PostgreSQL, WordPress>
hulpmiddelen: <naam en versie, volgens GIT-68>
gate: <opdracht en exitcode>
uitzonderingen: <ID's uit docs/uitzonderingen.md, of "geen">
---

## dicht-architectuur

| Regel | Status | Bewijs |
|---|---|---|
| ARCH-24 | voldaan | /health/ready version=1a2b3c4, git rev-parse --short HEAD=1a2b3c4 |
| ARCH-44 | niet gemeten | mutatietest nog niet gedraaid |

## dicht-api

| Regel | Status | Bewijs |
|---|---|---|
| AUTH-77 | voldaan | bewijs/2026-10-04-1a2b3c4/isolatie.txt (42 geslaagd, 0 mislukt) |

## dicht-web

| Regel | Status | Bewijs |
|---|---|---|
| WEB-11 | nvt | geen HTML-respons in deze dienst |

## dicht-database

| Regel | Status | Bewijs |
|---|---|---|
| DB-60 | uitzondering | U-003, verloopt 2027-01-01 |

## Openstaand

<Elk punt met "niet gemeten" of een leeg bewijs, letterlijk wat ontbreekt. Zolang hier iets staat is de taak niet klaar (ARCH-52).>
