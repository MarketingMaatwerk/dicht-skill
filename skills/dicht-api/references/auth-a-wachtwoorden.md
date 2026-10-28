# AUTH A: Wachtwoorden

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/auth.md` (regelnummer in `regel-index.tsv`).

### AUTH-01 Minimale en maximale wachtwoordlengte
hoog · hard · api | app | klantproject | website (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Eis minimaal 15 tekens als het wachtwoord de enige factor is en minimaal 8 tekens als MFA verplicht is; sta minimaal 64 tekens toe en tel elk Unicode-codepunt als één teken.
- Bewijs: Unit-test op het registratie- en wijzigingsschema: 14 tekens geweigerd, 15 geaccepteerd, 64 tekens met spaties en emoji geaccepteerd. Afgevinkt als de test in CI draait en het schema op alle drie de plekken (registratie, wijzigen, reset) hetzelfde is.
- Norm: ASVS 5.0.0 V6.2.1 (L1: minimaal 8, 15 sterk aanbevolen), V6.2.9 (L2: minimaal 64 toegestaan); NIST SP 800-63B-4 §3.1.1.2 (SHALL 15 als enige factor, SHALL 8 bij MFA, SHOULD maximaal ten minste 64).

### AUTH-02 Geen samenstellingsregels en geen verplichte periodieke wissel
middel · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg geen eisen op aan soorten tekens en dwing geen periodieke wachtwoordwissel af; dwing wel een wissel af zodra er aanwijzingen zijn dat het wachtwoord gelekt is.
- Bewijs: Codecheck: geen regex op tekensoorten in wachtwoordvalidatie, geen `password_expires_at` die inloggen blokkeert. Afgevinkt met de test uit AUTH-01 (wachtwoord van 15 kleine letters wordt geaccepteerd).
- Norm: ASVS 5.0.0 V6.2.5 (L1), V6.2.10 (L2); NIST SP 800-63B-4 §3.1.1.2 (SHALL NOT samenstellingsregels, SHALL NOT periodieke wissel, SHALL wissel bij compromittering).

### AUTH-03 Controleer nieuwe wachtwoorden tegen een blocklist
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Weiger bij registratie, wijziging en reset elk wachtwoord dat voorkomt in gelekte wachtwoorden of in een lijst met contextwoorden (bedrijfsnaam, productnaam, domein), en vertel de gebruiker waarom.
- Bewijs: Test: `Password123456789` en `<projectnaam>2026` worden geweigerd met een duidelijke melding. Bij uitval van de externe dienst valt de controle terug op een lokale lijst (minimaal de top 3000 die aan het beleid voldoet) en blokkeert registratie niet. Afgevinkt als beide tests groen zijn.
- Norm: ASVS 5.0.0 V6.2.4 (L1: top 3000), V6.2.12 (L2: gelekte wachtwoorden), V6.1.2 en V6.2.11 (L2: contextwoorden); NIST SP 800-63B-4 §3.1.1.2 (SHALL blocklist, hele wachtwoord vergelijken, reden melden).

### AUTH-04 Sla wachtwoorden op met Argon2id
kritiek · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Hash wachtwoorden met Argon2id met minimaal m=19456 KiB, t=2, p=1 (of m=47104 KiB, t=1, p=1) en een willekeurige salt per wachtwoord; gebruik bcrypt alleen in bestaande systemen en dan met cost 10 of hoger.
- Bewijs: `SELECT left(password_hash, 12) FROM users LIMIT 5` toont `$argon2id$` (of `$2y$` met cost 10 of hoger in bestaand werk). Codecheck: geen `createHash(` of `md5(` in de buurt van wachtwoorden. Afgevinkt als beide kloppen en de parameters uit configuratie komen.
- Norm: ASVS 5.0.0 V11.4.2 (L2) en Appendix C (argon2id t=1 m≥47104 p=1; bcrypt cost ≥10; PBKDF2-HMAC-SHA-256 ≥600.000); NIST SP 800-63B-4 §3.1.1.2 (SHALL salt van minimaal 32 bits en een geschikte wachtwoordhash).
- Zie ook: AUTH-05, AUTH-07, DB-81

### AUTH-05 Stop nooit meer dan het wachtwoord in bcrypt
hoog · hard · api | app | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik bcrypt nooit voor invoer die langer kan zijn dan 72 bytes en nooit voor een samengestelde string (gebruikersnaam plus wachtwoord, id plus geheim); begrens bij bcrypt de wachtwoordlengte op 72 bytes of stap over op Argon2id.
- Bewijs: `grep -rn "bcrypt" src/` en controleer elke aanroep: de invoer is alleen het wachtwoord en het schema begrenst op 72 bytes. Test: twee wachtwoorden van 80 tekens die pas na teken 72 verschillen mogen niet allebei slagen. Afgevinkt als de test groen is of bcrypt niet voorkomt.
- Norm: ASVS 5.0.0 V6.2.8 (L1: wachtwoord exact zoals ontvangen, zonder afkappen); NIST SP 800-63B-4 §3.1.1.2 (SHALL het hele wachtwoord verifiëren).
- Zie ook: AUTH-04, AUTH-07, DB-81

### AUTH-06 Verifieer het wachtwoord ongewijzigd en werk wachtwoordmanagers niet tegen
middel · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Verifieer het wachtwoord precies zoals ontvangen (geen trim, geen hoofdletterconversie, geen afkappen), pas alleen Unicode-normalisatie NFC toe vóór het hashen, en sta plakken en automatisch invullen toe.
- Bewijs: Codecheck van registratie, wijziging, reset en login: dezelfde functie `normalizePassword` (alleen `normalize('NFC')`). Handmatig: plakken werkt, het veld heeft `type="password"` en `autocomplete="current-password"` of `new-password`. Afgevinkt met een Playwright-test die een wachtwoord plakt.
- Norm: ASVS 5.0.0 V6.2.6, V6.2.7, V6.2.8 (L1); NIST SP 800-63B-4 §3.1.1.2 (SHOULD plakken toestaan, SHOULD NFC, SHALL niet afkappen).

### AUTH-07 Bewaar de hashparameters en herhash bij inloggen
middel · richtlijn · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Bewaar algoritme en kostenfactor in de hash zelf en herhash het wachtwoord bij een geslaagde login zodra de opgeslagen parameters lager zijn dan de huidige configuratie.
- Bewijs: Test: een gebruiker met een oude hash logt in, daarna staat er een hash met de huidige parameters. Afgevinkt als de test groen is.
- Norm: NIST SP 800-63B-4 §3.1.1.2 (SHOULD een verwijzing naar het schema en de kostenfactor opslaan om migratie mogelijk te maken); ASVS 5.0.0 V11.4.2 (L2: parameters volgens actuele richtlijn).
- Zie ook: AUTH-04, AUTH-05, DB-81

### AUTH-08 Wachtwoord wijzigen vraagt het huidige wachtwoord
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Eis bij een wachtwoordwijziging het huidige en het nieuwe wachtwoord, stuur daarna een melding naar de gebruiker en bied aan alle andere sessies te beëindigen.
- Bewijs: Integratietest: wijziging zonder of met fout huidig wachtwoord geeft 4xx en verandert niets; na een geslaagde wijziging is een tweede sessie van dezelfde gebruiker ongeldig als de gebruiker daarvoor kiest. Afgevinkt als de test groen is en de meldingsmail in de test-mailbox staat.
- Norm: ASVS 5.0.0 V6.2.2, V6.2.3 (L1), V7.4.3 (L2), V6.3.7 (L3: melding na wijziging van inloggegevens); OWASP API Security Top 10 2023 API2.

### AUTH-09 Geen hints, geen geheime vragen, geen standaardaccounts, geen blijvende startwachtwoorden
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Bouw geen wachtwoordhints of geheime vragen, lever geen standaardaccounts mee (`admin`, `test`, `demo`), en laat een door het systeem gemaakt startwachtwoord of activatiecode na eerste gebruik of na korte tijd vervallen.
- Bewijs: `wp user list --role=administrator` of `SELECT email FROM users WHERE role='admin'` toont alleen benoemde personen; geen seed-gebruiker in productiemigraties (`grep -rn "admin@" migrations/ seeds/`). Afgevinkt als de lijst klopt met de afgesproken beheerders.
- Norm: ASVS 5.0.0 V6.4.2, V6.4.1, V6.3.2 (L1); NIST SP 800-63B-4 §3.1.1.2 (SHALL NOT hints of kennisvragen).
