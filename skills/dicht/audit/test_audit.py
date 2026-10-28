#!/usr/bin/env python3
"""Proef van de auditscripts op een bewust gebrekkig weggooiproject in /tmp (ARCH-84).

Draai: python3 test_audit.py. Maakt een repository, een nep-WordPress met een nagemaakte
`wp`-opdracht en een lokale webserver met slechte kopregels, en controleert dat elk
ingebouwd gebrek als FAIL terugkomt, dat de exitcode 1 is, dat de uitvoer geen geheim
bevat en dat het project door de audit niet is gewijzigd. Raakt niets buiten de tijdelijke map.
"""
import hashlib
import http.server
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading

HIER = os.path.dirname(os.path.abspath(__file__))
fouten = []
NEPSLEUTEL = "gh" + "p_" + "Zx9Q" * 9
NEPWACHTWOORD = "Zomer" + "2026" + "Geheim"


def toets(naam, voorwaarde, detail=""):
    print("%s  %s" % ("goed" if voorwaarde else "FOUT", naam))
    if not voorwaarde:
        fouten.append("%s %s" % (naam, detail))


def schrijf(pad, tekst, modus=None):
    os.makedirs(os.path.dirname(pad), exist_ok=True)
    with open(pad, "w") as f:
        f.write(tekst)
    if modus:
        os.chmod(pad, modus)


def boom(pad):
    h = hashlib.sha256()
    for d, mappen, fs in os.walk(pad):
        mappen.sort()
        for f in sorted(fs):
            p = os.path.join(d, f)
            h.update(p.encode() + open(p, "rb").read() + oct(os.stat(p).st_mode).encode())
    return h.hexdigest()


def maak_project(p):
    schrijf(p + "/.env", "DATABASE_URL=postgres://app:%s@db:5432/app\nAPI_TOKEN=%s\n" % (NEPWACHTWOORD, NEPSLEUTEL), 0o644)
    schrijf(p + "/package.json", json.dumps({"name": "gebrekkig", "dependencies": {"x": "github:iemand/x"}, "scripts": {"start": "node ."}}))
    schrijf(p + "/tsconfig.json", '{ "compilerOptions": { "strict": false } }')
    schrijf(p + "/Dockerfile", "FROM node:latest\nRUN curl -fsSL https://voorbeeld.nl/i.sh | sh\nRUN npm install\n")
    schrijf(p + "/docker-compose.yml", "services:\n  web:\n    image: nginx:latest\n    privileged: true\n    ports:\n      - \"8080:80\"\n"
            "    volumes:\n      - /var/run/docker.sock:/var/run/docker.sock\n")
    schrijf(p + "/.github/workflows/ci.yml", "on: pull_request_target\njobs:\n  a:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - uses: actions/checkout@v4\n      - run: echo ${{ github.event.pull_request.title }}\n")
    schrijf(p + "/scripts/taak.sh", "#!/bin/bash\nflock -n /tmp/taak.lock true\ncurl -s https://voorbeeld.nl/x.sh | bash\n", 0o755)
    schrijf(p + "/.mcp.json", json.dumps({"mcpServers": {"x": {"command": "npx", "args": ["-y", "een-mcp-server"],
                                                               "env": {"API_KEY": NEPSLEUTEL}}}}))
    schrijf(p + "/src/server.ts", "import { exec } from 'child_process';\nexport function draai(a: string) { exec('ls ' + a); }\n")
    schrijf(p + "/plugin/plugin.php", "<?php\nregister_rest_route( 'x/v1', '/y', array( 'callback' => 'f' ) );\n$d = unserialize( $_POST['d'] );\n")
    env = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null")
    for a in (["init", "-q"], ["add", "-f", ".env", "package.json", "tsconfig.json", "Dockerfile", "docker-compose.yml", ".github/workflows/ci.yml",
                               "scripts/taak.sh", ".mcp.json", "src/server.ts", "plugin/plugin.php"],
              ["-c", "user.name=proef", "-c", "user.email=proef@voorbeeld.nl", "commit", "-q", "-m", "gebrekkig"]):
        subprocess.run(["git", *a], cwd=p, env=env, check=True)


