# SCR E: Geheimen in scripts

Compacte regels van `dicht-scripts`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/scripts-automatisering.md` (regelnummer in `regel-index.tsv`).

### SCR-19 Geef een geheim door via een bestand of standaardinvoer, nooit als argument
hoog · hard · alles · tegenlezer: scherpen (04-10-2026)
- Regel: Laat het programma een geheim zelf lezen uit een bestand met modus 600 of van standaardinvoer (`curl -K <bestand>`, `curl -H @<bestand>`, `--data @<bestand>`, `PGPASSFILE`, `docker login --password-stdin`, `mysql --defaults-extra-file=`), en bouw nooit een opdrachtregel waarin de waarde zelf staat.
- Bewijs: `/usr/bin/grep -nE '(curl|wget|mysql|psql|docker login|sshpass)[^|#]*(-u|--user|-p ?|--password[= ]|Bearer|token=|key=)[^|#]*\$' $(git ls-files '*.sh')` is leeg of elke treffer leest uit een bestand; tijdens een proefrun toont `ps -eo args` geen waarde van een geheim. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V13.3.1 (L2), V16.2.5 (L2); CWE-214.
- Zie ook: INFRA-76, SCR-20, SCR-05, SCR-13, SCR-16, SCR-50, MSG-41, AI-28

### SCR-20 Zet een geheim alleen in de omgeving van het ene proces dat het nodig heeft
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Exporteer een geheim niet voor het hele script (`set -a; . .env` boven aan een lang script, `export TOKEN=...`), maar geef het alleen mee aan de ene aanroep die het gebruikt (`TOKEN="$(cat "$BESTAND")" programma`), en gebruik in een unit `LoadCredential=` in plaats van `Environment=` voor een geheim.
- Bewijs: Per script met `set -a` of `export`: een lijst van de kindprocessen en welke sleutel elk nodig heeft; `systemctl cat <unit> | /usr/bin/grep -nE '^Environment=.*(TOKEN|SECRET|PASSWORD|KEY)'` is leeg. Afgevinkt met de lijst en de uitvoer.
- Norm: ASVS 5.0.0 V13.3.2 (L2, "access to secret assets adheres to the principle of least privilege").
- Zie ook: INFRA-76, SCR-19, SCR-05, SCR-13, SCR-16, SCR-50, MSG-41, AI-28
