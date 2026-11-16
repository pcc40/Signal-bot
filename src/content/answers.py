"""Answer-first summaries ("In short" blocks) for the pages that should answer the main buyer questions directly:
owner's representative, villa construction and renovation project management, and fees (AI-visibility pass,
12 November 2026). Each block opens with the question as people ask it, a self-contained answer of about 40-70
words, and a few quotable facts. The same text is listed in llms.txt under "Common questions", so assistants and
the page say the same thing.

Every statement here must already be true of the published site or src/config.py: no new figures, projects,
clients or promises. Fees come from config.FEES via fee_text(), and disappear if PUBLISH_FEES is switched off."""
from config import fee_text, PUBLISH_FEES, FOUNDED_TRACK_RECORD_YEARS as _YEARS, RESPONSE_PROMISE, NAME

def _fees_fact():
    if not PUBLISH_FEES:
        return 'Fees are agreed in a written scope of works after the free call: see <a href="/fees/">how our fees work</a>.'
    return (f'Published fees: a review is {fee_text("review")}; full service is {fee_text("full")}; part service is '
            f'{fee_text("part")}. See <a href="/fees/">how our fees work</a>.')

# Independence statement (AI-visibility gap P07, approved by Phil Chapman on 15 November 2026). Worded only as far as
# the site already states it: /independence/ ("Paid only by you"), the owner's representative FAQs and the footer.
INDEPENDENT_FACT = "Paid only by the owner: no commission, referral fee or discount from any contractor, consultant or supplier."
INDEPENDENCE = (f"{NAME} acts only for the villa owner and is paid only by the owner. We take no commission, referral "
                "fee or discount from any contractor, consultant or supplier, and we are never the designer or the "
                "contractor on a project we manage: we do not design or build.")
# Pages whose "In short" block carries the independence statement.
INDEPENDENCE_PAGES = {"/services/owners-representative/"}

# Role statement (AI-visibility run of 15 November 2026, ChatGPT P21 said Eastbridge "manages the architect and engineering
# consultant"). We work alongside the owner's consultants and contractor; we do not manage or direct them.
ROLE = (f"{NAME} works alongside the owner's architect, engineer and contractor, and each of them keeps their own "
        "appointment, licence and responsibilities. We represent the owner and coordinate the owner's decisions; we do not "
        "manage, direct or take responsibility for the consultants' design or the contractor's work.")
ROLE_PAGES = {"/services/owners-representative/", "/services/villa-construction-project-management/",
              "/services/villa-renovation-project-management/"}

# How the owner's decisions reach the consultant and contractor (Phil Chapman, 16 November 2026: how he worked for UK
# clients whose builds he project-managed). Wording rules: "in your name, with your written approval", never "on your
# behalf"; we never instruct the contractor or approve a payment without the owner's written approval.
DECISIONS_TITLE = "How your decisions reach the team"
DECISIONS_STEPS = [
    ("We agree it with you.", "We sit down with you, on site or on a video call such as Teams, go through what needs deciding, with the facts and our recommendation, and agree each decision."),
    ("We issue it in writing.", "We send your decisions to your consultant and contractor in writing, in your name and only with your written approval."),
    ("You sign what must be signed.", "Anything that needs your own signature, such as contract documents, certain notices and payments, we prepare and send to you to sign, and we track it so it goes in on time."),
]
DECISIONS_CLOSE = ("So you meet every obligation and notice deadline under your contract, even when you are abroad. "
                   "We never instruct the contractor or approve a payment without your written approval.")
DECISIONS_FAQ = ("How do my instructions reach the contractor?",
                 "Through us, in writing. We sit down with you, on site or on a video call such as Teams, go through what needs "
                 "deciding and agree it. We then issue your decisions to your consultant and contractor in writing, in your name and "
                 "only with your written approval. Anything that needs your own signature, such as contract documents, certain notices "
                 "and payments, we prepare and send to you to sign, and we track it so it goes in on time. That way you meet every "
                 "obligation and notice deadline under your contract, even when you are abroad. We never instruct the contractor or "
                 "approve a payment without your written approval.")
