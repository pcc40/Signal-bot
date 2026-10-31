# Eastbridge: off-site authority and citations kit

Prepared 31 October 2026 for Philip Chapman. Ready-to-paste copy for profiles, directories, press and video. Nothing here has been submitted or published anywhere.

**Why this matters.** Google's local results and AI assistants (ChatGPT, Perplexity, Gemini, Google AI Mode, Copilot) decide who to trust partly from what other sites say about a business. They check that the name, address and phone are identical everywhere, that the business is listed where its peers are listed, and that reputable publications quote it. The website is necessary but not enough on its own.

**Ground rules for everything in this kit** (from `src/content/WRITING_BRIEF.md`):

- Say "client-side project manager" first. "Owner's representative" is a synonym.
- Say "we represent the owner, alongside the owner's DM-registered consultant and the contractor".
- Never say Eastbridge supervises, is the engineer, architect, contractor or consultant of record, obtains or submits permits, certifies, prepares tender documents or prequalifies contractors.
- Never claim or imply UAE projects or existing Eastbridge clients. The Island E case study is illustrative and must always be labelled that way. No client names.
- UK photographs show work built by P Chapman Construction in Cornwall, UK. Always caption them that way.
- No invented statistics, reviews, testimonials, rankings, "as seen in" or "#1/best" claims. British English, calm voice, no emojis, no exclamation marks.
- **Timing:** the competitor report (business/seo-competitor-report.md) found eastbridgestrategicpartners.com not yet responding on 31 Oct 2026. Create listings only once the site is live, so every listing links to a working page.

---

## 0. NAP consistency sheet (use these exact strings everywhere)

Source: `src/config.py`. Copy and paste these strings. Do not retype them. If any value changes in `config.py`, update every listing in the tracker at the end of this section.

| Field | Exact string |
|---|---|
| Business name (public) | `Eastbridge Strategic Partners` |
| Short name (body copy only, never the listing name) | `Eastbridge` |
| Legal name (invoices, chamber, licence-based directories) | `Eastbridge Strategic Partners L.L.C-FZ` |
| Licence | `Meydan Free Zone licence 2540153.01` |
| Address, one line | `Business Centre, Meydan Grandstand, 6th Floor, Meydan Road, Nad Al Sheba, Dubai, United Arab Emirates` |
| Address line 1 | `Business Centre, Meydan Grandstand, 6th Floor` |
| Address line 2 | `Meydan Road` |
| Area / locality | `Nad Al Sheba` |
| City | `Dubai` |
| Country | `United Arab Emirates` (code `AE`) |
| Phone (display) | `+971 56 744 0057` |
| Phone (E.164, for forms that strip spaces) | `+971567440057` |
| WhatsApp | `https://wa.me/971567440057` |
| Email | `philip@eastbridgestrategicpartners.com` |
| Website | `https://eastbridgestrategicpartners.com` (always with `https://www.`, no trailing path, unless a field asks for a specific page) |
| Hours | `Monday to Friday, 9am–6pm Gulf Standard Time` (Saturday and Sunday closed) |
| Founder | `Philip Chapman, Founding Partner` |
| Founder's UK company | `P Chapman Construction` – `https://www.pchapmanconstruction.com/` |
| Instagram | `https://www.instagram.com/eastbridgestrategicpartners/` |
| Response promise | `A personal reply from Philip within one working day` |

**Rules**

