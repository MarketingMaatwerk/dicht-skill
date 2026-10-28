"""Controles op deze server (alleen met --server): cron, systemd, sshd, poorten, Docker, updates, nginx.

Alleen opvragen: crontab -l, systemctl show, ss, docker inspect met een vaste opmaak (nooit Env),
sshd -T en nginx -T via `sudo -n` als dat zonder wachtwoord kan. Van nginx -T en sshd -T worden
alleen de genoemde regels gelezen; de volledige uitvoer komt nergens terecht.
"""
import json
import os
import re
import stat
import time

from dicht_audit import FAIL, NVT, ONBEKEND, PASS, controle

MAX_UNITS = 40
MAX_CONTAINERS = 60
GEHEIMNAAM = re.compile(r"(TOKEN|SECRET|PASSWORD|KEY)=")


# --- cron ----------------------------------------------------------------------
def _cron(ctx):
    """Geeft (taken, ruwe regels). Een taak is (bron, opdracht)."""
    if "cron" in ctx.cache:
        return ctx.cache["cron"]
    regels = []
    code, uit = ctx.run(["crontab", "-l"])
    if code == 0:
        regels += [("crontab", r) for r in uit.splitlines()]
    try:
        for f in sorted(os.listdir("/etc/cron.d"))[:50]:
            try:
                regels += [("/etc/cron.d/" + f, r) for r in open("/etc/cron.d/" + f, errors="replace").read().splitlines()]
            except OSError:
                pass
    except OSError:
        pass
    taken = []
    for bron, r in regels:
        m = re.match(r"\s*(@\w+|(\S+\s+){5})(.*)", r)
        if m and re.match(r"\s*[0-9*@]", r):
            opdracht = m.group(3)
            if bron != "crontab":  # systeemcrontab: eerste woord is de gebruiker
                opdracht = opdracht.split(None, 1)[1] if len(opdracht.split(None, 1)) > 1 else ""
            taken.append((bron, opdracht))
    ctx.cache["cron"] = (taken[:60], regels)
    return ctx.cache["cron"]


def _script(opdracht):
    """Het eerste bestaande scriptpad in een cron-opdracht, of None."""
    for woord in re.split(r"[\s;&|]+", opdracht):
        if woord.startswith(("/", "~")) and os.path.isfile(os.path.expanduser(woord)):
            return os.path.expanduser(woord)
    return None


def _in_script(opdracht, patroon):
    pad = _script(opdracht)
    try:
        return bool(pad and os.path.getsize(pad) < 200_000 and re.search(patroon, open(pad, errors="replace").read()))
    except OSError:
        return False


def _naam(opdracht):
    pad = _script(opdracht)
    return os.path.basename(pad) if pad else (opdracht.split() or ["?"])[0]


@controle(["SCR-38", "SCR-18", "INFRA-69"], "server", "scripts", "cron-regels met time-out en slot",
          rest="proef met een taak die niet eindigt (exitcode 124) en een taak die twee keer start; per taak logpad en meldweg, met een proefmelding")
def cron_taken(ctx):
    taken, _ = _cron(ctx)
    if not taken:
        return {r: (NVT, "geen cron-taken voor deze gebruiker en in /etc/cron.d") for r in ("SCR-38", "SCR-18", "INFRA-69")}
    zonder_tijd = [_naam(o) for _, o in taken if not re.search(r"\btimeout\s", o) and not _in_script(o, r"\btimeout\s")]
    zonder_slot = [_naam(o) for _, o in taken if not re.search(r"\bflock\b", o) and not _in_script(o, r"\bflock\b")]
    tmp_slot = [_naam(o) for _, o in taken if re.search(r"flock[^|;]*/tmp/", o)]
    n = len(taken)
    return {
        "SCR-38": (FAIL, "%d van %d zonder timeout (regel of script): %s" % (len(zonder_tijd), n, ", ".join(zonder_tijd[:8]))) if zonder_tijd else (PASS, "%d taken met timeout" % n),
        "SCR-18": (FAIL, "slot in /tmp: " + ", ".join(tmp_slot[:8])) if tmp_slot else (PASS, "geen flock op /tmp in %d taken" % n),
        "INFRA-69": (FAIL, "%d van %d zonder flock (regel of script): %s" % (len(zonder_slot), n, ", ".join(zonder_slot[:8]))) if zonder_slot else (PASS, "%d taken met flock" % n),
    }


