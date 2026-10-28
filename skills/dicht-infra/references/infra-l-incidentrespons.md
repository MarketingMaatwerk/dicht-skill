# INFRA L: Incidentrespons

Compacte regels van `dicht-infra`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/infra.md` (regelnummer in `regel-index.tsv`).

### INFRA-91 Schrijf het draaiboek voordat er iets gebeurt
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd één document bij met: wie beslist, wie je belt (hostingpartij, panelbeheerder, betaalprovider), waar de back-ups en geheimen staan, de stappen uit INFRA-92 tot en met INFRA-95, en de meldplicht uit INFRA-96; en loop het één keer per jaar door.
- Bewijs: Het document bestaat, heeft een datum van de laatste doorloop, en de contactgegevens zijn getest (een echt bericht of telefoontje). Afgevinkt met het document en de datum.
- Norm: geen ASVS-eis; AVG art. 32 en 33 (zie PRIV).
- Zie ook: PRIV-31, INFRA-96, PRIV-32, PRIV-33, PRIV-71, AI-84, GIT-106, WP-78, INFRA-94

### INFRA-92 Isoleer eerst en bewaar bewijs voordat je opruimt
hoog · hard · alles · tegenlezer: scherpen (04-10-2026)
- Regel: Haal bij een vermoeden van inbraak de getroffen dienst van het netwerk of zet hem achter een onderhoudspagina, maak een snapshot en een kopie van de logs, en ruim daarna pas op.
- Bewijs: Bij elk incident een verslag met: tijdstip van isolatie, de snapshot of kopie (naam en datum), en waar de logkopie staat. Afgevinkt met het verslag. Op een klantsite eerst akkoord (eigen ervaring).
- Norm: geen ASVS-eis.

### INFRA-93 Vervang na een inbraak elk geheim dat de getroffen omgeving kon lezen
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Vervang na een bevestigde inbraak alle geheimen die het getroffen account of de getroffen host kon lezen: databasewachtwoorden, API-sleutels, SSH-sleutels, sessiesleutels en salts, en beëindig alle sessies.
- Bewijs: De lijst uit INFRA-73 voor de getroffen omgeving, met per geheim de datum van vervanging na het incident; alle sessies zijn beëindigd (voor WordPress: nieuwe salts). Afgevinkt met de lijst.
- Norm: ASVS 5.0.0 V13.3.4 (L3) naar de geest.
- Zie ook: GIT-36, WP-79, GIT-54, INFRA-75, WP-38

### INFRA-94 Herbouw vanaf een schone bron; ruim alleen op met volledige controle
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Herstel een gecompromitteerde dienst bij voorkeur door hem opnieuw op te bouwen uit git en een back-up van vóór de inbraak; als opruimen de enige weg is, zoek dan op wijzigingstijd van de inode (ctime), controleer kernbestanden tegen checksums, en loop alle automatisch geladen bestanden na.
- Bewijs: Het incidentverslag toont: de gekozen weg (herbouw of opruimen), bij opruimen de uitvoer van de ctime-zoekactie, de checksumcontrole en de controle van automatisch geladen bestanden (voor WordPress: `db.php`, `object-cache.php`, `advanced-cache.php`, `sunrise.php`, mu-plugins; uitwerking in WP), en een herhaalde controle na zeven dagen. Afgevinkt met het verslag.
- Norm: geen ASVS-eis.
- Zie ook: PRIV-31, INFRA-96, PRIV-32, PRIV-33, INFRA-91, PRIV-71, AI-84, GIT-106, WP-78

### INFRA-95 Leg tijdens het incident vast wat je doet en evalueer daarna
middel · richtlijn · alles · tegenlezer: scherpen (04-10-2026)
- Regel: Houd tijdens een incident een tijdlijn bij (tijd, waarneming, actie), en schrijf binnen een week op wat de oorzaak was, wat de detectie had moeten zijn en welke regel of controle erbij komt.
- Bewijs: Het verslag met tijdlijn, oorzaak en de aangepaste controle. Afgevinkt met het verslag.
- Norm: geen ASVS-eis.

### INFRA-96 Beoordeel bij elk incident met persoonsgegevens direct de meldplicht
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: WET
- Regel: Stel bij elk incident binnen 24 uur vast of er persoonsgegevens geraakt kunnen zijn, en leg het voor aan de verantwoordelijke (de klant, of Marketing Maatwerk voor eigen producten) zodat een melding binnen de wettelijke termijn mogelijk is. De wettelijke termijn voor de melding aan de Autoriteit Persoonsgegevens is 72 uur na kennisname (PRIV-31); voor een eigen product onder de Cyber Resilience Act geldt daarnaast de vroegtijdige waarschuwing binnen 24 uur (PRIV-71).
- Bewijs: In het incidentverslag: het tijdstip van ontdekking, de beoordeling, wie is geïnformeerd en wanneer. Afgevinkt met het verslag. De inhoudelijke regels en termijnen staan in PRIV.
- Norm: AVG art. 33 lid 1 (melding uiterlijk 72 uur na kennisname) en lid 2 (de verwerker informeert de verantwoordelijke zonder onredelijke vertraging).
- Zie ook: PRIV-31, PRIV-32, PRIV-33, INFRA-91, PRIV-71, AI-84, GIT-106, WP-78, INFRA-94
