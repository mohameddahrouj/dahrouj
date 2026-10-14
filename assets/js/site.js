// dahrouj.com: menu, calculators, market stats and forms. No dependencies.

// Web3Forms access key: get one free at https://web3forms.com (enter mohamed@dahrouj.com).
// It's safe to publish; it only lets this site send mail to that inbox.
const WEB3FORMS_KEY = "64bab466-4d07-4e12-bad6-cacfa73f4a39";

const $ = (sel) => document.querySelector(sel);
const money = (n) => n.toLocaleString("en-CA", { style: "currency", currency: "CAD", maximumFractionDigits: 0 });
const count = (n) => n.toLocaleString("en-CA");
const pct = (n, digits = 1) => `${n > 0 ? "+" : n < 0 ? "−" : ""}${Math.abs(n).toFixed(digits)}%`;
const rate = (n) => `(${String(+n.toFixed(2))}%)`;

function loadJSON(name) {
  const inline = window.__SITE_DATA && window.__SITE_DATA[name];
  if (inline) return Promise.resolve(inline);
  return fetch(`data/${name}.json`, { cache: "no-cache" }).then((r) => {
    if (!r.ok) throw new Error(`${name}.json: ${r.status}`);
    return r.json();
  });
}

/* ---------- Fee calculator ---------- */
function initFees(fees) {
  const price = $("#price");
  const out = $("#price-out");
  const tabs = [$("#tab-sell"), $("#tab-buy")];
  const panels = { "tab-sell": $("#panel-sell"), "tab-buy": $("#panel-buy") };
  const s = fees.selling;
  const b = fees.buying;
  const hst = fees.hstRate;

  $("#sell-rate").textContent = rate(s.listingRate);
  $("#coop-rate").textContent = rate(s.buyerAgentRate);
  $("#buy-rate").textContent = rate(b.assumedBuyerAgentRate);
  $("#sell-note").textContent = s.note;
  $("#buy-note").textContent = b.note;

  function bump(el, text) {
    if (el.textContent === text) return;
    el.textContent = text;
    el.classList.remove("bump");
    void el.offsetWidth;
    el.classList.add("bump");
  }

  function render() {
    const p = Number(price.value);
    out.textContent = money(p);
    const mine = p * s.listingRate / 100;
    const coop = p * s.buyerAgentRate / 100;
    const tax = (mine + coop) * hst;
    const total = mine + coop + tax;
    $("#sell-fee").textContent = money(mine);
    $("#coop-fee").textContent = money(coop);
    $("#sell-hst").textContent = money(tax);
    $("#sell-total").textContent = money(total);
    bump($("#sell-keep"), money(p - total));

    const comm = p * b.assumedBuyerAgentRate / 100;
    const rebate = (p / b.rebateStep) * b.rebatePer;
    $("#buy-comm").textContent = money(comm);
    bump($("#buy-rebate"), money(rebate));
  }

  function select(tab) {
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute("aria-selected", on);
      t.tabIndex = on ? 0 : -1;
      panels[t.id].hidden = !on;
    });
  }
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => select(t));
    t.addEventListener("keydown", (e) => {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      const next = tabs[(i + 1) % tabs.length];
      select(next);
      next.focus();
    });
  });
  if (location.hash === "#buying") select(tabs[1]);
  price.addEventListener("input", render);
  render();
}


/* ---------- Footer legal text ---------- */
function initLegal() {
  const btn = $(".legal-btn"), box = $("#legal-text");
  if (!btn || !box) return;
  btn.addEventListener("click", () => {
    const open = btn.getAttribute("aria-expanded") !== "true";
    btn.setAttribute("aria-expanded", open);
    box.classList.toggle("open", open);
  });
}

/* ---------- Call / Text buttons (phones) ---------- */
function initCallbar() {
  const bar = $(".callbar");
  if (!bar) return;
  const top = $(".hero") || $(".ff-hero") || $(".page-head");
  let typing = false, ticking = false;
  const update = () => {
    ticking = false;
    const pastTop = top ? top.getBoundingClientRect().bottom < 80 : scrollY > 300;
    bar.classList.toggle("is-hidden", !pastTop || typing);
  };
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  bar.classList.add("is-hidden");
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", onScroll, { passive: true });
  document.addEventListener("focusin", (e) => { if (e.target.matches("input, textarea, select")) { typing = true; update(); } });
  document.addEventListener("focusout", () => { typing = false; setTimeout(update, 100); });
  update();
}

