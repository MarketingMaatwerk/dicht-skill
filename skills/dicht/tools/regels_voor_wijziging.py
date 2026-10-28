#!/usr/bin/env python3
"""Kiest de regels die een wijziging raakt (besluit 27, het kleine-wijziging-pad).

Leest de gewijzigde bestanden uit git, het profiel `.dicht/profiel.json`, `regel-index.tsv` en
`wijziging-patronen.tsv`. Alleen de standaardbibliotheek. Leest alleen; schrijft niets, behalve met `--bewijs`.

  regels_voor_wijziging.py [--pad MAP] [--basis REF]      de werkmap tegenover de basis
  regels_voor_wijziging.py --bewijs [--pad MAP]           schrijft daarbij het voorgevulde bewijsbestand in bewijs/
  regels_voor_wijziging.py --commit HASH [--pad MAP]      één bestaande commit
  regels_voor_wijziging.py --bestanden a b c              een lijst (omvang en inhoud niet gemeten: nooit klein)
  regels_voor_wijziging.py --volledig                     het volledige pad van het profiel
  regels_voor_wijziging.py --controleer-profiel           toetst het profiel en toont wat eruit volgt

Overal: --profiel BESTAND (standaard <MAP>/.dicht/profiel.json) en --json.
De uitleg staat in `dicht/references/kleine-wijziging.md` en `dicht/references/intake.md`.
"""
import argparse
import csv
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
TYPES = ("website", "wp-plugin", "wp-thema", "api", "app", "mcp", "klantproject")
GEVOELIGHEID = ("persoonsgegevens", "betalingen", "zorgdata")
SOORTEN = ("kern", "licht", "pad", "rest", "inhoud", "profiel", "voorkant")
# Sinds 22-10-2026 (besluit van Marketing Maatwerk) leidt het profiel van een website, wp-thema of klantproject ook dicht-anti-vibe af. Een profiel
# van daarvoor noemt hem niet en blijft geldig; de hook vraagt hem dan via de projecttypes (dicht_lib.subskills_voor).
LATER_ERBIJ = "dicht-anti-vibe"
JA_NEE = ("bereikbaar_van_buiten", "ai_of_mcp", "scripts", "mail")
VELDEN = ("versie", "project", "datum", "door", "stand", "types", "gevoeligheid", "tenants", *JA_NEE, "subskills", "nvt", "paden")
# Vaste waarden van een kleine wijziging (besluit van Marketing Maatwerk, 04-10-2026; zie vaste-waarden.md): hooguit 5 bestanden en
# 50 gewijzigde regels (lichte bestanden tellen niet mee), en 12 kernregels die bij elke wijziging gelden.
KLEIN_MAX_BESTANDEN, KLEIN_MAX_REGELS, KERNREGELS = 5, 50, 12
MAX_TEKST = 200_000
# Tekst tussen aanhalingstekens en commentaar: een trefwoord dat alleen daar staat, haalt het thema erbij
# maar maakt de wijziging niet gewoon (een gewijzigde zin in een mail is geen nieuwe betaalstroom).
_PROZA = re.compile(r"""'(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*"|`[^`\n]*`|(?://|\#|--\s)[^\n]*""")
SOORT_REDEN = ("kernregel", "thema", "regel zelf", "kritiek in geraakt domein", "kritiek in het profiel", "volledig pad")


class Fout(Exception):
    pass


def _vind(naam, omgeving):
    for k in (os.environ.get(omgeving), HIER.parent / naam, HIER / naam, Path.home() / ".claude/skills/dicht" / naam):
        if k and Path(k).is_file():
            return Path(k)
    raise Fout("%s niet gevonden (zet %s)" % (naam, omgeving))


def types_van(geldt):
    g = geldt.lower()
    if "alles" in g:
        return set(TYPES)
    return {t for t in TYPES if re.search(r"(?<![a-z-])" + t + r"(?![a-z-])", g)}


