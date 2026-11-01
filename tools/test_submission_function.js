// Offline test for netlify/functions/submission-created.js. No network, no dependencies.
// Run: node tools/test_submission_function.js
// (Kept outside netlify/functions/ so Netlify does not deploy it as a function.)
//
// global.fetch is replaced with a recorder, so no email is sent and no sheet is written.
// It checks the marketing consent paths: opt-in captured, logged to the sheet, shown in the
// lead alert, and no marketing content in emails to people who did not opt in.

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

  console.log(`\n${passed} tests passed`);
})().catch((e) => {
  console.error("FAIL", e.message);
  process.exit(1);
});
