# Eastbridge insight articles — writing brief

## Who we are
Eastbridge Strategic Partners (Eastbridge) is an independent, client-side owner's representative and project manager for private clients building or renovating villas in Dubai and Abu Dhabi. The founding partner built and ran a premium residential construction company in the UK for 21 years (bespoke contemporary homes on the Cornish coast — e.g. waterside new-builds, cliff-top houses, cantilevered estuary houses, a development of fifteen beach houses; JCT contracts; extension-of-time and variation disputes, adjudication). The UK company was P Chapman Construction (pchapmanconstruction.com): about £17m annual turnover at peak; RIBA South West Award 2016 (Owers House); LABC Building Excellence Awards 2018 (winner) and 2020 (Highly Commended); a home featured on Channel 4's Grand Designs; Owers House reported in The Times; built for architects including John Pardey Architects and CSA Architects. Present this confidently, never apologetically. Eastbridge has not yet completed a UAE project: never claim or imply UAE projects or existing Eastbridge clients, and never volunteer or dwell on the point either. The angle: "we spent two decades as the builder; now we sit on the client's side of the table", so we know where budgets leak, how variations and delay claims are built, and what contractors hope clients won't check.

## Voice
- Firm voice: "we / our / the team". Never say "I". The founder is Philip Chapman, Founding Partner; every article is automatically bylined to him, so name him in the body only where it adds credibility (at most once), e.g. "our founder, Philip Chapman, ran P Chapman Construction for 21 years".
- British English spelling (programme, organise, metre), plain and direct, calm, expert, no hype, no "Best/#1", no emojis, no exclamation marks.
- Write for a wealthy, busy, intelligent owner (often British or European, sometimes living abroad). Short paragraphs. Concrete detail beats adjectives.
- Include at least one genuinely first-hand observation from the builder's side in each article (e.g. "On the contractor's side, the first thing we priced on any job was…"). Keep them general and plausible from 21 years of UK residential building — no client names, no invented project numbers, no awards.
- No invented statistics. Any figure must come from the facts list below (cite the source) or be framed clearly as our own rule of thumb ("in our experience…").

## Compliance — wording rules (important, legal)
Eastbridge is NOT an engineering consultancy office. Under Dubai Law No. 14 of 2025 only DM-registered consultancies may practise or present themselves as engineering consultants or supervision consultants.
- NEVER say Eastbridge supervises construction, is the "supervision consultant", "consultant of record", engineer, or that it obtains/submits permits, signs off, certifies, prepares tender documents or prequalifies contractors.
- SAY: we represent the owner; we work alongside the owner's DM-registered consultant and the contractor; independent client-side site visits and progress reporting; cost and programme control; commercial and contractual advice; we help you compare bids like-for-like and choose; the owner appoints.
- Authority route: say "Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where your plot sits" — do not assert which authority covers a specific community.
- Do not give legal advice; say "take advice from a UAE-qualified lawyer" where relevant.

## Format (Markdown file with YAML front matter)
File: src/content/insights/<slug>.md
```
---
title: "…"                      # ≤ 60 chars ideally, natural, includes the main keyword
description: "…"                # 140–160 chars, specific, no clickbait
date: 2026-10-29
updated: 2026-10-29
category: "Costs" | "Process" | "Approvals" | "Contracts" | "Choosing a team" | "Renovation" | "Plots" | "Overseas owners" | "Handover"
keypoints:                       # 3–5 one-sentence takeaways, shown at top (AI assistants love these)
  - "…"
faqs:                            # 3–5 Q&As specific to the article
  - q: "…"
    a: "…"
sources:                         # every external fact cited, title + URL
  - title: "…"
    url: "…"
---
Body in Markdown. 1,400–2,200 words. Start with a 2–3 sentence direct answer to the title question (no preamble). Use ## and ### headings phrased the way people search ("How long does it take to build a villa in Dubai?"). Use a table where data is tabular. Link internally using root-relative links where natural, e.g. [plot review](/services/plot-due-diligence/), [owner's representation](/services/owners-representative/), [contact](/contact/), other insight slugs listed below. End with a short section "How Eastbridge can help" (3–5 sentences, not salesy) linking to one relevant service and /contact/.
```
Do NOT include the H1 in the body (the title becomes the H1). Do not include the keypoints/faqs again in the body.

