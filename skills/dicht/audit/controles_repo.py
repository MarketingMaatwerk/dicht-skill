"""Controles op de repository: GIT, API (gate), SCR (scripts), INFRA (Compose-bestanden), AI (MCP-configuratie).

Alles leest alleen bestanden in --pad of vraagt git, npm, composer of gh om een overzicht.
"""
import json
import os
import re
import stat

from dicht_audit import FAIL, NVT, ONBEKEND, PASS, controle, lib

GEHEIMNAAM = re.compile(r"(^|/)\.env($|\.)|\.pem$|\.key$|\.sql(\.gz)?$|\.wpress$|\.bak", re.I)   # GIT-10
PIJP = re.compile(r"(curl|wget)[^|;]*\| *(sudo +)?(ba|z|da)?sh\b|(bash|sh|python3?) +<\((curl|wget)|eval +\"?\$\((curl|wget)")  # SCR-22


def _json(ctx, rel):
    tekst = ctx.lees(rel)
    if tekst is None:
        return None
    try:
        return json.loads(tekst)
    except ValueError:
        return {}


def _workflows(ctx):
    return [b for b in ctx.bestanden() if re.match(r"\.github/workflows/[^/]+\.ya?ml$", b)]


def _shell(ctx):
    uit = []
    for b in ctx.bestanden():
        if b.endswith(".sh") or ("." not in os.path.basename(b) and (ctx.lees(b, 200_000) or "").startswith(("#!/bin/bash", "#!/usr/bin/env bash", "#!/bin/sh"))):
            uit.append(b)
    return uit[:200]


def _treffers(ctx, bestanden, patroon, maximum=5):
    hits = []
    for b in bestanden:
        for nr, regel in enumerate((ctx.lees(b) or "").splitlines(), 1):
            if patroon.search(regel):
                hits.append("%s:%d" % (b, nr))
    return hits, ", ".join(hits[:maximum]) + (" en %d meer" % (len(hits) - maximum) if len(hits) > maximum else "")


# --- git en geheimen ---------------------------------------------------------
@controle("GIT-10", "repo", "git", ".gitignore sluit .env uit en er is geen geheimbestand gevolgd", dekking="volledig")
def git10(ctx):
    if not ctx.is_git():
        return ONBEKEND, "geen git-repository"
    gevolgd = [b for b in ctx.bestanden() if GEHEIMNAAM.search(b) and not re.search(r"\.env\.(example|sample|dist|template)$", b)]
    if gevolgd:
        return FAIL, "gevolgd: " + ", ".join(gevolgd[:8])
    code, uit = ctx.run(["git", "check-ignore", "-v", ".env"], cwd=ctx.pad)
    return (PASS, "check-ignore: " + uit) if code == 0 else (FAIL, "`git check-ignore .env` noemt geen regel")


@controle("INFRA-72", "repo", "infra", "geheimbestanden in de projectmap hebben modus 600 of 400",
          rest="eigenaar per bestand; systemd Environment= (zie de servercontrole); geheimscan over de volledige geschiedenis")
def infra72(ctx):
    fout, goed = [], 0
    for d, mappen, fs in os.walk(ctx.pad):
        mappen[:] = [m for m in mappen if m not in (".git", "node_modules", "vendor")]
        if d[len(str(ctx.pad)):].count(os.sep) >= 4:
            mappen[:] = []
        for f in fs:
            rel = os.path.relpath(os.path.join(d, f), ctx.pad)
            if lib.GEHEIM_BESTAND.search(rel) and not rel.endswith((".sql", ".sql.gz", ".bak", ".wpress")):
                modus = stat.S_IMODE(os.lstat(os.path.join(d, f)).st_mode)
                if modus in (0o600, 0o400):
                    goed += 1
                else:
                    fout.append("%s %o" % (rel, modus))
    if fout:
        return FAIL, "te ruim: " + ", ".join(fout[:8])
    return (PASS, "%d geheimbestand(en), alle 600 of 400" % goed) if goed else (NVT, "geen .env, sleutel of certificaatbestand in de projectmap")


@controle("GIT-32", "repo", "git", "geheimscan over de gevolgde bestanden",
          rest="scan van de hele geschiedenis (GIT-34); .env.example vergelijken met .env")
