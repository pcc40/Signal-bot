# Brief for Claude Code: improvements after reviewing Real Estate Club Dubai

Repository: `pcc40/eastbridge-website`, branch `main`. Live: https://eastbridgestrategicpartners.com (Netlify deploys on every push to `main`).
Reviewed: 1 November 2026, against https://realestateclubdubai.com (RECD), in particular
`/tools/villa-build-cost-calculator`, `/dubai-villa-architects` and
`/blog/buying-selling/snagging-inspection-dubai-complete-checklist-before-accepting-your-property-2026`.

Read `HANDOFF.md`, `AUTOMATION.md`, `src/content/WRITING_BRIEF.md` and `src/i18n/TRANSLATION_BRIEF.md` first; their rules override anything below.

## Rules for every change

- Eastbridge is a client-side project manager and owner's representative. Never an engineer, architect, contractor or design consultant. Never claim UAE projects or existing Eastbridge clients. No client names, invented figures, reviews or awards. Eastbridge takes no commissions or referral fees, so no "get matched" or referral mechanics.
- Every new or changed English string must be translated into Arabic, Russian, Chinese and Hindi (the Languages steps in `AUTOMATION.md`); `node tools/calc_check.js --strict` must pass for calculator text.
- Before pushing: `python3 build.py && python3 tools/i18n.py apply`; `python3 tools/seo_audit.py` reports 0 errors and 0 warnings; `python3.11 -m py_compile build.py tools/*.py src/*.py` passes (Netlify builds on Python 3.11).
- After `site.css` changes run `sh tools/make_rtl.sh` and check `/ar/` at mobile and desktop widths.
- Check the live deploy published, then run `python3 tools/indexnow.py` with the changed URLs.

## What RECD is

A Dubai property information and lead-referral platform (operator: a Turkish company, Reaktör Teknoloji). Not a licensed brokerage. About 20 calculators, a "Find a Pro" directory with paid lead partnerships, an iPhone app, a handover tracker, an AI chat, Telegram and WhatsApp channels, and a large blog (about 215 articles). English only. No named authors, few sources, several internal inconsistencies. It monetises by passing leads to partner firms.

Its calculator and its architects page target the same searches we do ("villa build cost Dubai", "cost to build a villa in Dubai", "villa snagging Dubai").

## Calculator comparison

| | RECD | Eastbridge |
|---|---|---|
| Modes | New build only | New build **and** renovation |
| Locations | None (one Dubai rate) | 8 Dubai communities plus Abu Dhabi, each with its approval route |
| Units | sq ft | sq ft and m² |
| Result | One total | Low, likely and high, line by line |
| Inputs | Area, finish tier, FF&E toggle, approvals toggle | Area, tier, basement, garden, pool, smart home, FF&E, demolition |
| Timeline | Shown, value unclear | Phase-by-phase timeline |
| Sources | 3 linked, 1 unlinked | Every rate footnoted |
| Methodology, FAQ, schema | Methodology only; no FAQ; no JSON-LD | Worked example, FAQ, WebApplication + FAQPage + Breadcrumb schema |
| Author or date | None | Named founder, dated |
| Languages | English | 5 |
| **Currency switch** | **Yes (approximate)** | No |
| **Email capture tied to the tool** | **"Send me the checklist"** | Newsletter form only |
| **Embeddable widget** | **Yes (iframe, "View all widgets")** | No |
| WhatsApp | Pre-filled about the calculator | Generic pre-filled message |

Their rates are close to ours (standard 350–500, premium 600–850, luxury 850–1,200, ultra 1,200+ AED/sq ft; design 9%; FF&E 35%; contingency 12%; approvals AED 25–75k). Their page applies a fixed 35% FF&E while quoting a 30–40% range, gives no defaults, and does not say what the contingency is applied to. Ours is more accurate and more transparent. The gaps are features that help people **use and share** the result.

## Recommended changes, in priority order

