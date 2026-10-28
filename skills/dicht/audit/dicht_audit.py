#!/usr/bin/env python3
"""Auditscript van de skill "dicht" (ARCH-84, ARCH-85, ARCH-86).

  dicht_audit.py <type> [--pad MAP] [--url URL] [--domein DOMEIN] [--server]
                        [--wp MAP | --wp-ssh gebruiker@host:/pad] [--uit MAP] [--geen-bewijs]

Verzamelt per projecttype het bewijs dat met een opdracht te meten is en schrijft
`bewijs/<datum>-<hash>.md` (kolommen Regel, Status, Bewijs) en `audit.json` ernaast.

Alleen lezen: het script wijzigt niets aan het project, de server of de site; het enige
wat het schrijft zijn de twee uitvoerbestanden. Begrensd: een time-out per opdracht, een
pauze tussen aanvragen en een maximum per host. Geen actieve payloads. Uitvoer gemaskeerd.

Uitkomst per controle: PASS, FAIL, ONBEKEND of NVT. ONBEKEND is nooit PASS. Een controle
die maar een deel van het bewijs van een regel dekt, levert in het bewijsbestand
`niet gemeten` met de rest als handmatige vraag, nooit `voldaan`.
Exitcode: 0 geen FAIL op een harde regel, 1 minstens één, 2 eigen fout.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER.parent / "hooks"))
import dicht_lib as lib  # noqa: E402

PASS, FAIL, ONBEKEND, NVT = "PASS", "FAIL", "ONBEKEND", "NVT"
MAX_AANVRAGEN = 40      # per host, per run
PAUZE = 0.5             # seconden tussen aanvragen
MAX_UITVOER = 300       # tekens bewijs per controle

GROEPEN = {
    "website": ["repo", "web", "dns", "wpsite"],
    "wp-plugin": ["repo", "wpcode"],
    "wp-thema": ["repo", "wpcode"],
    "api": ["repo", "server", "web", "dns", "api"],
    "app": ["repo", "server", "web", "dns", "api"],
    "mcp": ["repo", "server", "mcp", "web"],
    "klantproject": ["repo", "web", "dns", "wpsite", "wpcode"],
}
CONTROLES = []


def controle(regels, groep, domein, titel, dekking="deel", rest=""):
    """Registreert een controle. `regels` is één ID of een lijst; de functie geeft
    (status, uitvoer) of bij meer regels {regel: (status, uitvoer)}.
    `dekking` is "volledig" als de controle het hele veld Bewijs van de regel dekt;
    anders staat in `rest` wat met de hand nog moet."""
    def wikkel(f):
        CONTROLES.append({"regels": [regels] if isinstance(regels, str) else list(regels), "groep": groep,
                          "domein": domein, "titel": titel, "dekking": dekking, "rest": rest, "f": f})
        return f
    return wikkel


class Ctx:
    def __init__(self, a):
        self.type = a.type
        self.pad = Path(a.pad).resolve() if a.pad else None
        self.url = a.url.rstrip("/") if a.url else None
        self.host = urlparse(self.url).hostname if self.url else None
        self.domein = a.domein or (self.host[4:] if self.host and self.host.startswith("www.") else self.host)
        self.server = a.server
        self.wp, self.wp_ssh = a.wp, a.wp_ssh
        self.aanvragen = 0
        self.cache = {}

    def run(self, args, timeout=20, cwd=None, invoer=None):
        """Draait een opdracht als lijst, zonder shell. Geeft (exitcode, uitvoer); exitcode None als het niet kon."""
        if not shutil.which(args[0]):
            return None, "%s niet beschikbaar" % args[0]
        try:
            r = subprocess.run(args, capture_output=True, text=True, errors="replace", timeout=timeout,
                               cwd=str(cwd) if cwd else None, input=invoer, stdin=None if invoer else subprocess.DEVNULL)
            return r.returncode, (r.stdout + r.stderr).strip()
        except subprocess.TimeoutExpired:
            return None, "time-out na %ds" % timeout
        except OSError as fout:
            return None, type(fout).__name__

    def http(self, url, methode="GET"):
        """Eén anonieme aanvraag met curl. Geeft (status, kopregels als dict met lijsten, body) of (None, {}, reden)."""
        sleutel = (methode, url)
        if sleutel in self.cache:
            return self.cache[sleutel]
        if self.aanvragen >= MAX_AANVRAGEN:
            return None, {}, "maximum van %d aanvragen bereikt" % MAX_AANVRAGEN
        if self.aanvragen:
            time.sleep(PAUZE)
        self.aanvragen += 1
        code, uit = self.run(["curl", "-s", "-i", "--max-time", "15", "--max-filesize", "2000000", "--proto", "=http,https",
                              "-A", "dicht-audit (alleen lezen)", "-X", methode, "--", url], timeout=25)
        if code != 0:
            res = (None, {}, "curl exit %s" % code)
        else:
            kop, _, body = uit.replace("\r\n", "\n").partition("\n\n")
            regels = kop.split("\n")
            koppen = {}
            for r in regels[1:]:
                naam, _, waarde = r.partition(":")
                koppen.setdefault(naam.strip().lower(), []).append(waarde.strip())
            delen = regels[0].split()
            res = (int(delen[1]) if len(delen) > 1 and delen[1].isdigit() else None, koppen, body)
        self.cache[sleutel] = res
        return res

    def bestanden(self):
        """Gevolgde bestanden (git ls-files), of anders de bestanden in de map, begrensd."""
        if "bestanden" not in self.cache:
            code, uit = self.run(["git", "ls-files"], cwd=self.pad) if self.pad else (None, "")
            if code == 0:
                self.cache["git"] = True
                lijst = uit.splitlines()
            else:
                self.cache["git"] = False
                lijst = []
                for d, mappen, fs in os.walk(self.pad or "."):
                    mappen[:] = [m for m in mappen if m not in (".git", "node_modules", "vendor")]
                    lijst += [os.path.relpath(os.path.join(d, f), self.pad) for f in fs]
                    if len(lijst) > 5000:
                        break
            self.cache["bestanden"] = lijst[:5000]
        return self.cache["bestanden"]

    def is_git(self):
        self.bestanden()
        return self.cache["git"]

    def lees(self, rel, maximum=1_000_000):
        p = self.pad / rel
        try:
            if p.is_file() and not p.is_symlink() and p.stat().st_size <= maximum:
                return p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
        return None


def kort(tekst):
    tekst = lib.maskeer(" ".join(str(tekst).split())).replace("|", "/")
    return tekst if len(tekst) <= MAX_UITVOER else tekst[:MAX_UITVOER] + " [...]"


def draai(ctx, checklist_ids):
    """Draait de controles van het projecttype. Geeft een lijst van resultaten."""
    uit = []
    voorwaarde = {"repo": ctx.pad, "wpcode": ctx.pad, "mcp": ctx.pad, "web": ctx.url, "api": ctx.url, "dns": ctx.domein,
                  "server": ctx.server, "wpsite": ctx.url or ctx.wp or ctx.wp_ssh}
    optie = {"repo": "--pad", "wpcode": "--pad", "mcp": "--pad", "web": "--url", "api": "--url", "dns": "--url of --domein",
             "server": "--server", "wpsite": "--url, --wp of --wp-ssh"}
    for c in CONTROLES:
        if c["groep"] not in GROEPEN[ctx.type]:
            continue
        regels = [r for r in c["regels"] if checklist_ids is None or r in checklist_ids or r.split("-")[0] in ("SCR", "INV", "BIZ", "MSG")]
        if not regels:
            continue
        if not voorwaarde[c["groep"]]:
            res = {r: (ONBEKEND, "niet gemeten: %s niet opgegeven" % optie[c["groep"]]) for r in regels}
        else:
            try:
                res = c["f"](ctx)
                if isinstance(res, tuple):
                    res = {regels[0]: res}
            except Exception as fout:  # een kapotte controle is ONBEKEND, nooit PASS
                res = {r: (ONBEKEND, "fout in de controle (%s)" % type(fout).__name__) for r in regels}
        for r in regels:
            status, tekst = res.get(r, (ONBEKEND, "controle gaf geen uitkomst"))
            uit.append({"regel": r, "domein": c["domein"], "controle": c["titel"], "status": status,
                        "dekking": c["dekking"], "uitvoer": kort(tekst), "rest": c["rest"]})
    return uit


def bewijs_rij(resultaten):
    """Vat de controles van één regel samen tot (status, bewijs) voor het bewijsbestand."""
    st = [r["status"] for r in resultaten]
    tekst = "; ".join("%s: %s (%s)" % (r["controle"], r["status"], r["uitvoer"]) for r in resultaten)
    rest = "; ".join(dict.fromkeys(r["rest"] for r in resultaten if r["rest"] and r["dekking"] != "volledig"))
    if FAIL in st:
        return "niet voldaan", tekst
    if ONBEKEND in st:
        return "niet gemeten", tekst + (" · handmatig ook: " + rest if rest else "")
    if all(s == NVT for s in st):
        return "nvt", tekst
    if all(r["dekking"] == "volledig" for r in resultaten):
        return "voldaan", tekst
    return "niet gemeten", "deelcontrole geslaagd: " + tekst + " · handmatig nog: " + rest


def schrijf(ctx, resultaten, punten, uit_map, hash_, versies):
    per_regel = {}
    for r in resultaten:
        per_regel.setdefault(r["regel"], []).append(r)
    uitz = lib.lees_uitzonderingen(ctx.pad) if ctx.pad else {}
    nu = datetime.datetime.now(datetime.timezone.utc)
    rijen, secties = {}, {}
    for p in punten:
        if p["id"] in rijen:
            continue
        if p["id"] in per_regel:
            status, bewijs = bewijs_rij(per_regel[p["id"]])
        else:
            status, bewijs = "niet gemeten", "handmatig: " + p["tekst"].replace("|", "/")
        u = lib.uitzondering_voor(p["id"], uitz) if status in ("niet voldaan", "niet gemeten") else None
        if u:
            status, bewijs = "uitzondering", "%s, verloopt %s · %s" % (u[0], u[1].isoformat(), bewijs)
        rijen[p["id"]] = (status, bewijs)
        secties.setdefault(p["subskill"], []).append(p["id"])
    los = [r for r in per_regel if r not in rijen]
    for r in los:
        rijen[r] = bewijs_rij(per_regel[r])
        secties.setdefault("batch 4 (nog niet in de checklist)", []).append(r)
    tel = {}
    for s, _ in rijen.values():
        tel[s] = tel.get(s, 0) + 1
    naam = "%s-%s" % (nu.strftime("%Y-%m-%d"), hash_)
    doel, n = uit_map / (naam + ".md"), 1
    while doel.exists():  # een bewijsbestand wordt nooit achteraf gewijzigd
        n += 1
        doel = uit_map / ("%s-%d.md" % (naam, n))
    uit_map.mkdir(parents=True, exist_ok=True)
    kop = ["---", "project: %s" % (ctx.pad.name if ctx.pad else ctx.host or "server"), "type: %s" % ctx.type,
           "commit: %s" % hash_, "datum: %s" % nu.strftime("%Y-%m-%dT%H:%M:%SZ"), "door: dicht_audit.py (automatisch deel)",
           "akkoord: ", "runtime: %s" % versies, "hulpmiddelen: dicht_audit.py",
           "gate: dicht_audit.py %s, %s" % (ctx.type, ", ".join("%s %d" % kv for kv in sorted(tel.items()))),
           "uitzonderingen: %s" % (", ".join(sorted({b.split(",")[0] for s, b in rijen.values() if s == "uitzondering"})) or "geen"),
           "---", "",
           "Automatisch gemeten: %d regels. Handmatig te beoordelen: %d regels (status `niet gemeten`, met de vraag in de kolom Bewijs)."
           % (len(per_regel), len(rijen) - len(per_regel)),
           "Een `niet gemeten` is nooit `voldaan`. Vul de handmatige regels aan in een nieuw bestand; wijzig dit bestand niet.", ""]
    for sub, ids in secties.items():
        kop += ["## %s" % sub, "", "| Regel | Status | Bewijs |", "|---|---|---|"]
        kop += ["| %s | %s | %s |" % (i, rijen[i][0], rijen[i][1]) for i in ids] + [""]
    doel.write_text("\n".join(kop), encoding="utf-8")
    json_pad = doel.with_suffix(".json")
    json_pad.write_text(json.dumps({"type": ctx.type, "commit": hash_, "datum": nu.isoformat(), "controles": resultaten},
                                   indent=1, ensure_ascii=False), encoding="utf-8")
    return doel, json_pad, tel


def main(argv=None):
    p = argparse.ArgumentParser(description="Auditscript van de skill dicht: alleen lezen, begrensd, zonder geheimen in de uitvoer.")
    p.add_argument("type", choices=lib.TYPES)
    p.add_argument("--pad", help="map van het project (repository)")
    p.add_argument("--url", help="basis-URL van de site of dienst, voor anonieme aanvragen")
    p.add_argument("--domein", help="domein voor DNS-controles (standaard de host uit --url zonder www.)")
    p.add_argument("--server", action="store_true", help="meet ook deze server (cron, systemd, poorten, Docker, updates)")
    p.add_argument("--wp", help="pad van een lokale WordPress-installatie (WP-CLI)")
    p.add_argument("--wp-ssh", help="gebruiker@host:/pad van een WordPress-installatie op afstand (WP-CLI via ssh)")
    p.add_argument("--uit", help="map voor het bewijsbestand (standaard <pad>/bewijs)")
    p.add_argument("--geen-bewijs", action="store_true", help="schrijf niets, toon alleen de tabel")
    p.add_argument("--lijst", action="store_true", help="toon welke regels dit type automatisch meet en stop")
    a = p.parse_args(argv)
    import controles_repo, controles_server, controles_web, controles_wp  # noqa: F401,E401  (registreren zichzelf)

    if a.lijst:
        for c in CONTROLES:
            if c["groep"] in GROEPEN[a.type]:
                print("%-8s %-28s %-9s %s" % (c["domein"], ",".join(c["regels"]), c["dekking"], c["titel"]))
        return 0
    ctx = Ctx(a)
    pad = lib.checklist_pad(a.type)
    punten = lib.lees_checklist(pad) if pad else []
    if not pad:
        print("waarschuwing: checklist voor %s niet gevonden; alleen de automatische controles komen in het bewijs." % a.type, file=sys.stderr)
    resultaten = draai(ctx, {x["id"] for x in punten} if punten else None)
    hard = {x["id"] for x in punten if x["hard"]}
    for r in resultaten:
        print("%-9s %-10s %-9s %s: %s" % (r["status"], r["regel"], r["dekking"], r["controle"], r["uitvoer"]))
    tel = {s: sum(1 for r in resultaten if r["status"] == s) for s in (PASS, FAIL, ONBEKEND, NVT)}
    print("\n%d controles: %s" % (len(resultaten), ", ".join("%s %d" % kv for kv in tel.items())))
    if not a.geen_bewijs:
        code, h = ctx.run(["git", "rev-parse", "--short", "HEAD"], cwd=ctx.pad) if ctx.pad else (1, "")
        uit_map = Path(a.uit) if a.uit else (ctx.pad / "bewijs" if ctx.pad else Path("bewijs"))
        versies = "; ".join(kort(ctx.run([b, v])[1].splitlines()[0]) for b, v in (("node", "-v"), ("php", "-v"), ("git", "--version")) if shutil.which(b))
        doel, json_pad, tel_rijen = schrijf(ctx, resultaten, punten, uit_map, h if code == 0 else "geen-git", versies)
        print("bewijsbestand: %s (%s)\njson: %s" % (doel, ", ".join("%s %d" % kv for kv in sorted(tel_rijen.items())), json_pad))
    harde_fouten = sorted({r["regel"] for r in resultaten if r["status"] == FAIL and (r["regel"] in hard or not punten or r["regel"] not in {x["id"] for x in punten})})
    if harde_fouten:
        print("niet voldaan (hard): %s" % ", ".join(harde_fouten))
    return 1 if harde_fouten else 0


if __name__ == "__main__":
    try:
        # het script draait als __main__; maak het ook onder zijn modulenaam vindbaar voor de controles
        sys.modules.setdefault("dicht_audit", sys.modules["__main__"])
        sys.path.insert(0, str(HIER))
        sys.exit(main())
    except Exception as fout:
        print("dicht_audit: eigen fout (%s: %s)" % (type(fout).__name__, lib.maskeer(str(fout))[:200]), file=sys.stderr)
        sys.exit(2)