1. Never add keywords to the name ("Eastbridge Strategic Partners – Villa Project Management Dubai" breaks Google's naming rules and can get a profile suspended).
2. Use the same phone number everywhere. Do not use a different tracking number on one directory.
3. If a form has no "area" field, put `Nad Al Sheba` before `Dubai` on the city line.
4. If a directory insists on a P.O. Box, leave it blank rather than invent one.
5. After creating each new profile (LinkedIn, Facebook, Houzz, Crunchbase and the rest), add its URL to `SOCIAL` in `src/config.py`. The site's Organization schema outputs that list as `sameAs`, which is how Google and AI systems connect the profiles to one entity. Rebuild and redeploy after each addition.

**Citation tracker (fill in as you go)**

| Platform | Profile URL | Date created | NAP checked | Added to `SOCIAL` |
|---|---|---|---|---|
| Google Business Profile | | | | n/a (not a sameAs) |
| Bing Places | | | | n/a |
| Apple Business | | | | n/a |
| LinkedIn company page | | | | |
| Instagram | https://www.instagram.com/eastbridgestrategicpartners/ | existing | | yes |
| Facebook page | | | | |
| (continue for each directory in section 3) | | | | |

---

## 1. Google Business Profile (GBP)

### 1.1 Verification risk: read this before creating the profile

Google's guidelines (https://support.google.com/business/answer/3038177) say:

- "Businesses can't list an office at a co-working space unless that office maintains clear signage", receives customers during business hours and is staffed by the business's own staff during those hours.
- A rented mailing address where the business does not operate is "not eligible for a Business Profile".
- "Service-area businesses can't list a 'virtual' office unless that office is staffed during business hours."

The Meydan Grandstand Business Centre address is a free-zone business-centre address. Unless Eastbridge has a dedicated, signed office there that Philip staffs and where clients can visit during the stated hours, **listing it as a storefront address is likely to fail verification, or to be suspended later**. Google increasingly verifies by video, which means filming the signage, the office and proof of the business at that location.

**Recommended route (compliant):**

1. Set the profile up as a **service-area business**, with the address hidden from customers. The address entered for verification must be somewhere Philip actually works from. For a home-based business that is allowed, provided it stays hidden.
2. Service areas: `Dubai`, `Abu Dhabi`. Optionally add named communities later (Palm Jumeirah, Emirates Hills, Saadiyat Island). Google allows up to 20 service areas. Keep them to places Eastbridge would genuinely travel to.
3. Because the address is hidden, the public listing shows name, phone, website and hours only. The website and directories keep the Meydan address. That is consistent: a hidden address does not create a NAP conflict.
4. If Eastbridge later takes a dedicated, signed and staffed office, switch to a visible address at that point.

**Do not** create a second profile, use a different address to "get round" verification, or ask anyone to suggest edits. Duplicates and address workarounds are the most common causes of suspension.

### 1.2 Categories (verified against Google's category list)

Checked on 31 Oct 2026 against two current extracts of Google's GBP category list (Pleper's category tool and daltonluka.com's 2026 list). **Google has no "Project management company", "Construction management company" or "Owner's representative" category.** The closest available categories are compared below. Confirm the final choice in the GBP category field itself, because labels vary slightly by locale. Pleper's UK-English extract shows "Real estate consultant" as "Property Consultant".

| Category | Use? | Reason |
|---|---|---|
| **Building consultant** | **Primary (recommended, subject to the legal check below)** | Closest match to independent, client-side construction advice for homeowners. Shown for construction-advice searches without saying we build. |
| **Real estate consultant** | Secondary | Fits plot and pre-purchase review and development advisory. Matches a large share of overseas-owner searches. |
| **Consultant** | Secondary (optional) | Generic, low risk, adds little. Use only if a third category is wanted. |
| Construction company | **Do not use** | Tells Google and users that we build. We do not. |
| General contractor / Home builder / Custom home builder / Remodeler | **Do not use** | Same problem: these are contractor categories. |
| Engineering consultant | **Do not use** | Under Dubai Law No. 14 of 2025 only DM-registered consultancies may present themselves as engineering consultants. |
| Architect / Architecture firm / Building designer | **Do not use** | We do not design. |
| Building inspector / Home inspector | **Do not use** | Implies statutory inspection or certification. |
| Quantity surveyor / Surveyor | **Do not use** | Professional titles that imply a qualification (for example RICS) Eastbridge does not hold. |
| Property management company | **Do not use** | Means letting and managing tenanted property. Wrong intent. |

> **Legal check before choosing "Building consultant".** The word "consultant" is sensitive under Dubai Law No. 14 of 2025 (summary: https://www.tamimi.com/news/dubai-issues-new-law-regulating-engineering-consultancy-activities-key-takeaway-points/). "Building consultant" is not "engineering consultant", but take a view from a UAE-qualified lawyer, and check that the category sits comfortably with the activities on the Meydan Free Zone licence. If in doubt, make **Real estate consultant** primary and leave "Building consultant" out. The description and services still do the work of explaining what we do.

### 1.3 Business description (paste as is; 733 characters including spaces, under the 750 limit)

```
Eastbridge Strategic Partners is an independent, client-side project manager for private villa builds and renovations in Dubai and Abu Dhabi. We represent the owner, alongside the owner's DM-registered consultant and the contractor: cost and programme control, help comparing bids like-for-like, independent site visits with plain-English reports, and commercial advice on variations and delay claims. Our founder, Philip Chapman, ran P Chapman Construction, a UK premium residential builder, for 21 years, so we know where budgets leak and what contractors hope clients will not check. We are paid only by the owner: no commissions or referral fees from contractors or suppliers. A personal reply from Philip within one working day.
```

(Google forbids URLs, prices and promotional claims in the description. This text contains none.)

### 1.4 Services (GBP "Services" section: custom services, name plus description up to 300 characters)

Each description stays within the brief's wording. Paste one per service.

1. **Owner's representation for villa builds**: We represent the owner from plot to keys, alongside your DM-registered consultant and contractor. One independent adviser on your side for budget, programme, quality and decisions.
2. **Villa construction project management (client-side)**: Client-side management of a bespoke villa build: cost and programme control, decision logs, monthly reporting and commercial advice, so the project lands on budget, on time and as you imagined it.
3. **Villa renovation and extension project management**: Planning for the three things that break renovation budgets (hidden water damage, services that cannot be reused and structure that differs from the drawings) before the first wall comes down.
4. **Villa plot and pre-purchase review**: Before you buy a plot: realistic build cost, design rules, build-by deadlines and the approval route with Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where the plot sits.
5. **Design brief, budget and approvals management**: We help you set a clear brief and budget, keep design cost under watch, and track the approvals your consultant is pursuing, so delays and cost creep are visible early.
6. **Help choosing your consultant and contractor**: We help you compare bids like-for-like, check references and understand contract terms, so you can make the appointment with a clear view of cost and risk. You choose and appoint.
7. **Cost and programme control**: Every month you see what you have paid, what you have committed and what it will cost to finish, with the programme tracked against the contract dates.
8. **Independent site visits and progress reporting**: Client-side site visits with photos and a plain-English report written for you. Your consultant keeps their statutory duties. We report to you, independently.
9. **Variations, delays and claims advice**: Commercial advice on variations and extension-of-time claims from a team that spent two decades preparing and defending them. For legal questions we will recommend you take advice from a UAE-qualified lawyer.
10. **Stalled and troubled project recovery**: When a contractor walks off or a budget runs out halfway: an honest review of the contract, records and money, and a practical plan to get the villa finished.
11. **Snagging and handover management**: We make sure the house is finished before you accept it: snag lists, close-out tracking, documents and the defects period, managed from the owner's side.
12. **Representation for overseas owners**: For owners living in the UK or elsewhere: a named person in the UAE, regular honest reporting, and no decision made without you.
13. **Development advisory**: For small developers and investors: plot-to-sale villa projects, small residential schemes and build-to-rent, with a developer-builder's discipline on numbers and delivery.

Do not add prices while `PUBLISH_FEES = False` in `config.py`.

### 1.5 Questions and answers (10 pairs)

**Note on the Q&A feature.** Google discontinued the GBP Q&A API on 3 November 2025 and has been replacing public Q&A with an AI "Ask" feature in Maps that answers from the profile's description, posts, reviews and website (sources: https://ppc.land/google-discontinues-business-profile-q-a-api-effective-november-3/ ; https://www.brightlocal.com/learn/google-business-profile-qa). If the Q&A box is still offered on the profile, post these as owner questions and answers. If it is not, use them in three ways: (a) make sure each answer is on the website (most already are, in the service FAQs), (b) turn them into GBP posts, (c) reuse them on Bing Places, Facebook and LinkedIn. AI answer features draw on all of these.

1. **Q: Are you a contractor or an engineering consultant?**
   A: Neither. Eastbridge is an independent, client-side project manager. We represent the owner, alongside the owner's DM-registered consultant and the contractor. We do not design, build or supervise construction, and we take no fees from contractors or suppliers.
2. **Q: What does a client-side project manager actually do on a villa build?**
   A: We look after the owner's interests from plot to keys: setting the budget and programme, helping you compare bids like-for-like, tracking cost every month, visiting site independently and reporting in plain English, and advising on variations and delay claims.
3. **Q: Do I still need a consultant if I appoint you?**
   A: Yes. Your DM-registered consultant designs and has the statutory duties, including supervision and permit submissions. We sit on your side of the table and work alongside them and the contractor.
4. **Q: Which areas do you cover?**
   A: Private villa builds and renovations across Dubai and Abu Dhabi, including Palm Jumeirah, Emirates Hills, Jumeirah Bay, District One, Dubai Hills Estate, Al Barari, Dubai Islands, Palm Jebel Ali, Saadiyat and Hudayriyat.
5. **Q: I live in the UK. Can you represent me while I am abroad?**
   A: Yes. Representing owners who live overseas is a core part of our work: a named person in the UAE, regular honest reporting, and no decision made without you.
6. **Q: Can you help before I buy a plot?**
   A: Yes. A plot review looks at realistic build cost, design rules, build-by deadlines and the approval route with Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where the plot sits.
7. **Q: My project has stalled. Can you help?**
   A: Yes. We review the contract, the records and the money, tell you honestly where you stand, and set out a plan to get the villa finished. Where the issue is legal, we will recommend you take advice from a UAE-qualified lawyer.
8. **Q: How do you charge?**
   A: Fixed fees for reviews, and a monthly or percentage fee during construction, agreed in writing before we start. Our only income on your project is the fee you pay us.
9. **Q: What is your background?**
   A: Our founder, Philip Chapman, ran P Chapman Construction, a UK premium residential builder, for 21 years. Its homes won a RIBA South West Award (Owers House, 2016), an LABC Building Excellence Award (2018 winner) and a Highly Commended in 2020, were reported in The Times and featured on Channel 4's Grand Designs.
10. **Q: How quickly will you reply?**
    A: A personal reply from Philip within one working day. Office hours are Monday to Friday, 9am–6pm Gulf Standard Time.

### 1.6 First eight GBP posts

Google posts allow up to 1,500 characters. Keep them to 100–250 words with one button. Link each to the matching page on the site. Publish one a week. Where a post uses a UK photograph, the caption line is part of the post text and must stay in.

**Post 1: Introduction** (button: Learn more, `/`)
> Eastbridge Strategic Partners is now open in Dubai. We are an independent, client-side project manager for private villa builds and renovations in Dubai and Abu Dhabi. We represent the owner, alongside the owner's DM-registered consultant and the contractor. Our founder, Philip Chapman, spent 21 years running P Chapman Construction, a UK premium residential builder. We spent two decades as the builder. Now we sit on the client's side of the table.
> *Photo: Philip Chapman (portrait).*

**Post 2: Where budgets leak** (button: Learn more, `/services/cost-and-programme-control/`)
> Every month a villa owner should know three numbers: what has been paid, what has been committed, and what it will cost to finish. Most owners only know the first. Client-side cost control means a monthly forecast of the final cost, every variation priced before it is instructed, and no surprises at the final account.

**Post 3: Who does what** (button: Learn more, `/insights/owners-representative-vs-project-manager-vs-consultant/`)
> Consultant, contractor, project manager, owner's representative: who does what on a Dubai villa? Your DM-registered consultant designs and carries the statutory duties. Your contractor builds. A client-side project manager represents you, alongside both, with no fee from either. Our guide explains the difference.

**Post 4: UK work, honestly labelled** (button: Learn more, `/work/`)
> Built by P Chapman Construction, Cornwall, UK, the company our founder ran for 21 years. Owers House on the Fal estuary won a RIBA South West Award in 2016 and was reported in The Times. These are UK projects. They show the standard of building we know how to judge from the owner's side.
> *Photo: Owers House, Feock, Cornwall, UK. Built by P Chapman Construction. Photograph: James Morris.*

**Post 5: Before you buy a plot** (button: Learn more, `/services/plot-due-diligence/`)
> The plot price is the number everyone talks about. The build cost, the design rules and the build-by deadline decide whether it is a good purchase. A plot review before you commit sets out a realistic budget and the approval route, with Dubai Municipality, Trakhees or the Dubai Development Authority depending on where the plot sits.

**Post 6: Renovation** (button: Learn more, `/services/villa-renovation-project-management/`)
> In 21 years of altering and extending houses, the expensive surprises were almost always the same three: water where it should not be, services that could not be reused, and structure that was not what the old drawings showed. Opening up a few areas before the price is agreed costs very little and saves a great deal.
> *Photo: Menwinnion, Mylor Churchtown, Cornwall, UK: extension and full refurbishment by P Chapman Construction.*

**Post 7: Owners overseas** (button: Learn more, `/services/overseas-owners/`)
> Many villa owners are not in Dubai most of the time. The project still needs decisions every week. We were the builder for UK owners who lived away from their sites. What worked then still works: a named person on site and a regular, honest report.
> *Photo: Blue Seas, Constantine Bay, Cornwall, UK. Built by P Chapman Construction for owners living away. Photograph: Hugh Hastings.*

**Post 8: Illustrative case study** (button: Learn more, `/case-studies/island-e-waterfront-villa/`)
> What does a client-side project manager change on a waterfront villa? Our illustrative case study, an example rather than a real project, walks through a typical island villa build from plot review to handover. It shows where cost and programme risk usually sit and what the owner sees each month.

### 1.7 Photo plan

**GBP photos have no captions.** A UK project photo uploaded on its own to a Dubai profile would show users what looks like a Dubai villa with no explanation. That conflicts with the honesty rule. So:

| Slot | What to upload | Notes |
|---|---|---|
| Logo | `src/static/assets/logo.png` (square crop, at least 250×250 px) | |
| Cover | A neutral brand image: Dubai skyline or plot context photographed by Philip, or a brand graphic | Not a UK house. A cover photo reads as "this is the business". |
| Team | Philip Chapman portrait; Philip on a Dubai site visit once there is real, consented UAE work to show | Never stage a "site visit" photo on a project Eastbridge is not involved in. |
| At work | Photos of Eastbridge sample templates (monthly report, cost tracker, snag list), each labelled 'Sample template – illustrative data'. Never describe them as redacted client documents. | These show the service without implying projects. |
| UK portfolio | **Only inside Posts** (as in posts 4, 6 and 7), where the text says "Built by P Chapman Construction, Cornwall, UK" | Use the 1280 px WebP versions in `src/static/assets/img/` converted to JPG (GBP accepts JPG/PNG, 10 KB–5 MB, at least 720×720 px recommended). |

**Rights:** many UK photos have a named photographer (Hugh Hastings, James Morris, Andrew Meredith, Panoptic, Bad Wolf Horizon; see the `photo` field in `src/content/projects.py`). Before posting them on third-party platforms (GBP, Houzz, LinkedIn, Facebook, press), confirm the licence covers that use. Credit the photographer in the post text where possible.

Suggested UK images for posts: `owers-house` (RIBA South West Award 2016), `polgreen-manor` (LABC 2020 Highly Commended, new-build joined to restoration), `old-station-masters-house` (LABC 2018 winner), `blue-seas` (owners living away), `menwinnion` (extension and refurbishment), `gooden-heane` (exposed coastal site).

### 1.8 Review-request process (never incentivised, never fake)

Google prohibits fake reviews, reviews written by the business, reviews offered in exchange for anything, and "review gating" (asking only happy clients). Breaches can remove all reviews or suspend the profile.

**Who may review Eastbridge on GBP:** only people who have received an Eastbridge service: a client, or someone who had a paid plot review or rescue review.

**Who may not:** former clients of P Chapman Construction, architects Philip worked with as a builder, friends or family. Their experience is of P Chapman Construction, not Eastbridge. A Google review from them would mislead. They can instead write a **LinkedIn recommendation for Philip personally**, which describes his work honestly in its true context.

**Process**

1. **When to ask:** at a natural milestone: delivery of a plot review report, the end of a project stage, or handover. Never during a dispute or before an invoice is settled.
2. **Ask everyone you serve**, in the same neutral words. Do not screen for happy clients first.
3. **Message (email or WhatsApp; paste and personalise the first line):**
   > Thank you for asking us to work with you on [stage/report]. If you are willing, a short Google review describing your experience, good or bad, helps other owners decide whether we are right for them. Here is the link: [GBP review link]. There is no obligation, and it makes no difference to our work together.
4. Get the review link from GBP: Home → "Ask for reviews" → copy the link.
5. **Never** offer a discount, gift, donation or anything else for a review. Never draft the review for the client. Never post from a staff device or office Wi-Fi on the client's behalf.
6. **Reply to every review** within a week: thank them, add one specific, factual point, no client details. For a critical review, acknowledge it, give the facts calmly, offer to talk offline. Never disclose project or fee details.
7. Do not publish reviews on the website as "testimonials" unless the client has given written consent to that specific use.

Until the first client engagement, the profile will have no reviews. That is honest and normal for a new firm. Do not fill the gap.

---

## 2. Other profiles

### 2.1 Bing Places for Business (https://www.bingplaces.com/)

- Bing Places can import directly from a verified Google Business Profile. Do that once GBP is verified, then check every field. Country availability for the import is not documented clearly. If the import option does not appear for the UAE, add the listing manually.
- Use the same hidden-address / service-area set-up as GBP if Bing offers it. If Bing requires a visible address, use the Meydan address only if it meets Bing's own guidelines. If not, hold the listing until a qualifying address exists.
- Category: choose the closest available to "Building consultant" / "Real estate consultant", with the same exclusions as GBP.
- Description: paste the GBP description (1.3).
- Bing data feeds Microsoft Copilot answers and DuckDuckGo-style results, which is why it is worth doing.
- Separately, verify the site in **Bing Webmaster Tools** and put the code in `BING_VERIFICATION` in `config.py`. The site already supports IndexNow (`INDEXNOW_KEY`).

### 2.2 Apple Business (formerly Apple Business Connect: https://businessconnect.apple.com/)

- Apple renamed Business Connect to "Apple Business". Its current feature table lists the United Arab Emirates for Brand and Location Management, with footnotes that not every feature is offered in every country (https://support.apple.com/en-nz/126603). Confirm in the sign-up flow.
- Apple Maps place cards need a physical location customers can visit. The same staffed-address issue as GBP applies. If Apple will not accept a hidden-address service business, use **Brand** management only (name, logo, website, phone shown in Mail and Wallet where supported) and skip the location card for now.
- Category: closest to "Building consultant" / "Real estate consultant".
- About text (Apple allows around 500 characters):

```
Independent, client-side project manager for private villa builds and renovations in Dubai and Abu Dhabi. We represent the owner, alongside the owner's DM-registered consultant and the contractor: cost and programme control, like-for-like bid comparison, independent site visits and plain-English reports. Founded by Philip Chapman, who ran UK premium residential builder P Chapman Construction for 21 years. Paid only by the owner.
```

### 2.3 LinkedIn company page

Create from Philip's personal profile. **Page name:** `Eastbridge Strategic Partners`. **URL:** `linkedin.com/company/eastbridge-strategic-partners` (or the nearest available).

**Industry:** `Construction` is the honest top-level industry on LinkedIn (it does not imply we build). Alternative: `Business Consulting and Services`. Do not choose "Civil Engineering" or "Architecture and Planning".
**Company size:** 2–10 employees (or 1 if only Philip; pick the real figure).
**Company type:** Privately held. **Founded:** the year of the Meydan licence.
**Location:** the Meydan address, exactly as in the NAP sheet.

**Tagline (104 characters, limit 120):**
```
Independent client-side project manager for private villa builds and renovations in Dubai and Abu Dhabi.
```

**About (under the 2,000-character limit):**
```
Eastbridge Strategic Partners is an independent, client-side project manager and owner's representative for private clients building or renovating villas in Dubai and Abu Dhabi.

We represent the owner, alongside the owner's DM-registered consultant and the contractor. Our work covers plot and pre-purchase review, design brief and budget, help comparing bids like-for-like, monthly cost and programme control, independent site visits with plain-English reporting, commercial advice on variations and delay claims, stalled-project recovery, and snagging and handover.

Our founder, Philip Chapman, built and ran P Chapman Construction, a premium residential builder in the UK, for 21 years. The company built bespoke contemporary homes on the Cornish coast; its homes won a RIBA South West Award (Owers House, 2016), an LABC Building Excellence Award (2018 winner) and a Highly Commended in 2020, were reported in The Times and featured on Channel 4's Grand Designs.

We spent two decades as the builder. Now we sit on the client's side of the table. That means we know where budgets leak, how variations and delay claims are built, and what contractors hope clients will not check.

We are paid only by the owner. We accept no commission, referral fee or rebate from any consultant, contractor or supplier. We do not design and we do not build.

Many of the owners we work for live overseas, often in the UK or Europe. A named person in the UAE and a regular, honest report means nothing is decided without you.

Licensed in the Meydan Free Zone, Dubai. Enquiries: philip@eastbridgestrategicpartners.com
```

**Specialties (LinkedIn allows up to 20):**
```
Client-side project management; Owner's representation; Villa construction; Villa renovation; Cost control; Programme control; Bid comparison; Variations and claims advice; Extension of time; Site visits and reporting; Snagging and handover; Plot due diligence; Overseas owners; Stalled project recovery; Development advisory; Dubai; Abu Dhabi
```

**Philip's personal profile** matters more than the page for AI citations. Headline suggestion: `Founding Partner, Eastbridge Strategic Partners | Client-side project manager for villa builds in Dubai and Abu Dhabi | 21 years running P Chapman Construction (UK)`. List P Chapman Construction as a past position with the factual awards. Ask former UK architects and clients for **LinkedIn recommendations of Philip personally** (see 1.8).

**First LinkedIn posts:** republish each insight article as a short LinkedIn article (first 3–4 paragraphs plus a link to the full piece). LinkedIn content is frequently cited by AI assistants.

### 2.4 Instagram (existing: https://www.instagram.com/eastbridgestrategicpartners/)

- **Name field** (searchable, separate from the handle): `Eastbridge | Villa Project Manager`. The Instagram name field is not subject to Google's naming rules and is used in Instagram search.
- **Category:** "Consulting agency" is likely to be offered and is acceptable. Avoid "Construction company" and "Engineering service".
- **Bio (140 characters, limit 150):**
```
Client-side project manager for villa builds and renovations in Dubai and Abu Dhabi. We represent the owner. 21 years as a UK builder first.
```
- **Link:** `https://eastbridgestrategicpartners.com`. **Contact buttons:** the email and phone from the NAP sheet.
- **Highlights:** "Approach", "UK work" (every story says "Built by P Chapman Construction, Cornwall, UK"), "Insights", "Contact".
- **Grid rule:** every UK project post starts its caption with `UK project, built by P Chapman Construction, Cornwall.` and credits the photographer. Never geotag UK photos to Dubai.

### 2.5 Facebook page

- **Page name:** `Eastbridge Strategic Partners`. **Category:** "Consulting Agency" (plus "Real Estate Consultant" if offered). Avoid "Construction Company" and "Contractor".
- **Intro / bio (keep under 101 characters; this is 96):**
```
Independent client-side project manager for villa builds and renovations in Dubai and Abu Dhabi.
```
- **Details:** paste the LinkedIn About text. Address, phone, email, website and hours exactly as in the NAP sheet. If the Meydan address is not a visitable office, untick "show map / customers visit my business" and set service area to Dubai and Abu Dhabi.
- **Action button:** "Send WhatsApp message" (971567440057) or "Contact us" → `/contact/`.
- **Recommendations / reviews:** same rules as 1.8.
- Facebook is low priority for search and AI. Its main value is as a consistent citation and a sameAs link.

---

## 3. Directories and platforms (verified list)

**How to read this table.** "Checked" means the URL loaded or the cost was confirmed from the platform's own pages or a reputable source on 31 Oct 2026. Where something could not be confirmed, the table says so. **Link attribute:** whether a profile link passes ranking value ("dofollow") changes often and is rarely documented. Most large directories use nofollow or redirect links. Treat the value as **entity consistency and AI citation**, not PageRank. Check each live profile with the browser's inspect tool and record the result in the tracker.

### 3.1 Core local and map listings (do first)

| # | Platform | URL | Cost | Link attribute | Notes |
|---|---|---|---|---|---|
| 1 | Google Business Profile | https://business.google.com/ | Free | n/a (map listing) | See section 1. UAE is a supported country (https://support.google.com/business/answer/6270107). |
| 2 | Bing Places | https://www.bingplaces.com/ | Free | n/a | Section 2.1. Feeds Copilot. |
| 3 | Apple Business | https://businessconnect.apple.com/ | Free | n/a | Section 2.2. UAE listed in Apple's feature table. |
| 4 | 2GIS (Dubai) | https://www.2gis.ae/ | Free basic listing; paid advertising separate | n/a (map listing) | Widely used map and directory app in Dubai. 2GIS says its Dubai listing contains over 100,000 companies (Khaleej Times, https://www.khaleejtimes.com/uae/accurate-updated-and-consistent-local-listings-and-smart-city-map-with-2gis-ae). Add via the in-app "add company" flow; 2GIS staff verify (https://help.2gis.com/question/how-to-add-company-to-2GIS). |
| 5 | Yandex Business (Yandex Maps) | https://yandex.com/sprav/ | Free basic | n/a | Relevant to the Russian-speaking audience the `/ru/` site targets. Confirm Dubai coverage and verification method in the sign-up flow. |

### 3.2 Business bodies and chambers

| # | Platform | URL | Cost | Link attribute | Notes |
|---|---|---|---|---|---|
| 6 | Dubai Chambers membership | https://www.dubaichambers.com/new-membership | AED 300–2,200 (Dubai Chambers' new-membership page); valid one year | Unverified | Open to mainland and free-zone companies. Directory listing for free-zone members appears to be optional (Explorer guide). Confirm whether a member directory profile with a website link is included. |
| 7 | British Chamber of Commerce Dubai (formerly British Business Group Dubai) | https://britishchamberdubai.com/ (apply: /apply/membership; directories: /membership/directory, /company/directory) | Fees not published online; ask | Unverified | Open to British-owned Dubai companies and UK passport holders. Strong fit for the British owner audience: events, member directory, newsletter features. |
| 8 | Meydan Free Zone community | https://www.meydanfz.ae/ | Included with licence | Unverified | Ask whether Meydan FZ runs a member directory or spotlight feature for licensees. |

### 3.3 Construction, home and B2B platforms

| # | Platform | URL | Cost | Link attribute | Notes |
|---|---|---|---|---|---|
| 9 | Houzz (pro profile) | https://www.houzz.com/pro | Free basic profile; Houzz Pro software is paid | Website link usually nofollow (unverified) | UAE-based professionals do appear on houzz.com. Category: "Design-Build" and "General Contractors" are wrong. Choose the closest consulting/"Other" option. UK projects must be labelled "P Chapman Construction, Cornwall, UK". Strong image-search and homeowner audience, including British owners. |
| 10 | Clutch | https://clutch.co/get-listed | Free basic profile (Clutch help centre: https://help.clutch.co/en/knowledge/get-listed-on-clutch) | Unverified | B2B-focused. Fit is moderate; worth doing for the development-advisory audience. Reviews are verified by Clutch, so the same honesty rules apply: none until real clients. |
| 11 | Designing Buildings Wiki | https://www.designingbuildings.co.uk/ | Free to contribute | Unverified | UK construction wiki, ranked first in our baseline for "luxury villa renovation dubai". Contribute factual, non-promotional articles (for example "Owner's representative") with a byline, not adverts. |
| 12 | ProTenders company profiles | https://www.protenders.com/ | Free company profile; paid tiers for project data | Unverified | Middle East construction project database. Lists consultancy and PM firms. Confirm profile terms. |
| 13 | Big 5 Global (exhibitor/visitor) | https://www.big5global.com/ | Free to visit; exhibiting is paid | n/a | Dubai's main construction event. Use for networking and speaker applications, not a listing. |
| 14 | Crunchbase | https://www.crunchbase.com/ | Free basic profile | Nofollow | A structured company record that knowledge graphs and AI systems read. Fill in founder, location, founding year and website only. |
| 15 | Yellow Pages UAE (yellowpages-uae.com) | https://yellowpages-uae.com/ | Free listing (operator's own claim) | Unverified | Check you are on the intended domain. Several similarly named UAE "yellow pages" sites exist (for example yellowpagesae.com). Do not pay for "premium" placement. |
| 16 | Hotfrog UAE | https://www.hotfrog.ae/ | Free basic | Unverified | Generic citation. Low effort. |
| 17 | MyMidlist | https://www.mymidlist.com/ | Free | Unverified | Gulf-wide free directory. Generic citation. |
| 18 | Connect.ae | https://www.connect.ae/ | Not confirmed | Unverified | UAE directory. The site did not respond to our check on 31 Oct 2026. Retry before relying on it. |
| 19 | Expatica UAE directory | https://www.expatica.com/ae/directory/ | Check "add your listing" page; likely paid | Unverified | Expat audience. Use only if the cost is modest. |
| 20 | Female Fusion business directory | https://femalefusionnetwork.com/ | Basic free for non-members, AED 100 a year for trade-licence verification | Unverified | Only relevant if Eastbridge qualifies as women-founded or owned. Listed for completeness; probably not applicable. |

### 3.4 Professional bodies (only if Philip qualifies; say "if applicable")

| # | Body | URL | Cost | Notes |
|---|---|---|---|---|
| 21 | Chartered Institute of Building (CIOB): MCIOB | https://www.ciob.org/membership/mciob | Annual subscription (see CIOB) | **If applicable.** Routes: "Qualified & Experienced Practitioner" (degree holders, leading to the Professional Review) or "Experienced Practitioner" (no degree, via the Chartered Membership Programme) (https://www.ciob.org/membership/become-a-member/experienced-professional). 21 years running a building company is directly relevant experience. CIOB members get a public "find a member" record and can use MCIOB after their name. Never use the letters before membership is granted. |
| 22 | Association for Project Management (APM) | https://www.apm.org.uk/membership/ | Annual subscription | **If applicable.** UK project management body with international members. Chartered Project Professional (ChPP) is a longer-term option. |
| 23 | PMI UAE Chapter | https://www.pmi.org/ (find the UAE chapter from PMI's chapter finder) | Membership fee | **If applicable.** Networking and speaking. The pmi-uae.org address did not respond to our check. Find the current chapter URL via pmi.org. |
| 24 | RICS | https://www.rics.org/ | n/a | **Only if Philip holds or obtains RICS membership.** Do not call Eastbridge "surveyors" otherwise. |

### 3.5 Journalist-request platforms (for quotes, which AI assistants pick up)

| # | Platform | URL | Cost | Notes |
|---|---|---|---|---|
| 25 | Qwoted | https://www.qwoted.com/ | Free tier for experts | Journalists post requests. Answer only within the brief's facts and wording. |
| 26 | Featured.com | https://featured.com/ | Free tier and paid | Expert Q&A placed in publications. Quality varies. Answer only questions on villa building, renovation, contracts and costs. |
| 27 | ResponseSource (UK) | https://www.responsesource.com/ | Paid | UK journalist enquiry service. Good for The Times and UK homes titles. Check price against value. |

**Do not use:** paid "500 UAE backlinks" packages, private blog networks, article spinning, or any directory that charges for a "best villa project manager" badge. They break Google's spam policies and the brief's "no rankings" rule.

**ArchiExpo-type listings:** ArchiExpo is a catalogue for manufacturers of products. Eastbridge sells a service, not a product, so it is **not a fit**. The same applies to product catalogues generally.

**"Construction Week directory":** we could not confirm that Construction Week Middle East runs an open company directory (the site blocked automated checks). Treat CWME as a PR target (section 4), not a listing.

---

## 4. PR and thought leadership

### 4.1 Principles

- Pitch **expertise and commentary on current, verifiable news**, never "Eastbridge completes project X". There are no UAE projects to announce, and none should be implied.
- Every number in a pitch comes from the verified facts list in `WRITING_BRIEF.md`, with its source.
- Offer Philip as a named expert: "Philip Chapman, founding partner of Eastbridge Strategic Partners, ran P Chapman Construction, a UK premium residential builder, for 21 years."
- Send short emails: a three-line pitch, two or three bullet points of what Philip can say, availability, phone. No attachments on a first approach. Follow up once after five working days, then stop.
- Contact details below were found publicly on 31 Oct 2026. Staff move often. **Check each name on the outlet's site or LinkedIn the week you pitch.**

### 4.2 Outlet contact routes (found publicly)

| Outlet | Route | Source / confidence |
|---|---|---|
| Gulf News (Property) | `propertyweekly@gulfnews.com` (Property Weekly editorial enquiries); website feedback form with department editor dropdown; main office PO Box 6519, Dubai, +971 4 344 7100 | gulfnews.com Property Weekly page and FAQ (https://gulfnews.com/gnmedia/faqs-1.1376095). Address may be dated. Editor-in-chief Mark Thompson appointed Sept 2025 (search result). Medium confidence. |
| Khaleej Times | `news@khaleejtimes.com`, `reporters@khaleejtimes.com` | Official contact page https://khaleejtimes.com/contact-us. High confidence. |
| The National | `newstips@thenationalnews.com` (stories), `letters@thenationalnews.com` (letters), `info@thenationalnews.com` | Official contact page https://www.thenationalnews.com/contact-us/. High confidence. No published op-ed address; pitch the property or opinion editor named on the site. |
| Arabian Business | Contact page on arabianbusiness.com (blocked our fetch). Editor-in-chief Damian Reilly (appointed Oct 2025, https://www.mediasource.me/posts/arabian-business-appoints-editor-in-chief). Published by ITP Media Group. | Low–medium. Find the real estate editor's byline on recent property stories. |
| Construction Week Middle East (ITP) | 2025 media kit lists Associate Editor Julianne Tolentino and Deputy Editor Shehzin Shaikh, with itp.com email addresses (https://www.constructionweekonline.com/cloud/2025/07/14/CWME-Media-Kit-2025.pdf) | Medium. Copy the exact addresses from the media kit PDF in a browser. |
| MEED | Editor Colin Foreman `colin.foreman@meed.com`; Construction writer Yasir Iqbal `yasir.iqbal@meed.com`, +971 4 818 0263; Features & Analysis Editor John Bambridge `john.bambridge@meed.com` | Official contacts page https://www.meed.com/contacts. High confidence. MEED is project- and market-focused: pitch market commentary, not homeowner tips. |
| Property Finder blog | No public contributor route found. Approach the Property Finder PR/communications team (via LinkedIn) offering expert commentary for buyer guides. | Low. |
| Bayut / MyBayut | No public editorial route found. Use Bayut's contact page and LinkedIn to reach the MyBayut content team. | Low. |
| The Times, Bricks & Mortar (UK) | Carol Lewis is described as property editor of The Times and The Sunday Times (undated speaker bio, https://www.bristolideas.co.uk/speakers/carol-lewis/). Use ResponseSource or Qwoted for live Times property requests. | Low–medium. Verify the current editor first. Owers House was previously reported in The Times: mention it. |
| Grand Designs magazine (UK) | granddesignsmagazine.com. Reported as now web-only (media databases). Old contact addresses found are likely outdated. | Low. The hook is strong: a P Chapman Construction home featured on Channel 4's Grand Designs. Find the current digital editor via LinkedIn. |

### 4.3 Ten story angles, each matched to outlets

Each angle is commentary Philip can give from 21 years on the builder's side, tied to verified news.

1. **"What the AI permit checker will and will not catch."** Hook: in August 2026 Dubai Municipality announced an AI system checking villa drawings against the Dubai Building Code, phased in through Build in Dubai (https://www.khaleejtimes.com/uae/dubai-ai-system-villa-construction-permits). Angle: compliance checking speeds approval, but cost, buildability and contract risk still need a human on the owner's side. **Outlets:** Khaleej Times (news@ / reporters@), Construction Week ME.
2. **"Over-designed villas: why owners pay for steel they do not need."** Hook: in August 2025 Dubai Municipality warned villa engineering consultancies about over-designing structures and inflating costs (https://gulfnews.com/uae/dubai-municipality-warns-consultancies-inflating-villa-designs-raising-costs-1.500245704). Angle: how an owner can ask for a value review without undermining the consultant. (Do not link the separate June 2025 suspensions to over-design.) **Outlets:** Gulf News Property, Arabian Business.
3. **"Who can call themselves a consultant now? Dubai's new engineering law, explained for villa owners."** Hook: Dubai Law No. 14 of 2025 (Al Tamimi summary: https://www.tamimi.com/news/dubai-issues-new-law-regulating-engineering-consultancy-activities-key-takeaway-points/). Angle: what owners should check on the firms they appoint, and the difference between a DM-registered consultant and a client-side project manager. Recommend UAE-qualified legal advice for specifics. **Outlets:** The National (newstips@), Gulf News.
4. **"Abu Dhabi swaps paper permits for joint reports: what changes for villa owners."** Hook: Abu Dhabi's October 2026 Circular No. 9, under which certified joint reports by the supervision consultant and contractor replace phase-closure permits for designated categories (https://www.khaleejtimes.com/uae/abu-dhabi-replaces-paper-permits-for-buildings-with-digital-reports-new-directive?amp=1). Angle: when the people building also certify progress, who is checking for the owner? **Outlets:** The National, Khaleej Times.
5. **"Rooftop majlis and annex basements: what Abu Dhabi's villa rule changes mean for budgets."** Hook: DMT's September 2025 private-villa regulation amendments (rooftop majlis, 1.5 m front setback, annex basements) (https://www.dmt.gov.ae/en/Media-Centre/News/Department-of-Municipalities-and-Transport-Announces-Amendments-to-Private-Villas-Regulations). Angle: new allowances add cost and programme; how to price them before design. **Outlets:** The National, Gulf News Property, MyBayut.
6. **"1,700 plots on Hudayriyat: the five questions to ask before you buy a plot to build on."** Hook: Modon's Hudayriyat residential plots (1,700+ plots for 4–6 bed villas) (https://meconstructionnews.com/63729/modon-launches-its-first-residential-plots-community-on-hudayriyat-island). Angle: build-by deadlines, design rules and realistic build cost per square foot (Engel & Völkers ranges, https://www.engelvoelkers.com/ae/en/resources/construction-cost-dubai). **Outlets:** Property Finder blog, MyBayut, Arabian Business.
7. **"What does it really cost to build a villa in Dubai? Why quotes differ by AED 500 a square foot."** Hook: published 2025–26 ranges (E&V: standard AED 300–500/sq ft, luxury 900–1,400; Knight Frank Q2 2025 via Gulf Construction, https://gulfconstructiononline.com/ArticleTA/436847). Angle: what sits inside and outside a contractor's rate (preliminaries, contingency, FF&E, pools, landscaping) from someone who priced homes for 21 years. **Outlets:** Gulf News Property, MyBayut, Property Finder blog.
8. **"Building in Dubai from London: a UK builder's guide for British owners."** Hook: British owners buying villa plots and renovation projects in Dubai. Angle: how UK JCT habits differ from UAE practice (DM's standard private-villa contract forms, https://www.dm.gov.ae/municipality-business/guidance-contracts-forms-for-engineering-consulting-services-and-construction-contracting-for-private-villas/), the approval sequence, and how to manage a build from abroad. **Outlets:** The Times Bricks & Mortar, Grand Designs magazine (digital).
9. **"From Grand Designs to Dubai: what a Cornish builder learnt that applies to Gulf villas."** Hook: a P Chapman Construction home featured on Channel 4's Grand Designs, and Owers House won a RIBA South West Award 2016. Angle: coastal exposure, glazing, waterproofing and roof terraces, and why the same failure points appear on Dubai island plots. Must be framed as UK experience, with no UAE project claims. **Outlets:** Grand Designs magazine, The Times.
10. **"The contractor's view: what builders hope villa owners won't check."** Hook: evergreen, tied to the stalled-project problem owners talk about. Angle: preliminaries, provisional sums, variation pricing and delay claims, from 21 years on the builder's side. Recommend legal advice for disputes. **Outlets:** Construction Week ME (as an opinion column), MEED (market-commentary version: owner-side capability in the private villa market), Arabian Business.

### 4.4 Guest article outlines for the top three pitches

**A. Gulf News Property: "Before you sign: how to compare villa construction quotes like-for-like" (900–1,100 words)**

1. Opening (direct answer): two quotes for the same villa can differ by millions of dirhams, and the cheapest is often not the lowest cost. Why that happens.
2. What sits in a contractor's price: preliminaries (Turner & Townsend 2025: 12–14% in Dubai, via PRASOON https://prasoon.design/insights/owners-representative-vs-project-manager-uae), provisional sums, exclusions, contingency.
3. The builder's view (first-hand): "On the contractor's side, the first thing we priced on any job was the risk the drawings left open." What that means for the owner.
4. A five-line checklist for levelling bids: scope gaps, provisional sums, programme, payment terms, retention and defects period.
5. Published cost ranges as a sense check (E&V and Real Estate Club Dubai figures, cited), with the caveat that ranges are not quotes.
6. Where advice is needed: your DM-registered consultant on technical matters, a UAE-qualified lawyer on contract terms, and an independent client-side project manager on cost and commercial risk.
7. Author line: Philip Chapman, founding partner, Eastbridge Strategic Partners; ran P Chapman Construction (UK) for 21 years.

**B. The National: "Dubai's new engineering consultancy law: what villa owners should check before appointing anyone" (800–1,000 words)**

1. Direct answer: Dubai Law No. 14 of 2025 regulates engineering consultancy across Dubai, including free zones. Owners should check registration before appointing a design or supervision consultant.
2. What the law covers, from the Al Tamimi summary (cite). No legal advice; recommend a UAE-qualified lawyer.
3. The roles on a villa project: DM-registered consultant (design, statutory supervision, permits through Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where the plot sits), contractor, and an optional client-side project manager.
4. Why roles blur in practice (design-and-build offers, project managers who take referral fees), and why independence should be written into the appointment.
5. Practical checks: registration on the Dubai BPS app registry (https://www.dm.gov.ae/new-improved-building-permits-app-launched-for-streamlined-services/), the DM standard contract forms, references.
6. A builder's observation on what goes wrong when nobody is clearly on the owner's side.
7. Author line.

**C. Construction Week Middle East (opinion): "The missing seat at the private villa table" (700–900 words)**

1. Thesis: on large commercial projects the client has a project manager and cost consultant. On a multi-million-dirham private villa, the owner often has nobody on their side.
2. Market context, framed as estimates: international owner's-rep fees roughly 2–5% of construction cost; PRASOON notes no credible Dubai benchmark exists. UAE cost inflation around 3% forecast for 2026 (Currie & Brown, via PRASOON).
3. Regulatory direction: unified permit e-window (2022), Build in Dubai platform (2023), the AI drawing check (2026), Law No. 14 of 2025. Approval is becoming more digital, while commercial control on the owner's side remains a gap.
4. A contractor's confession (first-hand, general): how variations and extension-of-time claims are built, and where owners are weakest.
5. What good owner-side practice looks like: monthly cost-to-complete, priced variations before instruction, independent reporting, alongside, not instead of, the consultant.
6. Close: better-informed owners are good for good contractors too.
7. Author line.

### 4.5 Podcast and YouTube explainer plan

**Format:** 6–10 minute explainers filmed by Philip (talking head plus screen graphics). Upload to YouTube with full transcripts and chapters. Embed each video on the matching insight page (adds `VideoObject` schema later). Cut 45–60 second vertical clips for Instagram and LinkedIn. Pitch Philip as a guest to UK self-build and property podcasts and to UAE expat-business podcasts using the same five topics.

**Rules on camera:** no UAE project footage unless Eastbridge is genuinely involved and the owner consents. UK footage carries an on-screen caption: "Built by P Chapman Construction, Cornwall, UK". Say "we" not "I" in scripted segments, as the brief requires.

**Script outline 1: "What does a client-side project manager do on a Dubai villa?" (7 min)**
- Cold open (20 s): "Your architect works for the design. Your contractor works for his margin. Who works for you?"
- The three roles: DM-registered consultant, contractor, client-side project manager. Simple on-screen diagram.
- What we do, stage by stage: plot, design, bids, construction, handover.
- What we do not do: design, build, supervise, submit permits.
- Independence: paid only by the owner.
- Close: link to /why-a-client-side-project-manager/ and /contact/.

**Script outline 2: "How much does it cost to build a villa in Dubai in 2026?" (9 min)**
- Direct answer with sourced ranges on screen (E&V; Knight Frank via Gulf Construction; Real Estate Club Dubai). Each source shown on screen.
- What sits outside the build rate: design 6–12%, permits and connections, pool, landscaping, FF&E, contingency 10–15% (Real Estate Club Dubai, cited).
- From the builder's side: how a contractor builds up a rate and where the margin hides (general, no project numbers).
- The three numbers to track monthly.
- Close: link to the cost article (`/insights/villa-construction-cost-dubai/`).

**Script outline 3: "Building a villa in Dubai while living in the UK" (8 min)**
- Who this is for. The problem: weekly decisions, thousands of kilometres away.
- The approval sequence in plain English (Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where the plot sits; Build in Dubai platform).
- UK habits that do not transfer: JCT assumptions, contract forms; recommend UAE-qualified legal advice.
- How remote owners stay in control: decision log, monthly report, photo record, payment approvals.
- UK experience: building for owners who lived away (Blue Seas, captioned as UK).
- Close: /services/overseas-owners/.

**Script outline 4: "Variations and delay claims: how contractors build them" (10 min)**
- What a variation is; what an extension of time is.
- From 21 years on the builder's side: how a claim is assembled (records, programme, notices), shown generically.
- Where claims are strong and where they are weak.
- What owners should do from day one: priced variations before instruction, contemporaneous records, notice periods.
- Disputes: take advice from a UAE-qualified lawyer.
- Close: /services/variations-delays-and-claims/.

**Script outline 5: "Villa renovation in Dubai: the three surprises that break budgets" (7 min)**
- Water, services, structure: the three recurring surprises.
- Opening up before pricing: why a little cost early saves a lot later.
- Approvals: in Nakheel communities, renovations start with a Nakheel NOC through its portal before the authority permit.
- Living next door to the works: access, noise, neighbours (St Michael's Hotel lesson, captioned as UK).
- Close: /services/villa-renovation-project-management/ and the Palm Jumeirah renovation guide.

**Podcast pitch blurb (paste):**
> Philip Chapman ran P Chapman Construction, a UK premium residential builder, for 21 years: bespoke homes on the Cornish coast, a RIBA South West Award and a home featured on Channel 4's Grand Designs. He now runs Eastbridge Strategic Partners in Dubai, an independent client-side project manager for private villa builds and renovations. He can talk candidly about how builders price, how variations and delay claims are built, and what owners, especially those living abroad, should check before they sign.

---

## 5. Order of work

1. Site live and indexed (Search Console and Bing Webmaster Tools verification codes into `config.py`).
2. Take legal advice on category wording (1.2). Decide the GBP address route (1.1).
3. GBP → Bing Places (import) → Apple Business → 2GIS.
4. LinkedIn company page plus Philip's profile update → Facebook → Instagram refresh. Add each URL to `SOCIAL`.
5. Dubai Chambers and British Chamber of Commerce Dubai memberships.
6. Houzz, Crunchbase, Clutch, Yellow Pages UAE, Hotfrog, MyMidlist, ProTenders.
7. Start PR: one pitch a fortnight, beginning with angles 1, 2 and 7. Sign up to Qwoted / Featured for live requests.
8. Film explainer 1 and 2. Publish with transcripts.
9. CIOB / APM applications, if applicable.
10. Review requests: only after the first real engagement.

Recheck NAP across every listing each quarter. Search the business name in Google, Bing and two AI assistants each month and note which sources they cite.
