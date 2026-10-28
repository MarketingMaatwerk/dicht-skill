# WEB 6: Framing, berichten en vensters

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-36 Controleer afzender en inhoud bij postMessage
hoog · hard · website | app | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Voeg alleen een `message`-listener toe als je berichten verwacht, vergelijk in de listener `event.origin` exact met een allowlist, valideer de vorm van het bericht met een schema, behandel de inhoud als data, en stuur zelf altijd naar een exacte doel-origin en nooit naar `*`.
- Bewijs: `grep -rnE "addEventListener\(['\"]message|postMessage\(" src/` en per resultaat een origin-controle en een exacte doel-origin; een test die een bericht stuurt vanaf een andere origin en vaststelt dat er niets gebeurt. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V3.5.5 (L2).

### WEB-37 Zet niet-vertrouwde inhoud in een iframe met sandbox
middel · hard · app | website | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Toon HTML die je niet zelf hebt gemaakt (een ontvangen mail, een voorbeeld van een klantsite, een showcase, uitvoer van een model) in een `<iframe sandbox>` zonder `allow-same-origin` in combinatie met `allow-scripts`, bij voorkeur vanaf een aparte origin.
- Bewijs: `grep -rn "<iframe" src/` en per iframe met externe of door gebruikers geleverde inhoud een `sandbox`-attribuut; een test met een mail die `<script>parent.document.title='x'</script>` bevat laat de titel ongemoeid. Afgevinkt met grep en test.
- Norm: ASVS 5.0.0 V3.2.1 (L1), V15.2.5 (L3).

### WEB-38 Open externe links zonder verwijzing naar het eigen venster
laag · richtlijn · website | wp-thema | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef links naar externe sites die in een nieuw venster openen `rel="noopener noreferrer"` en roep `window.open` aan met `noopener,noreferrer`.
- Bewijs: `grep -rn 'target="_blank"' <templates>` en elk resultaat heeft `rel` met `noopener`; een lintregel dwingt het af in React. Afgevinkt met de grep.
- Norm: ASVS 5.0.0 V3.4.8 (L3) raakt hetzelfde risico via COOP.
