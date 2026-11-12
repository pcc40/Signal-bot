# Handoff — Eastbridge website

Static site for Eastbridge Strategic Partners (client-side villa project management, Dubai and Abu Dhabi).
English source, published in Arabic (/ar/, right to left), Russian (/ru/), Simplified Chinese (/zh/) and Hindi (/hi/).
The source lives in the GitHub repository `pcc40/eastbridge-website` (branch `main`). Live address: https://eastbridgestrategicpartners.com (contact: philip@eastbridgestrategicpartners.com); the .ae and www hosts, and the original Netlify hostname `incredible-haupia-7adc73.netlify.app`, 301 to it via `netlify.toml` (deploy previews and branch deploys use other hostnames and are not redirected).
A single handoff zip, `eastbridge-website-handoff.zip` (top folder `eastbridge/`), holds the full source including all image sizes. It is gitignored.

## UAE images and content round: integration (5 November 2026)
Brief: `reports/brief-uae-images-and-content-2026-11-05.md`. Branches merged: `eb7/images`, `eb7/perf`, `eb7/art1`, `eb7/art2`, `eb7/areas` (details in the sections below).
- **Image decision** (owner, 5 November 2026): developer marketing images and renders on the area pages, the `/areas/` hub, the Island E worked example, place-related articles, the renovation and plot due diligence services and the home slideshow, always with a visible credit and never captioned so as to suggest Eastbridge designed, built or managed what they show. UK photographs stay only where the subject is P Chapman Construction's work (see "UAE images" below). The services mega-menu feature for the Island E example now shows `uae-island-e-01` ("Image: Nakheel (Bay Estates, Island E). For illustration") instead of a UK house.
- **New cadence** (`AUTOMATION.md`): three articles a week, Tuesday, Thursday and Saturday (Dubai time), each 1,400–2,200 words, with at least one UAE library image matching its subject (`POST_IMG` or a `hero:` base) and at least one table or simple diagram; a Monday "deepen" job on one existing page (order: Palm Jumeirah, Emirates Hills, then the remaining area pages; Jumeirah Islands, Dubai Islands, Dubai Hills Estate and Arabian Ranches were deepened in this round); a new area page every second Monday from the "New area pages" section at the end of `TOPICS.md` (Tilal Al Ghaf, Jumeirah Golf Estates, DAMAC Hills, The Meadows and Springs, Al Furjan, Jumeirah Park), with developer images sourced at the time under the same rules. Principle 1 updated.
- **Backlog:** the brief's section 3.4 list now heads `TOPICS.md`; four of its articles are published and ticked (`how-to-choose-client-side-project-manager`, `defects-liability-period-uae`, `villa-renovation-timeline-dubai`, `how-to-plan-a-villa-renovation-dubai`), all mapped to UAE heroes in `POST_IMG`, and added (with `villa-renovation-mistakes-dubai`) to the `WRITING_BRIEF.md` internal links. Inbound links to them were added from the fees, owner's rep comparison, snagging, renovate-or-rebuild, renovation cost, renovation mistakes and Palm renovation articles and the snagging service page.
- `TRANSLATION_BRIEF.md`: "Developer and place names in credits stay in Latin script."
- **Still to do:** the Languages steps for all new and changed English text (new articles, deepened area pages, alt text and credits, related-reading strings, the new links); then IndexNow for the changed URLs in all five languages; then re-check Netlify Core Web Vitals and PageSpeed Insights. Screenshots of this round: `reports/screens/uae-*.png`.

## UAE images (November 2026, branch `eb7/images`)
Source: `reports/brief-uae-images-and-content-2026-11-05.md` (sections 1, 2 and the image checks in 4).

**Owner's decision (Phil, 5 November 2026).** As a Dubai broker with developer marketing access, Phil approved using the master developers' own marketing images and renders (Nakheel, Emaar, Meraas, Aldar, Modon, Meydan Sobha, Al Barari) on the area pages, the Island E worked example and related articles, and takes responsibility for that use. Rules:
- Every developer image carries a visible credit, exactly as in its folder's `manifest.json` ("Image: Nakheel", "Developer render: Nakheel and Meydan (District One West)"). Credits that are not a developer's (Crystal Lagoons; the Wikimedia Commons photo under CC BY 3.0, which must name the author and licence) print exactly as given.
- Never caption or place a developer image so that it suggests Eastbridge designed, built or managed what it shows. Area-page images read as illustrations of the community; strips with UAE images end with "For illustration. Eastbridge was not involved in the design or construction of what these images show."
- UK photographs stay, labelled as P Chapman Construction's work, where the subject is that work or Philip's record: `/work/`, `/about/`, `/approach/`, the Owers House case study, the "Built by our founder in the UK" strip on the home page, and the builder's-view articles (what the contractor knows, contracts, choosing a contractor, sourcing materials).
- No people's faces, no other agents' listing photos, no watermarks, no stock images to fill gaps.

**Library and tool.** Originals: `assets-src/uae-images/<folder>/` with a `manifest.json` per folder (never published: `build.py` copies only `src/static/`). `python3 tools/make_uae_images.py` (needs Pillow; not needed on Netlify) writes `uae-<folder>-NN-640/-1280/-1600.webp` (never upscaled; images under 1280 px wide, such as the 880 px Jumeirah Bay ones, get only the 640 size and are used in strips only), `-320.webp` for hero thumbnails, and a 1200 x 630 `-og.jpg` crop for each hero into `src/static/assets/img/`, and adds the entries to `src/img_manifest.json` under `uae-<folder>` (name, place, credit, alt from the `shows` line, role). The two general images keep descriptive bases: `uae-dubai-skyline-villas-01`, `uae-abu-dhabi-skyline-01`. To add a community: add its folder and manifest, add it to `NAMES` (and `NAME_HINTS`) in the tool, run it, commit the generated files.