/* ---------- Menu ---------- */
function initMenu() {
  const btn = $(".menu-btn");
  const header = $(".top");
  if (!btn) return;
  document.documentElement.classList.add("js");
  btn.addEventListener("click", () => {
    const open = btn.getAttribute("aria-expanded") !== "true";
    btn.setAttribute("aria-expanded", open);
    header.classList.toggle("open", open);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && header.classList.contains("open")) { btn.click(); btn.focus(); }
  });
}

/* ---------- Buying calculators (Ontario rules) ---------- */
const val = (id) => { const n = parseFloat($(id).value); return Number.isFinite(n) && n > 0 ? n : 0; };
const money2 = (n) => n.toLocaleString("en-CA", { style: "currency", currency: "CAD", minimumFractionDigits: 2, maximumFractionDigits: 2 });

function ontarioLTT(price) {
  const brackets = [[55000, 0.005], [250000, 0.01], [400000, 0.015], [2000000, 0.02], [Infinity, 0.025]];
  let tax = 0, lower = 0;
  for (const [upper, r] of brackets) {
    if (price > lower) tax += (Math.min(price, upper) - lower) * r;
    lower = upper;
  }
  return tax;
}

function minDown(price) {
  if (price >= 1500000) return price * 0.2;
  if (price <= 500000) return price * 0.05;
  return 25000 + (price - 500000) * 0.1;
}

function cmhcRate(price, down, thirty) {
  if (price >= 1500000) return null;
  const ltv = (price - down) / price;
  let r;
  if (ltv <= 0.8) return 0;
  else if (ltv <= 0.85) r = 0.028;
  else if (ltv <= 0.9) r = 0.031;
  else if (ltv <= 0.95) r = 0.04;
  else return null;
  return r + (thirty ? 0.002 : 0);
}

// Canadian fixed-rate mortgages compound semi-annually.
function periodicRate(annualPct, perYear) {
  return Math.pow(1 + annualPct / 100 / 2, 2 / perYear) - 1;
}
function payment(principal, annualPct, years, perYear) {
  const i = periodicRate(annualPct, perYear), n = years * perYear;
  return i === 0 ? principal / n : (principal * i) / (1 - Math.pow(1 + i, -n));
}
function principalFor(pmt, annualPct, years, perYear) {
  const i = periodicRate(annualPct, perYear), n = years * perYear;
  return i === 0 ? pmt * n : (pmt * (1 - Math.pow(1 + i, -n))) / i;
}

