"""Gedeelde functies voor de hooks en de auditscripts van de skill "dicht".

Alleen de standaardbibliotheek. Leest: `.dicht/project`, `.dicht/profiel.json`, de checklist van het
projecttype, het nieuwste bewijsbestand en `docs/uitzonderingen.md`. Met een profiel kiest
`tools/regels_voor_wijziging.py` de regels van een wijziging (het kleine-wijziging-pad).
Schrijft zelf niets, behalve `schrijf_overrule` (de noodrem van Marketing Maatwerk) en `log_hook` (één regel in het hooklog).
"""
import datetime
import os
import re
import sys
from pathlib import Path

TYPES = ("website", "wp-plugin", "wp-thema", "api", "app", "mcp", "klantproject")
SUBSKILLS = ("dicht-ai-mcp", "dicht-anti-vibe", "dicht-api", "dicht-architectuur", "dicht-berichten", "dicht-database", "dicht-git", "dicht-infra",
             "dicht-invoer", "dicht-privacy", "dicht-scripts", "dicht-web", "dicht-wordpress")
REGEL_ID = re.compile(r"^[A-Z]{2,5}-\d{1,3}$")
AFGEVINKT = ("voldaan", "nvt", "uitzondering")

# --- geheimen herkennen en maskeren -----------------------------------------
# Bestandsnamen uit GIT-04 en GIT-10. Verbindingsreeks uit GIT-32. AWS-regel uit GIT-33.
# De overige tokenvormen zijn een aanvulling uit algemene kennis van die leveranciers
# (niet uit het onderzoek); zie HOOKS-AUDIT-NOTITIES.md.
_GEHEIM_BESTAND = re.compile(
    r"(^|/)\.env($|\.(?!example$|sample$|dist$|template$))|\.pem$|\.key$|\.sql(\.gz)?$|\.wpress$|\.bak$"
    r"|(^|/)id_(rsa|ed25519|ecdsa)$", re.I)
class _GeheimBestand:
    """Zelfde gebruik als het patroon (`.search(naam)`), zonder vrijstellingen; zet een eigen vrijstelling hier, met verloopdatum (ARCH-30). `vandaag` is er voor de proef."""

    @staticmethod
    def search(naam, vandaag=None):
        return _GEHEIM_BESTAND.search(naam)


