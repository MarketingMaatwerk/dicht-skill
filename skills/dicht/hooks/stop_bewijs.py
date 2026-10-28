#!/usr/bin/env python3
"""Stop-hook: laat een beurt niet eindigen met "klaar" zonder volledig bewijs (ARCH-52, besluit 2).

Werkt alleen in een project met een `.dicht/`-map. Blokkeert als het laatste bericht
een klaar-melding is en een harde regel die het pad eist niet is afgevinkt. Het pad: bij een
wijziging aan een bestaand project met `.dicht/profiel.json` de regels die
tools/regels_voor_wijziging.py kiest; bij een nieuw project, een oplevering of zonder profiel
alle harde regels van het projecttype (zie dicht/references/kleine-wijziging.md).
Aangescherpt na de proef bij het CRM (besluit van Marketing Maatwerk 17-10-2026, een eigen notitie):
- een klaar-melding is alleen een klaar-woord aan het begin van een regel of zin (`KLAAR: ...`, `Klaar.`),
  niet `KLAAR (deel)`, `KLAAR-regel`, `Klaar als`, `staat klaar` of `de taak is klaar` midden in een zin;
- getoetst wordt het bewijs van de projecten waarin de sessie code schreef (sessielog en subagents), niet
  dat van de cwd; een sessie die geen code schreef wordt niet geblokkeerd. Zonder sessielog: de cwd, zoals eerst.
Noodrem: Marketing Maatwerk typt `DICHT OVERRULE: <reden>` (zie prompt_overrule.py); dat wordt vastgelegd.
Een fout in deze hook blokkeert niet en geeft een zichtbare melding.
"""
import json
import os
import re
import sys

KLAAR = re.compile(r"(?:^|[.!?][ \t]+)[ \t>*_#`-]*(klaar|afgerond|voltooid|opgeleverd|gereed|done|completed?|finished)\b"
                   r"(?![*_`]*[ \t]*\((?:deel|gedeeltelijk)|-|[ \t]+(?:als|zodra|wanneer|nadat|voordat|tenzij|om|voor)\b|[^\n.!:·]*\?)",
                   re.I | re.M)
ONTKENNING = re.compile(r"\b(niet|nog niet|geen|pas|not|bijna|zodra|voordat|tot)\b[^.!?\n]{0,25}$", re.I)
OPLEVERING = re.compile(r"\b(opgeleverd|oplevering)\b", re.I)


def meldt(patroon, tekst):
    return any(not ONTKENNING.search(tekst[max(0, m.start() - 40):m.start()]) for m in patroon.finditer(tekst))


def main():
    import dicht_lib as lib
    from pretool_verplicht import doelen_bash
    invoer = json.load(sys.stdin)
    cwd_root = lib.vind_project(invoer.get("cwd") or ".")
    bericht = invoer.get("last_assistant_message")
    if bericht is None:
        if cwd_root:
            print(json.dumps({"systemMessage": "dicht: Stop-hook kreeg geen last_assistant_message; bewijs niet getoetst."}))
        return
    if not KLAAR.search(bericht):
        return
    log = invoer.get("transcript_path")
    roots = lib.geschreven_projecten(log, doelen_bash) if log and os.path.isfile(log) else {cwd_root} - {None}
    if not roots:
        return
    oplevering = meldt(OPLEVERING, bericht)
    uitkomsten = [(root, *lib.beoordeel(root, oplevering=oplevering)) for root in sorted(roots)]
    open_ = [u for u in uitkomsten if u[1]]
    if not open_:
        meldingen = [m for u in uitkomsten for m in u[3]]
        if meldingen:
            print(json.dumps({"systemMessage": "dicht: bewijs volledig (%s). Let op: %s"
                              % ("; ".join(u[2] for u in uitkomsten), " ".join(meldingen))}))
        return
    sessie = invoer.get("session_id", "")
    reden = next((r for r in (lib.overrule_van(x, sessie) for x in sorted({cwd_root, *roots} - {None})) if r is not None), None)
    root, ontbrekend, toelichting, meldingen = open_[0]
    if reden is not None:
        print(json.dumps({"systemMessage": "dicht: klaar-melding doorgelaten op overrule van Marketing Maatwerk (%s); %d harde regels niet afgevinkt in %s."
                          % (reden, len(ontbrekend), root)}))
        return
    lijst = "; ".join("%s (%s)" % o for o in ontbrekend[:15])
    print(json.dumps({"decision": "block", "reason": (
        "dicht: je meldt klaar, maar het bewijs is niet volledig (%s, project %s). Niet afgevinkt: %d harde regels, waaronder: %s. "
        "Doe één van drie: (1) vul het bewijs aan (bij een wijziging: tools/regels_voor_wijziging.py toont de regels; "
        "bij een oplevering: /dicht-audit, daarna de handmatige regels) of leg een uitzondering vast "
        "in docs/uitzonderingen.md met datum, reden en verloopdatum, na akkoord van Marketing Maatwerk; (2) meld niet klaar en zeg letterlijk "
        "wat niet is getoetst; (3) alleen Marketing Maatwerk kan de noodrem gebruiken door `DICHT OVERRULE: <reden>` te typen."
    "%s"
    ) % (toelichting or "geen bewijsbestand", root, len(ontbrekend), lijst, "".join(" Let op: " + m for m in meldingen))}))


if __name__ == "__main__":
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        main()
    except Exception as fout:  # faal veilig: nooit blokkeren op een eigen fout
        print(json.dumps({"systemMessage": "dicht: fout in de Stop-hook (%s); het werk is niet geblokkeerd en het bewijs is niet getoetst." % type(fout).__name__}))
    sys.exit(0)
