"""Make the 1200x630 link preview images in assets/img/share.
Run from anywhere: python3 scripts/make_share_images.py (needs: pip install playwright pillow; playwright install chromium)."""
import json, pathlib, html, tempfile
from playwright.sync_api import sync_playwright
from PIL import Image
SITE = pathlib.Path(__file__).resolve().parents[1]
TMP = pathlib.Path(tempfile.mkdtemp())
OUT = SITE / "assets/img/share"; OUT.mkdir(parents=True, exist_ok=True)
lakes = json.loads((SITE / "assets/img/lakes.json").read_text())
I = lambda p: f'<svg viewBox="0 0 24 24">{p}</svg>'
ICONS = {
 "receipt": '<path d="M6 3h12v18l-2-1.3-2 1.3-2-1.3-2 1.3-2-1.3L6 21z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
 "house": '<path d="M3 11 12 4l9 7"/><path d="M5 9.5V20h14V9.5"/><path d="M10 17.5l4-5"/><circle cx="10" cy="13" r="0.9"/><circle cx="14" cy="17" r="0.9"/>',
 "wallet": '<path d="M4 7.5h15a1 1 0 0 1 1 1V19a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z"/><path d="M4 7.5 15 4v3.5"/><path d="M15.5 13.75h4.5"/>',
}
CARDS = {
 "home":       dict(photo="hero-canal.webp", pos="60% 55%", title="Your next move in Ottawa, handled personally.", sub="Selling, buying and leasing across Ottawa"),
 "home-value": dict(photo="ottawa2.jpg", pos="70% 60%", title="What’s your Ottawa home worth?", sub="A free value based on recent sales nearby"),
 "moving":     dict(photo="ottawa.jpeg", pos="55% 60%", title="Moving to Ottawa", sub="Relocating for work, new to Canada, or posted to Ottawa"),
 "contact":    dict(photo="hero-canal.webp", pos="85% 70%", title="Book a consultation", sub="Our office is in the Glebe. There’s no cost to meet."),
 "market":     dict(art="bars", title="Ottawa real estate market", sub="Monthly numbers from the Ottawa Real Estate Board"),
 "calculators":dict(art="icons", title="Home buying calculators", sub="Land transfer tax, mortgage payments and affordability"),
 "cottages":   dict(art="lakes", title="Buying a cottage near Ottawa", sub="Rideau Lakes, Lanark County, Calabogie and the Ottawa Valley"),
 "fairfee":    dict(art="fairfee", title="Your home.<br>You call the shots.", sub="A lower listing fee, in writing before you hire us"),
}
def art(kind):
    if kind == "bars":
        bars = "".join(f'<div class="bar" style="height:{h}%"><span>{t}</span></div>' for h, t in [(92, "Single family"), (71, "Townhouse"), (49, "Apartment")])
        return f'<div class="bars">{bars}</div>'
    if kind == "icons":
        return '<div class="icons">' + "".join(f'<div class="ico">{I(ICONS[k])}</div>' for k in ["receipt", "house", "wallet"]) + "</div>"
    if kind == "lakes":
        return '<div class="lakes">' + "".join(f'<div class="lake"><svg viewBox="0 0 100 100"><path d="{v["d"]}"/></svg><span>{html.escape(v["lake"])}</span></div>' for v in lakes.values()) + "</div>"
    if kind == "fairfee":
        return '<div class="ffmark">Fair<b>Fee</b><sup>™</sup></div>'
    return ""
