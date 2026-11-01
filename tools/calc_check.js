// Targeted check of the villa build cost calculator in a real browser.
//   python3 build.py && python3 tools/i18n.py apply && node tools/calc_check.js [--strict] [--port 8791]
// Serves dist/ on a local port, then on /tools/villa-build-cost-calculator/ exercises project type, specification,
// location, units and extras, and verifies that:
//   - every column total equals the sum of the cost lines shown, construction equals its lines, and the headline
//     figures match the table;
//   - switching sq ft <-> m² keeps the estimate unchanged and returns the same area;
//   - every renovation band ignores the area (input disabled) and shows the assessment prompt; luxury and
//     ultra-luxury renovation show only a starting (low) figure, with no likely or high figure;
//   - a new build with no built-up area shows no estimate;
//   - pool and garden choices are kept per project type when switching modes;
//   - no unfilled {placeholder} is left in the output;
//   - currency display: AED is the default; the AED figures behind the display never change; each converted line is
//     the AED line divided by the FX rate and rounded the same way, the converted columns add up and the converted
//     total is within rounding of AED total / rate; an "approximate, at rates of <date>" note is shown;
//   - the inputs round-trip through the URL (history.replaceState, read on load) and "Copy link" copies that URL;
//   - the WhatsApp link carries the one-line summary; the "estimate" form's hidden fields follow the calculator;
//   - the print stylesheet shows the letterhead and inputs, hides the form, and saves as a one-page A4 PDF.
// On /ar/ /ru/ /zh/ /hi/ it repeats the arithmetic checks and looks for English calculator messages in the visible
// output, checks the language's currencies (RUB on /ru/, CNY on /zh/, INR on /hi/), the WhatsApp text, the link round
// trip and the translated estimate form. Missing translations are reported, not failed, unless --strict is given.
// POST requests are aborted, so the checks never submit a form.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');

const args = process.argv.slice(2);
const STRICT = args.includes('--strict');
const PORT = Number((args[args.indexOf('--port') + 1] || '').match(/^\d+$/) ? args[args.indexOf('--port') + 1] : 8791);
const DIST = path.join(__dirname, '..', 'dist');
const CALC = '/tools/villa-build-cost-calculator/';
const LANGS = ['ar', 'ru', 'zh', 'hi'];

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