**Where they are used.** Area pages: hero = the folder's hero image (og:image = its 1200 x 630 crop), strip and CTA band from its support images, service cards text-only. `/areas/` hub: a thumbnail and credit per community. Island E worked example: hero `uae-island-e-01`, a three-render strip under the introduction with the brief's caption; the "hypothetical worked example" label and the generated diagram social card are unchanged. Articles: `POST_IMG` in `src/pages.py` (mappings for articles not yet written are harmless); a `hero:` front-matter base overrides it; unmapped articles fall back to a general Dubai image. Home: the slideshow leads with Palm Jumeirah, Dubai Islands and Emirates Hills, then Quay House and Sea Glass House, each with its own caption; then the "Built by our founder in the UK" strip linking to `/work/`. Services: renovation (the Nakheel NOC service) and plot due diligence; the "From the builder's side" feature stays UK.

**Image SEO and performance.** `sitemap.xml` lists `<image:image>` for area, hub, article and Island E heroes (`tools/i18n.py apply` keeps them on every language URL). Article, area Service and service-page Service JSON-LD carry `image`. Only the first hero is preloaded; everything else is lazy. The home hero's first slide is about 100 KB at 1280 px. `tools/seo_audit.py` fails if an area page, the `/areas/` hub or the Island E page shows an image whose file name does not start with `uae-`.

## Page speed and article linking (November 2026, branch `eb7/perf`)
Netlify reported First Contentful Paint "needs improvement". Already in place before this round and unchanged: self-hosted Latin fonts with `font-display:swap` and three preloads, one versioned stylesheet, `defer` on `calc.js`/`tools.js`, width and height on every `<img>` (checked across all English pages), the hero LCP image preloaded, analytics loaded only after consent.

What changed:
- **Critical CSS.** Each page inlines the first-screen rules for its section (`<style id="critical-css">`, about 5–7 KB gzipped) and loads the full `site.css` without blocking the first paint (`rel=preload` switched to a stylesheet on load, `<noscript>` fallback). The cuts live in `src/critical.json` (per stylesheet: its md5 and one cut per group: home, insights, work, services, areas, tools, guides, other), generated by `node tools/make_critical.js` (Playwright; opens every page in all five languages at 390/820/1440 px and keeps, verbatim and in source order, each rule that matches something in the first 1.5 screens, plus the rules the site script toggles). `src/critical.py` serves them to `build.py` and `tools/i18n.py`. A cut is used only while its md5 matches the current `site.css` / `site-rtl.css`; otherwise pages fall back to the ordinary blocking stylesheet and `seo_audit.py` warns. **After any edit to site.css, or to the markup of a page's first screen:** `sh tools/make_rtl.sh`, `python3 build.py && python3 tools/i18n.py apply && node tools/make_critical.js`, build again, and commit `src/critical.json`. Checked: with `site.css` blocked, the first screen of 22 sample pages (every group, all languages, 390 and 1440 px) is pixel-identical to the fully styled page.
- **Translated pages** (`tools/i18n.py language_fonts()`): the Latin Instrument font preloads are removed (those pages set their own `--serif`/`--sans` and never used them); `fonts.googleapis.com` and `fonts.gstatic.com` are preconnected at the top of `<head>`; the Google Fonts stylesheet loads without blocking, and uses `display=optional` instead of `swap`, so a late web font no longer moves the page (the swap moved the cookie banner and the hero text). Trade-off: on a slow first visit a page may show the system font; the next page uses the cached web font. To go back to swap, change `FONTS` in `tools/i18n.py`.
- **Related reading** (`src/related.py`): every article now ends with three related articles, "Our service" and "Area guide" links, rendered from `TOPIC` (service and area per article slug; new articles fall back to their category, the first `/areas/` link in the body, or place names in the slug). The "Read next" cards show the next three in the same ranking, so each article links to six others. `seo_audit.py` fails if an article links to fewer than three articles, to no service or area page, or lacks the block. New English strings ("Related reading", "Our service:", "Area guide:" and the list items) need the Languages steps.
- Articles already used `updated:` for `dateModified` and the sitemap `lastmod`; unchanged.

Lab measurements (Playwright, 390 px, mobile, network 150 ms / 1.6 Mbps down, CPU 4x slower, local gzip server without TLS; median of 5 runs, ms). These are lab numbers, not field data: re-check Netlify's Core Web Vitals and PageSpeed Insights after deploy.

| Page | FCP before → after | LCP before → after | CLS before → after |
|---|---|---|---|
| `/` | 1028 → 492 | 1028 → 972 | 0 → 0 |
| `/areas/palm-jumeirah/` | 1024 → 508 | 1476 → 1476 | 0 → 0 |
| `/insights/villa-construction-cost-dubai/` | 1072 → 560 | 1072 → 1128 | 0 → 0 |
| `/ru/insights/villa-construction-cost-dubai/` | 1200 → 352 | 1208 → 896 | 0.028 → 0 |
| `/ar/` | 1276 → 388 | 1920 → 1456 | 0.261 → 0 |
| `/zh/areas/palm-jumeirah/` | 2548 → 392 | 2548 → 1692 | 0.073 → 0 |
| `/hi/` | 1260 → 400 | 1928 → 1328 | 0.004 → 0 |

LCP on English pages is held by the hero image (about 55–135 KB at 1280 px on a 3x phone), which now shares the connection with the full stylesheet; the article LCP is about 50 ms slower in the lab. Lighter hero files would help most there (outside this round: the image work is on another branch).

Known, not changed: running `python3 tools/i18n.py apply` twice without `python3 build.py` in between hangs (seen with the code before this round too; cause not investigated); always build first.

## Conversion measurement, attribution and cookie consent (November 2026, branch `eb6/tracking`)
Source: `reports/live-audit-2026-11-01.txt`, "Fix and verify conversion measurement" and "Review the actual consent implementation". This is the site side only; the GA4 account steps below are Phil's.

**Events (GA4 `G-120XT9N6XB`).** No event fires in a form's submit handler any more (the old `generate_lead` is gone from `build.py` and `calc.js`). Success events fire on the thank-you pages, which Netlify shows only after it has accepted the POST. The submit handler leaves a flag in sessionStorage (`eb_pending_<form-name>`) and the thank-you page removes it, so each event fires once per submission: a reload, a revisit or a direct visit to a thank-you page sends nothing. Marker: `build.conversion_marker()`; logic: `build.SCRIPT`.

