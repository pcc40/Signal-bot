# AI visibility tracking: method and weekly routine

Started 7 November 2026. This folder measures whether AI assistants and AI search mention, recommend and cite Eastbridge Strategic Partners when a villa owner asks a normal, non-branded question. It answers item 5 of the AI search visibility audit (6 November 2026): "there is no baseline from repeatable testing on multiple assistants".

Files:

| File | What it is |
|---|---|
| `prompts.csv` | The 40 fixed buyer prompts (`id, prompt, intent, segment`). Never reword a prompt. If a prompt has to change, retire its id and add a new one (P41 onwards), so old results stay comparable. |
| `tracking.csv` | One row per prompt, per platform, per run. Append only. Never edit or delete old rows. |
| `README.md` | This file. |

## 1. Method

1. **Fixed prompts, same wording.** Paste each prompt exactly as written in `prompts.csv`, in a new chat, with nothing before it. Do not add "in Dubai" or "please", do not name Eastbridge, and do not ask follow-up questions.
2. **Logged out where possible.** Use each platform logged out, or in its private/temporary mode, so past chats and memory do not shape the answer. Where a platform needs a login, use the account that is already signed in on the Mac, switch off memory/personalisation if the setting is there, and note the mode in the `mode` column. Never create or log in to a new account for this.
3. **Location: UAE.** Run from the Mac in Dubai, with no VPN. Do not tell the assistant where you are.
4. **Cadence.** Weekly, on Sundays, for `chatgpt`, `gemini`, `perplexity` and `google_ai_mode` (Claude Desktop in Chrome). Weekly, on Mondays, for `web_search_proxy` (the daily SEO engine). `claude` is optional and monthly (first Sunday): a fresh claude.ai chat with web search on.
5. **One answer per prompt.** Record the first answer only. Do not regenerate.
6. **Record what is on the screen, nothing else.** If an answer is ambiguous, mark `N` and explain in `notes`. Never guess a position.

### Platforms (`platform` column)

| Value | What it is | Typical `mode` value |
|---|---|---|
| `web_search_proxy` | The Code/SEO engine's WebSearch tool (a US-based web index that returns links plus a short synthesised answer). **This is a proxy, not an AI assistant answer.** It shows whether the pages AI answers draw on include ours. | `websearch_tool_us_index` |
| `chatgpt` | chatgpt.com | `logged_out`, `temporary_chat`, or `logged_in_memory_off` |
| `gemini` | gemini.google.com | `logged_out` or `logged_in_activity_off` |
| `perplexity` | perplexity.ai | `logged_out` or `logged_in` |
| `google_ai_mode` | google.com, "AI Mode" tab (or the AI Overview at the top of ordinary results, if AI Mode is not offered; say which in `mode`) | `ai_mode` or `ai_overview` |
| `claude` | claude.ai with web search on | `logged_in_new_chat` |

### Columns (`tracking.csv`)

| Column | Meaning |
|---|---|
| `date` | Date the prompt was run, `YYYY-MM-DD`. |
| `platform` | One of the six values above. |
| `mode` | How it was run (see table). Keep it the same week to week. |
| `prompt_id` | `P01` to `P40`, from `prompts.csv`. |
| `eastbridge_mentioned` | `Y` if the answer names "Eastbridge" or "Eastbridge Strategic Partners" anywhere (text, list, source card or link). Otherwise `N`. |
| `eastbridge_recommended` | `Y` only if the answer puts Eastbridge forward as an option for the user to consider or contact (in a list of firms, as "you could speak to…", and so on). A passing mention, or citing our article only for a fact, is `N`. |
| `position` | Where a list of firms is given and Eastbridge is in it, its place in that list (`1` = first). `-` if not listed or if the answer has no list. For `web_search_proxy`, the rank of the first eastbridgestrategicpartners.com result among the returned links, or `-`. |
| `eastbridge_cited` | `Y` if a link or source card points to eastbridgestrategicpartners.com. |
| `url_shown` | The Eastbridge URL that was linked or cited (first one), otherwise blank. |
| `competitors_named` | Firms the answer names or links, separated by `;`. Always check for: Project Wizards, Tanmu, NU Projects, DNA Project Management, NEXTSTEP, Bauhaus Project Management, PRASOON, Capital Associated, Real Estate Club Dubai. Write `(none)` if no firm is named. |
| `notes` | Anything that helps later: "answer said no fee benchmark exists", "only law firms named", "cited our fees page for a fact". Keep it short. Put commas inside quotes. |

### How to compute the rates

Compute every rate **per platform and per run date**, never pooled across platforms, and keep the three rates separate:

- **Mention rate** = rows with `eastbridge_mentioned = Y` ÷ prompts run (normally 40).
- **Recommendation rate** = rows with `eastbridge_recommended = Y` ÷ prompts run.
- **Citation rate** = rows with `eastbridge_cited = Y` ÷ prompts run.
- **Average position when listed** = mean of `position` over rows where it is a number (report with how many rows it is based on).
- **Competitor share** (optional) = for each competitor, prompts where it is named ÷ prompts run.
- **Overall share of prompts** (for the monthly STATUS.md line only) = prompts where Eastbridge was mentioned on at least one AI platform that week ÷ 40. Exclude `web_search_proxy` from this figure.

A one-line way to compute them in the repository:

