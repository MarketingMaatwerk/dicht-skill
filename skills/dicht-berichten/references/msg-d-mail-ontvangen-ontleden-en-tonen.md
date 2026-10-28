# MSG D: Mail ontvangen, ontleden en tonen

Compacte regels van `dicht-berichten`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/email-berichten-bots.md` (regelnummer in `regel-index.tsv`).

### MSG-22 Vertrouw From niet: beslis op het oordeel van je eigen ontvangende server
kritiek · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat geen enkele beslissing (bekende klant, vertrouwde afzender, lijn pauzeren, ticket sluiten, afmelden, een opdracht uitvoeren) afhangen van het From-adres alleen; lees de kop `Authentication-Results` met de naam van je eigen mailserver, negeer elke andere, eis `dmarc=pass` voor het From-domein, en eis voor een actie per mail daarnaast een onraadbaar token in het antwoordadres of het onderwerp.
- Bewijs: Een test met drie opgeslagen berichten: (a) echt bericht met `dmarc=pass` van de eigen server, (b) hetzelfde From zonder geldige uitkomst, (c) hetzelfde From met een meegestuurde valse `Authentication-Results` op een andere servernaam. Alleen (a) krijgt het label vertrouwd; (b) en (c) worden als onbekend behandeld en tonen een waarschuwing. De servernaam staat in de configuratie. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V6.3.6 (L3, mail niet als authenticatiemiddel) naar de geest; AI-03 (vertrouwensniveau per bron).
- Zie ook: AI-03, MSG-24, MSG-25, MSG-31, MSG-33

### MSG-23 Toon HTML-mail alleen opgeschoond, in een sandbox zonder scripts en zonder verzoeken naar buiten
kritiek · hard · app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Toon de HTML van een ontvangen bericht alleen na opschoning met een allowlist-bibliotheek, in een `iframe` met `sandbox` zonder `allow-scripts` en zonder `allow-same-origin`, met een CSP die scripts verbiedt en afbeeldingen van buiten standaard blokkeert; toon platte tekst als tekst en maak links daarin zelf klikbaar via DOM-functies, niet via tekstvervanging naar HTML.
- Bewijs: Een e2e-test die vier berichten opent (een `<script>`, een `<img onerror>`, een SVG met `<animate>` en `onbegin`, een platte tekst met `javascript:`-link) en controleert dat geen ervan een verzoek doet of een dialoog opent, en dat een bericht met een externe afbeelding geen netwerkverzoek naar die host geeft tot de gebruiker erom vraagt. In de code: `grep -rnE "dangerouslySetInnerHTML|innerHTML|v-html|textToHtml" <mailweergave>` is per treffer verklaard. Afgevinkt met de testuitvoer en grep. Het attribuut `csp` op een iframe werkt niet in elke browser: zet dezelfde CSP ook als `<meta>` in de `srcdoc` (niet per browser nagemeten, zie Niet bevestigd punt 6).
- Norm: ASVS 5.0.0 V1.3.1 (L1, opschonen met een bekende bibliotheek), V1.3.4 (L2, SVG), V3.2.1 (L1, sandbox). Zie WEB-37, WEB-01, AI-13, AI-14.
- Zie ook: WEB-03, WP-04, AI-13, WEB-07, INV-22, INV-23, INV-24, INV-26

### MSG-24 Begrens wat de parser van één bericht mag kosten
hoog · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Stel vóór het ontleden een maximum aan de grootte van het bericht, de lengte van een kop, het aantal MIME-delen, de nestdiepte en het aantal bijlagen, ontleed buiten de hoofdlus of met een tijdslimiet, en zet een bericht dat een grens raakt apart zonder de verwerking van de rest te stoppen.
- Bewijs: Een test met een bericht boven elke grens (te groot, kop van 1 MB, 1000 delen, 100 niveaus diep): elk wordt binnen de tijdslimiet afgewezen en als `overgeslagen` vastgelegd met mailbox en UID; het volgende bericht wordt gewoon verwerkt. De grenzen staan in de configuratie. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V5.2.1 (L1, alleen bestanden van een grootte die verwerkt kan worden); zie API-57 (lineaire patronen), WEB-43.
- Zie ook: INFRA-45, API-18, WEB-43, API-19, ARCH-13, INV-44, INV-10, MSG-22, AI-03, MSG-25, MSG-31, MSG-33

### MSG-25 Behandel een bijlage als een upload van een onbekende en pak niets automatisch uit
hoog · hard · api | app | mcp | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Pas op elke bijlage de uploadregels toe (grootte, type op inhoud, eigen bestandsnaam en pad, opslag buiten de webroot, uitlevering als download), gebruik de naam uit het bericht alleen als weergavetekst, en pak archieven niet automatisch uit; als uitpakken nodig is, doe het met limieten en in een afgeschermde map.
- Bewijs: De opslagfunctie voor bijlagen gebruikt een zelf gemaakte naam en een pad onder de map van de tenant (API-54, DB-23); een test met een bijlage genaamd `../../x.php` en een zip met een pad naar buiten en met een symlink schrijft niets buiten de bedoelde map; `grep -rnE "unzip|tar |cpio|extractall|extract\(" <mailcode>` is per treffer verklaard. Afgevinkt met de testuitvoer en grep.
- Norm: ASVS 5.0.0 V5.3.2 (L1), V5.2.2 (L1), V5.2.3 (L2), V5.4.1 (L2, eigen bestandsnaam en Content-Disposition bij uitlevering). V5.4.3 (L2) eist daarnaast een virusscan van bestanden uit een onvertrouwde bron: dat regelt WEB-48, niet deze regel. Zie WEB-43 tot en met WEB-49, API-54.
- Zie ook: WEB-44, WEB-43, WEB-46, API-60, WP-22, WP-23, WP-24, INV-33, INV-65, MSG-22, AI-03, MSG-24, MSG-31, MSG-33

### MSG-26 Zet geen invoer met een regeleinde in een IMAP- of SMTP-opdracht
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef mapnamen, zoektermen, bericht-ID's en adressen alleen via de functies van de bibliotheek aan de mailserver door, valideer ze tegen een vast patroon, en weiger elke waarde met `\r` of `\n`.
- Bewijs: Een unit-test die `INBOX\r\nA1 DELETE INBOX` als mapnaam en `1\r\nA1 LOGOUT` als bericht-ID geeft en een validatiefout verwacht voordat er een verbinding is; `grep -rnE "\.(exec|send|_simple_command|raw)\(" <mailcode>` toont geen aaneengeplakte invoer. Afgevinkt met de testuitvoer en grep.
- Norm: ASVS 5.0.0 V1.3.11 (L2).
- Zie ook: INV-48, WEB-68, INV-56, INV-49, INV-50, MSG-04

### MSG-27 Een mailserver die de gebruiker opgeeft, is een uitgaand verzoek naar een onbekend adres
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Sta bij een door de gebruiker opgegeven IMAP- of SMTP-server alleen de poorten 993, 465 en 587 toe, los de hostnaam zelf op, weiger privé-, loopback- en link-local-adressen (WEB-40), verbind met het gecontroleerde adres, en toon de gebruiker een vaste foutmelding in plaats van het antwoord van de server.
- Bewijs: Een test per geval (`127.0.0.1`, `10.0.0.1`, `169.254.169.254`, een hostnaam die naar een privé-adres wijst, poort 22 en 5432): alle worden geweigerd met dezelfde melding en zonder verbinding (controleer met een luisterende testpoort). Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V1.3.6 (L2, allowlist van protocollen, domeinen en poorten), V13.2.4 (L2).
- Zie ook: WEB-40, WEB-41, API-48, API-47, AI-48, WP-28, INFRA-18, INV-59, INV-61, MSG-46

### MSG-28 Koppel mailboxen van klanten met OAuth waar de aanbieder dat eist, en bewaar een wachtwoord versleuteld en zo kort mogelijk
hoog · hard · api | app | mcp · tegenlezer: scherpen (04-10-2026)
- Regel: Gebruik voor Google- en Microsoft 365-mailboxen OAuth met de smalste scope, vraag nooit om het gewone accountwachtwoord, en bewaar een IMAP-wachtwoord of vernieuwtoken van een klant alleen versleuteld met een sleutel buiten de database, met een einddatum: bij een eenmalige taak (migratie) tot die klaar is.
- Bewijs: `psql -c "select count(*) from <tabel> where wachtwoord is not null and taak_status = 'klaar'"` geeft 0; de kolom bevat versleutelde waarden (steekproef) en de sleutel staat niet in de database of de repository (GIT-32); de OAuth-scopes staan in de documentatie. Afgevinkt met de query en de configuratie.
- Norm: ASVS 5.0.0 V13.3.1 (L2, geheimen in een beheerde opslag); AVG artikel 32; zie PRIV-25 (einddatum op tijdelijke kopieën), INFRA-72 en verder.

### MSG-29 Identificeer een bericht met map, UIDVALIDITY en UID
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per verwerkt bericht de mailbox, de mapnaam, `UIDVALIDITY` en `UID` vast met een unieke index, begin een map opnieuw als `UIDVALIDITY` is gewijzigd, en gebruik `Message-ID` alleen als hulpmiddel om draden te koppelen, nooit als sleutel.
- Bewijs: Het schema heeft een unieke index op (mailbox, map, uidvalidity, uid); een test die twee berichten met dezelfde `Message-ID` aanbiedt, verwerkt beide; een test die `UIDVALIDITY` wijzigt, leidt tot een nieuwe volledige synchronisatie zonder dubbele rijen. Afgevinkt met het schema en de testuitvoer.
- Norm: zie DB-68 (idempotente verwerking met een unieke sleutel).

### MSG-30 Vernieuw IDLE binnen 29 minuten en haal na elke herverbinding in wat is gemist
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Beëindig en herstart een IMAP IDLE uiterlijk elke 29 minuten, herverbind met oplopende wachttijd na een verbroken verbinding, haal na elke herverbinding alle berichten boven de laatst verwerkte UID op, en meld het als er langer dan een vastgelegde tijd geen geslaagde controle was.
- Bewijs: Een test die de verbinding verbreekt tijdens IDLE: binnen de vastgelegde tijd is er een nieuwe verbinding en is een tussentijds afgeleverd testbericht verwerkt; de health-check van de dienst toont het tijdstip van de laatste geslaagde controle en slaat alarm boven de drempel (ARCH, health-checks). Afgevinkt met de testuitvoer en de health-check.
- Norm: zie ARCH (health-checks en alarmering).

### MSG-31 Antwoord nooit automatisch op een automatisch bericht
hoog · hard · api | app | wp-plugin | klantproject | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Verstuur geen automatisch antwoord (ontvangstbevestiging, afwezigheidsmelding, AI-antwoord, foutmelding) op een bericht met een kop `Auto-Submitted` anders dan `no`, met een lege envelopafzender, met `List-`koppen of `Precedence: bulk|list|junk`, of van een adres als `mailer-daemon`, `postmaster`, `noreply` of `owner-*`.
- Bewijs: Een test met vijf opgeslagen berichten (`Auto-Submitted: auto-replied`, `Return-Path: <>`, een bericht met `List-Id`, een van `MAILER-DAEMON@`, een gewoon bericht): alleen het laatste levert een automatisch antwoord op. Afgevinkt met de testuitvoer.
- Norm: geen ASVS-eis.
- Zie ook: MSG-22, AI-03, MSG-24, MSG-25, MSG-33

### MSG-32 Markeer elk automatisch verstuurd bericht
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke mail die zonder menselijke handeling wordt verstuurd `Auto-Submitted: auto-generated`, en op elk automatisch antwoord `Auto-Submitted: auto-replied`.
- Bewijs: `grep -ci '^Auto-Submitted:' <ontvangen testbericht>` geeft 1 voor elke automatische stroom (formulierbevestiging, melding, verzendlijn, automatisch antwoord). Afgevinkt met de koppen per stroom.
- Norm: geen ASVS-eis.

### MSG-33 Herken een automatisch antwoord aan de koppen, niet aan het onderwerp
middel · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bepaal of een inkomend bericht een bounce, een afwezigheidsmelding of een echte reactie is aan de hand van de MIME-structuur (`multipart/report`), de kop `Auto-Submitted` en de envelopafzender, en gebruik tekstpatronen op het onderwerp alleen als laatste vangnet dat naar "onzeker" leidt.
- Bewijs: Een test met opgeslagen voorbeelden (echte reactie met "Afwezig" in het onderwerp, automatische melding met `Auto-Submitted: auto-replied` en een gewoon onderwerp, DSN in het Duits, reactie zonder duidelijke kenmerken): de indeling is respectievelijk reactie, automatisch, bounce, en bij twijfel `onzeker` met pauze (PRIV-51). Afgevinkt met de testuitvoer.
- Norm: geen ASVS-eis.
- Zie ook: MSG-22, AI-03, MSG-24, MSG-25, MSG-31

### MSG-34 Stuur een automatisch antwoord hooguit één keer per afzender per zeven dagen, naar het envelopadres
middel · richtlijn · api | app | klantproject | wp-plugin · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd per afzender bij wanneer het laatste automatische antwoord is verstuurd, stuur binnen zeven dagen geen tweede, adresseer het antwoord aan de `Return-Path` van het bericht, en antwoord alleen als het eigen adres in `To` of `Cc` staat.
- Bewijs: Een test die twee berichten van dezelfde afzender binnen een uur aanbiedt: er gaat één antwoord uit; de tabel met (afzender, laatste antwoord) bestaat en wordt opgeruimd (PRIV-21). Afgevinkt met de testuitvoer.
- Norm: geen ASVS-eis.
