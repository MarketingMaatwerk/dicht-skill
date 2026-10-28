# INFRA J: Back-up en herstel van de host

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-79 Bewaar drie kopieën op twee soorten opslag, waarvan één buiten de server
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Zorg dat van alle gegevens die niet opnieuw te maken zijn drie kopieën bestaan, op twee soorten opslag, waarvan minstens één bij een andere aanbieder dan de server.
- Bewijs: Per dataset (databases, uploads, n8n-data, configuratie, geheimen) een regel met de drie locaties en de leeftijd van de jongste kopie per locatie, gemeten met een commando op die locatie. Afgevinkt als elke dataset een kopie buiten de server heeft die jonger is dan het afgesproken verlies (INFRA-84).
- Norm: geen ASVS-eis.
- Zie ook: DB-44, DB-45, DB-49, INFRA-81, GIT-09, INFRA-83, DB-57

### INFRA-80 → DB-45
Samengevoegd: "Versleutel een back-up voordat hij de server verlaat" is gedekt door DB-45. Gebruik die regel.

### INFRA-81 Maak de externe kopie onwisbaar vanaf de server
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Richt de externe opslag zo in dat de server alleen kan toevoegen en niet kan wissen of overschrijven (alleen-toevoegen-sleutel, versiebeheer of onveranderbare opslag), en ruim oude back-ups op vanaf een andere plek.
- Bewijs: Een proef met de inloggegevens van de server: een bestaande externe back-up wissen of overschrijven mislukt, of de vorige versie is daarna nog terug te halen. Afgevinkt met de uitvoer van de proef.
- Norm: geen ASVS-eis.
- Zie ook: DB-44, DB-45, DB-49, INFRA-79, GIT-09, INFRA-83, DB-57

### INFRA-82 Doe elk kwartaal een herstelproef op een lege machine
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Herstel minstens elk kwartaal één volledige dienst (database, bestanden, configuratie, geheimen) op een lege machine uit de externe kopie, meet hoe lang het duurt, en leg datum en uitkomst vast.
- Bewijs: Een verslag met datum, de herstelde dienst, de duur, wat er ontbrak, en een functionele controle (inloggen, een record lezen). Afgevinkt als het verslag jonger is dan drie maanden. Zie DB-46.
- Norm: geen ASVS-eis.
- Zie ook: DB-46, DB-53, INFRA-84, DB-55, INFRA-78

### INFRA-83 Neem de configuratie van de server mee in de back-up
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg nginx-configuratie, Compose-bestanden, systemd-units en drop-ins, crontabs, firewallregels, sshd-configuratie en `daemon.json` vast in git of in de back-up, en de geheimen versleuteld apart.
- Bewijs: Een lijst van de genoemde bestanden met per stuk waar de kopie staat en van wanneer; `diff <(crontab -l) <kopie>` is leeg; `diff -r /etc/systemd/system <kopie>` toont geen eigen units die ontbreken. Afgevinkt met de lijst en de diffs.
- Norm: geen ASVS-eis.
- Zie ook: DB-44, DB-45, DB-49, INFRA-79, INFRA-81, GIT-09, DB-57

### INFRA-84 Leg per dienst vast hoeveel verlies en uitval aanvaardbaar is
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: WET
- Regel: Noteer per dienst het maximale gegevensverlies (RPO) en de maximale hersteltijd (RTO), en toets de back-upfrequentie en de gemeten hersteltijd daaraan.
- Bewijs: Een tabel met per dienst RPO, RTO, back-upfrequentie en de gemeten hersteltijd uit INFRA-82; elke regel waar de meting de afspraak niet haalt heeft een actie. Afgevinkt met de tabel. Zie DB-53.
- Norm: geen ASVS-eis.
- Zie ook: DB-46, INFRA-82, DB-53, DB-55, INFRA-78

### INFRA-85 Reken een snapshot van de hostingpartij niet als de enige back-up
middel · richtlijn · klantproject | api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik snapshots en back-ups van de provider of het panel als snelle terugweg vóór een ingreep, en houd daarnaast een eigen kopie bij een andere partij.
- Bewijs: Per site of server: de snapshots bij de provider (aantal, jongste) en de eigen kopie elders met datum. Afgevinkt met beide.
- Norm: geen ASVS-eis.
