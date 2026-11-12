"""Service pages. Wording follows the compliance rules: Eastbridge represents the owner and works alongside the
owner's registered consultant and contractor. It does not supervise as consultant of record, submit permits,
prepare tender documents, prequalify contractors or certify anything."""
from config import fee_text as _fee_text, PUBLISH_FEES as _SHOW, COVERAGE as _COVERAGE

# The full-service, one-off villa story (competitor brief 2.0). P Chapman Construction's record is the evidence.
ONE_OFF_STORY = ("For a truly one-off villa, one person on your side does the work with you. We review every drawing, quote, "
                 "payment and variation, are on site regularly through construction, at the frequency agreed in your scope of works, "
                 "and travel with you to "
                 "source stone, joinery, lighting and fittings.")
UK_RECORD = ("It is how Philip worked with clients on the high-end houses P Chapman Construction built in the UK over "
             "21 years: everything reviewed, a weekly presence on site, and sourcing trips with the owner.")

def _fee(level, text, fallback=""):
    """A published fee sentence when PUBLISH_FEES is on; otherwise the fallback (no figure).
    {fee} becomes the published range for the level, e.g. "AED 9,500–15,000 per review"."""
    return text.format(fee=_fee_text(level)) if _SHOW else fallback

SERVICES = [
 {
  "slug": "owners-representative",
  "short": "Full representation, plot to keys",
  "name": "Owner's representative for villa builds in Dubai and Abu Dhabi",
  "title": "Owner\'s Representative Dubai | Villa Builds | Eastbridge",
  "description": "Independent owner\'s representation for villa builds and renovations in Dubai and Abu Dhabi. We act only for you and take nothing from contractors.",
  "h1": "An independent representative on your side of the project",
  "lede": "Your consultant is responsible for the design and its statutory duties. Your contractor is responsible for building it. We represent you, from the plot to the day you move in.",
  "image": "quay-house-01",
  "stage": "From the first budget to the end of the defects period",
  "intro": f"""<p>A private villa in Dubai brings together a master developer, a permitting authority, a registered consultant, a main contractor, a dozen specialist subcontractors and an interior designer. Each of them has real duties and each has their own commercial position. What is often missing is someone appointed to coordinate the whole project and look at every price, payment and decision from the owner's side.</p>
<p><strong>{ONE_OFF_STORY}</strong> {UK_RECORD} <a href="/services/materials-and-specialist-sourcing/">Materials and specialist sourcing</a>.</p>
<p>That is the role we fill. We sit beside you, set the budget and programme with you, help you appoint the right consultant and contractor, then work alongside them to keep the project to what was agreed until handover. Philip spent 21 years running a building company whose houses have won RIBA and LABC recognition, so we know how a tender is priced, where variations come from and how delay claims are assembled. That knowledge now works for you.</p>
<p>Philip leads every appointment personally, supported by a team of three project managers who attend site and provide cover when he is unavailable. How often we attend site and what we report are agreed in writing in your appointment before work starts, and capacity is confirmed before an appointment is accepted. Where the project needs a quantity surveyor, an engineer or another specialist, you appoint and pay them directly, and we help you compare proposals and choose. Our role is commercial and project management on your side; statutory design, authority submissions and supervision stay with your registered consultant. <a href="/approach/#uae-appointments">How an appointment works in the UAE</a>.</p>
<p>{_COVERAGE}</p>""",
  "alongside": True,
  "insight": ("client-side-project-manager-fees-dubai", "Client-side project manager fees in Dubai"),
  "does": [
   "Set a realistic budget, programme and brief before any design money is spent",
   "Help you choose and appoint a registered consultant and a main contractor, and agree fair terms with each",
   "Run the decision log, so every choice you make is recorded with its cost and time effect",
   "Attend site for you and report progress, quality and risks in plain English",
   "Travel with you to source stone, joinery, lighting and fittings, and check what arrives against what you chose",
   "Review every payment application and variation before you pay it",
   "Deal with disagreements early, on the facts, before they become formal claims",
   "Lead snagging, handover documents and the defects period",
  ],
  "gets": [
   "A single monthly report: forecast final cost, programme, decisions needed, risks",
   "Regular photo updates from site, at the frequency agreed in your scope of works",
   "A clear recommendation before every payment",
   "A record of every decision, so nothing is relitigated later",
  ],
  "builder_view": "On the contractor's side, the jobs that ran best were the ones where the owner had someone experienced checking the valuations. Payments were fair and on time, and the whole job ran tighter. An owner's representative does not slow a good contractor down. It removes the ambiguity that bad projects live on.",
  "faqs": [
   ("What does an owner's representative do on a villa build?", "We act as your single point of control. We set the budget and programme with you, help you appoint the consultant and contractor, track cost and time, review payments and variations, report progress and lead handover. We do not replace the registered consultant, who remains responsible for the statutory design, permit submissions and supervision duties."),
   ("Is an owner's representative worth it on a villa?", "On a straightforward build with an experienced owner who lives in Dubai, perhaps not. On a bespoke villa, a major renovation, or any project where you are often abroad, it gives you regular cost reporting, programme monitoring, review of every payment and variation, and early warning of risks, from someone who works only for you. We will tell you honestly if you don't need us. See <a href=\"/fees/#worth-it\">is it worth it?</a>"),
   ("Who will I deal with, and how often will you be on site?", "Philip Chapman, our founder, leads every appointment personally and is your point of contact throughout. He is supported by a team of three project managers who attend site and provide cover when he is unavailable. Site attendance and reporting are agreed in writing in the scope of your appointment: we are on site regularly through construction, at the frequency agreed in your scope of works, planned around key stages such as waterproofing, first fix and pre-handover."),
   ("Who appoints the quantity surveyor and engineers?", "You do, and you pay them directly. We help you work out which specialists the project needs, compare their proposals like-for-like and choose. We take no commission or referral fee from any of them."),
   ("Do you take commission from contractors or suppliers?", "No. We take no commission, referral fee or discount from any consultant, contractor or supplier. Our only income on your project is the fee you pay us. That is written into our appointment."),
   ("Do you replace the architect or the consultant?", "No. Your registered consultant designs, submits for permits and carries the statutory responsibilities. We represent you alongside them and check the design against your budget and brief at each stage."),
  ],
  "related": ["villa-construction-project-management", "cost-and-programme-control", "variations-delays-and-claims"],
 },
 {
  "slug": "villa-construction-project-management",
  "short": "New villa builds",
  "name": "Villa construction project management (client-side)",
  "title": "Villa Construction Project Management Dubai | Eastbridge",
  "description": "Building a villa in Dubai or Abu Dhabi? We manage it from your side: budget, programme, appointments, cost control, site reports and handover.",
  "h1": "Building a new villa, managed from your side of the table",
  "lede": "A bespoke villa is a two-year project and, for most owners, a once-in-a-lifetime one. We keep cost, programme and quality under control from your side, so problems surface early and decisions stay with you.",
  "image": "sea-glass-house-01",
  "stage": "Plot to keys",
  "intro": """<p>Most villa builds that go wrong do so in the first three months, long before anything is built. The brief is loose, the budget is a guess, the design runs ahead of the money and the contract is signed before anyone has priced the risk. By the time the slab is poured, the outcome is mostly decided.</p>
<p>We start before design. We test the brief against the plot's design guidelines and a realistic cost per square foot, then hold the project to it through design, approvals, appointment, construction and handover. Your consultant designs and carries the statutory responsibilities; your contractor builds; we work alongside both, checking cost, programme and quality against what you are paying for.</p>""",
  "does": [
   "Brief, budget and programme set before design starts",
   "Design reviews against cost at each stage, so the drawings stay aligned with the budget",
   "Coordination with the master developer and authority route through your consultant",
   "Help comparing contractor bids like-for-like and agreeing the contract",
   "Cost and programme control throughout construction",
   "Regular client-side site visits with a written report",
   "Payment and variation review before anything is paid",
   "Snagging, handover documents and defects follow-up",
  ],
  "gets": [
   "A budget built from the brief and the plot, with contingency held by you, not the contractor",
   "A programme with the decisions you need to make, and when",
   "Monthly cost and programme reports, with the forecast final cost",
   "A clean handover file: completion certificate, as-built drawings, warranties and manuals",
  ],
  "builder_view": "When we priced a one-off house as a contractor, the first thing we looked for was what the drawings didn't say. Every gap became a provisional sum, and every provisional sum became a conversation later. The best protection an owner has is a complete design and a contract that leaves little to interpretation. We help you get both before you sign.",
  "faqs": [
   ("How long does it take to build a villa in Dubai?", "Market guides put plot to keys at roughly 12 to 24 months, and 24 to 36 months for a custom luxury villa, split across design, approvals, construction and snagging. The biggest variable is how quickly the design is fixed. See our <a href=\"/insights/how-to-build-a-villa-in-dubai/\">step-by-step guide</a>."),
   ("What does it cost to build a luxury villa in Dubai?", "Published 2025–26 guides put luxury construction at roughly AED 850 to 1,400 per sq ft, before land, design fees, authority fees, furniture and landscaping. Our <a href=\"/insights/villa-construction-cost-dubai/\">cost guide</a> breaks this down."),
   ("When should we appoint you?", "Ideally before you appoint the architect, or before you buy the plot. The earlier we are involved, the more influence there is over cost, because most of it is set by the brief, the design and the contract."),
  ],
  "related": ["plot-due-diligence", "design-and-approvals", "consultant-and-contractor-selection"],
 },
 {
  "slug": "villa-renovation-project-management",
  "short": "Renovations and extensions",
  "name": "Villa renovation and extension project management",
  "title": "Villa Renovation Project Manager, Dubai & Abu Dhabi",
  "description": "Villa renovation project management in Dubai and Abu Dhabi from the owner's side: condition review, NOC route, budget, contractor choice, site visits and handover.",
  "h1": "Renovations and extensions, with the unknowns planned for",
  "lede": "Renovation is where budgets are most at risk: waterproofing and services of unknown condition, and approvals that take longer than promised. We investigate all three before the first wall comes down.",
  "image": "trelowen-01",
  "stage": "Survey to handover",
  "intro": """<p>A large share of Dubai's best villas are not new. They are fifteen or twenty-year-old houses on outstanding plots, waiting for a new layout, a new façade, a pool, an extension or a complete strip-out. Renovation can create a great deal of value. It also carries more unknowns than a new build, because nobody knows what is behind the walls until they come down.</p>
<p>We start with what can be known: a condition survey arranged through the right specialists, the master developer's renovation rules and NOC requirements, and a realistic budget with a contingency set for the age of the house. Then we help you choose a contractor who is good at this kind of work, which is a different skill from building new.</p>
<p>Planning a renovation? Our <a href="/insights/how-to-plan-a-villa-renovation-dubai/">step-by-step plan for a villa renovation in Dubai</a> links every renovation guide and tool we publish, from renovate or rebuild to snagging.</p>""",
  "does": [
   "Condition review of the existing villa before design, arranged with the right specialists",
   "Master developer NOC and authority route coordinated with your consultant or contractor",
   "Renovate-or-rebuild comparison when the numbers are close",
   "Scope and budget set with a contingency matched to the house",
   "Help selecting a renovation contractor and agreeing the contract",
   "Site visits, reporting and payment review through the works",
   "Neighbour and community management during noisy phases",
   "Snagging and handover",
  ],
  "gets": [
   "An honest renovate-or-rebuild view, with numbers",
   "A scope that separates what must be done from what you'd like done",
   "A contingency that reflects the age and condition of the house",
   "Reports you can read from anywhere in the world",
  ],
  "builder_view": "In 21 years of altering and extending houses, the expensive surprises were almost always the same three: water where it shouldn't be, services that couldn't be reused, and structure that wasn't what the old drawings showed. Opening up a few areas before the price is agreed costs little and can remove a large part of that risk.",
  "faqs": [
   ("Do I need approval to renovate a villa on Palm Jumeirah?", "Most work beyond like-for-like interior finishes needs a Nakheel NOC first, then a permit from the relevant authority depending on your plot. Extensions, façade changes, pools and structural alterations always do. See our <a href=\"/insights/palm-jumeirah-villa-renovation/\">Palm Jumeirah renovation guide</a> and our explainer on the <a href=\"/insights/nakheel-noc-villa-renovation/\">Nakheel NOC</a>."),
   ("How much does a villa renovation cost in Dubai?", "Published guides disagree. <a href=\"https://www.propertyfinder.ae/blog/villa-renovation-dubai/\" rel=\"noopener\">Property Finder</a> (September 2025) runs from about AED 250,000–400,000 for a three-bedroom townhouse refresh to AED 1.5–3.5 million or more for structural work on a luxury villa, while <a href=\"https://smartrenovation.ae/villa-renovation-in-dubai-complete-2026-guide-to-costs-timeline-permits/\" rel=\"nofollow noopener\">a Dubai renovation contractor's 2026 guide</a> (the publisher gives no sources) puts mid-range work at AED 400,000–800,000 and luxury from AED 1 million. Full strip-outs of large villas on prime plots go well beyond that. Our <a href=\"/insights/villa-renovation-cost-dubai/\">villa renovation cost guide</a> sets out a worked budget and the hidden costs in older villas."),
   ("Should I renovate or knock down and rebuild?", "It depends on the structure, the plot's current guidelines and how much of the existing house survives your brief. When more than about half the house is changing, the comparison is worth doing properly. We do it with real numbers."),
  ],
  "related": ["owners-representative", "stalled-project-rescue", "snagging-and-handover"],
 },
 {
  "slug": "plot-due-diligence",
  "short": "Plot and pre-purchase review",
  "name": "Villa plot and pre-purchase review",
  "title": "Villa Plot Due Diligence, Dubai & Abu Dhabi | Eastbridge",
  "description": "Buying a villa plot in Dubai or Abu Dhabi? A written review of design rules, build-by deadlines and realistic build cost before you commit.",
  "h1": "Know what you can build, and what it will cost, before you buy the plot",
  "lede": "The plot price is the number everyone talks about. The build cost, the design rules and the build-by deadline decide whether it is a good purchase.",
  "image": "saqqara-01",
  "stage": "Before you commit",
  "intro": """<p>New villa plot releases in Dubai and Abu Dhabi now sell quickly, often on brochures and plot maps. Buyers compare plot prices per square foot and rarely the things that decide the total outcome: what the master developer's guidelines actually allow, how long you have to build, what the ground and access are like, and what the house you want will really cost to deliver.</p>
<p>Our plot review answers those questions in a short written report before you commit. We look at the plot as a builder would on day one of a project, then tell you plainly whether the numbers work.</p>""",
  "does": [
   "Review of the master developer's design guidelines: coverage, heights, setbacks, materials",
   "Build-by deadlines and any penalties in the sale terms",
   "Access, levels, neighbouring plots and practical buildability",
   "A realistic build budget range for the house you want",
   "Total cost of ownership: plot, design, approvals, build, furniture, landscaping",
   "A short list of questions to put to the seller or developer",
  ],
  "gets": [
   "A written report you can read in fifteen minutes",
   "A total project budget range, not just a plot price",
   "A clear view of the risks, and which ones matter",
  ],
  "builder_view": "As a contractor, the first site visit told us most of what the project would cost: access for deliveries, space to store materials, the slope, what was next door. Those things rarely appear in a sales brochure and they all appear in the final account.",
  "faqs": [
   ("What should I check before buying a villa plot in Dubai?", "Title and plot details, the master developer's design guidelines, any build-by deadline, service charges, access and ground conditions, and a realistic total build budget. Our <a href=\"/insights/buying-a-villa-plot-in-dubai-checks/\">plot checklist</a> covers each one."),
   ("Is this legal or valuation advice?", "No. We give a practical, construction-led view. For title and contract terms, take advice from a UAE-qualified lawyer. For value, use a RICS or RERA-registered valuer. We are happy to work alongside both."),
   ("How quickly can you turn a review around?", "Within five working days of receiving the plot documents, sooner when a release window demands it."),
   ("What does a plot review cost?", _fee("review", "It is priced within our Review range, {fee}, depending on the number of plots, the documents available and your timetable. The scope and fee are confirmed in writing after the free call, before we start. See <a href=\"/fees/\">how fees work</a>.", "It is quoted in writing after the free call, before we start. See <a href=\"/fees/\">how fees work</a>.")),
  ],
  "related": ["villa-construction-project-management", "development-advisory", "cost-and-programme-control"],
 },
 {
  "slug": "design-and-approvals",
  "short": "Design and approvals management",
  "name": "Design brief, budget and approvals management",
  "title": "Villa Design & Approvals Management Dubai | Eastbridge",
  "description": "We write the brief, check the design against your budget at every stage, and track master developer and authority approvals with your consultant.",
  "h1": "A design that matches the brief and the budget",
  "lede": "Design is the cheapest place to change your mind and the most expensive place to lose control of cost. We keep both under watch.",
  "image": "owers-house-01",
  "stage": "Brief, concept, detailed design, approvals",
  "intro": """<p>Good architects design beautiful houses. They are not always asked to design them to a number. In August 2025 Dubai Municipality formally warned villa consultancies about over-designing structures and inflating build costs. Owners felt the effect long before that warning, in tenders that came back far above budget.</p>
<p>We write the brief with you, agree the budget with your consultant, and review the design against cost at each stage. We also coordinate the approvals route with your consultant, who prepares and submits the drawings: master developer review first, then the authority permit through Dubai Municipality, Trakhees or the Dubai Development Authority depending on where your plot sits.</p>""",
  "does": [
   "A written brief: rooms, sizes, finishes, priorities and what you won't compromise on",
   "Budget and design reviewed together at concept, detailed design and before pricing",
   "Value review of structural and services design where cost looks high",
   "Interior design and fit-out integrated early, so services and joinery fit first time",
   "Approvals programme tracked with your consultant, with risks flagged early",
  ],
  "gets": [
   "A brief your consultant can design to",
   "A cost check at every design stage",
   "An approvals tracker showing what's submitted, what's waiting and on whom",
  ],
  "builder_view": "The most costly changes we ever dealt with were interior decisions made after first fix: a moved kitchen, a new lighting scheme, a different bath. Bringing the interior designer in at the same time as the architect is the single cheapest decision an owner can make.",
  "faqs": [
   ("Do you design villas?", "No. Design and the statutory submissions are the role of your registered consultant. We write the brief, review the design against your budget and represent you through the process."),
   ("Who submits the building permit application?", "Your appointed consultant, through the relevant authority's system. We track the process with them and keep you informed. Our <a href=\"/insights/dubai-municipality-villa-building-permit/\">villa building permit guide</a> explains each step."),
   ("Can you help choose an architect?", "Yes. We help you shortlist, compare fee proposals like-for-like and agree a clear appointment. You make the appointment directly."),
  ],
  "related": ["consultant-and-contractor-selection", "cost-and-programme-control", "villa-construction-project-management"],
 },
 {
  "slug": "consultant-and-contractor-selection",
  "short": "Choosing the team",
  "name": "Help choosing your consultant and contractor",
  "title": "Choosing a Villa Contractor in Dubai | Eastbridge",
  "description": "Independent help choosing a villa consultant and contractor in Dubai: like-for-like bid comparison, reference checks and fair contract terms.",
  "h1": "The right team, chosen on the right evidence",
  "lede": "The lowest price is rarely the lowest cost. We help you see the difference before you sign.",
  "image": "gooden-heane-01",
  "stage": "Before appointment",
  "intro": """<p>Contractor bids for a villa rarely compare directly. One excludes the pool, one carries a large provisional sum for MEP, one assumes a programme nobody could achieve, and one has priced the drawings exactly as drawn, knowing the gaps will become variations. On paper the cheapest bid wins. In the final account it often doesn't.</p>
<p>Philip wrote and priced these bids himself for 21 years. We help you and your consultant put bids on an equal footing, test the assumptions, call the references that matter and agree a contract that is fair to both sides. You appoint directly; we advise.</p>""",
  "does": [
   "Shortlisting consultants and contractors suited to your type of villa",
   "Checking licences and registrations through the official registries",
   "Like-for-like comparison of bids: exclusions, provisional sums, preliminaries, programme",
   "Reference calls with past clients, not just showcase projects",
   "Advice on contract terms: payment, retention, bonds, delay and variations",
  ],
  "gets": [
   "A side-by-side bid comparison you can understand",
   "A recommendation with reasons",
   "Contract terms that protect you without scaring good contractors away",
  ],
  # Contractor quote review (competitor brief 2.1; paid, within the Review range per decision D2).
  "extra": """<h2 id="quote-review">Contractor quote review</h2>
<p>Already holding a contractor's quote? Send it to us with the draft contract before you sign. Philip spent 21 years pricing quotes like these as the builder, at P Chapman Construction, so we read one the way the contractor wrote it: where the price leaves room, what it leaves out, and which lines are likely to come back as variations.</p>
<h3>What we look at</h3>
<ul><li>Scope gaps: what the drawings and specification show that the quote does not price</li>
<li>Provisional sums and allowances: how much of the price is still an estimate</li>
<li>The payment schedule, and whether payments run ahead of the work</li>
<li>The variation clause: how changes are priced, agreed and instructed</li>
<li>Exclusions and the assumptions behind the price</li></ul>
<h3>You receive</h3>
<ul><li>A written report, with the questions to put to the contractor before you sign</li></ul>
<p>""" + _fee("review", "Priced within our Review range, {fee}, and agreed in writing before we start. ", "Quoted in writing before we start. ") + """The report is a commercial review, not legal advice: for the contract's legal effect, take advice from a UAE-qualified lawyer. <a href="/fees/#quote-review">How the review is charged</a>.</p>""",
  "builder_view": "When we tendered, we could tell within ten minutes whether a client's team would run the job well: clear drawings, a fair contract, sensible payment terms. Good contractors choose their clients too. A well-prepared owner gets better prices from better builders.",
  "faqs": [
   ("Can you review a contractor's quote before I sign?", "Yes. Send us the quote and the draft contract, and we review the scope gaps, provisional sums, payment schedule, variation clause and exclusions, with a written report and the questions to put to the contractor. " + _fee("review", "It is priced within our Review range, {fee}. ", "It is quoted in writing before we start. ") + "See <a href=\"/fees/#quote-review\">how the review is charged</a>."),
   ("How do I check a contractor's licence in Dubai?", "Ask for the trade licence and authority registration, then verify them through the official channels. Dubai's building permits app includes a consultant and contractor registry. Our <a href=\"/insights/how-to-choose-a-villa-contractor-dubai/\">contractor guide</a> lists the twelve questions to ask."),
   ("Do you get paid by the contractor you recommend?", "Never. We take no commission or referral fee from anyone. See our <a href=\"/independence/\">independence pledge</a>."),
   ("Can you work with a contractor I already know?", "Yes. We will still check the price and contract terms, so you can proceed with confidence."),
  ],
  "related": ["design-and-approvals", "variations-delays-and-claims", "owners-representative"],
 },
 {
  "slug": "cost-and-programme-control",
  "short": "Cost and programme control",
  "name": "Villa construction cost and programme control",
  "title": "Villa Construction Cost Control Dubai | Eastbridge",
  "description": "Client-side cost and programme control for villa builds in Dubai: monthly forecast final cost, payment review and variation control.",
  "h1": "Know the final cost before it arrives",
  "lede": "Every month you should know three numbers: what you have paid, what it will cost to finish, and what the house will cost in total. Most owners only know the first.",
  "image": "polgreen-manor-01",
  "stage": "Design through final account",
  "intro": """<p>Construction budgets rarely fail in one dramatic moment. They drift: a variation here, a provisional sum that came in high, a delay that becomes a claim. By the time the drift is visible without proper reporting, much of it is hard to recover.</p>
<p>We keep a live cost plan from the first budget to the final account, and a programme that shows the real critical path rather than the optimistic one. Every payment application and every variation is reviewed before you pay it, with a clear recommendation.</p>""",
  "does": [
   "Cost plan at each design stage, then a monthly forecast cost to complete and forecast final cost during construction",
   "Review of every payment application against work actually done",
   "Variation control: is it a genuine change, is the price fair, what does it do to time?",
   "Programme review and monitoring of the critical path",
   "Contingency held and released by you, with a clear audit trail",
   "Final account agreed line by line",
  ],
  "gets": [
   "A monthly one-page cost and programme summary",
   "A payment recommendation before every payment",
   "A final account agreed line by line, with the records behind it",
  ],
  "builder_view": "Contractors live on cash flow. Front-loaded valuations, over-measured work and early release of retention are normal pressures, not dishonesty. An owner who reviews every valuation properly is not being difficult. They are keeping the job balanced, which is better for everyone.",
  "faqs": [
   ("What is the difference between cost to complete and forecast final cost?", "Forecast cost to complete is what is still to be spent: committed cost not yet paid, the forecast cost of work not yet committed, and an allowance for the remaining risks. It leaves out what you have already paid. Forecast final cost is what you have paid to date plus the forecast cost to complete. Set against your approved budget, the forecast final cost tells you whether you are on budget. See the <a href=\"/glossary/#forecast-final-cost\">glossary</a> for each term."),
   ("How much contingency should a villa build carry?", "Published guidance suggests 10 to 15 percent for new builds. Renovations of older villas often need more. The key point is that you hold it, not the contractor."),
   ("Do you replace a quantity surveyor?", "On most private villas we provide the cost control an owner needs. On larger projects we can work alongside an appointed quantity surveyor."),
  ],
  "related": ["variations-delays-and-claims", "site-visits-and-reporting", "owners-representative"],
 },
 {
  "slug": "site-visits-and-reporting",
  "short": "Site visits and reporting",
  "name": "Independent client-side site visits and progress reporting",
  "title": "Villa Construction Progress Reporting Dubai | Eastbridge",
  "description": "Independent, client-side site visits and progress reports for villa builds in Dubai and Abu Dhabi, with photos, written for owners.",
  "h1": "Eyes on site that answer only to you",
  "lede": "Your consultant has statutory duties on site. Your contractor reports on its own work. We report to you, independently and in plain English.",
  "image": "the-lookout-01",
  "stage": "Construction",
  "intro": """<p>On a Dubai villa, the registered consultant carries the statutory supervision role, and the contractor manages the works. Both report properly within their roles, but neither is appointed to report only to you. For an owner who is busy, often abroad, or simply not a builder, it is hard to know whether the project is really where the reports say it is.</p>
<p>We visit site for you, regularly and sometimes unannounced, and report what we see: progress against programme, quality of workmanship, safety and housekeeping, and anything that will cost money or time later. We raise issues with the consultant and contractor through the proper channels and track them until they are closed.</p>""",
  "does": [
   "Scheduled and unannounced site visits, reporting to you",
   "Progress checked against the programme, not against the contractor's report",
   "Workmanship and finish observations, with photographs",
   "Issues raised through your consultant and tracked to close-out",
   "Attendance at progress meetings as your representative",
  ],
  "gets": [
   "Regular photo updates, at the frequency agreed in your scope of works",
   "A monthly written report with the decisions you need to make",
   "An issues log with owners and dates",
  ],
  "builder_view": "Every site manager knows the difference between a visit and an inspection. A visit is a walk round and a coffee. An inspection opens the ceiling void before it's boarded. We know which areas get closed up quickly, and we make sure we see them first.",
  "faqs": [
   ("Is this the same as construction supervision?", "No. Statutory supervision on a Dubai villa is carried out by the registered consultant. Our visits are independent, client-side monitoring and reporting, which sits alongside that role and reports only to you."),
   ("How often do you visit?", "It depends on the stage and your appointment. We are on site regularly through construction, at the frequency agreed in your scope of works, planned around key stages such as waterproofing, first fix and pre-handover."),
   ("Can I see the reports on my phone?", "Yes. Reports are short, photo-led and readable on a phone, with a fuller version for your records."),
  ],
  "related": ["overseas-owners", "cost-and-programme-control", "snagging-and-handover"],
 },
 {
  "slug": "materials-and-specialist-sourcing",
  "short": "Materials and specialist sourcing",
  "name": "Materials and specialist sourcing with the owner",
  "title": "Villa Materials and Specialist Sourcing Dubai | Eastbridge",
  "description": "Sourcing stone, joinery, lighting and fittings for a one-off villa in Dubai or Abu Dhabi: trips with you, samples, lead times, shipping and checks on arrival.",
  "h1": "Choosing the materials that make a one-off villa, with someone on your side",
  "lede": "Stone, joinery, lighting and fittings decide how a one-off villa looks and feels. We travel with you to choose them, then make sure what arrives on site is what you chose, on time for the programme.",
  "image": "morvoren-01",
  "stage": "Design, procurement and construction",
  "insight": ("sourcing-materials-abroad-dubai-villa", "Sourcing materials abroad for a Dubai villa"),
  "intro": f"""<p>On a truly one-off villa, the materials are where the owner's taste shows: a particular stone, a joinery workshop, a lighting designer's fittings, taps and ironmongery chosen piece by piece. They are also where programmes slip and budgets leak. Samples are approved without a reference, lead times are guessed, shipping and customs are left to the last month, and the delivery that arrives is not quite what was chosen.</p>
<p>{ONE_OFF_STORY} {UK_RECORD}</p>
<p>We plan sourcing around your programme and budget, travel with you to quarries, workshops and showrooms when a choice needs to be made in person, and keep a record of every sample and decision. When the goods arrive, we check them against what you chose before they are fixed. We take no commission, referral fee or discount from any supplier, so the recommendation you receive is about the material, not the margin.</p>
<p>You buy from the supplier directly or through your contractor, as your contract sets out; money never passes through us. Who orders, receives, stores, insures and fits each owner-supplied item is agreed with your contractor in writing before anything is ordered. Sourcing trips are agreed in your scope of works before they are booked.</p>""",
  "does": [
   "Sourcing trips with you to quarries, workshops, showrooms and makers, when a choice needs to be made in person",
   "Samples and reference panels logged, labelled and kept, so every later delivery is checked against what you approved",
   "Lead times confirmed with each supplier and set against the construction programme, with order-by dates",
   "Shipping and UAE customs clearance timing planned with the supplier, the freight forwarder and your contractor",
   "Owner-supplied items agreed with your contractor: who orders, receives, stores, insures and fits each one",
   "Deliveries checked on arrival against the approved sample, specification and quantity, before anything is fixed",
   "No supplier commissions, referral fees or discounts: the only fee on your project is the one you pay us",
  ],
  "gets": [
   "A sourcing schedule: each item, its supplier, lead time, order-by date and delivery window",
   "A sample record with photographs and the decision you made on each",
   "A note after each sourcing trip with what was chosen, prices quoted and the next steps",
   "A delivery check note for every consignment, with any shortfall or damage raised at once",
  ],
  "builder_view": "As the builder, the late items on a high-end house were rarely the structure. They were the stone that had to come from one quarry, the joinery made abroad and the light fittings on a long lead time. The owners who travelled with us to choose them, and who signed off a reference sample we kept on site, got what they wanted, when the programme needed it.",
  "faqs": [
   ("Will you travel with me to choose stone, joinery and fittings?", "Yes, where a choice needs to be made in person. Sourcing trips are planned around your programme and agreed in your scope of works before they are booked. Where a decision can be made from samples, we arrange the samples instead."),
   ("Do you take commission from suppliers?", "No. We take no commission, referral fee or discount from any supplier, consultant or contractor. Our only income on your project is the fee you pay us."),
   ("Who pays the supplier and who imports the goods?", "You buy from the supplier directly or through your contractor, as your contract sets out, and money never passes through us. Shipping and customs clearance are handled by the supplier, a freight forwarder or your contractor; we plan the timing with them so the goods arrive when the programme needs them."),
   ("How do you check what arrives?", "Against the approved sample, the specification and the order: material, finish, size, quantity and condition. Anything that does not match is recorded and raised with the supplier or contractor before it is fixed."),
   ("Do you keep a list of approved suppliers?", "No. We help you find and compare suppliers for the material you want, and you choose. We have no approved-supplier list and no supplier arrangements."),
  ],
  "related": ["owners-representative", "cost-and-programme-control", "overseas-owners"],
 },
 {
  "slug": "variations-delays-and-claims",
  "short": "Variations, delays and claims",
  "name": "Variations, delays and construction claims advice",
  "title": "Villa Construction Claims and EOT Advice | Eastbridge",
  "description": "Client-side advice on variations, extension of time claims and delay on villa projects in Dubai, led by a builder who prepared and defended claims for 21 years.",
  "h1": "Variations and delay claims, handled by people who used to write them",
  "lede": "Philip spent two decades preparing and defending extension of time and variation claims under JCT contracts and through adjudication. We know how they are built, and where they are weak.",
  "image": "three-mile-beach-01",
  "stage": "Whenever the contract is tested",
  "intro": """<p>Variations and delay are where villa budgets are most often lost, and where owners are least equipped. A contractor's extension of time claim can look persuasive: a programme, a list of events, a delay analysis and a demand for time and money. Whether it is right depends on the contract, the records and the critical path, not on how persuasive it looks.</p>
<p>We review variation requests and delay claims for you, test them against the contract and the records, and help you reach a fair answer quickly. In our experience, disagreements are cheaper to resolve in the first month than the sixth. Where legal advice is needed, we work alongside your UAE-qualified lawyer and give them the construction analysis they need.</p>""",
  "does": [
   "Review of variation requests: entitlement, price and time effect",
   "Extension of time claims tested against the programme and records",
   "Delay and disruption analysis in plain English",
   "Record-keeping set up from day one, so your position is documented if a claim arrives",
   "Negotiation support and settlement strategy",
   "Construction analysis to support your lawyer where a dispute escalates",
  ],
  "gets": [
   "A clear view of what you owe, and what you don't",
   "A draft response for you to send, set out on the facts",
   "Disagreements dealt with early and on the record",
  ],
  "builder_view": "A delay claim is only as strong as the contemporaneous records behind it. The side with better records is usually in the stronger position. We set up your records from the start, so that if a claim ever comes, the facts are already on your side.",
  "faqs": [
   ("What is an extension of time claim?", "It is a contractor's request for more time to complete, usually because of events they say were not their responsibility, such as late information or owner changes. If granted, it can remove your right to delay damages and may come with a claim for extra cost."),
   ("Are you lawyers?", "No. We give construction and commercial advice. For legal advice, and for any formal dispute process, you should appoint a UAE-qualified lawyer. We often work alongside one."),
   ("My project is already in dispute. Can you help?", "Yes. We will review the contract, the records and the claim, and tell you honestly where you stand. See also our <a href=\"/services/stalled-project-rescue/\">stalled project service</a>."),
  ],
  "related": ["stalled-project-rescue", "cost-and-programme-control", "consultant-and-contractor-selection"],
 },
 {
  "slug": "stalled-project-rescue",
  "short": "Stalled or troubled builds",
  "name": "Stalled and troubled villa project recovery",
  "title": "Stalled Villa Project Rescue Dubai | Eastbridge",
  "description": "Villa build stalled, over budget or in dispute? We establish where it really stands, set a recovery plan and see it through on your side.",
  "h1": "When the build has stalled",
  "lede": "Contractors walk off. Consultants go quiet. Budgets run out halfway. It happens more often than anyone admits, and many stalled projects can be recovered.",
  "image": "esplanade-road-01",
  "stage": "Mid-project",
  "intro": """<p>A stalled villa is stressful because nobody seems to have the full picture. The contractor says the owner owes money. The consultant says the contractor is late. The owner has paid more than half the contract value for a building that looks less than half finished.</p>
<p>We start with a fixed-scope review: what has been built and to what standard, what has been paid and what is owed, what the contract says, and what it will take to finish. Then we set out the options plainly, from getting the current contractor back on track to a managed changeover, and help you carry out the one you choose.</p>""",
  "does": [
   "Independent review of progress, quality, payments and contract position",
   "A realistic cost and time to complete",
   "Options appraisal: continue, renegotiate or replace",
   "Support through a contractor changeover, with records protected",
   "Recovery programme and reporting through to completion",
  ],
  "gets": [
   "The full picture within two to three weeks",
   "Clear options with costs and risks",
   "A recovery plan, and someone to run it",
  ],
  "builder_view": "From the builder's side, we know what an incoming contractor needs: a clear record of what's there, what's defective and what's paid. Without that, the new price carries every unknown as risk. With it, the job can restart at a fair price.",
  "faqs": [
   ("What should I do if my contractor stops work?", "Pause any payment not yet properly valued until you understand the position, keep all records, photograph the site, and take advice from a UAE-qualified lawyer before withholding sums the contract says are due or terminating anything. Then get an independent view of what it will take to finish. Our guide to <a href=\"/insights/stalled-villa-project-dubai/\">the first ten days of a stalled build</a> sets out the order."),
   ("Can a half-built villa be finished by a new contractor?", "Yes, often successfully. The key is an accurate record of the work in place and its quality, so the new contractor can price it fairly."),
   ("How quickly can you start?", "Within a week, with the full picture within two to three weeks. The initial review is " + _fee("review", "priced within our Review range, {fee}, and confirmed in writing after the free call", "quoted in writing after the free call") + "."),
  ],
  "related": ["variations-delays-and-claims", "site-visits-and-reporting", "owners-representative"],
 },
 {
  "slug": "snagging-and-handover",
  "short": "Snagging and handover",
  "name": "Villa snagging and handover management",
  "title": "Villa Snagging & Handover Dubai | Eastbridge",
  "description": "Snagging, commissioning checks and handover as one stage of our full client-side service for villas in Dubai and Abu Dhabi, tracked to close-out.",
  "h1": "Handover is not the end of the project. It is the last chance to get it right.",
  "lede": "Once you have the keys and the contractor has his money, defects are harder to close. We help make sure the house is finished, tested and documented before you accept it.",
  "image": "ansells-01",
  "stage": "Practical completion and defects period",
  "intro": """<p>A good handover is quiet. The snag list is short because quality was managed throughout, the systems have been tested and demonstrated, and a full set of documents is waiting. A poor handover is a long list, a frustrated contractor who wants to leave, and months of chasing.</p>
<p>We plan handover from the start of construction, not the end. We inspect room by room and system by system, witness commissioning, compile the snag list with the consultant and contractor, and make sure the documents you'll need for the life of the house are collected before retention is released.</p>
<p>Snagging and handover are one stage of our full client-side service, on a villa we have represented you on from the start. They are not sold on their own, and there is no separate snagging fee.</p>
<h2>How this differs from a one-visit snag report</h2>
<p>A snagging inspection firm usually visits once, near the end, and reports what it can see on the day. That is a useful service, and a different one. Because we have followed the villa through construction, we know what sits behind the finishes, which areas gave trouble on the way, and what the contract says about completion, retention and defects. So our work does not stop at a report: it runs through close-out of every item, the handover documents, the release of retention and the defects liability period.</p>
<p>Doing a first pass yourself? Download our free <a href="/guides/villa-snagging-checklist/">villa snagging checklist</a>: systems and rooms with tick boxes and a severity column, the handover documents to collect, and the defects liability periods with their legal sources. After handover, our guide to <a href="/insights/defects-liability-period-uae/">the defects liability period in the UAE</a> covers what to do in the first year.</p>""",
  "does": [
   "Pre-handover inspection, room by room and system by system",
   "Witnessing of commissioning: air conditioning, water, pool, lighting controls, security",
   "Snag list compiled, issued and tracked to close-out",
   "Handover documents collected and checked",
   "Defects period managed and retention released only when earned",
  ],
  "gets": [
   "Systems tested and demonstrated before you accept the house",
   "A complete handover file: completion certificate, as-built drawings, warranties, O&M manuals",
   "Defects tracked to close-out",
  ],
  "builder_view": "Snag lists stall when they are vague, very long or issued late. Clear photographs, specific locations, and a list issued in sections as areas finish are the fastest way to get every item closed. Retention is your leverage. Spend it wisely.",
  "faqs": [
   ("What should I check before accepting a new villa?", "Waterproofing, drainage and roof areas, air conditioning performance, plumbing and hot water, electrical and lighting controls, glazing and doors, finishes, pool and external works. Our <a href=\"/insights/villa-snagging-checklist-dubai/\">snagging guide</a> goes room by room, and the <a href=\"/guides/villa-snagging-checklist/\">printable checklist</a> adds a severity column and a snag log."),
   ("Can I appoint you just for snagging?", "No. Snagging and handover are one stage of our full service on a villa we represent, so there is no snagging-only fee. If all you need is a single inspection of a finished villa, a snagging inspection firm offers that, and our free <a href=\"/guides/villa-snagging-checklist/\">snagging checklist</a> will help you do a first pass yourself."),
   ("What documents should I receive at handover?", "At least the completion certificate, as-built drawings, warranties and guarantees, operation and maintenance manuals, test certificates and keys and codes schedules."),
   ("Can I inspect before final payment?", "Usually, yes, and you should. Building contracts commonly tie the payment due at completion, and the first release of retention, to an inspection and an agreed snag list, but the order is set by your contract, so read it before the handover appointment. For a villa bought from a developer, the sale and purchase agreement sets the order of payment, inspection and handover. A UAE-qualified lawyer can confirm your rights. On our appointments, the pre-handover inspection is planned into the programme so that it happens before the payment, not after it."),
   ("What if the villa fails inspection?", "A handover inspection rarely ends in a simple pass or fail. It produces a list. Minor items are normally recorded on a snag list for the contractor to close within an agreed period. Serious defects, such as water coming in, unsafe electrics or systems that do not work, are a reason to delay accepting the villa until they are put right and inspected again. The authority's completion inspection is separate; your registered consultant will confirm where it stands. What you can do next depends on your contract: we set out the options and recommend one, and a UAE-qualified lawyer advises on your rights."),
   ("Should I sign handover documents before snags are closed?", "Read exactly what you are being asked to sign first. A handover or completion certificate can start the defects liability period, trigger the release of part of the retention and affect delay damages, so signing one is a significant step. Accepting handover with a list of minor snags attached is common, provided the list forms part of the document and the contractor's obligation to close each item, and by when, is clear. Do not sign anything stating the villa was accepted free of defects while items are still open. If in doubt, take advice from a UAE-qualified lawyer before you sign."),
   ("Do I need to be present?", "Not at every inspection. On our appointments we carry out the pre-handover inspections and report each item with photographs, so you can follow it from abroad. If you can, attend the final walk-through and the demonstration of the systems: it is your home, and that is when you are shown how to run it. If you cannot travel, we can take you through it on a video call. Whatever is signed at handover is your decision."),
  ],
  "related": ["site-visits-and-reporting", "villa-renovation-project-management", "owners-representative"],
 },
 {
  "slug": "overseas-owners",
  "short": "For owners living overseas",
  "name": "Villa project representation for owners living overseas",
  "title": "Build a Dubai Villa From the UK or Abroad | Eastbridge",
  "description": "Building or renovating a villa in Dubai while living in the UK or Europe? We represent you on the ground and send you clear, regular reports.",
  "h1": "Building in Dubai while living somewhere else",
  "lede": "Many villa owners are not in Dubai most of the time. The project still needs decisions every week. We bring them to you with the information and a recommendation, so that nothing is decided without you.",
  "image": "menwinnion-01",
  "stage": "The whole project",
  "intro": f"""<p>Absentee owners are the most exposed clients in construction. Decisions are made on site because the owner isn't there. Payments are approved from a photograph. Small problems are reported late because nobody wants to deliver bad news by phone. By the time the owner visits, the project has drifted.</p>
<p>Philip is British and spent 21 years building award-winning homes for demanding owners, many of whom lived away from site, so we know how British and European owners expect a project to be run and reported. We represent you on the ground in Dubai, report in a form you can read in five minutes, and bring you every decision that matters with a clear recommendation.</p>
<p>{_COVERAGE}</p>""",
  "does": [
   "Representation on site and in meetings in your absence",
   "Regular written reports with photographs, at the frequency agreed in your scope of works",
   "A decision log so nothing is agreed without your sign-off",
   "Payment review before any money leaves your account",
   "Video walk-throughs at key stages",
   "Scheduling of your visits around the decisions that need you in person",
  ],
  "gets": [
   "Confidence that the project is where the reports say it is",
   "Decisions brought to you with options and a recommendation",
   "A single point of contact, in your time zone when you need it",
  ],
  "builder_view": "The sites that ran best for remote clients were the ones with a disciplined weekly rhythm: a set report, a set call, and decisions logged with dates. It isn't complicated. It just has to happen every week without fail.",
  "faqs": [
   ("Can I build a villa in Dubai without living there?", "Yes. Many owners do. You will need a reliable local team, clear reporting, and a few well-timed visits at the key decision points. Our <a href=\"/insights/building-a-villa-in-dubai-from-the-uk/\">guide for overseas owners</a> explains how."),
   ("How do you report to me?", "Regular written reports with photographs, at the frequency agreed in your scope of works, plus calls whenever a decision is needed. Everything is readable on a phone."),
   ("Do I need to give you power of attorney?", "Usually not. We advise and represent; you make the decisions and payments. Where a formal authority is needed for a specific task, take legal advice first."),
  ],
  "related": ["site-visits-and-reporting", "owners-representative", "cost-and-programme-control"],
 },
 {
  "slug": "development-advisory",
  "short": "Development advisory",
  "name": "Development advisory for small developers and investors",
  "title": "Residential Development Advisory Dubai | Eastbridge",
  "description": "Development advisory for private investors and small developers in Dubai and Abu Dhabi: feasibility, build cost, team and delivery control.",
  "h1": "For investors building more than one house",
  "lede": "Plot-to-sale villa projects, small residential schemes and build-to-rent. We bring a developer-builder's discipline to the numbers and the delivery.",
  "image": "three-mile-beach-02",
  "stage": "Feasibility to sale or let",
  "intro": """<p>Our UK background includes residential developments as well as one-off homes, including a scheme of fifteen beach houses and several multi-unit developments delivered as main contractor. Building more than one house changes the priorities: repeatability, procurement, phasing, sales timing and cash flow matter as much as design.</p>
<p>We help private investors and small developers test feasibility, set realistic build costs and programmes, appoint the right team and keep delivery on track. We are not a broker and do not sell property; where sales or leasing are involved, we work alongside your appointed licensed agents.</p>""",
  "does": [
   "Feasibility: build cost, programme and risk for the scheme you are considering",
   "Plot-to-sale or plot-to-let appraisals with realistic construction assumptions",
   "Team appointment advice and contract strategy",
   "Delivery control: cost, programme, quality and reporting",
   "Phasing and cash-flow planning with your finance partners",
  ],
  "gets": [
   "Feasibility built by someone who has priced and delivered real schemes",
   "A delivery plan that matches the money",
   "Monthly reporting suitable for partners and lenders",
  ],
  "builder_view": "On multi-unit schemes, the profit was made or lost on repetition. When every house was slightly different, every house was priced as a one-off. Fixing details early and repeating them is the cheapest efficiency there is.",
  "faqs": [
   ("Do you invest in projects?", "No. We advise and represent the client. That keeps our advice independent."),
   ("Do you sell or let the finished homes?", "No. We are not a brokerage. Sales and leasing are carried out by licensed agents you appoint."),
   ("What size of project do you take on?", "From a single villa to small residential schemes. We scale the appointment to the scheme."),
  ],
  "related": ["plot-due-diligence", "cost-and-programme-control", "consultant-and-contractor-selection"],
 },
]