@controle("INFRA-70", "server", "infra", "cron-scripts niet schrijfbaar voor anderen en geen geheim in de crontab",
          rest="sudo crontab -l en de Exec-paden van eigen units; de eigenaar past bij het uitvoerende account")
def infra70(ctx):
    taken, regels = _cron(ctx)
    if not taken:
        return NVT, "geen cron-taken"
    fout = ["%s regel met een geheim in de omgeving" % b for b, r in regels if GEHEIMNAAM.search(r) and not r.lstrip().startswith("#")][:3]
    for _, o in taken:
        pad = _script(o)
        if pad and stat.S_IMODE(os.stat(pad).st_mode) & 0o022:
            fout.append("%s %o" % (pad, stat.S_IMODE(os.stat(pad).st_mode)))
    return (FAIL, "; ".join(dict.fromkeys(fout))) if fout else (PASS, "%d taken, scripts niet schrijfbaar voor groep of anderen" % len(taken))


# --- systemd ---------------------------------------------------------------------
def _units(ctx):
    """Eigen units: gewone bestanden (geen koppelingen) in /etc/systemd/system."""
    if "units" not in ctx.cache:
        try:
            namen = sorted(f for f in os.listdir("/etc/systemd/system")
                           if f.endswith(".service") and not os.path.islink("/etc/systemd/system/" + f))
        except OSError:
            namen = []
        ctx.cache["units"] = namen[:MAX_UNITS]
    return ctx.cache["units"]


def _show(ctx, unit, velden):
    code, uit = ctx.run(["systemctl", "show", unit, "-p", ",".join(velden)])
    return dict(r.split("=", 1) for r in uit.splitlines() if "=" in r) if code == 0 else {}


@controle("INFRA-66", "server", "infra", "elke eigen dienst heeft een eigen account zonder sudo of docker",
          rest="sudo -u <account> cat van een sleutel van de beheerder geeft Permission denied")
def infra66(ctx):
    units = _units(ctx)
    if not units:
        return ONBEKEND, "geen eigen units in /etc/systemd/system gevonden"
    gebruikers, fout = {}, []
    for u in units:
        g = _show(ctx, u, ["User"]).get("User", "") or "root"
        gebruikers.setdefault(g, []).append(u)
    for g, us in gebruikers.items():
        code, groepen = ctx.run(["id", "-nG", g])
        if g == "root":
            fout.append("als root: " + ", ".join(us[:6]))
        elif len(us) > 1:
            fout.append("%s deelt %d diensten" % (g, len(us)))
        elif code == 0 and set(groepen.split()) & {"sudo", "docker"}:
            fout.append("%s zit in sudo of docker" % g)
    return (FAIL, "; ".join(fout[:6])) if fout else (PASS, "%d units, elk een eigen account" % len(units))


@controle("INFRA-67", "server", "infra", "systemd-analyze security onder 5,0 per eigen dienst",
          rest="afwijkende regels verklaard; de dienst is na het aanzetten van de sandbox functioneel getest")
def infra67(ctx):
    units = _units(ctx)
    if not units:
        return ONBEKEND, "geen eigen units in /etc/systemd/system gevonden"
    hoog, gemeten = [], 0
    for u in units:
        code, uit = ctx.run(["systemd-analyze", "security", "--no-pager", u], timeout=30)
        m = re.search(r"Overall exposure level[^:]*:\s*([\d.]+)", uit)
        if m:
            gemeten += 1
            if float(m.group(1)) >= 5.0:
                hoog.append("%s %s" % (u.replace(".service", ""), m.group(1)))
    if not gemeten:
        return ONBEKEND, "systemd-analyze security gaf geen score"
    return (FAIL, "%d van %d op 5,0 of hoger: %s" % (len(hoog), gemeten, ", ".join(hoog[:8]))) if hoog else (PASS, "%d units onder 5,0" % gemeten)


@controle("INFRA-68", "server", "infra", "herstartbeleid en geheugenlimiet per eigen dienst", rest="NRestarts wordt bewaakt (INFRA-87)")
def infra68(ctx):
    units = _units(ctx)
    if not units:
        return ONBEKEND, "geen eigen units in /etc/systemd/system gevonden"
    fout = []
    for u in units:
        s = _show(ctx, u, ["Restart", "MemoryMax", "Type"])
        if s.get("Type") != "oneshot" and (s.get("Restart", "no") == "no" or s.get("MemoryMax", "infinity") == "infinity"):
            fout.append(u.replace(".service", ""))
    return (FAIL, "zonder Restart of MemoryMax: " + ", ".join(fout[:10])) if fout else (PASS, "%d units" % len(units))


