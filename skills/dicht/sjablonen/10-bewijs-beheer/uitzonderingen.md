<!--
Sjabloon: het uitzonderingenregister van een project.
Dekt: ARCH-30, GIT-65, ARCH-55 (de afbakening)
Bron van de vorm: skill/dicht/references/uitzonderingen.md.
Plek: docs/uitzonderingen.md in de repository van het project.
Regels:
  - Alleen Marketing Maatwerk kan een harde regel overrulen, expliciet en per regel.
  - Elke uitzondering heeft een datum, een reden, een verloopdatum en een vervangende maatregel. Voor een
    genegeerde bevinding van een scanner is de verloopdatum hooguit 90 dagen na de datum (GIT-65).
  - Een verlopen uitzondering telt als niet afgevinkt, tot Marketing Maatwerk haar verlengt of de regel alsnog wordt gehaald.
  - Een overgeslagen stap in de gate of de uitrol (SKIP_TESTS=1, --no-verify, continue-on-error, een uitgezette
    scan) is een uitzondering en komt ook in het bewijsbestand.
  - Een onderdrukking in de code met een reden op dezelfde regel (ARCH-55) hoeft niet in het register.
  - Een regel verdwijnt nooit uit het register: een afgesloten uitzondering krijgt in de kolom Reden de
    toevoeging "afgesloten <datum>".
Aanpassen: de rijen. De eerste rij is de vaste uitzondering van besluit 25 en hoort alleen in het register van
  de server; Marketing Maatwerk kiest de verloopdatum en de vervangende maatregel. De tweede rij is een voorbeeld.
Controleren: python3 controleer-bewijs.py <bewijsbestand> docs/uitzonderingen.md meldt elke verlopen of
  onvolledige rij.
Haal dit commentaarblok weg in het echte bestand.
-->
# Uitzonderingen

| ID | Regel | Datum | Door | Reden | Verloopt | Vervangende maatregel |
|---|---|---|---|---|---|---|
| U-001 | INFRA-10, INFRA-66 | 2026-10-04 | Marketing Maatwerk | <waarom de regel hier niet gehaald wordt> | <datum, door Marketing Maatwerk te kiezen> | <door Marketing Maatwerk te kiezen> |
| U-002 | <regel-ID> | <jjjj-mm-dd> | Marketing Maatwerk | <waarom de regel hier niet gehaald wordt> | <jjjj-mm-dd> | <wat het risico in de tussentijd beperkt> |
