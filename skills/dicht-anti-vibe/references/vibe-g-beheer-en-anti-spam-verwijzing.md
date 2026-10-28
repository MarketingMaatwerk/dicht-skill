# VIBE G: Beheer en anti-spam (verwijzing)

Compacte regels van `dicht-anti-vibe`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/anti-vibe.md` (regelnummer in `regel-index.tsv`).

### VIBE-36 Loop beheer, anti-spam en blootstelling na volgens de regels die er al zijn
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Deze regel voegt niets toe; hij zorgt dat de oplevercontrole de bestaande regels meeneemt. (1) Beheer: geen enkel beheerscherm is een WordPress-rijenlijst en elke bento-kaart is direct bewerkbaar met opslaan per kaart (het eigen websiteproces (stap 8), harde regel). (2) Anti-spam: elk formulier en endpoint heeft de vijf lagen uit het eigen websiteproces (stap 8) en voldoet aan WEB-66, WEB-67 en WEB-70. (3) Reacties uit, XML-RPC dicht (WP-55) en geen gebruikersnamen weg (WP-56).
- Bewijs: (1) Playwright als beheerder op de testomgeving: op elk eigen beheerscherm is het aantal links naar `post.php?post=` 0; (2) de Playwright-tests uit Stap 8 (echte inzending, gevulde honeypot, te snel, zesde binnen het uur) en het bewijs van WEB-66, WEB-67 en WEB-70; (3) `vibe_meet.py` regel VIBE-36: `/xmlrpc.php` geeft geen 200, `/wp-json/wp/v2/users` geeft geen gebruikers, `/?author=1` stuurt niet door naar een auteurspagina, en `wp option get default_comment_status` is `closed`. Afgevinkt met alle drie.
- Norm: Zie WEB-66, WEB-67, WEB-70, WP-55 en WP-56.
- Bron: website.md Stap 9, O36 (geen rijenlijst, bento), O37 (vijf anti-spamlagen met Playwright getest) en O38 (reacties, xmlrpc en gebruikersenumeratie dicht); Stap 8 (harde regels beheer en anti-spam).
  
  ---
