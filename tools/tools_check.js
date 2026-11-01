// Browser check of the three owner tools (src/pages_owner_tools.py + src/static/assets/tools.js):
//   /tools/renovate-or-rebuild/  /tools/stage-payment-planner/  /tools/delay-cost-estimator/
//   python3 build.py && python3 tools/i18n.py apply && node tools/tools_check.js [--strict] [--port 8792]
// Serves dist/ on a local port and, for each tool in English, verifies that:
//   - the figures tools.js writes on load are identical to the server-rendered example (the Python and JavaScript
//     arithmetic agree);
//   - in every scenario each low/likely/high column of cost lines adds up to its total, the headline matches the
//     table, and no NaN, Infinity, undefined or unfilled {placeholder} appears;
//   - renovate or rebuild: switching sq ft <-> m² leaves every total unchanged; luxury renovation shows a starting
//     figure only;
//   - stage payments: the schedule pays exactly the contract sum, work valued adds up to the contract sum, the
//     advance is fully recovered, retention is fully released, and the headline is the largest monthly payment;
//   - delay cost: the total for the delay is the monthly total times the number of months;
//   - "Save as PDF" prints the letterhead and inputs without the form, on one A4 page (two for the payment schedule);
//   - tools.js never asks for a message that is missing from #tool-msgs (it logs a console error).
// On /ar/ /ru/ /zh/ /hi/ it repeats the arithmetic, checks every message keeps its {placeholders}, and reports
// messages still in English and English message text visible in the output (failures with --strict).
// POST requests are aborted, so nothing is ever submitted.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');

const args = process.argv.slice(2);
const STRICT = args.includes('--strict');
const pi = args.indexOf('--port');
const PORT = pi >= 0 && /^\d+$/.test(args[pi + 1] || '') ? Number(args[pi + 1]) : 8792;
const DIST = path.join(__dirname, '..', 'dist');
const LANGS = ['ar', 'ru', 'zh', 'hi'];
const TOOLS = { rr: '/tools/renovate-or-rebuild/', sp: '/tools/stage-payment-planner/', dc: '/tools/delay-cost-estimator/' };

let failures = 0, reports = 0;
function fail(m) { failures++; console.log('FAIL  ' + m); }
function report(m) { reports++; console.log((STRICT ? 'FAIL  ' : 'note  ') + m); if (STRICT) failures++; }
function ok(m) { console.log('ok    ' + m); }

function waitFor(url, tries) {
  return new Promise((res, rej) => {
    const go = n => http.get(url, r => { r.resume(); res(); }).on('error', () => n ? setTimeout(() => go(n - 1), 200) : rej(new Error('server did not start')));
    go(tries);
  });
}

// Text of every node tools.js writes, keyed by its data attribute (schedule rows by position).
async function written(p) {
  return p.evaluate(() => {
    const clean = s => (s || '').replace(/[⁦-⁩]/g, '').replace(/\s+/g, ' ').trim();
    const o = {};
    document.querySelectorAll('#tool-out [data-v], #tool-out [data-out]').forEach(el => { o[el.getAttribute('data-v') || 'out:' + el.getAttribute('data-out')] = clean(el.textContent); });
    document.querySelectorAll('[data-schedule] tr').forEach((tr, i) => { o['row:' + i] = Array.from(tr.children).map(c => clean(c.textContent)).join(' | '); });
    return o;
  });
}

// Digits only (works for any grouping); '–' and empty give null.
async function numbers(p) {
  return p.evaluate(() => {
    const n = s => { const d = (s || '').replace(/[⁦-⁩]/g, '').replace(/[^0-9]/g, ''); return d ? parseInt(d, 10) : null; };
    const o = {};
    document.querySelectorAll('#tool-out [data-v], #tool-out [data-out]').forEach(el => { o[el.getAttribute('data-v') || 'out:' + el.getAttribute('data-out')] = n(el.textContent); });
    o.rows = Array.from(document.querySelectorAll('[data-schedule] tr')).map(tr => Array.from(tr.querySelectorAll('td')).map(td => n(td.textContent)));
    o.state = document.getElementById('tool-out').getAttribute('data-state');
    o.text = document.getElementById('tool-out').innerText;
    return o;
  });
}

