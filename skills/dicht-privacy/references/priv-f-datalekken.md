# PRIV F: datalekken

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-31 Meld een datalek binnen 72 uur na kennisname, ook als het onderzoek nog loopt
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per project een meldprocedure vast waarin staat wie beslist, binnen welke tijd de beoordeling klaar is, en dat de melding bij de Autoriteit Persoonsgegevens uiterlijk 72 uur na kennisname gebeurt tenzij een risico voor betrokkenen onwaarschijnlijk is; ontbrekende informatie lever je later na.
- Bewijs: Het document `docs/incident.md` (of het draaiboek uit INFRA-95) bevat: het meldformulier van de AP als link, wie meldt, de vier verplichte onderdelen van artikel 33 lid 3 (aard en aantallen, contactpunt, waarschijnlijke gevolgen, genomen maatregelen), en een tijdlijn-sjabloon met het tijdstip van kennisname. Afgevinkt als het document bestaat en één keer is doorgelopen met een oefengeval. Niet technisch af te dwingen; de oefennotitie is het bewijs.
- Norm: AVG artikel 33 lid 1, 3 en 4; ASVS 5.0.0 heeft hier geen eis.
- Zie ook: INFRA-96, PRIV-32, PRIV-33, INFRA-91, PRIV-71, AI-84, GIT-106, WP-78, INFRA-94

### PRIV-32 Informeer als verwerker de klant direct, en leg de termijn vast in de overeenkomst
kritiek · hard · klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Informeer de klant voor wie je verwerker bent zodra je van een inbreuk weet, zonder eerst het onderzoek af te ronden, en leg in de verwerkersovereenkomst een concrete termijn (in uren) en een contactadres aan beide kanten vast.
- Bewijs: (1) De verwerkersovereenkomst noemt de termijn en het adres. (2) Het klantoverzicht uit PRIV-04 heeft per klant een contactadres voor incidenten. (3) In het incidentverslag staat het tijdstip waarop de klant is geïnformeerd. Afgevinkt met de drie. Let op de gouden regel: het bericht aan de klant gaat als concept naar Marketing Maatwerk, die verstuurt.
- Norm: AVG artikel 33 lid 2, artikel 28 lid 3 onder f.
- Zie ook: PRIV-31, INFRA-96, PRIV-33, INFRA-91, PRIV-71, AI-84, GIT-106, WP-78, INFRA-94

### PRIV-33 Registreer elk datalek, ook als je het niet meldt
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd één datalekregister bij waarin elke inbreuk staat met de feiten, de gevolgen, de genomen maatregelen en de afweging om wel of niet te melden.
- Bewijs: Een bestand of tabel `datalekregister` met per regel: datum ontdekking, wat, welke gegevens en hoeveel personen, gevolgen, maatregelen, gemeld ja of nee met reden. Afgevinkt als het bestand bestaat (ook als het leeg is) en in het draaiboek genoemd wordt. Niet technisch af te dwingen.
- Norm: AVG artikel 33 lid 5.
- Zie ook: PRIV-31, INFRA-96, PRIV-32, INFRA-91, PRIV-71, AI-84, GIT-106, WP-78, INFRA-94

### PRIV-34 Zorg dat je kunt vaststellen of er toegang is geweest
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewaar toegangslogs van elke plek waar persoonsgegevens te halen zijn (webserver, applicatie, database-audit, objectopslag, back-uplocatie) lang genoeg en buiten het bereik van de aanvaller, zodat je na een ontdekking kunt zeggen of, wanneer en door wie gegevens zijn opgehaald.
- Bewijs: Het logoverzicht uit INFRA-88 (ASVS V16.1.1) noemt per bron de bewaartermijn; voor elke bron met persoonsgegevens is die minimaal de termijn die in het project is gekozen (zie PRIV-23 voor de afweging met opslagbeperking), en een proef laat zien dat een download van een testbestand terug te vinden is. Afgevinkt met overzicht en proef. Technisch af te dwingen.
- Norm: AVG artikel 33 lid 3 onder a, artikel 32 lid 1 onder d; ASVS 5.0.0 V16.2.1, V16.3.2, V16.4.3 (L2).

### PRIV-35 Informeer betrokkenen bij een hoog risico, en weet wanneer versleuteling dat voorkomt
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem in de meldprocedure op dat betrokkenen onverwijld bericht krijgen als het lek waarschijnlijk een hoog risico voor hen oplevert, en versleutel gegevens met een hoog risico (inloggegevens, bijzondere gegevens, kopieën van identiteitsbewijzen, back-ups) zo dat een buitgemaakt bestand onleesbaar is.
- Bewijs: (1) De procedure noemt de drempel en een conceptbericht in gewone taal. (2) Voor elke gegevensklasse "hoog" uit DB-87: versleuteld in rust per kolom of op bestandsniveau met de sleutel op een andere plek (DB-80, DB-45), aangetoond met het commando uit die regels. Afgevinkt met beide.
- Norm: AVG artikel 34 lid 1 tot en met 3, artikel 32 lid 1 onder a.

### PRIV-36 Spreek vooraf af of de verwerker namens de klant mag melden
laag · richtlijn · klantproject | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg in de verwerkersovereenkomst vast of je als verwerker een lek namens de klant bij de AP meldt, en zo ja, laat de klant daarvoor een schriftelijke machtiging tekenen die je bij de melding kunt uploaden.
- Bewijs: De verwerkersovereenkomst bevat de keuze; bij "ja" is de machtiging getekend en opgeslagen bij de klant. Afgevinkt met het document. Niet technisch af te dwingen.
- Norm: AVG artikel 33 lid 1 en 2.