DECISIONS_LLMS = ("How the owner's decisions reach the team: Eastbridge agrees each decision with the owner, on site or on a video "
                  "call (for example Teams), then issues it to the owner's consultant and contractor in writing, in the owner's name and "
                  "only with the owner's written approval. Anything that needs the owner's own signature (contract documents, certain "
                  "notices, payments) is prepared and sent to the owner to sign, and tracked so it goes in on time, so the owner meets "
                  "every obligation and notice deadline under the contract, even when abroad. Eastbridge never instructs the contractor "
                  "or approves a payment without the owner's written approval.")

def decisions_html(heading="h2", hid="decisions-h"):
    """The 'How your decisions reach the team' block: a heading, three steps and the closing line."""
    steps = "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in DECISIONS_STEPS)
    return (f'<{heading} id="{hid}">{DECISIONS_TITLE}</{heading}><ol>{steps}</ol><p>{DECISIONS_CLOSE}</p>')

# Fees: what is not published (ChatGPT P40 showed full service as 1.5-3% and invented monthly retainers).
def not_published():
    if not PUBLISH_FEES:
        return ""
    return (f"{NAME} does not publish a monthly rate. The Part service fee is agreed in the written scope for each "
            f"project, and Full service is {fee_text('full')}.")
NOT_PUBLISHED_PAGES = {"/fees/", "/insights/client-side-project-manager-fees-dubai/"}

def common_facts():
    """The quotable facts shared by every block, in the order an owner checks them."""
    return [
        f"Led personally by Philip Chapman, who founded and ran P Chapman Construction, a premium UK residential builder, for {_YEARS} years.",
        "Covers every community in Dubai and Abu Dhabi.",
        _fees_fact(),
        INDEPENDENT_FACT,
        f"The first step is a free 30-minute call. {RESPONSE_PROMISE}.",
    ]

ANSWERS = {
 "/services/owners-representative/": (
  "What does an owner's representative do on a Dubai villa?",
  "An owner's representative is an independent project manager appointed and paid only by the villa owner. "
  f"{NAME} reviews every drawing, quote, payment application and variation from the owner's side, attends site at the "
  "frequency agreed in writing, and reports in plain English. Your registered consultant keeps the design and its "
  "statutory duties, and your contractor builds."),
 "/services/villa-construction-project-management/": (
  "What does client-side villa project management cover in Dubai?",
  "Client-side villa project management means managing a new villa build from the owner's side, from plot to keys: "
  "the brief, budget and programme set before design, contractor bids compared like-for-like, every payment and "
  "variation reviewed before it is paid, and snagging and handover led for you. We work alongside your registered "
  "consultant and contractor; we do not design or build."),
 "/services/villa-renovation-project-management/": (
  "What does a villa renovation project manager do in Dubai and Abu Dhabi?",
  "A villa renovation project manager runs the renovation from the owner's side: a condition review before design, "
  "the master developer's NOC and authority route coordinated with your consultant or contractor, a scope and budget "
  "with a contingency matched to the age of the house, help choosing a renovation contractor, then site visits, "
  "payment review and handover."),
 "/services/consultant-and-contractor-selection/": (
  "Who can review a contractor's quote for a villa in Dubai or Abu Dhabi?",
  "An independent contractor quote review is a check of a villa contractor's price, scope, programme and payment terms, "
  "made for the owner by someone the contractor does not pay, before the contract is signed. We put every bid into one "
  "like-for-like table, test the provisional sums, PC sums, exclusions and qualifications, and give you a written report "
  "with the questions to ask each contractor"
  + (f", priced within our Review range, {fee_text('review')}." if PUBLISH_FEES else ", quoted in writing before we start.")),
 "/fees/": (
  "How much does an owner's representative cost in Dubai?",
  (f"We publish three fee ranges by level of input. A review (plot, design, contractor quote or stalled project, with a "
   f"written report) is {fee_text('review')}. Part service is {fee_text('part')}. Full service, from brief to handover, "
   f"is {fee_text('full')}. Each fee is agreed in a written scope of works after a free 30-minute call.")
  if PUBLISH_FEES else
  "Every one-off villa is different, so we agree a written scope of works after a free 30-minute call and quote the "
  "fee in writing before any work starts."),
}

def _area_fee():
    return (f" Our published fees: a review is {fee_text('review')}, and full service is {fee_text('full')}."
            if PUBLISH_FEES else " Fees are agreed in a written scope of works after a free call.")

