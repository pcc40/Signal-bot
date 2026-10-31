// Review check (October 2026 brief): pages x languages x widths, menu, overflow, contact buttons, tables, RTL,
// console errors; enquiry and checklist forms (every POST is aborted, nothing is sent); Quay House film; checklist PDF.
// Usage: python3 -m http.server 8767 --directory dist & node tools/review_check.js   (writes reports/screens/review2-*.png)
const { chromium } = require('playwright');
const BASE = 'http://127.0.0.1:8767';
const OUT = require('path').join(__dirname, '..', 'reports', 'screens');
const LANGS = ['', 'ar', 'ru', 'zh', 'hi'];
const PAGES = ['/', '/case-studies/island-e-waterfront-villa/', '/fees/', '/contact/', '/tools/villa-build-cost-calculator/',
  '/privacy/', '/guides/villa-owner-checklist/', '/about/', '/approach/', '/services/owners-representative/'];
const WIDTHS = [360, 390, 768, 1440];
const res = { pages: 0, fails: [], notes: [] };
const fail = m => { res.fails.push(m); console.log('FAIL ' + m); };

async function newCtx(b, w) {
  const ctx = await b.newContext({ viewport: { width: w, height: w < 900 ? 844 : 900 }, isMobile: w < 900, hasTouch: w < 900 });
  const posts = [];
  await ctx.route('**/*', r => {
    const req = r.request();
    if (req.method() === 'POST') { posts.push({ url: req.url(), body: req.postData() || '' }); return r.abort(); }
    const u = req.url();
    if (!u.startsWith(BASE)) return r.abort(); // keep the test offline: no analytics, no Vimeo
    return r.continue();
  });
  return { ctx, posts };
}