def lees_index(pad=None):
    """De actieve regels, met domein (prefix van het ID), thema (begin van de naam van de referentie) en sub-skill."""
    regels = []
    with open(pad or _vind("regel-index.tsv", "DICHT_INDEX"), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            if r["status"] == "actief":
                regels.append({"id": r["id"], "titel": r["titel"], "ernst": r["ernst"], "hard": r["type"].startswith("hard"),
                               "types": types_van(r["geldt_voor"]), "domein": r["id"].split("-")[0],
                               "thema": re.match(r"[a-z]+-[a-z0-9]+", Path(r["referentie"]).name)[0],
                               "subskill": r["referentie"].split("/")[0], "referentie": r["referentie"]})
    return regels


def lees_patronen(pad=None):
    pat = {s: [] for s in SOORTEN}
    with open(pad or HIER / "wijziging-patronen.tsv", encoding="utf-8") as f:
        for nr, r in enumerate(csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE), 2):
            try:
                r["doelen"] = [d for d in r["doelen"].split(",") if d != "-"]
                if r["soort"] in ("licht", "pad", "rest", "inhoud", "voorkant"):
                    r["re"] = re.compile(r["patroon"], re.I)
                pat[r["soort"]].append(r)
            except (re.error, KeyError, AttributeError) as fout:
                raise Fout("wijziging-patronen.tsv rij %d is ongeldig (%s)" % (nr, type(fout).__name__))
    return pat


def doelen_in(index):
    """Waar een patroon naar mag wijzen: een domein (WEB), een thema (web-1) of een regel (WEB-11)."""
    return {x for r in index for x in (r["domein"], r["thema"], r["id"])}


# --- profiel -------------------------------------------------------------------
def antwoord(profiel, vraag):
    if vraag in GEVOELIGHEID:
        return "ja" if vraag in profiel["gevoeligheid"] else "nee"
    return {True: "ja", False: "nee"}.get(profiel[vraag], profiel[vraag])


def afgeleid_nvt(profiel, pat):
    """Wat de antwoorden van de intake op nvt zetten: {domein of thema: reden}."""
    nvt = {}
    for r in pat["profiel"]:
        vraag, waarde = r["patroon"].split("=")
        if antwoord(profiel, vraag) == waarde:
            nvt.update({d: r["toelichting"] for d in r["doelen"]})
    return nvt


def nvt_reden(regel, nvt):
    return nvt.get(regel["thema"]) or nvt.get(regel["domein"])


def afgeleide_subskills(profiel, index, nvt):
    return sorted({r["subskill"] for r in index if r["types"] & set(profiel["types"]) and not nvt_reden(r, nvt)})


def controleer_profiel(p, index, pat):
    """Geeft de fouten in een profiel; een lege lijst betekent geldig."""
    if not isinstance(p, dict):
        return ["het profiel is geen JSON-object"]
    fouten = ["veld %s ontbreekt" % v for v in VELDEN[:-1] if v not in p] + ["onbekend veld %s" % v for v in p if v not in VELDEN]
    if fouten:
        return fouten
    doelen = doelen_in(index)
    tekst = lambda v: isinstance(v, str) and v.strip()
    if p["versie"] != 1:
        fouten.append("versie moet 1 zijn")
    fouten += ["%s is leeg" % v for v in ("project", "door") if not tekst(p[v])]
    if not (tekst(p["datum"]) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p["datum"])):
        fouten.append("datum moet jjjj-mm-dd zijn")
    if p["stand"] not in ("nieuw", "bestaand"):
        fouten.append("stand moet nieuw of bestaand zijn")
    if not (isinstance(p["types"], list) and p["types"] and set(p["types"]) <= set(TYPES)):
        fouten.append("types moet een lijst zijn uit: " + ", ".join(TYPES))
    g = p["gevoeligheid"]
    if not (isinstance(g, list) and g and set(g) <= {*GEVOELIGHEID, "geen"} and (g == ["geen"] or "geen" not in g)):
        fouten.append("gevoeligheid moet een lijst zijn uit persoonsgegevens, betalingen, zorgdata, of alleen geen")
    if p["tenants"] not in ("een", "meerdere"):
        fouten.append("tenants moet een of meerdere zijn")
    fouten += ["%s moet true of false zijn" % v for v in JA_NEE if not isinstance(p[v], bool)]
    if not (isinstance(p["nvt"], dict) and all(tekst(v) for v in p["nvt"].values())):
        fouten.append("nvt moet per domein of thema een reden geven")
    paden = p.get("paden", {})
    if not (isinstance(paden, dict) and all(isinstance(v, list) and v for v in paden.values())):
        fouten.append("paden moet per patroon een lijst van domeinen of thema's geven")
    if fouten:
        return fouten
    fouten += ["nvt noemt %s; dat domein of thema bestaat niet" % d for d in p["nvt"] if d not in doelen]
    for patroon, lijst in paden.items():
        try:
            re.compile(patroon)
        except re.error:
            fouten.append("paden: %s is geen geldig patroon" % patroon)
        fouten += ["paden noemt %s; dat domein of thema bestaat niet" % d for d in lijst if d not in doelen]
    moet = afgeleid_nvt(p, pat)
    fouten += ["nvt mist %s (volgt uit de antwoorden: %s)" % (d, r) for d, r in moet.items() if d not in p["nvt"]]
    afgeleid = afgeleide_subskills(p, index, p["nvt"]) if not fouten else []
    if not fouten and p["subskills"] not in (afgeleid, [s for s in afgeleid if s != LATER_ERBIJ]):
        fouten.append("subskills moet zijn: " + json.dumps(afgeleid))
    return fouten