@controle("SCR-38", "server", "scripts", "elke eigen timer-dienst heeft een eindige time-out", rest="proef met een opdracht die niet eindigt")
def timers(ctx):
    code, uit = ctx.run(["systemctl", "list-timers", "--all", "--no-legend", "--no-pager"])
    if code != 0:
        return ONBEKEND, "systemctl list-timers lukte niet"
    eigen = set(_units(ctx))
    diensten = sorted({w for r in uit.splitlines() for w in r.split() if w.endswith(".service") and w in eigen})
    if not diensten:
        return NVT, "geen eigen timer-diensten"
    fout = []
    for d in diensten:
        s = _show(ctx, d, ["TimeoutStartUSec", "RuntimeMaxUSec"])
        if s.get("TimeoutStartUSec", "infinity") == "infinity" and s.get("RuntimeMaxUSec", "infinity") == "infinity":
            fout.append(d.replace(".service", ""))
    return (FAIL, "zonder eindige TimeoutStartUSec: " + ", ".join(fout[:10])) if fout else (PASS, "%d timer-diensten" % len(diensten))


@controle("INFRA-72", "server", "infra", "geen geheim in Environment= van een unit", rest="modus en eigenaar van elk geheimbestand; geheimscan over de geschiedenis")
def infra72_units(ctx):
    fout = []
    for u in _units(ctx):
        try:
            tekst = open("/etc/systemd/system/" + u, errors="replace").read()
        except OSError:
            continue
        if re.search(r"^Environment=.*(TOKEN|SECRET|PASSWORD|KEY)=", tekst, re.M):
            fout.append(u)
    if not _units(ctx):
        return ONBEKEND, "geen eigen units gevonden"
    return (FAIL, "geheim in Environment=: " + ", ".join(fout[:8])) if fout else (PASS, "%d units, geen treffer" % len(_units(ctx)))


# --- ssh, poorten, updates ---------------------------------------------------------
def _sudo(ctx, args, timeout=20):
    code, uit = ctx.run(args, timeout=timeout)
    if code is not None and code != 0:
        code, uit = ctx.run(["sudo", "-n"] + args, timeout=timeout)
    return code, uit


@controle(["INFRA-01", "INFRA-02"], "server", "infra", "effectieve sshd-configuratie",
          rest="INFRA-01: inlogpoging met wachtwoord vanaf een andere machine; INFRA-02: /root/.ssh/authorized_keys is leeg")
def sshd(ctx):
    code, uit = _sudo(ctx, ["sshd", "-T"])
    if code != 0:
        return {r: (ONBEKEND, "sshd -T vraagt root en sudo -n lukte niet") for r in ("INFRA-01", "INFRA-02")}
    c = dict(r.lower().split(None, 1) for r in uit.splitlines() if " " in r)
    w = (c.get("passwordauthentication"), c.get("kbdinteractiveauthentication"), c.get("pubkeyauthentication"))
    return {"INFRA-01": (PASS if w == ("no", "no", "yes") else FAIL, "password %s, kbdinteractive %s, pubkey %s" % w),
            "INFRA-02": (PASS if c.get("permitrootlogin") == "no" else FAIL, "permitrootlogin %s" % c.get("permitrootlogin"))}


@controle("INFRA-14", "server", "infra", "alleen sshd en de proxy luisteren op alle adressen",
          rest="procesnaam per poort (sudo ss -tulnp); bewust publieke diensten hebben een reden")
def infra14(ctx):
    code, uit = ctx.run(["ss", "-H", "-tuln"])
    if code != 0:
        return ONBEKEND, "ss lukte niet"
    open_ = set()
    for r in uit.splitlines():
        d = r.split()
        if len(d) > 4 and not re.match(r"^(127\.|\[::1\]|172\.|\[fe80)", d[4]):
            poort = d[4].rsplit(":", 1)[-1]
            if poort not in ("22", "80", "443"):
                open_.add("%s/%s" % (poort, d[0]))
    return (FAIL, "publiek luisterend naast 22, 80, 443: " + ", ".join(sorted(open_)[:15])) if open_ else (PASS, "alleen 22, 80 en 443")


