# Index van de sjablonen

Gemaakt door `bouw-index.py` uit de koppen van de sjablonen. Niet met de hand wijzigen: pas de kop van het sjabloon of `STATUS` in het script aan en draai het opnieuw.

- 85 sjabloonbestanden, 80 gevalideerd en 5 niet gevalideerd.
- 314 verschillende regel-ID's, 490 koppelingen van regel naar sjabloon.
- Elk regel-ID is gecontroleerd tegen `skill/regel-index.tsv` en de vier batch-4-bestanden in `research/`.

Status:

- `gevalideerd`: het commando dat de juistheid aantoont is gedraaid en geslaagd, op de server of in een wegwerpcontainer; de tabel per bestand zegt welk commando en wat niet is gedraaid. Het is geen bewijs dat het sjabloon in een echt project werkt.
- `niet gevalideerd`: er is geen commando dat de juistheid aantoont; de reden staat in de tabel per bestand.
- `dekt gedeeltelijk`: het sjabloon voert de regel niet volledig uit; wat ontbreekt staat in de kop van het sjabloon.

## Per regel

| Regel | Sjabloon | Status |
|---|---|---|
| AI-02 | `10-bewijs-beheer/projectintake.md` | niet gevalideerd, dekt gedeeltelijk |
| AI-26 | `04-scripts/bulk.sh` | gevalideerd, dekt gedeeltelijk |
| AI-26 | `04-scripts/skelet.py` | gevalideerd, dekt gedeeltelijk |
| API-01 | `08-api/src/env.ts` | gevalideerd, dekt gedeeltelijk |
| API-01 | `08-api/src/routes/bestellen.ts` | gevalideerd |
| API-01 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd |
| API-02 | `08-api/src/routes/bestellen.ts` | gevalideerd |
| API-03 | `08-api/src/routes/bestellen.ts` | gevalideerd |
| API-05 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd |
| API-05 | `08-api/src/server.ts` | gevalideerd |
| API-09 | `08-api/src/routes/bestellen.ts` | gevalideerd |
| API-10 | `08-api/src/fouten.ts` | gevalideerd |
| API-10 | `08-api/src/server.ts` | gevalideerd |
| API-11 | `08-api/src/fouten.ts` | gevalideerd |
| API-11 | `08-api/src/server.ts` | gevalideerd |
| API-12 | `08-api/src/routes/bestellen.ts` | gevalideerd |
| API-12 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd |
| API-12 | `08-api/src/server.ts` | gevalideerd |
| API-12 | `11-berichten/afmelden-routes.ts` | gevalideerd |
| API-13 | `08-api/src/server.ts` | gevalideerd |
| API-18 | `01-nginx/conf.d/00-dicht-http.conf` | gevalideerd |
| API-18 | `01-nginx/conf.d/site-voorbeeld.conf` | gevalideerd |
| API-18 | `08-api/src/server.ts` | gevalideerd |
| API-19 | `08-api/src/server.ts` | gevalideerd |
| API-20 | `08-api/src/routes/bestellen.ts` | gevalideerd |
| API-20 | `08-api/src/server.ts` | gevalideerd, dekt gedeeltelijk |
| API-22 | `08-api/src/server.ts` | gevalideerd |
| API-27 | `08-api/src/routes/bestellen.ts` | gevalideerd |
| API-30 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd |
| API-31 | `08-api/migraties/idempotentie.sql` | gevalideerd |
| API-33 | `08-api/migraties/idempotentie.sql` | gevalideerd |
| API-33 | `08-api/src/routes/bestellen.ts` | gevalideerd |
| API-35 | `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd |
| API-35 | `08-api/src/routes/bestellen.ts` | gevalideerd |
| API-36 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd |
| API-37 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd |
| API-38 | `08-api/migraties/idempotentie.sql` | gevalideerd, dekt gedeeltelijk |
| API-38 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd |
| API-39 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd |
| API-40 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd, dekt gedeeltelijk |
| API-45 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd |
| API-65 | `08-api/src/env.ts` | gevalideerd |
| API-66 | `04-scripts/skelet.py` | gevalideerd |
| API-66 | `08-api/src/server.ts` | gevalideerd |
| API-67 | `07-typescript-tests/tsconfig.json` | gevalideerd, dekt gedeeltelijk |
| API-68 | `07-typescript-tests/eslint.config.mjs` | gevalideerd |
| API-69 | `07-typescript-tests/eslint.config.mjs` | gevalideerd |
| API-70 | `07-typescript-tests/eslint.config.mjs` | gevalideerd |
| API-72 | `02-docker/Dockerfile` | gevalideerd |
| API-72 | `03-systemd/voorbeeld.service` | gevalideerd |
| API-74 | `02-docker/Dockerfile` | gevalideerd |
| API-74 | `03-systemd/voorbeeld.service` | gevalideerd |
| API-74 | `08-api/src/server.ts` | gevalideerd |
| API-75 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| API-75 | `09-wordpress/mu-plugins/dicht-testomgeving-afschermen.php` | gevalideerd |
| ARCH-01 | `10-bewijs-beheer/projectintake.md` | niet gevalideerd |
| ARCH-02 | `07-typescript-tests/eslint.config.mjs` | gevalideerd, dekt gedeeltelijk |
| ARCH-05 | `02-docker/.dockerignore` | gevalideerd |
| ARCH-05 | `02-docker/Dockerfile` | gevalideerd |
| ARCH-07 | `08-api/src/env.ts` | gevalideerd |
| ARCH-08 | `08-api/src/env.ts` | gevalideerd |
| ARCH-09 | `02-docker/Dockerfile` | gevalideerd |
| ARCH-09 | `08-api/src/server.ts` | gevalideerd |
| ARCH-12 | `02-docker/compose.yml` | gevalideerd |
| ARCH-12 | `03-systemd/voorbeeld.service` | gevalideerd |
| ARCH-12 | `05-git-ci/package-scripts.json` | gevalideerd, dekt gedeeltelijk |
| ARCH-12 | `07-typescript-tests/playwright.config.ts` | gevalideerd |
| ARCH-12 | `07-typescript-tests/vitest.config.ts` | gevalideerd, dekt gedeeltelijk |
| ARCH-17 | `03-systemd/voorbeeld.service` | gevalideerd |
| ARCH-17 | `08-api/src/server.ts` | gevalideerd |
| ARCH-20 | `08-api/migraties/idempotentie.sql` | gevalideerd, dekt gedeeltelijk |
| ARCH-20 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd |
| ARCH-24 | `10-bewijs-beheer/bewijsbestand.md` | gevalideerd |
| ARCH-28 | `04-scripts/bulk.sh` | gevalideerd, dekt gedeeltelijk |
| ARCH-28 | `04-scripts/skelet.py` | gevalideerd |
| ARCH-30 | `10-bewijs-beheer/bewijsbestand.md` | gevalideerd, dekt gedeeltelijk |
| ARCH-30 | `10-bewijs-beheer/controleer-bewijs.py` | gevalideerd, dekt gedeeltelijk |
| ARCH-30 | `10-bewijs-beheer/uitzonderingen.md` | gevalideerd |
| ARCH-34 | `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd |
| ARCH-35 | `07-typescript-tests/tests/tenant-isolatie.test.ts` | gevalideerd |
| ARCH-36 | `07-typescript-tests/e2e/voorbeeld.spec.ts` | gevalideerd |
| ARCH-36 | `07-typescript-tests/eslint.config.mjs` | gevalideerd, dekt gedeeltelijk |
| ARCH-37 | `07-typescript-tests/e2e/opzet.ts` | gevalideerd |
| ARCH-37 | `07-typescript-tests/e2e/voorbeeld.spec.ts` | gevalideerd |
| ARCH-37 | `07-typescript-tests/eslint.config.mjs` | gevalideerd, dekt gedeeltelijk |
| ARCH-38 | `07-typescript-tests/e2e/voorbeeld.spec.ts` | gevalideerd, dekt gedeeltelijk |
| ARCH-38 | `07-typescript-tests/playwright.config.ts` | gevalideerd, dekt gedeeltelijk |
| ARCH-38 | `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd, dekt gedeeltelijk |
| ARCH-39 | `07-typescript-tests/playwright.config.ts` | gevalideerd |
| ARCH-44 | `07-typescript-tests/stryker.config.json` | gevalideerd, dekt gedeeltelijk |
| ARCH-45 | `07-typescript-tests/vitest.config.ts` | gevalideerd |
| ARCH-46 | `07-typescript-tests/e2e/voorbeeld.spec.ts` | gevalideerd |
| ARCH-48 | `07-typescript-tests/e2e/voorbeeld.spec.ts` | gevalideerd |
| ARCH-49 | `05-git-ci/.gitignore` | gevalideerd, dekt gedeeltelijk |
| ARCH-49 | `07-typescript-tests/playwright.config.ts` | gevalideerd |
| ARCH-50 | `07-typescript-tests/e2e/voorbeeld.spec.ts` | gevalideerd |
| ARCH-50 | `07-typescript-tests/tests/opzet.ts` | gevalideerd |
| ARCH-50 | `07-typescript-tests/vitest.config.ts` | gevalideerd, dekt gedeeltelijk |
| ARCH-52 | `10-bewijs-beheer/bewijsbestand.md` | gevalideerd |
| ARCH-53 | `10-bewijs-beheer/bewijsbestand.md` | gevalideerd |
| ARCH-53 | `10-bewijs-beheer/controleer-bewijs.py` | gevalideerd, dekt gedeeltelijk |
| ARCH-55 | `07-typescript-tests/eslint.config.mjs` | gevalideerd |
| ARCH-55 | `10-bewijs-beheer/uitzonderingen.md` | gevalideerd, dekt gedeeltelijk |
| ARCH-58 | `04-scripts/skelet.py` | gevalideerd, dekt gedeeltelijk |
| ARCH-58 | `08-api/src/server.ts` | gevalideerd, dekt gedeeltelijk |
| ARCH-60 | `08-api/src/server.ts` | gevalideerd |
| ARCH-61 | `03-systemd/voorbeeld.service` | gevalideerd |
| ARCH-62 | `03-systemd/meld-fout.sh` | gevalideerd |
| ARCH-62 | `04-scripts/skelet.py` | gevalideerd |
| ARCH-62 | `08-api/src/server.ts` | gevalideerd |
| ARCH-67 | `02-docker/compose.yml` | gevalideerd |
| ARCH-67 | `08-api/src/server.ts` | gevalideerd |
| ARCH-69 | `03-systemd/meld-fout@.service` | gevalideerd, dekt gedeeltelijk |
| ARCH-72 | `01-nginx/50x.html` | gevalideerd |
| ARCH-72 | `01-nginx/conf.d/site-voorbeeld.conf` | gevalideerd |
| ARCH-80 | `10-bewijs-beheer/projectintake.md` | niet gevalideerd, dekt gedeeltelijk |
| ARCH-80 | `10-bewijs-beheer/threat-model.md` | niet gevalideerd |
| ARCH-81 | `10-bewijs-beheer/threat-model.md` | niet gevalideerd, dekt gedeeltelijk |
| ARCH-82 | `10-bewijs-beheer/threat-model.md` | niet gevalideerd, dekt gedeeltelijk |
| ARCH-85 | `06-database/controleer-backup.sh` | gevalideerd |
| ARCH-85 | `09-wordpress/controleer-blokkades.sh` | gevalideerd |
| ARCH-85 | `10-bewijs-beheer/controleer-bewijs.py` | gevalideerd |
| AUTH-57 | `11-berichten/afmelden.ts` | gevalideerd |
| AUTH-57 | `11-berichten/webhook-verificatie.ts` | gevalideerd |
| AUTH-58 | `11-berichten/webhook-verificatie.ts` | gevalideerd |
| AUTH-60 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd (ID is samengevoegd, zie de kanonieke regel in regel-index.tsv) |
| AUTH-72 | `06-database/tenant-context.ts` | gevalideerd |
| AUTH-72 | `08-api/src/routes/bestellen.ts` | gevalideerd |
| AUTH-74 | `06-database/migraties/0001_tenant_tabel_met_rls.sql` | gevalideerd |
| AUTH-74 | `06-database/tenant-context.ts` | gevalideerd |
| AUTH-74 | `07-typescript-tests/tests/tenant-isolatie.test.ts` | gevalideerd |
| AUTH-75 | `06-database/tenant-context.ts` | gevalideerd (ID is samengevoegd, zie de kanonieke regel in regel-index.tsv) |
| AUTH-77 | `07-typescript-tests/tests/tenant-isolatie.test.ts` | gevalideerd, dekt gedeeltelijk |
| BIZ-10 | `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd |
| BIZ-11 | `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd |
| BIZ-12 | `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd |
| BIZ-23 | `04-scripts/bulk.sh` | gevalideerd, dekt gedeeltelijk |
| BIZ-23 | `04-scripts/skelet.py` | gevalideerd, dekt gedeeltelijk |
| BIZ-26 | `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd |
| BIZ-27 | `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd, dekt gedeeltelijk |
| BIZ-29 | `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd, dekt gedeeltelijk |
| BIZ-33 | `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd, dekt gedeeltelijk |
| BIZ-39 | `08-api/migraties/idempotentie.sql` | gevalideerd, dekt gedeeltelijk |
| BIZ-39 | `08-api/src/routes/bestellen.ts` | gevalideerd, dekt gedeeltelijk |
| BIZ-52 | `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd, dekt gedeeltelijk |
| DB-01 | `06-database/rollen.sql` | gevalideerd |
| DB-02 | `06-database/rollen.sql` | gevalideerd |
| DB-03 | `06-database/rollen.sql` | gevalideerd |
| DB-04 | `06-database/rollen.sql` | gevalideerd |
| DB-05 | `06-database/rollen.sql` | gevalideerd |
| DB-06 | `06-database/rollen.sql` | gevalideerd |
| DB-07 | `06-database/rollen.sql` | gevalideerd |
| DB-08 | `06-database/rollen.sql` | gevalideerd |
| DB-10 | `06-database/rollen.sql` | gevalideerd, dekt gedeeltelijk |
| DB-11 | `10-bewijs-beheer/projectintake.md` | niet gevalideerd, dekt gedeeltelijk |
| DB-12 | `06-database/migraties/0001_tenant_tabel_met_rls.sql` | gevalideerd |
| DB-13 | `06-database/migraties/0001_tenant_tabel_met_rls.sql` | gevalideerd |
| DB-14 | `06-database/rollen.sql` | gevalideerd |
| DB-14 | `07-typescript-tests/tests/tenant-isolatie.test.ts` | gevalideerd |
| DB-15 | `06-database/migraties/0001_tenant_tabel_met_rls.sql` | gevalideerd |
| DB-16 | `06-database/tenant-context.ts` | gevalideerd |
| DB-17 | `06-database/migraties/0001_tenant_tabel_met_rls.sql` | gevalideerd |
| DB-17 | `06-database/tenant-context.ts` | gevalideerd |
| DB-17 | `07-typescript-tests/tests/tenant-isolatie.test.ts` | gevalideerd |
| DB-20 | `06-database/migraties/0001_tenant_tabel_met_rls.sql` | gevalideerd |
| DB-21 | `06-database/rollen.sql` | gevalideerd |
| DB-22 | `07-typescript-tests/tests/tenant-isolatie.test.ts` | gevalideerd, dekt gedeeltelijk |
| DB-30 | `06-database/migraties/0001_tenant_tabel_met_rls.sql` | gevalideerd |
| DB-30 | `06-database/migraties/0002_expand.sql` | gevalideerd |
| DB-31 | `06-database/migraties/0002_expand.sql` | gevalideerd |
| DB-31 | `06-database/migraties/0005_contract.sql` | gevalideerd |
| DB-32 | `06-database/migraties/0001_tenant_tabel_met_rls.sql` | gevalideerd |
| DB-32 | `06-database/migraties/0002_expand.sql` | gevalideerd |
| DB-32 | `06-database/migraties/0004_valideer.sql` | gevalideerd, dekt gedeeltelijk |
| DB-32 | `06-database/migraties/0005_contract.sql` | gevalideerd |
| DB-33 | `06-database/migraties/0003_expand_index.sql` | gevalideerd |
| DB-34 | `06-database/migraties/0002_expand.sql` | gevalideerd |
| DB-34 | `06-database/migraties/0004_valideer.sql` | gevalideerd |
| DB-35 | `06-database/migraties/0004_valideer.sql` | gevalideerd |
| DB-36 | `06-database/migraties/0002_expand.sql` | gevalideerd, dekt gedeeltelijk |
| DB-38 | `06-database/migraties/backfill.sh` | gevalideerd |
| DB-40 | `06-database/migraties/0002_expand.sql` | gevalideerd |
| DB-40 | `06-database/migraties/0005_contract.sql` | gevalideerd, dekt gedeeltelijk |
| DB-43 | `06-database/migraties/0001_tenant_tabel_met_rls.sql` | gevalideerd |
| DB-44 | `06-database/backup.sh` | gevalideerd |
| DB-45 | `06-database/backup.sh` | gevalideerd |
| DB-46 | `06-database/herstelproef.sh` | gevalideerd |
| DB-47 | `06-database/backup.sh` | gevalideerd, dekt gedeeltelijk |
| DB-47 | `06-database/controleer-backup.sh` | gevalideerd |
| DB-48 | `06-database/backup.sh` | gevalideerd |
| DB-50 | `06-database/backup.sh` | gevalideerd |
| DB-50 | `06-database/herstelproef.sh` | gevalideerd |
| DB-57 | `06-database/backup.sh` | gevalideerd, dekt gedeeltelijk |
| DB-61 | `06-database/rollen.sql` | gevalideerd |
| DB-62 | `08-api/src/db.ts` | gevalideerd |
| DB-63 | `08-api/src/db.ts` | gevalideerd, dekt gedeeltelijk |
| DB-65 | `06-database/rollen.sql` | gevalideerd |
| DB-65 | `08-api/src/db.ts` | gevalideerd, dekt gedeeltelijk |
| DB-68 | `08-api/migraties/idempotentie.sql` | gevalideerd |
| DB-68 | `08-api/src/routes/mollie-webhook.ts` | gevalideerd |
| DB-74 | `06-database/migraties/0001_tenant_tabel_met_rls.sql` | gevalideerd |
| DB-98 | `02-docker/compose.yml` | gevalideerd |
| GIT-10 | `05-git-ci/.gitignore` | gevalideerd |
| GIT-24 | `05-git-ci/ruleset-main.json` | gevalideerd, dekt gedeeltelijk |
| GIT-25 | `05-git-ci/ruleset-main.json` | gevalideerd |
| GIT-26 | `05-git-ci/ruleset-tags.json` | gevalideerd, dekt gedeeltelijk |
| GIT-29 | `05-git-ci/CODEOWNERS` | niet gevalideerd, dekt gedeeltelijk |
| GIT-30 | `05-git-ci/SECURITY.md` | niet gevalideerd (ID is samengevoegd, zie de kanonieke regel in regel-index.tsv) |
| GIT-32 | `05-git-ci/.gitignore` | gevalideerd, dekt gedeeltelijk |
| GIT-33 | `05-git-ci/.pre-commit-config.yaml` | gevalideerd |
| GIT-33 | `05-git-ci/lefthook.yml` | gevalideerd |
| GIT-34 | `05-git-ci/scripts/scan.sh` | gevalideerd |
| GIT-41 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-43 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-44 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-45 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-46 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-47 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-48 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-52 | `05-git-ci/.github/dependabot.yml` | gevalideerd |
| GIT-53 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-55 | `05-git-ci/.github/dependabot.yml` | gevalideerd, dekt gedeeltelijk |
| GIT-56 | `05-git-ci/scripts/scan.sh` | gevalideerd |
| GIT-57 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-57 | `05-git-ci/package-scripts.json` | gevalideerd |
| GIT-58 | `05-git-ci/.githooks/pre-push` | gevalideerd |
| GIT-58 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-58 | `05-git-ci/lefthook.yml` | gevalideerd |
| GIT-58 | `05-git-ci/package-scripts.json` | gevalideerd |
| GIT-59 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-59 | `05-git-ci/scripts/scan.sh` | gevalideerd |
| GIT-60 | `05-git-ci/scripts/scan.sh` | gevalideerd |
| GIT-61 | `05-git-ci/scripts/scan.sh` | gevalideerd |
| GIT-62 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-65 | `10-bewijs-beheer/controleer-bewijs.py` | gevalideerd, dekt gedeeltelijk |
| GIT-65 | `10-bewijs-beheer/uitzonderingen.md` | gevalideerd |
| GIT-66 | `02-docker/Dockerfile` | gevalideerd, dekt gedeeltelijk |
| GIT-67 | `10-bewijs-beheer/bewijsbestand.md` | gevalideerd (ID is samengevoegd, zie de kanonieke regel in regel-index.tsv) |
| GIT-68 | `10-bewijs-beheer/bewijsbestand.md` | gevalideerd |
| GIT-69 | `02-docker/Dockerfile` | gevalideerd |
| GIT-69 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd |
| GIT-71 | `02-docker/Dockerfile` | gevalideerd |
| GIT-71 | `05-git-ci/.github/workflows/gate.yml` | gevalideerd, dekt gedeeltelijk |
| GIT-71 | `05-git-ci/.npmrc` | gevalideerd |
| GIT-72 | `05-git-ci/.github/dependabot.yml` | gevalideerd |
| GIT-72 | `05-git-ci/.npmrc` | gevalideerd, dekt gedeeltelijk |
| GIT-76 | `05-git-ci/.github/dependabot.yml` | gevalideerd |
| GIT-80 | `02-docker/Dockerfile` | gevalideerd |
| GIT-91 | `02-docker/Dockerfile` | gevalideerd |
| GIT-91 | `02-docker/compose.yml` | gevalideerd |
| GIT-92 | `05-git-ci/.github/dependabot.yml` | gevalideerd |
| GIT-93 | `02-docker/Dockerfile` | gevalideerd |
| GIT-94 | `02-docker/Dockerfile` | gevalideerd |
| GIT-95 | `02-docker/.dockerignore` | gevalideerd |
| GIT-95 | `02-docker/Dockerfile` | gevalideerd |
| GIT-96 | `02-docker/Dockerfile` | gevalideerd |
| GIT-105 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| INFRA-13 | `01-nginx/conf.d/site-voorbeeld.conf` | gevalideerd |
| INFRA-13 | `02-docker/compose.yml` | gevalideerd |
| INFRA-17 | `02-docker/compose.yml` | gevalideerd |
| INFRA-26 | `02-docker/compose.yml` | gevalideerd |
| INFRA-27 | `02-docker/Dockerfile` | gevalideerd |
| INFRA-27 | `02-docker/compose.yml` | gevalideerd |
| INFRA-28 | `02-docker/compose.yml` | gevalideerd |
| INFRA-29 | `02-docker/compose.yml` | gevalideerd |
| INFRA-30 | `02-docker/compose.yml` | gevalideerd |
| INFRA-31 | `02-docker/compose.yml` | gevalideerd |
| INFRA-32 | `02-docker/compose.yml` | gevalideerd, dekt gedeeltelijk |
| INFRA-33 | `02-docker/daemon.json` | gevalideerd |
| INFRA-35 | `02-docker/compose.yml` | gevalideerd, dekt gedeeltelijk |
| INFRA-37 | `02-docker/.dockerignore` | gevalideerd |
| INFRA-37 | `02-docker/Dockerfile` | gevalideerd |
| INFRA-39 | `02-docker/compose.yml` | gevalideerd |
| INFRA-40 | `02-docker/compose.yml` | gevalideerd |
| INFRA-43 | `01-nginx/conf.d/01-default-server.conf` | gevalideerd |
| INFRA-44 | `01-nginx/conf.d/00-dicht-http.conf` | gevalideerd |
| INFRA-45 | `01-nginx/conf.d/00-dicht-http.conf` | gevalideerd |
| INFRA-45 | `01-nginx/conf.d/site-voorbeeld.conf` | gevalideerd |
| INFRA-46 | `01-nginx/conf.d/00-dicht-http.conf` | gevalideerd |
| INFRA-46 | `01-nginx/conf.d/site-voorbeeld.conf` | gevalideerd |
| INFRA-47 | `01-nginx/nginx-test.conf` | gevalideerd, dekt gedeeltelijk |
| INFRA-49 | `01-nginx/conf.d/00-dicht-http.conf` | gevalideerd (ID is samengevoegd, zie de kanonieke regel in regel-index.tsv) |
| INFRA-49 | `01-nginx/controleer-headers.sh` | gevalideerd (ID is samengevoegd, zie de kanonieke regel in regel-index.tsv) |
| INFRA-56 | `11-berichten/dns-records.zone` | gevalideerd |
| INFRA-57 | `11-berichten/dns-records.zone` | gevalideerd |
| INFRA-58 | `11-berichten/dns-records.zone` | gevalideerd |
| INFRA-59 | `11-berichten/dns-records.zone` | gevalideerd |
| INFRA-60 | `11-berichten/dns-records.zone` | gevalideerd |
| INFRA-65 | `05-git-ci/SECURITY.md` | niet gevalideerd, dekt gedeeltelijk |
| INFRA-65 | `05-git-ci/security.txt` | niet gevalideerd |
| INFRA-66 | `03-systemd/voorbeeld-taak.service` | gevalideerd |
| INFRA-66 | `03-systemd/voorbeeld.service` | gevalideerd |
| INFRA-67 | `03-systemd/voorbeeld-taak.service` | gevalideerd |
| INFRA-67 | `03-systemd/voorbeeld.service` | gevalideerd |
| INFRA-68 | `03-systemd/voorbeeld.service` | gevalideerd |
| INFRA-69 | `03-systemd/crontab-voorbeeld` | gevalideerd, dekt gedeeltelijk |
| INFRA-69 | `03-systemd/meld-fout.sh` | gevalideerd |
| INFRA-69 | `03-systemd/meld-fout@.service` | gevalideerd |
| INFRA-69 | `03-systemd/voorbeeld-taak.service` | gevalideerd |
| INFRA-69 | `04-scripts/taak.sh` | gevalideerd, dekt gedeeltelijk |
| INFRA-70 | `03-systemd/crontab-voorbeeld` | gevalideerd |
| INFRA-70 | `03-systemd/voorbeeld-taak.service` | gevalideerd |
| INFRA-70 | `04-scripts/taak.sh` | gevalideerd |
| INFRA-72 | `02-docker/compose.yml` | gevalideerd |
| INFRA-72 | `03-systemd/voorbeeld-taak.service` | gevalideerd |
| INFRA-72 | `03-systemd/voorbeeld.service` | gevalideerd |
| INFRA-82 | `06-database/herstelproef.sh` | gevalideerd, dekt gedeeltelijk |
| INFRA-87 | `06-database/controleer-backup.sh` | gevalideerd, dekt gedeeltelijk |
| INFRA-101 | `09-wordpress/controleer-blokkades.sh` | gevalideerd |
| INV-50 | `01-nginx/conf.d/site-voorbeeld.conf` | gevalideerd |
| INV-50 | `01-nginx/snippets/proxy-headers.conf` | gevalideerd |
| MSG-02 | `11-berichten/dns-records.zone` | gevalideerd |
| MSG-07 | `11-berichten/afmelden-routes.ts` | gevalideerd |
| MSG-07 | `11-berichten/afmelden.test.ts` | gevalideerd |
| MSG-07 | `11-berichten/afmelden.ts` | gevalideerd, dekt gedeeltelijk |
| MSG-08 | `11-berichten/afmelden-routes.ts` | gevalideerd |
| MSG-09 | `11-berichten/afmelden-routes.ts` | gevalideerd |
| MSG-09 | `11-berichten/afmelden.test.ts` | gevalideerd |
| MSG-09 | `11-berichten/afmelden.ts` | gevalideerd |
| MSG-10 | `11-berichten/afmelden-routes.ts` | gevalideerd, dekt gedeeltelijk |
| MSG-12 | `11-berichten/dns-records.zone` | gevalideerd, dekt gedeeltelijk |
| MSG-35 | `11-berichten/webhook-verificatie.test.ts` | gevalideerd |
| MSG-35 | `11-berichten/webhook-verificatie.ts` | gevalideerd |
| MSG-36 | `11-berichten/webhook-verificatie.test.ts` | gevalideerd |
| MSG-36 | `11-berichten/webhook-verificatie.ts` | gevalideerd |
| MSG-39 | `11-berichten/webhook-verificatie.test.ts` | gevalideerd |
| MSG-39 | `11-berichten/webhook-verificatie.ts` | gevalideerd |
| MSG-41 | `03-systemd/meld-fout.sh` | gevalideerd |
| MSG-43 | `11-berichten/webhook-verificatie.test.ts` | gevalideerd |
| MSG-43 | `11-berichten/webhook-verificatie.ts` | gevalideerd |
| PRIV-01 | `10-bewijs-beheer/projectintake.md` | niet gevalideerd |
| PRIV-37 | `10-bewijs-beheer/projectintake.md` | niet gevalideerd |
| PRIV-51 | `04-scripts/bulk.sh` | gevalideerd, dekt gedeeltelijk |
| PRIV-51 | `04-scripts/skelet.py` | gevalideerd, dekt gedeeltelijk |
| PRIV-52 | `10-bewijs-beheer/projectintake.md` | niet gevalideerd |
| PRIV-59 | `10-bewijs-beheer/projectintake.md` | niet gevalideerd |
| PRIV-65 | `10-bewijs-beheer/projectintake.md` | niet gevalideerd |
| PRIV-70 | `10-bewijs-beheer/projectintake.md` | niet gevalideerd |
| PRIV-72 | `05-git-ci/SECURITY.md` | niet gevalideerd |
| PRIV-72 | `05-git-ci/security.txt` | niet gevalideerd |
| SCR-01 | `03-systemd/meld-fout.sh` | gevalideerd |
| SCR-01 | `04-scripts/bulk.sh` | gevalideerd |
| SCR-01 | `04-scripts/lus.sh` | gevalideerd |
| SCR-01 | `04-scripts/taak.sh` | gevalideerd |
| SCR-01 | `05-git-ci/scripts/scan.sh` | gevalideerd |
| SCR-01 | `06-database/backup.sh` | gevalideerd |
| SCR-01 | `06-database/herstelproef.sh` | gevalideerd |
| SCR-01 | `06-database/migraties/backfill.sh` | gevalideerd |
| SCR-02 | `04-scripts/taak.sh` | gevalideerd |
| SCR-03 | `04-scripts/taak.sh` | gevalideerd |
| SCR-04 | `04-scripts/bulk.sh` | gevalideerd |
| SCR-04 | `04-scripts/lus.sh` | gevalideerd |
| SCR-04 | `04-scripts/taak.sh` | gevalideerd |
| SCR-04 | `06-database/backup.sh` | gevalideerd |
| SCR-04 | `06-database/herstelproef.sh` | gevalideerd |
| SCR-05 | `04-scripts/taak.sh` | gevalideerd |
| SCR-06 | `03-systemd/meld-fout.sh` | gevalideerd |
| SCR-06 | `04-scripts/bulk.sh` | gevalideerd |
| SCR-06 | `04-scripts/taak.sh` | gevalideerd |
| SCR-08 | `04-scripts/bulk.sh` | gevalideerd |
| SCR-08 | `04-scripts/taak.sh` | gevalideerd |
| SCR-11 | `06-database/migraties/backfill.sh` | gevalideerd |
| SCR-11 | `06-database/rollen.sql` | gevalideerd |
| SCR-14 | `04-scripts/taak.sh` | gevalideerd |
| SCR-14 | `06-database/herstelproef.sh` | gevalideerd |
| SCR-15 | `06-database/herstelproef.sh` | gevalideerd |
| SCR-16 | `04-scripts/bulk.sh` | gevalideerd |
| SCR-16 | `04-scripts/taak.sh` | gevalideerd |
| SCR-16 | `06-database/backup.sh` | gevalideerd |
| SCR-17 | `04-scripts/taak.sh` | gevalideerd |
| SCR-18 | `03-systemd/crontab-voorbeeld` | gevalideerd |
| SCR-18 | `04-scripts/bulk.sh` | gevalideerd |
| SCR-18 | `04-scripts/taak.sh` | gevalideerd |
| SCR-18 | `06-database/backup.sh` | gevalideerd |
| SCR-19 | `03-systemd/meld-fout.sh` | gevalideerd |
| SCR-19 | `04-scripts/skelet.py` | gevalideerd |
| SCR-19 | `04-scripts/taak.sh` | gevalideerd |
| SCR-20 | `03-systemd/voorbeeld-taak.service` | gevalideerd |
| SCR-20 | `03-systemd/voorbeeld.service` | gevalideerd |
| SCR-20 | `04-scripts/taak.sh` | gevalideerd |
| SCR-21 | `03-systemd/meld-fout.sh` | gevalideerd |
| SCR-21 | `04-scripts/taak.sh` | gevalideerd |
| SCR-23 | `04-scripts/gate-scripts.sh` | gevalideerd |
| SCR-23 | `05-git-ci/scripts/scan.sh` | gevalideerd |
| SCR-24 | `04-scripts/skelet.py` | gevalideerd |
| SCR-25 | `04-scripts/skelet.py` | gevalideerd |
| SCR-26 | `04-scripts/skelet.py` | gevalideerd |
| SCR-31 | `04-scripts/skelet.py` | gevalideerd |
| SCR-32 | `04-scripts/gate-scripts.sh` | gevalideerd, dekt gedeeltelijk |
| SCR-35 | `04-scripts/gate-scripts.sh` | gevalideerd |
| SCR-36 | `03-systemd/voorbeeld-taak.service` | gevalideerd |
| SCR-37 | `03-systemd/crontab-voorbeeld` | gevalideerd |
| SCR-37 | `04-scripts/taak.sh` | gevalideerd |
| SCR-38 | `03-systemd/crontab-voorbeeld` | gevalideerd |
| SCR-38 | `03-systemd/voorbeeld-taak.service` | gevalideerd |
| SCR-38 | `04-scripts/bulk.sh` | gevalideerd, dekt gedeeltelijk |
| SCR-39 | `03-systemd/voorbeeld-taak.timer` | gevalideerd |
| SCR-40 | `03-systemd/crontab-voorbeeld` | gevalideerd, dekt gedeeltelijk |
| SCR-40 | `03-systemd/voorbeeld-taak.timer` | gevalideerd |
| SCR-40 | `04-scripts/skelet.py` | gevalideerd |
| SCR-40 | `04-scripts/taak.sh` | gevalideerd |
| SCR-41 | `03-systemd/voorbeeld-taak.service` | gevalideerd |
| SCR-41 | `03-systemd/voorbeeld-taak.timer` | gevalideerd |
| SCR-42 | `03-systemd/meld-fout@.service` | gevalideerd, dekt gedeeltelijk |
| SCR-42 | `03-systemd/voorbeeld.service` | gevalideerd |
| SCR-42 | `04-scripts/lus.sh` | gevalideerd, dekt gedeeltelijk |
| SCR-43 | `04-scripts/lus.sh` | gevalideerd |
| SCR-45 | `04-scripts/bulk.sh` | gevalideerd |
| SCR-45 | `04-scripts/skelet.py` | gevalideerd |
| SCR-46 | `04-scripts/bulk.sh` | gevalideerd |
| SCR-46 | `04-scripts/skelet.py` | gevalideerd |
| SCR-47 | `04-scripts/bulk.sh` | gevalideerd |
| SCR-47 | `04-scripts/skelet.py` | gevalideerd |
| WEB-09 | `01-nginx/controleer-headers.sh` | gevalideerd |
| WEB-09 | `01-nginx/snippets/security-headers.conf` | gevalideerd, dekt gedeeltelijk |
| WEB-11 | `01-nginx/snippets/security-headers.conf` | gevalideerd, dekt gedeeltelijk |
| WEB-11 | `08-api/src/csp-nonce.ts` | gevalideerd |
| WEB-12 | `08-api/src/csp-nonce.ts` | gevalideerd |
| WEB-13 | `08-api/src/csp-nonce.ts` | gevalideerd |
| WEB-14 | `08-api/src/csp-nonce.ts` | gevalideerd, dekt gedeeltelijk |
| WEB-15 | `08-api/src/csp-nonce.ts` | gevalideerd |
| WEB-17 | `01-nginx/controleer-headers.sh` | gevalideerd |
| WEB-17 | `01-nginx/snippets/security-headers.conf` | gevalideerd |
| WEB-19 | `01-nginx/controleer-headers.sh` | gevalideerd |
| WEB-19 | `01-nginx/snippets/security-headers.conf` | gevalideerd |
| WEB-20 | `01-nginx/snippets/security-headers.conf` | gevalideerd |
| WEB-21 | `01-nginx/snippets/security-headers.conf` | gevalideerd, dekt gedeeltelijk |
| WEB-22 | `01-nginx/conf.d/00-dicht-http.conf` | gevalideerd |
| WEB-22 | `01-nginx/controleer-headers.sh` | gevalideerd |
| WEB-22 | `01-nginx/snippets/proxy-headers.conf` | gevalideerd, dekt gedeeltelijk |
| WEB-23 | `01-nginx/conf.d/00-dicht-http.conf` | gevalideerd |
| WEB-23 | `01-nginx/controleer-headers.sh` | gevalideerd |
| WEB-23 | `01-nginx/snippets/security-headers.conf` | gevalideerd |
| WEB-24 | `01-nginx/controleer-headers.sh` | gevalideerd |
| WEB-24 | `01-nginx/snippets/security-headers.conf` | gevalideerd |
| WEB-24 | `08-api/src/csp-nonce.ts` | gevalideerd |
| WEB-29 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WEB-29 | `11-berichten/afmelden-routes.ts` | gevalideerd |
| WEB-51 | `01-nginx/conf.d/site-voorbeeld.conf` | gevalideerd |
| WEB-51 | `01-nginx/snippets/proxy-headers.conf` | gevalideerd |
| WEB-51 | `08-api/src/server.ts` | gevalideerd |
| WEB-56 | `01-nginx/conf.d/site-voorbeeld.conf` | gevalideerd |
| WEB-62 | `01-nginx/50x.html` | gevalideerd |
| WEB-62 | `08-api/src/server.ts` | gevalideerd |
| WEB-64 | `01-nginx/snippets/blokkades.conf` | gevalideerd |
| WEB-64 | `09-wordpress/controleer-blokkades.sh` | gevalideerd |
| WEB-64 | `09-wordpress/htaccess-versterking` | gevalideerd, dekt gedeeltelijk |
| WEB-66 | `01-nginx/conf.d/00-dicht-http.conf` | gevalideerd |
| WEB-66 | `01-nginx/conf.d/site-voorbeeld.conf` | gevalideerd |
| WEB-72 | `01-nginx/snippets/testomgeving.conf` | gevalideerd |
| WEB-72 | `09-wordpress/mu-plugins/dicht-testomgeving-afschermen.php` | gevalideerd, dekt gedeeltelijk |
| WP-01 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-02 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-05 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-06 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-08 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-08 | `09-wordpress/dicht-voorbeeld/uninstall.php` | gevalideerd |
| WP-08 | `09-wordpress/mu-plugins/dicht-testomgeving-afschermen.php` | gevalideerd |
| WP-09 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-10 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd, dekt gedeeltelijk |
| WP-11 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-13 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-16 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-17 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-18 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-21 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-21 | `09-wordpress/dicht-voorbeeld/uninstall.php` | gevalideerd |
| WP-24 | `09-wordpress/controleer-blokkades.sh` | gevalideerd |
| WP-24 | `09-wordpress/htaccess-versterking` | gevalideerd |
| WP-27 | `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd |
| WP-33 | `09-wordpress/wp-config-versterking.php` | gevalideerd |
| WP-34 | `09-wordpress/mu-plugins/dicht-testomgeving-afschermen.php` | gevalideerd |
| WP-38 | `09-wordpress/wp-config-versterking.php` | gevalideerd, dekt gedeeltelijk |
| WP-39 | `09-wordpress/wp-config-versterking.php` | gevalideerd |
| WP-40 | `09-wordpress/wp-config-versterking.php` | gevalideerd |
| WP-41 | `09-wordpress/controleer-blokkades.sh` | gevalideerd |
| WP-41 | `09-wordpress/htaccess-versterking` | gevalideerd |
| WP-43 | `09-wordpress/wp-config-versterking.php` | gevalideerd |
| WP-46 | `09-wordpress/wp-config-versterking.php` | gevalideerd |
| WP-47 | `09-wordpress/wp-config-versterking.php` | gevalideerd |
| WP-55 | `09-wordpress/controleer-blokkades.sh` | gevalideerd |
| WP-55 | `09-wordpress/htaccess-versterking` | gevalideerd |
| WP-61 | `09-wordpress/mu-plugins/dicht-testomgeving-afschermen.php` | gevalideerd, dekt gedeeltelijk |
| WP-62 | `09-wordpress/controleer-blokkades.sh` | gevalideerd |
| WP-63 | `01-nginx/snippets/blokkades.conf` | gevalideerd, dekt gedeeltelijk |
| WP-63 | `09-wordpress/controleer-blokkades.sh` | gevalideerd |
| WP-63 | `09-wordpress/htaccess-versterking` | gevalideerd |
| WP-64 | `09-wordpress/controleer-blokkades.sh` | gevalideerd |
| WP-64 | `09-wordpress/htaccess-versterking` | gevalideerd |
| WP-65 | `09-wordpress/htaccess-versterking` | gevalideerd |

