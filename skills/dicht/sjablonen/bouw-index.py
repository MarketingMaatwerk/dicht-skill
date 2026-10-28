#!/usr/bin/env python3
"""Bouwt INDEX.md uit de koppen van de sjablonen en controleert elk regel-ID.

Gebruik: python3 bouw-index.py            schrijft INDEX.md, exitcode 1 bij een onbekend ID of een bestand zonder status
Leest: de regel "Dekt:" en het blok "Dekt gedeeltelijk:" bovenaan elk sjabloon (bij een JSON-bestand uit het
  LEESMIJ-bestand ernaast), skill/regel-index.tsv en de vier batch-4-bestanden in research/.
Een ID telt als "dekt gedeeltelijk" als het in de regel "Dekt:" een toelichting tussen haakjes heeft, als het in
  "Dekt:" staat en ook aan het begin van een punt in het blok "Dekt gedeeltelijk:", of als het op de regel
  "Dekt gedeeltelijk:" zelf staat. Een ID dat alleen in dat blok wordt genoemd ("staat hier niet") telt niet als
  gedekt en komt niet in de index.
De status per bestand (gevalideerd of niet, en hoe) staat hieronder in STATUS en is met de hand bijgehouden:
  hij beschrijft wat op 04-10-2026 echt is gedraaid, op de server zelf of in een wegwerpcontainer op de server.
"""
import fnmatch
import pathlib
import re
import subprocess
import sys

HIER = pathlib.Path(__file__).resolve().parent
ROOT = HIER.parents[1]
BATCH4 = ["scripts-automatisering.md", "invoer-bestandsformaten.md", "bedrijfslogica-gelijktijdigheid.md",
          "email-berichten-bots.md"]
ID = re.compile(r"\b(?:WEB|AUTH|API|DB|INFRA|GIT|WP|AI|PRIV|ARCH|SCR|INV|BIZ|MSG)-\d+\b")
LABEL = re.compile(r"^[A-Z][A-Za-z ()]*:")
G, N = "gevalideerd", "niet gevalideerd"