GEHEIM_BESTAND = _GeheimBestand()
GEHEIM_PATRONEN = [
    ("privesleutel", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("verbindingsreeks-met-wachtwoord", re.compile(r"\b(postgres(ql)?|mysql|mongodb(\+srv)?|redis|amqp)://[^:@/\s]+:[^@\s$<{]{3,}@")),
    ("aws-sleutel-id", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("aws-geheime-sleutel", re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*['\"]?[A-Za-z0-9/+=]{40}")),
    ("github-token", re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})")),
    ("anthropic-sleutel", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("openai-sleutel", re.compile(r"\bsk-(proj-)?[A-Za-z0-9_-]{32,}")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("stripe-sleutel", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{20,}")),
    ("mollie-sleutel", re.compile(r"\blive_[A-Za-z0-9]{30,}\b")),
    ("google-sleutel", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("discord-webhook", re.compile(r"discord(app)?\.com/api/webhooks/\d+/[A-Za-z0-9_-]{30,}")),
]
_TOEWIJZING = re.compile(
    r"(?i)\b([A-Z0-9_.-]*(password|passwd|wachtwoord|secret|token|api[_-]?key|private[_-]?key|auth[_-]?key)[A-Z0-9_]*)"
    r"\s*[=:]\s*['\"]?([^\s'\"]{12,})")
_NEP = re.compile(r"(?i)example|voorbeeld|changeme|change_me|placeholder|dummy|nepwaarde|your[_-]|xxxx|<|\$\{|\$\(|process\.env|getenv|os\.environ|^\$|\*\*\*|^(true|false|null|none)$")
_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")


def lijkt_echt(waarde):
    """Een toegewezen waarde telt als geheim als hij letters en cijfers mengt en geen nepwaarde is."""
    return bool(re.search(r"[A-Za-z]", waarde) and re.search(r"\d", waarde) and not _NEP.search(waarde))


def vind_geheimen(tekst):
    """Geeft de namen van de patronen die in de tekst voorkomen. Nooit de waarde zelf."""
    namen = [naam for naam, pat in GEHEIM_PATRONEN if pat.search(tekst)]
    for m in _TOEWIJZING.finditer(tekst):
        if lijkt_echt(m.group(3)):
            namen.append("toewijzing-" + m.group(2).lower().replace("-", "_"))
            break
    return namen


def maskeer(tekst):
    """Vervangt alles wat op een geheim of een e-mailadres lijkt (ARCH-85)."""
    tekst = re.sub(r"(://[^:@/\s]+:)[^@\s]+@", r"\1[GEMASKEERD]@", tekst)
    for naam, pat in GEHEIM_PATRONEN:
        tekst = pat.sub("[GEMASKEERD:%s]" % naam, tekst)
    tekst = _TOEWIJZING.sub(lambda m: m.group(1) + "=[GEMASKEERD]", tekst)
    return _EMAIL.sub("[e-mail]", tekst)


# --- project, checklist, bewijs, uitzonderingen ------------------------------
def vind_project(cwd):
    """Zoekt omhoog naar een map met `.dicht/`. Geeft het pad of None."""
    p = Path(cwd).resolve()
    for d in (p, *p.parents):
        if (d / ".dicht").is_dir():
            return d
    return None


def lees_project(root):
    """Leest `.dicht/project` (regels `sleutel: waarde`). Geeft de lijst van projecttypes."""
    f = root / ".dicht" / "project"
    if not f.is_file():
        try:  # alleen een profiel: de types staan daar
            import json
            return [t for t in json.loads((root / ".dicht" / "profiel.json").read_text(encoding="utf-8"))["types"] if t in TYPES]
        except (OSError, ValueError, KeyError, TypeError):
            return []
    for regel in f.read_text(encoding="utf-8", errors="replace").splitlines():
        if regel.lower().startswith("type:"):
            return [t.strip() for t in regel.split(":", 1)[1].split(",") if t.strip() in TYPES]
    return []


def checklist_pad(projecttype):
    hier = Path(__file__).resolve().parent
    kandidaten = [os.environ.get("DICHT_CHECKLISTS"), hier.parent / "checklists",
                  hier.parent / "dicht" / "checklists", Path.home() / ".claude/skills/dicht/checklists"]
    for k in kandidaten:
        if k and (Path(k) / (projecttype + ".md")).is_file():
            return Path(k) / (projecttype + ".md")
    return None


def lees_checklist(pad):
    """Geeft per punt: id, hard (bool), subskill, fase en de tekst (wat telt als afgevinkt)."""
    punten, hard, fase, sub = [], False, "", ""
    for regel in pad.read_text(encoding="utf-8").splitlines():
        if regel.startswith("## "):
            fase, _, soort = regel[3:].partition(":")
            hard = soort.strip().startswith("hard")
        elif regel.startswith("### "):
            sub = regel[4:].strip()
        else:
            m = re.match(r"- \[.\] ([A-Z]+-\d+)(?: → \S+)? \((\w+)\) (.*)", regel)
            if m:
                punten.append({"id": m.group(1), "hard": hard, "subskill": sub, "fase": fase.strip(),
                               "ernst": m.group(2), "tekst": m.group(3)})
    return punten


def nieuwste_bewijs(root):
    bestanden = sorted((root / "bewijs").glob("*.md"), key=lambda p: p.stat().st_mtime)
    return bestanden[-1] if bestanden else None


def _cellen(regel):
    return [c.strip() for c in regel.strip().strip("|").split("|")]


def lees_kop(pad):
    """De velden uit de kop van een bewijsbestand (tussen de twee regels `---`), zoals `pad` en `basis`."""
    kop, binnen = {}, False
    for regel in pad.read_text(encoding="utf-8", errors="replace").splitlines():
        if regel.strip() == "---":
            if binnen:
                break
            binnen = True
        elif binnen and ":" in regel:
            sleutel, waarde = regel.split(":", 1)
            kop[sleutel.strip().lower()] = waarde.strip()
    return kop


def laad_keuze():
    """Laadt tools/regels_voor_wijziging.py (naast de hooks, in $DICHT_TOOLS of in de geinstalleerde skill)."""
    hier = Path(__file__).resolve().parent
    for k in (os.environ.get("DICHT_TOOLS"), hier.parent / "tools", Path.home() / ".claude/skills/dicht/tools"):
        if k and (Path(k) / "regels_voor_wijziging.py").is_file():
            sys.path.insert(0, str(k))
            import regels_voor_wijziging
            return regels_voor_wijziging
    return None


def lees_bewijs(pad):
    """Geeft {regel-ID: (status, bewijs)} uit de tabellen Regel, Status, Bewijs."""
    rijen = {}
    for regel in pad.read_text(encoding="utf-8", errors="replace").splitlines():
        if regel.startswith("|"):
            c = _cellen(regel)
            if len(c) >= 3 and REGEL_ID.match(c[0]):
                rijen[c[0]] = (c[1].lower(), " | ".join(c[2:]))
    return rijen


def _datum(tekst):
    for vorm in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.datetime.strptime(tekst.strip(), vorm).date()
        except ValueError:
            pass
    return None


def lees_uitzonderingen(root):
    """Leest `docs/uitzonderingen.md` (ARCH-30). Geeft {U-ID: dict}; `geldig` vraagt datum, reden en een verloopdatum in de toekomst."""
    f = root / "docs" / "uitzonderingen.md"
    uit = {}
    if not f.is_file():
        return uit
    for regel in f.read_text(encoding="utf-8", errors="replace").splitlines():
        c = _cellen(regel) if regel.startswith("|") else []
        if len(c) >= 6 and re.match(r"^U-\d+$", c[0]):
            verloopt = _datum(c[5])
            uit[c[0]] = {"regels": re.findall(r"[A-Z]{2,5}-\d{1,3}", c[1]), "verloopt": verloopt,
                         "geldig": bool(_datum(c[2]) and c[3] and c[4] and verloopt
                                        and verloopt >= datetime.date.today())}
    return uit


def uitzondering_voor(regel_id, uitzonderingen):
    """Geeft (U-ID, verloopdatum) van een geldige uitzondering voor deze regel, of None."""
    for uid, u in uitzonderingen.items():
        if u["geldig"] and regel_id in u["regels"]:
            return uid, u["verloopt"]
    return None


def _open(rid, rijen, uitz):
    """Geeft de reden waarom een regel niet is afgevinkt, of None."""
    status, bewijs = rijen.get(rid, ("ontbreekt", ""))
    if status in ("voldaan", "nvt") and bewijs:
        return None
    if status == "uitzondering":
        m = re.search(r"U-\d+", bewijs)
        u = uitz.get(m.group(0)) if m else None
        if u and u["geldig"] and rid in u["regels"]:
            return None
        return "uitzondering ontbreekt in het register, dekt de regel niet, of is verlopen"
    return {"voldaan": "voldaan zonder bewijs", "nvt": "nvt zonder reden", "": "leeg"}.get(status, status)


def beoordeel(root, oplevering=False):
    """Toetst het nieuwste bewijsbestand. Geeft (ontbrekend, toelichting, meldingen); `ontbrekend` is een lijst
    van (regel-ID, reden) en leeg betekent: alles wat het pad eist is afgevinkt. `meldingen` zegt wat het
    wijzigingspad opviel (een bestand zonder patroon, een wijziging tegen het profiel in).

    Volledig pad (geen profiel, een nieuw project, een oplevering, of `pad: volledig` in de kop): elke harde
    regel van het projecttype; een domein of thema dat het profiel met reden op nvt zet, telt als afgevinkt.
    Wijzigingspad (`pad: klein` of `pad: gewoon` in de kop, bestaand project met profiel): de harde regels
    die regels_voor_wijziging.py kiest voor de wijziging tegenover de basis.
    """
    rvw, profiel, index, pat = None, None, [], None
    if (root / ".dicht" / "profiel.json").is_file():
        rvw = laad_keuze()
        if not rvw:
            return [("-", "er is een profiel, maar tools/regels_voor_wijziging.py is niet gevonden (zet DICHT_TOOLS)")], "", []
        try:
            index, pat = rvw.lees_index(), rvw.lees_patronen()
            profiel = rvw.lees_profiel(root / ".dicht" / "profiel.json", index, pat)
            rvw.controleer_plek(root)
        except rvw.Fout as fout:
            return [("-", str(fout))], "", []
    types = profiel["types"] if profiel else lees_project(root)
    if not types:
        return [("-", "geen geldig projecttype in .dicht/project (regel `type: <%s>`)" % " | ".join(TYPES))], "", []
    bewijs_pad = nieuwste_bewijs(root)
    kop = lees_kop(bewijs_pad) if bewijs_pad else {}
    pad, vereist, meldingen = "volledig", {}, []
    if profiel and profiel["stand"] == "bestaand" and not oplevering and kop.get("pad") in ("klein", "gewoon"):
        try:
            basis = rvw.bepaal_basis(root, kop.get("basis"))
            keuze = rvw.kies(rvw.lees_wijziging(root, basis), profiel, index, pat)
        except rvw.Fout as fout:
            return [("-", "de wijziging is niet te bepalen (%s); herstel `basis` in de kop of zet `pad: volledig`" % fout)], "", []
        pad, meldingen = keuze["pad"], keuze["meldingen"]
        if pad != kop["pad"]:
            meldingen = ["de kop zegt pad %s, de wijziging is %s (%s)" % (kop["pad"], pad, "; ".join(keuze["waarom_niet_klein"][:3]) or "geen reden om gewoon te zijn")] + meldingen
        vereist = {r["id"]: None for r in keuze["regels"] if r["hard"]}
        pad = "%s tegenover %s, %d bestanden" % (pad, basis[:7], len(keuze["bestanden"]))
    else:
        nvt = {r["id"]: rvw.nvt_reden(r, profiel["nvt"]) for r in index} if profiel else {}
        for t in types:
            lijst = checklist_pad(t)
            if not lijst:
                return [("-", "checklist voor type %s niet gevonden (zet DICHT_CHECKLISTS)" % t)], "", []
            vereist.update({p["id"]: nvt.get(p["id"]) for p in lees_checklist(lijst) if p["hard"]})
    if not bewijs_pad:
        return [("-", "geen bewijsbestand in bewijs/ (draai /dicht-audit)")], "%d harde regels" % len(vereist), []
    rijen, uitz = lees_bewijs(bewijs_pad), lees_uitzonderingen(root)
    ontbrekend = [(rid, reden) for rid, nvt_profiel in vereist.items()
                  if not nvt_profiel and (reden := _open(rid, rijen, uitz))]
    return ontbrekend, "%s, pad %s, %d harde regels, type %s" % (bewijs_pad.name, pad, len(vereist), ", ".join(types)), meldingen


# --- verplicht laden (besluit van Marketing Maatwerk, 05-10-2026) -----------------------------
# Overal waar gebouwd wordt: eerst de skill laden, en in een bouwproject eerst een profiel.
THUIS = Path(os.path.realpath(os.environ.get("DICHT_THUIS") or Path.home()))
# Altijd vrij: geen code, of een plek waar niet gebouwd wordt. Dit is de vastgelegde lijst (README.md).
VRIJE_MAPPEN = ("/tmp", "/dev", str(THUIS / ".claude/projects"), str(THUIS / "docs"), str(THUIS / "backups"))
VRIJE_EXTENSIES = frozenset(
    "md markdown txt rst csv tsv log pdf doc docx xls xlsx odt png jpg jpeg gif webp avif ico bmp woff woff2 ttf otf eot "
    "mp3 mp4 webm wav mov zip gz tar bak orig".split())
# Altijd code, waar het bestand ook staat. Al het andere (html, css, json, yaml, onbekend) is code binnen een bouwproject.
CODE_EXTENSIES = frozenset("php js mjs cjs ts mts cts tsx jsx vue svelte py sh bash sql service timer conf htaccess".split())
CODE_NAMEN = re.compile(r"^(Dockerfile|Makefile|crontab|(docker-)?compose[^/]*\.ya?ml$)")
VERPLICHT_REGEL = ("dicht (besluit van Marketing Maatwerk, 05-10-2026): is dit een bouw- of codetaak (website, plugin, thema, API, app, MCP, script, configuratie, "
                   "infrastructuur, klantproject)? Laad dan eerst de skill `dicht`, noem het projecttype en laad de sub-skills voor wat je "
                   "raakt, voordat je code schrijft. Een hook weigert Write en Edit op code tot dat is gedaan en het project een "
                   ".dicht/profiel.json heeft. Geen bouwtaak (tekst, mail, vraag): negeer dit.")
PROJECTKENMERK = ("package.json", "composer.json", "pyproject.toml", "requirements.txt", "Dockerfile", "docker-compose.yml",
                  "compose.yml", "style.css")


def geladen_skills(transcript):
    """De dicht-skills die deze sessie heeft geladen: een aanroep van de Skill-tool in het sessielog, of `/dicht` van de gebruiker."""
    import json
    namen = set()
    if not transcript:
        return namen
    with open(transcript, "rb") as f:
        for regel in f:
            if b"dicht" not in regel or not (b'"Skill"' in regel or b"<command-name>" in regel):
                continue
            try:
                bericht = json.loads(regel).get("message") or {}
            except ValueError:
                continue
            inhoud = bericht.get("content")
            if bericht.get("role") == "assistant" and isinstance(inhoud, list):
                namen.update(str((b.get("input") or {}).get("skill", "")) for b in inhoud
                             if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill")
            elif bericht.get("role") == "user":
                tekst = inhoud if isinstance(inhoud, str) else " ".join(
                    str(b.get("text", "")) for b in inhoud or [] if isinstance(b, dict) and b.get("type") == "text")
                # Alleen een opdracht die de gebruiker zelf typte: het bericht begint ermee (hooguit de opdrachtregel
                # ervoor). Dezelfde tekst midden in een geplakt of ingelezen bericht telt niet (AI-05).
                m = re.match(r"\s*(?:<command-message>[^<]{0,100}</command-message>\s*)?<command-name>/?(dicht[a-z-]*)</command-name>", tekst)
                if m:
                    namen.add(m.group(1))
    return {n for n in namen if re.fullmatch(r"dicht(-[a-z-]+)?", n)}


def soort_bestand(pad):
    """`vrij` (geen code of een vrije map), `code` (altijd code) of `project` (code zodra het in een bouwproject staat)."""
    pad = os.path.realpath(pad)  # waar het bestand werkelijk staat: een koppeling in een vrije map maakt code niet vrij (AI-06)
    if any(pad == m or pad.startswith(m + "/") for m in map(os.path.realpath, VRIJE_MAPPEN)):
        return "vrij"
    naam = os.path.basename(pad)
    kern = re.sub(r"(\.(bak|orig))+$", "", naam, flags=re.I)  # x.py.bak is een kopie van code, geen vrij bestand
    ext = lambda n: n.rsplit(".", 1)[-1].lower() if "." in n else ""
    if ext(kern) in CODE_EXTENSIES or CODE_NAMEN.match(kern):
        return "code"
    return "vrij" if ext(naam) in VRIJE_EXTENSIES else "project"


def vind_profiel(pad):
    """Zoekt omhoog vanaf een bestand. Geeft (root, profiel): de map van het bouwproject en het pad van `.dicht/profiel.json`.
    root is None buiten een bouwproject; profiel is None als het project er geen heeft. Een bouwproject is een map met een
    profiel, een git-repo of een map met een projectkenmerk. De thuismap zelf is een verzamelmap en geen project. In een
    worktree telt ook het profiel op dezelfde plek in de hoofdcheckout (een branch van voor het profiel)."""
    p = Path(os.path.realpath(pad))
    kandidaat = None
    for d in p.parents:
        if d == THUIS or d == d.parent:
            break
        if (d / ".dicht" / "profiel.json").is_file():
            return d, d / ".dicht" / "profiel.json"
        if kandidaat is None and any((d / k).exists() for k in PROJECTKENMERK):
            kandidaat = d
        git = d / ".git"
        if git.is_file():
            m = re.match(r"gitdir:\s*(.+)/\.git/worktrees/", git.read_text(encoding="utf-8", errors="replace"))
            hoofd = Path(os.path.realpath(m.group(1))) if m else None
            if hoofd and hoofd != d:
                root, profiel = vind_profiel(hoofd / p.relative_to(d))
                if root:
                    return d / root.relative_to(hoofd), profiel
                return kandidaat, None
        if git.exists():
            return d, None
    return kandidaat, None


def subskills_voor(rel, profiel):
    """De sub-skills die de padpatronen van het kleine-wijziging-pad aan dit bestand koppelen; met een profiel alleen
    de sub-skills die het profiel noemt. Zonder het hulpmiddel of de index: geen (alleen de kern is dan verplicht)."""
    import json
    rvw = laad_keuze()
    if not rvw:
        return set()
    index, pat = rvw.lees_index(), rvw.lees_patronen()
    eigen, toegestaan = {}, None
    if profiel:
        try:
            p = json.loads(Path(profiel).read_text(encoding="utf-8"))
            eigen, toegestaan = p.get("paden") or {}, set(p.get("subskills") or [])
            if rvw.LATER_ERBIJ in rvw.afgeleide_subskills(p, index, p.get("nvt") or {}):
                toegestaan.add(rvw.LATER_ERBIJ)  # profiel van voor 22-10-2026: de types bepalen het
        except (OSError, ValueError, AttributeError, KeyError, TypeError):
            pass
    # een voorkantbestand vraagt de oplevercontrole (dicht-anti-vibe), ook als het licht is; alleen met een profiel (de types)
    voorkant = {d for r in pat["voorkant"] if r["re"].search(rel) for d in r["doelen"]} if profiel else set()
    if any(r["re"].search(rel) for r in pat["licht"]):
        doelen = voorkant
    else:
        doelen = voorkant | ({d for k, v in eigen.items() if re.search(k, rel, re.I) for d in v}
                             or {d for r in pat["pad"] if r["re"].search(rel) for d in r["doelen"]}
                             or {d for r in pat["rest"] if r["re"].search(rel) for d in r["doelen"]})
    subs = {r["subskill"] for r in index if doelen & {r["id"], r["thema"], r["domein"]}}
    return subs & toegestaan if toegestaan is not None else subs


def profiel_fout(profiel):
    """Waarom een profiel niet geldig is (de tekst van `regels_voor_wijziging.lees_profiel`), of None.
    Zonder het hulpmiddel is er niets te toetsen: None."""
    rvw = laad_keuze()
    if not rvw:
        return None
    try:
        rvw.lees_profiel(profiel, rvw.lees_index(), rvw.lees_patronen())
    except rvw.Fout as fout:
        return str(fout)
    return None


def verplicht(pad, geladen, alleen_code=False):
    """Toetst of een bestand geschreven mag worden. Geeft None (door) of de tekst van de weigering.
    `geladen` is de verzameling geladen skills. Met `alleen_code` tellen alleen bestanden die altijd code zijn (Bash)."""
    soort = soort_bestand(pad)
    if soort == "vrij" or (alleen_code and soort != "code"):
        return None
    root, profiel = vind_profiel(pad)
    if soort == "project" and not root:
        return None
    rel = os.path.relpath(os.path.realpath(pad), root) if root else os.path.basename(pad)
    intake = rel.replace(os.sep, "/").startswith(".dicht/")
    ongeldig = profiel_fout(profiel) if profiel else None
    if ongeldig and not intake:  # een leeg, onvolledig of kapot profiel telt niet als profiel (SCR-47); weigeren, niet doorlaten (AI-25)
        return ("%s is code in een bouwproject waarvan het profiel niet geldig is: %s. Herstel %s (dat mag: schrijven in .dicht/ blijft "
                "toegestaan; zie dicht/references/intake.md) en controleer het met `python3 ~/.claude/skills/dicht/tools/regels_voor_wijziging.py "
                "--pad %s --controleer-profiel`. Herhaal daarna deze bewerking." % (pad, ongeldig[:600], profiel, root))
    subs = subskills_voor(rel.replace(os.sep, "/"), None if ongeldig else profiel)
    nodig = ["dicht"] + sorted(subs)
    mist = [s for s in nodig if s not in geladen]
    stappen = []
    if mist:
        stappen.append("roep de Skill-tool aan voor: %s (elk een eigen aanroep), en noem het projecttype" % ", ".join("`%s`" % s for s in mist))
    if root and not profiel and not intake:
        stappen.append(
            "het bouwproject %s heeft geen profiel: doe de intake (dicht/references/intake.md), schrijf %s/.dicht/profiel.json en controleer het met "
            "`python3 ~/.claude/skills/dicht/tools/regels_voor_wijziging.py --pad %s --controleer-profiel`; staat het profiel in een andere "
            "branch, haal het dan op met `git checkout <branch> -- .dicht/profiel.json`" % (root, root, root))
    if not stappen:
        return None
    return ("%s is code en mag pas geschreven worden als de skill `dicht` en de sub-skills voor dit bestand zijn geladen en het project een "
            "profiel heeft (besluit van Marketing Maatwerk, 05-10-2026: bij alles wat we bouwen). Doe nu: %s. Herhaal daarna deze bewerking. "
            "Vrij zijn alleen tekst en gegevens (.md, .txt, .csv), de scratchmap, /tmp, ~/docs en de geheugenmap. Een uitzondering "
            "geeft alleen Marketing Maatwerk (VRAAG AAN MARKETING MAATWERK); maak er zelf geen." % (pad, "; ".join("(%d) %s" % (i, s) for i, s in enumerate(stappen, 1))))


# --- waar de sessie code schreef (Stop-hook, besluit van Marketing Maatwerk 17-10-2026) ---------
SCHRIJF_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")


def geschreven_projecten(transcript, doelen_bash):
    """De projecten met `.dicht/` waarin de sessie code schreef, uit het sessielog en de logs van haar subagents:
    Write, Edit, MultiEdit en NotebookEdit, en een zichtbare schrijfactie in Bash (`doelen_bash` uit pretool_verplicht.py,
    met dezelfde blinde vlekken: een script, een variabele, `patch`). Een vrij bestand (tekst, ~/docs, /tmp) en alles in
    `bewijs/` van het project telt niet; een aanroep die werd geweigerd telt wel mee; een afwijkende logregel wordt overgeslagen. Bij Bash, net als in die hook, alleen een bestand dat altijd code is,
    en na een `cd` alleen een absoluut doel (waar een relatief doel dan staat, is uit de tekst niet te zien)."""
    import json
    logs = [Path(transcript)] + sorted(Path(transcript).with_suffix("").glob("subagents/*.jsonl"))
    roots, gezien = set(), {}
    cd = re.compile(r"(?:^|[\s;&|(])(?:cd|pushd)(?:\s|$)")
    for log in logs:
        with open(log, "rb") as f:
            for regel in f:
                if b'"tool_use"' not in regel:
                    continue
                try:
                    d = json.loads(regel)
                except ValueError:
                    continue
                bericht = d.get("message") if isinstance(d, dict) else None
                if not isinstance(bericht, dict) or bericht.get("role") != "assistant" or not isinstance(bericht.get("content"), list):
                    continue
                cwd = str(d.get("cwd") or "/")
                for b in bericht["content"]:
                    if not isinstance(b, dict) or b.get("type") != "tool_use" or not isinstance(b.get("input"), dict):
                        continue
                    inp = b["input"]
                    if b.get("name") in SCHRIJF_TOOLS:
                        paden, telt = [inp.get("file_path") or inp.get("notebook_path")], ("code", "project")
                    elif b.get("name") == "Bash":
                        cmd = str(inp.get("command", ""))
                        paden = [p for p in doelen_bash(cmd, cwd) if os.path.isabs(os.path.expanduser(p)) or not cd.search(cmd)]
                        telt = ("code",)
                    else:
                        continue
                    for p in paden:
                        p = os.path.join(cwd, os.path.expanduser(str(p))) if p else None
                        if p and soort_bestand(p) in telt:
                            map_ = os.path.dirname(p)
                            if map_ not in gezien:
                                gezien[map_] = vind_project(map_)
                            root = gezien[map_]
                            if root and not os.path.realpath(p).startswith(os.path.realpath(root / "bewijs") + "/"):
                                roots.add(root)
    return roots


# --- hooklog -------------------------------------------------------------------
def log_hook(tekst):
    """Eén regel in `~/.claude/dicht-hooks.log` (modus 600) voor wat een hook niet kon controleren.
    Lukt het schrijven niet, dan gebeurt er niets: het log mag een hook nooit laten falen."""
    try:
        fd = os.open(str(THUIS / ".claude" / "dicht-hooks.log"), os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        with os.fdopen(fd, "a", encoding="utf-8") as f:
            f.write("%s\t%s\n" % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), " ".join(tekst.split())[:300]))
    except OSError:
        pass


# --- noodrem -----------------------------------------------------------------
OVERRULE_BESTAND = "overrules.log"


def schrijf_overrule(root, sessie, reden):
    regel = "%s\t%s\t%s\n" % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                              sessie, maskeer(" ".join(reden.split()))[:500])
    with open(root / ".dicht" / OVERRULE_BESTAND, "a", encoding="utf-8") as f:
        f.write(regel)


def overrule_van(root, sessie):
    f = root / ".dicht" / OVERRULE_BESTAND
    if not f.is_file():
        return None
    for regel in reversed(f.read_text(encoding="utf-8", errors="replace").splitlines()):
        delen = regel.split("\t")
        if len(delen) == 3 and delen[1] == sessie:
            return delen[2]
    return None
