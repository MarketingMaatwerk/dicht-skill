# WEB 8: Bestandsupload en -download

Compacte regels van `dicht-web`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/web.md` (regelnummer in `regel-index.tsv`).

### WEB-43 Begrens de grootte van elke upload en elke body
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel per uploadfunctie een maximale bestandsgrootte en een maximaal aantal bestanden in, dwing die af in de webserver (`client_max_body_size`) én in de applicatie, en leg de waarden vast.
- Bewijs: Een test die een bestand van limiet plus 1 byte uploadt en 413 terugkrijgt, zowel via nginx als rechtstreeks op de applicatie; de limiet staat in de documentatie. Afgevinkt met de test. Context: Fastify heeft standaard `bodyLimit` 1048576 bytes (1 MiB); `requestTimeout` is standaard 0 (geen limiet) en moet volgens de documentatie op een waarde staan als er geen reverse proxy voor staat.
- Norm: ASVS 5.0.0 V5.2.1 (L1), V5.1.1 (L2), V5.2.4 (L3).
- Zie ook: WEB-44, WEB-46, API-60, WP-22, WP-23, WP-24, INV-33, INV-65, MSG-25, INFRA-45, API-18, API-19, ARCH-13, INV-44, INV-10, MSG-24

### WEB-44 Sta alleen een allowlist van typen toe en controleer de inhoud
hoog · hard · website | wp-plugin | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Accepteer per uploadfunctie alleen de extensies die het doel nodig heeft, controleer na het decoderen van de naam dat de extensie op de allowlist staat en dat de inhoud bij die extensie past (magic bytes alleen om vroeg te weigeren, en volledig parsen of hercoderen als bewijs: INV-33), en vertrouw nooit op het `Content-Type` dat de client meestuurt.
- Bewijs: Tests per uploadfunctie met `shell.php`, `shell.jpg.php`, `shell.pHp`, `shell.phtml`, een PHP-bestand met de naam `foto.jpg` en een echt JPEG met `Content-Type: application/x-php`; alleen het laatste wordt geaccepteerd. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V5.2.2 (L1; voor alle bestanden vanaf L2); OWASP Top 10 2025 A06 Insecure Design.
- Zie ook: WEB-43, WEB-46, API-60, WP-22, WP-23, WP-24, INV-33, INV-65, MSG-25

### WEB-45 Bepaal bestandsnaam en pad zelf
hoog · hard · website | wp-plugin | api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Sla een upload op onder een door de applicatie gegenereerde naam (UUID) in een door de applicatie bepaalde map, bewaar de oorspronkelijke naam alleen als metadata, en gebruik door gebruikers aangeleverde namen nooit in een pad.
- Bewijs: Test met de bestandsnamen `../../x.txt`, `..\\..\\x.txt` en `/etc/passwd`; er ontstaat geen bestand buiten de uploadmap (`find` vóór en na). `grep -rnE "filename|originalname" src/` toont geen gebruik in een padfunctie. Afgevinkt met test en grep.
- Norm: ASVS 5.0.0 V5.3.2 (L1), V5.3.3 (L3); OWASP Top 10 2025 A01 en A05.
- Zie ook: API-54, AI-46, WP-25, API-76, WP-29, INV-41, INV-34, SCR-15

### WEB-46 Sla uploads op waar ze nooit als code worden uitgevoerd
kritiek · hard · website | wp-plugin | wp-thema | app | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Bewaar uploads buiten de webroot of op een aparte opslag, en lever ze uit via een handler die een ID naar een bestand vertaalt; moet een map wel publiek zijn (WordPress `uploads`), schakel dan de uitvoering van PHP en andere scripts in die map uit op de webserver.
- Bewijs: Zet een bestand `test.php` met `<?php echo 'UITGEVOERD';` in de uploadmap van een testomgeving en vraag het op: de respons is 403 of de broncode als download, nooit `UITGEVOERD`. Op LiteSpeed en Apache: de regel staat in `.htaccess` en is gemeten, niet aangenomen. Afgevinkt met de curl-uitvoer.
- Norm: ASVS 5.0.0 V5.3.1 (L1); OWASP Top 10 2025 A05 en A02.
- Zie ook: WEB-44, WEB-43, API-60, WP-22, WP-23, WP-24, INV-33, INV-65, MSG-25

### WEB-47 Lever bestanden van gebruikers uit als download of vanaf een aparte origin
hoog · hard · website | wp-plugin | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stuur bestanden die een gebruiker heeft aangeleverd terug met `Content-Disposition: attachment` met een door de server bepaalde, gecodeerde bestandsnaam, een vast `Content-Type` (`application/octet-stream` voor onbekende typen) en `X-Content-Type-Options: nosniff`; toon ze alleen inline vanaf een aparte origin zonder cookies of met `Content-Security-Policy: sandbox`.
- Bewijs: `curl -sI` op een download-URL toont `Content-Disposition: attachment; filename=…`, een vast type en `nosniff`; een geüpload HTML-bestand wordt gedownload en niet getoond; een oorspronkelijke naam met `"` of een regeleinde breekt de header niet. Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V3.2.1 (L1), V5.4.1 en V5.4.2 (L2).
- Zie ook: INV-31, INV-32, WEB-07, WP-23

### WEB-48 Scan bestanden uit niet-vertrouwde bron op malware
middel · hard · website | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat elk bestand dat van buiten komt en dat andere mensen kunnen downloaden door een virusscanner gaan vóór het beschikbaar komt, en leg vast wat er gebeurt bij een treffer.
- Bewijs: Upload van het EICAR-testbestand wordt geweigerd of in quarantaine gezet en gelogd. Afgevinkt met de logregel. Welke scanner (bijvoorbeeld ClamAV) en waar die draait, is een keuze voor INFRA: zie Open vragen.
- Norm: ASVS 5.0.0 V5.4.3 (L2), V5.1.1 (L2).

### WEB-49 Herschrijf afbeeldingen en wantrouw archieven
middel · richtlijn · website | wp-plugin | api | app · tegenlezer: bevestigd (04-10-2026)
- Regel: Codeer geüploade afbeeldingen opnieuw met een beeldbibliotheek (dat verwijdert ingebedde inhoud en metadata zoals GPS), weiger afbeeldingen boven een maximaal aantal pixels, en pak archieven alleen uit met een limiet op uitgepakte grootte en aantal bestanden, zonder symlinks en zonder paden uit het archief te volgen.
- Bewijs: Tests: een afbeelding van 30000 bij 30000 pixels wordt geweigerd; een opgeslagen foto bevat geen EXIF-GPS (`exiftool`); een zip met `../x` en een zip-bom worden geweigerd. Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V5.2.3 (L2), V5.2.5, V5.2.6, V5.3.3 en V14.2.8 (L3).
- Zie ook: INV-41, INV-42, INV-43, INV-45, SCR-29, INV-28, INV-27, INV-29, INV-30, INV-32
