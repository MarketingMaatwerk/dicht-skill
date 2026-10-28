# De intake en het profiel (besluit 27)

Eén keer per project, vóór de eerste regel code, en opnieuw zodra een antwoord verandert. De intake legt in `.dicht/profiel.json` vast welke sub-skills, domeinen en thema's voor dit project gelden. Het uitgebreide formulier met de vragen over register, DPIA en ASVS-niveau is `sjablonen/10-bewijs-beheer/projectintake.md`; het profiel is de samenvatting die de hulpmiddelen lezen.

## Plek en moment (besluit van Marketing Maatwerk, 04-10-2026)

- `.dicht/` staat in de repo-root, met één profiel per repo. Een repo met meer diensten beschrijft ze samen: `types` is de vereniging, een antwoord geldt zodra het voor één dienst geldt, en `paden` wijst een map aan die de algemene patronen niet kennen. Een `.dicht/` in een submap wordt geweigerd.
- Uitzondering (05-10-2026): de git-repo van de thuismap (`~`) is een verzamelmap en geen project. Een project daarin (`~/web-terminal`, `~/klanten/<klant>`) heeft zijn eigen `.dicht/` in de map van het project. In een worktree van de thuisrepo staat het profiel op dezelfde plek onder de worktree.
- Een worktree van een branch van vóór het profiel: de hook voor verplicht laden telt dan het profiel in de hoofdcheckout; het hulpmiddel leest alleen de werkmap, dus haal het profiel op met `git checkout <hoofdbranch> -- .dicht/profiel.json`.
- Nieuw project: de intake vóór de eerste regel code, met `stand: nieuw`.
- Bestaand project: het profiel wordt gemaakt bij de audit van dat project (het eigen CRM eerst, besluit 24), met Marketing Maatwerk. Tot dan is er geen profiel en geldt het volledige pad.
- Sinds 05-10-2026 (opdracht van Marketing Maatwerk: dicht bij alles wat we bouwen) heeft elk bestaand bouwproject een profiel, gemaakt uit een meting van de code met aannames (`door` zegt dat). Zo'n profiel is een beginstand: loop het bij de audit van het project met Marketing Maatwerk na. Zonder profiel weigert de hook `pretool_verplicht.py` elke regel code in een bouwproject.

## De zeven vragen

| Veld | Vraag | Waarden |
|---|---|---|
| `types` | Welk projecttype? Kies elk type dat past: een applicatie met een eigen backend is `api` en `app`. | `website`, `wp-plugin`, `wp-thema`, `api`, `app`, `mcp`, `klantproject` |
| `gevoeligheid` | Welke gevoelige gegevens? | een lijst uit `persoonsgegevens`, `betalingen`, `zorgdata`, of alleen `geen` |
| `tenants` | Eén klant of meerdere in dezelfde installatie? | `een`, `meerdere` |
| `bereikbaar_van_buiten` | Bereikbaar vanaf internet? | `true`, `false` |
| `ai_of_mcp` | Zit er een model, agent of MCP-server in? | `true`, `false` |
| `scripts` | Een script, geplande taak of lus? | `true`, `false` |
| `mail` | Verstuurt of leest het mail of berichten (ook Discord, Slack, WhatsApp, push)? | `true`, `false` |

Daarbij `stand`: `nieuw` (nog niet opgeleverd: altijd het volledige pad) of `bestaand` (het wijzigingspad mag). Twijfel bij een antwoord: kies het antwoord dat meer regels geeft.

## Wat uit de antwoorden volgt

Een antwoord zet een domein (hoofdletters) of een thema (het begin van de naam van een referentie) op `nvt`, met de reden. De tabel staat als gegevens in `tools/wijziging-patronen.tsv` (soort `profiel`); dit is dezelfde tabel.

