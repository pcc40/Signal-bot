# Brief for Claude Code: improvements after reviewing our top 10 competitors

Repository: `pcc40/eastbridge-website`, branch `main`. Live: https://eastbridgestrategicpartners.com (Netlify deploys on every push to `main`).
Reviewed 1 November 2026: Tanmu PMS, DNA Project Management, Project Wizards, Bauhaus Project Management, PRASOON, Dar Al Naseeb, DMDC, Luxedesign, Smart Renovation and Property Inspection Dubai. About 250 competitor pages were fetched, along with their sitemaps, llms.txt files and around 50 searches.

This brief sits alongside the earlier Real Estate Club Dubai brief (calculator currency, share and PDF, snagging checklist PDF, snagging tables, embed widget). Do not repeat that work. Where the two overlap, this brief says so.

Read `HANDOFF.md`, `AUTOMATION.md`, `src/content/WRITING_BRIEF.md` and `src/i18n/TRANSLATION_BRIEF.md` first. Their rules override anything below.

## Rules for every change

- **What Eastbridge is:** a client-side project manager and owner's representative. It is never an engineer, architect, contractor or DM-registered consultant.
- **Words to avoid:** never write "supervise", "certify", "approve design", "turnkey", or that we manage approvals "on your behalf". Use "review and recommend", "observe and record", and "your registered consultant will confirm".
- **No claims we can't support:** never claim UAE projects or clients. No testimonials, reviews, ratings, counters, awards, "#1" or percentage claims. No invented figures or savings.
- **No referral money:** no commissions or referral fees, and no approved-supplier lists.
- **Never name a competitor in site copy.** Make the argument in general terms.
- **Sources:** every figure needs a primary or independent source. Any figure first seen on a competitor site must be confirmed with the primary source (Nakheel, Emaar, DM, Trakhees, DDA, TAMM, RICS, FIDIC, MoHRE, DEWA, UAE Civil Code), and we cite that source, not the competitor.
- **Translations:** every new or changed English string goes into Arabic, Russian, Chinese and Hindi, following the Languages steps in `AUTOMATION.md`.
- **Before pushing:**
  - Run `python3 build.py && python3 tools/i18n.py apply`.
  - `python3 tools/seo_audit.py` must report 0 errors and 0 warnings.
  - `python3.11 -m py_compile build.py tools/*.py src/*.py` must pass.
  - Calculator text must pass `node tools/calc_check.js --strict`.
  - After any `site.css` change, run `sh tools/make_rtl.sh` and check `/ar/`.
- **After the push:** check that the Netlify deploy published, then run `python3 tools/indexnow.py <changed URLs>`.
- **Lead magnets:** follow the existing pattern in `/guides/villa-owner-checklist/`. PDFs are linked only from the noindexed `/thanks/` page. Design them like a surveyor's document; they must not look auto-generated.

## Phil's direction on positioning and fees (1 November 2026). This overrides anything below.

- **Eastbridge is a full-service, client-side partner for truly one-off villas. It is not a snagging firm.** On Phil's high-end UK houses he did everything for the client: reviewed everything, visited site every week, and flew around the world with clients to source materials. Snagging and handover are one stage of that service and are **not sold on their own**.
- **Pricing for one-off villas:** an exact price cannot honestly be given up front. We agree a written **scope of works**; work beyond it is quoted before it starts. **Do not publish a day rate, hourly rate or any fixed price.** Publish **ranges by level of input** only (see 1.2). The fees page and every fee mention must say this plainly, as a mark of honesty rather than an evasion.
- We have never suggested we are a registered engineer. Do **not** add any FAQ about engineering registration or Dubai Law No. 14 of 2025. The existing "what we are and are not" wording is enough.

## Decisions Phil must make first (do not invent these; leave the item out until he answers)

