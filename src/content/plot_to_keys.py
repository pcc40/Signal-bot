"""From plot to keys: every decision a villa owner makes (pillar guide, 16 November 2026).

Phil Chapman's brief (16 Nov 2026): "we need to explain the benefit of our service better. A plot purchaser with no
construction knowledge: we can guide them through every step from purchase to keys."

This module is the single source for
  - the guide body at /insights/plot-to-keys-villa-owner-decisions-dubai/ (build.load_insights() calls render(); the
    .md file of the same slug holds only the front matter),
  - its key points, FAQs and sources (so every inline citation is also in the sources list),
  - the "From plot to keys" tiles on the home page (HOME_TILES, pages_new.home()),
  - the guide link on the services pages (link_block()) and the llms.txt summary (LLMS_SUMMARY),
  - Phil's plain Markdown review copy (python3 tools/make_plot_to_keys_md.py writes business/plot-to-keys-guide-review-copy.md).

The number of decisions is counted from STAGES at build time: never type it by hand.

Wording rules (WRITING_BRIEF.md): Eastbridge reads, checks, compares like-for-like, tracks, reports and recommends. The
registered consultant keeps statutory design, authority submissions and statutory site inspections; the contractor
builds. We never instruct the contractor or approve a payment without the owner's written approval. No visit
frequency is promised. Every "You receive" document is a name from DELIVERABLES in services.py (checked below).
Every external fact carries a source from SRC; where a rule varies or could not be confirmed, the text says so.
"""
import re
from config import fee_text, PUBLISH_FEES, FEES, RESPONSE_PROMISE

SLUG = "plot-to-keys-villa-owner-decisions-dubai"
PATH = f"/insights/{SLUG}/"

# ---------------------------------------------------------------- sources (key: title, url[, nofollow])
SRC = {
 "dld": ("Dubai Land Department: property sale registration (fees)", "https://dubailand.gov.ae/en/eservices/request-for-sale-registration"),
 "nakheel-pd": ("Nakheel: Development Control and Planning Approval, preliminary design NOC (example issued June 2026)", "https://www.cgidubai.gov.in/content/Nakheel-PD-approval-PD_IC1-CTYL-16_013_09-Jun-2026.pdf"),
 "dda-soil": ("Dubai Development Authority: Circular 350, soil report review (April 2020)", "https://dda.gov.ae/-/media/DD544423AE174606AC17B53168436FF9.pdf"),
 "dm-proc": ("Dubai Municipality: procedure for the building permit and building completion certificate, villas", "https://dmpmedia.dm.gov.ae/uploads/2020/06/Residential-Buildings_Building-Permits-Procedures.pdf"),
 "law14-mo": ("Dubai Media Office: law regulating engineering consultancy activities (October 2025)", "https://www.mediaoffice.ae/en/news/2025/october/05-10/mohammed-bin-rashid"),
 "law7": ("Mayer Brown: Dubai Law No. 7 of 2025 on contracting activities, what employers need to know (September 2025)", "https://www.mayerbrown.com/en/insights/publications/2025/09/dubai-overhauls-construction-sector-with-new-law-to-regulate-contracting-activities-what-employers-need-to-know-part-2"),
 "ecr28": ("Dubai Executive Council Resolution No. (28) of 2022: insurance policy required for licensing construction works (Dubai Legislation Portal)", "https://dlp.dubai.gov.ae/Legislation%20Reference/2022/Executive%20Council%20Resolution%20No.%20(28)%20of%202022%20Concerning%20the%20Insurance%20Policy%20Required.html"),
 "res275": ("Dubai Municipality Administrative Resolution No. (275) of 2024: replacing engineering firms and contractors (Dubai Legislation Portal)", "https://dlp.dubai.gov.ae/Legislation%20Reference/2024/Administrative%20Resolution%20No.%20(275)%20of%202024%20Replacing%20Engineering%20Firms%20and%20Contracting%20Companies.html"),
 "dm-warn": ("Dubai Municipality: warnings issued to consultancy offices for inflating villa designs (26 August 2025)", "https://www.dm.gov.ae/warnings-issued-to-consultancy-offices-for-inflating-villa-designs/"),
 "propertyfinder-permit": ("Property Finder: how to get a building permit in Dubai (permit validity)", "https://www.propertyfinder.ae/blog/how-to-get-a-building-permit-dubai/"),
 "ev": ("Engel & Völkers: construction cost in Dubai (December 2025)", "https://www.engelvoelkers.com/ae/en/resources/construction-cost-dubai"),
 "optimal": ("Optimal Engineering Consultants: cost to build a villa in Dubai (March 2026)", "https://www.optimal.ae/blog/cost-to-build-a-villa-in-dubai"),
 "tt": ("Turner & Townsend: UAE market intelligence 2025, construction cost performance", "https://marketintelligence.turnerandtownsend.com/uaemi-2025/construction-cost-performance/"),
 "pwc": ("PwC Worldwide Tax Summaries: United Arab Emirates, other taxes (VAT and customs duty)", "https://taxsummaries.pwc.com/united-arab-emirates/corporate/other-taxes"),
 "fta": ("Federal Tax Authority: VAT refund for UAE nationals building new residences", "https://tax.gov.ae/en/services/vat.refund.for.uae.nationals.homebuilders.aspx"),
 "dla": ("DLA Piper, Global Construction Bulletin: security of payment, UAE (October 2025)", "https://www.dlapiper.com/en/insights/publications/global-construction-bulletin/2025/september-2025/security-of-payment-uae"),
 "tamimi-adv": ("Al Tamimi & Company: highlights of the laws of the UAE, China and the common law (advance payments)", "https://www.tamimi.com/law-update-articles/highlights-of-the-laws-of-the-united-arab-emirates-the-peoples-republic-of-china-and-the-common-law/"),
 "klgates": ("K&L Gates: the impact of the new Civil Transactions Law on construction contracts in the UAE (March 2026)", "https://www.klgates.com/The-Impact-of-the-New-Civil-Transactions-Law-on-Construction-Contracts-in-the-United-Arab-Emirates-3-9-2026"),
 "bracewell": ("Bracewell: the UAE's new Civil Code explained (effective date and transition)", "https://www.bracewell.com/resources/the-uaes-new-civil-code-explained-practical-changes-for-businesses-and-investors/"),
 "kay-dec": ("Kayrouz & Associates: decennial liability and the new UAE Civil Code (2026)", "https://www.kayrouzandassociates.com/insights/decennial-liability-uae-contractors-engineers-2026"),
 "kay-ret": ("Kayrouz & Associates: retention and the final account in UAE construction (October 2026)", "https://www.kayrouzandassociates.com/insights/retention-final-account-uae-construction"),
 "rics-hka": ("RICS: construction disputes in the Middle East, reporting HKA's CRUX research (February 2023)", "https://www.rics.org/news-insights/wbef/construction-disputes-in-the-middle-east-managing-the-worlds-highest-risk-of-overruns"),
 "nakheel": ("Nakheel: customer FAQs (NOCs, access permits, contractor requirements)", "https://www.nakheel.com/en/contact-us"),
 "adm-estidama": ("Abu Dhabi City Municipality: sustainable building and the Estidama Pearl rating (8 January 2025)", "https://www.dmt.gov.ae/en/adm/Media-Centre/News/08Jan2025"),
 "dmt-occ": ("Abu Dhabi DMT: Building Occupancy and Legalisation Certificate Programme (October 2024)", "https://www.dmt.gov.ae/en/Media-Centre/News/DMT-Unveils-New-Building-Occupancy-and-Legalisation-Certificate-Programme-in-Abu-Dhabi"),
 "dewa-water": ("DEWA: getting water connections (builder services)", "https://dewa.gov.ae/en/builder/electricity-network-services/getting-water-connection"),
 "dewa-elec": ("DEWA: getting electricity permits and connections (builder services)", "https://www.dewa.gov.ae/en/builder/electricity-network-services/getting-electricity-connection"),
 "hassantuk": ("The National: Hassantuk fire alarm system mandatory in villas from 1 January 2024", "https://www.thenationalnews.com/uae/2024/01/19/dubai-civil-defence-expects-hassantuk-fire-alarm-system-in-all-villas-by-end-of-2024"),
 "midday": ("Khaleej Times: UAE midday break starts 15 June 2026", "https://www.khaleejtimes.com/uae/uae-midday-break-starts-june-15-work-under-direct-sunlight-banned-during-peak-afternoon-hours?amp=1"),
}
_used = []