| Antwoord | Op nvt |
|---|---|
| geen `persoonsgegevens` | `priv-b`, `priv-d`, `priv-e`, `priv-g` |
| geen `betalingen` | `api-e`, `biz-b`, `priv-p`, `wp-n` |
| geen `zorgdata` | `priv-j` |
| `tenants`: `een` | `auth-j`, `db-b` |
| niet bereikbaar van buiten | `infra-e`, `infra-f`, `infra-n`, `web-13` |
| geen AI of MCP | `AI`, `priv-o` |
| geen scripts | `SCR` |
| geen mail of berichten | `MSG`, `priv-i` |

Het projecttype doet de rest: een regel die niet voor het type geldt, staat niet in de checklist. De sub-skills zijn die waarvan na aftrek van `nvt` nog een regel voor het type overblijft.

## Formaat van `.dicht/profiel.json`

```json
{
  "versie": 1,
  "project": "voorbeeld-api",
  "datum": "2026-10-04",
  "door": "Marketing Maatwerk",
  "stand": "bestaand",
  "types": ["api"],
  "gevoeligheid": ["persoonsgegevens"],
  "tenants": "een",
  "bereikbaar_van_buiten": true,
  "ai_of_mcp": false,
  "scripts": true,
  "mail": false,
  "subskills": ["dicht-api", "dicht-architectuur", "dicht-database", "dicht-git", "dicht-infra", "dicht-invoer", "dicht-privacy", "dicht-scripts", "dicht-web"],
  "nvt": {
    "api-e": "het project kent geen betalingen",
    "biz-b": "het project kent geen betalingen",
    "priv-p": "het project kent geen betalingen",
    "wp-n": "het project kent geen betalingen",
    "priv-j": "het project verwerkt geen zorgdata",
    "auth-j": "het project heeft een tenant",
    "db-b": "het project heeft een tenant",
    "AI": "het project heeft geen model, agent of MCP-server",
    "priv-o": "het project heeft geen model, agent of MCP-server",
    "MSG": "het project verstuurt en leest geen mail of berichten",
    "priv-i": "het project verstuurt en leest geen mail of berichten"
  }
}
```

- Alle velden zijn verplicht; een onbekend veld is een fout. `paden` is het enige vrije veld: een eigen bestandspatroon met de domeinen, thema's of regels die het raakt, voor een map die de algemene patronen niet kennen, bijvoorbeeld `"paden": {"^wp/.*\\.js$": ["web-1"]}`. Een eigen pad gaat voor op de algemene patronen.
- `nvt` bevat minstens wat uit de antwoorden volgt. Een extra domein of thema mag erbij met een eigen reden (bijvoorbeeld `"DB": "geen database"`); dat is een besluit dat in de diff van het profiel zichtbaar is.
- `subskills` is afgeleid en moet kloppen. Uitzondering sinds 22-10-2026: een profiel van een website, wp-thema of klantproject van daarvoor noemt `dicht-anti-vibe` nog niet en blijft geldig; de hook vraagt die sub-skill dan via de projecttypes bij een voorkantbestand. Een nieuw profiel noemt hem wel.
- Controleren: `python3 tools/regels_voor_wijziging.py --controleer-profiel`. Bij een fout zegt de melding wat `nvt` mist en wat `subskills` moet zijn. Een ongeldig profiel blokkeert de klaar-melding.

## Wat het profiel doet

- **Volledig pad**: een regel in een domein of thema dat op `nvt` staat, telt als afgevinkt met de reden uit het profiel. Eén reden in plaats van tientallen regels `nvt` in het bewijsbestand.
- **Wijzigingspad**: het profiel bepaalt het projecttype, de kritieke regels die bij een gewone wijziging meekomen en wat niet meekomt. Raakt een wijziging iets wat op `nvt` staat (een modelaanroep in een project zonder AI), dan komen de regels toch mee, is de wijziging niet klein, en zegt het hulpmiddel dat de intake moet worden bijgewerkt.
- Een wijziging aan het profiel zelf is nooit een kleine wijziging.