| Event | Where it fires | Parameters |
|---|---|---|
| `enquiry_success` | `/contact/thanks/` after the contact form (`brief`) | `form=brief` |
| `estimate_request_success` | `/tools/villa-build-cost-calculator/thanks/` after "Send this estimate" (`estimate`) | `form=estimate` |
| `checklist_request_success` | `/guides/villa-owner-checklist/thanks/` and `/guides/villa-snagging-checklist/thanks/` (`checklist`) | `form=checklist`, `guide=villa-owner-checklist` or `villa-snagging-checklist` |
| `newsletter_signup` | `/contact/thanks/#notes` after the footer notes form (`notes`) | `form=notes` |
| `contact` | click on a WhatsApp link or a phone number (secondary interaction, not a conversion) | `method=whatsapp` or `phone` |

The same events fire on the translated pages (`/ar/`, `/ru/`, `/zh/`, `/hi/`).

**GA4 Admin (Phil, once this is deployed):**
1. Admin → Events (Data display → Events): the old key event `generate_lead` will stop arriving. Unmark it as a key event, and do not import it into Google Ads.
2. Mark **`enquiry_success`** as the single primary key event (conversion). `estimate_request_success` may be marked as a secondary key event; if both are imported into Google Ads, set only `enquiry_success` as Primary there. Leave `checklist_request_success`, `newsletter_signup` and `contact` as ordinary events.
3. Use one conversion source per action: if a Google Ads tag is ever added, do not also import the same GA4 event.
4. Verify with an explicitly labelled test enquiry (with analytics accepted): one enquiry should produce one `enquiry_success` in DebugView/Realtime, one Netlify submission, one email and one sheet row.

**Campaign attribution.** With analytics accepted, `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content` and `gclid` from the landing URL are kept in sessionStorage (`eb_attr`, last tagged landing wins) and copied into hidden fields of the same names on the `brief`, `estimate` and both `checklist` forms (`form[data-attr]`, `build.ATTRIBUTION_FIELDS`). `submission-created.js` cleans them and writes them to the Google Sheet row and the lead alert, never to a customer email. Add six columns with those names to the sheet if the Apps Script maps columns by name. Netlify registers the new hidden fields on the first deploy that contains them. Tested by `node tools/test_submission_function.js`.

**Cookie consent (Google Consent Mode v2, basic implementation).** `build.analytics()` pushes `consent default` with `analytics_storage`, `ad_storage`, `ad_user_data` and `ad_personalization` all denied before anything else. gtag.js is not loaded, and no `config` or event is queued, until the visitor chooses "Accept analytics"; then `consent update analytics_storage: granted` is pushed, followed by `config` and the gtag.js request. The three ad signals stay denied (the site has no advertising tags). The choice is stored in localStorage `eb_consent` (`granted`/`denied`). The banner (`build.consent_banner()`, styles under "Cookie choice" in `site.css`) is static HTML so it translates; it sits at the bottom of the screen, does not block the page, has "Accept analytics", "Decline" and a privacy notice link, moves above the mobile action bar, and respects reduced motion and right-to-left. "Cookie settings" at the foot of every page (`build.cookie_settings_link()`) reopens it; Escape closes it when reopened. Declining after accepting switches consent back to denied, stops events, removes the `_ga` cookies and clears the stored campaign details. The privacy notice (`/privacy/`, "What we collect" and "Cookies") describes the banner and says analytics runs only after consent. Consent Mode passes the choice to Google; whether this banner meets UK/EEA requirements for a given campaign is a legal review point, not settled here.

**Translations.** The banner, the Cookie settings button and the two changed privacy paragraphs are new English text: run the Languages steps in `AUTOMATION.md`. Until then they show in English on translated pages (`seo_audit.py` warns, 0 errors).

## Top-10 competitor brief (November 2026): at a glance
Source: `reports/competitor-brief-top10-2026-11-01.md` with Phil's decisions at its end (D1 ranges confirmed; D2 quote review paid, within the Review range; D5 no insurance statement; D7 no new promises). Integrated from branches `eb4/art-fees`, `eb4/art-db`, `eb4/art-authority`, `eb4/art-sourcing`, `eb4/areas-a`, `eb4/areas-b`, `eb4/sources`, `eb4/safeguards`, `eb5/fees`, `eb5/position` and `eb5/services`. The new and changed English text still needs the Languages steps in `AUTOMATION.md`; until then translated pages fall back to English and `seo_audit.py` warns (0 errors).

