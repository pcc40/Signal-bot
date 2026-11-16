# Competitor ads research (16 November 2026)

Research for Phil Chapman before the Eastbridge Google and Meta campaigns go live. Read-only: nothing was logged into, submitted, bought or changed on any site.

## How this was done, and how far to trust it

| Source | Method | What worked | Limits |
|---|---|---|---|
| Meta Ad Library | Headless Chromium (Playwright), logged out, `country=AE` and `country=GB`, active ads only, keyword search. Ad data read from the page's own JSON (advertiser, start date, format, headline, text, CTA, link). | Works without a login. About 30 ads read per search (Meta sorts by impressions). | Meta's public library intermittently returned "No ads match" to the headless browser, even for searches that had worked minutes before. A competitor marked "none found" below means none found in three attempts, not proof they have no ads. Two firms (Bauhaus and Kikoola) were found only through keyword searches, not name searches. Meta shows a start date but no spend or impressions for commercial ads in the UAE. |
| Meta Ad Library API | `graph.facebook.com/ads_archive` without a token | No | Returns an OAuth error. It needs a token from a verified Meta account, so it was not used. |
| Google Ads Transparency Center | Its public search endpoints, read from a logged-out browser session, by advertiser name and by domain. Region UAE (and "anywhere" as a check). Archived renderings of the ads were downloaded and read. | Works without a login. It gives every ad an advertiser has run, with format, first-shown and last-shown dates and the number of days shown. | No impressions, spend or keywords. It cannot be searched by keyword, so other advertisers on "villa project management Dubai" could only be found by name. |
| WebSearch | "villa project management Dubai owner's representative" | Organic results only | It does not show ads, so it says nothing about who is bidding. The organic results were Tanmu's community pages, Prime Project Partners and job adverts. |

**Ad-library scraping tools:** none are installed or available here. ToolSearch for "ad library", "meta ads library" and "scraper" found only the Adplane tools. Those manage your own Google and Meta ad accounts; they cannot read competitors' ads. A claude.ai skills search for "ad library", "meta ads library", "scraper", "competitor ads" and "google ads transparency" returned nothing. No skill or plugin in the session does this. Paid options exist outside the session, such as Apify actors for the Meta Ad Library (Apify account and paid API key), SerpAPI's Google Ads Transparency endpoint (paid key), and Meta's official Ad Library API (free, but it needs identity verification on a Meta developer account). Nothing was installed and no credentials were entered. The Playwright scripts used here do the same job for free, if a little unreliably.

## 1. Per competitor

Dates are first shown to last shown. "Live" means last shown on 15 or 16 November 2026 (Google), or listed as active today (Meta). "Days" is the number of days Google records the ad as shown.

### Owner-side / client-side project managers (direct competitors)

