# Eastbridge: business automation blueprint

Prepared 31 October 2026 for Philip Chapman. This is the operating system for Eastbridge, from the first visit to the website to the weekly report a client reads on a Thursday evening in London.

It is ordered by impact on **winning and serving the first client**. Each section says plainly what is **already built**, what **Phil needs to set up once** (with click-paths), and what then **runs by itself**.

The one thing deliberately not automated: the reply to a brief. The site promises "a personal reply from Philip within one working day". Automation makes sure nothing is missed and the enquirer hears back in seconds. The real answer still comes from Phil.

Prices and menu names are as of October 2026 and change often. Check before you pay. AED figures use the fixed peg of AED 3.6725 to USD 1.

---

## 0. At a glance

| # | Area | Already built (in this repo) | One-time setup by Phil | Then runs by itself |
|---|---|---|---|---|
| 1 | Website live and indexed | Full multilingual site, schema, sitemap, robots, llms.txt, IndexNow key file, `tools/indexnow.py` | Point domain at Netlify, link repo, Search Console, Bing, GA4 | Netlify redeploys on every push |
| 2 | Lead capture | Netlify form `brief` on /contact/ (all 5 languages), `checklist` form on /guides/villa-owner-checklist/, `notes` newsletter form in the footer, optional unticked `marketing_opt_in` box on `brief` and `checklist`, honeypot spam field, WhatsApp click-to-chat links, GA4 events `generate_lead` and `contact` (inactive until GA4 ID set) | Enable form detection, add notification email | Every submission stored by Netlify |
| 3 | Instant acknowledgement | **New:** `netlify/functions/submission-created.js` (branded reply via Resend or Postmark, optional internal alert, optional Google Sheet log); `[functions]` added to `netlify.toml` | Email provider account, verify domain, add 4–8 environment variables | Enquirer gets a branded email within seconds |
| 4 | CRM pipeline | Lead log fields defined by the function | Create Google Sheet + Apps Script (code below), or HubSpot free | Every lead lands as a row with status "New enquiry" |
| 5 | Booking link | Function and email support `BOOKING_URL` | Create a Google Calendar appointment schedule or Calendly event | Prospects book the first call themselves |
| 6 | WhatsApp Business | `wa.me` links with pre-filled text on every page | Install WhatsApp Business, profile, greeting, away message, quick replies, catalogue | Greeting and away messages fire automatically |
| 7 | Proposal, e-sign, invoice | Fee figures in `src/config.py` (hidden) | Proposal template, e-sign tool, accounting tool, payment rails, VAT position | Template proposals, e-signed letters, invoice reminders |
| 8 | Client onboarding pack | Outline below | Write once in Google Drive | Copied per client in minutes |
| 9 | Weekly client report | Template below | Set up a Google Doc or Sheet template | Filled after each site visit, sent every Thursday |
| 10 | Monthly business dashboard | KPI list below | Connect GA4, Search Console, Sheet | Reviewed on the first working day of the month |
| 11 | Daily SEO engine | `AUTOMATION.md` playbook, `tools/seo_audit.py`, `tools/i18n.py`, `tools/indexnow.py`, `reports/visibility.csv` | **Blocked:** give the Claude GitHub app access to the repo | Daily checks, two articles a week, translations, IndexNow |
| 12 | Weekly content and social engine | Articles, offsite kit (`business/offsite-authority-kit.md`) | LinkedIn page, Instagram scheduling, newsletter sender | Each article becomes posts and a monthly note |

---

## 1. Go live first (highest impact)

The competitor report (`business/seo-competitor-report.md`) found www.eastbridgepartners.ae not responding on 31 October 2026. No form, email or SEO engine helps until the domain serves the site.

**Phil, once:**

