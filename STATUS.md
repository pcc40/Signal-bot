# Eastbridge: where we are (single status file)

**Purpose.** One file that every session, scheduled task and Master Control sweep reads first, so they all know the current state of the Eastbridge business and website. It lives at the root of `pcc40/eastbridge-website` (branch `main`).
Raw URL for Master Control: `https://raw.githubusercontent.com/pcc40/eastbridge-website/main/STATUS.md` (if the repo is private, read it with the GitHub connector or `gh`).

**Who updates it.**
- The daily SEO engine updates the *Website* and *SEO* sections on each run.
- Any Code session that changes the site or sends outreach updates the relevant section and the *Last updated* line.
- Master Control does not edit this file. It mirrors it into tracker B7 (see the last section).

Last updated: 6 November 2026, by the Code session (website build and outreach).

---

## 1. Business in one paragraph
Eastbridge Strategic Partners L.L.C-FZ (Meydan Free Zone licence 2540153.01) is an independent client-side project manager and owner's representative for one-off private villas in Dubai and Abu Dhabi. Philip Chapman leads every appointment and is supported by three project managers. He was previously founder of P Chapman Construction, a UK builder, for 21 years.
- **Fees:** Review AED 9,500–15,000 per review. Part service is a monthly fee agreed in the written scope, with no published minimum. Full service is typically 1.75–3% of build cost. No day rate, hourly rate or fixed price is published.
- **Contact:** philip@eastbridgestrategicpartners.com · +971 56 744 0057 · https://eastbridgestrategicpartners.com
- **Status:** no client yet. The priority is winning the first appointment.

## 2. Website (live)
| Item | State |
|---|---|
| Live site | https://eastbridgestrategicpartners.com. The .ae and www addresses redirect to it with a 301, and so does the old Netlify preview address. |
| Code | `pcc40/eastbridge-website`, branch `main`. Netlify builds every push automatically (Python 3.11). Backup copy: `pcc40/Signal-bot`, branch `claude/eastbridge-website-automation-veh823`. |
| Size | 92 pages × 5 languages (English, Arabic, Russian, Chinese, Hindi) = 460 URLs, all returning 200. 26 insight articles. 4 tools: cost calculator, renovate or rebuild, stage payment planner, delay cost estimator. 2 free PDF guides. 14 service pages. 12 area pages. |
| Brand | Keystone-arch logo (chosen 5 Nov). The Outlook signature is in `business/email-signature.html`. |
| Images | UAE developer images, with credits, on area pages and place-based articles. The "Built by our founder in the UK" strip of Cornish houses appears on home, area, service and article pages. |
| Checks | `python3 build.py && python3 tools/i18n.py apply && python3 tools/seo_audit.py` must report 0 errors and 0 warnings. Last run: 490 pages, 0/0. |
| Forms | Netlify Forms: `brief` (contact), `estimate`, `checklist` and `notes`. Only the English pages register the forms. Success events fire only on the thank-you pages. There is a cookie banner, and GA4 runs only after the visitor consents. |
| Rules | See `src/content/WRITING_BRIEF.md` and `HANDOFF.md`:<br>• never supervise, certify, turnkey or "on your behalf"<br>• no UAE projects or clients claimed<br>• no architect names, no turnover, no team names<br>• Island E is hypothetical |

## 3. SEO and automation
| Item | State |
|---|---|
| Daily SEO engine | Scheduled task "Eastbridge SEO engine", 06:38 Dubai daily, playbook `AUTOMATION.md`. It publishes 3 articles a week (Tuesday, Thursday and Saturday), deepens one page every Monday and adds a new area page every second Monday, and writes the visibility log in `reports/visibility.csv`. |
| Indexing | Google first showed impressions on 3 Nov 2026. Search Console is verified (GSC_VERIFICATION in `src/config.py`). The sitemap has 460 URLs and 215 image entries. IndexNow resubmitted all 460 URLs on 6 Nov. |
| Analytics | GA4 G-120XT9N6XB, consent-gated. **Phil to do:** in GA4, unmark `generate_lead` and mark `enquiry_success` as the key event. |
| Next topics | See `src/content/TOPICS.md` (top of the backlog). |

