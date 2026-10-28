"""Controles voor WordPress: de site (WP-CLI en anonieme aanvragen) en eigen plugin- of themacode.

WP-CLI draait met --skip-plugins --skip-themes (WP-69), als het account van de site (WP-68),
en alleen met opdrachten die lezen. Namen en adressen van gebruikers komen niet in de uitvoer.
"""
import json
import re
import shlex

from dicht_audit import FAIL, NVT, ONBEKEND, PASS, controle

WP_VLAGGEN = ["--skip-plugins", "--skip-themes", "--no-color"]


def _op_site(ctx, args, timeout=40):
    """Draait een opdracht in de map van de WordPress-installatie, lokaal of via ssh."""
    if ctx.wp_ssh:
        doel, _, pad = ctx.wp_ssh.partition(":")
        # de opdracht achter ssh is tekst voor een tweede shell (SCR-10): elk deel apart quoten
        return ctx.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", doel, "--",
                        "cd %s && %s" % (shlex.quote(pad), " ".join(shlex.quote(a) for a in args))], timeout=timeout)
    if ctx.wp:
        return ctx.run(args, timeout=timeout, cwd=ctx.wp)
    return None, "geen --wp of --wp-ssh opgegeven"


def _wp(ctx, *args, timeout=40):
    code, uit = _op_site(ctx, ["wp", *args, *WP_VLAGGEN], timeout)
    if code is not None and "allow-root" in uit:
        return None, "WP-CLI weigert als root (WP-68): draai als het account van de site"
    return code, uit


def _geen_cli(ctx):
    return not (ctx.wp or ctx.wp_ssh)


def _config(ctx, naam):
    code, uit = _wp(ctx, "config", "get", naam)
    return None if code is None else (uit.strip().lower() if code == 0 else "")


@controle("WP-39", "wpsite", "wordpress", "DISALLOW_FILE_EDIT staat aan", rest="wp_is_file_mod_allowed( 'automatic_updater' ) is true, tenzij updates buiten WordPress lopen")
def wp39(ctx):
    v = _config(ctx, "DISALLOW_FILE_EDIT")
    if v is None:
        return ONBEKEND, "WP-CLI niet beschikbaar"
    return (PASS, "DISALLOW_FILE_EDIT = " + v) if v in ("1", "true") else (FAIL, "DISALLOW_FILE_EDIT is niet gezet of onwaar")


@controle("WP-40", "wpsite", "wordpress", "WP_DEBUG uit en debug.log onbereikbaar", rest="een opzettelijke fout op een testkopie toont de bezoeker geen PHP-melding")
def wp40(ctx):
    delen, status = [], PASS
    v = _config(ctx, "WP_DEBUG")
    if v is None:
        status = ONBEKEND
        delen.append("WP_DEBUG niet gemeten (geen WP-CLI)")
    elif v in ("1", "true"):
        return FAIL, "WP_DEBUG staat aan"
    else:
        delen.append("WP_DEBUG uit")
    if ctx.url:
        code, _, _ = ctx.http(ctx.url + "/wp-content/debug.log")
        if code not in (403, 404):
            return (FAIL, "debug.log geeft %s" % code) if code == 200 else (ONBEKEND, "debug.log geeft %s" % code)
        delen.append("debug.log %s" % code)
    else:
        status = ONBEKEND
        delen.append("debug.log niet gemeten (geen --url)")
    return status, "; ".join(delen)


@controle("WP-41", "wpsite", "wordpress", "wp-config.php is onleesbaar voor anderen en heeft geen kopieën",
          rest="de eigenaar is het account van de site")
def wp41(ctx):
    if _geen_cli(ctx):
        return ONBEKEND, "geen --wp of --wp-ssh opgegeven"
    code, uit = _op_site(ctx, ["stat", "-c", "%a", "wp-config.php"])
    if code != 0:
        return ONBEKEND, "stat lukte niet"
    if uit.strip() not in ("400", "440", "600"):
        return FAIL, "wp-config.php heeft modus " + uit.strip()
    code, lijst = _op_site(ctx, ["find", ".", "-maxdepth", "1", "-iname", "wp-config*", "-not", "-name", "wp-config.php", "-not", "-name", "wp-config-sample.php"])
    if code == 0 and lijst.strip():
        return FAIL, "kopie in de webroot: " + ", ".join(lijst.split()[:5])
    if ctx.url:
        open_ = [e for e in (".bak", ".old", ".save", ".orig", ".txt", "~", ".swp") if ctx.http("%s/wp-config.php%s" % (ctx.url, e))[0] not in (403, 404)]
        if open_:
            return FAIL, "variant bereikbaar of onduidelijk: wp-config.php" + ", ".join(open_)
        return PASS, "modus %s, geen kopie, zeven varianten geven 403 of 404" % uit.strip()
    return ONBEKEND, "modus %s en geen kopie; de varianten zijn niet opgevraagd (geen --url)" % uit.strip()


