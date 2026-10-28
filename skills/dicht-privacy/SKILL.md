---
name: dicht-privacy
description: Regels met bewijs voor wat de wet van de bouw vraagt (persoonsgegevens, verwerkingsregister policy-state.yaml, verwerkers, bewaren en wissen, datalekken, cookies, ongevraagde mail, zorgdata, toegankelijkheid, CRA, NIS2, AI-verordening, betalen). Geen juridisch advies.
---

# dicht-privacy: privacy, wet en normen die de bouw raken

Sub-skill van `dicht` en kern-aanvulling: de kern verwijst er bij elk nieuw project naar. Bevat de 91 regels van domein PRIV in zestien thema's. Dit is geen juridisch advies. De punten die een jurist moet bevestigen staan in `OPEN-VRAGEN.md` onder (b): domeinverkoop onder de Cyberbeveiligingswet (PRIV-77), klantgegevens via de modelproxy (PRIV-83), koude mail naar info-adressen (PRIV-47) en de CRA-status van eigen plugins (PRIV-70). De normteksten van NEN 7510, 7512 en 7513 zijn niet gelezen; thema J steunt op citaten van de Autoriteit Persoonsgegevens en op de wet.

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/priv-a-rol-register-en-policy-state-yaml.md` | PRIV-01 t/m PRIV-06 (6 actief) | rol, register en policy-state.yaml |
| `references/priv-b-grondslag-doel-en-minimale-gegevens.md` | PRIV-07 t/m PRIV-13 (7 actief) | grondslag, doel en minimale gegevens |
| `references/priv-c-verwerkers-subverwerkers-en-doorgifte.md` | PRIV-14 t/m PRIV-20 (7 actief) | verwerkers, subverwerkers en doorgifte |
| `references/priv-d-bewaren-en-wissen.md` | PRIV-21 t/m PRIV-25 (5 actief) | bewaren en wissen |
| `references/priv-e-rechten-van-betrokkenen.md` | PRIV-26 t/m PRIV-30 (5 actief) | rechten van betrokkenen |
| `references/priv-f-datalekken.md` | PRIV-31 t/m PRIV-36 (6 actief) | datalekken |
| `references/priv-g-dpia-en-functionaris-gegevensbescherming.md` | PRIV-37 t/m PRIV-39 (3 actief) | DPIA en functionaris gegevensbescherming |
| `references/priv-h-cookies-opslag-in-de-browser-en-tracking.md` | PRIV-40 t/m PRIV-46 (7 actief) | cookies, opslag in de browser en tracking |
| `references/priv-i-ongevraagde-mail-en-acquisitie.md` | PRIV-47 t/m PRIV-51 (5 actief) | ongevraagde mail en acquisitie |
| `references/priv-j-zorgdata-en-nen-7510-7512-en-7513.md` | PRIV-52 t/m PRIV-58 (7 actief) | zorgdata en NEN 7510, 7512 en 7513 |
| `references/priv-k-owasp-asvs-5-0-0-vertaald-naar-de-stack.md` | PRIV-59 t/m PRIV-64 (6 actief) | OWASP ASVS 5.0.0 vertaald naar de stack |
| `references/priv-l-toegankelijkheid-europese-toegankelijkheidswet.md` | PRIV-65 t/m PRIV-69 (5 actief) | toegankelijkheid (Europese toegankelijkheidswet) |
| `references/priv-m-cyber-resilience-act-software-en-plugins-die-je.md` | PRIV-70 t/m PRIV-75 (6 actief) | Cyber Resilience Act (software en plugins die je levert) |
| `references/priv-n-nis2-en-de-cyberbeveiligingswet.md` | PRIV-76 t/m PRIV-78 (3 actief) | NIS2 en de Cyberbeveiligingswet |
| `references/priv-o-ai-verordening-het-minimum-voor-ai-functies.md` | PRIV-79 t/m PRIV-83 (5 actief) | AI-verordening (het minimum voor AI-functies) |
| `references/priv-p-betalen-mollie-kaartgegevens-bestelknop-bewaarpl.md` | PRIV-84 t/m PRIV-91 (8 actief) | betalen (Mollie, kaartgegevens, bestelknop, bewaarplicht) |

## Wanneer niet

- De technische uitvoering van een eis staat in de sub-skill van dat domein; deze sub-skill geeft de wettelijke basis en het bewijs. Voorbeelden: opruimjob (DB-83), auditlog (AUTH-84, ARCH-64), tweede factor (AUTH-16), derden in de browser (WEB-58, WEB-59).

## Verhouding tot bestaande skills

De bestaande skills (`owasp-security`, `cc-skill-security-review`, `secrets-management`) noemen de AVG alleen als trefwoord en bevatten geen toetsbare privacyregels. Dit domein vult dat aan en dupliceert niets. De regel uit de globale instructies blijft gelden: werk `policy-state.yaml` bij zodra een nieuwe dienst persoonsgegevens verwerkt (PRIV-03).