const calcs = {
  ltt() {
    const price = val("#ltt-price");
    const tax = ontarioLTT(price);
    const refund = $("#ltt-ftb").checked ? Math.min(tax, 4000) : 0;
    $("#ltt-tax").textContent = money2(tax);
    $("#ltt-refund").textContent = refund ? `−${money2(refund)}` : "None";
    $("#ltt-total").textContent = money2(tax - refund);
  },
  payment() {
    const price = val("#pay-price"), down = val("#pay-down"), rate = val("#pay-rate");
    const years = Number($("#pay-amort").value), freq = $("#pay-freq").value;
    const msg = $("#pay-msg");
    const base = Math.max(price - down, 0);
    let prem = 0, note = "Uses semi-annual compounding, as Canadian fixed-rate mortgages do.";
    if (down < minDown(price)) {
      note = `The minimum down payment on this price is ${money(minDown(price))}.`;
    } else if (down < price * 0.2) {
      const r = cmhcRate(price, down, years === 30);
      prem = r ? base * r : 0;
      if (years > 25 && r) note = "30-year insured mortgages are for first-time buyers and new builds.";
    }
    const loan = base + prem;
    const monthly = payment(loan, rate, years, 12);
    let label = "Monthly payment", amt = monthly;
    if (freq === "biweekly") { label = "Payment every two weeks"; amt = payment(loan, rate, years, 26); }
    if (freq === "weekly") { label = "Weekly payment"; amt = payment(loan, rate, years, 52); }
    if (freq === "accel") { label = "Accelerated payment every two weeks"; amt = monthly / 2; }
    $("#pay-loan").textContent = money(loan);
    $("#pay-prem").textContent = prem ? money(prem) : "None";
    $("#pay-label").textContent = label;
    $("#pay-amount").textContent = money2(amt);
    msg.textContent = note;
  },
  afford() {
    const income = val("#aff-income") / 12, down = val("#aff-down"), debts = val("#aff-debts");
    const rate = val("#aff-rate"), tax = val("#aff-tax"), heat = val("#aff-heat"), condo = val("#aff-condo");
    const q = Math.max(rate + 2, 5.25);
    const housing = tax + heat + condo / 2;
    const maxPmt = Math.max(0, Math.min(income * 0.39 - housing, income * 0.44 - housing - debts));
    const maxLoan = principalFor(maxPmt, q, 25, 12);
    // Largest price where the down payment meets the minimum and the loan (with any insurance) fits.
    let lo = 0, hi = 5000000;
    for (let k = 0; k < 60; k++) {
      const p = (lo + hi) / 2;
      let ok = down >= minDown(p);
      if (ok) {
        const r = down < p * 0.2 ? cmhcRate(p, down, false) : 0;
        ok = r !== null && (p - down) * (1 + (r || 0)) <= maxLoan;
      }
      if (ok) lo = p; else hi = p;
    }
    const price = Math.floor(lo / 1000) * 1000;
    $("#aff-qrate").textContent = `${q.toFixed(2)}%`;
    $("#aff-loan").textContent = money(Math.floor(maxLoan / 1000) * 1000);
    $("#aff-price").textContent = price > 0 ? money(price) : "Add your income and savings";
  },
  cmhc() {
    const price = val("#cmhc-price"), down = val("#cmhc-down"), thirty = $("#cmhc-30").checked;
    const msg = $("#cmhc-msg");
    const share = price ? (down / price) * 100 : 0;
    $("#cmhc-pct").textContent = `${share.toFixed(2)}%`;
    const reset = (text) => {
      $("#cmhc-rate").textContent = "None"; $("#cmhc-prem").textContent = "None"; $("#cmhc-pst").textContent = "None";
      msg.textContent = text;
    };
    const base = "Premiums: 2.80% with 15–19.99% down, 3.10% with 10–14.99% down, 4.00% with 5–9.99% down, plus 0.20% for a 30-year amortization. Homes priced at $1.5 million or more can’t be insured.";
    if (!price) return reset(base);
    if (down >= price * 0.2) return reset("With 20% or more down, you don’t need mortgage insurance.");
    if (price >= 1500000) return reset("Homes priced at $1.5 million or more can’t be insured, so you’ll need 20% down.");
    if (down < minDown(price)) return reset(`The minimum down payment on this price is ${money(minDown(price))}.`);
    const r = cmhcRate(price, down, thirty);
    const prem = (price - down) * r;
    $("#cmhc-rate").textContent = `${(r * 100).toFixed(2)}%`;
    $("#cmhc-prem").textContent = money2(prem);
    $("#cmhc-pst").textContent = money2(prem * 0.08);
    msg.textContent = base;
  },
};

function initCalculators() {
  document.querySelectorAll("form[data-calc]").forEach((form) => {
    const run = calcs[form.dataset.calc];
    form.addEventListener("input", run);
    form.addEventListener("change", run);
    form.addEventListener("submit", (e) => e.preventDefault());
    run();
  });
}


