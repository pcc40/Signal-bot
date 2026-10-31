// Netlify event-triggered function: runs automatically after every verified
// (non-spam) Netlify Forms submission. No dependencies; uses Node 18+ fetch.
//
// What it does
//   1. "brief" form  -> sends the enquirer a branded acknowledgement email.
//      "notes" form  -> sends a short subscription confirmation.
//   2. Optionally emails an internal lead alert (LEAD_ALERT_TO).
//   3. Optionally logs the lead to a Google Sheet (SHEET_WEBHOOK_URL, a Google
//      Apps Script web app; see business/automation-blueprint.md, section 3).
//
// Configuration (Netlify -> Project configuration -> Environment variables).
// No secrets live in this file.
//   EMAIL_PROVIDER      "resend" (default) or "postmark"
//   EMAIL_API_KEY       Resend API key, or Postmark server token
//   EMAIL_FROM          e.g. "Eastbridge Strategic Partners <enquiries@eastbridgepartners.ae>"
//                       (the domain must be verified with the email provider)
//   EMAIL_REPLY_TO      optional, defaults to the address inside EMAIL_FROM
//   LEAD_ALERT_TO       optional, internal address(es) for a lead alert, comma separated
//   BOOKING_URL         optional, Google Calendar appointment page or Calendly link
//   SHEET_WEBHOOK_URL   optional, Apps Script web app URL
//   SHEET_WEBHOOK_TOKEN optional, shared secret checked by the Apps Script
//   AUTOREPLY_DISABLED  optional, set to "true" to stop customer emails (logging continues)
//
// If EMAIL_API_KEY or EMAIL_FROM is missing the function skips email and still
// logs to the sheet, so a half-finished setup never breaks form submissions.

"use strict";

const SITE = process.env.SITE_PUBLIC_URL || "https://www.eastbridgepartners.ae";
const PHONE_DISPLAY = "+971 56 744 0057";
const PHONE_E164 = "+971567440057";
const WHATSAPP = "971567440057";
const HOURS = "Sunday to Thursday, 9am to 6pm Gulf Standard Time";

// ---------- helpers ----------------------------------------------------------

