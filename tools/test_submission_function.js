// Offline test for netlify/functions/submission-created.js. No network, no dependencies.
// Run: node tools/test_submission_function.js
// (Kept outside netlify/functions/ so Netlify does not deploy it as a function.)
//
// global.fetch is replaced with a recorder, so no email is sent and no sheet is written.
// It checks the marketing consent paths (brief, checklist, notes, estimate): opt-in captured, logged to the sheet, shown in the
// lead alert, and no marketing content in emails to people who did not opt in; and for "estimate" that the
// inputs, result and link reach the sheet and the alert but never the customer email; and for "brief" that the
// optional service, community and property fields reach the sheet and the alert, with forged values cleaned;
// and that the campaign attribution fields (utm_*, gclid) reach the sheet and the alert, cleaned, never the customer email.

"use strict";
const assert = require("assert");
const path = require("path");

Object.assign(process.env, {
  EMAIL_PROVIDER: "resend",
  EMAIL_API_KEY: "test-key",
  EMAIL_FROM: "Eastbridge Strategic Partners <philip@eastbridgestrategicpartners.com>",
  LEAD_ALERT_TO: "alerts@example.com",
  SHEET_WEBHOOK_URL: "https://sheet.example.com/exec",
  SHEET_WEBHOOK_TOKEN: "t",
});
delete process.env.AUTOREPLY_DISABLED;
delete process.env.BOOKING_URL;

const fn = require(path.join(__dirname, "..", "netlify", "functions", "submission-created.js"));

let calls = [];
global.fetch = async (url, opts) => {
  calls.push({ url, body: JSON.parse(opts.body) });
  return { ok: true, status: 200, text: async () => "ok" };
};

async function submit(form, data) {
  calls = [];
  const event = { body: JSON.stringify({ payload: { form_name: form, id: "sub-1", created_at: "2026-10-31T09:00:00Z", data: { "form-name": form, ...data } } }) };
  const res = await fn.handler(event);
  assert.strictEqual(res.statusCode, 200);
  const sheet = calls.filter((c) => c.url.startsWith("https://sheet.example.com"));
  const emails = calls.filter((c) => c.url === "https://api.resend.com/emails");
  const toCustomer = emails.filter((e) => e.body.to.includes(data.email));
  const alerts = emails.filter((e) => e.body.to.includes("alerts@example.com"));
  return { sheet, toCustomer, alerts };
}

const MARKETING = /notes for villa owners|unsubscribe|subscribed/i;
const base = { name: "Sarah Example", email: "sarah@example.com", message: "A villa on Island E, plot bought." };
let passed = 0;
const test = async (name, f) => { await f(); passed++; console.log("ok  " + name); };