// Reads the table, headline and output text from the page. Numbers: keep digits only (works for any grouping).
async function snapshot(p) {
  return p.evaluate(() => {
    const clean = s => (s || '').replace(/[⁦-⁩]/g, '').trim();
    const n = s => { const d = clean(s).replace(/[^0-9]/g, ''); return d ? parseInt(d, 10) : 0; };
    const cell = (k, i) => { const el = document.querySelector(`[data-v="${k}-${i}"]`); return el ? n(el.textContent) : null; };
    const lines = ['build', 'basement', 'demo', 'pool', 'land', 'smart', 'design', 'permits', 'contingency', 'ffe'];
    const cols = [0, 1, 2].map(i => ({ lines: lines.map(k => cell(k, i)), total: cell('total', i) }));
    const out = document.getElementById('calc-out'), form = document.getElementById('calc');
    const visible = el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    // Only the nodes calc.js writes (static markup is covered by the normal translation workflow).
    const WRITTEN = '[data-v],[data-out],[data-tier-note],[data-unit],[data-time] li,[data-time-note],[data-route],[data-js-note],[data-row-label],[data-leg]';
    const texts = [];
    form.querySelectorAll(WRITTEN).forEach(el => { if (visible(el)) texts.push(clean(el.textContent)); });
    out.querySelectorAll(WRITTEN).forEach(el => { if (visible(el)) texts.push(clean(el.textContent)); });
    const area = document.querySelector('#c-area');
    return {
      cols, texts,
      likely: n(document.querySelector('[data-out="likely"]').textContent),
      low: n(document.querySelector('[data-out="low"]').textContent),
      high: n(document.querySelector('[data-out="high"]').textContent),
      area: area.value, areaDisabled: area.disabled, state: out.getAttribute('data-state'),
      likelyText: clean(document.querySelector('[data-out="likely"]').textContent),
      assess: visible(document.querySelector('[data-reno-assess]')) && !!document.querySelector('[data-reno-assess] a[href$="/contact/"]'),
      pool: document.querySelector('[name="pool"]').checked, garden: document.querySelector('#c-garden').value,
      output: clean(out.innerText),
      // AED value behind each displayed cell (calc.js writes data-aed), the display currency and the share outputs.
      aed: [0, 1, 2].map(i => lines.concat(['total']).map(k => { const el = document.querySelector(`[data-v="${k}-${i}"]`); return el && el.getAttribute('data-aed') ? Number(el.getAttribute('data-aed')) : 0; })),
      cur: out.getAttribute('data-cur') || 'AED',
      curSelect: (document.querySelector('#c-cur') || {}).value,
      curOptions: Array.from(document.querySelectorAll('#c-cur option')).map(o => o.value),
      fxNote: (() => { const el = document.querySelector('[data-fx-note]'); return el && !el.hidden ? clean(el.textContent) : ''; })(),
      wa: (() => { const a = document.querySelector('[data-wa-estimate]'); try { return a ? new URL(a.href).searchParams.get('text') : ''; } catch (e) { return ''; } })(),
      // Every other WhatsApp link on the page (phone action bar, floating button, header, footer) must carry the same text.
      waOthers: Array.from(document.querySelectorAll('a[href*="wa.me/"]')).filter(a => !a.hasAttribute('data-wa-estimate')).map(a => { try { return new URL(a.href).searchParams.get('text'); } catch (e) { return ''; } }),
      waBar: (() => { const a = document.querySelector('a.ab-wa'); try { return a ? new URL(a.href).searchParams.get('text') : null; } catch (e) { return ''; } })(),
      href: location.href,
      unit: (document.querySelector('input[name="unit"]:checked') || {}).value,
      checks: ['pool', 'smart', 'ffe', 'demo'].map(k => document.querySelector(`[name="${k}"]`).checked).join(','),
      sendFields: (() => { const fm = document.querySelector('form[name="estimate"]'); if (!fm) return null;
        return { inputs: fm.elements.estimate_inputs.value, result: fm.elements.estimate_result.value, link: fm.elements.estimate_link.value,
                 currency: fm.elements.currency.value, netlify: fm.hasAttribute('data-netlify'), formName: (fm.querySelector('input[name="form-name"]') || {}).value }; })(),
    };
  });
}

function checkSums(s, label) {
  let good = true;
  s.cols.forEach((c, i) => {
    const sum = c.lines.reduce((a, b) => a + (b || 0), 0);
    if (sum !== c.total) { good = false; fail(`${label}: column ${i} lines add to ${sum} but total shows ${c.total}`); }
  });
  if (s.state === 'low-only') {
    // Only the starting column is shown; likely and high columns must be blank, the headline is the starting total.
    if (s.cols[1].total || s.cols[2].total || s.high || s.likely !== s.cols[0].total || !s.cols[0].total) {
      good = false; fail(`${label}: starting-figure band shows likely/high figures or a headline that does not match the low total`);
    }
  } else if (s.likely !== s.cols[1].total || s.low !== s.cols[0].total || s.high !== s.cols[2].total) {
    good = false; fail(`${label}: headline ${s.low}/${s.likely}/${s.high} does not match table totals ${s.cols.map(c => c.total).join('/')}`);
  }
  if (/\{\w+\}/.test(s.output)) { good = false; fail(`${label}: unfilled placeholder in output`); }
  return good;
}

async function setInputs(p, o) {
  await p.evaluate(o => {
    const f = document.getElementById('calc');
    const fire = (el, t) => el.dispatchEvent(new Event(t, { bubbles: true }));
    const pick = (name, v) => { const el = f.querySelector(`input[name="${name}"][value="${v}"]`); if (el && !el.checked) { el.checked = true; fire(el, 'input'); fire(el, 'change'); } };
    if (o.mode) pick('mode', o.mode);
    if (o.unit) pick('unit', o.unit);
    if (o.tier) pick('tier', o.tier);
    if (o.loc) { f.elements.loc.value = o.loc; fire(f.elements.loc, 'change'); }
    ['area', 'basement', 'garden'].forEach(k => { if (o[k] != null) { const el = f.elements[k]; el.value = o[k]; fire(el, 'input'); fire(el, 'change'); } });
    ['pool', 'smart', 'ffe', 'demo'].forEach(k => { if (o[k] != null && f.elements[k].checked !== o[k]) { f.elements[k].checked = o[k]; fire(f.elements[k], 'change'); } });
    if (o.cur) { f.elements.cur.value = o.cur; fire(f.elements.cur, 'change'); }
  }, o);
}