## 4. Outreach (partner referrals)
Emails are sent from philip@eastbridgestrategicpartners.com through Bird (sending domain verified 5 Nov: DKIM, DMARC, return path). Each email is BCC'd to Philip, and replies arrive in his Eastbridge Outlook.

| Batch | Sent | Result | Files |
|---|---|---|---|
| 1 | Late Oct, sent by Phil | 8 firms (ANARCHITECT, CK, SAOTA, Bluehaus, Kat Black, Shawa, Unique Properties, Hadef) | `business/outreach-drafts-ready.md` |
| 2 | 5 Nov 2026, 20:31 UTC | 20 sent; Galadari bounced (spam filter), the rest delivered or retrying | `business/outreach-batch-2.md`, `business/outreach-batch-2-log.md` |
| 3 | 6 Nov 2026, 07:16 UTC | 23 sent, 23 delivered (architecture and design firms from the research doc) | `business/outreach-batch-3.md`, `business/outreach-batch-3-log.md` |

**Follow-ups:** created as Outlook drafts by the Claude Desktop chat (Chrome), as replies to Phil's BCC copies. Phil reviews and sends them. They go only to firms that have not replied, bounced or opted out.
| Batch | Day-4 drafts | Day-10 (final) drafts |
|---|---|---|
| 2 | Mon 9 Nov, 09:20 Dubai | Mon 16 Nov, 09:20 Dubai |
| 3 | Tue 10 Nov, 09:20 Dubai | Mon 16 Nov, 09:20 Dubai |

**Replies so far:** none recorded. Update this line, or the Master Control row, when one arrives.
**Next batch:** research 30–50 more firms (Abu Dhabi studios, villa agents, family offices and relocation firms), excluding everyone above. Send about 20 a day.

## 5. Open items for Phil
1. Google Business Profile: finish verification (copy is in `business/offsite-authority-kit.md`).
2. GA4 key event: switch to `enquiry_success`.
3. Lawyer review of the privacy notice and opt-in wording.
4. Decision D8: may we use the wording "we take no commissions from contractors, consultants or suppliers on your project"?
5. Search Console: request indexing for the new key pages.
6. Send test submissions from the contact, estimate and checklist forms, and check that each arrives in Netlify Forms and by email.
7. Native-speaker check of the Russian and Chinese place names.

## 6. What can and cannot be automated (and who does it)
| Job | Done by | Notes |
|---|---|---|
| Site content, SEO, translations, IndexNow | Daily SEO engine (cloud scheduled task) | Fully automatic, pushes to `main`. |
| Sending new outreach | Code session (cloud) via Bird | Needs Phil's go-ahead per batch. |
| Reading replies and drafting answers and follow-ups | Claude Desktop on Phil's Mac (Chrome, Outlook as philip@) | The cloud cannot read the Eastbridge inbox. Desktop creates drafts; Phil sends. |
| Master Control board | Triage sweep v2 on Phil's Mac | Reads this file and mirrors it into B7 (below). |

## 7. For Master Control (Triage sweep v2): mirror into B7
On each sweep:
1. Read this file (raw URL above).
2. Update or add these B7 rows in place. Newest fact first, 300 characters or fewer, re-stamp `⟨upd⟩`.
   - "Eastbridge website": section 2 (key line: live, 460 URLs, audit 0/0, last change).
   - "Eastbridge SEO engine": section 3 (last article published, impressions or indexing news).
   - "Eastbridge outreach": section 4 (totals, replies, next follow-up date).
   - "Eastbridge open items": section 5 (count and the top item).
3. Open Outlook (philip@) in Chrome and list new replies from any firm in batches 1–3, plus any website enquiries (Netlify notifications). For each genuine reply, draft an answer in Outlook (never send) and record it in the B7 outreach row. Put follow-up draft dates in the diary.
4. Feeds master line for B7 (40 words or fewer): "Eastbridge: site live; 51 partner emails out (1 bounce); follow-up drafts 9, 10 and 16 Nov; replies: <n>. Next: Phil sends follow-ups, answer replies within a day, verify the Google Business Profile."
