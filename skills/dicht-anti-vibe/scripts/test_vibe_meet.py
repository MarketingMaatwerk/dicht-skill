"""Test van de metingen voor VIBE-37 tot en met VIBE-43 in vibe_meet.py, op vaste HTML in een lege browser (geen netwerk).

Aanroep: /usr/bin/python3 test_vibe_meet.py   (Playwright uit de gebruikers-site, zoals vibe_meet.py zelf)
Exitcode 0 alles goed, 1 een fout.
"""
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("vibe_meet", Path(__file__).with_name("vibe_meet.py"))
vm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vm)
fouten = 0


def toets(naam, ok, detail=""):
    global fouten
    fouten += 0 if ok else 1
    print(f"{'goed' if ok else 'FOUT'}  {naam}" + ("" if ok else f": {detail}"))


KLIK = """<body style="margin:0;font:16px sans-serif">
<div id="dicht"><a href="/a" style="display:inline-block;width:16px;height:16px;position:absolute;left:10px;top:10px">a</a>
<a href="/b" style="display:inline-block;width:16px;height:16px;position:absolute;left:30px;top:10px">b</a></div>
<a href="/c" style="display:inline-block;width:16px;height:16px;position:absolute;left:200px;top:10px">c</a>
<p style="position:absolute;top:100px;font-size:12px">Lees de <a href="/d">voorwaarden</a> en de <a href="/e">privacy</a> goed.</p>
<button style="position:absolute;top:200px;width:44px;height:44px">ok</button>
<input type="checkbox" style="position:absolute;top:300px;left:0"><input type="checkbox" style="position:absolute;top:300px;left:16px">
</body>"""
# Uit de review: klein naast breed, een skiplink, iconen zonder tekst naast lopende tekst, een opgemaakt vinkje.
KLIK2 = """<body style="margin:0;font:16px sans-serif">
<a href="/i" style="position:absolute;left:0;top:0;width:16px;height:16px;display:block"></a>
<a href="/lang" style="position:absolute;left:18px;top:0;width:200px;height:16px;display:block">lange link</a>
<a href="#main" class="sr" style="position:absolute;left:0;top:100px;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Ga naar inhoud</a>
<a href="/" style="position:absolute;left:4px;top:96px;width:40px;height:40px;display:block">Logo</a>
<div style="position:absolute;top:200px">Volg ons <a href="/fb"><svg width="16" height="16"></svg></a><a href="/ig"><svg width="16" height="16"></svg></a></div>
<input type="checkbox" style="appearance:none;width:16px;height:16px;position:absolute;top:300px;left:0;border:1px solid">
<input type="checkbox" style="appearance:none;width:16px;height:16px;position:absolute;top:300px;left:18px;border:1px solid">
</body>"""
KOPPEN = """<body style="font:16px sans-serif">
<h2 id="los" style="width:200px">Dit is een lange kop die over meerdere regels loopt</h2>
<h2 id="mooi" style="width:200px;text-wrap:balance">Dit is een lange kop die over meerdere regels loopt</h2>
<h2>Kort</h2><h2 id="blok" style="width:200px"><a href="/x" style="display:block">Een kop met een link als blok die ook over regels loopt</a></h2></body>"""
TABEL = """<body><table style="font-family:Carlito;{stijl}"><tr><td>Bedrag</td><td>€ 1.111,11</td></tr><tr><td>Btw</td><td>€ 233,33</td></tr>
<tr><td>Totaal</td><td>€ 1.344,44</td></tr></table></body>"""
VELD = """<head><meta name="viewport" content="width=device-width, viewport-fit=cover">{css}</head><body>
<form><label for="vb-code">Code</label><input type="text" id="vb-code" inputmode="numeric" {ac}>
<label for="pc">Postcode</label><input id="pc" name="postcode"><input name="kortingscode"><input name="promo-code">
<label for="ref">Referral code (optional)</label><input id="ref" name="referentiecode">
<label for="b1">Bevestigingscode</label><input id="b1"><label for="b2">Activation code</label><input id="b2"><input id="b3" name="otpCode">
<input id="b4" name="verificationCode"><label for="n1">Area code</label><input id="n1" type="tel"><label for="n2">Order code</label><input id="n2">
<input id="b5" type="number" name="inlogcode" autocomplete="one-time-code">
<div><input id="v1" name="code1" maxlength="1" {ac}><input id="v2" name="code2" maxlength="1"><input id="v3" name="code3" maxlength="1"></div></form></body>"""
# Submenu's: een dropdown met een gat van 12 px, een zonder gat, en een flyout opzij met en zonder sluitvertraging.
MENU = """<style>body{margin:0;font:16px sans-serif} nav ul{list-style:none;margin:0;padding:0}
nav > ul > li{position:relative;display:inline-block;width:160px;height:40px;line-height:40px}
nav li ul{display:none;position:absolute;left:0;width:200px;background:#eee}
#gat:hover > ul{display:block;top:calc(100% + 12px)} #dicht:hover > ul{display:block;top:100%}
#zij{position:absolute;top:120px;left:0;width:160px} #zij > li{display:block;height:40px;position:relative}
#zij > li > ul{top:0;left:160px;height:240px} #zij:not(.traag) > li:hover > ul{display:block}
#zij.traag > li > ul.open{display:block}
</style><nav><ul><li id="gat"><a href="/g">Gat</a><ul><li><a href="/g1">g1</a></li><li><a href="/g2">g2</a></li></ul></li>
<li id="dicht"><a href="/d">Dicht</a><ul><li><a href="/d1">d1</a></li><li><a href="/d2">d2</a></li></ul></li></ul>
<ul id="zij" class="{klasse}"><li><a href="/z">Zij</a><ul><li><a href="/z1">z1</a></li><li><a href="/z2">z2</a></li>
<li><a href="/z3">z3</a></li><li><a href="/z4">z4</a></li><li><a href="/z5">z5</a></li></ul></li>
<li><a href="/y">Buur</a><ul><li><a href="/y1">y1</a></li><li><a href="/y2">y2</a></li></ul></li></ul></nav>
{script}"""
MENU2 = """<style>body{margin:0;font:16px sans-serif} nav ul{list-style:none;margin:0;padding:0}
nav > ul > li{position:relative;display:inline-block;width:160px;height:40px;line-height:40px}
nav li ul{display:none;position:absolute;left:0;width:200px;background:#eee;top:100%} #w:hover > ul{display:block}
#weg ul{display:block;top:calc(100% + 12px)}</style>
<nav><ul><li id="w"><div class="t"><a href="/w">Wrapper</a></div><ul><li><a href="/w1">w1</a></li><li><a href="/w2">w2</a></li></ul></li>
<li id="weg"><a href="/weg">Weg</a><ul style="display:none"><li><a href="/x1">x1</a></li></ul></li></ul></nav>
<script>const li = document.getElementById('weg'); let sub = li.querySelector('ul');
li.addEventListener('mouseenter', () => { if (sub) sub.style.display = 'block'; else { sub = document.createElement('ul'); sub.innerHTML = '<li><a href="/x1">x1</a></li><li><a href="/x2">x2</a></li>'; li.appendChild(sub); } });
li.addEventListener('mouseleave', () => { if (sub) { sub.remove(); sub = null; } });</script>"""
VERTRAGING = """<script>for (const li of document.querySelectorAll('#zij > li')) { let t;
  const sub = li.querySelector('ul');
  li.addEventListener('mouseenter', () => { clearTimeout(t); t = setTimeout(() => { document.querySelectorAll('#zij ul.open').forEach(u => u !== sub && u.classList.remove('open')); sub.classList.add('open'); }, 250); });
  li.addEventListener('mouseleave', () => { clearTimeout(t); t = setTimeout(() => sub.classList.remove('open'), 500); });
}</script>"""