def cite(key, label):
    """An inline citation link; records the source so the sources list holds exactly what the text cites."""
    title, url = SRC[key][:2]
    if key not in _used:
        _used.append(key)
    return f'<a href="{url}" rel="noopener">{label}</a>'

# ---------------------------------------------------------------- stages
# when: (duration, basis). basis "ours" = our own planning allowance; otherwise the named source.
# decide: the decisions, one line each (these are what is counted). who: (party, what stays with them).
# eb: what Eastbridge does. docs: document names from DELIVERABLES. links: further reading on this site.
def _stages():
    c = cite
    return [
 {"id": "before-you-buy", "title": "Before you buy the plot",
  "when": ("1 to 3 weeks", "ours"),
  "lede": "Everyone quotes the plot price. What the rules let you build, by when, and at what cost decides whether it is a good purchase.",
  "decide": [
   "Whether the house you want fits the permitted area, coverage, height and floors.",
   "Whether you can live with the setbacks and the rules on style and materials.",
   "Whether you can meet any build-by deadline in the sale terms.",
   "Whether the service charges are acceptable every year, built or not.",
   "Whether to pay for a soil investigation and level survey before you commit.",
   "Whether access, orientation, neighbours and views suit the house.",
   "Whether the whole budget works: plot, fees, build, VAT, contingency, landscape and furniture.",
   "Whether to buy, negotiate or walk away.",
  ],
  "cost": f"A plot sold \"with approved drawings\" may come with nothing you can use. One Nakheel preliminary design approval, published in June 2026, was valid for six months at most unless extended in writing, and stayed subject to the plot's sale agreement ({c('nakheel-pd', 'Nakheel')}). Build-by deadlines and penalties vary by developer and by sale. We found no published standard, so read yours.",
  "who": [
   ("The master developer", "sets the plot's development controls, design guidelines and any deadline to build."),
   ("Your lawyer", "checks title and the terms you are asked to sign."),
  ],
  "eb": [
   "We read the design guidelines and the sale terms, and tell you what they allow and commit you to.",
   "We look at the plot as a builder would: access, levels, neighbours and buildability.",
   "We price the whole project, in a written report within five working days of receiving the plot documents.",
  ],
  "docs": ["Written plot review report", "Design guideline summary", "Build budget range", "Questions for the seller or developer"],
  "links": [("/services/plot-due-diligence/", "Plot and pre-purchase review"), ("/insights/buying-a-villa-plot-in-dubai-checks/", "Plot checks before you pay"),
            ("/tools/villa-build-cost-calculator/", "Villa build cost calculator"), ("/areas/dubai-islands/", "Dubai Islands"), ("/areas/palm-jebel-ali/", "Palm Jebel Ali")],
 },
 {"id": "buying", "title": "Buying the plot",
  "when": ("2 to 6 weeks", "ours"),
  "lede": "The purchase is a legal transaction with construction consequences. What you sign sets the rules for what you build.",
  "decide": [
   "Which UAE-qualified lawyer reads the sale agreement before you sign.",
   "Whose name the plot goes in: yours, joint names or a company.",
   "Whether to accept the building obligations, resale restrictions and penalties as written.",
   "How you pay: cash, the developer's payment plan or finance.",
   "Who bears the transfer fees, which the agreement decides.",
   "Whether any design approvals the seller holds can pass to you.",
   "What you must hold at handover: title deed, plot plan, development controls and cleared charges.",
  ],
  "cost": f"Dubai Land Department lists the sale registration fee as 2% of the sale value for the seller and 2% for the buyer, plus a service partner fee of AED 4,000 and VAT ({c('dld', 'Dubai Land Department')}). The two 2% shares come to AED 400,000 on a plot of AED 10 million. Who actually pays is whatever your agreement says.",
  "who": [
   ("Your lawyer", "advises on the agreement and the transfer. We do not give legal advice."),
   ("Dubai Land Department", "registers the sale and issues the title deed. Abu Dhabi has its own registration process."),
  ],
  "eb": [
   "We read the sale terms as a builder: build-by dates, penalties and design obligations, flagged for your lawyer.",
   "We check the plot documents against what a consultant will ask for on day one.",
   "We update the total budget with the real purchase and transfer costs.",
  ],
  "docs": ["Sale terms notes", "Questions for the seller or developer"],
  "links": [("/services/plot-due-diligence/", "Plot and pre-purchase review"), ("/glossary/#affection-plan", "What an affection plan is"), ("/areas/hudayriyat/", "Hudayriyat"), ("/areas/saadiyat/", "Saadiyat")],
 },
 {"id": "brief-and-budget", "title": "Brief and budget",
  "when": ("2 to 6 weeks", "ours"),
  "lede": "The brief is the cheapest document to change and the one that fixes most of the cost. Nobody else is paid to write it for you.",
  "decide": [
   "The rooms: bedrooms, living rooms, majlis, staff rooms, study, gym, garages.",
   "The size, and whether the plot and the money both allow it.",
   "Basement or no basement.",
   "The quality level, which sets the rate per square foot.",
   "What the budget covers beyond construction: fees, VAT, pool, landscape, kitchens, furniture.",
   "How much contingency to hold, and who holds it.",
   "How the build is funded, and what cash is needed each month.",
   "The date you want to move in, and how fixed it is.",
   "What you will not compromise on, and what goes first if money is tight.",
  ],
  "cost": f"A budget built on a rate per square foot is short before the first drawing. Published guides put design and engineering at 6 to 12% of the contract value ({c('optimal', 'Optimal Engineering')}) and contingency at 10 to 15% ({c('ev', 'Engel &amp; Völkers')}); VAT is 5% ({c('pwc', 'PwC')}). UAE nationals building their own home can reclaim that VAT; other owners cannot ({c('fta', 'Federal Tax Authority')}).",
  "who": [
   ("You", "own the brief and the budget. No licensed party is responsible for either unless you appoint one."),
   ("Your registered consultant", "designs to the brief, so the brief should exist first."),
  ],
  "eb": [
   "We write the brief with you: rooms, sizes, finishes and priorities.",
   "We build the budget from the brief and the plot, with the contingency held by you, not the contractor.",
   "We set a programme showing the decisions you need to make and when, and forecast what falls due each month.",
  ],
  "docs": ["Brief, budget and programme", "Payment and cash-flow forecast"],
  "links": [("/tools/villa-build-cost-calculator/", "Villa build cost calculator"), ("/tools/stage-payment-planner/", "Stage payment planner"),
            ("/insights/villa-construction-cost-dubai/", "What a villa costs to build"), ("/services/design-and-approvals/", "Design brief and budget")],
 },
 {"id": "consultant", "title": "Choosing the architect and registered consultant",
  "when": ("3 to 6 weeks", "ours"),
  "lede": "In Dubai only a registered engineering consultancy may design your villa and deal with the authority. Which firm, and on what terms, is your choice.",
  "decide": [
   "A separate consultant and contractor, or one design-and-build firm.",
   "Which firms to approach, and whether each is registered for villa work.",
   "One firm for everything, or a lead architect with a local registered consultant.",
   "The scope: interiors, landscape, pool, lighting and statutory site inspection, or only some.",
   "The fee basis: a percentage of build cost, a lump sum or a fee per stage.",
   "The appointment terms: payments, insurance, termination and who owns the design.",
   "Who the named designer is, and how much of their time you are buying.",
   "Whether the interior designer and landscape architect are appointed now or later.",
  ],
  "cost": f"In August 2025 Dubai Municipality warned consultancy offices for exaggerated structural designs on citizens' villas that caused unjustified increases in construction cost ({c('dm-warn', 'Dubai Municipality')}). A fee set as a percentage of build cost does nothing to discourage that. And the cheapest fee proposal is often the one with the most left out.",
  "who": [
   ("Your registered consultant", f"is a firm authorised to practise engineering consultancy in Dubai; nobody may do so without authorisation ({c('law14-mo', 'Dubai Law No. 14 of 2025')}). Statutory design, authority submissions and statutory site inspections are theirs."),
   ("You", "appoint and pay the consultant directly."),
  ],
  "eb": [
   "We help you shortlist firms, and check licences and registrations through the official registries.",
   "We compare fee proposals like-for-like, so nothing is missing from the scope you pay for.",
   "We read the appointment and give you the points to raise before you sign.",
  ],
  "docs": ["Shortlist with reasons", "Licence and registration check record", "Contract terms notes"],
  "links": [("/insights/design-build-vs-separate-architect-villa/", "Design and build or a separate architect"), ("/services/consultant-and-contractor-selection/", "Choosing the team"),
            ("/insights/owners-representative-vs-project-manager-vs-consultant/", "Who does what"), ("/insights/dubai-municipality-villa-over-design-warning/", "The over-design warning")],
 },
 {"id": "design", "title": "Design: concept, developed and detailed",
  "when": ("3 to 6 months", "ours"),
  "lede": "Design is the cheapest place to change your mind and the most expensive place to lose control of cost.",
  "decide": [
   "The concept: layout, massing and where the house sits on the plot.",
   "The structure: spans, cantilevers and basement, each justified against the code.",
   "The glazing: sizes, sliding systems and solar control.",
   "The air conditioning: the system, the plant location and the noise.",
   "The interiors: kitchens, bathrooms, joinery and lighting, designed now or later.",
   "The pool, the landscape and the external levels.",
   "Home automation, audio-visual and security.",
   "Which products the specification names, and which it leaves as allowances.",
   "What to cut when a cost check comes in over budget, and what never to cut.",
   "The design freeze: the date after which every change is a variation.",
  ],
  "cost": f"Research into large Middle East projects found the two leading causes of trouble were changes to scope and design information that arrived late or incomplete ({c('rics-hka', 'RICS, reporting HKA')}). A villa is smaller; the mechanism is the same. As the builder in the UK, the costliest changes we saw were interior decisions made after the services were in the walls.",
  "who": [
   ("Your registered consultant", "produces the design and is responsible for it meeting the building code."),
   ("You", "approve each stage in writing. Later changes are measured against that signature."),
  ],
  "eb": [
   "We check the design against the budget at concept, at detailed design and before pricing.",
   "Where structure or services cost looks high, we give you the questions to put to your consultant.",
   "We keep the decision log and keep your decisions on time.",
  ],
  "docs": ["Design-stage cost check notes", "Value review notes", "Decision log"],
  "links": [("/services/design-and-approvals/", "Design and approvals management"), ("/services/materials-and-specialist-sourcing/", "Materials and specialist sourcing"),
            ("/glossary/#value-engineering", "Value engineering explained"), ("/areas/emirates-hills/", "Emirates Hills")],
 },
 {"id": "approvals", "title": "Surveys and approvals",
  "when": ("4 to 8 weeks for a straightforward project", "optimal"),
  "lede": "Two approvals, in order: the master developer's, then the authority's. Your consultant applies. Your part is the surveys, the signatures and the fees.",
  "decide": [
   "When to commission the soil investigation and the topographic survey.",
   "Whether to seek the developer's concept approval before the design is finished.",
   "How to answer the developer's comments: redesign, or make the case.",
   "When the design is complete enough to go to the authority.",
   "Whether to apply for early works, such as excavation, ahead of the main permit.",
   "Paying the developer, authority and utility fees on the day they are due.",
   "Whether a change after approval is worth a resubmission.",
  ],
  "cost": f"Approvals expire. One property portal's guide says a Dubai Municipality permit should be issued within nine months of the drawings being approved, unless an extension is requested, and is then valid for two years ({c('propertyfinder-permit', 'Property Finder')}); we could not confirm this from the authority itself, so ask your consultant. The soil report comes before the foundations are designed; in Dubai Development Authority areas a single villa needs at least two boreholes ({c('dda-soil', 'DDA')}). In Abu Dhabi, a one-pearl Estidama rating is essential for a private project's building permit ({c('adm-estidama', 'Abu Dhabi City Municipality')}).",
  "who": [
   ("Your registered consultant", f"prepares and submits the applications ({c('dm-proc', 'Dubai Municipality')})."),
   ("The authority", "is Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where your plot sits; in Abu Dhabi, the municipality through TAMM."),
  ],
  "eb": [
   "We track every application with your consultant: what has been sent, what is waiting, and on whom.",
   "We keep your signatures, documents and fees ahead of the dates they are needed.",
   "We sit beside you at meetings with the consultant and the developer.",
  ],
  "docs": ["Approvals tracker"],
  "links": [("/insights/dubai-municipality-villa-building-permit/", "Dubai villa building permits"), ("/insights/which-dubai-authority-covers-my-villa/", "Which authority covers your plot"),
            ("/insights/abu-dhabi-villa-permit-tamm/", "Abu Dhabi permits through TAMM"), ("/insights/nakheel-noc-villa-renovation/", "The Nakheel NOC")],
 },
 {"id": "tender", "title": "Tender and choosing the contractor",
  "when": ("4 to 8 weeks", "ours"),
  "lede": "Contractor bids rarely compare directly. On paper the cheapest wins. In the final account it often does not.",
  "decide": [
   "Who to invite, and whether each is licensed and classified for your villa.",
   "Whether the drawings are complete enough to price.",
   "A priced bill of quantities, or drawings and specification only.",
   "Which items are left as provisional sums, and at what allowance.",
   "How bidders' questions are answered, so that all price the same thing.",
   "How to compare: on like-for-like totals, not the headline price.",
   "Who to interview, and which past clients to call.",
   "What to negotiate first: price, programme and the named site team.",
   "Who to appoint.",
  ],
  "cost": f"Since January 2026, contractors in Dubai must be on a single register and may only take work within their classification. Fines go up to AED 100,000, and an owner who engages a non-compliant contractor can be investigated too ({c('law7', 'Mayer Brown on Dubai Law No. 7 of 2025')}). Existing contractors were given a year to comply, so check on the day you appoint.",
  "who": [
   ("Your registered consultant", "normally puts together the bid package: drawings, specification and any bill of quantities."),
   ("You", "decide who is invited and who is appointed."),
  ],
  "eb": [
   "We check each bidder's licence and registration through the official registries.",
   "We put every bid into one like-for-like table: exclusions, provisional sums, preliminaries and programme.",
   "We call past clients, sit beside you at the interviews and give you a written recommendation.",
  ],
  "docs": ["Normalised tender comparison", "Reference call notes", "Written recommendation"],
  "links": [("/insights/how-to-choose-a-villa-contractor-dubai/", "How to choose a villa contractor"), ("/services/consultant-and-contractor-selection/#quote-review", "Contractor quote review"),
            ("/insights/contractor-quote-review-villa-dubai/", "How a quote review works"), ("/glossary/#provisional-sum", "Provisional sums")],
 },
 {"id": "contract", "title": "The contract",
  "when": ("2 to 4 weeks", "ours"),
  "lede": "The contract decides who carries each risk. Most of it is negotiable until the day you sign, and very little afterwards.",
  "decide": [
   "The form: Dubai Municipality's guidance contract, a FIDIC form or the contractor's own.",
   "The price: lump sum, remeasured or a blend.",
   "The payments: monthly against work valued on site, or fixed stages.",
   "The advance payment, and the bank guarantee that secures it.",
   "The retention: how much, and when each part is released.",
   "The performance bond: its amount, wording and expiry date.",
   "The completion date and the rate of delay damages.",
   "Who may instruct a variation, and that it is priced first.",
   "What insurance the contractor carries, and for how long.",
   "The defects period, termination and how disputes are resolved.",
  ],
  "cost": f"An advance of 10 to 20% is described as industry practice ({c('tamimi-adv', 'Al Tamimi')}): AED 500,000 on a contract of AED 5 million, paid before a block is laid, and unsecured without a guarantee. Retention is commonly 10%, with half released at handover and half after the defects period ({c('dla', 'DLA Piper')}). And a UAE court can reduce pre-agreed delay damages; for contracts made from 1 June 2026, the new Civil Code sets out when ({c('klgates', 'K&amp;L Gates')}).",
  "who": [
   ("Your lawyer", "advises on the contract's legal effect. Take advice from a UAE-qualified lawyer before you sign."),
   ("Your registered consultant", "is usually named in the contract to value payments and issue instructions."),
  ],
  "eb": [
   "We read the draft the way a contractor reads it: Philip signed building contracts as the contractor, in the UK, at P Chapman Construction for 21 years.",
   "We set out the payment, retention, bond, delay and variation terms, with the points to raise before you sign.",
   "We test the payment schedule against the programme, so payments do not run ahead of the work.",
  ],
  "docs": ["Contract terms notes", "Payment and cash-flow forecast"],
  "links": [("/insights/villa-construction-contracts-uae/", "UAE villa construction contracts"), ("/tools/stage-payment-planner/", "Stage payment planner"),
            ("/glossary/#retention", "Retention"), ("/glossary/#performance-bond", "Performance bond")],
 },
 {"id": "before-work-starts", "title": "Before work starts",
  "when": ("2 to 4 weeks", "ours"),
  "lede": "Between signing and the first day on site, the rules of the job are set. Every later argument is measured against them.",
  "decide": [
   "The start date, and whether permit, contract and guarantees are in place for it.",
   "Whether to release the advance before the guarantee and insurance are in your hands.",
   "The baseline programme, against which every delay is measured.",
   "The named site team and the main subcontractors.",
   "The site set-up: fence, access, working hours, and what the neighbours are told.",
   "Who may instruct the contractor, and how questions and payments will run.",
   "Your decision schedule: every choice still to make, with its last date.",
   "Which long-lead items to order now.",
  ],
  "cost": f"In Dubai, before a new building's permit is issued, the contractor must give the authority an insurance policy covering the works and third parties until a year after the completion certificate ({c('ecr28', 'Executive Council Resolution No. 28 of 2022')}). Nakheel also requires a security deposit, a site access permit and a site fence ({c('nakheel', 'Nakheel')}). A contractor who has not allowed for these starts late, or charges them as extras.",
  "who": [
   ("The contractor", "holds the works insurance, pays the developer's deposit, sets up the site and is responsible for safety on it."),
   ("Your registered consultant", "takes up the statutory site inspection role."),
  ],
  "eb": [
   "We check the guarantee, the bond and the insurance before we recommend that you release the advance.",
   "We test the contractor's programme: the critical path, the lead times and the dates that depend on you.",
   "We set up the records and the risk register from day one.",
  ],
  "docs": ["Programme review notes", "Record-keeping set-up", "Risk register"],
  "links": [("/services/cost-and-programme-control/", "Cost and programme control"), ("/insights/how-long-to-build-a-villa-dubai/", "How long a villa takes to build"),
            ("/areas/palm-jumeirah/", "Palm Jumeirah"), ("/glossary/#mobilisation", "Mobilisation")],
 },
 {"id": "construction", "title": "Construction",
  "when": ("12 to 18 months, typically", "optimal"),
  "lede": "The contractor builds and your consultant carries out the statutory inspections. Your decisions now arrive one after another, each with a date on it.",
  "decide": [
   "Each month: how much to pay against the contractor's payment application.",
   "Each variation: accept, reject or negotiate before it is built.",
   "Each sample and mock-up: stone, façade, joinery, paint and fittings.",
   "Each question from site, answered by the date the programme needs.",
   "Each claim for more time: granted, refused or granted in part.",
   "Whether work that is not right is redone before it is covered over.",
   "When to release contingency, and for what.",
   "When to visit, and what to see in person.",
   "What to order from abroad, when, and who imports it.",
   "Whether the programme is still realistic, and what to do if not.",
  ],
  "checks": ("The stages worth seeing before they are covered up",
             "Setting out; foundations and below-ground waterproofing; each slab before the concrete is poured; roof and wet-room waterproofing under test; "
             "pipes, ducts and cables before walls and ceilings are closed; plaster; glazing; fittings; finishes. "
             f"The authority's own inspections cover shoring and foundations, then the structure ({c('dm-proc', 'Dubai Municipality')})."),
  "cost": f"Delay is paid for monthly. Turner &amp; Townsend puts a contractor's preliminaries, the cost of running the site, at about 12% on a small Dubai project ({c('tt', 'Turner &amp; Townsend')}), and those costs continue every month a job overruns. Summer is slower too: outdoor work under direct sun stops from 12:30pm to 3pm between 15 June and 15 September ({c('midday', 'Khaleej Times')}).",
  "who": [
   ("The contractor", "builds, runs the site, and is responsible for workmanship and safety."),
   ("Your registered consultant", "carries out the statutory site inspections and usually values the payments under the contract."),
  ],
  "eb": [
   "We are on site regularly, at the frequency agreed in your scope of works, and photograph work before it is covered up.",
   "We check each payment application against the work in place and the contract, and recommend an amount before you pay.",
   "We test each variation: is it a genuine change, is the price fair, and what does it do to time?",
   "We never instruct the contractor or approve a payment without your written approval.",
  ],
  "docs": ["Site note after every visit", "Monthly cost and programme report", "Payment-application review notes", "Variation register", "Decision log"],
  "links": [("/insights/owner-site-visits-villa-build/", "The visits an owner should make"), ("/services/site-visits-and-reporting/", "Site visits and reporting"),
            ("/services/variations-delays-and-claims/", "Variations, delays and claims"), ("/tools/delay-cost-estimator/", "Delay cost estimator"),
            ("/insights/what-the-contractor-knows/", "What the contractor knows")],
 },
 {"id": "fit-out", "title": "Fit-out, joinery, kitchens, landscape and pool",
  "when": ("the second half of construction", "ours"),
  "lede": "The things you will touch every day are chosen here, and this is where programmes slip.",
  "decide": [
   "Who supplies each item: the contractor, or you directly.",
   "The kitchen: the maker, the appliances and the date its drawings are fixed.",
   "The joinery: the workshop, the samples and the shop drawings.",
   "The stone and tiles: the slabs themselves, and a mock-up on site.",
   "Sanitaryware, ironmongery and light fittings, each with an order-by date.",
   "The pool: finish, plant, and a water test before it is tiled.",
   "The landscape: planting, irrigation, lighting, walls and gates.",
   "Loose furniture, curtains and art: the budget and the delivery date.",
   "Which choices to make in person, at the quarry, workshop or showroom.",
  ],
  "cost": f"Goods bought abroad arrive with tax and paperwork attached: customs duty is generally 5% of the cost, insurance and freight value, with VAT on top ({c('pwc', 'PwC')}). An item that lands late, or does not match the sample, holds up every trade behind it. If you bought it yourself, that delay is yours.",
  "who": [
   ("The fit-out contractor and specialists", "make and fit their own packages."),
   ("The main contractor", "coordinates the trades and, where the contract says so, receives, stores and fits owner-supplied items."),
  ],
  "eb": [
   "We keep a sourcing schedule: each item, its supplier, lead time and order-by date.",
   "With the full service we travel with you to choose stone, joinery, lighting and fittings; trips are agreed in your scope first.",
   "We check each delivery against the sample you approved, and take no commission from any supplier.",
  ],
  "docs": ["Sourcing schedule", "Sample record", "Owner-supplied items schedule", "Delivery check note"],
  "links": [("/services/materials-and-specialist-sourcing/", "Materials and specialist sourcing"), ("/insights/sourcing-materials-abroad-dubai-villa/", "Sourcing materials abroad"),
            ("/insights/villa-fit-out-dubai/", "Fitting out a villa"), ("/areas/jumeirah-bay/", "Jumeirah Bay")],
 },
 {"id": "utilities", "title": "Utilities, testing and commissioning",
  "when": ("2 to 6 weeks", "ours"),
  "lede": "A finished house with no permanent power is not finished. Connections run to other people's timetables.",
  "decide": [
   "When to apply for permanent power and water, so completion is not held up.",
   "Paying the connection charges and deposits when they are raised.",
   "Which telecoms provider, and where the fibre comes in.",
   "Which tests you want witnessed: air conditioning, water, drainage, pool, lighting and security.",
   "The fire alarm link that villas now need.",
   "Whether to accept any system you have not seen working.",
   "Who is shown how to run the house: you, your family and your staff.",
  ],
  "cost": f"DEWA says a small water meter is connected within three working days, once the charges are paid, the site is ready and the documents are in ({c('dewa-water', 'DEWA')}). Each condition is a chance to lose a week. The Hassantuk fire alarm link has been compulsory in villas since 1 January 2024 ({c('hassantuk', 'The National')}). Abu Dhabi has its own utility and its own steps.",
  "who": [
   ("Your consultant and contractor", f"apply for the connections through the authority's system ({c('dewa-elec', 'DEWA')})."),
   ("The specialist subcontractors", "commission their own systems and demonstrate them."),
  ],
  "eb": [
   "We track the connection applications with your consultant and contractor.",
   "We witness commissioning: air conditioning, water, pool, lighting controls and security.",
   "We record which systems we saw tested and demonstrated, and what was outstanding.",
  ],
  "docs": ["Approvals tracker", "Commissioning record"],
  "links": [("/services/snagging-and-handover/", "Snagging and handover"), ("/glossary/#commissioning", "Commissioning"), ("/glossary/#dewa-connection", "DEWA connection")],
 },
 {"id": "completion", "title": "Completion",
  "when": ("2 to 4 weeks", "ours"),
  "lede": "Completion is a legal event as well as a physical one. The documents matter as much as the paint.",
  "decide": [
   "Whether the villa is finished enough to call for the final inspection.",
   "Whether to accept completion with outstanding work listed.",
   "What you sign, knowing it starts the defects period and releases retention.",
   "Whether the handover file is complete before the completion payment is released.",
   "When the contractor's insurance ends and your own begins.",
   "Whether you can reclaim VAT on the build, and by when.",
   "When furniture arrives, and who is liable for damage to it.",
  ],
  "cost": f"In Dubai the completion certificate follows a joint final inspection, and the permanent connections follow the certificate ({c('dm-proc', 'Dubai Municipality')}). For UAE nationals, the VAT refund on a new home must be claimed within 12 months of completion ({c('fta', 'Federal Tax Authority')}). In Abu Dhabi, a 2024 programme introduced building occupancy certificates; existing villas are exempt, and the announcement does not say how it applies to a new private villa, so ask your consultant ({c('dmt-occ', 'DMT')}).",
  "who": [
   ("Your consultant and contractor", "request the final inspection; the authority issues the building completion certificate."),
   ("The master developer", "issues its final clearance and returns deposits under its own rules, which vary by community."),
  ],
  "eb": [
   "We check the handover file item by item: completion certificate, as-built drawings, warranties, manuals and test certificates.",
   "We read what you are asked to sign and tell you what it starts, before you sign it.",
   "We review the payment due at completion against what is still outstanding, and recommend an amount.",
  ],
  "docs": ["Close-out document list", "Payment-application review notes"],
  "links": [("/glossary/#building-completion-certificate", "Building completion certificate"), ("/glossary/#as-built-drawings", "As-built drawings"),
            ("/insights/villa-snagging-checklist-dubai/", "Villa snagging checklist")],
 },
 {"id": "handover", "title": "Snagging and handover",
  "when": ("4 to 8 weeks", "ours"),
  "lede": "Handover is the last moment your payment still has weight. A good one is quiet: a short list, systems demonstrated, documents waiting.",
  "decide": [
   "When to inspect: in sections as areas finish, or once at the end.",
   "What stops handover, and what is a snag to close afterwards.",
   "The date by which the contractor must close each item.",
   "Whether to move in with snags still open.",
   "How much to hold against open items, as far as the contract allows.",
   "Who attends the final walk-through: you in person, or on a video call.",
   "Whether to sign the handover document, with the snag list attached.",
  ],
  "cost": "From the builder's side, snag lists stall when they are vague, long or late, and they stall for good once the money has gone. Retention and the final payment are your leverage. A document saying the villa was accepted free of defects, signed while items are open, gives that leverage away.",
  "who": [
   ("The contractor", "puts right every item on the agreed list."),
   ("You", "accept the house. Whatever is signed at handover is your decision."),
  ],
  "eb": [
   "We inspect room by room and system by system, before the payment, not after it.",
   "We compile the snag list, numbered, located, photographed and graded, and track every item to close-out.",
   "Snagging and handover are one stage of our full service. They are not sold on their own.",
  ],
  "docs": ["Pre-handover inspection notes", "Snag list", "Close-out document list"],
  "links": [("/services/snagging-and-handover/", "Snagging and handover"), ("/guides/villa-snagging-checklist/", "Free villa snagging checklist"),
            ("/insights/villa-snagging-checklist-dubai/", "What to inspect, room by room"), ("/areas/dubai-hills-estate/", "Dubai Hills Estate")],
 },
 {"id": "defects-period", "title": "The defects period and the years after",
  "when": ("commonly 12 months, then 10 years of liability for the structure", "kay-ret"),
  "lede": "A new villa meets its first summer and its first heavy rain after you move in. The contract gives you a period to have what they reveal put right.",
  "decide": [
   "How defects are reported, and how quickly the contractor must respond.",
   "What to test in the first summer and after the first heavy rain.",
   "When to hold the end-of-period inspection: before the period ends.",
   "Whether the rest of the retention has been earned.",
   "The final account: the last variations and provisional sums, line by line.",
   "The maintenance contracts for air conditioning, pool, lifts and landscape.",
   "Where the drawings, warranties and records are kept for ten years.",
  ],
  "cost": f"The defects period is whatever your contract says; twelve months for building work is a common example ({c('kay-ret', 'Kayrouz &amp; Associates')}). Separately, UAE law makes the contractor and the engineer jointly liable for ten years for collapse and for defects that threaten the building's stability or safety ({c('kay-dec', 'Kayrouz &amp; Associates')}). That does not cover finishes or ordinary faults.",
  "who": [
   ("The contractor", "returns to put right defects notified within the period."),
   ("The contractor and the engineer", f"carry the ten-year liability: under the 1985 Civil Transactions Law, or Federal Decree-Law No. 25 of 2025 for contracts made from 1 June 2026 ({c('bracewell', 'Bracewell')})."),
  ],
  "eb": [
   "We keep the defects register: what was reported, when, and when each item was closed.",
   "We recommend whether the retention has been earned, and say what is still open.",
   "We check the final account line by line, with the records behind every figure, and recommend what to agree.",
  ],
  "docs": ["Defects register", "Retention release recommendation", "Final account statement"],
  "links": [("/insights/defects-liability-period-uae/", "The defects liability period in the UAE"), ("/glossary/#decennial-liability", "Decennial liability"), ("/glossary/#final-account", "Final account")],
 },
 {"id": "when-things-go-wrong", "title": "When things go wrong",
  "when": ("at any point", "ours"),
  "lede": "Contractors run out of cash. Consultants go quiet. Claims arrive. The first decisions are the hardest to undo.",
  "decide": [
   "Whether to keep paying, and against what.",
   "Whether to continue with the contractor, renegotiate or replace.",
   "When to bring in a UAE-qualified lawyer: before you withhold money or end the contract.",
   "How to secure the site, the materials and the records.",
   "Whether to call on the bond or the guarantee before it expires.",
   "Who finishes the house, and at what price.",
  ],
  "cost": f"Replacing a contractor is a procedure, not a phone call. Where Dubai Municipality issued the permit, the replacement needs a new permit in its own name before it can start ({c('res275', 'Administrative Resolution No. 275 of 2024')}). Without a record of what is built and what is paid, the new contractor prices every unknown as risk.",
  "who": [
   ("Your lawyer", "advises on your rights, on termination and on any call on a bond."),
   ("Your registered consultant", "makes the application to the authority and reports on the state of the works."),
  ],
  "eb": [
   "We start within a week and give you the full picture within two to three weeks: what is built, to what standard, and what has been paid.",
   "We set out the options, continue, renegotiate or replace, with the cost and risk of each.",
   "We draft the replies for you to send, and give your lawyer the construction analysis they need.",
  ],
  "docs": ["Position report", "Record of work in place", "Options appraisal"],
  "links": [("/insights/stalled-villa-project-dubai/", "What to do when a villa build stalls"), ("/services/stalled-project-rescue/", "Stalled project recovery"),
            ("/services/variations-delays-and-claims/", "Variations, delays and claims"), ("/tools/renovate-or-rebuild/", "Renovate or rebuild")],
 },
    ]

