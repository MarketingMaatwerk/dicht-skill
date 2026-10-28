# ARCH L: Threat modeling in vijftien minuten

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-80 Maak bij elk nieuw project een threat model in vier vragen
hoog · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Beantwoord vóór de eerste regel code van een nieuw project of een nieuwe dienst in maximaal vijftien minuten de vier vragen (waar werken we aan, wat kan er misgaan, wat doen we eraan, hebben we het goed genoeg gedaan), met een schets van de gegevensstromen en vertrouwensgrenzen en de zes STRIDE-categorieën per grens, en leg de uitkomst vast in `docs/threat-model.md` met per dreiging de maatregel als regel-ID uit deze skill.
- Bewijs: Het bestand bestaat, is gedateerd vóór de eerste functionele commit of in dezelfde wijziging, noemt elke grens uit `docs/ARCHITECTURE.md` en heeft per grens minstens één dreiging met een regel-ID. Afgevinkt als het bestand compleet is. Het sjabloon staat uitgewerkt in Open vragen, punt 5.
- Norm: NIST SSDF PW.1.1; OWASP Top 10 2025 A06; ASVS 5.0.0 V15.1.5 (L3).
- Zie ook: ARCH-81, PRIV-37, PRIV-59, PRIV-01

### ARCH-81 Herzie het threat model bij elke nieuwe ingang of grens
middel · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Werk het threat model bij in dezelfde wijziging als: een nieuwe soort invoer (mail, upload, webhook, import), een nieuwe externe dienst, een nieuwe rol of een wijziging in inloggen, een nieuwe tool voor een model of agent, en een nieuwe betaal- of verzendstroom.
- Bewijs: `git log --follow --format=%cs docs/threat-model.md | head -1` is niet ouder dan de laatste wijziging die een van de genoemde soorten toevoegde; de reviewchecklist (ARCH-54) bevat de vraag "nieuwe ingang of grens?". Afgevinkt met de datumvergelijking.
- Norm: NIST SSDF PW.1.1.
- Zie ook: ARCH-80, PRIV-37, PRIV-59, PRIV-01

### ARCH-82 Schrijf voor elke stroom met geld of limieten de misbruikgevallen op
middel · richtlijn · api | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Beschrijf voor elke stroom met geld, tegoed, kortingen, proefperiodes of limieten wat er gebeurt als iemand stappen overslaat, in een andere volgorde uitvoert, herhaalt, gelijktijdig uitvoert of met de waarden van een ander uitvoert, en leg de limieten per gebruiker en voor het geheel vast.
- Bewijs: `docs/threat-model.md` heeft per stroom een lijstje misbruikgevallen met per geval de test die het bewijst (ARCH-38, as herhaling) of de regel-ID van de maatregel. Afgevinkt als elke stroom met geld een lijst heeft.
- Norm: ASVS 5.0.0 V2.1.3 (L2), V2.3.1 (L1), V2.3.2 (L2).

### ARCH-83 Genereer de lijst van ingangen en vergelijk hem met het document
middel · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd een lijst bij van alle ingangen van de applicatie (routes, webhooks, geplande taken, wachtrij-verwerkers, MCP-tools, beheerschermen, mail-in, uploads), genereer die lijst uit de code waar dat kan, en laat een test falen als er een ingang bestaat die niet in de autorisatiematrix of het threat model staat.
- Bewijs: Een test vergelijkt de geregistreerde routes (Fastify: de routelijst; WordPress: `rest_get_server()->get_routes()` en de geregistreerde `wp_ajax_`-acties; MCP: de toollijst) met de matrix uit AUTH-66 en faalt bij een onbekende. Het aantal ingangen per soort staat in het bewijsbestand. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V8.1.1 (L1), V15.2.3 (L2); NIST SSDF PW.1.1.
- Zie ook: API-25, AUTH-13, WP-62
