import json, re, urllib.request, os
from playwright.sync_api import sync_playwright
BASE = "https://www.dahrouj.com/"
PAGES = ["", "market.html", "calculators.html", "moving-to-ottawa.html", "cottages.html", "home-value.html", "contact.html", "fairfee.html", "privacy.html"]
R = {"pages": {}, "checks": {}, "links": {}}
os.makedirs("shots", exist_ok=True)

def status(url, method="GET"):
    try:
        req = urllib.request.Request(url, method=method, headers={"User-Agent": "Mozilla/5.0 site-check"})
        with urllib.request.urlopen(req, timeout=20) as r: return r.status, r.geturl()
    except urllib.error.HTTPError as e: return e.code, url
    except Exception as e: return str(e), url

for u in ["http://dahrouj.com/", "https://dahrouj.com/", "http://www.dahrouj.com/", "https://www.dahrouj.com/sitemap.xml", "https://www.dahrouj.com/robots.txt", "https://www.dahrouj.com/llms.txt", "https://www.dahrouj.com/data/stats.json", "https://www.dahrouj.com/data/fees.json"]:
    R["checks"]["url " + u] = status(u)

import traceback
def save():
    json.dump(R, open("result.json", "w"), indent=1, ensure_ascii=False)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    seen_links = set()
    for vp, (w, h) in {"desk": (1280, 900), "phone": (390, 844)}.items():
        for p in PAGES:
            ctx = b.new_context(viewport={"width": w, "height": h})
            pg = ctx.new_page()
            errs, fails, cons = [], [], []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: cons.append(m.text) if m.type == "error" else None)
            pg.on("requestfailed", lambda r: fails.append(f"{r.url} {r.failure}"))
            pg.on("response", lambda r: fails.append(f"{r.status} {r.url}") if r.status >= 400 else None)
            pg.goto(BASE + p, wait_until="networkidle"); pg.wait_for_timeout(800)
            info = pg.evaluate("""() => ({title: document.title, h1: (document.querySelector('h1')||{}).innerText,
                sw: document.documentElement.scrollWidth, fonts: [...document.fonts].filter(f=>f.status=='loaded').length,
                imgsBroken: [...document.images].filter(i=>i.complete && i.naturalWidth===0 && !i.closest('picture source')).map(i=>i.src),
                footer: (document.querySelector('.foot')||{}).innerText,
                links: [...document.querySelectorAll('a[href]')].map(a=>a.href)})""")
            for l in info.pop("links"):
                if l.startswith(BASE) or l.startswith("https://dahrouj.com"): seen_links.add(l)
            R["pages"][f"{vp} /{p}"] = {**info, "pageErrors": errs, "consoleErrors": cons, "failedRequests": fails, "overflow": info["sw"] > w}
            pg.screenshot(path=f"shots/{vp}-{p or 'index'}.png", full_page=(vp == "phone"))
            ctx.close()

    save()
    try:
      # internal links + anchors
      for l in sorted(seen_links):
          url, _, frag = l.partition("#")
          st = status(url)
          ok = st[0] == 200
          if ok and frag:
              html = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 site-check"}), timeout=20).read().decode()
              ok = f'id="{frag}"' in html
          R["links"][l] = "ok" if ok else f"BROKEN {st}"

      pg = b.new_page(viewport={"width": 1280, "height": 900})
      errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
      # home snapshot + market stats
      pg.goto(BASE, wait_until="networkidle"); pg.wait_for_timeout(500)
      R["checks"]["home snapshot"] = pg.evaluate("[...document.querySelectorAll('[data-stat]')].map(e=>e.dataset.stat+': '+e.innerText)")
      pg.goto(BASE + "market.html", wait_until="networkidle"); pg.wait_for_timeout(500)
      R["checks"]["market rows"] = pg.evaluate("[...document.querySelectorAll('#mk-rows tr')].map(t=>t.innerText.replace(/\\s+/g,' '))")
      R["checks"]["market more rows"] = pg.evaluate("document.querySelectorAll('#mk-more tr').length")
      R["checks"]["market types"] = pg.evaluate("(document.querySelector('.types')||{}).innerText")
      R["checks"]["market summary"] = pg.evaluate("document.querySelector('#mk-summary').innerText")
      # calculators
      pg.goto(BASE + "calculators.html", wait_until="networkidle"); pg.wait_for_timeout(500)
      pg.fill("#ltt-price", "700000"); pg.dispatch_event("#ltt-price", "input"); pg.wait_for_timeout(200)
      ltt1 = pg.inner_text("#ltt-total")
      pg.check("#ltt-ftb"); pg.wait_for_timeout(200)
      R["checks"]["LTT 700k (normal / first-time)"] = [ltt1, pg.inner_text("#ltt-total"), pg.inner_text("#ltt-refund")]
      pg.click("#t-payment"); pg.fill("#pay-price", "600000"); pg.fill("#pay-down", "60000"); pg.fill("#pay-rate", "4.5"); pg.dispatch_event("#pay-rate", "input"); pg.wait_for_timeout(200)
      R["checks"]["Mortgage 600k, 60k down, 4.5%, 25y"] = {k: pg.inner_text(k) for k in ["#pay-loan", "#pay-prem", "#pay-amount"]}
      pg.click("#t-afford"); pg.fill("#aff-income", "150000"); pg.fill("#aff-down", "100000"); pg.fill("#aff-debts", "500"); pg.fill("#aff-rate", "4.5"); pg.dispatch_event("#aff-rate", "input"); pg.wait_for_timeout(200)
      R["checks"]["Affordability 150k income, 100k down"] = {k: pg.inner_text(k) for k in ["#aff-qrate", "#aff-loan", "#aff-price"]}
      # fairfee
      pg.goto(BASE + "fairfee.html", wait_until="networkidle"); pg.wait_for_timeout(500)
      R["checks"]["FairFee sell @650k"] = {k: pg.inner_text(k) for k in ["#sell-fee", "#coop-fee", "#sell-hst", "#sell-total", "#sell-keep"]}
      pg.click("#tab-buy"); pg.wait_for_timeout(200)
      R["checks"]["FairFee buy @650k"] = {k: pg.inner_text(k) for k in ["#buy-comm", "#buy-rebate"]}
      # menu + legal toggle
      pg.goto(BASE + "contact.html#search", wait_until="networkidle"); pg.wait_for_timeout(500)
      R["checks"]["contact #search preset topic"] = pg.eval_on_selector("#c-topic", "s=>s.value")
      pg.click(".menu-btn"); pg.wait_for_timeout(300)
      R["checks"]["menu opens"] = pg.evaluate("getComputedStyle(document.querySelector('#site-nav')).display")
      pg.click(".legal-btn"); pg.wait_for_timeout(200)
      R["checks"]["legal toggle opens"] = pg.evaluate("getComputedStyle(document.querySelector('#legal-text')).display")
      # address suggestions (real Geoapify, from the real origin)
      pg = b.new_page(viewport={"width": 390, "height": 844})
      geo = []
      pg.on("response", lambda r: geo.append(f"{r.status} {r.url.split('?')[0]}") if "geoapify" in r.url else None)
      pg.goto(BASE + "home-value.html", wait_until="networkidle"); pg.wait_for_timeout(500)
      pg.click("#v-address"); pg.type("#v-address", "14 Chamberlain Ave Ott", delay=60); pg.wait_for_timeout(2500)
      opts = pg.evaluate("[...document.querySelectorAll('#v-address-list [role=option]')].map(l=>l.innerText)")
      R["checks"]["address suggestions"] = {"geoapify responses": geo, "options": opts, "attribution": pg.evaluate("(document.querySelector('.addr-attrib')||{}).innerText")}
      pg.screenshot(path="shots/address-suggestions.png")
      if opts:
          pg.keyboard.press("ArrowDown"); pg.keyboard.press("Enter"); pg.wait_for_timeout(800)
      R["checks"]["address chosen"] = [pg.input_value("#v-address"), pg.input_value("#v-postal")]
      # real form submissions (one each, clearly marked as a test)
      pg.fill("#v-name", "TEST - website check (please ignore)")
      pg.fill("#v-contact", "mohamed@dahrouj.com")
      pg.fill("#v-notes", "Automated production test of the home value form after the redesign. Please ignore.")
      w3 = []
      pg.on("response", lambda r: w3.append(f"{r.status} {r.url}") if "web3forms" in r.url else None)
      pg.click("#value-form button[type=submit]"); pg.wait_for_timeout(6000)
      R["checks"]["home value form"] = {"status": pg.inner_text("#value-form .form-status"), "web3forms": w3}
      pg.goto(BASE + "contact.html", wait_until="networkidle"); pg.wait_for_timeout(500)
      w3c = []
      pg.on("response", lambda r: w3c.append(f"{r.status} {r.url}") if "web3forms" in r.url else None)
      pg.fill("#c-name", "TEST - website check (please ignore)")
      pg.fill("#c-contact", "mohamed@dahrouj.com")
      pg.fill("#c-message", "Automated production test of the contact form after the redesign. Please ignore.")
      pg.click("#contact-form button[type=submit]"); pg.wait_for_timeout(6000)
      R["checks"]["contact form"] = {"status": pg.inner_text("#contact-form .form-status"), "web3forms": w3c}
      R["checks"]["js errors during interaction"] = errs

    except Exception:
        R["ERROR"] = traceback.format_exc()
    save()
    b.close()
json.dump(R, open("result.json", "w"), indent=1, ensure_ascii=False)
