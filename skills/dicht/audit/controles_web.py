"""Controles van buitenaf (met --url): kopregels, bekende paden, TLS, DNS, health.

Alleen anonieme GET-aanvragen op wat een bezoeker mag opvragen, met een pauze en een
maximum per host (ARCH-85). Geen POST, geen payloads, geen inlogpogingen.
"""
import datetime
import re
import secrets

from dicht_audit import FAIL, ONBEKEND, PASS, controle

PADEN = [".git/config", ".env", "wp-config.php.bak", "backup.zip", "dump.sql", "wp-content/debug.log",
         "wp-content/ai1wm-backups/", "phpinfo.php"]    # de lijst uit WEB-64
LEK = re.compile(r"Traceback \(most recent|\bat .+\.(js|ts):\d+|SQLSTATE|Stack trace:|Fatal error:|/home/\w+/|/var/www/|node_modules/")


def _basis(ctx):
    """De vaste set aanvragen: homepage, een niet-bestaand pad en de http-variant."""
    if "basis" not in ctx.cache:
        nep = "/dicht-audit-bestaat-niet-" + secrets.token_hex(4)
        ctx.cache["basis"] = {"/": ctx.http(ctx.url + "/"), "404": ctx.http(ctx.url + nep),
                              "http": ctx.http("http://%s/" % ctx.host)}
    return ctx.cache["basis"]


def _kop(antwoord, naam):
    return "; ".join(antwoord[1].get(naam, []))


def _beide(ctx, naam, toets, wat):
    """Toetst een kopregel op de homepage en op de 404."""
    b = _basis(ctx)
    if b["/"][0] is None:
        return ONBEKEND, "homepage niet op te vragen (%s)" % b["/"][2]
    fout = [plek for plek in ("/", "404") if not toets(_kop(b[plek], naam))]
    waarde = _kop(b["/"], naam) or "ontbreekt"
    return (FAIL, "%s op %s: %s" % (wat, " en ".join(fout), waarde)) if fout else (PASS, "%s: %s" % (naam, waarde))


@controle("WEB-17", "web", "web", "HSTS op de homepage en op een 404", rest="de subdomeinen uit DNS zijn nagelopen op HTTPS")
def web17(ctx):
    def goed(v):
        m = re.search(r"max-age=(\d+)", v)
        return bool(m and int(m.group(1)) >= 31536000 and "includesubdomains" in v.lower())
    return _beide(ctx, "strict-transport-security", goed, "geen max-age van minstens 31536000 met includeSubDomains")


@controle("WEB-09", "web", "web", "nosniff en Content-Type met charset op de homepage en op een 404", rest="ook een API-route, een 500 en een statisch bestand")
def web09(ctx):
    b = _basis(ctx)
    if b["/"][0] is None:
        return ONBEKEND, "homepage niet op te vragen"
    fout = [p for p in ("/", "404") if "nosniff" not in _kop(b[p], "x-content-type-options").lower() or "charset=" not in _kop(b[p], "content-type").lower()]
    return (FAIL, "ontbreekt op " + " en ".join(fout)) if fout else (PASS, "nosniff en charset op beide")


@controle("WEB-11", "web", "web", "CSP met object-src none, base-uri none en een nonce of hash", rest="de pagina werkt in een Playwright-test zonder CSP-fouten in de console")
def web11(ctx):
    b = _basis(ctx)
    if b["/"][0] is None:
        return ONBEKEND, "homepage niet op te vragen"
    csp = _kop(b["/"], "content-security-policy")
    if not csp:
        return FAIL, "geen Content-Security-Policy-header"
    mist = [n for n, pat in (("object-src 'none'", r"object-src\s+'none'"), ("base-uri 'none'", r"base-uri\s+'none'"),
                             ("nonce of hash in script-src", r"script-src[^;]*'(nonce-|sha(256|384|512)-)")) if not re.search(pat, csp)]
    return (FAIL, "CSP mist: " + ", ".join(mist)) if mist else (PASS, "CSP met de drie onderdelen")