STAGES = _stages()
N_STAGES = len(STAGES)
N_DECISIONS = sum(len(s["decide"]) for s in STAGES)

BASIS = {"ours": "our planning allowance", "optimal": "Optimal Engineering", "kay-ret": "Kayrouz &amp; Associates"}

# Every "You receive" name must be a document the site already lists (DELIVERABLES in services.py).
def _check_docs():
    from content.services import DELIVERABLES
    names = {n for v in DELIVERABLES.values() for n, _ in v}
    # combined rows on the site, e.g. "Snag list and close-out document list", count for each of their parts
    low = " | ".join(sorted(names)).lower()
    for s in STAGES:
        for d in s["docs"]:
            if d not in names and d.lower() not in low:
                raise SystemExit(f"plot_to_keys: '{d}' is not a document in DELIVERABLES (services.py)")
_check_docs()

# ---------------------------------------------------------------- opening, closing, FAQs, key points
TITLE = "Plot to keys in Dubai: every decision a villa owner makes"
H1 = "From plot to keys: every decision a villa owner makes in Dubai"
DESCRIPTION = (f"The {N_STAGES} stages and {N_DECISIONS} decisions between buying a villa plot in Dubai or Abu Dhabi and "
               "getting the keys: who is responsible for what, and what we do.")