def git32(ctx):
    treffers = []
    for b in ctx.bestanden():
        for nr, regel in enumerate((ctx.lees(b) or "").splitlines(), 1):
            if "gitleaks:allow" not in regel:
                treffers += ["%s:%d %s" % (b, nr, n) for n in lib.vind_geheimen(regel)]
    return (FAIL, "%d treffer(s): %s" % (len(treffers), ", ".join(treffers[:6]))) if treffers else (PASS, "geen treffer in %d bestanden" % len(ctx.bestanden()))


@controle("GIT-33", "repo", "git", "pre-commit-hook met geheimscan aanwezig", rest="een testcommit met een nepsleutel wordt geweigerd")
def git33(ctx):
    if not ctx.is_git():
        return ONBEKEND, "geen git-repository"
    code, pad = ctx.run(["git", "rev-parse", "--git-path", "hooks/pre-commit"], cwd=ctx.pad)
    hook = ctx.pad / pad if code == 0 else None
    if hook and hook.is_file() and os.access(hook, os.X_OK):
        tekst = hook.read_text(errors="replace")
        if re.search(r"geheimscan|gitleaks|betterleaks|trufflehog|pre-commit", tekst):
            return PASS, "%s roept een geheimscan aan" % pad
        return FAIL, "%s bestaat maar noemt geen geheimscan" % pad
    if "gitleaks" in (ctx.lees(".pre-commit-config.yaml") or ""):
        return ONBEKEND, ".pre-commit-config.yaml noemt gitleaks, maar de hook is hier niet geinstalleerd"
    return FAIL, "geen uitvoerbare pre-commit-hook"


@controle("GIT-18", "repo", "git", "laatste commit is ondertekend", rest="op GitHub staat Verified bij de commit")
def git18(ctx):
    code, uit = ctx.run(["git", "log", "-1", "--format=%G?"], cwd=ctx.pad)
    if code != 0:
        return ONBEKEND, "geen git-repository of geen commit"
    return (PASS, "%G? = G") if uit.strip() == "G" else (FAIL, "%%G? = %s" % (uit.strip() or "leeg"))


@controle("GIT-09", "repo", "git", "er is een remote buiten de server", rest="git ls-remote geeft de laatste commit van main; herstelproef binnen drie maanden")
def git09(ctx):
    code, uit = ctx.run(["git", "remote"], cwd=ctx.pad)
    if code != 0:
        return ONBEKEND, "geen git-repository"
    return (PASS, "remote: " + ", ".join(uit.split())) if uit.strip() else (FAIL, "geen remote; alleen geldig met een bundle in de offsite back-up")


def _github(ctx):
    code, uit = ctx.run(["git", "remote", "get-url", "origin"], cwd=ctx.pad)
    m = re.search(r"github\.com[:/]([^/\s]+)/([^/\s]+?)(\.git)?$", uit) if code == 0 else None
    return "%s/%s" % (m.group(1), m.group(2)) if m else None


@controle("GIT-24", "repo", "git", "actieve ruleset op de standaardbranch", dekking="volledig")
def git24(ctx):
    repo = _github(ctx)
    if not repo:
        return ONBEKEND, "geen GitHub-remote"
    code, uit = ctx.run(["gh", "api", "repos/%s/rulesets" % repo], timeout=30)
    try:
        sets = json.loads(uit) if code == 0 else None
    except ValueError:
        sets = None
    if not isinstance(sets, list):
        return ONBEKEND, "gh api gaf geen lijst (exit %s)" % code
    actief = [s for s in sets if s.get("enforcement") == "active" and s.get("target") == "branch"]
    if not actief:
        return FAIL, "geen actieve ruleset op een branch (%d rulesets)" % len(sets)
    laatste = "details van de ruleset niet te lezen"
    nodig = {"non_fast_forward", "deletion", "required_signatures", "pull_request", "required_status_checks"}
    for s in actief[:3]:
        code, uit = ctx.run(["gh", "api", "repos/%s/rulesets/%s" % (repo, s.get("id"))], timeout=30)
        try:
            d = json.loads(uit)
        except ValueError:
            continue
        mist = nodig - {r.get("type") for r in d.get("rules", [])}
        if not mist and not d.get("bypass_actors"):
            return PASS, "ruleset %s: alle vijf regels, lege bypass-lijst" % s.get("name")
        laatste = "ruleset %s mist %s, bypass %d" % (s.get("name"), ", ".join(sorted(mist)) or "niets", len(d.get("bypass_actors") or []))
    return FAIL, laatste


