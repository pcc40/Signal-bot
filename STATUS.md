# Eastbridge: where we are (single status file)

**Purpose.** One file that every session, scheduled task and Master Control sweep reads first, so they all know the current state of the Eastbridge business and website. It lives at the root of `pcc40/eastbridge-website` (branch `main`).
Raw URL for Master Control: `https://raw.githubusercontent.com/pcc40/eastbridge-website/main/STATUS.md` (if the repo is private, read it with the GitHub connector or `gh`).

**Who updates it.**
- The daily SEO engine updates the *Website* and *SEO* sections on each run.
- Any Code session that changes the site or sends outreach updates the relevant section and the *Last updated* line.
- Master Control does not edit this file. It mirrors it into tracker B7 (see the last section).

Last updated: 11 November 2026, daily SEO engine (Wednesday checks only, no article; audit 0/0, all live checks 200).

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
| Size | 92 pages × 5 languages (English, Arabic, Russian, Chinese, Hindi) = 460 URLs, all returning 200. 28 insight articles (latest: /insights/emaar-community-villa-renovation/, 10 Nov). 4 tools: cost calculator, renovate or rebuild, stage payment planner, delay cost estimator. 2 free PDF guides. 14 service pages. 12 area pages. |
| Brand | Keystone-arch logo (chosen 5 Nov). The Outlook signature is in `business/email-signature.html`. |
| Images | UAE developer images, with credits, on area pages and place-based articles. The "Built by our founder in the UK" strip of Cornish houses appears on home, area, service and article pages. |
| Checks | `python3 build.py && python3 tools/i18n.py apply && python3 tools/seo_audit.py` must report 0 errors and 0 warnings. Last run: 500 pages, 0/0 (11 Nov). |
| Forms | Netlify Forms: `brief` (contact), `estimate`, `checklist` and `notes`. Only the English pages register the forms. Success events fire only on the thank-you pages. There is a cookie banner, and GA4 runs only after the visitor consents. |
| Rules | See `src/content/WRITING_BRIEF.md` and `HANDOFF.md`:<br>• never supervise, certify, turnkey or "on your behalf"<br>• no UAE projects or clients claimed<br>• no architect names, no turnover, no team names<br>• Island E is hypothetical |

## 3. SEO and automation
| Item | State |
|---|---|
| Daily SEO engine | Scheduled task "Eastbridge SEO engine", 06:38 Dubai daily, playbook `AUTOMATION.md`. It publishes 3 articles a week (Tuesday, Thursday and Saturday), deepens one page every Monday and adds a new area page every second Monday, and writes the visibility log in `reports/visibility.csv`. |
| Indexing | Google first showed impressions on 3 Nov 2026; Search Console, 7 days to 8 Nov: 1 click, 29 impressions, average position 22.3 (queries incl. villa renovation cost dubai, villa renovation emirates hills, villa construction cost; first Russian query); request indexing 10 Nov for Emaar article, Jumeirah Bay, ru Hudayriyat, zh FAQ; page indexing (11 Nov): 452 indexed, 8 not — 1 noindex (calculator embed, intended), 1 canonical alternate (contact ?area= link, intended), 4 crawled-not-indexed (ar/ru renovation guide, hi timeline, feed.xml), 2 discovered (ru Hudayriyat, zh FAQ). Sitemap resubmitted 9 Nov. GA4 6–7 Nov: first Google organic visits (3) and first ChatGPT referral (1). Search Console is verified (GSC_VERIFICATION in `src/config.py`). The sitemap has 460 URLs and 215 image entries. IndexNow resubmitted all 460 URLs on 6 Nov. |
| LinkedIn | Company pages live 10 Nov: Eastbridge (/company/eastbridge-strategic-partners/, in SOCIAL sameAs) and DealDeed (/company/dealdeed/). Personal-profile posts now carry the link in the first comment (scheduled task adds it at 09:04 UK). |
| Analytics | GA4 G-120XT9N6XB, consent-gated. **Phil to do:** in GA4, unmark `generate_lead` and mark `enquiry_success` as the key event. |
| Next topics | See `src/content/TOPICS.md` (top of the backlog). Next article Thu 12 Nov (first unticked topic). |
| AI visibility | 40 fixed buyer prompts in `reports/ai-visibility/` (method and weekly Claude Desktop prompt in its README). Baseline 7 Nov 2026, web-search proxy only: Eastbridge in 0 of 40; Tanmu named in 25 of 40. AI platforms (ChatGPT, Gemini, Perplexity, Google AI Mode) are run by Claude Desktop every Sunday from 8 Nov; the SEO engine reruns the proxy every Monday and adds monthly rates to section 8. |

## 4. Outreach (partner referrals)
Emails are sent from philip@eastbridgestrategicpartners.com through Bird (sending domain verified 5 Nov: DKIM, DMARC, return path). Each email is BCC'd to Philip, and replies arrive in his Eastbridge Outlook.

