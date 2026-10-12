#!/usr/bin/env python3
"""Pull the monthly OREB market update and write data/stats.json.

Usage:
  python scripts/update_stats.py                 # last month's report
  python scripts/update_stats.py --month 2026-09 # a specific month
  python scripts/update_stats.py --dump out.txt  # also save the extracted text

The script exits with code 2 when the report for that month isn't published
yet, so the workflow can stop quietly and try again later.
"""
import argparse
import calendar
import datetime as dt
import io
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "stats.json"
UA = "Mozilla/5.0 (compatible; dahrouj.com stats updater)"


def previous_month(today):
    first = today.replace(day=1)
    last = first - dt.timedelta(days=1)
    return last.year, last.month


def candidate_urls(year, month):
    name = calendar.month_name[month]
    yy = f"{year % 100:02d}"
    # OREB uploads the report in the month after it covers (sometimes later).
    uploads = []
    for offset in (1, 2, 0):
        m = month + offset
        y = year + (m - 1) // 12
        m = (m - 1) % 12 + 1
        uploads.append((y, m))
    for host in ("www.oreb.ca", "members.oreb.ca"):
        for y, m in uploads:
            for stem in (f"OREB_MarketUpdate_HLP_{name}{yy}", f"OREB_MarketUpdate_{name}{yy}"):
                yield f"https://{host}/wp-content/uploads/{y}/{m:02d}/{stem}.pdf"


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if not data.startswith(b"%PDF"):
        raise ValueError("not a PDF")
    return data


def pdf_text(data):
    import pdfplumber

    with pdfplumber.open(io.BytesIO(data)) as pdf:
        return "\n\f\n".join((p.extract_text() or "") for p in pdf.pages)


NUM = r"-?\$?[\d,]+(?:\.\d+)?"


def num(s):
    return float(s.replace("$", "").replace(",", ""))


def section(text, heading):
    """Text from the first line that starts with `heading` onward."""
    i = text.find("\n" + heading)
    if i < 0:
        raise LookupError(f"section not found: {heading!r}")
    return text[i + 1:]


def row(text, label, count):
    """Return the first `count` numbers that follow `label` on its line.

    Table labels sometimes carry a footnote digit ("Months of Inventory2 4.8"
    or "Ratio 5 44.8"); a lone single digit right after the label is skipped.
    """
    for line in text.splitlines():
        if line.strip().lower().startswith(label.lower()):
            rest = line.strip()[len(label):]
            rest = re.sub(r"^\s*\d(?=\s)", "", rest)
            vals = re.findall(NUM, rest.replace("%", ""))
            vals = [v for v in vals if re.search(r"\d", v)]
            if len(vals) >= count:
                return [num(v) for v in vals[:count]]
    raise LookupError(f"row not found: {label!r}")


def parse(text):
    """Parse the citywide 'MLS® Residential Market Activity' and HPI tables.

    Activity rows read <label> <this year> <change vs last year> ...; for
    ratio rows the second number is last year's value instead of a change.
    HPI rows read <type> <benchmark> <1 mo> <3 mo> <6 mo> <12 mo> <3 yr> <5 yr>.
    """
    month = section(text, "MLS® Residential Market Activity")
    ytd = section(month, "Year-to-Date")
    m = {}
    v, c = row(month, "Sales Activity", 2)
    m["sales"] = {"value": int(v), "yoy": c}
    v, c = row(month, "Average Price", 2)
    m["averagePrice"] = {"value": int(v), "yoy": c}
    v, c = row(month, "Median Price", 2)
    m["medianPrice"] = {"value": int(v), "yoy": c}
    v, c = row(month, "New Listings", 2)
    m["newListings"] = {"value": int(v), "yoy": c}
    v, c = row(month, "Active Listings", 2)
    m["activeListings"] = {"value": int(v), "yoy": c}
    v, last = row(month, "Months of Inventory", 2)
    m["monthsOfInventory"] = {"value": v, "lastYear": last}
    v, last = row(month, "Median Days on Market", 2)
    m["daysOnMarket"] = {"value": int(v), "lastYear": int(last)}
    v, last = row(month, "Sale to List Price Ratio", 2)
    m["saleToListRatio"] = {"value": v, "lastYear": last}

    hpi = section(text, "MLS® Home Price Index Benchmark Price")
    types = []
    for label, name in (("Composite", None), ("Single Family", "Single family"),
                        ("Townhouse", "Townhouse"), ("Apartment", "Apartment")):
        vals = row(hpi, label, 7)
        if name is None:
            m["benchmarkPrice"] = {"value": int(vals[0]), "yoy": vals[4]}
        else:
            types.append({"type": name, "value": int(vals[0]), "yoy": vals[4]})

    y = {}
    v, c = row(ytd, "Sales Activity", 2)
    y["sales"] = {"value": int(v), "yoy": c}
    v, c = row(ytd, "Average Price", 2)
    y["averagePrice"] = {"value": int(v), "yoy": c}
    return m, types, y


def sanity_check(m):
    s = m["sales"]["value"]
    p = m["averagePrice"]["value"]
    b = m["benchmarkPrice"]["value"]
    assert 200 <= s <= 5000, f"sales out of range: {s}"
    assert 300_000 <= p <= 2_000_000, f"average price out of range: {p}"
    assert 300_000 <= b <= 2_000_000, f"benchmark out of range: {b}"
    assert 0.5 <= m["monthsOfInventory"]["value"] <= 15, "months of inventory out of range"
    assert 85 <= m["saleToListRatio"]["value"] <= 115, "sale-to-list ratio out of range"
    for k, v in m.items():
        if "yoy" in v:
            assert -60 <= v["yoy"] <= 60, f"{k} change out of range: {v['yoy']}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", help="YYYY-MM (default: last month)")
    ap.add_argument("--dump", help="write the extracted PDF text here")
    ap.add_argument("--dump-only", action="store_true")
    args = ap.parse_args()

    if args.month:
        year, month = map(int, args.month.split("-"))
    else:
        year, month = previous_month(dt.date.today())

    data = url = None
    for u in candidate_urls(year, month):
        try:
            data = download(u)
            url = u
            break
        except (urllib.error.URLError, ValueError, TimeoutError) as e:
            print(f"  no report at {u} ({e})")
    if data is None:
        print(f"OREB report for {year}-{month:02d} isn't published yet.")
        return 2
    print(f"Found report: {url}")

    text = pdf_text(data)
    if args.dump:
        pathlib.Path(args.dump).write_text(text)
    if args.dump_only:
        return 0

    market, types, ytd = parse(text)
    sanity_check(market)

    current = json.loads(OUT.read_text()) if OUT.exists() else {}
    released = re.search(r"OTTAWA,\s+([A-Z][a-z]+ \d{1,2}, \d{4})", text)
    out = {
        "month": f"{year}-{month:02d}",
        "label": f"{calendar.month_name[month]} {year}",
        "compareLabel": f"{calendar.month_name[month]} {year - 1}",
        "released": (dt.datetime.strptime(released.group(1), "%B %d, %Y").date().isoformat()
                     if released else dt.date.today().isoformat()),
        "source": "Ottawa Real Estate Board (OREB)",
        "sourceUrl": url,
        "market": market,
        "benchmarkByType": types,
        "yearToDate": ytd,
    }
    if current.get("month") == out["month"] and current.get("market") == market \
            and current.get("yearToDate") == ytd:
        print("Stats already up to date.")
        return 0
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write(f"label={out['label']}\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
