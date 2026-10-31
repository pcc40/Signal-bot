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
//   - no unfilled {placeholder} is left in the output.
// On /ar/ /ru/ /zh/ /hi/ it repeats the arithmetic checks and looks for English calculator messages in the visible
// output. Missing translations are reported, not failed, unless --strict is given.
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
  }, o);
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
  const latinOnly = x => !/[A-Za-z]{2,}/.test(x.replace(/\{\w+\}/g, '').replace(/\bAED\b|\bsq ft\b/g, ''));
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
}

(async () => {
  const srv = spawn('python3', ['-m', 'http.server', String(PORT), '--bind', '127.0.0.1', '--directory', DIST], { stdio: 'ignore' });
  let browser;
  try {
    await waitFor(`http://127.0.0.1:${PORT}${CALC}`, 50);
    browser = await chromium.launch();
    const p = await browser.newPage();
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