## Per bestand

| Sjabloon | Status | Hoe gecontroleerd, of waarom niet | Regels |
|---|---|---|---|
| `01-nginx/50x.html` | gevalideerd | HTML ontleed met de Python-parser | 2 |
| `01-nginx/conf.d/00-dicht-http.conf` | gevalideerd | nginx -t geslaagd en gedraaid in een wegwerpcontainer zonder netwerk (nginx 1.29.8, zelfondertekend certificaat, nep-upstream): zeven vaste headers op elke respons ook bij 404 en 502, 301 met vaste host, 403 op /api via poort 80, onbekende host geweigerd op 80 en 443, blokkades 404, limieten geven 429, 413 boven 1 MB, interne koppen leeg, eigen 50x-pagina, testomgeving 401 zonder wachtwoord | 8 |
| `01-nginx/conf.d/01-default-server.conf` | gevalideerd | nginx -t geslaagd en gedraaid in een wegwerpcontainer zonder netwerk (nginx 1.29.8, zelfondertekend certificaat, nep-upstream): zeven vaste headers op elke respons ook bij 404 en 502, 301 met vaste host, 403 op /api via poort 80, onbekende host geweigerd op 80 en 443, blokkades 404, limieten geven 429, 413 boven 1 MB, interne koppen leeg, eigen 50x-pagina, testomgeving 401 zonder wachtwoord | 1 |
| `01-nginx/conf.d/site-voorbeeld.conf` | gevalideerd | nginx -t geslaagd en gedraaid in een wegwerpcontainer zonder netwerk (nginx 1.29.8, zelfondertekend certificaat, nep-upstream): zeven vaste headers op elke respons ook bij 404 en 502, 301 met vaste host, 403 op /api via poort 80, onbekende host geweigerd op 80 en 443, blokkades 404, limieten geven 429, 413 boven 1 MB, interne koppen leeg, eigen 50x-pagina, testomgeving 401 zonder wachtwoord | 9 |
| `01-nginx/controleer-headers.sh` | gevalideerd | bash -n; shellcheck 0.11.0 zonder bevinding | 7 |
| `01-nginx/nginx-test.conf` | gevalideerd | nginx -t geslaagd in een wegwerpcontainer (nginx 1.29.8), zoals geleverd en met site-voorbeeld.conf erbij | 1 |
| `01-nginx/snippets/blokkades.conf` | gevalideerd | nginx -t geslaagd en gedraaid in een wegwerpcontainer zonder netwerk (nginx 1.29.8, zelfondertekend certificaat, nep-upstream): zeven vaste headers op elke respons ook bij 404 en 502, 301 met vaste host, 403 op /api via poort 80, onbekende host geweigerd op 80 en 443, blokkades 404, limieten geven 429, 413 boven 1 MB, interne koppen leeg, eigen 50x-pagina, testomgeving 401 zonder wachtwoord | 2 |
| `01-nginx/snippets/proxy-headers.conf` | gevalideerd | nginx -t geslaagd en gedraaid in een wegwerpcontainer zonder netwerk (nginx 1.29.8, zelfondertekend certificaat, nep-upstream): zeven vaste headers op elke respons ook bij 404 en 502, 301 met vaste host, 403 op /api via poort 80, onbekende host geweigerd op 80 en 443, blokkades 404, limieten geven 429, 413 boven 1 MB, interne koppen leeg, eigen 50x-pagina, testomgeving 401 zonder wachtwoord | 3 |
| `01-nginx/snippets/security-headers.conf` | gevalideerd | nginx -t geslaagd en gedraaid in een wegwerpcontainer zonder netwerk (nginx 1.29.8, zelfondertekend certificaat, nep-upstream): zeven vaste headers op elke respons ook bij 404 en 502, 301 met vaste host, 403 op /api via poort 80, onbekende host geweigerd op 80 en 443, blokkades 404, limieten geven 429, 413 boven 1 MB, interne koppen leeg, eigen 50x-pagina, testomgeving 401 zonder wachtwoord | 8 |
| `01-nginx/snippets/testomgeving.conf` | gevalideerd | nginx -t geslaagd en gedraaid in een wegwerpcontainer zonder netwerk (nginx 1.29.8, zelfondertekend certificaat, nep-upstream): zeven vaste headers op elke respons ook bij 404 en 502, 301 met vaste host, 403 op /api via poort 80, onbekende host geweigerd op 80 en 443, blokkades 404, limieten geven 429, 413 boven 1 MB, interne koppen leeg, eigen 50x-pagina, testomgeving 401 zonder wachtwoord | 1 |
| `02-docker/.dockerignore` | gevalideerd | docker build --check zonder waarschuwing op een ingevulde kopie en echt gebouwd met een proefproject (node:24-slim): uid 10001, /app niet schrijfbaar, alleen productie-afhankelijkheden, de bouwcontext zonder .env, .git, sleutels, dumps en tests. hadolint niet gedraaid | 3 |
| `02-docker/Dockerfile` | gevalideerd | docker build --check zonder waarschuwing op een ingevulde kopie en echt gebouwd met een proefproject (node:24-slim): uid 10001, /app niet schrijfbaar, alleen productie-afhankelijkheden, de bouwcontext zonder .env, .git, sleutels, dumps en tests. hadolint niet gedraaid | 15 |
| `02-docker/compose.yml` | gevalideerd | docker compose config geslaagd op een ingevulde kopie (Compose v5.1.4); de db-dienst los gestart als wegwerpcontainer met dezelfde capabilities en het volumepad (postgres:18.6). Hersteld: het volumepad voor PostgreSQL 18. Het geheel is niet met compose gestart | 17 |
| `02-docker/daemon.json` | gevalideerd | JSON geladen | 1 |
| `03-systemd/crontab-voorbeeld` | gevalideerd | geinstalleerd en gestart door cron in een wegwerpcontainer (Debian cron 3.0pl1-162); vier gevallen gedraaid: geslaagd, fout, time-out, slot bezet | 6 |
| `03-systemd/meld-fout.sh` | gevalideerd | bash -n; shellcheck 0.11.0 zonder bevinding | 7 |
| `03-systemd/meld-fout@.service` | gevalideerd | systemd-analyze verify (systemd 249) op een kopie: geen syntaxfout of onbekende sleutel; alleen de melding dat de voorbeeldpaden niet bestaan. De score van systemd-analyze security is niet gemeten | 3 |
| `03-systemd/voorbeeld-taak.service` | gevalideerd | systemd-analyze verify (systemd 249) op een kopie: geen syntaxfout of onbekende sleutel; alleen de melding dat de voorbeeldpaden niet bestaan. De score van systemd-analyze security is niet gemeten | 9 |
| `03-systemd/voorbeeld-taak.timer` | gevalideerd | systemd-analyze verify (systemd 249) op een kopie: geen syntaxfout of onbekende sleutel; alleen de melding dat de voorbeeldpaden niet bestaan. De score van systemd-analyze security is niet gemeten | 3 |
| `03-systemd/voorbeeld.service` | gevalideerd | systemd-analyze verify (systemd 249) op een kopie: geen syntaxfout of onbekende sleutel; alleen de melding dat de voorbeeldpaden niet bestaan. De score van systemd-analyze security is niet gemeten | 11 |
| `04-scripts/bulk.sh` | gevalideerd | bash -n en uitgevoerd in de scratchmap: negen gevallen (noodstop, plafond, lege selectie, verkeerd aantal, pauze, slecht id); shellcheck 0.11.0 zonder bevinding | 14 |
| `04-scripts/gate-scripts.sh` | gevalideerd | bash -n; shellcheck 0.11.0 zonder bevinding | 3 |
| `04-scripts/lus.sh` | gevalideerd | bash -n; shellcheck 0.11.0 zonder bevinding | 4 |
| `04-scripts/skelet.py` | gevalideerd | py_compile en uitgevoerd in de scratchmap (proefstand, plafond, noodstop, verkeerd aantal) | 16 |
| `04-scripts/taak.sh` | gevalideerd | bash -n; shellcheck 0.11.0 zonder bevinding | 18 |
| `05-git-ci/.githooks/pre-push` | gevalideerd | sh -n; shellcheck 0.11.0 zonder bevinding | 1 |
| `05-git-ci/.github/dependabot.yml` | gevalideerd | YAML geladen; niet met zizmor of GitHub zelf | 5 |
| `05-git-ci/.github/workflows/gate.yml` | gevalideerd | actionlint 1.7.12 zonder bevinding (wegwerpcontainer); de twee commit-SHA's nagevraagd met git ls-remote en de GitHub-API. Niet met zizmor of op GitHub gedraaid | 14 |
| `05-git-ci/.gitignore` | gevalideerd | git check-ignore in een lege proefrepo | 3 |
| `05-git-ci/.npmrc` | gevalideerd | gemeten met npm 11.19.0 (node:24-slim, wegwerpcontainer): met min-release-age=7 kiest npm de nieuwste versie van minstens 7 dagen oud, zonder de regel de allernieuwste; ignore-scripts slaat de installatie- en pre-scripts over. Op de server (npm 10.9.8) doet min-release-age niets | 2 |
| `05-git-ci/.pre-commit-config.yaml` | gevalideerd | YAML geladen; het hulpmiddel zelf staat niet op de server | 1 |
| `05-git-ci/CODEOWNERS` | niet gevalideerd | tekstsjabloon: er bestaat geen commando dat de juistheid aantoont zonder het in een echte repository of op een echte site te plaatsen | 1 |
| `05-git-ci/SECURITY.md` | niet gevalideerd | tekstsjabloon: er bestaat geen commando dat de juistheid aantoont zonder het in een echte repository of op een echte site te plaatsen | 3 |
| `05-git-ci/lefthook.yml` | gevalideerd | YAML geladen; het hulpmiddel zelf staat niet op de server | 2 |
| `05-git-ci/package-scripts.json` | gevalideerd | JSON geladen | 3 |
| `05-git-ci/ruleset-main.json` | gevalideerd | geldig tegen het schema van POST /repos/{owner}/{repo}/rulesets uit de OpenAPI-beschrijving van GitHub (versie 1.1.4), ook met onbekende sleutels verboden. Niet ingestuurd naar een repository | 3 |
| `05-git-ci/ruleset-tags.json` | gevalideerd | geldig tegen het schema van POST /repos/{owner}/{repo}/rulesets uit de OpenAPI-beschrijving van GitHub (versie 1.1.4), ook met onbekende sleutels verboden. Niet ingestuurd naar een repository | 3 |
| `05-git-ci/scripts/scan.sh` | gevalideerd | bash -n; shellcheck 0.11.0 zonder bevinding; de scanners zelf staan niet op de server | 7 |
| `05-git-ci/security.txt` | niet gevalideerd | tekstsjabloon: er bestaat geen commando dat de juistheid aantoont zonder het in een echte repository of op een echte site te plaatsen | 2 |
| `06-database/backup.sh` | gevalideerd | bash -n; shellcheck 0.11.0 zonder bevinding; controleer-backup.sh ook uitgevoerd in de scratchmap. backup.sh en herstelproef.sh niet tegen Docker of een server | 10 |
| `06-database/controleer-backup.sh` | gevalideerd | bash -n; shellcheck 0.11.0 zonder bevinding; controleer-backup.sh ook uitgevoerd in de scratchmap. backup.sh en herstelproef.sh niet tegen Docker of een server | 3 |
| `06-database/herstelproef.sh` | gevalideerd | bash -n; shellcheck 0.11.0 zonder bevinding; controleer-backup.sh ook uitgevoerd in de scratchmap. backup.sh en herstelproef.sh niet tegen Docker of een server | 7 |
| `06-database/migraties/0001_tenant_tabel_met_rls.sql` | gevalideerd | gedraaid tegen een wegwerp-PostgreSQL 18.6 met de rollen uit rollen.sql; de tenantgrens getest met de app-rol (zonder context, andere tenant, hergebruikte verbinding, eigenaar). Hersteld: de rechten van de app-rol eerst intrekken | 10 |
| `06-database/migraties/0002_expand.sql` | gevalideerd | gedraaid tegen een wegwerp-PostgreSQL 18.6, in volgorde 0002 tot en met 0005 met de backfill ertussen (2500 rijen); niet op een kopie van productie | 6 |
| `06-database/migraties/0003_expand_index.sql` | gevalideerd | gedraaid tegen een wegwerp-PostgreSQL 18.6, in volgorde 0002 tot en met 0005 met de backfill ertussen (2500 rijen); niet op een kopie van productie | 1 |
| `06-database/migraties/0004_valideer.sql` | gevalideerd | gedraaid tegen een wegwerp-PostgreSQL 18.6, in volgorde 0002 tot en met 0005 met de backfill ertussen (2500 rijen); niet op een kopie van productie | 3 |
| `06-database/migraties/0005_contract.sql` | gevalideerd | gedraaid tegen een wegwerp-PostgreSQL 18.6, in volgorde 0002 tot en met 0005 met de backfill ertussen (2500 rijen); niet op een kopie van productie | 3 |
| `06-database/migraties/backfill.sh` | gevalideerd | bash -n en gedraaid tegen een wegwerp-PostgreSQL 18.6: 2500 rijen in vier batches, tweede run 0 rijen; shellcheck 0.11.0 zonder bevinding | 3 |
| `06-database/rollen.sql` | gevalideerd | gedraaid tegen een wegwerp-PostgreSQL 18.6 (postgres:18, zonder netwerk); de vier controles uit de kop geven de genoemde uitkomst | 14 |
| `06-database/tenant-context.ts` | gevalideerd | tsc --noEmit (TypeScript 6.0.3, strikte tsconfig uit 07) en eslint (typescript-eslint 8.71.0) groen in een wegwerpcontainer; niet tegen een database gedraaid | 5 |
| `07-typescript-tests/e2e/opzet.ts` | gevalideerd | typecontrole met tsc 6.0.3; playwright test --list (1.63.0) toont acht tests in twee projecten. Niet in een browser gedraaid | 1 |
| `07-typescript-tests/e2e/voorbeeld.spec.ts` | gevalideerd | typecontrole met tsc 6.0.3; playwright test --list (1.63.0) toont acht tests in twee projecten. Niet in een browser gedraaid | 6 |
| `07-typescript-tests/eslint.config.mjs` | gevalideerd | eslint 10.12.0 met typescript-eslint 8.71.0: het API-skelet is groen, een proef met een diepe import, any en een losse promise is rood. De e2e-regels niet gedraaid | 7 |
| `07-typescript-tests/playwright.config.ts` | gevalideerd | typecontrole met tsc 6.0.3; playwright test --list (1.63.0) toont acht tests in twee projecten. Niet in een browser gedraaid | 4 |
| `07-typescript-tests/stryker.config.json` | gevalideerd | JSON geladen; niet met StrykerJS | 1 |
| `07-typescript-tests/tests/grenzen.test.ts` | gevalideerd | typecontrole met tsc 6.0.3; vitest list (5.0.3) laadt de configuratie en toont de tests. De tests zelf niet gedraaid (ze vragen het eigen project) | 11 |
| `07-typescript-tests/tests/opzet.ts` | gevalideerd | typecontrole met tsc 6.0.3; vitest list (5.0.3) laadt de configuratie en toont de tests. De tests zelf niet gedraaid (ze vragen het eigen project) | 1 |
| `07-typescript-tests/tests/tenant-isolatie.test.ts` | gevalideerd | typecontrole met tsc 6.0.3; vitest list (5.0.3) laadt de configuratie en toont de tests. De tests zelf niet gedraaid (ze vragen het eigen project) | 6 |
| `07-typescript-tests/tsconfig.json` | gevalideerd | tsc 6.0.3: --showConfig toont de zes opties, het API-skelet compileert ermee en een proef met een typefout wordt gevonden | 1 |
| `07-typescript-tests/vitest.config.ts` | gevalideerd | typecontrole met tsc 6.0.3; vitest list (5.0.3) laadt de configuratie en toont de tests. De tests zelf niet gedraaid (ze vragen het eigen project) | 3 |
| `08-api/migraties/idempotentie.sql` | gevalideerd | gedraaid tegen een wegwerp-PostgreSQL 18.6; dubbele sleutel, dubbele taak en onbekende status geweigerd. Hersteld: de app-rol hield DELETE op taken via de standaardrechten | 6 |
| `08-api/src/csp-nonce.ts` | gevalideerd | tsc --noEmit (TypeScript 6.0.3, strikte tsconfig uit 07) en eslint --max-warnings 0 (typescript-eslint 8.71.0) groen in een wegwerpcontainer. Hersteld: vier lintfouten (zod 4, enum van Mollie, ongebruikte parameter). Niet gedraaid als dienst | 6 |
| `08-api/src/db.ts` | gevalideerd | tsc --noEmit (TypeScript 6.0.3, strikte tsconfig uit 07) en eslint --max-warnings 0 (typescript-eslint 8.71.0) groen in een wegwerpcontainer. Hersteld: vier lintfouten (zod 4, enum van Mollie, ongebruikte parameter). Niet gedraaid als dienst | 3 |
| `08-api/src/env.ts` | gevalideerd | tsc --noEmit (TypeScript 6.0.3, strikte tsconfig uit 07) en eslint --max-warnings 0 (typescript-eslint 8.71.0) groen in een wegwerpcontainer. Hersteld: vier lintfouten (zod 4, enum van Mollie, ongebruikte parameter). Niet gedraaid als dienst | 4 |
| `08-api/src/fouten.ts` | gevalideerd | tsc --noEmit (TypeScript 6.0.3, strikte tsconfig uit 07) en eslint --max-warnings 0 (typescript-eslint 8.71.0) groen in een wegwerpcontainer. Hersteld: vier lintfouten (zod 4, enum van Mollie, ongebruikte parameter). Niet gedraaid als dienst | 2 |
| `08-api/src/routes/bestellen.ts` | gevalideerd | tsc --noEmit (TypeScript 6.0.3, strikte tsconfig uit 07) en eslint --max-warnings 0 (typescript-eslint 8.71.0) groen in een wegwerpcontainer. Hersteld: vier lintfouten (zod 4, enum van Mollie, ongebruikte parameter). Niet gedraaid als dienst | 11 |
| `08-api/src/routes/mollie-webhook.ts` | gevalideerd | tsc --noEmit (TypeScript 6.0.3, strikte tsconfig uit 07) en eslint --max-warnings 0 (typescript-eslint 8.71.0) groen in een wegwerpcontainer. Hersteld: vier lintfouten (zod 4, enum van Mollie, ongebruikte parameter). Niet gedraaid als dienst | 13 |
| `08-api/src/server.ts` | gevalideerd | tsc --noEmit (TypeScript 6.0.3, strikte tsconfig uit 07) en eslint --max-warnings 0 (typescript-eslint 8.71.0) groen in een wegwerpcontainer. Hersteld: vier lintfouten (zod 4, enum van Mollie, ongebruikte parameter). Niet gedraaid als dienst | 19 |
| `09-wordpress/controleer-blokkades.sh` | gevalideerd | bash -n; shellcheck 0.11.0 zonder bevinding | 9 |
| `09-wordpress/htaccess-versterking` | gevalideerd | gedraaid op Apache 2.4.68 in een wegwerp-WordPress (7.1.2): 22 geblokkeerde paden geven 403, zes gewone paden 200. Niet op LiteSpeed gedraaid; de meting op de productieserver blijft nodig (WP-64) | 9 |
| `09-wordpress/dicht-voorbeeld/dicht-voorbeeld.php` | gevalideerd | php -l (PHP 8.3.35) en gedraaid in een wegwerp-WordPress 7.1.2 met MariaDB 10.11: activeren, nonce, capability, REST, escapen, zoeken en verwijderen via HTTP en wp-cli. PHPCS, Plugin Check en PHPStan niet gedraaid | 17 |
| `09-wordpress/dicht-voorbeeld/uninstall.php` | gevalideerd | php -l (PHP 8.3.35) en gedraaid in een wegwerp-WordPress 7.1.2 met MariaDB 10.11: activeren, nonce, capability, REST, escapen, zoeken en verwijderen via HTTP en wp-cli. PHPCS, Plugin Check en PHPStan niet gedraaid | 2 |
| `09-wordpress/mu-plugins/dicht-testomgeving-afschermen.php` | gevalideerd | php -l (PHP 8.3.35) en gedraaid in een wegwerp-WordPress 7.1.2: 302 naar de inlogpagina met X-Robots-Tag, REST anoniem 401, XML-RPC uit; zonder de constante doet het niets | 5 |
| `09-wordpress/wp-config-versterking.php` | gevalideerd | php -l (PHP 8.3.35) en de regels overgenomen in de wp-config.php van een wegwerp-WordPress: wp config get toont de waarden, wp-admin gaat naar https, de editor is uit | 7 |
| `10-bewijs-beheer/bewijsbestand.md` | gevalideerd | vorm gecontroleerd met controleer-bewijs.py | 6 |
| `10-bewijs-beheer/controleer-bewijs.py` | gevalideerd | py_compile en uitgevoerd op het sjabloon en op een ingevuld proefbestand | 4 |
| `10-bewijs-beheer/projectintake.md` | niet gevalideerd | tekstsjabloon: er bestaat geen commando dat de juistheid aantoont; de inhoud vraagt een lezer | 10 |
| `10-bewijs-beheer/threat-model.md` | niet gevalideerd | tekstsjabloon: er bestaat geen commando dat de juistheid aantoont; de inhoud vraagt een lezer | 3 |
| `10-bewijs-beheer/uitzonderingen.md` | gevalideerd | vorm gecontroleerd met controleer-bewijs.py | 3 |
| `11-berichten/afmelden-routes.ts` | gevalideerd | tsc --noEmit (strikt, TypeScript 6.0.3) groen; niet met een draaiende Fastify | 6 |
| `11-berichten/afmelden.test.ts` | gevalideerd | uitgevoerd met node --test (Node 24.21.0): 8 tests geslaagd; tsc --noEmit (strikt) groen | 2 |
| `11-berichten/afmelden.ts` | gevalideerd | uitgevoerd met node --test (Node 24.21.0): 8 tests geslaagd; tsc --noEmit (strikt) groen | 3 |
| `11-berichten/dns-records.zone` | gevalideerd | named-checkzone (BIND 9, wegwerpcontainer) laadt de ingevulde records met een sleutel van 2048 bit. Hersteld: de DKIM-waarde in twee delen. Niet gepubliceerd of opgevraagd | 7 |
| `11-berichten/webhook-verificatie.test.ts` | gevalideerd | uitgevoerd met node --test (Node 24.21.0): 8 tests geslaagd; tsc --noEmit (strikt) groen | 4 |
| `11-berichten/webhook-verificatie.ts` | gevalideerd | uitgevoerd met node --test (Node 24.21.0): 8 tests geslaagd; tsc --noEmit (strikt) groen | 6 |