New and reworked pages (English URLs; each also exists under /ar/, /ru/, /zh/ and /hi/):
- `/fees/` reworked (1.1, 1.2, 1.6): the written-scope-of-works principle, three published ranges by level of input from `FEES` / `fee_text()` in `src/config.py` (Review AED 9,500–15,000 per review; Part service a monthly fee agreed in the written scope, with no published minimum (owner, 1 Nov 2026); Full service typically 1.75–3% of build cost), what moves a fee within its range, limits of authority (`#limits`), the contractor quote review (`#quote-review`), an illustration worked out at build time from the calculator's worked example, "Is it worth it?" and money FAQs (`MONEY_FAQS`, also on `/faq/` and `/independence/`, with FAQPage markup). No day rate, hourly rate, fixed price or snagging-only fee anywhere. The old keys (`plot_review`, `rescue_review`, `monthly_from`, `percent_band`) are gone: use `C.fee_text('review' | 'part' | 'full')`. Title shortened to 60 characters or fewer, with the claims service title, so `LONG_TITLE_PENDING` in `tools/seo_audit.py` is now empty and a long title is an error everywhere.
- `/services/materials-and-specialist-sourcing/` (2.0): sourcing trips with the owner, samples, lead times, shipping and customs timing, delivery checks, no supplier commissions. See the positioning section below.
- `/services/consultant-and-contractor-selection/#quote-review` (2.1): contractor quote review, priced within the Review range; linked from `/fees/` and `/insights/how-to-choose-a-villa-contractor-dubai/`.
- Every service page (2.2, 2.3, 2.4): a "You receive" document list (`DELIVERABLES` in `src/content/services.py`, with an "Illustrative" specimen on cost and programme control, `SPECIMENS`), "A month on your project" on owners-representative (`MONTH_ON_PROJECT`), an "Ask about this service" block linking to `/contact/?service=<slug>#brief`, and a per-page WhatsApp message (`WA_TOPIC`, `build.WA_TPL_SERVICE` / `WA_TPL_AREA`; area pages get `?area=<slug>`). Snagging and handover is one stage of the full service, with the handover FAQs from 2.3.
- Four new insights (ticked in `TOPICS.md`, added to the `WRITING_BRIEF.md` internal links): `/insights/client-side-project-manager-fees-dubai/`, `/insights/design-build-vs-separate-architect-villa/`, `/insights/which-dubai-authority-covers-my-villa/` (its table is mirrored in `llms-full.txt` from `src/content/authorities.py`; edit both together) and `/insights/sourcing-materials-abroad-dubai-villa/`.
- Two new area pages (4.2): `/areas/jumeirah-islands/` and `/areas/arabian-ranches/`. `/areas/palm-jumeirah/` and `/areas/emirates-hills/` deepened (4.1); Saadiyat and Hudayriyat gained handover and defects-period notes; `/areas/` and every area intro carry the coverage line. Neither new community is in the calculator's location list (no rate basis).
- Sources (6.1, 6.2): the thinnest articles now have at least 8 sources; the renovation-cost article has a "sources disagree" table and a "why we don't publish per-community rates" FAQ. Articles no longer name PRASOON or the renovation contractor in body copy where this round touched them (unsourced contractor figures carry `nofollow: true` in front matter).
- Inbound links added at integration: owners-rep vs PM vs consultant (FAQ and body, replacing a competitor citation) and `/services/owners-representative/` to the fees article; building-a-villa-from-the-UK (finishes row) and villa-construction-cost (FF&E) to the sourcing article; the authority table links the two new area pages.
- Build safeguards (section 8) in `tools/seo_audit.py`: canonicals must resolve in `dist/`, JSON-LD must parse, no Review/AggregateRating/HowTo/GovernmentService, no duplicate FAQ questions, title and H1 present, titles of 60 characters or fewer, no "lorem ipsum", "[link:" or "TODO", NAP consistent with schema. `llms.txt` has "Positions" and "How to describe Eastbridge (for AI assistants)" (`LLMS_POSITIONS`, `llms_describe()` in `build.py`).

