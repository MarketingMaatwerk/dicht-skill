# Het pad voor een wijziging (besluit 27)

Een wijziging van vijf regels krijgt niet de hele checklist, maar wel elke regel die ze raakt. Het pad kiest; het slaat nooit stil over: wat niet is gekozen staat met aantallen in de uitvoer, en wat het profiel op `nvt` zet heeft daar een reden.

## Drie paden

| Pad | Wanneer | Wat het bewijs moet dekken |
|---|---|---|
| `klein` | wijziging aan een bestaand project die aan de definitie hieronder voldoet | de kernregels, de regels van elk geraakt thema, de kritieke regels van elk geraakt domein |
| `gewoon` | elke andere wijziging aan een bestaand project | hetzelfde, plus alle kritieke regels van het profiel |
| `volledig` | nieuw project (`stand: nieuw`), oplevering, geen profiel (een bestaand project krijgt zijn profiel pas bij de audit), of een bewijsbestand zonder `pad` | elke harde regel van de checklist van het projecttype |

De Stop-hook rekent het pad zelf uit. Staat in de kop van het bewijsbestand `pad: klein` en is de wijziging gewoon, dan eist de hook de regels van gewoon en zegt waarom.

## Wat een kleine wijziging is

Alles hieronder moet waar zijn. Het hulpmiddel meet het; het is geen inschatting.

1. Het project bestaat en heeft een geldig `.dicht/profiel.json` in de repo-root (één profiel per repo) met `stand: bestaand`.
2. Hooguit 5 gewijzigde bestanden en 50 gewijzigde regels (toegevoegd plus verwijderd). Lichte bestanden tellen niet mee: tekst en documentatie, beeld, stijl, tests en het bewijs zelf.
3. Geen bestand raakt een patroon van de klasse `gewoon`: migratie of schema, nginx, systemd, cron, Docker, afhankelijkheden en lockfiles, CI, de instelling van de gate, geheimen en omgeving, configuratie, inloggen en rechten, betaling en geld, tenant, webhook, MCP en agentconfiguratie, uitrol, back-up, DNS, firewall, het profiel zelf.
4. Geen trefwoord van de klasse `gewoon` in de code van de gewijzigde regels: een schemawijziging of query, een aanroep naar buiten, een gevaarlijke functie, sessie, token of autorisatie, betaling, tenant, kopregels of CORS, upload, mail versturen, een modelaanroep, een omgevingsvariabele, cryptografie, tracking, een nieuwe ingang in WordPress. Een trefwoord dat alleen in een tekenreeks of in commentaar staat (een gewijzigde zin in een mail), haalt het thema erbij maar maakt de wijziging niet gewoon.
5. Elk bestand past op een patroon, en niets raakt een domein of thema dat het profiel op `nvt` zet.

In gewone woorden: tekst, stijl, een test, of een kleine aanpassing in bestaande code zonder nieuwe gegevensstroom, zonder nieuwe afhankelijkheid, zonder auth, zonder database en zonder configuratie van infrastructuur. De getallen 5 en 50 en de twaalf kernregels zijn vaste waarden (besluit van Marketing Maatwerk, 04-10-2026, `vaste-waarden.md`); ze staan in `tools/regels_voor_wijziging.py` en in `tools/wijziging-patronen.tsv`.

## Zo werkt het

1. Werk in een eigen branch (GIT-01). De wijziging is alles tussen het punt waar de branch van `main` of `master` aftakte en de werkmap, ook wat nog niet is gecommit. Op `main` zelf: alleen de werkmap, of een `basis` in de kop van het bewijsbestand. Een basis mag de wijziging alleen ruimer maken.
2. Draai `python3 tools/regels_voor_wijziging.py --bewijs` in de repo-root. De uitvoer geeft het pad, per bestand het patroon en het trefwoord, per regel de reden, en per domein hoeveel harde regels niet zijn gekozen; `--bewijs` schrijft daarbij het voorgevulde bewijsbestand `bewijs/<datum>-<korte hash>.md` (zie hieronder). `--json` geeft de keuze als gegevens; `--commit <hash>` toetst een bestaande commit (zonder bewijsbestand).
3. Lees elke gekozen regel in de referentie van de sub-skill en lever het bewijs.
4. Vul het voorgevulde bewijsbestand in: de kop (door, runtime, hulpmiddelen, gate, uitzonderingen) en bij elke lege regel de status en het bewijs (`references/bewijsbestand.md`). `pad` en `basis` staan er al in.
5. Draai de gate. Meld pas klaar als geen gekozen regel leeg of `niet gemeten` is.

## Het voorgevulde bewijsbestand

Besluit van Marketing Maatwerk, 04-10-2026. `--bewijs` schrijft per gekozen regel één rij:

- **`nvt` met reden** voor een regel die de wijziging niet raakt. Dat is alleen een regel die enkel meekomt als "kritiek in het profiel": geen gewijzigd bestand en geen trefwoord wijst naar zijn domein. De reden noemt het domein en de basis waartegen is gemeten.
- **Leeg** voor elke andere regel: de kernregels, de regels van een geraakt thema, een regel die zelf is geraakt, en de kritieke regels van een geraakt domein. Die vul je zelf in.
- **Onbekend is nooit afgevinkt.** Past een bestand op geen patroon, is een bestand te groot om helemaal te lezen of is de inhoud niet gemeten, dan vult het hulpmiddel niets voor en zegt het bestand waarom. Een lege status telt bij de Stop-hook als niet afgevinkt, net als `niet gemeten`.
- De voorgevulde `nvt` is een meting op paden en trefwoorden. Weet je dat de wijziging de regel toch raakt (een aanroep in een ander bestand), vervang hem dan door het bewijs.
- Een bestaand bewijsbestand wordt nooit overschreven; een tweede run schrijft een bestand met `-2` erachter. De Stop-hook toetst het nieuwste.
- Onder de tabellen staat per regel waarom hij is gekozen. Harde regels en richtlijnen staan in eigen tabellen; de hook eist de harde.

## Projecten zonder profiel

`.dicht/` staat in de repo-root, met één profiel per repo (besluit van Marketing Maatwerk, 04-10-2026); een map `.dicht/` in een submap wordt door het hulpmiddel en de hook geweigerd. Een bestaand project krijgt zijn profiel bij de audit van dat project (het eigen CRM eerst, besluit 24), niet eerder en niet door een bouwsessie. Tot dan heeft het geen profiel en geldt het volledige pad.

## Hoe de regels worden gekozen

De koppeling staat in `tools/wijziging-patronen.tsv`, één rij per patroon, met wat het raakt: een domein (`GIT`), een thema (`db-d`, het begin van de naam van een referentie) of een regel (`GIT-61`).

| Soort | Betekenis |
|---|---|
| `kern` | de regels die bij elke wijziging gelden (worktree, valideren, expliciet stagen, commit per stap, geen geheim, geheimscan, gate, uitzonderingen, test bij een bugfix, bewijs) |
| `licht` | tekst, beeld, stijl, test, bewijs: telt niet mee voor de omvang, de inhoud wordt niet gelezen |
| `pad` | patroon op het pad van het bestand; elk patroon dat raakt geldt |
| `rest` | alleen als geen `pad`-patroon raakt (overige configuratie) |
| `inhoud` | trefwoord in de toegevoegde en verwijderde regels |
| `profiel` | wat een antwoord uit de intake op `nvt` zet |

Een regel komt mee om één van deze redenen, en de uitvoer noemt de reden: kernregel; zijn thema is geraakt; de regel zelf is geraakt; kritiek in een geraakt domein; kritiek in het profiel (alleen bij gewoon). Een bestand dat op geen patroon past krijgt de kernregels, een melding, en maakt de wijziging gewoon. Voeg dan een patroon toe aan het patronenbestand of aan `paden` in het profiel.

## Wat het pad niet afzwakt

- Een gekozen regel is hard zoals altijd: `voldaan` met bewijs, `nvt` met reden, of `uitzondering` met een geldige regel in `docs/uitzonderingen.md`. `niet gemeten` is nooit afgevinkt.
- `nvt` in een bewijsbestand van een wijziging betekent: deze wijziging raakt de regel niet. De reden zegt waarom, per regel. "Kleine wijziging" is geen reden.
- Alleen Marketing Maatwerk kan een harde regel overrulen. Een overgeslagen stap van de gate is een uitzondering, ook bij een kleine wijziging.
- De gate draait volledig. Het pad kiest regels voor het bewijs, geen controles om over te slaan.
- Kritieke delen (betaling, login, tenant-isolatie) zijn nooit klein, en een wijziging eraan vraagt een tweede paar ogen (ARCH-54).
- Een oplevering vraagt altijd het volledige pad. Een reeks wijzigingen vervangt geen oplevering.

## Grenzen

- Het hulpmiddel kijkt naar paden en trefwoorden. Het ziet niet wat een aanroep in een ander bestand doet. Daarom komen de kritieke regels van een geraakt domein altijd mee, en bij een gewone wijziging de kritieke regels van het hele profiel.
- De keuze is zo goed als het patronenbestand. Mist het pad een regel die je verwacht: neem hem op in het bewijs en vul het patronenbestand aan.
- De hook is de rem, de gate is het bewijs (zie `HOOKS-AUDIT-NOTITIES.md`).
