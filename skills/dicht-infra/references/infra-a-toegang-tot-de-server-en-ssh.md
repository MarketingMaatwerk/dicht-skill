# INFRA A: Toegang tot de server en SSH

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-01 Laat SSH alleen sleutels toe
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `PasswordAuthentication no` en `KbdInteractiveAuthentication no` in de sshd-configuratie van elke server die je beheert.
- Bewijs: `sudo sshd -T | grep -Ei '^(passwordauthentication|kbdinteractiveauthentication|pubkeyauthentication) '` geeft `no`, `no`, `yes`. Daarnaast vanaf een andere machine: `ssh -o PubkeyAuthentication=no -o PreferredAuthentications=password gebruiker@host` eindigt met `Permission denied (publickey)`. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V12.3.1 (L2), V13.2.3 (L2).

### INFRA-02 Verbied inloggen als root
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `PermitRootLogin no` en log in met een persoonlijk account dat via sudo rechten krijgt.
- Bewijs: `sudo sshd -T | grep -i '^permitrootlogin '` geeft `no`; `sudo cat /root/.ssh/authorized_keys` is leeg of bestaat niet. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V13.2.2 (L2).

### INFRA-03 Lees de effectieve configuratie, niet het bestand
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewijs elke sshd-instelling met `sshd -T` en nooit met een blik op `sshd_config`.
- Bewijs: De uitvoer van `sudo sshd -T` (gefilterd op de trefwoorden uit INFRA-01, 02 en 05) zit in de oplevering, samen met `ssh -V` en `ls /etc/ssh/sshd_config.d/`. Afgevinkt als de waarden uit `sshd -T` kloppen.
- Norm: geen ASVS-eis; onderbouwing van het bewijs bij INFRA-01 en INFRA-02.

### INFRA-04 Beperk wie mag inloggen
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `AllowUsers` of `AllowGroups` met alleen de accounts die via SSH binnen moeten komen.
- Bewijs: `sudo sshd -T | grep -Ei '^(allowusers|allowgroups) '` toont de lijst; `getent passwd | awk -F: '$7 !~ /(nologin|false)$/ {print $1}'` toont welke accounts een shell hebben, en elk daarvan is verklaard. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V13.2.2 (L2).

### INFRA-05 Zet doorsturen uit dat je niet gebruikt
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `X11Forwarding no` en `AllowAgentForwarding no`, en zet `AllowTcpForwarding` alleen aan voor de accounts die een tunnel nodig hebben.
- Bewijs: `sudo sshd -T | grep -Ei '^(x11forwarding|allowagentforwarding|allowtcpforwarding) '`; afwijkingen staan in een `Match`-blok met reden. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.2.2 (L2).

### INFRA-06 Demp raadpogingen en houd OpenSSH bij
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai fail2ban met een sshd-jail op elke server met OpenSSH ouder dan 9.8, en vertrouw op `PerSourcePenalties` pas als `ssh -V` 9.8 of hoger meldt.
- Bewijs: `ssh -V`; `sudo fail2ban-client status sshd` toont een actieve jail met tellers; `apt list --upgradable 2>/dev/null | grep -i openssh` is leeg. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V15.2.1 (L1) voor de versie; OWASP Top 10 2025 A03 Software Supply Chain Failures.

### INFRA-07 Geef elke sleutel één doel en beperk automatiseringssleutels
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet bij elke sleutel die door een script of dienst wordt gebruikt de opties `restrict` en, waar het kan, `from="..."` en `command="..."` in `authorized_keys`, en gebruik per doel een eigen sleutel.
- Bewijs: Een lijst van elke regel in elke `authorized_keys` op de server met eigenaar, doel en opties; per private sleutel op de server op welke hosts hij toegang geeft. Afgevinkt als elke automatiseringssleutel `restrict` heeft of de uitzondering is genoteerd.
- Norm: ASVS 5.0.0 V13.2.2 (L2), V13.3.2 (L2).

### INFRA-08 Trek toegang in met een lijst, niet uit het hoofd
middel · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd per server en per klantsite bij welke sleutels en accounts toegang hebben, en loop die lijst na bij elk vertrek, elke gelekte laptop en minstens elk kwartaal.
- Bewijs: De lijst bestaat, heeft een datum van de laatste controle, en is vergeleken met de werkelijke `authorized_keys` op de server zelf (niet alleen met het panel). Afgevinkt met de lijst en de vergelijking.
- Norm: ASVS 5.0.0 V13.3.2 (L2).

### INFRA-09 Hergebruik één SSH-verbinding bij geautomatiseerd werk
middel · richtlijn · klantproject | api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bundel commando's in één SSH-sessie of gebruik `ControlMaster` met `ControlPersist`, en open nooit meer dan acht gelijktijdige verbindingen naar dezelfde host.
- Bewijs: Scripts en agent-opdrachten die SSH gebruiken, tonen één sessie of een `ControlPath`; in een opdracht aan subagents staat de limiet letterlijk. Afgevinkt met het script of de opdrachttekst.
- Norm: geen; beschikbaarheid van de beheerweg.

### INFRA-10 Behandel de docker-groep en wachtwoordloze sudo als root
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat geen dienst, cron-taak of AI-agent draaien onder een account dat in de groep `docker` zit of `NOPASSWD: ALL` in sudoers heeft.
- Bewijs: `id <dienstaccount>` toont geen `docker` en geen `sudo`; `sudo -l -U <dienstaccount>` geeft geen regels; `systemctl show -p User <unit>` toont voor elke eigen unit een eigen account (zie INFRA-66). Afgevinkt met de uitvoer per dienst, of met een genoteerde uitzondering.
- Norm: ASVS 5.0.0 V13.2.2 (L2).
- Zie ook: INFRA-66, AUTH-56, DB-02, INFRA-97, WP-45, WP-68, AI-21

### INFRA-11 Zet beheerschermen niet open op internet
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak beheer- en monitoringinterfaces (databasebeheer, n8n, Uptime Kuma, webterminal, statuspagina's, API-documentatie) alleen bereikbaar via een VPN of een IP-allowlist, of zet er minimaal een eigen login met tweede factor voor.
- Bewijs: Een lijst van alle beheerinterfaces met per stuk de afscherming; per interface een `curl -sI` van buiten het toegestane netwerk die 403 geeft of een verbinding die niet tot stand komt, of een schermafdruk van de ingeschakelde tweede factor. Afgevinkt met de lijst en de uitvoer.
- Norm: ASVS 5.0.0 V13.4.5 (L2).
- Zie ook: AUTH-16, AUTH-82, WP-58, INFRA-98, GIT-14, PRIV-53
