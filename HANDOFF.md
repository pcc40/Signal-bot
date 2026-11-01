# Handoff — Eastbridge website

Static site for Eastbridge Strategic Partners (client-side villa project management, Dubai and Abu Dhabi).
English source, published in Arabic (/ar/, right to left), Russian (/ru/), Simplified Chinese (/zh/) and Hindi (/hi/).
The source lives in the GitHub repository `pcc40/eastbridge-website` (branch `main`). Live address: https://eastbridgestrategicpartners.com (contact: philip@eastbridgestrategicpartners.com); the .ae and www hosts 301 to it via `netlify.toml`.
A single handoff zip, `eastbridge-website-handoff.zip` (top folder `eastbridge/`), holds the full source including all image sizes. It is gitignored.

## Calculator: currency, share, save and send (November 2026, branch `eb3/calc`)
From the competitor brief (`reports/competitor-brief-recd-2026-11-01.md`, items 1, 2 and 8):
- **Currency display.** "Show amounts in" selector: AED (default everywhere), GBP, USD and EUR on every language; RUB only on /ru/, CNY only on /zh/, INR only on /hi/. AED stays the only calculation currency; other currencies are display-only conversions labelled "approximate, at rates of <date>". Each converted line is rounded like the AED lines, so converted columns still add up. Fixed rates live in `FX` / `FX_INPUTS` / `FX_AS_AT` in `src/pages_tools.py` (no live API calls): US dollar from the AED 3.6725 peg, GBP/EUR/CNY/INR crossed from the ECB euro reference rates, RUB from the Bank of Russia official rate. Sources are listed on the page (sources 9–11) and in the methodology.
- **Shareable link.** Inputs are mirrored to the query string (`history.replaceState`) and read on load; "Copy link" button.
- **Save as PDF.** `window.print()` with a dedicated print stylesheet (`@media print` block under "Currency, review line, share/save/send" in `site.css`): letterhead, inputs, line-by-line result (lines not included are left out), timeline, date, sources note, Eastbridge contact line and the link to reopen the estimate. One A4 page in all five languages, even with every extra selected.
- **WhatsApp with the estimate.** "Discuss on WhatsApp" is pre-filled with a one-line summary (messages `wa-*` in `#calc-msgs`, translated like every calculator message).
- **"Send this estimate to Philip".** New Netlify form **`estimate`** on the calculator page (name, email, optional phone, plot location and notes; hidden `estimate_inputs`, `estimate_result`, `estimate_link`, `currency`; `company_site` honeypot; optional unticked `marketing_opt_in`; "We never pass your details to contractors or suppliers."). Thanks page `/tools/villa-build-cost-calculator/thanks/` (noindex). Registered in `netlify/functions/submission-created.js`: logged to the sheet (status "Estimate request"), lead alert, and an acknowledgement that never repeats the submitted figures. After deploy, check the `estimate` form appears under Netlify → Forms and send a test from the English and one translated page.
- **Trust line.** "Rates last reviewed: <month year>, by Philip Chapman" under the result, from `RATES_REVIEWED` in `src/pages_tools.py`.
- **Privacy notice** lists calculator estimates.
- Checks: `node tools/calc_check.js --strict` now also covers currency switching, the URL round trip, Copy link, the WhatsApp text, the hidden form fields and the one-page PDF; `node tools/test_submission_function.js` covers the `estimate` form.
- **Monthly upkeep:** refresh `FX_INPUTS` and `FX_AS_AT`, and `RATES_REVIEWED` once the construction rates are re-checked (AUTOMATION.md, Monthly, step 12). The dates appear in translated text, so run the Languages steps afterwards.

## What was added in the latest round (October 2026)
All new pages are translated into the four other languages (1,337 new segments per language, 0 untranslated) and pass `tools/seo_audit.py` with 0 errors and 0 warnings across 390 pages.

New pages (English URLs; each also exists under /ar/, /ru/, /zh/ and /hi/):
- `/tools/` — tools hub
- `/tools/villa-build-cost-calculator/` — build and renovation cost calculator (`src/pages_tools.py`, `src/static/assets/calc.js`); every rate is sourced on the page
- `/glossary/` — villa construction glossary, 68 terms (`src/content/glossary.py`, `src/pages_glossary.py`)
- `/guides/villa-owner-checklist/` and `/guides/villa-owner-checklist/thanks/` — lead magnet landing page and download page for the Villa Owner's Pre-Construction Checklist PDF (`src/pages_guides.py`; PDF built by `tools/make_checklist_pdf.py`)
- Six new insights:
  - `/insights/dubai-municipality-villa-building-permit/`
  - `/insights/abu-dhabi-villa-permit-tamm/`
  - `/insights/villa-renovation-cost-dubai/`
  - `/insights/how-long-to-build-a-villa-dubai/`
  - `/insights/nakheel-noc-villa-renovation/`
  - `/insights/stalled-villa-project-dubai/`