BY_SLUG = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- "You receive" (competitor brief 2.2)
# The documents each service produces, as a scannable list: (document, one line on what is in it).
# Kept apart from SERVICES so the page copy above can change without touching these lists.
# Wording rules: we observe and record, review and recommend; nothing here certifies, approves
# design or promises a visit frequency (that is set in each written appointment).
DELIVERABLES = {
 "owners-representative": [
  ("Brief, budget and programme", "Agreed with you before design money is spent, with contingency held by you."),
  ("Site note after every visit", "Photographs, progress against programme, workmanship observations and issues raised."),
  ("Monthly cost and programme report", "Paid to date, forecast cost to complete and forecast final cost; programme against the contract date; risks; decisions needed."),
  ("Normalised tender comparison", "Consultant and contractor bids set out like-for-like: exclusions, provisional sums, preliminaries and programme."),
  ("Payment-application review notes", "Each application checked against the work in place and the contract, with a recommended amount."),
  ("Variation register", "Every change request with its reason, price, time effect, status and your decision."),
  ("Decision log", "Every choice you make, with its date, cost and time effect, so nothing is relitigated later."),
  ("Risk and issues log", "Open risks and issues, who owns each one and when it is due to close."),
  ("Close-out document list", "The handover file checked item by item: completion certificate, as-built drawings, warranties and manuals."),
 ],
 "villa-construction-project-management": [
  ("Brief, budget and programme pack", "Set from the brief and the plot before design starts."),
  ("Design-stage cost check notes", "The design reviewed against the budget at concept, detailed design and before pricing."),
  ("Normalised tender comparison", "Contractor bids set out like-for-like, with the assumptions tested."),
  ("Site note after every visit", "Photographs, progress against programme and anything that will cost money or time later."),
  ("Monthly cost and programme report", "Paid to date, forecast cost to complete and forecast final cost, with the programme and the decisions needed."),
  ("Payment-application review notes", "A recommendation before every payment."),
  ("Variation register", "Every change logged with its price, time effect and your decision."),
  ("Decision log", "What you decided, when, and what it changed."),
  ("Snag list and close-out document list", "Defects tracked to close-out and the handover file checked item by item."),
 ],
 "villa-renovation-project-management": [
  ("Condition summary", "What the specialists you appoint found, in plain English, and what it means for scope and budget."),
  ("Renovate-or-rebuild comparison", "Prepared where the numbers are close, on the same basis for both options."),
  ("Scope and budget split", "What must be done separated from what you would like done, with a contingency set for the age of the house."),
  ("Approvals tracker", "Master developer NOC and authority permit status, followed with your consultant or contractor."),
  ("Normalised tender comparison", "Renovation bids set out like-for-like."),
  ("Site note after every visit", "Photographs, progress and anything found once walls and ceilings are opened."),
  ("Monthly cost and programme report", "Forecast cost to complete and forecast final cost, programme, risks and decisions needed."),
  ("Payment-application review notes and variation register", "A recommendation before every payment, and every change logged."),
  ("Snag list and close-out document list", "Defects tracked to close-out and the handover documents collected."),
 ],
 "plot-due-diligence": [
  ("Written plot review report", "A plain answer on whether the numbers work, and why."),
  ("Design guideline summary", "Coverage, heights, setbacks and materials from the master developer's rules."),
  ("Sale terms notes", "Build-by deadlines and any penalties in the sale terms, flagged for your lawyer."),
  ("Build budget range", "A realistic range for the house you want, and the total cost of ownership around it."),
  ("Questions for the seller or developer", "A short list to put to them before you commit."),
 ],
 "design-and-approvals": [
  ("Written brief", "Rooms, sizes, finishes, priorities and what you will not compromise on."),
  ("Design-stage cost check notes", "The design reviewed against the budget at concept, detailed design and before pricing."),
  ("Value review notes", "Where structural or services cost looks high, the questions to put to your consultant."),
  ("Approvals tracker", "What your consultant has submitted, what is waiting, and on whom."),
  ("Decision log", "Design decisions recorded with their cost and time effect."),
 ],
 "consultant-and-contractor-selection": [
  ("Shortlist with reasons", "Consultants and contractors suited to your type of villa."),
  ("Licence and registration check record", "What was checked, where and when, through the official registries."),
  ("Normalised tender comparison", "Bids set out like-for-like: exclusions, provisional sums, preliminaries and programme."),
  ("Reference call notes", "What past clients said, not only the showcase projects."),
  ("Contract terms notes", "Payment, retention, bonds, delay and variation terms, with points to raise before you sign."),
  ("Written recommendation", "Which bid we would choose and why. You make the appointment."),
 ],
 "cost-and-programme-control": [
  ("Cost plan at each design stage", "The budget broken down and updated as the design develops."),
  ("Monthly cost and programme report", "One page: paid to date, forecast cost to complete, forecast final cost against your budget, programme and decisions needed, with the detail behind it."),
  ("Cost-to-complete forecast", "What is still to be spent: remaining committed cost, remaining uncommitted cost and a risk allowance, each shown separately and counted once. Added to paid to date, it gives the forecast final cost."),
  ("Payment-application review notes", "Each application checked against the work actually done, with a recommended amount before you pay."),
  ("Payment and cash-flow forecast", "What falls due and when, so the money is ready before it is needed."),
  ("Variation register", "Every change request: is it a genuine change, is the price fair, what does it do to time, and your decision."),
  ("Provisional sum tracker", "Each provisional sum against its final cost, as the work is priced and built."),
  ("Contingency register", "Contingency held and released by you, with a clear audit trail. Open risks are priced from it into the risk allowance; the rest is shown as unallocated, never as a second allowance on top."),
  ("Advance payment and retention tracker", "What has been paid in advance, recovered, held back and released, against the contract terms. Retention held back is still owed, so it stays in remaining committed cost until it is released."),
  ("Programme review notes", "The contractor's programme tested, and the critical path watched month by month."),
  ("Risk register", "Each risk with its likely cost and time exposure, and who owns it."),
  ("Final account statement", "Agreed line by line, with the records behind every figure."),
 ],
 "site-visits-and-reporting": [
  ("Site note after every visit", "Photographs, progress against programme, workmanship observations and housekeeping."),
  ("Photo record before work is covered up", "What we observed and recorded in ceiling voids, wall chases and waterproofing before they were closed."),
  ("Monthly written report", "Progress, quality and the decisions you need to make."),
  ("Issues log", "Each issue raised through your consultant, with an owner and a date, tracked to close-out."),
  ("Progress meeting notes", "What was said and agreed, written from your side."),
 ],
 "materials-and-specialist-sourcing": [
  ("Sourcing schedule", "Each item, its supplier, lead time, order-by date and delivery window, set against the programme."),
  ("Sample record", "Photographs of every sample and reference panel, with the decision you made on each."),
  ("Sourcing trip note", "What was chosen on each trip, the prices quoted and the next steps."),
  ("Owner-supplied items schedule", "Who orders, receives, stores, insures and fits each item, as agreed with your contractor."),
  ("Delivery check note", "Each consignment checked against the approved sample, specification and quantity, with any shortfall raised at once."),
 ],
 "variations-delays-and-claims": [
  ("Variation register", "Every variation with its entitlement, price, time effect and status."),
  ("Variation review notes", "Is it a genuine change, is the price fair, and what does it do to time?"),
  ("Extension of time assessment", "The contractor's claim tested against the contract, the programme and the records."),
  ("Record-keeping set-up", "What to record, and how, from day one, so your position is documented."),
  ("Draft responses", "A reply you can send to the contractor, set out on the facts."),
  ("Construction analysis for your lawyer", "Where a dispute escalates, the technical and commercial picture your lawyer needs."),
 ],
 "stalled-project-rescue": [
  ("Position report", "Progress, quality, payments and the contract position, within two to three weeks."),
  ("Record of work in place", "A photographed record of what is built, its condition and what is defective."),
  ("Payments reconciliation", "What has been paid against the value of the work in place."),
  ("Cost and time to complete", "A realistic forecast of what it will take to finish, kept separate from what has already been paid."),
  ("Options appraisal", "Continue, renegotiate or replace, with the cost and risk of each."),
  ("Recovery programme and monthly report", "The plan you choose, and progress against it through to completion."),
 ],
 "snagging-and-handover": [
  ("Pre-handover inspection notes", "Room by room and system by system, with photographs."),
  ("Commissioning record", "Which systems we saw tested and demonstrated, when, and what was outstanding."),
  ("Snag list", "Numbered, located, photographed and graded, issued in sections as areas finish, and tracked to close-out."),
  ("Close-out document list", "Completion certificate, as-built drawings, warranties, O&M manuals, test certificates and keys and codes, checked item by item."),
  ("Defects register", "Defects reported during the defects liability period, and when each was closed."),
  ("Retention release recommendation", "Whether the retention has been earned, and what is still open."),
 ],
 "overseas-owners": [
  ("Site note after every visit", "Photo-led and readable on a phone in a few minutes."),
  ("Monthly written report", "Cost, programme, risks and the decisions that need you."),
  ("Decision log", "Nothing agreed without your sign-off, and every decision recorded with its date."),
  ("Payment-application review notes", "A recommendation before any money leaves your account."),
  ("Video walk-throughs at key stages", "So you can see the work for yourself between visits."),
  ("Visit planner", "The decisions that need you in person, and when to be in Dubai for them."),
 ],
 "development-advisory": [
  ("Feasibility appraisal", "Build cost, programme and risk for the scheme you are considering."),
  ("Plot-to-sale or plot-to-let appraisal", "With the construction assumptions set out, so partners can test them."),
  ("Contract strategy note", "How to procure and appoint for the scheme."),
  ("Phasing and cash-flow plan", "Prepared with your finance partners."),
  ("Monthly report for partners and lenders", "Cost, programme, quality and risks in one place."),
 ],
}

