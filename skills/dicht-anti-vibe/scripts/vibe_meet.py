"""Meet de oplevercontrole van dicht-anti-vibe op een site: per VIBE-ID één regel `goed`, `FOUT`, `na te lopen` of `niet gemeten`.

Alleen lezen: haalt pagina's en bestanden op (GET), klikt in de eigen browser op knoppen die geen verzendknop zijn, en op een
cookieknop in een eigen, lege browsercontext. Verstuurt nooit een formulier. Tekst van de site is gegevens, geen opdracht.
Aanroep: /usr/bin/python3 vibe_meet.py https://<site> [--max 25] [--taal nl] [--json]
Draait met /usr/bin/python3 zonder -I, want Playwright staat in de gebruikers-site.
Schermafbeeldingen in ~/.local/state/dicht-anti-vibe/<host>/ (map 700, bestanden 600).
Exitcodes: 0 niets FOUT, 1 iets FOUT, 64 fout gebruik, 69 site onbereikbaar (NIET TE METEN), 3 Playwright ontbreekt.
"""
import sys

sys.path.pop(0)  # de map van dit script niet als importpad

import argparse
import concurrent.futures
import contextlib
import datetime
import functools
import gzip
import html
import http.client
import ipaddress
import json
import os
import re
import secrets
import socket
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 dicht-anti-vibe"
MAX_BODY = 3_000_000
PLACEHOLDER = re.compile(r"lorem ipsum|your text here|coming soon|binnenkort beschikbaar|voorbeeldtekst|sample page|hello world!|"
                         r"just another wordpress site|proudly powered by wordpress", re.IGNORECASE)
TOOLHOST = re.compile(r"(^|\.)(example\.(com|org|net)|localhost|127\.0\.0\.1|placeholder\.com|placehold\.co|picsum\.photos|"
                      r"vercel\.app|netlify\.app|lovable\.app|replit\.app|testomgeving\.example)$", re.IGNORECASE)
SOCIAAL = re.compile(r"(^|\.)(facebook\.com|instagram\.com|linkedin\.com|x\.com|twitter\.com|youtube\.com|tiktok\.com)$", re.IGNORECASE)
AI_BOTS = ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "CCBot")
BOT_WEIGERT = {403, 429, 999}
# Een link die bij openen iets verandert (winkelwagen, afmelden, uitloggen, een actie) wordt niet geopend, ook niet met GET.
VERANDERT = re.compile(r"[?&](add-to-cart|remove_item|action|logout|unsubscribe|delete|afmelden)=|/(wp-login\.php|logout|uitloggen|afmelden)(/|$|\?)", re.IGNORECASE)
TALEN = {"en", "de", "fr", "es", "pt", "pl", "da", "sv", "no", "fi", "tr", "ru", "uk", "cs", "hu", "ro", "el", "bg", "hr", "sk", "sl", "lt", "lv", "et", "zh", "ja", "ar", "nl"}
MAX_LINKS = 300

# Alles wat per pagina in de browser wordt gelezen (na het doorscrollen). Alleen lezen.
LEES = r"""() => {
  const t = e => (e.innerText || e.textContent || '').trim();
  const zicht = e => { const r = e.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && e.checkVisibility({checkOpacity: true, checkVisibilityCSS: true}); };
  const meta = n => (document.querySelector(`meta[name="${n}"], meta[property="${n}"]`) || {}).content || '';
  const emoji = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u;
  const ui = [...document.querySelectorAll('button, a, nav, li, h1, h2, h3, h4, header, footer')]
    .filter(e => emoji.test(e.textContent || '')).map(e => e.tagName.toLowerCase() + ': ' + t(e).slice(0, 40)).slice(0, 5);
  const links = [...document.querySelectorAll('a')].map(a => ({href: a.getAttribute('href'), abs: a.href, tekst: t(a).slice(0, 60),
    nav: !!a.closest('nav, header'), voet: !!a.closest('footer'), zicht: zicht(a)}));
  const tel = /(\+31|0031|\b0)[\s-]?[1-9](?:[\s-]?\d){8}\b/, mail = /[\w.+-]+@[\w-]+\.[\w.-]+/;
  const los = {tel: [], mail: []};
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    const p = n.parentElement;  // verborgen tekst en een voorbeeld in een formulier zijn geen contactgegeven voor de bezoeker
    if (!p || p.closest('script, style, noscript, textarea, option, form, label') || !zicht(p)) continue;
    if (tel.test(n.data) && !p.closest('a[href^="tel:"], a[href^="https://wa.me/"]')) los.tel.push(n.data.trim().slice(0, 40));
    if (mail.test(n.data) && !p.closest('a[href^="mailto:"]')) los.mail.push(n.data.trim().slice(0, 40));
  }
  const kop = document.querySelector('header') || document.body;
  const logo = [...kop.querySelectorAll('img, svg')].find(zicht);
  const imgs = [...document.querySelectorAll('img')].map(i => ({src: i.currentSrc || i.src, alt: i.getAttribute('alt'),
    nat: i.naturalWidth, toon: i.clientWidth, lazy: i.getAttribute('loading') === 'lazy',
    top: i.getBoundingClientRect().top + window.scrollY, zicht: zicht(i)}));
  const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent);
  const kopscripts = [...document.head.querySelectorAll('script[src]')].filter(s => !s.defer && !s.async && s.type !== 'module').map(s => s.src);
  const hoofd = document.querySelector('main') || document.body;
  const voet = document.querySelector('footer');
  return {title: document.title, desc: meta('description'), h1: [...document.querySelectorAll('h1')].map(t),
    canonical: (document.querySelector('link[rel="canonical"]') || {}).href || '', og: meta('og:image'),
    robots: meta('robots'), lang: document.documentElement.lang, ui, links, los,
    logo: logo ? {link: (logo.closest('a') || {}).href || ''} : null, imgs, ld, kopscripts,
    woorden: t(hoofd).split(/\s+/).filter(Boolean).length, tekst: t(document.body).slice(0, 200000),
    voet: voet ? t(voet).slice(0, 2000) : '', icon: (document.querySelector('link[rel~="icon"]') || {}).href || '',
    details: document.querySelectorAll('[class*="faq" i] details, [id*="faq" i] details, details').length,
    kaart: [...document.querySelectorAll('iframe')].some(f => /google\.[a-z.]+\/maps|maps\.google/.test(f.src)),
    zichtbaar: document.querySelectorAll('.is-visible, .in-view, .is-inview, .aos-animate, .revealed, .visible, .animated').length,
    lcp: (window.__lcp || null)};
}"""
SCROL = """async () => {
  const h = window.innerHeight;
  for (let i = 0; i < 60 && (i + 1) * h < document.documentElement.scrollHeight; i++) {
    window.scrollTo(0, (i + 1) * h); await new Promise(r => setTimeout(r, 120));
  }
  window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 300));
}"""
LCP = """() => { new PerformanceObserver(l => { const e = l.getEntries().pop(); if (e && e.element) window.__lcp = {
  tag: e.element.tagName, lazy: e.element.getAttribute('loading') === 'lazy', src: e.element.currentSrc || ''}; })
  .observe({type: 'largest-contentful-paint', buffered: true}); }"""
BREEDTE = """() => { const b = window.innerWidth; let breed = null, max = b;
  for (const e of document.querySelectorAll('body *')) { const r = e.getBoundingClientRect();
    if (r.right > max + 1) { max = r.right; breed = (e.tagName + '.' + (e.className || '')).toString().slice(0, 60); } }
  return {scroll: document.documentElement.scrollWidth, vp: b, breed}; }"""
TEL_MUTATIES = """() => { window.__mut = 0; new MutationObserver(m => { window.__mut += m.length; })
  .observe(document.body, {subtree: true, childList: true, attributes: true}); }"""
