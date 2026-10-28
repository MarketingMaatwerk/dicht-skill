#!/usr/bin/env python3
"""SessionStart-hook: toont in een bouwproject het projecttype, de checklist en de verplichting om dicht te laden.

Zwijgt buiten een bouwproject (een map met `.dicht/`, een git-repo of een projectkenmerk; zie
`dicht_lib.vind_profiel`). Gewone tekst op stdout komt bij deze gebeurtenis in de context van Claude.
"""
import json
import os
import sys


def main():
    import dicht_lib as lib
    cwd = json.load(sys.stdin).get("cwd") or "."
    root, profiel = lib.vind_profiel(os.path.join(cwd, "x"))
    oud = lib.vind_project(cwd)
    if not root and not oud:
        return
    types = lib.lees_project(profiel.parent.parent if profiel else oud) if profiel or oud else []
    if profiel or oud:
        if not types:
            print("dicht: %s heeft een .dicht/-map zonder geldig projecttype (zet `type: <type>` in .dicht/project)." % (oud or root))
        for t in types:
            print("dicht: projecttype %s, checklist %s" % (t, lib.checklist_pad(t) or "niet gevonden"))
    else:
        print("dicht: bouwproject %s heeft geen .dicht/profiel.json; doe eerst de intake (dicht/references/intake.md)." % root)
    subs = ""
    if profiel:
        try:
            # Alleen bestaande namen: het profiel van een project is tekst van buiten en komt hier in de context (AI-03, AI-86).
            namen = [n for n in json.loads(profiel.read_text(encoding="utf-8"))["subskills"] if n in lib.SUBSKILLS]
            if namen:
                subs = " Sub-skills van dit project: %s." % ", ".join(namen)
        except (OSError, ValueError, KeyError, TypeError):
            pass
    print(lib.VERPLICHT_REGEL + subs)


if __name__ == "__main__":
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        main()
    except Exception as fout:
        print("dicht: fout in de SessionStart-hook (%s); projecttype niet bepaald." % type(fout).__name__)
    sys.exit(0)