@controle("WP-42", "wpsite", "wordpress", "geen bestand of map schrijfbaar voor anderen (tot vier niveaus diep)", rest="dieper dan vier niveaus; find . ! -user <account> is leeg")
def wp42(ctx):
    if _geen_cli(ctx):
        return ONBEKEND, "geen --wp of --wp-ssh opgegeven"
    code, uit = _op_site(ctx, ["find", ".", "-maxdepth", "4", "-perm", "-o+w", "-not", "-type", "l"], timeout=60)
    if code != 0:
        return ONBEKEND, "find lukte niet"
    n = len(uit.splitlines())
    return (FAIL, "%d schrijfbaar voor anderen, bijvoorbeeld %s" % (n, ", ".join(uit.splitlines()[:3]))) if n else (PASS, "geen treffer")


@controle("WP-43", "wpsite", "wordpress", "HTTPS voor de site en voor wp-admin", rest="www en het hoofddomein 10 tot 20 keer gemeten met een volledige GET (WP-65)")
def wp43(ctx):
    delen, status = [], PASS
    if not _geen_cli(ctx):
        for optie in ("siteurl", "home"):
            code, uit = _wp(ctx, "option", "get", optie)
            if code != 0:
                status = ONBEKEND
            elif not uit.strip().startswith("https://"):
                return FAIL, "%s begint niet met https://" % optie
        v = _config(ctx, "FORCE_SSL_ADMIN")
        if v not in ("1", "true"):
            return FAIL, "FORCE_SSL_ADMIN is niet waar"
        delen.append("siteurl, home en FORCE_SSL_ADMIN in orde")
    else:
        status = ONBEKEND
        delen.append("opties niet gemeten (geen WP-CLI)")
    if ctx.url:
        code, koppen, _ = ctx.http("http://%s/wp-login.php" % ctx.host)
        if code != 301 or not "; ".join(koppen.get("location", [])).startswith("https://"):
            return FAIL, "http://.../wp-login.php geeft %s en geen 301 naar https" % code
        delen.append("wp-login.php 301 naar https")
    else:
        status = ONBEKEND
    return status, "; ".join(delen)


@controle("WP-47", "wpsite", "wordpress", "de kernversie is volgens wordpress.org niet onveilig", rest="automatic_updater_disabled geeft false")
def wp47(ctx):
    code, versie = _wp(ctx, "core", "version")
    if code != 0:
        return ONBEKEND, "wp core version lukte niet"
    versie = versie.strip().splitlines()[-1]
    code2, body = ctx.run(["curl", "-s", "--max-time", "15", "https://api.wordpress.org/core/stable-check/1.0/"], timeout=20)
    try:
        oordeel = json.loads(body).get(versie)
    except ValueError:
        return ONBEKEND, "versie %s; stable-check niet te lezen" % versie
    if oordeel == "insecure":
        return FAIL, "versie %s is insecure" % versie
    return (PASS, "versie %s is %s" % (versie, oordeel)) if oordeel in ("latest", "outdated") else (ONBEKEND, "versie %s staat niet in stable-check" % versie)


@controle("WP-49", "wpsite", "wordpress", "geen plugin of thema met een openstaande update", rest="per openstaande update een datum en reden; de termijnen staan in de werkafspraak; WP-48 is gedaan")
def wp49(ctx):
    namen = []
    for soort in ("plugin", "theme"):
        code, uit = _wp(ctx, soort, "list", "--update=available", "--field=name")
        if code != 0:
            return ONBEKEND, "wp %s list lukte niet" % soort
        namen += ["%s %s" % (soort, n) for n in uit.split()]
    return (FAIL, "%d update(s) open: %s" % (len(namen), ", ".join(namen[:8]))) if namen else (PASS, "geen openstaande updates")


@controle("WP-51", "wpsite", "wordpress", "geen inactieve plugins", rest="thema's: hooguit het bovenliggende thema en één standaardthema")
def wp51(ctx):
    code, uit = _wp(ctx, "plugin", "list", "--status=inactive", "--field=name")
    if code != 0:
        return ONBEKEND, "wp plugin list lukte niet"
    return (FAIL, "inactief: " + ", ".join(uit.split()[:10])) if uit.split() else (PASS, "geen inactieve plugins")


