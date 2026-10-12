import json
from playwright.sync_api import sync_playwright
R={}
with sync_playwright() as pw:
    b=pw.chromium.launch()
    pg=b.new_page(viewport={"width":390,"height":844})
    log=[]
    pg.on("request", lambda r: log.append(f"REQ {r.method} {r.url} {r.headers.get('content-type','')}") if "web3forms" in r.url else None)
    pg.on("requestfailed", lambda r: log.append(f"FAILED {r.method} {r.url} {r.failure}"))
    pg.on("response", lambda r: log.append(f"RESP {r.status} {r.url}") if "web3forms" in r.url else None)
    pg.on("console", lambda m: log.append(f"CONSOLE {m.type}: {m.text}"))
    pg.goto("https://www.dahrouj.com/contact.html", wait_until="networkidle")
    pg.fill("#c-name","TEST - website check (please ignore)"); pg.fill("#c-contact","mohamed@dahrouj.com")
    pg.fill("#c-message","Automated production test of the contact form. Please ignore.")
    pg.click("#contact-form button[type=submit]"); pg.wait_for_timeout(8000)
    R["status"]=pg.inner_text("#contact-form .form-status"); R["log"]=log
    b.close()
json.dump(R,open("form_result.json","w"),indent=1)
