#!/bin/sh
# Regenerates the right-to-left stylesheet used by the Arabic pages. Run after editing site.css.
# Needs Node: npx rtlcss@4.3.0
cd "$(dirname "$0")/.." && npx --yes rtlcss@4.3.0 src/static/assets/site.css src/static/assets/site-rtl.css && cat >> src/static/assets/site-rtl.css <<'X'
/* RTL extras */
.hero::after{background:linear-gradient(270deg,rgba(10,14,16,.74) 0%,rgba(10,14,16,.42) 42%,rgba(10,14,16,.05) 78%),linear-gradient(180deg,rgba(10,14,16,.45) 0%,rgba(10,14,16,0) 22%,rgba(10,14,16,0) 58%,rgba(10,14,16,.62) 100%)}
[dir="rtl"] .chart,[dir="rtl"] .triad,[dir="rtl"] .chart *{direction:ltr}
[dir="rtl"] a[href^="tel:"],[dir="rtl"] a[href^="mailto:"]{direction:ltr;unicode-bidi:isolate}
@media (max-width:1100px){[dir="rtl"] .nav{inset:0 auto 0 0}}
X
