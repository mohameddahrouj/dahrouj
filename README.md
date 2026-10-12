# dahrouj.com

Single-page site for Mohamed Dahrouj, Sales Representative, Right at Home Realty, Brokerage. Hosted on GitHub Pages from `master`.

## Files

- `index.html`, `assets/css/site.css`, `assets/js/site.js` — the page. No build step, no dependencies.
- `data/fees.json` — the listing fee, buyer rebate and wording shown in the fee calculator. Set `"draft": false` once the terms are final.
- `data/stats.json` — Ottawa market numbers. Updated by the monthly workflow below.

## Contact form and Fairfee waitlist

Both forms send through [Web3Forms](https://web3forms.com), which works on static hosts like GitHub Pages. Get a free access key for mohamed@dahrouj.com and paste it into `WEB3FORMS_KEY` at the top of `assets/js/site.js`. Until then the forms tell visitors to call or email instead.

## Monthly market stats

`.github/workflows/monthly-stats.yml` runs on the 6th, 9th and 13th of each month. It downloads the Ottawa Real Estate Board's monthly market update PDF, extracts the headline numbers with `scripts/update_stats.py`, and opens a pull request that changes `data/stats.json`. Check the numbers against the PDF and merge to publish.

To run it by hand: Actions tab → Monthly market stats → Run workflow (optionally enter a month like `2026-09`).

One-time setting: Settings → Actions → General → Workflow permissions → allow GitHub Actions to create pull requests.