1. **Decide the canonical repository.** `HANDOFF.md` names the private repo `pcc40/eastbridge-website`. This working copy currently lives in the `Signal-bot` repository on branch `claude/eastbridge-website-automation-veh823`. Push to one, and use only that one from now on.
2. **Link Netlify to the repo.** app.netlify.com → your project → Project configuration → Build & deploy → Continuous deployment → Link repository → GitHub → choose the repo → branch `main`. Build settings come from `netlify.toml`.
3. **Domain.** Project configuration → Domain management → Add a domain → `www.eastbridgepartners.ae` (and `eastbridgepartners.ae` redirecting to www). Add the DNS records Netlify shows at your .ae registrar. Wait for the HTTPS certificate to issue.
4. **Business email.** The site publishes `enquiries@eastbridgepartners.ae`. Confirm it actually receives mail (Google Workspace or Microsoft 365). If not: workspace.google.com → Get started → use the existing domain → verify with a TXT record → add Google's MX records.
5. **Google Search Console.** search.google.com/search-console → Add property → Domain → `eastbridgepartners.ae` → add the TXT record at the registrar → Verify. Then Sitemaps → submit `https://www.eastbridgepartners.ae/sitemap.xml`. (Alternative: URL-prefix property, paste the meta code into `GSC_VERIFICATION` in `src/config.py`.)
6. **Bing Webmaster Tools.** bing.com/webmasters → Add site → Import from Google Search Console (fastest). This also feeds Copilot and ChatGPT search.
7. **GA4.** analytics.google.com → Admin → Create → Property → "Eastbridge" → Web stream → `www.eastbridgepartners.ae` → copy the Measurement ID (`G-…`) into `GA4_ID` in `src/config.py`, rebuild, push. Then Admin → Events → mark `generate_lead` as a key event. Optional: Admin → Data display → Channel groups → add a channel "AI assistants" matching sources `chatgpt.com|perplexity.ai|gemini.google.com|copilot.microsoft.com|claude.ai`.
8. **IndexNow, once live:** `python3 tools/indexnow.py --all` after a build.
9. **Google Business Profile, Bing Places, LinkedIn page:** follow `business/offsite-authority-kit.md` (copy is ready). Add every new profile URL to `SOCIAL` in `src/config.py`.

---

## 2. Lead capture (built) and Netlify setup (one-time)

**Already built**

- `brief` form on `/contact/` (and `/ar/contact/`, `/ru/contact/`, `/zh/contact/`, `/hi/contact/`): name, email, phone/WhatsApp, area, stage (multi-choice), budget band, where based, message. Honeypot field `company_site`. Redirects to `/contact/thanks/` (noindex).
- `brief` and `checklist` forms each carry an optional, **unticked** checkbox `marketing_opt_in` (value `yes`) asking for Eastbridge notes. Both forms submit normally without it.
- `checklist` form on `/guides/villa-owner-checklist/`: name, email, project stage (optional), optional notes box. Redirects to the download page `/guides/villa-owner-checklist/thanks/` (noindex).
- `notes` newsletter form in the site footer: email only. Its only purpose is the notes, so subscribing is the request; the footer says so and gives the unsubscribe route.
- WhatsApp click-to-chat links with pre-filled text (`build.py: wa_link`), phone and email links.
- GA4 events: `generate_lead` on brief submit, `contact` (method whatsapp) on WhatsApp clicks. They start recording once `GA4_ID` is set.

**Phil, once (Netlify)**

1. **Turn on form detection** (new Netlify projects have it off): app.netlify.com → project → **Forms** → **Enable form detection**. Then trigger a redeploy (Deploys → Trigger deploy → Deploy project). `brief`, `checklist` and `notes` should all appear under Forms.
2. **Internal notification** (a safety net even if everything else fails): Project configuration → Notifications → Emails and webhooks → Form submission notifications → Add notification → Email notification → event "New form submission" → form `brief` → your email. Repeat for `notes` if wanted.
3. **Spam:** Forms → Settings and usage → keep spam filtering on. Netlify's `submission-created` event fires only for submissions that pass spam filtering.
4. **Plan check:** Project configuration → Usage/Billing. Forms and functions draw on the plan's allowance (Netlify moved new accounts to credit-based plans in 2025). One enquiry a day is well within the free allowance; check once traffic grows.

---

## 3. Instant acknowledgement and lead log (built, needs keys)

**Already built:** `netlify/functions/submission-created.js`. Netlify runs it automatically after each verified submission. It has no dependencies and holds no secrets. In order, it:

1. **Logs the lead** to a Google Sheet (if `SHEET_WEBHOOK_URL` is set), first, so a lead is never lost even if email fails. It records the page and language (`en`, `ar`, `ru`, `zh`, `hi`, worked out from the page the form was sent from).
2. **Emails the enquirer** a branded acknowledgement for `brief` ("Your brief has reached Eastbridge": personal reply from Philip within one working day, the three next steps from the contact page, booking button if `BOOKING_URL` is set, WhatsApp button, phone and hours, privacy line). For `notes` it sends a short subscription confirmation. For `checklist` it sends nothing (the download is on the thank-you page), unless the visitor ticked the notes box, in which case they get the same subscription confirmation. The `brief` acknowledgement contains no marketing content unless the enquirer ticked the notes box; if they did, it adds one line confirming the notes and how to stop them. To prevent abuse of a public form, the email uses only the enquirer's first name (letters only) and never repeats anything else they typed.
3. **Emails an internal lead alert** for `brief` with every field, including `marketing_opt_in` (if `LEAD_ALERT_TO` is set), with Reply-To set to the enquirer, so Phil can reply straight from the alert.

