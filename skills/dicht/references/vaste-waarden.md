# Vaste waarden (besluiten van Marketing Maatwerk)

Deze getallen gelden in elke regel waar ze spelen. Een domein dat iets anders noemde, is aangepast (zie `SYNTHESE-NOTITIES.md`).

| Onderwerp | Waarde | Besluit | Regels |
|---|---|---|---|
| Norm | OWASP ASVS 5.0.0 niveau 2; niveau 3 voor betaling, login en tenant-isolatie | 6 | PRIV-59, PRIV-61 |
| Mutatietests op kritieke delen | minstens 80 procent van de mutanten gedood, als poort | 21 | ARCH-44 |
| Hersteltermijn kritiek of actief misbruikt (CISA KEV) | 48 uur, ook voor de herstart die de fix actief maakt en voor software buiten de distributie | 22 | GIT-77, INFRA-24, ARCH-32, WP-49, DB-92, GIT-88, INFRA-21, INFRA-23, MSG-06, SCR-32 |
| Hersteltermijn hoog | 7 dagen | 22 | dezelfde |
| Hersteltermijn middel | 30 dagen | 22 | dezelfde |
| Logkopie buiten de server | dagelijks, versleuteld, audit- en beveiligingslogs, naar eigen opslag | 23 | INFRA-89, ARCH-65 |
| Diensten en agents niet onder het beheeraccount | hard; een uitzondering staat in het register | 25 | INFRA-10, INFRA-66 |
| Architectuur | modulaire monoliet; afwijken vraagt een ADR | 9 | ARCH-01, ARCH-29 |
| Nieuwe afhankelijkheid | korte onderbouwing, lockfile en digest, minimale leeftijd van 7 dagen (het getal is een eigen keuze uit GIT-72) | 16 | GIT-75, GIT-69, GIT-91, GIT-72 |
| Bestaand werk | audit per project, niets wijzigen zonder akkoord; het eigen CRM eerst | 19, 24 | ARCH-86 |
| Geldigheid van links in mail | resetlink 1 uur; magic link die direct inlogt 10 minuten; verificatie en uitnodiging hooguit 24 uur | Marketing Maatwerk, 04-10-2026 (OPEN-VRAGEN A4) | AUTH-25, AUTH-30 |
| Afstemming met Mollie | dagelijks de niet-definitieve betalingen opnieuw ophalen: hard voor elk project met Mollie | Marketing Maatwerk, 04-10-2026 (OPEN-VRAGEN A8) | API-43, BIZ-48, BIZ-49 |
| Partnervergoeding voorlopig | 14 dagen bij iDEAL, 56 dagen bij SEPA-incasso | Marketing Maatwerk, 04-10-2026 (A27) | BIZ-16, BIZ-36 |
| Kopie van een repo buiten de server | met geheimen of klantgegevens: versleutelde bundle in de offsite back-up; anders een privé-remote op GitHub | Marketing Maatwerk, 04-10-2026 (A15) | GIT-09 |
| SheetJS | per project beslissen; de versie van het CDN van de maker mag als uitzondering met hash, reden en einddatum | Marketing Maatwerk, 04-10-2026 (A29) | INV-21, GIT-73 |
| Kleine wijziging | hooguit 5 gewijzigde bestanden en 50 gewijzigde regels; 12 kernregels gelden bij elke wijziging | Marketing Maatwerk, 04-10-2026 | GIT-01, GIT-03, GIT-04, GIT-05, GIT-32, GIT-33, GIT-58, GIT-59, ARCH-30, ARCH-34, ARCH-52, ARCH-53 |
| Profiel | `.dicht/` in de repo-root, één profiel per repo; een bestaand project krijgt het bij zijn audit (het eigen CRM eerst) en volgt tot dan het volledige pad | Marketing Maatwerk, 04-10-2026 | ARCH-52, ARCH-86 |
| Bewaartermijn van back-ups | 14 dagen voor websites; 30 dagen voor webshops en eigen systemen (CRM, registrar) | Marketing Maatwerk, 05-10-2026 | DB-57 |
| Reactie op een gemelde kwetsbaarheid | ontvangstbevestiging binnen 1 werkdag; eerste beoordeling binnen 5 werkdagen (de 5 is een eigen voorstel, geen bron) | Marketing Maatwerk, 05-10-2026 | PRIV-72 |
| Updates van afhankelijkheden | Dependabot, niet Renovate | Marketing Maatwerk, 05-10-2026 | GIT-76, GIT-92 |
| Overige lege plekken in de sjablonen | per project invullen bij de intake, niet bij Marketing Maatwerk: limieten per route, uploadgrootte, dagplafond, aantal fouten van een lus, time-out per stap, dekkingsdrempel (`sjablonen/VASTE-WAARDEN.md`) | Marketing Maatwerk, 05-10-2026 | INFRA-46, API-20, API-18, AI-26, BIZ-23, SCR-43, SCR-38, ARCH-45 |
| Melding datalek | 72 uur na kennisname (wettelijk); staat los van de hersteltermijn | AVG | PRIV-31, INFRA-96 |
| Logging van zorgsystemen | minstens vijf jaar (wettelijk) | NEN 7513 | PRIV-55, INFRA-88 |
