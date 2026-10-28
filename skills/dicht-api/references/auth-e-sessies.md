# AUTH E: Sessies

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/auth.md` (regelnummer in `regel-index.tsv`).

### AUTH-32 Sessie-id: willekeurig, ondoorzichtig, op de server gecontroleerd
kritiek · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Genereer sessie-id's met een CSPRNG met minimaal 128 bits, zet er geen betekenis of persoonsgegevens in, en valideer elke aanvraag tegen de sessieopslag op de server.
- Bewijs: Codecheck: sessie-id uit `randomBytes(32)` of de sessiebibliotheek van het framework; `grep -rn "Math.random\|uniqid(" src/` levert geen treffer in auth-code. Test: een willekeurige of aangepaste cookiewaarde geeft 401. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V7.2.1, V7.2.3 (L1: CSPRNG, minimaal 128 bits); NIST SP 800-63B-4 §5.1 (minimaal 64 bits, na authenticatie aangemaakt, cookie bevat alleen een ondoorzichtige string).

### AUTH-33 Sessiecookie: `__Host-`, Secure, HttpOnly, SameSite, en nooit in webopslag
kritiek · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet de sessie in een cookie met de naam `__Host-...`, met `Secure`, `HttpOnly`, `Path=/`, zonder `Domain`, en `SameSite=Lax` of `Strict`; bewaar sessie-id's, JWT's en refresh tokens nooit in `localStorage` of `sessionStorage`.
- Bewijs: `curl -sI -X POST https://app/login ... | grep -i set-cookie` toont de vier attributen en de prefix. `grep -rnE "localStorage|sessionStorage" src/` levert geen token- of sessiecode op. Afgevinkt als beide kloppen.
- Norm: ASVS 5.0.0 V3.3.1 (L1), V3.3.2, V3.3.3, V3.3.4 (L2), V10.1.1 (L2: tokens alleen bij de backend); NIST SP 800-63B-4 §5.1.1 (SHALL Secure; SHOULD HttpOnly, `__Host-`, `SameSite=Lax` of `Strict`) en §5.1 (SHOULD NOT in HTML5 Local Storage).
- Zie ook: WEB-25, WEB-26

### AUTH-34 Nieuw sessie-id bij inloggen en bij elke rechtenwijziging
hoog · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef bij elke login, herauthenticatie en wijziging van rol of tenant een nieuw sessie-id uit en maak het oude ongeldig; accepteer alleen sessie-id's die de server zelf heeft uitgegeven.
- Bewijs: Integratietest: cookiewaarde vóór en na login verschilt, en de oude waarde geeft 401. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V7.2.4 (L1).

### AUTH-35 Leg een idle timeout en een absolute timeout vast en dwing ze op de server af
hoog · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel per applicatie een inactiviteitsgrens en een absolute levensduur van de sessie in, dwing beide op de server af en leg de waarden met onderbouwing vast; begin bij 1 uur inactiviteit en 24 uur absoluut voor applicaties met klantdata en MFA, 15 minuten en 12 uur voor beheer van kritieke delen, en maximaal 30 dagen absoluut voor laag risico.
- Bewijs: `docs/auth.md` noemt beide waarden per rol. Test met een verzette klok: een verzoek na de inactiviteitsgrens en een verzoek na de absolute grens geven beide 401, ook als het cookie nog bestaat. Afgevinkt als de test groen is.
- Norm: ASVS 5.0.0 V7.1.1, V7.3.1, V7.3.2 (L2: gedocumenteerd, afwijking van NIST onderbouwd); NIST SP 800-63B-4 §2.1.3 (AAL1: SHOULD maximaal 30 dagen), §2.2.3 (AAL2: SHOULD maximaal 24 uur en 1 uur inactiviteit), §2.3.3 (AAL3: SHALL maximaal 12 uur, SHOULD 15 minuten inactiviteit), §5.1.1 (cookieverloop SHALL NOT de afdwinging zijn).

### AUTH-36 Uitloggen en blokkeren werken direct op de server
kritiek · hard · alles (met login) · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak bij uitloggen, verlopen, blokkeren of verwijderen van een account de sessie in de serveropslag ongeldig; gebruik voor browsersessies geen zelfstandige tokens (JWT) tenzij er een intrekmechanisme is (lijst van ingetrokken tokens of een tijdstip per gebruiker waarvóór tokens ongeldig zijn).
- Bewijs: Integratietests: na `POST /logout` geeft hetzelfde cookie of token 401; na `UPDATE users SET disabled_at = now()` geeft een eerder uitgegeven token op het eerstvolgende verzoek 401. Afgevinkt als beide tests groen zijn.
- Norm: ASVS 5.0.0 V7.4.1, V7.4.2 (L1); NIST SP 800-63B-4 §5.1 (sessiegeheim SHALL bij uitloggen worden gewist of ongeldig gemaakt).

### AUTH-37 Geef gebruiker en beheerder zicht op en controle over actieve sessies
middel · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Toon de gebruiker zijn actieve sessies (apparaat, laatst gebruikt, plaats bij benadering) met de mogelijkheid ze na herauthenticatie te beëindigen, bied na elke factorwijziging aan alle andere sessies te beëindigen, zet een zichtbare uitlogknop op elke ingelogde pagina, en geef beheerders een knop om sessies van één of alle gebruikers te beëindigen.
- Bewijs: Playwright-test: twee browsers ingelogd, sessie twee beëindigen vanuit sessie één, sessie twee krijgt de loginpagina. Beheerfunctie "alle sessies beëindigen" heeft een integratietest. Afgevinkt als beide groen zijn.
- Norm: ASVS 5.0.0 V7.5.2, V7.4.3, V7.4.4, V7.4.5, V7.1.2 (L2).

### AUTH-38 Vraag opnieuw om authenticatie voor gevoelige handelingen
hoog · hard · api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Eis een verse authenticatie (wachtwoord of tweede factor, niet ouder dan een vastgelegde termijn zoals 10 minuten) voor het wijzigen van e-mail, wachtwoord, MFA en herstelgegevens, het aanmaken van API-sleutels, het wijzigen van uitbetaal- of factuurgegevens, het exporteren van alle data en het verwijderen van een account of tenant.
- Bewijs: Integratietest per genoemde handeling: met een sessie waarvan `reauthenticated_at` ouder is dan de termijn volgt 401 of 403 met een herauthenticatie-aanwijzing. Afgevinkt als elke handeling uit de lijst een test heeft.
- Norm: ASVS 5.0.0 V7.5.1 (L2), V7.5.3 (L3: extra factor voor zeer gevoelige transacties); OWASP API Security Top 10 2023 API2.
