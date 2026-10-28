#!/usr/bin/env python3
"""UserPromptSubmit-hook: de noodrem van Marketing Maatwerk voor de Stop-hook (besluit 2, ARCH-30).

Een prompt die begint met `DICHT OVERRULE: <reden>` wordt vastgelegd in
`.dicht/overrules.log` (tijd, sessie, reden) en geldt voor deze sessie.
De reden wordt gemaskeerd opgeslagen. Elke andere prompt: niets doen.
"""
import json
import os
import re
import sys


def main():
    import dicht_lib as lib
    invoer = json.load(sys.stdin)
    m = re.match(r"\s*DICHT OVERRULE:\s*(.{5,})", invoer.get("prompt") or "", re.S)
    if not m:
        return
    root = lib.vind_project(invoer.get("cwd") or ".")
    if not root:
        print(json.dumps({"systemMessage": "dicht: overrule genegeerd, hier is geen project met een .dicht/-map."}))
        return
    lib.schrijf_overrule(root, invoer.get("session_id", ""), m.group(1))
    print(json.dumps({"systemMessage": "dicht: overrule vastgelegd in .dicht/overrules.log; de Stop-hook laat deze sessie door.",
                      "hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext":
                          "Marketing Maatwerk heeft de noodrem van de Stop-hook gebruikt (vastgelegd in .dicht/overrules.log). "
                          "Dit is geen uitzondering op een regel: noem in je eindbericht welke harde regels niet zijn afgevinkt."}}))


if __name__ == "__main__":
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        main()
    except Exception as fout:
        print(json.dumps({"systemMessage": "dicht: fout in de overrule-hook (%s); de overrule is niet vastgelegd." % type(fout).__name__}))
    sys.exit(0)