| Batch | Sent | Result | Files |
|---|---|---|---|
| 1 | Late Oct, sent by Phil | 8 firms (ANARCHITECT, CK, SAOTA, Bluehaus, Kat Black, Shawa, Unique Properties, Hadef) | `business/outreach-drafts-ready.md` |
| 2 | 5 Nov 2026, 20:31 UTC | 20 sent; Galadari bounced (spam filter), the rest delivered or retrying | `business/outreach-batch-2.md`, `business/outreach-batch-2-log.md` |
| 3 | 6 Nov 2026, 07:16 UTC | 23 sent, 23 delivered (architecture and design firms from the research doc) | `business/outreach-batch-3.md`, `business/outreach-batch-3-log.md` |
| 4 | 6 Nov 2026 (#1–2); 9 Nov 2026, 03:45 UTC (#3–20) | 20 sent, 20 delivered (Abu Dhabi studios and agents, Dubai villa agencies, relocation and private-client advisers, Dubai studios, QS) | `business/outreach-batch-4.md`, `business/outreach-batch-4-log.md` |
| 5 | 9 Nov 2026, 03:52 UTC | 7 sent, 7 delivered (construction law, landscape and pool, UK interiors with Dubai villas, relocation) | `business/outreach-batch-5.md`, `business/outreach-batch-5-log.md` |
| 6 | 10 Nov 2026 | 24 sent, 24 delivered (UAE villa studios and agencies incl. Abu Dhabi; UK interiors with Dubai villas; wealth, family office, relocation; law; QS; landscape and pool). Primo Capital dropped on Phil's instruction (do not contact) | `business/outreach-batch-6a.md`, `business/outreach-batch-6b.md`, `business/outreach-batch-6-log.md` |
| 7 | 11 Nov 2026 | 49 sent, 49 delivered, no BCC. **First short-style batch** (55–85 words, no link, one question) for comparing reply rates with batches 2–6. UAE studios and agencies, UK practices, wealth and family offices, law, QS, landscape, mortgage brokers, holiday-home operators, smart-home and lighting, kitchens, inspectors | `business/outreach-batch-7a.md`, `7b.md`, `7c.md`, `business/outreach-batch-7-log.md` |

**Totals (11 Nov):** 151 firms contacted (8 by Phil, 143 via Bird); 1 bounce (Galadari); 2 replies (Aparna Kaushik, not now; Fedari, partnership and a possible Al Barari introduction). Daily runs continue to Fri 13 Nov at up to 50 firms a day, no BCC, short style.

**Follow-ups:** created as Outlook drafts by the Claude Desktop chat (Chrome), as replies to Phil's BCC copies. Phil reviews and sends them. They go only to firms that have not replied, bounced or opted out.
| Batch | Day-4 drafts | Day-10 (final) drafts |
|---|---|---|
| 2 | Mon 9 Nov, 09:20 Dubai | Mon 16 Nov, 09:20 Dubai |
| 3 | Tue 10 Nov, 09:20 Dubai | Mon 16 Nov, 09:20 Dubai |
| 4 and 5 | Fri 13 Nov (not yet scheduled) | Thu 19 Nov (not yet scheduled) |
| 6 | Mon 16 Nov (not yet scheduled) | Fri 20 Nov (not yet scheduled) |
| 7 | Mon 16 Nov, via Bird (no BCC copies; not yet scheduled) | Fri 20 Nov, via Bird (not yet scheduled) |

**Replies so far:**
- 6 Nov: **Aparna Kaushik Design Group** (batch 2, #2). Polite holding reply from Nupur Kapoor, EA to Ms. Kaushik: they will review and come back if there is an opportunity. Status: *replied, not now*. No follow-ups; one light check-in in about three months (early Feb 2027).
- 11 Nov: **Fedari Building Inspection** (batch 7, #47, short style). Khalid Gaddur, Managing Director, phoned and then emailed the same day: wants a two-way referral partnership and mutual website listings, and mentioned a possible introduction to an owner in Al Barari planning a small renovation. Status: *warm, first possible project*. Reply drafted 11 Nov (no referral fees either way; our listing details sent; asks for theirs and for the Al Barari introduction). To do once Fedari sends its logo and text: add a Fedari listing to the website. No follow-up emails to Fedari from the sequence.
**Next batch:** the daily run (07:41 Dubai, Tue 10 – Fri 13 Nov) researches and sends up to 25 new firms a day, excluding everyone above.

## 5. Open items for Phil
1. Google Business Profile: finish verification (copy is in `business/offsite-authority-kit.md`).
2. GA4 key event: switch to `enquiry_success`.
3. Lawyer review of the privacy notice and opt-in wording.
4. Decision D8: may we use the wording "we take no commissions from contractors, consultants or suppliers on your project"?
5. Search Console: request indexing for the new key pages.
6. Send test submissions from the contact, estimate and checklist forms, and check that each arrives in Netlify Forms and by email.
7. Native-speaker check of the Russian and Chinese place names.
8. Create the third-party profiles in `business/authority-profiles.md` (LinkedIn page, Bing Places, Apple Business, Houzz, 2GIS, Yellow Pages UAE first) The three press pitches in its section 10 were SENT on 7 Nov 2026 (Construction Week to julianne.tolentino@itp.com cc shehzin.shaikh@itp.com; Gulf News readers@; Khaleej Times letters@ cc news@). One follow-up each on 14 Nov if no reply, then stop.
9. Start the weekly AI visibility run: paste the prompt in `reports/ai-visibility/README.md` (section 3) into Claude Desktop each Sunday.
10. Quay House case study: send the facts (scope, dates, role of P Chapman Construction, authorised photographs) so it can be written.

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
4. Feeds master line for B7 (40 words or fewer): "Eastbridge: site live; 151 partner firms contacted (1 bounce); 50 a day to 13 Nov; follow-up drafts 9, 10 and 16 Nov; replies: 1 (Aparna Kaushik, not now). Next: Phil sends follow-ups, answer replies within a day, verify the Google Business Profile."

## 8. 30/60/90-day plan and KPIs
Set 7 November 2026 from the AI search visibility audit (items 1, 2, 4 and 5 approved by Phil). **Targets are goals, not claims or forecasts.** Baselines are what was measured or known on 7 November 2026; "not measured" means nobody has the number yet, not zero.

**Milestones**
| By | Milestones |
|---|---|
| **7 Dec 2026 (30 days)** | Google Business Profile verified. LinkedIn company page, Bing Places and Apple Business live (copy in `business/authority-profiles.md`). Weekly AI visibility runs started on all four AI platforms (first run 8 Nov). Three press pitches sent (Construction Week, Gulf News, Khaleej Times). GA4 key event switched to `enquiry_success` and one labelled test enquiry seen end to end. Quay House facts received from Phil. Search Console baseline recorded in this table. |
| **6 Jan 2027 (60 days)** | Houzz, 2GIS, Yellow Pages UAE and ProTenders live; Meydan FZ asked about a listing; decision on Dubai Chambers and British Chamber membership. Quay House case study published (P Chapman Construction's UK work, clearly labelled). At least one press piece or quoted comment published. Second outreach follow-up round complete. Monthly AI rates added below for November and December. |
| **5 Feb 2027 (90 days)** | All section 9 profiles in `authority-profiles.md` live and listed in `SOCIAL`. Second press piece. Three months of weekly AI data, with the trend reported per platform. Review which prompts still show no Eastbridge mention and plan content for them (Island E, Saadiyat, stalled projects and fees were open gaps in the baseline). |

**KPIs**
| KPI | Source | Baseline (7 Nov 2026) | Goal by 7 Dec | Goal by 6 Jan | Goal by 5 Feb |
|---|---|---|---|---|---|
| Search Console impressions (28 days) | GSC, Performance | Not measured in this session; first impressions seen 3 Nov | Record baseline | 2x the 7 Dec figure | 4x the 7 Dec figure |
| Non-branded clicks (28 days; queries without "eastbridge") | GSC, Performance, query filter | Not measured | Record baseline | 10 | 30 |
| Enquiries (`enquiry_success` events) | GA4 (after the key-event switch) | 0 recorded; no client yet | Tracking verified | 2 cumulative | 5 cumulative |
| Outreach replies | `business/outreach-batch-*-log.md`, section 4 | 53 emails sent (1 bounce), 1 reply (not now) | 4 replies | 8 replies | 12 replies |
| Outreach meetings or calls held | Outlook / diary | 0 | 1 | 3 | 5 |
| AI mention rate, 40 prompts, per platform | `reports/ai-visibility/tracking.csv` | web_search_proxy 0/40 (0%); ChatGPT, Gemini, Perplexity, Google AI Mode: first run 8 Nov | Baselines recorded on all four AI platforms; proxy at least 2/40 | At least 4/40 (10%) on two or more platforms | At least 8/40 (20%) on two or more platforms |
| AI recommendation rate, per platform | same | web_search_proxy 0/40 (0%) | Baselines recorded | At least 1/40 on one platform | At least 4/40 (10%) on one platform |
| AI citation rate (link to our site), per platform | same | web_search_proxy 0/40 (0%) | Baselines recorded | At least 2/40 on one platform | At least 4/40 (10%) on two platforms |
| Live third-party profiles | tracker in `business/authority-profiles.md` | 1 (Instagram) | 4 | 8 | 10 |
| Press pieces published or quoted | links logged here | 0 | 3 pitches sent | 1 | 2 |
| Google Business Profile verified | GBP dashboard | No | Yes | Yes | Yes |
| Quay House case study published | site | No (pending Phil's facts) | Facts received | Published | Published |

**Monthly AI rates** (added by the SEO engine on the first run of each month; see `AUTOMATION.md` step 10a)
| Month | Platform | Runs | Mention | Recommendation | Citation |
|---|---|---|---|---|---|
| Nov 2026 (baseline, 7 Nov) | web_search_proxy | 1 | 0/40 (0%) | 0/40 (0%) | 0/40 (0%) |
