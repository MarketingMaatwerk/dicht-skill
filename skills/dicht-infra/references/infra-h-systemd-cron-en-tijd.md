# INFRA H: systemd, cron en tijd

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-66 Geef elke dienst een eigen systeemaccount
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai elke eigen systemd-dienst onder een eigen systeemgebruiker zonder shell, zonder sudo en zonder lidmaatschap van `docker`, en nooit onder het beheeraccount of root.
- Bewijs: `for u in <eigen units>; do systemctl show -p User --value $u; done` toont per dienst een eigen account; `id <account>` toont geen `sudo` en geen `docker`; `sudo -u <account> cat /home/<beheerder>/.ssh/id_ed25519` geeft `Permission denied`. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.2.2 (L2), V13.3.2 (L2).
- Zie ook: INFRA-10, AUTH-56, DB-02, INFRA-97, WP-45, WP-68, AI-21

### INFRA-67 Zet de sandbox van systemd aan op elke eigen dienst
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in elke eigen unit minimaal `NoNewPrivileges=yes`, `ProtectSystem=strict` met expliciete `ReadWritePaths=`, `ProtectHome=yes` (of `read-only`), `PrivateTmp=yes`, `PrivateDevices=yes`, `ProtectKernelTunables=yes`, `ProtectControlGroups=yes`, `RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX` en `CapabilityBoundingSet=` (leeg), en streef naar een score onder 5,0 in `systemd-analyze security`.
- Bewijs: `systemd-analyze security <unit>` met de totaalscore; de score is onder 5,0 of de afwijkende regels zijn verklaard; de dienst is daarna functioneel getest (een sandbox die de dienst breekt, wordt weer uitgezet). Afgevinkt met de uitvoer en de test. De drempel 5,0 is een eigen keuze.
- Norm: ASVS 5.0.0 V13.2.2 (L2), V15.2.5 (L3).

### INFRA-68 Geef een dienst een herstartbeleid en een geheugenlimiet
laag · richtlijn · api | app | mcp · tegenlezer: scherpen (04-10-2026)
- Regel: Zet `Restart=on-failure` met `RestartSec=`, een `MemoryMax=` en een `StartLimitBurst=` op elke eigen unit. Voor een lus of monitor die permanent moet lopen zijn dezelfde instellingen hard, met `StartLimitIntervalSec=` en `OnFailure=` erbij (SCR-42).
- Bewijs: `systemctl show -p Restart,MemoryMax,StartLimitBurst <unit>` toont ingestelde waarden; `systemctl show -p NRestarts <unit>` wordt bewaakt (INFRA-87). Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V15.2.2 (L2).
- Zie ook: SCR-42, SCR-43, SCR-44

### INFRA-69 Laat elke geplande taak een fout melden en voorkom dubbel draaien
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke cron-taak en elke timer een slot (`flock -n`), een log op een vaste plek buiten `/tmp`, en een melding op het alarmkanaal bij een exitcode ongelijk aan nul of bij het uitblijven van een geslaagde run.
- Bewijs: `crontab -l` en `systemctl list-timers` naast een lijst met per taak: slot, logpad, meldweg; een proef waarin de taak met opzet faalt en de melding aankomt. Afgevinkt met de lijst en de proefmelding.
- Norm: ASVS 5.0.0 V16.3.4 (L2), V16.2.3 (L2).
- Zie ook: SCR-18, SCR-38, SCR-39, SCR-37, SCR-36, SCR-41, INFRA-70, BIZ-31

### INFRA-70 Bescherm de scripts die door cron en timers worden uitgevoerd
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zorg dat elk script dat door cron, een timer of een unit wordt gestart alleen schrijfbaar is voor zijn eigenaar (en voor root-taken alleen voor root), gebruik absolute paden, en zet geen geheimen in de crontab-regel zelf.
- Bewijs: Voor elk pad uit `crontab -l`, `sudo crontab -l` en `systemctl cat <unit> | grep Exec`: `stat -c '%a %U %n' <pad>` toont geen schrijfrecht voor groep of anderen en een eigenaar die past bij het uitvoerende account; `grep -nE '(TOKEN|SECRET|PASSWORD|KEY)=' <(crontab -l)` is leeg. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.2.2 (L2), V13.3.1 (L2).
- Zie ook: INFRA-69, SCR-18, SCR-38, SCR-39, SCR-37, SCR-36, SCR-41, BIZ-31

### INFRA-71 Synchroniseer de klok en wees expliciet over de tijdzone
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd tijdsynchronisatie actief, log met een expliciete tijdzone-offset of in UTC, en noteer de tijdzone van de server bij elke geplande taak.
- Bewijs: `timedatectl` toont `System clock synchronized: yes` en de tijdzone; een logregel per dienst toont een offset of `Z`. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V16.2.2 (L2).
- Zie ook: DB-74, ARCH-12, BIZ-26, BIZ-27, BIZ-28, BIZ-29, SCR-40, SCR-52