@controle("GIT-28", "repo", "git", "Dependabot-meldingen en beveiligingsupdates aan", dekking="volledig")
def git28(ctx):
    repo = _github(ctx)
    if not repo:
        return ONBEKEND, "geen GitHub-remote"
    code, uit = ctx.run(["gh", "api", "repos/%s/vulnerability-alerts" % repo, "-i"], timeout=30)
    if code is None:
        return ONBEKEND, uit
    eerste = uit.splitlines()[0] if uit else ""
    if " 204" not in eerste:
        return (FAIL, "vulnerability-alerts: " + eerste) if " 404" in eerste else (ONBEKEND, "vulnerability-alerts: " + eerste)
    code, uit = ctx.run(["gh", "api", "repos/%s/automated-security-fixes" % repo], timeout=30)
    try:
        aan = json.loads(uit).get("enabled") is True
    except ValueError:
        return ONBEKEND, "automated-security-fixes gaf geen JSON"
    return (PASS, "alerts 204, automated-security-fixes enabled") if aan else (FAIL, "alerts 204, automated-security-fixes uit")


@controle("GIT-76", "repo", "git", ".github/dependabot.yml bestaat", rest="een blok per ecosysteem; Dependabot-PR's gezien of npm outdated zonder achterstand")
def git76(ctx):
    return (PASS, "aanwezig") if any(b in (".github/dependabot.yml", ".github/dependabot.yaml") for b in ctx.bestanden()) else (FAIL, "ontbreekt")


# --- afhankelijkheden ---------------------------------------------------------
@controle("GIT-69", "repo", "git", "lockfile gevolgd en geen kale npm install", rest="npm ci slaagt in een schone map")
def git69(ctx):
    if ctx.lees("package.json") is None:
        return NVT, "geen package.json"
    locks = [b for b in ctx.bestanden() if b in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "npm-shrinkwrap.json")]
    if not locks:
        return FAIL, "geen lockfile gevolgd"
    waar = [b for b in ctx.bestanden() if b.startswith(("Dockerfile", ".github/", "scripts/")) or b == "package.json"]
    hits, tekst = _treffers(ctx, waar, re.compile(r"npm (install|i)( |$)(?!.*-g )"))
    return (FAIL, "kale npm install: " + tekst) if hits else (PASS, locks[0] + " gevolgd")


@controle("GIT-81", "repo", "git", "composer.lock gevolgd", rest="composer validate groen; installeren met --no-dev")
def git81(ctx):
    if ctx.lees("composer.json") is None:
        return NVT, "geen composer.json"
    return (PASS, "composer.lock gevolgd") if "composer.lock" in ctx.bestanden() else (FAIL, "composer.lock niet gevolgd")


@controle("GIT-61", "repo", "git", "afhankelijkheden-audit op het lockfile", rest="npm audit signatures; uitzondering met einddatum per bevinding (GIT-65)")
def git61(ctx):
    delen, status = [], NVT
    if ctx.lees("package-lock.json", 20_000_000) is not None:
        code, uit = ctx.run(["npm", "audit", "--omit=dev", "--json"], timeout=90, cwd=ctx.pad)
        try:
            v = json.loads(uit[uit.index("{"):])["metadata"]["vulnerabilities"]
            n = sum(v.get(k, 0) for k in ("critical", "high", "moderate", "low"))
            status = FAIL if n else PASS
            delen.append("npm audit: kritiek %d, hoog %d, middel %d, laag %d" % (v.get("critical", 0), v.get("high", 0), v.get("moderate", 0), v.get("low", 0)))
        except (ValueError, KeyError, TypeError):
            status = ONBEKEND
            delen.append("npm audit gaf geen bruikbare uitvoer (exit %s)" % code)
    if "composer.lock" in ctx.bestanden():
        code, uit = ctx.run(["composer", "audit", "--locked", "--no-interaction"], timeout=90, cwd=ctx.pad)
        if code is None:
            status = ONBEKEND if status != FAIL else FAIL
            delen.append("composer audit: " + uit)
        else:
            status = FAIL if code else (status if status != NVT else PASS)
            delen.append("composer audit exit %d" % code)
    return status, "; ".join(delen) or "geen package-lock.json of composer.lock"


