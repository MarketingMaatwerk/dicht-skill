# ARCH M: Auditscripts en de audit per project

Compacte regels van `dicht-architectuur`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/architectuur-testen-observability.md` (regelnummer in `regel-index.tsv`).

### ARCH-84 Bouw per projecttype één auditscript dat het bewijs verzamelt
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg de controles die met een opdracht te meten zijn vast in één script per projecttype (`audit-website`, `audit-wp-site`, `audit-api`, `audit-server`) dat per controle de regel-ID, de uitkomst (voldaan, niet voldaan, niet gemeten) en de ruwe uitvoer schrijft, als tabel voor een mens en als JSON voor het bewijsbestand, met exitcode ongelijk aan nul bij een niet-voldane harde regel.
- Bewijs: De scripts staan bij de skill; elke regel die ze meten staat in de kop van het script; een proef tegen een bewust fout ingerichte testsite geeft per fout een "niet voldaan" en een exitcode ongelijk aan nul (GIT-59). Afgevinkt met de uitvoer van de proef. De inhoud per script staat in Open vragen, punt 2.
- Norm: BRIEF besluit 17 en 19; NIST SSDF PO.3.3, PO.4.2.

### ARCH-85 Laat een auditscript alleen lezen, begrensd en zonder geheimen in de uitvoer
hoog · hard · alles · eigen bron · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een auditscript niets wijzigen, alleen opvragen wat een anonieme bezoeker of een leesrol mag zien, met een pauze tussen aanvragen en een maximum per site, zonder actieve aanvalspayloads tegen productie of een klantsite, en maskeer in de uitvoer alles wat op een geheim of een persoonsgegeven lijkt.
- Bewijs: Het script bevat geen schrijvende opdrachten (`grep -nE "POST|PUT|DELETE|wp .* (delete|update|set)|rm |> /" audit-*.sh` is leeg of verklaard); er zit een vaste pauze en een maximum in; de uitvoer van een proefrun bevat geen waarde die de geheimscan herkent. Afgevinkt met de drie controles.
- Norm: BRIEF besluit 19 ("niets wijzigen zonder akkoord").
- Eigen bron: geen primaire bron; bron is de brief (besluit 19) en eigen ervaring. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).

### ARCH-86 Lever de audit van een bestaand project op als lijst van bevindingen, niet als herstel
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Lever een audit van een bestaand project op als lijst met per bevinding de regel-ID, de ernst, het bewijs, het voorstel voor herstel en de inspanning, gesorteerd op ernst, en wijzig niets tot Marketing Maatwerk per bevinding of per groep akkoord geeft; leg wat bewust blijft staan vast als uitzondering (ARCH-30).
- Bewijs: Het auditrapport staat in de repository van het project (`audit/<datum>.md`) met de JSON van het auditscript ernaast; `git status` van de live checkout is na de audit ongewijzigd. Afgevinkt met rapport en status.
- Norm: BRIEF besluit 19; NIST SSDF PW.7.2 ("record and triage all discovered issues and recommended remediations").
