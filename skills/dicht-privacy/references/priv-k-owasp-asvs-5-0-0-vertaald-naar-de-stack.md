# PRIV K: OWASP ASVS 5.0.0 vertaald naar de stack

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-59 Leg per project het ASVS-niveau vast, per onderdeel
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Noteer bij de start van elk project welk ASVS-niveau geldt: L2 voor de toepassing als geheel, L3 voor de onderdelen betaling, login en sessie, en tenant-isolatie, en L1 als ondergrens voor een site zonder login of opslag van persoonsgegevens.
- Bewijs: Een bestand `docs/asvs.md` met: het niveau per onderdeel, de datum, en de ASVS-versie (5.0.0). Afgevinkt als het bestand bestaat vóór de eerste regel code van een nieuw project en bij de oplevering van een bestaand project.
- Norm: ASVS 5.0.0, hoofdstuk "What is the ASVS" (niveaus).
- Zie ook: ARCH-80, ARCH-81, PRIV-37, PRIV-01

### PRIV-60 Maak een toepasbaarheidstabel en verklaar elk hoofdstuk dat vervalt
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in `docs/asvs.md` per ASVS-hoofdstuk of het van toepassing is, en zo nee waarom niet; laat een hoofdstuk alleen vervallen als de functie echt ontbreekt.
- Bewijs: De tabel met 17 regels; bij elk "niet van toepassing" een grep die laat zien dat de functie ontbreekt (bijvoorbeeld `grep -rniE "oauth|openid|jwt|jsonwebtoken" package.json composer.json src/` voor V9 en V10). Afgevinkt met tabel en grep-uitvoer.
- Norm: ASVS 5.0.0, "What is the ASVS" (forking).

### PRIV-61 Deze L3-eisen zijn hard voor betaling, login en tenant-isolatie
hoog · hard · api | app | mcp | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Behandel voor de onderdelen betaling, login en sessie, en tenant-isolatie ten minste deze L3-eisen als blokkerend: 7.5.3 (herbevestiging vóór een zeer gevoelige handeling), 8.3.2 (rechtenwijziging werkt direct door), 8.3.3 (toegang op basis van de rechten van de oorspronkelijke gebruiker, niet van een tussenliggende dienst), 6.3.5 en 6.3.7 (melding bij verdachte inlog en bij wijziging van inloggegevens), 6.3.6 (e-mail niet als authenticatiefactor), 6.3.8 (geen afleiden van geldige gebruikers), 2.4.2 (realistische menselijke snelheid bij transacties), 14.2.6 (alleen de minimaal nodige gevoelige gegevens teruggeven), 14.2.7 (automatisch wissen volgens bewaartermijn) en 16.3.2 op L3 (elke autorisatiebeslissing en elke toegang tot gevoelige gegevens gelogd).
- Bewijs: In `docs/asvs.md` per eis: de domeinregel die hem dekt (bijvoorbeeld AUTH-15 voor 6.3.5, DB-83 voor 14.2.7, AUTH-84 voor 16.3.2) en het bewijs uit die regel. Afgevinkt als alle elf een verwijzing en een bewijs hebben. De nummers en teksten zijn letterlijk gecontroleerd tegen de brontekst.
- Norm: ASVS 5.0.0 V2.4.2, V6.3.5 tot en met V6.3.8, V7.5.3, V8.3.2, V8.3.3, V14.2.6, V14.2.7, V16.3.2 (L3).

### PRIV-62 De documentatie-eisen van ASVS zijn zelf het bewijs: schrijf ze
middel · hard · api | app | mcp | wp-plugin · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Lever bij elk project op L2 ten minste deze drie documenten op: de autorisatieregels per functie en per gegeven (8.1.1) en per veld (8.1.2), de classificatie van gevoelige gegevens met beschermingseisen per klasse (14.1.1 en 14.1.2), en de inventaris van logging per laag (16.1.1).
- Bewijs: De drie documenten staan in de repo; de classificatie is dezelfde als in DB-87, de loginventaris dezelfde als in INFRA-88. Afgevinkt als ze bestaan en de autorisatietests (AUTH) naar de matrix verwijzen.
- Norm: ASVS 5.0.0 V8.1.1 (L1), V8.1.2 (L2), V14.1.1 en V14.1.2 (L2), V16.1.1 (L2).

### PRIV-63 ASVS dekt de AVG niet: gebruik de koppeltabel
middel · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik ASVS als invulling van "passende technische maatregelen" uit artikel 32, en loop voor de rest van de AVG de thema's A tot en met G van dit domein na; neem nooit aan dat een ASVS-niveau AVG-naleving betekent, of omgekeerd.
- Bewijs: De tabel hieronder staat in `docs/asvs.md` met per rij de verwijzing naar het bewijs. Afgevinkt als elke rij een verwijzing heeft.
- Norm: AVG artikel 32 lid 1; ASVS 5.0.0 V14.

### PRIV-64 Herbeoordeel het niveau bij elke wijziging van functie of gegevens
laag · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Loop `docs/asvs.md` opnieuw na zodra een project een login, een betaling, een tweede tenant, een nieuwe soort persoonsgegevens of een AI-functie met toegang tot gegevens krijgt, en bij elke nieuwe ASVS-versie in de verversroutine per kwartaal.
- Bewijs: `docs/asvs.md` heeft een wijzigingslog met datum en aanleiding; de datum is niet ouder dan de laatste wijziging in de lijst van onderdelen. Afgevinkt met de log.
- Norm: ASVS 5.0.0 (niveaukeuze op basis van risico).
