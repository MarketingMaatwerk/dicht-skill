#!/usr/bin/env python3
"""PreToolUse-hook (Bash, Write, Edit): weigert gevaarlijke opdrachten, met een melding die zegt wat wel kan.

De hook vraagt nooit om bevestiging (besluit van Marketing Maatwerk, 04-10-2026): een sessie zonder mens zou dan blijven wachten.
Wat akkoord vraagt, wordt geweigerd met de melding dat Marketing Maatwerk de opdracht zelf uitvoert.

  GIT-04            git add -A, -u, ., :/ of *, git stage, git commit -a   weigeren
  GIT-24, GIT-37    git push --force, -f, +ref, --force-with-lease  weigeren
  ARCH-30, GIT-58   --no-verify, core.hooksPath via -c of GIT_CONFIG_*   weigeren (is een uitzondering)
  SCR-15, ARCH-28   rm -r buiten het project en buiten /tmp         weigeren
  SCR-22, GIT-62    curl of wget naar een shell                     weigeren
  SCR-53            pkill of killall op een breed patroon           weigeren
  SCR-19, INFRA-76, WP-71, AI-28   geheim als argument              weigeren (de waarde komt nooit in de melding)
  besluit 2         schrijven naar .dicht/overrules.log             weigeren (alleen Marketing Maatwerk, via de noodrem)

Dit is een vangnet op tekstpatronen, geen sandbox: een opdracht in een variabele, een
script of een andere tool ziet deze hook niet. Een fout in de hook blokkeert niet.
"""
import json
import os
import re
import shlex
import subprocess
import sys

DEEL = r"[^;&|\n]*"


def zonder_heredoc(cmd):
    return re.sub(r"<<-?\s*['\"]?(\w+)['\"]?.*?\n\1\b", "", cmd, flags=re.S)


def kaal(cmd):
    """De opdracht zonder here-documents en zonder de inhoud van aanhalingstekens (voor vlaggen)."""
    return re.sub(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"", '""', zonder_heredoc(cmd))


def git_regels(k, cmd):
    """`k` is de kale opdracht; `cmd` de opdracht zonder here-documents, alleen voor een vorm die tussen aanhalingstekens staat ('*', "core.hooksPath=...")."""
    stage = r"\bgit\b" + DEEL + r"\b(add|stage)\b" + DEEL
    if re.search(stage + r"(\s-[a-zA-Z]*[Au][a-zA-Z]*(?=\s|$)|\s--all\b|\s--update\b|\s(\.|:/|\*)(?=\s|$))", k) or \
       re.search(stage + r"\s[\"'](\.|:/|\*)[\"'](?=\s|$)", cmd) or \
       re.search(r"\bgit\b" + DEEL + r"\bcommit\b" + DEEL + r"(\s-[b-zB-Z]*a[a-zA-Z]*\b|\s--all\b)", k):
        return "deny", ("GIT-04: stage alleen expliciete paden (`git add <pad> <pad>`), nooit `git add -A`, `-u`, `.`, `:/` of `*`, `git stage` in die vormen "
                        "of `git commit -a`. `git status --short` toont welke bestanden gewijzigd zijn; noem ze bij naam.")
    if re.search(r"(?i)(\bgit\b" + DEEL + r"\s-c\s*|\bGIT_CONFIG_KEY_\d+=)core\.hookspath\b", k) or \
       re.search(r"(?i)(\bgit\b" + DEEL + r"\s-c\s*|\bGIT_CONFIG_KEY_\d+=)[\"']core\.hookspath\b", cmd):
        return "deny", ("ARCH-30: geweigerd. `core.hooksPath` meegeven (met `-c` of `GIT_CONFIG_*`) zet de git-hook buiten werking, net als `--no-verify`; dat is een "
                        "uitzondering die Marketing Maatwerk vooraf vastlegt in docs/uitzonderingen.md. Los op wat de hook tegenhoudt, of meld het; Marketing Maatwerk voert de opdracht dan zelf uit.")
    push = re.search(r"\bgit\b" + DEEL + r"\bpush\b(" + DEEL + ")", k)
    if push:
        rest = push.group(1)
        if re.search(r"\s(--force|-f)(\s|$)|\s\+\S", rest):
            return "deny", "GIT-24, GIT-37: geen `git push --force`. Een geforceerde push vraagt akkoord van Marketing Maatwerk, die hem zelf uitvoert met `--force-with-lease`."
        if "--force-with-lease" in rest:
            if re.search(r"\b(main|master)\b", rest):
                return "deny", "GIT-24: geen geforceerde push naar main of master."
            return "deny", ("GIT-37: geweigerd. Een geforceerde push (`--force-with-lease`) herschrijft de geschiedenis van deze branch en vraagt akkoord van Marketing Maatwerk. "
                            "Meld waarom het nodig is; Marketing Maatwerk voert de opdracht dan zelf uit.")
    if re.search(r"\bgit\b" + DEEL + r"\b(commit|push|merge)\b" + DEEL + r"\s--no-verify\b", k) or \
       re.search(r"\bgit\b" + DEEL + r"\bcommit\b" + DEEL + r"\s-[a-zA-Z]*n[a-zA-Z]*\b", k):
        return "deny", ("ARCH-30: geweigerd. `--no-verify` slaat de gate over; dat is een uitzondering die Marketing Maatwerk vooraf vastlegt in docs/uitzonderingen.md. "
                        "Los op wat de gate tegenhoudt, of meld het; Marketing Maatwerk voert de opdracht dan zelf uit.")
    return None


