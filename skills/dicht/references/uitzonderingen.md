# Het uitzonderingenregister (ARCH-30)

Alleen Marketing Maatwerk kan een harde regel overrulen, expliciet en per regel. Elke uitzondering staat in `docs/uitzonderingen.md` van het project.

## Vorm

```
| ID | Regel | Datum | Door | Reden | Verloopt | Vervangende maatregel |
|---|---|---|---|---|---|---|
| U-001 | INFRA-10, INFRA-66 | 2026-10-04 | Marketing Maatwerk | <waarom de regel hier niet gehaald wordt> | <datum> | <door Marketing Maatwerk te kiezen, bijvoorbeeld AI-02 en AI-86 als rem> |
```

## Regels

- Elke uitzondering heeft een verloopdatum. Voor een genegeerde bevinding van een scanner is dat hooguit 90 dagen (GIT-65).
- Een verlopen uitzondering telt als niet afgevinkt, tot Marketing Maatwerk haar verlengt of de regel alsnog wordt gehaald.
- Een overgeslagen stap in de gate of de uitrol (`SKIP_TESTS=1`, `--no-verify`, `continue-on-error`, een uitgezette scan) is een uitzondering en komt ook in het bewijsbestand.
- Een onderdrukking in de code (`@ts-expect-error`, `eslint-disable`, `phpcs:ignore`, `@phpstan-ignore`) heeft een reden op dezelfde regel (ARCH-55) en hoeft niet in het register.
- Het bewijsbestand noemt in de kop de ID's van de uitzonderingen die gelden, en per regel de status `uitzondering` met het ID en de verloopdatum.
