# ruleset-main.json en ruleset-tags.json

Dekt: GIT-24 (ruleset-main.json), GIT-25, GIT-26 (ruleset-tags.json, zonder "release immutability")

Status: dekt gedeeltelijk. Gevalideerd op 04-10-2026 tegen de OpenAPI-beschrijving van GitHub (github/rest-api-description, versie 1.1.4, het schema van POST /repos/{owner}/{repo}/rulesets): beide bestanden zonder fout, ook met onbekende sleutels verboden; een verzonnen regeltype en een ontbrekende verplichte parameter worden wel afgekeurd. Niet ingestuurd naar een repository: of het plan rulesets toelaat en of `~DEFAULT_BRANCH` wordt aangenomen blijkt pas daar (het schema ziet die waarde als gewone tekst).

## Wat erin staat

- `ruleset-main.json`: de zes eisen uit GIT-24: force-push geblokkeerd (`non_fast_forward`), verwijderen geblokkeerd (`deletion`), ondertekende commits verplicht (`required_signatures`), een pull request verplicht (`pull_request`), de gate verplicht (`required_status_checks` met de job `gate` uit `.github/workflows/gate.yml`, GIT-53) en een lege `bypass_actors`.
- Bewust niet: `required_linear_history` (GIT-25: de werkwijze gebruikt een merge-commit).
- `ruleset-tags.json`: bijwerken en verwijderen van `v*` geblokkeerd (GIT-26).

## Wat uit de bron komt en wat niet

- Uit de bron (GIT-24, bewijs): de regeltypes `non_fast_forward`, `deletion`, `required_signatures`, `pull_request`, `required_status_checks` en het veld `bypass_actors`.
- Niet uit de bron: de namen van de parameters onder `pull_request` en `required_status_checks`, de vorm van `conditions`, `~DEFAULT_BRANCH`, en het regeltype `update` in de tag-ruleset. Ze zijn op 04-10-2026 nagelezen in de OpenAPI-beschrijving van GitHub en kloppen met het schema.
- `required_approving_review_count` staat op 0: de bron zegt dat een pull request geopend moet zijn maar niet goedgekeurd hoeft te worden; bij een tweede persoon met schrijfrecht hoort daar review van CODEOWNERS bij (GIT-29).

## Gebruik (een bewuste handeling van Marketing Maatwerk, niet van een sessie)

```
gh api repos/<eigenaar>/<repo>/rulesets --method POST --input ruleset-main.json
gh api repos/<eigenaar>/<repo>/rulesets --method POST --input ruleset-tags.json
```

Eerst vaststellen of het plan rulesets toelaat (GIT-23): op een privé-repo van een persoonlijk account zonder Pro bestaan ze niet; dan geldt de lokale hook `.githooks/pre-push` (GIT-58).

"Enable release immutability" (GIT-26) is een instelling van de repo en zit niet in dit bestand; of het op een privé-repo van een persoonlijk account werkt is in het onderzoek niet bevestigd.

## Controleren (GIT-24, GIT-26)

```
gh api repos/<o>/<r>/rulesets --jq '.[]|{name,enforcement,target}'
gh api repos/<o>/<r>/rulesets/<id>
git push --force origin v<bestaand>      # wordt geweigerd
```