# patroon -> (status, hoe of waarom niet). De eerste treffer telt.
STATUS = [
    ("01-nginx/controleer-headers.sh", (G, "bash -n; shellcheck 0.11.0 zonder bevinding")),
    ("01-nginx/50x.html", (G, "HTML ontleed met de Python-parser")),
    ("01-nginx/nginx-test.conf", (G, "nginx -t geslaagd in een wegwerpcontainer (nginx 1.29.8), zoals geleverd en met site-voorbeeld.conf erbij")),
    ("01-nginx/*", (G, "nginx -t geslaagd en gedraaid in een wegwerpcontainer zonder netwerk (nginx 1.29.8, zelfondertekend certificaat, nep-upstream): zeven vaste headers op elke respons ook bij 404 en 502, 301 met vaste host, 403 op /api via poort 80, onbekende host geweigerd op 80 en 443, blokkades 404, limieten geven 429, 413 boven 1 MB, interne koppen leeg, eigen 50x-pagina, testomgeving 401 zonder wachtwoord")),
    ("02-docker/compose.yml", (G, "docker compose config geslaagd op een ingevulde kopie (Compose v5.1.4); de db-dienst los gestart als wegwerpcontainer met dezelfde capabilities en het volumepad (postgres:18.6). Hersteld: het volumepad voor PostgreSQL 18. Het geheel is niet met compose gestart")),
    ("02-docker/daemon.json", (G, "JSON geladen")),
    ("02-docker/*", (G, "docker build --check zonder waarschuwing op een ingevulde kopie en echt gebouwd met een proefproject (node:24-slim): uid 10001, /app niet schrijfbaar, alleen productie-afhankelijkheden, de bouwcontext zonder .env, .git, sleutels, dumps en tests. hadolint niet gedraaid")),
    ("03-systemd/crontab-voorbeeld", (G, "geinstalleerd en gestart door cron in een wegwerpcontainer (Debian cron 3.0pl1-162); vier gevallen gedraaid: geslaagd, fout, time-out, slot bezet")),
    ("03-systemd/meld-fout.sh", (G, "bash -n; shellcheck 0.11.0 zonder bevinding")),
    ("03-systemd/*", (G, "systemd-analyze verify (systemd 249) op een kopie: geen syntaxfout of onbekende sleutel; alleen de melding dat de voorbeeldpaden niet bestaan. De score van systemd-analyze security is niet gemeten")),
    ("04-scripts/bulk.sh", (G, "bash -n en uitgevoerd in de scratchmap: negen gevallen (noodstop, plafond, lege selectie, verkeerd aantal, pauze, slecht id); shellcheck 0.11.0 zonder bevinding")),
    ("04-scripts/skelet.py", (G, "py_compile en uitgevoerd in de scratchmap (proefstand, plafond, noodstop, verkeerd aantal)")),
    ("04-scripts/*.sh", (G, "bash -n; shellcheck 0.11.0 zonder bevinding")),
    ("05-git-ci/.gitignore", (G, "git check-ignore in een lege proefrepo")),
    ("05-git-ci/.npmrc", (G, "gemeten met npm 11.19.0 (node:24-slim, wegwerpcontainer): met min-release-age=7 kiest npm de nieuwste versie van minstens 7 dagen oud, zonder de regel de allernieuwste; ignore-scripts slaat de installatie- en pre-scripts over. Op de server (npm 10.9.8) doet min-release-age niets")),
    ("05-git-ci/ruleset-*.json", (G, "geldig tegen het schema van POST /repos/{owner}/{repo}/rulesets uit de OpenAPI-beschrijving van GitHub (versie 1.1.4), ook met onbekende sleutels verboden. Niet ingestuurd naar een repository")),
    ("05-git-ci/*.json", (G, "JSON geladen")),
    ("05-git-ci/.github/workflows/*", (G, "actionlint 1.7.12 zonder bevinding (wegwerpcontainer); de twee commit-SHA's nagevraagd met git ls-remote en de GitHub-API. Niet met zizmor of op GitHub gedraaid")),
    ("05-git-ci/.github/*", (G, "YAML geladen; niet met zizmor of GitHub zelf")),
    ("05-git-ci/*.y*ml", (G, "YAML geladen; het hulpmiddel zelf staat niet op de server")),
    ("05-git-ci/scripts/scan.sh", (G, "bash -n; shellcheck 0.11.0 zonder bevinding; de scanners zelf staan niet op de server")),
    ("05-git-ci/.githooks/pre-push", (G, "sh -n; shellcheck 0.11.0 zonder bevinding")),
    ("05-git-ci/*", (N, "tekstsjabloon: er bestaat geen commando dat de juistheid aantoont zonder het in een echte repository of op een echte site te plaatsen")),
    ("06-database/migraties/backfill.sh", (G, "bash -n en gedraaid tegen een wegwerp-PostgreSQL 18.6: 2500 rijen in vier batches, tweede run 0 rijen; shellcheck 0.11.0 zonder bevinding")),
    ("06-database/*.sh", (G, "bash -n; shellcheck 0.11.0 zonder bevinding; controleer-backup.sh ook uitgevoerd in de scratchmap. backup.sh en herstelproef.sh niet tegen Docker of een server")),
    ("06-database/*.ts", (G, "tsc --noEmit (TypeScript 6.0.3, strikte tsconfig uit 07) en eslint (typescript-eslint 8.71.0) groen in een wegwerpcontainer; niet tegen een database gedraaid")),
    ("06-database/rollen.sql", (G, "gedraaid tegen een wegwerp-PostgreSQL 18.6 (postgres:18, zonder netwerk); de vier controles uit de kop geven de genoemde uitkomst")),
    ("06-database/migraties/0001*", (G, "gedraaid tegen een wegwerp-PostgreSQL 18.6 met de rollen uit rollen.sql; de tenantgrens getest met de app-rol (zonder context, andere tenant, hergebruikte verbinding, eigenaar). Hersteld: de rechten van de app-rol eerst intrekken")),
    ("06-database/*", (G, "gedraaid tegen een wegwerp-PostgreSQL 18.6, in volgorde 0002 tot en met 0005 met de backfill ertussen (2500 rijen); niet op een kopie van productie")),
    ("07-typescript-tests/tsconfig.json", (G, "tsc 6.0.3: --showConfig toont de zes opties, het API-skelet compileert ermee en een proef met een typefout wordt gevonden")),
    ("07-typescript-tests/stryker.config.json", (G, "JSON geladen; niet met StrykerJS")),
    ("07-typescript-tests/eslint.config.mjs", (G, "eslint 10.12.0 met typescript-eslint 8.71.0: het API-skelet is groen, een proef met een diepe import, any en een losse promise is rood. De e2e-regels niet gedraaid")),
    ("07-typescript-tests/e2e/*", (G, "typecontrole met tsc 6.0.3; playwright test --list (1.63.0) toont acht tests in twee projecten. Niet in een browser gedraaid")),
    ("07-typescript-tests/playwright.config.ts", (G, "typecontrole met tsc 6.0.3; playwright test --list (1.63.0) toont acht tests in twee projecten. Niet in een browser gedraaid")),
    ("07-typescript-tests/*", (G, "typecontrole met tsc 6.0.3; vitest list (5.0.3) laadt de configuratie en toont de tests. De tests zelf niet gedraaid (ze vragen het eigen project)")),
    ("08-api/migraties/*", (G, "gedraaid tegen een wegwerp-PostgreSQL 18.6; dubbele sleutel, dubbele taak en onbekende status geweigerd. Hersteld: de app-rol hield DELETE op taken via de standaardrechten")),
    ("08-api/*", (G, "tsc --noEmit (TypeScript 6.0.3, strikte tsconfig uit 07) en eslint --max-warnings 0 (typescript-eslint 8.71.0) groen in een wegwerpcontainer. Hersteld: vier lintfouten (zod 4, enum van Mollie, ongebruikte parameter). Niet gedraaid als dienst")),
    ("09-wordpress/controleer-blokkades.sh", (G, "bash -n; shellcheck 0.11.0 zonder bevinding")),
    ("09-wordpress/htaccess-versterking", (G, "gedraaid op Apache 2.4.68 in een wegwerp-WordPress (7.1.2): 22 geblokkeerde paden geven 403, zes gewone paden 200. Niet op LiteSpeed gedraaid; de meting op de productieserver blijft nodig (WP-64)")),
    ("09-wordpress/wp-config-versterking.php", (G, "php -l (PHP 8.3.35) en de regels overgenomen in de wp-config.php van een wegwerp-WordPress: wp config get toont de waarden, wp-admin gaat naar https, de editor is uit")),
    ("09-wordpress/mu-plugins/*", (G, "php -l (PHP 8.3.35) en gedraaid in een wegwerp-WordPress 7.1.2: 302 naar de inlogpagina met X-Robots-Tag, REST anoniem 401, XML-RPC uit; zonder de constante doet het niets")),
    ("09-wordpress/*", (G, "php -l (PHP 8.3.35) en gedraaid in een wegwerp-WordPress 7.1.2 met MariaDB 10.11: activeren, nonce, capability, REST, escapen, zoeken en verwijderen via HTTP en wp-cli. PHPCS, Plugin Check en PHPStan niet gedraaid")),
    ("10-bewijs-beheer/controleer-bewijs.py", (G, "py_compile en uitgevoerd op het sjabloon en op een ingevuld proefbestand")),
    ("10-bewijs-beheer/bewijsbestand.md", (G, "vorm gecontroleerd met controleer-bewijs.py")),
    ("10-bewijs-beheer/uitzonderingen.md", (G, "vorm gecontroleerd met controleer-bewijs.py")),
    ("10-bewijs-beheer/*", (N, "tekstsjabloon: er bestaat geen commando dat de juistheid aantoont; de inhoud vraagt een lezer")),
    ("11-berichten/dns-records.zone", (G, "named-checkzone (BIND 9, wegwerpcontainer) laadt de ingevulde records met een sleutel van 2048 bit. Hersteld: de DKIM-waarde in twee delen. Niet gepubliceerd of opgevraagd")),
    ("11-berichten/afmelden-routes.ts", (G, "tsc --noEmit (strikt, TypeScript 6.0.3) groen; niet met een draaiende Fastify")),
    ("11-berichten/*", (G, "uitgevoerd met node --test (Node 24.21.0): 8 tests geslaagd; tsc --noEmit (strikt) groen")),
]
# Een LEESMIJ beschrijft het bestand ernaast.
LEESMIJ = {
    "02-docker/daemon.json.LEESMIJ.md": ["02-docker/daemon.json"],
    "05-git-ci/package-scripts.LEESMIJ.md": ["05-git-ci/package-scripts.json"],
    "05-git-ci/rulesets.LEESMIJ.md": ["05-git-ci/ruleset-main.json", "05-git-ci/ruleset-tags.json"],
    "07-typescript-tests/stryker.LEESMIJ.md": ["07-typescript-tests/stryker.config.json"],
}
# Een LEESMIJ voor twee bestanden: welke ID's bij welk bestand horen.
ALLEEN = {
    "05-git-ci/ruleset-main.json": {"GIT-24", "GIT-25"},
    "05-git-ci/ruleset-tags.json": {"GIT-26"},
}
GEEN_KOP = {"INDEX.md", "bouw-index.py", "VASTE-WAARDEN.md"} | {doel for doelen in LEESMIJ.values() for doel in doelen}


