# GIT G: Afhankelijkheden in npm

Compacte regels van `dicht-git`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/git-supplychain.md` (regelnummer in `regel-index.tsv`).

### GIT-69 Commit het lockfile en installeer alleen met npm ci
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Commit `package-lock.json` in elke applicatie en gebruik in de gate, in CI, in een Dockerfile en bij een deploy alleen `npm ci`; gebruik `npm install` alleen om bewust een afhankelijkheid toe te voegen of bij te werken.
- Bewijs: `git ls-files package-lock.json` geeft het bestand; `/usr/bin/grep -rnE "npm (install|i)( |$)" Dockerfile* .github/ scripts/ package.json` toont geen kale installatie; `npm ci` slaagt in een schone map. Afgevinkt met de drie.
- Norm: ASVS 5.0.0 V15.2.1 (L1) en V15.2.4 (L3); OWASP Top 10 2025 A03; OWASP Software Supply Chain Security Cheat Sheet (lockfile en versie vastzetten).
- Zie ook: SCR-32, GIT-72

### GIT-70 Lees de diff van het lockfile
middel · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Beoordeel bij elke wijziging van `package-lock.json` welke pakketten erbij komen en controleer dat elke `resolved`-URL naar `https://registry.npmjs.org/` wijst.
- Bewijs: `/usr/bin/grep -o '"resolved": "[^"]*"' package-lock.json | /usr/bin/grep -v 'https://registry.npmjs.org/' ` is leeg; in de merge-notitie staat de lijst van nieuwe pakketten (`git diff main -- package-lock.json | /usr/bin/grep '^+.*"node_modules/'`). Afgevinkt met beide. In npm 12 staan `allow-git` en `allow-remote` standaard op `none`; of dat elke vorm van lockfile-injectie afdekt, is niet bevestigd (punt 13).
- Norm: ASVS 5.0.0 V15.2.4 (L3); OWASP CI/CD CICD-SEC-3.

### GIT-71 Draai geen install-scripts van afhankelijkheden
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in de `.npmrc` van elk project `ignore-scripts=true` (npm tot en met 11) of gebruik npm 12 met een `allowScripts`-lijst in `package.json`, en keur per pakket met een buildstap de uitzondering goed.
- Bewijs: `npm config get ignore-scripts` in de projectmap geeft `true`, of `npm --version` is 12 of hoger en `package.json` bevat `allowScripts`; `npm query ":attr(scripts, [postinstall])"` toont welke pakketten een script hebben, en elk daarvan is beoordeeld. Afgevinkt met de uitvoer. Dit is niet genoeg op zichzelf: bij axios en bij debug (september 2025) zat de malware in de code zelf. Met `ignore-scripts=true` slaat npm ook de eigen `pre`- en `post`-scripts over.
- Norm: OWASP NPM Security Cheat Sheet punt 3; OWASP CI/CD CICD-SEC-3; OWASP Top 10 2025 A03.

### GIT-72 Installeer geen versie die jonger is dan zeven dagen
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel een wachttijd van 7 dagen in voor nieuwe versies: `min-release-age=7` in `.npmrc` (npm 11.10 of hoger) en `cooldown: default-days: 7` in `dependabot.yml`; wijk alleen af voor een beveiligingsfix, per pakket en met een notitie.
- Bewijs: `npm config get min-release-age` geeft 7 in de projectmap; `dependabot.yml` bevat de cooldown; een proef met een versie van gisteren (`npm install <pakket>@<nieuwste>`) wordt geweigerd. Afgevinkt met de drie. Op npm 10.9.8 bestaat de instelling niet: gebruik daar `npm install --before=<datum van zeven dagen geleden>` en de cooldown van Dependabot, of werk npm bij (GIT-74). Dependabot hanteert sinds 14-07-2026 zelf drie dagen; pnpm 11 en Yarn 4.15 één dag. Een beveiligingsfix die jonger is dan de wachttijd laat je toe met `min-release-age-exclude` (npm 12). De keuze voor 7 dagen is een afweging, geen norm (open vraag 5).
- Norm: besluit 16 (minimale leeftijd van een versie); OWASP NPM Security Cheat Sheet ("Hold-off on upgrading immediately to new versions"); OWASP Top 10 2025 A03.
- Zie ook: GIT-69, SCR-32