// Currency: AED figures behind the display never change; each converted line is the AED line / rate, rounded like the
// AED lines; the converted columns still add up; the converted total is within rounding of AED total / rate.
const rnd = x => { const s = x >= 1e6 ? 1e4 : 1e3; return Math.round(x / s) * s; };
async function fxRates(p) { return p.evaluate(() => JSON.parse(document.getElementById('calc-data').textContent).fx); }
function checkCurrency(base, s, cur, fx, label) {
  let good = true;
  const rate = fx.aedPer[cur];
  if (!rate) { fail(`${label}: no FX rate for ${cur}`); return false; }
  if (s.cur !== cur || s.curSelect !== cur) { fail(`${label}: display currency is ${s.cur}/${s.curSelect}, expected ${cur}`); return false; }
  if (JSON.stringify(s.aed) !== JSON.stringify(base.aed)) { good = false; fail(`${label}: AED figures changed when switching to ${cur}`); }
  s.cols.forEach((c, i) => {
    const aedCol = base.aed[i];
    c.lines.forEach((v, n) => {
      if (!aedCol[n]) return;
      const want = rnd(aedCol[n] / rate);
      if (v !== want) { good = false; fail(`${label}: ${cur} line ${n} column ${i} shows ${v}, expected ${want} (AED ${aedCol[n]} / ${rate})`); }
    });
    const aedTot = aedCol[aedCol.length - 1];
    if (aedTot && c.total) {
      const step = aedTot / rate >= 1e6 ? 1e4 : 1e3;
      if (Math.abs(c.total - aedTot / rate) > 6 * step) { good = false; fail(`${label}: ${cur} total ${c.total} is not within rounding of AED ${aedTot} / ${rate}`); }
    }
  });
  if (!checkSums(s, label)) good = false;
  if (!s.fxNote || !/\d{4}/.test(s.fxNote)) { good = false; fail(`${label}: no "approximate, at rates of <date>" note beside ${cur} figures`); }
  return good;
}

// The expected English WhatsApp summary for a new build (mirrors compact() in calc.js).
function compactAED(x, sym) {
  x = rnd(x);
  const f = new Intl.NumberFormat('en-GB', { maximumFractionDigits: 2 });
  return x >= 1e6 ? `${sym}${f.format(x / 1e6)}m` : `${sym}${new Intl.NumberFormat('en-GB').format(Math.round(x / 1000))}k`;
}

