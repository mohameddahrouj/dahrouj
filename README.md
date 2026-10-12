# dahrouj.com

Team website (Right at Home Realty, Brokerage), hosted on GitHub Pages from `master`. The team name "Capital Home Group" is a placeholder: search-and-replace it across the four HTML pages once a name is chosen.

## Files

- `index.html` (home), `market.html` (market report), `contact.html` (consultation form), `fairfee.html` (Fairfee soft launch and fee calculator)
- `assets/css/site.css`, `assets/js/site.js` — shared styles and script. No build step, no dependencies.
- `data/fees.json` — the listing fee, buyer rebate and wording shown in the fee calculator. Set `"draft": false` once the terms are final.
- `data/stats.json` — Ottawa market numbers. Updated by the monthly workflow below.

## Contact form and Fairfee waitlist

Both forms send through [Web3Forms](https://web3forms.com), which works on static hosts like GitHub Pages. Get a free access key for mohamed@dahrouj.com and paste it into `WEB3FORMS_KEY` at the top of `assets/js/site.js`. Until then the forms tell visitors to call or email instead.

## Monthly market stats

`.github/workflows/monthly-stats.yml` runs on the 6th, 9th and 13th of each month. It downloads the Ottawa Real Estate Board's monthly market update PDF, extracts the headline numbers with `scripts/update_stats.py`, and opens a pull request that changes `data/stats.json`. Check the numbers against the PDF and merge to publish.

To run it by hand: Actions tab → Monthly market stats → Run workflow (optionally enter a month like `2026-09`).

One-time setting: Settings → Actions → General → Workflow permissions → allow GitHub Actions to create pull requests.
