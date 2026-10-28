# SCR H: Cron en systemd-timers

Compacte regels van `dicht-scripts`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/scripts-automatisering.md` (regelnummer in `regel-index.tsv`).

### SCR-37 Zet de omgeving die een cron-taak nodig heeft in het script zelf
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in elk script dat uit cron draait zelf `PATH` (volledig, met absolute mappen), de werkmap (`cd /pad || exit 1`) en elke variabele die het nodig heeft; reken niet op het inlogprofiel, schrijf de cron-regel met absolute paden, en zet een backslash voor elk `%` in de regel. Kies voor een script dat uit cron draait `#!/bin/bash` als eerste regel: met `#!/usr/bin/env bash` (toegestaan in SCR-01) hangt de gekozen `bash` af van het zoekpad van cron (INFRA-70).
- Bewijs: `crontab -l | /usr/bin/grep -v '^\s*#' | /usr/bin/grep -nE '(^|[^\\])%'` is leeg; elk script uit `crontab -l` zet `PATH` of gebruikt uitsluitend absolute paden; een proefrun met een lege omgeving slaagt: `env -i HOME="$HOME" /bin/sh -c '<de cron-regel>'`. Afgevinkt met de uitvoer van de proefrun.
- Norm: ASVS 5.0.0 V13.2.2 (L2); CWE-426 (zoekpad); past ruim.
- Zie ook: INFRA-69, SCR-18, SCR-38, SCR-39, SCR-36, SCR-41, INFRA-70, BIZ-31

### SCR-38 Geef elke geplande run een harde time-out
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Start elke cron-taak via `timeout -k 30 <duur> <opdracht>` en zet in elke timer-unit `TimeoutStartSec=<duur>` op de bijbehorende `Type=oneshot`-service; kies de duur op ruim de normale looptijd en behandel exitcode 124 als een fout die gemeld wordt.
- Bewijs: `crontab -l | /usr/bin/grep -v '^\s*#' | /usr/bin/grep -E '^[0-9*@]' | /usr/bin/grep -vc 'timeout '` is nul; voor elke timer: `systemctl show -p TimeoutStartUSec <service>` toont een eindige waarde; een proef met een opdracht die niet eindigt (`sleep 999` als vervanger) stopt op de ingestelde tijd met exitcode 124 en de melding komt aan. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V15.2.2 (L2), V15.1.3 (L2).
- Zie ook: INFRA-69, SCR-18, SCR-39, SCR-37, SCR-36, SCR-41, INFRA-70, BIZ-31

### SCR-39 Bepaal per taak wat er gebeurt met een gemiste run
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per geplande taak vast of een gemiste run moet worden ingehaald; zo ja, gebruik een systemd-timer met `OnCalendar=` en `Persistent=true`, of laat het script zelf uitrekenen wat er sinds de laatste geslaagde run openstaat in plaats van "vandaag" te verwerken.
- Bewijs: Een lijst met per taak "inhalen: ja of nee" en waarom; voor elke taak met "ja": `systemctl show -p Persistent <timer>` geeft `yes`, of een test laat zien dat het script na een overgeslagen dag de gemiste items alsnog verwerkt. Afgevinkt met de lijst en de uitvoer.
- Norm: ASVS 5.0.0 V2.3.1 (L1, stappen niet overslaan); past ruim. Zie ARCH-18 (een taak draait meer dan één keer of niet).
- Zie ook: INFRA-69, SCR-18, SCR-38, SCR-37, SCR-36, SCR-41, INFRA-70, BIZ-31

### SCR-40 Plan niets tussen 02:00 en 03:00 en reken in het script met een vaste tijdzone
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Plan geen taak met een vast uur tussen 02:00 en 03:00 lokale tijd als het script zelf op het uur of de datum beslist, zet geen `TZ=` in de crontab in de verwachting dat de planning meeschuift, en laat een script dat op datum of uur beslist de tijdzone expliciet noemen (`TZ=Europe/Amsterdam date`, `zoneinfo.ZoneInfo("Europe/Amsterdam")`).
- Bewijs: `crontab -l | /usr/bin/grep -v '^\s*#' | /usr/bin/grep -nE '^[0-9*,/-]+ +2 '` is leeg; `crontab -l | /usr/bin/grep -nE '^(CRON_)?TZ='` is leeg; `timedatectl show -p Timezone` staat in het runbook; elk commentaar in de crontab noemt dezelfde tijdzone als de server. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V16.2.2 (L2, tijdstempels met expliciete tijdzone); past ruim.
- Zie ook: DB-74, ARCH-12, INFRA-71, BIZ-26, BIZ-27, BIZ-28, BIZ-29, SCR-52

### SCR-41 Kies voor een nieuwe geplande taak een systemd-timer boven cron
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak een nieuwe geplande taak als `.timer` met een `Type=oneshot`-service, met `TimeoutStartSec=`, `OnFailure=`, uitvoer naar het journal en de sandbox uit INFRA-67; gebruik cron alleen als de taak aantoonbaar niets van die vier nodig heeft.
- Bewijs: Voor elke nieuwe taak: `systemctl cat <naam>.timer <naam>.service` toont `OnCalendar=`, `TimeoutStartSec=` en `OnFailure=`; `systemd-analyze security <naam>.service` is beoordeeld (INFRA-67); of er staat een notitie waarom cron volstaat. Afgevinkt met de uitvoer of de notitie.
- Norm: ASVS 5.0.0 V16.3.4 (L2), V15.2.2 (L2); past ruim.
- Zie ook: INFRA-69, SCR-18, SCR-38, SCR-39, SCR-37, SCR-36, INFRA-70, BIZ-31
