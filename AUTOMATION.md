# Eastbridge SEO engine — the playbook the scheduled task follows

## Principles (non-negotiable)
1. Quality over volume. Google's spam policy treats "many pages generated without adding value" as scaled content abuse, and that now includes attempts to manipulate AI answers. We publish at most TWO new articles a week, each 1,400–2,200 words, each with a first-hand builder's-side insight, sourced figures and no invented statistics.
2. Every article follows src/content/WRITING_BRIEF.md (voice, compliance wording, format, facts, internal links).
3. Compliance: Eastbridge is not an engineering consultancy. tools/seo_audit.py must pass with 0 errors before anything is published.
4. Never claim a UAE project or existing Eastbridge clients, and never volunteer the point; present P Chapman Construction's record confidently. Articles are bylined to the founder, Philip Chapman, automatically. No client names. No awards.
5. Never fabricate reviews, testimonials, rankings or "as seen in" claims.

## Daily (every run)
1. Build and audit: `pip install --break-system-packages markdown pyyaml beautifulsoup4 && python3 build.py && python3 tools/i18n.py apply && python3 tools/seo_audit.py`. Fix any error.
2. Live check (once the domain is live): fetch the home page, sitemap.xml, robots.txt, llms.txt, llms-full.txt, insights/feed.xml and three random pages; report anything not returning 200.
3. Visibility check: web-search 6 of the target queries below (rotate daily) and record whether the site appears in the top 10 and which competitor holds position 1. Append one line per query to reports/visibility.csv (date, query, our position or "-", top result domain).
4. Competitor watch: check the insights/blog pages of Tanmu PMS, DNA Project Management, Project Wizards, Bauhaus Project Management, DMDC, Luxedesign, Dar Al Naseeb, PRASOON. If any published a new article on a topic we don't cover, add it to the TOPICS backlog (not a copy — our own angle).
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
11. Suggest 3 off-site actions (directory listings, a guest article, a trade-press story, a YouTube explainer script) — off-site citations matter as much as on-site content for AI answers.

## Report to Phil (every run) — max 8 lines
- What was published or updated (with URLs)
- Visibility movements worth knowing
- Anything broken
- One recommended action for him (only if it needs him)

## Target queries (rotate 6 a day)
villa construction dubai · villa renovation dubai · luxury villa renovation dubai · owner's representative dubai · villa project management dubai · build a villa in dubai · cost of building a villa in dubai · villa construction cost per square foot dubai · palm jumeirah villa renovation · nakheel noc renovation · emirates hills villa construction · villa snagging dubai · how to choose a villa contractor dubai · construction claims consultants dubai · villa construction abu dhabi · hudayriyat plots build · dubai islands plot villa · building a villa in dubai from uk · villa contractor contract uae · how long to build a villa in dubai

Arabic pages use src/static/assets/site-rtl.css, generated from site.css. After any edit to site.css run `sh tools/make_rtl.sh` (needs Node) and commit both files.