@controle("GIT-73", "repo", "git", "geen afhankelijkheid uit git of van een losse URL", rest="npm query \":type(git)\" is leeg")
def git73(ctx):
    tekst = ctx.lees("package.json")
    if tekst is None:
        return NVT, "geen package.json"
    hits = re.findall(r"\"(?:git\+|github:|https?://)[^\"]*\"", tekst)
    hits = [h for h in hits if not re.search(r"\"(homepage|url|bugs|repository)\"", tekst[max(0, tekst.index(h) - 40):tekst.index(h)])]
    return (FAIL, "%d verwijzing(en) naar git of een URL" % len(hits)) if hits else (PASS, "geen treffer in package.json")


# --- gate, types, lint --------------------------------------------------------
def _scripts(ctx):
    s = {}
    for rel in ("package.json", "composer.json"):
        d = _json(ctx, rel)
        if d:
            s.update({k: str(v) for k, v in (d.get("scripts") or {}).items()})
    return s


@controle("GIT-57", "repo", "git", "de gate noemt lint, typecheck of analyse, en tests",
          rest="de scans in de gate (geheimen, afhankelijkheden, SAST); de laatste uitvoer met exitcode 0")
def git57(ctx):
    s = _scripts(ctx)
    if not s:
        return ONBEKEND, "geen scripts in package.json of composer.json; waar staat de gate?"
    alles = " ".join(list(s) + list(s.values())).lower()
    mist = [n for n, pat in (("lint", r"lint|phpcs"), ("typecheck of analyse", r"typecheck|tsc|phpstan|psalm"), ("tests", r"\btest|vitest|jest|phpunit|playwright")) if not re.search(pat, alles)]
    return (FAIL, "ontbreekt: " + ", ".join(mist)) if mist else (PASS, "scripts: " + ", ".join(sorted(s)[:10]))


@controle("GIT-58", "repo", "git", "er is één gate-opdracht", rest="de opdracht geeft exitcode 0 in de worktree en CI draait dezelfde")
def git58(ctx):
    namen = [k for k in _scripts(ctx) if k in ("gate", "check", "ci", "verify", "validate")]
    namen += [b for b in ctx.bestanden() if re.match(r"(scripts/)?(gate|check|ci)\.sh$", b)]
    if re.search(r"^(gate|check|ci):", ctx.lees("Makefile") or "", re.M):
        namen.append("Makefile")
    return (PASS, "gate: " + ", ".join(namen)) if namen else (FAIL, "geen script gate, check, ci of verify")


@controle("API-67", "repo", "api", "tsconfig zet strict expliciet aan", rest="tsc --showConfig toont de zes opties; npm run typecheck groen in CI")
def api67(ctx):
    tekst = ctx.lees("tsconfig.json")
    if tekst is None:
        return NVT, "geen tsconfig.json"
    return (PASS, '"strict": true') if re.search(r'"strict"\s*:\s*true', tekst) else (FAIL, '"strict": true ontbreekt in tsconfig.json')


@controle("API-68", "repo", "api", "ESLint-configuratie aanwezig", rest="eslint . --max-warnings 0 groen in CI, met de type-bewuste set")
def api68(ctx):
    if ctx.lees("tsconfig.json") is None:
        return NVT, "geen TypeScript-project"
    gevonden = [b for b in ctx.bestanden() if re.match(r"(eslint\.config\.(js|mjs|cjs|ts)|\.eslintrc(\..+)?)$", b)]
    return (PASS, gevonden[0]) if gevonden else (FAIL, "geen eslint.config.* of .eslintrc")


@controle("API-72", "repo", "api", "package.json eist een ondersteunde Node-versie", rest="node -v op de server en in het image")
def api72(ctx):
    d = _json(ctx, "package.json")
    if d is None:
        return NVT, "geen package.json"
    eis = str((d.get("engines") or {}).get("node", ""))
    m = re.search(r"(\d+)", eis)
    if not m:
        return FAIL, "engines.node ontbreekt"
    return (PASS, "engines.node " + eis) if int(m.group(1)) >= 22 else (FAIL, "engines.node %s is lager dan 22" % eis)


@controle("API-78", "repo", "api", "phpstan.neon staat in de repository", rest="phpstan analyse --level 8 groen in CI")
def api78(ctx):
    if not any(b.endswith(".php") for b in ctx.bestanden()):
        return NVT, "geen PHP-bestanden"
    return (PASS, "aanwezig") if any(re.match(r"phpstan(\.dist)?\.neon(\.dist)?$", b) for b in ctx.bestanden()) else (FAIL, "phpstan.neon ontbreekt")


