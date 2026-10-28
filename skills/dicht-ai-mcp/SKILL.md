---
name: dicht-ai-mcp
description: Regels met bewijs voor taalmodellen, prompts, agents, tools, MCP-servers en -clients, RAG en embeddings (prompt injection, modeluitvoer, agentrechten, menselijke goedkeuring, kosten, evals). Niet voor API-beveiliging zonder model (dicht-api).
---

# dicht-ai-mcp: AI-functies, agents en MCP

Sub-skill van `dicht`. Bevat de 86 regels van domein AI in acht thema's. Norm: OWASP Top 10 for LLM Applications, de MCP-specificatie (autorisatie en security best practices), NIST AI 600-1. Uitgangspunt: ontwerp op de aanname dat een injectie slaagt (AI-01, AI-02).

## Zo gebruik je deze sub-skill

1. Kies in de tabel het thema dat de taak raakt en lees alleen dat bestand uit `references/`.
2. Elke regel heeft een ID, ernst, type (hard of richtlijn), de regel, het bewijs en de norm. Hard betekent: zonder bewijs of vastgelegde uitzondering is de taak niet klaar.
   Op de kopregel staat ook het oordeel van de tegenlezer met datum (`niet tegengelezen`: de regel is na de tegenlezing geschreven op besluit van Marketing Maatwerk). `eigen bron` betekent: geen primaire bron, opgenomen op besluit van Marketing Maatwerk. `bron niet gelezen: <code>` betekent: de regel is bevestigd op de bronnen die wel zijn geopend, maar de genoemde norm of wettekst zelf niet; lees een verwijzing naar die norm dus niet als bevestigd. De codes staan in `SYNTHESE-NOTITIES.md`, sectie 10.
3. Waarom, aanvalsvoorbeeld, fout en goed en bron: zoek het ID op in `regel-index.tsv` en lees die plek in `research/` (niet in de publieke export). Na installatie staan `regel-index.tsv` en `SYNTHESE-NOTITIES.md` (alleen de broncodes) in de map van de kern (`~/.claude/skills/dicht/`).
4. Schrijf per regel de status en het bewijs in het bewijsbestand (kern, `references/bewijsbestand.md`).

## Thema's

| Bestand | Regels | Onderwerp |
|---|---|---|
| `references/ai-1-prompt-injection-en-de-grens-tussen-instructie-e.md` | AI-01 t/m AI-10 (10 actief) | Prompt injection en de grens tussen instructie en gegevens |
| `references/ai-2-wat-er-met-de-uitvoer-van-een-model-gebeurt.md` | AI-11 t/m AI-18 (8 actief) | Wat er met de uitvoer van een model gebeurt |
| `references/ai-3-tools-agentrechten-en-menselijke-goedkeuring.md` | AI-19 t/m AI-31 (13 actief) | Tools, agentrechten en menselijke goedkeuring |
| `references/ai-4-een-mcp-server-bouwen.md` | AI-32 t/m AI-54 (23 actief) | Een MCP-server bouwen |
| `references/ai-5-mcp-servers-skills-en-plugins-van-anderen-gebrui.md` | AI-55 t/m AI-64 (10 actief) | MCP-servers, skills en plugins van anderen gebruiken |
| `references/ai-6-gegevens-leveranciers-tenants-en-rag.md` | AI-65 t/m AI-72 (8 actief) | Gegevens, leveranciers, tenants en RAG |
| `references/ai-7-kosten-limieten-en-misbruik.md` | AI-73 t/m AI-76 (4 actief) | Kosten, limieten en misbruik |
| `references/ai-8-testen-uitrol-bewaking-en-incidenten.md` | AI-77 t/m AI-86 (10 actief) | Testen, uitrol, bewaking en incidenten |

## Wanneer niet

- Klassieke invoer-, SQL-, pad- en shellregels: `dicht-api` en `dicht-database`; AI-12, AI-46 en AI-47 verwijzen ernaar.
- OAuth en API-sleutels in het algemeen: `dicht-api`, thema's AUTH-G en AUTH-H.
- De AI-verordening en de verwerkersovereenkomst met een modelleverancier: `dicht-privacy`, thema O en C.
- Schakelaars, alarmering en de plek van evals in de gate: `dicht-architectuur`.

## Verhouding tot bestaande skills

- `prompt-guard` (patroonherkenning) is bruikbaar als extra laag, maar is geen grens: filters op patronen zijn te omzeilen. In deze skill geldt hij alleen als signaal (AI-09). De code haalt standaard patronen op bij een externe dienst; zet dat uit met `PG_API_ENABLED=false` (AI-62). Dat laatste is in de broncode gelezen, niet op het netwerk gemeten.
- `owasp-security`, `api-security-best-practices` en `cc-skill-security-review` noemen AI niet.
- Voor het bouwen met de Claude API: de skill `claude-api`.
