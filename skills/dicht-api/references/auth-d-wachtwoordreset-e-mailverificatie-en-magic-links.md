# AUTH D: Wachtwoordreset, e-mailverificatie en magic links

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/auth.md` (regelnummer in `regel-index.tsv`).

### AUTH-25 Reset- en verificatietokens: willekeurig, gehasht, eenmalig, kort geldig
kritiek · hard · alles (met login) · tegenlezer: scherpen (04-10-2026)
- Regel: Maak elk reset-, verificatie- en uitnodigingstoken met een CSPRNG met minimaal 128 bits, sla alleen de SHA-256-hash op, koppel het aan één gebruiker en één doel, maak het na gebruik ongeldig en laat het vervallen (resetlink maximaal 1 uur als projectstandaard; een magic link die direct inlogt maximaal 10 minuten, zie AUTH-30; verificatie en uitnodiging nooit langer dan 24 uur).
- Bewijs: `SELECT * FROM password_resets LIMIT 1` toont een hash en een vervaltijd, geen bruikbaar token. Tests: token tweemaal gebruiken faalt de tweede keer; verlopen token faalt; token voor doel `verify_email` werkt niet op de resetroute. Afgevinkt als de drie tests groen zijn.
- Norm: ASVS 5.0.0 V11.5.1 (L2: CSPRNG, minimaal 128 bits, UUID's voldoen niet), V6.5.2 (L2: bij 112 bits of meer mag een standaardhash), V6.4.1 (L1: eenmalig en kort geldig); NIST SP 800-63B-4 §4.2.1.2 (toegestuurde herstelcode per e-mail maximaal 24 uur geldig, per sms 10 minuten).

### AUTH-26 → WEB-42
Samengevoegd: "Bouw links in mails nooit uit de Host-header" is gedekt door WEB-42. Gebruik die regel.

### AUTH-27 Stuur resetmails alleen naar het geverifieerde adres uit de database
kritiek · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Zoek bij een resetverzoek de gebruiker op en verstuur uitsluitend naar het geverifieerde adres dat in de database staat; gebruik het adres uit het verzoek alleen om te zoeken, accepteer precies één string, en wijzig niets aan het account tot een geldig token is aangeboden.
- Bewijs: Tests: verzoek met `email` als array of met twee adressen geeft 400; verzoek voor een niet-geverifieerd adres verstuurt niets; na een resetverzoek zonder inwisselen werkt het oude wachtwoord nog. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V6.4.3 (L2); OWASP API Security Top 10 2023 API2.

### AUTH-28 Na een reset: niet automatisch inloggen, sessies weg, melding
hoog · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Log de gebruiker na het instellen van een nieuw wachtwoord niet automatisch in, beëindig alle bestaande sessies en langlevende tokens van dat account (of vraag het de gebruiker), en stuur een bevestiging zonder het wachtwoord.
- Bewijs: Integratietest: sessie A actief, reset uitvoeren, sessie A geeft daarna 401; de reset-respons zet geen sessiecookie. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V7.4.3 (L2), V6.3.7 (L3: melding).

### AUTH-29 Verifieer een e-mailadres voordat het iets betekent, en bescherm de wijziging ervan
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Behandel een e-mailadres pas als identiteit (inloggen, uitnodigingen koppelen, tenant-toegang op domein) nadat de gebruiker het met een token heeft bevestigd; eis voor het wijzigen van het adres opnieuw inloggen, bevestig het nieuwe adres met een token en meld de wijziging op het oude adres.
- Bewijs: Tests: een account met `email_verified_at IS NULL` kan geen uitnodiging accepteren en geen reset aanvragen; e-mailwijziging zonder recent wachtwoord of MFA geeft 401 of 403; het adres wijzigt pas na de bevestigingslink. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V7.5.1 (L2: volledige herauthenticatie voor wijziging van e-mail, telefoon, MFA en herstelgegevens), V6.3.7 (L3); NIST SP 800-63B-4 §4.2.1.2 (een hersteladres SHALL worden geverifieerd met een bevestigingscode).

### AUTH-30 Magic links: dezelfde eisen als een reset, gebonden aan de browser, niet voor kritieke delen
hoog · hard · api | app | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Behandel een magic link als een resettoken (AUTH-25 tot en met AUTH-27), laat een magic link die direct inlogt maximaal 10 minuten gelden, bind hem aan de browsersessie die hem aanvroeg, verbruik hem pas bij een POST na een klik van de gebruiker, en gebruik hem niet als enige inlogmiddel voor beheer, betaling of zorgdata.
- Bewijs: Tests: de link openen in een andere browser dan waarin hij is aangevraagd logt niet in (toont hooguit een bevestigingsstap); een GET op de link verbruikt het token niet; de tweede keer inwisselen faalt; een link van 11 minuten oud logt niet in. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V6.5.5 (L2: toegestuurde inlogverzoeken, codes of tokens maximaal 10 minuten geldig), V6.6.2 (L2: gebonden aan het oorspronkelijke verzoek), V6.3.6 (L3: geen e-mail als enige of tweede factor), V7.6.2 (L2: een sessie ontstaat alleen na een expliciete handeling van de gebruiker); NIST SP 800-63B-4 §3.1.3 (e-mail SHALL NOT voor out-of-band authenticatie).

### AUTH-31 Houd tokens uit referers, logs en pagina's met scripts van derden
middel · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet op elke pagina die een token in de URL ontvangt `Referrer-Policy: no-referrer`, laad daar geen scripts of afbeeldingen van derden, en haal het token uit de URL zodra het is gelezen; zet alle andere geheimen (sessie, API-sleutel) nooit in een URL.
- Bewijs: `curl -sI https://app/reset?token=x | grep -i referrer-policy` toont `no-referrer`. Playwright-test: op de resetpagina gaan geen verzoeken naar andere hosts. nginx-logformaat voor deze routes laat de querystring weg (zie INFRA). Afgevinkt als alle drie kloppen.
- Norm: ASVS 5.0.0 V14.2.1 (L1: geen gevoelige gegevens in URL of querystring).