SCENE = ("You have bought a plot, or you are about to. You have a plan with a plot number on it, a folder from the developer and a "
         "figure in your head for what the house should cost. Someone has told you to find an architect. Someone else knows a "
         f"contractor. Nobody has told you that between today and the day you are handed the keys you will make {N_DECISIONS} "
         "decisions, most of them once, many of them before a single block is laid, and almost all of them about something "
         "you have never had to decide before.")

IN_SHORT = (f"Building a villa in Dubai or Abu Dhabi takes an owner through {N_STAGES} stages and the {N_DECISIONS} decisions listed "
            "below, from checking the plot to the end of the defects period. Your registered consultant designs and deals with the "
            "authority; your contractor builds. Every decision about money, time and what you accept is yours. Eastbridge sits "
            "beside you for each one.")

HOW_TO_READ = ("Every stage below is set out the same way: what you have to decide, what it costs you if it goes wrong, who is "
               "responsible, and what Eastbridge does. Rules differ between communities and between authorities, so where a rule "
               "varies, or we could not confirm it from a primary source, we say so.")

KEYPOINTS = [
 f"An owner building a villa in Dubai or Abu Dhabi goes through {N_STAGES} stages and makes the {N_DECISIONS} decisions listed in this guide, from checking the plot to releasing the last of the retention.",
 "Statutory design, authority submissions and statutory site inspections stay with your registered consultant; building, site safety and the works insurance stay with your contractor; every decision on money, time and acceptance stays with you.",
 "The decisions that fix most of the cost come before construction: what the plot allows, the brief, the budget, the design freeze and the contract.",
 "Rules vary by plot: the permit authority is Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where your plot sits, and each master developer has its own guidelines, deadlines and deposits.",
 "Eastbridge works beside the owner at every stage, and never instructs the contractor or approves a payment without the owner's written approval.",
]