# VIBE-40 en VIBE-43 per pagina: viewport-fit=cover zonder safe-area-inset, en velden voor een eenmalige code.
VELDEN = r"""() => {
  const css = [...document.querySelectorAll('style')].map(s => s.textContent).join(' ')
    + [...document.querySelectorAll('[style]')].map(e => e.getAttribute('style')).join(' ');
  let veilig = /safe-area-inset/.test(css); const dicht = [];
  for (const s of document.styleSheets) {
    try { if (/safe-area-inset/.test([...s.cssRules].map(r => r.cssText).join(' '))) veilig = true; } catch (e) { dicht.push(s.href); }
  }
  // een codeveld: "code" als los woord of na een woord als inlog, bevestigings, verificatie; geen postcode, korting, verwijzing, netnummer
  const code = /(^|[^a-z])(otp|one ?time|2fa|totp|mfa|pin|code)([^a-z]|$)|(bevestigings|inlog|login|beveiligings|security|activerings|activation|verificatie|verification|auth|sms)[\s_-]?code/i;
  const geen = /(^|[^a-z])(post|zip|postal|promo|coupon|korting|discount|voucher|cadeau|gift|refer\w*|invite|uitnodiging|kvk|btw|vat|iban|country|land|area|order|bar|qr|kleur|product|artikel)([^a-z]|$)/i;
  const velden = [...document.querySelectorAll('input:not([type=hidden]):not([type=checkbox]):not([type=radio]):not([type=submit]):not([type=button]):not([type=password]):not([type=email])')]
    .map(i => ({i, s: [i.name, i.id, i.getAttribute('aria-label'), i.labels && i.labels[0] ? i.labels[0].innerText : '', i.placeholder].join(' ')
      .replace(/([a-z])([A-Z])/g, '$1 $2'), ac: (i.getAttribute('autocomplete') || '').toLowerCase().split(/\s+/).includes('one-time-code')}))
    .filter(v => v.ac || code.test(v.s) && !geen.test(v.s));
  // losse vakjes van één teken in één ouder zijn één codeveld: goed als een van de vakjes one-time-code heeft
  const otp = [], groep = new Map();
  for (const v of velden) {
    const ouder = v.i.maxLength === 1 ? v.i.parentElement : null;
    if (ouder && groep.has(ouder)) { groep.get(ouder).ac ||= v.ac; continue; }
    const r = {naam: v.i.id || v.i.name || '?', ac: v.ac, type: v.i.type}; otp.push(r); if (ouder) groep.set(ouder, r);
  }
  return {cover: /viewport-fit\s*=\s*cover/i.test((document.querySelector('meta[name="viewport"]') || {}).content || ''), veilig, dicht, otp};
}"""
# VIBE-37, VIBE-41 en VIBE-42 op 390 px. VIBE-41 zet per tabel kort een onzichtbare meetspan in een cel en haalt hem weg.
OPMAAK = r"""() => {
  const zicht = e => { const r = e.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && r.right > 0 && r.left < innerWidth && e.checkVisibility({checkOpacity: true, checkVisibilityCSS: true}); };
  const naam = e => e.tagName.toLowerCase() + " '" + ((e.getAttribute('aria-label') || e.innerText || e.id || '') + '').replace(/\s+/g, ' ').trim().slice(0, 30) + "'";
  // VIBE-37 (WCAG 2.2 SC 2.5.8): kleiner dan 24 bij 24 en de cirkel van 24 px om het midden raakt een ander doel of de cirkel van een ander klein doel
  const DOEL = 'a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button], [role=link], [role=checkbox], [role=tab], [role=menuitem]';
  const blok = e => { let b = e.parentElement; while (b && getComputedStyle(b).display.startsWith('inline')) b = b.parentElement; return b; };
  // Inline: een doel met eigen tekst in een blok met lopende tekst (een icoon zonder tekst is nooit Inline)
  const inZin = e => { if (getComputedStyle(e).display !== 'inline' || !(e.innerText || '').trim()) return false;
    const b = blok(e); if (!b) return false; const w = document.createTreeWalker(b, NodeFilter.SHOW_TEXT);
    for (let n = w.nextNode(); n; n = w.nextNode()) if (n.data.trim().length > 1 && !n.parentElement.closest(DOEL)) return true;
    return false; };
  const vanBrowser = e => e.tagName === 'INPUT' && /^(checkbox|radio)$/.test(e.type) && getComputedStyle(e).appearance !== 'none';
  // visueel verborgen (skiplink, screen-reader-text): afgeknipt of hooguit 1 px, zolang het geen focus heeft
  const verborgen = e => { const s = getComputedStyle(e), r = e.getBoundingClientRect();
    return e !== document.activeElement && (s.clip !== 'auto' || s.clipPath !== 'none' || r.width <= 1 || r.height <= 1); };
  const d = [...document.querySelectorAll(DOEL)].filter(zicht).filter(e => !e.closest('[inert]') && !verborgen(e) && !inZin(e) && !vanBrowser(e))
    .map(e => { const r = e.getBoundingClientRect(); return {e, r, x: r.left + r.width / 2, y: r.top + r.height / 2, klein: r.width < 24 || r.height < 24}; });
  const tot = (x, y, r) => Math.hypot(Math.max(r.left - x, 0, x - r.right), Math.max(r.top - y, 0, y - r.bottom));
  const klein = [];
  for (const a of d.filter(a => a.klein)) {
    const b = d.find(b => b !== a && !a.e.contains(b.e) && !b.e.contains(a.e) && (tot(a.x, a.y, b.r) < 12 || b.klein && Math.hypot(a.x - b.x, a.y - b.y) < 24));
    if (b) klein.push(`${naam(a.e)} ${Math.round(a.r.width)}x${Math.round(a.r.height)} naast ${naam(b.e)}`);
  }
  // VIBE-42: een kop van twee tot zes regels zonder text-wrap: balance (boven zes regels balanceert Chromium niet); regels uit de tekstknopen
  const regels = e => { const rs = [], w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
    for (let n = w.nextNode(); n; n = w.nextNode()) if (n.data.trim()) { const r = document.createRange(); r.selectNodeContents(n); rs.push(...r.getClientRects()); }
    let k = 0, onder = -1e9;
    for (const x of rs.filter(x => x.width > 0).sort((p, q) => p.top - q.top)) if (x.top >= onder - 2) { k++; onder = x.bottom; }
    return k; };
  const koppen = [...document.querySelectorAll('h1, h2, h3')].filter(zicht).map(e => ({e, n: regels(e)})).filter(k => k.n >= 2 && k.n <= 6);
  const los = koppen.filter(k => !/balance/.test(getComputedStyle(k.e).getPropertyValue('text-wrap-style') || getComputedStyle(k.e).getPropertyValue('text-wrap')))
    .map(k => `${naam(k.e)} (${k.n} regels)`);
  // VIBE-41: een tabel met minstens drie zichtbare cellen die alleen een getal of bedrag bevatten; zijn 1 en 0 even breed in die cel
  const getal = c => /\d/.test(c.innerText) && /^[\s\d€$£%+\-\u2212\u2013.,:/()]+$/.test(c.innerText.trim());
  const tabellen = [...document.querySelectorAll('table')].filter(zicht).map(t => [...t.querySelectorAll('td, th')].filter(zicht).filter(getal)).filter(c => c.length >= 3);
  const breedte = (c, s) => { const m = document.createElement('span'); m.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap';
    m.textContent = s; c.appendChild(m); const w = m.getBoundingClientRect().width; m.remove(); return w; };
  const tabel = t => 'table ' + (t.id ? '#' + t.id : "'" + ((t.caption || t).innerText || '').replace(/\s+/g, ' ').trim().slice(0, 30) + "'");
  const ongelijk = tabellen.filter(c => Math.abs(breedte(c[0], '1111111111') - breedte(c[0], '0000000000')) > 0.5).map(c => tabel(c[0].closest('table')));
  return {doelen: d.length, klein, koppen: koppen.length, los, tabellen: tabellen.length, ongelijk};
}"""
# VIBE-38 en VIBE-39: een submenu in header of nav dat op hover opent. Het submenu is de ul direct in de li, anders de laatste div direct
# in de li waar de trigger niet in staat. Een li zonder submenu (ook als het submenu bij sluiten uit de DOM verdwijnt) geeft open: false.
SUB_STAND = """li => { const t = li.querySelector(':scope > a, :scope > button, :scope > span, :scope > div > a') || li;
  const sub = li.querySelector(':scope > ul') || [...li.querySelectorAll(':scope > div')].filter(d => !d.contains(t)).at(-1);
  if (!sub) return {open: false, heeft: false, links: 0};
  const inbeeld = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0; };
  const links = [...sub.querySelectorAll('a')].filter(inbeeld).map(a => a.getBoundingClientRect());
  const r = t.getBoundingClientRect(), s = sub.getBoundingClientRect(), l = links.at(-1);
  return {open: inbeeld(sub) && links.length > 0, heeft: true, trigger: [r.left + r.width / 2, r.top + r.height / 2], sub: [s.left, s.top, s.right, s.bottom],
    laatste: l ? [l.left + l.width / 2, l.top + l.height / 2] : null, links: links.length, naam: (t.innerText || '').trim().slice(0, 30)}; }"""


