"""Location -> authority -> what it changes for your programme, for the communities we write about.

Used by build.py for the compact section in llms-full.txt. The same table appears, written out, in
src/content/insights/which-dubai-authority-covers-my-villa.md: keep the two in step.

Rule: in Dubai, the permit authority is never asserted by community name. Jurisdiction is set plot by plot
(Decree No. 22 of 2009, Law No. 8 of 2023, Law No. 16 of 2023), so the authority column says
"confirm with your consultant" unless a primary source settles it. Master developers are as verified in
WRITING_BRIEF.md and the area pages.
"""

RULE = ("Confirm with your consultant; never assume by community. In Dubai the permit authority (Dubai Municipality, "
        "Trakhees or the Dubai Development Authority) is set by the plot, not the community name, and can change.")

# (area, emirate, master developer: first approval, permit authority, what it changes for your programme)
AUTHORITY_TABLE = [
    ("Palm Jumeirah", "Dubai", "Nakheel NOC", "Confirm with your consultant",
     "Nakheel NOC before any authority submission; Nakheel site-access conditions before the contractor mobilises"),
    ("Jumeirah Islands", "Dubai", "Nakheel NOC", "Confirm with your consultant",
     "Nakheel NOC first; extensions and external changes need written approval before design is fixed"),
    ("Dubai Islands", "Dubai", "Nakheel NOC and guidelines", "Confirm with your consultant",
     "Plot builds start with Nakheel's design guidelines; allow for a developer review stage before the permit"),
    ("Palm Jebel Ali", "Dubai", "Nakheel", "Confirm with your consultant",
     "Nakheel NOC before any change to the villa or plot; get the current guidelines and NOC process from Nakheel"),
    ("Emirates Hills", "Dubai", "Emaar", "Confirm with your consultant",
     "Developer approval first; get Emaar's current design guidelines and review process, and programme the review before the permit"),
    ("Arabian Ranches", "Dubai", "Emaar NOC", "Confirm with your consultant",
     "Emaar NOC for extensions and external works before any authority permit"),
    ("Dubai Hills Estate", "Dubai", "Emaar with Meraas", "Confirm with your consultant",
     "Developer approval first; get the current guidelines and NOC process for your sub-community from the developer"),
    ("Jumeirah Bay Island", "Dubai", "Meraas (Dubai Holding)", "Confirm with your consultant",
     "Developer approval first; get the current guidelines and NOC process from Meraas"),
    ("District One, MBR City", "Dubai", "Meydan Sobha", "Confirm with your consultant",
     "Developer approval first; get the current guidelines and NOC process from Meydan Sobha"),
    ("Al Barari", "Dubai", "Al Barari", "Confirm with your consultant",
     "Developer approval first; get the current guidelines and NOC process from Al Barari"),
    ("Saadiyat Island", "Abu Dhabi", "Aldar",
     "Abu Dhabi municipality through TAMM, under DMT regulations",
     "Developer approval first, then the municipality building permit through TAMM; under DMT's 2025 rules some minor works follow a quicker route"),
    ("Hudayriyat Island", "Abu Dhabi", "Modon", "Abu Dhabi municipality through TAMM, under DMT regulations",
     "Modon's plot requirements first, then the municipality permit; DMT's 2025 private-villa rule changes apply"),
]


def llms_lines(article_url):
    """Compact Markdown section for llms-full.txt."""
    out = ["## Which authority covers a villa: location, authority, programme effect", "",
           f"Source article: {article_url}", "", f"Rule: {RULE}", "",
           "| Area | Emirate | Master developer (first approval) | Permit authority | What it changes for your programme |",
           "|---|---|---|---|---|"]
    out += [f"| {a} | {e} | {d} | {p} | {w} |" for a, e, d, p, w in AUTHORITY_TABLE]
    out += ["", "Eastbridge covers every community in Dubai and Abu Dhabi; these rows are examples, not limits. "
            "Eastbridge is a client-side project manager: the owner's registered consultant prepares and submits "
            "the applications and confirms which authority covers the plot."]
    return out
