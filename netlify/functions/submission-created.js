// Netlify event-triggered function: runs automatically after every verified
// (non-spam) Netlify Forms submission. No dependencies; uses Node 18+ fetch.
//
// What it does
//   1. "brief" form     -> sends the enquirer a branded acknowledgement email. Its optional
//                          "service", "area" (community) and "property" fields go to the
//                          sheet row and the lead alert, never into the customer email.
//      "notes" form     -> sends a short subscription confirmation.
//      "checklist" form -> no email (the download is shown on the thank-you page),
//                          unless the visitor ticked the optional notes box, in which
//                          case they get the same subscription confirmation as "notes".
//                          Both lead magnets post to "checklist"; a hidden field "guide"
//                          says which one (villa-owner-checklist or villa-snagging-checklist).
//                          It is written to the sheet row and the log line.
//      "estimate" form  -> sends an acknowledgement that the calculator estimate reached
//                          Philip (from /tools/villa-build-cost-calculator/). The email never
//                          repeats the submitted figures: the hidden fields can be edited by
//                          anyone, so only the lead alert and the sheet carry them.
//      Campaign attribution: "brief", "estimate" and "checklist" carry hidden fields
//                          utm_source, utm_medium, utm_campaign, utm_term, utm_content and gclid,
//                          filled by the site script only after the visitor accepted analytics
//                          (build.py ATTRIBUTION_FIELDS). They go to the sheet row and the lead
//                          alert, cleaned to plain tokens, never into a customer email.
//   2. Optionally emails an internal lead alert for "brief" and "estimate" (LEAD_ALERT_TO).
//   3. Optionally logs every submission to a Google Sheet (SHEET_WEBHOOK_URL, a Google
//      Apps Script web app; see business/automation-blueprint.md, section 4).
//
// Marketing consent
//   The "brief", "checklist" and "estimate" forms carry an optional, unticked checkbox
//   name="marketing_opt_in" value="yes". Only a ticked box counts as consent.
//   Subscribing through the "notes" form is itself the request for notes.
//   The result is written as marketing_opt_in "yes"/"no" (plus marketing_source)
//   to the sheet row, the log line and the lead alert. Acknowledgement emails to
//   people who did not opt in contain no marketing content. This function never
//   adds anyone to a mailing list: there is no list integration. Unsubscribes are
//   handled by hand (reply to any note, or write to philip@eastbridgestrategicpartners.com).
//
// Configuration (Netlify -> Project configuration -> Environment variables).
// No secrets live in this file.
//   EMAIL_PROVIDER      "resend" (default) or "postmark"
//   EMAIL_API_KEY       Resend API key, or Postmark server token
//   EMAIL_FROM          e.g. "Eastbridge Strategic Partners <philip@eastbridgestrategicpartners.com>"
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

const SITE = process.env.SITE_PUBLIC_URL || "https://eastbridgestrategicpartners.com";
const PHONE_DISPLAY = "+971 56 744 0057";
const PHONE_E164 = "+971567440057";
const WHATSAPP = "971567440057";
// Keep in step with HOURS in src/config.py (the hours published on the site).
const HOURS = "Monday to Friday, 9am to 6pm Gulf Standard Time";
const CONTACT_EMAIL = "philip@eastbridgestrategicpartners.com";

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

// Only an explicit tick counts. Browsers send value="yes" for a ticked box and
// nothing at all for an unticked one; anything else is treated as "no".
function isOptedIn(formName, data) {
  if (formName === "notes") return true; // subscribing is the request for notes
  const v = Array.isArray(data && data.marketing_opt_in) ? data.marketing_opt_in[0] : data && data.marketing_opt_in;
  return ["yes", "on", "true"].includes(String(v == null ? "" : v).trim().toLowerCase());
}

function marketingSource(formName, optedIn) {
  if (!optedIn) return "";
  return formName === "notes" ? "notes form" : `ticked box on ${formName} form`;
}

// Lead magnets that post to the "checklist" form (hidden field name="guide").
// Submissions from before the field existed carry no value and count as the original guide.
const GUIDES = ["villa-owner-checklist", "villa-snagging-checklist"];
function guideOf(data) {
  const v = String((Array.isArray(data && data.guide) ? data.guide[0] : data && data.guide) || "").trim();
  if (!v) return GUIDES[0];
  return GUIDES.includes(v) ? v : "unknown";
}

const asText = (v) => (Array.isArray(v) ? v.join(", ") : v == null ? "" : String(v)).slice(0, 5000);