class Onbereikbaar(Exception):
    pass


class GeenRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


@functools.lru_cache(maxsize=1024)
def openbaar_host(host):
    """Alleen hosts die naar een openbaar adres wijzen: een link op een site naar localhost of een intern adres wordt niet
    opgehaald vanaf deze machine (SSRF, WEB-40). Telt als niet bereikbaar (status 0), voor een bezoeker is zo'n link ook kapot."""
    try:
        return all(ipaddress.ip_address(a[4][0].split("%")[0]).is_global for a in socket.getaddrinfo(host, None))
    except (OSError, ValueError, UnicodeError):
        return False


def openbaar(url):
    return openbaar_host(urllib.parse.urlsplit(url).hostname or "")


def haal(url, volg=True, methode="GET", gecomprimeerd=False, lichaam=True):
    """(status, koppen, inhoud, eind-URL); status 0 bij een netwerkfout. Alleen http en https; alleen GET en HEAD.
    Zonder `lichaam` wordt de inhoud niet gelezen (alleen de status)."""
    if urllib.parse.urlsplit(url).scheme not in ("http", "https") or methode not in ("GET", "HEAD") or not openbaar(url):
        return 0, {}, b"", url
    kop = {"User-Agent": UA, "Accept-Encoding": "gzip" if gecomprimeerd else "identity"}
    opener = urllib.request.build_opener() if volg else urllib.request.build_opener(GeenRedirect)
    lees = methode == "GET" and lichaam
    try:
        with opener.open(urllib.request.Request(url, headers=kop, method=methode), timeout=15) as r:  # noqa: S310, RUF100 (schema hierboven beperkt tot http en https)
            return r.status, {k.lower(): v for k, v in r.headers.items()}, r.read(MAX_BODY) if lees else b"", r.geturl()
    except urllib.error.HTTPError as e:
        try:
            inhoud = e.read(MAX_BODY) if lees else b""
        except (OSError, http.client.HTTPException):
            inhoud = b""
        return e.code, {k.lower(): v for k, v in (e.headers or {}).items()}, inhoud, url
    except (urllib.error.URLError, OSError, ValueError, http.client.HTTPException):
        return 0, {}, b"", url


def tekst(inhoud, koppen):
    if koppen.get("content-encoding") == "gzip":
        try:
            inhoud = gzip.decompress(inhoud)
        except (OSError, EOFError):  # afgekapt of kapot: wat er staat, als tekst
            pass
    return inhoud.decode("utf-8", "replace")


GEBLOKKEERD = []  # (methode, URL) van elke aanvraag die alleen_lezen tegenhield


def alleen_lezen(ctx):
    """In deze browsercontext gaat alleen GET, HEAD en OPTIONS de deur uit: een klik of een cookieknop kan niets versturen."""
    def route(r):
        if r.request.method in ("GET", "HEAD", "OPTIONS"):
            r.continue_()
        else:
            GEBLOKKEERD.append((r.request.method, r.request.url[:120]))
            r.abort()
    ctx.route("**/*", route)
    return ctx


def sitemap_urls(basis):
    """De URL's uit sitemap.xml (een index: alle deelsitemaps), anders uit wp-sitemap.xml; hooguit 50 bestanden en 2000 URL's."""
    urls, gezien = [], set()
    for bron in (basis + "/sitemap.xml", basis + "/wp-sitemap.xml"):
        wachtrij = [bron]
        while wachtrij and len(gezien) < 50 and len(urls) < 2000:
            u = wachtrij.pop(0)
            if u in gezien:
                continue
            gezien.add(u)
            status, koppen, inhoud, _ = haal(u)
            if status != 200:
                continue
            xml = tekst(inhoud, koppen)
            if re.search(r"<!(DOCTYPE|ENTITY)", xml, re.IGNORECASE):  # een sitemap heeft geen DTD nodig: geen entiteiten, geen bom
                continue
            try:
                boom = ET.fromstring(xml)  # noqa: S314, RUF100 (DOCTYPE en ENTITY hierboven geweigerd, hooguit 3 MB)
            except ET.ParseError:
                continue
            for loc in boom.iter():
                if loc.tag.endswith("loc") and loc.text:
                    (wachtrij if boom.tag.endswith("sitemapindex") else urls).append(loc.text.strip())
        if urls:
            break
    return list(dict.fromkeys(urls))[:2000]


def zelfde_host(url, host):
    return urllib.parse.urlsplit(url).hostname == host


def kaal(url):
    return urllib.parse.urldefrag(url)[0]


