# SCR I: Lange lussen en monitors

Compacte regels van `dicht-scripts`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/scripts-automatisering.md` (regelnummer in `regel-index.tsv`).

### SCR-42 Draai een lus die moet blijven lopen onder een procesbeheerder met een trage herstart en een alarm
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai een monitor of lus die permanent moet lopen als systemd-unit met `Restart=on-failure`, een `RestartSec=` van minstens enkele seconden, `StartLimitIntervalSec=` en `StartLimitBurst=` die bij die pauze passen, `MemoryMax=` en `OnFailure=` naar het alarmkanaal; niet met `nohup`, een losse `tmux`-sessie of `while true; do script; done` in een terminal.
- Bewijs: `systemctl show -p Restart,RestartUSec,StartLimitBurst,StartLimitIntervalUSec,MemoryMax,OnFailure <unit>` toont ingestelde waarden met `RestartUSec` van minstens 5 seconden; een proef waarin de afhankelijkheid één minuut weg is laat de unit daarna vanzelf terugkomen; een proef waarin de unit blijft falen levert een melding op. Afgevinkt met de drie uitvoeren.
- Norm: ASVS 5.0.0 V16.5.2 (L2, blijft veilig werken als een externe bron uitvalt), V15.2.2 (L2).
- Zie ook: INFRA-68, SCR-43, SCR-44

### SCR-43 Laat een lus bij een fout trager gaan, nooit sneller
middel · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke lus een pauze in elk pad (ook het foutpad), een time-out per stap, een oplopende pauze met een maximum bij herhaalde fouten, een kleine willekeurige spreiding, en een melding als hetzelfde blijft falen; laat een lus nooit zonder pauze terugspringen naar het begin.
- Bewijs: Per lus: de code toont een pauze in elk pad en een maximum; een test waarin de stap altijd faalt laat zien dat het aantal pogingen in vijf minuten onder een vooraf genoteerd getal blijft en dat er een melding komt. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V13.1.3 (L3, "where retry logic is implemented, specifying retry limits, delays, and back-off algorithms"), V2.4.1 (L2), V15.2.2 (L2).
- Zie ook: API-48, API-49, ARCH-13, ARCH-14, AI-76, DB-65, API-19, SCR-21, SCR-25, SCR-26, MSG-42, SCR-42, INFRA-68, SCR-44

### SCR-44 Laat een taak die zichzelf opnieuw inplant eerst controleren of er al een exemplaar loopt
hoog · hard · app | mcp | klantproject · eigen bron · tegenlezer: scherpen (04-10-2026)
- Regel: Neem in elke taak die zichzelf herstart of opnieuw inplant (een wekker in een agentsessie, `at`, een script dat zichzelf opnieuw aanroept, een timer die door de taak wordt gezet) als eerste stap een slot of een controle op een lopend exemplaar, en plan alleen opnieuw in als je dat slot hebt.
- Bewijs: Een test waarin de taak wordt gestart terwijl er een exemplaar loopt: het tweede exemplaar stopt zonder werk te doen en zonder een nieuwe ronde in te plannen (aantoonbaar: het aantal geplande rondes blijft één). Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V15.4.1 (L3), V2.4.1 (L2); OWASP LLM Top 10 2026 LLM06 Unbounded Consumption zoals in AI-31 (daar gelezen, hier niet opnieuw).
- Eigen bron: geen primaire bron; de eis komt uit een eigen incident (17-08-2026, eigen ervaring); flock(1) draagt alleen het mechanisme. Opgenomen op besluit van Marketing Maatwerk (04-10-2026).
- Zie ook: SCR-42, INFRA-68, SCR-43
