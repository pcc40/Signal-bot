# Eastbridge SEO engine — the playbook the scheduled task follows

Repository: `pcc40/eastbridge-website`, branch `main`. Live site: https://eastbridgestrategicpartners.com (Netlify deploys on every push to `main`). The .ae and www hosts must 301 to it — include one of them in the daily live check.

## Principles (non-negotiable)
1. Quality over volume. Google's spam policy treats "many pages generated without adding value" as scaled content abuse, and that now includes attempts to manipulate AI answers. We publish at most TWO new articles a week, each 1,400–2,200 words, each with a first-hand builder's-side insight, sourced figures and no invented statistics.
2. Every article follows src/content/WRITING_BRIEF.md (voice, compliance wording, format, facts, internal links).
3. Compliance: Eastbridge is not an engineering consultancy. tools/seo_audit.py must pass with 0 errors before anything is published.
4. Never claim a UAE project or existing Eastbridge clients, and never volunteer the point; present P Chapman Construction's record confidently. Articles are bylined to the founder, Philip Chapman, automatically. No client names. No awards.
5. Never fabricate reviews, testimonials, rankings or "as seen in" claims.

## Daily (every run)
1. Build and audit: `pip install --break-system-packages markdown pyyaml beautifulsoup4 && python3 build.py && python3 tools/i18n.py apply && python3 tools/seo_audit.py`. Fix any error. Netlify builds with Python 3.11, so before every push also run `python3.11 -m py_compile build.py tools/*.py src/*.py` (no 3.12-only syntax such as backslashes inside f-strings). After pushing, check the Netlify deploy published; if it failed, fix and push again the same day.
2. Live check (once the domain is live): fetch the home page, sitemap.xml, robots.txt, llms.txt, llms-full.txt, insights/feed.xml and three random pages; report anything not returning 200.
3. Visibility check: web-search 6 of the target queries below (rotate daily) and record whether the site appears in the top 10 and which competitor holds position 1. Append one line per query to reports/visibility.csv (date, query, our position or "-", top result domain).
4. Competitor watch: check the insights/blog pages of Tanmu PMS, DNA Project Management, Project Wizards, Bauhaus Project Management, DMDC, Luxedesign, Dar Al Naseeb, PRASOON, and realestateclubdubai.com (its blog and its /tools/ calculators; it ranks for several of our target searches, including villa build cost and villa snagging). For RECD, also note any new calculator or widget, but do not copy its directory, referral, app or investment features (see reports/competitor-brief-recd-2026-11-01.md, "Not recommended"). If any published a new article on a topic we don't cover, add it to the TOPICS backlog (not a copy — our own angle).
5. Freshness: if a cited figure in an existing article has a newer official source, update the article and its `updated:` date. Never change `date:`.

## Tuesday and Friday runs (publishing days)
6. Take the first unticked topic in src/content/TOPICS.md. Research it (official sources first: dm.gov.ae, buildindubai.gov.ae, dmt.gov.ae, tamm.abudhabi, master developer sites; then reputable industry sources). Write it to src/content/insights/<slug>.md per the brief. Tick the topic.
7. Add 2–3 internal links to the new article from the most relevant existing articles or service pages.
8. Translate (see Languages below), rebuild, audit (0 errors), commit with message "Insight: <title>", push. Netlify deploys automatically.
9. After deploy: `python3 tools/indexnow.py <new URL> <changed URLs>`.

## Languages (every run that changes any English text)
The site is published in English, Arabic (right to left), Russian, Simplified Chinese and Hindi, under /ar/, /ru/, /zh/ and /hi/.
English is the source. Translations are stored in src/i18n/<lang>.json, keyed by a hash of the English text.
1. `python3 build.py && python3 tools/i18n.py extract` — writes src/i18n/todo-<lang>.json with every new or changed segment.
2. Translate each todo file per src/i18n/TRANSLATION_BRIEF.md (same keys, HTML tags kept). Save the result as
   src/i18n/parts/<lang>-NN.json (copy the todo to src/i18n/parts/en-NN.json first so `python3 tools/i18n_check.py` can check it; fix until 0 problems). Delete src/i18n/parts after merging.
3. `python3 tools/i18n.py merge`, then rebuild and `python3 tools/i18n.py apply`. Untranslated text falls back to English, and the audit warns about it.
4. Ping IndexNow with the English and translated URLs of a new article.

## Monthly (first run of the month)
10. Review reports/visibility.csv trends; propose (don't make) changes to titles/descriptions of pages that are stuck on page 2.
11. Suggest 3 off-site actions (directory listings, a guest article, a trade-press story, a YouTube explainer script) — off-site citations matter as much as on-site content for AI answers. When a new profile goes live, add a company profile (e.g. the LinkedIn company page) to `SOCIAL` in `src/config.py` (Organization `sameAs`) and Philip's own profile to `FOUNDER["same_as"]` (Person `sameAs`).
12. Calculator rates: refresh the currency table in `src/pages_tools.py` — `FX_INPUTS` (AED 3.6725 per USD peg, as in the Central Bank of the UAE's monthly exchange-rate table, source `cbfx`; ECB euro reference rates for USD, GBP, CNY, INR from https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml; Bank of Russia AED rate from https://www.cbr.ru/eng/currency_base/daily/) and `FX_AS_AT` (the ECB date). Re-check the construction rates against their sources and set `RATES_REVIEWED` to the current month ("Rates last reviewed: <month year>, by Philip Chapman"); if a rate changes, update the worked example, FAQ and translations. Where a line is still cited only to Real Estate Club Dubai (landscaping, smart home, demolition, FF&E, the fixed approvals band, the phase timeline; `NOFOLLOW` sources in `src/pages_tools.py`), look for a primary or industry source and switch to it when one appears. Never call a live rate API from the site. Then run the Languages steps (the dates appear in translated text) and `node tools/calc_check.js --strict`.
    Owner tools (`src/pages_owner_tools.py`): refresh `RENT_ANNUAL` from https://www.engelvoelkers.com/ae/en/resources/villa-rental-prices (update the "May 2026" wording in the tool text and in the renovate-or-rebuild article if the date changes) and `BASE_RATE` from the Central Bank of the UAE's latest base-rate announcement (update its date in the delay cost estimator text and the `cbuae` source). The tools share the calculator's `RATES`, so a rate change there flows through; re-check the worked-example figures quoted in `/insights/renovate-or-rebuild-villa-dubai/`. Then `node tools/tools_check.js --strict`.

## Report to Phil (every run) — max 8 lines
- What was published or updated (with URLs)
- Visibility movements worth knowing
- Anything broken
- One recommended action for him (only if it needs him)

## Target queries (rotate 6 a day)
villa construction dubai · villa renovation dubai · luxury villa renovation dubai · owner's representative dubai · villa project management dubai · build a villa in dubai · cost of building a villa in dubai · villa construction cost per square foot dubai · palm jumeirah villa renovation · nakheel noc renovation · emirates hills villa construction · villa snagging dubai · how to choose a villa contractor dubai · construction claims consultants dubai · villa construction abu dhabi · hudayriyat plots build · dubai islands plot villa · building a villa in dubai from uk · villa contractor contract uae · how long to build a villa in dubai

Arabic pages use src/static/assets/site-rtl.css, generated from site.css. After any edit to site.css run `sh tools/make_rtl.sh` (needs Node) and commit both files.