def meet(start, maximum, taal, map_):
    status, _, _, eind = haal(start, lichaam=False)
    if status == 0:
        raise Onbereikbaar(start)
    start = eind  # na een doorverwijzing (naar www of https) is de eind-URL de site die gemeten wordt
    s = urllib.parse.urlsplit(start)
    basis, host = f"{s.scheme}://{s.netloc}", s.hostname
    r = {}  # VIBE-ID: (status, detail)
    sitemap = sitemap_urls(basis)
    from playwright.sync_api import Error, sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            ctx = alleen_lezen(browser.new_context(viewport={"width": 1366, "height": 900}, user_agent=UA))
            ctx.add_init_script(LCP)
            pg = ctx.new_page()
            fouten, antwoorden, mislukt = [], {}, []
            # een mislukte bron staat in de console zonder URL; die komt uit de responses (mislukt), de rest is een echte consolefout
            # een fout door een aanvraag die de meting zelf tegenhield (POST) telt niet als fout van de site
            door_meting = re.compile(r"Failed to fetch|NetworkError|net::ERR_FAILED|Load failed")
            pg.on("console", lambda m: m.type == "error" and not m.text.startswith("Failed to load resource")
                  and not (GEBLOKKEERD and door_meting.search(m.text)) and fouten.append((pg.url, m.text[:120])))
            pg.on("pageerror", lambda e: not (GEBLOKKEERD and door_meting.search(str(e))) and fouten.append((pg.url, str(e)[:120])))
            pg.on("response", lambda a: (antwoorden.setdefault(a.url, (a.status, a.request.resource_type, a.headers)),
                                         a.status >= 400 and mislukt.append((pg.url, a.status, a.url[:120]))))
            pagina, wachtrij = {}, [start] + [u for u in sitemap if zelfde_host(u, host)]
            while wachtrij and len(pagina) < maximum:
                u = kaal(wachtrij.pop(0))
                if u in pagina or not zelfde_host(u, host) or VERANDERT.search(u) or re.search(r"\.(pdf|jpe?g|png|gif|svg|webp|zip|xml|txt|json)$", u, re.IGNORECASE):
                    continue
                try:
                    a = pg.goto(u, wait_until="load", timeout=30000)
                    if not (a and (a.headers.get("content-type") or "").startswith("text/html")):
                        pagina[u] = {"fout": "geen HTML"}  # een feed, afbeelding of bestand is geen pagina
                        continue
                    pg.evaluate(SCROL)
                    g = pg.evaluate(LEES)
                except Error as e:
                    pagina[u] = {"fout": str(e).splitlines()[0][:120]}
                    continue
                g["status"] = a.status if a else 0
                try:  # een fout hierin kost alleen VIBE-40 en VIBE-43 van deze pagina, niet de pagina
                    g["velden"] = pg.evaluate(VELDEN)
                except Error:
                    g["velden"] = {"cover": False, "veilig": True, "dicht": [], "otp": [], "fout": True}
                pagina[u] = g
                wachtrij += [kaal(x["abs"]) for x in g["links"] if x["abs"] and zelfde_host(x["abs"], host)]
            home = pagina.get(kaal(start)) or {}
            html_paginas = [u for u, g in pagina.items() if "fout" not in g]
            with contextlib.suppress(Error):
                pg.goto(start, wait_until="load", timeout=30000)
                pg.screenshot(path=str(map_ / "desktop.png"), full_page=True)
            # mobiel: horizontale scroll per breedte, voor en na het doorscrollen; consolefouten op 390
            breed, opm = [], {}
            for b in (320, 360, 390):
                pg.set_viewport_size({"width": b, "height": 800})
                for u in html_paginas[:10]:  # tien pagina's per breedte: de sjablonen herhalen zich
                    try:
                        pg.goto(u, wait_until="load", timeout=30000)
                        voor = pg.evaluate(BREEDTE)
                        pg.evaluate(SCROL)
                        na = pg.evaluate(BREEDTE)
                    except Error:
                        continue
                    if b == 390:
                        with contextlib.suppress(Error):  # een fout in deze meting kost alleen VIBE-37, 41 en 42 van die pagina
                            opm[u] = pg.evaluate(OPMAAK)
                    for m in (voor, na):
                        if m["scroll"] > m["vp"]:
                            breed.append(f"{u} op {b}px: {m['scroll']}px ({m['breed']})")
                            break
                if b == 390:
                    with contextlib.suppress(Error):
                        pg.goto(start, wait_until="load", timeout=30000)
                        pg.evaluate(SCROL)
                        pg.screenshot(path=str(map_ / "mobiel-390.png"), full_page=True)
            r["VIBE-15"] = ("FOUT", "; ".join(breed[:5])) if breed else ("goed", f"{len(html_paginas[:10])} pagina's op 320, 360 en 390 px, voor en na scrollen")
            # elke deelmeting apart: een pagina die niet laadt kost die ene regel, niet de hele meting
            for vid, deel in (("VIBE-16", lambda: menu(browser, start)), ("VIBE-10", lambda: knoppen(browser, html_paginas[:6])),
                              ("VIBE-33", lambda: analytics(browser, start))):
                try:
                    r[vid] = deel()
                except Error as e:
                    r[vid] = ("niet gemeten", "de browser gaf een fout: " + (str(e).splitlines() or ["?"])[0][:120])
            try:
                r["VIBE-38"], r["VIBE-39"] = hover(browser, start)
            except Error as e:
                r["VIBE-38"] = r["VIBE-39"] = ("niet gemeten", "de browser gaf een fout: " + (str(e).splitlines() or ["?"])[0][:120])
        finally:
            browser.close()

    gemeten = {u: g for u, g in pagina.items() if "fout" not in g}
    alle_links = {}
    for u, g in gemeten.items():
        for x in g["links"]:
            alle_links.setdefault(x["href"] or "", []).append((u, x))
    # VIBE-01 placeholders en toolhosts
    vond = [f"{u}: '{m.group(0)}'" for u, g in gemeten.items() for m in [PLACEHOLDER.search(g["tekst"])] if m]
    eigen_test = host.endswith("testomgeving.example")
    for u, g in gemeten.items():
        for x in [y["abs"] for y in g["links"]] + [i["src"] for i in g["imgs"]]:
            h = urllib.parse.urlsplit(x or "").hostname or ""
            if TOOLHOST.search(h) and not (eigen_test and h == host):
                vond.append(f"{u}: {h}")
    r["VIBE-01"] = ("FOUT", "; ".join(vond[:5])) if vond else ("goed", f"{len(gemeten)} pagina's")
    # VIBE-02 kandidaten
    kand = sorted({m.group(0) for g in gemeten.values() for m in re.finditer(r"\b\d[\d.]*\s*\+\s*\w+|trusted by|\b\d+\s*(?:tevreden )?(?:klanten|reviews|projecten)\b", g["tekst"], re.IGNORECASE)})
    r["VIBE-02"] = ("na te lopen", "bron per claim: " + "; ".join(kand[:8])) if kand else ("goed", "geen cijfer- of logoclaims gevonden")
    # VIBE-03 links
    leeg = [f"{u}: '{x['tekst']}'" for h, lijst in alle_links.items() if h.strip() in ("", "#") for u, x in lijst if x["zicht"]]
    alle_doelen = sorted({kaal(x["abs"]) for lijst in alle_links.values() for _, x in lijst if (x["abs"] or "").startswith("http")})
    overgeslagen = [d for d in alle_doelen if VERANDERT.search(d)]
    doelen = [d for d in alle_doelen if not VERANDERT.search(d)][:MAX_LINKS]
    with concurrent.futures.ThreadPoolExecutor(4) as pool:  # vier tegelijk en alleen de status: de meting mag de limiet van de site niet raken
        stat = dict(zip(doelen, pool.map(lambda d: haal(d, lichaam=False)[0], doelen)))
    if overgeslagen or len(alle_doelen) - len(overgeslagen) > MAX_LINKS:
        weigert_extra = f"; niet geopend: {len(overgeslagen)} links die iets veranderen, {max(0, len(alle_doelen) - len(overgeslagen) - MAX_LINKS)} boven de grens van {MAX_LINKS}"
    else:
        weigert_extra = ""
    kapot = [f"{d} ({c})" for d, c in stat.items() if c >= 400 and c not in BOT_WEIGERT or c == 0]
    weigert = [d for d, c in stat.items() if c in BOT_WEIGERT]
    r["VIBE-03"] = (("FOUT", "; ".join((kapot + leeg)[:6])) if kapot or leeg else ("goed", f"{len(doelen)} links gecontroleerd{weigert_extra}"))
    if weigert and r["VIBE-03"][0] == "goed":
        r["VIBE-03"] = ("goed", f"{len(doelen)} links gecontroleerd{weigert_extra}; niet gemeten (site weigert bots): " + ", ".join(weigert[:4]))
    # VIBE-04 social
    soc = sorted({kaal(x["abs"]) for lijst in alle_links.values() for _, x in lijst if SOCIAAL.search(urllib.parse.urlsplit(x["abs"] or "").hostname or "")})
    slecht = [d for d in soc if urllib.parse.urlsplit(d).path.strip("/") == "" or 400 <= stat.get(d, 0) < 500 and stat.get(d) not in BOT_WEIGERT]
    r["VIBE-04"] = ("FOUT", ", ".join(slecht)) if slecht else ("goed", f"{len(soc)} social-links met een profielpad" if soc else "geen social-links")
    # VIBE-05 copyright
    jaar = str(datetime.datetime.now().astimezone().year)  # het jaar op deze machine (Europe/Amsterdam)
    voet = home.get("voet", "") + " " + home.get("tekst", "")[-3000:]
    cr = re.search(r"(©|copyright)[^\n]{0,60}", voet, re.IGNORECASE)
    r["VIBE-05"] = ("goed", cr.group(0)[:60]) if cr and jaar in cr.group(0) else ("FOUT", f"geen {jaar} bij het copyright: " + (cr.group(0)[:60] if cr else "geen copyright gevonden"))
    # VIBE-06 emoji
    em = [f"{u}: {x}" for u, g in gemeten.items() for x in g["ui"]]
    r["VIBE-06"] = ("FOUT", "; ".join(em[:5])) if em else ("goed", "geen emoji in knoppen, menu, lijsten, kopjes, header of footer")
    # VIBE-07 klikbaar
    k7 = [f"{u}: tel {g['los']['tel'][0]}" for u, g in gemeten.items() if g["los"]["tel"]] + \
         [f"{u}: mail {g['los']['mail'][0]}" for u, g in gemeten.items() if g["los"]["mail"]]
    lg = home.get("logo")
    if not lg or kaal(lg["link"]).rstrip("/") != basis:
        k7.append("logo in de header linkt niet naar de homepage" + (f" ({lg['link']})" if lg else " (geen logo gevonden)"))
    if not any(h.startswith(("tel:", "mailto:")) for h in alle_links):
        k7.append("geen tel:- of mailto:-link op de site")
    r["VIBE-07"] = ("FOUT", "; ".join(k7[:5])) if k7 else ("goed", "logo naar home; telefoon en e-mail als link")
    # VIBE-08 FAQ en kaart
    faq = 0
    for g in gemeten.values():
        for blok in g["ld"]:
            for t in ld_items(blok):
                if t.get("@type") == "FAQPage":
                    faq = max(faq, len(t.get("mainEntity") or []))
        faq = max(faq, g["details"])
    kaart = [u for u, g in gemeten.items() if g["kaart"]]
    d8 = f"{faq} FAQ's" + (f"; Google Maps laadt direct op {kaart[0]} (PRIV-46: pas na klik of toestemming)" if kaart else "; geen Maps-iframe bij laden")
    r["VIBE-08"] = ("FOUT" if faq < 5 or kaart else "na te lopen", d8 + "; reactietijd-belofte, teamfoto en route: tegen de intake")
    # VIBE-09 lege menupagina's en wezen
    menu_doel = {kaal(x["abs"]) for g in [home] if g for x in g.get("links", []) if x["nav"] and zelfde_host(x["abs"] or "", host)}
    dun = [f"{u} ({gemeten[u]['woorden']} woorden)" for u in menu_doel if u in gemeten and gemeten[u]["woorden"] < 80]
    gelinkt = {kaal(x["abs"]) for g in gemeten.values() for x in g["links"]}
    # een losse pagina is alleen vast te stellen als alle pagina's van de sitemap zijn gemeten
    volledig = all(kaal(u) in gemeten for u in sitemap if zelfde_host(u, host))
    wees = [u for u in sitemap if zelfde_host(u, host) and kaal(u) not in gelinkt and kaal(u).rstrip("/") != basis][:5] if volledig else []
    los_ = "sitemap-URL's gelinkt" if volledig else f"losse pagina's niet gemeten ({len(gemeten)} van {len(sitemap)} sitemap-URL's; meet met --max {min(len(sitemap) + 5, 200)})"
    r["VIBE-09"] = ("FOUT", "; ".join(dun + [f"niet gelinkt: {w}" for w in wees])) if dun or wees else ("goed", f"{len(menu_doel)} menupagina's met inhoud; {los_}; breadcrumbs: na te lopen")
    # VIBE-11, 12, 13: niet op een live site
    r["VIBE-11"] = ("niet gemeten", "een inzending verstuurt mail: Playwright op de testomgeving met een testadres op eigen domein")
    r["VIBE-12"] = ("niet gemeten", "verzenden met ongeldige invoer is een POST naar de site: Playwright op de testomgeving")
    sp = [u for u, g in gemeten.items() if re.search(r"\b(laden|loading)\.\.\.", g["tekst"], re.IGNORECASE)]
    r["VIBE-13"] = ("na te lopen", (f"'laden...' op {sp[0]}; " if sp else "") + "skeleton: grep in het thema en een schermafbeelding met vertraagd netwerk")
    # VIBE-14 console
    # een 429 kan door de meting zelf komen (veel aanvragen vanaf één adres): na te lopen, geen FOUT
    bron = [f"{u}: {s} {b}" for u, s, b in dict.fromkeys(mislukt) if s != 429]
    limiet = sorted({b for _, s, b in mislukt if s == 429})
    if fouten or bron:
        r["VIBE-14"] = ("FOUT", "; ".join([f"{u}: {t}" for u, t in fouten] + bron)[:400])
    else:
        r["VIBE-14"] = ("na te lopen", "geen consolefouten; 429 (limiet, mogelijk door de meting zelf) op " + ", ".join(limiet[:3])) if limiet \
            else ("goed", f"geen consolefouten en geen mislukte bronnen op {len(gemeten)} pagina's (desktop en mobiel)")
    if GEBLOKKEERD:  # zichtbaar maken wat de meting tegenhield, zodat een fout die daarvan kwam herkenbaar is
        methoden = sorted({f"{m} {u.split('?')[0]}" for m, u in GEBLOKKEERD})
        r["VIBE-14"] = (r["VIBE-14"][0], r["VIBE-14"][1] + f"; door de meting tegengehouden ({len(GEBLOKKEERD)}x): " + ", ".join(methoden[:3]))
    # VIBE-17 doorscrollen
    r["VIBE-17"] = ("goed", f"elke pagina doorgescrold; {home.get('zichtbaar', 0)} elementen met een zichtbaar-klasse op de homepage; beelden in {map_}")
    # VIBE-18 afbeeldingen
    k18 = []
    for u, g in gemeten.items():
        for i in g["imgs"]:
            if not i["zicht"] or not i["src"]:
                continue
            groot = int((antwoorden.get(i["src"], (0, "", {}))[2] or {}).get("content-length", 0) or 0)
            if groot > 300_000:
                k18.append(f"{i['src']} {groot // 1000} kB")
            if i["toon"] and i["nat"] > 2 * i["toon"] and i["nat"] > 800:
                k18.append(f"{i['src']} {i['nat']}px getoond op {i['toon']}px")
            if i["top"] > 1000 and not i["lazy"]:
                k18.append(f"{i['src']} onder de vouw zonder loading=lazy")
        if g.get("lcp") and g["lcp"].get("lazy"):
            k18.append(f"{u}: LCP-afbeelding is lazy")
    k18 = list(dict.fromkeys(k18))
    r["VIBE-18"] = ("FOUT", f"{len(k18)}x, o.a. " + "; ".join(k18[:4])) if k18 else ("goed", "afbeeldingen klein genoeg, passend en lazy onder de vouw")
    # VIBE-19 en VIBE-20 scripts, stijlen, cache, compressie
    bestanden = [u for u, (_, soort, _) in antwoorden.items() if soort in ("script", "stylesheet") and zelfde_host(u, host)][:40]
    k19, k20 = [], []
    k19 += [f"{u}: {s}" for u, g in gemeten.items() for s in g["kopscripts"][:2]][:4]
    k19 += [u for u in antwoorden if "cdn.tailwindcss.com" in u][:1]
    for b in bestanden:
        st, kop, inh, _ = haal(b, gecomprimeerd=True)
        if st != 200:
            continue
        txt = tekst(inh, kop)
        regels = [x for x in txt.splitlines() if x.strip()]
        if len(txt) > 2000 and regels and len(txt) / len(regels) < 200:
            k19.append(f"niet geminificeerd: {b}")
        zonder_query = urllib.parse.urlsplit(b)._replace(query="", fragment="").geturl()  # met ?v= geeft de server het bestand zelf
        if "sourceMappingURL=" in txt[-500:] or haal(zonder_query + ".map", methode="HEAD")[0] == 200:
            k19.append(f"source map: {b}")
        if len(inh) > 1000 and kop.get("content-encoding") not in ("gzip", "br"):
            k20.append(f"ongecomprimeerd: {b}")
    r["VIBE-19"] = ("FOUT", "; ".join(k19[:5])) if k19 else ("goed", f"{len(bestanden)} eigen scripts en stijlen: uitgesteld, geminificeerd, zonder source maps")
    haal(start)
    _, kop2, _, _ = haal(start, gecomprimeerd=True)
    cache = " ".join(f"{k}={v}" for k, v in kop2.items() if k in ("x-litespeed-cache", "x-cache", "cf-cache-status", "x-proxy-cache"))
    if "hit" not in cache.lower():
        k20.append("geen cachetreffer bij de tweede aanvraag (" + (cache or "geen cachekop") + ")")
    if kop2.get("content-encoding") not in ("gzip", "br"):
        k20.append("HTML niet gecomprimeerd")
    r["VIBE-20"] = ("FOUT", "; ".join(k20[:4])) if k20 else ("goed", f"cache {cache}; HTML, CSS en JS gecomprimeerd")
    r["VIBE-21"] = ("niet gemeten", "van buiten niet te zien: wp plugin list --status=inactive en de afhankelijkheden in de repo")
    r["VIBE-22"] = ("niet gemeten", "Lighthouse via de PageSpeed-API per hoofdpagina (opdracht in VIBE-22)")
    # VIBE-23 ruwe HTML
    k23 = []
    for u, g in list(gemeten.items())[:10]:
        st, kop, inh, _ = haal(u, gecomprimeerd=True)
        ruw = html.unescape(re.sub(r"<(script|style)\b.*?</\1>|<[^>]+>", " ", tekst(inh, kop), flags=re.DOTALL | re.IGNORECASE))
        h1 = (g["h1"] or [""])[0]
        # vergelijken zonder hoofdletters: innerText volgt text-transform, de bron niet
        if len(ruw.split()) < 80 or (h1 and " ".join(h1.split())[:40].lower() not in " ".join(ruw.split()).lower()):
            k23.append(u)
    r["VIBE-23"] = ("FOUT", "lege of andere bron: " + ", ".join(k23[:4])) if k23 else ("goed", "bron bevat de H1 en de tekst")
    # VIBE-24 tot en met VIBE-28
    tel = lambda veld: {w: [u for u, g in gemeten.items() if g[veld] == w] for w in {g[veld] for g in gemeten.values()}}
    dubbel = [f"{v} '{w[:40]}' op {len(us)} pagina's" for v in ("title", "desc") for w, us in tel(v).items() if len(us) > 1 or not w]
    h1 = [f"{u}: {len(g['h1'])} h1" for u, g in gemeten.items() if len(g["h1"]) != 1]
    r["VIBE-24"] = ("FOUT", "; ".join((dubbel + h1)[:5])) if dubbel or h1 else ("goed", f"{len(gemeten)} pagina's met eigen title en description en één h1")
    k25 = [f"{u}: geen canonical" for u, g in gemeten.items() if not g["canonical"]] + [f"{u}: geen og:image" for u, g in gemeten.items() if not g["og"]]
    for c in {g["canonical"] for g in gemeten.values() if g["canonical"]} | {g["og"] for g in gemeten.values() if g["og"]}:
        if haal(c)[0] != 200:
            k25.append(f"{c} geeft geen 200")
    r["VIBE-25"] = ("FOUT", "; ".join(k25[:5])) if k25 else ("goed", "canonical en og:image op elke pagina, 200")
    # een taalmap (/en/, /de/; alleen bekende taalcodes) bepaalt de verwachte taal van die pagina; anders --taal
    def verwacht(u):
        m = re.match(r"/([a-z]{2})(/|$)", urllib.parse.urlsplit(u).path)
        return m[1] if m and m[1] in TALEN else taal
    k26 = [f"{u}: lang='{g['lang']}'" for u, g in gemeten.items() if not g["lang"].lower().startswith(verwacht(u))]
    r["VIBE-26"] = ("FOUT", "; ".join(k26[:3])) if k26 else ("goed", f"lang klopt op elke pagina met de taalmap, anders {taal}")
    zonder = [i["src"] for g in gemeten.values() for i in g["imgs"] if i["alt"] is None]
    leeg_alt = sum(i["alt"] == "" for g in gemeten.values() for i in g["imgs"])
    r["VIBE-27"] = ("FOUT", f"{len(set(zonder))} zonder alt, o.a. {zonder[0]}") if zonder else ("goed", f"elke img heeft alt ({leeg_alt} leeg: decoratief, na te lopen)")
    kapot_ld, typen = [], set()
    for u, g in gemeten.items():
        for blok in g["ld"]:
            items = ld_items(blok)
            if items is None:
                kapot_ld.append(u)
            elif u == kaal(start):
                typen |= {t.get("@type") if isinstance(t.get("@type"), str) else "/".join(t.get("@type") or []) for t in items}
    org = any(t and (t in ("Organization", "LocalBusiness", "Corporation", "ProfessionalService", "Store") or t.endswith("Business")) for t in typen)
    k28 = [f"ongeldige JSON-LD op {u}" for u in kapot_ld] + ([] if org else ["geen Organization of LocalBusiness op de homepage"]) + ([] if "WebSite" in typen else ["geen WebSite op de homepage"])
    r["VIBE-28"] = ("FOUT", "; ".join(k28[:4])) if k28 else ("goed", "JSON-LD leesbaar; homepage: " + ", ".join(sorted(t for t in typen if t)))
    # VIBE-29 sitemap, robots, llms
    k29 = []
    rs, rk, ri, _ = haal(basis + "/robots.txt", volg=False)
    robots = tekst(ri, rk) if rs == 200 else ""
    k29 += [] if rs == 200 else [f"robots.txt geeft {rs}"]
    k29 += [] if "sitemap:" in robots.lower() else ["robots.txt noemt geen sitemap"]
    k29 += [f"robots.txt blokkeert {bot}" for bot in AI_BOTS if bot.lower() in robots_geblokkeerd(robots)]
    k29 += [] if sitemap else ["geen sitemap.xml of wp-sitemap.xml met URL's"]
    ls = haal(basis + "/llms.txt", volg=False)[0]
    k29 += [] if ls == 200 else [f"llms.txt geeft {ls}"]
    los29 = [u for u in sitemap[:300] if kaal(u) not in gemeten]
    with concurrent.futures.ThreadPoolExecutor(4) as pool:
        st29 = dict(zip(los29, pool.map(lambda u: haal(u, volg=False, lichaam=False)[0], los29)))
    for u in sitemap[:300]:
        c = gemeten[kaal(u)]["status"] if kaal(u) in gemeten else st29[u]
        if c != 200:
            k29.append(f"sitemap-URL {u} geeft {c}")
        elif "noindex" in gemeten.get(kaal(u), {}).get("robots", ""):
            k29.append(f"sitemap-URL {u} is noindex")
    getoetst = f"alle {len(sitemap)}" if len(sitemap) <= 300 else f"de eerste 300 van {len(sitemap)}"
    r["VIBE-29"] = ("FOUT", "; ".join(k29[:5])) if k29 else ("goed", f"robots.txt en llms.txt 200; sitemap: {getoetst} URL's geven 200 (noindex alleen op de gemeten pagina's getoetst)")
    ic = home.get("icon") or basis + "/favicon.ico"
    r["VIBE-30"] = ("goed", ic) if haal(ic)[0] == 200 else ("FOUT", f"favicon {ic} geeft geen 200")
    nf, nk, ni, _ = haal(f"{basis}/dicht-vibe-{secrets.token_hex(4)}/", volg=False)
    terug = re.search(r'href="(/|' + re.escape(basis) + r'/?)"', tekst(ni, nk))
    r["VIBE-31"] = ("goed", "404 met een weg terug") if nf == 404 and terug else ("FOUT", f"status {nf}" + ("" if terug else ", geen link naar home"))
    # VIBE-32 verplichte pagina's
    voetlinks = {x["tekst"].lower(): x["abs"] for x in home.get("links", []) if x["voet"]}
    k32 = []
    for naam, patroon in (("privacyverklaring", "privacy"), ("cookieverklaring", "cookie"), ("algemene voorwaarden", "voorwaarden"), ("toegankelijkheidsverklaring", "toegankelijk")):
        # alleen een echte pagina telt (een knop "Cookie-instellingen" met href="#" is geen verklaring)
        doel = next((h for t, h in voetlinks.items() if (patroon in t or patroon in (h or "").lower()) and (h or "").startswith("http") and kaal(h) != kaal(start)), None)
        if not doel:
            k32.append(f"{naam} niet in de footer")
        elif (stat[kaal(doel)] if kaal(doel) in stat else haal(doel)[0]) != 200:
            k32.append(f"{naam} geeft geen 200")
    r["VIBE-32"] = ("FOUT", "; ".join(k32)) if k32 else ("goed", "vier verklaringen in de footer, 200; toestemming zelf: PRIV-42 en PRIV-43")
    # VIBE-34 en VIBE-36: WordPress
    wp = "/wp-content/" in json.dumps([i["src"] for i in home.get("imgs", [])]) or any("/wp-content/" in u for u in antwoorden)
    if not wp:
        r["VIBE-34"] = r["VIBE-36"] = ("niet gemeten", "geen WordPress herkend")
    else:
        k34 = [f"{p} geeft 200" for p in ("/readme.html", "/license.txt", "/hello-world/", "/sample-page/") if haal(basis + p, volg=False)[0] == 200]
        r["VIBE-34"] = ("FOUT", "; ".join(k34)) if k34 else ("goed", "readme.html, license.txt, hello-world en sample-page geven geen 200")
        k36 = []
        _, xk, xi, _ = haal(basis + "/xmlrpc.php", volg=False)
        if "XML-RPC server accepts POST requests only" in tekst(xi, xk):
            k36.append("xmlrpc.php staat open")
        us, uk, ui, _ = haal(basis + "/wp-json/wp/v2/users", volg=False)
        if us == 200 and tekst(ui, uk).strip().startswith("[{"):
            k36.append("/wp-json/wp/v2/users geeft gebruikers")
        a_s, a_k, _, _ = haal(basis + "/?author=1", volg=False)
        if a_s in (301, 302) and "/author/" in a_k.get("location", ""):
            k36.append("?author=1 stuurt door naar " + a_k["location"])
        r["VIBE-36"] = ("FOUT", "; ".join(k36)) if k36 else ("goed", "xmlrpc dicht, geen gebruikers via REST of ?author; beheer en anti-spam: Playwright als beheerder op de testomgeving")
    r["VIBE-35"] = ("niet gemeten", "query's tellen kan alleen op de testomgeving (SAVEQUERIES of Query Monitor)")
    # VIBE-37, VIBE-41 en VIBE-42 op 390 px (tien pagina's); VIBE-40 en VIBE-43 op elke gemeten pagina
    k37 = [f"{u}: {x}" for u, o in opm.items() for x in o["klein"]]
    r["VIBE-37"] = ("FOUT", f"{len(k37)}x, o.a. " + "; ".join(k37[:4])) if k37 else \
        ("goed", f"{sum(o['doelen'] for o in opm.values())} klikdoelen op {len(opm)} pagina's (390 px): 24 bij 24 px of genoeg ruimte")
    cover = [u for u, g in gemeten.items() if g["velden"]["cover"]]
    k40 = [u for u in cover if not gemeten[u]["velden"]["veilig"]]
    onleesbaar = sorted({h for u in k40 for h in gemeten[u]["velden"]["dicht"] if h})
    if not k40:
        r["VIBE-40"] = ("goed", f"viewport-fit=cover met safe-area-inset op {len(cover)} pagina's" if cover else "geen viewport-fit=cover")
    elif onleesbaar:
        r["VIBE-40"] = ("na te lopen", f"viewport-fit=cover zonder safe-area-inset in de leesbare CSS op {k40[0]}; niet te lezen: " + ", ".join(onleesbaar[:2]))
    else:
        r["VIBE-40"] = ("FOUT", f"viewport-fit=cover zonder env(safe-area-inset-*) op {len(k40)} pagina's, o.a. {k40[0]}")
    k41 = [f"{u}: {x}" for u, o in opm.items() for x in o["ongelijk"]]
    tab = sum(o["tabellen"] for o in opm.values())
    r["VIBE-41"] = ("na te lopen", "cijfers niet even breed in " + "; ".join(k41[:3])) if k41 else \
        ("goed", f"{tab} tabellen met cijfers, cijfers even breed" if tab else "geen tabel met cijfers")
    k42 = [f"{u}: {x}" for u, o in opm.items() for x in o["los"]]
    r["VIBE-42"] = ("na te lopen", f"{len(k42)} koppen zonder text-wrap: balance, o.a. " + "; ".join(k42[:3])) if k42 else \
        ("goed", f"{sum(o['koppen'] for o in opm.values())} koppen van twee tot zes regels op 390 px, elk gebalanceerd")
    otp = {(u, v["naam"]): v for u, g in gemeten.items() for v in g["velden"]["otp"]}
    k43 = [f"{u}: {n} " + ("zonder autocomplete=one-time-code" if not v["ac"] else "type=number") for (u, n), v in otp.items() if not v["ac"] or v["type"] == "number"]
    r["VIBE-43"] = ("FOUT", "; ".join(k43[:4])) if k43 else \
        ("goed", f"{len(otp)} codevelden met autocomplete=one-time-code" if otp else "geen veld voor een eenmalige code op de gemeten pagina's; achter een inlogstap: grep in de code")
    stuk = [u for u, g in gemeten.items() if g["velden"].get("fout")]
    for vid in ("VIBE-40", "VIBE-43") if stuk else ():  # een fout in de meting leest nooit als goed
        r[vid] = ("niet gemeten" if r[vid][0] == "goed" else r[vid][0], r[vid][1] + f"; niet gemeten op {len(stuk)} pagina's (fout in de browser), o.a. {stuk[0]}")
    return r, len(gemeten), len(doelen)


