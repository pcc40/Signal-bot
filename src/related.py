"""Related reading for insight articles: at least three related articles, the matching service page and the
matching area page, rendered at the end of every article from this shared data (never hand-written in the .md).

TOPIC maps an article slug to its service and area page. A new article needs no entry: its service comes from its
category, and its area from the first /areas/ link in its body, then from place names in its slug, then from the
category default. Add an entry only to override that. Area pages are linked as community guides, never as places
where Eastbridge has worked.

Articles are ranked by: a link between the two articles (either direction), same category, same service, same
area, shared words in the slug; ties go to the newer article. pages.insights() shows the first three in the
"Related reading" block and the next three as the "Read next" cards, so each article links to six others.
tools/seo_audit.py fails the build if an article page links to fewer than three other articles, or to no
service or area page."""
import re

TOPIC = {
    "abu-dhabi-villa-permit-tamm": ("design-and-approvals", "saadiyat"),
    "building-a-villa-in-dubai-from-the-uk": ("overseas-owners", "dubai-islands"),
    "buying-a-villa-plot-in-dubai-checks": ("plot-due-diligence", "dubai-islands"),
    "client-side-project-manager-fees-dubai": ("owners-representative", "palm-jumeirah"),
    "design-build-vs-separate-architect-villa": ("consultant-and-contractor-selection", "emirates-hills"),
    "dubai-municipality-villa-building-permit": ("design-and-approvals", "emirates-hills"),
    "how-long-to-build-a-villa-dubai": ("cost-and-programme-control", "dubai-islands"),
    "how-to-build-a-villa-in-dubai": ("villa-construction-project-management", "dubai-islands"),
    "how-to-choose-a-villa-contractor-dubai": ("consultant-and-contractor-selection", "emirates-hills"),
    "nakheel-noc-villa-renovation": ("villa-renovation-project-management", "palm-jumeirah"),
    "owners-representative-vs-project-manager-vs-consultant": ("owners-representative", "palm-jumeirah"),
    "palm-jumeirah-villa-renovation": ("villa-renovation-project-management", "palm-jumeirah"),
    "renovate-or-rebuild-villa-dubai": ("villa-renovation-project-management", "jumeirah-islands"),
    "sourcing-materials-abroad-dubai-villa": ("materials-and-specialist-sourcing", "al-barari"),
    "stalled-villa-project-dubai": ("stalled-project-rescue", "dubai-hills-estate"),
    "villa-construction-contracts-uae": ("variations-delays-and-claims", "emirates-hills"),
    "villa-construction-cost-dubai": ("cost-and-programme-control", "emirates-hills"),
    "villa-renovation-cost-dubai": ("villa-renovation-project-management", "jumeirah-islands"),
    "villa-renovation-mistakes-dubai": ("villa-renovation-project-management", "jumeirah-islands"),
    "villa-snagging-checklist-dubai": ("snagging-and-handover", "dubai-hills-estate"),
    "what-the-contractor-knows": ("variations-delays-and-claims", "emirates-hills"),
    "which-dubai-authority-covers-my-villa": ("design-and-approvals", "palm-jumeirah"),
}

# Fallbacks for articles not in TOPIC.
CATEGORY = {
    "Costs": ("cost-and-programme-control", "emirates-hills"),
    "Process": ("villa-construction-project-management", "dubai-islands"),
    "Approvals": ("design-and-approvals", "palm-jumeirah"),
    "Contracts": ("variations-delays-and-claims", "emirates-hills"),
    "Choosing a team": ("consultant-and-contractor-selection", "emirates-hills"),
    "Renovation": ("villa-renovation-project-management", "palm-jumeirah"),
    "Plots": ("plot-due-diligence", "dubai-islands"),
    "Overseas owners": ("overseas-owners", "dubai-islands"),
    "Handover": ("snagging-and-handover", "dubai-hills-estate"),
}
DEFAULT = ("owners-representative", "palm-jumeirah")
# Slug words that name a community (checked in this order).
PLACE_WORDS = [("palm-jebel-ali", "palm-jebel-ali"), ("jebel-ali", "palm-jebel-ali"), ("palm", "palm-jumeirah"),
               ("nakheel", "palm-jumeirah"), ("emirates-hills", "emirates-hills"), ("jumeirah-islands", "jumeirah-islands"),
               ("jumeirah-bay", "jumeirah-bay"), ("district-one", "district-one"), ("dubai-hills", "dubai-hills-estate"),
               ("emaar", "dubai-hills-estate"), ("al-barari", "al-barari"), ("dubai-islands", "dubai-islands"),
               ("island-e", "dubai-islands"), ("saadiyat", "saadiyat"), ("hudayriyat", "hudayriyat"),
               ("abu-dhabi", "saadiyat"), ("arabian-ranches", "arabian-ranches")]
STOP = {"a", "an", "and", "the", "of", "in", "to", "for", "on", "vs", "dubai", "villa", "uae", "how", "what", "your"}

def _links(p, kind):
    return re.findall(rf'href="/{kind}/([a-z0-9-]+)/', p.get("html", ""))

def topic(p, services, areas):
    """(service slug, area slug) for article p; both always exist in `services` / `areas`."""
    svc, area = TOPIC.get(p["slug"]) or (None, None)
    cat_svc, cat_area = CATEGORY.get(p.get("category"), DEFAULT)
    if not svc or svc not in services:
        svc = cat_svc if cat_svc in services else DEFAULT[0]
    if not area or area not in areas:
        area = next((a for a in _links(p, "areas") if a in areas), None) \
            or next((a for w, a in PLACE_WORDS if w in p["slug"] and a in areas), None) \
            or (cat_area if cat_area in areas else DEFAULT[1])
    return svc, area

def ranked(p, posts, services, areas):
    """Every other published article, most related first."""
    mine = topic(p, services, areas)
    out_links = set(_links(p, "insights"))
    words = set(p["slug"].split("-")) - STOP
    def score(q):
        theirs = topic(q, services, areas)
        s = 0
        if q["slug"] in out_links or p["slug"] in set(_links(q, "insights")):
            s += 4
        if q.get("category") == p.get("category"):
            s += 3
        if theirs[0] == mine[0]:
            s += 2
        if theirs[1] == mine[1]:
            s += 1
        s += len(words & (set(q["slug"].split("-")) - STOP))
        return s
    others = [q for q in posts if q["slug"] != p["slug"]]
    others.sort(key=lambda q: str(q.get("updated") or q["date"]), reverse=True)
    others.sort(key=score, reverse=True)       # stable: equal scores stay newest first
    return others

def block_html(p, posts, services, areas, esc):
    """The "Related reading" block: three articles, then the service and the area guide."""
    rel = ranked(p, posts, services, areas)[:3]
    svc, area = topic(p, services, areas)
    items = "".join(f'<li><a href="/insights/{q["slug"]}/">{esc(q["title"])}</a></li>' for q in rel)
    return (f'<nav class="keypoints related-reading" aria-labelledby="related-h"><h2 id="related-h">Related reading</h2><ul>{items}'
            f'<li>Our service: <a href="/services/{svc}/">{esc(services[svc]["short"])}</a></li>'
            f'<li>Area guide: <a href="/areas/{area}/">{esc(areas[area]["name"])}</a></li></ul></nav>')
