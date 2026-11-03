// HTML -> PDF with headless Chromium (Playwright). Used by pack_design.py.
// node render_pdf.js jobs.json   jobs: [{html, pdf, kind: "doc"|"deck", footer}]
const fs = require('fs');
let pw;
try { pw = require('playwright'); } catch (e) { pw = require('playwright-core'); }
const FIT = fs.readFileSync(__dirname + '/fit.js', 'utf8');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  let browser;
  try { browser = await pw.chromium.launch(); }
  catch (e) { browser = await pw.chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); }
  // Lay the page out at its printed width before fit.js measures it: A4 content width with the
  // 19 mm side margins is 172 mm = 650 px; a cover is full A4 (794 px); a deck slide is 1280 px.
  // Measuring at the default 1280 px screen width under-counted wrapped lines and clipped one-pagers.
  const WIDTH = { deck: 1280, cover: 794 };
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: WIDTH[j.kind] || 650, height: 1000 } });
    await page.emulateMedia({ media: 'print' });
    await page.goto('file://' + j.html);
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(FIT);
    if (j.kind === 'deck') {
      await page.pdf({ path: j.pdf, width: '13.333in', height: '7.5in', printBackground: true,
        margin: { top: '0', bottom: '0', left: '0', right: '0' }, preferCSSPageSize: true });
    } else if (j.kind === 'cover') {
      await page.pdf({ path: j.pdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
    } else {
      await page.pdf({ path: j.pdf, format: 'A4', printBackground: true, displayHeaderFooter: true,
        headerTemplate: j.header, footerTemplate: j.footer, preferCSSPageSize: true });
    }
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
