const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '../..');
const evidence = path.join(root, 'reports/evidence');
const figures = path.join(evidence, 'figures');
const origin = process.env.CHICKFLOW_URL || 'http://127.0.0.1:8516';
const channel = process.env.CHICKFLOW_CHROME;
const data = JSON.parse(fs.readFileSync(path.join(root, 'data/manifest.json')));
const viewport = { width: 1440, height: 1100 };

async function shiftTo(page, route, heading) {
  await page.goto(origin + route);
  await page.getByRole('heading', { name: heading, exact: true }).waitFor();
  assert.deepEqual(await page.locator('[data-testid="stException"]').allTextContents(), []);
}

async function capture(element, id, route) {
  await element.scrollIntoViewIfNeeded();
  await element.page().mouse.move(1, 1);
  const box = await element.boundingBox();
  assert.ok(box && box.width >= 190 && box.height >= 100, 'Figure too small: ' + id);
  const filename = path.join(figures, id + '.png');
  await element.screenshot({ path: filename, animations: 'disabled' });
  return { id, route, file: path.relative(evidence, filename),
    width: Math.round(box.width), height: Math.round(box.height),
    sha256: crypto.createHash('sha256').update(fs.readFileSync(filename)).digest('hex') };
}

async function plot(page, id, route) {
  const element = page.locator('.st-key-' + id + ' [data-testid="stPlotlyChart"]');
  await element.locator('.main-svg').first().waitFor();
  return capture(element, id, route);
}

async function branch(page, title, id) {
  const heading = page.getByRole('heading', { name: title, exact: true });
  const element = heading.locator('xpath=ancestor::*[@data-testid="stColumn"][1]');
  await heading.waitFor();
  if (id === 'V-L01') {
    await element.locator('img').evaluate(image => image.decode());
  } else {
    await element.locator('svg').first().waitFor();
  }
  return capture(element, id, '/orders');
}

(async () => {
  fs.mkdirSync(figures, { recursive: true });
  const browser = await chromium.launch({ headless: true, ...(channel ? { executablePath: channel } : {}) });
  try {
    const page = await browser.newPage({ viewport });
    page.setDefaultTimeout(10000);
    const notes = [];
    const errors = [];
    page.on('pageerror', err => errors.push(String(err)));
    const plan = [
      ['/', 'Ringkasan operasional', ['V-Q01']],
      ['/orders', 'Pesanan dan jam sibuk', ['V-Q03', 'V-Q09']],
      ['/kitchen', 'Waktu persiapan dapur', ['V-Q05', 'V-Q06', 'V-Q10']],
      ['/inventory', 'Persediaan bahan', ['V-Q08', 'V-Q12']],
      ['/sales', 'Penjualan cabang', ['V-Q02', 'V-Q04', 'V-G01']],
      ['/profit', 'Biaya dan laba menu', ['V-Q07', 'V-Q11']],
    ];
    for (const [route, heading, ids] of plan) {
      await shiftTo(page, route, heading);
      await page.getByText(/24\/10\/2026–30\/10\/2026 WIB · Semua cabang · Semua kategori/).waitFor();
      if (route === '/inventory') {
        const expander = page.locator('summary').filter({ hasText: 'Lihat saldo terhadap batas pesan ulang' });
        await expander.click();
      }
      for (const id of ids) notes.push(await plot(page, id, route));
      if (route === '/orders') {
        await page.getByRole('button', { name: 'Lihat pesanan dan ulasan' }).click();
        notes.push(await branch(page, 'Alur pesanan · V-L02', 'V-L02'));
        notes.push(await branch(page, 'Kata yang sering muncul · V-L01', 'V-L01'));
      }
    }
    assert.equal(new Set(notes.map(x => x.id)).size, 15);
    assert.deepEqual(errors, []);
    notes.sort((a,b) => a.id.localeCompare(b.id));
    fs.writeFileSync(path.join(evidence, 'figures-manifest.json'), JSON.stringify({
      seed: data.seed, csv_sha256: data.sha256, viewport, browser: browser.version(), origin,
      filter: { start_date:'2026-10-24', end_date:'2026-10-30', branches:'Semua cabang', categories:'Semua kategori' },
      figures: notes,
    }, null, 2) + '\n');
    console.log(notes.length + ' visual diambil dari dashboard.');
  } finally {
    await browser.close();
  }
})().catch(err => { console.error(err); process.exit(1); });