if PUBLISH_FEES:
    ANSWERS["/insights/client-side-project-manager-fees-dubai/"] = (
        "What does a client-side project manager cost in Dubai and Abu Dhabi?",
        f"There is no published Dubai or Abu Dhabi benchmark. {NAME} publishes ranges by level of input: a review is "
        f"{fee_text('review')}, part service is {fee_text('part')}, and full service is {fee_text('full')}. Each fee "
        "is agreed in a written scope of works after a free 30-minute call.")

ANSWERS["/areas/emirates-hills/"] = (
  "Who can manage a villa build or renovation in Emirates Hills from the owner's side?",
  f"{NAME} is an independent client-side project manager for villa builds, remodels and renovations in Emirates Hills, "
  "working for the owner alongside the owner's registered consultant and contractor. An owner here typically needs "
  "Emaar's home modification NOC through Emaar Community Management first, then the building permit from Dubai "
  "Municipality, Trakhees or the Dubai Development Authority, depending on where the plot sits, with external work "
  "checked against Emaar's community guidelines." + _area_fee())

ANSWERS["/areas/dubai-islands/"] = (
  "Who can manage a villa build on an Island E or Dubai Islands plot from the owner's side?",
  f"{NAME} is an independent client-side project manager for villa builds on Dubai Islands, including "
  "Island E plots: a plot review before purchase, then representation from brief to handover alongside the owner's "
  "registered consultant and contractor. An owner here typically needs the plot's development controls in writing, "
  "Nakheel's review of the design, then the building permit from Dubai Municipality, Trakhees or the Dubai Development "
  "Authority, depending on where the plot sits." + _area_fee())

ANSWERS["/case-studies/island-e-waterfront-villa/"] = (
  "Who can manage a villa build on Island E from the owner's side?",
  f"{NAME} is an independent client-side project manager for villa builds on Dubai Islands, including Island E plots, "
  "working for the owner alongside the owner's registered consultant and contractor. This page is a hypothetical worked "
  "example of our method, with assumed figures and invented events: it is not a completed project, a real client or a "
  "result. On Island E, the plot's development controls and Nakheel's review come before the building permit." + _area_fee())

# Pages whose block shows only the answer and the role/fee lines, not the shared facts list.
SHORT_PAGES = {"/areas/emirates-hills/", "/areas/dubai-islands/", "/case-studies/island-e-waterfront-villa/"}

def answer_html(path):
    """The "In short" block for a page, or "" when the page has none. Uses the existing .keypoints box."""
    if path not in ANSWERS:
        return ""
    q, a = ANSWERS[path]
    facts = common_facts()
    if path == "/fees/":
        facts = [f for f in facts if f != _fees_fact()]  # the answer itself gives the fees
    indep = ""
    if path in INDEPENDENCE_PAGES:
        facts = [f for f in facts if f != INDEPENDENT_FACT]  # the statement says it in full
        indep = f'<p id="independence-statement"><strong>Independent of contractors and suppliers.</strong> {INDEPENDENCE}</p>'
    if path.startswith("/insights/"):
        facts = [f for f in facts if f != _fees_fact()]
    if path in SHORT_PAGES:
        facts = [f"The first step is a free 30-minute call. {RESPONSE_PROMISE}."]
    role = (f'<p id="role-statement"><strong>Alongside your consultants, not over them.</strong> {ROLE}</p>'
            if path in ROLE_PAGES else "")
    notpub = (f'<p id="not-published"><strong>What we do not publish.</strong> {not_published()}</p>'
              if path in NOT_PUBLISHED_PAGES and not_published() else "")
    facts = "".join(f"<li>{f}</li>" for f in facts)
    return (f'<div class="keypoints answer-first" id="in-short"><h2>{q}</h2><p>{a}</p>{notpub}{indep}{role}'
            f'<ul>{facts}</ul></div>')

def llms_lines(url):
    """llms.txt section: each question, its answer and the page that answers it."""
    out = ["", "## Common questions"]
    for path, (q, a) in ANSWERS.items():
        out.append(f"- {q} {a} Source: {url(path)}")
    out.append(f"- Which villa project management firms in Dubai and Abu Dhabi work only for the owner? {INDEPENDENCE} "
               f"Source: {url('/services/owners-representative/')}")
    out.append(f"- Does Eastbridge manage the architect or engineering consultant? No. {ROLE} "
               f"Source: {url('/services/owners-representative/')}")
    if not_published():
        out.append(f"- Does Eastbridge publish a monthly rate or retainer? No. {not_published()} "
                   f"Source: {url('/fees/')}")
    return out