async function setInputs(p, o) {
  await p.evaluate(o => {
    const f = document.getElementById('tool-form');
    const fire = (el, t) => el.dispatchEvent(new Event(t, { bubbles: true }));
    Object.keys(o).forEach(k => {
      const v = o[k];
      const radio = f.querySelector(`input[type="radio"][name="${k}"][value="${v}"]`);
      if (radio) { radio.checked = true; fire(radio, 'input'); fire(radio, 'change'); return; }
      const el = f.elements[k];
      if (!el) throw new Error('no input ' + k);
      if (el.type === 'checkbox') { el.checked = !!v; fire(el, 'change'); }
      else { el.value = v; fire(el, 'input'); fire(el, 'change'); }
    });
  }, o);
}

function bad(s, label) {
  if (/NaN|Infinity|undefined|\{\w+\}/.test(s.text)) { fail(`${label}: NaN, Infinity, undefined or a placeholder in the output`); return true; }
  return false;
}

function colSum(s, prefix, lines, n) { return lines.reduce((a, k) => a + (s[`${prefix}${k}-${n}`] || 0), 0); }

function checkRR(s, label) {
  let good = !bad(s, label);
  const sides = { rn: ['works', 'design', 'permits', 'contingency', 'living'], nb: ['demo', 'build', 'design', 'permits', 'contingency', 'living'] };
  if (s.state === 'no-area') return good;
  for (const side of Object.keys(sides)) {
    for (let n = 0; n < 3; n++) {
      if (side === 'rn' && s.state === 'low-only' && n > 0) {
        if (s[`rn-total-${n}`] !== null) { good = false; fail(`${label}: luxury renovation shows a ${n === 1 ? 'likely' : 'high'} figure`); }
        continue;
      }
      const sum = colSum(s, side + '-', sides[side], n);
      if (sum !== s[`${side}-total-${n}`]) { good = false; fail(`${label}: ${side} column ${n} lines add to ${sum}, total shows ${s[`${side}-total-${n}`]}`); }
    }
    const c = side === 'rn' && s.state === 'low-only' ? 0 : 1;
    if (s[`out:${side}-likely`] !== s[`${side}-total-${c}`] || s[`out:${side}-low`] !== s[`${side}-total-0`]) { good = false; fail(`${label}: ${side} headline does not match the table`); }
  }
  return good;
}

function checkSP(s, label, contract) {
  let good = !bad(s, label);
  if (!contract) return good;
  const rows = s.rows;           // advance, months..., handover, final; columns: value, ret, rec, pay, paid, held, unrec
  const months = rows.slice(1, -2);
  const pays = rows.reduce((a, r) => a + (r[3] || 0), 0);
  const value = months.reduce((a, r) => a + r[0], 0), ret = months.reduce((a, r) => a + r[1], 0), rec = months.reduce((a, r) => a + r[2], 0);
  const adv = rows[0][3], last = rows[rows.length - 1];
  const checks = [
    [pays === contract, `payments add to ${pays}, not the contract sum ${contract}`],
    [value === contract, `work valued adds to ${value}, not ${contract}`],
    [rec === adv, `advance recovered ${rec} differs from the advance ${adv}`],
    [ret === rows[rows.length - 2][3] + last[3], `retention held back ${ret} differs from retention released ${rows[rows.length - 2][3] + last[3]}`],
    [last[4] === contract && last[5] === 0 && last[6] === 0, 'schedule does not end fully paid with nothing held'],
    [months[months.length - 1][6] === 0, 'advance not fully recovered by the last month'],
    [s['sum-pay'] === contract && s['sum-value'] === contract, 'totals row does not show the contract sum'],
    [s.state === 'range', 'state not set'],
  ];
  months.forEach((r, i) => { if (r[0] - r[1] - r[2] !== r[3]) checks.push([false, `month ${i + 1}: value less retention less recovery is not the payment`]); });
  const peak = Math.max(...months.map(r => r[3]));
  const prof = s.profile;
  const col = { even: 0, s: 1, peak: 2 }[prof];
  checks.push([s[`peak-${col}`] !== null && String(s[`peak-${col}`]).startsWith(String(peak)), `key figures (${prof}) do not show the busiest month ${peak}`]);
  checks.forEach(([c, m]) => { if (!c) { good = false; fail(`${label}: ${m}`); } });
  return good;
}