def bekende_ids():
    ids = {r.split("\t")[0]: r.split("\t")[7] for r in (ROOT / "skill/regel-index.tsv").read_text().splitlines()[1:]}
    for naam in BATCH4:
        for m in re.finditer(r"^### ([A-Z]+-\d+) ", (ROOT / "research" / naam).read_text(), flags=re.M):
            ids[m.group(1)] = "batch 4"
    return ids


def kale_regels(tekst):
    for regel in tekst.splitlines()[:80]:
        yield re.sub(r"^\s*(?:#|//|--|;|\*|<!--)?\s?", "", regel).rstrip()


def lees_kop(tekst):
    """Geeft (volledig, gedeeltelijk): de ID's uit "Dekt:" en uit "Dekt gedeeltelijk:"."""
    blok, dekt, deels = None, "", []
    for regel in kale_regels(tekst):
        kaal = regel.strip()
        if kaal.startswith("Dekt gedeeltelijk:"):
            blok, kaal = "deels", kaal[len("Dekt gedeeltelijk:"):].strip()
            if kaal:
                deels.append("- lijst: " + kaal)
            continue
        if kaal.startswith("Dekt:"):
            blok, dekt = "dekt", kaal[len("Dekt:"):]
            continue
        if LABEL.match(kaal) or not kaal:
            blok = None
        elif blok == "dekt":
            dekt += " " + kaal
        elif blok == "deels":
            deels.append(kaal)
    volledig, gedeeltelijk = [], []
    for stuk in re.split(r",(?![^()]*\))", dekt):
        for i in ID.findall(stuk.split("(")[0]):
            (gedeeltelijk if "(" in stuk else volledig).append(i)
    genoemd = volledig + gedeeltelijk
    for punt in deels:
        if punt.startswith("- lijst: "):
            gedeeltelijk += ID.findall(punt)
            continue
        begin = re.match(r"- ((?:[A-Z]+-\d+)(?:(?:, | en | tot en met )[A-Z]+-\d+)*)", punt)
        if begin:
            gedeeltelijk += [i for i in ID.findall(begin.group(1)) if i in genoemd]
    volledig = [i for i in volledig if i not in gedeeltelijk]
    return volledig, sorted(set(gedeeltelijk))


