# PRIV L: toegankelijkheid (Europese toegankelijkheidswet)

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-65 Stel per webwinkel of dienst vast of de toegankelijkheidswet geldt
hoog · hard · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Noteer bij elk project waar een consument online een overeenkomst kan sluiten (webshop, bestelstraat, abonnement, boeking) of de aanbieder tien of meer werknemers heeft of meer dan 2 miljoen euro jaaromzet of balanstotaal; zo ja, dan zijn de toegankelijkheidseisen een harde eis van het project.
- Bewijs: In de projectdocumentatie: het antwoord op de twee drempelvragen, met de bron (opgave van de klant). Afgevinkt als het er staat. `[jurist]` bij twijfel of iets een e-handelsdienst voor consumenten is.
- Norm: Richtlijn (EU) 2019/882 artikel 2 lid 2 onder f, artikel 3 punt 23 en 30, artikel 4 lid 5, artikel 31 lid 2; BW artikel 6:230fa tot en met 6:230fd.

### PRIV-66 Bouw elke nieuwe site op WCAG 2.2 niveau AA
hoog · hard · website | wp-thema | wp-plugin | app | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Lever elke nieuwe website, webshop en app op tegen WCAG 2.2 niveau A en AA, ook als de wet (nog) niet geldt voor de klant, en leg elke afwijking met reden vast.
- Bewijs: (1) Een geautomatiseerde scan in de gate (axe-core via Playwright) op elk paginatype, zonder fouten op A en AA. (2) Een handmatige controle van de hoofdroute (zoeken, product, winkelwagen, afrekenen, account) met alleen het toetsenbord en met een schermlezer, vastgelegd met datum. Afgevinkt met beide; een scan alleen vindt maar een deel van de criteria. Technisch deels af te dwingen.
- Norm: Richtlijn (EU) 2019/882 bijlage I afdeling III onder c (waarneembaar, bedienbaar, begrijpelijk, robuust); EN 301 549; WCAG 2.2 (W3C Recommendation, 12 december 2024).
- Zie ook: PRIV-67, WEB-70, ARCH-46

### PRIV-67 Maak inloggen, beveiligingsstappen en betalen toegankelijk
hoog · hard · website | wp-plugin | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Test identificatie, beveiligingsstappen (captcha, tweede factor, bevestigingscodes) en de betaalstap apart op toegankelijkheid, en kies geen botbescherming of betaalweergave die een gebruiker met een beperking buitensluit.
- Bewijs: De e2e-test van de bestelroute draait één keer met alleen toetsenbord (Tab, Enter, spatie) tot en met de betaalpagina, en de axe-scan omvat de pagina met de captcha en de pagina met de betaalvelden. Afgevinkt met de testuitvoer. Zie WEB-70 voor de botbescherming.
- Norm: Richtlijn (EU) 2019/882 bijlage I afdeling IV onder g; WCAG 2.2 criterium 3.3.8.
- Zie ook: PRIV-66, WEB-70, ARCH-46

### PRIV-68 Lever een toegankelijkheidsverklaring mee en houd haar actueel
middel · hard · website | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet bij elke dienst die onder de wet valt een toegankelijkheidsverklaring op de site die uitlegt hoe de dienst aan de eisen voldoet, eenvoudig vindbaar en zelf toegankelijk, en lever de inhoud aan zodat de klant haar ook in de algemene voorwaarden of een gelijkwaardig document kan opnemen.
- Bewijs: De verklaring staat op een vaste URL met de datum van de laatste toets, en is gelinkt in de voettekst; een e2e-test vindt de link op elke pagina. Afgevinkt met de URL en de testuitvoer. De exacte inhoud van de verklaring: `[jurist]` of de ACM-voorbeeldtekst.
- Norm: Richtlijn (EU) 2019/882 artikel 13 en bijlage V; BW artikel 6:230fb lid 2.

### PRIV-69 Ken de uitzonderingen voor inhoud, en gebruik ze niet voor nieuwe inhoud
laag · richtlijn · website | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Beroep je voor inhoud alleen op de uitzonderingen die de richtlijn noemt (video en kantoorbestanden van vóór 28 juni 2025, kaarten met een toegankelijk alternatief, inhoud van derden waarover de aanbieder geen zeggenschap heeft, archieven die niet meer wijzigen) en maak alles wat daarna is gepubliceerd toegankelijk: ondertiteling, tekstalternatieven, toegankelijke pdf's.
- Bewijs: Een lijst van downloads en video's met publicatiedatum; alles van na 28 juni 2025 heeft een tekstlaag en koppen (pdf) of ondertiteling (video). Afgevinkt met de lijst en een steekproef.
- Norm: Richtlijn (EU) 2019/882 artikel 2 lid 4.
