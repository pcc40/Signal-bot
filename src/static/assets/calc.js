/* Eastbridge villa build and renovation cost calculator.
   Rates come from the JSON block #calc-data (generated from src/pages_tools.py RATES).
   The server renders the worked example; this script updates the same nodes in place. */
(function () {
  var f = document.getElementById('calc'), d = document.getElementById('calc-data'), out = document.getElementById('calc-out');
  if (!f || !d || !out) return;
  var R = JSON.parse(d.textContent), K = R.sqftPerM2;
  var unit = 'sqft';
  function q(s) { return out.querySelector(s); }
  function put(s, t) { var el = q(s); if (el) el.textContent = t; }
  function qa(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function val(n) { var e = f.elements[n]; return e.length && !e.tagName ? (qa('input[name="' + n + '"]:checked', f)[0] || {}).value : e.value; }
  function num(n) { var el = f.elements[n], sq = parseFloat(el.getAttribute('data-sqft')), v = parseFloat(el.value); if (!isFinite(sq)) sq = unit === 'm2' ? v * K : v; return isFinite(sq) && sq > 0 && v > 0 ? sq : 0; }
  function on(n) { return f.elements[n].checked && !f.elements[n].disabled; }
  function tri(p) { return [p[0], (p[0] + p[1]) / 2, p[1]]; }
  function rnd(x) { var s = x >= 1e6 ? 1e4 : 1e3; return Math.round(x / s) * s; }
  function aed(x) { return 'AED ' + rnd(x).toLocaleString('en-GB'); }
  function compact(x) { x = rnd(x); return x >= 1e6 ? 'AED ' + (x / 1e6).toFixed(2).replace(/\.00$/, '') + 'm' : 'AED ' + Math.round(x / 1000).toLocaleString('en-GB') + 'k'; }
  function range(p, open) { return p[0] + '–' + (p[1] == null ? '' : p[1]) + ' months' + (open ? ' or longer' : ''); }

  function estimate(i) {
    var t = R.tiers[i.tier], nb = tri(t.nb), z = [0, 0, 0], o = {}, n, open;
    function mul(a, m) { return a.map(function (r) { return r * m; }); }
    if (i.mode === 'new') {
      o.build = mul(nb, i.area); o.basement = mul(nb, i.basement);
      o.demo = i.demo ? tri(R.demo) : z; open = !!t.open;
    } else {
      var rv = R.reno[i.tier], lo = rv.cost[0], hi = rv.cost[1];
      if (hi == null) hi = Math.max(lo, i.area * t.nb[0]);
      o.build = tri([lo, hi]); o.basement = z; o.demo = z; open = rv.cost[1] == null;
    }
    o.pool = i.pool ? tri(R.pool) : z;
    o.land = mul(tri(R.land), i.garden);
    o.smart = i.smart ? tri(R.smart) : z;
    var c = [0, 1, 2].map(function (k) { return o.build[k] + o.basement[k] + o.demo[k] + o.pool[k] + o.land[k] + o.smart[k]; });
    o.construction = c;
    o.design = c.map(function (v, k) { return v * R.design[k]; });
    o.permits = i.mode === 'new' ? c.map(function (v, k) { return Math.max(R.permitsFixed[k], v * R.permitsPct[k]); }) : R.permitsFixed.slice();
    o.contingency = c.map(function (v, k) { return v * R.contingency[k]; });
    o.ffe = i.ffe ? c.map(function (v, k) { return v * R.ffe[k]; }) : z;
    o.total = c.map(function (v, k) { return v + o.design[k] + o.permits[k] + o.contingency[k] + o.ffe[k]; });
    o.open = open;
    return o;
  }

  function route(opt, mode) {
    var city = opt.getAttribute('data-city'), dev = opt.getAttribute('data-dev');
    if (city === 'Abu Dhabi') {
      return 'In Abu Dhabi the Department of Municipalities and Transport regulates villa building, and permits are issued by the municipality through TAMM.' +
        (dev ? ' The master developer, ' + dev + ', has its own approval requirements; check them before design starts.' : '');
    }
    var s = 'Approvals in Dubai go through Dubai Municipality, Trakhees or the Dubai Development Authority, depending on where your plot sits.';
    if (dev === 'Nakheel') s += mode === 'reno' ? ' In Nakheel communities, renovation and extension approvals start with a Nakheel NOC application through its portal.' : ' The master developer, Nakheel, has its own approval requirements; check them before design starts.';
    else if (dev) s += ' The master developer, ' + dev + ', has its own approval requirements; check them before design starts.';
    return s;
  }

  function render() {
    var mode = val('mode'), tier = val('tier');
    qa('[data-new-only]', f).forEach(function (el) {
      el.classList.toggle('is-off', mode !== 'new');
      qa('input', el).forEach(function (inp) { inp.disabled = mode !== 'new'; });
    });
    var rh = f.querySelector('[data-reno-hint]'); if (rh) rh.classList.toggle('is-off', mode !== 'reno');
    Object.keys(R.tiers).forEach(function (k) {
      var el = f.querySelector('[data-tier-note="' + k + '"]'), t = R.tiers[k], rv = R.reno[k];
      if (!el) return;
      el.textContent = mode === 'new'
        ? 'AED ' + t.nb[0].toLocaleString('en-GB') + '–' + t.nb[1].toLocaleString('en-GB') + (t.open ? '+' : '') + ' per sq ft'
        : rv.label + ', ' + (rv.cost[1] == null ? 'from AED ' + (rv.cost[0] / 1e6) + 'm' : 'AED ' + rv.cost[0] / 1000 + 'k–' + rv.cost[1] / 1000 + 'k');
    });
    var i = { mode: mode, tier: tier, area: num('area'), basement: num('basement'), garden: num('garden'),
              pool: on('pool'), smart: on('smart'), ffe: on('ffe'), demo: on('demo') };
    var e = estimate(i), plus = e.open ? '+' : '';
    Object.keys(e).forEach(function (k) {
      if (!Array.isArray(e[k])) return;
      var zero = e[k][0] === 0 && e[k][2] === 0;
      for (var n = 0; n < 3; n++) {
        var c = q('[data-v="' + k + '-' + n + '"]');
        if (c) c.textContent = zero ? (n === 1 ? 'Not included' : '–') : aed(e[k][n]) + (k === 'total' && n === 2 ? plus : '');
      }
    });
    put('[data-out="likely"]', aed(e.total[1]));
    put('[data-out="low"]', aed(e.total[0]));
    put('[data-out="high"]', aed(e.total[2]) + plus);
    put('[data-out="cons"]', aed(e.construction[1]));
    var area = parseFloat(f.elements.area.value) || 0;
    put('[data-out="rate"]', area ? 'AED ' + (Math.round(e.construction[1] / area / 10) * 10).toLocaleString('en-GB') : '–');
    var sub = q('.calc-sub'); if (sub && unit && sub.lastChild && sub.lastChild.nodeType === 3) sub.lastChild.textContent = ' per ' + (unit === 'm2' ? 'm²' : 'sq ft') + ' of built-up area (construction only)';
    var parts = { build: e.build[1], extras: e.basement[1] + e.demo[1] + e.pool[1] + e.land[1] + e.smart[1], design: e.design[1],
                  permits: e.permits[1], contingency: e.contingency[1], ffe: e.ffe[1] };
    var tot = 0; Object.keys(parts).forEach(function (k) { tot += parts[k]; }); tot = tot || 1;
    Object.keys(parts).forEach(function (k) {
      var s = q('[data-seg="' + k + '"]'), l = q('[data-leg="' + k + '"]');
      if (s) s.style.width = (parts[k] / tot * 100).toFixed(2) + '%';
      if (l) l.textContent = parts[k] ? compact(parts[k]) : '–';
    });
    // timeline
    var T = R.time, tl = q('[data-time]'), li = tl ? qa('li', tl) : [], rows, note;
    if (mode === 'new') {
      rows = [['Design', range(T.design)], ['Approvals and NOCs', range(T.approvals)], ['Construction', range(T.build)], ['Snagging and handover', range(T.snag)]];
      var a = T.design[0] + T.approvals[0] + T.build[0] + T.snag[0], b = T.design[1] + T.approvals[1] + T.build[1] + T.snag[1];
      note = (tier === 'luxury' || tier === 'ultra')
        ? 'Custom luxury villas commonly take ' + T.luxTotal[0] + '–' + T.luxTotal[1] + ' months from plot to keys. Phases can overlap.'
        : 'Typically ' + a + '–' + b + ' months from appointing a designer to receiving the keys. Phases can overlap.';
      if (i.basement > 0) note += ' A basement adds time to the ground works stage.';
    } else {
      var m = R.reno[tier].months;
      rows = [['Developer NOC and permit', 'A few weeks'], ['Works', m[1] == null ? m[0] + ' months or longer' : range(m)]];
      note = 'Smaller interior upgrades take around two to three months; structural changes and extensions six months or longer.';
    }
    li.forEach(function (el, n) {
      var r = rows[n]; el.hidden = !r;
      if (r && el.children.length === 2) { el.children[0].textContent = r[0]; el.children[1].textContent = r[1]; }
    });
    put('[data-time-note]', note);
    put('[data-route]', route(f.elements.loc.options[f.elements.loc.selectedIndex], mode));
  }

  function setUnit(u) {
    if (u === unit) return;
    ['area', 'basement', 'garden'].forEach(function (n) {
      var el = f.elements[n], v = parseFloat(el.value), sq = parseFloat(el.getAttribute('data-sqft'));
      if (!isFinite(sq)) sq = unit === 'm2' ? v * K : v;
      if (isFinite(sq)) { el.value = Math.round(u === 'm2' ? sq / K : sq); el.setAttribute('data-sqft', sq); }
      el.step = u === 'm2' ? 5 : 50;
    });
    unit = u;
    qa('[data-unit]', f).forEach(function (s) { s.textContent = u === 'm2' ? 'm²' : 'sq ft'; });
  }

  function remember(el) { var v = parseFloat(el.value); if (el.type === 'number') el.setAttribute('data-sqft', isFinite(v) ? (unit === 'm2' ? v * K : v) : ''); }
  f.addEventListener('input', function (ev) { if (ev.target.name === 'unit') setUnit(ev.target.value); else remember(ev.target); render(); });
  f.addEventListener('change', function (ev) { if (ev.target.name === 'unit') setUnit(ev.target.value); render(); });
  var js = q('[data-js-note]'); if (js) js.textContent = 'Figures update as you change the inputs.';
  var checked = qa('input[name="unit"]:checked', f)[0];
  if (checked && checked.value === 'm2') { unit = 'm2'; qa('[data-unit]', f).forEach(function (s) { s.textContent = 'm²'; }); }
  render();
})();
