# Vaste waarden bij de sjablonen: wat besloten is en wat per project wordt ingevuld

Opgesteld door de validatie-sessie op 04-10-2026 als lijst van lege plekken in de sjablonen waar het onderzoek geen waarde geeft. Bijgewerkt op 05-10-2026 met de besluiten van Marketing Maatwerk: vier punten zijn besloten (7, 8, 10 en 11), en zeven punten zijn geen besluit van Marketing Maatwerk maar worden per project ingevuld (1 tot en met 6 en 9). Punt 11 is op 05-10-2026 na een apart akkoord uitgevoerd. Een besloten waarde staat ook in `skill/dicht/references/vaste-waarden.md`. In dit bestand staat geen voorstel voor een getal dat niet uit de bron komt, behalve waar dat er uitdrukkelijk bij staat (punt 8).

Per project invullen betekent: de waarde blijft in het sjabloon een lege plek die faalt tot ze is ingevuld (of commentaar met `<kies>`); wie het project bouwt kiest de waarde bij de intake, onderbouwt haar in één zin en legt haar vast in het project (configuratie en bewijsbestand). Er komt geen vaste waarde voor alle projecten en Marketing Maatwerk wordt er niet per project om gevraagd.

## De elf punten

| Nr | Onderwerp | Waar de plek staat | Wat de bron wel zegt | Stand |
|---|---|---|---|---|
| 1 | Limiet per bron voor webhooks, zoeken en algemeen verkeer (nginx) | `01-nginx/conf.d/00-dicht-http.conf`, de drie regels met `rate=<kies>` | Alleen inloggen 5 per minuut (INFRA-46) en formulieren 1 per seconde (WEB-66). Die twee zijn gemeten: bij 30 aanvragen achter elkaar komen er 6 door en krijgen 24 een 429 | per project invullen (besluit van Marketing Maatwerk, 05-10-2026) |
| 2 | Limiet per minuut in de applicatie, algemeen en voor bestellen | `08-api/src/env.ts`: `RATE_LIMIT_ALGEMEEN_PER_MINUUT`, `RATE_LIMIT_BESTELLEN_PER_MINUUT` (verplicht, geen standaardwaarde) | API-20 eist een limiet per route, geen getal | per project invullen (besluit van Marketing Maatwerk, 05-10-2026) |
| 3 | Maximale grootte van een upload | `01-nginx/conf.d/site-voorbeeld.conf`, de uitgeschakelde uploadroute; gelijk aan `bodyLimit` van de route | INFRA-45 en API-18: 1 MB als algemene grens (gemeten: 413 boven 1 MB), hoger alleen op de uploadroute | per project invullen (besluit van Marketing Maatwerk, 05-10-2026) |
| 4 | Dagplafond voor bulkwerk en verzendlijnen | `04-scripts/bulk.sh` en `04-scripts/skelet.py`: `PLAFOND_PER_DAG` (verplicht) | AI-26 en BIZ-23 eisen een plafond, geen getal. De bestaande lijnen hebben elk een eigen plafond (bijvoorbeeld 20 plus 20 per dag) | per project invullen (besluit van Marketing Maatwerk, 05-10-2026): elke lijn houdt haar eigen plafond |
| 5 | Aantal fouten achter elkaar waarna een lus stopt | `04-scripts/lus.sh`: `MAX_FOUTEN` (verplicht) | SCR-43 geeft voorbeeldwaarden voor de pauzes (60, 900, 30 en 15), niet voor dit aantal | per project invullen (besluit van Marketing Maatwerk, 05-10-2026) |
| 6 | Time-out per stap in een script | `04-scripts/bulk.sh`: `STAP_TIMEOUT`; `03-systemd/crontab-voorbeeld`: 15m | SCR-38 noemt 15 minuten als voorbeeld, geen norm | per project invullen (besluit van Marketing Maatwerk, 05-10-2026) |
| 7 | Bewaartermijn van back-ups | `06-database/backup.sh`: `BEWAAR_DAGEN` (verplicht, de twee waarden staan in de kop) | DB-57 eist dat back-ups een eigen bewaartermijn hebben en dat die in het register staat, geen getal | BESLOTEN (Marketing Maatwerk, 05-10-2026): 14 dagen voor websites, 30 dagen voor webshops en eigen systemen (CRM, registrar). De variabele blijft verplicht omdat de waarde per soort project verschilt |
| 8 | Reactietermijnen bij een gemelde kwetsbaarheid | `05-git-ci/SECURITY.md`: ontvangstbevestiging en eerste beoordeling | PRIV-72 eist dat er een termijn staat, niet welke. De hersteltermijnen zelf zijn al besloten (48 uur, 7 dagen, 30 dagen; besluit 22) | BESLOTEN (Marketing Maatwerk, 05-10-2026): ontvangstbevestiging binnen 1 werkdag, eerste beoordeling binnen 5 werkdagen. De 5 werkdagen zijn een eigen voorstel zonder bron; het is een belofte aan buitenstaanders |
| 9 | Dekkingsdrempel van de tests | `07-typescript-tests/vitest.config.ts`: de drempels staan op 0 | ARCH-45 vraagt "het huidige niveau" als ondergrens; de mutatiedrempel van 80 procent is al besloten (besluit 21) | per project invullen (besluit van Marketing Maatwerk, 05-10-2026): het gemeten niveau van het project als ondergrens |
| 10 | Dependabot of Renovate | `05-git-ci/.github/dependabot.yml` | Dependabot komt volledig uit het onderzoek en werkt op het gratis plan | BESLOTEN (Marketing Maatwerk, 05-10-2026): Dependabot. Het sjabloon voor Renovate en zijn LEESMIJ zijn verwijderd |
| 11 | npm op de server | `05-git-ci/.npmrc`: `min-release-age=7` | Gemeten op de server op 05-10-2026 met npm 12.1.0: in een map met deze `.npmrc` geeft `npm config get min-release-age` 7 en weigert `npm install npm@12.2.0` (uitgebracht 30-09-2026) met ETARGET; zonder versie kiest npm 12.1.0. Buiten een project met deze `.npmrc` staat de instelling op `null` | BESLOTEN en uitgevoerd (akkoord van Marketing Maatwerk, 05-10-2026): npm op de server is 12.1.0 (was 10.9.8). 12.2.0 was op die dag 5 dagen oud en mag volgens GIT-72 vanaf 07-10-2026 18:46. Install-scripts draaien alleen nog voor de lijst in `~/.npmrc` (`allow-scripts`); de meting per project, de terugweg en wat open staat: `NPM12-NOTITIES.md` |

## Ook per project invullen

Naast punt 1 tot en met 6 en 9 hierboven hangen deze plekken aan het project en niet aan een vaste keuze:

- de versie en de digest in `FROM` en `image:` (`02-docker/`), en het volumepad van PostgreSQL dat per hoofdversie verschilt;
- `CONNECTION LIMIT` van de app-rol: de poolgrootte van de dienst plus een kleine marge (`06-database/rollen.sql`, DB-10);
- `AGE_ONTVANGER`: de publieke sleutel voor de versleutelde back-up (`06-database/backup.sh`);
- `--verwacht`: het aantal items per run, door de mens die de run start (`04-scripts/`);
- de scanners van de gate op een vaste versie met controlesom (`05-git-ci/.github/workflows/gate.yml`, stap "Scanners klaarzetten") en de commit-SHA van gitleaks in `.pre-commit-config.yaml`;
- de prijslijst in `08-api/src/routes/bestellen.ts` (staat op 0 tot hij uit de vertrouwde bron is ingevuld);
- de capabilities van een eigen image (`02-docker/compose.yml`): gemeten voor postgres:18.6, niet voor andere images.