@controle("WP-52", "wpsite", "wordpress", "de PHP-versie van de opdrachtregel krijgt nog fixes volgens php.net", rest="de versie die de webserver gebruikt (Site Health of het hostingpaneel)")
def wp52(ctx):
    code, uit = _op_site(ctx, ["wp", "cli", "info", "--format=json"])
    try:
        versie = re.match(r"\d+\.\d+", json.loads(uit[uit.index("{"):])["php_version"]).group(0)
    except (ValueError, KeyError, AttributeError, TypeError):
        return ONBEKEND, "wp cli info lukte niet"
    code, body = ctx.run(["curl", "-s", "--max-time", "15", "https://www.php.net/releases/active.php"], timeout=20)
    try:
        actief = [v for takken in json.loads(body).values() for v in takken]
    except (ValueError, AttributeError):
        return ONBEKEND, "PHP %s; de lijst van php.net is niet te lezen" % versie
    return (PASS, "PHP %s staat in de actieve lijst (%s)" % (versie, ", ".join(sorted(actief)))) if versie in actief else (FAIL, "PHP %s krijgt geen fixes meer (actief: %s)" % (versie, ", ".join(sorted(actief))))


@controle("WP-55", "wpsite", "wordpress", "xmlrpc.php is dicht op de server",
          rest="de regel vraagt een POST met system.listMethods die 403 geeft; het auditscript stuurt geen POST (ARCH-85) en meet alleen de GET")
def wp55(ctx):
    if not ctx.url:
        return ONBEKEND, "geen --url opgegeven"
    code, _, body = ctx.http(ctx.url + "/xmlrpc.php")
    if code in (403, 404):
        return PASS, "GET geeft %s" % code
    if code == 405 or "XML-RPC server accepts POST requests only" in body:
        return FAIL, "xmlrpc.php is bereikbaar (GET geeft %s)" % code
    return ONBEKEND, "GET geeft %s" % code


@controle("WP-56", "wpsite", "wordpress", "geen gebruikersnamen via REST, ?author=1 of een account admin",
          rest="een inlogpoging en wachtwoord vergeten geven dezelfde melding voor een bestaande en een niet-bestaande naam")
def wp56(ctx):
    delen, status = [], PASS
    if ctx.url:
        code, _, _ = ctx.http(ctx.url + "/wp-json/wp/v2/users")
        if code == 200:
            return FAIL, "/wp-json/wp/v2/users geeft 200"
        if code not in (401, 403):
            status = ONBEKEND
        delen.append("REST users %s" % code)
        code, koppen, _ = ctx.http(ctx.url + "/?author=1")
        loc = "; ".join(koppen.get("location", []))
        if "/author/" in loc:
            return FAIL, "?author=1 stuurt door naar een auteurspagina met een naam"
        delen.append("?author=1 %s" % code)
    else:
        status = ONBEKEND
        delen.append("anoniem niet gemeten (geen --url)")
    if not _geen_cli(ctx):
        code, uit = _wp(ctx, "user", "list", "--role=administrator", "--field=user_login")
        if code != 0:
            status = ONBEKEND
        elif "admin" in uit.split():
            return FAIL, "er is een beheerder met de naam admin"
        else:
            delen.append("geen beheerder met de naam admin")
    else:
        status = ONBEKEND
    return status, "; ".join(delen)


@controle("WP-59", "wpsite", "wordpress", "aantal beheerders en verdachte adressen", rest="de lijst komt overeen met de afgesproken lijst in het CRM; geen account van een vorig bureau")
def wp59(ctx):
    code, uit = _wp(ctx, "user", "list", "--role=administrator", "--field=user_email")
    if code != 0:
        return ONBEKEND, "wp user list lukte niet"
    adressen = uit.split()
    raar = sum(1 for a in adressen if re.search(r"\.(invalid|internal|local|test)$", a))
    if raar:
        return FAIL, "%d beheerder(s), waarvan %d met een adres op .invalid, .internal, .local of .test" % (len(adressen), raar)
    return ONBEKEND, "%d beheerder(s), geen verdacht adres; vergelijk de lijst met het CRM" % len(adressen)


@controle(["WP-63", "WP-62"], "wpsite", "wordpress", "geen back-up of dump in de webroot",
          rest="WP-63: een testbestand in de back-upmap geeft anoniem 403; WP-62: de lus over de bekende paden met een niet-bestaande naam ernaast")
def wp63(ctx):
    if _geen_cli(ctx):
        return {r: (ONBEKEND, "geen --wp of --wp-ssh opgegeven") for r in ("WP-63", "WP-62")}
    code, wpress = _op_site(ctx, ["find", "wp-content", "-maxdepth", "4", "-name", "*.wpress"], timeout=60)
    code2, rest = _op_site(ctx, ["find", ".", "-maxdepth", "3", "(", "-name", "*.sql*", "-o", "-name", "*.zip", "-o", "-name", "*.tar*", ")",
                                 "-not", "-path", "./wp-content/plugins/*", "-not", "-path", "./wp-content/themes/*"], timeout=60)
    def oordeel(c, uit, wat):
        if c != 0:
            return ONBEKEND, "find lukte niet"
        n = len(uit.splitlines())
        return (FAIL, "%d %s, bijvoorbeeld %s" % (n, wat, ", ".join(uit.splitlines()[:3]))) if n else (PASS, "geen " + wat)
    return {"WP-63": oordeel(code, wpress, ".wpress-bestanden"), "WP-62": oordeel(code2, rest, "sql-, zip- of tar-bestanden")}