**Marketing consent, end to end**

- Only a ticked box counts: the function records `marketing_opt_in` as `yes` only when the form sent `yes`; an unticked box sends nothing and is recorded as `no`. A `notes` subscription is recorded as `yes` with `marketing_source` = `notes form`.
- `marketing_opt_in` and `marketing_source` are written to the sheet row, the function log line and the lead alert.
- **There is no mailing-list integration.** The function never adds anyone to Resend Audiences, Buttondown or any other list. Building the notes list is a manual step (section 12) and must use only `notes` submissions and rows where `marketing_opt_in` is `yes`.
- **Unsubscribes are manual.** The site and emails say: reply to any note with "unsubscribe" or write to enquiries@eastbridgepartners.ae. Phil removes the address from the sending list, sets `marketing_opt_in` to `no` on that person's rows, and keeps a short suppression list (email and date) so the address is not re-imported from an old Netlify export. If a sending tool with an unsubscribe link is adopted, its unsubscribe list must be checked before every send as well.
- Offline test: `node tools/test_submission_function.js` (or `npm test`) mocks `fetch` and checks the opt-in yes/no paths for all three forms.

If keys are missing it skips email and carries on. It always returns success, so the form never breaks for the visitor. The auto-reply is in English for every language version. A translated reply would need wording checked by a native speaker under `src/i18n/TRANSLATION_BRIEF.md`. The `language` column tells Phil which language to reply in.

**Phil, once: email provider (pick one)**

*Resend (recommended, simplest, free up to 3,000 emails a month)*

1. resend.com → Sign up → **Domains** → Add domain → `eastbridgepartners.ae` → region closest (EU, Ireland, is fine).
2. Add the DNS records Resend shows (DKIM TXT, SPF TXT/MX on the `send` subdomain) at the registrar → Verify. Keep any existing Google/Microsoft MX records untouched.
3. Add or tighten DMARC at the registrar if absent: TXT `_dmarc` → `v=DMARC1; p=none; rua=mailto:enquiries@eastbridgepartners.ae` (move to `p=quarantine` after a month of clean reports).
4. **API Keys** → Create API key → permission "Sending access" → domain `eastbridgepartners.ae` → copy it once.

*Postmark (alternative, strong deliverability, paid from about USD 15 a month)*

1. postmarkapp.com → Sign up → Sender signatures → Domains → Add domain → add DKIM and Return-Path DNS records → Verify.
2. Servers → your server → API Tokens → copy the Server API token. Use the "outbound" transactional stream.

**Phil, once: Netlify environment variables**

app.netlify.com → project → Project configuration → **Environment variables** → Add a variable → "Add a single variable". Scope: Functions. Then redeploy.

| Variable | Value | Required |
|---|---|---|
| `EMAIL_PROVIDER` | `resend` or `postmark` | Optional (default `resend`) |
| `EMAIL_API_KEY` | the key from step above (mark as secret) | Yes, for email |
| `EMAIL_FROM` | `Eastbridge Strategic Partners <enquiries@eastbridgepartners.ae>` | Yes, for email |
| `EMAIL_REPLY_TO` | `enquiries@eastbridgepartners.ae` | Optional |
| `LEAD_ALERT_TO` | Phil's address (comma-separate for more) | Optional |
| `BOOKING_URL` | the booking page from section 5 | Optional |
| `SHEET_WEBHOOK_URL` | the Apps Script web app URL from section 4 | Optional |
| `SHEET_WEBHOOK_TOKEN` | any long random string, also pasted in the Apps Script | Optional, recommended |
| `AUTOREPLY_DISABLED` | `true` to pause customer emails | Optional |

**Test:** submit the live form with your own address. Then Logs & metrics → Functions → `submission-created` shows a line like `{"sheet":{"logged":true},"ack":{"sent":true}}`. Check the email lands in the inbox, not spam, on Gmail and Outlook.

**Privacy notice:** the notice on `/privacy/` (`src/pages.py`, function `legal`) names Netlify (stores submissions), "our email providers" (mailbox, confirmations and notes) and Google "when we use Google Sheets" for the log. It describes analytics only when `GA4_ID` is set in `src/config.py`. If you do not set up the sheet, delete the Google line; if you name a specific email provider, add it. The final wording needs your or a lawyer's review before launch.