ZOEKERS = ("grep", "egrep", "fgrep", "rg", "ag", "ack")


def zonder_zoekpatronen(cmd):
    """De opdracht, met in elk deel dat met grep of rg begint de tekst tussen aanhalingstekens leeggemaakt: een zoekpatroon
    is geen opdracht (`grep "a|rm -rf /" map`). Tekst met `$(` of een backtick blijft staan, want die wordt wel uitgevoerd."""
    uit, deel = [], []

    def sluit():
        woorden = "".join(t for t in deel if t[:1] not in "'\"").split()
        while woorden and (woorden[0] in ("sudo", "command", "nice", "time") or re.match(r"^\w+=", woorden[0])):
            woorden = woorden[1:]
        zoekt = woorden and (os.path.basename(woorden[0]) in ZOEKERS or woorden[:2] == ["git", "grep"])
        uit.extend("''" if zoekt and t[:1] in "'\"" and "$(" not in t and "`" not in t else t for t in deel)
        del deel[:]

    for t in re.findall(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"|&&|\|\||[;|\n]|[^'\";|&\n]+|.", cmd, re.S):
        if t in ("&&", "||", ";", "|", "\n"):
            sluit()
            uit.append(t)
        else:
            deel.append(t)
    sluit()
    return "".join(uit)


def rm_regels(cmd, cwd, scratch):
    for deel in re.split(r"&&|\|\||[;|\n]", zonder_zoekpatronen(cmd)):
        try:
            woorden = shlex.split(deel, posix=True)
        except ValueError:
            woorden = deel.split()
        while woorden and (woorden[0] in ("sudo", "command", "nice", "time") or re.match(r"^\w+=", woorden[0])):
            woorden = woorden[1:]
        if not woorden or os.path.basename(woorden[0]) != "rm":
            continue
        opties = [w for w in woorden[1:] if w.startswith("-") and w != "--"]
        if not any(re.match(r"^-[a-zA-Z]*[rR]", o) or o == "--recursive" for o in opties):
            continue
        for doel in (w for w in woorden[1:] if not w.startswith("-")):
            if re.search(r"\$\{?\w+\}?", doel) and ":?" not in doel:
                return "deny", "SCR-15: recursief verwijderen met een onbewaakte variabele. Schrijf `rm -rf -- \"${MAP:?}/vast-deel\"` met een absoluut pad."
            if "$" in doel or "`" in doel:
                continue  # bewaakte variabele of substitutie: niet te beoordelen
            if doel in ("/", "/*", "~", "~/", "~/*", ".", "..", "*", "./*") or doel.startswith("..") or "/../" in doel:
                return "deny", "SCR-15: recursief verwijderen van `%s` is geblokkeerd. Noem een exact pad binnen het project." % doel
            pad = os.path.realpath(os.path.join(cwd, os.path.expanduser(doel.rstrip("*").rstrip("/") or "/")))
            binnen = [os.path.realpath(p) for p in (cwd, scratch, "/tmp", "/var/tmp") if p]
            if pad in binnen or pad == os.path.join(os.path.realpath(cwd), ".git"):
                return "deny", "SCR-15: recursief verwijderen van de hele map `%s` is geblokkeerd." % doel
            if any(pad.startswith(b + os.sep) for b in binnen):
                continue
            if pad.count(os.sep) <= 2 or pad == os.path.realpath(os.path.expanduser("~")):
                return "deny", "SCR-15: recursief verwijderen van `%s` (systeem- of thuismap) is geblokkeerd." % doel
            return "deny", ("SCR-15, ARCH-28: geweigerd. `rm -r` op `%s` ligt buiten het project en buiten /tmp; verwijderen daar vraagt akkoord van Marketing Maatwerk. "
                            "Meld het exacte pad en de reden; Marketing Maatwerk voert de opdracht dan zelf uit." % doel)
    return None


