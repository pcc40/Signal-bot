# Handoff — Eastbridge website

Static site for Eastbridge Strategic Partners (client-side villa project management, Dubai and Abu Dhabi).
English source, published in Arabic (/ar/, right to left), Russian (/ru/), Simplified Chinese (/zh/) and Hindi (/hi/).
The source lives in the GitHub repository `pcc40/eastbridge-website` (branch `main`). Live address: https://eastbridgestrategicpartners.com (contact: philip@eastbridgestrategicpartners.com); the .ae and www hosts 301 to it via `netlify.toml`.
A single handoff zip, `eastbridge-website-handoff.zip` (top folder `eastbridge/`), holds the full source including all image sizes. It is gitignored.

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

## Snagging lead magnet (November 2026)
- `/guides/villa-snagging-checklist/` and `/guides/villa-snagging-checklist/thanks/` (thanks is noindex): second lead magnet, The Villa Snagging Checklist PDF, 13 pages (`src/pages_guides.py`; PDF and cover built by `python3 tools/make_snagging_pdf.py`, which reuses the design system in `tools/make_checklist_pdf.py`). Commit the regenerated PDF and `-cover.webp`.
- Both guides post to the same Netlify form, `checklist`, with identical fields; the hidden field `guide` (`villa-owner-checklist` or `villa-snagging-checklist`) tells them apart. `submission-created.js` writes `guide` to the sheet row and the log line; add a `guide` column header to the Leads sheet and the updated `COLS` from `business/automation-blueprint.md` section 4 to the Apps Script.
- Linked from `/insights/villa-snagging-checklist-dubai/` (body and end CTA: Handover-category articles show the snagging CTA), the snagging service page, `/tools/`, the footer and `llms.txt`.
- The defects-liability periods in the PDF (`LIABILITY`) and in the article must stay in step: Civil Transactions Law 1985 arts 880–883 (new law, Federal Decree-Law No. 25 of 2025, arts 821–824, for contracts from 1 June 2026) and Dubai Law No. 6 of 2019 art. 40.

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
- `netlify/functions/submission-created.js` — form auto-acknowledgement and lead log
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