// Saves the page as a PDF the way "Save as PDF" prints it and counts the pages.
async function pdfPages(p) {
  await p.emulateMedia({ media: 'print' });
  const buf = await p.pdf({ format: 'A4', preferCSSPageSize: true, printBackground: true });
  await p.emulateMedia({ media: 'screen' });
  return { pages: (buf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length, buf };
}

const SCENARIOS = [
  { mode: 'new', tier: 'standard', loc: 'palm-jumeirah', area: 4500, basement: 0, garden: 2000, pool: true, smart: false, ffe: false, demo: false },
  { mode: 'new', tier: 'ultra', loc: 'saadiyat', area: 9000, basement: 3000, garden: 5000, pool: true, smart: true, ffe: true, demo: true },
  { mode: 'new', tier: 'luxury', loc: 'abu-dhabi', area: 7000, basement: 0, garden: 0, pool: false, smart: true, ffe: false, demo: true },
  { mode: 'reno', tier: 'standard', loc: 'palm-jumeirah', smart: true, ffe: true },
  { mode: 'reno', tier: 'premium', loc: 'dubai', pool: true, garden: 1500 },
  { mode: 'reno', tier: 'luxury', loc: 'emirates-hills', area: 8000 },
  { mode: 'reno', tier: 'ultra', loc: 'hudayriyat', area: 12000, ffe: true },
  { mode: 'new', tier: 'premium', loc: 'dubai-hills-estate', area: 6000, basement: 0, garden: 3000, pool: true, smart: false, ffe: false, demo: false },
];

async function englishChecks(p) {
  await p.goto(`http://127.0.0.1:${PORT}${CALC}`, { waitUntil: 'load' });
  let s = await snapshot(p);
  if (checkSums(s, 'en initial')) ok('en initial render: totals equal the sum of the lines');
  for (const [i, sc] of SCENARIOS.entries()) {
    await setInputs(p, sc);
    s = await snapshot(p);
    if (checkSums(s, `en scenario ${i + 1} (${sc.mode}/${sc.tier}/${sc.loc})`)) ok(`en scenario ${i + 1} (${sc.mode}/${sc.tier}/${sc.loc}) reconciles`);
  }

  // Units: estimate preserved, area round-trips.
  await setInputs(p, { mode: 'new', tier: 'premium', unit: 'sqft', area: 6000, basement: 1200, garden: 3000 });
  const a = await snapshot(p);
  await setInputs(p, { unit: 'm2' });
  const b = await snapshot(p);
  await setInputs(p, { unit: 'sqft' });
  const c = await snapshot(p);
  if (a.likely === b.likely && a.low === b.low && a.high === b.high && b.likely === c.likely && c.area === '6000') ok(`units: sq ft -> m² -> sq ft keeps ${a.likely} and area 6000 (m² showed ${b.area})`);
  else fail(`units: estimate changed on unit switch (${a.likely} / ${b.likely} / ${c.likely}, area ${c.area})`);
  if (!checkSums(b, 'en in m²')) {}
  // Typing in m² then switching back keeps the same estimate.
  await setInputs(p, { unit: 'm2', area: 500 });
  const d = await snapshot(p);
  await setInputs(p, { unit: 'sqft' });
  const e = await snapshot(p);
  if (d.likely === e.likely && Math.abs(Number(e.area) - 500 * 10.7639) < 1) ok(`units: 500 m² typed -> ${e.area} sq ft, estimate unchanged`);
  else fail(`units: typed m² area did not convert cleanly (${d.likely} vs ${e.likely}, area ${e.area})`);

  // Renovation bands ignore the area.
  for (const tier of ['standard', 'premium', 'luxury', 'ultra']) {
    await setInputs(p, { mode: 'reno', tier });
    const r1 = await snapshot(p);
    await p.evaluate(() => { const el = document.querySelector('#c-area'); el.disabled = false; el.value = 20000; el.dispatchEvent(new Event('input', { bubbles: true })); });
    const r2 = await snapshot(p);
    if (r1.areaDisabled && r2.areaDisabled && r1.likely === r2.likely && r1.assess) ok(`renovation ${tier}: area disabled, not used, assessment prompt shown`);
    else fail(`renovation ${tier}: area handling wrong (disabled ${r1.areaDisabled}/${r2.areaDisabled}, ${r1.likely} vs ${r2.likely}, assess ${r1.assess})`);
  }
  for (const tier of ['luxury', 'ultra']) {
    await setInputs(p, { mode: 'reno', tier });
    const lx = await snapshot(p);
    if (lx.state === 'low-only' && lx.areaDisabled && lx.assess && !lx.high && lx.likely === lx.cols[0].total) ok(`renovation ${tier}: starting figure only (${lx.likelyText}), no likely or high figure`);
    else fail(`renovation ${tier}: expected a starting figure only (state ${lx.state}, high ${lx.high})`);
  }

  // New build with no built-up area: no estimate.
  await setInputs(p, { mode: 'new', tier: 'premium', unit: 'sqft', area: '', basement: 1500, garden: 2777, pool: true });
  const na = await snapshot(p);
  if (na.state === 'no-area' && na.likely === 0 && na.cols.every(c => !c.total)) ok('new build with no area: no estimate shown');
  else fail(`new build with no area: still shows an estimate (${na.likelyText})`);
  await setInputs(p, { area: 6000, basement: 0, garden: 3000 });

  // Extras kept per project type.
  await setInputs(p, { mode: 'reno', unit: 'sqft', tier: 'premium', pool: false, garden: 0 });
  await setInputs(p, { mode: 'new', pool: true, garden: 3000 });
  await setInputs(p, { mode: 'reno' });
  const m1 = await snapshot(p);
  await setInputs(p, { pool: true, garden: 800 });
  await setInputs(p, { mode: 'new' });
  const m2 = await snapshot(p);
  await setInputs(p, { mode: 'reno' });
  const m3 = await snapshot(p);
  if (!m1.pool && m1.garden === '0' && m2.pool && m2.garden === '3000' && m3.pool && m3.garden === '800') ok('modes: pool and garden kept separately for new build and renovation');
  else fail(`modes: extras not kept per mode (reno ${m1.pool}/${m1.garden}, new ${m2.pool}/${m2.garden}, reno again ${m3.pool}/${m3.garden})`);
  if (checkSums(m3, 'en after mode switches')) ok('modes: totals reconcile after switching');

  // Currency display.
  const fx = await fxRates(p);
  await setInputs(p, { mode: 'new', unit: 'sqft', tier: 'premium', loc: 'dubai-hills-estate', area: 6000, basement: 0, garden: 3000, pool: true, smart: false, ffe: false, demo: false, cur: 'AED' });
  const base = await snapshot(p);
  if (base.fxNote) fail('currency: AED shows an FX note');
  const enOpts = base.curOptions.join(',');
  if (enOpts === 'AED,GBP,USD,EUR' && base.curSelect === 'AED') ok('currency: English page offers AED (default), GBP, USD, EUR only');
  else fail(`currency: English page offers ${enOpts} (selected ${base.curSelect})`);
  for (const cur of ['GBP', 'USD', 'EUR']) {
    await setInputs(p, { cur });
    const s = await snapshot(p);
    if (checkCurrency(base, s, cur, fx, `en ${cur}`)) ok(`currency: ${cur} lines = AED / ${fx.aedPer[cur]} (rounded), AED unchanged, columns reconcile, note "${s.fxNote}"`);
  }
  for (const sc of [SCENARIOS[1], SCENARIOS[5], SCENARIOS[4]]) {
    await setInputs(p, { ...sc, cur: 'AED' });
    const b = await snapshot(p);
    await setInputs(p, { cur: 'EUR' });
    const s = await snapshot(p);
    if (checkCurrency(b, s, 'EUR', fx, `en EUR ${sc.mode}/${sc.tier}`)) ok(`currency: EUR correct for ${sc.mode}/${sc.tier} (state ${s.state})`);
  }
  await setInputs(p, { ...SCENARIOS[7], cur: 'AED' });
  const back = await snapshot(p);
  if (back.likely === base.likely && !back.fxNote) ok('currency: back to AED restores the original figures');
  else fail(`currency: back to AED shows ${back.likely}, expected ${base.likely}`);

  // WhatsApp summary.
  const wantWa = `Hello, I used your villa cost calculator: new build, 6,000 sq ft, Premium, Dubai Hills Estate, likely ${compactAED(back.likely, 'AED ')}. Could we talk it through?`;
  if (back.wa === wantWa) ok(`whatsapp: "${back.wa}"`);
  else fail(`whatsapp: got "${back.wa}", expected "${wantWa}"`);
  if (back.waBar === wantWa) ok('whatsapp: the phone action bar link (a.ab-wa) carries the summary');
  else fail(`whatsapp: a.ab-wa text is "${back.waBar}", expected "${wantWa}"`);
  if (back.waOthers.length && back.waOthers.every(t => t === wantWa)) ok(`whatsapp: all ${back.waOthers.length} other WhatsApp links carry the summary`);
  else fail(`whatsapp: other WhatsApp links differ: ${JSON.stringify(back.waOthers)}`);
  await setInputs(p, { cur: 'GBP' });
  const gw = await snapshot(p);
  if (gw.wa.includes(compactAED(gw.likely, '£')) && !/\{\w+\}/.test(gw.wa)) ok(`whatsapp in GBP: "${gw.wa}"`);
  else fail(`whatsapp in GBP: "${gw.wa}"`);
  await setInputs(p, { mode: 'reno', tier: 'luxury', cur: 'AED' });
  const rw = await snapshot(p);
  if (/renovation, Luxury, .*, from AED [\d.]+m/.test(rw.wa)) ok(`whatsapp renovation (starting figure): "${rw.wa}"`);
  else fail(`whatsapp renovation: "${rw.wa}"`);
  await setInputs(p, { mode: 'new', area: '' });
  const nw = await snapshot(p);
  if (nw.wa && !/likely|\{/.test(nw.wa)) ok('whatsapp with no estimate: generic message');
  else fail(`whatsapp with no estimate: "${nw.wa}"`);

  // Shareable link: the URL carries every input and reopens the same estimate.
  await setInputs(p, { mode: 'new', unit: 'm2', tier: 'luxury', loc: 'saadiyat', area: 650, basement: 120, garden: 400, pool: false, smart: true, ffe: true, demo: true, cur: 'USD' });
  const u1 = await snapshot(p);
  const q = new URL(u1.href).searchParams;
  if (['mode', 'tier', 'loc', 'unit', 'cur', 'area', 'basement', 'garden', 'pool', 'smart', 'ffe', 'demo'].every(k => q.has(k)) && q.get('cur') === 'USD' && q.get('unit') === 'm2') ok(`url: inputs written to the query string (${new URL(u1.href).search.slice(0, 80)}...)`);
  else fail(`url: query string incomplete: ${new URL(u1.href).search}`);
  const p2 = await p.context().newPage();
  await p2.goto(u1.href, { waitUntil: 'load' });
  const u2 = await snapshot(p2);
  const same = ['likely', 'low', 'high', 'area', 'unit', 'cur', 'checks', 'state'].every(k => u1[k] === u2[k]) && JSON.stringify(u1.aed) === JSON.stringify(u2.aed)
    && await p2.evaluate(() => document.querySelector('#c-loc').value) === 'saadiyat';
  if (same) ok(`url: reopening the link restores the estimate (${u2.likelyText}, ${u2.area} m², ${u2.cur})`);
  else fail(`url: round trip differs (${u1.likely}/${u2.likely}, area ${u1.area}/${u2.area}, cur ${u1.cur}/${u2.cur}, checks ${u1.checks}/${u2.checks})`);
  // Copy link puts the same URL on the clipboard.
  await p2.click('[data-copy-link]');
  await p2.waitForTimeout(200);
  const clip = await p2.evaluate(() => navigator.clipboard.readText().catch(() => ''));
  const st = await p2.evaluate(() => document.querySelector('[data-copy-status]').textContent);
  if (clip && new URL(clip).search === new URL(u1.href).search && st) ok(`copy link: clipboard holds the estimate URL; status "${st}"`);
  else fail(`copy link: clipboard "${clip}", status "${st}"`);
  // A forged or partial link falls back safely.
  await p2.goto(`http://127.0.0.1:${PORT}${CALC}?mode=reno&tier=bogus&loc=%3Cscript%3E&area=-5&cur=RUB&pool=1`, { waitUntil: 'load' });
  const u3 = await snapshot(p2);
  if (u3.cur === 'AED' && u3.state && checkSums(u3, 'en forged link')) ok('url: unknown tier, location and currency are ignored (RUB not offered on the English page)');
  else fail(`url: forged link not handled (cur ${u3.cur})`);
  await p2.close();

  // "Send this estimate to Philip": hidden fields follow the calculator; Netlify form registered on the English page.
  await setInputs(p, { ...SCENARIOS[7], unit: 'sqft', cur: 'GBP' });
  const sf = await snapshot(p);
  const f = sf.sendFields;
  if (f && f.netlify && f.formName === 'estimate' && f.currency === 'GBP' && f.link === sf.href.split('#')[0]
      && f.result.includes('likely ' + new Intl.NumberFormat('en-GB').format(sf.aed[1][10])) && /shown in GBP/.test(f.result) && /tier=premium/.test(f.inputs)) ok('send form: hidden fields carry the inputs, AED result, GBP figures and link');
  else fail(`send form: hidden fields wrong ${JSON.stringify(f)}`);

  // Save as PDF: one A4 page, with the letterhead and inputs, without the form.
  await setInputs(p, { ...SCENARIOS[1], cur: 'AED' });
  await p.evaluate(() => window.dispatchEvent(new Event('beforeprint')));
  await p.emulateMedia({ media: 'print' });
  const pr = await p.evaluate(() => {
    const vis = s => { const el = document.querySelector(s); return !!el && getComputedStyle(el).display !== 'none' && !!el.getClientRects().length; };
    return { head: vis('.calc-print-head'), foot: vis('.calc-print-foot'), form: vis('#calc'), send: vis('#send'), header: vis('.site-head'),
             inputs: document.querySelectorAll('[data-print-inputs] dt').length, date: document.querySelector('[data-print-date]').textContent };
  });
  await p.emulateMedia({ media: 'screen' });
  if (pr.head && pr.foot && !pr.form && !pr.send && !pr.header && pr.inputs >= 5 && pr.date) ok(`print: letterhead, ${pr.inputs} inputs, date "${pr.date}" and contact line shown; form, send section and site header hidden`);
  else fail(`print layout wrong ${JSON.stringify(pr)}`);
  for (const sc of [SCENARIOS[1], SCENARIOS[3]]) {
    await setInputs(p, { ...sc, cur: 'GBP' });
    const { pages } = await pdfPages(p);
    if (pages === 1) ok(`print: ${sc.mode}/${sc.tier} in GBP saves as a one-page PDF`);
    else fail(`print: ${sc.mode}/${sc.tier} saves as ${pages} pages`);
  }
  await setInputs(p, { ...SCENARIOS[7], cur: 'AED' });

  // Known English message fragments, for the leak check on translated pages.
  return p.evaluate(() => Array.from(document.querySelectorAll('#calc-msgs li')).map(li => ({
    key: li.getAttribute('data-m') || 'dev:' + li.getAttribute('data-dev'),
    text: li.textContent.replace(/\s+/g, ' ').trim(),
    ph: (li.textContent.match(/\{\w+\}/g) || []).sort().join(','),
  })));
}

async function langChecks(p, lang, en) {
  await p.goto(`http://127.0.0.1:${PORT}/${lang}${CALC}`, { waitUntil: 'load' });
  const dir = await p.evaluate(() => document.documentElement.dir);
  // Placeholders must survive translation.
  const tr = await p.evaluate(() => Array.from(document.querySelectorAll('#calc-msgs li')).map(li => ({
    key: li.getAttribute('data-m') || 'dev:' + li.getAttribute('data-dev'), text: li.textContent.replace(/\s+/g, ' ').trim(),
    ph: (li.textContent.match(/\{\w+\}/g) || []).sort().join(',') })));
  const byKey = Object.fromEntries(tr.map(t => [t.key, t]));
  const untranslated = [];
  // Terms TRANSLATION_BRIEF.md says stay in Latin script in every language ("AED", "sq ft", "m²").
  // A message made only of these, numbers and placeholders is correct when left unchanged.
  // Currency codes (and "US" in "US$") also stay in Latin script.
  const latinOnly = x => !/[A-Za-z]{2,}/.test(x.replace(/\{\w+\}/g, '').replace(/\b(AED|GBP|USD|EUR|RUB|CNY|INR|US)\b|\bsq ft\b/g, ''));
  en.forEach(m => {
    const t = byKey[m.key];
    if (!t) { fail(`${lang}: message ${m.key} missing from the page`); return; }
    if (t.ph !== m.ph) fail(`${lang}: message ${m.key} has placeholders "${t.ph}" instead of "${m.ph}"`);
    if (/[A-Za-z]{2,}/.test(m.text) && !latinOnly(m.text) && t.text === m.text && !m.key.startsWith('dev:')) untranslated.push(m.key);
  });
  // English fragments: the literal parts of each message with at least two words.
  const frags = [];
  en.filter(m => !m.key.startsWith('dev:')).forEach(m => m.text.split(/\{\w+\}/).forEach(x => {
    x = x.trim().replace(/^[·,;:.\s]+|[·,;:.\s]+$/g, '');
    if (x.split(/\s+/).length >= 2 && /[A-Za-z]{2,}/.test(x) && !latinOnly(x)) frags.push(x);
  }));
  const leaks = new Set();
  let sumsOk = true;
  for (const sc of SCENARIOS.concat([{ unit: 'm2' }, { mode: 'new', unit: 'm2', tier: 'luxury', basement: 100 }, { unit: 'sqft' }])) {
    await setInputs(p, sc);
    const s = await snapshot(p);
    if (!checkSums(s, `${lang} ${JSON.stringify(sc).slice(0, 60)}`)) sumsOk = false;
    const all = s.texts.join(' \n ');
    frags.forEach(fr => { if (all.includes(fr)) leaks.add(fr); });
  }
  if (sumsOk) ok(`${lang} (${dir}): totals reconcile in every scenario`);
  if (untranslated.length) report(`${lang}: ${untranslated.length} of ${en.length} calculator messages not yet translated (${untranslated.slice(0, 6).join(', ')}${untranslated.length > 6 ? ', ...' : ''})`);
  if (leaks.size) report(`${lang}: English calculator text visible: ${Array.from(leaks).slice(0, 4).map(x => JSON.stringify(x)).join('; ')}${leaks.size > 4 ? ` and ${leaks.size - 4} more` : ''}`);
  else ok(`${lang}: no English calculator messages visible`);

  // Currencies: GBP, USD, EUR everywhere, plus RUB on /ru/, CNY on /zh/, INR on /hi/; AED stays the default.
  const LOCAL = { ru: 'RUB', zh: 'CNY', hi: 'INR' };
  const want = ['AED', 'GBP', 'USD', 'EUR'].concat(LOCAL[lang] ? [LOCAL[lang]] : []).join(',');
  await setInputs(p, { mode: 'new', unit: 'sqft', tier: 'premium', loc: 'dubai-hills-estate', area: 6000, basement: 0, garden: 3000, pool: true, smart: false, ffe: false, demo: false, cur: 'AED' });
  const base = await snapshot(p);
  if (base.curOptions.join(',') === want && base.curSelect === 'AED') ok(`${lang}: currencies ${want}, AED by default`);
  else fail(`${lang}: currencies ${base.curOptions.join(',')} (selected ${base.curSelect}), expected ${want}`);
  const fx = await fxRates(p);
  for (const cur of ['GBP'].concat(LOCAL[lang] ? [LOCAL[lang]] : [])) {
    await setInputs(p, { cur });
    const s = await snapshot(p);
    if (checkCurrency(base, s, cur, fx, `${lang} ${cur}`)) ok(`${lang}: ${cur} conversion correct, AED unchanged`);
    const all = [s.fxNote].concat(s.texts).join(' \n ');
    frags.forEach(fr => { if (all.includes(fr)) report(`${lang} ${cur}: English calculator text visible: ${JSON.stringify(fr)}`); });
  }
  // WhatsApp summary: filled in, in the page language.
  await setInputs(p, { cur: 'AED' });
  const w = await snapshot(p);
  const waLeaks = frags.filter(fr => w.wa.includes(fr));
  if (!w.wa || /\{\w+\}/.test(w.wa) || !w.wa.includes(new Intl.NumberFormat('en-GB', { maximumFractionDigits: 2 }).format(rnd(w.likely) / 1e6))) fail(`${lang}: WhatsApp text not filled in: "${w.wa}"`);
  else if (waLeaks.length) report(`${lang}: WhatsApp text still in English: "${w.wa}"`);
  else ok(`${lang}: WhatsApp text "${w.wa}"`);
  // URL round trip in the local currency.
  if (LOCAL[lang]) {
    await setInputs(p, { cur: LOCAL[lang], tier: 'luxury', unit: 'm2' });
    const a = await snapshot(p);
    const p2 = await p.context().newPage();
    await p2.goto(a.href, { waitUntil: 'load' });
    const b = await snapshot(p2);
    await p2.close();
    if (a.likely === b.likely && b.cur === LOCAL[lang] && b.unit === 'm2') ok(`${lang}: link reopens the estimate in ${LOCAL[lang]}`);
    else fail(`${lang}: link round trip differs (${a.likely}/${b.likely}, ${b.cur}, ${b.unit})`);
    await setInputs(p, { cur: 'AED', unit: 'sqft' });
  }
  // Translated pages post to the English form registration (tools/i18n.py tag_forms).
  const sf = base.sendFields;
  if (sf && !sf.netlify && sf.formName === 'estimate') ok(`${lang}: estimate form posts via form-name (no data-netlify on the translated page)`);
  else fail(`${lang}: estimate form attributes wrong ${JSON.stringify(sf && { netlify: sf.netlify, formName: sf.formName })}`);
}

(async () => {
  const srv = spawn('python3', ['-m', 'http.server', String(PORT), '--bind', '127.0.0.1', '--directory', DIST], { stdio: 'ignore' });
  let browser;
  try {
    await waitFor(`http://127.0.0.1:${PORT}${CALC}`, 50);
    browser = await chromium.launch();
    const ctx = await browser.newContext({ permissions: ['clipboard-read', 'clipboard-write'] });
    const p = await ctx.newPage();
    // Never submit anything from the checks.
    await ctx.route(u => u.hostname === '127.0.0.1', r => r.request().method() === 'POST' ? r.abort() : r.continue());
    const errors = [];
    p.on('pageerror', e => errors.push(e.message));
    p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    const en = await englishChecks(p);
    for (const lang of LANGS) await langChecks(p, lang, en);
    if (errors.length) fail('script errors: ' + errors.slice(0, 3).join(' | '));
  } catch (e) {
    fail(e.stack || String(e));
  } finally {
    if (browser) await browser.close();
    srv.kill();
  }
  console.log(`\n${failures} failure(s), ${reports} translation note(s)${STRICT ? ' (strict)' : ''}`);
  process.exit(failures ? 1 : 0);
})();