```
python3 - <<'EOF'
import csv, collections
rows = list(csv.DictReader(open('reports/ai-visibility/tracking.csv')))
g = collections.defaultdict(list)
for r in rows: g[(r['date'], r['platform'])].append(r)
for (d, p), rs in sorted(g.items()):
    n = len(rs); f = lambda c: sum(r[c] == 'Y' for r in rs)
    print(f"{d} {p:17} n={n:2}  mention {f('eastbridge_mentioned')/n:4.0%}  recommend {f('eastbridge_recommended')/n:4.0%}  cite {f('eastbridge_cited')/n:4.0%}")
EOF
```

## 2. Baseline (7 November 2026, `web_search_proxy` only)

All 40 prompts were run through the Code session's WebSearch tool. **This is a web-search proxy, not an AI assistant answer.**

- Eastbridge mentioned: **0 of 40** (0%). Recommended: 0 of 40. Cited: 0 of 40. No eastbridgestrategicpartners.com URL appeared in any result list. A further check for "eastbridgestrategicpartners.com client-side project manager" also returned nothing from the site, which suggests this index has not yet picked up the domain.
- Firms named most often: **Tanmu** (Tanmu Project Management Services, served from `tanmu-website.pages.dev`) in 25 of 40; Capital Associated (a design-build contractor's blog) in 13; Real Estate Club Dubai in 8; Rady Interior in 6; Algedra in 5; Prime Project Partners in 4; Kayrouz & Associates (law firm) in 4.
- Not seen at all: Project Wizards, DNA Project Management, NU Projects, NEXTSTEP.
- Open gaps (no client-side firm named at all): P13, P14, P19 (Island E), P21 (Saadiyat), P24 (British owner), P30 (extension of time), P31 to P33 (stalled projects). P39 and P40 (fees): no firm publishes a fee; the only figure surfaced was a contractor blog's "3 to 8% of construction value".

The first AI-platform baseline (ChatGPT, Gemini, Perplexity, Google AI Mode) is the owner's first Sunday run, 8 November 2026.

## 3. Weekly prompt for Claude Desktop (Chrome), every Sunday

Paste this into a new Claude Desktop chat on the Mac, with Claude in Chrome enabled. It is written to run unattended, but Phil should glance at the summary at the end.

```
Weekly AI visibility check for Eastbridge Strategic Partners (eastbridgestrategicpartners.com). Today is Sunday; use today's date in YYYY-MM-DD form.

Rules:
- Use Chrome. Never create an account, never log in to any site you are not already logged in to, never enter a password, never accept a paid plan. If a platform demands a login that is not already in place, skip that platform and say so.
- Use each platform logged out, or in its private/temporary mode where offered (ChatGPT: Temporary Chat; Gemini: logged out if possible; Perplexity: logged out; Google: the "AI Mode" tab on google.com, or the AI Overview if AI Mode is not shown). Record the mode you used.
- Do not use a VPN and do not tell any assistant where you are.

Steps:
1. Open https://github.com/pcc40/eastbridge-website/blob/main/reports/ai-visibility/prompts.csv and read the 40 prompts (id, prompt). Also read reports/ai-visibility/README.md, section 1, for the column rules.
2. For each platform in this order: chatgpt, gemini, perplexity, google_ai_mode. For each prompt P01 to P40: open a new chat (or a new search), paste the prompt text exactly, wait for the full answer, and record one row:
   date,platform,mode,prompt_id,eastbridge_mentioned,eastbridge_recommended,position,eastbridge_cited,url_shown,competitors_named,notes
   - eastbridge_mentioned: Y if "Eastbridge" appears anywhere in the answer or its sources, else N.
   - eastbridge_recommended: Y only if Eastbridge is put forward as a firm to consider or contact.
   - position: Eastbridge's place in any list of firms (1 = first), else "-".
   - eastbridge_cited: Y if any link or source card points to eastbridgestrategicpartners.com; url_shown = that URL.
   - competitors_named: every firm named or linked, separated by ";" (watch for Project Wizards, Tanmu, NU Projects, DNA Project Management, NEXTSTEP, Bauhaus, PRASOON, Capital Associated, Real Estate Club Dubai), or "(none)".
   - notes: one short phrase. Wrap any field containing a comma in double quotes.
   Do not regenerate answers, do not ask follow-ups, do not guess. If a platform errors or rate-limits, note it and carry on.
3. Append all rows (up to 160) to reports/ai-visibility/tracking.csv in the GitHub repository pcc40/eastbridge-website, branch main, using the GitHub web editor only if I am already signed in to GitHub in Chrome: open the file, click the pencil (Edit), paste the rows at the end without changing any existing line, and commit directly to main with the message "AI visibility: week of <date>". If you cannot edit on GitHub, do not try to sign in: put all rows in one plain-text code block in your reply so I can paste them into the Claude Code session.
4. Finish with a short summary table, one line per platform: prompts run, mention rate, recommendation rate, citation rate (each as count and %), Eastbridge URLs cited, and the three competitors named most often. Then list any prompt where Eastbridge was recommended, and any prompt where a platform said something about Eastbridge that is wrong (for example, claims of UAE projects, a fee we do not charge, or the word "supervise"); those need correcting on the site.

If the run is too long for one session, do two platforms today and two tomorrow, and say so in the summary.
```

If the Desktop chat pastes rows back instead of committing them, the next Code session (or the SEO engine's Monday run) appends them to `tracking.csv` unchanged and commits with the same message.