def page(c):
    bg = (f'<img class="photo" src="file://{SITE}/assets/img/{c["photo"]}" style="object-position:{c["pos"]}"><div class="shade"></div>' if "photo" in c else '<div class="solid"></div>')
    right = art(c.get("art", ""))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: SG; font-weight: 400; src: url(file://{SITE}/assets/fonts/schibsted-grotesk-latin-400-normal.woff2); }}
@font-face {{ font-family: SG; font-weight: 500; src: url(file://{SITE}/assets/fonts/schibsted-grotesk-latin-500-normal.woff2); }}
@font-face {{ font-family: SG; font-weight: 700; src: url(file://{SITE}/assets/fonts/schibsted-grotesk-latin-700-normal.woff2); }}
@font-face {{ font-family: SG; font-weight: 800; src: url(file://{SITE}/assets/fonts/schibsted-grotesk-latin-800-normal.woff2); }}
@font-face {{ font-family: Pop; font-weight: 700; src: url(file://{SITE}/assets/fonts/poppins-latin-700-normal.woff2); }}
html,body {{ margin:0; width:1200px; height:630px; overflow:hidden; font-family:SG; color:#fff; }}
.card {{ position:relative; width:1200px; height:630px; }}
.photo {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.shade {{ position:absolute; inset:0; background: linear-gradient(90deg, rgba(24,10,56,.92) 0%, rgba(24,10,56,.78) 42%, rgba(24,10,56,.15) 78%, rgba(24,10,56,0) 100%), linear-gradient(0deg, rgba(24,10,56,.55), rgba(24,10,56,0) 35%); }}
.solid {{ position:absolute; inset:0; background: radial-gradient(circle at 85% 30%, #3B1F7A 0%, #260E58 55%, #1B0A40 100%); }}
.content {{ position:absolute; left:72px; top:64px; bottom:56px; width:{'640' if right else '700'}px; display:flex; flex-direction:column; }}
.logo {{ display:flex; align-items:flex-end; line-height:1; font-family:Pop; font-weight:700; font-size:30px; }}
.logo .t {{ letter-spacing:-.005em; margin-left:.06em; margin-bottom:.08em; }}
.mark {{ display:block; width:38.7px; height:41.1px; object-fit:contain; flex:none; }}
h1 {{ margin:auto 0 18px; font-size:{'64' if right else '66'}px; line-height:1.03; letter-spacing:-.035em; font-weight:800; }}
.sub {{ font-size:27px; line-height:1.3; color:rgba(255,255,255,.88); margin:0 0 34px; }}
.sig {{ font-size:17px; color:rgba(255,255,255,.75); border-top:1px solid rgba(255,255,255,.25); padding-top:16px; }}
.art {{ position:absolute; right:64px; top:0; bottom:0; width:380px; display:flex; align-items:center; justify-content:center; }}
.bars {{ display:flex; align-items:flex-end; gap:26px; height:330px; }}
.bar {{ width:86px; border-radius:14px 14px 4px 4px; background:linear-gradient(180deg,#B9A2F2,#7C5CC9); position:relative; }}
.bar span {{ position:absolute; bottom:-34px; left:50%; transform:translateX(-50%); white-space:nowrap; font-size:16px; color:rgba(255,255,255,.75); }}
.icons {{ display:grid; gap:22px; }}
.ico {{ width:112px; height:112px; border-radius:28px; background:rgba(185,162,242,.18); display:flex; align-items:center; justify-content:center; }}
.ico:nth-child(2) {{ margin-left:90px; }}
.ico svg {{ width:60px; height:60px; fill:none; stroke:#D9CCFA; stroke-width:1.5; stroke-linecap:round; stroke-linejoin:round; }}
.lakes {{ display:grid; grid-template-columns:1fr 1fr; gap:18px 26px; }}
.lake {{ text-align:center; }}
.lake svg {{ width:150px; height:150px; }}
.lake path {{ fill:rgba(185,162,242,.22); stroke:#D9CCFA; stroke-width:.9; stroke-linejoin:round; }}
.lake span {{ display:block; font-size:15px; color:rgba(255,255,255,.75); margin-top:2px; }}
.ffmark {{ font-size:96px; letter-spacing:-.03em; font-weight:500; color:#fff; }}
.ffmark b {{ font-weight:800; }} .ffmark sup {{ font-size:34px; font-weight:600; vertical-align:top; position:relative; top:12px; }}
</style></head><body><div class="card">{bg}
<div class="content"><div class="logo"><img class="mark" src="file://{TMP / 'logo-white.png'}"><span class="t">ahrouj.com</span></div>
<h1>{c['title']}</h1><p class="sub">{c['sub']}</p>
<div class="sig">Mohamed Dahrouj, Sales Representative · Right at Home Realty, Brokerage</div></div>
{f'<div class="art">{right}</div>' if right else ''}
</div></body></html>"""
_logo = Image.open(SITE / "assets/img/dahrouj-logo.png").convert("RGBA")
_white = Image.new("RGBA", _logo.size, (255, 255, 255, 255)); _white.putalpha(_logo.split()[3]); _white.save(TMP / "logo-white.png")
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
    for name, c in CARDS.items():
        f = TMP / f"{name}.html"; f.write_text(page(c))
        pg.goto(f.resolve().as_uri()); pg.wait_for_timeout(500)
        pg.screenshot(path=str(TMP / f"{name}.png"))
        Image.open(TMP / f"{name}.png").convert("RGB").save(OUT / f"{name}.jpg", quality=84, optimize=True, progressive=True)
        print(name, (OUT / f"{name}.jpg").stat().st_size // 1024, "KB")
    b.close()
