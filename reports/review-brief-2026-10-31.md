# EASTBRIDGE WEBSITE - FEEDBACK AND IMPLEMENTATION BRIEF (review of 31 October 2026)
Reviewed preview: https://incredible-haupia-7adc73.netlify.app/ (built from this repo's dist/)

Implement in the source templates, content files and translation system (never only in generated HTML).
Preserve brand, photography, typography, restrained palette and premium feel. No wholesale redesign.
Complete changes supported by existing facts. Where commercial information or evidence is missing, continue and list the exact owner inputs needed. Do not publish invented facts or visible placeholder claims.

Assessment: overall 7.5/10; presentation 8.5; proposition clarity 8; evidence/credibility 6.5; enquiry journey 7.
Weaknesses: prominence of modelled results, limited evidence of UAE delivery arrangements, vague initial pricing, some overconfident wording.
Keep: client-side PM / owner's rep positioning; Philip Chapman's UK construction background and real photography; distinction between Eastbridge, main contractor and registered consultant; independence pledge and direct client payment of consultants/contractors; service pages, portfolio, guides, WhatsApp, staged enquiry.

## 1. Reposition the Island E example
Pages: /, /case-studies/, /case-studies/island-e-waterfront-villa/ and all language versions, cards, metadata, structured data.
- Rename presentation, e.g. "Island E: worked project example" / "How we would manage an Island E villa".
- Short prominent explanation BEFORE the numbers: hypothetical project showing the method; not a completed Eastbridge appointment or a promise of savings.
- Conditional language for invented events and outcomes throughout.
- Remove simulated savings (AED 3.87m cost avoided) and under-budget (AED 0.55m) results from homepage proof/achievement tiles. Replace with useful outputs: budget structure, cash-flow planning, tender comparison, programme review.
- If simulated financial outcomes remain on the worked-example page, label them "modelled" beside the figures, incl. charts, tables and mobile layouts.
- Keep distinct: published plot information vs planning assumptions vs invented events. Draft development controls are draft.
- Do not describe assumed infrastructure access or construction dates as confirmed developer commitments.
- Titles, descriptions, social previews, structured data must not imply a completed UAE client project.
- Preserve URLs where practical; if changed, add 301 and update internal links, canonical, hreflang, sitemap.
Lead track-record evidence with actual UK projects. Where records support it, expand one into a genuine case study (brief, Philip/P Chapman Construction's role, constraints, work delivered, documented outcome). Attribute UK contracting experience accurately; never as an Eastbridge UAE owner's-rep appointment.

## 2. Make the worked budget complete and transparent
Final-account table adds up, but what the headline total covers is unclear: Eastbridge fee excluded; VAT, plot acquisition charges and escalation not carried into the overall picture.
- Consistent breakdown: plot cost, acquisition/registration charges where applicable, design and consultant fees, approvals and connections, construction, basement, pool/landscape, contingency, Eastbridge fees, VAT treatment, furniture and other exclusions.
- Separate quantified allowances from costs awaiting quotation/confirmation. Never silently treat an unknown fee or tax as zero.
- If not every cost is quantified, label the sum as a subtotal of stated allowances, not an all-in budget.
- State price base date, assumed construction period and whether escalation is included. Do not invent an escalation rate.
- Use tax/transaction assumptions supported by current authoritative sources; do not apply a generic percentage to every line.
- Modelled cost avoidance is a hypothetical comparison, not a demonstrated return on Eastbridge's fee. No double counting of savings, contingency and underspend.
- Reconcile tables, charts, annual cash flows and headline figures after editing.

## 3. Clarify UAE delivery arrangements
Pages: /about/, /approach/, /services/owners-representative/, relevant FAQs, homepage.
Explain using verified info: who leads and who attends site; how site attendance and reporting are agreed in scope; how registered consultants, QSs, engineers and specialists are appointed when needed; who covers when the lead is unavailable; how capacity is managed across several projects; boundaries between Eastbridge's commercial/PM role and statutory design, submissions, supervision and legal advice.
Only name partners, staff, credentials, insurance or licence activities with owner evidence and permission. No invented UAE team or UAE projects. If facts are missing, keep accurate existing wording and add precise questions to the owner-input list. Sample templates must be labelled samples; the worked example's model report is not an actual client report.

## 4. Make the first purchase and enquiry clearer
Pages: /fees/, /contact/, service CTAs, shared navigation. "Typical fee" column repeatedly says "quoted on request".
- Present a clear initial service: plot/pre-purchase review or project health check, with scope, deliverables, exclusions, pricing method, turnaround if confirmed.
- Publish an indicative price only when owner supplied/approved it. Never invent a rate. (Note: src/config.py FEES exist but PUBLISH_FEES=False — owner has not approved publishing; keep hidden.)
- If prices unavailable, replace the repetitive "Typical fee" column with scope and how the quotation is determined. Missing pricing decision -> owner-input list.
- Explain relationship between free introductory call, paid first review and subsequent appointment.
- Primary CTA more understandable, e.g. "Arrange a free 30-minute call", linking to the existing enquiry route (no real booking system exists). Do not imply instant booking if the form only requests a reply.
- Keep WhatsApp; preserve phone +971 56 744 0057 and enquiries@eastbridgepartners.ae.
- Keep the form's three required items clear; optional stage, location, budget, preferred contact fields must not look compulsory.
- Preserve promised reply time only if it is an operational commitment (owner-input to confirm).

## 5. Shorten the homepage and improve the tone
Cut repetition by roughly one third, using judgement.
Order: 1) proposition + primary contact action; 2) concise substantiated founder/track-record evidence; 3) three routes: new build, renovation, troubled project; 4) one strong real project example or portfolio selection; 5) short appointment process + independence; 6) owner questions + final contact action.
Keep details on their own pages. Remove duplicated service grids and repeated "21 years" / "paid only by the owner" statements where they add little.
Review ALL pages for absolute/unsupported promises: delivery on time, guaranteed budgets, guaranteed dispute outcomes, "an avoided variation will typically exceed the fee" without evidence. Describe controls: cost reporting, programme monitoring, payment review, decisions, records, early risk management. Persuasive without guarantee.
Revise claims that only Eastbridge is paid to protect the owner's money or that consultants care only about design/compliance. Explain the additional independent coordination and commercial scrutiny while recognising the duties of properly appointed consultants and contractors. Collaborative and fair tone.

