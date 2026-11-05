// Critical CSS: the rules a page needs to draw its first screen, inlined in <head> by build.py so the first paint
// does not wait for the full stylesheet (Netlify reported First Contentful Paint "needs improvement").
//
//   python3 build.py && python3 tools/i18n.py apply && node tools/make_critical.js [--port 8793]
//
// Run it after every edit to site.css, after `sh tools/make_rtl.sh`, then build again. It serves dist/, opens every
// page (English at 390, 820 and 1440 px; ru/zh/hi and ar at 390 and 1440 px) and keeps each rule of the source
// stylesheet whose selector matches an element in the first 1.5 screens (hidden elements count where their nearest
// visible ancestor sits, so off-canvas menus and closed panels keep their "hidden" rules). Rules that JavaScript
// switches on (stuck header, open menu, cookie banner, reveal) are always kept. Rules are copied verbatim, in source
// order, so the cascade is unchanged when the full stylesheet arrives.
//
// Output: src/critical.json: per stylesheet (site.css for English, ru, zh and hi; site-rtl.css for ar) the md5 of
// the sheet and one cut per page group (home, insights, work, services, areas, tools, guides, other), so an article
// does not carry the calculator's first-screen rules. build.py and tools/i18n.py (via src/critical.py) inline a cut
// only while that hash matches the current sheet, and otherwise fall back to the ordinary render-blocking
// stylesheet, so a stale file can never leave a page half-styled.
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
const { spawn } = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const http = require('http');
const zlib = require('zlib');

const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');
const ASSETS = path.join(ROOT, 'src/static/assets');
const OUT = path.join(ROOT, 'src/critical.json');
// Page groups; keep in step with GROUPS in src/critical.py.
const GROUPS = ['insights', 'work', 'services', 'areas', 'tools', 'guides'];
function groupOf(u) {
  const seg = u.replace(/^\/(ar|ru|zh|hi)(?=\/)/, '').split('/')[1] || '';
  return seg === '' ? 'home' : (GROUPS.includes(seg) ? seg : 'other');
}
const args = process.argv.slice(2);
const PORT = Number(args.includes('--port') ? args[args.indexOf('--port') + 1] : 8793);
const FOLD = 1.5;                       // screens counted as "first screen", to allow for an early scroll
// Classes and attributes the site script toggles after load; their rules are always kept.
const ALWAYS = /\.(js|stuck|open|nav-open|is-in|in|on|invalid|is-sending|has-hero)\b|\[hidden\]|\[aria-expanded|:root\b|^html\b|^body\b|^\*/;

// ---------------------------------------------------------------- a small CSS splitter (no dependencies)
function stripComments(css) {
  let out = '', i = 0, q = null;
  while (i < css.length) {
    const c = css[i];
    if (q) { out += c; if (c === '\\') { out += css[i + 1] || ''; i += 2; continue; } if (c === q) q = null; i++; continue; }
    if (c === '"' || c === "'") { q = c; out += c; i++; continue; }
    if (c === '/' && css[i + 1] === '*') { const e = css.indexOf('*/', i + 2); i = e < 0 ? css.length : e + 2; continue; }
    out += c; i++;
  }
  return out;
}
// Splits a block body into top-level items: {prelude, body} for blocks, {stmt} for @statements.
function split(css) {
  const items = []; let i = 0;
  while (i < css.length) {
    while (i < css.length && /\s/.test(css[i])) i++;
    if (i >= css.length) break;
    let j = i, q = null, depth = 0, open = -1;
    for (; j < css.length; j++) {
      const c = css[j];
      if (q) { if (c === '\\') { j++; continue; } if (c === q) q = null; continue; }
      if (c === '"' || c === "'") { q = c; continue; }
      if (c === ';' && depth === 0 && open < 0) break;
      if (c === '{') { if (depth === 0) open = j; depth++; }
      else if (c === '}') { depth--; if (depth === 0) break; }
    }
    if (open < 0) { items.push({ stmt: css.slice(i, j + 1).trim() }); }
    else items.push({ prelude: css.slice(i, open).trim(), body: css.slice(open + 1, j).trim() });
    i = j + 1;
  }
  return items;
}
const GROUP = /^@(media|supports|layer|container)\b/i;
function parse(css) {
  return split(stripComments(css)).map(it => {
    if (it.prelude && GROUP.test(it.prelude)) return { ...it, children: split(it.body) };
    return it;
  });
}
// Selector used to test a rule: dynamic pseudo-classes and pseudo-elements removed.
function testable(sel) {
  return sel
    .replace(/::?(before|after|placeholder|marker|selection|first-letter|first-line|backdrop|file-selector-button|-webkit-[\w-]+|-moz-[\w-]+)(\([^)]*\))?/g, '')
    .replace(/:(hover|focus-visible|focus-within|focus|active|visited|target|checked|disabled|enabled|invalid|valid|user-invalid|placeholder-shown|autofill|-webkit-autofill)\b/g, '')
    .trim() || '*';
}
function selectorsOf(prelude) {
  // split on top-level commas (not inside parentheses)
  const out = []; let d = 0, cur = '';
  for (const c of prelude) { if (c === '(') d++; if (c === ')') d--; if (c === ',' && d === 0) { out.push(cur.trim()); cur = ''; } else cur += c; }
  if (cur.trim()) out.push(cur.trim());
  return out;
}

