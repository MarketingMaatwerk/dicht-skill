#!/usr/bin/env python3
"""Geheimscan zonder netwerk (GIT-32, GIT-33): eigen patronen, en gitleaks erbij als de losse binary er staat.

  geheimscan.py --staged          scant wat gestaged is (toegevoegde regels en bestandsnamen)
  geheimscan.py <pad> [<pad>...]  scant bestanden of mappen (bijvoorbeeld bewijs/)

Meldt per treffer bestand, regelnummer en de naam van het patroon, nooit de waarde.
Een regel met `gitleaks:allow` wordt overgeslagen (zelfde afspraak als gitleaks).
Exitcode: 0 schoon, 1 treffer, 2 eigen fout.

gitleaks (besluit van Marketing Maatwerk, 04-10-2026): staat er een binary op $DICHT_GITLEAKS_BIN of
~/.claude/skills/dicht/bin/gitleaks, dan gaan de toegevoegde regels daarna ook door `gitleaks stdin`.
De binary draait alleen als zijn sha256 gelijk is aan de waarde in `gitleaks.sha256` ernaast (vastgelegd bij
de installatie, zie README.md); klopt die niet, dan faalt de scan gesloten. Zonder binary: alleen de eigen patronen.
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dicht_lib as lib  # noqa: E402

MAX_BYTES = 1_000_000
MAX_BESTANDEN = 5000


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, errors="replace", timeout=30, check=True).stdout


def scan_regel(tekst):
    return [] if "gitleaks:allow" in tekst else lib.vind_geheimen(tekst)


def scan_diff(ref, paden=()):
    """Scant de toegevoegde regels en de bestandsnamen van `git diff <ref> -- <paden>`. Geeft (treffers, toegevoegde tekst)."""
    treffers, tekst = [], []
    for naam in git("diff", *ref, "--name-only", "--diff-filter=ACMR", "--", *paden).splitlines():
        if lib.GEHEIM_BESTAND.search(naam):
            treffers.append((naam, 0, "bestandsnaam (GIT-04, GIT-10)"))
    bestand, nr = "?", 0
    for regel in git("diff", *ref, "-U0", "--no-color", "--diff-filter=ACMR", "--", *paden).splitlines():
        if regel.startswith("+++ "):
            bestand = regel[6:] if regel.startswith("+++ b/") else regel[4:]
        elif regel.startswith("@@"):
            nr = int(regel.split("+")[1].split(",")[0].split(" ")[0]) - 1
        elif regel.startswith("+"):
            nr += 1
            tekst.append(regel[1:])
            treffers += [(bestand, nr, n) for n in scan_regel(regel[1:])]
    return treffers, "\n".join(tekst)


def scan_staged():
    return scan_diff(["--cached"])


def scan_paden(paden):
    treffers, aantal = [], 0
    for pad in paden:
        bestanden = [pad] if os.path.isfile(pad) else [
            os.path.join(d, f) for d, mappen, fs in os.walk(pad) for f in fs
            if not mappen.__setitem__(slice(None), [m for m in mappen if m not in (".git", "node_modules", "vendor")])]
        for b in bestanden:
            aantal += 1
            if aantal > MAX_BESTANDEN or os.path.islink(b) or os.path.getsize(b) > MAX_BYTES:
                continue
            with open(b, "rb") as f:
                inhoud = f.read()
            if b"\0" in inhoud[:8000]:
                continue
            for nr, regel in enumerate(inhoud.decode("utf-8", "replace").splitlines(), 1):
                treffers += [(b, nr, n) for n in scan_regel(regel)]
    return treffers


def gitleaks(tekst):
    """Tweede scan met de losse gitleaks-binary. Geeft None als er geen binary staat, anders (treffer, uitvoer).
    Een binary met een andere sha256 dan vastgelegd draait niet: dat is een fout (exitcode 2)."""
    binary = Path(os.environ.get("DICHT_GITLEAKS_BIN") or Path.home() / ".claude/skills/dicht/bin/gitleaks")
    if not binary.is_file():
        return None
    vast = binary.parent / "gitleaks.sha256"
    verwacht = vast.read_text().split()[0] if vast.is_file() and vast.read_text().split() else ""
    if hashlib.sha256(binary.read_bytes()).hexdigest() != verwacht:
        raise RuntimeError("de sha256 van gitleaks klopt niet met gitleaks.sha256")
    r = subprocess.run([str(binary), "stdin", "--redact", "--exit-code", "1"], input=tekst, capture_output=True, text=True, timeout=120)
    if r.returncode not in (0, 1):
        raise RuntimeError("gitleaks gaf exitcode %d" % r.returncode)
    return r.returncode == 1, (r.stdout + r.stderr).strip()


def main(args):
    if not args:
        print(__doc__)
        return 2
    staged = args == ["--staged"]
    treffers, tekst = scan_staged() if staged else (scan_paden(args), "")
    for bestand, nr, naam in treffers:
        print("GEHEIM %s:%s %s" % (bestand, nr or "-", naam))
    tweede = gitleaks(tekst) if staged else None
    if tweede and tweede[0]:
        print(tweede[1])
        print("GEHEIM gitleaks meldt een treffer in wat gestaged is (zie hierboven; waarden zijn afgeschermd).")
    if treffers or (tweede and tweede[0]):
        print("geheimscan: treffer(s). Haal het geheim weg; was het echt, trek het dan eerst in (GIT-36).")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as fout:
        print("geheimscan: eigen fout (%s: %s); de scan is niet uitgevoerd." % (type(fout).__name__, str(fout)[:120]), file=sys.stderr)
        sys.exit(2)