def pijp_regels(cmd, k):
    haal = r"(curl|wget)\b"
    for t in (cmd, k):
        if re.search(haal + r"[^|;&\n]*\|\s*(sudo\s+)?(env\s+)?((ba|z|da|k)?sh|python[0-9.]*|node|perl|php|ruby)\b", t) or \
           re.search(r"\b((ba|z)?sh|python[0-9.]*|source|\.)\s+<\(\s*" + haal, t) or \
           re.search(r"\beval\s+[\"']?\$\(\s*" + haal, t) or \
           re.search(r"\b(ba|z)?sh\s+-c\s+[\"']?\$\(\s*" + haal, t):
            return "deny", "SCR-22, GIT-62: voer niets uit dat je in dezelfde regel ophaalt. Haal een vaste versie op, controleer de checksum, lees het, voer het dan uit."
    return None


ALGEMEEN = {"node", "nodejs", "python", "python2", "python3", "php", "tsx", "ts-node", "npm", "npx", "deno", "bun", "bash", "sh", "zsh",
            "java", "ruby", "perl", "nginx", "apache2", "httpd", "postgres", "mysqld", "redis-server", "docker", "dockerd", "containerd",
            "claude", "tmux", "sshd", "systemd", "cron", "chrome", "chromium", "exec", "run", "start", "server", "src"}
KILL_MET_WAARDE = {"-u", "-U", "-g", "-G", "-s", "-t", "-r", "--signal", "--euid", "--uid", "--group", "--pgroup", "--session",
                   "--terminal", "--runstates", "--ns", "--nslist", "--user", "--older-than", "--younger-than"}
KILL_GERICHT = {"-P", "--parent", "-F", "--pidfile"}
KILL_HOE = ("SCR-53: geweigerd. %s Stop een proces op proces-id (`kill <pid>`, een pidbestand) of op poort (`fuser -k <poort>/tcp`), "
            "of geef een patroon dat alleen het eigen proces raakt (het volledige pad van de eigen worktree).")


def raakt_dienst(pgrep_args):
    """Namen van systemd-diensten buiten de eigen cgroup waarvan een proces op de selectie past. Alleen lezen."""
    eigen = open("/proc/self/cgroup").read().strip()
    pids = subprocess.run(["pgrep"] + pgrep_args, capture_output=True, text=True, timeout=5).stdout.split()
    diensten = set()
    for pid in pids:
        try:
            cg = open("/proc/%s/cgroup" % pid).read().strip()
        except OSError:
            continue
        if cg != eigen and cg.endswith(".service"):
            diensten.add(cg.rsplit("/", 1)[-1])
    return sorted(diensten)


def kill_regels(cmd):
    for deel in re.split(r"&&|\|\||[;|\n]", cmd):
        try:
            woorden = shlex.split(deel, posix=True)
        except ValueError:
            woorden = deel.split()
        while woorden and (woorden[0] in ("sudo", "command", "nice", "time") or re.match(r"^\w+=", woorden[0])):
            woorden = woorden[1:]
        if not woorden or os.path.basename(woorden[0]) not in ("pkill", "killall"):
            continue
        prog, rest = os.path.basename(woorden[0]), woorden[1:]
        opties, namen, selectie, i = [], [], [], 0
        while i < len(rest):
            w = rest[i]
            if w in KILL_GERICHT:
                opties.append(w)
                i += 1
            elif w in KILL_MET_WAARDE or (prog == "killall" and w in ("-o", "-y")):
                if w in ("-u", "-U", "-g", "-G", "--euid", "--uid", "--user", "--group") and i + 1 < len(rest):
                    selectie += [w if prog == "pkill" else "-u", rest[i + 1]]
                i += 1
            elif w.startswith("-") and w != "--":
                opties.append(w)
            elif w != "--":
                namen.append(w)
            i += 1
        if any(o in KILL_GERICHT for o in opties):
            continue
        if not namen:
            return "deny", KILL_HOE % ("`%s` zonder patroon stopt elk proces van de gebruiker." % prog)
        vol = prog == "pkill" and any(re.match(r"^-[a-zA-Z]*f", o) or o == "--full" for o in opties)
        for naam in namen:
            kern = re.sub(r"[\[\]^$]", "", naam)
            if "/" not in kern and all(w.lower() in ALGEMEEN or len(w) < 3 for w in re.split(r"[\s.*]+", kern) if w):
                return "deny", KILL_HOE % ("Het patroon `%s` past op elk proces met die naam, ook op live diensten." % naam)
            try:
                diensten = raakt_dienst(selectie + (["-f"] if vol else ["-x"] if prog == "killall" or "-x" in opties else []) + ["--", naam])
            except Exception:
                diensten = []
            if diensten:
                return "deny", KILL_HOE % ("Het patroon `%s` past nu op een proces van %s." % (naam, ", ".join(diensten[:3])))
    return None


