# Translation review task

You are a senior native-level reviewer. A premium Dubai villa project-management website (Eastbridge Strategic Partners) was translated from English. The HOME page is already reviewed. You review a list of other pages in ONE language.

Read first: /home/claude/eastbridge/src/i18n/TRANSLATION_BRIEF.md (glossary, format and compliance rules).

Data:
- English segments: /home/claude/eastbridge/src/i18n/segments.json  {key: English}
- Translations: /home/claude/eastbridge/src/i18n/<lang>.json  {key: translation}  (READ ONLY for you)
- Rendered pages: /home/claude/eastbridge/dist/<path>index.html (English) and /home/claude/eastbridge/dist/<lang>/<path>index.html.
  To map page text to keys, use: python3 -c "import sys; sys.path.insert(0,'/home/claude/eastbridge/tools'); import i18n" and
  i18n.segments_of(soup) / i18n.inner(node) / i18n.key(text) on the ENGLISH page (bs4 is installed). Also check <title>, meta description and alt text.

Look for what a native high-net-worth reader would notice: wrong meaning, omissions, machine-sounding calques, wrong tense, wrong register,
inconsistent glossary terms, grammar, punctuation, numbers/currency that differ from English, and the idiom "your side of the table"
(must mean "on your side, representing you", never a literal table). Compliance: Eastbridge is never an engineer, architect, contractor or
design consultant; never claims UAE projects or clients; the Island E case study stays clearly illustrative. Fix genuine problems only; do not
rewrite good copy for taste.

Output: write ONLY your fixes to /home/claude/eastbridge/src/i18n/fixes/<lang>-<group>.json as {key: corrected full translation}, keeping
every HTML tag and attribute exactly as in the English segment, valid JSON (python json.dump, ensure_ascii=False). Edit no other file.
Then reply with: number of fixes, the 5 most important (English gist -> new), and a one-line quality verdict.
