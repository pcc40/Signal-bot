# Outreach batch 4: send log

Send started 6 November 2026 at about 13:08 UTC from philip@eastbridgestrategicpartners.com through Bird
(sending domain eastbridgestrategicpartners.com). Each email was BCC'd to Philip, and replies go to his Outlook.
Emails and sources: `business/outreach-batch-4.md`. Bird tag: `campaign:outreach-batch-4`.

**The batch stopped partway.** Only #1 and #2 went out (13:08 UTC). At #3, Bird refused the send with error E04017: "This organization is limited to 50 emails per day; this request needs 2 and 0 remain". Each send counts as 2 because of the BCC to Philip. The retry with the same idempotency key failed the same way. The limit resets at 00:00 UTC, so #3–#20 were not sent. They still need to be sent with the same wording, using idempotency keys `eb-b4-live-03` to `eb-b4-live-20`. Before that, either wait for the reset or have the daily limit raised (upgrade the Bird plan, or ask Bird support if already on a paid plan).

**Completed 9 November 2026:** #3–#20 sent at about 03:45 UTC with keys `eb-b4-live-03` to `eb-b4-live-20`; all 18 delivered (firm copy and BCC), no bounces. Bird ids: em_01m6z6ekrjf09rmgmxr9g6b66w (#3) to em_01m6z6p058ffb9bfc6ys0725sv (#20). Day-4 follow-up drafts due Fri 13 Nov; final follow-up Thu 19 Nov.

| # | Firm | Address | Segment | Status (13:11 UTC) |
|---|---|---|---|---|
| 1 | OTILÌA Interior Design | otilialuxuryinterior@gmail.com | Abu Dhabi studio | Delivered |
| 2 | Bon Marche Interior Design & Fit-Out | info@bonmarche.vip | Abu Dhabi studio | Delivered |
| 3 | UPA Italia by Paolo Lettieri Architects | contact@upaitalia.com | Abu Dhabi studio | Delivered 9 Nov 2026 |
| 4 | Laurent Galle Interior Design | contact@laurentgalle.fr | Abu Dhabi studio | Delivered 9 Nov 2026 |
| 5 | Royal Lounge Properties | info@royallp.com | Abu Dhabi agent | Delivered 9 Nov 2026 |
| 6 | Crompton Partners | guides@cromptonpartners.com | Abu Dhabi agent | Delivered 9 Nov 2026 |
| 7 | Engel & Völkers Dubai | dubai@engelvoelkers.com | Dubai villa agency | Delivered 9 Nov 2026 |
| 8 | fäm Properties | info@famproperties.com | Dubai villa agency | Delivered 9 Nov 2026 |
| 9 | Morgan's International Realty | info@morgansrealty.com | Dubai villa agency / private office | Delivered 9 Nov 2026 |
| 10 | Banke International Properties | enquiries@banke.ae | Dubai villa agency | Delivered 9 Nov 2026 |
| 11 | Prime by betterhomes | info@bhomes.com | Dubai villa agency / private office | Delivered 9 Nov 2026 |
| 12 | Quintessentially Estates | info@quintessentiallyestates.com | Relocation / concierge | Delivered 9 Nov 2026 |
| 13 | HelpXpat | enquiry@helpxpat.com | Relocation | Delivered 9 Nov 2026 |
| 14 | Move One | relo@moveoneinc.com | Relocation | Delivered 9 Nov 2026 |
| 15 | NH Management | info@nhmanagement.com | Private-client adviser | Delivered 9 Nov 2026 |
| 16 | Interior Lab | info@interiorlab.ae | Dubai studio | Delivered 9 Nov 2026 |
| 17 | DERUN | info@derun.ae | Dubai studio | Delivered 9 Nov 2026 |
| 18 | Killa Design | info@killadesign.com | Dubai architecture studio | Delivered 9 Nov 2026 |
| 19 | Saif Elite QS | info@saifeliteqs.com | Cost consultant / QS | Delivered 9 Nov 2026 |
| 20 | TC Consultancy | info@tccons.ae | Cost consultant / QS | Delivered 9 Nov 2026 |

Of the 2 sent, both were delivered, with no bounces or deferrals. There were 18 send errors, all caused by the daily limit (E04017).

Follow-ups use the same process as batches 2 and 3. The day-4 and day-10 follow-ups are prepared as Outlook drafts from the templates in `business/outreach-kit.md` (b) for Philip to approve. Count from each firm's actual send date: firms #3–#20 start their clock when they are sent. Do not follow up anyone who replies or asks not to be contacted.