@controle("WEB-15", "web", "web", "CSP komt als header en niet als meta-tag", dekking="volledig")
def web15(ctx):
    b = _basis(ctx)
    if b["/"][0] is None:
        return ONBEKEND, "homepage niet op te vragen"
    meta = re.search(r"http-equiv=[\"']Content-Security-Policy", b["/"][2], re.I)
    if not _kop(b["/"], "content-security-policy"):
        return FAIL, "geen CSP-header" + (" (wel een meta-tag)" if meta else "")
    return (ONBEKEND, "header aanwezig, maar ook een meta-tag: bewust en gedocumenteerd?") if meta else (PASS, "header aanwezig, geen meta-tag")


@controle("WEB-19", "web", "web", "Referrer-Policy op een gewone pagina", rest="no-referrer op de resetpagina; die laadt geen bronnen van derden")
def web19(ctx):
    return _beide(ctx, "referrer-policy", bool, "geen Referrer-Policy")


@controle("WEB-20", "web", "web", "Permissions-Policy aanwezig", dekking="volledig")
def web20(ctx):
    b = _basis(ctx)
    if b["/"][0] is None:
        return ONBEKEND, "homepage niet op te vragen"
    v = _kop(b["/"], "permissions-policy")
    return (PASS, v) if v else (FAIL, "geen Permissions-Policy")


@controle("WEB-22", "web", "web", "geen versie of verouderde kopregel in de respons", dekking="volledig")
def web22(ctx):
    b = _basis(ctx)
    if b["/"][0] is None:
        return ONBEKEND, "homepage niet op te vragen"
    fout = ["%s: %s" % (n, _kop(b["/"], n)) for n in ("x-powered-by", "x-xss-protection", "public-key-pins", "expect-ct") if _kop(b["/"], n)]
    if re.search(r"\d", _kop(b["/"], "server")):
        fout.append("server: " + _kop(b["/"], "server"))
    return (FAIL, "; ".join(fout)) if fout else (PASS, "server: %s" % (_kop(b["/"], "server") or "geen"))


@controle("WEB-24", "web", "web", "frame-ancestors in de CSP-header op de homepage en op een 404", rest="ook een API-respons; een testpagina met een iframe toont een geblokkeerd frame")
def web24(ctx):
    return _beide(ctx, "content-security-policy", lambda v: "frame-ancestors" in v, "geen frame-ancestors")


@controle("WEB-23", "web", "web", "de verplichte kopregels staan op elke gemeten respons", rest="minimaal vijf URL's: ook een statisch bestand en een API-route")
def web23(ctx):
    b = _basis(ctx)
    if b["/"][0] is None:
        return ONBEKEND, "homepage niet op te vragen"
    nodig = ("strict-transport-security", "x-content-type-options", "content-security-policy", "referrer-policy")
    rijen = []
    for plek in ("/", "404"):
        mist = [n for n in nodig if n not in b[plek][1]]
        rijen.append("%s (%s): %s" % (plek, b[plek][0], "alle vier" if not mist else "mist " + ", ".join(mist)))
    rijen.append("http: %s naar %s" % (b["http"][0], _kop(b["http"], "location") or "geen Location"))
    slecht = any("mist" in r for r in rijen) or b["http"][0] not in (301, 308) or not _kop(b["http"], "location").startswith("https://")
    return (FAIL if slecht else PASS), "; ".join(rijen)


@controle("WEB-25", "web", "web", "elke cookie op de homepage heeft Secure", rest="de login-respons: sessiecookie met HttpOnly, SameSite en __Host-; document.cookie toont hem niet")
def web25(ctx):
    b = _basis(ctx)
    if b["/"][0] is None:
        return ONBEKEND, "homepage niet op te vragen"
    cookies = b["/"][1].get("set-cookie", [])
    zonder = [c.split("=")[0] for c in cookies if not re.search(r";\s*secure", c, re.I)]
    if zonder:
        return FAIL, "zonder Secure: " + ", ".join(zonder[:6])
    return (PASS, "%d cookie(s) met Secure" % len(cookies)) if cookies else (ONBEKEND, "de homepage zet geen cookie; meet de login-respons")