def faqs():
    fee = (f"We publish three ranges by level of input. A review, such as a plot review before you buy, is {fee_text('review')}. "
           f"Part service is {fee_text('part')}. Full service, from brief to handover, is {fee_text('full')}. "
           "Each fee is agreed in a written scope of works after a free 30-minute call. See <a href=\"/fees/\">how fees work</a>."
           if PUBLISH_FEES else
           "Every one-off villa is different, so we agree a written scope of works after a free 30-minute call and quote the fee "
           "in writing before any work starts. See <a href=\"/fees/\">how fees work</a>.")
    return [
     ("How many decisions does an owner make when building a villa in Dubai?",
      f"This guide lists {N_DECISIONS} across {N_STAGES} stages, from checking the plot before purchase to the end of the defects period. "
      "Some are made once, such as basement or no basement. Others repeat: every monthly payment and every variation is a decision of its own, "
      "so the real number on a two-year build is higher."),
     ("How long does it take from buying a plot to getting the keys?",
      "Engel &amp; Völkers says most villas take 12 to 24 months from approval to completion. Design, approvals and choosing a contractor come before that. "
      "For a one-off villa, plan on two years or more from plot to keys; "
      "see <a href=\"/insights/how-long-to-build-a-villa-dubai/\">how long it takes to build a villa in Dubai</a>."),
     ("Which decisions can I not hand to anyone else?",
      "The brief, the budget, who you appoint, what you sign, each payment, each change and whether you accept the finished house. "
      "We bring each one to you with the facts and a recommendation; the decision stays yours."),
     ("What stays with the registered consultant and the contractor?",
      "Statutory design, authority submissions and statutory site inspections stay with your registered consultant. Building the villa, "
      "site safety, the works insurance and the quality of the work stay with your contractor. Eastbridge does not replace either: "
      "we work alongside them and represent you."),
     ("Do the rules differ between Dubai and Abu Dhabi, and between communities?",
      "Yes. In Dubai the building permit comes from Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where your plot sits. "
      "In Abu Dhabi it comes from the municipality through TAMM. Each master developer adds its own design guidelines, approval, deadlines and deposits, "
      "so read the documents for your own plot. Our <a href=\"/insights/which-dubai-authority-covers-my-villa/\">guide to the authorities</a> explains why."),
     ("I live abroad. How many of these decisions need me in Dubai?",
      "Few. Some choices of stone, joinery and fittings are better made in person, and the final walk-through is worth attending. "
      "The rest can come to you with photographs, options and a recommendation, recorded in a decision log so that nothing is agreed "
      "without your sign-off. See <a href=\"/services/overseas-owners/\">building in Dubai while living abroad</a>."),
     ("Can I use Eastbridge for one stage only, and what does it cost?",
      "Yes. A review answers one question, such as a plot before you buy or a contractor's quote before you sign, with a written report. " + fee),
    ]

