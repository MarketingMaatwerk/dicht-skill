---
name: dicht-berichten
description: Regels met bewijs voor code die berichten verstuurt of ontvangt (mail en afzender, DKIM, afmelden, bounces, sjablonen, inkomende mail en IMAP, verzendlijnen, nieuwsbrieven, contactformulieren, WhatsApp, Discord, Slack, web push). Niet voor DNS-records (dicht-infra).
---

# dicht-berichten: e-mail, berichten en bots

Sub-skill van `dicht` (batch 4, besluit 26). Bevat de 48 regels van domein MSG in zeven thema's. Begint waar de DNS-zone klaar is: wat de code in het bericht zet en wat ze met een ontvangen bericht doet. De vier regels over WhatsApp (MSG-35 tot en met MSG-38) dragen `bron niet gelezen: META`: de documentatie van Meta is alleen via een model gelezen. MSG-10 (afmelding direct verwerken) is samengevoegd met PRIV-28 en MSG-14 (onzekere verzending) met SCR-45.

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/msg-a-afzender-en-verzendroute.md` | MSG-01 t/m MSG-06 (6 actief) | Afzender en verzendroute |
| `references/msg-b-afmelden-bounces-en-klachten.md` | MSG-07 t/m MSG-15, MSG-49 (8 actief) | Afmelden, bounces en klachten |
| `references/msg-c-inhoud-van-uitgaande-berichten.md` | MSG-16 t/m MSG-21 (6 actief) | Inhoud van uitgaande berichten |
| `references/msg-d-mail-ontvangen-ontleden-en-tonen.md` | MSG-22 t/m MSG-34 (13 actief) | Mail ontvangen, ontleden en tonen |
| `references/msg-e-whatsapp-business.md` | MSG-35 t/m MSG-38 (4 actief) | WhatsApp Business |
| `references/msg-f-discord-en-slack.md` | MSG-39 t/m MSG-45 (7 actief) | Discord en Slack |
| `references/msg-g-web-push.md` | MSG-46 t/m MSG-48 (3 actief) | Web push |

## Wanneer niet

- SPF, DKIM, DMARC, null MX, MTA-STS en de eisen van grote ontvangers als geheel: `dicht-infra`, thema G (INFRA-56 tot en met INFRA-64).
- Wie je mag mailen, wat erin moet staan en de afmeldlijst als wettelijke plicht: `dicht-privacy`, thema I (PRIV-47 tot en met PRIV-51, PRIV-28).
- Plafond, noodstop en automatische pauze van een verzendlijn, en de poging vooraf vastleggen: `dicht-scripts`, thema J, en AI-26, ARCH-76.
- Prompt-injectie via inkomende mail: `dicht-ai-mcp` (AI-01 tot en met AI-04).
- De algemene webhookregels (AUTH-58, AUTH-59, DB-68): `dicht-api`. Hier staat wat per kanaal afwijkt.
- Reset- en verificatiemail en magic links: `dicht-api`, thema's AUTH.

## Verhouding tot bestaande skills

Geen van de bestaande skills gaat over mail of berichtenkanalen vanuit code: een zoekopdracht in de `SKILL.md` van elke skill op SMTP, IMAP, nodemailer, DKIM en `List-Unsubscribe` gaf op 04-10-2026 alleen `javascript-testing-patterns`, dat nodemailer gebruikt als voorbeeld van een mock in een test (alleen de `SKILL.md`-bestanden zijn doorzocht, niet hun bijlagen).
