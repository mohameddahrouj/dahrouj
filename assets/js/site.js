// dahrouj.com: fee calculator, market stats and forms. No dependencies.

// Web3Forms access key: get one free at https://web3forms.com (enter mohamed@dahrouj.com).
// It's safe to publish; it only lets this site send mail to that inbox.
const WEB3FORMS_KEY = "YOUR_WEB3FORMS_ACCESS_KEY";

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

  $("#fees-draft").hidden = !fees.draft;
  $("#sell-rate").textContent = rate(s.listingRate);
  $("#coop-rate").textContent = rate(s.buyerAgentRate);
  $("#buy-rate").textContent = rate(b.assumedBuyerAgentRate);
  $("#buy-share").textContent = `${b.rebateShare}%`;
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
    const rebate = p >= b.minimumPrice ? comm * b.rebateShare / 100 : 0;
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

/* ---------- Market stats ---------- */
function summarize(m) {
  const parts = [];
  const more = m.activeListings.yoy > 0;
  parts.push(more ? "More homes are for sale than a year ago" : "Fewer homes are for sale than a year ago");
  if (m.daysOnMarket.value > m.daysOnMarket.lastYear) parts.push("and they’re taking longer to sell");
  else if (m.daysOnMarket.value < m.daysOnMarket.lastYear) parts.push("and they’re selling faster");
  let s = parts.join(" ") + ". ";
  const p = m.benchmarkPrice.yoy;
  s += Math.abs(p) < 1
    ? "Benchmark prices are close to where they were last year."
    : `Benchmark prices are ${p > 0 ? "up" : "down"} ${Math.abs(p).toFixed(1)}% from last year.`;
  return s;
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
  $("#mk-rows").replaceChildren(...rows.map(([label, now, then]) => {
    const tr = document.createElement("tr");
    const th = Object.assign(document.createElement("td"), { textContent: label });
    const a = Object.assign(document.createElement("td"), { textContent: now });
    const c = Object.assign(document.createElement("td"), { textContent: then });
    tr.append(th, a, c);
    return tr;
  }));

  const max = Math.max(...st.benchmarkByType.map((t) => t.value));
  $("#mk-types").replaceChildren(...st.benchmarkByType.map((t) => {
    const li = document.createElement("li");
    li.innerHTML = `<div class="bar-head"><span></span><span></span></div>
      <div class="bar-track" aria-hidden="true"><div class="bar-fill"></div></div>
      <span class="bar-change"></span>`;
    const [name, val] = li.querySelectorAll(".bar-head span");
    name.textContent = t.type;
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

/* ---------- Forms ---------- */
function initForm(form) {
  const status = form.querySelector(".form-status");
  const button = form.querySelector("button[type=submit]");
  const kind = form.dataset.form;
  const done = kind === "waitlist"
    ? "You’re on the list. We’ll email you when Fairfee opens in your area."
    : "Request sent. We’ll be in touch to find a time.";

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    status.className = "form-status";
    let bad = null;
    form.querySelectorAll("[required]").forEach((el) => {
      const ok = el.value.trim() !== "" && el.checkValidity();
      el.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok && !bad) bad = el;
    });
    if (bad) {
      const name = form.querySelector(`label[for="${bad.id}"]`).firstChild.textContent.trim().toLowerCase();
      status.textContent = bad.type === "email" && bad.value ? "Enter a full email address, like name@example.com." : `Add your ${name} to send this.`;
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
      subject: kind === "waitlist" ? `Fairfee waitlist: ${data.role}, ${data.area}` : `dahrouj.com: ${data.topic} (${data.name})`,
      from_name: kind === "waitlist" ? "Fairfee waitlist" : "dahrouj.com",
      replyto: data.email,
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

/* ---------- Boot ---------- */
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
document.querySelectorAll("form[data-form]").forEach(initForm);