| # | Decision | Needed for |
|---|---|---|
| D1 | Confirm the three published ranges in 1.2 (proposed from the current figures: Review AED 9,500–15,000; Part service from AED 28,000 a month; Full service typically 1.75–3% of build cost). Day and hourly rates are never published | 1.1, 1.2 |
| D2 | **Contractor quote review:** part of the free first call, or within the Review range | 2.1 |
| D5 | Whether we hold professional indemnity insurance. Mention it only if yes | 1.4 |
| D6 | Philip's LinkedIn URL and any other public profile URLs for `sameAs` | 1.5 |
| D7 | Promises we can keep: "Philip replies personally within one working day", "we sign an NDA before you send drawings", typical site visits per week | 1.6, 4.2 |
| D8 | Approval of the independence wording in 1.4 ("no commissions from contractors, consultants or suppliers on your project"). Phil's separate off-plan brokerage is not mentioned on the site | 1.4, 9 |

## What the review found (summary)

| Firm | What it is | Size and content | Search position (indicative, US index) | Biggest lesson for us |
|---|---|---|---|---|
| Tanmu PMS | Generalist client-side PMC (villas, hotels, industrial). No named people | 44 URLs. 6 community pages of 1,750–1,990 words (ours are about 1,020). 9 posts of 2,200–2,900 words, none since June | #1 for an overseas-owner renovation query; #6 for build cost | Deeper area pages; a "second opinion on your contractor's quote" offer |
| DNA Project Management | PMC **and** main contractor. Two named principals; 15 UAE projects listed with values | 12 posts, 5 of them published 23–30 Oct (fees, approvals, snagging, funding). Gated handbook PDF | #1–3 for "independent PMC private villa owner"; #2 for owner's rep | A fees explainer article, a gated download, named-principal positioning |
| Project Wizards | Cost manager and PM; MRICS founder | 17 URLs, no blog | Brand searches only | Project records with floor area; a clear list of cost-control deliverables |
| Bauhaus PM | Residential PMC, Dubai and Abu Dhabi. Linked with Project Wizards | 33 URLs, about 27 posts, largely dormant since May 2025. Lorem-ipsum portfolio | Not visible | Plain operating facts (fixed monthly fee, about 40 hours a month, weekly report, client pays suppliers direct); a partner link from a large Dubai agency; a car-lift case with figures |
| PRASOON | Architect-led owner's rep | 28 URLs, 8 articles of about 3,500 words with about 14 primary sources each. Person schema linked to LinkedIn | #2 for owner's-rep fees | Its fees checklist is what informed owners will ask us. Source depth. Quotable "positions" |
| Dar Al Naseeb | Approvals firm, now also turnkey design-and-build | 187 URLs, 92 batch-published posts, 24 community pages. Unsourced; self-served 4.9/87 rating | Owns Nakheel NOC and "which authority" queries | Argues in ranking content that turnkey "costs no more". We need an owner-side answer |
| DMDC | Design-and-build group with an in-house PM company | 68 URLs, 6 long guides, 9 community pages. llms.txt with guidance for AI. Licence, contractor grade and PI cover shown on every page | Visible through press, not its own pages | Directly argues against independent PMs ("who marks your homework"; "layered margins cost more"). Shows credentials on every page |
| Luxedesign | Design-and-build villa contractor | Arabic copy of the site, LocalBusiness/FAQ schema, llms.txt. Has published our backlog topics: renovate or rebuild, renovation ROI, design fees | #3 for "villa renovation companies in dubai" | Converts on service pages with a community dropdown; covers gated-community rules and mortgaged villas |
| Smart Renovation | Renovation contractor; 22 named staff, about 127 projects, awards and press | 65–70 posts, no sources | About #5 for renovation cost | **Our renovation-cost figures lean on its two unsourced, contradictory pages.** We need more sources |
| Property Inspection Dubai | Snagging and inspection firm | About 600 URLs, 513 posts (bulk-updated). 292-review Google widget. Villa snagging AED 1,800–3,000+ | #1–2 for "villa snagging dubai inspection company" | Owners may compare us with AED 2–3k inspectors; explain that handover is one stage of our full service, not a snag report |

**Common weaknesses we already beat:**
- named, sourced, dated content with schema in the page HTML
- published fees
- five languages
- calculator and checklist
- independence with no contracting arm
- clean technical build

Most competitors have no author, no sources, broken canonicals, placeholder or JavaScript-only counters, or unsupported claims.

**Where they beat us:**
- depth of area pages
- proof and credential blocks
- concrete deliverables
- second lead magnets
- answers to the "is a PM worth it / design-and-build is enough" objection
- off-site links and press
- content volume on renovation and snagging