def lees_profiel(pad, index, pat):
    try:
        p = json.loads(Path(pad).read_text(encoding="utf-8"))
    except (OSError, ValueError) as f:
        raise Fout("profiel %s niet te lezen (%s)" % (pad, type(f).__name__))
    fouten = controleer_profiel(p, index, pat)
    if fouten:
        raise Fout("profiel ongeldig: " + "; ".join(fouten))
    return p


# --- de wijziging uit git ------------------------------------------------------
def git(root, *args, mag_falen=False):
    r = subprocess.run(["git", "-c", "core.quotepath=off", "-C", str(root), *args], capture_output=True, text=True,
                       errors="replace", timeout=30)
    if r.returncode and not mag_falen:
        raise Fout("git %s mislukt: %s" % (args[0], r.stderr.strip()[:200]))
    return r.stdout if not r.returncode else None


def controleer_plek(root):
    """`.dicht/` staat in de repo-root, met één profiel per repo (besluit van Marketing Maatwerk, 04-10-2026). Buiten git: geen controle.
    De repo van de thuismap is een verzamelmap en geen project: daar staat het profiel in de map van het project (05-10-2026)."""
    top = git(root, "rev-parse", "--show-toplevel", mag_falen=True)
    gedeeld = git(root, "rev-parse", "--path-format=absolute", "--git-common-dir", mag_falen=True)
    if gedeeld and Path(gedeeld.strip()).resolve().parent == Path(os.environ.get("DICHT_THUIS") or Path.home()).resolve():
        return
    if top and Path(top.strip()).resolve() != Path(root).resolve():
        raise Fout("`.dicht/` staat in %s, maar hoort in de repo-root %s: één profiel per repo" % (Path(root).resolve(), top.strip()))


def bepaal_basis(root, opgegeven=None):
    """De commit waartegen de wijziging wordt gemeten: het punt waar de branch van main of master aftakte,
    anders HEAD (alleen de werkmap). Een opgegeven basis mag de wijziging alleen ruimer maken."""
    standaard = git(root, "rev-parse", "HEAD").strip()
    for tak in ("main", "master"):
        mb = git(root, "merge-base", "HEAD", tak, mag_falen=True)
        if mb:
            standaard = mb.strip()
            break
    if not opgegeven:
        return standaard
    basis = git(root, "rev-parse", "--verify", opgegeven + "^{commit}").strip()
    if git(root, "merge-base", "--is-ancestor", basis, standaard, mag_falen=True) is None:
        raise Fout("basis %s is geen voorouder van %s; een basis mag de wijziging alleen ruimer maken" % (opgegeven, standaard[:7]))
    return basis