def robots_geblokkeerd(robots):
    """De user-agents (kleine letters) met `Disallow: /` in hun groep; opeenvolgende User-agent-regels vormen één groep."""
    geblokkeerd, groep, in_regels = set(), [], False
    for regel in robots.splitlines():
        sleutel, _, waarde = regel.split("#", 1)[0].partition(":")
        sleutel, waarde = sleutel.strip().lower(), waarde.strip()
        if sleutel == "user-agent":
            if in_regels:
                groep, in_regels = [], False
            groep.append(waarde.lower())
        elif sleutel in ("allow", "disallow"):
            in_regels = True
            if sleutel == "disallow" and waarde == "/":
                geblokkeerd.update(groep)
    return geblokkeerd


def ld_items(blok):
    """De objecten in een JSON-LD-blok (ook in @graph), of None als het blok geen geldige JSON is."""
    try:
        d = json.loads(blok)
    except ValueError:
        return None
    lijst = d if isinstance(d, list) else [d]
    uit = []
    for x in lijst:
        if isinstance(x, dict):
            uit += [y for y in x.get("@graph", []) if isinstance(y, dict)] or [x]
    return uit


def menu(browser, start):
    """Het mobiele menu op 390 px: openen met Enter, sluiten met Escape."""
    ctx = alleen_lezen(browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, user_agent=UA))
    try:
        pg = ctx.new_page()
        pg.goto(start, wait_until="load", timeout=30000)
        knop = pg.locator("header button[aria-expanded], button[aria-controls], .menu-toggle, .hamburger, [class*='burger']").filter(visible=True).first
        if not knop.count():
            return ("niet gemeten", "geen menuknop met aria-expanded of aria-controls gevonden op 390 px: test met de hand in Playwright")
        # open: aria-expanded is true en het paneel uit aria-controls staat in beeld met links (een paneel buiten beeld telt als dicht)
        stand = """b => { const p = document.getElementById(b.getAttribute('aria-controls') || ''); const e = b.getAttribute('aria-expanded');
          const inbeeld = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
            return r.width > 0 && r.height > 0 && r.right > 0 && r.left < innerWidth && r.bottom > 0 && r.top < innerHeight
              && s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0; };
          const links = p ? [...p.querySelectorAll('a')].filter(inbeeld).length : null;
          return {open: (e === null || e === 'true') && (p ? links > 0 : e === 'true'), links}; }"""
        voor = knop.evaluate(stand)
        knop.focus()
        pg.keyboard.press("Enter")
        pg.wait_for_timeout(800)
        na_enter = knop.evaluate(stand)
        links = na_enter["links"] if na_enter["links"] is not None else "?"
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(800)
        na_escape, doel = knop.evaluate(stand)["open"], knop.get_attribute("aria-controls")
        voor, na_enter = voor["open"], na_enter["open"]
        if voor or not na_enter:
            return ("FOUT", "Enter op de menuknop opent het menu niet")
        if na_escape:
            return ("FOUT", "Escape sluit het menu niet")
        return ("goed", f"opent met Enter ({links} links in #{doel}), sluit met Escape; menulinks in VIBE-03")
    finally:
        ctx.close()


