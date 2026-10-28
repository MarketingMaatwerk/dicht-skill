# PRIV D: bewaren en wissen

Compacte regels van `dicht-privacy`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/privacy-compliance.md` (regelnummer in `regel-index.tsv`).

### PRIV-21 Elke gegevenssoort heeft een termijn met een reden, in het register en in de code
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per gegevenssoort een bewaartermijn vast met het startmoment en de reden (doel bereikt, wettelijke plicht, verjaring van een vordering), en zorg dat de termijn in het register dezelfde is als de termijn in de opruimjob.
- Bewijs: Een script vergelijkt de termijnen in het register met de constanten of configuratie van de opruimjobs (DB-83) en meldt verschillen en ontbrekende jobs; de laatste run van elke job staat in het log met een aantal. Afgevinkt met de vergelijking en de logregels. Technisch af te dwingen. De hoogte van een termijn: `[jurist]` waar geen wet hem noemt.
- Norm: AVG artikel 5 lid 1 onder e, artikel 13 lid 2 onder a, artikel 30 lid 1 onder f; ASVS 5.0.0 V14.2.7 (L3).
- Zie ook: DB-83, DB-84, PRIV-24, PRIV-26, DB-78, AI-70, PRIV-22

### PRIV-22 Formulierinzendingen en bestellingen in WordPress krijgen een ingestelde termijn
middel · hard · website | wp-plugin | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Stel op elke WordPress-site in hoe lang formulierinzendingen, bestellingen, accounts van inactieve klanten en afgebroken winkelwagens bewaard worden, of laat inzendingen alleen per mail gaan zonder opslag in de database.
- Bewijs: Per site een regel in de opleverlijst: welke plugin slaat inzendingen op, welke termijn staat ingesteld (voor WooCommerce: Instellingen, Accounts en privacy, onderdeel "Personal data retention" met de velden "Retain inactive accounts", "Retain pending orders", "Retain failed orders", "Retain canceled orders" en "Retain completed orders"; een leeg veld betekent onbeperkt bewaren, dus geen van de vijf is leeg), en een telling `wp db query "SELECT MIN(datum) ..."` van het oudste record per soort die binnen de termijn valt. Afgevinkt met instelling en telling. WooCommerce heeft geen eigen instelling voor afgebroken winkelwagens; die vallen onder "pending orders" of onder de plugin die ze opslaat.
- Norm: AVG artikel 5 lid 1 onder e, artikel 25 lid 2.
- Zie ook: PRIV-21, DB-83, DB-84, PRIV-24, PRIV-26, DB-78, AI-70

### PRIV-23 Geef logs met persoonsgegevens een termijn die het doel dekt en niet meer
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Kies per logsoort een termijn op basis van het doel (storing zoeken: dagen tot weken; beveiligingsonderzoek en datalekbeoordeling: maanden; wettelijk voorgeschreven logging: de wettelijke termijn), leg de afweging vast, en houd IP-adressen en identificatoren uit logs waar het doel ze niet nodig heeft.
- Bewijs: Het logoverzicht uit INFRA-88 met per bron doel, termijn en reden; `logrotate`-configuratie en `journalctl --disk-usage` komen ermee overeen. Afgevinkt met overzicht en configuratie. Technisch af te dwingen.
- Norm: AVG artikel 5 lid 1 onder c en e, artikel 32; ASVS 5.0.0 V16.1.1 en V16.2.5 (L2).
- Zie ook: ARCH-71, PRIV-55, INFRA-88, INFRA-33

### PRIV-24 Leg vast hoe een wisverzoek zich verhoudt tot back-ups
middel · richtlijn · api | app | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Beschrijf per systeem dat gewiste gegevens nog tot het einde van de back-uptermijn in back-ups staan, dat back-ups alleen voor herstel worden gebruikt, en dat na een herstel de lijst van uitgevoerde wisverzoeken opnieuw wordt toegepast (DB-84); houd de back-uptermijn daarom kort (DB-57).
- Bewijs: De passage staat in `docs/privacy.md` en in het antwoordsjabloon voor wisverzoeken; de hersteltest (DB) bevat de stap "wisverzoeken opnieuw toepassen". Afgevinkt met de passage en de teststap. `[jurist]`: dit is de open vraag die DB-84 aan dit domein overdroeg; een primaire bron die dit uitdrukkelijk regelt, is niet gevonden.
- Norm: AVG artikel 17 lid 1, artikel 5 lid 1 onder e en f.
- Zie ook: PRIV-21, DB-83, DB-84, PRIV-26, DB-78, AI-70, PRIV-22

### PRIV-25 Geef elke tijdelijke kopie een einddatum op het moment dat je hem maakt
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet bij elke tijdelijke kopie van persoonsgegevens (bewijskopie bij een incident, migratiebestand, export voor een klant, dump voor een hersteltest) direct een einddatum en een eigenaar in het register of in een bestand naast de kopie, en ruim op die datum op.
- Bewijs: `grep -n -i "tijdelijk" policy-state.yaml` laat bij elke treffer een einddatum zien; een geplande taak of agendapunt bestaat voor die datum; na de datum is het bestand weg (`ls` op het pad). Afgevinkt met de drie. Verwijderen gebeurt na akkoord van Marketing Maatwerk.
- Norm: AVG artikel 5 lid 1 onder e.
