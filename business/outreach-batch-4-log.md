# Outreach batch 4: send log

Send started 6 November 2026 at about 13:08 UTC from philip@eastbridgestrategicpartners.com through Bird
(sending domain eastbridgestrategicpartners.com). Each email was BCC'd to Philip, and replies go to his Outlook.
Emails and sources: `business/outreach-batch-4.md`. Bird tag: `campaign:outreach-batch-4`.

**The batch stopped partway.** Only #1 and #2 went out (13:08 UTC). At #3, Bird refused the send with error E04017: "This organization is limited to 50 emails per day; this request needs 2 and 0 remain". Each send counts as 2 because of the BCC to Philip. The retry with the same idempotency key failed the same way. The limit resets at 00:00 UTC, so #3–#20 were not sent. They still need to be sent with the same wording, using idempotency keys `eb-b4-live-03` to `eb-b4-live-20`. Before that, either wait for the reset or have the daily limit raised (upgrade the Bird plan, or ask Bird support if already on a paid plan).

| # | Firm | Address | Segment | Status (13:11 UTC) |
|---|---|---|---|---|
| 1 | OTILÌA Interior Design | otilialuxuryinterior@gmail.com | Abu Dhabi studio | Delivered |
| 2 | Bon Marche Interior Design & Fit-Out | info@bonmarche.vip | Abu Dhabi studio | Delivered |
| 3 | UPA Italia by Paolo Lettieri Architects | contact@upaitalia.com | Abu Dhabi studio | Not sent (daily limit) |
| 4 | Laurent Galle Interior Design | contact@laurentgalle.fr | Abu Dhabi studio | Not sent (daily limit) |
| 5 | Royal Lounge Properties | info@royallp.com | Abu Dhabi agent | Not sent (daily limit) |
| 6 | Crompton Partners | guides@cromptonpartners.com | Abu Dhabi agent | Not sent (daily limit) |
| 7 | Engel & Völkers Dubai | dubai@engelvoelkers.com | Dubai villa agency | Not sent (daily limit) |
| 8 | fäm Properties | info@famproperties.com | Dubai villa agency | Not sent (daily limit) |
| 9 | Morgan's International Realty | info@morgansrealty.com | Dubai villa agency / private office | Not sent (daily limit) |
| 10 | Banke International Properties | enquiries@banke.ae | Dubai villa agency | Not sent (daily limit) |
| 11 | Prime by betterhomes | info@bhomes.com | Dubai villa agency / private office | Not sent (daily limit) |
| 12 | Quintessentially Estates | info@quintessentiallyestates.com | Relocation / concierge | Not sent (daily limit) |
| 13 | HelpXpat | enquiry@helpxpat.com | Relocation | Not sent (daily limit) |
| 14 | Move One | relo@moveoneinc.com | Relocation | Not sent (daily limit) |
| 15 | NH Management | info@nhmanagement.com | Private-client adviser | Not sent (daily limit) |
| 16 | Interior Lab | info@interiorlab.ae | Dubai studio | Not sent (daily limit) |
| 17 | DERUN | info@derun.ae | Dubai studio | Not sent (daily limit) |
| 18 | Killa Design | info@killadesign.com | Dubai architecture studio | Not sent (daily limit) |
| 19 | Saif Elite QS | info@saifeliteqs.com | Cost consultant / QS | Not sent (daily limit) |
| 20 | TC Consultancy | info@tccons.ae | Cost consultant / QS | Not sent (daily limit) |

Of the 2 sent, both were delivered, with no bounces or deferrals. There were 18 send errors, all caused by the daily limit (E04017).

Follow-ups use the same process as batches 2 and 3. The day-4 and day-10 follow-ups are prepared as Outlook drafts from the templates in `business/outreach-kit.md` (b) for Philip to approve. Count from each firm's actual send date: firms #3–#20 start their clock when they are sent. Do not follow up anyone who replies or asks not to be contacted.