def lees_wijziging(root, basis=None, commit=None):
    """Geeft per gewijzigd bestand het pad, de aantallen en de tekst van de toegevoegde en verwijderde regels."""
    opdracht = ("show", "--format=", commit) if commit else ("diff", basis)
    aantallen = git(root, *opdracht, "--relative", "--no-renames", "--numstat")
    bestanden = {}
    for regel in aantallen.splitlines():
        plus, minus, pad = regel.split("\t", 2)
        bestanden[pad] = {"pad": pad, "plus": int(plus) if plus.isdigit() else 0, "min": int(minus) if minus.isdigit() else 0, "tekst": []}
    huidig, kop = None, False
    for regel in git(root, *opdracht, "--relative", "--no-renames", "-U0").splitlines():
        if regel.startswith("diff --git "):
            huidig, kop = None, True
        elif regel.startswith("@@"):
            kop = False
        elif kop and regel[:4] in ("--- ", "+++ "):
            if regel[4:] != "/dev/null":
                huidig = bestanden.get(regel[6:])
        elif not kop and huidig and regel[:1] in "+-":
            huidig["tekst"].append(regel[1:])
    if not commit:
        for pad in git(root, "ls-files", "--others", "--exclude-standard").splitlines():
            try:
                tekst = (Path(root) / pad).read_text(encoding="utf-8", errors="replace")[:MAX_TEKST + 1]
            except OSError:
                tekst = ""
            bestanden[pad] = {"pad": pad, "plus": tekst.count("\n"), "min": 0, "tekst": [tekst]}
    if not bestanden:
        raise Fout("geen gewijzigde bestanden tegenover %s; geef een basis op" % (commit or basis)[:12])
    for b in bestanden.values():
        tekst = "\n".join(b["tekst"])
        b["tekst"], b["afgekapt"] = tekst[:MAX_TEKST], len(tekst) > MAX_TEKST
    return list(bestanden.values())


