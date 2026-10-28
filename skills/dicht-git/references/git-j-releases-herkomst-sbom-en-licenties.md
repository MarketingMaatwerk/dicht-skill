# GIT J: Releases, herkomst, SBOM en licenties

Compacte regels van `dicht-git`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/git-supplychain.md` (regelnummer in `regel-index.tsv`).

### GIT-101 Maak bij elke release een SBOM
middel · hard · wp-plugin | wp-thema | api | app | mcp · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: WET
- Regel: Genereer bij elke release een SBOM in CycloneDX of SPDX (`npm sbom --sbom-format=cyclonedx`, `syft <image> -o cyclonedx-json`, of de Composer-plugin `cyclonedx/cyclonedx-php-composer`) en bewaar hem bij de release.
- Bewijs: Het SBOM-bestand staat bij de laatste release en bevat de directe en transitieve afhankelijkheden (`jq '.components | length' sbom.json` is groter dan het aantal directe). Afgevinkt met het bestand. `npm sbom` bestaat sinds npm 10.2.0. De Composer-plugin moet in `allow-plugins` (GIT-83). CycloneDX is versie 1.7, SPDX 3.0. Het `jq`-pad is niet getest (niet bevestigd, punt 9).
- Norm: ASVS 5.0.0 V15.1.2 (L2); NIST SSDF PS.3.2; OWASP Top 10 2025 A03; Cyber Resilience Act bijlage I deel II punt 1 (zie PRIV voor de reikwijdte). Wettelijke basis: zie PRIV-75, PRIV-70 (SBOM onder de Cyber Resilience Act).
- Zie ook: PRIV-75, GIT-98

### GIT-102 Een release is een ondertekende tag op een gevalideerde commit
middel · hard · wp-plugin | wp-thema | api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak elke release met `git tag -s v<versie>` op een commit waarop de gate groen was, verplaats of hergebruik nooit een tag, en publiceer bij elk releasebestand de SHA-256.
- Bewijs: `git tag -v v<versie>` slaagt; `git rev-parse v<versie>^{commit}` is de commit uit het gate-bewijs (GIT-67); de SHA-256 staat in de release-notitie. Afgevinkt met de drie. Zonder `allowed_signers` (GIT-18) faalt de verificatie lokaal.
- Norm: NIST SSDF PS.2.1 (voorbeeld 1) en PS.3.1; OWASP CI/CD CICD-SEC-9.

### GIT-103 Leg herkomst vast met wat het plan toelaat
laag · richtlijn · wp-plugin | mcp | api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor een publieke repo artifact attestations (`actions/attest`) en controleer ze met `gh attestation verify`; gebruik voor een privé-repo de ondertekende tag, de controlesom en de SBOM als herkomstbewijs.
- Bewijs: Voor publiek: de uitvoer van `gh attestation verify <bestand> -R <eigenaar>/<repo>`. Voor privé: GIT-101 en GIT-102 zijn afgevinkt en in het projectdocument staat welk SLSA-niveau wordt gehaald (L1: herkomst bestaat). Afgevinkt met uitvoer of document.
- Norm: SLSA 1.2 Build L1 tot en met L3; NIST SSDF PS.3.2; OWASP CI/CD CICD-SEC-9.

### GIT-104 Controleer de licentie van elke afhankelijkheid
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per project vast welke licenties zijn toegestaan en controleer bij elke nieuwe afhankelijkheid en in de gate dat er geen AGPL, SSPL, "source available" (BUSL, Elastic) of onbekende licentie in productie-afhankelijkheden zit zonder een besluit.
- Bewijs: `trivy fs --scanners license --severity HIGH,CRITICAL .` is leeg of elke treffer heeft een besluit; voor PHP `composer licenses --format=json --no-dev`. Afgevinkt met de uitvoer. Trivy deelt licenties in klassen in (Forbidden, Restricted, Reciprocal, Notice, Permissive); welke licentie in welke klasse valt, is niet per licentie nagelezen. Dit is geen juridisch advies: de afweging hoort bij PRIV en bij twijfel bij een jurist. Renovate en trufflehog zijn zelf AGPL: als los hulpmiddel gebruiken is iets anders dan de code opnemen in een product.
- Norm: OpenSSF Concise Guide for Evaluating Open Source Software (het punt over licenties; citaat weggelaten, zie THIRD-PARTY.md); NIST SSDF PW.4.1.

### GIT-105 WordPress-plugins en thema's: GPL-compatibel, ook wat je meelevert
middel · hard · wp-plugin | wp-thema · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke plugin en elk thema dat je levert een GPL-compatibele licentie ("GPLv2 or later" tenzij er een reden is) en controleer dat elke meegeleverde bibliotheek, afbeelding en elk lettertype daarmee verenigbaar is.
- Bewijs: De pluginkop bevat `License:` en `License URI:`; de lijst van GIT-89 heeft per meegeleverd onderdeel een licentie die GPL-compatibel is. Afgevinkt met beide. wordpress.org erkent zelf "some legal grey area" over wat afgeleid werk is; markeer bij een betaald of gesloten model de vraag voor een jurist (PRIV). De overeenkomstige eis voor thema's is niet als citaat opgehaald (niet bevestigd, punt 14).
- Norm: richtlijn 1 van de Detailed Plugin Guidelines van wordpress.org.

### GIT-106 Heb een draaiboek voor een gekaapt pakket
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per project vast wat je doet als een afhankelijkheid, image of actie gekaapt blijkt: zoek de genoemde versies in alle lockfiles en SBOM's, stel vast of er in het venster is geïnstalleerd of gebouwd, behandel bij een treffer de machine als overgenomen (GIT-54), pin terug op de laatste goede versie, en bouw en rol opnieuw uit.
- Bewijs: Het draaiboek bestaat (een halve pagina) en is één keer geoefend met een echt incident uit dit document: de zoekopdracht over alle repo's en worktrees geeft binnen een minuut antwoord. Afgevinkt met draaiboek en de uitvoer van de oefening. Een ingetrokken versie verdwijnt niet uit de tijdlijn van de registry: `npm view axios time` toont 1.14.1 nog.
- Norm: NIST SSDF RV.1.1 en RV.1.3; OWASP Top 10 2025 A03; AVG artikel 33 bij toegang tot persoonsgegevens (zie PRIV en INFRA voor incidentrespons).
- Zie ook: PRIV-31, INFRA-96, PRIV-32, PRIV-33, INFRA-91, PRIV-71, AI-84, WP-78, INFRA-94