@controle("WEB-62", "web", "web", "een 404 toont geen stacktrace, query of pad", rest="forceer per applicatie ook ongeldige JSON en een te lange waarde; het referentienummer staat in het serverlog")
def web62(ctx):
    b = _basis(ctx)
    if b["404"][0] is None:
        return ONBEKEND, "aanvraag mislukt"
    m = LEK.search(b["404"][2])
    return (FAIL, "de foutpagina bevat een intern detail (patroon %s)" % m.re.pattern[:20]) if m else (PASS, "status %s, geen intern detail" % b["404"][0])


@controle(["WEB-64", "WP-62"], "web", "web", "bekende paden geven 403 of 404",
          rest="een map zonder index geeft geen lijst; WP-62: ook de zoekopdracht op de server naar sql, zip en tar")
def web64(ctx):
    b = _basis(ctx)
    if b["404"][0] is None:
        return {r: (ONBEKEND, "aanvraag mislukt") for r in ("WEB-64", "WP-62")}
    fout, vaag = [], []
    for p in PADEN:
        code, _, body = ctx.http("%s/%s" % (ctx.url, p))
        if code is None:
            vaag.append("%s (%s)" % (p, body))
        elif code in (403, 404, 410):
            continue
        elif code == b["404"][0] and abs(len(body) - len(b["404"][2])) <= max(50, len(body) // 20):
            vaag.append("%s geeft %s, net als een niet-bestaand pad" % (p, code))
        elif code in (301, 302, 307, 308):
            vaag.append("%s stuurt door (%s)" % (p, code))
        else:
            fout.append("%s %s" % (code, p))
    if fout:
        res = (FAIL, "bereikbaar: " + ", ".join(fout))
    elif vaag:
        res = (ONBEKEND, "; ".join(vaag[:4]))
    else:
        res = (PASS, "%d paden geven 403 of 404" % len(PADEN))
    return {"WEB-64": res, "WP-62": res}


@controle("INFRA-65", "web", "infra", "security.txt met Contact en een geldige Expires", dekking="volledig")
def infra65(ctx):
    code, _, body = ctx.http(ctx.url + "/.well-known/security.txt")
    if code != 200:
        return FAIL, "status %s" % code
    m = re.search(r"^Expires:\s*(\d{4}-\d{2}-\d{2})", body, re.M | re.I)
    if not re.search(r"^Contact:", body, re.M | re.I) or not m:
        return FAIL, "Contact of Expires ontbreekt"
    return (PASS, "Expires " + m.group(1)) if m.group(1) > datetime.date.today().isoformat() else (FAIL, "verlopen op " + m.group(1))


# --- TLS ------------------------------------------------------------------------
def _s_client(ctx, vlag):
    return ctx.run(["openssl", "s_client", "-connect", "%s:443" % ctx.host, "-servername", ctx.host, vlag,
                    "-cipher", "DEFAULT@SECLEVEL=0"], timeout=15, invoer="\n")


@controle("INFRA-44", "web", "infra", "TLS 1.0 en 1.1 worden geweigerd, 1.2 of 1.3 werkt", rest="nginx -T toont de regels; een scan met testssl.sh of internet.nl toont geen zwakke suites")
def infra44(ctx):
    uit = {}
    for vlag in ("-tls1", "-tls1_1", "-tls1_2", "-tls1_3"):
        code, tekst = _s_client(ctx, vlag)
        if code is None or re.search(r"no protocols available|unknown option|Option unknown", tekst):
            return ONBEKEND, "openssl kan %s hier niet proberen" % vlag
        uit[vlag] = bool(re.search(r"Cipher is (?!\(NONE\))", tekst)) and "Protocol  : TLSv1" in tekst
    oud = [v for v in ("-tls1", "-tls1_1") if uit[v]]
    if oud:
        return FAIL, "de server accepteert " + " en ".join(oud)
    return (PASS, "1.0 en 1.1 geweigerd; 1.2 %s, 1.3 %s" % ("ja" if uit["-tls1_2"] else "nee", "ja" if uit["-tls1_3"] else "nee")) if uit["-tls1_2"] or uit["-tls1_3"] else (ONBEKEND, "geen enkele TLS-versie gaf een verbinding")


@controle("INFRA-52", "web", "infra", "het certificaat is nog minstens 14 dagen geldig", rest="de bewaking toont per hostnaam de vervaldatum en de drempel; een testmelding is aangekomen")
def infra52(ctx):
    code, tekst = ctx.run(["openssl", "s_client", "-connect", "%s:443" % ctx.host, "-servername", ctx.host], timeout=15, invoer="\n")
    m = re.search(r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", tekst, re.S)
    if not m:
        return ONBEKEND, "geen certificaat ontvangen"
    code, eind = ctx.run(["openssl", "x509", "-noout", "-enddate"], invoer=m.group(0))
    try:
        d = datetime.datetime.strptime(eind.split("=", 1)[1].strip(), "%b %d %H:%M:%S %Y %Z")
    except (IndexError, ValueError):
        return ONBEKEND, "vervaldatum niet te lezen"
    dagen = (d - datetime.datetime.utcnow()).days
    return (PASS if dagen >= 14 else FAIL), "verloopt %s (%d dagen)" % (d.date().isoformat(), dagen)


# --- DNS ------------------------------------------------------------------------
def _dig(ctx, soort, naam):
    code, uit = ctx.run(["dig", "+short", "+time=5", "+tries=1", soort, naam])
    return None if code != 0 else [r.strip() for r in uit.splitlines() if r.strip() and not r.startswith(";")]


@controle("INFRA-56", "dns", "infra", "precies één SPF-record dat eindigt op -all", rest="hooguit tien lookups (ook genest); een echte mail per verzendroute toont spf=pass")
def infra56(ctx):
    txt = _dig(ctx, "TXT", ctx.domein)
    if txt is None:
        return ONBEKEND, "dig lukte niet"
    spf = [t.replace('" "', "").strip('"') for t in txt if "v=spf1" in t]
    if len(spf) != 1:
        return FAIL, "%d SPF-records op %s" % (len(spf), ctx.domein)
    return (PASS, spf[0]) if spf[0].rstrip().endswith("-all") else (FAIL, "eindigt niet op -all: " + spf[0])


@controle("INFRA-58", "dns", "infra", "DMARC-record met een beleid", rest="bij een extern rua-adres bestaat het autorisatierecord; er is een rapport van de laatste zeven dagen")
def infra58(ctx):
    txt = _dig(ctx, "TXT", "_dmarc." + ctx.domein)
    if txt is None:
        return ONBEKEND, "dig lukte niet"
    rec = [t.replace('" "', "").strip('"') for t in txt if "v=DMARC1" in t]
    if len(rec) != 1 or not re.search(r"\bp=(none|quarantine|reject)", rec[0]):
        return FAIL, "geen geldig DMARC-record op _dmarc.%s" % ctx.domein
    return PASS, rec[0]


@controle("INFRA-53", "dns", "infra", "CAA-record aanwezig", rest="de CA van de hostingpartij staat erin; een vernieuwing daarna is geslaagd")
def infra53(ctx):
    caa = _dig(ctx, "CAA", ctx.domein)
    if caa is None:
        return ONBEKEND, "dig lukte niet"
    return (PASS, "; ".join(caa[:4])) if caa else (FAIL, "geen CAA-record op %s" % ctx.domein)


# --- API ------------------------------------------------------------------------
@controle("ARCH-67", "api", "architectuur", "/health antwoordt en /ready geeft van buiten geen details",
          rest="op 127.0.0.1 geven /health en /ready 200; met de database gestopt blijft /health 200 en geeft /ready 503; de Docker-healthcheck heeft interval, timeout, retries en start_period")
def arch67(ctx):
    code, _, body = ctx.http(ctx.url + "/health")
    if code is None:
        return ONBEKEND, "aanvraag mislukt"
    if code != 200:
        return ONBEKEND, "/health geeft %s van buiten; meet op 127.0.0.1" % code
    rcode, _, rbody = ctx.http(ctx.url + "/ready")
    lekt = rcode == 200 and re.search(r"version|postgres|redis|database|\d+\.\d+\.\d+", rbody, re.I)
    return (FAIL, "/ready geeft van buiten versie of namen van onderdelen") if lekt else (PASS, "/health 200, /ready %s zonder details" % rcode)
