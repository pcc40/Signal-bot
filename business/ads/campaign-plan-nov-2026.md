# Paid ads plan (prepared 16 Nov 2026; built PAUSED once Adplane is renewed; nothing spends until Phil says go)

Rules for all ads: British English, no exclamation marks; never supervise/certify/turnkey/"on your behalf"/obtain or submit permits; no UAE projects or clients claimed; fees only as published ranges; no referral offers.

## 1. Google Search — "Owner's side villa project management" (start first)
- Budget: AED 100–150/day (≈ AED 3,000–4,500/month). Bidding: Maximise clicks with a max CPC cap for the first 2 weeks, then Maximise conversions once `enquiry_success` is a GA4 key event imported to Google Ads (Phil: switch the key event in GA4 first).
- Locations: UAE (presence), plus UK (people in or regularly in the UK, interested in UAE) as a separate ad group budget share ≈ 25%.
- Languages: English. Schedule: all days; review search terms weekly.
- Negative keywords from day one: jobs, job, vacancy, salary, career, course, training, certification, pmp, cv, internship, cheap, free, apartment, flat, rent, rental, holiday, airbnb, maintenance company, cleaning, interior design ideas, contractor jobs, contractor license, contractor vacancy, developer jobs, golden visa, valuation, permit, approval, NOC, nakheel noc, trakhees. (Not plain "contractor": it would block ad groups 4 and 6.)

Ad groups (phrase and exact match):
1. Owner's representative — "owner's representative dubai", "owners rep dubai", "client side project manager dubai", "client representative villa dubai", "independent project manager villa dubai" → /services/owners-representative/
2. Villa build PM — "villa construction project manager dubai", "villa project management dubai", "villa project management abu dhabi", "project manager for villa construction", "build villa dubai project manager" → /services/villa-construction-project-management/
3. Renovation PM — "villa renovation project manager dubai", "villa renovation management dubai", "palm jumeirah villa renovation manager", "emirates hills renovation project manager" → /services/villa-renovation-project-management/
4. Quote and contract review — "contractor quote review dubai", "review construction contract dubai villa", "check contractor quote villa", "bill of quantities review dubai" → /services/consultant-and-contractor-selection/#quote-review
5. Plot buyers — "building a villa in dubai", "how to build a villa in dubai", "villa plot construction cost dubai" → /insights/plot-to-keys-villa-owner-decisions-dubai/ (second landing page: /services/plot-due-diligence/)
6. Stalled projects — "contractor stopped work villa dubai", "stalled villa project dubai", "villa contractor dispute dubai" → /services/stalled-project-rescue/ (slug confirmed)

Responsive search ad (shared, adapt per group; ≤30-char headlines, ≤90-char descriptions):
Headlines: Villa Project Manager Dubai | On the Owner's Side, Not Theirs | 21 Years as a UK Builder | We Don't Build. We Check. | Every Quote, Payment, Change | Dubai and Abu Dhabi Villas | Free 30-Minute Call | Fees Published Upfront | Contractor Quote Review | From Plot to Keys | Independent and Owner-Paid | Built a Grand Designs House
Descriptions:
- Independent villa project management for owners in Dubai and Abu Dhabi. Free 30-minute call.
- 21 years running a premium UK builder. Now on the owner's side: quotes, contracts, payments.
- We check every quote, payment and change before you commit. Paid only by you.
- Published fees: reviews AED 9,500–15,000. Full service typically 1.75–3% of build cost.
Assets: sitelinks (Fees, Plot-to-keys guide, Quote review, About Philip), callouts (Paid only by the owner; No commission from contractors; Dubai and Abu Dhabi; Reply within one working day), call asset +971 56 744 0057.

## 1b. Changes from the competitor ads research (16 Nov) — see competitor-ads-research-nov-2026.md
- Add community ad groups (Palm Jumeirah, Emirates Hills, Jumeirah Islands, Dubai Hills Estate, Al Barari, District One, Saadiyat), each landing on its /areas/ page, phrase and exact match only; about 30% of the Google budget. This copies the longest-running structure in the market (Dar Al Naseeb, about 280 days). Copy: ad set B in the research file.
- Use ad sets A (owner's side core) and C (quote review) from the research file as the ad copy for groups 1–4.
- Add a WhatsApp message asset on Google; on Meta the default CTA is "Send WhatsApp message".
- UK ad group lands on /services/overseas-owners/.
- Caption any Owers House or Quay House image as UK work.

## 2. Meta (Facebook/Instagram) test — after Google has run 1–2 weeks
- Objective: Leads (instant form) or Traffic to the plot-to-keys guide; start with Traffic to the guide plus a WhatsApp click CTA, AED 50/day for 14 days.
- special_ad_categories: confirm with Phil (real estate services may fall under "housing" in some regions; check schema before building).
- Audiences: (a) UAE, age 35–65, interests: luxury real estate, property investment, Emaar, Nakheel, Palm Jumeirah, Dubai Hills, interior design (high-end); (b) UK, age 40–65, interests: Dubai property, overseas property investment, Grand Designs.
- Creative: (1) Quay House or Owers House photo, text "Building or renovating a villa in Dubai? 131 decisions between your plot and your keys. We sit on your side for every one." CTA Learn more → guide. (2) Philip portrait, text "21 years as the builder. Now on the owner's side in Dubai and Abu Dhabi." CTA Send WhatsApp message.
- Needs: Facebook Page for Eastbridge (check which Page exists), Meta pixel or Conversions API on the site (not yet installed; add with consent mode before any conversion-optimised campaign).

### Meta revisions (16 Nov research)
- Run the three concepts in the research file: 1 founder video to camera ("Check the quote before you sign"), 2 the three problems (pain list), 3 the UK overseas-owner carousel (131 decisions / cost calculator / who we are). Keep the portrait still as a second variation.
- Give the UK audience a larger share: almost no one advertises Dubai villa services to UK audiences.
- Use the cost calculator as a landing page alongside the guide; set GA4 enquiry_success (and a calculator-completion event) before optimising for conversions.
- Re-check the Ad Library around 14 Dec for Bauhaus and Kikoola (both started owner-side PM ads on Meta 11 Nov).

## Before go-live (Phil)
1. Renew Adplane (adplane.ai) and confirm the Google Ads and Meta ad accounts are connected.
2. In GA4 mark `enquiry_success` as the key event (still open).
3. Confirm budget caps.
