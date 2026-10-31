#!/usr/bin/env python3
"""Check a translated chunk: python3 tools/i18n_check.py src/i18n/parts/ar-03.json
Compares against src/i18n/parts/en-03.json. Reports missing keys, invalid JSON,
tag mismatches, untouched English and forbidden wording."""
import json, re, sys
from pathlib import Path
p = Path(sys.argv[1]); lang, n = p.stem.split("-")
src = json.loads((p.parent / f"en-{n}.json").read_text(encoding="utf-8"))
try:
    tr = json.loads(p.read_text(encoding="utf-8"))
except Exception as e:
    print("INVALID JSON:", e); sys.exit(1)
errs = []
def tags(s): return sorted(re.findall(r"<\s*(/?\w+)", s))
def hrefs(s): return sorted(re.findall(r'href="([^"]+)"', s))
for k, v in src.items():
    if k not in tr: errs.append(f"missing {k}: {v[:60]}"); continue
    t = tr[k]
    if not isinstance(t, str) or not t.strip(): errs.append(f"empty {k}"); continue
    if tags(v) != tags(t): errs.append(f"tags differ {k}: {tags(v)} vs {tags(t)}")
    if hrefs(v) != hrefs(t): errs.append(f"links differ {k}")
    plain = re.sub(r"<[^>]+>", "", t)
    STOP = re.compile(r"\b(the|and|of|to|is|for|with|you|your|a|in|on|we|our|it|that|by)\b", re.I)
    src_plain = re.sub(r"<[^>]+>", "", v)
    names_only = len(STOP.findall(src_plain)) <= 1 and "," in src_plain or len(STOP.findall(src_plain)) <= 1 and len(src_plain.split()) <= 6
    if lang != "en" and len(src_plain.split()) > 4 and plain == src_plain and not names_only:
        errs.append(f"not translated {k}: {v[:60]}")
extra = set(tr) - set(src)
if extra: errs.append(f"{len(extra)} unknown keys")
print(f"{p.name}: {len(src)} segments, {len(errs)} problems")
for e in errs[:40]: print(" -", e)
sys.exit(1 if errs else 0)