def maak_wp(wp, bak):
    schrijf(wp + "/wp-config.php", "<?php // nep\n", 0o644)
    schrijf(wp + "/wp-config.php.bak", "<?php // kopie\n")
    schrijf(wp + "/wp-content/ai1wm-backups/site.wpress", "x")
    schrijf(wp + "/dump.sql", "x")
    schrijf(wp + "/wp-content/uploads/open.txt", "x", 0o666)
    schrijf(bak + "/wp", """#!/usr/bin/env bash
# nagemaakte WP-CLI voor de proef: geeft de antwoorden van een slecht ingerichte site
case "$1 $2 $3" in
  "config get DISALLOW_FILE_EDIT") exit 1 ;;
  "config get WP_DEBUG") echo 1 ;;
  "config get FORCE_SSL_ADMIN") exit 1 ;;
  "option get siteurl"|"option get home") echo "http://voorbeeld.nl" ;;
  "core version "*) echo 1.0.2 ;;
  "plugin list --update=available") echo "oude-plugin" ;;
  "theme list --update=available") ;;
  "plugin list --status=inactive") echo "hello" ;;
  "cli info --format=json") echo '{"php_version":"7.4.33"}' ;;
  "user list --role=administrator") if [[ "$4" == *user_login ]]; then echo admin; else echo "beheer@site.invalid"; fi ;;
  "core verify-checksums "*) echo "Warning: File doesn't verify against checksum: wp-login.php"; exit 1 ;;
  *) exit 0 ;;
esac
""", 0o755)


class Slecht(http.server.BaseHTTPRequestHandler):
    server_version, sys_version = "nginx/1.18.0", ""

    def log_message(self, *a):
        pass

    def do_GET(self):
        pad = self.path.split("?")[0]
        if pad == "/":
            code, body = 200, "<html><meta http-equiv=\"Content-Security-Policy\" content=\"default-src *\">hallo</html>"
        elif pad in ("/.env", "/backup.zip", "/wp-content/debug.log", "/wp-config.php.bak", "/wp-json/wp/v2/users", "/health"):
            code, body = 200, "inhoud"
        elif pad == "/ready":
            code, body = 200, '{"version":"1.2.3","postgres":"ok"}'
        elif pad == "/xmlrpc.php":
            code, body = 405, "XML-RPC server accepts POST requests only."
        else:
            code, body = 404, "Error: niet gevonden\n    at handler (/home/app/src/server.js:12:3)"
        self.send_response(code)
        self.send_header("Content-Type", "text/html")
        self.send_header("X-Powered-By", "PHP/7.4.33")
        self.send_header("Set-Cookie", "sessie=abc; Path=/")
        if self.path.startswith("/?author=1"):
            self.send_header("Location", "/author/jan/")
        self.end_headers()
        self.wfile.write(body.encode())