@controle("INFRA-20", "server", "infra", "automatische beveiligingsupdates staan aan", rest="het log toont een run van de laatste twee dagen zonder fout")
def infra20(ctx):
    try:
        tekst = open("/etc/apt/apt.conf.d/20auto-upgrades").read()
    except OSError:
        return FAIL, "/etc/apt/apt.conf.d/20auto-upgrades ontbreekt of is onleesbaar"
    aan = len(re.findall(r'(Update-Package-Lists|Unattended-Upgrade)\s+"1"', tekst)) == 2
    code, actief = ctx.run(["systemctl", "is-active", "unattended-upgrades"])
    return (PASS if aan and actief == "active" else FAIL), "beide waarden op 1: %s, dienst: %s" % ("ja" if aan else "nee", actief)


@controle("INFRA-21", "server", "infra", "geen herstart die langer dan een week wacht", dekking="volledig")
def infra21(ctx):
    delen, status = [], PASS
    if os.path.exists("/var/run/reboot-required"):
        dagen = (time.time() - os.stat("/var/run/reboot-required").st_mtime) / 86400
        delen.append("reboot-required is %.0f dagen oud" % dagen)
        status = FAIL if dagen > 7 else PASS
    else:
        delen.append("geen reboot-required")
    code, draait = ctx.run(["uname", "-r"])
    kernels = sorted((f[8:] for f in os.listdir("/boot") if f.startswith("vmlinuz-")),
                     key=lambda v: [int(x) for x in re.findall(r"\d+", v)])
    if kernels and draait != kernels[-1]:
        delen.append("draait %s, nieuwste is %s" % (draait, kernels[-1]))
        if status == PASS and not os.path.exists("/var/run/reboot-required"):
            status = FAIL
    else:
        delen.append("kernel %s is de nieuwste" % draait)
    return status, "; ".join(delen)


@controle("INFRA-22", "server", "infra", "versie van het besturingssysteem", rest="einddatum uit de releasecyclus ligt meer dan drie maanden weg, of de upgrade is ingepland")
def infra22(ctx):
    try:
        naam = re.search(r'PRETTY_NAME="?([^"\n]+)', open("/etc/os-release").read()).group(1)
    except (OSError, AttributeError):
        naam = "onbekend"
    return ONBEKEND, "%s; de einddatum is niet zonder bron te bepalen" % naam


# --- Docker (draaiende containers) ---------------------------------------------------
DOCKER_REGELS = ["INFRA-13", "INFRA-26", "INFRA-27", "INFRA-28", "INFRA-29", "INFRA-30", "INFRA-31", "INFRA-32", "INFRA-33", "INFRA-35"]
OPMAAK = ('{"n":{{json .Name}},"poorten":{{json .HostConfig.PortBindings}},"mounts":{{json .Mounts}},"user":{{json .Config.User}},'
          '"capdrop":{{json .HostConfig.CapDrop}},"secopt":{{json .HostConfig.SecurityOpt}},"ro":{{json .HostConfig.ReadonlyRootfs}},'
          '"priv":{{json .HostConfig.Privileged}},"net":{{json .HostConfig.NetworkMode}},"pid":{{json .HostConfig.PidMode}},'
          '"mem":{{json .HostConfig.Memory}},"pids":{{json .HostConfig.PidsLimit}},"log":{{json .HostConfig.LogConfig}},'
          '"restart":{{json .HostConfig.RestartPolicy.Name}},"health":{{json .State.Health}}}')


@controle(DOCKER_REGELS, "server", "infra", "docker inspect op de draaiende containers",
          rest="welke containers eigen diensten zijn en welke afwijking een genoteerde reden heeft; INFRA-27: docker exec <c> id -u; INFRA-26: geen poort 2375 of 2376")