/* ---------- Market stats ---------- */
function summarize(m) {
  const parts = [];
  const more = m.activeListings.yoy > 0;
  parts.push(more ? "More homes are for sale than a year ago" : "Fewer homes are for sale than a year ago");
  if (m.daysOnMarket.value > m.daysOnMarket.lastYear) parts.push("and they’re taking longer to sell");
  else if (m.daysOnMarket.value < m.daysOnMarket.lastYear) parts.push("and they’re selling faster");
  let s = parts.join(" ") + ". ";
  const sold = m.sales.yoy;
  s += Math.abs(sold) < 1
    ? "Sales were about the same as a year ago. "
    : `Sales were ${sold > 0 ? "up" : "down"} ${Math.abs(sold).toFixed(1)}% from a year ago. `;
  const p = m.benchmarkPrice.yoy;
  s += Math.abs(p) < 1
    ? "Benchmark prices are close to where they were last year, "
    : `Benchmark prices are ${p > 0 ? "up" : "down"} ${Math.abs(p).toFixed(1)}% from last year, `;
  s += `and homes sold for ${m.saleToListRatio.value.toFixed(1)}% of their asking price on average. `;
  const moi = m.monthsOfInventory, d = moi.value - moi.lastYear;
  if (Math.abs(d) >= 0.2) {
    s += d > 0
      ? `With ${moi.value.toFixed(1)} months of inventory, up from ${moi.lastYear.toFixed(1)}, buyers have more choice and more room to negotiate.`
      : `With ${moi.value.toFixed(1)} months of inventory, down from ${moi.lastYear.toFixed(1)}, well-priced homes are moving quickly.`;
  }
  return s.trim();
}

function initSnapshot(st) {
  const m = st.market;
  const set = (k, v) => document.querySelectorAll(`[data-stat="${k}"]`).forEach((el) => { el.textContent = v; });
  set("label", st.label);
  set("averagePrice", money(m.averagePrice.value));
  set("averagePriceChange", `${pct(m.averagePrice.yoy)} from a year ago`);
  set("sales", count(m.sales.value));
  set("salesChange", `${pct(m.sales.yoy)} from a year ago`);
  set("moi", m.monthsOfInventory.value.toFixed(1));
  set("moiChange", `${m.monthsOfInventory.lastYear.toFixed(1)} a year ago`);
}

const TYPE_ICONS = {
  "Single family": '<svg class="type-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11 12 4l9 7"/><path d="M5 9.5V20h14V9.5"/><path d="M10 20v-5h4v5"/></svg>',
  "Townhouse": '<svg class="type-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M2 11l3.5-3.5L9 11l3-3 3 3 3.5-3.5L22 11"/><path d="M3 10v10h18V10"/><path d="M9 11v9M15 11v9"/></svg>',
  "Apartment": '<svg class="type-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 21V3h14v18"/><path d="M3 21h18"/><path d="M8.5 7h2M13.5 7h2M8.5 11h2M13.5 11h2M8.5 15h2M13.5 15h2"/></svg>',
};

const STAT_ICONS = {
  "Homes sold": '<svg class="type-ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="8" cy="15.5" r="4.5"/><path d="M11.2 12.3 20 3.5"/><path d="M17 6.5l3 3"/><path d="M14.6 8.9l2 2"/></svg>',
  "Average price": '<svg class="type-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12V4h8l9.5 9.5-8 8z"/><circle cx="7.5" cy="8" r="1.4"/></svg>',
  "Benchmark price (MLS® HPI)": '<svg class="type-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 20h18"/><path d="M4 16l5-5 4 3 7-8"/><path d="M15 6h5v5"/></svg>',
  "Homes for sale": '<svg class="type-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 21V3"/><path d="M5 6h14v8H5"/><path d="M9 6v-2M15 6v-2"/></svg>',
  "Months of inventory": '<svg class="type-ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17"/><path d="M8 3v4M16 3v4"/><path d="M8 14h3M8 17h6"/></svg>',
};