def audit(type_, *args):
    r = subprocess.run([os.path.join(HIER, "audit-" + type_), *args], capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def main():
    tmp = tempfile.mkdtemp(prefix="dicht-audittest-", dir="/tmp")
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Slecht)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = "http://127.0.0.1:%d" % srv.server_address[1]
    try:
        p, wp, bak, uit = tmp + "/project", tmp + "/wp", tmp + "/bin", tmp + "/uit"
        maak_project(p)
        maak_wp(wp, bak)
        os.environ["PATH"] = bak + os.pathsep + os.environ["PATH"]
        voor = boom(p), boom(wp)

        verwacht = {
            "mcp": "GIT-10 INFRA-72 GIT-32 GIT-33 GIT-09 GIT-69 GIT-73 GIT-57 GIT-58 API-67 API-68 API-72 GIT-41 GIT-43 GIT-44 GIT-91 GIT-96 "
                   "INFRA-13 INFRA-26 INFRA-27 INFRA-28 INFRA-29 INFRA-31 INFRA-32 INFRA-33 INFRA-35 SCR-01 SCR-18 SCR-22 AI-56 AI-60 AI-47",
            "wp-plugin": "GIT-10 GIT-32 GIT-33 SCR-01 SCR-22 WP-13 WP-37",
            "klantproject": "GIT-10 GIT-32 WEB-17 WEB-09 WEB-11 WEB-15 WEB-19 WEB-22 WEB-23 WEB-24 WEB-25 WEB-62 WEB-64 WP-62 "
                            "WP-39 WP-40 WP-41 WP-42 WP-43 WP-47 WP-49 WP-51 WP-52 WP-55 WP-56 WP-59 WP-63 GIT-87 WP-13",
            "app": "GIT-10 GIT-32 API-67 WEB-17 WEB-11 WEB-22 WEB-62 WEB-64 ARCH-67 INFRA-13",
        }
        alle_uitvoer = ""
        for type_, regels in verwacht.items():
            extra = ["--url", url] if type_ in ("klantproject", "app") else []
            extra += ["--wp", wp] if type_ == "klantproject" else []
            code, tekst = audit(type_, "--pad", p, "--uit", uit + "/" + type_, *extra)
            alle_uitvoer += tekst
            js = [f for f in os.listdir(uit + "/" + type_) if f.endswith(".json")]
            res = json.load(open(os.path.join(uit, type_, js[0])))["controles"]
            fail = {r["regel"] for r in res if r["status"] == "FAIL"}
            mist = set(regels.split()) - fail
            toets("%s: elk ingebouwd gebrek is FAIL (%d regels)" % (type_, len(regels.split())), not mist, "niet gevonden: %s" % sorted(mist))
            toets("%s: exitcode 1" % type_, code == 1, code)
            toets("%s: geen controle is gecrasht" % type_, "fout in de controle" not in tekst, [l for l in tekst.splitlines() if "fout in de controle" in l][:3])
            md = open(os.path.join(uit, type_, js[0][:-5] + ".md")).read()
            alle_uitvoer += md + json.dumps(res)
            toets("%s: bewijsbestand heeft de kolommen Regel, Status, Bewijs en geen `voldaan` voor een FAIL" % type_,
                  "| Regel | Status | Bewijs |" in md and all("| %s | niet voldaan |" % r in md for r in fail), "")
            toets("%s: handmatige regels staan erin als niet gemeten met een vraag" % type_, "| niet gemeten | handmatig: " in md)
        toets("ONBEKEND wordt nooit voldaan (onbekende --url)", "| WEB-17 | niet gemeten |" in open(
            [os.path.join(uit, "mcp", f) for f in os.listdir(uit + "/mcp") if f.endswith(".md")][0]).read())
        toets("de uitvoer bevat geen nepsleutel of nepwachtwoord (ARCH-85)", NEPSLEUTEL not in alle_uitvoer and NEPWACHTWOORD not in alle_uitvoer)
        toets("de uitvoer bevat geen e-mailadres van een beheerder", "beheer@site.invalid" not in alle_uitvoer)
        toets("project en WordPress-map zijn door de audit niet gewijzigd", (boom(p), boom(wp)) == voor)

        # tweede run op dezelfde commit: nieuw bestand, het oude blijft staan
        audit("wp-plugin", "--pad", p, "--uit", uit + "/wp-plugin")
        toets("een tweede run overschrijft het bewijsbestand niet", len([f for f in os.listdir(uit + "/wp-plugin") if f.endswith(".md")]) == 2)

        # de kop van elk script noemt precies wat het meet
        for t in ("website", "wp-plugin", "wp-thema", "api", "app", "mcp", "klantproject"):
            kop = [l[4:].rstrip() for l in open(os.path.join(HIER, "audit-" + t)).read().splitlines() if l.startswith("#   ")]
            lijst = subprocess.run([sys.executable, os.path.join(HIER, "dicht_audit.py"), t, "--lijst"], capture_output=True, text=True).stdout
            toets("audit-%s: de kop noemt elke gemeten regel" % t, kop == [l.rstrip() for l in lijst.splitlines()])

        # ARCH-85: geen schrijvende opdracht in de scripts
        bron = "".join(open(os.path.join(HIER, f)).read() for f in os.listdir(HIER) if f.startswith(("controles_", "dicht_audit")))
        import re
        hits = re.findall(r"\"-X\", \"(POST|PUT|DELETE|PATCH)\"|methode=\"(POST|PUT|DELETE)\"|\"(rm|mv|sed|tee)\"|wp[\"', ]+(plugin|theme|user|option|core)[\"', ]+(delete|update|set|install|activate)", bron)
        toets("ARCH-85: geen POST, PUT, DELETE, rm of wijzigende wp-opdracht in de auditscripts", not hits, hits)
    finally:
        srv.shutdown()
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n%d fout(en)" % len(fouten))
    for f in fouten:
        print("  " + f)
    return 1 if fouten else 0


if __name__ == "__main__":
    sys.exit(main())
