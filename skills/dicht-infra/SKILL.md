---
name: dicht-infra
description: Regels met bewijs voor de server (VPS, SSH, firewall, updates, Docker en Compose, nginx, TLS, DNS en mailauthenticatie, systemd en cron, geheimen, back-up, logging, incidenten, klantsites op hosting). Niet voor CI en images als afhankelijkheid (dicht-git).
---

# dicht-infra: servers, containers en netwerk

Sub-skill van `dicht`. Bevat de 105 regels van domein INFRA in veertien thema's. Vaste waarden: hersteltermijnen 48 uur, 7 dagen, 30 dagen (INFRA-24); dagelijkse versleutelde logkopie buiten de server (INFRA-89); INFRA-10 en INFRA-66 zijn hard.

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/infra-a-toegang-tot-de-server-en-ssh.md` | INFRA-01 t/m INFRA-11 (11 actief) | Toegang tot de server en SSH |
| `references/infra-b-firewall-en-netwerk.md` | INFRA-12 t/m INFRA-19 (8 actief) | Firewall en netwerk |
| `references/infra-c-updates-en-patchbeleid.md` | INFRA-20 t/m INFRA-25 (6 actief) | Updates en patchbeleid |
| `references/infra-d-docker-en-compose.md` | INFRA-26 t/m INFRA-41 (13 actief) | Docker en Compose |
| `references/infra-e-nginx-als-voordeur.md` | INFRA-42 t/m INFRA-49 (7 actief) | nginx als voordeur |
| `references/infra-f-tls-en-certificaten.md` | INFRA-50 t/m INFRA-55 (6 actief) | TLS en certificaten |
| `references/infra-g-dns-en-e-mailauthenticatie.md` | INFRA-56 t/m INFRA-65 (10 actief) | DNS en e-mailauthenticatie |
| `references/infra-h-systemd-cron-en-tijd.md` | INFRA-66 t/m INFRA-71 (6 actief) | systemd, cron en tijd |
| `references/infra-i-geheimen-op-de-server.md` | INFRA-72 t/m INFRA-78 (7 actief) | Geheimen op de server |
| `references/infra-j-back-up-en-herstel-van-de-host.md` | INFRA-79 t/m INFRA-85 (6 actief) | Back-up en herstel van de host |
| `references/infra-k-logging-bewaking-en-alarmering.md` | INFRA-86 t/m INFRA-90 (5 actief) | Logging, bewaking en alarmering |
| `references/infra-l-incidentrespons.md` | INFRA-91 t/m INFRA-96 (6 actief) | Incidentrespons |
| `references/infra-m-klantsites-op-gedeelde-hosting-en-panelen.md` | INFRA-97 t/m INFRA-104 (8 actief) | Klantsites op gedeelde hosting en panelen |
| `references/infra-n-overbelasting-en-ddos.md` | INFRA-105 (1 actief) | Overbelasting en DDoS |

## Wanneer niet

- Images vastzetten op digest, image-scan als poort, geheimen in images: `dicht-git`, thema I. INFRA-34, INFRA-36 en INFRA-38 zijn daarmee samengevoegd.
- Security headers en hun waarden: `dicht-web`. INFRA-49 is samengevoegd met WEB-23.
- Back-up van de database zelf: `dicht-database`, thema E. INFRA-80 is samengevoegd met DB-45.
- WordPress-commando's op een klantsite: `dicht-wordpress`.
- De meldplicht bij een datalek: `dicht-privacy`, thema F.
- Het script dat cron of een timer start (strikte modus, time-out, gemiste run, zomertijd, lussen en monitors): `dicht-scripts`. INFRA-68, INFRA-69 en INFRA-70 verwijzen ernaar.
- Wat de code in een bericht zet, afmelden, bounces en inkomende mail: `dicht-berichten`. Dit domein houdt de DNS-records; INFRA-58 volgt RFC 9989 (`p=reject` alleen zonder menselijke afzenders).

## Verhouding tot bestaande skills

- `docker-expert` dekt niet-root gebruikers, multi-stage builds, healthchecks en Compose-secrets. Hij mist: Docker omzeilt ufw (INFRA-13), `cap_drop`, `no-new-privileges`, `read_only`, pids-limiet, logrotatie en de docker-groep als root (INFRA-10, INFRA-27 tot en met INFRA-33). Het build-voorbeeld daar tagt met `myapp:latest`: GIT-91 gaat voor.
- `secrets-management` gaat over Vault, AWS, Azure en CI-pijplijnen. Voor één VPS met systemd en Compose gelden INFRA-72 tot en met INFRA-78.
