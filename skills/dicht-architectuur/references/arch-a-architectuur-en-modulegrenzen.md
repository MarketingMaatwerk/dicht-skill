# ARCH A: Architectuur en modulegrenzen

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-01 Bouw een modulaire monoliet; een extra proces of dienst vraagt een vastgelegd besluit
middel · hard · api | app | mcp | klantproject · eigen bron · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw elke applicatie als één uitrolbare eenheid met modules per bedrijfsdomein, en voeg een apart proces, een aparte dienst of een aparte database alleen toe met een ADR (ARCH-29) die één van deze redenen noemt: werk dat langer duurt dan een verzoek (worker, ARCH-18), een andere vertrouwensgrens (ARCH-04), of een ander herstart- of schaalpatroon dat gemeten is.
- Bewijs: `docs/ARCHITECTURE.md` (ARCH-06) noemt elk proces met de reden; elk proces dat geen webproces of worker van dezelfde codebase is, heeft een ADR. `systemctl list-units --type=service` of `docker compose ps` komt overeen met die lijst. Afgevinkt als lijst en werkelijkheid gelijk zijn.
- Norm: BRIEF besluit 9; ASVS 5.0.0 V15.2.5 (L3) voor de uitzondering "andere vertrouwensgrens".
- Eigen bron: geen primaire bron; de eis is besluit 9 en een eigen incident; ASVS V15.2.5 dekt alleen de uitzondering voor een andere vertrouwensgrens. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).

### ARCH-02 Geef elke module één publieke ingang en dwing de grens af in de gate
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat code buiten een module alleen het ingangsbestand van die module importeren (bijvoorbeeld `src/modules/<naam>/index.ts`), en laat de gate falen op een import die dieper in een andere module reikt.
- Bewijs: `npx depcruise src --config .dependency-cruiser.cjs` geeft exitcode 0 en staat in de gate (GIT-57); een proef met één verboden import maakt de gate rood (GIT-59). Een alternatief zonder extra hulpmiddel is de ESLint-regel `no-restricted-imports` met `patterns`. Afgevinkt met de groene en de rode uitvoer.
- Norm: BRIEF besluit 9 en 10; ASVS 5.0.0 V8.3.1 (L1, autorisatie op een vertrouwde laag).

### ARCH-03 Laat afhankelijkheden één kant op lopen en sta geen cirkels toe
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per project de toegestane richting vast (bijvoorbeeld routes naar domeinlogica naar opslag, nooit terug) en laat de gate falen op een cirkel tussen modules.
- Bewijs: De dependency-cruiser-configuratie bevat een regel met `circular: true` op niveau `error`; de uitvoer toont nul overtredingen. Afgevinkt met de uitvoer.
- Norm: BRIEF besluit 9.

### ARCH-04 Zet gevaarlijke functionaliteit apart en geef haar minder rechten
hoog · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Benoem in de documentatie welke onderdelen gevaarlijk zijn (bestanden van gebruikers verwerken, HTML of pdf renderen, externe URL's ophalen, code of commando's uitvoeren, modeluitvoer verwerken) en draai die in een apart proces of een aparte container met eigen, kleinere rechten.
- Bewijs: `docs/ARCHITECTURE.md` heeft een lijst "gevaarlijke functionaliteit" met per onderdeel het proces, de gebruiker, de netwerktoegang en de regel-ID van de inperking (INFRA thema D en H). Afgevinkt als de lijst bestaat en elk onderdeel een inperking heeft of een genoteerde reden waarom niet.
- Norm: ASVS 5.0.0 V15.1.5 (L3) en V15.2.5 (L3). Op L2 een richtlijn; voor kritieke delen hard.

### ARCH-05 Lever geen test-, voorbeeld- of ontwikkelcode mee naar productie
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zorg dat de productiebuild en de productie-image alleen bevatten wat de applicatie nodig heeft: geen testbestanden, geen voorbeeld- of demoroutes, geen seed-accounts, geen ontwikkelafhankelijkheden en geen debugroutes.
- Bewijs: (1) `docker run --rm <image> sh -c 'ls; ls node_modules/.bin | head'` of een lijst van de uitgerolde map toont geen `test`, `__tests__`, `*.spec.*`, `fixtures` of ontwikkeltools. (2) De routelijst van de draaiende applicatie (Fastify: `app.printRoutes()`) bevat geen test- of debugroutes. (3) `SELECT` op de gebruikerstabel toont geen seed-account. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V15.2.3 (L2), V13.2.3 (L2, geen standaardwachtwoorden), V13.4.2 (L2).
- Zie ook: WEB-64, API-81, WP-63, WP-41, API-25

### ARCH-06 Houd één architectuurdocument bij met vaste onderdelen
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd per project `docs/ARCHITECTURE.md` bij met minimaal: de processen en modules, elke externe dienst waarmee de applicatie praat (ook adressen die een gebruiker kan opgeven), de dure functies met hun limiet, de gevaarlijke functionaliteit (ARCH-04), de autorisatieregels in hoofdlijnen, en de loginventaris (ARCH-57).
- Bewijs: Het bestand bestaat en is gewijzigd in dezelfde wijziging als de laatste nieuwe externe dienst (`git log -1 --format=%cs docs/ARCHITECTURE.md`); elke host in de uitgaande aanroepen (`grep -rnoE "https?://[a-z0-9.-]+" src | sort -u`) staat in het document. Afgevinkt als beide kloppen.
- Norm: ASVS 5.0.0 V13.1.1 (L2), V15.1.3 (L2), V15.1.5 (L3), V16.1.1 (L2), V8.1.1 (L1).
