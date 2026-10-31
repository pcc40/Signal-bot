/* Eastbridge villa build and renovation cost calculator.
   Rates come from the JSON block #calc-data (generated from src/pages_tools.py RATES).
   Every word the script shows comes from the hidden message list #calc-msgs, which the i18n pipeline
   translates with the rest of the page; this file holds no user-facing text.
   Areas are kept internally in square feet (data-sqft on each input), so switching units never changes the estimate.
   The server renders the worked example; this script updates the same nodes in place. */
(function () {
  var f = document.getElementById('calc'), d = document.getElementById('calc-data'), out = document.getElementById('calc-out'),
      M = document.getElementById('calc-msgs');
  if (!f || !d || !out || !M) return;
  var R = JSON.parse(d.textContent), K = R.sqftPerM2;
  var root = document.documentElement, RTL = root.dir === 'rtl', LANG = root.lang || 'en-GB';
  var unit = 'sqft';
  var LINES = ['build', 'basement', 'demo', 'pool', 'land', 'smart', 'design', 'permits', 'contingency', 'ffe'];
  var CONS = LINES.slice(0, 6);

  /* ---------- messages and number formatting ---------- */
  function nf(opts) {
    try { return new Intl.NumberFormat(LANG + '-u-nu-latn', opts); } catch (e) { return new Intl.NumberFormat('en-GB', opts); }
  }
  var N0 = nf({ maximumFractionDigits: 0 }), N2 = nf({ maximumFractionDigits: 2 });
  var msgs = {};
  Array.prototype.forEach.call(M.querySelectorAll('[data-m]'), function (el) { msgs[el.getAttribute('data-m')] = el.textContent.replace(/\s+/g, ' ').trim(); });
  var devs = {};
  Array.prototype.forEach.call(M.querySelectorAll('[data-dev]'), function (el) { devs[el.getAttribute('data-dev')] = el.textContent.trim(); });
  // Keep numbers in one left-to-right run inside right-to-left text, so "1,250,000+" cannot be reordered.
  function iso(s) { return RTL ? '⁦' + s + '⁩' : s; }
  function msg(k, v) {
    var s = msgs[k] == null ? '' : msgs[k];
    return s.replace(/\{(\w+)\}/g, function (m, n) { return v && v[n] != null ? v[n] : m; });
  }
  function aed(x, plus) { return msg('money', { n: iso(N0.format(x) + (plus ? '+' : '')) }); }
  function compact(x) {
    x = rnd(x);
    return x >= 1e6 ? msg('moneyM', { n: iso(N2.format(x / 1e6)) }) : msg('moneyK', { n: iso(N0.format(Math.round(x / 1000))) });
  }
  function unitName(u) { return msg('unit-' + u); }

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
  function fixedBand(tier) { return R.reno[tier].cost[1] != null; }

  /* ---------- estimate (mirror of estimate() and rounded() in src/pages_tools.py) ---------- */
  function estimate(i) {
    var t = R.tiers[i.tier], nb = tri(t.nb), z = [0, 0, 0], o = {}, open;
    function mul(a, m) { return a.map(function (r) { return r * m; }); }
    if (i.mode === 'new') {
      o.build = mul(nb, i.area); o.basement = mul(nb, i.basement);
      o.demo = i.demo ? tri(R.demo) : z; open = !!t.open;
    } else {
      // Basic and mid-range bands are fixed whole-villa examples: the area is not used. Luxury bands have no
      // published ceiling; the high figure is the area at the lowest new-build rate (documented on the page).
      var rv = R.reno[i.tier], lo = rv.cost[0], hi = rv.cost[1];
      if (hi == null) hi = Math.max(lo, i.area * t.nb[0]);
      o.build = tri([lo, hi]); o.basement = z; o.demo = z; open = rv.cost[1] == null;
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
    var r = { open: open };
    LINES.forEach(function (k) { r[k] = o[k].map(rnd); });
    function sum(keys) { return [0, 1, 2].map(function (n) { return keys.reduce(function (a, k) { return a + r[k][n]; }, 0); }); }
    r.construction = sum(CONS);
    r.total = sum(LINES);
    return r;
  }

  function route(opt, mode) {
    var city = opt.getAttribute('data-city'), dev = opt.getAttribute('data-dev'), k;
    if (city === 'Abu Dhabi') k = dev ? 'ad-dev' : 'ad';
    else if (dev === 'Nakheel' && mode === 'reno') k = 'dubai-nakheel-reno';
    else k = dev ? 'dubai-dev' : 'dubai';
    return msg('route-' + k, { dev: dev ? (devs[dev] || dev) : '' });
  }

  function show(el, yes) { if (el) el.hidden = !yes; }

  function render() {
    var mode = val('mode'), tier = val('tier'), reno = mode === 'reno', fixed = reno && fixedBand(tier);
    qa('[data-new-only]', f).forEach(function (el) {
      el.classList.toggle('is-off', reno);
      qa('input', el).forEach(function (inp) { inp.disabled = reno; });
    });
    var rh = f.querySelector('[data-reno-hint]'); if (rh) rh.classList.toggle('is-off', !reno);
    // Area: not used by fixed renovation bands, so disable it and say why.
    var areaEl = f.elements.area, af = f.querySelector('[data-area-field]');
    areaEl.disabled = fixed;
    if (af) { var lbl = af.querySelector('label'); if (lbl) lbl.classList.toggle('is-off', fixed); }
    areaEl.classList.toggle('is-off', fixed);
    var hints = { 'data-area-typical': !reno, 'data-area-fixed': fixed, 'data-area-open': reno && !fixed }, desc = [];
    Object.keys(hints).forEach(function (a) { var h = f.querySelector('[' + a + ']'); show(h, hints[a]); if (h && hints[a] && h.id) desc.push(h.id); });
    areaEl.setAttribute('aria-describedby', desc.join(' '));
    show(q('[data-reno-assess]'), reno);

    Object.keys(R.tiers).forEach(function (k) {
      var el = f.querySelector('[data-tier-note="' + k + '"]');
      if (el) el.textContent = reno ? msg('tierReno-' + k) : msg('tierNew-' + k + '-' + unit);
    });
    var i = { mode: mode, tier: tier, area: num('area'), basement: num('basement'), garden: num('garden'),
              pool: on('pool'), smart: on('smart'), ffe: on('ffe'), demo: on('demo') };
    var e = estimate(i);
    LINES.concat(['total']).forEach(function (k) {
      var zero = e[k][0] === 0 && e[k][2] === 0;
      for (var n = 0; n < 3; n++) {
        var c = q('[data-v="' + k + '-' + n + '"]');
        if (c) c.textContent = zero ? (n === 1 ? msg('notIncluded') : '–') : aed(e[k][n], k === 'total' && n === 2 && e.open);
      }
    });
    put('[data-row-label]', msg('rowBuild-' + mode));
    put('[data-out="likely"]', aed(e.total[1]));
    put('[data-out="low"]', aed(e.total[0]));
    put('[data-out="high"]', aed(e.total[2], e.open));
    var sub, cons = aed(e.construction[1]);
    if (reno) sub = msg(fixed ? 'sub-reno-fixed' : 'sub-reno-open', { cons: cons });
    else {
      var rate = i.area ? Math.round(e.build[1] / i.area * (unit === 'm2' ? K : 1) / 10) * 10 : 0;
      sub = msg('sub-new-' + unit, { cons: cons, rate: rate ? aed(rate) : '–' });
    }
    put('[data-out="sub"]', sub);

    var parts = { build: e.build[1], extras: e.basement[1] + e.demo[1] + e.pool[1] + e.land[1] + e.smart[1], design: e.design[1],
                  permits: e.permits[1], contingency: e.contingency[1], ffe: e.ffe[1] };
    var tot = e.total[1] || 1;
    Object.keys(parts).forEach(function (k) {
      var s = q('[data-seg="' + k + '"]'), l = q('[data-leg="' + k + '"]');
      if (s) s.style.width = (parts[k] / tot * 100).toFixed(2) + '%';
      if (l) l.textContent = parts[k] ? compact(parts[k]) : '–';
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
  }

  /* ---------- units: inputs show the chosen unit, data-sqft keeps the exact area in square feet ---------- */
  function labelUnits() { qa('[data-unit]', f).forEach(function (s) { s.textContent = unitName(unit); }); }
  function setUnit(u) {
    if (u === unit) return;
    ['area', 'basement', 'garden'].forEach(function (n) {
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

  f.addEventListener('input', function (ev) {
    if (ev.target.name === 'unit') setUnit(ev.target.value);
    else if (ev.target.name === 'mode') switchMode(ev.target.value);
    else remember(ev.target);
    render();
  });
  f.addEventListener('change', function (ev) {
    if (ev.target.name === 'unit') setUnit(ev.target.value);
    else if (ev.target.name === 'mode') switchMode(ev.target.value);
    render();
  });
  var js = q('[data-js-note]'); if (js) js.textContent = msg('jsNote');
  var checked = qa('input[name="unit"]:checked', f)[0];
  if (checked && checked.value === 'm2') unit = 'm2';
  labelUnits();
  render();
})();
