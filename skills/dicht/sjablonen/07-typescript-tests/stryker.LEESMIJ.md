# stryker.config.json: mutatietests op kritieke modules

Dekt: ARCH-44 (besluit 21: minstens 80 procent van de mutanten gedood, als poort)

- `thresholds.break: 80` is de poort: onder 80 eindigt de opdracht met exitcode 1. Zonder deze instelling is `break` `null` en faalt er nooit iets (ARCH-44). `high: 90` en `low: 80` komen letterlijk uit het voorbeeld in de regel.
- Aanpassen: `mutate`. De kritieke delen zijn betaling, login en tenant-isolatie (besluit 21); `billing` en `auth` staan in het voorbeeld van de regel, `tenancy` is een eigen naam voor het derde deel. Zet hier de echte paden.
- `testRunner` en `reporters` staan niet in het onderzoek: het zijn de gangbare waarden bij Vitest. Lees ze na in de documentatie van StrykerJS.
- Draaien: voor elke oplevering die zo'n module raakt, op gewijzigde regels om de duur te beperken (ARCH-44).
- Voor PHP: `infection --min-msi=80`, met `--git-diff-lines` voor alleen gewijzigde regels (ARCH-44).
- Controleren: het rapport met de score zit in het bewijsbestand; een proef met een weggehaalde test laat de score zakken en de opdracht falen.
- Status: niet gevalideerd met StrykerJS (niet aanwezig op de server); het bestand laadt als JSON.
