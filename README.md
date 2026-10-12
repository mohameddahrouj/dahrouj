# dahrouj.com

Real estate website (Right at Home Realty, Brokerage), hosted on GitHub Pages from `master`. There is no header bar (the menu lists What’s my home worth?, Ottawa Market, Calculators, FairFee™ and Contact; Moving to Ottawa and Cottages are linked from the home page): each page opens with the Dahrouj house logo standing in for the “D” of “dahrouj.com” (`assets/img/dahrouj-logo.png`, drawn in the site colour) and a Menu button. The brokerage logo is in the footer.

## Files

- `index.html` (home), `market.html` (Ottawa Market: monthly report and neighbourhoods), `home-value.html` (free home value request: just the address), `calculators.html` (land transfer tax, mortgage payment with CMHC insurance, affordability, shown one at a time in tabs), `moving-to-ottawa.html` (relocation, newcomers to Canada, military postings), `cottages.html` (buying a cottage near Ottawa), `contact.html` (consultation form; `contact.html#search` and `#cottage` open it as a custom search request and a simplified office map drawn from OpenStreetMap data, `assets/img/office-map.svg`), `fairfee.html` (our FairFee™ fee and calculator), `privacy.html` (privacy policy, linked from the footer and under each form)
- `assets/css/site.css`, `assets/js/site.js` — shared styles and script. No build step, no dependencies.
- `assets/fonts/` — Schibsted Grotesk and Poppins, self-hosted (SIL Open Font License, licence files included) so no visitor data goes to Google Fonts.
- `data/fees.json` — FairFee terms: 1.5% listing brokerage, 2% buyer's brokerage, and buyer cash back prorated at $1,000 per $400,000 of purchase price (shown only in the calculator).
- Calculator rules (Ontario land transfer tax brackets, CMHC premiums, the 5.25% stress-test floor, 39%/44% debt limits) live in `assets/js/site.js`; check them when governments change the rules.
- `data/stats.json` — Ottawa market numbers. Updated by the monthly workflow below.

## Home page photo

`assets/img/hero-canal*.webp`: the Rideau Canal from Laurier Avenue by Dylan Phair, from Unsplash (free under the Unsplash License; no credit required). `hero-canal.webp` and `hero-canal-1400.webp` are wide crops for computers, and `hero-canal-tall.webp` is a portrait crop for phones.

## Lake outlines

The Cottages page draws Big Rideau Lake, Mississippi Lake, Calabogie Lake and White Lake from OpenStreetMap shorelines (`assets/img/lakes.json`, simplified SVG paths; © OpenStreetMap contributors).

## Search engines and AI assistants

Every page has its own title, description and canonical link. The home page carries `RealEstateAgent` structured data (services, areas served, topics), and the Moving to Ottawa and Cottages pages carry `FAQPage` data. `sitemap.xml` and `robots.txt` are generated with the pages, and `llms.txt` gives AI assistants a plain summary of the business. Keep the name, address and phone identical here, on Google Business Profile and on the brokerage roster.

## Contact and home value forms

The forms send through [Web3Forms](https://web3forms.com), which works on static hosts like GitHub Pages. Get a free access key for mohamed@dahrouj.com and paste it into `WEB3FORMS_KEY` at the top of `assets/js/site.js`. Until then the forms tell visitors to call or email instead. If you change form or address providers, update `privacy.html` (generated from the `PRIVACY` text in the page script) to name them.

## Address suggestions (home-value.html)

The address box suggests real addresses as people type. Get a free Geoapify key (myprojects.geoapify.com, 3,000 lookups a day), restrict it to `dahrouj.com` under the key's allowed origins, and paste it into `ADDRESS_LOOKUP.key` in `assets/js/site.js`. Google Places (`provider: "google"`) and Canada Post AddressComplete (`provider: "canadapost"`) are also wired in if you'd rather use one of those. With no key, the box works as a normal text field.

## Monthly market stats

`.github/workflows/monthly-stats.yml` runs on the 6th, 9th and 13th of each month. It downloads the Ottawa Real Estate Board's monthly market update PDF, extracts the headline numbers with `scripts/update_stats.py`, and opens a pull request that changes `data/stats.json`. Check the numbers against the PDF and merge to publish.

To run it by hand: Actions tab → Monthly market stats → Run workflow (optionally enter a month like `2026-09`).

One-time setting: Settings → Actions → General → Workflow permissions → allow GitHub Actions to create pull requests.