def hover(browser, start):
    """VIBE-38 en VIBE-39 op de homepage, 1366 px."""
    ctx = alleen_lezen(browser.new_context(viewport={"width": 1366, "height": 900}, user_agent=UA))
    try:
        pg = ctx.new_page()
        pg.goto(start, wait_until="load", timeout=30000)
        return submenus(pg)
    finally:
        ctx.close()


def beweeg(pg, li, van, naar):
    """Muis in vijftien stappen van 25 ms (samen ongeveer 0,4 s, als een hand) van `van` naar `naar`; is het submenu daarna nog open."""
    for k in range(1, 16):
        pg.mouse.move(van[0] + (naar[0] - van[0]) * k / 15, van[1] + (naar[1] - van[1]) * k / 15)
        pg.wait_for_timeout(25)
    pg.wait_for_timeout(300)
    return li.evaluate(SUB_STAND)["open"]


def submenus(pg):
    """Per submenu dat op hover opent (hooguit vijf): de muis gaat van het midden van de trigger (1) recht naar het dichtstbijzijnde
    punt van het submenu (VIBE-38, WCAG 1.4.13 hoverable) en (2) schuin naar de laatste link erin (VIBE-39). Alleen bewegen, nooit klikken."""
    lis, recht, schuin, getest = pg.locator("header li, nav li"), [], [], 0
    rust = (1, pg.viewport_size["height"] - 1)
    heeft = lis.evaluate_all(f"els => els.map(li => ({SUB_STAND})(li).heeft)")  # dezelfde nummering als nth(), ook in shadow DOM
    for i in [i for i, h in enumerate(heeft) if h][:30]:
        li = lis.nth(i)
        if getest == 5 or not li.is_visible():
            continue
        pg.mouse.move(*rust)
        pg.wait_for_timeout(500)
        if li.evaluate(SUB_STAND)["open"]:
            continue  # al open zonder hover: geen hover-submenu
        pg.mouse.move(*li.evaluate(SUB_STAND)["trigger"])
        pg.wait_for_timeout(500)
        st = li.evaluate(SUB_STAND)
        if not st["open"]:
            continue  # opent niet op hover: klik of geen submenu
        getest += 1
        (x, y), (links_, boven, rechts, onder) = st["trigger"], st["sub"]
        if not beweeg(pg, li, (x, y), (min(max(x, links_ + 6), rechts - 6), min(max(y, boven + 6), onder - 6))):
            recht.append(st["naam"])
        if st["links"] > 1:
            pg.mouse.move(*rust)
            pg.wait_for_timeout(500)
            pg.mouse.move(x, y)
            pg.wait_for_timeout(500)
            if not beweeg(pg, li, (x, y), st["laatste"]):
                schuin.append(st["naam"])
    if not getest:
        geen = ("goed", "geen submenu dat op hover opent in header of nav")
        return geen, geen
    return (("FOUT", f"submenu sluit op de rechte weg erheen: {', '.join(recht)}") if recht else ("goed", f"{getest} submenu(s) blijven open op de rechte weg"),
            ("na te lopen", f"submenu sluit op de schuine weg naar de laatste link: {', '.join(schuin)}") if schuin
            else ("goed", f"{getest} submenu(s) blijven open op de schuine weg"))