(async () => {
  const b = await chromium.launch();
  for (const w of WIDTHS) {
    const { ctx } = await newCtx(b, w);
    const p = await ctx.newPage();
    for (const lang of LANGS) for (const path of PAGES) {
      const url = BASE + (lang ? '/' + lang : '') + path;
      const errs = [];
      const onC = m => { if (m.type() === 'error' && !/net::ERR_FAILED|ERR_BLOCKED|Failed to load resource/.test(m.text())) errs.push(m.text()); };
      const onE = e => errs.push(String(e));
      p.on('console', onC); p.on('pageerror', onE);
      const r = await p.goto(url, { waitUntil: 'load' });
      await p.waitForTimeout(150);
      res.pages++;
      const tag = `${lang || 'en'} ${path} @${w}`;
      if (!r || r.status() !== 200) fail(`${tag}: HTTP ${r && r.status()}`);
      const info = await p.evaluate(() => {
        const de = document.documentElement;
        const vis = el => { const s = getComputedStyle(el), rc = el.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && rc.width > 0 && rc.height > 0; };
        const tables = Array.from(document.querySelectorAll('table')).map(t => {
          const wrap = t.parentElement; const ws = getComputedStyle(wrap);
          const fits = t.getBoundingClientRect().width <= de.clientWidth + 1;
          const scrolls = /auto|scroll/.test(ws.overflowX) && wrap.getBoundingClientRect().width <= de.clientWidth + 1;
          return fits || scrolls || getComputedStyle(t).display === 'block';
        });
        return { dir: de.dir, lang: de.lang, overflow: de.scrollWidth - de.clientWidth,
          contact: Array.from(document.querySelectorAll('a[href^="tel:"],a[href^="https://wa.me"],a[href$="/contact/"],a.btn')).some(vis),
          tablesBad: tables.filter(x => !x).length, tables: tables.length };
      });
      if (info.overflow > 1) fail(`${tag}: horizontal overflow ${info.overflow}px`);
      if (!info.contact) fail(`${tag}: no visible contact button`);
      if (info.tablesBad) fail(`${tag}: ${info.tablesBad}/${info.tables} tables wider than viewport without scroll wrapper`);
      if (lang === 'ar' && info.dir !== 'rtl') fail(`${tag}: dir=${info.dir}`);
      if (lang && lang !== 'ar' && info.dir === 'rtl') fail(`${tag}: unexpected rtl`);
      if (w < 900) {
        const t = await p.$('.menu-toggle');
        if (!t || !(await t.isVisible())) fail(`${tag}: menu toggle not visible`);
        else {
          await t.click(); await p.waitForTimeout(250);
          const open = await p.evaluate(() => { const n = document.getElementById('nav'); const a = n && n.querySelector('a'); const rc = a && a.getBoundingClientRect();
            return !!(rc && rc.width > 0 && rc.left >= -1 && rc.right <= document.documentElement.clientWidth + 1 && getComputedStyle(n).visibility !== 'hidden'); });
          const exp = await t.getAttribute('aria-expanded');
          if (!open) fail(`${tag}: menu did not open`);
          if (exp !== 'true') res.notes.push(`${tag}: aria-expanded=${exp} after opening`);
          const c = await p.$('.menu-close'); if (c && await c.isVisible()) await c.click(); else await p.keyboard.press('Escape');
        }
      }
      p.off('console', onC); p.off('pageerror', onE);
      if (errs.length) fail(`${tag}: console errors: ${errs.slice(0, 2).join(' | ')}`);
    }
    await ctx.close();
  }

  // Forms (English and Arabic)
  for (const lang of ['', 'ar']) {
    const { ctx, posts } = await newCtx(b, 390);
    const p = await ctx.newPage();
    const pre = lang ? '/' + lang : '';
    await p.goto(BASE + pre + '/contact/');
    // empty submit -> errors shown, no POST
    await p.click('#brief button[type=submit]'); await p.waitForTimeout(200);
    let inv = await p.$$eval('#brief .field.invalid', e => e.length);
    if (inv < 3 || posts.length) fail(`${lang || 'en'} contact: empty submit invalid=${inv} posts=${posts.length}`);
    await p.fill('#f-name', 'Test Person'); await p.fill('#f-email', 'test@example.com'); await p.fill('#f-msg', 'A villa project on a plot in Dubai Hills.');
    await p.check('input[name=contact_method][value=WhatsApp]');
    const phReq = await p.$eval('#f-phone', e => e.required);
    if (!phReq) fail(`${lang || 'en'} contact: phone not required after choosing WhatsApp`);
    await p.click('#brief button[type=submit]'); await p.waitForTimeout(200);
    const phInv = await p.$eval('#f-phone', e => e.getAttribute('aria-invalid'));
    if (phInv !== 'true' || posts.length) fail(`${lang || 'en'} contact: WhatsApp without phone accepted (posts=${posts.length})`);
    await p.check('input[name=contact_method][value=Email]');
    if (await p.$eval('#f-phone', e => e.required)) fail(`${lang || 'en'} contact: phone still required for Email`);
    await p.check('input[name=contact_method][value=WhatsApp]');
    await p.fill('#f-phone', '+971 50 000 0000');
    // without opt-in
    await p.click('#brief button[type=submit]'); await p.waitForTimeout(600);
    const a = posts.shift();
    if (!a) fail(`${lang || 'en'} contact: valid form did not submit`);
    else {
      const q = new URLSearchParams(a.body);
      if (q.get('form-name') !== 'brief' || q.has('marketing_opt_in') || q.get('contact_method') !== 'WhatsApp' || !q.get('phone')) fail(`${lang || 'en'} contact (no opt-in) body: ${a.body.slice(0, 200)}`);
      else res.notes.push(`${lang || 'en'} contact submit without opt-in intercepted: fields ${Array.from(q.keys()).join(',')}`);
    }
    await p.goto(BASE + pre + '/contact/');
    await p.fill('#f-name', 'Test Person'); await p.fill('#f-email', 'test@example.com'); await p.fill('#f-msg', 'A villa project on a plot in Dubai Hills.');
    await p.check('#f-mkt');
    await p.click('#brief button[type=submit]'); await p.waitForTimeout(600);
    const bb = posts.shift();
    if (!bb || new URLSearchParams(bb.body).get('marketing_opt_in') !== 'yes') fail(`${lang || 'en'} contact (opt-in) body: ${bb && bb.body.slice(0, 200)}`);
    else res.notes.push(`${lang || 'en'} contact submit with opt-in intercepted: marketing_opt_in=yes`);
    if (lang === '') await p.goto(BASE + '/contact/').then(async () => { await p.setViewportSize({ width: 360, height: 800 }); await p.waitForTimeout(300); await p.screenshot({ path: OUT + '/review2-contact-360.png' }); });

    // Checklist
    for (const opt of [false, true]) {
      await p.goto(BASE + pre + '/guides/villa-owner-checklist/');
      const f = 'form[data-guide]';
      const nm = await p.$(f + ' input[name=name]'); if (nm) await nm.fill('Test Person');
      await p.fill(f + ' input[name=email]', 'test@example.com');
      const st = await p.$(f + ' select[name=stage]'); if (st) { const v = await st.$$eval('option', o => (o.find(x => x.value) || {}).value); if (v) await st.selectOption(v); }
      if (opt) await p.check(f + ' input[name=marketing_opt_in]');
      await p.click(f + ' button[type=submit]'); await p.waitForTimeout(600);
      const c = posts.shift();
      const q = c && new URLSearchParams(c.body);
      if (!c || q.get('form-name') !== 'checklist' || (opt ? q.get('marketing_opt_in') !== 'yes' : q.has('marketing_opt_in'))) fail(`${lang || 'en'} checklist opt=${opt}: ${c && c.body.slice(0, 200)}`);
      else res.notes.push(`${lang || 'en'} checklist submit opt-in=${opt} intercepted: fields ${Array.from(q.keys()).join(',')}`);
    }
    await ctx.close();
  }

  // Video and downloads
  {
    const { ctx } = await newCtx(b, 1440);
    const p = await ctx.newPage();
    await p.goto(BASE + '/work/quay-house/');
    const v = await p.$('.video');
    if (!v) fail('quay-house: no .video element');
    else {
      const src = await v.getAttribute('data-src');
      const poster = await p.$eval('.video img', i => ({ ok: i.complete || true, src: i.currentSrc || i.src }));
      await p.$eval('.video', e => e.scrollIntoView()); await p.waitForTimeout(400);
      const nat = await p.$eval('.video img', i => i.naturalWidth);
      if (!nat) fail('quay-house: video poster did not load');
      await p.click('.video button'); await p.waitForTimeout(300);
      const fr = await p.$eval('.video iframe', f => f.src).catch(() => null);
      if (fr !== src) fail(`quay-house: iframe src ${fr} != ${src}`);
      else res.notes.push(`quay-house: poster loads (${poster.src.split('/').pop()}), play button inserts iframe ${fr}`);
    }
    for (const u of ['/assets/guides/villa-owner-checklist.pdf']) {
      const r = await p.request.get(BASE + u);
      const ct = r.headers()['content-type'];
      const body = await r.body();
      if (r.status() !== 200 || !body.slice(0, 5).toString().startsWith('%PDF')) fail(`${u}: ${r.status()} ${ct}`);
      else res.notes.push(`${u}: 200, ${ct}, ${body.length} bytes`);
    }
    for (const lang of LANGS) {
      await p.goto(BASE + (lang ? '/' + lang : '') + '/guides/villa-owner-checklist/thanks/');
      const hrefs = await p.$$eval('a[href$=".pdf"]', a => a.map(x => x.getAttribute('href')));
      if (!hrefs.length) fail(`${lang || 'en'} checklist thanks: no PDF link`);
      for (const h of hrefs) { const r = await p.request.get(new URL(h, p.url()).href); if (r.status() !== 200) fail(`${lang} pdf ${h}: ${r.status()}`); }
    }
    // Screenshots
    const shots = [['/', 1440, 'review2-home-desktop'], ['/', 390, 'review2-home-390'], ['/case-studies/island-e-waterfront-villa/', 390, 'review2-worked-example-390'],
      ['/fees/', 1440, 'review2-fees-desktop'], ['/fees/', 390, 'review2-fees-390'], ['/zh/tools/villa-build-cost-calculator/', 390, 'review2-calculator-zh-390'], ['/ar/', 390, 'review2-ar-home-390']];
    await ctx.close();
    for (const [u, w, n] of shots) {
      const { ctx: c2 } = await newCtx(b, w); const q = await c2.newPage();
      await q.goto(BASE + u, { waitUntil: 'load' }); await q.waitForTimeout(900);
      await q.screenshot({ path: `${OUT}/${n}.png`, fullPage: w < 900 && /calculator|worked|fees/.test(n) ? false : false });
      await c2.close();
    }
  }
  await b.close();
  console.log(`\nPAGES CHECKED: ${res.pages}  FAILURES: ${res.fails.length}`);
  res.notes.forEach(n => console.log('note ' + n));
  process.exit(res.fails.length ? 1 : 0);
})();