Site-wide changes: technical SEO and AI-search pass (structured data, `llms.txt` and `llms-full.txt`, full-text RSS feed at `/insights/feed.xml`, IndexNow key, security and cache headers in `netlify.toml`); design and conversion pass (robust hero, mobile action bar, "How it starts" strip, rebuilt contact form, `/contact/thanks/`); Netlify form function `netlify/functions/submission-created.js` (auto-acknowledgement email, lead alert, Google Sheet log).

Calculator: all live-updating text is translated (fixed in the October review round; `node tools/calc_check.js --strict` checks it).

## Business documents (`business/`)
- `business/first-client-plan.md` — ideal client profiles, referral partners, founding-client offer, 14-day sprint and 30/60/90 plan, discovery call script and objections
- `business/automation-blueprint.md` — lead capture, auto-acknowledgement, CRM, booking, WhatsApp, proposals and payment, onboarding, reporting, cost of the stack, and Phil's one-time checklist (section 14)
- `business/offsite-authority-kit.md` — NAP sheet, Google Business Profile copy (categories, description, services, Q&A, first posts), directories and LinkedIn
- `business/outreach-kit.md` — outreach templates for referral partners
- `business/seo-competitor-report.md` — competitor and keyword review
- `reports/visibility.csv` — search and AI-assistant visibility log; `src/content/TOPICS.md` — article backlog

## Go-live checklist (Phil)
1. **Domain and config** (`src/config.py`): confirm `SITE_URL` is the live domain; `INDEXABLE` defaults to True, so a normal build is indexable. For a preview, build with `EB_INDEXABLE=0` instead of editing the file (see "Noindex preview build" below).
2. **Fees**: published (`PUBLISH_FEES = True`, figures in `FEES`). Set it to False to hide them.
3. **Hero film**: `HERO_VIDEO = False` by default (see the section below). Enable only after the Vimeo embed domain is allowed.
4. **Analytics and verification** — done 1 Nov 2026: GA4 property "Eastbridge" (Measurement ID `G-120XT9N6XB`, UAE time zone, AED), Search Console verified by HTML tag (URL-prefix property), sitemap submitted (Success, 375 URLs), home page indexing requested; Bing Webmaster Tools imported from Search Console with the sitemap.
5. **Netlify** — done 31 Oct 2026: linked to `pcc40/eastbridge-website` (auto-publish from `main`, deploys from non-team Git contributors auto-approved), form detection on, `brief`, `checklist` and `notes` forms active, submission emails to philip@eastbridgestrategicpartners.com.
6. **Netlify environment variables** for `submission-created` (Project configuration → Environment variables). Without the first two, forms still work but no emails are sent:
   - `EMAIL_API_KEY` — Resend API key (or Postmark server token) — required for email
   - `EMAIL_FROM` — e.g. `Eastbridge Strategic Partners <philip@eastbridgestrategicpartners.com>`; the domain must be verified with the email provider (DNS records) — required for email
   - `EMAIL_PROVIDER` — `resend` (default) or `postmark`
   - `EMAIL_REPLY_TO`, `LEAD_ALERT_TO`, `BOOKING_URL`, `SHEET_WEBHOOK_URL`, `SHEET_WEBHOOK_TOKEN`, `AUTOREPLY_DISABLED`, `SITE_PUBLIC_URL` — optional; see the header of the function file and `business/automation-blueprint.md` section 3
   - After setting them, send a test enquiry from `/contact/` and from `/guides/villa-owner-checklist/`.
7. **Google Business Profile** — set up, not yet verified (1 Nov 2026). The existing unverified profile was used (no duplicate): service-area business, address hidden, category Property Consultant (Real estate consultant), service areas Dubai and Abu Dhabi, website corrected from dealdeed.ae to this site, description, Mon–Fri 9–6 hours and all 13 services with descriptions from `business/offsite-authority-kit.md`. Still to do: choose the verification route (read section 1.1 first), add the logo and photos per 1.7, then Bing Places and the LinkedIn company page, and add each profile URL to `SOCIAL` in `src/config.py`.
8. **Claude GitHub app access**: github.com/settings/installations → Claude → Configure → Repository access → include the site repository, so the daily scheduled SEO task can clone, publish articles and push. Each push redeploys Netlify.
9. **IndexNow**: after the first live deploy, run `python3 tools/indexnow.py --all` (after a local build) to notify Bing and other IndexNow engines.
10. **Review before launch**: read the six new insights, the glossary and the calculator page yourself; you are the named author.

