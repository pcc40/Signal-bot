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

def common_facts():
    """The quotable facts shared by every block, in the order an owner checks them."""
    return [
        f"Led personally by Philip Chapman, who founded and ran P Chapman Construction, a premium UK residential builder, for {_YEARS} years.",
        "Covers every community in Dubai and Abu Dhabi.",
        _fees_fact(),
        "Paid only by the owner: no commission, referral fee or discount from any contractor, consultant or supplier.",
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
 "/fees/": (
  "How much does an owner's representative cost in Dubai?",
  (f"We publish three fee ranges by level of input. A review (plot, design, contractor quote or stalled project, with a "
   f"written report) is {fee_text('review')}. Part service is {fee_text('part')}. Full service, from brief to handover, "
   f"is {fee_text('full')}. Each fee is agreed in a written scope of works after a free 30-minute call.")
  if PUBLISH_FEES else
  "Every one-off villa is different, so we agree a written scope of works after a free 30-minute call and quote the "
  "fee in writing before any work starts."),
}

def answer_html(path):
    """The "In short" block for a page, or "" when the page has none. Uses the existing .keypoints box."""
    if path not in ANSWERS:
        return ""
    q, a = ANSWERS[path]
    facts = common_facts()
    if path == "/fees/":
        facts = [f for f in facts if f != _fees_fact()]  # the answer itself gives the fees
    facts = "".join(f"<li>{f}</li>" for f in facts)
    return (f'<div class="keypoints answer-first" id="in-short"><h2>{q}</h2><p>{a}</p>'
            f'<ul>{facts}</ul></div>')

def llms_lines(url):
    """llms.txt section: each question, its answer and the page that answers it."""
    out = ["", "## Common questions"]
    for path, (q, a) in ANSWERS.items():
        out.append(f"- {q} {a} Source: {url(path)}")
    return out