# --- de keuze ------------------------------------------------------------------
def kies(bestanden, profiel, index, pat, gemeten=True, volledig=False):
    """Kiest de regels voor deze bestanden. Geeft pad (klein, gewoon of volledig), regels met reden en meldingen."""
    types, nvt = set(profiel["types"]), profiel["nvt"]
    kern = {d for r in pat["kern"] for d in r["doelen"]}
    domein_van = {r["thema"]: r["domein"] for r in index}
    eigen = [{"soort": "pad", "re": re.compile(k, re.I), "doelen": v, "klasse": "klein", "toelichting": "eigen pad uit het profiel"}
             for k, v in profiel.get("paden", {}).items()]
    geraakt, meldingen, zwaar, overzicht, aantal, regels_gewijzigd, onbekend = {}, [], [], [], 0, 0, []
    _nvt = lambda d: nvt.get(d) or nvt.get(domein_van.get(d, d.split("-")[0]))
    for b in bestanden:
        licht = [p for p in pat["licht"] if p["re"].search(b["pad"])]
        rijen = licht or [p for p in eigen if p["re"].search(b["pad"])] or [p for p in pat["pad"] if p["re"].search(b["pad"])] \
            or [p for p in pat["rest"] if p["re"].search(b["pad"])]
        treffers = [(p, p["toelichting"]) for p in rijen]
        # een voorkantbestand haalt de oplevercontrole erbij, ook als het licht is (stijl); alleen voor de types van die regels
        # zonder de thema's die het profiel op nvt zet (een site zonder WordPress: vibe-f), anders wordt elke stijlwijziging "gewoon"
        treffers += [(dict(p, doelen=[d for d in p["doelen"] if not _nvt(d)]), p["toelichting"]) for p in pat["voorkant"] if p["re"].search(b["pad"])]
        if not rijen:
            meldingen.append("%s past op geen patroon: alleen de kernregels, en de wijziging telt niet als klein. "
                             "Voeg een patroon toe aan wijziging-patronen.tsv of aan paden in het profiel." % b["pad"])
            zwaar.append("%s past op geen patroon" % b["pad"])
            onbekend.append("%s past op geen patroon" % b["pad"])
        if b.get("afgekapt"):
            onbekend.append("%s is te groot om helemaal te lezen" % b["pad"])
        if not licht:
            aantal, regels_gewijzigd = aantal + 1, regels_gewijzigd + b["plus"] + b["min"]
            for p in pat["inhoud"] if b["tekst"] else []:
                m = p["re"].search(b["tekst"])
                if m:
                    in_code = p["re"].search(_PROZA.sub(" ", b["tekst"]))
                    # alleen in tekst of commentaar: het thema komt mee, maar het maakt de wijziging niet gewoon
                    # en het spreekt het profiel niet tegen
                    doelen = p["doelen"] if in_code else [d for d in p["doelen"] if not _nvt(d)]
                    treffers.append((dict(p, doelen=doelen, klasse=p["klasse"] if in_code else "klein"), "trefwoord `%s`%s, %s" % (
                        " ".join(m.group(0).split())[:40], "" if in_code else " alleen in tekst of commentaar", p["toelichting"])))
        for p, wat in treffers:
            if p["klasse"] == "gewoon":
                zwaar.append("%s: %s" % (b["pad"], wat))
            for d in p["doelen"]:
                geraakt.setdefault(d, []).append("%s (%s)" % (b["pad"], wat))
        overzicht.append({"pad": b["pad"], "plus": b["plus"], "min": b["min"], "licht": bool(licht), "treffers": [w for _, w in treffers]})
    if not gemeten:
        zwaar.append("omvang en inhoud zijn niet gemeten (lijst van bestanden)")
        onbekend.append("omvang en inhoud zijn niet gemeten (lijst van bestanden)")
    elif aantal > KLEIN_MAX_BESTANDEN or regels_gewijzigd > KLEIN_MAX_REGELS:
        zwaar.append("omvang: %d bestanden en %d gewijzigde regels (grens: %d en %d)" % (aantal, regels_gewijzigd, KLEIN_MAX_BESTANDEN, KLEIN_MAX_REGELS))
    for d in sorted(geraakt):
        reden = _nvt(d)
        if reden:
            meldingen.append("de wijziging raakt %s, dat volgens het profiel niet geldt (%s). Werk de intake bij; de regels komen nu mee." % (d, reden))
            zwaar.append("raakt %s tegen het profiel in" % d)
    pad = "volledig" if volledig else "gewoon" if zwaar else "klein"
    domeinen = {domein_van.get(d, d.split("-")[0]) for d in geraakt}
    gekozen = {}

    def neem(r, reden):
        gekozen.setdefault(r["id"], dict(r, types=sorted(r["types"]), redenen=[]))["redenen"].append(reden)

    geldig = [r for r in index if r["types"] & types]
    for r in geldig:
        stil = nvt_reden(r, nvt)
        if volledig:
            if not stil:
                neem(r, "volledig pad")
            continue
        if r["id"] in kern:
            neem(r, "kernregel")
        if r["thema"] in geraakt:
            neem(r, "thema %s: %s" % (r["thema"], geraakt[r["thema"]][0]) + (" en %d meer" % (len(geraakt[r["thema"]]) - 1) if len(geraakt[r["thema"]]) > 1 else ""))
        if r["id"] in geraakt:
            neem(r, "regel zelf: %s" % geraakt[r["id"]][0])
        if r["ernst"] == "kritiek" and r["domein"] in domeinen and (r["domein"] in geraakt or not stil):
            neem(r, "kritiek in geraakt domein %s" % r["domein"])
        elif r["ernst"] == "kritiek" and pad == "gewoon" and not stil:
            neem(r, "kritiek in het profiel")
    regels = list(gekozen.values())
    return {"pad": pad, "waarom_niet_klein": zwaar, "bestanden": overzicht, "omvang": {"bestanden": aantal, "regels": regels_gewijzigd},
            "meldingen": meldingen, "onbekend": onbekend, "regels": regels,
            "telling": {"hard": sum(r["hard"] for r in regels), "richtlijn": sum(not r["hard"] for r in regels),
                        "volledig_hard": sum(r["hard"] for r in geldig), "volledig": len(geldig),
                        "volledig_hard_na_profiel": sum(r["hard"] and not nvt_reden(r, nvt) for r in geldig),
                        "hard_per_reden": {s: n for s in SOORT_REDEN if (n := sum(r["hard"] and r["redenen"][0].startswith(s) for r in regels))}},
            "niet_gekozen_hard": {d: n for d in dict.fromkeys(r["domein"] for r in geldig)
                                  if (n := sum(r["hard"] and r["domein"] == d and r["id"] not in gekozen for r in geldig))}}


