# INFRA I: Geheimen op de server

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-72 Bewaar geheimen in bestanden met modus 600 buiten elke repository
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet elk geheim in een bestand dat alleen leesbaar is voor het account van de dienst (modus 600 of 400), in een map buiten elke git-werkmap, en nooit in code, een unit-bestand, een Compose-bestand, een image of een crontab.
- Bewijs: `stat -c '%a %U %n' <elk geheimbestand>` toont 600 of 400 en het juiste account; `git -C <repo> ls-files | grep -E '(^|/)\.env|secret|\.key$|\.pem$'` is leeg; `grep -rnE 'Environment=.*(TOKEN|SECRET|PASSWORD|KEY)=' /etc/systemd/system/` is leeg; een geheimscan over de volledige historie (zie GIT) is schoon of elke treffer is ingetrokken dan wel als geaccepteerd risico genoteerd. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V13.3.1 (L2), V13.3.2 (L2); OWASP Top 10 2025 A02. Afwijking: V13.3.1 vraagt op L2 "a secrets management solution, such as a key vault"; bestanden met modus 600 zijn daar een afwijking van zolang OPEN-VRAGEN A13 openstaat. Leg haar vast in het uitzonderingenregister (ARCH-30).
- Zie ook: API-65, GIT-32, GIT-95, DB-62, AI-28, WP-33, INFRA-76, WP-71, DB-61, AI-60, ARCH-49

### INFRA-73 Houd per geheim één bron en een lijst van gebruikers bij
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg voor elk geheim vast: waar de bron staat, welke diensten het lezen, uit welk bestand, en welk commando de dienst het opnieuw laat laden.
- Bewijs: De lijst bestaat en is gecontroleerd tegen de werkelijkheid: per dienst toont `sudo cat /proc/<pid>/environ | tr '\0' '\n' | grep -c <NAAM>` of `docker exec <c> printenv <NAAM> | sha256sum` dezelfde waarde als de bron (vergelijk hashes zonder regeleinde: `tr -d '\n' | sha256sum`). Afgevinkt met de lijst en de vergelijking.
- Norm: ASVS 5.0.0 V13.1.4 (L3), V13.3.1 (L2).

### INFRA-74 Geef elke omgeving eigen geheimen en eigen data
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor ontwikkeling, acceptatie en productie verschillende databasewachtwoorden, API-sleutels en signeersleutels, en gebruik voor betaal- en maildiensten buiten productie de test- of sandbox-sleutels.
- Bewijs: Per geheim de hash per omgeving naast elkaar (`sha256sum` zonder regeleinde): ze verschillen; de betaal- en mailsleutels buiten productie zijn test-sleutels (herkenbaar aan het voorvoegsel van de aanbieder). Afgevinkt met de vergelijking.
- Norm: ASVS 5.0.0 V13.3.1 (L2), V13.3.2 (L2).
- Zie ook: ARCH-48, DB-85, ARCH-50, ARCH-08, WEB-72

### INFRA-75 Oefen het vervangen van een geheim voordat het nodig is
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf per geheim op hoe je het vervangt, voer die stappen minstens één keer uit, en vervang een geheim direct bij een vermoeden van lekken, bij vertrek van iemand met toegang en na elk incident op de host. Aanvulling uit GIT-40: Noteer per geheim ook de uitgever en hoe je het intrekt, en herhaal de proef elk jaar met minstens één geheim dat je echt vervangt; noteer de gevonden afwijkingen.
- Bewijs: Per geheim een datum van de laatste vervanging en de stappen; voor de kritieke geheimen (databasewachtwoord, betaalsleutel, signeersleutel, paneltoken, SSH-sleutel naar klantsites) is de vervanging het afgelopen jaar uitgevoerd. Afgevinkt met de lijst.
    Ook (uit GIT-40): De lijst bestaat (zonder waarden) en de laatste proef heeft een datum binnen twaalf maanden met de gevonden afwijkingen. Afgevinkt met lijst en datum.
- Norm: ASVS 5.0.0 V13.1.4 (L3), V13.3.4 (L3). Op L2 een richtlijn; hard voor de vijf kritieke geheimen.
- Dekt ook: GIT-40
- Zie ook: GIT-36, INFRA-93, WP-79, GIT-54, WP-38

### INFRA-76 Houd geheimen uit commandoregels, logs en shellgeschiedenis
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef een geheim nooit als argument op de commandoregel mee, log het nooit, en zet waarden in een env-bestand altijd tussen enkele aanhalingstekens.
- Bewijs: `grep -rnE '(password|token|secret|key)=' ~/.bash_history | wc -l` is nul of de treffers zijn opgeruimd en de geheimen vervangen; `ps aux | grep -iE 'token|password|secret'` toont geen waarden; een steekproef uit de logs van elke dienst toont geen geheimen (zie ook INFRA-88). Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V16.2.5 (L2), V13.3.1 (L2).
- Zie ook: INFRA-72, API-65, GIT-32, GIT-95, DB-62, AI-28, WP-33, WP-71, DB-61, AI-60, ARCH-49, SCR-19, SCR-20, SCR-05, SCR-13, SCR-16, SCR-50, MSG-41

### INFRA-77 Geef elke dienst een eigen sleutel met de kleinste reikwijdte
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak per dienst een eigen API-sleutel of databasegebruiker met alleen de rechten die die dienst nodig heeft, en beperk de sleutel bij de leverancier tot de IP-adressen van de server waar dat kan (IPv4 en IPv6).
- Bewijs: De lijst uit INFRA-73 toont per dienst een eigen sleutel; bij de leverancier is per sleutel de reikwijdte en de IP-beperking vastgelegd (schermafdruk of API-uitvoer). Afgevinkt met de lijst.
- Norm: ASVS 5.0.0 V13.2.1 (L2), V13.2.2 (L2), V13.3.2 (L2).

### INFRA-78 Zorg dat je zonder de server bij de geheimen kunt
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewaar een versleutelde kopie van alle geheimen en van de sleutels waarmee back-ups zijn versleuteld op een plek buiten de server, en test dat je die kopie zonder de server kunt openen.
- Bewijs: Een herstelproef (INFRA-82) die begint op een lege machine: de geheimen en de back-upsleutel komen uit de externe kopie, niet van de server. Afgevinkt met het verslag van de proef. Zie ook DB-55.
- Norm: ASVS 5.0.0 V13.3.1 (L2).
- Zie ook: DB-46, INFRA-82, DB-53, INFRA-84, DB-55
