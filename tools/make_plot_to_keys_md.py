#!/usr/bin/env python3
"""Write Phil's plain Markdown review copy of the plot-to-keys guide from src/content/plot_to_keys.py.
Usage: python3 tools/make_plot_to_keys_md.py   -> business/plot-to-keys-guide-review-copy.md"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "src"))
from content import plot_to_keys as G
out = ROOT / "business" / "plot-to-keys-guide-review-copy.md"
out.write_text(G.markdown_copy(), encoding="utf-8")
print(f"{out.relative_to(ROOT)}: {G.N_STAGES} stages, {G.N_DECISIONS} decisions, {len(G.sources())} sources")