# --- GitHub Actions -----------------------------------------------------------
@controle("GIT-41", "repo", "git", "elke actie staat vast op een commit-SHA", rest="zizmor meldt geen unpinned-uses; repo-instelling van GIT-27")
def git41(ctx):
    wf = _workflows(ctx)
    if not wf:
        return NVT, "geen workflows"
    hits, tekst = _treffers(ctx, wf, re.compile(r"uses: +(?!\./)[^#\s]+@(?![0-9a-f]{40}(\s|$))"))
    return (FAIL, "niet op SHA: " + tekst) if hits else (PASS, "%d workflow(s), alles op SHA" % len(wf))


@controle("GIT-43", "repo", "git", "elke workflow heeft permissions op het hoogste niveau", rest="zizmor meldt geen excessive-permissions")
def git43(ctx):
    wf = _workflows(ctx)
    if not wf:
        return NVT, "geen workflows"
    zonder = [b for b in wf if not re.search(r"^permissions:", ctx.lees(b) or "", re.M)]
    return (FAIL, "zonder permissions: " + ", ".join(zonder[:6])) if zonder else (PASS, "%d workflow(s)" % len(wf))


@controle("GIT-44", "repo", "git", "geen expressie met invoer van buiten in een run-stap", rest="zizmor meldt geen template-injection (ook meerregelige run-blokken)")
def git44(ctx):
    wf = _workflows(ctx)
    if not wf:
        return NVT, "geen workflows"
    hits, tekst = _treffers(ctx, wf, re.compile(r"run:.*\$\{\{ *(github\.(event|head_ref)|inputs\.)"))
    return (FAIL, tekst) if hits else (PASS, "geen treffer")


@controle("GIT-45", "repo", "git", "geen gevaarlijke trigger in een workflow", rest="zizmor meldt geen dangerous-triggers")
def git45(ctx):
    wf = _workflows(ctx)
    if not wf:
        return NVT, "geen workflows"
    hits, tekst = _treffers(ctx, wf, re.compile(r"pull_request_target|workflow_run|issue_comment"))
    return (ONBEKEND, "stel per treffer vast dat er geen checkout van PR-code volgt: " + tekst) if hits else (PASS, "geen treffer")


# --- Docker-bestanden ---------------------------------------------------------
def _dockerfiles(ctx):
    return [b for b in ctx.bestanden() if os.path.basename(b).startswith("Dockerfile")]


def _compose(ctx):
    return [b for b in ctx.bestanden() if re.match(r"(docker-)?compose[^/]*\.ya?ml$", os.path.basename(b))]


@controle("GIT-91", "repo", "git", "elke image staat vast op een digest", rest="de treffers zijn alleen bouwfasen of eigen images; digest van de index")
def git91(ctx):
    bestanden = _dockerfiles(ctx) + _compose(ctx)
    if not bestanden:
        return NVT, "geen Dockerfile of Compose-bestand"
    hits, tekst = _treffers(ctx, bestanden, re.compile(r"^(FROM |\s*image:)(?!.*@sha256:)(?!.*\bscratch\b)"))
    return (FAIL, "zonder digest: " + tekst) if hits else (PASS, "%d bestand(en), alles op digest" % len(bestanden))


@controle("GIT-96", "repo", "git", "een Dockerfile haalt niets op zonder controlesom", dekking="volledig")
def git96(ctx):
    df = _dockerfiles(ctx)
    if not df:
        return NVT, "geen Dockerfile"
    hits, tekst = _treffers(ctx, df, re.compile(r"curl[^|]*\| *(ba)?sh|wget[^|]*\| *(ba)?sh|^ADD +(?!--checksum)https?://"))
    return (FAIL, tekst) if hits else (PASS, "geen treffer in %d Dockerfile(s)" % len(df))


COMPOSE_REGELS = ["INFRA-13", "INFRA-26", "INFRA-27", "INFRA-28", "INFRA-29", "INFRA-30", "INFRA-31", "INFRA-32", "INFRA-33", "INFRA-35"]


@controle(COMPOSE_REGELS, "repo", "infra", "vlaggen in het Compose-bestand",
          rest="dezelfde meting met docker inspect op de draaiende containers (servercontrole)")