def knoppen(browser, paginas):
    """Klikt op elke zichtbare knop die geen verzendknop is en kijkt of er iets verandert (URL, DOM, dialoog, download, nieuw venster,
    afdrukken). window.print wordt in deze browser vervangen door een teller, zodat er geen afdrukvenster opent."""
    from playwright.sync_api import Error
    dood, geteld, gebeurd = [], 0, []
    ctx = alleen_lezen(browser.new_context(viewport={"width": 1366, "height": 900}, user_agent=UA, accept_downloads=False))
    ctx.add_init_script("window.print = () => { window.__mut = (window.__mut || 0) + 1; };")
    ctx.on("page", lambda p: gebeurd.append(p))
    try:
        pg = ctx.new_page()
        pg.on("dialog", lambda d: (gebeurd.append(d), d.dismiss()))
        pg.on("download", lambda d: gebeurd.append(d))
        for u in paginas:
            pg.goto(u, wait_until="load", timeout=30000)
            aantal = pg.locator("button:not([type=submit]):not(form button)").count()
            for i in range(min(aantal, 30)):
                if pg.url != u:
                    pg.goto(u, wait_until="load", timeout=30000)
                k = pg.locator("button:not([type=submit]):not(form button)").nth(i)
                if not k.is_visible():
                    continue
                naam = (k.inner_text() or k.get_attribute("aria-label") or "?").strip()[:30]
                pg.evaluate(TEL_MUTATIES)
                al = len(gebeurd)
                try:
                    k.click(timeout=3000, no_wait_after=True)
                    pg.wait_for_timeout(600)
                except Error:
                    continue
                geteld += 1
                if pg.url == u and len(gebeurd) == al and not pg.evaluate("window.__mut"):
                    dood.append(f"{u}: '{naam}'")
    finally:
        ctx.close()
    return ("FOUT", f"{len(dood)} knop(pen) zonder effect: " + "; ".join(dood[:4])) if dood else ("goed", f"{geteld} knoppen geklikt, elk met effect; verzendknoppen: VIBE-11")


