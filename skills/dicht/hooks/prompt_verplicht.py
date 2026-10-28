#!/usr/bin/env python3
"""UserPromptSubmit-hook: herinnert aan de verplichting om dicht te laden (besluit van Marketing Maatwerk, 05-10-2026).

Geeft de regel mee als de prompt een bouwwoord bevat of de werkmap in een bouwproject ligt, en de
sessie de skill `dicht` nog niet heeft geladen. Daarna zwijgt hij. De harde grens is
`pretool_verplicht.py`; dit is alleen de herinnering vooraf. Een fout blokkeert niets.
"""
import json
import os
import re
import sys

BOUWWOORD = re.compile(
    r"\b(bouw\w*|gebouwd|implementeer\w*|programmeer\w*|refactor\w*|fix\w*|bugs?|debug\w*|plugins?|mu-plugin|thema|theme|scripts?|deploy\w*|"
    r"uitrol\w*|uitrollen|livegang|wp-admin|wp-cli|endpoints?|api|mcp|migraties?|hooks?|dockerfile|docker|nginx|systemd|cron\w*|"
    r"functions\.php|commit\w*|merge\w*|worktree|code|feature)\b", re.I)


def main():
    import dicht_lib as lib
    invoer = json.load(sys.stdin)
    root, profiel = lib.vind_profiel(os.path.join(invoer.get("cwd") or ".", "x"))
    if not root and not BOUWWOORD.search(invoer.get("prompt") or ""):
        return
    try:
        geladen = lib.geladen_skills(invoer.get("transcript_path"))
    except OSError:  # bij de eerste prompt bestaat het sessielog nog niet: dan is er niets geladen
        geladen = set()
    if "dicht" in geladen:
        return
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": lib.VERPLICHT_REGEL}}))


if __name__ == "__main__":
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        main()
    except Exception as fout:
        print(json.dumps({"systemMessage": "dicht: fout in de herinneringshook (%s); er is niets gecontroleerd." % type(fout).__name__}))
    sys.exit(0)
