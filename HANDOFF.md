# Handoff — Eastbridge website

Delivered as two zips: unzip BOTH into the same place (part 2 adds the 1280px images into src/static/assets/img/). The build fails without them.

Static site for Eastbridge Strategic Partners (client-side villa project management, Dubai and Abu Dhabi).
English source, published in Arabic (/ar/, right to left), Russian (/ru/), Simplified Chinese (/zh/) and Hindi (/hi/).
This folder is not yet a git repository. First run: `git init -b main && git add -A && git commit -m "Initial site"`

## Goal
1. Push this repository to GitHub as private repo `pcc40/eastbridge-website` (already created, empty):
   `git remote add origin https://github.com/pcc40/eastbridge-website.git && git push -u origin main`
2. Link the existing Netlify site to that repo (Netlify → Site configuration → Build & deploy → Link repository).
   Build settings come from `netlify.toml`: `pip install markdown pyyaml beautifulsoup4 && python3 build.py && python3 tools/i18n.py apply`, publish `dist`, Python 3.11.
3. Give the Claude GitHub app access to the repo (github.com/settings/installations → Claude → Configure → Repository access)
   so the daily scheduled "Eastbridge SEO engine" task can clone, publish articles and push. Each push redeploys Netlify.

## Build and check locally
```
pip install markdown pyyaml beautifulsoup4
python3 build.py && python3 tools/i18n.py apply
python3 tools/seo_audit.py        # must report 0 errors
python3 -m http.server 8765 --directory dist
```

## Where things are
- `build.py`, `src/pages.py`, `src/pages_new.py` — page templates; `src/content/` — copy, projects, case study model, articles (`insights/*.md`)
- `src/config.py` — domain, contact details, fees switch. Set `SITE_URL` to the live domain before launch.
- `src/i18n/<lang>.json` — translations keyed by a hash of each English segment; `tools/i18n.py extract|merge|apply`
- `src/i18n/TRANSLATION_BRIEF.md` — glossary and compliance rules for translations
- `src/content/WRITING_BRIEF.md` — voice and compliance rules for all copy (read before editing text)
- `src/static/assets/site.css` and generated `site-rtl.css` (run `sh tools/make_rtl.sh` after editing site.css)
- `AUTOMATION.md` — the daily SEO engine playbook; `tools/indexnow.py` — pings search engines

## Rules that must not be broken
- Eastbridge is a client-side project manager / owner's representative. Never an engineer, architect, contractor or design consultant.
- Never claim or imply UAE projects or existing Eastbridge clients. The Island E case study is illustrative and must stay labelled so.
- No client names. All project photos are P Chapman Construction's (UK) and Phil holds the rights.

## Home hero film (`HERO_VIDEO` in `src/config.py`)
- Default `False`: the hero shows the photo slideshow only. The Vimeo film (`HERO_VIDEO_VIMEO_ID`, 219974514) currently returns 401 because its privacy setting does not allow embedding on our domain, which used to leave a loading spinner over the hero.
- To enable: in Vimeo, open the video, Settings > Privacy > "Where can this be embedded?" > Specific domains, add `eastbridgepartners.ae` (and the Netlify preview domain if wanted). Then set `HERO_VIDEO = True`, rebuild and deploy.
- Even when enabled, the film loads only on screens 900px and wider, never with reduced-motion or Save-Data, and stays invisible until Vimeo reports that it is playing. If it has not started within 9 seconds, or Vimeo reports an error, it is removed and the poster stays.

## Conversion components
- Mobile action bar (WhatsApp / Call / Start a brief) replaces the WhatsApp float below 760px; on larger screens the float remains. `build.action_bar()`.
- "How it starts" strip (free 30-minute call, fixed-fee first review, appointment) sits above the home CTA and in short form on the contact page: `build.start_steps()` / `build.how_it_starts()`. A fee figure appears only when `PUBLISH_FEES = True`.
- Contact form: Netlify attributes, `form-name` and the `company_site` honeypot are unchanged. New/renamed fields: `stage` (now a select, was checkboxes), `contact_method` (Email / Phone call / WhatsApp; phone becomes required for the last two), `based`, `area`, `budget`. Inline validation messages are HTML (so they translate); the script only shows them.
- `/contact/thanks/` serves both forms. The newsletter posts to `/contact/thanks/#notes`, which swaps in the subscriber wording.

## Design checks
- `python3 tools/contrast_check.py` checks WCAG AA contrast for the colour pairs the stylesheet uses (reads the `:root` tokens). Run it after any palette change.
- `node tools/screens.js <port> <outdir> <tag>` takes desktop (1440) and mobile (390) screenshots of the key pages from a locally served `dist/`. Before/after shots from the design pass are in `reports/screens/`.
- After editing `site.css`, run `sh tools/make_rtl.sh` and check `/ar/`.