def docker(ctx):
    code, ids = ctx.run(["docker", "ps", "-q"])
    if code != 0:
        return {r: (ONBEKEND, "docker ps lukte niet") for r in DOCKER_REGELS}
    ids = ids.split()[:MAX_CONTAINERS]
    if not ids:
        return {r: (NVT, "geen draaiende containers") for r in DOCKER_REGELS}
    code, uit = ctx.run(["docker", "inspect", "--format", OPMAAK] + ids, timeout=40)
    try:
        cs = [json.loads(r) for r in uit.splitlines() if r.startswith("{")]
    except ValueError:
        cs = []
    if code != 0 or not cs:
        return {r: (ONBEKEND, "docker inspect gaf geen bruikbare uitvoer") for r in DOCKER_REGELS}

    def publiek(c):
        return any((b.get("HostIp") or "0.0.0.0") in ("0.0.0.0", "::") and b.get("HostPort") not in ("80", "443")
                   for bs in (c["poorten"] or {}).values() for b in (bs or []))

    toetsen = {
        "INFRA-13": lambda c: not publiek(c),
        "INFRA-26": lambda c: not any("docker.sock" in str(m.get("Source")) for m in (c["mounts"] or [])),
        "INFRA-28": lambda c: "ALL" in [x.upper() for x in (c["capdrop"] or [])],
        "INFRA-29": lambda c: any("no-new-privileges" in o for o in (c["secopt"] or [])),
        "INFRA-30": lambda c: c["ro"] is True,
        "INFRA-31": lambda c: not c["priv"] and c["net"] != "host" and c["pid"] != "host",
        "INFRA-32": lambda c: bool(c["mem"]) and bool(c["pids"]) and c["pids"] > 0,
        "INFRA-33": lambda c: "max-size" in ((c["log"] or {}).get("Config") or {}) or (c["log"] or {}).get("Type") not in ("json-file", "local"),
        "INFRA-35": lambda c: c["restart"] not in ("", "no") and (c["health"] or {}).get("Status") == "healthy",
    }
    uit = {}
    for regel, f in toetsen.items():
        fout = [c["n"].lstrip("/") for c in cs if not f(c)]
        uit[regel] = (FAIL, "%d van %d: %s" % (len(fout), len(cs), ", ".join(fout[:8]))) if fout else (PASS, "%d containers" % len(cs))
    leeg = [c["n"].lstrip("/") for c in cs if str(c["user"]).split(":")[0] in ("", "0", "root")]
    uit["INFRA-27"] = (ONBEKEND, "Config.User leeg of root bij %d van %d (%s); meet met docker exec <c> id -u" % (len(leeg), len(cs), ", ".join(leeg[:8]))) if leeg else (PASS, "%d containers met een eigen gebruiker" % len(cs))
    return uit


# --- nginx op de host --------------------------------------------------------------
NGINX_REGELS = ["INFRA-43", "INFRA-44", "INFRA-45", "INFRA-46", "WEB-22"]


@controle(NGINX_REGELS, "server", "infra", "nginx -T op de host",
          rest="INFRA-43: handshake met een onbekende hostnaam mislukt; INFRA-44: zie de TLS-controle; INFRA-45: te grote aanvraag geeft 413; INFRA-46: lus per route toont 429; WEB-22: zie de kopregels")
def nginx(ctx):
    code, uit = _sudo(ctx, ["nginx", "-T"], timeout=30)
    if code != 0:
        return {r: (ONBEKEND, "nginx -T lukte niet op de host (%s); draait nginx in een container, meet dan met docker exec <container> nginx -T" % ("niet geinstalleerd" if code is None else "geen rechten")) for r in NGINX_REGELS}
    regels = [r.strip() for r in uit.splitlines() if not r.strip().startswith("#")]
    heeft = lambda pat: [r for r in regels if re.search(pat, r)]
    prot = heeft(r"^ssl_protocols\b")
    zwak = [r for r in prot if re.search(r"SSLv|TLSv1(\.1)?(\s|;)", r)]
    return {
        "INFRA-43": (PASS, "default_server met weigering aanwezig") if heeft(r"listen .*default_server") and heeft(r"ssl_reject_handshake\s+on|return\s+444") else (FAIL, "geen default_server met ssl_reject_handshake on of return 444"),
        "INFRA-44": (FAIL, "zwak protocol in: " + "; ".join(zwak[:3])) if zwak else ((PASS, "; ".join(sorted(set(prot)))) if prot else (FAIL, "ssl_protocols niet gezet")),
        "INFRA-45": (PASS, "%d regel(s) client_max_body_size" % len(heeft(r"^client_max_body_size"))) if heeft(r"^client_max_body_size") and heeft(r"^client_(header|body)_timeout") else (FAIL, "client_max_body_size of client_*_timeout niet expliciet gezet"),
        "INFRA-46": (PASS, "limit_req en limit_req_status 429 aanwezig") if heeft(r"^limit_req\s") and heeft(r"^limit_req_status\s+429") else (FAIL, "limit_req of limit_req_status 429 ontbreekt"),
        "WEB-22": (PASS, "server_tokens off") if heeft(r"^server_tokens\s+off") else (FAIL, "server_tokens off ontbreekt"),
    }
