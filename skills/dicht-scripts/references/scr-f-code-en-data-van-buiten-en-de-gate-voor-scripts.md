# SCR F: Code en data van buiten, en de gate voor scripts

Compacte regels van `dicht-scripts`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/scripts-automatisering.md` (regelnummer in `regel-index.tsv`).

### SCR-21 Geef elke `curl` in een script `--fail`, een time-out en alleen HTTPS
hoog · hard · alles · tegenlezer: scherpen (04-10-2026)
- Regel: Roep `curl` in een script altijd aan met `--fail` (of `--fail-with-body`), `--max-time <seconden>`, `--connect-timeout <seconden>` en bij een URL uit configuratie `--proto '=https'`; gebruik nooit `-k` of `--insecure`.
- Bewijs: `/usr/bin/grep -nE '\bcurl\b' $(git ls-files '*.sh') | /usr/bin/grep -vE '(^|[[:space:]])(-[a-zA-Z]*f[a-zA-Z]*|--fail(-with-body)?)([[:space:]]|$)'` en dezelfde zoekactie op `-m |--max-time` zijn leeg (een aanroep over meerdere regels loop je met de hand na); `/usr/bin/grep -rnE 'curl[^|]*( -k\b| --insecure)|wget[^|]*--no-check-certificate' .` is leeg. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V12.3.2 (L2, "TLS clients validate certificates"), V13.1.3 (L3, time-outs en herhalingen vastgelegd).
- Zie ook: API-48, API-49, ARCH-13, ARCH-14, AI-76, DB-65, API-19, SCR-25, SCR-26, SCR-43, MSG-42

### SCR-22 Voer nooit iets uit dat je in dezelfde regel ophaalt
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `curl ... | bash`, `wget -O- ... | sh`, `bash <(curl ...)`, `python3 <(curl ...)` en `eval "$(curl ...)"` nergens: niet in een installatie, niet in een uitrolscript, niet in cron en niet in een Dockerfile; haal het bestand op een vaste versie op, controleer de checksum of handtekening, lees het, en voer het dan uit.
- Bewijs: `/usr/bin/grep -rnE '(curl|wget)[^|;]*\| *(sudo +)?(ba|z|da)?sh\b|(bash|sh|python3?) +<\((curl|wget)|eval +"?\$\((curl|wget)' . <(crontab -l)` is leeg (zoek ook in Dockerfiles, `Makefile`, README-installatiestappen die je zelf uitvoert). Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V15.2.4 (L3, onderdelen uit de verwachte bron); OWASP CI/CD CICD-SEC-3 en NIST SSDF PO.3.2 zoals in GIT-62 (daar gelezen, hier niet opnieuw).
- Zie ook: GIT-62

### SCR-23 Maak shellcheck en een syntaxcontrole een gate voor elk shellscript
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai `bash -n` en `shellcheck --severity=warning` (vastgezet op een versie, nu v0.11.0) over elk shellscript in de repository vóór elke commit en in CI, en laat een onderdrukking alleen toe als `# shellcheck disable=SCxxxx` met de reden op dezelfde of de vorige regel.
- Bewijs: `shellcheck --version` toont de vastgezette versie; de gate-uitvoer is leeg; `/usr/bin/grep -rn 'shellcheck disable' $(git ls-files '*.sh')` toont bij elke treffer een reden. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V15.1.5 en V15.2.5 (L3, extra bescherming rond gevaarlijke functionaliteit); past ruim. BRIEF besluit 10 (lint als gate).
- Zie ook: GIT-57, SCR-35, INV-55