def toon(k, kop):
    t = k["telling"]
    uit = ["pad: %s (%s; %d bestanden en %d regels tellen mee voor de omvang)" % (k["pad"], kop, k["omvang"]["bestanden"], k["omvang"]["regels"])]
    uit += ["niet klein omdat: " + z for z in k["waarom_niet_klein"]]
    uit += ["melding: " + m for m in k["meldingen"]]
    uit.append("bestanden:")
    uit += ["  %s +%d -%d%s: %s" % (b["pad"], b["plus"], b["min"], " (licht)" if b["licht"] else "", "; ".join(b["treffers"]) or "geen patroon") for b in k["bestanden"]]
    uit.append("regels: %d hard en %d richtlijn; het volledige pad heeft %d hard (%d na het profiel) en %d in totaal"
               % (t["hard"], t["richtlijn"], t["volledig_hard"], t["volledig_hard_na_profiel"], t["volledig"]))
    uit.append("waarvan hard: " + ", ".join("%s %d" % sn for sn in t["hard_per_reden"].items()))
    uit += ["  %s %s %s %s [%s]" % (r["id"], r["ernst"], "hard" if r["hard"] else "richtlijn", r["titel"], "; ".join(r["redenen"])) for r in k["regels"]]
    uit.append("niet gekozen, want niet geraakt door deze wijziging (hard, per domein): "
               + (", ".join("%s %d" % dn for dn in k["niet_gekozen_hard"].items()) or "geen"))
    return "\n".join(uit)


NIET_GERAAKT = "kritiek in het profiel"


def voorgevuld(k, profiel, basis, commit, nu):
    """De tekst van het voorgevulde bewijsbestand (besluit van Marketing Maatwerk, 04-10-2026). Een regel die de wijziging niet raakt
    (gekozen als kritiek in het profiel: geen bestand of trefwoord wijst naar zijn domein) krijgt `nvt` met die reden;
    elke andere regel blijft leeg. Kon het hulpmiddel iets niet meten, dan blijft alles leeg: onbekend is nooit afgevinkt."""
    def rij(r):
        if not k["onbekend"] and all(x.startswith(NIET_GERAAKT) for x in r["redenen"]):
            return "| %s | nvt | de wijziging raakt domein %s niet: geen gewijzigd bestand of trefwoord wijst ernaar (voorgevuld, gemeten tegenover %s) |" % (r["id"], r["domein"], basis[:7])
        return "| %s |  |  |" % r["id"]

    hard, richtlijn = [r for r in k["regels"] if r["hard"]], [r for r in k["regels"] if not r["hard"]]
    rijen = [rij(r) for r in hard]
    uit = ["---", "project: " + profiel["project"], "type: " + ", ".join(profiel["types"]), "commit: " + commit, "datum: " + nu,
           "door: ", "akkoord: ", "runtime: ", "hulpmiddelen: ", "gate: ", "uitzonderingen: ", "pad: " + k["pad"], "basis: " + basis[:12], "---", "",
           "Voorgevuld door `tools/regels_voor_wijziging.py --bewijs`. Vul bij elke lege regel status en bewijs in; een lege regel is niet afgevinkt.",
           "Een voorgevulde `nvt` is een meting op paden en trefwoorden: weet je dat de wijziging de regel toch raakt, vervang hem dan door het bewijs.", ""]
    uit += ["Niets is voorgevuld, want niet alles is gemeten: " + "; ".join(k["onbekend"]) + ".", ""] if k["onbekend"] else []
    uit += ["## Harde regels (%d, waarvan %d voorgevuld als nvt)" % (len(hard), sum(" | nvt | " in x for x in rijen)), "", "| Regel | Status | Bewijs |", "|---|---|---|"] + rijen
    if richtlijn:
        uit += ["", "## Richtlijnen (%d)" % len(richtlijn), "", "| Regel | Status | Bewijs |", "|---|---|---|"] + [rij(r) for r in richtlijn]
    uit += ["", "## Waarom gekozen", ""] + ["- %s %s (%s): %s" % (r["id"], r["titel"], r["ernst"], "; ".join(r["redenen"])) for r in k["regels"]]
    return "\n".join(uit) + "\n", len(hard), sum(" | nvt | " in x for x in rijen)