@controle("GIT-87", "wpsite", "git", "core en plugins kloppen met de controlesommen van wordpress.org", dekking="volledig")
def git87(ctx):
    code, uit = _wp(ctx, "core", "verify-checksums", timeout=90)
    if code is None:
        return ONBEKEND, uit
    if code != 0:
        return FAIL, "core wijkt af: " + " ".join(uit.splitlines()[:2])
    code, uit = _wp(ctx, "plugin", "verify-checksums", "--all", timeout=120)
    if code is None:
        return ONBEKEND, "core klopt; plugins: " + uit
    return (PASS, "core en plugins kloppen") if code == 0 else (FAIL, "plugins wijken af of staan niet op wordpress.org: " + " ".join(uit.splitlines()[:2]))


# --- eigen plugin- of themacode -------------------------------------------------------
def _php(ctx):
    return [b for b in ctx.bestanden() if b.endswith(".php") and not b.startswith(("vendor/", "node_modules/", "tests/"))]


@controle("WP-08", "wpcode", "wordpress", "elk PHP-bestand weigert rechtstreeks uitvoeren", rest="de gemelde bestanden bevatten alleen klasse- of functiedefinities; Plugin Check meldt geen direct file access")
def wp08(ctx):
    php = _php(ctx)
    if not php:
        return NVT, "geen PHP-bestanden"
    zonder = [b for b in php if "ABSPATH" not in (ctx.lees(b) or "") and "WP_UNINSTALL_PLUGIN" not in (ctx.lees(b) or "")]
    return (ONBEKEND, "%d zonder ABSPATH, na te kijken: %s" % (len(zonder), ", ".join(zonder[:8]))) if zonder else (PASS, "%d bestand(en) met ABSPATH" % len(php))


@controle("WP-13", "wpcode", "wordpress", "elke REST-route heeft een permission_callback",
          rest="elke __return_true staat op de lijst met publieke routes; debug.log zonder melding na het laden van /wp-json/; per route een test met drie rollen")
def wp13(ctx):
    routes = callbacks = open_ = 0
    for b in _php(ctx):
        t = ctx.lees(b) or ""
        routes += len(re.findall(r"\bregister_rest_route\s*\(", t))
        callbacks += len(re.findall(r"['\"]permission_callback['\"]", t))
        open_ += len(re.findall(r"permission_callback['\"]\s*=>\s*['\"]__return_true", t))
    if not routes:
        return NVT, "geen register_rest_route"
    if callbacks < routes:
        return FAIL, "%d routes, %d permission_callback" % (routes, callbacks)
    return (ONBEKEND, "%d routes, waarvan %d met __return_true: staan die op de lijst met publieke routes?" % (routes, open_)) if open_ else (PASS, "%d routes, %d permission_callback, geen __return_true" % (routes, callbacks))


@controle("WP-26", "wpcode", "wordpress", "geen unserialize van invoer", dekking="volledig")
def wp26(ctx):
    hits = []
    for b in _php(ctx):
        for nr, regel in enumerate((ctx.lees(b) or "").splitlines(), 1):
            if re.search(r"\b(maybe_)?unserialize\(", regel) and "allowed_classes" not in regel:
                hits.append("%s:%d" % (b, nr))
    if not _php(ctx):
        return NVT, "geen PHP-bestanden"
    return (ONBEKEND, "%d treffer(s), per treffer aantonen dat een gebruiker de waarde niet kan vullen: %s" % (len(hits), ", ".join(hits[:6]))) if hits else (PASS, "geen unserialize zonder allowed_classes")


@controle("WP-37", "wpcode", "wordpress", "PHPCS- en PHPStan-configuratie aanwezig", rest="de uitvoer van phpcs (nul fouten), wp plugin check en phpstan zit bij de oplevering; elke phpcs:ignore heeft een reden")
def wp37(ctx):
    if not _php(ctx):
        return NVT, "geen PHP-bestanden"
    mist = [n for n, pat in (("phpcs.xml", r"\.?phpcs\.xml(\.dist)?$"), ("phpstan.neon", r"phpstan(\.dist)?\.neon(\.dist)?$")) if not any(re.match(pat, b) for b in ctx.bestanden())]
    return (FAIL, "ontbreekt: " + ", ".join(mist)) if mist else (PASS, "beide aanwezig")
