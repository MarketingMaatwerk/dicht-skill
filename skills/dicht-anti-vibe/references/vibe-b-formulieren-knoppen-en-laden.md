# VIBE B: Formulieren, knoppen en laden

Compacte regels van `dicht-anti-vibe`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/anti-vibe.md` (regelnummer in `regel-index.tsv`).

### VIBE-10 Elke knop en CTA doet iets
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Klik in Playwright op elke zichtbare knop en CTA: elke klik navigeert, opent iets, verstuurt iets of verandert de pagina. Geen dode knop en geen knop zonder actie.
- Bewijs: `vibe_meet.py` regel VIBE-10 klikt per pagina op elke zichtbare `button` die geen verzendknop is en meldt elke knop waarna URL, DOM, `aria-expanded` en dialogen gelijk blijven; links met een echte `href` vallen onder VIBE-03, verzendknoppen onder VIBE-11. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, A2 (knoppen en CTA's); H paragraaf 2 punt 11.

### VIBE-11 Elk formulier toont na verzenden een melding op de pagina
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elk formulier (niet alleen het contactformulier) toont na een geslaagde verzending een bedankbericht op dezelfde pagina, zonder aparte bedankpagina, en de inzending komt aan.
- Bewijs: Playwright op de testomgeving: per formulier een echte inzending met een testadres op eigen domein, de melding is zichtbaar (`toBeVisible`) en de inzending staat in het beheer of in de mailbox (IMAP). Niet op een live site zonder akkoord (een inzending verstuurt mail). Afgevinkt met de testuitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook WEB-67 (botbescherming).
- Bron: website.md Stap 9, O21 (inline bedankbericht) en A6 (formulieren); Stap 8 S6 (contactformulier); H paragraaf 2 punt 12.

### VIBE-12 Elk formulier toont een foutmelding per veld
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Bij ongeldige invoer staat de foutmelding bij het veld zelf (met `aria-invalid` en `aria-describedby`), niet alleen één algemene melding bovenaan.
- Bewijs: Playwright op de testomgeving: per formulier verzenden met een leeg verplicht veld en een ongeldig e-mailadres; per veld is een melding zichtbaar en het veld heeft `aria-invalid="true"`. Afgevinkt met de testuitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook PRIV-66 (WCAG 2.2 AA).
- Bron: website.md Stap 9, A6 (formulieren); Stap 8 S6 (inline foutmeldingen per veld); H paragraaf 2 punt 13.

### VIBE-13 Laden toont een skeleton, geen spinner
laag · richtlijn · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Een onderdeel dat later laadt (reviews, portfolio, formulierverzending) toont bij een wachttijd boven 300 tot 400 ms een skeleton in de vorm en maat van de inhoud, geen spinner of "laden...". De ruimte staat vast vóór de inhoud komt (geen layout shift), en met `prefers-reduced-motion` is het skeleton stil.
- Bewijs: `grep -rniE "spinner|laden\.\.\.|loading\.\.\." <thema>/` geeft niets in eigen code, en een Playwright-schermafbeelding met vertraagd netwerk (`page.route` met 1 s vertraging) toont het skeleton. Afgevinkt met beide.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook ARCH-74 (CLS).
- Bron: website.md Stap 8 S1 (loading states = skeleton); H paragraaf 3 (loading skeletons).

### VIBE-14 Geen fouten in de console
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Op geen enkele pagina en op geen enkel formaat (desktop en mobiel) staat een fout in de console of een niet-afgevangen JavaScript-fout.
- Bewijs: `vibe_meet.py` regel VIBE-14 (console `error` en `pageerror` per pagina, op 1366 en 390 px). Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O0 (volledige Playwright-testronde) en O17 (geen console errors).

### VIBE-43 Een veld voor een eenmalige code heeft autocomplete="one-time-code"
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elk invoerveld voor een eenmalige code (inlogcode, verificatiecode per mail of sms, tweestapsverificatie) heeft `autocomplete="one-time-code"` en `type="text"` (niet `number`), en bij een code van alleen cijfers ook `inputmode="numeric"`.
- Bewijs: `vibe_meet.py` regel VIBE-43: op elke gemeten pagina heeft elk veld waarvan naam, id, label of placeholder op een code wijst (los woord, of na inlog, bevestigings, verificatie, activerings en dergelijke; niet postcode, korting, promo, cadeau, verwijzing, netnummer of ordercode) `one-time-code` en is het geen `type=number`; losse vakjes van één teken in één ouder tellen als één veld. Een codeveld achter een inlogstap dat de meting niet bereikt: `grep -rn 'one-time-code' <thema>/` bij elk codeveld. Geen codeveld op de site: `nvt`. Afgevinkt met de uitvoer of de grep.
- Norm: HTML Standard, autofill-veldnaam `one-time-code` ("One-time code used for verifying user identity"); web.dev, SMS OTP form best practices (`type="text"`, `inputmode="numeric"`, `autocomplete="one-time-code"`; aanbeveling, pagina bijgewerkt 2020-12-09).
- Bron: UI-tip 15 "One-time code autofill" (Marketing Maatwerk, 26-10-2026); https://html.spec.whatwg.org/multipage/form-control-infrastructure.html#autofill en https://web.dev/articles/sms-otp-form, gelezen 26-10-2026.
