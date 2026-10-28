# SCR K: Scripts die een terminal of een AI-agent aansturen

Compacte regels van `dicht-scripts`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/scripts-automatisering.md` (regelnummer in `regel-index.tsv`).

### SCR-48 Stuur tekst naar een tmux-venster als letterlijke tekst en de Enter apart
middel · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Verstuur tekst met `tmux send-keys -t <doel> -l -- "$tekst"` en de `Enter` in een aparte aanroep; gebruik voor tekst van meer dan één regel `tmux load-buffer` met `paste-buffer`; verstuur nooit een variabele zonder `-l`.
- Bewijs: `/usr/bin/grep -rnE 'send-keys[^|;]*\$' . | /usr/bin/grep -v -- ' -l'` is leeg; een test met de teksten `Enter`, `C-c` en `-t x` laat zien dat ze als tekst in het venster verschijnen. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V1.2.5 (L1), V1.3.3 (L2); CWE-88; past ruim.

### SCR-49 Typ pas als het scherm in de verwachte toestand staat, en stop bij elk onbekend scherm
hoog · hard · app | mcp | klantproject · eigen bron · tegenlezer: bevestigd (04-10-2026)
- Regel: Lees het venster (`tmux capture-pane -p`) en controleer op een exact kenmerk van het invoerveld voordat een script tekst verstuurt; bevestig alleen dialogen die het script op hun letterlijke tekst herkent en waarvoor de bevestiging vooraf is besloten; stop met een fout en een verwijzing naar het venster bij een time-out of een onbekend scherm.
- Bewijs: Het script bevat een wachtlus op een exact kenmerk met een eindige grens en een exitcode ongelijk aan nul; een test met een venster dat een andere dialoog toont eindigt zonder dat er tekst is verstuurd. Afgevinkt met de testuitvoer. Welke dialogen het script zelf mag bevestigen staat als lijst in het script, met datum en besluit.
- Norm: ASVS 5.0.0 V2.3.1 (L1, stappen in de verwachte volgorde); past ruim. Zie AI-24 en AI-25 voor goedkeuring buiten het model.
- Eigen bron: geen primaire bron; de eis komt uit een eigen incident (28-09-2026, aantekeningen in het eigen startscript); tmux(1) draagt alleen het mechanisme. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Zie ook: SCR-51, SCR-50, AI-01, AI-24, AI-25

### SCR-50 Geef een prompt met gegevens door via standaardinvoer of een bestand, nooit als argument
hoog · hard · app | mcp | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Geef een prompt die klantgegevens, mailtekst of andere inhoud van buiten bevat aan een agent door via standaardinvoer of een bestand met modus 600; zet in de opdrachtregel alleen een vaste tekst of de naam van een vaste opdracht; zet nooit een geheim in een prompt.
- Bewijs: `/usr/bin/grep -rnE '(claude|codex|llm|ollama)[^|;]* -p +"[^"]*\$' . <(crontab -l)` is leeg; tijdens een proefrun toont `ps -eo args` geen inhoud van buiten; de geheimscan over de promptbestanden is schoon. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V16.2.5 (L2), V13.3.1 (L2); CWE-214.
- Zie ook: INFRA-76, SCR-19, SCR-20, SCR-05, SCR-13, SCR-16, MSG-41, AI-28, SCR-51, SCR-49, AI-01, AI-24, AI-25

### SCR-51 Wie bij de tmux-socket of de lokale aansturing kan, bestuurt de agent
hoog · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd de map met tmux-sockets op modus 700 en elke socket zonder rechten voor anderen, laat een lokale dienst die sessies start of toetsen doorgeeft alleen op `127.0.0.1` of een unix-socket luisteren met authenticatie op elk verzoek, en behandel tekst die een script van het ene venster naar het andere doorgeeft als onvertrouwde invoer (AI-01).
- Bewijs: `stat -c '%a %U' /tmp/tmux-$(id -u)` geeft `700`; `ss -ltnp | /usr/bin/grep <poort>` toont `127.0.0.1` en een verzoek zonder sleutel wordt geweigerd; in elk script dat tekst tussen vensters doorgeeft is te zien dat de tekst als gegevens wordt gemarkeerd en niet als opdracht wordt uitgevoerd (AI-01, AI-12). Afgevinkt met de drie controles.
- Norm: ASVS 5.0.0 V13.2.1 (L2, verkeer tussen onderdelen is geauthenticeerd), V13.2.2 (L2).
- Zie ook: SCR-49, SCR-50, AI-01, AI-24, AI-25