---

## 4. CRM pipeline

Start with the Google Sheet. It costs nothing, the function already writes to it, and with fewer than 50 leads a year a full CRM adds clicks, not value. Move to HubSpot's free CRM (or Zoho CRM, which pairs with Zoho Books) when there are more than about 10 live opportunities at once.

**Phil, once: the sheet and webhook**

1. sheets.google.com → Blank → name it "Eastbridge pipeline". Rename the first tab `Leads`.
2. Extensions → Apps Script → replace the code with the script below → set `TOKEN` to the same string as `SHEET_WEBHOOK_TOKEN` → Save.
3. Deploy → New deployment → type "Web app" → Execute as "Me" → Who has access "Anyone" → Deploy → authorise → copy the Web app URL into `SHEET_WEBHOOK_URL` on Netlify.

```javascript
const TOKEN = 'paste-the-same-long-random-string';
const COLS = ['received','form','status','name','email','phone','area','stage','budget','based',
  'message','contact_method','marketing_opt_in','marketing_source','page','language','submission_id',
  'owner','next_action','next_action_date',
  'source','fee_estimate_aed','probability','proposal_sent','decision_date','lost_reason','notes'];
function doPost(e) {
  const body = JSON.parse(e.postData.contents || '{}');
  if (TOKEN && body.token !== TOKEN) return ContentService.createTextOutput('forbidden');
  const sh = SpreadsheetApp.getActive().getSheetByName('Leads');
  if (sh.getLastRow() === 0) sh.appendRow(COLS);
  const r = body.row || {};
  sh.appendRow(COLS.map(c => c === 'next_action' && r.form === 'brief' ? 'Reply personally'
                         : c === 'next_action_date' && r.form === 'brief' ? new Date(Date.now() + 864e5)
                         : (r[c] || '')));
  return ContentService.createTextOutput('ok');
}
```

4. Data → Data validation on the `status` column → dropdown with the stages below. Format → Conditional formatting → highlight `next_action_date` before today in red.
5. Optional: Tools → Notification settings → "Notify me when any changes are made" for a second alert.

**Pipeline stages (status column)**

| Stage | Entry rule | Automation | Target time |
|---|---|---|---|
| New enquiry | Form, WhatsApp, call or referral | Function logs it, acknowledges, alerts Phil | – |
| Replied | Phil's personal reply sent | Phil changes status | Within 1 working day |
| Call booked | First conversation in calendar | Booking tool emails confirmation and reminders | Within 5 working days |
| Call held | Conversation done, notes in `notes` | – | – |
| Proposal sent | Written scope and fee sent | Template (section 7); e-sign tool tracks opens | Within 3 working days of call |
| Negotiation | Questions or changes | Follow-up reminder in `next_action_date` | – |
| Won | Engagement letter signed and first invoice issued | E-sign tool and accounting tool | – |
| Onboarding | Pack sent, kick-off booked | Section 8 | Within 5 working days of win |
| Active | Work under way | Weekly report (section 9) | – |
| Closed – complete | Handover done, final invoice paid | Ask for a Google review from the client (genuine Eastbridge client only) | – |
| Lost / Not a fit / Referred on | Record `lost_reason` | – | – |
| Checklist download | `checklist` form | Logged; subscription confirmation only if `marketing_opt_in` is `yes` | – |
| Subscriber | `notes` form | Confirmation email | – |

**Fields** are the columns in the script. Add `source` by hand (Google, AI assistant, LinkedIn, referral from architect, agent, word of mouth) and ask "How did you hear about us?" in the first call. That one column tells you where to spend time.

---

## 5. Booking link

**Option A: Google Calendar appointment schedule (free with a Google account; Workspace adds reminders and payment features).** calendar.google.com → Create → **Appointment schedule** → title "First conversation with Eastbridge (30–45 min)" → duration 45 minutes → availability Monday–Friday, add early-morning and evening Gulf slots for UK and European clients → Booking form: ask name, email, phone, "Where is the project?" → Location: Google Meet → Booked appointment settings: buffer 15 minutes, maximum 3 per day, minimum notice 12 hours → Save → Open booking page → copy the link into `BOOKING_URL`.

**Option B: Calendly (better time-zone handling and reminders; free plan allows one event type).** calendly.com → Sign up with Google → connect the calendar → New event type → One-on-one → same details as above → Invitee questions as above → Notifications → email reminder 24 hours before → copy link into `BOOKING_URL`.

