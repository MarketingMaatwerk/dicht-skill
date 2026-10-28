# PRIV I: ongevraagde mail en acquisitie

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-47 Mail een bedrijf alleen ongevraagd op een adres dat het daarvoor zelf heeft bekendgemaakt
hoog · hard · api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Verstuur ongevraagde commerciële mail aan een bedrijf alleen naar een adres dat dat bedrijf zelf heeft bestemd en bekendgemaakt voor het ontvangen van zulke berichten, leg per adres de vindplaats en de datum vast, en mail in alle andere gevallen alleen met aantoonbare voorafgaande toestemming.
- Bewijs: Elke rij in de adressentabel heeft `bron_url`, `gevonden_op` en het soort adres; een query op rijen zonder bron geeft nul; de verzendfunctie weigert een rij zonder bron (test). Afgevinkt met query en test. Technisch af te dwingen. `[jurist]`: of de gebruikte adressen onder lid 3 onder a vallen; dit is niet door een primaire bron beantwoord voor een algemeen info-adres.
- Norm: Telecommunicatiewet artikel 11.7 lid 1 en 3; AVG artikel 6 lid 1 onder f voor de persoonsgegevens.

### PRIV-48 Elk bericht noemt de echte afzender en een werkende afmelding
hoog · hard · api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in elk commercieel bericht de werkelijke identiteit van degene namens wie het wordt verstuurd, een geldig adres of nummer waar de ontvanger kan vragen te stoppen, en een afmeldmogelijkheid die gratis is, zonder inloggen werkt en direct effect heeft.
- Bewijs: Een test op elk verzendsjabloon: de tekst bevat de bedrijfsnaam, een postadres of telefoonnummer en de afmeldzin; de afmeldlink werkt zonder login en zet het adres op de lijst (PRIV-28); de headers bevatten `List-Unsubscribe` en `List-Unsubscribe-Post` (INFRA-63). Afgevinkt met de testuitvoer en een ontvangen bericht. Technisch af te dwingen. De vaste teksten van de eigen lijnen bevatten de afmeldzin letterlijk (eigen regels in `CLAUDE.md`).
- Norm: Telecommunicatiewet artikel 11.7 lid 2, 4 en 7.
- Zie ook: PRIV-28, MSG-07, MSG-08, MSG-09, MSG-13, MSG-49

### PRIV-49 Mail aan eigen klanten mag alleen voor eigen gelijksoortige producten en met afmelding vanaf het begin
middel · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik het adres van een klant voor reclame alleen voor eigen gelijksoortige producten of diensten, en alleen als de klant bij het verzamelen van het adres de kans kreeg zich af te melden en die kans in elk bericht terugkrijgt.
- Bewijs: De bestelstraat toont bij het e-mailveld de afmeldkeuze (e2e-test); de klantentabel legt vast via welk product het adres is verkregen; de verzendfunctie voor reclame filtert op dat product en op de lijst uit PRIV-28. Afgevinkt met test en query. Wat "gelijksoortig" is: `[jurist]`.
- Norm: Telecommunicatiewet artikel 11.7 lid 4.

### PRIV-50 Persoonsgegevens uit openbare bronnen vragen een belangenafweging en informatie aan de persoon
middel · hard · api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg voor acquisitie waarin namen of persoonsgebonden adressen voorkomen de belangenafweging vast, verzamel niet meer dan naam, functie en zakelijk adres, en vertel de ontvanger in het eerste bericht waar zijn gegevens vandaan komen en dat hij bezwaar kan maken.
- Bewijs: Het document met de belangenafweging bestaat en is gedateerd; het eerste bericht bevat de bron en de afmeldzin; de opruimjob voert de termijnen uit (PRIV-21). Afgevinkt met document, sjabloon en logregel van de job.
- Norm: AVG artikel 6 lid 1 onder f, artikel 14, artikel 21 lid 2 en 4.

### PRIV-51 Begrens automatische verzendlijnen met een plafond, een noodstop en een pauze bij twijfel
middel · hard · api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke lijn die zonder mens verstuurt een dagplafond, een noodstop die direct werkt, een automatische pauze bij een bounce, een klacht, een onzekere verzending of een reactie, en een vaste tekst die alleen binnen vastgelegde grenzen varieert.
- Bewijs: Een test per lijn: boven het plafond wordt niets verstuurd; de noodstop houdt een lopende run tegen; een gesimuleerde bounce of reactie zet de lijn op pauze. Afgevinkt met de testuitvoer. Technisch af te dwingen. Zie AI-24 voor goedkeuring door een mens bij acties naar buiten.
- Norm: Telecommunicatiewet artikel 11.7; AVG artikel 24 en 25.
- Zie ook: ARCH-76, AI-79, AI-26, ARCH-77, SCR-46, BIZ-23, SCR-52, MSG-49