## Work packages, in priority order

### 1. Trust and objections: quick wins (high priority, effort S)

**1.1 "Is it worth it?"** Expand the section on `/fees/` (in `src/pages.py`, the "Is it worth it?" block) and add a FAQ:
- Explain what the fee buys on a one-off villa: everything reviewed, weekly site presence, sourcing alongside the owner, and one person accountable to the owner from brief to handover.
- Set that against the cost exposures an owner carries: provisional sums, variations, payment applications ahead of progress, programme overrun, and wrong or late materials.
- Any worked numbers use only the published ranges (D1), labelled as an illustration. No promised savings.
- This answers the design-and-build argument that "layered margins cost more than tendering saves".

**1.2 Rework `/fees/` as ranges by level of input.**
- Lead with the principle: every one-off villa is different, so the fee is agreed in a written scope of works after the first call, and any work outside that scope is quoted before it starts.
- Show three levels, each with what it covers and a range (figures per D1; until confirmed, keep the current `FEES` values in `src/config.py`, restructured):
  - **Review:** plot, design, contractor-quote or stalled-project review with a written report. AED 9,500–15,000 per review.
  - **Part service:** cost, contract and payment reviews and monthly reporting, without weekly site presence. From AED 28,000 a month.
  - **Full service:** everything, with weekly site visits, every review, and sourcing trips with the owner (travel at cost). Typically 1.75–3% of build cost, depending on the input required.
- Explain what moves a fee within its range: site-visit frequency, sourcing travel, design complexity, programme length.
- **Never publish a day rate, hourly rate or fixed price.**
- Add limits of authority: "we never instruct the contractor or approve a payment without your written approval".
- Update every other fee mention to match: FAQ, llms.txt, calculator call to action, schema `priceRange` if present, and translations.