(async () => {
  await test("brief without opt-in: logged as no, plain acknowledgement, alert shows no", async () => {
    const r = await submit("brief", base);
    assert.strictEqual(r.sheet.length, 1);
    assert.strictEqual(r.sheet[0].body.row.marketing_opt_in, "no");
    assert.strictEqual(r.sheet[0].body.row.marketing_source, "");
    assert.strictEqual(r.sheet[0].body.row.status, "New enquiry");
    assert.strictEqual(r.toCustomer.length, 1);
    assert.ok(!MARKETING.test(r.toCustomer[0].body.text), "no marketing in text email");
    assert.ok(!MARKETING.test(r.toCustomer[0].body.html), "no marketing in html email");
    assert.strictEqual(r.alerts.length, 1);
    assert.match(r.alerts[0].body.text, /marketing_opt_in: no/);
  });

  await test("brief with opt-in: logged as yes, acknowledgement carries unsubscribe line, alert shows yes", async () => {
    const r = await submit("brief", { ...base, marketing_opt_in: "yes" });
    assert.strictEqual(r.sheet[0].body.row.marketing_opt_in, "yes");
    assert.strictEqual(r.sheet[0].body.row.marketing_source, "ticked box on brief form");
    assert.match(r.toCustomer[0].body.text, /reply with "unsubscribe" or write to philip@eastbridgestrategicpartners\.com/);
    assert.match(r.alerts[0].body.text, /marketing_opt_in: yes/);
  });

  await test("brief with service, community and property: on the sheet row and in the alert, not in the customer email", async () => {
    const r = await submit("brief", { ...base, service: "Snagging and handover", area: "Jumeirah Islands", property: "Villa, 5 bedrooms, about 7,000 sq ft" });
    const row = r.sheet[0].body.row;
    assert.strictEqual(row.service, "Snagging and handover");
    assert.strictEqual(row.area, "Jumeirah Islands");
    assert.strictEqual(row.property, "Villa, 5 bedrooms, about 7,000 sq ft");
    assert.match(r.alerts[0].body.text, /service: Snagging and handover/);
    assert.match(r.alerts[0].body.text, /area: Jumeirah Islands/);
    assert.match(r.alerts[0].body.text, /property: Villa, 5 bedrooms/);
    assert.match(r.alerts[0].body.subject, /\(Jumeirah Islands\)/);
    const ack = r.toCustomer[0].body;
    assert.ok(!ack.text.includes("7,000 sq ft") && !ack.html.includes("Jumeirah Islands") && !ack.text.includes("Snagging and handover"));
  });

  await test("brief without the new optional fields: still logged, empty values", async () => {
    const r = await submit("brief", base);
    const row = r.sheet[0].body.row;
    assert.strictEqual(row.service, "");
    assert.strictEqual(row.property, "");
    assert.ok(!/service:|property:/.test(r.alerts[0].body.text));
  });

  await test("brief with a forged service value: markup stripped, length capped", async () => {
    const r = await submit("brief", { ...base, service: "<script>alert(1)</script>" + "x".repeat(200), property: "y".repeat(500) });
    const row = r.sheet[0].body.row;
    assert.ok(!/[<>()]/.test(row.service));
    assert.ok(row.service.length <= 80);
    assert.strictEqual(row.property.length, 200);
  });

  await test("brief with a forged value: treated as no", async () => {
    const r = await submit("brief", { ...base, marketing_opt_in: "no" });
    assert.strictEqual(r.sheet[0].body.row.marketing_opt_in, "no");
    assert.ok(!MARKETING.test(r.toCustomer[0].body.text));
  });

  await test("checklist without opt-in: logged as no, no email to the visitor, no alert", async () => {
    const r = await submit("checklist", { name: "Sarah Example", email: "sarah@example.com", stage: "Plot bought" });
    assert.strictEqual(r.sheet[0].body.row.marketing_opt_in, "no");
    assert.strictEqual(r.sheet[0].body.row.status, "Checklist download");
    assert.strictEqual(r.toCustomer.length, 0);
    assert.strictEqual(r.alerts.length, 0);
  });

  await test("checklist with opt-in: logged as yes, subscription confirmation sent", async () => {
    const r = await submit("checklist", { name: "Sarah Example", email: "sarah@example.com", marketing_opt_in: "yes" });
    assert.strictEqual(r.sheet[0].body.row.marketing_opt_in, "yes");
    assert.strictEqual(r.sheet[0].body.row.marketing_source, "ticked box on checklist form");
    assert.strictEqual(r.toCustomer.length, 1);
    assert.match(r.toCustomer[0].body.subject, /subscribed/);
    assert.match(r.toCustomer[0].body.text, /philip@eastbridgestrategicpartners\.com/);
  });

  await test("checklist guide field: snagging guide logged; missing means the original guide; forged value is not echoed", async () => {
    const logs = [];
    const orig = console.log;
    console.log = (...a) => logs.push(a.join(" "));
    let r;
    try {
      r = await submit("checklist", { name: "Sarah Example", email: "sarah@example.com", guide: "villa-snagging-checklist" });
    } finally {
      console.log = orig;
    }
    assert.strictEqual(r.sheet[0].body.row.guide, "villa-snagging-checklist");
    assert.strictEqual(r.sheet[0].body.row.status, "Checklist download");
    assert.ok(logs.some((l) => /submission-created checklist .*guide=villa-snagging-checklist/.test(l)), "guide in log line");
    r = await submit("checklist", { name: "Sarah Example", email: "sarah@example.com" });
    assert.strictEqual(r.sheet[0].body.row.guide, "villa-owner-checklist");
    r = await submit("checklist", { name: "Sarah Example", email: "sarah@example.com", guide: "<script>x</script>" });
    assert.strictEqual(r.sheet[0].body.row.guide, "unknown");
    r = await submit("brief", base);
    assert.strictEqual(r.sheet[0].body.row.guide, "");
  });

  await test("notes form: subscribing is the opt-in, confirmation includes manual unsubscribe route", async () => {
    const r = await submit("notes", { email: "sarah@example.com" });
    assert.strictEqual(r.sheet[0].body.row.marketing_opt_in, "yes");
    assert.strictEqual(r.sheet[0].body.row.marketing_source, "notes form");
    assert.strictEqual(r.sheet[0].body.row.status, "Subscriber");
    assert.match(r.toCustomer[0].body.text, /reply with "unsubscribe" or write to philip@eastbridgestrategicpartners\.com/);
  });

  const est = {
    name: "Sarah Example", email: "sarah@example.com", phone: "+44 7700 900123", plot: "Dubai Hills Estate, plot 12",
    message: "Design stage, no quotes yet.",
    estimate_inputs: "mode=new; tier=premium; loc=dubai-hills-estate; unit=sqft; cur=GBP; area=6000; basement=0; garden=3000; pool=1; smart=0; ffe=0; demo=0",
    estimate_result: "AED low 5,113,000; likely 6,239,000; high 7,365,000 | shown in GBP (approximate, rates of 2026-10-30): GBP low 1,039,000; likely 1,268,000; high 1,497,000",
    estimate_link: "https://eastbridgestrategicpartners.com/tools/villa-build-cost-calculator/?mode=new&tier=premium",
    currency: "GBP",
    referrer: "https://eastbridgestrategicpartners.com/ru/tools/villa-build-cost-calculator/",
  };

  await test("estimate without opt-in: logged with inputs and result, estimate acknowledgement, alert carries the estimate", async () => {
    const r = await submit("estimate", est);
    assert.strictEqual(r.sheet.length, 1);
    const row = r.sheet[0].body.row;
    assert.strictEqual(row.status, "Estimate request");
    assert.strictEqual(row.marketing_opt_in, "no");
    assert.strictEqual(row.plot, est.plot);
    assert.strictEqual(row.estimate_inputs, est.estimate_inputs);
    assert.strictEqual(row.estimate_result, est.estimate_result);
    assert.strictEqual(row.estimate_link, est.estimate_link);
    assert.strictEqual(row.currency, "GBP");
    assert.strictEqual(row.language, "ru");
    assert.strictEqual(r.toCustomer.length, 1);
    const ack = r.toCustomer[0].body;
    assert.match(ack.subject, /estimate has reached Eastbridge/);
    assert.match(ack.text, /replies personally within one working day/);
    assert.ok(!MARKETING.test(ack.text) && !MARKETING.test(ack.html), "no marketing in the acknowledgement");
    // The submitted figures and link are attacker-editable, so they never appear in the customer email.
    assert.ok(!ack.text.includes("6,239,000") && !ack.html.includes("6,239,000") && !ack.text.includes("tier=premium"));
    assert.strictEqual(r.alerts.length, 1);
    assert.match(r.alerts[0].body.subject, /New estimate enquiry: Sarah Example \(Dubai Hills Estate, plot 12\)/);
    assert.match(r.alerts[0].body.text, /estimate_result: AED low 5,113,000/);
    assert.match(r.alerts[0].body.text, /estimate_link: https:\/\/eastbridgestrategicpartners\.com\/tools\/villa-build-cost-calculator\//);
    assert.match(r.alerts[0].body.text, /marketing_opt_in: no/);
    assert.strictEqual(r.alerts[0].body.reply_to, "sarah@example.com");
  });

  await test("estimate with opt-in: logged as yes, acknowledgement carries unsubscribe line", async () => {
    const r = await submit("estimate", { ...est, marketing_opt_in: "yes" });
    assert.strictEqual(r.sheet[0].body.row.marketing_opt_in, "yes");
    assert.strictEqual(r.sheet[0].body.row.marketing_source, "ticked box on estimate form");
    assert.match(r.toCustomer[0].body.text, /reply with "unsubscribe" or write to philip@eastbridgestrategicpartners\.com/);
  });

  await test("estimate with a hostile name: first name only, no markup in the email", async () => {
    const r = await submit("estimate", { ...est, name: "<img src=x onerror=alert(1)> Bob" });
    const ack = r.toCustomer[0].body;
    assert.ok(!/<img|onerror|alert\(/.test(ack.html) && !/<img|onerror/.test(ack.text));
    assert.match(ack.text, /^(Hello|Dear [\p{L}'-]+),\n/u);
  });

  const utm = { utm_source: "google", utm_medium: "cpc", utm_campaign: "villa-pm-dubai", utm_term: "client side project manager", utm_content: "ad-1", gclid: "Cj0KCQiA_test-123" };

  await test("brief with campaign details: on the sheet row and in the alert, never in the customer email", async () => {
    const r = await submit("brief", { ...base, ...utm });
    const row = r.sheet[0].body.row;
    for (const [k, v] of Object.entries(utm)) assert.strictEqual(row[k], v, k);
    assert.match(r.alerts[0].body.text, /utm_source: google/);
    assert.match(r.alerts[0].body.text, /utm_campaign: villa-pm-dubai/);
    assert.match(r.alerts[0].body.text, /gclid: Cj0KCQiA_test-123/);
    const ack = r.toCustomer[0].body;
    assert.ok(!/utm_|gclid|villa-pm-dubai|Cj0KCQiA/.test(ack.text + ack.html), "no attribution in the customer email");
  });

  await test("estimate and checklist with campaign details: logged on the sheet row", async () => {
    let r = await submit("estimate", { ...est, ...utm });
    assert.strictEqual(r.sheet[0].body.row.utm_medium, "cpc");
    assert.strictEqual(r.sheet[0].body.row.gclid, utm.gclid);
    assert.match(r.alerts[0].body.text, /utm_medium: cpc/);
    r = await submit("checklist", { name: "Sarah Example", email: "sarah@example.com", guide: "villa-snagging-checklist", ...utm });
    assert.strictEqual(r.sheet[0].body.row.utm_source, "google");
    assert.strictEqual(r.sheet[0].body.row.utm_term, "client side project manager");
  });

  await test("no campaign details: empty values, nothing extra in the alert", async () => {
    const r = await submit("brief", base);
    const row = r.sheet[0].body.row;
    for (const k of Object.keys(utm)) assert.strictEqual(row[k], "", k);
    assert.ok(!/utm_|gclid/.test(r.alerts[0].body.text));
  });

  await test("forged campaign values: markup stripped, length capped", async () => {
    const r = await submit("brief", { ...base, utm_source: "<script>alert(1)</script>", gclid: "a".repeat(400), utm_campaign: "spring\n\nsale\"><img src=x>" });
    const row = r.sheet[0].body.row;
    assert.ok(!/[<>()"]/.test(row.utm_source + row.utm_campaign));
    assert.strictEqual(row.gclid.length, 150);
    assert.ok(!/\n/.test(row.utm_campaign));
  });

  console.log(`\n${passed} tests passed`);
})().catch((e) => {
  console.error("FAIL", e.message);
  process.exit(1);
});