# The headline outcome, one line above each "You receive" list (audit 1 November 2026, priority 3), so a buyer
# sees what the service achieves before the detailed paperwork. Same wording rules as DELIVERABLES.
OUTCOMES = {
 "owners-representative": "One person on your side from brief to handover, so you always know where the cost, the programme and the decisions stand.",
 "villa-construction-project-management": "A design checked against your budget at every stage, a contractor chosen on like-for-like bids, and every payment and change reviewed before you approve it.",
 "villa-renovation-project-management": "A renovation scoped and priced on what the house actually needs, with the approvals route and the budget clear before work starts.",
 "plot-due-diligence": "A written answer on whether the plot suits the house you want, and what the whole project is likely to cost, before you commit.",
 "design-and-approvals": "A design checked against your brief and budget before it goes for approval, and the approvals your consultant submits tracked through to the permit.",
 "consultant-and-contractor-selection": "Bids you can compare like-for-like, and a contract you understand, before you make the appointment.",
 "cost-and-programme-control": "Every month, an up-to-date forecast final cost set against your budget, and a recommendation in front of you before any payment or change.",
 "site-visits-and-reporting": "An independent view of progress and workmanship, reported to you in plain English.",
 "materials-and-specialist-sourcing": "The stone, joinery, lighting and fittings you chose, with lead times planned and each delivery checked against the sample you approved.",
 "variations-delays-and-claims": "Every variation and delay claim tested against the contract and the records before you decide.",
 "stalled-project-rescue": "A clear picture of where the project stands and a costed route to completion that you choose.",
 "snagging-and-handover": "Defects listed and tracked to close-out, and the handover documents checked, before you accept the house.",
 "overseas-owners": "A project you can follow and decide on from abroad, with nothing agreed without your sign-off.",
 "development-advisory": "Construction assumptions your partners and lenders can test, and one monthly report on cost, programme and risk.",
}