# The home page tiles: (stage ids covered, title, "You decide", "We").
HOME_TILES = [
 ("before-you-buy", "Before you buy the plot", "whether this plot can take the house you want, and what the whole project will cost.",
  "read the developer's rules and the sale terms, and price the whole project before you commit."),
 ("brief-and-budget", "Brief and budget", "the rooms, the size, the quality and the total you are prepared to spend.",
  "turn that into a brief, a budget and a programme your consultant can design to."),
 ("consultant", "Architect and design", "who designs it, on what terms, and when the design is frozen.",
  "compare fee proposals like-for-like and check the design against the budget at every stage."),
 ("approvals", "Approvals", "when to sign, when to pay and whether a late change is worth a resubmission.",
  "track what your consultant has sent, what is waiting and on whom."),
 ("tender", "Contractor and contract", "who builds it, at what price and on what terms.",
  "put every bid into one like-for-like table and read the contract before you sign."),
 ("construction", "Construction", "every payment, every change and every sample.",
  "check each one against the work on site and the contract, and recommend before you approve."),
 ("fit-out", "Fit-out and sourcing", "kitchens, joinery, stone, lighting, pool and garden.",
  "plan the lead times, travel with you to choose, and check what arrives."),
 ("handover", "Completion and handover", "when the house is finished enough to accept.",
  "witness the testing, track every snag to close-out and check the documents before retention is released."),
]

