#!/usr/bin/env python3
"""PreToolUse-hook (Bash): geheimscan vóór elke `git commit` van een sessie, in elke repo (GIT-32, GIT-33).

Globale veiligheidshook (besluit van Marketing Maatwerk, 04-10-2026). Scant wat gestaged is, en bij `git add <paden> && git commit`
in één opdracht ook de wijzigingen en nieuwe bestanden van die paden, want die zijn op dit moment nog niet gestaged.
Bij een treffer wordt de opdracht geweigerd met bestand, regel en de naam van het patroon, nooit de waarde.
Staat de gitleaks-binary er (zie geheimscan.py), dan scant die mee.

Dit is een vangnet: de hook ziet geen commit uit een script of een andere tool, en geen `cd map && git commit`.
De git-hook per repo (git-pre-commit) blijft de poort die gesloten faalt. Een fout in deze hook blokkeert niet.
"""
import json
import os
import re
import shlex
import subprocess
import sys


def toegevoegde_paden(cmd):
    """De paden van elke `git add` in de opdracht; None als een pad niet te bepalen is (variabele of substitutie)."""
    paden = []
    for deel in re.split(r"&&|\|\||[;|\n]", cmd):
        try:
            w = shlex.split(deel)
        except ValueError:
            return None
        if "git" in w and "add" in w[w.index("git"):]:
            for x in w[w.index("add", w.index("git")) + 1:]:
                if "$" in x or "`" in x:
                    return None
                if not x.startswith("-"):
                    paden.append(x)
    return paden


def main():
    import geheimscan
    import pretool_gevaarlijk
    invoer = json.load(sys.stdin)
    cmd = str((invoer.get("tool_input") or {}).get("command", ""))
    m = re.search(r"\bgit\b(" + pretool_gevaarlijk.DEEL + r")\bcommit\b", pretool_gevaarlijk.kaal(cmd))
    if invoer.get("tool_name") != "Bash" or not m:
        return
    map_ = re.search(r"\s-C\s+(\S+)", m.group(1))
    os.chdir(os.path.join(invoer.get("cwd") or ".", map_.group(1) if map_ else ""))
    if subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True).returncode:
        return  # geen repository: git weigert de commit zelf
    treffers, tekst = geheimscan.scan_staged()
    paden = toegevoegde_paden(cmd)
    if paden is None or paden:
        t2, tekst2 = geheimscan.scan_diff(["HEAD"], paden or ())
        nieuw = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "--", *(paden or ())],
                               capture_output=True, text=True, timeout=30).stdout.splitlines()
        t2 += [(n, 0, "bestandsnaam (GIT-04, GIT-10)") for n in nieuw if geheimscan.lib.GEHEIM_BESTAND.search(n)] + geheimscan.scan_paden(nieuw)
        treffers, tekst = treffers + [x for x in t2 if x not in treffers], tekst + "\n" + tekst2
    tweede = geheimscan.gitleaks(tekst)
    if tweede and tweede[0]:
        treffers.append(("gitleaks", 0, "treffer van gitleaks (draai geheimscan.py --staged voor de afgeschermde uitvoer)"))
    if treffers:
        lijst = "; ".join("%s:%s %s" % (b, nr or "-", naam) for b, nr, naam in treffers[:10])
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": (
            "dicht: GIT-32, GIT-33: geweigerd. De geheimscan vindt %d treffer(s) in wat deze commit vastlegt: %s. Haal het geheim weg "
            "(of zet `gitleaks:allow` achter een regel met een nepwaarde); was het echt, trek het dan eerst in (GIT-36)." % (len(treffers), lijst))}}))


if __name__ == "__main__":
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        main()
    except Exception as fout:
        print(json.dumps({"systemMessage": "dicht: fout in de geheimscan-hook (%s); de commit is niet gescand en niet geblokkeerd." % type(fout).__name__}))
    sys.exit(0)