def status_van(pad):
    for patroon, waarde in STATUS:
        if fnmatch.fnmatch(pad, patroon):
            return waarde
    return None


def main():
    ids = bekende_ids()
    bestanden = subprocess.run(["git", "ls-files", "."], cwd=HIER, check=True, timeout=30,
                               capture_output=True, text=True).stdout.split()
    rijen, per_bestand, fouten = [], [], []
    for pad in sorted(bestanden):
        if pad in GEEN_KOP:
            continue
        volledig, gedeeltelijk = lees_kop((HIER / pad).read_text())
        if not volledig and not gedeeltelijk:
            fouten.append(f"{pad}: geen regel 'Dekt:' gevonden")
        for doel in LEESMIJ.get(pad, [pad]):
            stand = status_van(doel)
            if stand is None:
                fouten.append(f"{doel}: geen status in STATUS")
                continue
            per_bestand.append((doel, stand[0], stand[1], len(volledig) + len(gedeeltelijk)))
            for i in volledig + gedeeltelijk:
                if doel in ALLEEN and i not in ALLEEN[doel]:
                    continue
                if i not in ids:
                    fouten.append(f"{pad}: onbekend regel-ID {i}")
                tekst = stand[0] + (", dekt gedeeltelijk" if i in gedeeltelijk else "")
                if ids.get(i) == "samengevoegd":
                    tekst += " (ID is samengevoegd, zie de kanonieke regel in regel-index.tsv)"
                rijen.append((i, doel, tekst))

    def sleutel(rij):
        prefix, nr = rij[0].split("-")
        return (prefix, int(nr), rij[1])

    rijen = sorted(set(rijen), key=sleutel)
    uniek = sorted({r[0] for r in rijen})
    n_g = sum(1 for b in per_bestand if b[1] == G)
    uit = [
        "# Index van de sjablonen",
        "",
        "Gemaakt door `bouw-index.py` uit de koppen van de sjablonen. Niet met de hand wijzigen: pas de kop van het sjabloon of `STATUS` in het script aan en draai het opnieuw.",
        "",
        f"- {len(per_bestand)} sjabloonbestanden, {n_g} gevalideerd en {len(per_bestand) - n_g} niet gevalideerd.",
        f"- {len(uniek)} verschillende regel-ID's, {len(rijen)} koppelingen van regel naar sjabloon.",
        "- Elk regel-ID is gecontroleerd tegen `skill/regel-index.tsv` en de vier batch-4-bestanden in `research/`.",
        "",
        "Status:",
        "",
        "- `gevalideerd`: het commando dat de juistheid aantoont is gedraaid en geslaagd, op de server of in een wegwerpcontainer; de tabel per bestand zegt welk commando en wat niet is gedraaid. Het is geen bewijs dat het sjabloon in een echt project werkt.",
        "- `niet gevalideerd`: er is geen commando dat de juistheid aantoont; de reden staat in de tabel per bestand.",
        "- `dekt gedeeltelijk`: het sjabloon voert de regel niet volledig uit; wat ontbreekt staat in de kop van het sjabloon.",
        "",
        "## Per regel",
        "",
        "| Regel | Sjabloon | Status |",
        "|---|---|---|",
    ]
    uit += [f"| {i} | `{pad}` | {tekst} |" for i, pad, tekst in rijen]
    uit += ["", "## Per bestand", "", "| Sjabloon | Status | Hoe gecontroleerd, of waarom niet | Regels |", "|---|---|---|---|"]
    uit += [f"| `{pad}` | {stand} | {hoe} | {aantal} |" for pad, stand, hoe, aantal in per_bestand]
    (HIER / "INDEX.md").write_text("\n".join(uit) + "\n")
    for fout in fouten:
        print(fout)
    print(f"{len(per_bestand)} bestanden ({n_g} gevalideerd), {len(uniek)} regel-ID's, {len(rijen)} koppelingen, {len(fouten)} fouten")
    return 1 if fouten else 0


if __name__ == "__main__":
    sys.exit(main())