def main():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            pg = browser.new_page(viewport={"width": 390, "height": 800})
            pg.set_content(KLIK)
            o = pg.evaluate(vm.OPMAAK)
            klein = " ".join(o["klein"])
            toets("VIBE-37: twee doelen van 16 px op 4 px afstand zijn FOUT", "'a'" in klein and "'b'" in klein, o["klein"])
            toets("VIBE-37: een los doel van 16 px met ruimte eromheen is goed (Spacing)", "'c'" not in klein, o["klein"])
            toets("VIBE-37: een link in een zin telt niet (Inline)", "voorwaarden" not in klein and "privacy" not in klein, o["klein"])
            toets("VIBE-37: een knop van 44 px is goed", "'ok'" not in klein, o["klein"])
            toets("VIBE-37: een niet-opgemaakt vinkje telt niet (User agent control)", "input" not in klein, o["klein"])

            pg.set_content(KLIK2)
            klein = " ".join(pg.evaluate(vm.OPMAAK)["klein"])
            toets("VIBE-37: een doel van 16 px op 2 px van een brede lage link is FOUT", "a '' 16x16 naast a 'lange link'" in klein, klein)
            toets("VIBE-37: een visueel verborgen skiplink telt niet", "Ga naar inhoud" not in klein, klein)
            toets("VIBE-37: iconen zonder tekst naast lopende tekst zijn niet Inline", klein.count("16x17 naast a ''") == 2, klein)
            toets("VIBE-37: een opgemaakt vinkje (appearance:none) telt wel mee", "input" in klein, klein)

            pg.set_content(KOPPEN)
            o = pg.evaluate(vm.OPMAAK)
            toets("VIBE-42: de koppen van meer regels zonder balance staan in de lijst", any("lange kop" in x for x in o["los"]) and len(o["los"]) == 2, o["los"])
            toets("VIBE-42: drie koppen van meer regels geteld (ook met een link als blok), de korte niet", o["koppen"] == 3, o["koppen"])

            # VIBE-41: Carlito heeft gelijke cijfers, maar met proportional-nums niet; tabular-nums op de cel herstelt dat
            pg.set_content(TABEL.replace("{stijl}", "font-variant-numeric:proportional-nums"))
            o = pg.evaluate(vm.OPMAAK)
            toets("VIBE-41: een tabel met ongelijke cijfers staat in de lijst", o["tabellen"] == 1 and len(o["ongelijk"]) == 1, o)
            pg.set_content(TABEL.replace("{stijl}", "font-variant-numeric:proportional-nums").replace("<td>", '<td style="font-variant-numeric:tabular-nums">'))
            o = pg.evaluate(vm.OPMAAK)
            toets("VIBE-41: met tabular-nums op de cel geen melding", o["tabellen"] == 1 and not o["ongelijk"], o)
            pg.set_content(TABEL.replace("{stijl}", ""))
            toets("VIBE-41: een lettertype met gelijke cijfers geeft geen melding", not pg.evaluate(vm.OPMAAK)["ongelijk"])
            pg.set_content(TABEL.replace("{stijl}", "font-variant-numeric:proportional-nums").replace("<td>€ 1.111,11", '<td style="display:none">€ 1.111,11</td><td>€ 1.111,11'))
            toets("VIBE-41: een verborgen eerste cijfercel verbergt de melding niet", len(pg.evaluate(vm.OPMAAK)["ongelijk"]) == 1)
            toets("VIBE-41: de meetspan is weer weg", pg.evaluate("() => document.querySelectorAll('td span').length") == 0)

            pg.set_content(VELD.format(css="", ac=""))
            v = pg.evaluate(vm.VELDEN)
            toets("VIBE-40: viewport-fit=cover zonder safe-area-inset", v["cover"] and not v["veilig"], v)
            namen = [x["naam"] for x in v["otp"]]
            toets("VIBE-43: de codevelden gevonden, ook samenstellingen en camelCase; de vakjes als één veld",
                  namen == ["vb-code", "b1", "b2", "b3", "b4", "b5", "v1"], namen)
            toets("VIBE-43: niet postcode, kortingscode, promo-code, referral code, area code of order code", not {"pc", "ref", "n1", "n2"} & set(namen), namen)
            toets("VIBE-43: zonder autocomplete is het codeveld fout", not v["otp"][0]["ac"], v["otp"])
            pg.set_content(VELD.format(css="<style>.balk{padding-bottom:env(safe-area-inset-bottom)}</style>", ac='autocomplete="one-time-code"'))
            v = pg.evaluate(vm.VELDEN)
            toets("VIBE-40: met env(safe-area-inset-bottom) goed", v["cover"] and v["veilig"], v)
            toets("VIBE-43: met autocomplete=one-time-code goed", v["otp"][0]["ac"] and v["otp"][0]["type"] == "text", v["otp"])
            b5 = next(x for x in v["otp"] if x["naam"] == "b5")
            toets("VIBE-43: type=number wordt gezien", b5["type"] == "number", b5)
            toets("VIBE-43: losse vakjes zijn goed als het eerste vakje one-time-code heeft", next(x for x in v["otp"] if x["naam"] == "v1")["ac"], v["otp"])

            pg = browser.new_page(viewport={"width": 1366, "height": 900})
            pg.set_content(MENU.replace("{klasse}", "").replace("{script}", ""))
            r38, r39 = vm.submenus(pg)
            toets("VIBE-38: het submenu met een gat van 12 px is FOUT, het submenu zonder gat niet",
                  r38[0] == "FOUT" and "Gat" in r38[1] and "Dicht" not in r38[1] and "Zij" not in r38[1], r38)
            toets("VIBE-39: de flyout opzij sluit op de schuine weg (de buur neemt de hover over)", r39[0] == "na te lopen" and "Zij" in r39[1], r39)
            pg.set_content(MENU.replace("{klasse}", "traag").replace("{script}", VERTRAGING))
            r38, r39 = vm.submenus(pg)
            toets("VIBE-39: met een sluitvertraging blijft de flyout open op de schuine weg", "Zij" not in r39[1], r39)
            pg.set_content(MENU2)
            r38, r39 = vm.submenus(pg)
            toets("VIBE-38: een menu met een div om de trigger wordt getest (geen gat: goed)", r38[0] == "FOUT" and "Wrapper" not in r38[1], r38)
            toets("VIBE-38: een submenu dat bij sluiten uit de DOM gaat geeft FOUT, geen exceptie", "Weg" in r38[1], r38)
            pg.set_content("<nav><ul><li><a href='/x'>x</a></li></ul></nav>")
            toets("VIBE-38: zonder submenu goed", vm.submenus(pg)[0][0] == "goed")
        finally:
            browser.close()
    print(f"{fouten} fout(en)")
    return 1 if fouten else 0


if __name__ == "__main__":
    sys.exit(main())
