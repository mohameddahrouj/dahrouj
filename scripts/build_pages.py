"""Write the static pages with one shared header and footer."""
import pathlib, sys, json, re

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1]
DESC_SITE = "Full-service Ottawa real estate agent with Right at Home Realty, Brokerage. Personal help selling, buying and leasing, relocating to Ottawa, newcomers to Canada, military postings and cottages near Ottawa."

FF_MARK = """<span class="ff-logo" aria-label="FairFee trademark"><span class="ff-word">Fair<b>Fee</b></span><sup>™</sup></span>"""

def head(title, desc, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://www.dahrouj.com/assets/img/hero-canal-1400.webp">
  <link rel="icon" href="assets/img/favicon-32x32.png">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="preload" href="assets/fonts/schibsted-grotesk-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/site.css">{extra}
</head>
"""

NAV = [("home-value.html", "What’s my home worth?", "home-value"), ("market.html", "Ottawa Market", "market"),
       ("moving-to-ottawa.html", "Moving to Ottawa", "moving"), ("fairfee.html", '<span class="ff-word">Fair<b>Fee</b></span><sup>™</sup>', "fairfee"), ("contact.html", "Contact", "contact")]

def header(active):
    links = "\n".join(
        f'        <a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for h, t, k in NAV)
    return f"""<body{' class="home"' if active == "home" else ""}>
<!--SITE-BODY-START-->
<a class="skip" href="#main">Skip to content</a>
<header class="top" id="top">
  <div class="wrap top-row">
    <a class="brand" href="./" aria-label="dahrouj.com, home">
      <span class="brand-mark" aria-hidden="true"></span><span class="brand-text" aria-hidden="true">ahrouj.com</span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="menu-icon" aria-hidden="true"></span><span class="menu-label">Menu</span>
    </button>
    <nav class="nav" id="site-nav" aria-label="Main">
{links}
    </nav>
  </div>
</header>
"""

FOOTER = f"""
<footer class="foot">
  <div class="wrap foot-row">
    <div class="brokerage">
      <picture>
        <source srcset="assets/img/rahr-logo-white.svg" media="(prefers-color-scheme: dark)">
        <img class="rahr-logo" src="assets/img/rahr-logo.svg" alt="Right at Home Realty, Brokerage" width="85" height="77">
      </picture>
      <span class="brokerage-name"><span class="agent-name">Mohamed Dahrouj, Sales Representative</span><span>Right at Home Realty, Brokerage</span></span>
    </div>
    <nav class="foot-meta" aria-label="Footer">
      <a class="foot-link" href="calculators.html">Calculators</a>
      <a class="foot-link" href="privacy.html">Privacy</a>
      <button class="foot-link legal-btn" type="button" aria-expanded="false" aria-controls="legal-text">Legal</button>
      <a class="social" href="https://www.instagram.com/dahroujrealestate" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" class="dot"/></svg></a>
    </nav>
    <div class="legal-text" id="legal-text">
      <p>Right at Home Realty, Brokerage, independently owned and operated, 14 Chamberlain Ave, Suite 101, Ottawa, ON K1S 1V9. Office 613-369-5199. Not intended to solicit buyers or sellers currently under contract with a brokerage.</p>
      <p>MLS®, Multiple Listing Service® and REALTOR® are trademarks controlled by the Canadian Real Estate Association. FairFee™ is a trademark of its owner.</p>
    </div>
    <p class="foot-copy">© <span class="year">2026</span> Mohamed Dahrouj. All rights reserved.</p>
  </div>
</footer>
<nav class="callbar" aria-label="Call or text">
  <a href="tel:+16138695923"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h3.5l1.5 5-2 1.5a12 12 0 0 0 6.5 6.5L16 14l5 1.5V19a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>Call</a>
  <a href="sms:+16138695923"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/></svg>Text</a>
</nav>
<!--SITE-BODY-END-->
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""

LD = """
  <script type="application/ld+json">
  {"@context": "https://schema.org", "@type": "RealEstateAgent", "@id": "https://www.dahrouj.com/#agent",
    "name": "Mohamed Dahrouj, Right at Home Realty, Brokerage", "url": "https://www.dahrouj.com/",
    "description": "Full-service Ottawa real estate sales representative helping people sell, buy and lease homes, relocate to Ottawa, settle as newcomers to Canada, move on Canadian Armed Forces postings, and buy cottages near Ottawa.",
    "telephone": "+1-613-869-5923", "email": "mohamed@dahrouj.com", "image": "https://www.dahrouj.com/assets/img/hero-canal-1400.webp",
    "logo": "https://www.dahrouj.com/assets/img/android-chrome-512x512.png",
    "parentOrganization": {"@type": "Organization", "name": "Right at Home Realty, Brokerage"},
    "address": {"@type": "PostalAddress", "streetAddress": "14 Chamberlain Ave, Suite 101", "addressLocality": "Ottawa", "addressRegion": "ON", "postalCode": "K1S 1V9", "addressCountry": "CA"},
    "geo": {"@type": "GeoCoordinates", "latitude": 45.40787, "longitude": -75.69195},
    "areaServed": ["Ottawa", "Kanata", "Stittsville", "Barrhaven", "Findlay Creek", "Riverside South", "Orléans", "Manotick", "Westboro", "The Glebe", "Rideau Lakes", "Lanark County", "Calabogie", "Ottawa Valley"],
    "knowsAbout": ["Selling a home in Ottawa", "Buying a home in Ottawa", "Relocating to Ottawa", "Newcomers to Canada buying a home", "Canadian Armed Forces posting and military relocation to Ottawa", "Buying a cottage near Ottawa", "First-time home buyers", "Ottawa real estate market statistics"],
    "makesOffer": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Home selling", "areaServed": "Ottawa"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Home buying", "areaServed": "Ottawa"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Relocation and military posting home search", "areaServed": "Ottawa"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Cottage and waterfront purchases", "areaServed": "Eastern Ontario"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Free home valuation", "areaServed": "Ottawa"}}
    ],
    "sameAs": ["https://www.instagram.com/dahroujrealestate"]}
  </script>"""

AREAS = [
    ("kanata", "Kanata", "West end",
     "A large west-end suburb built around the Kanata North tech park, with established neighbourhoods like Kanata Lakes, Beaverbrook, Bridlewood and Morgan’s Grant.",
     "Detached family homes and townhomes, close to the Canadian Tire Centre, Kanata Centrum and the Queensway."),
    ("stittsville", "Stittsville", "West end",
     "Just southwest of Kanata, with a village-style main street and newer subdivisions growing around it.",
     "Mostly newer detached homes and townhomes, with the Trans Canada Trail running through town."),
    ("barrhaven", "Barrhaven", "South end",
     "One of Ottawa’s biggest family suburbs, including Stonebridge and Half Moon Bay, with its own shopping, schools and recreation centres.",
     "Detached homes and townhomes, many built in the last twenty years."),
    ("findlay-creek", "Findlay Creek", "South end",
     "A newer community off Bank Street and Leitrim Road near the airport, with parks, trails and new schools.",
     "Mostly newer townhomes and detached homes, popular with first-time buyers moving up."),
    ("riverside-south", "Riverside South", "South end",
     "A growing community along the Rideau River, across from Barrhaven and connected to the O-Train’s Trillium Line.",
     "Newer detached homes and townhomes, with more construction under way."),
    ("orleans", "Orléans", "East end",
     "A large, bilingual east-end community along the Ottawa River, with established and newer neighbourhoods side by side.",
     "A wide mix, from older bungalows and split-levels to new townhomes."),
    ("manotick", "Manotick", "Rural south",
     "A historic village on the Rideau River, known for Watson’s Mill and its quiet, small-town feel.",
     "Larger lots, estate homes and waterfront properties within reach of the city."),
    ("westboro", "Westboro", "Inner west",
     "A walkable inner-city neighbourhood centred on Richmond Road shops and restaurants, close to the Ottawa River pathways.",
     "Older homes, modern infill and condos."),
    ("glebe", "The Glebe", "Central",
     "Our home base. A central neighbourhood between Bank Street, Lansdowne Park and the Rideau Canal.",
     "Older brick homes, semis and low-rise condos in walking distance of downtown."),
]

CTA = """<div class="actions"><a class="btn" href="contact.html">Let’s talk</a><a class="btn btn-quiet" href="home-value.html">What’s my home worth?</a></div>"""

def SEARCH_CTA(tag):
    return f"""<div class="actions"><a class="btn" href="contact.html#{tag}">Start my custom search</a><a class="btn btn-quiet" href="contact.html">Let’s talk</a></div>"""

def area_cards():
    out = []
    for slug, name, region, about, homes in AREAS:
        out.append(f"""      <details class="area" id="{slug}">
        <summary><span class="area-name">{name}</span><span class="area-region">{region}</span></summary>
        <p>{about}</p>
        <p class="area-homes">{homes}</p>
      </details>""")
    return "\n".join(out)

HOME = f"""
<main id="main">
  <section class="wrap hero-wrap">
    <div class="hero">
      <picture>
        <source media="(max-width: 700px)" srcset="assets/img/hero-canal-tall.webp">
        <img class="hero-bg" src="assets/img/hero-canal.webp" srcset="assets/img/hero-canal-1400.webp 1400w, assets/img/hero-canal.webp 2400w" sizes="100vw" width="2400" height="1350" alt="" fetchpriority="high">
      </picture>
      <div class="hero-text">
        <h1>Your next move in Ottawa, handled personally.</h1>
        <p class="lede">Full-service real estate for selling, buying and leasing, with the same person from your first call to closing day.</p>
        <div class="actions"><a class="btn btn-light" href="contact.html">Let’s talk</a><a class="btn btn-ghost-light" href="home-value.html">What’s my home worth?</a></div>
      </div>
    </div>
  </section>

  <section id="services" class="wrap section">
    <h2>Everything handled for you</h2>
    <div class="tiles">
      <div class="tile"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 21V3"/><path d="M5 5h12l-2.5 3.5L17 12H5"/></svg><h3>Selling</h3><p>A plan, a price and a full launch</p></div>
      <a class="tile tile-link" href="calculators.html#afford"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="8" cy="15.5" r="4.5"/><path d="M11.2 12.3 20 3.5"/><path d="M17 6.5l3 3"/><path d="M14.6 8.9l2 2"/></svg><h3>Buying</h3><p>Find it, price it, win it</p><span class="tile-more">See what you can afford →</span></a>
      <div class="tile"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="3" width="10" height="18" rx="1"/><path d="M14 9h6v12h-6"/><path d="M7.5 7h3M7.5 11h3M7.5 15h3"/></svg><h3>Leasing &amp; investing</h3><p>Rentals, tenants and the numbers</p></div>
      <div class="tile"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21h18"/><path d="M6 21v-7"/><path d="M11 21V5"/><path d="M16 21v-10"/><path d="M21 21v-4"/></svg><h3>Pricing research</h3><p>Recent sales on your street</p></div>
      <div class="tile"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="14" height="6" rx="1.5"/><path d="M17 6h3v5.5h-8V15"/><rect x="10.5" y="15" width="3" height="6" rx="1"/></svg><h3>Staging &amp; paint</h3><p>Ready for buyers on day one</p></div>
      <div class="tile"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 8h4l2-3h6l2 3h4v12H3z"/><circle cx="12" cy="13.5" r="3.8"/></svg><h3>Photos &amp; video</h3><p>Professional media for every listing</p></div>
    </div>
    <a class="fee-strip" href="fairfee.html">
      <span class="fee-strip-mark">{FF_MARK}</span>
      <span class="fee-strip-text"><strong>A lower listing fee, in writing before you hire us.</strong> <span>Full service, same as always.</span></span>
      <span class="link fee-strip-go">See our fees <span aria-hidden="true">→</span></span>
    </a>
  </section>

  <section class="wrap section help-more">
    <h2>Moving to Ottawa, or out to the lake?</h2>
    <div class="next-links">
      <a class="next" href="moving-to-ottawa.html#relocating"><span class="h3">Relocating to Ottawa</span><span>New job or transfer? We’ll match neighbourhoods to your commute, schools and budget, and can show homes by video.</span></a>
      <a class="next" href="moving-to-ottawa.html#newcomers"><span class="h3">Newcomers to Canada</span><span>Buying or renting your first Canadian home, explained step by step, from mortgages to closing.</span></a>
      <a class="next" href="moving-to-ottawa.html#military"><span class="h3">Military postings</span><span>Posted to Ottawa or posted out? We work to your report date and relocation paperwork.</span></a>
      <a class="next" href="cottages.html"><span class="h3">Cottages near Ottawa</span><span>Rideau Lakes, Calabogie, Lanark County and the Ottawa Valley, with the checks waterfront needs.</span></a>
    </div>
  </section>

  <section class="wrap section snapshot">
    <div class="split-head">
      <h2>Ottawa market, <span data-stat="label">September 2026</span></h2>
      <span class="snap-links"><a class="link" href="market.html">See the full report</a><a class="link" href="market.html#alerts">Get sales updates for your area</a></span>
    </div>
    <dl class="figures">
      <div><dt>Average sale price</dt><dd data-stat="averagePrice">$685,640</dd><dd class="sub" data-stat="averagePriceChange">−1.0% from a year ago</dd></div>
      <div><dt>Homes sold</dt><dd data-stat="sales">1,010</dd><dd class="sub" data-stat="salesChange">−6.6% from a year ago</dd></div>
      <div><dt>Months of inventory</dt><dd data-stat="moi">4.8</dd><dd class="sub" data-stat="moiChange">4.1 a year ago</dd></div>
    </dl>
    <div class="areas-teaser">
      <h3>Where we work</h3>
      <ul class="chips">
{chr(10).join(f'        <li><a href="market.html#{s}">{n}</a></li>' for s, n, *_ in AREAS)}
      </ul>
    </div>
  </section>

  <section class="band">
    <div class="wrap section closing">
      <h2>Thinking about a move?</h2>
      <p>Tell us what you’re planning and we’ll set up a time to talk it through. There’s no cost to meet.</p>
      {CTA}
    </div>
  </section>
</main>
"""

NEIGHBOURHOODS = f"""
<main id="main">
  <section class="wrap page-head">
    <h1>Ottawa neighbourhoods</h1>
    <p class="lede">From the west-end suburbs to the inner city, these are the areas we buy and sell in most. Ask us about any of them, or one that isn’t listed.</p>
  </section>
  <section class="wrap section areas">
{area_cards()}
  </section>
  <section class="band">
    <div class="wrap section closing">
      <h2>Weighing two neighbourhoods?</h2>
      <p>We’ll pull recent sales for both so you can compare prices, how fast homes are selling and what your budget gets you.</p>
      {CTA}
    </div>
  </section>
</main>
"""

MARKET_TMPL = """
<main id="main" class="wrap">
  <section class="page-head">
    <h1>Ottawa market, <span id="mk-month">September 2026</span></h1>
    <p id="mk-summary" class="lede">Monthly numbers from the Ottawa Real Estate Board.</p>
  </section>
  <section class="section market-grid">
    <div class="table-wrap">
      <table class="stats">
        <thead>
          <tr><th scope="col">Citywide</th><th scope="col" id="mk-col-now">This month</th><th scope="col">vs a year ago</th></tr>
        </thead>
        <tbody id="mk-rows"></tbody>
      </table>
      <details class="more-stats">
        <summary>More stats</summary>
        <table class="stats"><tbody id="mk-more"></tbody></table>
      </details>
    </div>
    <div class="types">
      <h2 class="h3">Benchmark price by home type</h2>
      <ul id="mk-types" class="bars"></ul>
      <p class="fine">The benchmark (MLS® Home Price Index) tracks a typical home, so it moves less than the average price when the mix of sales changes.</p>
    </div>
  </section>
  <p class="source" id="mk-source"></p>
  <section class="section neighbourhoods" id="neighbourhoods" aria-labelledby="nb-h">
    <h2 id="nb-h">Neighbourhoods</h2>
    <p class="fine">Areas we work in across Ottawa. Tap one to learn more, or ask about one that isn’t listed.</p>
    <div class="areas">
AREA_CARDS
    </div>
  </section>
  <section class="section closing market-close">
    <h2>Want the numbers for your street?</h2>
    <p>We’ll pull recent sales near you, or compare two neighbourhoods side by side.</p>
    CTA_PAIR
  </section>
</main>
"""

def num_field(id_, label, value, step="1000", prefix="$", suffix="", extra=""):
    pre = f'<span class="affix">{prefix}</span>' if prefix else ""
    suf = f'<span class="affix">{suffix}</span>' if suffix else ""
    return f"""<div class="field"><label for="{id_}">{label}</label><div class="affixed">{pre}<input id="{id_}" type="number" inputmode="decimal" min="0" step="{step}" value="{value}"{extra}>{suf}</div></div>"""

CALCULATORS = f"""
<main id="main" class="wrap">
  <section class="page-head">
    <h1>Calculators</h1>
    <p class="lede">Quick estimates for buying in Ottawa. Your lender and lawyer will confirm the exact numbers.</p>
    <div class="tabs calc-tabs" role="tablist" aria-label="Choose a calculator" data-tabs>
      <button role="tab" id="t-ltt" aria-controls="ltt" aria-selected="true"><svg class="tab-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h12v18l-2-1.3-2 1.3-2-1.3-2 1.3-2-1.3L6 21z"/><path d="M9 8h6M9 12h6M9 16h3"/></svg><span>Land transfer</span></button>
      <button role="tab" id="t-payment" aria-controls="payment" aria-selected="false" tabindex="-1"><svg class="tab-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11 12 4l9 7"/><path d="M5 9.5V20h14V9.5"/><path d="M10 17.5l4-5"/><circle cx="10" cy="13" r="0.9"/><circle cx="14" cy="17" r="0.9"/></svg><span>Mortgage</span></button>
      <button role="tab" id="t-afford" aria-controls="afford" aria-selected="false" tabindex="-1"><svg class="tab-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7.5h15a1 1 0 0 1 1 1V19a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z"/><path d="M4 7.5 15 4v3.5"/><path d="M15.5 13.75h4.5"/></svg><span>Affordability</span></button>
    </div>
  </section>

  <section class="calc-block" id="ltt" role="tabpanel" aria-labelledby="t-ltt">
    <div class="calc-intro">
      <h2 id="ltt-h">Land transfer tax</h2>
      <p>Ontario’s tax on buying a home, paid on closing. Ottawa has no separate city land transfer tax.</p>
    </div>
    <form class="calc-form" data-calc="ltt" novalidate>
      {num_field("ltt-price", "Purchase price", 650000)}
      <label class="check"><input id="ltt-ftb" type="checkbox"> First-time home buyer</label>
      <dl class="results">
        <div><dt>Ontario land transfer tax</dt><dd id="ltt-tax"></dd></div>
        <div><dt>First-time buyer refund</dt><dd id="ltt-refund"></dd></div>
        <div class="total"><dt>You pay on closing</dt><dd id="ltt-total"></dd></div>
      </dl>
      <p class="fine">Rates for a home with one or two single-family residences: 0.5% up to $55,000, 1% to $250,000, 1.5% to $400,000, 2% to $2 million and 2.5% above. First-time buyers can get up to $4,000 back.</p>
    </form>
  </section>

  <section class="calc-block" id="payment" role="tabpanel" aria-labelledby="t-payment" hidden>
    <div class="calc-intro">
      <h2 id="pay-h">Mortgage payment</h2>
      <p>Your regular payment, including CMHC insurance when you put down less than 20%.</p>
    </div>
    <form class="calc-form" data-calc="payment" novalidate>
      <div class="field-row">
        {num_field("pay-price", "Purchase price", 650000)}
        {num_field("pay-down", "Down payment", 65000)}
      </div>
      <div class="field-row">
        {num_field("pay-rate", "Interest rate", 4.29, step="0.01", prefix="", suffix="%")}
        <div class="field"><label for="pay-amort">Amortization</label><select id="pay-amort"><option value="25" selected>25 years</option><option value="30">30 years</option><option value="20">20 years</option><option value="15">15 years</option></select></div>
        <div class="field"><label for="pay-freq">Payments</label><select id="pay-freq"><option value="monthly" selected>Monthly</option><option value="biweekly">Every two weeks</option><option value="accel">Accelerated every two weeks</option><option value="weekly">Weekly</option></select></div>
      </div>
      <dl class="results">
        <div><dt>Mortgage amount</dt><dd id="pay-loan"></dd></div>
        <div><dt>CMHC insurance added</dt><dd id="pay-prem"></dd></div>
        <div class="total"><dt id="pay-label">Monthly payment</dt><dd id="pay-amount"></dd></div>
      </dl>
      <p class="fine" id="pay-msg">Uses semi-annual compounding, as Canadian fixed-rate mortgages do.</p>
      <p class="fine">With less than 20% down, CMHC insurance (2.80% to 4.00% of the mortgage) is added for you.</p>
    </form>
  </section>

  <section class="calc-block" id="afford" role="tabpanel" aria-labelledby="t-afford" hidden>
    <div class="calc-intro">
      <h2 id="aff-h">Affordability</h2>
      <p>The highest price you’re likely to qualify for, using the federal stress test and standard debt limits.</p>
    </div>
    <form class="calc-form" data-calc="afford" novalidate>
      <div class="field-row">
        {num_field("aff-income", "Household income (yearly, before tax)", 140000)}
        {num_field("aff-down", "Down payment saved", 80000)}
      </div>
      <div class="field-row">
        {num_field("aff-debts", "Other debt payments (monthly)", 400, step="50")}
        {num_field("aff-rate", "Interest rate", 4.29, step="0.01", prefix="", suffix="%")}
      </div>
      <details class="more-opts">
        <summary>More options <span class="opt">(property tax, utilities, condo fees)</span></summary>
        <div class="field-row">
          {num_field("aff-tax", "Property tax (monthly)", 450, step="25")}
          {num_field("aff-utilities", "Utilities (monthly)", 250, step="10")}
          {num_field("aff-condo", "Condo fees (monthly)", 0, step="25")}
        </div>
      </details>
      <dl class="results">
        <div><dt>Qualifying rate</dt><dd id="aff-qrate"></dd></div>
        <div><dt>Largest mortgage</dt><dd id="aff-loan"></dd></div>
        <div class="total"><dt>Price you could afford</dt><dd id="aff-price"></dd></div>
      </dl>
      <p class="fine" id="aff-msg">Lenders qualify you at the higher of your rate plus 2% or 5.25%, with housing costs under 39% of income and all debts under 44%. Assumes a 25-year amortization, $450 a month in property tax and $250 in utilities unless you change them.</p>
    </form>
  </section>

  <section class="section closing calc-close">
    <h2>Selling too?</h2>
    <p>Find out what your home could sell for before you buy.</p>
    {CTA}
  </section>
</main>
"""


HOMEVALUE = """
<main id="main" class="wrap">
  <section class="page-head">
    <h1>What’s my home worth?</h1>
    <p class="lede">Online estimates miss what makes your home different. Send us your address and we’ll get back to you with a free, no-obligation value based on recent sales nearby.</p>
  </section>
  <section class="calc-block value-block" id="value" aria-labelledby="val-h">
    <div class="calc-intro">
      <h2 id="val-h">How it works</h2>
      <ol class="steps icon-steps">
        <li><svg class="li-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/></svg><span><strong>Send your address.</strong> That’s all we need to start.</span></li>
        <li><svg class="li-ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.4 15.4 21 21"/><path d="M7.5 11.5 10.5 9l3 2.5V14h-6z"/></svg><span><strong>We study recent sales nearby,</strong> on your street and in homes like yours.</span></li>
        <li><svg class="li-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/><path d="M12 10.5v7M14 11.8c-.4-.6-1.1-.9-2-.9-1.1 0-2 .6-2 1.5 0 2 4 1 4 3 0 .9-.9 1.5-2 1.5-.9 0-1.7-.4-2.1-1"/></svg><span><strong>You get your value,</strong> with the sales behind it, from a real person.</span></li>
      </ol>
    </div>
    <form class="calc-form" id="value-form" data-form="valuation" novalidate autocomplete="off">
      <div class="field addr">
        <label for="v-address">Property address</label>
        <input id="v-address" name="address" type="text" required placeholder="Start typing, e.g. 123 Main St" role="combobox" aria-describedby="v-address-hint" aria-autocomplete="list" aria-expanded="false" aria-controls="v-address-list" autocomplete="off">
        <ul class="addr-list" id="v-address-list" role="listbox" hidden></ul>
        <p class="hint" id="v-address-hint">Just the address. Leave the rest to us.</p>
        <input type="hidden" name="postal_code" id="v-postal">
        <input type="hidden" name="coordinates" id="v-coords">
      </div>
      <div class="field-row">
        <div class="field">
          <label for="v-name">Name</label>
          <input id="v-name" name="name" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="v-contact">Phone or email</label>
          <input id="v-contact" name="contact" autocomplete="email" inputmode="email" required>
        </div>
      </div>
      <div class="field">
        <label for="v-notes">Anything we should know? <span class="opt">(optional)</span></label>
        <textarea id="v-notes" name="notes" rows="3" placeholder="Renovations, finished basement, garage, lot size"></textarea>
      </div>
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn" type="submit">Get my home value</button>
      <p class="form-privacy">We’ll only use this to reply to you. <a href="privacy.html">Privacy</a></p>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </section>

</main>
"""

CONTACT = """
<main id="main" class="wrap contact">
  <section class="contact-head">
    <h1 id="c-title">Let’s talk about your move</h1>
    <p class="lede" id="c-lede">Tell us a little about your plans and we’ll be in touch to find a time.</p>
  </section>
  <form class="contact-form" id="contact-form" data-form="contact" novalidate>
    <div class="field-row">
      <div class="field">
        <label for="c-name">Name</label>
        <input id="c-name" name="name" autocomplete="name" required>
      </div>
      <div class="field">
        <label for="c-contact">Phone or email</label>
        <input id="c-contact" name="contact" autocomplete="email" inputmode="email" required>
      </div>
    </div>
    <div class="field">
      <label for="c-topic">How can we help?</label>
      <select id="c-topic" name="topic">
        <option>Selling a home</option>
        <option>Buying a home</option>
        <option>Starting a custom home search</option>
        <option>Buying and selling</option>
        <option>Renting or leasing</option>
        <option>Relocating to Ottawa</option>
        <option>A military posting</option>
        <option>Buying a cottage</option>
        <option>Something else</option>
      </select>
    </div>
    <div class="field">
      <label for="c-message">Message <span class="opt">(optional)</span></label>
      <textarea id="c-message" name="message" rows="4" placeholder="Budget, timing, neighbourhoods, must-haves"></textarea>
    </div>
    <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <button class="btn" type="submit">Send request</button>
    <p class="form-privacy">We’ll only use this to reply to you. <a href="privacy.html">Privacy</a></p>
    <p class="form-status" role="status" aria-live="polite"></p>
    <p class="fine">Selling? <a class="link" href="home-value.html">Get your home’s value</a> with just your address.</p>
  </form>
  <section class="contact-info">
    <dl class="reach">
      <div><dt>Mobile</dt><dd><a href="tel:+16138695923">613-869-5923</a></dd></div>
      <div><dt>Office</dt><dd><a href="tel:+16133695199">613-369-5199</a></dd></div>
      <div><dt>Email</dt><dd><a href="mailto:mohamed@dahrouj.com">mohamed@dahrouj.com</a></dd></div>
    </dl>
    <figure class="office-map">
      <a href="https://www.openstreetmap.org/?mlat=OFFICE_LAT&amp;mlon=OFFICE_LON#map=17/OFFICE_LAT/OFFICE_LON" target="_blank" rel="noopener">
        OFFICE_MAP_SVG
      </a>
      <figcaption><strong>Our office in the Glebe</strong><br>14 Chamberlain Ave, Suite 101, Ottawa, ON K1S 1V9<br><a href="https://www.google.com/maps/search/?api=1&amp;query=14+Chamberlain+Ave+Ottawa+ON" target="_blank" rel="noopener">Get directions</a> <span class="attrib">Map © OpenStreetMap contributors</span></figcaption>
    </figure>
  </section>
</main>
""".replace("AREA_OPTIONS", "".join(f'<option value="{n}"></option>' for _, n, *_ in AREAS))

FAIRFEE = f"""
<main id="main">
  <section class="wrap ff-hero">
    <div class="ff-intro">
      <p class="ff-badge">Proud agent on {FF_MARK}</p>
      <h1>Your home.<br>You call the shots.</h1>
      <p class="lede">Set the terms, see every dollar and stay in control of your sale. A lower listing fee, in writing before you hire us, with full service included. Move the price to see your numbers.</p>
      <a class="btn btn-quiet" href="contact.html">Let’s talk</a>
    </div>
    <div class="calc" id="calc">
      <div class="tabs" role="tablist" aria-label="Choose selling or buying">
        <button role="tab" id="tab-sell" aria-controls="panel-sell" aria-selected="true">Selling</button>
        <button role="tab" id="tab-buy" aria-controls="panel-buy" aria-selected="false" tabindex="-1">Buying</button>
      </div>
      <div class="price-input">
        <label for="price">Home price</label>
        <div class="price-row">
          <input id="price" type="range" min="100000" max="1500000" step="5000" value="650000">
          <output id="price-out" for="price">$650,000</output>
        </div>
      </div>
      <div role="tabpanel" id="panel-sell" aria-labelledby="tab-sell" class="panel">
        <dl class="ledger">
          <div><dt>Listing brokerage <span id="sell-rate"></span></dt><dd id="sell-fee"></dd></div>
          <div><dt>Buyer’s brokerage <span id="coop-rate"></span></dt><dd id="coop-fee"></dd></div>
          <div><dt>HST on commission (13%)</dt><dd id="sell-hst"></dd></div>
          <div class="total"><dt>Total commission</dt><dd id="sell-total"></dd></div>
        </dl>
        <p class="keep"><span class="keep-label">You keep</span> <strong id="sell-keep"></strong> <span class="keep-small">before your mortgage payout and legal fees</span></p>
        <p class="fine" id="sell-note"></p>
      </div>
      <div role="tabpanel" id="panel-buy" aria-labelledby="tab-buy" class="panel" hidden>
        <dl class="ledger">
          <div><dt>Commission our brokerage receives <span id="buy-rate"></span></dt><dd id="buy-comm"></dd></div>
        </dl>
        <p class="keep"><span class="keep-label">Cash back to you</span> <strong id="buy-rebate"></strong> <span class="keep-small">after closing</span></p>
        <p class="fine" id="buy-note"></p>
      </div>
    </div>
  </section>

  <p class="wrap ff-small">FairFee™ is a separate project and isn’t a Right at Home Realty service.</p>
</main>
"""


MOVING = """
<main id="main">
  <section class="wrap page-head">
    <h1>Moving to Ottawa</h1>
    <p class="lede">Whether you’re relocating for work, arriving in Canada, or moving on a military posting, we help you find the right neighbourhood and the right home, often before you’ve set foot in the city.</p>
    <nav class="jump" aria-label="On this page">
      <a href="#relocating">Relocating</a><a href="#newcomers">Newcomers to Canada</a><a href="#military">Military postings</a><a href="#faq">Questions</a>
    </nav>
  </section>

  <section class="wrap section topic" id="relocating" aria-labelledby="rel-h">
    <div class="topic-intro">
      <div class="topic-head"><svg class="topic-ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7"/><path d="M3 12.5h18"/><path d="M12 11.5v2"/></svg><h2 id="rel-h">Relocating to Ottawa for work</h2></div>
      <p>Ottawa’s big employers are spread out: federal departments downtown and in Gatineau, the Kanata North tech park in the west end, hospitals and universities in the core. Where you work shapes where you’ll want to live.</p>
      <p class="topic-link"><a class="link" href="calculators.html#afford">See what you can afford →</a></p>
    </div>
    <ul class="checks">
      <li>A neighbourhood shortlist that fits your commute, schools and budget</li>
      <li>Video tours when you can’t be here in person</li>
      <li>Closing dates timed with the sale of your current home</li>
      <li>Help finding a rental first, if you’d rather settle in</li>
    </ul>
  </section>

  <section class="band">
    <div class="wrap section topic" id="newcomers" aria-labelledby="new-h">
      <div class="topic-intro">
        <div class="topic-head"><svg class="topic-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21v-4.5"/><path d="M12 16.5 7.6 17.3l.6-1.9-5.2-4.1 1.6-.9-1-3.2 2.8.6.8-1.7 2.9 2.6-.8-4.8 2.1 1.1L12 2.5l1.6 2.5 2.1-1.1-.8 4.8 2.9-2.6.8 1.7 2.8-.6-1 3.2 1.6.9-5.2 4.1.6 1.9z"/></svg><h2 id="new-h">Newcomers to Canada</h2></div>
        <p>Buying or renting your first home in a new country comes with new rules and new words. We explain each step in plain language and take the time to answer every question.</p>
        <p class="topic-link"><a class="link" href="calculators.html#payment">Estimate your mortgage payment →</a></p>
      </div>
      <ul class="checks">
        <li>How buying works in Ontario, step by step, from offer to closing</li>
        <li>Lenders with newcomer mortgage programs, even without a long Canadian credit history</li>
        <li>Federal rules on who can buy, and first-time buyer programs, checked for your situation</li>
        <li>Renting first while you settle in</li>
      </ul>
    </div>
  </section>

  <section class="wrap section topic" id="military" aria-labelledby="mil-h">
    <div class="topic-intro">
      <div class="topic-head"><svg class="topic-ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="9" width="19" height="10" rx="5"/><path d="M8.5 9V7.5A1.5 1.5 0 0 1 10 6h4a1.5 1.5 0 0 1 1.5 1.5V9"/><path d="M8 9v10M16 9v10"/></svg><h2 id="mil-h">Military postings</h2></div>
      <p>Posted to National Defence Headquarters at the Carling campus, CFS Leitrim or another Ottawa unit? Or posted out and need to sell? Military moves run on fixed dates, so we plan around yours.</p>
    </div>
    <ul class="checks">
      <li>House-hunting trips and closing dates planned around your report date</li>
      <li>Help with the paperwork your relocation provider asks for</li>
      <li>Neighbourhoods near your unit: Kanata and Westboro for Carling, Findlay Creek and Riverside South for Leitrim</li>
      <li>Selling or renting out your home when you’re posted out</li>
    </ul>
  </section>

  <section class="band">
    <div class="wrap section faq" id="faq" aria-labelledby="faq-h">
      <h2 id="faq-h">Common questions</h2>
      FAQ_ITEMS
    </div>
  </section>

  <section class="wrap section closing">
    <h2>Start your custom search</h2>
    <p>Tell us your budget, timing and must-haves. We’ll build a custom search, send you a neighbourhood shortlist and new listings as they come up, and get started right away.</p>
    {SEARCH_MOVE}
  </section>
</main>
"""

MOVING_FAQ = [
    ("Can you help me buy a home in Ottawa before I move there?",
     "Yes. We shortlist neighbourhoods and homes for you, tour them by live video, and handle offers and paperwork remotely, so many clients buy before they arrive."),
    ("Which Ottawa neighbourhoods are good for families relocating?",
     "It depends on where you’ll work and your budget. Kanata, Stittsville, Barrhaven, Findlay Creek, Riverside South and Orléans are popular family suburbs, while the Glebe and Westboro suit people who want to walk to shops and downtown."),
    ("Can newcomers to Canada get a mortgage?",
     "Many lenders have programs for newcomers, including permanent residents and some work permit holders, even without a long Canadian credit history. We connect you with mortgage specialists who work with newcomers."),
    ("I’ve been posted to Ottawa. How quickly can you help me find a home?",
     "We can start as soon as you have your posting message. We plan your house-hunting trip around the days you’re given and set closing dates to match your report date."),
    ("Do you help people rent in Ottawa as well as buy?",
     "Yes. Many people rent first while they get to know the city, and we help with finding and applying for leases."),
]

COTTAGES = r"""
<main id="main">
  <section class="wrap page-head">
    <h1>Buying a cottage near Ottawa</h1>
    <p class="lede">From the Rideau Lakes to Calabogie, there’s lake country within a short drive of the city. A cottage is a different purchase from a house in town, and we’ll help you get the details right.</p>
  </section>

  <section class="wrap section topic" aria-labelledby="where-h">
    <div class="topic-intro">
      <h2 id="where-h">Where people look</h2>
      <p>Each area has its own feel, from busy boating lakes to quiet bays. We’ll help you narrow it down by drive time, water and budget.</p>
    </div>
    <div class="lakes">
      <div class="lake-card">
        <svg class="lake" viewBox="0 0 100 100" role="img" aria-label="Outline of Big Rideau Lake"><path d="M34.3,45.7 33.5,47.1 33.3,46.6 32.8,47.1 32.8,45.8 32.4,45.9 32.6,47.5 33.0,47.6 32.0,48.2 32.1,49.6 31.5,50.0 31.1,49.5 30.0,49.7 30.4,48.1 29.0,48.4 29.6,49.0 28.0,51.3 24.4,54.2 24.9,54.6 24.7,55.2 25.1,54.7 25.5,55.5 26.2,54.6 26.6,55.2 27.0,54.8 26.4,54.6 26.6,54.2 28.5,53.3 29.5,52.2 29.9,52.9 31.4,51.9 30.8,52.8 32.6,51.5 32.4,52.1 33.0,51.7 33.7,50.6 34.2,51.3 33.9,52.2 34.3,51.9 32.6,54.9 31.9,54.7 30.1,56.5 29.4,56.2 28.1,57.5 25.8,57.6 24.8,58.7 25.0,59.4 24.4,60.1 26.9,58.5 27.5,59.0 27.5,58.1 28.2,58.2 29.7,56.5 28.0,60.9 27.6,62.7 28.2,63.4 27.9,64.3 26.8,66.3 25.4,65.6 26.3,66.5 25.5,66.9 26.1,67.9 25.5,68.4 24.7,68.1 23.8,69.9 22.8,69.4 20.7,69.7 20.8,70.5 22.7,69.8 24.3,70.2 24.4,70.9 24.7,70.3 24.6,70.8 22.9,72.6 21.7,71.9 21.8,70.8 20.8,72.3 19.9,69.8 18.7,71.7 19.2,71.8 18.9,72.6 19.7,72.9 19.2,72.2 19.7,71.9 20.2,72.3 19.9,72.8 21.8,73.9 20.5,75.3 20.5,76.0 20.4,75.3 19.6,75.0 19.4,75.8 20.2,75.7 20.0,76.6 17.6,79.6 15.5,81.2 15.1,82.1 10.1,85.2 10.3,86.5 7.3,86.6 7.4,87.5 6.9,87.9 7.3,88.8 8.1,88.5 9.0,89.9 10.4,88.5 10.6,87.2 11.5,87.8 11.5,89.1 12.5,89.0 12.0,90.7 10.7,92.0 11.6,92.8 10.2,94.6 10.2,95.0 12.0,93.4 11.1,96.0 12.1,94.1 13.3,93.7 12.7,93.6 13.6,89.4 15.1,88.3 15.6,86.6 16.4,87.7 16.9,87.5 17.4,86.3 16.7,86.5 16.3,86.0 18.2,83.7 20.1,84.3 21.0,85.4 22.1,85.3 23.4,87.4 24.1,91.1 25.3,89.5 25.2,88.2 26.2,86.7 28.2,87.6 27.7,89.1 28.2,89.1 28.9,88.8 29.2,87.4 29.7,87.9 29.1,88.7 30.7,88.5 31.3,87.7 30.5,86.3 32.2,87.0 32.6,85.6 33.7,86.6 32.9,87.7 34.5,87.2 33.7,88.3 35.6,88.1 36.6,89.1 36.1,89.6 36.4,90.3 38.1,88.7 38.0,89.2 38.8,89.2 38.8,88.5 39.3,88.8 39.9,87.9 39.1,87.6 40.2,86.8 40.3,86.0 41.7,85.4 42.0,83.8 41.0,83.7 42.1,82.0 41.1,82.5 40.9,81.6 41.1,81.3 41.2,82.0 42.2,81.0 42.1,79.1 42.6,78.5 42.1,77.8 42.5,76.6 42.0,77.1 42.3,75.9 41.8,73.9 41.2,74.0 41.1,75.5 41.5,75.3 40.7,76.4 40.9,77.1 40.1,77.6 39.9,76.7 40.3,78.9 39.0,79.7 39.0,80.6 38.2,79.8 37.7,80.0 38.8,79.0 38.8,77.1 39.3,77.6 38.7,76.1 39.8,76.6 40.3,75.6 39.9,74.9 40.2,74.0 39.9,74.6 39.6,74.1 40.0,74.2 40.4,72.5 40.1,72.3 39.1,73.0 40.8,70.6 40.6,70.2 39.3,71.3 40.0,70.4 39.3,70.6 39.3,69.9 38.1,69.6 39.9,63.1 40.8,64.0 40.8,63.1 41.9,62.6 40.9,62.6 39.8,60.9 39.7,62.0 39.1,62.1 38.6,63.0 38.3,64.3 38.8,63.5 38.9,64.3 37.2,69.4 35.9,69.4 36.0,70.3 37.0,69.9 36.6,72.2 36.4,71.8 35.2,73.4 34.9,72.4 34.0,74.9 34.1,75.3 34.5,75.1 34.4,76.1 33.3,74.9 33.1,73.8 35.1,71.1 34.5,70.6 34.4,71.2 34.1,70.1 33.9,71.8 32.7,73.9 31.8,72.7 31.6,71.0 32.0,68.3 32.3,68.6 32.6,67.1 33.5,66.6 33.1,65.3 32.8,66.1 32.4,66.0 33.1,64.4 33.0,61.8 33.9,60.7 32.8,61.1 34.3,58.8 34.3,58.2 33.7,58.9 33.8,57.3 34.7,53.5 35.7,52.5 35.3,52.3 35.4,49.8 36.5,47.7 38.8,47.5 39.4,46.3 38.7,43.9 39.1,42.1 39.5,41.9 40.1,42.7 41.1,41.9 41.0,39.1 42.3,39.9 44.0,38.9 43.8,36.5 44.4,35.3 44.9,35.7 45.5,35.5 45.0,37.5 45.6,36.2 46.9,35.3 47.2,36.1 47.7,36.1 47.1,34.8 47.7,32.7 48.7,32.6 50.1,29.9 52.2,28.9 52.6,29.3 53.1,28.6 53.2,29.5 54.3,29.2 54.4,30.4 56.1,29.5 56.8,31.0 57.4,31.1 58.2,29.0 58.0,27.6 59.7,25.4 62.1,24.8 62.8,22.2 63.6,21.6 64.6,21.8 64.5,23.3 65.6,22.6 66.4,23.0 66.7,22.0 68.0,21.9 68.5,23.4 68.6,22.6 69.2,22.9 69.1,22.1 70.3,22.1 71.5,21.3 71.4,20.9 72.6,20.5 72.9,20.1 71.9,20.0 71.2,17.6 70.4,17.2 69.9,16.2 70.4,15.9 70.6,12.4 71.3,12.2 71.8,10.8 72.7,11.8 73.2,10.7 75.8,10.9 76.1,10.1 75.7,8.8 77.1,9.4 77.5,7.7 78.2,8.8 77.9,10.2 78.7,10.3 79.3,9.5 80.1,11.1 81.9,10.4 82.0,12.2 82.6,12.1 82.1,10.1 82.8,8.6 84.0,9.1 85.0,9.0 84.5,8.6 85.0,8.4 86.8,8.7 86.9,7.7 87.2,8.4 88.2,8.6 90.5,10.4 93.1,10.8 87.0,7.7 86.7,8.4 84.6,8.2 82.6,4.0 82.5,8.0 82.3,8.4 81.9,8.1 81.2,6.6 81.2,9.7 80.5,9.3 80.4,8.1 79.1,6.7 76.9,6.7 77.3,7.3 76.8,9.0 76.2,8.2 75.8,5.5 76.0,7.9 75.2,8.9 75.9,10.3 73.7,10.2 72.7,8.5 72.8,9.2 72.0,8.6 71.6,9.6 70.9,9.6 70.8,11.3 70.0,11.3 69.5,13.5 68.0,13.6 68.3,14.1 67.5,14.0 65.3,16.3 64.8,15.9 63.9,16.7 63.5,16.2 61.1,16.4 61.3,12.7 60.7,13.1 60.2,11.5 59.2,11.3 58.2,12.4 58.4,13.6 59.8,12.8 59.8,14.3 60.9,14.7 60.2,15.9 57.8,17.2 57.9,17.9 57.0,17.8 57.1,18.5 56.4,17.9 56.4,17.0 55.9,17.8 56.0,16.9 55.2,16.8 53.3,17.6 52.5,18.8 52.6,20.1 55.1,21.2 54.3,21.3 53.8,22.4 54.0,24.3 52.0,27.6 52.3,28.3 51.1,28.4 50.7,27.0 49.2,28.0 48.2,27.1 49.7,28.7 50.1,27.9 50.7,28.0 50.4,28.7 49.1,29.3 47.8,28.9 46.9,29.9 47.2,28.7 46.8,28.4 45.7,30.8 44.7,31.8 44.5,30.4 43.1,32.1 42.9,30.9 43.6,29.5 43.8,30.4 44.8,28.0 43.4,29.0 43.4,27.9 42.4,27.3 40.9,28.1 40.6,28.8 41.4,29.5 41.0,31.6 41.4,31.8 39.9,32.6 39.1,34.6 38.9,33.3 37.7,34.2 37.4,40.7 35.8,44.6 35.4,44.9 35.1,44.2 34.3,45.7Z"/></svg>
        <div><h3>Rideau Lakes</h3><p class="lake-name">Big Rideau Lake</p><p>A chain of lakes along the Rideau Canal system southwest of Ottawa, popular for boating and family cottages.</p></div>
      </div>
      <div class="lake-card">
        <svg class="lake" viewBox="0 0 100 100" role="img" aria-label="Outline of Mississippi Lake"><path d="M54.0,25.4 55.2,21.2 57.8,20.6 57.3,15.6 54.1,14.3 47.9,13.3 47.6,12.3 48.5,10.5 51.5,9.9 51.7,8.4 53.8,7.0 53.9,5.2 56.1,4.2 57.9,4.6 59.0,4.0 61.6,4.3 62.9,5.3 65.0,5.4 66.2,6.4 67.3,6.0 68.2,6.6 70.2,6.6 70.9,9.2 70.7,10.5 69.6,10.8 66.7,14.1 64.7,14.9 63.9,14.5 63.2,13.8 63.3,12.3 62.5,12.1 62.2,16.6 61.3,18.2 62.2,18.5 62.4,19.6 63.1,20.0 63.4,19.4 64.3,19.5 66.0,21.5 72.4,25.7 73.3,27.3 73.7,31.4 75.4,35.4 74.9,36.8 73.1,37.9 70.9,37.3 70.0,34.8 69.3,35.4 68.7,34.8 66.3,39.7 66.4,40.8 66.9,40.8 66.8,43.0 67.8,44.9 67.3,45.6 68.3,46.6 68.3,48.5 68.8,49.3 67.5,54.4 66.4,56.6 66.5,58.9 67.7,60.2 67.0,60.8 67.1,61.9 68.3,63.7 68.0,64.8 66.1,66.9 65.6,68.5 64.7,68.4 64.4,67.6 64.2,70.9 63.4,72.0 63.0,75.0 64.2,74.7 64.5,75.2 63.7,76.1 64.5,76.5 64.3,77.0 62.6,76.9 60.9,77.6 60.4,77.3 60.4,76.0 57.3,78.6 55.5,77.0 53.5,79.0 52.5,77.9 51.9,82.3 52.1,84.9 51.7,86.5 50.7,86.4 50.2,86.9 50.6,88.7 50.1,89.3 49.4,93.8 48.1,95.2 46.4,95.5 46.1,96.0 44.9,94.6 43.7,95.8 41.3,95.7 39.8,93.0 38.8,93.4 38.2,94.6 37.8,94.3 37.9,90.3 36.9,89.7 36.9,88.4 35.5,86.5 34.1,82.7 34.3,81.4 33.4,81.7 32.5,81.2 31.9,78.6 30.9,78.8 30.1,80.6 30.5,78.8 29.2,77.8 28.9,75.5 25.7,72.6 24.6,70.3 26.1,68.5 27.1,68.2 29.3,69.0 32.2,70.5 32.7,73.3 33.0,73.2 33.3,69.7 37.2,69.0 37.8,69.7 39.1,68.8 42.3,69.3 48.6,70.4 52.0,72.0 53.0,71.1 53.6,69.0 55.0,67.7 55.4,68.5 54.7,69.7 55.3,71.3 55.2,73.1 55.6,73.4 56.3,73.1 56.4,73.8 57.9,71.0 58.7,71.9 58.9,73.1 59.3,72.9 58.6,70.9 60.1,68.1 61.5,67.9 63.0,65.7 63.0,64.4 61.4,65.3 61.2,64.7 61.9,62.1 60.7,62.9 60.2,64.1 57.4,65.8 57.0,65.4 57.9,62.7 59.9,59.5 59.7,58.7 60.4,58.5 60.0,57.5 61.2,56.6 60.7,54.3 59.8,54.2 60.8,54.1 60.9,53.3 59.9,53.4 60.9,52.5 61.2,54.0 61.9,53.6 62.2,52.2 61.3,51.5 62.5,51.5 64.6,44.4 63.4,44.5 62.8,43.8 62.2,45.1 60.7,46.0 59.1,45.5 58.6,43.5 58.7,40.2 61.7,36.3 57.7,36.6 56.6,35.9 56.3,35.1 57.1,32.5 54.8,29.4 54.0,25.4Z"/></svg>
        <div><h3>Lanark County</h3><p class="lake-name">Mississippi Lake</p><p>Smaller lakes and rivers west of the city, with a mix of seasonal cottages and year-round homes.</p></div>
      </div>
      <div class="lake-card">
        <svg class="lake" viewBox="0 0 100 100" role="img" aria-label="Outline of Calabogie Lake"><path d="M93.6,43.7 93.1,43.4 92.8,44.1 92.0,43.9 92.8,45.6 92.2,45.1 92.0,46.1 91.8,45.0 91.1,45.3 91.4,46.2 92.7,46.9 91.4,46.4 91.7,47.1 91.0,49.4 91.5,49.8 91.3,51.0 90.1,51.6 90.3,52.4 89.3,52.7 89.6,54.3 88.3,54.3 88.0,53.6 86.8,54.4 89.7,56.9 89.6,56.2 90.0,56.3 91.4,58.9 92.4,58.7 93.1,59.8 94.3,59.6 93.9,62.1 93.2,62.5 92.5,62.2 92.0,61.0 90.0,59.9 87.4,59.9 86.9,60.5 86.2,60.1 82.6,55.7 81.5,55.0 81.3,54.2 78.4,51.9 77.9,50.3 75.7,50.5 74.5,47.8 74.1,48.5 73.7,48.0 72.8,45.5 71.0,45.0 69.1,42.5 67.7,40.1 67.0,37.1 66.7,38.7 64.5,40.3 64.6,41.8 64.0,42.2 64.4,42.3 63.9,42.6 64.3,43.4 63.7,44.7 63.1,50.1 62.5,50.7 63.0,50.8 62.7,54.1 63.0,56.6 62.3,60.3 60.7,63.6 58.9,64.6 56.0,69.6 57.6,71.7 57.6,72.8 60.6,79.3 59.8,80.5 60.2,81.7 59.6,84.9 58.9,84.4 61.0,87.8 60.6,89.0 58.5,88.8 57.5,87.2 57.2,85.0 55.7,83.7 54.1,83.9 53.8,82.1 52.2,80.9 54.7,79.0 55.7,81.4 56.4,81.4 57.2,76.6 57.0,76.0 56.4,76.2 56.0,75.6 54.9,76.6 54.4,73.4 53.3,73.0 52.8,73.3 52.8,74.4 54.7,77.5 54.4,79.0 52.9,80.1 51.7,80.0 50.9,77.4 49.7,77.6 49.8,78.3 48.5,78.9 46.9,79.2 45.5,77.6 45.2,76.4 44.2,75.8 43.7,77.1 42.0,78.2 41.1,77.6 40.8,78.9 40.2,79.0 38.9,78.9 38.5,76.7 36.7,75.9 35.0,77.2 33.5,77.4 31.7,81.9 27.4,83.0 27.7,85.9 26.4,88.1 26.5,91.4 27.4,92.9 30.4,92.8 32.3,94.5 31.5,94.8 30.6,93.9 31.2,95.2 29.3,93.6 29.6,94.8 28.9,96.0 27.7,95.5 27.6,94.3 25.9,93.4 24.3,92.8 24.4,89.6 23.4,88.0 23.9,85.6 23.4,81.3 24.3,74.7 23.1,74.4 18.5,77.0 15.1,75.0 14.7,72.7 16.4,69.1 16.2,67.1 16.9,64.9 16.6,64.6 15.8,65.6 14.3,64.8 13.3,61.0 9.5,59.4 8.9,55.8 7.3,55.3 5.7,55.6 5.3,55.0 8.5,54.8 9.7,54.0 9.9,53.3 9.4,52.2 8.9,52.2 8.8,52.8 7.5,52.9 6.2,50.7 7.0,49.8 8.7,49.3 8.5,48.7 9.8,47.5 11.0,47.9 12.4,47.3 15.2,48.2 16.0,47.4 18.1,47.4 19.4,46.6 23.9,36.0 23.7,34.3 24.3,34.3 25.1,35.4 26.0,35.3 26.5,36.1 27.0,34.7 26.1,34.8 26.6,32.3 28.6,29.2 27.6,27.6 25.1,26.4 25.4,25.6 25.9,26.4 26.6,26.1 26.0,24.4 25.4,24.4 25.7,23.9 27.2,26.1 29.5,26.9 31.1,26.1 32.3,24.6 35.7,24.2 37.0,23.7 37.5,22.9 37.1,22.6 40.4,22.5 40.3,21.9 40.9,21.5 43.0,21.9 44.9,21.1 47.6,22.4 48.8,22.4 48.9,23.7 49.6,23.2 50.5,24.1 51.8,23.0 51.3,21.4 52.1,19.7 55.8,17.9 57.8,19.1 58.2,22.0 57.2,23.1 60.1,24.4 62.1,23.9 63.7,24.9 63.5,22.3 63.1,21.6 62.2,22.7 62.6,21.7 62.0,21.7 64.6,18.6 66.5,18.8 69.1,15.6 71.1,14.8 73.4,13.0 73.9,12.0 75.8,11.2 76.9,11.7 77.8,11.0 78.1,9.6 81.3,7.6 81.9,6.3 84.8,4.0 86.5,4.8 85.1,7.1 82.3,7.8 78.1,11.0 77.4,13.1 78.5,14.3 78.0,16.0 74.0,20.1 70.5,22.7 69.6,22.5 70.3,22.7 69.4,22.9 68.2,24.5 68.9,26.4 68.5,28.8 69.2,26.5 69.8,26.9 69.5,27.3 71.3,26.7 72.8,25.5 74.4,27.3 79.9,27.0 82.5,28.3 83.0,29.1 82.7,29.7 85.6,31.3 87.3,34.1 87.1,37.0 87.9,39.0 87.5,40.7 87.9,41.9 88.4,39.6 87.6,38.1 87.7,37.5 88.9,38.4 90.4,38.1 91.4,39.2 91.9,38.8 91.4,39.4 92.4,39.9 91.9,40.0 92.2,40.6 93.3,40.5 93.2,41.2 94.7,42.1 94.1,42.0 93.6,43.7Z"/></svg>
        <div><h3>Calabogie</h3><p class="lake-name">Calabogie Lake</p><p>Calabogie Lake and the surrounding hills, with skiing and trails as well as the water.</p></div>
      </div>
      <div class="lake-card">
        <svg class="lake" viewBox="0 0 100 100" role="img" aria-label="Outline of White Lake"><path d="M71.0,38.8 72.0,39.4 72.2,38.2 74.0,39.0 74.4,38.4 75.2,39.4 77.1,39.2 80.1,40.9 78.4,43.7 79.4,47.7 77.7,49.5 76.5,50.0 75.0,52.5 72.3,53.4 72.1,54.0 72.8,55.1 75.4,54.7 74.8,56.6 75.3,57.7 73.7,59.4 74.5,59.9 75.9,59.2 76.4,63.3 78.0,65.5 80.6,67.5 80.8,65.9 78.6,60.6 77.0,59.7 77.1,58.6 79.7,56.9 81.2,54.0 80.8,53.3 82.6,51.5 83.3,49.2 82.7,46.8 83.4,46.2 83.8,44.0 85.0,43.9 85.8,42.4 87.1,43.8 88.2,42.4 89.9,41.9 90.3,41.2 90.6,41.7 91.0,40.9 91.5,41.0 92.3,36.4 91.2,35.1 87.2,35.1 83.2,39.3 83.1,40.3 82.5,40.4 77.3,37.8 75.2,35.9 73.8,35.6 70.6,37.3 70.0,35.9 70.6,35.5 69.4,35.2 69.2,34.1 67.3,32.8 66.9,31.9 63.0,31.0 62.6,30.4 63.4,29.8 63.0,29.0 64.8,28.4 64.2,28.7 63.0,27.1 62.3,23.9 63.2,23.3 62.3,21.6 62.7,20.8 62.8,22.0 64.3,23.5 66.1,22.5 67.0,21.2 68.1,22.2 67.2,21.1 69.0,16.0 68.3,13.2 69.3,11.2 68.6,9.7 69.3,7.1 68.9,6.4 61.1,4.0 59.7,5.6 57.1,5.1 55.5,5.6 54.8,7.6 56.1,8.5 56.4,10.1 57.7,11.7 59.6,12.2 59.9,13.8 60.4,14.0 58.2,19.5 55.7,19.4 55.6,20.4 55.0,20.3 53.6,21.5 55.0,20.9 55.4,21.4 58.0,20.9 58.8,21.4 59.5,22.6 60.5,27.6 59.6,29.6 56.8,31.0 56.4,30.8 54.7,33.2 53.4,33.7 52.6,33.0 51.0,36.8 49.9,36.9 50.3,38.6 49.7,40.2 51.2,37.9 51.8,37.6 52.3,38.2 52.4,37.5 52.9,37.5 52.7,36.3 54.0,37.6 54.1,40.7 54.9,40.1 54.9,38.5 55.3,39.1 54.3,43.1 54.2,47.1 51.9,49.3 51.6,55.7 51.3,56.6 51.1,55.6 50.6,59.0 48.7,63.6 46.7,67.2 43.6,70.2 42.3,72.6 41.6,72.0 41.4,73.0 40.8,73.4 41.1,72.4 37.5,75.9 37.1,76.6 38.4,77.0 36.8,79.6 35.6,80.4 35.3,80.0 34.7,81.0 32.3,81.2 31.0,83.9 26.4,86.3 25.0,86.2 23.2,88.2 19.2,89.6 18.2,88.9 17.0,89.6 11.4,90.7 10.7,91.5 9.0,91.9 10.5,92.1 9.1,93.7 10.0,93.7 10.3,94.3 7.8,95.1 7.8,95.8 8.7,95.9 11.0,96.0 13.5,94.3 15.1,95.1 17.9,94.0 17.8,92.6 19.7,92.0 20.2,93.2 23.9,95.1 25.6,94.4 25.8,95.1 26.9,95.0 29.2,93.6 30.7,94.7 32.4,92.9 31.9,92.0 33.2,90.8 32.6,90.1 34.9,90.1 35.1,91.3 36.2,90.7 36.6,90.2 36.1,90.1 37.1,89.9 37.0,89.3 38.0,89.5 39.3,88.6 42.2,89.6 43.1,89.0 45.9,89.2 49.2,91.0 52.1,91.5 53.3,91.2 53.6,90.2 56.3,90.6 59.0,91.7 60.9,91.5 65.3,93.3 65.4,93.9 68.7,94.3 69.6,95.7 70.4,95.7 69.8,95.1 70.1,94.1 73.6,93.9 76.0,92.4 76.9,93.1 77.3,92.4 78.3,93.0 79.5,92.4 79.8,91.7 78.7,91.6 79.7,91.1 79.2,89.9 76.8,90.6 75.2,90.2 73.6,91.0 72.4,89.5 71.1,89.7 69.5,87.6 68.7,88.6 63.0,88.8 60.6,88.1 60.3,87.1 57.0,87.8 56.6,86.9 54.7,86.4 53.3,87.3 51.7,86.9 49.9,87.5 46.9,86.2 45.6,86.7 45.1,86.2 45.4,85.5 44.9,85.6 44.6,85.0 44.0,84.9 43.3,85.9 42.6,85.6 42.0,84.9 43.1,84.3 43.2,83.5 41.6,82.9 43.8,82.8 43.4,81.9 44.2,82.1 44.9,80.9 45.9,80.9 48.2,79.0 49.3,79.9 49.2,78.8 50.7,76.2 52.0,75.9 51.9,75.2 53.0,76.1 52.6,76.5 52.7,78.7 53.4,79.9 54.1,79.7 54.7,78.5 55.4,79.1 58.3,79.0 59.4,81.2 60.4,81.4 63.0,79.2 63.3,79.9 63.7,79.4 64.2,79.9 64.4,80.7 65.2,80.3 66.4,81.5 66.3,79.1 65.1,76.6 64.7,77.1 64.0,77.0 64.4,76.4 63.5,76.3 61.5,74.7 61.8,74.3 59.4,71.8 62.1,71.9 63.8,72.9 63.3,72.1 65.3,71.6 65.6,70.7 62.2,69.1 61.5,69.1 61.1,69.7 60.1,69.0 60.1,70.1 58.8,70.3 58.7,69.4 58.6,69.8 57.7,69.0 56.1,68.9 56.4,67.4 57.6,67.3 55.0,64.4 54.9,62.4 56.7,60.0 56.6,59.0 57.2,58.1 55.8,55.1 56.2,51.5 57.0,50.7 57.0,49.8 59.2,49.7 59.9,47.8 61.2,50.5 61.3,48.4 63.3,48.2 61.8,46.4 61.2,46.6 61.4,45.8 59.8,44.7 59.1,43.2 61.1,41.3 60.4,41.0 61.0,39.4 60.7,37.8 61.9,38.6 62.3,42.4 67.6,44.6 73.9,44.5 73.9,43.6 73.3,43.3 73.4,40.8 72.8,40.0 71.0,40.0 70.6,39.3 71.0,38.8Z"/></svg>
        <div><h3>Ottawa Valley</h3><p class="lake-name">White Lake</p><p>Waterfront along the Ottawa and Madawaska Rivers and lakes like White Lake, from quiet retreats to larger properties.</p></div>
      </div>
    </div>
    <p class="fine lakes-note">Lake outlines © OpenStreetMap contributors.</p>
  </section>

  <section class="band">
    <div class="wrap section topic" aria-labelledby="checks-h">
      <div class="topic-intro">
        <h2 id="checks-h">What we check on a cottage</h2>
        <p>These are the things that catch city buyers off guard. We build them into your offer so you know what you’re buying before you firm up.</p>
      </div>
      <ul class="checks icon-checks">
        <li><svg class="li-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5s6 6.4 6 10.5a6 6 0 0 1-12 0c0-4.1 6-10.5 6-10.5z"/><path d="M9 14.5a3 3 0 0 0 3 3"/></svg>Well water: flow and water quality testing</li>
        <li><svg class="li-ico" viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="7" rx="7" ry="2.5"/><path d="M5 7v9c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5V7"/><path d="M12 2v2.5"/><path d="M19 11.5h2.5"/></svg>Septic system: age, size and an inspection</li>
        <li><svg class="li-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 16.5V13l2.2-4.5h9.6L18 13h1.5A1.5 1.5 0 0 1 21 14.5v2h-2"/><path d="M3 13h15"/><path d="M9 16.5h5.5"/><circle cx="7" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/></svg>Road access: year-round municipal road, or a private or seasonal road with shared costs</li>
        <li><svg class="li-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9c1.5-1.3 3-1.3 4.5 0s3 1.3 4.5 0 3-1.3 4.5 0 3 1.3 4.5 0"/><path d="M3 14c1.5-1.3 3-1.3 4.5 0s3 1.3 4.5 0 3-1.3 4.5 0 3 1.3 4.5 0"/><path d="M3 19c1.5-1.3 3-1.3 4.5 0s3 1.3 4.5 0 3-1.3 4.5 0 3 1.3 4.5 0"/></svg>Shoreline: ownership of the shore road allowance, docks and frontage</li>
        <li><svg class="li-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6z"/><path d="M9 12l2.2 2.2L15.5 10"/></svg>Insurance and financing, which can differ for seasonal properties</li>
        <li><svg class="li-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21a6 6 0 0 0 6-6c0-3.5-2.5-5.5-3.5-8.5-1.5 1.5-2 3-2 4.5-1-.8-1.8-2.2-1.8-3.8C8 9 6 11.5 6 15a6 6 0 0 0 6 6z"/><path d="M12 21a2.5 2.5 0 0 1-2.5-2.5c0-1.6 1.3-2.4 2.5-4 1.2 1.6 2.5 2.4 2.5 4A2.5 2.5 0 0 1 12 21z"/></svg>Heating, winterizing and internet for year-round use</li>
      </ul>
    </div>
  </section>

  <section class="wrap section faq" aria-labelledby="cfaq-h">
    <h2 id="cfaq-h">Common questions</h2>
    FAQ_ITEMS
  </section>

  <section class="band">
    <div class="wrap section closing">
      <h2>Start your cottage search</h2>
      <p>Tell us your budget, how far you’ll drive and the kind of water you want. We’ll build a custom search and send you cottages as they list.</p>
      {SEARCH_COTTAGE}
    </div>
  </section>
</main>
"""

COTTAGE_FAQ = [
    ("Where can I buy a cottage near Ottawa?",
     "Popular areas include the Rideau Lakes, Lanark County, Calabogie and the Ottawa Valley, all within a comfortable drive of the city."),
    ("Is buying a cottage different from buying a house?",
     "Yes. Cottages often have a well, a septic system, a private or seasonal road, and shoreline rules, and financing and insurance can differ. We make sure each is checked before you firm up your offer."),
    ("Can I get a mortgage on a cottage?",
     "Usually, yes. Year-round, easily accessible cottages are treated much like houses, while seasonal properties may need a larger down payment. We’ll connect you with lenders who finance recreational properties."),
    ("Do you help sell cottages too?",
     "Yes. We price cottages using recent sales on the same lake or area and market them to Ottawa buyers looking for a getaway."),
]

def faq_html(items):
    return "\n".join(f'''<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>''' for q, a in items)

def faq_ld(items):
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return "\n  <script type=\"application/ld+json\">" + json.dumps(data, ensure_ascii=False) + "</script>"

MOVING = MOVING.replace("FAQ_ITEMS", faq_html(MOVING_FAQ))
COTTAGES = COTTAGES.replace("FAQ_ITEMS", faq_html(COTTAGE_FAQ))


# ---------- Ottawa Market page, built from data/stats.json so the numbers are in the page itself ----------
ST = json.loads((ROOT / "data/stats.json").read_text())
SVG = lambda p, cls="mk-ico": f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{p}</svg>'
MK_ICONS = {
    "sales": '<circle cx="8" cy="15.5" r="4.5"/><path d="M11.2 12.3 20 3.5"/><path d="M17 6.5l3 3"/><path d="M14.6 8.9l2 2"/>',
    "averagePrice": '<path d="M3 12V4h8l9.5 9.5-8 8z"/><circle cx="7.5" cy="8" r="1.4"/>',
    "benchmarkPrice": '<path d="M3 20h18"/><path d="M4 16l5-5 4 3 7-8"/><path d="M15 6h5v5"/>',
    "activeListings": '<path d="M5 21V3"/><path d="M5 6h14v8H5"/><path d="M9 6v-2M15 6v-2"/>',
    "daysOnMarket": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5"/><path d="M9.5 3h5"/>',
    "saleToListRatio": '<path d="M4 20 20 4"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
    "Single family": '<path d="M3 11 12 4l9 7"/><path d="M5 9.5V20h14V9.5"/><path d="M10 20v-5h4v5"/>',
    "Townhouse": '<path d="M2 11l3.5-3.5L9 11l3-3 3 3 3.5-3.5L22 11"/><path d="M3 10v10h18V10"/><path d="M9 11v9M15 11v9"/>',
    "Apartment": '<path d="M5 21V3h14v18"/><path d="M3 21h18"/><path d="M8.5 7h2M13.5 7h2M8.5 11h2M13.5 11h2M8.5 15h2M13.5 15h2"/>',
}
UP, DOWN = '<path d="M12 19V5M6 11l6-6 6 6"/>', '<path d="M12 5v14M6 13l6 6 6-6"/>'
money = lambda v: f"${v:,.0f}"
def change(pct, what="vs last year"):
    if abs(pct) < 0.05:
        return f'<span class="chg">No change {what}</span>'
    arrow = SVG(UP if pct > 0 else DOWN, "chg-ico")
    word = "up" if pct > 0 else "down"
    return f'<span class="chg">{arrow}<span><span class="vh">{word} </span>{abs(pct):.1f}% {what}</span></span>'

def mk_summary(m):
    s = ("More homes are for sale than a year ago" if m["activeListings"]["yoy"] > 0 else "Fewer homes are for sale than a year ago")
    d = m["daysOnMarket"]
    s += " and they’re taking longer to sell" if d["value"] > d["lastYear"] else (" and they’re selling faster" if d["value"] < d["lastYear"] else "")
    s += ". "
    sold = m["sales"]["yoy"]
    s += "Sales were about the same as a year ago. " if abs(sold) < 1 else f"Sales were {'up' if sold > 0 else 'down'} {abs(sold):.1f}% from a year ago. "
    p = m["benchmarkPrice"]["yoy"]
    s += "Typical prices are close to where they were last year. " if abs(p) < 1 else f"Typical prices are {'up' if p > 0 else 'down'} {abs(p):.1f}% from last year. "
    moi = m["monthsOfInventory"]; dm = moi["value"] - moi["lastYear"]
    if abs(dm) >= 0.2:
        s += "Buyers have more choice and more room to negotiate." if dm > 0 else "Well-priced homes are moving quickly."
    return s.strip()

def market_page(st):
    m = st["market"]; short = st["compareLabel"].split()[0][:3] + ". " + st["compareLabel"].split()[1]
    kpis = [
        ("sales", "Homes sold", f'{m["sales"]["value"]:,}', change(m["sales"]["yoy"])),
        ("averagePrice", "Average sale price", money(m["averagePrice"]["value"]), change(m["averagePrice"]["yoy"])),
        ("benchmarkPrice", "Typical home price", money(m["benchmarkPrice"]["value"]), change(m["benchmarkPrice"]["yoy"])),
        ("activeListings", "Homes for sale", f'{m["activeListings"]["value"]:,}', change(m["activeListings"]["yoy"])),
    ]
    tiles = "\n".join(f'''      <div class="kpi"><dt>{SVG(MK_ICONS[k])}{label}</dt><dd class="kpi-val">{val}</dd><dd>{chg}</dd></div>''' for k, label, val, chg in kpis)

    # Market balance meter: months of inventory on a 0-8 scale (rule of thumb: under 4 sellers', 4-6 balanced, over 6 buyers')
    moi = m["monthsOfInventory"]; pos = lambda v: min(max(v, 0), 8) / 8 * 100
    side = "a balanced market" if 4 <= moi["value"] <= 6 else ("a sellers’ market" if moi["value"] < 4 else "a buyers’ market")
    meter = f'''<div class="meter" role="img" aria-label="{moi['value']:.1f} months of inventory, {side}. A year ago it was {moi['lastYear']:.1f} months.">
          <div class="meter-track"><span class="zone z1"></span><span class="zone z2"></span><span class="zone z3"></span>
            <span class="meter-last" style="left:{pos(moi['lastYear']):.1f}%" title="{st['compareLabel']}: {moi['lastYear']:.1f} months"></span>
            <span class="meter-now" style="left:{pos(moi['value']):.1f}%" title="{st['label']}: {moi['value']:.1f} months"></span></div>
          <div class="meter-zones" aria-hidden="true"><span>Sellers’ market</span><span>Balanced</span><span>Buyers’ market</span></div>
          <div class="meter-axis" aria-hidden="true"><span style="left:0">0</span><span style="left:50%">4</span><span style="left:75%">6</span><span style="left:100%">8+ months</span></div>
        </div>'''

    types = st["benchmarkByType"]; top = max(t["value"] for t in types)
    bars = "\n".join(f'''          <li><div class="tbar-head"><span class="tbar-name">{SVG(MK_ICONS[t['type']])}{t['type']}</span><span class="tbar-val">{money(t['value'])}</span></div>
            <div class="tbar" title="{t['type']}: {money(t['value'])}, {('up' if t['yoy'] > 0 else 'down')} {abs(t['yoy']):.1f}% from a year ago"><span style="width:{t['value'] / top * 100:.1f}%"></span></div>
            {change(t['yoy'])}</li>''' for t in types)

    def pair(key, label, unit_now, unit_last, now, last, lo_is_fast=True):
        mx = max(now, last)
        return f'''<div class="pace"><p class="pace-label">{SVG(MK_ICONS[key])}{label}</p>
            <div class="pace-row"><span class="pace-year">{st['label'].split()[0][:3]}. {st['label'].split()[1]}</span><span class="pace-bar now" style="width:{now / mx * 100:.0f}%" title="{st['label']}: {unit_now}"></span><b>{unit_now}</b></div>
            <div class="pace-row"><span class="pace-year">{short}</span><span class="pace-bar last" style="width:{last / mx * 100:.0f}%" title="{st['compareLabel']}: {unit_last}"></span><span>{unit_last}</span></div></div>'''
    dom = m["daysOnMarket"]; stl = m["saleToListRatio"]
    pace = pair("daysOnMarket", "Typical days to sell", f'{dom["value"]} days', f'{dom["lastYear"]} days', dom["value"], dom["lastYear"]) + "\n" + \
           pair("saleToListRatio", "Sold for, compared with the asking price", f'{stl["value"]:.1f}%', f'{stl["lastYear"]:.1f}%', stl["value"], stl["lastYear"])

    rows = [("Homes sold", f'{m["sales"]["value"]:,}', f'{m["sales"]["yoy"]:+.1f}%'),
            ("Average price", money(m["averagePrice"]["value"]), f'{m["averagePrice"]["yoy"]:+.1f}%'),
            ("Median price", money(m["medianPrice"]["value"]), f'{m["medianPrice"]["yoy"]:+.1f}%'),
            ("Benchmark price (MLS® HPI)", money(m["benchmarkPrice"]["value"]), f'{m["benchmarkPrice"]["yoy"]:+.1f}%'),
            ("New listings", f'{m["newListings"]["value"]:,}', f'{m["newListings"]["yoy"]:+.1f}%'),
            ("Homes for sale", f'{m["activeListings"]["value"]:,}', f'{m["activeListings"]["yoy"]:+.1f}%'),
            ("Months of inventory", f'{moi["value"]:.1f}', f'{moi["lastYear"]:.1f} last year'),
            ("Median days on market", str(dom["value"]), f'{dom["lastYear"]} last year'),
            ("Sale-to-list price", f'{stl["value"]:.1f}%', f'{stl["lastYear"]:.1f}% last year')]
    table = "\n".join(f"            <tr><td>{a}</td><td>{b}</td><td>{c.replace('-', '−')}</td></tr>" for a, b, c in rows)

    return f'''
<main id="main" class="wrap">
  <section class="page-head">
    <h1>Ottawa market, {st['label']}</h1>
    <p class="lede mk-summary">{mk_summary(m)}</p>
  </section>

  <section class="mk-section" aria-label="Key numbers">
    <dl class="kpis">
{tiles}
    </dl>
  </section>

  <section class="mk-grid">
    <div class="mk-card">
      <h2 class="h3">Who has the upper hand?</h2>
      <p class="mk-big">{moi['value']:.1f} <span>months of homes for sale</span></p>
      <p class="fine">How long it would take to sell every home on the market at this month’s pace. It was {moi['lastYear']:.1f} a year ago, so Ottawa is now {side}.</p>
      {meter}
      <p class="meter-key"><span class="key-now"></span>{st['label']} <span class="key-last"></span>{st['compareLabel']}</p>
    </div>
    <div class="mk-card">
      <h2 class="h3">Typical price by home type</h2>
      <ul class="tbars">
{bars}
      </ul>
      <p class="fine">The MLS® Home Price Index “benchmark” tracks a typical home, so it moves less than the average price when the mix of sales changes.</p>
      <p class="mk-link"><a class="link" href="calculators.html#payment">What would this cost you? Try the mortgage calculator →</a></p>
    </div>
    <div class="mk-card mk-wide">
      <h2 class="h3">How fast homes are selling</h2>
      <div class="paces">
{pace}
      </div>
    </div>
  </section>

  <details class="more-stats mk-table">
    <summary>See all the numbers</summary>
    <div class="table-wrap"><table class="stats">
      <thead><tr><th scope="col">Citywide</th><th scope="col">{st['label']}</th><th scope="col">vs a year ago</th></tr></thead>
      <tbody>
{table}
      </tbody>
    </table></div>
  </details>
  <p class="source">Source: <a href="{st['sourceUrl']}" target="_blank" rel="noopener">{st['source']} monthly market update, {st['label']}</a>. Updated monthly.</p>

  <section class="section neighbourhoods" id="neighbourhoods" aria-labelledby="nb-h">
    <h2 id="nb-h">Neighbourhoods</h2>
    <p class="fine">Areas we work in across Ottawa. Tap one to learn more, or ask about one that isn’t listed.</p>
    <div class="areas">
{area_cards()}
    </div>
  </section>

  <section class="section alerts" id="alerts" aria-labelledby="al-h">
    <div class="alerts-copy">
      <h2 id="al-h">Get the stats for your street</h2>
      <p>Tell us your neighbourhood and we’ll email you when homes sell nearby: what they sold for and how fast. About once a month, and you can stop any time.</p>
      <p class="fine">Want a one-time look at your home instead? <a href="home-value.html">See what it’s worth</a> or <a href="contact.html">let’s talk</a>.</p>
    </div>
    <form class="alerts-form" id="alerts-form" data-form="alerts" novalidate>
      <div class="field-row">
        <div class="field">
          <label for="al-name">Name</label>
          <input id="al-name" name="name" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="al-email">Email</label>
          <input id="al-email" name="email" type="email" autocomplete="email" required>
        </div>
      </div>
      <div class="field">
          <label for="al-area">Neighbourhood</label>
          <input id="al-area" name="neighbourhood" list="al-areas" autocomplete="off" required placeholder="e.g. Kanata">
          <datalist id="al-areas">{''.join(f'<option value="{n}"></option>' for _, n, *_ in AREAS)}</datalist>
      </div>
      <label class="check consent"><input id="al-consent" name="consent" type="checkbox" value="yes" required> <span>Yes, email me neighbourhood sales updates from Mohamed Dahrouj, Right at Home Realty, Brokerage. I can unsubscribe any time.</span></label>
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn" type="submit">Send me updates</button>
      <p class="form-privacy">We’ll only use your email for these updates. <a href="privacy.html">Privacy</a></p>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </section>
</main>
'''

MARKET = market_page(ST)

# Home page snapshot uses the same numbers
_m = ST["market"]
_snap = {"label": ST["label"], "averagePrice": money(_m["averagePrice"]["value"]),
         "averagePriceChange": f'{_m["averagePrice"]["yoy"]:+.1f}% from a year ago'.replace("-", "−"),
         "sales": f'{_m["sales"]["value"]:,}', "salesChange": f'{_m["sales"]["yoy"]:+.1f}% from a year ago'.replace("-", "−"),
         "moi": f'{_m["monthsOfInventory"]["value"]:.1f}', "moiChange": f'{_m["monthsOfInventory"]["lastYear"]:.1f} a year ago'}
for _k, _v in _snap.items():
    HOME = re.sub(rf'(data-stat="{_k}">)[^<]*(<)', lambda mm: mm.group(1) + _v + mm.group(2), HOME)
MOVING = MOVING.replace("{CTA}", CTA).replace("{SEARCH_MOVE}", SEARCH_CTA("search"))
COTTAGES = COTTAGES.replace("{CTA}", CTA).replace("{SEARCH_COTTAGE}", SEARCH_CTA("cottage"))

PRIVACY = """
<main id="main" class="wrap">
  <section class="page-head">
    <h1>Privacy</h1>
    <p class="lede">What we collect on this site, why, and what you can ask us to do with it.</p>
    <p class="fine updated">Last updated October 2026</p>
  </section>
  <section class="section prose">
    <h2>Who we are</h2>
    <p>This site is run by Mohamed Dahrouj, Sales Representative with Right at Home Realty, Brokerage, 14 Chamberlain Ave, Suite 101, Ottawa, ON K1S 1V9. Questions or requests about your information go to <a href="mailto:mohamed@dahrouj.com">mohamed@dahrouj.com</a> or 613-869-5923.</p>

    <h2>What we collect</h2>
    <p>Only what you choose to send us through a form or by email, phone or text: usually your name, phone number or email, and, for a home value, the property address and any notes you add. If you become a client, we also collect what a real estate deal needs, such as the identity verification that federal anti-money-laundering rules (FINTRAC) require.</p>
    <p>This site doesn’t use cookies, analytics, tracking pixels or ads.</p>

    <h2>How we use it</h2>
    <ul>
      <li>To reply to you and set up a time to talk</li>
      <li>To prepare the home value or home search you asked for</li>
      <li>To provide real estate services if you hire us, and to keep the records the law requires</li>
    </ul>
    <p>We don’t sell or rent your information, and we won’t add you to a mailing list unless you ask to be added. If you sign up for neighbourhood sales updates, we email you about once a month, and every email lets you unsubscribe; you can also just reply “stop”.</p>

    <h2>Who else handles it</h2>
    <p>A few services help run this site. They only get what they need to do their job, and some of them store or process information outside Canada, including in the United States and Europe.</p>
    <ul>
      <li><strong>Web3Forms</strong> delivers form messages to our email</li>
      <li><strong>Geoapify</strong> suggests addresses as you type on the home value form, so what you type in the address box is sent to it</li>
      <li><strong>GitHub Pages</strong> hosts the site and, like any web host, keeps basic server logs such as IP addresses</li>
      <li><strong>Right at Home Realty, Brokerage</strong> keeps client and transaction records as Ontario’s real estate law requires</li>
    </ul>
    <p>We may also share information when the law requires it, or with others involved in your deal (such as your lawyer or lender) when you ask us to.</p>

    <h2>How long we keep it</h2>
    <p>We keep enquiries only as long as we need them to help you. Client and transaction records are kept for as long as real estate and anti-money-laundering laws require, then deleted.</p>

    <h2>Your choices</h2>
    <p>You can ask to see the information we have about you, correct it, or have us delete it where the law allows. You can also withdraw your consent at any time. Just email or call us. If you’re not satisfied with our answer, you can contact the <a href="https://www.priv.gc.ca/" target="_blank" rel="noopener">Office of the Privacy Commissioner of Canada</a>.</p>
  </section>
</main>
"""

# Link preview images (1200x630), made from assets/img/share; see README
SHARE = {
    "index.html": ("home.jpg", "Rideau Canal in downtown Ottawa with the words: Your next move in Ottawa, handled personally"),
    "home-value.html": ("home-value.jpg", "Parliament Hill with the words: What's your Ottawa home worth?"),
    "moving-to-ottawa.html": ("moving.jpg", "Parliament Hill in autumn with the words: Moving to Ottawa"),
    "contact.html": ("contact.jpg", "Rideau Canal with the words: Let’s talk about your move"),
    "market.html": ("market.jpg", "Bar chart graphic with the words: Ottawa real estate market"),
    "calculators.html": ("calculators.jpg", "Calculator icons with the words: Home buying calculators"),
    "cottages.html": ("cottages.jpg", "Outlines of four lakes near Ottawa with the words: Buying a cottage near Ottawa"),
    "fairfee.html": ("fairfee.jpg", "FairFee wordmark with the words: Your home. You call the shots."),
}

pages = {
    "index.html": head("Ottawa Real Estate, Handled Personally", DESC_SITE, LD) + header("home") + HOME,
    "market.html": head("Ottawa Real Estate Market: Monthly Stats & Neighbourhoods", "Monthly Ottawa real estate numbers from the Ottawa Real Estate Board, plus guides to Kanata, Stittsville, Barrhaven, Findlay Creek, Riverside South, Orléans, Manotick, Westboro and the Glebe.") + header("market") + MARKET,
    "calculators.html": head("Home Buying Calculators | Ottawa Real Estate", "Ontario land transfer tax, mortgage payment (with CMHC insurance) and affordability calculators for Ottawa home buyers.") + header("calculators") + CALCULATORS,
    "moving-to-ottawa.html": head("Moving to Ottawa: Relocation, Newcomers & Military Postings", "Relocating to Ottawa, new to Canada, or posted to Ottawa with the Canadian Armed Forces? Get a neighbourhood shortlist, video tours and help buying or renting from an Ottawa real estate agent.", faq_ld(MOVING_FAQ)) + header("moving") + MOVING,
    "cottages.html": head("Buying a Cottage Near Ottawa | Rideau Lakes, Calabogie, Lanark", "Buy a cottage near Ottawa in the Rideau Lakes, Lanark County, Calabogie or the Ottawa Valley, with wells, septic, road access and shoreline checked before you buy.", faq_ld(COTTAGE_FAQ)) + header("cottages") + COTTAGES,
    "home-value.html": head("What’s My Home Worth? Free Ottawa Home Valuation", "Get a free, no-obligation value for your Ottawa home based on recent sales nearby. Just send your address.") + header("home-value") + HOMEVALUE,
    "contact.html": head("Contact | Ottawa Real Estate", "Talk to us about selling, buying or leasing a home in Ottawa. Our office is in the Glebe.") + header("contact") + CONTACT,
    "privacy.html": head("Privacy | dahrouj.com", "How dahrouj.com collects, uses and protects the information you send us.") + header("privacy") + PRIVACY,
    "fairfee.html": head("Our Fees | Proud FairFee™ Agent", "A proud FairFee™ agent in Ottawa: a lower listing fee with full service, in writing before you hire us. Your home, you call the shots.") + header("fairfee") + FAIRFEE,
}
geo = json.loads((ROOT / "assets/img/office-map.json").read_text()) if (ROOT / "assets/img/office-map.json").exists() else {"lat": 45.4047, "lon": -75.69}
svg_map = (ROOT / "assets/img/office-map.svg").read_text()
for name, html in pages.items():
    url = "https://www.dahrouj.com/" + ("" if name == "index.html" else name)
    img, alt = SHARE.get(name, SHARE["index.html"])
    og = (f'  <meta property="og:image" content="https://www.dahrouj.com/assets/img/share/{img}">\n'
          f'  <meta property="og:image:type" content="image/jpeg">\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n'
          f'  <meta property="og:image:alt" content="{alt}">\n  <meta property="og:site_name" content="dahrouj.com">\n  <meta property="og:locale" content="en_CA">\n'
          f'  <meta name="twitter:card" content="summary_large_image">')
    html = html.replace('  <meta property="og:image" content="https://www.dahrouj.com/assets/img/hero-canal-1400.webp">', og, 1)
    html = html.replace('  <meta property="og:type" content="website">', f'  <link rel="canonical" href="{url}">\n  <meta property="og:url" content="{url}">\n  <meta property="og:type" content="website">', 1)
    foot = re.sub(r'<nav class="callbar".*?</nav>\n', "", FOOTER, flags=re.S) if name in ("contact.html", "home-value.html") else FOOTER
    html = (html + foot).replace("OFFICE_MAP_SVG", svg_map).replace("OFFICE_LAT", f"{geo['lat']:.5f}").replace("OFFICE_LON", f"{geo['lon']:.5f}")
    (ROOT / name).write_text(html)
    print("wrote", name)

import datetime
today = datetime.date.today().isoformat()
urls = "".join(f"  <url><loc>https://www.dahrouj.com/{'' if n == 'index.html' else n}</loc><lastmod>{today}</lastmod></url>\n" for n in pages)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
(ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: https://www.dahrouj.com/sitemap.xml\n")