function checkDC(s, label, months) {
  let good = !bad(s, label);
  const lines = ['housing', 'finance', 'escalation', 'prelims', 'fees'];
  for (let n = 0; n < 3; n++) {
    const sum = colSum(s, '', lines, n);
    if (sum !== s[`total-${n}`]) { good = false; fail(`${label}: column ${n} lines add to ${sum}, total shows ${s[`total-${n}`]}`); }
    if ((s[`total-${n}`] || 0) * months !== (s[`over-${n}`] || 0)) { good = false; fail(`${label}: total for the delay ${s[`over-${n}`]} is not ${months} x ${s[`total-${n}`]}`); }
  }
  if (s['out:likely'] !== s['total-1'] || s['out:low'] !== s['total-0'] || s['out:high'] !== s['total-2']) { good = false; fail(`${label}: headline does not match the table`); }
  return good;
}

const RR_SCEN = [
  { unit: 'sqft', area: 6000, newArea: 6000, scope: 'mid', tier: 'premium', living: true, rent: 28600 },
  { scope: 'basic', tier: 'standard', area: 3500, newArea: 4200 },
  { scope: 'lux', tier: 'luxury', area: 9000, newArea: 12000, living: false },
  { scope: 'mid', tier: 'ultra', area: 12000, newArea: 12000, living: true, rent: 60000 },
  { area: '', newArea: '' },
  { area: 6000, newArea: '', scope: 'mid', tier: 'premium' },
];
const SP_SCEN = [
  { contract: 5115000, months: 12, advance: 10, retention: 10, dlp: 12, profile: 's' },
  { contract: 3333333, months: 7, advance: 20, retention: 5, dlp: 12, profile: 'even' },
  { contract: 12750000, months: 22, advance: 15, retention: 10, dlp: 24, profile: 'peak' },
  { contract: 999999, months: 1, advance: 0, retention: 7.5, dlp: 6, profile: 's' },
  { contract: 4800000, months: 18, advance: 12.5, retention: 0, dlp: 0, profile: 'peak' },
];
const DC_SCEN = [
  { months: 3, loc: 'dubai', rent: 28600, borrowed: 2550000, rate: 3.9, remaining: 2550000, prelims: false, contract: 5115000, fees: 0 },
  { months: 6, loc: 'ad', rent: 45600, borrowed: 0, rate: 7.25, remaining: 4000000, prelims: true, contract: 8000000, fees: 28000 },
  { months: 1, loc: 'dubai', rent: 0, borrowed: 1000000, rate: 6, remaining: 0, prelims: true, contract: 3000000, fees: 15000 },
  { months: 0, loc: 'dubai', rent: 17700 },
];

