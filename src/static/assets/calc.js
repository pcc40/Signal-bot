/* Eastbridge villa build and renovation cost calculator.
   Rates come from the JSON block #calc-data (generated from src/pages_tools.py RATES and FX).
   Every word the script shows comes from the hidden message list #calc-msgs, or from labels already on the page,
   which the i18n pipeline translates with the rest of the page; this file holds no user-facing text.
   Areas are kept internally in square feet (data-sqft on each input), so switching units never changes the estimate.
   Every estimate is calculated in AED. Other currencies are display-only conversions at the fixed FX rates; each
   converted line is rounded like the AED lines and the converted totals are the sums of those lines.
   The inputs are mirrored to the URL query string (history.replaceState) and read back on load, so a link
   reopens the same estimate. The server renders the worked example; this script updates the same nodes in place. */
(function () {
  var f = document.getElementById('calc'), d = document.getElementById('calc-data'), out = document.getElementById('calc-out'),
      M = document.getElementById('calc-msgs');
  if (!f || !d || !out || !M) return;
  var R = JSON.parse(d.textContent), K = R.sqftPerM2, FX = R.fx || { aedPer: {} };
  var root = document.documentElement, RTL = root.dir === 'rtl', LANG = root.lang || 'en-GB', LANG0 = LANG.split('-')[0];
  var unit = 'sqft', cur = 'AED';
  var LINES = ['build', 'basement', 'demo', 'pool', 'land', 'smart', 'design', 'permits', 'contingency', 'ffe'];
  var CONS = LINES.slice(0, 6);
  var AREAS = ['area', 'basement', 'garden'], CHECKS = ['pool', 'smart', 'ffe', 'demo'];
  root.classList.add('calc-page');

  /* ---------- messages and number formatting ---------- */
  // One number style in every language (Latin digits, comma grouping), matching the figures rendered on the server
  // in the tier notes, renovation bands and worked example, so a panel never mixes two thousands separators.
  function nf(opts) { return new Intl.NumberFormat('en-GB', opts); }
  var N0 = nf({ maximumFractionDigits: 0 }), N2 = nf({ maximumFractionDigits: 2 });
  var msgs = {};
  Array.prototype.forEach.call(M.querySelectorAll('[data-m]'), function (el) { msgs[el.getAttribute('data-m')] = el.textContent.replace(/\s+/g, ' ').trim(); });
  var devs = {};
  Array.prototype.forEach.call(M.querySelectorAll('[data-dev]'), function (el) { devs[el.getAttribute('data-dev')] = el.textContent.trim(); });
  // Keep numbers in one left-to-right run inside right-to-left text, so "1,250,000+" cannot be reordered.
  function iso(s) { return RTL ? '⁦' + s + '⁩' : s; }
  function plain(s) { return String(s).replace(/[⁦-⁩]/g, '').replace(/\s+/g, ' ').trim(); }
  function msg(k, v) {
    var s = msgs[k] == null ? '' : msgs[k];
    return s.replace(/\{(\w+)\}/g, function (m, n) { return v && v[n] != null ? v[n] : m; });
  }
  // AED keeps the original message keys (money, moneyK, moneyM); other currencies use money-GBP and so on.
  function mkey(base, c) { return c === 'AED' ? base : base + '-' + c; }
  function fmt(x, plus, c) { return msg(mkey('money', c || cur), { n: iso(N0.format(x) + (plus ? '+' : '')) }); }
  function aed(x, plus) { return fmt(x, plus, 'AED'); }
  function compactIn(x, c) {
    x = rnd(x);
    return x >= 1e6 ? msg(mkey('moneyM', c), { n: iso(N2.format(x / 1e6)) }) : msg(mkey('moneyK', c), { n: iso(N0.format(Math.round(x / 1000))) });
  }
  function unitName(u) { return msg('unit-' + u); }
  function fmtDate(iso8601) {
    var dt = iso8601 ? new Date(iso8601 + 'T00:00:00Z') : new Date(), o = { day: 'numeric', month: 'long', year: 'numeric' };
    if (iso8601) o.timeZone = 'UTC';
    try { return new Intl.DateTimeFormat(LANG + '-u-nu-latn', o).format(dt); } catch (e) { return new Intl.DateTimeFormat('en-GB', o).format(dt); }
  }

  /* ---------- helpers ---------- */
  function q(s) { return out.querySelector(s); }
  function put(s, t) { var el = q(s); if (el) el.textContent = t; }
  function qa(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function val(n) { var e = f.elements[n]; return e.length && !e.tagName ? (qa('input[name="' + n + '"]:checked', f)[0] || {}).value : e.value; }
  function toSqft(v) { return unit === 'm2' ? v * K : v; }
  function sqftOf(el) {
    var sq = parseFloat(el.getAttribute('data-sqft')), v = parseFloat(el.value);
    if (!isFinite(sq)) sq = toSqft(v);
    return isFinite(sq) ? sq : 0;
  }
  function num(n) { var el = f.elements[n], v = parseFloat(el.value), sq = sqftOf(el); return sq > 0 && v > 0 ? sq : 0; }
  function on(n) { return f.elements[n].checked && !f.elements[n].disabled; }
  function tri(p) { return [p[0], (p[0] + p[1]) / 2, p[1]]; }
  function rnd(x) { var s = x >= 1e6 ? 1e4 : 1e3; return Math.round(x / s) * s; }
  function txt(el) { return el ? plain(el.textContent) : ''; }
  function sum(r, keys) { return [0, 1, 2].map(function (n) { return keys.reduce(function (a, k) { return a + r[k][n]; }, 0); }); }

  /* ---------- estimate (mirror of estimate() and rounded() in src/pages_tools.py) ---------- */
  function estimate(i) {
    var t = R.tiers[i.tier], nb = tri(t.nb), z = [0, 0, 0], o = {}, open, lowOnly = false;
    function mul(a, m) { return a.map(function (r) { return r * m; }); }
    if (i.mode === 'new') {
      o.build = mul(nb, i.area); o.basement = mul(nb, i.basement);
      o.demo = i.demo ? tri(R.demo) : z; open = !!t.open;
    } else {
      // Renovation bands are whole-villa scope examples: the area is never used. Luxury has no published ceiling
      // ("above AED 1 million"), so only the starting (low) column is shown and the rest needs an assessment.
      var rv = R.reno[i.tier], lo = rv.cost[0], hi = rv.cost[1];
      lowOnly = hi == null;
      o.build = lowOnly ? [lo, lo, lo] : tri([lo, hi]); o.basement = z; o.demo = z; open = lowOnly;
    }
    o.pool = i.pool ? tri(R.pool) : z;
    o.land = mul(tri(R.land), i.garden);
    o.smart = i.smart ? tri(R.smart) : z;
    var c = [0, 1, 2].map(function (k) { return o.build[k] + o.basement[k] + o.demo[k] + o.pool[k] + o.land[k] + o.smart[k]; });
    var soft = i.mode === 'new' || R.reno[i.tier].soft !== false;
    o.design = soft ? c.map(function (v, k) { return v * R.design[k]; }) : z;
    o.permits = soft ? R.permitsFixed.slice() : z;
    o.contingency = c.map(function (v, k) { return v * R.contingency[k]; });
    o.ffe = i.ffe ? c.map(function (v, k) { return v * R.ffe[k]; }) : z;
    // Round each line, then add up the rounded lines so the figures shown always reconcile.
    var r = { open: open, lowOnly: lowOnly };
    LINES.forEach(function (k) { r[k] = o[k].map(rnd); });
    r.construction = sum(r, CONS);
    r.total = sum(r, LINES);
    return r;
  }

  // Display-only conversion: each rounded AED line divided by the rate (AED per unit) and rounded the same way,
  // so the converted lines still add up to the converted total.
  function rate(c) { return c === 'AED' ? 1 : FX.aedPer[c]; }
  function convert(e, c) {
    if (c === 'AED') return e;
    var r = rate(c), o = { open: e.open, lowOnly: e.lowOnly };
    LINES.forEach(function (k) { o[k] = e[k].map(function (v) { return rnd(v / r); }); });
    o.construction = sum(o, CONS);
    o.total = sum(o, LINES);
    return o;
  }

  function route(opt, mode) {
    var city = opt.getAttribute('data-city'), dev = opt.getAttribute('data-dev'), k;
    if (city === 'Abu Dhabi') k = dev ? 'ad-dev' : 'ad';
    else if (dev === 'Nakheel' && mode === 'reno') k = 'dubai-nakheel-reno';
    else k = dev ? 'dubai-dev' : 'dubai';
    return msg('route-' + k, { dev: dev ? (devs[dev] || dev) : '' });
  }

  function show(el, yes) { if (el) el.hidden = !yes; }

  function inputs() {
    return { mode: val('mode'), tier: val('tier'), area: num('area'), basement: num('basement'), garden: num('garden'),
             pool: on('pool'), smart: on('smart'), ffe: on('ffe'), demo: on('demo') };
  }

  var last = null;   // the latest estimate, for the share, print, WhatsApp and send features

  function render() {
    var mode = val('mode'), tier = val('tier'), reno = mode === 'reno', fixed = reno;
    qa('[data-new-only]', f).forEach(function (el) {
      el.classList.toggle('is-off', reno);
      qa('input', el).forEach(function (inp) { inp.disabled = reno; });
    });
    var rh = f.querySelector('[data-reno-hint]'); if (rh) rh.classList.toggle('is-off', !reno);
    // Area: not used by any renovation band, so disable it and say why.
    var areaEl = f.elements.area, af = f.querySelector('[data-area-field]');
    areaEl.disabled = fixed;
    if (af) { var lbl = af.querySelector('label'); if (lbl) lbl.classList.toggle('is-off', fixed); }
    areaEl.classList.toggle('is-off', fixed);
    var hints = { 'data-area-typical': !reno, 'data-area-fixed': fixed }, desc = [];
    Object.keys(hints).forEach(function (a) { var h = f.querySelector('[' + a + ']'); show(h, hints[a]); if (h && hints[a] && h.id) desc.push(h.id); });
    areaEl.setAttribute('aria-describedby', desc.join(' '));
    show(q('[data-reno-assess]'), reno);

    Object.keys(R.tiers).forEach(function (k) {
      var el = f.querySelector('[data-tier-note="' + k + '"]');
      if (el) el.textContent = reno ? msg('tierReno-' + k) : msg('tierNew-' + k + '-' + unit);
    });
    var i = inputs();
    var a = estimate(i), e = convert(a, cur);
    // No built-up area on a new build: show no estimate rather than a total that leaves out the house itself.
    var noArea = !reno && i.area === 0, lowOnly = !!e.lowOnly;
    LINES.concat(['total']).forEach(function (k) {
      var zero = e[k][0] === 0 && e[k][2] === 0, row = q('tr[data-row="' + k + '"]');
      if (row) row.toggleAttribute('data-zero', zero || noArea);
      for (var n = 0; n < 3; n++) {
        var c = q('[data-v="' + k + '-' + n + '"]');
        if (!c) continue;
        c.setAttribute('data-aed', noArea || (lowOnly && n > 0) ? '' : a[k][n]);
        if (noArea || (lowOnly && n > 0)) c.textContent = '–';
        else if (zero) c.textContent = n === 1 ? msg('notIncluded') : '–';
        else c.textContent = fmt(e[k][n], (k === 'total' && n === 2 && e.open) || (lowOnly && (k === 'total' || k === 'build')));
      }
    });
    put('[data-row-label]', msg('rowBuild-' + mode));
    show(q('.calc-range'), !noArea && !lowOnly);
    put('[data-sr]', msg(lowOnly ? 'srFrom' : 'srLikely') + ' ');
    if (noArea) { put('[data-out="likely"]', '–'); put('[data-out="low"]', '–'); put('[data-out="high"]', '–'); }
    else if (lowOnly) { put('[data-out="likely"]', fmt(e.total[0], true)); put('[data-out="low"]', fmt(e.total[0], true)); put('[data-out="high"]', '–'); }
    else {
      put('[data-out="likely"]', fmt(e.total[1]));
      put('[data-out="low"]', fmt(e.total[0]));
      put('[data-out="high"]', fmt(e.total[2], e.open));
    }
    out.setAttribute('data-state', noArea ? 'no-area' : (lowOnly ? 'low-only' : 'range'));
    out.setAttribute('data-cur', cur);
    var c0 = lowOnly ? 0 : 1, nil = noArea ? 0 : 1;   // the starting column when there is no likely figure
    // Converted figures: say plainly that AED is the calculation currency and the rest is approximate.
    var fx = q('[data-fx-note]');
    if (fx) {
      fx.hidden = cur === 'AED' || noArea;
      // Some languages end a date with a full stop ("30 октября 2026 г."), so never print two in a row.
      fx.textContent = fx.hidden ? '' : msg('fxNote', { aed: aed(a.total[c0], lowOnly), date: fmtDate(FX.asAt) }).replace(/\.\./g, '.');
    }
    var sub, cons = fmt(e.construction[1]);
    if (noArea) sub = msg('enterArea');
    // sub-reno-open already says "from", so no trailing + on the figure.
    else if (reno) sub = lowOnly ? msg('sub-reno-open', { cons: fmt(e.construction[0]) }) : msg('sub-reno-fixed', { cons: cons });
    else {
      var rt = i.area ? Math.round(a.build[1] / i.area * (unit === 'm2' ? K : 1) / rate(cur) / 10) * 10 : 0;
      sub = msg('sub-new-' + unit, { cons: cons, rate: rt ? fmt(rt) : '–' });
    }
    put('[data-out="sub"]', sub);

    var parts = { build: e.build[c0] * nil, extras: (e.basement[c0] + e.demo[c0] + e.pool[c0] + e.land[c0] + e.smart[c0]) * nil, design: e.design[c0] * nil,
                  permits: e.permits[c0] * nil, contingency: e.contingency[c0] * nil, ffe: e.ffe[c0] * nil };
    var tot = (e.total[c0] * nil) || 1;
    Object.keys(parts).forEach(function (k) {
      var s = q('[data-seg="' + k + '"]'), l = q('[data-leg="' + k + '"]');
      if (s) s.style.width = (parts[k] / tot * 100).toFixed(2) + '%';
      if (l) l.textContent = parts[k] ? compactIn(parts[k], cur) : '–';
    });

    // timeline
    var tl = q('[data-time]'), li = tl ? qa('li', tl) : [], rows, note;
    if (!reno) {
      rows = ['design', 'approvals', 'build', 'snag'].map(function (k) { return [msg('time-' + k), msg('timeV-' + k)]; });
      note = (tier === 'luxury' || tier === 'ultra' ? 'note-lux' : 'note-new') + (i.basement > 0 ? '-base' : '');
    } else {
      rows = [[msg('time-noc'), msg('timeV-noc')], [msg('time-works'), msg('timeV-works-' + tier)]];
      note = 'note-reno';
    }
    li.forEach(function (el, n) {
      var r = rows[n]; el.hidden = !r;
      if (r && el.children.length === 2) { el.children[0].textContent = r[0]; el.children[1].textContent = r[1]; }
    });
    put('[data-time-note]', msg(note));
    put('[data-route]', route(f.elements.loc.options[f.elements.loc.selectedIndex], mode));

    last = { i: i, aed: a, shown: e, noArea: noArea, lowOnly: lowOnly, c0: c0 };
    share();
  }

  /* ---------- units: inputs show the chosen unit, data-sqft keeps the exact area in square feet ---------- */
  function labelUnits() { qa('[data-unit]', f).forEach(function (s) { s.textContent = unitName(unit); }); }
  function setUnit(u) {
    if (u === unit) return;
    AREAS.forEach(function (n) {
      var el = f.elements[n], sq = sqftOf(el);
      el.setAttribute('data-sqft', sq);
      el.value = Math.round(u === 'm2' ? sq / K : sq);
      el.step = u === 'm2' ? 5 : 50;
    });
    unit = u;
    labelUnits();
  }
  function remember(el) { var v = parseFloat(el.value); if (el.type === 'number') el.setAttribute('data-sqft', isFinite(v) ? toSqft(v) : ''); }

  /* ---------- modes: pool and garden are kept separately for new build and renovation ---------- */
  var mode0 = val('mode'), kept = { reno: { pool: false, sq: 0 } };
  function switchMode(m) {
    if (m === mode0) return;
    var pool = f.elements.pool, g = f.elements.garden;
    kept[mode0] = { pool: pool.checked, sq: sqftOf(g) };
    var s = kept[m];
    if (s) {
      pool.checked = s.pool;
      g.setAttribute('data-sqft', s.sq);
      g.value = Math.round(unit === 'm2' ? s.sq / K : s.sq);
    }
    mode0 = m;
  }

  /* ---------- currency: AED everywhere; GBP, USD, EUR on every page; RUB, CNY, INR only on their language page ---------- */
  var curSel = f.elements.cur;
  if (curSel) {
    qa('option[data-cur-lang]', curSel).forEach(function (o) { if (o.getAttribute('data-cur-lang') !== LANG0) o.parentNode.removeChild(o); });
    curSel.value = 'AED';
  }
  function hasCur(c) { return c === 'AED' || (!!curSel && !!curSel.querySelector('option[value="' + c + '"]') && !!FX.aedPer[c]); }
  function setCur(c) { cur = hasCur(c) ? c : 'AED'; if (curSel) curSel.value = cur; }

  /* ---------- shareable link: inputs <-> query string ---------- */
  function round2(x) { return Math.round(x * 100) / 100; }
  function state() {
    var s = { mode: val('mode'), tier: val('tier'), loc: f.elements.loc.value, unit: unit, cur: cur };
    AREAS.forEach(function (n) { s[n] = round2(sqftOf(f.elements[n])); });
    CHECKS.forEach(function (n) { s[n] = f.elements[n].checked ? '1' : '0'; });
    return s;
  }
  function query() {
    var s = state();
    return Object.keys(s).map(function (k) { return k + '=' + encodeURIComponent(s[k]); }).join('&');
  }
  function shareUrl() { return location.origin + location.pathname + '?' + query(); }
  function writeUrl() {
    try { history.replaceState(history.state, '', location.pathname + '?' + query() + location.hash); } catch (e) { /* file:// or sandboxed */ }
  }
  function pick(name, v) {
    var el = f.querySelector('input[name="' + name + '"][value="' + v + '"]');
    if (el) el.checked = true;
    return !!el;
  }
  function readUrl() {
    var p;
    try { p = new URLSearchParams(location.search); } catch (e) { return false; }
    if (!p.has('mode') && !p.has('tier') && !p.has('area')) return false;
    var m = p.get('mode');
    if (m === 'new' || m === 'reno') pick('mode', m);
    mode0 = val('mode');
    var t = p.get('tier');
    if (t && R.tiers[t]) pick('tier', t);
    var l = p.get('loc');
    if (l && f.elements.loc.querySelector('option[value="' + l.replace(/[^a-z0-9-]/g, '') + '"]')) f.elements.loc.value = l;
    var u = p.get('unit') === 'm2' ? 'm2' : 'sqft';
    pick('unit', u);
    unit = u;
    AREAS.forEach(function (n) {
      if (!p.has(n)) return;
      var el = f.elements[n], raw = p.get(n), sq = parseFloat(raw);
      el.step = u === 'm2' ? 5 : 50;
      if (raw === '' || !isFinite(sq) || sq < 0) { el.value = ''; el.setAttribute('data-sqft', ''); return; }
      sq = Math.min(sq, 1e6);
      el.setAttribute('data-sqft', sq);
      el.value = Math.round(u === 'm2' ? sq / K : sq);
    });
    CHECKS.forEach(function (n) { if (p.has(n)) f.elements[n].checked = p.get(n) === '1'; });
    setCur(p.get('cur') || 'AED');
    return true;
  }

  /* ---------- share, print, WhatsApp and send ---------- */
  var acts = q('[data-calc-actions]'), status = q('[data-copy-status]'), fb = q('[data-copy-fallback]');
  var sendF = document.querySelector('form[data-estimate]');

  function optText(sel) { var o = sel && sel.options[sel.selectedIndex]; return o ? plain(o.textContent) : ''; }
  function tierText() { return txt(f.querySelector('input[name="tier"]:checked + span b')); }

  function waText() {
    if (!last || last.noArea) return msg('wa-none');
    var e = last.shown, v = { tier: tierText(), loc: optText(f.elements.loc) };
    if (last.lowOnly) return plain(msg('wa-from', Object.assign(v, { total: compactIn(e.total[0], cur) })));
    v.total = compactIn(e.total[1], cur);
    if (last.i.mode === 'reno') return plain(msg('wa-reno', v));
    var shownArea = unit === 'm2' ? last.i.area / K : last.i.area;
    v.area = N0.format(Math.round(shownArea)) + ' ' + unitName(unit);
    return plain(msg('wa-new', v));
  }

  // Input summary for the printed estimate, written with the labels already on the page (so it is translated).
  function printInputs() {
    var dl = q('[data-print-inputs]');
    if (!dl) return;
    var rows = [], reno = last && last.i.mode === 'reno';
    function legend(sel) { var el = f.querySelector(sel); return el ? txt(el.closest('fieldset').querySelector('legend')) : ''; }
    function label(name) { var el = f.querySelector('label[for="' + (f.elements[name] || {}).id + '"]'); return txt(el); }
    rows.push([legend('input[name="mode"]'), txt(f.querySelector('input[name="mode"]:checked + span'))]);
    rows.push([label('loc'), optText(f.elements.loc)]);
    var tn = txt(f.querySelector('input[name="tier"]:checked + span small'));
    // A renovation note already starts with the band name ("Luxury: premium materials..."), so it stands alone.
    rows.push([legend('input[name="tier"]'), reno && tn ? tn : tierText() + (tn ? ' · ' + tn : '')]);
    if (!reno) {
      rows.push([label('area'), f.elements.area.value ? N0.format(parseFloat(f.elements.area.value)) : '–']);
      if (num('basement')) rows.push([label('basement'), N0.format(parseFloat(f.elements.basement.value))]);
    }
    if (num('garden')) rows.push([label('garden'), N0.format(parseFloat(f.elements.garden.value))]);
    var ex = CHECKS.filter(function (n) { return on(n); }).map(function (n) { return txt(f.elements[n].closest('label')); });
    rows.push([legend('input[name="pool"]'), ex.length ? ex.join(', ') : msg('none')]);
    if (cur !== 'AED' && curSel) rows.push([label('cur'), optText(curSel)]);
    dl.textContent = '';
    rows.forEach(function (r) {
      var dt = document.createElement('dt'), dd = document.createElement('dd');
      dt.textContent = r[0]; dd.textContent = r[1];
      dl.appendChild(dt); dl.appendChild(dd);
    });
    put('[data-print-date]', fmtDate());
    put('[data-print-url]', shareUrl().replace(/^https?:\/\//, ''));
  }

  // Hidden fields of the "estimate" form: language-neutral codes and AED figures for Philip, plus the shareable link.
  function fillSend() {
    if (!sendF || !last) return;
    var s = state(), a = last.aed, e = last.shown;
    function trio(r, c) { return last.noArea ? 'no estimate (no built-up area)' : (last.lowOnly ? 'from ' + c + ' ' + N0.format(r.total[0]) : c + ' low ' + N0.format(r.total[0]) + '; likely ' + N0.format(r.total[1]) + '; high ' + N0.format(r.total[2]) + (r.open ? '+' : '')); }
    // With no published ceiling (lowOnly) the page shows only the starting column, so Philip gets only that column too.
    var lines = LINES.filter(function (k) { return a[k][0] || a[k][2]; }).map(function (k) { return k + ' ' + (last.lowOnly ? 'from ' + N0.format(a[k][0]) : a[k].map(function (x) { return N0.format(x); }).join('/')); });
    var res = trio(a, 'AED') + (last.noArea ? '' : (last.lowOnly ? ' | lines (AED, starting figures): ' : ' | lines (AED low/likely/high): ') + lines.join(', '));
    if (cur !== 'AED' && !last.noArea) res += ' | shown in ' + cur + ' (approximate, rates of ' + FX.asAt + '): ' + trio(e, cur);
    var set = function (n, v) { var el = sendF.elements[n]; if (el) el.value = v; };
    set('estimate_inputs', Object.keys(s).map(function (k) { return k + '=' + s[k]; }).join('; '));
    set('estimate_result', res);
    set('estimate_link', shareUrl());
    set('currency', cur);
  }

  // Embed page: "Open this estimate in the full calculator" carries the inputs, so the full page opens on the same estimate.
  var full = q('[data-full-link]');
  function share() {
    if (full) full.href = full.href.split('?')[0] + '?' + query();
    // Every WhatsApp link on the page carries the estimate: the result button, the floating button, the phone
    // action bar (a.ab-wa), the header and the footer.
    var wt = encodeURIComponent(waText());
    Array.prototype.forEach.call(document.querySelectorAll('a[href*="wa.me/"]'), function (l) {
      l.href = 'https://wa.me/' + (l.href.match(/wa\.me\/(\d+)/) || [0, ''])[1] + '?text=' + wt;
    });
    printInputs();
    fillSend();
    postHeight();
  }

  // Inside another site's iframe (the embed page), tell the host page our height so its optional resize snippet
  // can size the iframe and avoid a scroll area inside a scroll area. Message: {type: 'eb-calc-height', height: px}.
  var framed = window.parent !== window, lastH = 0;
  function postHeight() {
    if (!framed) return;
    // Measure the content, not the document: the document is never shorter than the iframe, so it could not shrink.
    var m = document.getElementById('main') || document.body;
    var h = Math.ceil(m.getBoundingClientRect().bottom + (window.pageYOffset || 0)) + 2;
    if (h === lastH) return;
    lastH = h;
    try { window.parent.postMessage({ type: 'eb-calc-height', height: h }, '*'); } catch (err) { /* host blocked messages */ }
  }
  if (framed) {
    window.addEventListener('load', postHeight);
    window.addEventListener('resize', function () { lastH = 0; postHeight(); });
  }

  function say(t) { if (status) status.textContent = t; }
  function copyLink() {
    var u = shareUrl();
    writeUrl();
    function fallback() {
      if (!fb) { say(msg('copyFail') + ' ' + u); return; }
      fb.hidden = false; fb.value = u; fb.focus(); fb.select();
      var okc = false;
      try { okc = document.execCommand('copy'); } catch (e) { okc = false; }
      if (okc) { say(msg('copied')); } else { say(msg('copyFail')); }
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(u).then(function () { if (fb) fb.hidden = true; say(msg('copied')); }, fallback);
    } else fallback();
    if (window.gtag) gtag('event', 'share', { method: 'copy_link', content_type: 'calculator' });
  }

  if (acts) {
    acts.hidden = false;
    var cb = acts.querySelector('[data-copy-link]'), pb = acts.querySelector('[data-print]');
    if (cb) cb.addEventListener('click', copyLink);
    if (pb) pb.addEventListener('click', function () {
      printInputs();
      if (window.gtag) gtag('event', 'print', { content_type: 'calculator' });
      window.print();
    });
  }
  window.addEventListener('beforeprint', printInputs);
  // No conversion event here: estimate_request_success fires on the thank-you page, after Netlify accepted the form (build.py SCRIPT).
  if (sendF) sendF.addEventListener('submit', fillSend);

  /* ---------- "Add this calculator to your website" (full page): embed code in the page's language, Copy code ---------- */
  var ec = document.querySelector('[data-embed-code]'), ecb = document.querySelector('[data-embed-copy]'),
      ecs = document.querySelector('[data-embed-status]'), ep = document.querySelector('[data-embed-preview]');
  if (ec && ep) {
    // The preview link is localised by the i18n pipeline (/ru/..., /zh/...), so it gives this language's embed path.
    var epath = ep.pathname || '';
    if (/\/embed\/$/.test(epath)) ec.value = ec.value.replace(/src="[^"]*"/, 'src="' + ec.getAttribute('data-site') + epath + '"');
  }
  function sayEmbed(t) { if (ecs) ecs.textContent = t; }
  if (ec && ecb) ecb.addEventListener('click', function () {
    function fallback() {
      ec.focus(); ec.select();
      var okc = false;
      try { okc = document.execCommand('copy'); } catch (e) { okc = false; }
      sayEmbed(msg(okc ? 'embedCopied' : 'embedCopyFail'));
    }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(ec.value).then(function () { sayEmbed(msg('embedCopied')); }, fallback);
    else fallback();
    if (window.gtag) gtag('event', 'share', { method: 'embed_code', content_type: 'calculator' });
  });

  /* ---------- events ---------- */
  function onInput(ev) {
    var n = ev.target.name;
    if (n === 'unit') setUnit(ev.target.value);
    else if (n === 'mode') switchMode(ev.target.value);
    else if (n === 'cur') setCur(ev.target.value);
    else if (ev.type === 'input') remember(ev.target);
    render();
    writeUrl();
    say('');
  }
  f.addEventListener('input', onInput);
  f.addEventListener('change', onInput);
  var js = q('[data-js-note]'); if (js) js.textContent = msg('jsNote');
  var checked = qa('input[name="unit"]:checked', f)[0];
  if (checked && checked.value === 'm2') unit = 'm2';
  readUrl();
  labelUnits();
  render();
})();