# An illustrative layout shown beside the document list. No figures: the owner's own cost plan supplies them.
# Cost vocabulary (audit 1 November 2026), used the same way across the site and in the glossary:
# paid to date + forecast cost to complete = forecast final cost, where forecast cost to complete =
# remaining committed cost + remaining uncommitted cost + risk allowance, and approved budget - forecast final
# cost = unallocated contingency. Nothing is counted twice: remaining committed cost excludes what has been
# paid, and the risk allowance is drawn from the contingency, so the two are never added together.
SPECIMENS = {
 "cost-and-programme-control": ("The one-page monthly summary", [
  ("Paid to date", "Cash actually paid, including any advance payment"),
  ("Remaining committed cost", "Contract sum, agreed variations and signed orders, less paid to date. Retention held back stays here until released"),
  ("Remaining uncommitted cost", "Work not yet let or agreed, at its forecast value, including pending variations and the forecast change to provisional sums"),
  ("Risk allowance", "Each open risk, priced and drawn from your contingency, counted once"),
  ("Forecast cost to complete", "Remaining committed plus remaining uncommitted cost plus risk allowance. Excludes paid to date"),
  ("Forecast final cost", "Paid to date plus forecast cost to complete"),
  ("Unallocated contingency", "Approved budget less forecast final cost: held by you, each release recorded"),
  ("Variations awaiting your decision", "Price and time effect of each"),
  ("Programme", "Forecast completion against the contract date"),
  ("Decisions needed this month", "With the date each one is needed by"),
  ("Top risks", "Likely cost and time exposure, and who owns each"),
 ]),
}

