# ARCH J: Prestatie en beschikbaarheid

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-73 Leg per dienst een prestatie- en beschikbaarheidsdoel vast en meet het
middel · richtlijn · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per dienst vast welke responstijd (p95 per soort route) en welke beschikbaarheid per maand je nastreeft, meet beide (ARCH-68, INFRA-86), en behandel een overschrijding als een bevinding met een eigenaar.
- Bewijs: De doelen staan in `docs/ARCHITECTURE.md`; het overzicht uit ARCH-68 toont de gemeten p95 per route naast het doel; de bewaking van buiten toont de beschikbaarheid over de laatste 30 dagen. Afgevinkt met de drie onderdelen. Voorstel voor de beginwaarden, als eigen keuze: leesroutes p95 onder 300 ms, schrijfroutes onder 800 ms, alles wat langer dan 5 seconden kan duren in een wachtrij; beschikbaarheid volgens INFRA-84.
- Norm: ASVS 5.0.0 V15.1.3 (L2), V15.2.2 (L2).

### ARCH-74 Houd de Core Web Vitals op het 75e percentiel binnen de drempels
middel · hard · website | wp-thema | klantproject | app · tegenlezer: scherpen (04-10-2026)
- Regel: Lever een publieke site op met LCP van 2,5 seconden of minder, INP van 200 milliseconden of minder en CLS van 0,1 of minder, gemeten op het 75e percentiel van paginaladingen en apart voor mobiel en desktop; meet vóór de oplevering in het lab op de vijf belangrijkste paginatypes en daarna met velddata.
- Bewijs: Een Lighthouse-rapport per paginatype (mobiel) met LCP en CLS binnen de drempels en TBT als labvervanger voor INP; daarna velddata uit het Chrome-gebruikersrapport of de bibliotheek `web-vitals` over minimaal 28 dagen. Afgevinkt met de labrapporten bij oplevering en de velddata bij de eerste controle daarna. Zie de skill `performance` voor de maatregelen.
- Norm: geen ASVS-eis; Google Core Web Vitals.

### ARCH-75 Leg het prestatiebudget vast als controle die kan falen
laag · richtlijn · website | wp-thema | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg voor eigen sites en apps de budgetten vast in een Lighthouse CI-configuratie met controles op niveau `error` (LCP, CLS, totale omvang van scripts) en draai die in de gate of vóór elke oplevering tegen het tweede exemplaar uit ARCH-26.
- Bewijs: `lhci autorun` (of `lhci collect` en `lhci assert`) geeft exitcode 0; een proef met een kunstmatig vertraagde pagina maakt de opdracht rood. Afgevinkt met beide uitvoeren. Draai meerdere runs per pagina; één meting schommelt.
- Norm: BRIEF besluit 12 en 17.
