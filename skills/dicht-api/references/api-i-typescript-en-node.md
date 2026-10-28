# API I: TypeScript en Node

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/api-code.md` (regelnummer in `regel-index.tsv`).

### API-67 Zet de strikte TypeScript-opties aan en maak de typecheck een gate
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik in elke `tsconfig.json` `"strict": true` plus `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch` en `noImplicitReturns`, en laat `tsc --noEmit` slagen voordat iets wordt gemerged of uitgerold.
- Bewijs: `tsc --showConfig` toont de zes opties. `npm run typecheck` is groen in CI en voor elke deploy. Let op: sinds TypeScript 6.0 (23-03-2026) is `strict` standaard `true`; zet het toch expliciet, want de registrar staat nog op `^5.7`. Op npm is TypeScript 7.0.2 de laatste versie (gemeten met `npm view typescript version` op 04-10-2026).
- Norm: ASVS 5.0.0 V15.3.5 (L2); besluit 10 van Marketing Maatwerk.
- Zie ook: GIT-57, GIT-58, GIT-59, API-68, API-78, WP-37, ARCH-40, ARCH-56, GIT-60, GIT-61, GIT-34, AI-85

### API-68 Lint met type-informatie en laat de build erop falen
hoog · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik typescript-eslint met minimaal `recommended-type-checked` (voor nieuw werk `strict-type-checked`) en behandel elke melding als fout in CI.
- Bewijs: `eslint . --max-warnings 0` is groen in CI. De configuratie toont de gekozen set. Let op: de `strict`-sets zijn volgens typescript-eslint niet stabiel onder semver; pin de versie.
- Norm: besluit 10 van Marketing Maatwerk; ASVS 5.0.0 V15.3.5 (L2).
- Zie ook: GIT-57, GIT-58, GIT-59, API-67, API-78, WP-37, ARCH-40, ARCH-56, GIT-60, GIT-61, GIT-34, AI-85

### API-69 Geen `any`, geen cast en geen `!` op data van buiten
middel · hard · api | app | mcp | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef alles wat van buiten komt het type `unknown` en maak er pas via een schema een concreet type van; gebruik geen `as X`, `any` of `!` om de compiler stil te krijgen.
- Bewijs: De lint van API-68 is groen zonder `eslint-disable` voor `no-explicit-any` of `no-unsafe-*`. `grep -rn "eslint-disable\|@ts-ignore\|@ts-expect-error" src` wordt per treffer onderbouwd.
- Norm: ASVS 5.0.0 V15.3.5 (L2).

### API-70 Handel elke promise af
hoog · hard · api | app | mcp · tegenlezer: scherpen (04-10-2026)
- Regel: Zet `await` voor elke promise of handel hem expliciet af met `.catch`; geef geen `async`-functie mee waar een synchrone callback wordt verwacht (`forEach`, `EventEmitter`, `setInterval`) zonder de fout daarin zelf af te vangen.
- Bewijs: `no-floating-promises` en `no-misused-promises` staan aan (API-68). Achtergrondtaken hebben een eigen `try/catch` die logt en alarmeert.
- Norm: ASVS 5.0.0 V16.5.3 (L2), V16.5.4 (L3).

### API-71 Koppel streams met `pipeline`
middel · richtlijn · api | app | mcp · tegenlezer: scherpen (04-10-2026)
- Regel: Gebruik `pipeline` uit `node:stream/promises` in plaats van `.pipe()`, en geef er een `signal` aan mee voor een time-out.
- Bewijs: `grep -rn "\.pipe(" src` is leeg of onderbouwd. Test: een afgebroken upload laat geen tijdelijk bestand achter.
- Norm: ASVS 5.0.0 V1.4.3 (L2).

### API-72 Draai op een ondersteunde Node-versie
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik een Node-versie die nog onderhoud krijgt en zet hem vast in `engines`, in het Docker-image en in de service-unit.
- Bewijs: `node -v` op de server en in het image toont 22.x (ondersteund tot 30-04-2027) of 24.x (tot 30-04-2028). `package.json` heeft `"engines": { "node": ">=22" }`.
- Norm: ASVS 5.0.0 V15.2.1 (L1).
- Zie ook: GIT-93, WP-52, DB-93, INFRA-22, INFRA-42, AI-54, SCR-33

### API-73 → ARCH-17
Samengevoegd: "Sluit netjes af" is gedekt door ARCH-17. Gebruik die regel.

### API-74 Geen debugmodus, inspector of experimentele functies in productie
hoog · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Start productie zonder `--inspect`, zonder watch-modus en zonder experimentele vlaggen, met `NODE_ENV=production`, en luister alleen op het adres dat nodig is.
- Bewijs: `systemctl cat <dienst>` en de `CMD` van het image tonen geen `--inspect` of `watch`. `ss -ltnp` toont geen 9229 en geen servicepoort op `0.0.0.0` die niet achter de firewall zit (zie INFRA).
- Norm: ASVS 5.0.0 V13.4.2 (L2), V15.2.3 (L2).