LETTERLIJK = r"(?![\"']?\$|[\"']?<|[\"']?@)[\"']?[^\s\"']{6,}"


def geheim_regels(cmd, lib):
    namen = lib.vind_geheimen(cmd)
    if not namen:
        for naam, pat in (
            ("wachtwoord-optie", r"\s--(password|passwd|user_pass|pass|secret|token|api-key)[= ]" + LETTERLIJK),
            ("mysql -p<wachtwoord>", r"\bmysql(dump)?\b" + DEEL + r"\s-p(?!\s|$)" + LETTERLIJK),
            ("PGPASSWORD of MYSQL_PWD", r"\b(PGPASSWORD|MYSQL_PWD)=" + LETTERLIJK),
            ("curl -u gebruiker:wachtwoord", r"\bcurl\b" + DEEL + r"\s(-u|--user)\s+[\"']?[^\s:\"'$]+:(?!\$)[^\s\"']{3,}"),
            ("Authorization-kop", r"(?i)authorization:\s*(bearer|basic|token)\s+(?!\$)[A-Za-z0-9._~+/=-]{12,}"),
            ("wp config set met geheim", r"\bwp\b" + DEEL + r"\bconfig\s+set\s+\S*(KEY|SECRET|PASS|SALT)\S*\s+" + LETTERLIJK),
            ("docker login -p", r"\bdocker\s+login\b" + DEEL + r"\s(-p|--password)\s+" + LETTERLIJK),
        ):
            if re.search(pat, cmd):
                namen = [naam]
                break
    if namen:
        return "deny", ("SCR-19, INFRA-76, AI-28: de opdracht bevat een geheim als argument (%s). Laat het programma het geheim zelf lezen uit een "
                        "bestand met modus 600 of van standaardinvoer. Als de waarde echt was: beschouw haar als gelekt (GIT-36)." % ", ".join(sorted(set(namen))))
    return None


def overrule_regels(tool, ti, lib):
    naam = ".dicht/" + lib.OVERRULE_BESTAND
    if tool in ("Write", "Edit") and str(ti.get("file_path", "")).replace("\\", "/").endswith(naam):
        return "deny", "besluit 2: alleen Marketing Maatwerk legt een overrule vast, door `DICHT OVERRULE: <reden>` te typen."
    cmd = ti.get("command", "") if tool == "Bash" else ""
    if lib.OVERRULE_BESTAND in cmd and re.search(r">|\btee\b|\bsed\b|\brm\b|\bmv\b|\bcp\b|\btruncate\b|\bdd\b|python|perl|\bed\b", cmd):
        return "deny", "besluit 2: .dicht/overrules.log wordt alleen door de noodrem van Marketing Maatwerk geschreven."
    return None


def main():
    import dicht_lib as lib
    invoer = json.load(sys.stdin)
    tool, ti = invoer.get("tool_name"), invoer.get("tool_input") or {}
    besluit = overrule_regels(tool, ti, lib)
    if not besluit and tool == "Bash":
        cmd = str(ti.get("command", ""))
        k = kaal(cmd)
        besluit = (geheim_regels(cmd, lib) or pijp_regels(cmd, k) or git_regels(k, zonder_heredoc(cmd)) or kill_regels(cmd)
                   or rm_regels(cmd, invoer.get("cwd") or os.getcwd(), invoer.get("scratchpad_dir")))
    if besluit:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": besluit[0],
                                                 "permissionDecisionReason": "dicht: " + besluit[1]}}))


if __name__ == "__main__":
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        main()
    except Exception as fout:
        print(json.dumps({"systemMessage": "dicht: fout in de PreToolUse-hook (%s); de opdracht is niet gecontroleerd en niet geblokkeerd." % type(fout).__name__}))
    sys.exit(0)
