# INFRA C: Updates en patchbeleid

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-20 Laat beveiligingsupdates van het besturingssysteem automatisch installeren
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd `unattended-upgrades` actief met de security-bron in `Allowed-Origins`, en controleer wekelijks dat de laatste run is geslaagd.
- Bewijs: `cat /etc/apt/apt.conf.d/20auto-upgrades` toont beide waarden op `"1"`; `systemctl is-active unattended-upgrades` geeft `active`; `tail -20 /var/log/unattended-upgrades/unattended-upgrades.log` toont een run van de laatste twee dagen zonder fout. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V15.2.1 (L1); OWASP Top 10 2025 A03.

### INFRA-21 Herstart binnen een week na een update die erom vraagt
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Herstart de server binnen zeven dagen nadat `/var/run/reboot-required` is verschenen, of stel `Unattended-Upgrade::Automatic-Reboot "true"` met een vaste tijd in. De zeven dagen gelden voor een kernel- of pakketupdate zonder bekende kritieke kwetsbaarheid; dicht de wachtende update een kritieke of actief misbruikte kwetsbaarheid (CISA KEV), dan valt de herstart binnen de 48 uur van besluit 22 (INFRA-24).
- Bewijs: `ls /var/run/reboot-required 2>/dev/null` is leeg, of het bestand is jonger dan zeven dagen (`stat -c %y`), en jonger dan 48 uur als de wachtende update een kritieke of actief misbruikte kwetsbaarheid dicht; `uname -r` is gelijk aan de nieuwste geïnstalleerde kernel (`ls /boot/vmlinuz-* | sort -V | tail -1`). Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V15.2.1 (L1).

### INFRA-22 Draai een besturingssysteem dat nog beveiligingsupdates krijgt
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Plan de upgrade naar de volgende LTS minstens drie maanden voor het einde van de standaardondersteuning, of neem aantoonbaar Ubuntu Pro (ESM) af.
- Bewijs: `lsb_release -ds` plus de einddatum uit de releasecyclus van Ubuntu; `pro status` als ESM wordt gebruikt. Afgevinkt als de einddatum meer dan drie maanden weg is of de upgrade is ingepland met datum.
- Norm: ASVS 5.0.0 V15.1.1 (L1), V15.2.1 (L1).
- Zie ook: GIT-93, API-72, WP-52, DB-93, INFRA-42, AI-54, SCR-33

### INFRA-23 Geef software van buiten de distributie een eigen updateroute
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak voor elk pakket uit een externe bron (Docker Engine, containerd, Node, Tailscale, Ollama) een keuze: de bron toevoegen aan `Allowed-Origins`, of een vaste maandelijkse updateronde met een controle op achterstand. De maandelijkse ronde is voor updates zonder bekende kwetsbaarheid; een beveiligingsfix volgt de termijnen van besluit 22 (INFRA-24): kritiek of actief misbruikt (CISA KEV) binnen 48 uur, hoog binnen 7 dagen, middel binnen 30 dagen.
- Bewijs: `apt list --upgradable 2>/dev/null` toont geen pakketten van externe bronnen die ouder zijn dan 30 dagen; of `apt-cache policy docker-ce containerd.io` toont `Installed` gelijk aan `Candidate`. Geen pakket van een externe bron heeft een openstaande beveiligingsfix buiten de termijn van INFRA-24. Afgevinkt met de uitvoer en de datum van de laatste ronde.
- Norm: ASVS 5.0.0 V15.1.1 (L1), V15.2.1 (L1); OWASP Top 10 2025 A03.

### INFRA-24 Volg de advisories van wat je draait en leg termijnen vast
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd een lijst bij van elke serverdienst met versie (OpenSSH, Docker, nginx, PostgreSQL, Redis, Node, n8n, Asterisk) en leg per ernst vast binnen hoeveel dagen een beveiligingsupdate erop staat. De termijnen zijn vast (besluit 22, GIT-77): kritiek of actief misbruikt (CISA KEV) binnen 48 uur, hoog binnen 7 dagen, middel binnen 30 dagen.
- Bewijs: De lijst met versies en datum bestaat; per dienst is de laatste advisory-pagina bekeken en staat erbij of de draaiende versie in een kwetsbaar bereik valt; de termijnen staan in het projectdocument. Afgevinkt met de lijst en de termijnen.
- Norm: ASVS 5.0.0 V15.1.1 (L1), V15.2.1 (L1), V15.1.2 (L2).
- Zie ook: GIT-77, ARCH-32, WP-49, GIT-88, DB-92, GIT-61, PRIV-73, MSG-06, SCR-32

### INFRA-25 Haal weg wat niet nodig is
middel · richtlijn · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stop en verwijder diensten, containers, test- en demo-omgevingen en pakketten die geen functie meer hebben, en doe dat bij elke oplevering voor wat het project achterlaat.
- Bewijs: `docker ps --format '{{.Names}}'` en `systemctl list-units --type=service --state=running` naast de lijst uit INFRA-24: elke regel heeft een eigenaar en een doel, of is gestopt. Afgevinkt met de vergelijking.
- Norm: ASVS 5.0.0 V15.2.3 (L2).