// The "service" select on the contact form sends a service's short English name. A forged value
// is reduced to plain words so the log and the alert never carry markup.
function serviceOf(data) {
  return asText(data && data.service).replace(/[^\p{L}'’ ,\-]/gu, "").replace(/\s+/g, " ").trim().slice(0, 80);
}

// Campaign attribution fields (keep in step with ATTRIBUTION_FIELDS in build.py). Anyone can post any value,
// so each is reduced to the characters a UTM value or a click ID uses and capped in length.
const ATTRIBUTION = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid"];
function attributionOf(data) {
  const out = {};
  for (const k of ATTRIBUTION) {
    out[k] = asText(data && data[k]).replace(/[^A-Za-z0-9_.~%+:\/ \-]/g, "").replace(/\s+/g, " ").trim().slice(0, 150);
  }
  return out;
}

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

// Copy for the two acknowledgement emails. Everything except the first name is fixed text.
const ACK = {
  brief: {
    subject: "Your brief has reached Eastbridge",
    intro: "Thank you for sending us your brief. It has reached us safely and Philip Chapman, our founding partner, replies personally within one working day.",
    steps: [
      "We read your brief carefully.",
      "We arrange a free 30-minute call at a time that suits you.",
      "If we can help, we propose a fixed-fee first review, such as a plot review or a project health check, with the scope and fee in writing before we start. If we cannot, we say so and, where we can, point you to someone who can.",
    ],
    wa: "Hello Eastbridge, I have just sent a brief through your website.",
  },
  estimate: {
    subject: "Your estimate has reached Eastbridge",
    intro: "Thank you for sending us your estimate from our villa build cost calculator. Your inputs and the line-by-line result have reached us safely, and Philip Chapman, our founding partner, replies personally within one working day.",
    steps: [
      "Philip looks at your inputs, the result and any notes about the plot.",
      "He replies with a plain view of whether the figures look realistic for the plot and specification, and which lines carry the most risk.",
      "If a closer look would help, such as a plot review, we set out the scope and a fixed fee in writing before we start. A free 30-minute call is always available first.",
    ],
    wa: "Hello Eastbridge, I have just sent you an estimate from your villa cost calculator.",
  },
};

function briefEmail(firstName, optedIn) {
  return ackEmail("brief", firstName, optedIn);
}

function estimateEmail(firstName, optedIn) {
  return ackEmail("estimate", firstName, optedIn);
}

function ackEmail(kind, firstName, optedIn) {
  const copy = ACK[kind];
  const hello = firstName ? `Dear ${firstName},` : "Hello,";
  const booking = process.env.BOOKING_URL || "";
  const wa = waLink(copy.wa);
  const subject = copy.subject;

  const text = [
    hello,
    "",
    copy.intro,
    "",
    "What happens next:",
    ...copy.steps.map((t, i) => `${i + 1}. ${t}`),
    "",
    booking ? `If you would like to choose a time for that call now, you can book here: ${booking}` : "",
    `If it is urgent, message us on WhatsApp: ${wa}`,
    `Or call ${PHONE_DISPLAY} (${HOURS}).`,
    "",
    optedIn
      ? "Nothing you send is published, and it is shared only with the service providers named in our privacy notice. We use your details to reply to you and, as you asked, to send our occasional notes for villa owners, no more than once a month."
      : "Nothing you send is published, and it is shared only with the service providers named in our privacy notice. We use your details to reply to you.",
    optedIn ? `To stop the notes at any time, reply with "unsubscribe" or write to ${CONTACT_EMAIL}.` : "",
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
<p style="margin:0 0 16px">${esc(copy.intro)}</p>
<p style="margin:24px 0 8px;font-family:Arial,Helvetica,sans-serif;font-size:13px;letter-spacing:.1em;text-transform:uppercase">What happens next</p>
<ol style="margin:0 0 16px;padding-left:20px">
${copy.steps.map((t, i) => `<li${i < copy.steps.length - 1 ? ' style="margin-bottom:6px"' : ""}>${esc(t)}</li>`).join("\n")}
</ol>
<p style="margin:24px 0 8px">${booking ? btn(booking, "Choose a time to talk") : ""}${btn(wa, "Message us on WhatsApp")}</p>
<p style="margin:16px 0 0;font-size:15px">Or call <a href="tel:${PHONE_E164}" style="color:#1f2a2e">${PHONE_DISPLAY}</a>, ${esc(HOURS)}.</p>
<p style="margin:24px 0 0;font-size:14px;color:#5c6468">${optedIn
    ? `Nothing you send is published, and it is shared only with the service providers named in our privacy notice. We use your details to reply to you and, as you asked, to send our occasional notes for villa owners, no more than once a month. To stop the notes at any time, reply with "unsubscribe" or write to ${esc(CONTACT_EMAIL)}.`
    : "Nothing you send is published, and it is shared only with the service providers named in our privacy notice. We use your details to reply to you."}</p>
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
    `To unsubscribe at any time, or if you did not ask for this, reply with "unsubscribe" or write to ${CONTACT_EMAIL} and we will remove your address.`,
    "",
    "Eastbridge Strategic Partners",
    SITE,
  ].join("\n");
  const html = `<!doctype html><html lang="en"><body style="font-family:Georgia,'Times New Roman',serif;color:#1f2a2e;font-size:16px;line-height:1.6;max-width:560px;margin:24px auto;padding:0 16px">
<p>Hello,</p>
<p>Thank you for subscribing. We will send occasional notes on building and renovating a villa in Dubai and Abu Dhabi: costs, contracts, approvals and the questions worth asking. No more than one a month.</p>
<p style="color:#5c6468;font-size:14px">To unsubscribe at any time, or if you did not ask for this, reply with "unsubscribe" or write to ${esc(CONTACT_EMAIL)} and we will remove your address.</p>
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
    subject: `New ${formName} enquiry: ${lead.name || lead.email || "unknown"}${lead.area || lead.plot ? " (" + (lead.area || lead.plot) + ")" : ""}`.slice(0, 150),
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
  const optedIn = isOptedIn(formName, d);

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
    contact_method: asText(d.contact_method),
    // "brief" form, optional (Nov 2026): the service chosen (pre-selected from a service page's
    // enquiry link) and the property type and size. Both may be absent.
    service: serviceOf(d),
    property: asText(d.property).slice(0, 200),
    plot: asText(d.plot).slice(0, 300),
    estimate_inputs: asText(d.estimate_inputs).slice(0, 1000),
    estimate_result: asText(d.estimate_result).slice(0, 2000),
    estimate_link: asText(d.estimate_link).slice(0, 1000),
    currency: asText(d.currency).slice(0, 8),
    marketing_opt_in: optedIn ? "yes" : "no",
    marketing_source: marketingSource(formName, optedIn),
    page: referrer,
    language: langFromReferrer(referrer),
    submission_id: payload.id || "",
    // Which lead magnet a "checklist" submission came from. Only known slugs are kept, so the
    // log never carries free text typed into a forged field.
    guide: formName === "checklist" ? guideOf(d) : "",
    // Campaign details captured on landing (empty without analytics consent or a tagged link).
    ...attributionOf(d),
  };

  const results = {};

  // 1. Log first, so a lead is never lost even if email fails.
  try {
    const status = { brief: "New enquiry", estimate: "Estimate request", checklist: "Checklist download" }[formName] || "Subscriber";
    results.sheet = await logToSheet({ ...lead, status });
  } catch (e) {
    console.error("Sheet log failed:", e.message);
    results.sheet = { error: e.message };
  }

  // 2. Customer acknowledgement.
  const autoreplyOff = String(process.env.AUTOREPLY_DISABLED || "").toLowerCase() === "true";
  // "checklist" gets an email only when the visitor opted in to notes.
  const wantsAck = formName === "brief" || formName === "estimate" || formName === "notes" || (formName === "checklist" && optedIn);
  if (!autoreplyOff && isEmail(email) && wantsAck) {
    try {
      const first = safeFirstName(d.name);
      const msg = formName === "brief" ? briefEmail(first, optedIn) : formName === "estimate" ? estimateEmail(first, optedIn) : notesEmail();
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
  if (alertTo.length && (formName === "brief" || formName === "estimate")) {
    try {
      results.alert = await sendEmail({ to: alertTo, ...alertEmail(formName, lead), replyTo: isEmail(email) ? email : undefined });
    } catch (e) {
      console.error("Lead alert failed:", e.message);
      results.alert = { error: e.message };
    }
  }

  console.log("submission-created", formName, payload.id || "", ...(lead.guide ? ["guide=" + lead.guide] : []),
    "marketing_opt_in=" + lead.marketing_opt_in, JSON.stringify(results));
  // Always 200: the submission itself is already stored by Netlify Forms.
  return { statusCode: 200, body: JSON.stringify(results) };
};

// Exposed for tools/test_submission_function.js only.
exports._test = { isOptedIn, briefEmail, estimateEmail, notesEmail, alertEmail, guideOf, serviceOf, attributionOf };