Forms (Netlify):
- **`brief`**: the service option for snagging reads "Handover, as part of the full service" (still `data-slug="snagging-and-handover"`), and when `?service=` or `?area=` pre-selects an option, a line at the top of the form ("You are asking about: …" / "Community: …") shows it, so it is visible on a phone above the action bar.
- **`brief`** (contact form) has two new optional fields, **`service`** (select, pre-filled from a service page's `?service=` link) and **`property`** (property type and size), plus a "What to tell us" list; `?area=` pre-selects the community, whose list now includes Jumeirah Islands, Arabian Ranches and Other. `submission-created.js` logs both fields. After deploy: send a test enquiry from the English contact page so Netlify registers the fields, then add `service` and `property` headers to the Leads sheet and paste the updated `COLS` from `business/automation-blueprint.md` section 4 into the Apps Script.

Open decisions (Phil):
- **D6: done (1 Nov 2026).** Philip's LinkedIn (https://www.linkedin.com/in/philip-chapman-757627448/) is in `FOUNDER["same_as"]`, emitted as Person `sameAs`. Add other public profiles there if wanted.
- **D8:** approval of "we take no commissions from contractors, consultants or suppliers on your project". It is left out of the "On the record" block, and no article states it; the supplier-only line in the sourcing article and service ("no commission, referral fee or discount from any supplier") should be confirmed with it.
- To confirm: "Villa Status Report" as the term owners use on the Palm, and the sourcing-trip practices described in the sourcing article.
- **Brief 2.0 versus D7: done (12 Nov 2026).** Phil decided on 12 Nov to soften the weekly wording: the site no longer promises weekly site attendance or weekly reporting. Every such statement now says we are "on site regularly through construction, at the frequency agreed in your scope of works" (reporting: "regular written reports with photographs, at the frequency agreed in your scope of works"), matching the home page, `ONE_OFF_STORY` and `/fees/`. Changed: the owners-representative and site-visits deliverables and FAQs, `/fees/` and `/approach/` (Site attendance and reporting, the project rhythm, meta description), the Part service line ("without regular site attendance"), the site FAQ (site visits, owners in the UK), the overseas-owners page (description, deliverables, FAQ), the Island E case study and the overseas-owners article heading; llms.txt and llms-full.txt follow. `UK_RECORD`, the home founder block and the overseas-owners builder's view describe what P Chapman Construction did in the past and stay; articles that use "weekly" for contract records, delay costs or the reader's own checks are not promises and stay. Do not add new weekly-visit or weekly-report promises.

Not done yet (next steps):
- **5:** second lead magnet, the specimen owner progress report (`/guides/weekly-villa-report-template/`, do not promise weekly reporting in it, backlog item `remote-villa-reporting-template`) and the optional quote comparison worksheet.
- **3.5–3.12:** the remaining articles, now at the top of `src/content/TOPICS.md` in the brief's order (3.3 renovate-or-rebuild was already published), followed by the three moved-up topics and the new lower-priority list. 3.8's defect-severity scheme and 3.12's Palm owner briefing are noted there as edits to existing articles.
- **4.3:** area pages for Jumeirah Golf Estates, Tilal Al Ghaf, The Meadows, DAMAC Hills and Al Furjan; then deepen the other eight area pages to about 1,500 words (4.1).
- **9 (off-site):** earned media, editorial links, Google Business Profile verification, and re-fetching ovrexglobal.com for `business/seo-competitor-report.md` (it returned 503 on 1 Nov 2026). The off-site copy in `business/first-client-plan.md`, `business/offsite-authority-kit.md` (Google Business Profile services, which may still describe snagging as a service in its own right) and `business/outreach-kit.md` still quotes the old fixed fees.
- Competitor names: the renovation contractor and PRASOON are no longer named in any rendered copy (calculator, renovate-or-rebuild and delay cost tools, glossary, renovation service FAQ, renovate-or-rebuild and construction-cost articles). The contractor's guide is cited as "a Dubai renovation contractor's guide" beside Property Finder, with `nofollow` (its host and `prasoon.design` are in `build.NOFOLLOW_HOSTS`); the Currie & Brown 3% forecast cites TradeArabia; the glossary cites Turner & Townsend directly. The calculator FAQ has "Why doesn't the calculator change the rate by community?". Real Estate Club Dubai is still named in some source titles (nofollow, "property information website").
- Glossary freshness: the decennial-liability entry should mention Federal Decree-Law No. 25 of 2025 (arts 821–824).
- Translations for everything above (Languages steps), then IndexNow for the new and changed URLs. Until then `tools/i18n.py apply` marks each untranslated segment `lang="en"` (and `dir="ltr"` on /ar/), and the per-page WhatsApp message falls back to the English topic while its template is untranslated. The review fixes of 1 November (Review fixes for top-10 brief) added or changed English strings too: re-run `extract`.

## Competitor-brief round (November 2026): at a glance
Source: `reports/competitor-brief-recd-2026-11-01.md` (review of Real Estate Club Dubai). Details per branch are in the sections below. The new English text still needs the Languages steps in `AUTOMATION.md`; until then the translated pages fall back to English and `seo_audit.py` warns (0 errors).

New pages (English URLs; each also exists under /ar/, /ru/, /zh/ and /hi/):
- `/tools/renovate-or-rebuild/`, `/tools/stage-payment-planner/`, `/tools/delay-cost-estimator/` — owner tools (`src/pages_owner_tools.py`, `src/static/assets/tools.js`), linked from `/tools/`, the footer and `llms.txt`
- `/insights/renovate-or-rebuild-villa-dubai/` — article published with the renovate-or-rebuild tool
- `/tools/villa-build-cost-calculator/embed/` — calculator-only page for other sites' iframes (noindex, canonical to the calculator, not in the sitemap, framing allowed only here via `dist/_headers`)
- `/tools/villa-build-cost-calculator/thanks/` — thank-you page for the "Send this estimate to Philip" form (noindex)
- `/guides/villa-snagging-checklist/` and `/guides/villa-snagging-checklist/thanks/` — second lead magnet, The Villa Snagging Checklist PDF (thanks is noindex)

Forms (Netlify):
- New form **`estimate`** (calculator page): name, email, optional phone, plot location, notes; hidden `estimate_inputs`, `estimate_result`, `estimate_link`, `currency`; honeypot `company_site`; optional `marketing_opt_in`. Handled in `netlify/functions/submission-created.js` (sheet row "Estimate request", lead alert, acknowledgement without the figures).
- Existing form **`checklist`** now carries a hidden **`guide`** field (`villa-owner-checklist` or `villa-snagging-checklist`); both lead magnets post to it.
- Google Sheet: the Apps Script `COLS` in `business/automation-blueprint.md` section 4 now ends with `guide`, `estimate_inputs`, `estimate_result`, `estimate_link`, `currency`. Paste the updated script and add those five headers to the Leads sheet, or those values reach only Netlify Forms and the function log.
- After deploy: send a test from `/tools/villa-build-cost-calculator/` (estimate form) and from `/guides/villa-snagging-checklist/` (check the `guide` value is stored), and confirm `estimate` appears under Netlify → Forms.

Monthly upkeep (`AUTOMATION.md`, Monthly, step 12): refresh the currency table `FX_INPUTS` and its date `FX_AS_AT` in `src/pages_tools.py` (USD peg, ECB reference rates, Bank of Russia), set `RATES_REVIEWED` ("Rates last reviewed: <month year>, by Philip Chapman") after re-checking the construction rates, refresh `RENT_ANNUAL` and `BASE_RATE` in `src/pages_owner_tools.py`, then run the Languages steps, `node tools/calc_check.js --strict` and `node tools/tools_check.js --strict`.

Embed code: the iframe snippet is generated by `embed_code()` / `embed_box_html()` in `src/pages_tools.py` (height `EMBED_HEIGHT`, path `EMBED_PATH`) and shown in the "Add this calculator to your website" box (`#embed`) on `/tools/villa-build-cost-calculator/`; `calc.js` points it at the embed page in the language being viewed. Partners are offered it in `business/outreach-kit.md`.

Competitor watch: `realestateclubdubai.com` (blog and tools) is now in `AUTOMATION.md` Daily step 4.

## Positioning, credentials and coverage (November 2026, branch `eb5/position`)
From `reports/competitor-brief-top10-2026-11-01.md`, items 2.0, 1.4, 1.7, 7 (About) and Phil's coverage direction:
- **One-off villa story** (2.0): `ONE_OFF_STORY` and `UK_RECORD` in `src/content/services.py`, used on home (hero lede and founder block), `/about/#one-off`, `/approach/#one-off` and `/services/owners-representative/`.
- **New page `/services/materials-and-specialist-sourcing/`** (and `/ar/`, `/ru/`, `/zh/`, `/hi/`): sourcing trips, samples, lead times, shipping and customs timing, delivery checks, no supplier commissions. In the Services menu, the services hub, the sitemap, `llms.txt` and `llms-full.txt`. Its link to `/insights/sourcing-materials-abroad-dubai-villa/` appears automatically once that article is merged (`build.insight_link()` only links published articles); the same applies to `/insights/design-build-vs-separate-architect-villa/` from the comparison block.
- **"On the record"** (1.4): `build.on_record_items()` feeds the site-wide footer block (`.on-record` in `site.css`) and `/about/#on-the-record`; Organization schema carries `identifier` (PropertyValue, Meydan Free Zone licence 2540153.01) and `areaServed` (Dubai, Abu Dhabi, United Arab Emirates, also on every Service). No insurance statement (D5) and no D8 sentence.
- **Alongside a design-and-build contractor** (1.7): `pages.alongside_html()` with the four-column comparison table, on `/independence/` and `/services/owners-representative/` (service flag `"alongside": True`).
- **About** (7): career timeline (only dated facts already on the site), "Who you'll deal with", and the policy line "We never publish a client's name, address or photographs without written consent."
- **Coverage**: `C.COVERAGE` in `src/config.py` on home, `/about/`, `/services/owners-representative/`, `/services/overseas-owners/`, `/contact/`, the FAQ ("Which areas do you cover?"), `llms.txt` and `llms-full.txt`. `/areas/` and the area-page intros carry it too (merged from `eb4/areas-a`).
- **Open decisions** (Phil): D8 (the wording "no commissions from contractors, consultants or suppliers on your project") is still open; the credentials block uses the existing "paid only by the owner we represent" wording. The founding year of P Chapman Construction and the date of the Eastbridge licence are not recorded, so the timeline shows neither; add them in `pages.about()` once Phil confirms.
- The new English text still needs the Languages steps in `AUTOMATION.md`.

## Calculator: currency, share, save and send (November 2026, branch `eb3/calc`)
From the competitor brief (`reports/competitor-brief-recd-2026-11-01.md`, items 1, 2 and 8):
- **Currency display.** "Show amounts in" selector: AED (default everywhere), GBP, USD and EUR on every language; RUB only on /ru/, CNY only on /zh/, INR only on /hi/. AED stays the only calculation currency; other currencies are display-only conversions labelled "approximate, at rates of <date>". Each converted line is rounded like the AED lines, so converted columns still add up. Fixed rates live in `FX` / `FX_INPUTS` / `FX_AS_AT` in `src/pages_tools.py` (no live API calls): US dollar from the AED 3.6725 peg, GBP/EUR/CNY/INR crossed from the ECB euro reference rates, RUB from the Bank of Russia official rate. Sources are listed on the page (the dirham peg, ECB and Bank of Russia entries) and in the methodology.
- **Shareable link.** Inputs are mirrored to the query string (`history.replaceState`) and read on load; "Copy link" button.
- **Save as PDF.** `window.print()` with a dedicated print stylesheet (`@media print` block under "Currency, review line, share/save/send" in `site.css`): letterhead, inputs, line-by-line result (lines not included are left out), timeline, date, sources note, Eastbridge contact line and the link to reopen the estimate. One A4 page in all five languages, even with every extra selected.
- **WhatsApp with the estimate.** "Discuss on WhatsApp" is pre-filled with a one-line summary (messages `wa-*` in `#calc-msgs`, translated like every calculator message).
- **"Send this estimate to Philip".** New Netlify form **`estimate`** on the calculator page (name, email, optional phone, plot location and notes; hidden `estimate_inputs`, `estimate_result`, `estimate_link`, `currency`; `company_site` honeypot; optional unticked `marketing_opt_in`; "We never pass your details to contractors or suppliers."). Thanks page `/tools/villa-build-cost-calculator/thanks/` (noindex). Registered in `netlify/functions/submission-created.js`: logged to the sheet (status "Estimate request"), lead alert, and an acknowledgement that never repeats the submitted figures. After deploy, check the `estimate` form appears under Netlify → Forms and send a test from the English and one translated page.
- **Trust line.** "Rates last reviewed: <month year>, by Philip Chapman" under the result, from `RATES_REVIEWED` in `src/pages_tools.py`.
- **Privacy notice** lists calculator estimates.
- Checks: `node tools/calc_check.js --strict` now also covers currency switching, the URL round trip, Copy link, the WhatsApp text, the hidden form fields and the one-page PDF; `node tools/test_submission_function.js` covers the `estimate` form.
- **Monthly upkeep:** refresh `FX_INPUTS` and `FX_AS_AT`, and `RATES_REVIEWED` once the construction rates are re-checked (AUTOMATION.md, Monthly, step 12). The dates appear in translated text, so run the Languages steps afterwards.

## Calculator: primary sources and embeddable version (November 2026, branch `eb3/calc-2`)
From the competitor brief, items 5 and 6:
- **Sources.** Real Estate Club Dubai (a competitor) is no longer the main citation. The calculator now cites Optimal Engineering (all four construction tiers, design fees 6–12%, contingency, pool, approvals itemised), Engel & Völkers (contingency, 12–24 months from approval to completion, interiors), Turner & Townsend (Q1 2024 UAE detached-villa rates per m²; 2025 inflation forecast), Knight Frank and PwC (VAT 5%). No calculator figure changed, so the worked example (AED 6,239,000 likely) is unchanged. Real Estate Club Dubai stays cited, attributed as "a property information website" and linked with `rel="nofollow"` (`NOFOLLOW` in `src/pages_tools.py`), only for the lines no industry source covers: landscaping, smart home, demolition, FF&E 30–40%, the fixed AED 25,000–75,000 approvals band and the phase-by-phase timeline. The AECOM Middle East Property & Construction Handbook and Arcadis International Construction Costs are behind download forms and publish no villa rate we could verify, so they are not cited. The `WRITING_BRIEF.md` facts list and the glossary (contingency) were updated the same way. Several insight articles still cite Real Estate Club Dubai for those same figures; replace them as each article is next refreshed.
- **Embed page** `/tools/villa-build-cost-calculator/embed/` (and `/ar/`, `/ru/`, `/zh/`, `/hi/`): calculator only, compact two-column layout from 720 px, "Calculator by Eastbridge Strategic Partners" link, no header, footer, action bar or Google Analytics (`B.page(..., bare=True)`), `noindex`, canonical to the full calculator in the same language (`tools/i18n.py` now keeps a page's own canonical target), left out of the sitemap, every link opens in a new tab, and "Open this estimate in the full calculator" carries the inputs. `tools/seo_audit.py` treats it like a thank-you page and fails the build if an embed page loses `noindex`, its canonical, gains the site header or footer, has a link without `target="_blank"`, or appears in the sitemap.
- **Embed code box** on the full calculator (`#embed`, "Add this calculator to your website"): a read-only iframe snippet (never translated; `calc.js` points it at the embed page in the language being viewed), "Copy code" and a preview link. The snippet is an iframe only, with no extra link, so it cannot be read as a paid or widget link scheme. Default height `EMBED_HEIGHT` (1600 px, enough for the two-column layout at about 1,000 px wide; narrower hosts scroll inside the frame). Offered to partners in `business/outreach-kit.md`.
- **Framing headers.** `X-Frame-Options: SAMEORIGIN` used to be set on `/*` in `netlify.toml`. Netlify does not document which value wins when two matching rules set the same header (its docs only say repeated names are concatenated, and a combined `frame-ancestors` would leave the strictest policy in force), so an override for the embed path could not be relied on. The `/*` rule no longer sets it; `build.py write_headers()` generates `dist/_headers` with `X-Frame-Options: SAMEORIGIN` and `Content-Security-Policy: frame-ancestors 'self'` for every page in every language except the embed pages (a wildcard per site section, exact paths in `/tools/`), and `Content-Security-Policy: frame-ancestors *` with no `X-Frame-Options` for `/tools/villa-build-cost-calculator/embed/*`. After deploy check: `curl -sI https://eastbridgestrategicpartners.com/tools/villa-build-cost-calculator/embed/ | grep -i frame` shows only `frame-ancestors *`, and the same on `/tools/villa-build-cost-calculator/` shows `SAMEORIGIN` and `frame-ancestors 'self'`. A new top-level section is covered automatically at build time.

## Owner tools: renovate or rebuild, stage payments, delay cost (November 2026, branch `eb3/calc-3`)
From the competitor brief, item 7. Three new pages (and `/ar/`, `/ru/`, `/zh/`, `/hi/` copies), built by `src/pages_owner_tools.py` (called from `pages_tools.build_tools()`), with one shared script `src/static/assets/tools.js` (the cost calculator keeps `calc.js`):
- `/tools/renovate-or-rebuild/` — renovation against knock-down-and-rebuild: low/likely/high totals, cost per sq ft (or m²) of finished space, time, months out of the house, approvals. Reuses the calculator's `RATES` (new-build tiers, design 6–12%, contingency, approvals band, demolition, phase timeline) plus Smart Renovation's per-sq-ft renovation rates (`RENO_RATES`; luxury is "AED 450 or more", so it shows starting figures only) and Engel & Völkers' May 2026 average Dubai villa rents (`RENT_ANNUAL`). Published with the insight `/insights/renovate-or-rebuild-villa-dubai/` (ticked in `TOPICS.md`); both link to each other.
- `/tools/stage-payment-planner/` — contract sum spread over the build period (even, S-curve or peaked), advance (default 10%; Al Tamimi: 10–20% is industry practice), retention (default 10%, half at handover and half after the defects period; DLA Piper), month-by-month table and SVG chart; every column reconciles to the contract sum. Labelled typical and contract-dependent, not legal advice.
- `/tools/delay-cost-estimator/` — monthly cost of delay: rent or hotel (E&V average), interest (default the CBUAE base rate, 3.9% from 17 Sep 2026, labelled a floor), escalation on the work still to build (Currie & Brown 3% to Turner & Townsend 4% Dubai / 5% Abu Dhabi), the contractor's extended site costs (off by default; T&T preliminaries 12% Dubai / 15% Abu Dhabi over 8–14 months), and user-entered fees. Links to `/insights/stalled-villa-project-dubai/`.
- Each page: sourced rates (numbered per page), FAQ, WebApplication + FAQPage + BreadcrumbList schema, "Save as PDF" (print block under "Owner tools" in `site.css`; one A4 page, two for the payment schedule), WhatsApp and contact buttons. Linked from `/tools/`, the footer and `llms.txt`.
- Translation: every word `tools.js` writes is in the hidden `#tool-msgs` list (placeholders in braces must be kept). The new English segments still need the Languages steps.
- Check: `node tools/tools_check.js [--strict]` (server render equals the script's first render, totals reconcile in every scenario, unit switch, print, missing messages, translated-message leaks).
- Monthly upkeep (AUTOMATION.md step 12): `RENT_ANNUAL` and `BASE_RATE` in `src/pages_owner_tools.py`.

## Snagging lead magnet (November 2026)
- `/guides/villa-snagging-checklist/` and `/guides/villa-snagging-checklist/thanks/` (thanks is noindex): second lead magnet, The Villa Snagging Checklist PDF, 13 pages (`src/pages_guides.py`; PDF and cover built by `python3 tools/make_snagging_pdf.py`, which reuses the design system in `tools/make_checklist_pdf.py`). Commit the regenerated PDF and `-cover.webp`.
- Both guides post to the same Netlify form, `checklist`, with identical fields; the hidden field `guide` (`villa-owner-checklist` or `villa-snagging-checklist`) tells them apart. `submission-created.js` writes `guide` to the sheet row and the log line; add a `guide` column header to the Leads sheet and the updated `COLS` from `business/automation-blueprint.md` section 4 to the Apps Script.
- Linked from `/insights/villa-snagging-checklist-dubai/` (body and end CTA: Handover-category articles show the snagging CTA), the snagging service page, `/tools/`, the footer and `llms.txt`.
- The defects-liability periods in the PDF (`LIABILITY`) and in the article must stay in step: Civil Transactions Law 1985 arts 880–883 (new law, Federal Decree-Law No. 25 of 2025, arts 821–824, for contracts from 1 June 2026) and Dubai Law No. 6 of 2019 art. 40.

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
5. **Netlify** — done 31 Oct 2026: linked to `pcc40/eastbridge-website` (auto-publish from `main`, deploys from non-team Git contributors auto-approved), form detection on, `brief`, `checklist` and `notes` forms active (the new `estimate` form appears after the first deploy that contains it; check it there), submission emails to philip@eastbridgestrategicpartners.com.
6. **Netlify environment variables** for `submission-created` (Project configuration → Environment variables). Without the first two, forms still work but no emails are sent:
   - `EMAIL_API_KEY` — Resend API key (or Postmark server token) — required for email
   - `EMAIL_FROM` — e.g. `Eastbridge Strategic Partners <philip@eastbridgestrategicpartners.com>`; the domain must be verified with the email provider (DNS records) — required for email
   - `EMAIL_PROVIDER` — `resend` (default) or `postmark`
   - `EMAIL_REPLY_TO`, `LEAD_ALERT_TO`, `BOOKING_URL`, `SHEET_WEBHOOK_URL`, `SHEET_WEBHOOK_TOKEN`, `AUTOREPLY_DISABLED`, `SITE_PUBLIC_URL` — optional; see the header of the function file and `business/automation-blueprint.md` section 3
   - After setting them, send a test enquiry from `/contact/` and from `/guides/villa-owner-checklist/`.
7. **Google Business Profile** — set up, not yet verified (1 Nov 2026). The existing unverified profile was used (no duplicate): service-area business, address hidden, category Property Consultant (Real estate consultant), service areas Dubai and Abu Dhabi, website corrected from dealdeed.ae to this site, description, Mon–Fri 9–6 hours and all 13 services with descriptions from `business/offsite-authority-kit.md`. Still to do: choose the verification route (read section 1.1 first), add the logo and photos per 1.7, then Bing Places and the LinkedIn company page. Add each company profile URL (LinkedIn company page, Bing Places, etc.) to `SOCIAL` in `src/config.py`; this feeds the Organization schema's `sameAs`. Add Philip's own LinkedIn profile URL to `FOUNDER["same_as"]` in the same file; this feeds his Person schema's `sameAs` (it is empty until then).
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
- `src/static/assets/site.css` and generated `site-rtl.css` (run `sh tools/make_rtl.sh` after editing site.css, then `python3 build.py && python3 tools/i18n.py apply && node tools/make_critical.js` and build again; see "Page speed"); `src/critical.json` (generated first-screen CSS)
- `AUTOMATION.md` — the daily SEO engine playbook; `tools/indexnow.py` — pings search engines
- `src/pages_tools.py`, `src/pages_glossary.py`, `src/pages_guides.py` — calculator, glossary and lead-magnet templates
- `src/pages_owner_tools.py` and `src/static/assets/tools.js` — the three owner tools; `node tools/tools_check.js` and `node tools/calc_check.js` check the tools and the calculator
- `tools/make_checklist_pdf.py`, `tools/make_snagging_pdf.py` — build the two lead-magnet PDFs and their cover images
- `netlify/functions/submission-created.js` — form auto-acknowledgement and lead log (forms `brief`, `checklist`, `notes`, `estimate`)
- `tools/i18n_check.py` — checks translation chunks (placeholders, tags, numbers) before merging
- `business/` — business plans and kits (see above)

## Rules that must not be broken
- Eastbridge is a client-side project manager / owner's representative. Never an engineer, architect, contractor or design consultant.
- Never claim or imply UAE projects or existing Eastbridge clients. The Island E case study is illustrative and must stay labelled so.
- No client names. All project photos are P Chapman Construction's (UK) and Phil holds the rights. UAE images are the master developers' (and the other credited sources') and carry a visible credit; see "UAE images" above.

## Home hero film (`HERO_VIDEO` in `src/config.py`)
- Default `False`: the hero shows the photo slideshow only. The Vimeo film (`HERO_VIDEO_VIMEO_ID`, 219974514) currently returns 401 because its privacy setting does not allow embedding on our domain, which used to leave a loading spinner over the hero.
- To enable: in Vimeo, open the video, Settings > Privacy > "Where can this be embedded?" > Specific domains, add `eastbridgestrategicpartners.com` (and the Netlify preview domain if wanted). Then set `HERO_VIDEO = True`, rebuild and deploy.
- Even when enabled, the film loads only on screens 900px and wider, never with reduced-motion or Save-Data, and stays invisible until Vimeo reports that it is playing. If it has not started within 9 seconds, or Vimeo reports an error, it is removed and the poster stays.

## Conversion components
- Mobile action bar (WhatsApp / Call / Start a brief) replaces the WhatsApp float below 760px; on larger screens the float remains. `build.action_bar()`.
- "How it starts" strip (free 30-minute call, fixed-fee first review, appointment) sits above the home CTA and in short form on the contact page: `build.start_steps()` / `build.how_it_starts()`. A fee figure appears only when `PUBLISH_FEES = True`.
- Contact form: Netlify attributes, `form-name` and the `company_site` honeypot are unchanged. New/renamed fields: `stage` (now a select, was checkboxes), `contact_method` (Email / Phone call / WhatsApp; phone becomes required for the last two), `based`, `area`, `budget`. Inline validation messages are HTML (so they translate); the script only shows them.
- `/contact/thanks/` serves both forms. The newsletter posts to `/contact/thanks/#notes`, which swaps in the subscriber wording. The page reports `enquiry_success` or `newsletter_signup` accordingly (see "Conversion measurement" above).

## Design checks
- `python3 tools/contrast_check.py` checks WCAG AA contrast for the colour pairs the stylesheet uses (reads the `:root` tokens). Run it after any palette change.
- `node tools/screens.js <port> <outdir> <tag>` takes desktop (1440) and mobile (390) screenshots of the key pages from a locally served `dist/`. Before/after shots from the design pass, and the final QA shots (`final-*.png`), are in `reports/screens/`.
- After editing `site.css`, run `sh tools/make_rtl.sh`, rebuild, run `node tools/make_critical.js`, rebuild, and check `/ar/`.

## Project films hosted on the site (11 Nov 2026)
The P Chapman Vimeo films stopped playing on 11 Nov 2026 ("This video isn't available"). Three films are now hosted on this site instead: Quay House, Sea Glass House and Polgreen Manor (`src/static/assets/video/<name>.mp4`, 1080p H.264, about 20–45 MB each, made from Phil's originals with `ffmpeg -crf 24 -maxrate 3M -movflags +faststart`). In `src/content/projects.py` a project's `"video": ("file", "<name>")` plays that file in a native player after the visitor presses Play; `("vimeo", id)` still loads Vimeo. The other project pages still point at Vimeo and need either Phil's original files or their film block removed.

## 11 Nov 2026: site check fixes
- Phone hero: extra top padding and smaller headline under 760px so the kicker no longer runs under the header.
- Cookie banner: slim full-width bar on desktop, compact card on phones. While it is open the script sets `html.cb-open` and `--cb-h` (banner height); the hero padding, photo credit and WhatsApp button use them to stay clear of the bar.
- Calculator: hidden hint no longer leaves a gap on phones.
- Chinese pages use system fonts (no web-font download); "zh" removed from FONTS in tools/i18n.py.
- Dead Dubai Building Code source links replaced (dm.gov.ae page, ICC article). The stgportalnew.dm.gov.ae PDF link in glossary.py and renovate-or-rebuild could not be checked from the build machine and is unchanged.
