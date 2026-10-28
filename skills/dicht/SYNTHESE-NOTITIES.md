# Broncodes

Uit de synthese-notities; de rest van de notities is niet publiek.

## 10. Regels waarvan de bron niet (volledig) is gelezen

Deze 62 regels zijn door de tegenlezer bevestigd op de bronnen die wel zijn geopend, maar de norm of wettekst hieronder is niet gelezen. Ze staan in de skill met `bron niet gelezen: <code>` op de kopregel, in de checklist en in de index (kolom `bron_niet_gelezen`); een verwijzing naar die norm leest dus nooit als bevestigd. De lijst staat in `tools/synthese.py` (`BRON_NIET_GELEZEN`).

| Code | Wat niet is gelezen | Regels |
|---|---|---|
| NEN | NEN 7510, 7512 en 7513: betaalde normen, de normtekst is niet geopend; gelezen zijn het zorgbesluit, de Staatscourant, de AP-besluiten en de inhoudsopgave | PRIV-52, PRIV-53, PRIV-54, PRIV-55, PRIV-56, AUTH-16, AUTH-84, DB-44, DB-46, DB-53, DB-91, ARCH-64, ARCH-71, INFRA-88, AI-72 |
| PCI | PCI DSS v4.0.1 eis 6.4.3 en 11.6.1 en SAQ A: niet gelezen; gelezen zijn de blog en FAQ 1588 van de PCI SSC | PRIV-84, PRIV-85 |
| SEPA | SEPA-rulebook: niet gelezen; gelezen is alleen de documentatie van Mollie | PRIV-87 |
| CBW | Cyberbeveiligingswet: bijlage 1 en 2 en de artikelen 9 tot en met 11, 42 en 47 zijn niet gelezen | PRIV-76, PRIV-77 |
| CIS | CIS Benchmarks (Docker, PostgreSQL, Ubuntu): achter een registratie, niet gelezen; een CIS-nummer in het veld Norm is niet bevestigd | GIT-63, GIT-66, GIT-91, GIT-92, GIT-94, GIT-95, GIT-96, GIT-99, DB-04, DB-58, DB-59, INFRA-19 |
| WET | AVG artikel 32 en 33 en de tekst van de Cyber Resilience Act: voor deze regels niet bij de officiële bron geopend door de tegenlezer van INFRA en GIT (EUR-Lex gaf een lege pagina); de tegenlezers van DB en PRIV hebben dezelfde teksten wel gelezen via het Publicatiebureau | INFRA-84, INFRA-96, GIT-101 |
| AGENTIC | OWASP Top 10 for Agentic Applications 2026: de lijst zelf is niet geopend; de tien namen zijn bevestigd via de kruistabel in de OWASP LLM-lijst 2026, de publicatiedatum niet | AI-01, AI-02, AI-06, AI-10, AI-12, AI-17, AI-19, AI-21, AI-25, AI-26, AI-27, AI-29, AI-30, AI-47, AI-55, AI-58, AI-59, AI-62, AI-69, AI-86 |
| AI-VO | AI-verordening artikel 5 en 6 en bijlage III en de praktijkcode voor het markeren van AI-inhoud: niet gelezen; de regels eisen alleen dat je rol en risico vastlegt | PRIV-80, PRIV-81 |
| EDPB | EDPB Guidelines 01/2025 over pseudonimisering: alleen de indexpagina gelezen, die een gesloten raadpleging toont en geen definitieve versie | DB-86 |
| META | Documentatie van Meta voor de WhatsApp Cloud API (developers.facebook.com): met curl niet te lezen (HTTP 400); de citaten zijn twee keer onafhankelijk via WebFetch opgehaald (een model leest de pagina) en niet in de ruwe brontekst teruggevonden | MSG-35, MSG-36, MSG-37, MSG-38 |
