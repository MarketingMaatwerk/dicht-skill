# ARCH E: Beslissingen, uitzonderingen en schuld vastleggen

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-29 Leg elke architectuurbeslissing vast als ADR
middel · hard · api | app | mcp | klantproject | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf voor elke beslissing die structuur, afhankelijkheden, interfaces, beveiligingsmodel of niet-functionele eigenschappen raakt een kort genummerd bestand in `docs/adr/` met context, besluit, status en gevolgen; herschrijf een oud besluit nooit maar markeer het als vervangen door het nieuwe.
- Bewijs: `ls docs/adr/` toont oplopende nummers zonder gaten; er is in elk geval een ADR voor: een afwijking van de modulaire monoliet (ARCH-01), het tenantmodel (DB-11), het inlog- en sessiemodel, elke nieuwe externe dienst die persoonsgegevens verwerkt (ook `policy-state.yaml` bijwerken), en elke keuze voor een framework of opslag. Afgevinkt als die bestanden bestaan en de status klopt.
- Norm: NIST SSDF PW.1.1 (ontwerpbeslissingen en risico's vastleggen); BRIEF besluit 9.

### ARCH-30 Leg elke uitzondering op een harde regel vast, ook een overgeslagen stap
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Wijk alleen van een harde regel af met een expliciet besluit van Marketing Maatwerk, en leg dat vast met de regel-ID, de reden, de datum, de einddatum of herzieningsdatum en de vervangende maatregel; behandel een overgeslagen stap in de gate of de uitrol (`SKIP_TESTS=1`, `--no-verify`, een uitgezette scan) als zo'n uitzondering en schrijf hem in het bewijsbestand.
- Bewijs: `docs/uitzonderingen.md` (of ADR's met het label uitzondering) bevat per regel: ID, wie, wanneer, waarom, tot wanneer, vervangende maatregel. `grep -rnE "SKIP_[A-Z]+|--no-verify|continue-on-error|\|\| true" deploy/ scripts/ .github/ package.json` toont alleen plekken waar het overslaan ook naar het bewijsbestand wordt geschreven. Afgevinkt als het bestand bestaat en geen uitzondering over zijn einddatum heen is.
- Norm: BRIEF besluit 2; NIST SSDF PO.3.3.
- Zie ook: GIT-65, ARCH-55

### ARCH-31 Schrijf per dienst een runbook met de vijf handelingen en elk alarm
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd per dienst `docs/runbooks/<dienst>.md` bij met: starten en stoppen, uitrollen, terugdraaien, herstellen uit een back-up, een vastgelopen of mislukte taak opnieuw aanbieden, en per alarm (ARCH-69) wat het betekent en wat de eerste drie stappen zijn.
- Bewijs: Het bestand bestaat; elke alarmnaam uit de bewakingsconfiguratie komt erin voor (`diff` tussen de lijst alarmnamen en de koppen in het runbook is leeg); de terugdraai-oefening (ARCH-25) is met dit bestand gedaan. Afgevinkt met de vergelijking en de datum van de oefening. Zie INFRA-91 voor het draaiboek bij een beveiligingsincident.
- Norm: OWASP Top 10 2025 A09.

### ARCH-32 Leg hersteltermijnen vast en houd een schuldregister bij
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per project vast binnen hoeveel dagen een kwetsbare afhankelijkheid per ernst wordt bijgewerkt, en houd één register bij van bekende technische schuld (uitgestelde upgrades, baselines van linters, kapotte of overgeslagen tests, tijdelijke omwegen) met per punt een eigenaar, een datum en de voorwaarde waaronder het wordt opgelost. De termijnen zijn vast (besluit 22, GIT-77): kritiek of actief misbruikt (CISA KEV) binnen 48 uur, hoog binnen 7 dagen, middel binnen 30 dagen.
- Bewijs: `docs/SCHULD.md` (of het issue-overzicht) bestaat; het aantal `it.skip`, `test.skip`, `markTestSkipped`, `eslint-disable`, `phpcs:ignore`, `@ts-expect-error` en regels in de PHPStan-baseline is geteld en staat erin met datum; het aantal is niet hoger dan bij de vorige oplevering, of de toename heeft een reden. De hersteltermijnen staan in `docs/ARCHITECTURE.md` of `SECURITY.md`. Afgevinkt met de tellingen. De termijnen zijn besluit 22.
- Norm: ASVS 5.0.0 V15.1.1 (L1), V15.2.1 (L1).
- Zie ook: GIT-77, INFRA-24, WP-49, GIT-88, DB-92, GIT-61, PRIV-73, MSG-06, SCR-32
