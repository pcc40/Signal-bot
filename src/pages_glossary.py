"""Glossary page: /glossary/ — villa construction terms for Dubai and Abu Dhabi owners."""
import datetime, html as H
import build as B
from content.glossary import GLOSSARY, BY_ID, SOURCES

esc = H.escape
PATH = "/glossary/"
TITLE = "Villa construction glossary for Dubai and Abu Dhabi owners"
SET_ID = B.url(PATH) + "#terms"


def _letter(g):
    return g["term"][0].upper()


def terms_sorted():
    return sorted(GLOSSARY, key=lambda g: g["term"].casefold())


def first_sentence(text):
    end = text.find(". ")
    return text if end < 0 else text[:end + 1]


def term_html(g):
    full = f' <span class="g-full">({esc(g["full"])})</span>' if g.get("full") else ""
    links = "".join(f'<a href="{h}">{esc(lbl)}</a>' for lbl, h in g.get("links", []))
    see = ", ".join(f'<a href="#{s}">{esc(BY_ID[s]["term"])}</a>' for s in g.get("see", []))
    extra = ""
    if links:
        extra += f'<p class="g-more"><span>Read more:</span> {links}</p>'
    if see:
        extra += f'<p class="g-see"><span>See also:</span> {see}</p>'
    return (f'<div class="g-item" id="{g["id"]}" data-term="{esc(g["term"].lower())} {esc(g.get("full", "").lower())}">'
            f'<dt><a class="g-anchor" href="#{g["id"]}">{esc(g["term"])}</a>{full}</dt>'
            f'<dd><p>{esc(g["d"])}</p>{extra}</dd></div>')


def schema():
    return {"@context": "https://schema.org", "@type": "DefinedTermSet", "@id": SET_ID,
            "name": TITLE, "url": B.url(PATH), "inLanguage": "en-GB",
            "description": "Plain-English definitions of the contract, cost, approval and handover terms that private villa owners meet when building or renovating in Dubai and Abu Dhabi.",
            "publisher": {"@id": B.ORG_ID},
            "hasDefinedTerm": [dict({"@type": "DefinedTerm", "@id": B.url(PATH) + "#" + g["id"], "name": g["term"],
                                     "description": g["d"], "url": B.url(PATH) + "#" + g["id"],
                                     "inDefinedTermSet": {"@id": SET_ID}},
                                    **({"alternateName": g["full"]} if g.get("full") else {}))
                               for g in terms_sorted()]}


FILTER_JS = """<script>
(function(){var i=document.getElementById('g-filter');if(!i)return;var items=[].slice.call(document.querySelectorAll('.g-item')),
groups=[].slice.call(document.querySelectorAll('.g-letter')),none=document.getElementById('g-none');
i.addEventListener('input',function(){var q=i.value.trim().toLowerCase(),shown=0;
items.forEach(function(el){var t=el.getAttribute('data-term')+' '+el.textContent.toLowerCase(),m=!q||t.indexOf(q)>-1;el.hidden=!m;if(m)shown++});
groups.forEach(function(g){g.hidden=!g.querySelector('.g-item:not([hidden])')});none.hidden=shown>0})})();
</script>"""


def glossary_page():
    from pages import credit_of
    crumbs = [("Home", "/"), ("Glossary", PATH)]
    terms = terms_sorted()
    letters = {}
    for g in terms:
        letters.setdefault(_letter(g), []).append(g)
    az = "".join(f'<li><a href="#letter-{l.lower()}">{l}</a></li>' if l in letters else
                 f'<li><span aria-hidden="true">{l}</span></li>' for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    groups = "".join(
        f'<section class="g-letter" id="letter-{l.lower()}" aria-labelledby="h-letter-{l.lower()}">'
        f'<h2 id="h-letter-{l.lower()}">{l}</h2><dl class="g-list">{"".join(term_html(g) for g in gs)}</dl></section>'
        for l, gs in letters.items())
    srcs = "".join(f'<li><a href="{esc(u)}" rel="noopener">{esc(t)}</a></li>' for t, u in SOURCES)
    image = "trelowen-03"
    body = B.banner(crumbs, "Villa construction glossary", (
        f"{len(terms)} terms you will meet when building or renovating a villa in Dubai or Abu Dhabi, "
        "explained in plain English from the owner's side of the table."), image, credit_of(image)) + f'''
<section class="section--tight"><div class="wrap g-intro">
<div class="prose"><p>Contracts, cost plans and site meetings come with their own language. Knowing what a provisional sum, an extension of time or a defects liability period actually means, and who is responsible for it, is the first step to keeping control of your budget and programme.</p>
<p>Each definition says who usually does what: the owner, the owner's DM-registered consultant, the contractor, or Eastbridge as your client-side project manager. This is general information, not legal or technical advice for your project. For contract questions, take advice from a UAE-qualified lawyer.</p></div>
<div class="g-tools"><label for="g-filter">Find a term</label><input id="g-filter" type="search" placeholder="For example: retention" autocomplete="off"></div>
</div></section>
<nav class="g-az" aria-label="Glossary A to Z"><div class="wrap"><ul>{az}</ul></div></nav>
<section class="section--tight g-body"><div class="wrap">
<p id="g-none" class="muted" hidden>No terms match your search. Try a shorter word, or <a href="/contact/">ask us</a>.</p>
{groups}
<div class="g-foot prose"><h2 id="sources">Sources</h2><ol class="small">{srcs}</ol>
<p class="small muted">Definitions reflect common usage and the official sources listed. Rules and procedures change, and your contract governs your project. Last reviewed {datetime.date.fromisoformat(B.TODAY).strftime("%B %Y")}.</p></div>
</div></section>
{FILTER_JS}
{B.cta_band("A term in your contract you are not sure about?", "Send it to us. We will explain how it usually works in practice and what to ask about it. For its legal effect on your contract, take advice from a UAE-qualified lawyer.")}'''
    B.page(PATH, "Villa Construction Glossary: Dubai & Abu Dhabi | Eastbridge",
           f"Plain-English definitions of {len(terms)} villa construction terms for Dubai and Abu Dhabi owners: NOCs, BOQs, retention, extensions of time and more.",
           body, crumbs, [schema()], og=B.og_image(image))


def llms_lines():
    lines = ["", "## Glossary", f"- [{TITLE}]({B.url(PATH)}): {len(GLOSSARY)} plain-English definitions"]
    for g in terms_sorted():
        name = g["term"] + (f" ({g['full']})" if g.get("full") else "")
        lines.append(f"- [{name}]({B.url(PATH)}#{g['id']}): {first_sentence(g['d'])}")
    return lines