### GIT-73 Geen afhankelijkheden uit git of van een losse URL
middel · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Neem in `package.json` alleen afhankelijkheden op met een versie uit de registry; een verwijzing naar een git-repo of een tarball-URL mag alleen met een commit-SHA of hash, een reden en een einddatum. Toegestane uitzondering (besluit van Marketing Maatwerk, 04-10-2026): SheetJS van het CDN van de maker, per project besloten en vastgelegd met hash, reden en einddatum (INV-21).
- Bewijs: `npm query ":type(git)"` geeft een lege lijst, en `/usr/bin/grep -nE "\"(git\+|github:|https?://)" package.json` is leeg. Afgevinkt met beide, of met elke treffer naast zijn regel in het uitzonderingenregister (ARCH-30) met commit-SHA of hash, reden en einddatum; de bekende uitzondering is SheetJS van de eigen bron van de maker (INV-21). npm 12 zet `allow-git` en `allow-remote` standaard op `none`; in npm 11 is de standaard nog `all`.
- Norm: ASVS 5.0.0 V15.1.2 (L2, componenten uit vooraf bepaalde, vertrouwde bronnen) en V15.2.4 (L3).
- Zie ook: INV-21

### GIT-74 Gebruik een pakketbeheerder met veilige standaarden
middel · richtlijn · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Werk npm bij naar versie 12 (vraagt Node 22.22.2 of hoger, 24.15 of hoger, of 26) of gebruik pnpm 11, en leg de versie vast in `package.json` onder `packageManager` of `engines`.
- Bewijs: `npm --version` geeft 12 of hoger op de bouwmachine en in de Dockerfile; `package.json` noemt de versie. Afgevinkt met beide. Dit raakt alle projecten op een server tegelijk en vraagt een eigen test: npm 12 verwijdert `npm-shrinkwrap.json` en slaat install-scripts over die een project nu stilzwijgend nodig heeft (bijvoorbeeld native modules).
- Norm: OWASP Top 10 2025 A03 (ontwikkelgereedschap bijwerken); NIST SSDF PO.3.2.

### GIT-75 Onderbouw elke nieuwe afhankelijkheid kort
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf vóór het toevoegen van een directe afhankelijkheid een onderbouwing van vijf regels in de commit of PR: waarom nodig en waarom niet zelf of met wat er al is; onderhoud (laatste release en commits binnen twaalf maanden, aantal beheerders); bekende lekken en meldpunt; wat hij meebrengt (aantal transitieve pakketten, install-scripts); licentie.
- Bewijs: De commit die de afhankelijkheid toevoegt, bevat de vijf regels; `git log -p -- package.json` toont geen nieuwe directe afhankelijkheid zonder. Afgevinkt met de commit. Kijk ook op deps.dev naar de Scorecard-score en bekende lekken. Eén beheerder is geen afwijzing: de OpenSSF-gids zegt zelf dat veel breed gebruikte projecten er één hebben.
- Norm: NIST SSDF PW.4.1 (voorbeeld 1) en PW.4.4; ASVS 5.0.0 V15.1.4 (L3, risicovolle componenten benoemen); besluit 16.

### GIT-76 Laat Dependabot versies bijwerken, gegroepeerd en met wachttijd
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet in elke repo op GitHub een `.github/dependabot.yml` met een blok per ecosysteem dat de repo gebruikt (`npm`, `composer`, `docker`, `docker-compose`, `github-actions`), een wekelijks schema, de wachttijd van GIT-72 en een groep voor minor- en patch-updates.
- Bewijs: Het bestand bestaat met een blok per ecosysteem; er zijn Dependabot-PR's gezien of de afhankelijkheden zijn actueel (`npm outdated` toont geen achterstand van meer dan één major). Afgevinkt met bestand en uitvoer. Voor een repo zonder remote: plan `npm outdated` en de audit van GIT-61 maandelijks in. De wachttijd geldt niet voor beveiligingsupdates; die komen direct. Controleer dat de bibliotheken waarvan een regel een ondergrens noemt onder een blok vallen: `fastify`, `@fastify/multipart`, `fast-xml-parser`, `sharp`, `jsdom`, `dompurify`, `pdfjs-dist` en `dompdf/dompdf` (INV-03, INV-15, INV-23, INV-28, INV-38, INV-39, INV-65) en de mailbibliotheek (MSG-06); een Python-project draait `pip-audit` als gate (SCR-32).
- Norm: ASVS 5.0.0 V15.1.1 en V15.2.1 (L1); OWASP Top 10 2025 A03; besluit 15.
- Zie ook: GIT-28, GIT-52