const esc = (s) =>
  String(s == null ? "" : s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");

const isEmail = (s) => typeof s === "string" && s.length <= 254 && /^[^\s@<>"',;]+@[^\s@<>"',;]+\.[^\s@<>"',;]{2,}$/.test(s);

// Anyone can type any address into a public form, so the customer email must
// never carry attacker-controlled text. Use a first name only, letters only.
function safeFirstName(name) {
  const first = String(name || "").trim().split(/\s+/)[0] || "";
  const clean = first.replace(/[^\p{L}'\-]/gu, "").slice(0, 30);
  return clean.length >= 2 ? clean : "";
}

const asText = (v) => (Array.isArray(v) ? v.join(", ") : v == null ? "" : String(v)).slice(0, 5000);

function langFromReferrer(ref) {
  try {
    const m = new URL(ref).pathname.match(/^\/(ar|ru|zh|hi)\//);
    return m ? m[1] : "en";
  } catch (_) {
    return "";
  }
}

function addressOnly(from) {
  const m = String(from || "").match(/<([^>]+)>/);
  return (m ? m[1] : String(from || "")).trim();
}

function waLink(text) {
  return `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(text)}`;
}

// ---------- email copy (British English, calm, no exclamation marks) ---------

function briefEmail(firstName) {
  const hello = firstName ? `Dear ${firstName},` : "Hello,";
  const booking = process.env.BOOKING_URL || "";
  const wa = waLink("Hello Eastbridge, I have just sent a brief through your website.");
  const subject = "Your brief has reached Eastbridge";

  const text = [
    hello,
    "",
    "Thank you for sending us your brief. It has reached us safely and Philip Chapman, our founding partner, will reply personally within one working day.",
    "",
    "What happens next:",
    "1. We read your brief carefully.",
    "2. We arrange a free first conversation, usually 30 to 45 minutes, to understand the project.",
    "3. If we can help, we send a written proposal with a clear scope and fee. If we cannot, we say so and, where we can, point you to someone who can.",
    "",
    booking ? `If you would like to choose a time for that first conversation now, you can book here: ${booking}` : "",
    `If it is urgent, message us on WhatsApp: ${wa}`,
    `Or call ${PHONE_DISPLAY} (${HOURS}).`,
    "",
    "Nothing you send us is shared or published. We use your details only to reply to you.",
    "",
    "Eastbridge Strategic Partners",
    "Client-side project management for private villas in Dubai and Abu Dhabi",
    SITE,
  ]
    .filter((l, i, a) => !(l === "" && a[i - 1] === ""))
    .join("\n");

  const btn = (href, label) =>
    `<a href="${esc(href)}" style="display:inline-block;background:#1f2a2e;color:#ffffff;text-decoration:none;padding:12px 20px;border-radius:2px;font-weight:600;margin:4px 8px 4px 0">${esc(label)}</a>`;

  const html = `<!doctype html><html lang="en"><body style="margin:0;background:#f4f1ec;font-family:Georgia,'Times New Roman',serif;color:#1f2a2e">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f4f1ec"><tr><td align="center" style="padding:32px 16px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#ffffff">
<tr><td style="padding:28px 32px;border-bottom:1px solid #e5e0d8;font-family:Arial,Helvetica,sans-serif;font-size:13px;letter-spacing:.14em;text-transform:uppercase">Eastbridge Strategic Partners</td></tr>
<tr><td style="padding:32px;font-size:17px;line-height:1.6">
<p style="margin:0 0 16px">${esc(hello)}</p>
<p style="margin:0 0 16px">Thank you for sending us your brief. It has reached us safely and Philip Chapman, our founding partner, will reply personally within one working day.</p>
<p style="margin:24px 0 8px;font-family:Arial,Helvetica,sans-serif;font-size:13px;letter-spacing:.1em;text-transform:uppercase">What happens next</p>
<ol style="margin:0 0 16px;padding-left:20px">
<li style="margin-bottom:6px">We read your brief carefully.</li>
<li style="margin-bottom:6px">We arrange a free first conversation, usually 30 to 45 minutes, to understand the project.</li>
<li>If we can help, we send a written proposal with a clear scope and fee. If we cannot, we say so and, where we can, point you to someone who can.</li>
</ol>
<p style="margin:24px 0 8px">${booking ? btn(booking, "Choose a time to talk") : ""}${btn(wa, "Message us on WhatsApp")}</p>
<p style="margin:16px 0 0;font-size:15px">Or call <a href="tel:${PHONE_E164}" style="color:#1f2a2e">${PHONE_DISPLAY}</a>, ${esc(HOURS)}.</p>
<p style="margin:24px 0 0;font-size:14px;color:#5c6468">Nothing you send us is shared or published. We use your details only to reply to you.</p>
</td></tr>
<tr><td style="padding:20px 32px;border-top:1px solid #e5e0d8;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:1.5;color:#5c6468">
Client-side project management for private villas in Dubai and Abu Dhabi.<br>
<a href="${esc(SITE)}" style="color:#5c6468">${esc(SITE.replace(/^https?:\/\//, ""))}</a> &middot; Eastbridge Strategic Partners L.L.C-FZ, Meydan Free Zone, Dubai
</td></tr></table></td></tr></table></body></html>`;

  return { subject, text, html };
}

function notesEmail() {
  const subject = "You are subscribed to Eastbridge notes";
  const text = [
    "Hello,",
    "",
    "Thank you for subscribing. We will send occasional notes on building and renovating a villa in Dubai and Abu Dhabi: costs, contracts, approvals and the questions worth asking. No more than one a month.",
    "",
    "If you did not ask for this, reply with \"unsubscribe\" and we will remove your address.",
    "",
    "Eastbridge Strategic Partners",
    SITE,
  ].join("\n");
  const html = `<!doctype html><html lang="en"><body style="font-family:Georgia,'Times New Roman',serif;color:#1f2a2e;font-size:16px;line-height:1.6;max-width:560px;margin:24px auto;padding:0 16px">
<p>Hello,</p>
<p>Thank you for subscribing. We will send occasional notes on building and renovating a villa in Dubai and Abu Dhabi: costs, contracts, approvals and the questions worth asking. No more than one a month.</p>
<p style="color:#5c6468;font-size:14px">If you did not ask for this, reply with "unsubscribe" and we will remove your address.</p>
<p>Eastbridge Strategic Partners<br><a href="${esc(SITE)}" style="color:#1f2a2e">${esc(SITE.replace(/^https?:\/\//, ""))}</a></p>
</body></html>`;
  return { subject, text, html };
}

function alertEmail(formName, lead) {
  const rows = Object.entries(lead)
    .filter(([, v]) => v)
    .map(([k, v]) => `<tr><td style="padding:4px 12px 4px 0;color:#5c6468;vertical-align:top">${esc(k)}</td><td style="padding:4px 0;white-space:pre-wrap">${esc(v)}</td></tr>`)
    .join("");
  const text = Object.entries(lead)
    .filter(([, v]) => v)
    .map(([k, v]) => `${k}: ${v}`)
    .join("\n");
  return {
    subject: `New ${formName} enquiry: ${lead.name || lead.email || "unknown"}${lead.area ? " (" + lead.area + ")" : ""}`.slice(0, 150),
    text,
    html: `<table style="font-family:Arial,Helvetica,sans-serif;font-size:14px">${rows}</table>`,
  };
}

// ---------- providers --------------------------------------------------------

async function sendEmail({ to, subject, text, html, replyTo }) {
  const key = process.env.EMAIL_API_KEY;
  const from = process.env.EMAIL_FROM;
  if (!key || !from) return { skipped: "EMAIL_API_KEY or EMAIL_FROM not set" };
  const provider = (process.env.EMAIL_PROVIDER || "resend").toLowerCase();
  const reply = replyTo || process.env.EMAIL_REPLY_TO || addressOnly(from);
  const toList = Array.isArray(to) ? to : [to];

  let res;
  if (provider === "postmark") {
    res = await fetch("https://api.postmarkapp.com/email", {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json", "X-Postmark-Server-Token": key },
      body: JSON.stringify({ From: from, To: toList.join(","), ReplyTo: reply, Subject: subject, TextBody: text, HtmlBody: html, MessageStream: "outbound" }),
    });
  } else {
    res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from, to: toList, reply_to: reply, subject, text, html }),
    });
  }
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`${provider} ${res.status}: ${body.slice(0, 300)}`);
  }
  return { sent: true };
}