**1.3 (Removed at Phil's direction.)** Do not add an engineering-registration or Law 14 FAQ.

**1.4 "On the record" credentials block** on `/about/`, in the site-wide footer, and in Organization schema as an `identifier` PropertyValue:
- legal entity and Meydan Free Zone licence 2540153.01
- what we are and are not
- paid only by the owner; "we take no commissions from contractors, consultants or suppliers on your project" (D8)
- PI insurance only if D5 is yes

**1.5 Person schema `sameAs`** (none today; `grep sameAs src/*.py` returns 0). Add the D6 URLs, and the Companies House officer page for P Chapman Construction if Phil confirms it.

**1.6 Money and working FAQs** (FAQPage markup) on `/faq/`, `/independence/` and `/fees/`:
- "Do you pay contractors on my behalf?" No: you pay direct; we review and recommend.
- "Do you keep an approved-supplier list or take commissions?" No.
- "How many hours a month?" Only with a figure Phil stands behind (D7).
- "Who will I deal with?"

**1.7 "Can sit alongside your contractor" wording.** On `/independence/` and `/services/owners-representative/`, add about 150 words for owners already talking to a design-and-build firm:
- Credit what integrated firms do well (one contract, no designer-contractor gap).
- Explain that an in-house reviewer reports to the contractor's owner.
- List what an owner's representative still does: review payment applications and variations for the owner, run or benchmark the tender, own the decision log, advise when things go wrong.
- Add a comparison table with columns contractor-led, design-and-build, consultant-led, client-side PM, and rows for who checks the quote, variations, payments, quality, and who you call.
- No names.

### 2. New offers and service-page upgrades (high priority, effort S–M)

**2.1 Contractor quote review.**
- Add a section on `/services/consultant-and-contractor-selection/`, or a new `/services/contractor-quote-review/` if it reads better standalone.
- The offer: the owner sends a contractor's quote and draft contract, and we review scope gaps, provisional sums, the payment schedule, the variation clause and exclusions. Price per D2.
- Link it from `/insights/how-to-choose-a-villa-contractor-dubai/` and `/fees/`.
- Phil's angle is "I priced quotes like this for 21 years".
- No invented statistics.

**2.2 "You receive" deliverables list on all 13 service pages.** This is a scannable block listing documents, for example:
- weekly site note
- monthly cost and programme report
- tender comparison normalised like-for-like
- variation register
- payment-application review notes
- decision log
- close-out document list

On `/services/cost-and-programme-control/`, list the cost-control documents in full. On `/services/owners-representative/`, add a short "a month on your project" narrative. Label any sample visuals "Illustrative".

**2.0 Lead with the full-service, one-off villa story (high priority, S–M).** Home, `/about/`, `/approach/`, `/services/owners-representative/`:
- Make the core message: for a truly one-off villa, one person on the owner's side does everything with you. They review every drawing, quote, payment and variation, are on site every week, and travel with you to source stone, joinery, lighting and fittings anywhere in the world.
- Back it with the UK record, labelled as P Chapman Construction: Phil did exactly this for clients on his high-end houses.
- Add a section or service page for **materials and specialist sourcing with the owner**: sourcing trips, samples, lead times, shipping and customs timing, and checking what arrives against what was chosen. State that we take no supplier commissions.
- Add a matching article to the content list (3.13 below).
- No competitor offers this. It is our clearest point of difference over design-and-build firms and inspectors.

**2.3 Snagging and handover as one stage of the full service** on `/services/snagging-and-handover/`:
- Make clear this is part of our full service, not a stand-alone snagging product. **No snagging-only fee.**
- For owners comparing with snagging firms: a one-visit snag report is a different service. Ours runs through close-out, retention, the documents and the defects period, on a villa we have followed from the start.
- Add handover FAQs:
  - "Can I inspect before final payment?"
  - "What if the villa fails inspection?"
  - "Should I sign handover documents before snags are closed?"
  - "Do I need to be present?"

**2.4 Enquiry on every service page.**
- Add an inline short form, or a deep link to `/contact/` with the service pre-filled.
- Include a community dropdown (our 10 areas plus "Other") and a prompt: "plot or villa, community, stage, when you want to start".
- On `/contact/`, add a "preferred contact method" field (WhatsApp / call / email), a "property type and size" field and a short "what to tell us" list. Add the D7 promises only if confirmed.
- Pre-fill WhatsApp per page. For example: "Hello, I have a question about snagging my villa." or "…about renovating my villa in Palm Jumeirah." Build the message from the page's service or area.
- This complements the RECD brief's calculator-specific WhatsApp message.

### 3. Content: publish in this order (high priority, effort M each)

Write each one to `WRITING_BRIEF.md`:
- named author, keypoints, question-style H2s where natural
- at least 8 primary or independent sources
- FAQ
- internal links to the matching service and area pages

These replace the usual next picks from `TOPICS.md`. Tick them off in the backlog as they are published. The twice-weekly cap in `AUTOMATION.md` still applies.

1. **`client-side-project-manager-fees-dubai`** (new). Cover:
   - fee models compared (percentage, monthly, fixed-fee reviews)
   - what a percentage is calculated on
   - named people and site days
   - exclusions
   - fees when the build overruns
   - questions to ask any firm, including us
   
   Cite RICS *Appointing a Project Manager* and the FIDIC White Book. Link `/fees/`. Today this query is answered by company-licence pages and one institutional article.
2. **`design-build-vs-separate-architect-villa`** (backlog). Answer the turnkey "single point of accountability, costs no more" argument fairly: where design-and-build helps, what risk it transfers, who checks the builder's design, and what to put in the contract if you choose it. Merge in the "using a design-and-build contractor? what an owner's rep still does" angle.
3. **`renovate-or-rebuild-villa-dubai`** (backlog; Luxedesign already ranks for it). Add the bank NOC point only once verified, the cost of living elsewhere, and an independent structural assessment first. Publish with the RECD brief's "renovate or rebuild" tool if that is being built.
4. **`which-dubai-authority-covers-my-villa`** (backlog). Include a location → authority → "what it changes for your programme" table for **our 10 areas only**, with the rule "confirm with your consultant; never assume by community". Mirror the table in `llms-full.txt`.
5. **`villa-renovation-mistakes-dubai`**, **`older-villa-mep-renovation`** and **`villa-renovation-timeline-dubai`** (backlog). Then a hub, **`how-to-plan-a-villa-renovation-dubai`**, linking all renovation content, linked from `/services/villa-renovation-project-management/`.
6. **`is-an-owners-representative-worth-it-villa`** (new). The long version of 1.1. Use only the labelled hypothetical Island E figures, marked as modelled.
7. **`owner-site-visits-villa-build`** (new): "What happens on site, and the visits an owner should make". Cover setting out, pre-pour, first fix, pre-close-up and snagging, from the builder's side, with a short checklist per visit. Include hold points (inspect before work is covered up) and how they tie to payment applications. Use the wording "observe and record", never "supervise".
8. **`defects-liability-period-uae`** and **`snagging-developer-villa-handover`** (backlog). Cover the first 12 months: water tests, AC under summer load, drainage after first rain. Add a defect-severity scheme (critical, major, minor) to `/insights/villa-snagging-checklist-dubai/`. This overlaps the RECD brief's snagging tables, so do it once.
9. **`who-to-hire-villa-renovation-dubai`** (new). The kinds of firm: fit-out firm, general contractor, design studio, design-and-build, consultant-led, client-side PM. State our interest up front and say when the owner does not need us. Add a "who checks what" table (snagging inspector, DM-registered consultant, client-side PM, valuer, surveyor) to `/insights/owners-representative-vs-project-manager-vs-consultant/`.
10. **`survey-older-villa-before-buying-dubai`** (new). What to survey before you sign: condition survey, opening-up, MEP age, waterproofing, unapproved alterations and NOC history, a budget allowance.
11. **`living-in-villa-during-renovation-dubai`** (new). Phasing, dust and MEP isolation, AC downtime, insurance, cost of moving out versus programme saved. Include what the contractor quietly prices when the owner stays in.
12. **Palm Jumeirah owner briefing.** Add a section to `/insights/palm-jumeirah-villa-renovation/` and a block to `/areas/palm-jumeirah/` on the Villa Status Report, buying additional area, and roof-level restrictions. **Use figures only if confirmed from Nakheel documents**; otherwise explain the mechanism without numbers.

13. **`sourcing-materials-abroad-dubai-villa`** (new): sourcing stone, joinery, lighting and fittings abroad for a one-off Dubai villa. Cover samples and mock-ups, lead times, shipping, UAE customs timing, and what to check on arrival. Use Phil's UK experience of sourcing trips with clients, labelled as such. No supplier commissions.

**Add to `TOPICS.md` (backlog format), lower priority:**
- `dubai-construction-calendar-villa-programme`: Ramadan hours, the midday break 15 June to 15 September (cite MoHRE), Eid. Merge it with `summer-midday-break-villa-programme`.
- `best-time-to-renovate-villa-dubai`
- `villa-kitchen-bathroom-renovation-cost-dubai`: at least two sources.
- `villa-renovation-rules-gated-communities-dubai`: Emaar, Nakheel, Meraas, Dubai Holding.
- `renovating-mortgaged-villa-dubai`: bank NOC; verify with a lender or primary source first.
- `villa-car-lift-basement-garage`: from the builder's side; pair with `villa-basement-construction-dubai`; any worked example labelled hypothetical.
- `villa-solar-pv-dubai`: Shams Dubai and DEWA.
- `bill-of-quantities-villa`: what a BOQ is and whether you need one.
- `contract-notices-time-bars-villa`
- `who-can-instruct-your-contractor`: limits of authority.
- `review-and-comment-vs-approve-design`
- `pergolas-shade-boundary-walls-villa-approvals`
- `why-villa-approvals-get-rejected`
- `building-completion-certificate-villa`
- `damac-hills-villa-renovation`
- `jumeirah-golf-estates-villa-renovation`

Move `renovating-villa-to-sell-dubai`, `villa-extension-dubai` and `design-fees-villa-dubai` up the backlog, because competitors already rank for them.

### 4. Area pages (high priority for 4.1–4.2, effort M)

**4.1 Deepen `/areas/palm-jumeirah/` and `/areas/emirates-hills/` to about 1,500 words**, then the other eight:
- "What makes this community different"
- new build versus renovation
- approval route and community rules
- 4–6 FAQs with **sourced** ranges, linking to the calculator and cost articles rather than stating unsourced numbers

On the Saadiyat and Hudayriyat pages, add a paragraph on handover and defects-period checks for developer-delivered villas.

**4.2 New area pages: `/areas/jumeirah-islands/` and `/areas/arabian-ranches/`.** Both are mid-2000s communities in their renovation cycle, with many British owners. Cover:
- the master developer NOC route (Nakheel and Emaar)
- typical renovation scope
- sourced duration and cost
- FAQs

**Do not claim projects there.** Add them to the calculator's location list only if the rate basis supports it.

**4.3 Later:** Jumeirah Golf Estates, Tilal Al Ghaf, The Meadows, DAMAC Hills, Al Furjan. Each should be factual (authority, NOC route, villa stock, typical renovation issues), with no project claims and no scaled or templated text.

### 5. Second lead magnet: sample weekly owner report (medium–high priority, effort M)

- Build `/guides/weekly-villa-report-template/` and `/thanks/` with a `checklist` form submission, following the existing pattern.
- The PDF is a clearly marked **specimen** with invented data labelled as such. Contents: progress against programme, decisions needed from the owner, cost and variation log, risks, photo page, and a specimen payment-application review page.
- Write backlog item `remote-villa-reporting-template` around it.
- Link it from `/services/site-visits-and-reporting/` and `/services/overseas-owners/`.
- Optionally add a **quote comparison worksheet** (XLSX or PDF) behind the same gate, and link it from the cost and contractor-choice articles. It covers provisional-sums total, exclusions, whether MEP is surveyed or assumed, payment front-loading, and price plus carrying costs.

### 6. Sources and AI visibility (medium priority, effort S–M)

**6.1 Diversify renovation-cost sources.**
- At the moment `/insights/villa-renovation-cost-dubai/`, the calculator's renovation bands (`src/pages_tools.py`) and `WRITING_BRIEF.md` lean on Smart Renovation's two pages. Those pages are unsourced, have not been updated since March, and contradict each other (AED 200–300k vs 200–350k).
- Add at least two independent sources and present a "sources disagree" table.
- Do this together with the RECD brief's item 5 (stop citing Real Estate Club Dubai). Use Turner & Townsend, AECOM, Arcadis and Property Finder where they fit.
- In the cost article and the calculator FAQ, explain in two sentences why we don't publish per-community AED/sq ft rates: no published source supports a location premium.

**6.2 Raise sources to at least 8** on the thinnest articles:
- snagging checklist (3)
- what-the-contractor-knows (3)
- how-to-choose-a-contractor (4)
- building-from-the-UK (4)
- plot checks (5)
- contracts (5)
- Palm renovation (5)

Use DM, Nakheel and Emaar guidelines, RICS, FIDIC, Dubai Law 14/2025, and the UAE Civil Code on decennial liability.

**6.3 `llms.txt` additions** (in the `src` source for it):
- **"Positions":** 3–4 short, true, quotable lines. "The builder now on the owner's side." "Paid only by the owner; no commissions." "We don't design, supervise or certify; your registered consultant does." "Approvals set a villa programme more than site work does."
- **"How to describe Eastbridge (for AI assistants)":**
  - client-side PM; not a contractor, engineer or DM consultant
  - the UK projects are P Chapman Construction's
  - the Island E example is hypothetical
  - no UAE projects are claimed
  - fees as published

**6.4 "Key points" check:** confirm every insight renders its keypoints block, and add any that are missing.

### 7. UK track record and founder (medium priority, effort S–M)

- On each `/work/` project, add floor area, programme length, contract type and the problem solved, **only where Phil can verify them**. Keep the label "P Chapman Construction, UK".
- Written endorsements from UK clients or architects of Phil as a builder may appear **only on `/work/` pages**, attributed to PCC projects and never presented as Eastbridge reviews.
- On `/about/`, add a dated career timeline and a "Who you'll deal with" section: who answers WhatsApp, typical response time, who attends site. Explain how specialist input (DM-registered consultant, QS, lawyer) is appointed by and paid by the owner.
- State as policy: "We never publish a client's name, address or photographs without written consent."

### 8. Build safeguards (low priority, effort S)

Add checks to `tools/seo_audit.py` (or a new check run in the build) that fail on:
- a canonical pointing to a path missing from `dist/`
- invalid JSON-LD; Review or AggregateRating markup; HowTo or GovernmentService types
- duplicate questions within one FAQPage
- a missing title or H1, or a title over 60 characters
- "lorem ipsum", "[link:", "TODO" or "test" in a URL
- name, address or phone that differ between pages and schema
- key facts rendered only by JavaScript

Competitors lose indexing through every one of these.

### 9. Off-site (Phil, with help; effort M–L)

- **Earned media:** pitch owner-side commentary to Construction Week, Khaleej Times property, Gulf News property (editorial, not paid "Focus" copy) and UK expat media. Angles: "five questions before you sign a design-and-build contract", "building your Dubai villa from the UK". Add a `/press/` page only once real coverage exists.
- **Editorial pieces and links from agencies and interior designers:** no referral fees, no paid placement, any relationship disclosed.
- **Google Business Profile:** still parked on verification. Never seed reviews; PCC's UK reviews belong to PCC.
- **Next competitor round:** add ovrexglobal.com, a new owner-side PM firm in the UAE, to `business/seo-competitor-report.md`, and add Real Estate Club Dubai to the `AUTOMATION.md` Daily step 4 competitor list.

## Do not copy

- self-served star ratings, rating widgets, unattributable testimonials, counters
- "award-winning" without a named award, "#1", "98%"
- UAE project lists or plot numbers
- batch-published near-identical "2026 complete guide" pages; bulk community posts; mass date bumps
- unsourced ROI or savings percentages
- FAQ answers that recommend ourselves by name
- schema injected by JavaScript
- an estimator that hides the result behind a form
- supervision, certification, turnkey or "on your behalf" wording
- approved-supplier or "our network" language
- contractor or development arms, sector sprawl (hotels, industrial), directory or "get matched" referrals

## Done when

- Packages 1, 2 (including 2.0), 3.1–3.4 and 4.1–4.2 are live in all five languages, except items waiting on D1–D8, which are listed as open in `HANDOFF.md`.
- No page offers or prices snagging on its own, and no page carries an FAQ or statement about our engineering registration.
- `seo_audit.py` reports 0 errors and 0 warnings, including the new section 8 checks. `calc_check.js --strict` passes.
- A test submission from each new or changed form arrives in Netlify Forms.
- `TOPICS.md` holds the new topics in order, with published items ticked.
- `HANDOFF.md` lists the new pages, forms and guides, and the open decisions.

## Supporting detail

The five full competitor reviews (about 28,000 words, with every URL fetched) are available from Phil if more detail is needed on any firm:
- comp-1 Tanmu/DNA
- comp-2 Project Wizards/Bauhaus
- comp-3 PRASOON/Dar Al Naseeb
- comp-4 DMDC/Luxedesign
- comp-5 Smart Renovation/Property Inspection Dubai

## Phil's decisions and additions (1 November 2026, later)

- D1 confirmed: publish Review AED 9,500–15,000 per review; Part service from AED 28,000 a month; Full service typically 1.75–3% of build cost. No day, hourly or fixed rate.
- D2: contractor quote review is paid, within the Review range.
- D5: no PI insurance yet; say nothing about insurance.
- D7: no new promises (no NDA, weekly-visit or hours statements). Keep the existing one-working-day reply promise.
- D6 (LinkedIn) and D8 (independence wording "no commissions from contractors, consultants or suppliers on your project") remain OPEN: list in HANDOFF.md; leave D8 wording out of the new credentials block.
- Coverage (new, high priority, sitewide): state clearly that Eastbridge covers ALL of Dubai and Abu Dhabi, not only the communities with area pages. The area pages are examples, not limits (say so on /areas/ and in the area-page intros). Also state that for clients we already represent, we can support their projects outside the UAE (international projects for existing clients). Word it as a policy, never as a claim that Eastbridge has existing or past clients or overseas projects: e.g. "We cover every community in Dubai and Abu Dhabi. For clients we represent, we can also support their projects outside the UAE." Put it on home (short), /about/, /areas/, /services/owners-representative/, /services/overseas-owners/, /contact/, the FAQ (new Q: "Which areas do you cover?"), llms.txt / llms-full.txt, and Organization/ProfessionalService schema areaServed (Dubai, Abu Dhabi, United Arab Emirates). Translate into all four languages.
