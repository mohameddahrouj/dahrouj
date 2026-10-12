# dahrouj.com

Team website (Right at Home Realty, Brokerage), hosted on GitHub Pages from `master`. The team name "Capital Home Group" is a placeholder: search-and-replace it across the HTML pages once a name is chosen.

## Files

- `index.html` (home), `neighbourhoods.html`, `market.html` (monthly report), `calculators.html` (land transfer tax, mortgage payment, affordability, CMHC), `contact.html` (consultation form and office map), `fairfee.html` (FairFee™ waitlist and fee calculator)
- `assets/css/site.css`, `assets/js/site.js` — shared styles and script. No build step, no dependencies.
- `data/fees.json` — FairFee terms: 1.5% listing brokerage, 2% buyer's brokerage, and buyer cash back prorated at $1,000 per $400,000 of purchase price (shown only in the calculator).
- Calculator rules (Ontario land transfer tax brackets, CMHC premiums, the 5.25% stress-test floor, 39%/44% debt limits) live in `assets/js/site.js`; check them when governments change the rules.
- `data/stats.json` — Ottawa market numbers. Updated by the monthly workflow below.

## Contact form and Fairfee waitlist

Both forms send through [Web3Forms](https://web3forms.com), which works on static hosts like GitHub Pages. Get a free access key for mohamed@dahrouj.com and paste it into `WEB3FORMS_KEY` at the top of `assets/js/site.js`. Until then the forms tell visitors to call or email instead.

## Monthly market stats

`.github/workflows/monthly-stats.yml` runs on the 6th, 9th and 13th of each month. It downloads the Ottawa Real Estate Board's monthly market update PDF, extracts the headline numbers with `scripts/update_stats.py`, and opens a pull request that changes `data/stats.json`. Check the numbers against the PDF and merge to publish.

To run it by hand: Actions tab → Monthly market stats → Run workflow (optionally enter a month like `2026-09`).

One-time setting: Settings → Actions → General → Workflow permissions → allow GitHub Actions to create pull requests.