def compose(ctx):
    bestanden = _compose(ctx)
    if not bestanden:
        return {r: (NVT, "geen Compose-bestand") for r in COMPOSE_REGELS}
    try:
        import yaml
    except ImportError:
        return {r: (ONBEKEND, "PyYAML ontbreekt; Compose-bestand niet gelezen") for r in COMPOSE_REGELS}
    diensten = {}
    for b in bestanden:
        try:
            d = yaml.safe_load(ctx.lees(b) or "") or {}
        except yaml.YAMLError:
            return {r: (ONBEKEND, "%s is geen geldige YAML" % b) for r in COMPOSE_REGELS}
        diensten.update({"%s:%s" % (b, n): s for n, s in (d.get("services") or {}).items() if isinstance(s, dict)})
    if not diensten:
        return {r: (ONBEKEND, "geen services gevonden") for r in COMPOSE_REGELS}

    def lijst(s, sleutel):
        v = s.get(sleutel) or []
        return [str(x) for x in (v if isinstance(v, list) else [v])]

    def poort_open(p):
        p = str(p.get("host_ip", "0.0.0.0") + ":x" if isinstance(p, dict) else p)
        return not p.startswith(("127.0.0.1:", "[::1]:")) and ":" in p

    toetsen = {
        "INFRA-13": lambda s: not any(poort_open(p) for p in (s.get("ports") or [])),
        "INFRA-26": lambda s: not any("docker.sock" in str(v) for v in (s.get("volumes") or [])),
        "INFRA-27": lambda s: str(s.get("user", "")).split(":")[0] not in ("", "0", "root"),
        "INFRA-28": lambda s: "ALL" in [c.upper() for c in lijst(s, "cap_drop")],
        "INFRA-29": lambda s: any("no-new-privileges" in o and not o.endswith("false") for o in lijst(s, "security_opt")),
        "INFRA-30": lambda s: s.get("read_only") is True,
        "INFRA-31": lambda s: not (s.get("privileged") or s.get("network_mode") == "host" or s.get("pid") == "host"),
        "INFRA-32": lambda s: bool((s.get("mem_limit") or ((s.get("deploy") or {}).get("resources") or {}).get("limits", {}).get("memory")) and s.get("pids_limit")),
        "INFRA-33": lambda s: "max-size" in ((s.get("logging") or {}).get("options") or {}) or (s.get("logging") or {}).get("driver") not in (None, "json-file", "local"),
        "INFRA-35": lambda s: bool(s.get("healthcheck")) and str(s.get("restart", "no")) != "no",
    }
    uit = {}
    for regel, f in toetsen.items():
        fout = [n.split(":", 1)[1] for n, s in diensten.items() if not f(s)]
        uit[regel] = (FAIL, "services: " + ", ".join(fout[:8])) if fout else (PASS, "%d service(s)" % len(diensten))
    return uit


# --- scripts (batch 4) --------------------------------------------------------
@controle("SCR-01", "repo", "scripts", "elk shellscript begint met de strikte modus", dekking="volledig")
def scr01(ctx):
    sh = _shell(ctx)
    if not sh:
        return NVT, "geen shellscripts"
    zonder = [b for b in sh if not re.search(r"^set -euo pipefail|^set -eu -o pipefail", "\n".join((ctx.lees(b) or "").splitlines()[:8]), re.M)]
    return (FAIL, "ONTBREEKT %s (of geef per bestand een commentaarregel met de reden)" % ", ".join(zonder[:8])) if zonder else (PASS, "%d script(s)" % len(sh))


@controle("SCR-18", "repo", "scripts", "geen slotbestand in /tmp", rest="proef: een tweede start eindigt met de melding draait al; crontab (servercontrole)")
def scr18(ctx):
    sh = _shell(ctx)
    if not sh:
        return NVT, "geen shellscripts"
    hits, tekst = _treffers(ctx, sh, re.compile(r"flock[^|;]*/tmp/"))
    return (FAIL, tekst) if hits else (PASS, "geen flock op /tmp in %d script(s)" % len(sh))


@controle("SCR-22", "repo", "scripts", "niets wordt uitgevoerd dat in dezelfde regel is opgehaald", rest="crontab (servercontrole); installatiestappen uit een README die je zelf uitvoert")
def scr22(ctx):
    waar = [b for b in ctx.bestanden() if b.endswith((".sh", ".yml", ".yaml", ".py")) or os.path.basename(b).startswith(("Dockerfile", "Makefile"))] + _shell(ctx)
    hits, tekst = _treffers(ctx, sorted(set(waar)), PIJP)
    return (FAIL, tekst) if hits else (PASS, "geen treffer in %d bestand(en)" % len(set(waar)))