## Build and check locally
```
pip install markdown pyyaml beautifulsoup4
python3 build.py && python3 tools/i18n.py apply
python3 tools/seo_audit.py        # must report 0 errors
python3 -m http.server 8765 --directory dist
```

### Noindex preview build
To publish a preview that search engines must not index (for example a Netlify drag-and-drop preview for review):
```
EB_INDEXABLE=0 python3 build.py && python3 tools/i18n.py apply
grep -c noindex dist/index.html     # 1 = every page carries noindex,nofollow
cat dist/robots.txt                 # User-agent: * / Disallow: /
```
`EB_INDEXABLE` accepts `0`, `false`, `no` or `off`; anything else, or leaving it unset, gives the normal indexable production build. Canonicals, hreflang, the sitemap and `SITE_URL` are not changed by this switch. Rebuild without the variable before the production deploy. On Netlify you can set `EB_INDEXABLE=0` as an environment variable scoped to deploy previews or branch deploys only, never to production.

## Where things are
- `build.py`, `src/pages.py`, `src/pages_new.py` — page templates; `src/content/` — copy, projects, case study model, articles (`insights/*.md`)
- `src/config.py` — domain, contact details, fees switch. Set `SITE_URL` to the live domain before launch.
- `src/i18n/<lang>.json` — translations keyed by a hash of each English segment; `tools/i18n.py extract|merge|apply`
- `src/i18n/TRANSLATION_BRIEF.md` — glossary and compliance rules for translations
- `src/content/WRITING_BRIEF.md` — voice and compliance rules for all copy (read before editing text)
- `src/static/assets/site.css` and generated `site-rtl.css` (run `sh tools/make_rtl.sh` after editing site.css)
- `AUTOMATION.md` — the daily SEO engine playbook; `tools/indexnow.py` — pings search engines
- `src/pages_tools.py`, `src/pages_glossary.py`, `src/pages_guides.py` — calculator, glossary and lead-magnet templates
- `netlify/functions/submission-created.js` — form auto-acknowledgement and lead log (forms `brief`, `checklist`, `notes`, `estimate`)
- `tools/i18n_check.py` — checks translation chunks (placeholders, tags, numbers) before merging
- `business/` — business plans and kits (see above)

## Rules that must not be broken
- Eastbridge is a client-side project manager / owner's representative. Never an engineer, architect, contractor or design consultant.
- Never claim or imply UAE projects or existing Eastbridge clients. The Island E case study is illustrative and must stay labelled so.
- No client names. All project photos are P Chapman Construction's (UK) and Phil holds the rights.

## Home hero film (`HERO_VIDEO` in `src/config.py`)
- Default `False`: the hero shows the photo slideshow only. The Vimeo film (`HERO_VIDEO_VIMEO_ID`, 219974514) currently returns 401 because its privacy setting does not allow embedding on our domain, which used to leave a loading spinner over the hero.
- To enable: in Vimeo, open the video, Settings > Privacy > "Where can this be embedded?" > Specific domains, add `eastbridgestrategicpartners.com` (and the Netlify preview domain if wanted). Then set `HERO_VIDEO = True`, rebuild and deploy.
- Even when enabled, the film loads only on screens 900px and wider, never with reduced-motion or Save-Data, and stays invisible until Vimeo reports that it is playing. If it has not started within 9 seconds, or Vimeo reports an error, it is removed and the poster stays.

## Conversion components
- Mobile action bar (WhatsApp / Call / Start a brief) replaces the WhatsApp float below 760px; on larger screens the float remains. `build.action_bar()`.
- "How it starts" strip (free 30-minute call, fixed-fee first review, appointment) sits above the home CTA and in short form on the contact page: `build.start_steps()` / `build.how_it_starts()`. A fee figure appears only when `PUBLISH_FEES = True`.
- Contact form: Netlify attributes, `form-name` and the `company_site` honeypot are unchanged. New/renamed fields: `stage` (now a select, was checkboxes), `contact_method` (Email / Phone call / WhatsApp; phone becomes required for the last two), `based`, `area`, `budget`. Inline validation messages are HTML (so they translate); the script only shows them.
- `/contact/thanks/` serves both forms. The newsletter posts to `/contact/thanks/#notes`, which swaps in the subscriber wording.

## Design checks
- `python3 tools/contrast_check.py` checks WCAG AA contrast for the colour pairs the stylesheet uses (reads the `:root` tokens). Run it after any palette change.
- `node tools/screens.js <port> <outdir> <tag>` takes desktop (1440) and mobile (390) screenshots of the key pages from a locally served `dist/`. Before/after shots from the design pass, and the final QA shots (`final-*.png`), are in `reports/screens/`.
- After editing `site.css`, run `sh tools/make_rtl.sh` and check `/ar/`.