async function runScenarios(p, kind, label) {
  let good = true;
  if (kind === 'rr') {
    for (const sc of RR_SCEN) {
      await setInputs(p, sc);
      if (!checkRR(await numbers(p), `${label} rr ${JSON.stringify(sc).slice(0, 70)}`)) good = false;
    }
    // Units: the same estimate in m².
    await setInputs(p, RR_SCEN[0]);
    const a = await numbers(p);
    await setInputs(p, { unit: 'm2' });
    const b = await numbers(p);
    const same = ['rn-total-0', 'rn-total-1', 'rn-total-2', 'nb-total-0', 'nb-total-1', 'nb-total-2'].every(k => a[k] === b[k]);
    const area = await p.evaluate(() => document.querySelector('[name="area"]').value);
    await setInputs(p, { unit: 'sqft' });
    const back = await p.evaluate(() => document.querySelector('[name="area"]').value);
    if (same && area === '557' && back === '6000') ok(`${label} rr: sq ft <-> m² keeps every total (6,000 sq ft = ${area} m²)`);
    else { good = false; fail(`${label} rr: unit switch changes the estimate or the area (${area}, back ${back})`); }
    await setInputs(p, { scope: 'lux' });
    const l = await numbers(p);
    if (l.state === 'low-only') ok(`${label} rr: luxury renovation shows a starting figure only`); else { good = false; fail(`${label} rr: luxury renovation state ${l.state}`); }
    await setInputs(p, RR_SCEN[0]);
  } else if (kind === 'sp') {
    for (const sc of SP_SCEN) {
      await setInputs(p, sc);
      const s = await numbers(p);
      s.profile = sc.profile;
      if (!checkSP(s, `${label} sp ${JSON.stringify(sc).slice(0, 70)}`, Math.round(sc.contract))) good = false;
    }
    await setInputs(p, { contract: '' });
    const z = await numbers(p);
    if (z.state === 'no-contract' && !bad(z, `${label} sp empty`)) ok(`${label} sp: no contract sum shows no schedule`); else { good = false; fail(`${label} sp: empty contract state ${z.state}`); }
    await setInputs(p, SP_SCEN[0]);
  } else {
    for (const sc of DC_SCEN) {
      await setInputs(p, sc);
      if (!checkDC(await numbers(p), `${label} dc ${JSON.stringify(sc).slice(0, 70)}`, sc.months)) good = false;
    }
    await setInputs(p, DC_SCEN[0]);
  }
  return good;
}

async function messages(p) {
  return p.evaluate(() => Array.from(document.querySelectorAll('#tool-msgs li')).map(li => ({
    key: li.getAttribute('data-m'), text: li.textContent.replace(/\s+/g, ' ').trim(),
    ph: (li.textContent.match(/\{\w+\}/g) || []).sort().join(',') })));
}