| Competitor | Google (Transparency Center) | Meta (Ad Library, AE and GB) |
|---|---|---|
| **Tanmu PMS** (tanmupms.com, tanmu-website.pages.dev) | No ads ever recorded for either domain. | None found ("Tanmu", three attempts). It relies on SEO: separate pages for Palm Jumeirah, Emirates Hills, Dubai Hills, Arabian Ranches, Jumeirah Islands and Dubai South. |
| **Stonehaven Project Management Services LLC** (stonehaven.ae) | **45 ads (31 text, 14 image), Oct 2025 to 29 Apr 2026. Nothing since.** Landing page: landing.stonehaven.ae. Text headlines: "Dubai Project Consultants - Get Independent Consulting"; "UAE Construction Consultant - Building Consultants UAE"; "Expert Cost Consultancy - Stonehaven Cost Management"; "UAE Quantity Surveying - Leading UAE Specialists"; "BOQ Preparation Experts - Exact Takeoffs. Zero Stress."; "Property Development Managers - Plan Right, Build Profitably"; "Design & Build Contractors - Integrated Project Solutions" ("Full Turnkey Management"). Descriptions: "Your Real Estate & Construction Projects Delivered On-Time, On-Budget, And Built To Last"; "Construction Consultancy Trusted By Developers Across The UAE For Major Projects". Image ads (hi-vis staff with tablets): "Protect Your Development From Delays and Overruns", "Build Complex Developments Without Construction Headaches", button "Talk To An Expert". Longest-running text ad: 191 days. | None found. |
| **Bauhaus Project Management** (bauhausproject.ae) | No ads ever recorded. | **1 active video ad, started 11 Nov 2026** (Page has 44 likes; no link or button, so most likely a boosted post): "A finished villa is the result. But what does it take to get there? An endless list of suppliers and countless decisions along the way. At Bauhaus Project Management, we bring all the moving parts together, managing the budget, programme and quality from start to finish. So our clients can focus on the vision, while we focus on making it happen. Planning to build or renovate a villa in Dubai? Let's talk." |
| **Kikoola Project Management LLC** (new; not on the original list) | Not checked by name. | **1 active dynamic-creative ad, started 11 Nov 2026** (Page has 3 likes). Headline "Request a Consultation", CTA "Sign up" to a Meta instant form: "Kikoola manages luxury villa builds and renovations in Dubai, from planning and contractor coordination through to handover. Request a consultation to discuss your scope, budget and timeline." |
| **Project Wizards** (projectwizards.ae) | No ads ever recorded. | None found (the only near match was "Wood Wizards Dubai", a joinery firm). |
| **DNA Project Management** (dnaprojectmanagement.com) | No ads ever recorded. | None found (the search returned only unrelated drama-app ads). |
| **NU Projects** (nuprojects.ae) | No ads ever recorded (nuprojects.ae). "Nuu Projects Ltd" (GB) is a different firm. | None found (three attempts; the results were unrelated). |
| **NEXTSTEP** (nextstep-pm.com) | No ads ever recorded. | None found. |
| **Prime Project Partners** (Ras Al Khaimah; prime-project-partners.vercel.app) | Not in the Transparency Center. | None found (the results included "Prime Estate Partners", an unrelated agency). |
| **North 51 Consulting** | Not found under "north 51" or "north51". | None found (the "North 51" search returned unrelated ads). |
| **HPM** | No UAE advertiser named HPM (only US, UK and other HPM firms). | None found. |
| **Turner & Townsend** (residential) | Recruitment ads only: Belgian project-manager jobs (5 text ads, Jul to Oct 2026), plus 2025 corporate "Transform Together" display ads (agency account). Nothing residential and nothing in the UAE. | None found in AE. |
| **Cavendish Maxwell** (valuers and surveyors) | **48 ads, 45 live.** Image: "Get Your Property Valued for Dubai's Golden Visa Programme – Schedule your valuation now"; "Know what you are buying before completion. Independent technical due diligence for prime real estate acquisitions across the UAE – Request an inspection"; "Handover ready? Speak to our building surveyors about your next acquisition in Dubai or Abu Dhabi." Text since Jul 2024 (733 days): "Dubai Property Consultants - UAE's Top Advisory Firm … RICS Certified". | None found. |
| **Real Estate Club Dubai** | No ads ever recorded for realestateclubdubai.com. | None from the club itself in the top 30 results for "Real Estate Club Dubai" (all property-agency ads). |
| **PRASOON** (owner's representative content) | No UAE advertiser. | Not searched. |

### Design-and-build and renovation firms (compete for the same owners)

| Competitor | Google | Meta |
|---|---|---|
| **Algedra** (algedra.ae) | **20 ads, 7 live. Three text ads have run since May/June 2024 (745–806 days).** Mostly Arabic: "Algedra, the best design company – more than 13 years' experience". English: "ALGEDRA Architectural Design - Villa Architectural Design – View our architectural portfolio and discuss the spaces and style you envision", with sitelinks Palaces Designs, Get a Free Consultation, Majlis Interior Design. Map/local ad showing 4.3 stars (145 reviews). Three video ads since Jul 2024. | None found by name. |
| **Smart Renovation** (smartrenovation.ae; SR Decoration Design & Fit-Out Est) | **62 ads, 15 live; core text ads since 17 Jan 2026 (≈300 days).** "Learn more \| Smart Renovation®, Dubai - Trusted by 500+ Homeowners"; "Interior Design Contractors - Deliver on Time, Within Budget"; "Villa Renovation Company Dubai" with a "40+ Years of Expertise" callout and a WhatsApp asset; "Renovate Your Home with Style … Our Italian experts …". Landing pages /book/consultation and /form. Local ad 4.8 stars (64). Display: "Renovated over 500+ Homes … Visit Site". New video from 14 Nov. | Active since 24 and 30 Oct 2026: "TRUST IS NOT GIVEN. IT'S EARNED. 15 years in Dubai. 500+ completed projects." (CTA Get offer, or Send WhatsApp message); "Italian Creativity. Timeless Design. We Renovate Your Villa" (See details, links to /smart-renovation-residential/). Page has 6,267 likes. |
| **Luxedesign** (luxedesign.ae) | **40 ads, 21 live; several since Feb to Apr 2025 (515–525 days).** "Construction Company in Dubai \| Luxedesign Villas – Villa construction in Dubai by one team: our villa contractors and builders handle every approval and run the site full time, from plot to handover"; "#1 Villa Construction Company - Turnkey Villa Solutions in UAE"; "Villa Contractor Company UAE - Trusted Villa Builders UAE – We Manage Permits, Design, & Construction". WhatsApp asset on most. The same Google account also runs dubaiapprovals.com ads ("#1 Authority Approvals Service"). | Organic build-progress videos boosted to Instagram ("Pearl Jumeirah. From the ground up …", started 13 Nov). |
| **Dar Al Naseeb** (daralnaseeb.com; approvals firm and contractor) | **20 text ads, all live, running since late Jan to mid-Feb 2026 (272–290 days). One final URL per community:** /communities/palm-jumeirah, /jumeirahislands, /jumeirahpark, /jvc-and-jvt, /jumeriahgs (Jumeirah Golf Estates), /damac-hills, /al-quoz, /business-bay, /jafza. The headline is just "Call 050 524 6565". Example description: "We handle all Nakheel NOCs & Trakhees permits. Fast approvals for your villa. Avoid fines & delays. Call our engineering team for a free consultation today!" Also "Build Your Dream, Legally - Villa Construction Approval". | None found by name. |
| **DMDC** (dmdc.ae) | **6 text ads, 4 live since 30 Aug 2026 (74–78 days).** "From Drawings to Keys - 1,200 In-House Specialists – Ultra-prime home design, construction and joinery delivered by one integrated team"; "DMDC Group Dubai – A villa taken back to structure and returned as a new house. One accountable team. Villa renovation in Dubai, in confidence"; "DMDC Design & Architecture - Design and Supervision". Sitelink "Types of Renovation Firm" (a content page). | None found by name. |
| **Capital Associated** (capitalassociated.com) | **8 ads (5 text, 2 image, 1 video), Feb to 11 Jun 2026. Nothing since.** "Top contracting company in Dubai - General Contractors in Dubai … get a free consltation" [sic]; "Construction Company in Dubai - Best Dubai Contractors"; image "Construction Company in Dubai … Get Quote". | None (a name search returned unrelated finance ads). |
| **BG Villas** (bgvillas.ae, Better Gardens Contracting) | 11 ads. Text ads ran Apr 2024 to Apr 2026 (≈660 days). Live since 17 Oct 2026: "BG Villas – Book a free villa visit this week. Our expert visits, assesses & designs a custom plan." Also "Luxury home renovation dubai" (map ad, 4.6 stars, 9 reviews) with sitelinks Full Turnkey Villa Renovation and Luxury Villa Renovation Dubai. | Not searched. |
| **Artagroup** (artagroup.ae) | 8 text ads. The latest ran Aug to 7 Oct 2026: "Full Home Renovation Dubai - Fixed-Price Renovation – Looking for a renovation company in Dubai? Book a free site visit to discuss your project." | Not searched. |
| **Rady Interior** | No ads ever recorded (radyinterior.ae and .com). | None found. |
| **Optimal Engineering, Projeco** | One local ad each (Optimal May to Dec 2025; Projeco 26 Oct to 4 Nov 2026). | Not searched. |

### Others found advertising on the same Meta searches (AE, active 16 Nov 2026)

On **"owner's representative Dubai"** no advertiser is in this market. The results were a yacht "Owner's Technical Representative", property managers and unrelated ads. **No Dubai firm is advertising owner's representation on Meta.**

On **"villa project management Dubai", "villa renovation Dubai", "villa construction Dubai" and "build villa Dubai"** (about 54, 320, 210 and 240 active ads respectively), the relevant advertisers were:

| Advertiser | Running since | Format / CTA | The hook in their words |
|---|---|---|---|
| **Trust Group Construction LLC** | **11 Mar 2026 (8 months)** | Before/after image ("Own property in Dubai? Turnkey apartment renovation without your involvement"), Instagram / Get offer, with the text pointing to "Get quote" | "Do you own an apartment or villa in Dubai? If you're planning a renovation, you've probably faced common problems: missed deadlines, budget increases during the project, constant contractor management … What you get: fixed budget and timeline in the contract, transparent step-by-step renovation process, regular photo and video progress reports, full contractor and quality management … get a preliminary renovation estimate in 1 minute." |
| **Bond Homes Real Estate** (Bond Interiors) | **3 May 2026 (6.5 months)**; two video versions plus an image added 21 Oct | Video / Get quote | Headline "Free Consultation", link line "Fast, tailored 24h quotes designed for luxury villa renovations"; "Several record-breaking achievements, Dubai's greatest in-house capabilities, and award-winning designers … 800-BOND-UAE". |
| **Azulejon Tiles** | 8 Jun 2026 (5 months) | Founder video / WhatsApp | "Are you planning to renovate your villa in Dubai? I'm Abel, founder of AzulejON. One of the biggest mistakes I see homeowners make is choosing flooring based only on price …" |
| **Maison De Nova** | 6 Aug 2026 (3+ months), refreshed 12 Oct | Video / WhatsApp | "Premium Villa Renovation Dubai – Free villa consultation · design + build under one roof". |
| **Smart Cities Building Contracting** | 10 Aug 2026 | Video / WhatsApp | "Planning your dream villa in Dubai? Build it with confidence … Get your quote today." |
| **Fitout & Renovation Dubai** | 11 Sep 2026 | Carousel / WhatsApp | Publishes prices: "Kitchens from AED 25,000. Bathrooms from AED 18,000 … Full villa or apartment renovation quoted after a free site visit. One licensed company since 1984." |
| **TaskRight** (marketplace) | 23 Sep 2026 | UGC video / Get a quote (UTM-tagged landing page) | **"Nobody can price a villa from a photo."** "Anyone who prices your villa off three pictures is guessing, and a guess is not something you can plan a budget around … they pay us a flat subscription, never a commission, so there is no cut to build into your quote." |
| **ANK Construction & Interiors** | 26 Sep 2026 | Video / quiz landing page | "Most homeowners have no idea what it will actually cost. Answer 10 quick questions and get a clear estimate for your project." |
| **Hammer and Heart** | 2 and 13 Oct 2026 | Video and carousel / Get quote | "Know the COST, Design with Confidence." "The real challenge isn't always the construction itself. It can be the disconnect between design, costing, approvals, contractors and project management." |
| **Redesign Fitout** | 23 Oct 2026 | Video / WhatsApp | "✔ 200+ projects delivered ✔ Handover date written into the contract ✔ 12 months of free maintenance … We take on full projects only, so small repairs aren't a fit. Send us the property type and size on WhatsApp, and we'll tell you if we're the right team." |
| **Twyst Interiors** | 29 Oct 2026 | Video / Request time (booking page) | "If you're building or renovating a villa in Dubai, you already know the hardest part isn't choosing a style. It's getting the villa built exactly as you pictured it, without living on site to make it happen." |
| **Utopia Renovations** (Abu Dhabi) | 30 Oct 2026 | Image / Learn more | Headline "One Team. Every Stage of Your Renovation."; "Discover British-led renovation in Abu Dhabi"; "Who's managing your renovation while you're managing everything else?" |
| **MM Studio+** (Mattia Michelon) | 2 Nov 2026 (4 versions) | Image / See details | "Your villa should feel like it was designed for you. Not just decorated … 20 years of luxury design experience and 15 years working specifically in the Dubai market … Book your free design consultation today." |
| **BRS Group** | 3 Nov 2026 | Video / Download (instant form) | "Your Dubai property could be worth 30% more — you just haven't renovated it yet … Dedicated project manager for every home … free renovation estimate in minutes." |
| **Housescaner** | 5 Nov 2026 | Video / Get quote | "Still living in a 2-bedroom villa in Dubai? … We transformed a 2-bed villa into a spacious 4-bed family home … Backed by a 12-month warranty." |
| **Designer East** (architects) | 6 Nov 2026 (2 versions) | Video / Get quote (instant form) | "Have a plot in Dubai? Turn it into the villa you've been planning. Designer East handles it all: architecture, engineering approvals and project management, from the first sketch to the keys. 500+ projects delivered in Dubai since 2013." |
| **Cardoso Engineering** | 9 Nov 2026 | Video / WhatsApp | "Design Project in 30 Days — or Money Back". |
| **AlignWorks** | 13 Nov 2026 | Image / Send WhatsApp message | "Thinking about renovating your Dubai villa but dreading chasing contractors?" |

**UK (country=GB):** "villa renovation Dubai" returned only two active ads (Project London UAE, an interior designer documenting a Tilal Al Ghaf villa; and "flippingindubai", a villa-flip investment pitch). "Build villa Dubai", "villa project management Dubai" and "owner's representative Dubai" returned none in GB. **Almost nobody targets UK-based owners on Meta for Dubai villa work.**

## 2. The best ads and why

Long-running ads are the closest public evidence of what pays. Nobody keeps paying for an ad that does not bring enquiries.

1. **Dar Al Naseeb, Google Search, one ad per community (20 ads, live since Jan/Feb 2026, about 280 days).** *Hook:* the community name in the URL path (/communities/palm-jumeirah) and the master-developer pain ("Nakheel NOCs & Trakhees permits … Avoid fines & delays"). *Offer:* free consultation. *Proof:* "our engineering team". *CTA:* the phone number as the headline. *Landing:* a page for that community. *Why it works:* the person searching sees their own community in the ad and lands on a page about it. Nine months of continuous spend on 20 variants is the strongest evidence in this research. **Eastbridge already has the pages for this:** /areas/palm-jumeirah/, /emirates-hills/, /jumeirah-islands/, /dubai-hills-estate/ and others. (Do not copy the permit offer, which Eastbridge cannot make.)

2. **Luxedesign, Google Search "plot to handover, one team" (live for 300–525 days, with a WhatsApp asset).** *Hook:* "Villa construction in Dubai by one team … from plot to handover". *Proof:* "run the site full time". *CTA:* WhatsApp plus sitelinks to projects. *Why it works:* it says the whole journey in one sentence and gives a low-effort WhatsApp route, which is how Dubai owners prefer to make first contact. Eastbridge can borrow the "plot to keys" framing and the WhatsApp asset, not the "we build it" claim.

3. **Algedra, Google Search brand and experience ads (745–806 days, still live).** *Hook:* "more than 13 years' experience". *Offer:* free consultation. *Proof:* the map pack with 4.3 stars from 145 reviews. *Why it works:* a plain years-of-experience claim, a free consultation and visible ratings, run in Arabic as well as English. The lesson for Eastbridge is to lead with "21 years running a UK builder" and to add Google Business Profile reviews as soon as there are any.

4. **Trust Group Construction, Meta image ad (8 months, since 11 Mar 2026).** *Hook:* "Do you own an apartment or villa in Dubai?" followed by the three pains owners already know: missed deadlines, budget creep and chasing contractors. *Offer:* "fixed budget and timeline in the contract … regular photo and video progress reports". *CTA:* an instant form for "a preliminary estimate in 1 minute". *Why it works:* it names the fear before the solution and asks for very little. It is the longest-running relevant Meta ad found. The pain list is exactly Eastbridge's territory; Eastbridge's honest answer is independent checking, not a contractor's promises.

5. **Smart Renovation, Google and Meta (Google text since 17 Jan 2026, about 300 days; Meta refreshed Oct 2026).** *Hook:* "Trusted by 500+ Homeowners", "Deliver on Time, Within Budget". *Proof:* numbers (15 years, 500+ projects, 4.8 stars). *CTA:* /book/consultation, a form or WhatsApp. *Why it works:* concrete numbers and a booking page rather than the home page. Eastbridge has no UAE numbers and must not invent any, but it can use the UK ones (21 years, Owers House, the RIBA award).

6. **Bond Homes, Meta video "Free Consultation – Fast, tailored 24h quotes" (6.5 months, since 3 May 2026).** *Hook:* speed and certainty ("24h quotes"). *Proof:* "award-winning designers". *CTA:* Get quote. *Why it works:* it promises a quick, specific next step. Eastbridge's equivalent is "Send your contractor's quote; we reply within one working day" (a reply, not a review turnaround).

7. **TaskRight, Meta UGC video "Nobody can price a villa from a photo." (since 23 Sep 2026, 8 weeks and scaling).** *Hook:* a contrarian line that makes the reader distrust what they have been told. *Proof:* it explains how the business is paid ("a flat subscription, never a commission, so there is no cut to build into your quote"). *Why it works:* it turns the business model into the reason to trust it. **This is the template for Eastbridge's independence message:** "We are paid only by you. No contractor pays us anything."

8. **Cavendish Maxwell, Google display "Know what you are buying before completion. Independent technical due diligence" (live since Oct 2026, alongside 45 other live ads).** *Hook:* fear of hidden defects. *Proof:* "independent" and RICS. *CTA:* "Request an inspection". *Why it works:* it sells independence as the product, and it is the only advertiser in the set that does. It also shows that "before you commit" risk messages are being bought in this market.

Worth noting rather than copying: **Twyst Interiors** ("… without living on site to make it happen") is the best hook for overseas owners, and **Redesign Fitout** qualifies people in the ad itself ("We take on full projects only … we'll tell you if we're the right team"). Both started in late October, so they are not yet proven.

**What stopped is a signal too.** Stonehaven, the only owner-side project manager with real Google spend, ran 45 ads from October 2025 and stopped on 29 April 2026. Its copy was aimed at developers ("Results Developers Depend On", "Build Profitably") and mixed in "turnkey" design-and-build. Capital Associated stopped on 11 June 2026. Generic "construction consultant / construction company Dubai" copy aimed at everyone did not last. The ads that lasted are specific: a community, a fear, a price or a WhatsApp button.

## 3. What Eastbridge should copy, adapt or avoid

**Copy**
- **One ad group per community, with the community page as the landing page** (Dar Al Naseeb). Start with Palm Jumeirah, Emirates Hills, Jumeirah Islands, Dubai Hills Estate, Al Barari, District One and Saadiyat (Abu Dhabi). Keep each to phrase and exact match, for example "palm jumeirah villa renovation project manager".
- **WhatsApp as the main contact route** on Google (message asset) and Meta (CTA "Send WhatsApp message"). Almost every Meta advertiser in this market uses it.
- **Pain first, then the answer** (Trust Group, Hammer and Heart, AlignWorks). The pains are missed deadlines, rising costs, chasing contractors, variations and stage payments.
- **Name the business model as the proof** (TaskRight). "Paid only by you. No commission from contractors or suppliers."
- **Content and tools in sitelinks** (DMDC links its "Types of Renovation Firm" page). Use the fees page, the plot-to-keys guide, the quote-review page and the villa build cost calculator.

**Adapt**
- **Cost estimators as lead magnets** (ANK's 10-question quiz, Trust Group's "estimate in 1 minute"). Eastbridge already has /tools/villa-build-cost-calculator/ and /tools/renovate-or-rebuild/. Use them as the Meta landing pages, framed as "a sense check of your budget" so it does not look like a contractor's quote.
- **The speed promise** (Bond's "24h quotes"). Turn it into "Reply within one working day". Do not promise a review turnaround time.
- **Numbers as proof** (Smart Renovation's 500+, Algedra's 13 years). Use only true UK numbers: 21 years running P Chapman Construction, Owers House (Grand Designs, RIBA South West Award 2016), and three independent UAE-based project managers. Never a count of UAE projects.
- **The overseas-owner hook** (Twyst's "without living on site"). Use it for the UK audience, landing on /services/overseas-owners/.
- **"Founder to camera" video** (Azulejon's "I'm Abel, founder … the biggest mistake I see …"). This is the natural format for Philip.

**Avoid**
- "Turnkey", "supervision", "we handle all permits/NOCs", "design and build": competitors lean on these, and they are banned for Eastbridge. They would also blur the one thing that makes Eastbridge different, that it does not build.
- "#1", "best", "top", "Dubai's greatest" (Luxedesign, BG Villas, Bond): these are unverifiable, and Google's policies restrict superlatives without proof.
- Developer-speak ("Build profitably", "Results developers depend on"). Stonehaven aimed at developers and stopped.
- Generic "construction company/consultant Dubai" keywords. They pull in contractors and job seekers (Turner & Townsend's only ads are job adverts).
- Discount and guarantee hooks ("10% off", "money back", "12-month warranty"): wrong for a professional adviser, and they read like a contractor.
- Competitor names in ad copy.

## 4. Eastbridge ad sets

All copy follows the Eastbridge rules: British English, no exclamation marks; no "supervise", "certify", "turnkey", "on your behalf" or obtaining or submitting permits; no UAE projects, clients or experience claimed; fees only as the published ranges; no referral offers. Headline lengths are counted to Google's 30-character limit and descriptions to its 90-character limit.

### Google ad set A: "Owner's side" core (owner's representative / client-side PM)
Landing page: /services/owners-representative/ (UK sub-group: /services/overseas-owners/)

Headlines:
1. Owner's Representative Dubai (28)
2. On the Owner's Side Only (24)
3. Paid Only by You, Never Them (28)
4. We Don't Build. We Check. (25)
5. 21 Years Running a UK Builder (29)
6. Built a Grand Designs House (27)
7. Dubai and Abu Dhabi Villas (26)
8. Every Quote, Payment, Change (28)
9. Fees Published Upfront (22)
10. Free 30-Minute Call (19)
11. Reply Within One Working Day (28)
12. Independent Villa Project Mgr (29)

Descriptions:
1. Independent client-side project management for villa owners in Dubai and Abu Dhabi. (83)
2. No commission from contractors or suppliers. We are paid only by the owner. (75)
3. 21 years running a premium UK builder. Now on the owner's side, checking the work. (82)
4. Reviews AED 9,500–15,000. Full service typically 1.75–3% of build cost. (71)

Assets: WhatsApp message asset (new; copied from Luxedesign and Smart Renovation); call asset +971 56 744 0057; sitelinks Fees, Plot-to-keys guide, Contractor quote review, About Philip; callouts "Paid only by the owner", "No contractor commission", "Dubai and Abu Dhabi", "Free 30-minute call".

### Google ad set B: Community villa renovation and build (the Dar Al Naseeb structure)
One ad group per community, with the community page as the final URL. The example below is Palm Jumeirah (/areas/palm-jumeirah/); swap the community name for Emirates Hills, Jumeirah Islands, Dubai Hills, Al Barari, District One and Saadiyat.
Keywords (phrase/exact): "palm jumeirah villa renovation", "palm jumeirah villa project manager", "renovate villa palm jumeirah", "palm jumeirah villa rebuild".

Headlines:
1. Palm Jumeirah Villa Project (27)
2. Renovating on Palm Jumeirah (27)
3. The Owner's Project Manager (27)
4. We Don't Build. We Check. (25)
5. Check Quotes Before You Sign (28)
6. Stage Payments Checked (22)
7. 21 Years Running a UK Builder (29)
8. Fees Published Upfront (22)
9. Free 30-Minute Call (19)
10. Paid Only by the Owner (22)

Descriptions:
1. Planning a Palm Jumeirah villa renovation? An independent project manager on your side. (87)
2. We check each contractor quote, variation and stage payment before you pay. (75)
3. Not a contractor. We are paid only by you, so our advice has no other interest. (79)
4. Reviews AED 9,500–15,000. Full service typically 1.75–3% of build cost. (71)

### Google ad set C: Contractor quote and contract review (the low-commitment first step)
Landing page: /services/consultant-and-contractor-selection/#quote-review (guide: /guides/quote-review/)
Keywords: "contractor quote review dubai", "villa renovation quote check", "check contractor quote villa", "bill of quantities review dubai", "villa construction contract review dubai".

Headlines:
1. Contractor Quote Review (23)
2. Check It Before You Sign (24)
3. Villa Quote Review, Dubai (25)
4. What Is Missing From the Quote (30)
5. Reviews AED 9,500–15,000 (24)
6. Checked by a 21-Year Builder (28)
7. Independent. Owner-Paid. (24)
8. Exclusions, PC Sums, Payments (29)
9. Send Your Quote on WhatsApp (27)
10. Reply Within One Working Day (28)

Descriptions:
1. Before you sign, we check the scope, exclusions, payment terms and programme. (77)
2. Independent review by a builder of 21 years. We take no commission from any contractor. (87)
3. Published fee: AED 9,500–15,000 per review, agreed before we start. (67)
4. Send the quote on WhatsApp. We reply within one working day to agree the scope. (79)

### Meta concept 1: "Nobody tells you this about a villa quote" (founder video, the TaskRight and Azulejon pattern)
- Format: 30–45 second vertical video of Philip to camera, with subtitles. Placement: Reels and Stories, plus Feed. Audience: UAE, ages 35–65, villa-community and luxury-property interests.
- Primary text: "Building or renovating a villa in Dubai? The cheapest quote is rarely the cheapest build. What is left out of it, and how the stage payments are set, decide what you really pay. I ran a premium UK building company for 21 years. Now I sit on the owner's side and check the quote before you sign. We do not build, and no contractor pays us anything."
- Headline: "Check the quote before you sign"
- Link description: "Reviews AED 9,500–15,000. Free 30-minute call."
- CTA: Send WhatsApp message (secondary version: Learn more to /guides/quote-review/)
- Proof on screen: "21 years running P Chapman Construction" and "Built Owers House, featured on Channel 4's Grand Designs". Any UK footage must be captioned as UK work.

### Meta concept 2: "The three problems" (pain list, the Trust Group pattern)
- Format: single image, a plain text card on the brand colour, or Philip on a UK site captioned as such. Placement: Feed.
- Primary text: "Do you own a villa in Dubai or Abu Dhabi and plan to build or renovate? Most owners meet the same three problems: the programme slips, variations push the cost up, and you end up chasing the contractor yourself. An independent project manager on your side checks every quote, change and stage payment before you pay. Paid only by you. Fees published: reviews AED 9,500–15,000; full service typically 1.75–3% of build cost."
- Headline: "On the owner's side, not the contractor's"
- CTA: Learn more, to /services/villa-renovation-project-management/, or an instant form with three questions (community, build or renovation, stage). Send leads to WhatsApp follow-up.

### Meta concept 3: "Building in Dubai from the UK" (overseas owners; UK audience, where competition is almost nil)
- Format: a three-card carousel. Card 1 "131 decisions between your plot and your keys" (to the plot-to-keys guide). Card 2 "Check costs before you commit" (to /tools/villa-build-cost-calculator/). Card 3 "Who we are: 21 years as a UK builder; three independent UAE-based project managers" (to /about/).
- Audience: UK, ages 40–65, interests in Dubai property, overseas property investment and Grand Designs.
- Primary text: "Building or renovating a villa in Dubai while you live in the UK? The hard part is not the design. It is knowing whether the work, the costs and the payments are right when you cannot be on site. Eastbridge sits on the owner's side: we check each quote, change and stage payment and report back to you in plain English. We do not build, and no contractor pays us."
- Headline: "Your villa in Dubai, checked from the owner's side"
- CTA: Learn more (the guide), with the WhatsApp number in the text.

## 5. Changes to the draft plan (`campaign-plan-nov-2026.md`)

1. **Add the community ad groups** (ad set B). This is the most proven structure found: Dar Al Naseeb has run it for about 280 days. Eastbridge's /areas/ pages already exist. Give it about 30% of the Google budget.
2. **Remove "contractor" from the negative keyword list.** As a broad negative it would block ad group 4 ("contractor quote review dubai") and ad group 6 ("contractor stopped work villa dubai", "villa contractor dispute dubai"). Use narrower negatives instead: "contractor jobs", "contractor license", "contractor vacancy". Also add: "golden visa", "valuation", "nakheel noc", "trakhees", "permit", "approval", "NOC". Approvals searchers want someone to get permits, which Eastbridge cannot offer.
3. **State fees as the full published ranges.** Change "Published fees: reviews from AED 9,500" to "Reviews AED 9,500–15,000. Full service typically 1.75–3% of build cost." "From AED 9,500" is not the published range.
4. **Add a WhatsApp message asset** to the Google campaign, and make "Send WhatsApp message" the default Meta CTA instead of Learn more. It is the market norm on both platforms.
5. **Start Meta with a founder video**, not only stills. Philip-to-camera is the format that lasts (Azulejon 5 months, TaskRight scaling). Keep the portrait still as a second variation.
6. **Lead the UK audience with the overseas-owner angle** (concept 3), and move the UK share of Meta budget up. Almost no one advertises Dubai villa services to UK audiences, so costs should be low. Point Google's UK ad group at /services/overseas-owners/ rather than the owner's-representative page.
7. **Use the cost calculator as a Meta landing page** (copying ANK and Trust Group), with the guide as the second landing page. Fire the GA4 `enquiry_success` event (and a calculator-completion event) before optimising for conversions.
8. **Ad group 5 (plot buyers):** drop "buy villa plot dubai". It draws plot buyers and agents looking for listings (the Meta results for those words were all agencies). Keep "building a villa in dubai" and "how to build a villa in dubai", and add a second landing page, /services/plot-due-diligence/.
9. **Ad group 6:** the page /services/stalled-project-rescue/ exists, so the "check slug" note can go.
10. **Photo captions:** in creative 1 of the draft, label Owers House (Feock, Cornwall) or Quay House as UK projects, so that no ad can be read as showing UAE work.
11. **Headline "Built a Grand Designs House"** is fine and true. A Meta variant could add "RIBA South West Award 2016" (Owers House), which the about page states.
12. **Watch Bauhaus and Kikoola.** Both started villa project-management ads on Meta on 11 Nov 2026, the first owner-side competitors seen on Meta. Re-check the Ad Library in four weeks: if their ads are still running, the format is working.

## Screenshots and raw data

All in `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/` (scratch space: copy anything worth keeping).

Best ads (named by advertiser, format and dates):
- Meta ad cards from the Ad Library:
  - `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/best/meta_ad_trust_group_914823674654563.png`
  - `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/best/meta_ad_taskright_2245057043004115.png`
  - `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/best/meta_ad_bond_homes_961668243040773.png`
  - `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/best/meta_ad_bauhaus_4644254355901205.png`
  - `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/best/meta_ad_kikoola_1884879566012213.png`
  - `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/best/meta_ad_twyst_2190921874855021.png`
  - `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/best/meta_ad_redesign_fitout_2016354652364367.png`
  - `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/best/meta_ad_smart_renovation_1453476976899652.png`
- Google ad renderings from the Transparency Center: `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/best/google_*.png` (28 files, covering Dar Al Naseeb, Luxedesign, Algedra, Smart Renovation, Cavendish Maxwell, DMDC, Stonehaven, BG Villas and Artagroup; the file names carry the first and last shown dates).

Contact sheets of the Google ads:
- `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/sheet_stonehaven_ae_text.png`
- `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/sheet_dar_al_naseeb_text.png`
- `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/sheet_luxedesign_text.png`
- `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/sheet_smartrenovation_ae_text.png`
- `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/sheet_dmdc_text.png`
- `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/sheet_algedra_text.png`
- `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/sheet_capital_associated_text.png`
- `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/sheet_turner_townsend_gb_text.png`
- `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/sheet_cavendish.png`
- `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/sheet_images1.png` (Stonehaven, Luxedesign, Capital Associated and Smart Renovation display ads)
- `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/sheet_villa_builders.png` (Artagroup, BG Villas, Optimal)

Transparency Center advertiser pages: `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/google_stonehaven_advertiser_page.png`, `google_luxedesign_advertiser_page.png`, `google_dmdc_advertiser_page.png` and `google_cavendish_maxwell_advertiser_page.png` (same folder).

Meta search-result pages: `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/final/meta_*.png`. Raw data: `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/final/meta_*.json` (one file per Meta search; `_EMPTY` means no ads returned in three attempts), `/tmp/claude-0/-home-user/83db516c-6210-58dd-9e07-f7c64ebf2422/scratchpad/ads-research/gatc_creatives_round1.json` and `gatc_creatives_round2.json` (every Google creative with its dates), and `gatc_suggestions*.json` (advertiser lookups). Scripts: `meta_scrape.js`, `meta_shot.js`, `gatc_sugg.js`, `gatc_creatives.js` and `run3.py` in the same folder. They can be re-run in about four weeks to see which ads are still live.


Copies of the 36 "best" screenshots are kept in business/ads/competitor-screens/ (the scratchpad copies are temporary).