### 1. Calculator: currency display (high)
Overseas owners (UK, Russia, India, China) think in their own currency.
- Add a currency selector: AED (default), GBP, USD, EUR, plus RUB on `/ru/`, CNY on `/zh/` and INR on `/hi/`. Default to AED on every page; the extra currencies are options, not defaults.
- AED remains the calculation currency; other currencies are display-only conversions.
- Use a fixed rate table in `src/pages_tools.py` (`FX`, with an "as at" date and a cited source, for example the UAE Central Bank's published rates). No live API calls.
- Show "approximate, at rates of <date>" beside converted figures. Keep the rate date in the methodology section.
- The AUTOMATION monthly step should refresh `FX` and its date (add a line to `AUTOMATION.md`, Monthly).

### 2. Calculator: share, save and send (high)
- **Shareable link.** Write the inputs to the URL query string (`history.replaceState`) and read them on load, so an estimate can be sent to a spouse, lender or adviser. Add a "Copy link" button.
- **Print or save as PDF.** A "Save as PDF" button using `window.print()` with a print stylesheet that prints only the inputs, the line-by-line result, the timeline, the date, the sources note and the Eastbridge contact line. Make it clean and professional, like a surveyor's one-page estimate; it must not look auto-generated.
- **WhatsApp with the estimate.** Pre-fill the WhatsApp link with a one-line summary, for example "Hello, I used your calculator: 6,000 sq ft, premium, Dubai Hills, likely AED 6.4m. Could we talk it through?"
- **"Send this estimate to Philip".** A short Netlify form (name, email, optional phone, optional plot location and notes) that submits the inputs and result as hidden fields. Use the existing `brief` form, or a new form name added to `netlify/functions/submission-created.js` and to `HANDOFF.md`. The thanks page should promise a personal reply within one working day.

### 3. Second lead magnet: printable villa snagging checklist PDF (high)
RECD's snagging article has inline tables but **no downloadable checklist**. Ours is villa-specific.
- Build `villa-snagging-checklist.pdf` the same way `tools/make_checklist_pdf.py` builds the pre-construction checklist (same design system; professional, not AI-looking).
- Gate it like `/guides/villa-owner-checklist/`: add `/guides/villa-snagging-checklist/` and `/guides/villa-snagging-checklist/thanks/`, with a `checklist` form submission.
- Link it from `/insights/villa-snagging-checklist-dubai/` and from the snagging service page.

### 4. Snagging article: make it the better answer (medium)
`/insights/villa-snagging-checklist-dubai/` is about 2,200 words with 1 table; RECD's is about 3,300 words with about 10 tables. Do not pad. Add only sourced material:
- A table of the handover documents to collect, with who issues each.
- A defect severity table (critical, major, minor), with villa examples and what to ask for.
- A table of the defects-liability position: structural vs non-structural periods, with the official source. RECD contradicts itself on whether the 10-year period runs from handover or from the completion certificate; state the correct position with a primary citation (UAE Civil Code art. 880, Dubai Land Department guidance).
- Keep "Key points" at the top (our equivalent of their TL;DR); make sure it gives the main figures in one place.

### 5. Primary sources instead of a competitor (medium)
`src/pages_tools.py` cites RECD (`"reca"`) for design fees, contingency and timelines. Linking to a competitor sends it authority, and its page has no named author or primary data.
- Replace or supplement it with primary or industry sources, for example Turner & Townsend International Construction Market Survey (Dubai), AECOM Middle East Property & Construction Handbook, Arcadis International Construction Costs, and RIBA/Dubai Municipality guidance on design-fee scope.
- Keep every figure traceable; if a figure changes, update the worked example, FAQ and translations.

### 6. Embeddable calculator for referral partners (medium)
RECD offers its calculators as free iframe widgets. That puts its brand and link on other sites.
- Add `/tools/villa-build-cost-calculator/embed/`: the calculator only, a compact layout, and a visible "Calculator by Eastbridge Strategic Partners" link back to the full page.
- `noindex` on the embed page, `canonical` to the full calculator, and no other navigation.
- On the full page, add an "Add this calculator to your website" box with the iframe code, aimed at agents, architects and lawyers in `business/outreach-kit.md`. Add a line to the outreach kit offering it.

### 7. New tools that match our positioning (medium; one at a time)
RECD wins on breadth (about 20 tools). We should not copy investment calculators. Add tools only an owner's representative would build:
1. **Renovate or rebuild?** Compares renovation and knock-down-and-rebuild on cost per sq ft of finished space, time and approvals. It matches the next topic in `src/content/TOPICS.md` (`renovate-or-rebuild-villa-dubai`), so publish both together.
2. **Stage payment and cash-flow planner.** Spreads a build budget over a typical payment schedule (advance, milestone payments, retention, release) so owners can see their monthly exposure.
3. **Delay cost estimator.** What a month's delay costs an owner (rent or hotel, finance, price escalation, extended fees), with a link to the stalled-project article.

Each tool: sourced rates, low/likely/high, FAQ, WebApplication schema, all five languages, linked from `/tools/`.

### 8. Calculator trust details (low effort)
- Add "Rates last reviewed: <month year>, by Philip Chapman" near the result, and keep it current from the monthly AUTOMATION step.
- When the LinkedIn company page exists, add it to `SOCIAL` and to the `Person` schema for Philip (`sameAs`).

### 9. SEO engine: add RECD to the competitor watch (low effort)
In `AUTOMATION.md`, Daily step 4, add `realestateclubdubai.com` (blog and tools) to the competitors list. It ranks for several of our target searches.

## What we already do better (keep it this way)

- Named, dated, sourced content by a person with 21 years as a builder; RECD has no authors.
- Villa-specific, owner-side advice; RECD's content is buyer- and investment-led and mostly about apartments.
- Five languages with hreflang; RECD is English only.
- No lead selling; RECD's forms say data may be shared with partners. Say "We never pass your details to contractors or suppliers" next to our forms, if it is not already there.

## Not recommended

- Copying their directory, paid listings, "Get matched" referrals, app, Telegram channel, AI chat or investment calculators. They conflict with Eastbridge's independence or are off-brand.
- Matching their article count. `AUTOMATION.md` caps output at two quality articles a week, on purpose.

## Done when

- Items 1–3 are live in all five languages, `seo_audit.py` reports 0 errors and 0 warnings, and `calc_check.js --strict` passes.
- A test submission from each new form arrives in Netlify Forms.
- `HANDOFF.md` lists the new pages, forms and the FX update step.
