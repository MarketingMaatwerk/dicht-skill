# syntax=docker/dockerfile:1
# check=error=true
#
# Sjabloon: gehard Dockerfile voor een Node-dienst (meerfasen, niet als root, digest vastgezet).
# Dekt: INFRA-27, INFRA-37, GIT-91, GIT-93, GIT-94, GIT-95, GIT-96, GIT-66 (alleen de check-regel),
#       GIT-69, GIT-71, GIT-80, API-72, API-74, ARCH-09, ARCH-05
# Aanpassen:
#   - <versie> en <digest> in beide FROM-regels. De regels noemen geen digest; haal hem zelf op:
#       docker buildx imagetools inspect node:<versie>-slim      (GIT-91)
#     Kies een Node-versie in actieve of onderhouds-LTS (GIT-93: stand 04-10-2026 Node 22 onderhoud tot
#     30-04-2027, Node 24 actief LTS tot 30-04-2028) en zet dezelfde versie in "engines" (API-72).
#   - de bouwopdracht, de map met het resultaat (dist/) en het startbestand.
# Geheim tijdens de build (GIT-95): alleen via RUN --mount=type=secret, nooit ARG, ENV of COPY:
#   RUN --mount=type=secret,id=npm_token,env=NPM_TOKEN npm ci
# Niets ophalen zonder controlesom (GIT-96): geen "curl ... | sh", en ADD <url> alleen met --checksum=sha256:<hash>.
# Controleren:
#   docker build --check .                         (GIT-66; "check=error=true" hierboven laat de build falen)
#   hadolint Dockerfile                            (GIT-66)
#   docker run --rm <image> id -u                  toont 10001 (INFRA-27)
#   docker history --no-trunc <image> | grep -iE 'token|secret|password'   is leeg (GIT-95)
#   docker image inspect <image> --format '{{.Config.User}}'               toont 10001
# Gevalideerd op 04-10-2026 in wegwerpcontainers: docker build --check zonder waarschuwing op een ingevulde
#   kopie (node:24-slim), en echt gebouwd met een proefproject: id -u geeft 10001, /app is niet schrijfbaar,
#   node_modules bevat alleen de productie-afhankelijkheid. Zoals geleverd faalt de build bewust op <versie>.
#   hadolint is niet gedraaid.

# Fase 1: bouwen, met dev-afhankelijkheden. Niets uit deze fase komt in het eindimage behalve dist/.
FROM node:<versie>-slim@sha256:<digest> AS bouw
WORKDIR /app
# Het lockfile eerst, voor de cache; installeren alleen met npm ci (GIT-69).
# .npmrc met ignore-scripts=true hoort in de repo (GIT-71, sjabloon in 05-git-ci/.npmrc).
COPY package.json package-lock.json .npmrc ./
RUN npm ci
COPY . .
RUN npm run build

# Fase 2: alleen productie-afhankelijkheden (GIT-80).
FROM node:<versie>-slim@sha256:<digest> AS prod-deps
WORKDIR /app
COPY package.json package-lock.json .npmrc ./
# mkdir: zonder productie-afhankelijkheden maakt npm ci geen node_modules en faalt de COPY in fase 3 (gemeten).
RUN npm ci --omit=dev && mkdir -p node_modules

# Fase 3: het eindimage. Geen compiler, geen tests, geen .git, geen dev-pakketten (INFRA-37, ARCH-05).
FROM node:<versie>-slim@sha256:<digest>
ENV NODE_ENV=production
WORKDIR /app
# Vast, niet-nul UID; de bestanden van de applicatie zijn van root en dus niet schrijfbaar voor het proces (INFRA-27).
RUN groupadd --gid 10001 app && useradd --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app
COPY --chown=root:root --from=prod-deps /app/node_modules ./node_modules
COPY --chown=root:root --from=bouw /app/dist ./dist
COPY --chown=root:root package.json ./
# Release-id in de build (ARCH-09): geef mee met --build-arg RELEASE=$(git rev-parse --short HEAD).
# Een release-id is geen geheim; een geheim hoort nooit in ARG (GIT-95).
ARG RELEASE
ENV RELEASE=${RELEASE}
USER 10001
# Geen --inspect, geen watch-modus, geen experimentele vlaggen (API-74). Exec-vorm, zodat SIGTERM bij node aankomt (ARCH-17).
CMD ["node", "dist/server.js"]