# Mid-article call to action (question, text, WhatsApp topic), placed after the contract stage by render().
MID_CTA = ("Looking at a plot, or just bought one?", "Send us the plot number and the community on WhatsApp.", "a plot review")

LINK_TITLE = "From plot to keys: every decision, stage by stage"
LINK_TEXT = (f"New to building? Our guide sets out the {N_STAGES} stages and {N_DECISIONS} decisions between buying a plot and getting "
             "the keys: what you decide, who is responsible, and what we do at each one.")
LINK_LABEL = "See every decision, stage by stage"

LLMS_SUMMARY = (f"the {N_STAGES} stages and {N_DECISIONS} owner decisions between buying a villa plot in Dubai or Abu Dhabi and the end of the "
                "defects period. Each stage states what the owner has to decide, what it costs if it goes wrong (with sources), who is "
                "responsible (the registered consultant keeps statutory design, authority submissions and statutory site inspections; the "
                "contractor builds), and what Eastbridge does and which documents the owner receives. Covers plot checks, purchase and Dubai "
                "Land Department fees, brief and budget, choosing the consultant, design, approvals, tender, the contract, mobilisation, "
                "construction, fit-out, utilities, completion, snagging, the defects period and stalled projects")

# ---------------------------------------------------------------- rendering
def link_block(cls=""):
    """The guide link shown on the services pages (and reused by the home page section)."""
    return (f'<aside class="ptk-link{(" " + cls) if cls else ""}" aria-label="Guide"><div><p class="ptk-link__t">{LINK_TITLE}</p>'
            f'<p class="ptk-link__d">{LINK_TEXT}</p></div><a class="btn btn--sm" href="{PATH}">{LINK_LABEL}</a></aside>')

def home_section():
    """Compact home page section: one tile per group of stages, each "You decide" and "We"."""
    tiles = "".join(
        f'<li><a href="{PATH}#{sid}"><h3>{t}</h3><p class="ptk-you"><b>You decide</b> {you}</p>'
        f'<p class="ptk-we"><b>We</b> {we}</p></a></li>' for sid, t, you, we in HOME_TILES)
    return (f'<section class="section--tight ptk-home" aria-labelledby="ptk-h"><div class="wrap">'
            f'<div class="head-row"><div><span class="kicker">From plot to keys</span><h2 id="ptk-h">{N_DECISIONS} decisions. One person beside you for all of them.</h2></div>'
            f'<p class="muted">A villa takes its owner through {N_STAGES} stages, from the plot to the end of the defects period. Your consultant designs and your '
            f'contractor builds. The decisions are yours, and we sit beside you for each one. '
            f'<a class="link" href="{PATH}">{LINK_LABEL}</a></p></div>'
            f'<ol class="ptk-tiles">{tiles}</ol></div></section>')

def _when(s):
    d, b = s["when"]
    return d, BASIS[b]

def _fee_section():
    """'What this adds up to': the count, the fee in proportion (the /fees/ worked example, from config.FEES and the
    calculator's example) and the three ways to start."""
    import pages_tools as PT
    ex = PT.EXAMPLE
    build = PT.estimate(ex)["construction"][1]
    def k(v):
        return f"{round(v / 1000) * 1000:,.0f}"
    out = ['<section class="ptk-sum" id="what-this-adds-up-to" aria-labelledby="sum-h"><h2 id="sum-h">What this adds up to</h2>',
           f'<p>{N_STAGES} stages and {N_DECISIONS} decisions, before counting the ones that repeat every month. None is beyond an intelligent owner. '
           'The difficulty is that you meet each one for the first time, across the table from people who have met it a hundred times and '
           'who each have a commercial interest in your answer.</p>',
           '<p>That is the gap we fill. Philip Chapman spent 21 years as the builder on the other side of that table, in the UK, at P Chapman Construction. '
           'He leads every appointment personally, supported by three independent, UAE-based project managers he works with, who attend site and provide cover when he is unavailable. '
           'We work for you alone, and take no commission, referral fee or discount from any contractor, consultant or supplier.</p>']
    if PUBLISH_FEES:
        lo, hi = FEES["full"]["pct"]
        out.append(
           f'<h3>The fee in proportion</h3><p>An illustration, not a quotation. The worked example in our <a href="/tools/villa-build-cost-calculator/">villa cost calculator</a> '
           f'is a {ex["area"]:,} sq ft {ex["tier"]} villa with a likely construction cost of AED {k(build)}. Our full-service fee, at {lo:g} to {hi:g}% of build cost, '
           f'would be about AED {k(build * lo / 100)} to {k(build * hi / 100)} over the whole project. The contingency on the same villa, at 10 to 15%, '
           f'is about AED {k(build * 0.10)} to {k(build * 0.15)}. '
           'We cannot promise a saving. We can make sure every dirham is checked before you pay it. <a href="/fees/">How our fees work</a>.</p>')
    else:
        out.append('<h3>The fee</h3><p>Every one-off villa is different, so the fee is agreed in a written scope of works after the free call. <a href="/fees/">How our fees work</a>.</p>')
    def rng(level):
        return f"{fee_text(level)[0].upper()}{fee_text(level)[1:]}" if PUBLISH_FEES else "Quoted in writing against the agreed scope"
    ways = [
     ("A review of a plot before you buy", rng("review"), "A written report on what the plot allows, what it commits you to and what the whole project is likely to cost.", "/services/plot-due-diligence/", "Plot and pre-purchase review"),
     ("Part service", rng("part"), "Every price, payment and variation checked from your side, with monthly reporting, without regular site attendance.", "/fees/", "How the levels compare"),
     ("Full service", rng("full"), "Every stage in this guide: regular site visits at the frequency agreed in your scope of works, every review, and sourcing trips with you.", "/services/owners-representative/", "Owner's representative"),
    ]
    cards = "".join(f'<li><h4>{t}</h4><p class="ptk-way__fee">{f}</p><p>{d}</p><p><a href="{h}">{l}</a></p></li>' for t, f, d, h, l in ways)
    out.append(f'<h3>Three ways to start</h3><ol class="ptk-ways">{cards}</ol>'
               f'<p>The first step is the same for all three: a free 30-minute call. {RESPONSE_PROMISE}. '
               'References from past UK clients are shared at appointment stage, before you sign.</p>'
               '<p class="ptk-cta"><a class="btn" href="/contact/">Arrange a free 30-minute call</a> '
               '<a class="link" href="/guides/villa-owner-checklist/">Or start with the free pre-construction checklist</a></p></section>')
    return "".join(out)

