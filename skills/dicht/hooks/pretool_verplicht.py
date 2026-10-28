#!/usr/bin/env python3
"""PreToolUse-hook: geen code schrijven zonder de skill dicht (besluit van Marketing Maatwerk, 05-10-2026).

Weigert Write, Edit, MultiEdit en NotebookEdit op een codebestand zolang de sessie de skill `dicht`
(en de sub-skills die bij het bestand horen) niet heeft geladen, of het bouwproject geen
`.dicht/profiel.json` heeft. Bij Bash hetzelfde voor een omleiding (ook `>|`), `tee`, `sed -i`, en voor
`cp`, `mv`, `install`, `dd of=`, `sponge`, `curl -o` en `python3 -c` met open of write_text, naar een
bestand dat altijd code is; dat is een vangnet op tekst en ziet geen script, variabele, `patch` of `git apply`.
Paden worden beoordeeld op waar ze werkelijk staan (`realpath`).
Of de skill is geladen leest de hook uit het sessielog (`transcript_path`).
Wat vrij is en wat een bouwproject is: `dicht_lib.py`, het blok "verplicht laden".
Gesloten bij twee voorspelbare fouten (AI-25, GIT-59): een sessielog dat bestaat maar niet te lezen is, en een
profiel dat niet geldig is (leeg, onvolledig, een ongeldig patroon in `paden`; SCR-47): dan weigert de hook met
een melding die zegt hoe het op te lossen.
Bestaat het sessielog niet (een sessie zonder opslag, zoals `claude -p --no-session-persistence`), dan is niet te
bepalen wat er geladen is: de bewerking gaat door met een melding en een regel in `~/.claude/dicht-hooks.log`.
Elke andere fout in deze hook blokkeert niet en geeft een zichtbare melding.
"""
import json
import os
import re
import shlex
import sys

HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n.*?\n\s*\2\b", re.S)
OMLEIDING = re.compile(r"(?:^|[\s;|&(])(?:\d?>>?\|?|&>>?|tee(?:\s+-a)?\s)\s*([^\s;|&<>()$`*]+)")
OP_DE_PLEK = re.compile(r"\b(?:sed|perl)\s(?:[^;|&\n]*?\s)?-[a-zA-Z]*i\S*\s[^;|&\n]*")


LEESTEKENS = ";&|()<>\n"
VOORAF = ("sudo", "command", "nice", "time", "env", "nohup", "then", "do", "else")
PY_SCHRIJFT = re.compile(r"""open\(\s*(['"])([^'"]+)\1\s*,\s*['"][^'"]*[wax+]|Path\(\s*(['"])([^'"]+)\3\s*\)\.write_(?:text|bytes)""")