Use the link in: the auto-acknowledgement (automatic once `BOOKING_URL` is set), Phil's personal reply, the WhatsApp quick reply `/book`, the LinkedIn page button, and the Google Business Profile "Book" link. Adding it as a button on `/contact/` is a small later change to `src/pages.py`.

---

## 6. WhatsApp Business

**Already built:** every page links to `wa.me/971567440057` with pre-filled text; WhatsApp clicks record as a GA4 `contact` event once GA4 is on.

**Phil, once (WhatsApp Business app, free).** Install "WhatsApp Business" on the phone holding +971 56 744 0057 (it can migrate an existing WhatsApp chat history).

1. Settings → Business tools → **Business profile**: name "Eastbridge Strategic Partners", category "Business service" or "Consulting", description (from the offsite kit: "Client-side project management for private villa builds and renovations in Dubai and Abu Dhabi. We represent the owner, alongside the owner's DM-registered consultant and the contractor."), address as in `src/config.py`, hours Monday–Friday 9:00–18:00, website, email.
2. Business tools → **Greeting message** → on → "Thank you for contacting Eastbridge Strategic Partners. Philip will reply personally, usually within a few hours during the working day. If it helps, tell us where the project is and what stage it has reached." → Recipients: everyone not in address book.
3. Business tools → **Away message** → on → outside business hours → "Thank you for your message. Our hours are Monday to Friday, 9am to 6pm Gulf Standard Time. Philip will reply on the next working day. To book a call at a time that suits you: [BOOKING_URL]".
4. Business tools → **Quick replies** (type `/` in a chat to use):

| Shortcut | Message |
|---|---|
| `/book` | "Here is a link to choose a time for a free first conversation, usually 30 to 45 minutes: [BOOKING_URL]" |
| `/brief` | "If it is easier, you can send the details through our private brief form: https://www.eastbridgepartners.ae/contact/" |
| `/role` | "We are a client-side project manager. We represent you, the owner, alongside your DM-registered consultant and the contractor. We do not build, design or certify, so our advice has no conflict." |
| `/fees` | "Our fee depends on the scope and length of the project. After a first conversation we send a written proposal with a clear scope and a fixed or monthly fee." |
| `/next` | "Next steps: a free first conversation, then a written proposal if we can help. If we cannot, we will say so." |
| `/plot` | "Before you buy or commit to a plot, our plot review looks at the developer's rules, likely build cost and programme: https://www.eastbridgepartners.ae/services/plot-due-diligence/" |
| `/overseas` | "Many owners build from abroad. Here is how we keep you informed with independent site visits, photos and weekly reports: https://www.eastbridgepartners.ae/services/overseas-owners/" |

5. Business tools → **Catalogue** → Add new item, one per core service, with no price (choose "price on request" or leave blank), the service page link and one UK project photo captioned "Built by P Chapman Construction, UK": Owner's representation; Villa construction project management; Villa renovation project management; Plot due diligence; Stalled project rescue; Variations, delays and claims; Snagging and handover.
6. **Labels**: New enquiry, Call booked, Proposal sent, Client, Not a fit. These mirror the sheet.
7. Optional, later: a WhatsApp Channel for article updates.

Upgrade path, only if volume justifies it: the WhatsApp Business Platform through a provider (Bird, 360dialog, Twilio) allows template messages and CRM sync, with per-conversation fees.

---

## 7. Proposal, e-signature, invoice and payment