def render(mid_cta=""):
    """The article body (HTML). mid_cta: the site's mid-article call to action, placed after the contract stage."""
    del _used[:]
    stages = _stages()          # rebuild so citations are recorded in reading order
    rows = "".join(
        f'<li><p class="ptk-ov__t"><a href="#{s["id"]}">{s["title"]}</a></p>'
        f'<p class="ptk-ov__d">{_when(s)[0]}{"" if s["when"][1] != "ours" else "<sup>*</sup>"}</p></li>'
        for i, s in enumerate(stages, 1))
    kp = "".join(f"<li>{k}</li>" for k in KEYPOINTS)
    out = [f'<p class="scene">{SCENE}</p>',
           f'<div class="keypoints answer-first" id="in-short"><h2>In short</h2><p>{IN_SHORT}</p></div>',
           f'<nav class="ptk-ov" id="stages" aria-labelledby="stages-h"><h2 id="stages-h">The {N_STAGES} stages, and how long each usually takes</h2>'
           f'<ol>{rows}</ol>'
           f'<p class="ptk-ov__note small muted"><sup>*</sup> Our own planning allowance. Other durations are from {cite("optimal", "Optimal Engineering")} '
           f'and {cite("kay-ret", "Kayrouz &amp; Associates")}. Stages overlap, and {cite("ev", "Engel &amp; Völkers")} puts most villas at 12 to 24 months from approval to completion.</p></nav>',
           f'<p>{HOW_TO_READ}</p>',
           f'<div class="keypoints"><h2>Key points</h2><ul>{kp}</ul></div>']
    for i, s in enumerate(stages, 1):
        dur, basis = _when(s)
        dec = "".join(f"<li>{d}</li>" for d in s["decide"])
        who = "".join(f"<li><b>{p}</b> {t}</li>" for p, t in s["who"])
        eb = "".join(f"<li>{e}</li>" for e in s["eb"])
        docs = "".join(f"<li>{d}</li>" for d in s["docs"])
        links = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in s["links"])
        checks = (f'<div class="ptk-box ptk-box--checks"><h3>{s["checks"][0]}</h3><p>{s["checks"][1]}</p></div>' if s.get("checks") else "")
        out.append(
            f'<section class="ptk-stage" id="{s["id"]}" aria-labelledby="{s["id"]}-h">'
            f'<header class="ptk-stage__head"><p class="ptk-stage__k">Stage {i} of {N_STAGES}</p><h2 id="{s["id"]}-h">{s["title"]}</h2>'
            f'<p class="ptk-stage__when">Typical duration: {dur} <span class="muted">({basis})</span></p></header>'
            f'<p class="ptk-stage__lede">{s["lede"]}</p>'
            f'<div class="ptk-box ptk-box--decide"><h3>What you have to decide</h3><ol>{dec}</ol></div>{checks}'
            f'<div class="ptk-pair"><div class="ptk-box ptk-box--risk"><h3>What it costs you if it goes wrong</h3><p>{s["cost"]}</p></div>'
            f'<div class="ptk-box ptk-box--who"><h3>Who is responsible</h3><ul>{who}</ul></div></div>'
            f'<div class="ptk-box ptk-box--eb"><h3>What Eastbridge does at this stage</h3><ul>{eb}</ul>'
            f'<p class="ptk-docs__h">You receive</p><ul class="ptk-docs">{docs}</ul></div>'
            f'<div class="ptk-more"><p class="ptk-more__h">Read more</p><ul>{links}</ul>'
            f'<a class="ptk-back" href="#stages">Back to stages</a></div></section>')
        if s["id"] == "contract" and mid_cta:
            out.append(mid_cta)
    out.append(_fee_section())
    return "\n".join(out)

def sources():
    """Sources cited in the text, in reading order, in the front-matter shape the article template expects."""
    render()
    return [{"title": SRC[k][0], "url": SRC[k][1]} for k in _used]

def insight_meta(meta, mid_cta=""):
    """Fill an insight's metadata from this module (called by build.load_insights for `generator: plot_to_keys`)."""
    html = render(mid_cta)
    meta.update({"title": TITLE, "h1": H1, "description": DESCRIPTION, "keypoints": KEYPOINTS,
                 "faqs": [{"q": q, "a": a} for q, a in faqs()], "sources": sources(), "html": html, "pillar": True,
                 "words": len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", html)))})
    return meta

# ---------------------------------------------------------------- Markdown review copy for Phil
def _md(s):
    s = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', lambda m: f"[{m.group(2)}]({m.group(1) if m.group(1).startswith('http') else 'https://eastbridgestrategicpartners.com' + m.group(1)})", s)
    s = re.sub(r"</?(b|strong)>", "**", s)
    s = re.sub(r"<sup>\*</sup>", "\\*", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.replace("&amp;", "&").replace("&ldquo;", '"').replace("&rdquo;", '"')

def markdown_copy():
    stages = _stages()
    L = [f"# {H1}", "",
         "*Review copy for Phil Chapman. Generated from `src/content/plot_to_keys.py`; edit the text there, not here.*", "",
         f"**Page title:** {TITLE}  ", f"**Description:** {DESCRIPTION}  ",
         f"**Live page:** https://eastbridgestrategicpartners.com{PATH}", "",
         _md(SCENE), "", "## In short", "", _md(IN_SHORT), "", _md(HOW_TO_READ), "",
         "## Key points", ""] + [f"- {_md(k)}" for k in KEYPOINTS] + ["",
         f"## The {N_STAGES} stages, and how long each usually takes", "",
         "| # | Stage | Typical duration | Basis | Decisions |", "|---|---|---|---|---|"]
    for i, s in enumerate(stages, 1):
        L.append(f"| {i} | {s['title']} | {s['when'][0]} | {_md(BASIS[s['when'][1]])} | {len(s['decide'])} |")
    L += [f"| | **Total** | | | **{N_DECISIONS}** |", ""]
    for i, s in enumerate(stages, 1):
        L += [f"## Stage {i} of {N_STAGES}: {s['title']}", "", f"*Typical duration: {s['when'][0]} ({_md(BASIS[s['when'][1]])})*", "", _md(s["lede"]), "",
              "### What you have to decide", ""] + [f"{n}. {_md(d)}" for n, d in enumerate(s["decide"], 1)] + [""]
        if s.get("checks"):
            L += [f"### {s['checks'][0]}", "", _md(s["checks"][1]), ""]
        L += ["### What it costs you if it goes wrong", "", _md(s["cost"]), "", "### Who is responsible", ""]
        L += [f"- **{p}** {_md(t)}" for p, t in s["who"]] + ["", "### What Eastbridge does at this stage", ""]
        L += [f"- {_md(e)}" for e in s["eb"]] + ["", "**You receive:** " + "; ".join(s["docs"]) + ".", "",
              "Read more: " + " · ".join(_md(f'<a href="{h}">{l}</a>') for h, l in s["links"]), ""]
    L += [_md(re.sub(r"<h2[^>]*>(.*?)</h2>", r"\n## \1\n\n", re.sub(r"<h3>(.*?)</h3>", r"\n\n### \1\n\n",
          re.sub(r"<h4>(.*?)</h4>", r"\n- **\1** ", re.sub(r"</p>", "\n\n", re.sub(r'<p class="ptk-way__fee">(.*?)</p>', r"(\1) ", _fee_section())))))).strip(), "",
          "## Questions", ""]
    for q, a in faqs():
        L += [f"**{q}**  ", _md(a), ""]
    L += ["## Sources", ""] + [f"{n}. [{s['title']}]({s['url']})" for n, s in enumerate(sources(), 1)] + ["",
          "## The home page section", "", f"**{N_DECISIONS} decisions. One person beside you for all of them.**", ""]
    L += [f"- **{t}.** You decide {you} We {we}" for _, t, you, we in HOME_TILES]
    return "\n".join(L) + "\n"