async function pdfPages(p) {
  await p.emulateMedia({ media: 'print' });
  const shown = await p.evaluate(() => {
    const vis = el => !!el && getComputedStyle(el).display !== 'none';
    return { head: vis(document.querySelector('.calc-print-head')), form: vis(document.getElementById('tool-form')),
             inputs: document.querySelectorAll('[data-print-inputs] dt').length, date: (document.querySelector('[data-print-date]') || {}).textContent || '' };
  });
  const buf = await p.pdf({ format: 'A4', preferCSSPageSize: true, printBackground: true });
  await p.emulateMedia({ media: 'screen' });
  return { pages: (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length, ...shown };
}

(async () => {
  const srv = spawn('python3', ['-m', 'http.server', String(PORT), '--bind', '127.0.0.1', '--directory', DIST], { stdio: 'ignore' });
  let browser;
  try {
    await waitFor(`http://127.0.0.1:${PORT}/tools/`, 50);
    browser = await chromium.launch();
    const ctx = await browser.newContext();
    const nojs = await browser.newContext({ javaScriptEnabled: false });
    for (const c of [ctx, nojs]) await c.route(u => u.hostname === '127.0.0.1', r => r.request().method() === 'POST' ? r.abort() : r.continue());
    const p = await ctx.newPage(), pn = await nojs.newPage();
    const errors = [];
    p.on('pageerror', e => errors.push(e.message));
    p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    for (const [kind, url] of Object.entries(TOOLS)) {
      // 1. The server-rendered example and the script's first render agree.
      await pn.goto(`http://127.0.0.1:${PORT}${url}`, { waitUntil: 'load' });
      await p.goto(`http://127.0.0.1:${PORT}${url}`, { waitUntil: 'load' });
      const a = await written(pn), b = await written(p);
      const diff = Object.keys(a).filter(k => a[k] !== b[k]);
      if (!diff.length && Object.keys(a).length > 10) ok(`${kind}: script output on load matches the server-rendered example (${Object.keys(a).length} values)`);
      else fail(`${kind}: server and script differ on ${diff.slice(0, 5).map(k => `${k}: "${a[k]}" vs "${b[k]}"`).join('; ')}`);
      // 2. Arithmetic in every scenario.
      if (await runScenarios(p, kind, 'en')) ok(`${kind}: totals reconcile in every scenario, no NaN or placeholders`);
      // 3. Print.
      const pr = await pdfPages(p);
      const maxPages = kind === 'sp' ? 2 : 1;
      if (pr.head && !pr.form && pr.inputs >= 3 && pr.date && pr.pages <= maxPages) ok(`${kind}: Save as PDF prints letterhead, ${pr.inputs} inputs and the date on ${pr.pages} page(s)`);
      else fail(`${kind}: print layout wrong ${JSON.stringify(pr)}`);
      const en = await messages(p);
      // English fragments of each message (two or more words), for the leak check.
      const latinOnly = x => !/[A-Za-z]{2,}/.test(x.replace(/\{\w+\}/g, '').replace(/\b(AED|US)\b|\bsq ft\b/g, ''));
      const frags = [];
      en.forEach(m => m.text.split(/\{\w+\}/).forEach(x => {
        x = x.trim().replace(/^[·,;:.()\s]+|[·,;:.()\s]+$/g, '');
        if (x.split(/\s+/).length >= 2 && /[A-Za-z]{2,}/.test(x) && !latinOnly(x)) frags.push(x);
      }));
      for (const lang of LANGS) {
        await p.goto(`http://127.0.0.1:${PORT}/${lang}${url}`, { waitUntil: 'load' });
        const tr = Object.fromEntries((await messages(p)).map(m => [m.key, m]));
        const untranslated = [];
        en.forEach(m => {
          const t = tr[m.key];
          if (!t) { fail(`${lang} ${kind}: message ${m.key} missing`); return; }
          if (t.ph !== m.ph) fail(`${lang} ${kind}: message ${m.key} has placeholders "${t.ph}" instead of "${m.ph}"`);
          if (/[A-Za-z]{2,}/.test(m.text) && !latinOnly(m.text) && t.text === m.text) untranslated.push(m.key);
        });
        if (await runScenarios(p, kind, lang)) ok(`${lang} ${kind}: totals reconcile in every scenario`);
        const shown = await p.evaluate(() => document.getElementById('tool-out').innerText);
        const leaks = frags.filter(fr => shown.includes(fr));
        if (untranslated.length) report(`${lang} ${kind}: ${untranslated.length} of ${en.length} messages not yet translated (${untranslated.slice(0, 5).join(', ')}${untranslated.length > 5 ? ', ...' : ''})`);
        if (leaks.length) report(`${lang} ${kind}: English tool text visible: ${leaks.slice(0, 3).map(x => JSON.stringify(x)).join('; ')}${leaks.length > 3 ? ` and ${leaks.length - 3} more` : ''}`);
        else ok(`${lang} ${kind}: no English tool messages visible`);
      }
    }
    if (errors.length) fail('script errors: ' + errors.slice(0, 3).join(' | '));
    else ok('no script errors or missing messages');
  } catch (e) {
    fail(e.stack || String(e));
  } finally {
    if (browser) await browser.close();
    srv.kill();
  }
  console.log(`\n${failures} failure(s), ${reports} translation note(s)${STRICT ? ' (strict)' : ''}`);
  process.exit(failures ? 1 : 0);
})();