**Proposal.** One Google Docs template: "Eastbridge proposal – [Client] – [Project]". Sections: your project as we understand it; what we will do (scope by stage, using the service names on the site); what we will not do (statutory design, authority submissions, supervision of construction and certification remain with the owner's DM-registered consultant; we do not build); who does what (owner, consultant, contractor, Eastbridge); reporting rhythm; fee (fixed fee per stage, monthly retainer, or percentage band; working figures in `FEES` in `src/config.py`); payment terms; assumptions; validity (30 days); next step. Take advice from a UAE-qualified lawyer on the engagement terms and confirm professional indemnity insurance before the first signature.

**E-signature (pick one).** Dropbox Sign or Docusign (simple, recognised by overseas clients), or Zoho Sign (bundled cheaply with Zoho One). Click-path, Dropbox Sign: sign.dropbox.com → Templates → Create template → upload the engagement letter PDF → add signer role "Client" and fields → Save. Then for each client: Use template → enter name and email → Send. Signed PDF returns to Phil and goes into the client folder.

**Accounting and invoicing in AED.**

| Option | Why | Watch |
|---|---|---|
| **Zoho Books (UAE edition)** | Built for UAE VAT returns and FTA-format tax invoices, AED base, multi-currency invoices, payment reminders, client portal | Pair with Zoho Sign/CRM if you like one vendor |
| Xero | Strong bank feeds, accountant familiarity, multi-currency | Check UAE VAT return support with your accountant |
| QuickBooks Online | Familiar to UK users | Confirm the UAE edition and VAT features available for a Meydan Free Zone company before choosing |

Automations to switch on in whichever tool: invoice templates per fee type; recurring monthly invoice for retainers; reminders at 3 days before, on the due date and 7 days after; online payment link on every invoice.

**Getting paid.**

- **Bank transfer in AED** to the company account: the default for UAE clients.
- **Airwallex** business account: local GBP and EUR receiving details so UK and European clients pay as a domestic transfer, converted to AED at low cost. Confirm onboarding is available for a Meydan Free Zone licence.
- **Stripe** (available to UAE businesses): card payment links on invoices for smaller fees such as a plot review. Card fees make it unsuitable for large retainers.

**VAT and tax: Eastbridge's VAT registration status must be confirmed before the first invoice.** UAE VAT is 5%. Registration is mandatory once taxable supplies pass AED 375,000 in the previous 12 months or are expected to in the next 30 days, and voluntary from AED 187,500 (Federal Tax Authority, https://tax.gov.ae/en/taxes/vat/vat.topics/registration.for.vat.aspx). Services connected with property in the UAE are generally not zero-rated even when the client lives abroad, but confirm this with a UAE tax agent. A tax invoice must show the TRN once registered. Also confirm corporate tax registration and free zone status with the same adviser, and ask about the UAE e-invoicing timetable for a business of Eastbridge's size. Until registered, invoices must not show VAT.

---

## 8. Client onboarding pack

Write once in Google Drive as a folder template, then copy it per client (Drive → right-click folder → Make a copy is file-by-file, so keep it as a short list of documents or use a "Copy folder" add-on).

1. **Welcome letter** (one page): who we are, who to contact, hours, how quickly we reply, how we report.
2. **Signed engagement letter and scope** (from section 7).
3. **Roles and responsibilities matrix**: owner, owner's DM-registered consultant, contractor, master developer, Eastbridge. Make clear the owner appoints, the consultant holds statutory design and supervision duties, and Eastbridge represents the owner.
4. **Communication protocol**: WhatsApp group for quick matters (owner, Phil), email for decisions, weekly report every Thursday, monthly cost and programme review call, what counts as urgent.
5. **Decision and approvals log** (Sheet): date, decision, options considered, cost and programme effect, approved by owner.
6. **Information request list**: title deed or sale agreement, plot affection plan, master developer guidelines, consultant and contractor contracts, drawings, programme, payment schedule, insurances, previous reports.
7. **Document register** (Sheet) and folder structure: 01 Contracts, 02 Drawings, 03 Programme, 04 Cost, 05 Site visits, 06 Correspondence, 07 Approvals (copies received from the consultant), 08 Handover.
8. **Kick-off meeting agenda**: objectives, budget, programme, risks, decision rights, reporting.
9. **Data and confidentiality note**: how project information is stored and shared, consistent with `/privacy/`.

Automation: when the sheet status changes to "Won", Phil copies the folder, sends the welcome letter and the kick-off booking link. With Zoho or HubSpot this can be a workflow; with the sheet it is a five-minute checklist.

---

## 9. Weekly client report template

Sent every Thursday by email as a PDF plus a link to the live folder, so an owner abroad can read it over the weekend. One template in Google Docs (narrative) with figures pulled from a Google Sheet (cost and programme).

**Header:** project, report number, period, date of last site visit, overall status (green, amber, red) for cost, programme, quality and risk.

1. **Summary in three lines.** What happened, what needs your decision, what we are watching.
2. **Decisions needed from you**, each with a date, options and our recommendation.
3. **Site visit.** Date, who attended, progress against the programme by area, 6–12 dated photos with captions. State that these are Eastbridge's independent client-side observations for the owner. Statutory supervision and inspections rest with the owner's DM-registered consultant and the relevant authority.
4. **Cost.** Contract sum, approved variations, pending variations (contractor's claim vs our view), forecast final cost, contingency remaining, payments certified by the consultant and paid to date, next payment due.
5. **Programme.** Contract completion date, current forecast, change since last week, critical path items, extension-of-time notices received.
6. **Risks and issues register.** Top five, each with likelihood, impact, owner and action.
7. **Quality and snagging observations** raised with the consultant and contractor, and their status.
8. **Approvals and NOCs** (status as reported by the consultant): what is pending with the master developer or authority.
9. **Correspondence of note** and actions agreed.
10. **Next week.** Planned site visit, meetings, expected milestones.

Automation: the cost and programme tables are linked from the Sheet (Insert → Chart/Table → From Sheets, "Update" in one click). Photos go straight from the phone into the week's folder (Google Drive app → Upload). A Claude session can draft the narrative from Phil's voice notes and photo captions for him to check and send.

---

## 10. Monthly business dashboard

A Looker Studio dashboard (free) on GA4, Search Console and the pipeline Sheet. lookerstudio.google.com → Create → Report → add data sources Google Analytics, Search Console, Google Sheets → one page per area below. Review on the first working day of each month, alongside the SEO engine's monthly report.

| Area | KPI | Source |
|---|---|---|
| Visibility | Organic clicks and impressions, average position for the 20 target queries | Search Console, `reports/visibility.csv` |
| Visibility | Sessions from AI assistants (ChatGPT, Perplexity, Gemini, Copilot) | GA4 "AI assistants" channel |
| Visibility | Pages indexed, Core Web Vitals pass rate | Search Console |
| Demand | Briefs received, WhatsApp clicks, calls; by source and language | GA4 key events, Sheet |
| Conversion | Enquiry to call booked; call to proposal; proposal to won (win rate) | Sheet |
| Speed | Median time to personal reply (target under 1 working day) | Sheet |
| Pipeline | Open proposals: count and fee value, weighted by probability | Sheet |
| Money | Fees invoiced, cash received, debtors over 30 days | Accounting tool |
| Delivery | Weekly reports sent on time, open decisions older than 14 days | Client trackers |
| Authority | New citations and profiles live, genuine reviews received | Offsite kit tracker |

---

## 11. Daily SEO engine (scheduled task)

**Already built:** `AUTOMATION.md` is the full playbook. Daily: build, audit (`tools/seo_audit.py`, must report 0 errors), live checks, visibility check into `reports/visibility.csv`, competitor watch, freshness updates. Tuesday and Friday: one researched article each from `src/content/TOPICS.md`, internal links, translation into Arabic, Russian, Chinese and Hindi through `tools/i18n.py`, commit and push, then `tools/indexnow.py`. Monthly: trend review and three off-site actions. A report to Phil of eight lines or fewer, every run.

**Currently blocked.** The scheduled Claude task cannot clone, commit or push until the Claude GitHub app can reach the canonical repository.

**Phil, once:**

1. github.com/settings/installations → **Claude** → Configure → Repository access → "Only select repositories" → add the canonical repo (see section 1) → Save. If Claude is not listed, install it from the Claude app's GitHub connection first (claude.ai → Settings → Connectors → GitHub).
2. Confirm Netlify is linked to the same repo and branch, so each push deploys.
3. Ask Claude to create the scheduled task: daily at a quiet hour Gulf time, fresh session each run, prompt "Follow AUTOMATION.md in the Eastbridge website repository: run the daily steps, and on Tuesdays and Fridays the publishing steps. Report to Phil in eight lines or fewer."

Until then, the same steps can be run by hand in any Claude Code session on the repo.

---

## 12. Weekly content and social engine

Quality over volume, as `AUTOMATION.md` requires. Each article feeds a week of honest, useful posts. Every post follows `src/content/WRITING_BRIEF.md`: no UAE project claims, UK photos captioned as P Chapman Construction's, no invented figures.

| Day | Output | Channel | Built / to set up |
|---|---|---|---|
| Tue, Fri | New article (EN + 4 languages), IndexNow ping | Website | Built (SEO engine) |
| Sun | One LinkedIn post from Phil's personal profile: a builder's-side lesson from the week's article, link in first comment | LinkedIn | Phil posts; Claude drafts |
| Mon | Company page post: three key points from the article, link | LinkedIn page | Page to create (offsite kit 2.3) |
| Wed | Instagram carousel: 5–7 slides of the article's key points over UK project photos, credited | Instagram (exists) | Canva template to make once; schedule in Meta Business Suite (business.facebook.com → Planner → Create post → Schedule) |
| Thu | WhatsApp Status or Channel: one line and a link | WhatsApp Business | Free |
| Monthly | "Eastbridge notes" email: the month's two to four articles, one paragraph each | Email to people who asked for notes only | Build the list by hand: `notes` submissions, plus `brief` and `checklist` submissions where `marketing_opt_in` is `yes` (Netlify Forms → Download CSV, or filter the sheet). Never import anyone else. Remove everyone on the suppression list (section 3) before each send. Import into Resend Audiences or Buttondown; include an unsubscribe link and the reply-to-unsubscribe line |
| Monthly | One off-site action from the SEO engine's list (directory, guest article, trade-press comment) | Various | Phil approves |

Claude can draft the posts, carousel text and newsletter each week from the published article. Phil approves and posts. Nothing is posted automatically under his name.

---

## 13. Cost of the stack

Indicative list prices, October 2026. AED at 3.6725 per USD. Many tools are cheaper billed annually.

| Tool | Purpose | Plan | USD / month | AED / month | Needed for first client |
|---|---|---|---|---|---|
| Netlify | Hosting, forms, functions | Free (paid from about USD 9–20 if limits reached) | 0 | 0 | Yes |
| Domain `.ae` | Website and email | Registrar renewal (about USD 30–60 a year) | ~4 | ~15 | Yes |
| Google Workspace Business Starter | Email, Calendar, Drive, Sheets, Meet | 1 user | ~7–8.40 | ~26–31 | Yes |
| Resend | Auto-acknowledgement, alerts | Free to 3,000 emails/month (Pro USD 20) | 0 | 0 | Yes |
| Postmark (alternative to Resend) | Same | Basic | ~15 | ~55 | – |
| Google Sheet + Apps Script | Pipeline CRM | Included | 0 | 0 | Yes |
| HubSpot CRM (later) | CRM | Free | 0 | 0 | Later |
| Google appointment schedule | Booking | Included | 0 | 0 | Yes |
| Calendly (alternative) | Booking | Standard | ~10–12 | ~37–44 | – |
| WhatsApp Business app | Chat, catalogue, quick replies | Free | 0 | 0 | Yes |
| Dropbox Sign or Docusign | E-signature | Essentials / Personal | ~10–20 | ~37–73 | Yes |
| Zoho Books (UAE) | Invoices, VAT, reminders | Standard | ~15–25 | ~55–90 | Yes |
| Airwallex | GBP/EUR receiving, FX | Business account | 0–~25 | 0–~90 | Helpful for UK clients |
| Stripe | Card payment links | Pay as you go (fee per transaction) | 0 | 0 | Optional |
| Canva Pro | Carousels, report covers | 1 user | ~15 | ~55 | Helpful |
| Looker Studio, GA4, Search Console, Bing Webmaster | Dashboard, analytics | Free | 0 | 0 | Yes |
| Claude (existing subscription) | SEO engine, drafting | Existing | – | – | Yes |
| **Lean total (first client)** | | | **~36–60** | **~130–220** | |

Not included: UAE tax agent, lawyer review of the engagement letter, professional indemnity insurance. These are worth more than everything in the table.

---

## 14. Phil's one-time checklist, in order

1. Choose the canonical repo; link Netlify; point the domain; confirm `enquiries@` receives mail. (Section 1)
2. Netlify: enable form detection, add form notification email, redeploy, test the form. (Section 2)
3. Resend: verify domain, create API key; add DMARC. Netlify: add `EMAIL_API_KEY`, `EMAIL_FROM`, `LEAD_ALERT_TO`; redeploy; test. (Section 3)
4. Google Sheet and Apps Script; add `SHEET_WEBHOOK_URL` and `SHEET_WEBHOOK_TOKEN`; test. Update the privacy notice to name Google. (Sections 3–4)
5. Appointment schedule or Calendly; add `BOOKING_URL`. (Section 5)
6. WhatsApp Business profile, greeting, away message, quick replies, catalogue. (Section 6)
7. Search Console, Bing Webmaster, GA4 ID into `src/config.py`; run IndexNow. (Section 1)
8. Give the Claude GitHub app access to the repo and create the daily SEO task. (Section 11)
9. Confirm VAT and corporate tax position with a UAE tax agent; set up Zoho Books (or chosen tool), payment rails and the e-sign template; lawyer review of the engagement letter; PI insurance. (Section 7)
10. Write the proposal template, onboarding pack and weekly report template once. (Sections 7–9)
11. Google Business Profile, LinkedIn page and directory listings from the offsite kit; add URLs to `SOCIAL`. (Section 1, offsite kit)
12. Looker Studio dashboard; first monthly review. (Section 10)

Steps 1 to 6 take roughly one focused day and are enough to capture, acknowledge, log and book the first client without anything falling through the cracks.
