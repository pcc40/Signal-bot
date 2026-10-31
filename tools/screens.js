// Visual check: node tools/screens.js <port> <outdir> <tag> [paths...]
// Serve dist first: (cd dist && python3 -m http.server <port>). FULL=1 for full-page shots.
const { chromium } = require('playwright');
const [,, port, outdir, tag, ...rest] = process.argv;
const pages = rest.length ? rest : ['/', '/services/', '/services/owners-representative/', '/areas/palm-jumeirah/',
  '/case-studies/island-e-waterfront-villa/', '/work/', '/work/ansells/', '/insights/villa-construction-cost-dubai/',
  '/about/', '/contact/', '/contact/thanks/', '/ar/'];
(async () => {
  const b = await chromium.launch();
  for (const [vw, vh, name] of [[1440, 900, 'd'], [390, 844, 'm']]) {
    const ctx = await b.newContext({ viewport: { width: vw, height: vh }, deviceScaleFactor: 1, isMobile: name === 'm', hasTouch: name === 'm' });
    const p = await ctx.newPage();
    for (const path of pages) {
      await p.goto(`http://127.0.0.1:${port}${path}`, { waitUntil: 'load' });
      await p.waitForTimeout(800);
      const slug = (path.replace(/\//g, '_').replace(/^_|_$/g, '') || 'home');
      await p.screenshot({ path: `${outdir}/${tag}-${slug}-${name}.png`, fullPage: process.env.FULL === '1' });
    }
    await ctx.close();
  }
  await b.close();
})();