def schrijf_bewijs(root, k, profiel, basis):
    """Schrijft bewijs/<datum>-<korte hash>.md in de projectmap; een bestaand bestand wordt nooit overschreven."""
    nu = datetime.datetime.now(datetime.timezone.utc)
    commit = git(root, "rev-parse", "--short", "HEAD").strip()
    tekst, hard, nvt = voorgevuld(k, profiel, basis, commit, nu.strftime("%Y-%m-%dT%H:%M:%SZ"))
    map_ = Path(root) / "bewijs"
    map_.mkdir(exist_ok=True)
    for n in range(1, 100):
        doel = map_ / ("%s-%s%s.md" % (nu.strftime("%Y-%m-%d"), commit, "" if n == 1 else "-%d" % n))
        try:
            with open(doel, "x", encoding="utf-8") as f:
                f.write(tekst)
            return doel, hard, nvt
        except FileExistsError:
            continue
    raise Fout("te veel bewijsbestanden voor %s" % commit)


def main():
    a = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    a.add_argument("--pad", default=".")
    a.add_argument("--profiel")
    a.add_argument("--basis")
    a.add_argument("--commit")
    a.add_argument("--bestanden", nargs="+")
    a.add_argument("--volledig", action="store_true")
    a.add_argument("--controleer-profiel", action="store_true")
    a.add_argument("--bewijs", action="store_true")
    a.add_argument("--json", action="store_true")
    o = a.parse_args()
    try:
        index, pat = lees_index(), lees_patronen()
        profiel = lees_profiel(o.profiel or Path(o.pad) / ".dicht" / "profiel.json", index, pat)
        if not o.profiel:
            controleer_plek(o.pad)
        if o.controleer_profiel:
            print("profiel geldig: types %s; sub-skills %s; nvt %s" % (", ".join(profiel["types"]), ", ".join(profiel["subskills"]),
                                                                    ", ".join(profiel["nvt"]) or "niets"))
            return 0
        basis = None
        if o.bestanden:
            bestanden, kop = [{"pad": b, "plus": 0, "min": 0, "tekst": ""} for b in o.bestanden], "lijst van bestanden"
        elif o.volledig or profiel["stand"] == "nieuw":
            bestanden, kop = [], "nieuw project of oplevering"
        elif o.commit:
            bestanden, kop = lees_wijziging(o.pad, commit=o.commit), "commit " + o.commit
        else:
            basis = bepaal_basis(o.pad, o.basis)
            bestanden, kop = lees_wijziging(o.pad, basis), "basis " + basis[:7]
        k = kies(bestanden, profiel, index, pat, gemeten=not o.bestanden, volledig=o.volledig or profiel["stand"] == "nieuw")
        if o.bewijs:
            if not basis:
                raise Fout("--bewijs is voor een wijziging aan een bestaand project (de werkmap tegenover de basis), niet voor --commit, "
                           "--bestanden, --volledig of een nieuw project; het bewijs van het volledige pad schrijft /dicht-audit")
            doel, hard, nvt = schrijf_bewijs(o.pad, k, profiel, basis)
            print("bewijsbestand: %s (%d harde regels: %d voorgevuld als nvt, %d leeg)" % (doel, hard, nvt, hard - nvt), file=sys.stderr)
    except Fout as f:
        print("fout: %s" % f, file=sys.stderr)
        return 2
    print(json.dumps(k, ensure_ascii=False, indent=1) if o.json else toon(k, kop))
    return 0


if __name__ == "__main__":
    sys.exit(main())