def doelen_programma(kaal, cwd):
    """De doelen van cp, mv, install, dd of=, sponge, curl -o en python -c met open of write_text, als absoluut pad.
    Alleen waar het programma zelf het eerste woord van een deel van de opdracht is (dus niet `docker cp`, `git mv`,
    `ssh host "cp ..."` of tekst tussen aanhalingstekens). Een opdracht die niet te ontleden is geeft geen doelen."""
    lex = shlex.shlex(kaal.replace("\\\n", " "), posix=True, punctuation_chars=LEESTEKENS)
    lex.whitespace, lex.whitespace_split, lex.commenters = " \t\r", True, ""
    try:
        woorden = list(lex)
    except ValueError:
        return []
    delen, deel, sla_over = [], [], False
    for w in woorden + [";"]:
        if w and not set(w) - set(LEESTEKENS):
            if set(w) & set(";&|()\n"):
                delen.append(deel)
                deel = []
            sla_over = "<" in w or ">" in w  # het doel van een omleiding is geen argument van het programma
            if sla_over and deel and deel[-1].isdigit():
                deel.pop()
        elif sla_over:
            sla_over = False
        else:
            deel.append(w)
    doelen = []
    for deel in delen:
        while deel and (deel[0] in VOORAF or re.match(r"^\w+=", deel[0])):
            deel = deel[1:]
        if not deel:
            continue
        prog, args = os.path.basename(deel[0]), deel[1:]
        los = [a for a in args if not a.startswith("-")]
        gevonden = []
        if prog in ("cd", "pushd"):
            cwd = os.path.join(cwd, os.path.expanduser(los[0])) if cwd and len(los) == 1 and "$" not in los[0] else None
        elif prog in ("cp", "mv", "install"):
            doelmap = next((args[i + 1] for i, a in enumerate(args[:-1]) if a in ("-t", "--target-directory")), None)
            bronnen = [a for a in los if a != doelmap] if doelmap else los[:-1]
            doel = doelmap or (los[-1] if len(los) > 1 else None)
            if doel and (doelmap or doel.endswith("/") or (cwd and os.path.isdir(os.path.join(cwd, os.path.expanduser(doel))))):
                gevonden = [os.path.join(doel, os.path.basename(b.rstrip("/"))) for b in bronnen]
            elif doel:
                gevonden = [doel]
        elif prog == "dd":
            gevonden = [a[3:] for a in args if a.startswith("of=")]
        elif prog == "sponge":
            gevonden = los[:1]
        elif prog == "curl":
            gevonden = [args[i + 1] for i, a in enumerate(args[:-1]) if a == "--output" or re.fullmatch(r"-[a-zA-Z]*o", a)]
        elif re.fullmatch(r"python[0-9.]*", prog) and "-c" in args[:-1]:
            gevonden = [m.group(2) or m.group(4) for m in PY_SCHRIJFT.finditer(args[args.index("-c") + 1])]
        for d in gevonden:
            d = os.path.expanduser(d)
            if d and (cwd or os.path.isabs(d)):
                doelen.append(os.path.join(cwd or "/", d))
    return doelen


def doelen_bash(cmd, cwd):
    """De bestanden waar een opdracht zichtbaar naartoe schrijft. De inhoud van een here-document telt niet mee."""
    kaal = HEREDOC.sub(lambda m: m.group(0).split("\n", 1)[0], cmd)
    doelen = [d.strip("'\"") for d in OMLEIDING.findall(kaal)]
    for stuk in OP_DE_PLEK.findall(kaal):
        doelen += [w.strip("'\"") for w in stuk.split()[1:] if not w.startswith("-") and ("/" in w or re.search(r"\.\w+['\"]?$", w))]
    doelen += doelen_programma(kaal, cwd)
    return [d for d in doelen if d and not d.startswith("&") and "$" not in d and "`" not in d]


def main():
    import dicht_lib as lib
    invoer = json.load(sys.stdin)
    tool, ti = invoer.get("tool_name"), invoer.get("tool_input") or {}
    cwd = invoer.get("cwd") or os.getcwd()
    if tool == "Bash":
        paden, alleen_code = doelen_bash(str(ti.get("command", "")), cwd), True
    else:
        paden, alleen_code = [ti.get("file_path") or ti.get("notebook_path")], False
    paden = [os.path.join(cwd, os.path.expanduser(str(p))) for p in paden if p]
    if not any(lib.soort_bestand(p) != "vrij" for p in paden):
        return
    try:
        geladen = lib.geladen_skills(invoer.get("transcript_path"))
    except FileNotFoundError:
        lib.log_hook("pretool_verplicht: sessielog bestaat niet (%s); %s niet gecontroleerd en niet geblokkeerd" % (invoer.get("transcript_path"), tool))
        raise
    except OSError as fout:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": (
            "dicht: het sessielog %s bestaat maar is niet te lezen (%s), dus is niet te bepalen of de skill `dicht` is geladen. "
            "Code schrijven is geweigerd tot het log leesbaar is (rechten nakijken); lukt dat niet, meld het aan Marketing Maatwerk."
            % (invoer.get("transcript_path"), type(fout).__name__))}}))
        return
    for pad in paden:
        reden = lib.verplicht(pad, geladen, alleen_code)
        if reden:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                     "permissionDecisionReason": "dicht: " + reden}}))
            return


if __name__ == "__main__":
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        main()
    except Exception as fout:
        print(json.dumps({"systemMessage": "dicht: fout in de hook voor verplicht laden (%s); de bewerking is niet gecontroleerd en niet geblokkeerd." % type(fout).__name__}))
    sys.exit(0)
