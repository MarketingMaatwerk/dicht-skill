---
description: Draait het auditscript van de skill dicht voor het projecttype en schrijft het bewijsbestand (alleen lezen, niets wijzigen)
argument-hint: "[type] [--url URL] [--server] [--wp MAP | --wp-ssh gebruiker@host:/pad]"
---

# /dicht-audit

Audit van dit project volgens de skill `dicht` (ARCH-84, ARCH-85, ARCH-86). De audit leest alleen; herstellen is een aparte stap na akkoord van Marketing Maatwerk.

Argumenten: $ARGUMENTS

## Stappen

1. **Projecttype.** Neem het type uit de argumenten, anders uit `.dicht/project` (regel `type: <type>`). Geldig: `website`, `wp-plugin`, `wp-thema`, `api`, `app`, `mcp`, `klantproject`. Staat het nergens, vraag het dan; raad niet.
2. **Bereik.** `--pad` is de map van het project (standaard de huidige map). `--url` alleen voor een eigen site of dienst, of een klantsite waarvoor Marketing Maatwerk akkoord gaf (GIT-64): het script doet per host hooguit 40 anonieme GET-aanvragen met een pauze, zonder POST en zonder payloads. `--server` meet deze server (cron, systemd, poorten, Docker, updates). `--wp` of `--wp-ssh` draait WP-CLI als het account van de site (WP-68), nooit als root.
3. **Draai** het script voor het type en lees de hele uitvoer:

   ```
   ~/.claude/skills/dicht/audit/audit-<type> --pad . [--url <URL>] [--server] [--wp-ssh <doel>:<pad>]
   ```

   Exitcode 1 betekent: minstens één harde regel is niet voldaan. Exitcode 2 is een fout in het script zelf: meld die letterlijk en concludeer niets.
4. **Bewijsbestand.** Het script schrijft `bewijs/<datum>-<hash>.md` (kolommen Regel, Status, Bewijs) en dezelfde gegevens als `.json`. Status `niet gemeten` is nooit `voldaan`. Een controle die maar een deel van het bewijs van een regel dekt, staat er als `niet gemeten` met "deelcontrole geslaagd" en wat met de hand nog moet. Elke regel die niet te automatiseren is, staat er met "handmatig:" en de vraag wat te controleren.
5. **Handmatige regels.** Loop ze per sub-skill na met de referentie van de regel (daar staat het volledige bewijs). Schrijf de uitkomst in een nieuw bewijsbestand; wijzig een bestaand bewijsbestand niet. `nvt` alleen met een reden. Een uitzondering alleen na akkoord van Marketing Maatwerk, in `docs/uitzonderingen.md` met datum, reden en verloopdatum.
6. **Rapport (ARCH-86).** Lever bij een bestaand project een lijst van bevindingen op in `audit/<datum>.md`: per bevinding regel-ID, ernst, bewijs, voorstel voor herstel en inspanning, gesorteerd op ernst. Wijzig niets tot Marketing Maatwerk per bevinding of per groep akkoord geeft. Controleer na afloop dat `git status` alleen de nieuwe bestanden in `bewijs/` en `audit/` toont.

## Grenzen

- Geen wijziging aan code, configuratie, server of site. Geen POST, geen inlogpoging, geen scan met payloads.
- Geen geheimen lezen of tonen: het script maskeert zijn uitvoer; neem zelf ook geen waarde uit `.env`, een unit of een configuratie over.
- Zeg bij elke conclusie of ze gemeten is. Wat het script niet kon meten (ONBEKEND) is niet in orde en niet fout: het is niet gemeten.