## 6. Fix calculator localisation and renovation behaviour
Pages: /tools/villa-build-cost-calculator/ + ar, ru, zh, hi. Script source: src/static/assets/calc.js; page: src/pages_tools.py.
Defect: dynamic labels, output explanations, timeline descriptions and instructions render in English on non-English pages (hard-coded English in shared JS).
- Move all generated user-facing text into the locale system or a per-locale dictionary. Cover initial render and every change of project type, specification, location, units, extras. Translate zero/not-included states, renovation scope descriptions, timelines, approvals explanations, chart legends, accessibility labels. Numbers, units, currencies and Arabic direction readable. Preserve sq ft/sq m conversion: switching units preserves underlying quantities and estimate within rounding.
Renovation logic: basic and mid-range renovation bands do not scale with area. Do not invent a size formula or unsupported rates. If no validated size model exists in project records, present those bands as generic whole-villa scope examples and adjust area input/results so they do not imply area-specific accuracy; an unsupported scenario prompts a project-specific assessment. Keep exclusions, assumptions and estimate-not-quotation near the output. Reconcile totals with cost lines; optional extras consistent when switching modes.

## 7. Align privacy and marketing choices
Pages: /privacy/, /guides/villa-owner-checklist/, newsletter, enquiry form, thank-you pages, translations.
Inconsistency: privacy notice says info is used for enquiries and services; checklist form says details used for occasional marketing notes.
- Make enquiry handling, checklist delivery and marketing descriptions consistent with actual systems.
- Marketing = clear separate choice: unchecked optional opt-in. Enquiry/checklist proceeds without it. Keep a working standalone newsletter route.
- New consent field must be captured by the form handler (Netlify forms + netlify/functions/submission-created.js) and respected downstream (e.g. only opted-in leads flagged for marketing in the sheet/log). A checkbox alone is not enough.
- Accurate unsubscribe wording; do not claim automation that does not exist. No analytics/ad tracking added. Final legal wording flagged for owner/legal review.

## 8. Strengthen sources and project attribution
References: https://www.johnpardeyarchitects.com/modern-architecture/one-off-houses-architecture/owers-house/ ; https://www.labc.co.uk/news/labc-south-west-winners-amp-highly-commended-2020
- Link award and project-team evidence beside the claims. Credit architects and project teams as well as photographers. Distinguish an architectural award for a house from a personal award to Philip or Eastbridge.
- Name the Grand Designs property/episode only when verified. Do not embellish.
- Exact substantiated dates/outcomes; omit unsupported project values, savings, floor areas, durations.
- Check high-impact regulatory statements against current official authority sources. Keep Dubai and Abu Dhabi routes distinct; draft plot controls qualified. Prefer original reports/authority guidance.
- KPMG 31% budget / 25% deadline statistics are from the 2015 Global Construction Survey (organisations with substantial capital projects worldwide) — historical context, not Dubai villa data. Reduce prominence, label year and scope beside them, or remove. Original: https://assets.kpmg.com/content/dam/kpmg/pdf/2015/04/Global-Construction-Survey.pdf

## 9. Preserve the technical foundation
Baseline at review: 375 sitemap URLs 200; 416 resources OK; unique titles, descriptions, canonicals, alt; JSON-LD parses; no broken fragments; form validation incl. phone required when WhatsApp selected; unit switching works; Quay House film plays.
Preserve routes, internal links, language alternates, metadata, sitemap, responsive images, form handling, accessible labels, keyboard focus, reduced-motion.
Canonicals point to https://www.eastbridgepartners.ae/ — do not change domain config. Keep preview indexing environment-specific; never noindex production. No DNS changes.

## 10. Verify and report
Build + existing checks (python3 build.py && python3 tools/i18n.py apply && python3 tools/seo_audit.py). Targeted checks for calculator/form behaviour; no large new test framework.
Verify: en/ar/ru/zh/hi of changed shared components; worked-example disclosures on cards, headers, numbers, charts, metadata; financial totals, exclusions, unit conversions, mode switching; no untranslated dynamic calculator text; enquiry validation and preferred-contact; checklist/newsletter choices, field capture, thank-you routes; navigation, links, downloads, video; 360/390/768 px and desktop plus Arabic RTL (menu, overflow, tables, labels, contact buttons); titles, descriptions, canonicals, hreflang, sitemap, structured data.
Do not send live enquiries or subscribe real addresses. Email delivery = unverified. Do not claim launch-ready.
Finish with: summary; files changed + build instructions; checks + limitations; owner-input list.