## Internal links available
Services: /services/owners-representative/ /services/villa-construction-project-management/ /services/villa-renovation-project-management/ /services/plot-due-diligence/ /services/design-and-approvals/ /services/consultant-and-contractor-selection/ /services/cost-and-programme-control/ /services/site-visits-and-reporting/ /services/variations-delays-and-claims/ /services/stalled-project-rescue/ /services/snagging-and-handover/ /services/overseas-owners/ /services/development-advisory/
Areas: /areas/palm-jumeirah/ /areas/emirates-hills/ /areas/jumeirah-bay/ /areas/district-one/ /areas/dubai-hills-estate/ /areas/al-barari/ /areas/dubai-islands/ /areas/palm-jebel-ali/ /areas/saadiyat/ /areas/hudayriyat/
Other: /fees/ /independence/ /approach/ /work/ /contact/
Insight slugs: villa-construction-cost-dubai, how-to-build-a-villa-in-dubai, owners-representative-vs-project-manager-vs-consultant, palm-jumeirah-villa-renovation, how-to-choose-a-villa-contractor-dubai, villa-construction-contracts-uae, building-a-villa-in-dubai-from-the-uk, villa-snagging-checklist-dubai, buying-a-villa-plot-in-dubai-checks, what-the-contractor-knows, dubai-municipality-villa-building-permit, villa-renovation-cost-dubai, how-long-to-build-a-villa-dubai, nakheel-noc-villa-renovation, stalled-villa-project-dubai, abu-dhabi-villa-permit-tamm. Other pages: /glossary/ (anchors like /glossary/#retention), /tools/villa-build-cost-calculator/, /guides/villa-owner-checklist/

## Verified facts you may use (cite the source URL when you use one)
Costs (construction only, AED per sq ft, 2025–26):
- Engel & Völkers (Dec 2025): standard 300–500, mid 500–600, luxury 900–1,400; design/engineering/permits AED 50k–150k. https://www.engelvoelkers.com/ae/en/resources/construction-cost-dubai
- Knight Frank Q2 2025 (via Gulf Construction / E&V): ~AED 4,200/m² (~390/sqft) standard; ~AED 11,000/m² (~1,020/sqft) high-end. https://gulfconstructiononline.com/ArticleTA/436847
- Real Estate Club Dubai: standard 350–500, premium 600–850, luxury 850–1,200, ultra-luxury 1,200+; contingency 10–15%; FF&E 30–40% at the top end; pool AED 80k–250k; landscaping AED 100–500/sqft of garden; permits/NOCs/DEWA AED 25k–75k or 2–5% of build; design fees multi-discipline 6–12% (~9% typical), architect-only 4–7%, engineering 3–5%; timeline design 3–4 months, approvals 2–3 months, construction 8–14 months, snagging 1–2 months, plot to keys 12–24 months (24–36 for custom luxury). https://realestateclubdubai.com/dubai-villa-architects and https://realestateclubdubai.com/tools/villa-build-cost-calculator
- Optimal Engineering: luxury up to 1,200+; full design & engineering 6–12% of contract value. https://www.optimal.ae/blog/cost-to-build-a-villa-in-dubai
- Renovation ranges (Smart Renovation guide): basic AED 200–300k, mid AED 400–800k, luxury AED 1m+. https://smartrenovation.ae/villa-renovation-in-dubai-complete-2026-guide-to-costs-timeline-permits/
- UAE construction cost inflation ~3% forecast for 2026 (Currie & Brown, cited by PRASOON); contractor preliminaries 12–14% in Dubai (Turner & Townsend 2025). https://prasoon.design/insights/owners-representative-vs-project-manager-uae
Process & authorities:
- Dubai single unified e-window for building permits (2022) across DM, DDA, Trakhees, DIEZ, with Civil Defence, RTA, DEWA, Etisalat, du linked. https://www.dm.gov.ae/dubai-launches-single-window-for-building-permits/
- "Building in Dubai" platform (Oct 2023) covers land, design, permits, construction, completion, connection, alterations. https://www.mediaoffice.ae/en/news/2023/october/18-10/dubai-municipality-launches-building-in-dubai-platform  site: https://buildindubai.gov.ae/
- Dubai BPS app relaunched Aug 2024 with consultant/contractor registry and ratings. https://www.dm.gov.ae/new-improved-building-permits-app-launched-for-streamlined-services/
- DM residential permit sequence: consultant/contractor submits drawings and fees online; authority NOCs via the unified window; permit and stamped drawings; staged inspections (shoring/foundations, slabs); joint completion inspection (Building Control, Survey, telecoms, Civil Defence where needed); completion certificate; service connection. https://stgportalnew.dm.gov.ae/wp-content/uploads/2020/06/Residential-Buildings_Building-Permits-Procedures.pdf
- Aug 2026: DM announced an AI system checking villa drawings against the Dubai Building Code, phased rollout via Build in Dubai. https://www.khaleejtimes.com/uae/dubai-ai-system-villa-construction-permits
- Aug 2025: DM warned villa engineering consultancies about over-designing structures and inflating build costs. (Note: separate June 2025 suspensions of two offices were for other ethics breaches — do not link them to over-design.) https://gulfnews.com/uae/dubai-municipality-warns-consultancies-inflating-villa-designs-raising-costs-1.500245704
- DM publishes standard contract forms for engineering consultancy and construction contracting for private villas (Arabic). https://www.dm.gov.ae/municipality-business/guidance-contracts-forms-for-engineering-consulting-services-and-construction-contracting-for-private-villas/
- Dubai Law No. 14 of 2025 regulates engineering consultancy across Dubai incl. free zones (Al Tamimi). https://www.tamimi.com/news/dubai-issues-new-law-regulating-engineering-consultancy-activities-key-takeaway-points/
- Abu Dhabi: DMT regulates; municipalities issue permits via TAMM; Sep 2025 private-villa regulation amendments (rooftop majlis, 1.5 m front setback, annex basements). https://www.dmt.gov.ae/en/Media-Centre/News/Department-of-Municipalities-and-Transport-Announces-Amendments-to-Private-Villas-Regulations ; minor works (extensions up to 25 m², pools, canopies, fences) permits direct by contractors, Aug 2025 https://www.dmt.gov.ae/en/Media-Centre/News/DMT-Unveils-Streamlined-Permit-Process-for-Minor-Works ; Oct 2026 Circular No. 9: certified joint reports by supervision consultant and contractor replace phase-closure permits for designated categories https://www.khaleejtimes.com/uae/abu-dhabi-replaces-paper-permits-for-buildings-with-digital-reports-new-directive?amp=1
- Modon's Hudayriyat residential plots (Wadeem): 1,700+ plots for 4–6 bed villas. https://meconstructionnews.com/63729/modon-launches-its-first-residential-plots-community-on-hudayriyat-island
- Master developers: Palm Jumeirah, Dubai Islands, Palm Jebel Ali, Jebel Ali Village — Nakheel; Emirates Hills — Emaar; Jumeirah Bay — Meraas (Dubai Holding); Dubai Hills Estate — Emaar with Meraas; Saadiyat — Aldar; Hudayriyat — Modon. Renovation/extension approvals in Nakheel communities start with a Nakheel NOC application through its portal before the authority permit.
General market estimates (frame as estimates, not facts): owner's rep/PM fees roughly 2–5% of construction cost internationally; no published Dubai benchmark exists (PRASOON says "no credible benchmark exists").


## Positioning
Use 'client-side project manager' as the primary description (owner's representative as a synonym). The Island E worked project example (hypothetical: never describe it as a case study, a completed project or a result, and never quote its modelled savings) is at /case-studies/island-e-waterfront-villa/; the real UK project case study is Owers House at /work/owers-house/#case-study and the value explainer at /why-a-client-side-project-manager/ — link to them where relevant.
