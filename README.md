# Eastbridge Strategic Partners — website

Static site, built with Python. No framework, no database: fast, secure and cheap to host.

## Build locally
pip install markdown pyyaml beautifulsoup4
python3 build.py && python3 tools/i18n.py apply   # writes dist/ in all five languages
python3 tools/seo_audit.py

## Where things live
- src/config.py — domain, email, phone, WhatsApp, fees switch, analytics IDs
- src/content/services.py, areas.py, projects.py — page content
- src/content/insights/*.md — articles (Markdown + front matter)
- src/content/TOPICS.md — article backlog for the SEO engine
- src/content/WRITING_BRIEF.md — voice, compliance and format rules for every article
- AUTOMATION.md — what the daily SEO task does
- src/pages_tools.py, pages_glossary.py, pages_guides.py — cost calculator (/tools/), glossary (/glossary/), checklist lead magnet (/guides/)
- netlify/functions/submission-created.js — form auto-acknowledgement, lead alert and Google Sheet log (configured by Netlify environment variables)
- business/ — first-client plan, automation blueprint, off-site authority kit (Google Business Profile copy), outreach kit, competitor report
- HANDOFF.md — what was added most recently and the full go-live checklist
- dist/ — the built site (what Netlify publishes; not committed)

## Deploy
Netlify: connect the GitHub repo (build command and publish folder are in netlify.toml), or drag the dist folder onto app.netlify.com/drop for a one-off deploy.

## Languages
The site is built in English and published in Arabic (/ar/, right to left), Russian (/ru/), Simplified Chinese (/zh/) and Hindi (/hi/).
- Build: `python3 build.py && python3 tools/i18n.py apply` (Netlify runs both; needs `beautifulsoup4`).
- Translations live in `src/i18n/<lang>.json`, keyed by a hash of each English sentence. Change the English and the old translation drops out; `python3 tools/i18n.py extract` lists what needs translating. Until it is translated, that text shows in English.
- Every page carries hreflang links for all five languages, a language switcher, and a hidden `language` field on forms so you can see which language an enquiry came from.
- Arabic uses `src/static/assets/site-rtl.css`; regenerate it with `sh tools/make_rtl.sh` after editing `site.css`, then rebuild and run `node tools/make_critical.js` to refresh the inlined first-screen CSS (`src/critical.json`).

## Go live
See the go-live checklist in HANDOFF.md: `SITE_URL`, `PUBLISH_FEES`, `HERO_VIDEO`, `GA4_ID` / `GSC_VERIFICATION`, Netlify environment variables for the form function (`EMAIL_API_KEY`, `EMAIL_FROM` and optional extras), Google Business Profile, and Claude GitHub app access for the daily SEO task.
