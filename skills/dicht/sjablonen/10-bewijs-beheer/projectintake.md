<!--
Sjabloon: projectintake, in te vullen voor de eerste regel code van een nieuw project of een nieuwe dienst.
Dekt: PRIV-59, PRIV-37, PRIV-01, PRIV-52, PRIV-65, PRIV-70, ARCH-01, ARCH-80 (de verwijzing), AI-02 (de vraag),
      DB-11 (de vraag)
Dekt gedeeltelijk: besluit 27 noemt een kleine-wijziging-pad met intake. Het pad staat in de kern
  (dicht/references/kleine-wijziging.md) en het profiel in dicht/references/intake.md; sectie 8 en 9 verwijzen ernaar.
Plek: docs/intake.md in de repository van het project.
Aanpassen: vul elke regel in. "Weet ik niet" is een antwoord dat eerst opgelost moet worden; laat geen regel leeg.
Controleren: elke vraag heeft een antwoord; het ASVS-niveau per onderdeel staat erin (PRIV-59); de DPIA-toets heeft
  een uitkomst met reden (PRIV-37); de geladen sub-skills volgen uit de antwoorden.
Haal dit commentaarblok weg in het echte bestand.
-->
# Projectintake <project>

Datum: <jjjj-mm-dd> · Door: <wie> · Opdrachtgever: <wie>

## 1. Projecttype

Kies wat geldt (meer dan een kan): website · wp-plugin · wp-thema · api · app · mcp · klantproject

- Wat wordt er gebouwd, in twee zinnen:
- Nieuw project of wijziging aan iets bestaands:
- Stack (besluit 4): WordPress en PHP · TypeScript, Node, React · PostgreSQL met Drizzle · VPS, Docker, nginx
- Architectuur: modulaire monoliet, of afwijking met een ADR (ARCH-01, ARCH-29):

## 2. Datagevoeligheid

| Vraag | Antwoord |
|---|---|
| Welke persoonsgegevens, van wie? | |
| Bijzondere gegevens (gezondheid, BSN, strafrechtelijk)? Zo ja: welke regels gelden (PRIV-12, PRIV-52, PRIV-57) | |
| Wie is verantwoordelijke, wie is verwerker, per gegevensstroom (PRIV-01) | |
| Verwerkersovereenkomst nodig of aanwezig (PRIV-14, PRIV-15) | |
| DPIA nodig: ja of nee, omdat (PRIV-37). Bij ja gaat er geen echte verwerking live voor de DPIA klaar is | |
| Nieuwe verwerking of nieuwe leverancier: register en policy-state.yaml bijgewerkt (PRIV-03) | |
| Bewaartermijn per gegevenssoort (PRIV-21) | |

## 3. ASVS-niveau per onderdeel (PRIV-59)

| Onderdeel | Niveau | Waarom |
|---|---|---|
| De toepassing als geheel | L2 (L1 als ondergrens voor een site zonder login of opslag van persoonsgegevens) | |
| Betaling | L3 | |
| Login en sessie | L3 | |
| Tenant-isolatie | L3 | |

## 4. Tenants

- Een klant of meerdere klanten in dezelfde installatie:
- Tenantmodel (rij met tenant_id, schema per tenant, database per tenant) en waarom (DB-11):
- Zo ja: RLS als vangnet (DB-13 tot en met DB-17) en de isolatietest als gate (DB-22, AUTH-77):

## 5. Betalingen

- Wordt er betaald, en via wie (Mollie):
- Eenmalig, terugkerend, terugbetalen:
- Zo ja: de betaalregels (API-27 tot en met API-45, BIZ) en de mutatiedrempel van 80 procent op de betaalmodule (ARCH-44, besluit 21):
- Kan een consument online een overeenkomst sluiten, en geldt de toegankelijkheidswet (PRIV-65):

## 6. AI

- Zit er een model, agent of MCP-server in:
- Welke invoer is onvertrouwd (mail, websites, documenten, tool-uitvoer) (AI-03):
- Onvertrouwde invoer, gevoelige data en een uitweg naar buiten tegelijk? Dat mag niet in een agent (AI-02):
- Gaan er persoonsgegevens naar een modelleverancier, en staat die in het register (PRIV-83, AI-66):
- Handelt iets zonder menselijke goedkeuring? Zo ja: plafond, noodstop, automatische pauze en een besluit met begin- en einddatum (AI-26):

## 7. Levering aan anderen

- Wordt de software aan anderen verstrekt (plugin, thema, bibliotheek, MCP-server, app), is het maatwerk voor een klant, of een dienst op de eigen server (PRIV-70):
- Zo ja: meldpunt en beleid (PRIV-72, 05-git-ci/SECURITY.md) en SBOM per release (PRIV-75):

## 8. Wat hieruit volgt

- Het profiel: leg de antwoorden vast in `.dicht/profiel.json` volgens dicht/references/intake.md (types, gevoeligheid, tenants, bereikbaar van buiten, AI of MCP, scripts, mail, stand) en controleer het met `regels_voor_wijziging.py --controleer-profiel`.
- Sub-skills die laden (het veld `subskills` van het profiel): <dicht-web, dicht-wordpress, dicht-api, dicht-database, dicht-infra, dicht-git, dicht-ai-mcp, dicht-privacy, dicht-architectuur, dicht-scripts, dicht-invoer, dicht-berichten>
- Checklist: skill/dicht/checklists/<type>.md
- Threat model in vier vragen, voor de eerste regel code (ARCH-80): docs/threat-model.md
- Domeinen en thema's die niet gelden, met de reden (het veld `nvt` van het profiel):

## 9. Wijziging aan dit project

Vastgelegd in dicht/references/kleine-wijziging.md. Per wijziging, zonder nieuwe intake:

- Draai `regels_voor_wijziging.py` in de projectmap: het geeft het pad (klein of gewoon) en de regels die de wijziging raakt, met de reden.
- Verandert een antwoord uit deze intake (een nieuwe gegevenssoort, betaling, tenant, AI, mail, van buiten bereikbaar)? Werk eerst de intake en het profiel bij.
- Bewijs: de gate plus de gekozen regels in een nieuw bewijsbestand met `pad: klein` of `pad: gewoon`.
