# DB E: back-up en herstel

Compacte regels van `dicht-database`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/database.md` (regelnummer in `regel-index.tsv`).

### DB-44 Maak dagelijks een automatische back-up van elke database en van de globale objecten
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Neem elke productiedatabase op in een dagelijkse, geautomatiseerde back-up, en dump daarbij ook rollen en rechten met `pg_dumpall --globals-only` (of gebruik `pg_dumpall` voor het geheel).
- Bewijs: Vergelijk `docker ps` (alle Postgres-containers) en `SELECT datname FROM pg_database WHERE NOT datistemplate` met de bestanden van vandaag in de back-upmap. Afgevinkt als elke database een bestand van minder dan 26 uur oud heeft en er een globals-bestand is.
- Norm: AVG artikel 32 lid 1 onder b en c; ASVS 5.0.0 geen directe eis; NEN 7510 (beheersmaatregel voor back-up, nummer niet bevestigd).
- Zie ook: DB-45, DB-49, INFRA-79, INFRA-81, GIT-09, INFRA-83, DB-57

### DB-45 Versleutel elke back-up voordat hij op schijf staat
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leid de dump via een pipe direct door een versleuteling met een publieke sleutel (bijvoorbeeld `age -r`), bewaar de privésleutel niet op de server die de back-up maakt, en zet het herstelcommando in het script. Aanvulling uit INFRA-80: Versleutel ook vóór het versturen. Geldt voor elke back-up die de server verlaat, ook van bestanden, uploads en configuratie, niet alleen voor de databasedump.
- Bewijs: `file` op de nieuwste back-up van elke database toont een age- of gpg-bestand en geen leesbare SQL of gzip; de privésleutel staat niet op de server (`find / -name '*.key'` in de relevante mappen) of staat er alleen met een vastgelegde reden. Afgevinkt als geen enkele back-up leesbaar is zonder sleutel.
    Ook (uit INFRA-80): `file <jongste back-upbestand>` toont versleutelde data en geen `gzip` of `SQL`; `ls -la <back-upmap>` toont geen platte dumps of sleutelbestanden; de private sleutel staat niet op de server (`find / -name '<sleutelnaam>' 2>/dev/null` is leeg). Afgevinkt met de uitvoer. Zie DB-45.
- Norm: AVG artikel 32 lid 1 onder a; ASVS 5.0.0 14.2.4 (L2), 11.3.2 (L1).
- Dekt ook: INFRA-80
- Zie ook: DB-44, DB-49, INFRA-79, INFRA-81, GIT-09, INFRA-83, DB-57

### DB-46 Doe een herstelproef met datum, minstens elk kwartaal
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Herstel minstens elk kwartaal, en na elke wijziging van het back-upscript of een major upgrade, de nieuwste back-up van elke database in een lege wegwerpcontainer, controleer rijtellingen van kerntabellen en leg datum, duur en uitkomst vast.
- Bewijs: Een logboek (`docs/herstelproeven.md` of gelijkwaardig) met per database: datum, back-upbestand, hersteltijd, rijtellingen naast productie, en wie het deed. Afgevinkt als de laatste regel per database jonger is dan 92 dagen en de tellingen kloppen.
- Norm: AVG artikel 32 lid 1 onder c en d; NEN 7510 (nummer niet bevestigd).
- Zie ook: INFRA-82, DB-53, INFRA-84, DB-55, INFRA-78

### DB-47 Een mislukte of ontbrekende back-up geeft alarm
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat het back-upscript stoppen bij elke fout (`set -euo pipefail`), en bewaak onafhankelijk van het script dat er per database een bestand van minder dan 26 uur oud bestaat dat niet kleiner is dan de helft van het vorige.
- Bewijs: De eerste regels van het script, plus een aparte controle (cron, health-check of monitor) die op leeftijd en grootte alarmeert via het kanaal dat Marketing Maatwerk echt leest. Afgevinkt als een proef (back-up een dag overslaan in een testomgeving, of de controle draaien tegen een lege map) een melding geeft.
- Norm: AVG artikel 32 lid 1 onder d.
- Zie ook: ARCH-67, INFRA-35, ARCH-69, INFRA-86, INFRA-87, DB-97, AI-83, INFRA-52

### DB-48 Dump met een pg_dump van dezelfde major als de server
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai `pg_dump` en `pg_dumpall` vanuit de databasecontainer zelf (`docker exec <container> pg_dump ...`) of met een client van dezelfde of een nieuwere major dan de server, nooit met een oudere client op de host.
- Bewijs: Het back-upcommando gebruikt `docker exec`, of `pg_dump --version` in de omgeving van het script is gelijk aan of nieuwer dan `SHOW server_version`. Afgevinkt als dat zo is.
- Norm: AVG artikel 32 lid 1 onder c.

### DB-49 Bewaar een versleutelde kopie buiten de server
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Kopieer elke back-up na het maken naar een locatie buiten de server en buiten hetzelfde account, met inloggegevens die daar alleen mogen toevoegen en niet verwijderen.
- Bewijs: Lijst van de offsite-locatie met bestanden van vandaag voor elke database; een proef dat het account op de server daar geen bestand kan verwijderen of overschrijven. Afgevinkt als beide kloppen.
- Norm: AVG artikel 32 lid 1 onder b en c. De 3-2-1-regel zelf: zie domein INFRA.
- Zie ook: DB-44, DB-45, INFRA-79, INFRA-81, GIT-09, INFRA-83, DB-57

### DB-50 Gebruik het custom-formaat en herstel met stop-bij-fout
middel · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Dump afzonderlijke databases met `pg_dump -Fc`, herstel met `pg_restore` (of `psql -X --set ON_ERROR_STOP=on --single-transaction` voor platte SQL) en voer daarna `ANALYZE` uit.
- Bewijs: Het herstelcommando in het runbook (DB-53) bevat `-X`, `ON_ERROR_STOP=on` en `ANALYZE`; de herstelproef uit DB-46 gebruikt exact dat commando. Afgevinkt als de proef zonder fouten eindigt.
- Norm: AVG artikel 32 lid 1 onder c.

### DB-51 Gebruik WAL-archivering en PITR waar een dag gegevensverlies te veel is
hoog · richtlijn · api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet voor databases met betalingen, bestellingen of klantadministratie (bestelstraat, het CRM, zorgdata) continue WAL-archivering met een periodieke base backup op, of leg expliciet vast dat 24 uur gegevensverlies is geaccepteerd.
- Bewijs: `SHOW archive_mode;` is `on`, `SELECT * FROM pg_stat_archiver;` toont een recente `last_archived_time` en geen oplopende `failed_count`, en er is een herstelproef naar een tijdstip. Of: een ADR met het geaccepteerde herstelpunt. Afgevinkt als een van beide bestaat.
- Norm: AVG artikel 32 lid 1 onder c; besluit 13.

### DB-52 Een archive_command meldt alleen succes bij succes en overschrijft niets
middel · hard · api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf een `archive_command` dat alleen exitcode 0 geeft als het bestand veilig is opgeslagen, een bestaand bestand met andere inhoud weigert, en zet `archive_timeout` zodat een rustige server toch regelmatig archiveert.
- Bewijs: De waarde van `archive_command`, `archive_timeout` en `pg_stat_archiver.failed_count`; een proef met een onbereikbaar doel laat `failed_count` oplopen. Afgevinkt als de proef dat toont. Alleen van toepassing als DB-51 is ingevoerd.
- Norm: AVG artikel 32 lid 1 onder c.

### DB-53 Elke database heeft een herstelplan met RPO en RTO
hoog · hard · api | app | mcp | klantproject · tegenlezer: scherpen (04-10-2026) · bron niet gelezen: NEN
- Regel: Leg per database vast: het maximale gegevensverlies (RPO), de maximale hersteltijd (RTO), waar de back-ups en de sleutel liggen, het exacte herstelcommando, de volgorde van herstel van afhankelijke diensten en wie beslist; bewaar het plan ook buiten de server.
- Bewijs: Het document bestaat, staat ook buiten de server (Drive of wachtwoordmanager), noemt RPO en RTO in uren, en de laatste herstelproef (DB-46) is ermee uitgevoerd en bleef binnen de RTO. Afgevinkt als alle vier waar zijn.
- Norm: AVG artikel 32 lid 1 onder c; NEN 7510 (continuïteit, nummer niet bevestigd).
- Zie ook: DB-46, INFRA-82, INFRA-84, DB-55, INFRA-78

### DB-54 Herstel alleen dumps uit een vertrouwde bron
middel · hard · klantproject | api | app · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Herstel een dump die niet van je eigen servers komt (een klantdatabase, een export van een leverancier) alleen in een wegwerpcontainer zonder netwerk en zonder geheimen, en lees de SQL eerst.
- Bewijs: Werkwijze in het runbook; `pg_restore --file=- <dump> | less` of gelijkwaardig is uitgevoerd vóór het herstel. Afgevinkt als het runbook de stap bevat en de client de actuele minor heeft (DB-92).
- Norm: ASVS 5.0.0 geen directe eis; OWASP Top 10 2025 A08 Software or Data Integrity Failures (zelfde nummer in 2021).

### DB-55 Neem configuratie en geheimen mee in het herstel
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewaar `docker-compose.yml`, eventuele `postgresql.conf` en `pg_hba.conf`, initialisatiescripts en de (versleutelde) geheimen samen met de back-ups, zodat een lege server volledig is op te bouwen.
- Bewijs: De herstelproef uit DB-46 begint op een lege machine of lege map en gebruikt alleen wat in de back-up en de repository staat. Afgevinkt als dat lukt zonder iets van de oude server te kopiëren.
- Norm: AVG artikel 32 lid 1 onder c.
- Zie ook: DB-46, INFRA-82, DB-53, INFRA-84, INFRA-78

### DB-56 Zet data-checksums aan bij een nieuw cluster
middel · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Initialiseer elk nieuw cluster met data-checksums: op PostgreSQL 18 is dat de standaard, op 16 en 17 in Docker met `POSTGRES_INITDB_ARGS="--data-checksums"`.
- Bewijs: `SHOW data_checksums;` geeft `on`. Afgevinkt als dat zo is voor nieuwe clusters; voor bestaande clusters is het een verbeterpunt bij de volgende major upgrade.
- Norm: AVG artikel 32 lid 1 onder b (integriteit).

### DB-57 Back-ups hebben zelf een bewaartermijn
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per database vast hoe lang back-ups worden bewaard, ruim oudere automatisch op (lokaal en offsite), en neem die termijn op in het verwerkingsregister en het antwoord op een verwijderverzoek.
- Bewijs: De opruimregels in het script (`find ... -mtime +N -delete`) en de spiegeling naar offsite, naast de termijn in `policy-state.yaml`. Afgevinkt als de oudste aanwezige back-up niet ouder is dan de vastgelegde termijn en het runbook beschrijft dat verwijderverzoeken na een herstel opnieuw worden toegepast (DB-84).
- Norm: AVG artikel 5 lid 1 onder e en artikel 17.
- Zie ook: DB-44, DB-45, DB-49, INFRA-79, INFRA-81, GIT-09, INFRA-83
