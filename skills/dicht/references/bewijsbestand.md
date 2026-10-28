# Het bewijsbestand (ARCH-52, ARCH-53)

Eén vorm voor alle projecttypes. Een auditscript leest het later (ARCH-84).

## Plek en naam

- `bewijs/<jjjj-mm-dd>-<korte hash>.md` in de repository van het project. Grote uitvoer in een map met dezelfde naam ernaast.
- Buiten de webroot. Bij een WordPress-plugin of -thema niet in het zip-bestand.
- Eén bestand per oplevering, per uitrol en per wijziging. Een bestand wordt nooit achteraf gewijzigd; een herstel krijgt een nieuw bestand. Het voorgevulde bestand van een wijziging (`tools/regels_voor_wijziging.py --bewijs`) vul je in tot de klaar-melding; daarna geldt hetzelfde.
- Geen geheimen, geen persoonsgegevens, geen volledige logregels van productie. De geheimscan draait ook op `bewijs/`.

## Kop

```
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
pad: <volledig | gewoon | klein>
basis: <commit waartegen de wijziging is gemeten; alleen bij gewoon of klein, mag weg op een eigen branch>
---
```

`pad` en `basis` zijn erbij gekomen met het pad voor een wijziging (besluit 27, 04-10-2026). Een bestand zonder `pad` telt als `volledig`; oudere bestanden blijven dus geldig. De kolommen en de statussen zijn niet gewijzigd.

## Lijf

Bij `pad: volledig` één tabel per sub-skill, met elk punt van de checklist van het projecttype. Bij `pad: gewoon` of `pad: klein` één tabel met alleen de regels die `tools/regels_voor_wijziging.py` kiest (`references/kleine-wijziging.md`); een regel die het pad niet kiest hoort er niet in. Het hulpmiddel schrijft dat bestand voor: `nvt` met reden voor een regel die de wijziging niet raakt, de rest leeg.

```
| Regel | Status | Bewijs |
|---|---|---|
| ARCH-24 | voldaan | /health version=1a2b3c4, git rev-parse=1a2b3c4 |
| AUTH-77 | voldaan | bewijs/2026-10-04-1a2b3c4/isolatie.txt (42 geslaagd, 0 mislukt) |
| WEB-11 | nvt | geen HTML-respons in deze dienst |
| DB-60 | uitzondering | U-003, verloopt 2027-01-01 |
| ARCH-44 | niet gemeten | mutatietest nog niet gedraaid |
```

## Status

| Status | Betekenis | Telt als afgevinkt |
|---|---|---|
| `voldaan` | het bewijs uit de regel is geleverd: letterlijke uitvoer van één regel, of een pad naar een bestand | ja |
| `nvt` | de regel speelt niet in dit project; de reden staat in de kolom Bewijs | ja, alleen met reden |
| `uitzondering` | Marketing Maatwerk heeft de regel overruled; verwijzing naar het register en de verloopdatum | ja, tot de verloopdatum |
| `niet gemeten` | niet getoetst, of een controle die door iets werd verborgen | nee |

In een bestand van een wijziging betekent `nvt`: deze wijziging raakt de regel niet, met de reden per regel. `voldaan` mag daar verwijzen naar een eerder bewijsbestand als de wijziging het bewijs niet verandert.

`niet gemeten` is nooit `voldaan`. Een lege status, een onbekende status en een uitkomst ONBEKEND van een auditscript tellen als niet afgevinkt. Een taak met een leeg punt of een `niet gemeten` is niet klaar; meld dan letterlijk wat ontbreekt.

## Controle van het bestand zelf

1. Het bestand van de laatste uitrol bestaat.
2. De commit erin is gelijk aan de commit die draait (ARCH-24).
3. Elk punt van de checklist komt erin voor (volledig), of elke regel die het pad kiest (gewoon en klein). Met een profiel telt een regel in een domein of thema dat daar met reden op `nvt` staat als afgevinkt (`references/intake.md`).
4. Een geheimscan op `bewijs/` is schoon.
