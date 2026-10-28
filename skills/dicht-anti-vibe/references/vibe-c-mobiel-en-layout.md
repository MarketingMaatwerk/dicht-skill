# VIBE C: Mobiel en layout

Compacte regels van `dicht-anti-vibe`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/anti-vibe.md` (regelnummer in `regel-index.tsv`).

### VIBE-15 Geen horizontale scroll op 320, 360 en 390 px
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Op elke pagina is `document.documentElement.scrollWidth` op 320, 360 en 390 px niet breder dan de viewport, ook na het doorscrollen (reveal-animaties). Kaarten komen op smalle schermen verticaal binnen, niet zijwaarts.
- Bewijs: `vibe_meet.py` regel VIBE-15 (per pagina en per breedte, voor en na het doorscrollen; noemt het breedste element als het fout is). Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook PRIV-66 (WCAG 2.2 AA).
- Bron: website.md Stap 9, A4 (horizontale scroll) en W6 (reveal-animaties op mobiel); H paragraaf 2 punt 1, 16 en 20.

### VIBE-16 Het mobiele menu werkt, ook met het toetsenbord
hoog · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Op 390 px opent en sluit het menu (ook met Enter en Escape), elk item is bereikbaar met Tab en navigeert naar een bestaande pagina.
- Bewijs: `vibe_meet.py` regel VIBE-16: op 390 px wordt de menuknop gevonden (`button` met `aria-expanded` of `aria-controls`), met Enter geopend (links zichtbaar), met Escape of een tweede klik gesloten, en elke menulink staat in de linkcontrole van VIBE-03. Geen knop gevonden: `niet gemeten`, test dan met de hand in Playwright. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. Zie ook PRIV-66 (WCAG 2.2 AA).
- Bron: website.md Stap 9, A3 (mobiel menu); H paragraaf 2 punt 3.

### VIBE-17 De testronde scrollt elke pagina echt door, op elk formaat
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: De Playwright-ronde loopt alle viewports (mobiel tot en met desktop) en alle interactieve elementen langs, en scrollt elke pagina helemaal door voordat er een schermafbeelding of meting komt. Tel hoeveel elementen de zichtbaar-klasse kregen.
- Bewijs: `vibe_meet.py` scrollt elke pagina door en geeft bij VIBE-17 het aantal elementen dat na het scrollen een zichtbaar-klasse kreeg (`is-visible`, `in-view`, `aos-animate` en dergelijke) en de schermafbeeldingen per formaat. Afgevinkt met de uitvoer en de bekeken beelden.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk.
- Bron: website.md Stap 9, O0 (volledige Playwright-testronde) en W7 (scroll de pagina echt door in de test).

### VIBE-37 Klikdoelen zijn minstens 24 bij 24 px, of hebben genoeg ruimte
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Elk klikdoel (link, knop, veld, `summary`, element met een knoprol) is minstens 24 bij 24 CSS-pixels. Kleiner mag alleen als een cirkel van 24 px doorsnede om het midden van het doel geen ander doel raakt en geen cirkel van een ander klein doel, of bij een uitzondering uit WCAG 2.5.8: een link in een zin (Inline), een element waarvan de browser de maat bepaalt en dat niet is opgemaakt (User agent control), dezelfde functie elders op de pagina in een doel dat wel groot genoeg is (Equivalent), of een vorm die wezenlijk is of wettelijk vastligt (Essential).
- Bewijs: `vibe_meet.py` regel VIBE-37: op 390 px (tien pagina's) elk zichtbaar doel kleiner dan 24 bij 24 waarvan de cirkel van 24 px een ander doel of de cirkel van een ander klein doel raakt; links met tekst in een zin, niet-opgemaakte vinkjes en rondjes en visueel verborgen links (skiplinks, afgeknipt of hooguit 1 px) tellen niet mee; een icoon zonder tekst telt altijd mee. Elke melding is opgelost, of staat in het bewijsbestand met de uitzondering (Equivalent of Essential) en de reden. Afgevinkt met de uitvoer.
- Norm: WCAG 2.2 SC 2.5.8 Target Size (Minimum), niveau AA. Zie ook PRIV-66 (WCAG 2.2 AA).
- Bron: UI-tip 13 "Hit slop" (Marketing Maatwerk, 26-10-2026); https://www.w3.org/TR/WCAG22/#target-size-minimum (niveau) en https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html (tekst van het criterium en de meting van de Spacing-uitzondering), gelezen 26-10-2026.

### VIBE-38 Een submenu blijft open als de muis er recht naartoe gaat
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Een submenu dat op hover opent, blijft open als de muis van het menu-item recht naar het submenu beweegt, ook over de ruimte ertussen. Er zit geen gat zonder hover tussen item en submenu.
- Bewijs: `vibe_meet.py` regel VIBE-38: op de homepage op 1366 px gaat de muis bij elk submenu in header of nav dat op hover opent (de `ul` direct in de `li`, anders de laatste `div` waar de trigger niet in staat; hooguit vijf) in vijftien stappen van 25 ms van het midden van het menu-item naar het dichtstbijzijnde punt van het submenu; daarna is het submenu nog open. Alleen bewegen, niet klikken. Afgevinkt met de uitvoer.
- Norm: WCAG 2.2 SC 1.4.13 Content on Hover or Focus (Hoverable), niveau AA. Zie ook PRIV-66 (WCAG 2.2 AA).
- Bron: UI-tip 20 "Amazon safe triangle" (Marketing Maatwerk, 26-10-2026); https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html ("Custom tooltips, sub-menus, and other nonmodal popups that display on hover and focus are examples of additional content covered by this criterion."), gelezen 26-10-2026.

### VIBE-39 Een submenu blijft open op de schuine weg ernaartoe
laag · richtlijn · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Een submenu dat op hover opent, blijft ook open als de muis schuin van het menu-item naar de verste link in het submenu gaat en onderweg een ander menu-item kruist: met een veilige driehoek tussen muis en submenu, of met een vertraging die langer duurt dan zo'n beweging voordat een ander item het overneemt.
- Bewijs: `vibe_meet.py` regel VIBE-39: dezelfde submenu's als VIBE-38, nu schuin in vijftien stappen van 25 ms (samen ongeveer 0,4 s) naar de laatste link; `na te lopen` als het submenu daarna dicht is. Afwijken met reden in het bewijsbestand. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. WCAG 1.4.13 (VIBE-38) eist alleen de rechte weg.
- Bron: UI-tip 20 "Amazon safe triangle" (Marketing Maatwerk, 26-10-2026, met de uitleg: de diagonaal tussen cursor en submenu blijft open zodat de muis het hoofdmenu kan kruisen).

### VIBE-40 viewport-fit=cover alleen samen met safe-area-insets
middel · hard · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Zet een pagina `viewport-fit=cover` in de viewport-meta, dan houden vaste en kleverige balken, knoppen en randen hun inhoud binnen het veilige deel van het scherm met `env(safe-area-inset-*)`, bijvoorbeeld `padding-bottom: max(12px, env(safe-area-inset-bottom))`. Zonder `cover` is dit niet nodig.
- Bewijs: `vibe_meet.py` regel VIBE-40: op elke gemeten pagina met `viewport-fit=cover` staat `safe-area-inset` in de CSS (stijlbladen, `<style>` en `style`-attributen); een stijlblad van een ander domein dat niet te lezen is geeft `na te lopen`. Daarbij per vaste of kleverige balk: `grep -rn "safe-area-inset" <thema>/` toont de regel bij die balk. Afgevinkt met beide.
- Norm: MDN, viewport-meta: bij `cover` "It's highly recommended to use the safe area inset variables to ensure that important content doesn't end up outside the display."; MDN, `env()` (Baseline sinds januari 2020). Geen W3C-eis gelezen.
- Bron: UI-tip 14 "Safe area insets" (Marketing Maatwerk, 26-10-2026); https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport en https://developer.mozilla.org/en-US/docs/Web/CSS/env, gelezen 26-10-2026.

### VIBE-41 Cijfers in een tabel zijn even breed
laag · richtlijn · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: Een tabel met getallen of bedragen (prijzen, tarieven, uren, statistieken) toont cijfers van gelijke breedte: `font-variant-numeric: tabular-nums` op de tabel of de cellen, tenzij het lettertype al gelijke cijfers heeft.
- Bewijs: `vibe_meet.py` regel VIBE-41: op 390 px per tabel met minstens drie cellen die alleen een getal of bedrag bevatten, de breedte van tien keer 1 tegen tien keer 0 in die cel, dus met het lettertype en de instellingen van de cel; een verschil groter dan 0,5 px geeft `na te lopen`. Afwijken met reden. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. De werking: MDN font-variant-numeric (Baseline sinds januari 2020).
- Bron: UI-tip 16 "Tabular numbers" (Marketing Maatwerk, 26-10-2026); https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric ("activating the set of figures where numbers are all of the same size, allowing them to be easily aligned like in tables"), gelezen 26-10-2026.

### VIBE-42 Koppen over meer regels zijn gebalanceerd
laag · richtlijn · website | wp-thema | klantproject · tegenlezer: niet tegengelezen
- Regel: `h1`, `h2` en `h3` krijgen `text-wrap: balance`, zodat een kop van twee tot zes regels gelijk verdeelde regels heeft en geen los woord op de laatste regel.
- Bewijs: `vibe_meet.py` regel VIBE-42: op 390 px elke zichtbare `h1` tot en met `h3` van twee tot zes regels zonder `balance`; boven zes regels balanceert Chromium niet. Afwijken met reden. Afgevinkt met de uitvoer.
- Norm: Geen externe norm; eigen opleverregel van Marketing Maatwerk. De werking: MDN text-wrap (Baseline sinds maart 2024; "only supported for blocks of text spanning a limited number of lines (six or less for Chromium and ten or less for Firefox)"; de invloed op de snelheid noemt MDN "negligible").
- Bron: UI-tip 17 "Balanced headlines" (Marketing Maatwerk, 26-10-2026); https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap, gelezen 26-10-2026.