# "A month on your project" (owners-representative only): an illustrative month during construction.
MONTH_ON_PROJECT = [
 ("Site visits", "We walk the site, observe and record progress and workmanship, photograph work before it is covered up, and send you a site note after each visit."),
 ("Progress meeting", "We attend as your representative, raise issues with the consultant and contractor, and log each one with an owner and a date."),
 ("Payment application", "We check the contractor's application against the work in place and the contract, and send you review notes with a recommended amount. You decide, and you pay the contractor directly."),
 ("Change requests", "Each one goes into the variation register with its price and time effect, and comes to you with a recommendation. Nothing changes without your decision."),
 ("Decisions", "The decision log shows what you need to decide, by when, and what each option costs."),
 ("Month end", "Your monthly cost and programme report: paid to date, forecast cost to complete, forecast final cost, programme, risks and decisions needed. Then a call to go through it."),
]

# WhatsApp: the topic slotted into the page's message template ("Hello, I have a question about {topic}.").
WA_TOPIC = {
 "owners-representative": "owner's representation for my villa",
 "villa-construction-project-management": "building a new villa",
 "villa-renovation-project-management": "renovating my villa",
 "plot-due-diligence": "a plot review",
 "design-and-approvals": "the design and approvals for my villa",
 "consultant-and-contractor-selection": "choosing a consultant and contractor",
 "cost-and-programme-control": "cost and programme control on my villa",
 "site-visits-and-reporting": "site visits and reporting on my villa",
 "materials-and-specialist-sourcing": "sourcing materials for my villa",
 "variations-delays-and-claims": "a variation, delay or claim on my villa",
 "stalled-project-rescue": "a stalled villa project",
 "snagging-and-handover": "the handover of my villa",
 "overseas-owners": "building in Dubai while living abroad",
 "development-advisory": "a development project",
}