function initStats(st) {
  const m = st.market;
  const short = (label) => label.replace(/^(\w{3})\w*/, "$1.");
  $("#mk-month").textContent = st.label;
  $("#mk-summary").textContent = summarize(m);
  $("#mk-col-now").textContent = short(st.label);

  const rows = [
    ["Homes sold", count(m.sales.value), pct(m.sales.yoy)],
    ["Average price", money(m.averagePrice.value), pct(m.averagePrice.yoy)],
    ["Median price", money(m.medianPrice.value), pct(m.medianPrice.yoy)],
    ["Benchmark price (MLS® HPI)", money(m.benchmarkPrice.value), pct(m.benchmarkPrice.yoy)],
    ["New listings", count(m.newListings.value), pct(m.newListings.yoy)],
    ["Homes for sale", count(m.activeListings.value), pct(m.activeListings.yoy)],
    ["Months of inventory", m.monthsOfInventory.value.toFixed(1), `${m.monthsOfInventory.lastYear.toFixed(1)} last year`],
    ["Median days on market", String(m.daysOnMarket.value), `${m.daysOnMarket.lastYear} last year`],
    ["Sale-to-list price", `${m.saleToListRatio.value.toFixed(1)}%`, `${m.saleToListRatio.lastYear.toFixed(1)}% last year`],
  ];
  const makeRow = ([label, now, then]) => {
    const tr = document.createElement("tr");
    [label, now, then].forEach((t) => tr.append(Object.assign(document.createElement("td"), { textContent: t })));
    if (STAT_ICONS[label]) {
      const name = document.createElement("span");
      name.className = "stat-name";
      name.innerHTML = STAT_ICONS[label] + "<span></span>";
      name.lastChild.textContent = label;
      tr.firstChild.replaceChildren(name);
    }
    return tr;
  };
  const MAIN = ["Homes sold", "Average price", "Benchmark price (MLS® HPI)", "Homes for sale", "Months of inventory"];
  $("#mk-rows").replaceChildren(...rows.filter((r) => MAIN.includes(r[0])).map(makeRow));
  if ($("#mk-more")) $("#mk-more").replaceChildren(...rows.filter((r) => !MAIN.includes(r[0])).map(makeRow));

  const max = Math.max(...st.benchmarkByType.map((t) => t.value));
  $("#mk-types").replaceChildren(...st.benchmarkByType.map((t) => {
    const li = document.createElement("li");
    li.innerHTML = `<div class="bar-head"><span></span><span></span></div>
      <div class="bar-track" aria-hidden="true"><div class="bar-fill"></div></div>
      <span class="bar-change"></span>`;
    const [name, val] = li.querySelectorAll(".bar-head span");
    name.innerHTML = (TYPE_ICONS[t.type] || "") + `<span class="type-name"></span>`;
    name.querySelector(".type-name").textContent = t.type;
    val.textContent = money(t.value);
    li.querySelector(".bar-fill").style.width = `${(t.value / max) * 100}%`;
    li.querySelector(".bar-change").textContent = `${pct(t.yoy)} vs a year ago`;
    return li;
  }));

  const src = $("#mk-source");
  const released = new Date(`${st.released}T12:00:00`).toLocaleDateString("en-CA", { month: "long", day: "numeric", year: "numeric" });
  const ytd = st.yearToDate
    ? `Year to date: ${count(st.yearToDate.sales.value)} homes sold (${pct(st.yearToDate.sales.yoy)}), average price ${money(st.yearToDate.averagePrice.value)}. `
    : "";
  src.textContent = `${ytd}Source: ${st.source}, released ${released}. `;
  const a = Object.assign(document.createElement("a"), { href: st.sourceUrl, textContent: "Full report (PDF)", target: "_blank", rel: "noopener" });
  src.append(a);
}


/* ---------- Address suggestions ----------
   Default: Geoapify (free key at myprojects.geoapify.com, 3,000 requests a day).
   Also supported: "google" (Places) and "canadapost" (AddressComplete).
   Restrict the key to dahrouj.com in the provider's console. With no key, the
   address box still works as a normal text field. */
const ADDRESS_LOOKUP = { provider: "geoapify", key: "b5100d4562804551be67884ccc099e21" };