// ---------------------------------------------------------------- pages
function walk(dir, acc = []) {
  for (const f of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, f.name);
    if (f.isDirectory()) walk(p, acc); else if (f.name === 'index.html') acc.push('/' + path.relative(DIST, path.dirname(p)).split(path.sep).join('/') + (path.dirname(p) === DIST ? '' : '/'));
  }
  return acc;
}
function waitFor(url) {
  return new Promise((res, rej) => {
    const go = n => http.get(url, r => { r.resume(); res(); }).on('error', () => n ? setTimeout(() => go(n - 1), 200) : rej(new Error('server did not start')));
    go(50);
  });
}

async function collect(browser, sets, tests) {
  const hits = {};
  const queue = [];
  for (const [urls, widths] of sets) for (const u of urls) for (const w of widths) queue.push([u, w]);
  async function worker() {
    while (queue.length) {
      const [u, w] = queue.shift();
      const g = groupOf(u), hit = hits[g] || (hits[g] = new Set());
      const ctx = await browser.newContext({ viewport: { width: w, height: w < 600 ? 844 : 900 }, isMobile: w < 600, hasTouch: w < 600 });
      const page = await ctx.newPage();
      try {
        await page.goto(`http://127.0.0.1:${PORT}${u}`, { waitUntil: 'load', timeout: 60000 });
        await page.waitForTimeout(150);
        const found = await page.evaluate(([tests, fold]) => {
          const lim = innerHeight * fold, keep = [];
          const topOf = el => { let e = el; while (e && !e.getClientRects().length) e = e.parentElement; return e ? e.getBoundingClientRect().top + (getComputedStyle(e).position === 'fixed' ? 0 : scrollY) : 0; };
          for (const [i, s] of tests) {
            let els;
            try { els = document.querySelectorAll(s); } catch (e) { keep.push(i); continue; }
            for (const el of els) { if (topOf(el) < lim) { keep.push(i); break; } }
          }
          return keep;
        }, [tests.filter(([i]) => !hit.has(i)), FOLD]);
        found.forEach(i => hit.add(i));
      } catch (e) { console.error(`skip ${u} @${w}: ${e.message}`); }
      await ctx.close();
    }
  }
  await Promise.all([1, 2, 3, 4].map(worker));
  return hits;
}

function build(items, hit, keepAt) {
  // keepAt(item) -> true/false for a style rule; @font-face/@keyframes/@statements kept; @media print dropped.
  const out = [];
  for (const it of items) {
    if (it.stmt) { if (!/^@import/i.test(it.stmt)) out.push(it.stmt); continue; }
    if (it.children) {
      if (/^@media\s+print\b/i.test(it.prelude)) continue;
      const inner = build(it.children, hit, keepAt);
      if (inner) out.push(`${it.prelude}{${inner}}`);
      continue;
    }
    if (it.prelude.startsWith('@')) { out.push(`${it.prelude}{${it.body}}`); continue; }
    if (keepAt(it)) out.push(`${it.prelude}{${it.body}}`);
  }
  return out.join('\n');
}

async function forSheet(browser, file, sets) {
  const src = fs.readFileSync(path.join(ASSETS, file), 'utf8');
  const hash = crypto.createHash('md5').update(fs.readFileSync(path.join(ASSETS, file))).digest('hex').slice(0, 8);
  const items = parse(src);
  // every distinct testable selector gets an index
  const idx = new Map(); const tests = [];
  const visit = list => list.forEach(it => {
    if (it.children) return visit(it.children);
    if (!it.prelude || it.prelude.startsWith('@')) return;
    it.sels = selectorsOf(it.prelude).map(s => {
      const t = testable(s);
      if (!idx.has(t)) { idx.set(t, tests.length); tests.push([tests.length, t]); }
      return { raw: s, i: idx.get(t) };
    });
  });
  visit(items);
  const hits = await collect(browser, sets, tests);
  const groups = {};
  for (const g of Object.keys(hits).sort()) {
    const hit = hits[g];
    groups[g] = build(items, hit, it => it.sels.some(s => ALWAYS.test(s.raw) || hit.has(s.i)));
  }
  return { hash, groups };
}

(async () => {
  if (!fs.existsSync(path.join(DIST, 'index.html'))) { console.error('Build first: python3 build.py && python3 tools/i18n.py apply'); process.exit(1); }
  const all = walk(DIST);
  const en = all.filter(u => !/^\/(ar|ru|zh|hi)\//.test(u));
  const other = all.filter(u => /^\/(ru|zh|hi)\//.test(u));
  const ar = all.filter(u => /^\/ar\//.test(u));
  const srv = spawn('python3', ['-m', 'http.server', String(PORT), '--bind', '127.0.0.1', '--directory', DIST], { stdio: 'ignore' });
  let code = 0;
  try {
    await waitFor(`http://127.0.0.1:${PORT}/`);
    const browser = await chromium.launch();
    const jobs = [['site.css', [[en, [390, 820, 1440]], [other, [390, 1440]]]],
                  ['site-rtl.css', [[ar, [390, 820, 1440]]]]];
    const out = {};
    for (const [sheet, sets] of jobs) {
      if (!sets.reduce((a, s) => a + s[0].length, 0)) { console.error(`no pages for ${sheet}`); code = 1; continue; }
      out[sheet] = await forSheet(browser, sheet, sets);
      for (const [g, css] of Object.entries(out[sheet].groups))
        console.log(`${sheet} ${g}: ${Buffer.byteLength(css)} bytes, ${zlib.gzipSync(css).length} gzipped`);
    }
    if (!code) fs.writeFileSync(OUT, JSON.stringify(out, null, 1) + '\n');
    await browser.close();
  } catch (e) { console.error(e); code = 1; }
  srv.kill();
  process.exit(code);
})();
