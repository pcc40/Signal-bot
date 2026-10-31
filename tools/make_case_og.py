"""Build the social-preview card for the Island E worked example (1200 x 630 PNG).

The card shows the indicative plan and section diagram with the label "Hypothetical worked example",
so the preview never shows a photo of a finished house next to the Island E title (review brief, section 1).
Run after changing case_island_e.svg_site():  python3 tools/make_case_og.py
Needs Google Chrome (headless) on the PATH as google-chrome."""
import pathlib, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import content.case_island_e as CS  # noqa: E402

OUT = ROOT / "src/static/assets/img/island-e-worked-example-og.png"
FONTS = (ROOT / "src/static/assets/fonts").as_uri()

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:"Instrument Serif";src:url({FONTS}/iserif-400.woff2) format("woff2")}}
@font-face{{font-family:"Instrument Sans";src:url({FONTS}/instrument-500.woff2) format("woff2");font-weight:500}}
html,body{{margin:0;width:1200px;height:630px;background:#F2F0EB;color:#151C1F;font-family:"Instrument Sans",Arial,sans-serif;overflow:hidden}}
.card{{box-sizing:border-box;width:1200px;height:630px;padding:48px 64px;display:flex;flex-direction:column}}
.top{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid rgba(21,28,31,.18);padding-bottom:18px}}
.wm{{font-family:"Instrument Serif",Georgia,serif;font-size:34px}}
.tag{{font-size:20px;letter-spacing:.14em;text-transform:uppercase;color:#7A5C2C;font-weight:500}}
h1{{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:52px;line-height:1.05;margin:26px 0 6px}}
p{{margin:0;font-size:22px;color:#4A5357}}
.fig{{flex:1;display:flex;align-items:flex-end;justify-content:center;margin-top:14px}}
svg{{width:760px;height:auto}}
.plot{{fill:#E4E1D9;stroke:#4A5357}} .water{{fill:#2F6A8A;opacity:.35}} .house{{fill:#26343A}} .pool{{fill:#2F6A8A;opacity:.6}}
.base{{fill:#E4E1D9;stroke:#4A5357;stroke-dasharray:4 3}} .ground{{stroke:#151C1F;stroke-width:1.5}} .limit{{stroke:#7A5C2C;stroke-dasharray:6 4}}
.lab{{font-size:14px;fill:#151C1F}} .tick{{font-size:12px;fill:#4A5357}} .lab-inv{{font-size:14px;fill:#fff}} .tick-inv{{font-size:12px;fill:#E4E1D9}}
</style></head><body><div class="card">
<div class="top"><span class="wm">Eastbridge Strategic Partners</span><span class="tag">Hypothetical worked example</span></div>
<h1>How we would manage an Island E villa</h1>
<p>A worked project example, not a completed project. Indicative plan and section under draft controls.</p>
<div class="fig">{CS.svg_site()}</div></div></body></html>"""

def main():
    with tempfile.TemporaryDirectory() as d:
        src = pathlib.Path(d) / "card.html"
        src.write_text(HTML, encoding="utf-8")
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        f"--screenshot={OUT}", "--window-size=1200,630", "--force-device-scale-factor=1",
                        src.as_uri()], check=True, capture_output=True)
    print("wrote", OUT.relative_to(ROOT))

if __name__ == "__main__":
    main()