def analytics(browser, start):
    """GA4: zonder toestemming geen meting, na een klik op accepteren wel (alleen in deze lege browsercontext)."""
    ctx = alleen_lezen(browser.new_context(viewport={"width": 1366, "height": 900}, user_agent=UA))  # het request-event komt vóór het blokkeren
    try:
        pg, metingen = ctx.new_page(), []
        pg.on("request", lambda q: re.search(r"google-analytics\.com/(g/)?collect|analytics\.google\.com/g/collect", q.url) and metingen.append(q.url))
        pg.goto(start, wait_until="load", timeout=30000)
        pg.wait_for_timeout(3000)
        voor = len(metingen)
        knop = pg.get_by_role("button", name=re.compile(r"accepte|alles toestaan|akkoord|accept all|allow all", re.IGNORECASE)).first
        if not knop.count():
            return ("niet gemeten", f"geen accepteerknop gevonden ({voor} metingen zonder klik); Search Console: GSC-hulpmiddel")
        knop.click(timeout=5000)
        pg.wait_for_timeout(4000)
        na = len(metingen) - voor
        tid = next((m.group(1) for u in metingen for m in [re.search(r"[?&]tid=(G-[A-Z0-9]+)", u)] if m), "?")
        if voor:
            return ("FOUT", f"{voor} GA-meting(en) vóór toestemming")
        if not na:
            return ("FOUT", "geen GA4-meting na accepteren")
        return ("goed", f"geen meting vóór toestemming, {na} erna (meet-ID {tid}); Search Console: niet gemeten, GSC-hulpmiddel")
    finally:
        ctx.close()


def main():
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("url")
    a.add_argument("--max", type=int, default=25, help="hooguit zoveel pagina's (standaard 25)")
    a.add_argument("--taal", default="nl")
    a.add_argument("--json", action="store_true")
    arg = a.parse_args()
    if urllib.parse.urlsplit(arg.url).scheme not in ("http", "https") or not urllib.parse.urlsplit(arg.url).hostname or not 1 <= arg.max <= 200:
        print("gebruik: vibe_meet.py https://<site> [--max 1-200] [--taal nl] [--json]", file=sys.stderr)
        return 64
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("NIET TE METEN: Playwright niet te importeren; draai met /usr/bin/python3", file=sys.stderr)
        return 3
    host = urllib.parse.urlsplit(arg.url).hostname
    if not re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+)*", host.lower()):  # de map voor de beelden komt uit de hostnaam: geen . of .. of /
        print("gebruik: de hostnaam bestaat alleen uit letters, cijfers, - en losse punten", file=sys.stderr)
        return 64
    os.umask(0o077)
    map_ = Path.home() / ".local/state/dicht-anti-vibe" / host.lower()
    map_.mkdir(parents=True, exist_ok=True)
    try:
        r, n, links = meet(arg.url.rstrip("/") + "/" if urllib.parse.urlsplit(arg.url).path in ("", "/") else arg.url, arg.max, arg.taal.lower(), map_)
    except Onbereikbaar as e:
        print(f"NIET TE METEN: {e} onbereikbaar", file=sys.stderr)
        return 69
    schoon = lambda s: re.sub("[\\x00-\\x1f\\x7f\\u200e\\u200f\\u202a-\\u202e\\u2066-\\u2069]", " ", s)[:400]
    if arg.json:
        print(json.dumps({"url": arg.url, "paginas": n, "links": links, "regels": {k: {"status": s, "detail": schoon(d)} for k, (s, d) in sorted(r.items())}}, ensure_ascii=False))
    else:
        print(f"{arg.url}: {n} pagina's, {links} links")
        for k in sorted(r):
            print(f"{k}  {r[k][0]:<12}  {schoon(r[k][1])}")
    return 1 if any(s == "FOUT" for s, _ in r.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