const addressProviders = {
  geoapify: {
    async find(q, key) {
      const url = "https://api.geoapify.com/v1/geocode/autocomplete?" + new URLSearchParams({
        text: q, filter: "countrycode:ca", bias: "proximity:-75.75,45.35", limit: "6", lang: "en", format: "json", apiKey: key,
      });
      const data = await (await fetch(url)).json();
      return (data.results || [])
        .filter((r) => r.housenumber || r.result_type === "building" || r.result_type === "street")
        .map((r) => {
          // Build the label from address parts so business names (e.g. a shop at that address) are left out
          const street = r.housenumber && r.street ? `${r.housenumber} ${r.street}` : r.street;
          const place = [r.city || r.town || r.village || r.county, [r.state_code, r.postcode].filter(Boolean).join(" ")].filter(Boolean).join(", ");
          const label = street ? [street, place].filter(Boolean).join(", ") : r.formatted.replace(/, Canada$/, "");
          return { text: label, async pick() { return { label, postal: r.postcode || "", coords: `${r.lat},${r.lon}` }; } };
        })
        .filter((it, i, all) => all.findIndex((o) => o.text === it.text) === i);
    },
  },
  google: {
    _lib: null, _token: null,
    async load(key) {
      if (this._lib) return this._lib;
      if (!window.google?.maps?.importLibrary) {
        await new Promise((ok, fail) => {
          const sc = document.createElement("script");
          sc.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(key)}&loading=async&libraries=places&v=weekly`;
          sc.async = true; sc.onload = ok; sc.onerror = fail;
          document.head.append(sc);
        });
        while (!window.google?.maps?.importLibrary) await new Promise((r) => setTimeout(r, 50));
      }
      this._lib = await google.maps.importLibrary("places");
      return this._lib;
    },
    async find(q, key) {
      const { AutocompleteSuggestion, AutocompleteSessionToken } = await this.load(key);
      this._token = this._token || new AutocompleteSessionToken();
      const { suggestions } = await AutocompleteSuggestion.fetchAutocompleteSuggestions({
        input: q, includedRegionCodes: ["ca"], sessionToken: this._token,
        locationBias: { center: { lat: 45.35, lng: -75.75 }, radius: 50000 },
      });
      return suggestions.filter((sg) => sg.placePrediction).map((sg) => ({
        text: sg.placePrediction.text.toString(),
        async pick() {
          const place = sg.placePrediction.toPlace();
          await place.fetchFields({ fields: ["formattedAddress", "addressComponents", "location"] });
          addressProviders.google._token = null; // the session ends with a details lookup
          const pc = (place.addressComponents || []).find((c) => c.types.includes("postal_code"));
          return { label: place.formattedAddress, postal: pc ? pc.longText : "", coords: place.location ? `${place.location.lat()},${place.location.lng()}` : "" };
        },
      }));
    },
  },
  canadapost: {
    base: "https://ws1.postescanada-canadapost.ca/AddressComplete/Interactive",
    async find(q, key, lastId = "") {
      const url = `${this.base}/Find/v2.10/json3.ws?` + new URLSearchParams({
        Key: key, SearchTerm: q, LastId: lastId, Country: "CAN", LanguagePreference: "en", MaxSuggestions: "7",
      });
      const data = await (await fetch(url)).json();
      return (data.Items || []).filter((it) => !it.Error).map((it) => ({
        text: [it.Text, it.Description].filter(Boolean).join(", "),
        more: it.Next === "Find",
        id: it.Id,
        async pick() {
          if (it.Next === "Find") return { expand: await addressProviders.canadapost.find(q, key, it.Id) };
          const r = await (await fetch(`${addressProviders.canadapost.base}/Retrieve/v2.11/json3.ws?` + new URLSearchParams({ Key: key, Id: it.Id }))).json();
          const a = (r.Items || []).find((x) => x.Language === "ENG") || (r.Items || [])[0] || {};
          return { label: [a.Line1, a.City, a.ProvinceCode, a.PostalCode].filter(Boolean).join(", "), postal: a.PostalCode || "", coords: "" };
        },
      }));
    },
  },
};

function initAddress(input) {
  const provider = addressProviders[ADDRESS_LOOKUP.provider];
  if (!provider || !ADDRESS_LOOKUP.key) return; // plain text field until a key is added
  const list = document.getElementById(input.getAttribute("aria-controls"));
  const postal = $("#v-postal"), coords = $("#v-coords");
  let items = [], active = -1, timer = null, seq = 0;
  const close = () => { list.hidden = true; input.setAttribute("aria-expanded", "false"); input.removeAttribute("aria-activedescendant"); active = -1; };
  const highlight = (i) => {
    active = i;
    [...list.querySelectorAll('[role="option"]')].forEach((li, j) => li.setAttribute("aria-selected", j === i));
    if (i >= 0) input.setAttribute("aria-activedescendant", `addr-opt-${i}`);
  };
  const show = (found) => {
    items = found;
    list.replaceChildren(...items.map((it, i) => {
      const li = document.createElement("li");
      li.id = `addr-opt-${i}`; li.setAttribute("role", "option");
      li.textContent = it.text + (it.more ? " (choose a unit)" : "");
      li.addEventListener("mousedown", (ev) => { ev.preventDefault(); choose(i); });
      return li;
    }));
    if (items.length && ADDRESS_LOOKUP.provider === "geoapify") {
      const note = document.createElement("li");
      note.className = "addr-attrib"; note.setAttribute("role", "presentation");
      note.innerHTML = 'Powered by <a href="https://www.geoapify.com/" target="_blank" rel="noopener">Geoapify</a> · © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors';
      note.addEventListener("mousedown", (ev) => ev.preventDefault());
      list.append(note);
    }
    const open = items.length > 0 && document.activeElement === input;
    list.hidden = !open; input.setAttribute("aria-expanded", open);
    highlight(-1);
  };
  async function choose(i) {
    const it = items[i]; if (!it) return;
    try {
      const res = await it.pick();
      if (res.expand) return show(res.expand);
      input.value = res.label || it.text; postal.value = res.postal; coords.value = res.coords;
    } catch (e) { input.value = it.text; }
    close();
  }
  input.addEventListener("input", () => {
    postal.value = ""; coords.value = "";
    clearTimeout(timer);
    const q = input.value.trim();
    if (q.length < 3) return close();
    timer = setTimeout(async () => {
      const mine = ++seq;
      try { const found = await provider.find(q, ADDRESS_LOOKUP.key); if (mine === seq) show(found); }
      catch (e) { console.warn("Address lookup unavailable", e); close(); }
    }, 220);
  });
  input.addEventListener("keydown", (e) => {
    if (list.hidden) return;
    if (e.key === "ArrowDown") { e.preventDefault(); highlight(Math.min(active + 1, items.length - 1)); }
    else if (e.key === "ArrowUp") { e.preventDefault(); highlight(Math.max(active - 1, 0)); }
    else if (e.key === "Enter" && active >= 0) { e.preventDefault(); choose(active); }
    else if (e.key === "Escape") close();
  });
  input.addEventListener("blur", () => setTimeout(close, 150));
}

/* ---------- Forms ---------- */
function initForm(form) {
  const status = form.querySelector(".form-status");
  const button = form.querySelector("button[type=submit]");
  const kind = form.dataset.form;
  const done = {
    waitlist: "You’re on the list. We’ll email you when FairFee™ opens in your area.",
    valuation: "Thanks! We’ll get back to you soon with your home’s value.",
    alerts: "You’re signed up. Your first neighbourhood update is on its way soon.",
  }[kind] || "Request sent. We’ll be in touch to find a time.";

  const valid = (el) => {
    const v = el.value.trim();
    let ok = v !== "" && el.checkValidity();
    if (ok && el.name === "contact") ok = /@.+\./.test(v) || v.replace(/\D/g, "").length >= 10;
    return ok;
  };
  // Clear an error as soon as the field is fixed, whether typed, pasted or filled in by the browser's autofill
  const recheck = (e) => {
    const el = e.target;
    if (el.getAttribute("aria-invalid") !== "true" || !valid(el)) return;
    el.setAttribute("aria-invalid", "false");
    if (!form.querySelector('[aria-invalid="true"]') && !status.classList.contains("ok")) status.textContent = "";
  };
  form.addEventListener("input", recheck);
  form.addEventListener("change", recheck);
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    status.className = "form-status";
    let bad = null;
    form.querySelectorAll("[required]").forEach((el) => {
      if (el.name === "contact" || el.type === "email") el.value = el.value.trim();
      const ok = valid(el);
      el.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok && !bad) bad = el;
    });
    if (bad) {
      const lab = form.querySelector(`label[for="${bad.id}"]`);
      const name = lab ? lab.firstChild.textContent.trim().toLowerCase() : "details";
      status.textContent = bad.type === "checkbox" ? "Tick the box so we’re allowed to email you."
        : bad.name === "contact" && bad.value
        ? "Enter a phone number with area code, or a full email address."
        : bad.type === "email" && bad.value ? "Enter a full email address, like name@example.com." : `Add your ${name} to send this.`;
      bad.focus();
      return;
    }
    if (WEB3FORMS_KEY.startsWith("YOUR_")) {
      status.textContent = "This form isn’t connected yet. Email mohamed@dahrouj.com or call 613-869-5923.";
      return;
    }
    const data = Object.fromEntries(new FormData(form));
    if (data.botcheck) return;
    delete data.botcheck;
    const payload = {
      access_key: WEB3FORMS_KEY,
      subject: {
        waitlist: `FairFee waitlist: ${data.role}, ${data.area}`,
        valuation: `Home value request: ${data.address}`,
        alerts: `Neighbourhood sales updates: ${data.neighbourhood} (${data.email})`,
      }[kind] || `dahrouj.com: ${data.topic} (${data.name})`,
      from_name: kind === "waitlist" ? "FairFee waitlist" : "dahrouj.com",
      replyto: data.email || (data.contact && data.contact.includes("@") ? data.contact : undefined),
      ...data,
    };
    button.disabled = true;
    status.textContent = "Sending…";
    try {
      const r = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload),
      });
      const res = await r.json().catch(() => ({}));
      if (!r.ok || res.success === false) throw new Error(res.message || r.status);
      form.reset();
      status.textContent = done;
      status.classList.add("ok");
    } catch (err) {
      status.textContent = "That didn’t go through. Check your connection and try again, or email mohamed@dahrouj.com.";
    } finally {
      button.disabled = false;
    }
  });
}

/* ---------- Calculator tabs ---------- */
function initTabs(list) {
  const tabs = [...list.querySelectorAll('[role="tab"]')];
  const select = (tab, focus) => {
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute("aria-selected", on); t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    });
    if (focus) tab.focus();
  };
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => select(t));
    t.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") select(tabs[(i + 1) % tabs.length], true);
      if (e.key === "ArrowLeft") select(tabs[(i - 1 + tabs.length) % tabs.length], true);
    });
  });
  const fromHash = tabs.find((t) => "#" + t.getAttribute("aria-controls") === location.hash);
  if (fromHash) select(fromHash);
}

/* ---------- Contact presets (contact.html#search, #cottage) ---------- */
function initContactPreset() {
  const presets = {
    search: { topic: "Starting a custom home search", title: "Start your custom search", lede: "Tell us your budget, timing and must-haves. We’ll build a custom search and send you homes as they list." },
    cottage: { topic: "Buying a cottage", title: "Start your cottage search", lede: "Tell us your budget, drive time and the kind of water you want. We’ll send you cottages as they list." },
  };
  const p = presets[location.hash.slice(1)];
  if (!p || !$("#c-topic")) return;
  $("#c-topic").value = p.topic;
  $("#c-title").textContent = p.title;
  $("#c-lede").textContent = p.lede;
}

/* ---------- Boot ---------- */
initContactPreset();
document.querySelectorAll("[data-tabs]").forEach(initTabs);
initMenu();
initLegal();
initCallbar();
initCalculators();
document.querySelectorAll(".year").forEach((el) => { el.textContent = new Date().getFullYear(); });
if ($("#calc")) loadJSON("fees").then(initFees).catch((e) => console.error(e));
if ($("#mk-rows") || $("[data-stat]")) {
  loadJSON("stats").then((st) => {
    if ($("[data-stat]")) initSnapshot(st);
    if ($("#mk-rows")) initStats(st);
  }).catch((e) => {
    console.error(e);
    const el = $("#mk-summary");
    if (el) el.textContent = "Market numbers couldn’t load right now. The full monthly reports are on the Ottawa Real Estate Board website.";
  });
}
if ($("#v-address")) initAddress($("#v-address"));
document.querySelectorAll("form[data-form]").forEach(initForm);
