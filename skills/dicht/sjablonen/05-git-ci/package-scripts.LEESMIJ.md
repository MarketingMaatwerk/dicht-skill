# package-scripts.json: de gate als een opdracht

Dekt: GIT-57, GIT-58, ARCH-12 (het testscript)

Neem het blok `scripts` over in `package.json` (JSON kent geen commentaar, daarom staat de uitleg hier).

- `npm run check` is de ene gate-opdracht, lokaal en in CI dezelfde (GIT-58). De volgorde is die van GIT-57: lint, typecheck, tests, daarna de scans.
- Aanpassen: de opdrachten achter `lint`, `typecheck` en `test` als het project iets anders gebruikt. De keten in `check` verandert niet.
- Controleren: `npm run check` geeft exitcode 0 in de worktree voor elke merge naar `main`; `.githooks/pre-push` roept dezelfde opdracht aan.
- `eslint .`, `tsc --noEmit` en `vitest run` zijn de gangbare aanroepen; het onderzoek schrijft alleen de namen van de scripts voor (lint, typecheck, test, scan, check). `TZ=UTC` voor de tests komt uit ARCH-12.
