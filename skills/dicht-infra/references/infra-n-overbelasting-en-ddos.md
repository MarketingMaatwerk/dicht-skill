# INFRA N: Overbelasting en DDoS

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-105 Weet wat je zelf kunt opvangen en wat alleen de aanbieder of een CDN kan
middel · richtlijn · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per publieke dienst vast welke bescherming er is op elke laag: de limieten in nginx (INFRA-45, INFRA-46) en de applicatie (WEB-66), de bescherming van de hostingaanbieder op netwerkniveau, en het besluit of er een CDN of proxydienst voor komt; en schrijf op wat je doet als de dienst wordt platgelegd.
- Bewijs: Het document met de lagen per dienst; een belastingsproef op een testomgeving die laat zien dat de limiet 429 geeft en de dienst voor andere bronnen bereikbaar blijft. Afgevinkt met document en proef.
- Norm: ASVS 5.0.0 V15.1.3 (L2), V15.2.2 (L2).