async function logToSheet(row) {
  const url = process.env.SHEET_WEBHOOK_URL;
  if (!url) return { skipped: "SHEET_WEBHOOK_URL not set" };
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token: process.env.SHEET_WEBHOOK_TOKEN || "", row }),
    redirect: "follow",
  });
  if (!res.ok) throw new Error(`sheet webhook ${res.status}`);
  return { logged: true };
}

// ---------- handler ----------------------------------------------------------

exports.handler = async (event) => {
  let payload;
  try {
    payload = JSON.parse(event.body || "{}").payload || {};
  } catch (e) {
    console.error("Bad event body", e.message);
    return { statusCode: 200, body: "ignored" };
  }

  const formName = payload.form_name || (payload.data && payload.data["form-name"]) || "";
  const d = payload.data || {};
  const email = String(d.email || payload.email || "").trim();
  const referrer = asText(d.referrer);

  const lead = {
    received: payload.created_at || new Date().toISOString(),
    form: formName,
    name: asText(d.name).slice(0, 120),
    email,
    phone: asText(d.phone).slice(0, 40),
    area: asText(d.area),
    stage: asText(d.stage),
    budget: asText(d.budget),
    based: asText(d.based),
    message: asText(d.message),
    page: referrer,
    language: langFromReferrer(referrer),
    submission_id: payload.id || "",
  };

  const results = {};

  // 1. Log first, so a lead is never lost even if email fails.
  try {
    results.sheet = await logToSheet({ ...lead, status: formName === "brief" ? "New enquiry" : "Subscriber" });
  } catch (e) {
    console.error("Sheet log failed:", e.message);
    results.sheet = { error: e.message };
  }

  // 2. Customer acknowledgement.
  const autoreplyOff = String(process.env.AUTOREPLY_DISABLED || "").toLowerCase() === "true";
  if (!autoreplyOff && isEmail(email) && (formName === "brief" || formName === "notes")) {
    try {
      const msg = formName === "brief" ? briefEmail(safeFirstName(d.name)) : notesEmail();
      results.ack = await sendEmail({ to: email, ...msg });
    } catch (e) {
      console.error("Acknowledgement failed:", e.message);
      results.ack = { error: e.message };
    }
  }

  // 3. Internal alert (optional; Netlify's own form notification email also works).
  const alertTo = String(process.env.LEAD_ALERT_TO || "")
    .split(",")
    .map((s) => s.trim())
    .filter(isEmail);
  if (alertTo.length && formName === "brief") {
    try {
      results.alert = await sendEmail({ to: alertTo, ...alertEmail(formName, lead), replyTo: isEmail(email) ? email : undefined });
    } catch (e) {
      console.error("Lead alert failed:", e.message);
      results.alert = { error: e.message };
    }
  }

  console.log("submission-created", formName, payload.id || "", JSON.stringify(results));
  // Always 200: the submission itself is already stored by Netlify Forms.
  return { statusCode: 200, body: JSON.stringify(results) };
};