@controle("SCR-23", "repo", "scripts", "shellcheck is schoon", rest="shellcheck staat vast op een versie; elke shellcheck disable heeft een reden")
def scr23(ctx):
    sh = _shell(ctx)
    if not sh:
        return NVT, "geen shellscripts"
    code, uit = ctx.run(["shellcheck", "-S", "warning", "-f", "gcc", "--"] + sh[:50], timeout=60, cwd=ctx.pad)
    if code is None:
        return ONBEKEND, uit
    return (PASS, "%d script(s) schoon" % len(sh[:50])) if code == 0 else (FAIL, "%d melding(en): %s" % (len(uit.splitlines()), "; ".join(uit.splitlines()[:3])))


# --- MCP-configuratie -----------------------------------------------------------
def _mcp_json(ctx):
    return [b for b in ctx.bestanden() if re.search(r"\.claude\.json$|\.mcp\.json$|mcp[^/]*\.json$", b)]


@controle("AI-56", "mcp", "ai-mcp", "elke MCP-server in het project staat vast op een versie", rest="dezelfde grep op ~/.claude.json (niet gelezen: bevat tokens)")
def ai56(ctx):
    mj = _mcp_json(ctx)
    if not mj:
        return NVT, "geen .mcp.json in het project"
    hits, tekst = _treffers(ctx, mj, re.compile(r"@latest|npx[^@]*\"-y\", *\"[^@\"]+\""))
    if not hits:  # ook de opmaak met één argument per regel
        for b in mj:
            for srv, d in ((_json(ctx, b) or {}).get("mcpServers") or {}).items():
                a = [str(x) for x in (d.get("args") or [])] if isinstance(d, dict) else []
                if d.get("command") in ("npx", "uvx") and not any(re.search(r".@\d", x) for x in a if not x.startswith("-")):
                    hits.append("%s:%s" % (b, srv))
        tekst = ", ".join(hits[:5])
    return (FAIL, "zonder vaste versie: " + tekst) if hits else (PASS, "%d bestand(en)" % len(mj))


@controle("AI-60", "mcp", "ai-mcp", "geen token in gevolgde MCP-configuratie", rest="stat -c %a ~/.claude.json geeft 600")
def ai60(ctx):
    mj = _mcp_json(ctx) if ctx.is_git() else []
    if not mj:
        return NVT, "geen gevolgde MCP-configuratie"
    hits = []
    for b in mj:
        for nr, regel in enumerate((ctx.lees(b) or "").splitlines(), 1):
            m = re.search(r"(Authorization|Bearer|API_KEY|TOKEN)[\"']?\s*[:=]\s*[\"']?(Bearer\s+)?([^\"'\s,]{8,})", regel)
            if m and lib.lijkt_echt(m.group(3)) or lib.vind_geheimen(regel):
                hits.append("%s:%d" % (b, nr))
    return (FAIL, "mogelijke echte waarde op " + ", ".join(hits[:5])) if hits else (PASS, "%d bestand(en), geen echte waarde" % len(mj))


@controle("AI-47", "mcp", "ai-mcp", "geen shell-aanroep in de servercode", rest="test met de argumenten `; id`, `$(id)` en `--output=/tmp/x`")
def ai47(ctx):
    code = [b for b in ctx.bestanden() if b.endswith((".ts", ".js", ".mjs", ".py")) and "node_modules" not in b and not re.search(r"(^|/)(test|tests|__tests__)/|\.test\.", b)]
    if not code:
        return NVT, "geen servercode gevonden"
    hits = []
    for b in code:
        t = ctx.lees(b) or ""
        # exec( telt alleen in een bestand dat child_process gebruikt (anders is het RegExp.exec)
        pat = r"shell: *true|shell=True|os\.system\(|\bpopen\(|\bexecSync\(" + (r"|\bexec\(" if "child_process" in t else "")
        hits += ["%s:%d" % (b, nr) for nr, regel in enumerate(t.splitlines(), 1) if re.search(pat, regel)]
    tekst = ", ".join(hits[:5])
    return (FAIL, tekst) if hits else (PASS, "geen treffer in %d bestand(en)" % len(code))
