# AUTH C: MFA en passkeys

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/auth.md` (regelnummer in `regel-index.tsv`).

### AUTH-16 MFA verplicht voor beheer en voor alles op niveau 2
kritiek · hard · api | app | klantproject | wp-plugin (beheer) | website (beheer) · tegenlezer: bevestigd (04-10-2026) · bron niet gelezen: NEN
- Regel: Verplicht een tweede factor voor elk beheer- en supportaccount en voor elke applicatie op ASVS-niveau 2; bied daarbij minimaal één phishing-bestendige optie (passkey of beveiligingssleutel) aan.
- Bewijs: `SELECT count(*) FROM users WHERE role IN ('admin','support') AND mfa_enabled = false` geeft 0. Test: een beheerder zonder MFA wordt na login naar de MFA-inrichting gestuurd en kan niets anders. Voor WordPress: een 2FA-plugin is verplicht gesteld voor de rol administrator (zie WP). Afgevinkt als query en test kloppen.
- Norm: ASVS 5.0.0 V6.3.3 (L2; L3: één factor hardware-gebonden en phishing-bestendig); NIST SP 800-63B-4 §2.2 (AAL2: SHALL minimaal één phishing-bestendige optie aanbieden); OWASP Top 10:2025 A07. Wettelijke basis: zie PRIV-53 (tweefactorauthenticatie bij patiëntgegevens).
- Zie ook: AUTH-82, WP-58, INFRA-98, GIT-14, PRIV-53, INFRA-11

### AUTH-17 TOTP: eenmalig, kort geldig, begrensd
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Accepteer een TOTP-code maar één keer, met een tijdstap van 30 seconden, genereer de seed met een CSPRNG, bewaar de seed versleuteld, en begrens het aantal pogingen per account.
- Bewijs: Tests: dezelfde code tweemaal aanbieden faalt de tweede keer; de zesde foute code binnen het venster geeft 429. `\d mfa_secrets` toont geen leesbare seed. Afgevinkt als de tests groen zijn.
- Norm: ASVS 5.0.0 V6.5.1 (L2: eenmalig bruikbaar), V6.5.3 (L2: CSPRNG), V6.5.5 (L2: TOTP maximaal 30 seconden geldig), V6.6.3 (L2: rate limiting op codes), V13.3.1 (L2: seeds in geheimenbeheer); RFC 6238 §5.2.

### AUTH-18 E-mail en sms zijn geen volwaardige tweede factor
middel · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik e-mail niet als tweede factor voor kritieke delen, bied sms alleen aan naast een sterkere optie en nooit voor kritieke delen, en bind elke toegestuurde code aan het inlogverzoek waarvoor hij is gemaakt, met een geldigheid van maximaal 10 minuten.
- Bewijs: Codecheck: de MFA-keuzes voor beheerders bevatten geen e-mail of sms. Test: een code uit inlogverzoek A werkt niet voor inlogverzoek B en niet na 10 minuten. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V6.3.6 (L3: geen e-mail als factor), V6.6.1 (L2; L3: geen telefoon of sms), V6.6.2 (L2: gebonden aan het verzoek), V6.5.5 (L2: maximaal 10 minuten); NIST SP 800-63B-4 §3.1.3 (e-mail SHALL NOT voor out-of-band authenticatie).

### AUTH-19 Herstelcodes: sterk, gehasht, eenmalig
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Genereer herstelcodes met een CSPRNG met minimaal 64 bits per code, toon ze één keer, sla ze op met een wachtwoordhash (AUTH-04) zolang ze minder dan 112 bits bevatten, en maak een code na gebruik ongeldig.
- Bewijs: `SELECT recovery_codes FROM ... LIMIT 1` toont hashes. Test: een code werkt één keer. Afgevinkt als beide kloppen.
- Norm: ASVS 5.0.0 V6.5.1, V6.5.2, V6.5.3 (L2); NIST SP 800-63B-4 §4.2.1.1 (bewaarde herstelcode: SHALL minimaal 64 bits, SHALL gehasht opgeslagen, onderworpen aan de limiet van §3.2.2).

### AUTH-20 Reset en herstel mogen MFA niet omzeilen
kritiek · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een wachtwoordreset de tweede factor intact (na de reset vraagt de login nog steeds om MFA) en eis bij verlies van de tweede factor een herstelcode of een identiteitscontrole die even sterk is als bij de inrichting.
- Bewijs: End-to-end-test: reset voor een account met MFA, daarna inloggen vraagt om de tweede factor. Test: "MFA kwijt" zonder herstelcode levert geen toegang op zonder de vastgelegde handmatige procedure. Afgevinkt als beide tests groen zijn.
- Norm: ASVS 5.0.0 V6.4.3, V6.4.4 (L2).

### AUTH-21 Passkeys: verifieer op de server volgens WebAuthn, met een bibliotheek
kritiek · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat registratie en login met passkeys verifiëren door een onderhouden WebAuthn-bibliotheek en controleer per ceremonie: een eigen, willekeurige challenge van minimaal 16 bytes die één keer geldig is, de exacte origin, de hash van de RP-id, de UP-vlag, de UV-vlag als je die eist, en de handtekening.
- Bewijs: Tests met de bibliotheek: assertion met een oude challenge faalt, met een andere origin faalt, een hergebruikte challenge faalt. Codecheck: de challenge komt uit `randomBytes(32)` en staat server-side bij de sessie, met een vervaltijd. Afgevinkt als de drie tests groen zijn.
- Norm: W3C WebAuthn Level 3 §7.1 en §7.2 (verificatiestappen), §13.4.3 (challenge minimaal 16 bytes); ASVS 5.0.0 V6.7.2 (L3: nonce minimaal 64 bits en uniek).

### AUTH-22 Passkeys: sla het juiste op en lek niets via de user handle
middel · hard · api | app | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Gebruik als `user.id` een willekeurige waarde zonder persoonsgegevens, weiger bij registratie een credential-id dat al geregistreerd is (bij welke gebruiker dan ook), en sla per credential de publieke sleutel, de signCount en de vlaggen BE en BS op.
- Bewijs: Codecheck: `user.id` komt uit `randomBytes` of een losse UUID-kolom, niet uit e-mail of het zichtbare gebruikers-id. `\d passkeys` toont een unieke index op `credential_id` en kolommen voor `sign_count`, `backup_eligible`, `backup_state`. Afgevinkt als beide kloppen.
- Norm: W3C WebAuthn Level 3 §14.6.1 ("The user handle MUST NOT contain personally identifying information"), §7.1 ("Verify that the credentialId is not yet registered for any user"), §7.2 (signCount en BE/BS).

### AUTH-23 Passkeys: eis gebruikersverificatie als de passkey de enige stap is, en laat de terugval niet zwakker zijn
hoog · hard · api | app | klantproject · tegenlezer: scherpen (04-10-2026)
- Regel: Zet `userVerification: 'required'` en controleer de UV-vlag wanneer een passkey wachtwoord en tweede factor samen vervangt, en zorg dat het terugvalpad (wachtwoord, herstel) dezelfde sterkte houdt als AUTH-16 voorschrijft.
- Bewijs: Test: een assertion zonder UV-vlag wordt geweigerd op het passkey-only pad. De tabel uit AUTH-13 toont dat het wachtwoordpad MFA eist. Afgevinkt als beide kloppen.
- Norm: W3C WebAuthn Level 3 §7.2 (UV-controle als de relying party die eist); NIST SP 800-63B-4 Appendix B ("Verifiers SHALL indicate that UV is preferred and SHALL inspect responses to confirm the value of the UV flag. This indicates whether the authenticator can be treated as a multi-factor cryptographic authenticator"); ASVS 5.0.0 V6.3.3, V6.3.4 (L2).

### AUTH-24 Begrens pushverzoeken en toegestuurde codes
middel · richtlijn · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Begrens het aantal push- of codeverzoeken per account per tijdvenster en gebruik bij pushgoedkeuring nummerherkenning in plaats van een kale knop "goedkeuren".
- Bewijs: Test: het vierde codeverzoek binnen het venster geeft 429 en verstuurt niets. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V6.6.4 (L3), V6.6.3 (L2).
