# INFRA K: Logging, bewaking en alarmering

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-86 Bewaak de bereikbaarheid vanaf een plek buiten de server
hoog · hard · api | app | mcp | website | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elke publieke dienst elke paar minuten controleren door een bewaking die niet op dezelfde server en bij voorkeur niet bij dezelfde aanbieder draait.
- Bewijs: Een lijst van bewaakte adressen met de plek waar de bewaking draait; een proef waarbij een dienst kort wordt gestopt op een testomgeving en de melding binnen de afgesproken tijd aankomt. Afgevinkt met de lijst en de proefmelding.
- Norm: ASVS 5.0.0 V16.4.3 (L2) naar de geest (bewaking op een logisch gescheiden systeem).
- Zie ook: ARCH-67, INFRA-35, ARCH-69, INFRA-87, DB-97, DB-47, AI-83, INFRA-52

### INFRA-87 Sla alarm op schijf, geheugen, herstarts, certificaten, back-ups en geplande taken
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel voor elke server alarmen in op: schijf boven 80 procent, een container of unit die herstart of ongezond is, een certificaat onder de drempel (INFRA-52), een back-up ouder dan het afgesproken interval, een geplande taak die faalt of uitblijft (INFRA-69), en een wachtende herstart ouder dan zeven dagen (INFRA-21).
- Bewijs: Per alarm de drempel, het kanaal en een testmelding met datum; `df -h`, `docker ps --filter health=unhealthy` en `systemctl --failed` zijn op het moment van oplevering schoon. Afgevinkt met de tabel en de testmeldingen. De drempel van 80 procent is een eigen keuze.
- Norm: ASVS 5.0.0 V16.3.4 (L2).
- Zie ook: ARCH-67, INFRA-35, ARCH-69, INFRA-86, DB-97, DB-47, AI-83, INFRA-52

### INFRA-88 Roteer logs, geef ze een bewaartermijn en houd geheimen en persoonsgegevens eruit
middel · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Zet voor elke logbron (nginx, containers, journald, eigen logbestanden, cron) rotatie en een bewaartermijn in, leg die vast in één overzicht, en log geen wachtwoorden, tokens, sessie-ID's of volledige querystrings met persoonsgegevens. Uitzondering: de NEN 7513-logging van zorgsystemen bewaar je ten minste vijf jaar en valt buiten de algemene rotatie (PRIV-55).
- Bewijs: Het overzicht (ASVS V16.1.1) met per bron: pad, rotatie, termijn, wie mag lezen; `ls /etc/logrotate.d/` en `journalctl --disk-usage`; een steekproef `grep -iE 'token=|password=|authorization:' <logs>` is leeg. Afgevinkt met het overzicht en de steekproef. De keuze van termijnen hoort in PRIV.
- Norm: ASVS 5.0.0 V16.1.1 (L2), V16.2.3 (L2), V16.2.5 (L2).
- Zie ook: ARCH-62, API-66, DB-88, AUTH-14, AI-67, AI-52, GIT-39, ARCH-71, PRIV-23, PRIV-55, INFRA-33

### INFRA-89 Bescherm logs tegen wijzigen en bewaar een kopie buiten de server
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef diensten alleen schrijfrecht op hun eigen log en geen leesrecht op andere logs, en stuur de beveiligingslogs (sshd, sudo, nginx, de audit-log van de applicatie) naar een tweede systeem. Maak dagelijks een versleutelde kopie van de audit- en beveiligingslogs naar eigen opslag buiten de server (besluit 23).
- Bewijs: `stat -c '%a %U %G %n' /var/log/nginx/* <eigen logs>`; op de eigen opslag staat een versleutelde kopie (`file <nieuwste kopie>` toont een age- of gpg-bestand en geen leesbare tekst); een herstelproef met de sleutel levert leesbare logregels op; de nieuwste kopie is jonger dan 26 uur (`stat -c %y <nieuwste kopie>`). Afgevinkt met de rechten en deze drie controles. Op L2 is V16.4.3 een eis; de dagelijkse versleutelde kopie naar eigen opslag telt als het tweede systeem (besluit 23); zonder die kopie is de regel niet gehaald.
- Norm: ASVS 5.0.0 V16.4.2 (L2), V16.4.3 (L2).
- Zie ook: ARCH-64, AUTH-84, ARCH-65, PRIV-54, DB-91, AI-52

### INFRA-90 Bekijk inlogpogingen en rechtenverhoging periodiek
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bekijk wekelijks de geslaagde SSH-logins, de sudo-regels en de fail2ban-tellers, en vergelijk de geslaagde logins met de lijst uit INFRA-08.
- Bewijs: `journalctl -u ssh --since '7 days ago' | grep -c 'Accepted publickey'` met de lijst van bronadressen en sleutelvingerafdrukken, elk verklaard. Afgevinkt met de uitvoer en de datum.
- Norm: ASVS 5.0.0 V16.3.1 (L2).