### GIT-77 Leg hersteltermijnen vast en houd je eraan
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Leg per project in de documentatie vast binnen welke termijn een kwetsbare afhankelijkheid wordt bijgewerkt, en laat de gate falen als de termijn is overschreden. Vaste termijnen (besluit 22): kritiek of actief misbruikt (CISA KEV) binnen 48 uur; hoog binnen 7 dagen; middel binnen 30 dagen; laag bij de volgende reguliere update. De meldtermijnen bij een datalek (72 uur, PRIV-31) en voor een eigen product onder de Cyber Resilience Act (24 uur, PRIV-71) lopen los van deze hersteltermijnen.
- Bewijs: De termijnen staan in de README of `SECURITY.md`; de audit van GIT-61 is groen of elke open bevinding is jonger dan zijn termijn. Afgevinkt met document en uitvoer. De getallen zijn besluit 22 van Marketing Maatwerk; ASVS V15.1.1 eist dat ze vastliggen, niet welke.
- Norm: ASVS 5.0.0 V15.1.1 (L1) en V15.2.1 (L1); NIST SSDF RV.1.3.
- Zie ook: INFRA-24, ARCH-32, WP-49, GIT-88, DB-92, GIT-61, PRIV-73, MSG-06, SCR-32

### GIT-78 Controleer de naam van een pakket voordat je het installeert
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Draai vóór het installeren van een pakket dat je niet kent, en altijd bij een naam die een AI-assistent voorstelt, `npm view <naam>` en controleer dat het bestaat, een geschiedenis heeft, bij de verwachte repo hoort en geen bijna-gelijke populaire tegenhanger heeft.
- Bewijs: In de onderbouwing van GIT-75 staat de uitvoer van `npm view <naam> time.created repository.url` met een aanmaakdatum ouder dan een paar maanden en de verwachte repo. Afgevinkt met die uitvoer. Dit geldt in het bijzonder voor sessies van Claude: een pakket dat alleen uit het model komt, is niet bevestigd tot `npm view` het toont.
- Norm: OWASP NPM Security Cheat Sheet punt 10 en 13; OWASP Top 10 2025 A03; zie AI voor de modelkant.

### GIT-79 Geef interne pakketten een scope en een vaste registry
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Noem elk eigen, niet-publiek pakket `@<scope>/<naam>`, markeer het als `"private": true`, en koppel de scope in `.npmrc` aan de registry waar het vandaan hoort als die niet de publieke is.
- Bewijs: `/usr/bin/grep -rn '"name"' packages/*/package.json` toont alleen namen met scope en elk heeft `"private": true`; workspace-pakketten staan in het lockfile als `link` (`/usr/bin/grep -c '"link": true' package-lock.json` komt overeen met het aantal). Afgevinkt met beide. Voor de monorepo's van Marketing Maatwerk (workspaces zoals `@crm/<pakket>`) is het risico klein zolang niets naar een registry gaat; de regel wordt hard zodra er een privé-registry komt.
- Norm: ASVS 5.0.0 V15.2.4 (L3); OWASP NPM Security Cheat Sheet punt 12.

### GIT-80 Houd productie klein: geen dev-pakketten, geen ongebruikte pakketten
middel · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Installeer in een productie-image of op de server alleen productie-afhankelijkheden (`npm ci --omit=dev`), zet bouw- en testgereedschap in `devDependencies`, en verwijder elke afhankelijkheid die nergens meer wordt geïmporteerd.
- Bewijs: In de runtime-image geeft `npm ls --omit=dev --depth=0` dezelfde lijst als `npm ls --depth=0`; een hulpmiddel voor ongebruikte afhankelijkheden of een handmatige `grep` per pakketnaam toont geen pakket zonder import. Afgevinkt met beide. Let op het omgekeerde in een worktree: met `NODE_ENV=production` in de shell slaat `npm ci` de dev-pakketten over en ontbreken `tsc` en de testrunner (GIT-06).
- Norm: ASVS 5.0.0 V15.2.3 (L2); OWASP Top 10 2025 A03 ("Reduce attack surface by removing unused dependencies, unnecessary features, components, files, and documentation").
