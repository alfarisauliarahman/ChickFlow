const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../..');
const ORIGIN = process.env.CHICKFLOW_URL || 'http://127.0.0.1:8516';
const PROTOTYPE = process.env.CHICKFLOW_V1_URL;
const chrome = process.env.CHICKFLOW_CHROME;
const metadata = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/manifest.json')));
const out = path.join(ROOT, 'reports/screenshots');
const routes = [
  ['', 'Ringkasan operasional', 'overview', 1],
  ['orders', 'Pesanan dan jam sibuk', 'orders', 2],
  ['kitchen', 'Waktu persiapan dapur', 'kitchen', 3],
  ['inventory', 'Persediaan bahan', 'inventory', 2],
  ['sales', 'Penjualan cabang', 'sales', 4],
  ['profit', 'Biaya dan laba menu', 'profit', 2],
];

async function heading(page, title) {
  await page.getByRole('heading', { name: title, exact: true }).waitFor();
  const errors = await page.locator('[data-testid="stException"]').allTextContents();
  assert.deepEqual(errors, []);
}

async function screenshot(page, filename) {
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(out, filename), animations: 'disabled' });
}

async function focusMainTop(page) {
  await page.locator('[data-testid="stMain"]').evaluate(element => element.scrollTo(0, 0));
}

async function openOverview(page) {
  await page.goto(ORIGIN);
  await heading(page, 'Ringkasan operasional');
  await page.locator('[data-testid="stMetric"]').nth(7).waitFor();
}

async function chooseFilter(page, index, option) {
  const input = page.locator('[data-testid="stMultiSelect"]').nth(index).locator('input');
  await input.click();
  await page.getByRole('option', { name: option, exact: true }).click();
  await page.keyboard.press('Escape');
}

async function confirmImage(page, selector) {
  const image = page.locator(selector).first();
  await image.waitFor();
  await image.evaluate(el => el.decode());
  assert.ok(await image.evaluate(el => el.naturalWidth > 0));
}

(async () => {
  const browser = await chromium.launch({ headless: true, ...(chrome ? { executablePath: chrome } : {}) });
  try {
    const page = await browser.newPage({ viewport: { width: 1366, height: 768 }, acceptDownloads: true });
    page.setDefaultTimeout(12000);
    const errors = [];
    const mapRequests = [];
    page.on('pageerror', error => errors.push(String(error)));
    page.on('request', req => {
      if (/cartocdn\.com|tile\.openstreetmap\.org/.test(req.url())) mapRequests.push(req.url());
    });
    const measurements = [];
    const filenames = [];

    for (const [route, title, slug, expectedCharts] of routes) {
      const start = performance.now();
      await page.goto(ORIGIN + '/' + route);
      await heading(page, title);
      await page.locator('[data-testid="stPlotlyChart"]').nth(expectedCharts - 1).waitFor({ state: 'attached' });
      assert.equal(await page.locator('[data-testid="stPlotlyChart"]').count(), expectedCharts);
      if (!route) await confirmImage(page, '.st-key-report-hero img');
      measurements.push({ page: slug, ready_ms: Math.round(performance.now() - start) });
      const filename = slug + '_v2_1366.png';
      await focusMainTop(page);
      await screenshot(page, filename);
      filenames.push(filename);
    }

    await openOverview(page);
    await page.getByRole('link', { name: 'Cek dapur', exact: true }).click();
    await heading(page, 'Waktu persiapan dapur');
    await page.getByText('Payakumbuh tertinggi', { exact: true }).waitFor();
    await page.getByText(/22,4% \(49 dari 219 pesanan\)/).waitFor();

    await openOverview(page);
    await page.getByRole('link', { name: 'Cek stok', exact: true }).click();
    await heading(page, 'Persediaan bahan');
    await page.getByRole('heading', { name: 'Saus teriyaki, Payakumbuh' }).waitFor();
    await page.getByText('48 ml tersisa · batas 103 ml').waitFor();
    await page.getByRole('button', { name: 'Lihat riwayat stok' }).click();
    await page.getByRole('heading', { name: 'Riwayat stok', exact: true }).waitFor();
    await page.getByRole('heading', { name: 'Saus teriyaki · Payakumbuh', exact: true }).waitFor();

    await openOverview(page);
    await page.getByRole('link', { name: 'Cek margin', exact: true }).click();
    await heading(page, 'Biaya dan laba menu');
    await page.getByText('Family Feast Box', { exact: true }).waitFor();
    await page.getByRole('button', { name: 'Cek biaya resep' }).click();
    await page.getByRole('heading', { name: 'Bahan dan kemasan' }).waitFor();
    await page.getByText('Biaya resep per unit · Rp58.320').waitFor();
    await confirmImage(page, '.st-key-recipe-photo img');
    await screenshot(page, 'recipe_v2_1366.png');
    filenames.push('recipe_v2_1366.png');

    await openOverview(page);
    assert.equal(await page.locator('[data-testid="stMetric"]').count(), 8);
    await chooseFilter(page, 0, 'Padang');
    await chooseFilter(page, 1, 'Beverage');
    await page.getByText('Omzet kategori per pesanan', { exact: true }).waitFor();
    await page.getByRole('link', { name: 'Pesanan', exact: true }).click();
    await heading(page, 'Pesanan dan jam sibuk');
    await page.getByText(/Padang · Beverage/).waitFor();
    await page.getByRole('heading', { name: 'Omzet kategori per pesanan per kanal' }).waitFor();

    await page.getByLabel('Cari ID pesanan').fill('XXXXX');
    await page.getByLabel('Cari ID pesanan').press('Enter');
    await page.getByText('ID tersebut tidak ditemukan pada filter ini.').waitFor();
    await page.getByRole('button', { name: 'Reset filter' }).click();
    await page.getByText(/Semua cabang · Semua kategori/).waitFor();
    await page.getByLabel('Cari ID pesanan').fill('');
    await page.getByLabel('Cari ID pesanan').press('Enter');
    const download = page.waitForEvent('download');
    await page.getByRole('button', { name: 'Unduh tabel CSV' }).click();
    assert.equal((await download).suggestedFilename(), 'chickflow-orders.csv');
    await page.getByRole('button', { name: 'Lihat pesanan dan ulasan' }).click();
    await page.getByRole('heading', { name: 'Alur pesanan · V-L02' }).waitFor();
    await page.getByRole('heading', { name: 'Kata yang sering muncul · V-L01' }).waitFor();
    await page.getByText('Kata yang lebih besar muncul lebih sering.').waitFor();
    await page.getByRole('heading', { name: 'Alur pesanan · V-L02' }).scrollIntoViewIfNeeded();
    await screenshot(page, 'orders_qualitative_v2_1366.png');
    filenames.push('orders_qualitative_v2_1366.png');

    await page.goto(ORIGIN + '/sales');
    await heading(page, 'Penjualan cabang');
    assert.equal(await page.getByRole('checkbox', { name: 'Tampilkan peta dasar dari internet' }).isChecked(), false);
    const map = page.locator('.st-key-sales-map [data-testid="stPlotlyChart"]');
    await map.getByText('Payakumbuh', { exact: true }).waitFor();
    assert.deepEqual(mapRequests, []);

    if (PROTOTYPE) {
      const prototype = await browser.newPage();
      await prototype.goto(PROTOTYPE);
      await heading(prototype, 'Ringkasan operasional');
      assert.equal(await prototype.getByRole('link', { name: 'Pesanan', exact: true }).count(), 0);
      await prototype.getByRole('link', { name: 'Dapur', exact: true }).click();
      await heading(prototype, 'Waktu persiapan dapur');
      await prototype.close();
    }

    const responsive = [];
    for (const width of [1920, 768, 390]) {
      const small = await browser.newPage({ viewport: { width, height: width === 390 ? 844 : 900 } });
      await small.goto(ORIGIN);
      await heading(small, 'Ringkasan operasional');
      await small.locator('[data-testid="stMetric"]').nth(4).waitFor();
      await small.keyboard.press('Tab');
      const sizes = await small.evaluate(() => ({
        width: document.documentElement.clientWidth,
        scroll: document.documentElement.scrollWidth,
        focus: document.activeElement?.tagName,
      }));
      assert.ok(sizes.scroll <= sizes.width + 1, JSON.stringify(sizes));
      responsive.push(sizes);
      await small.evaluate(() => document.activeElement?.blur());
      const filename = 'overview_v2_' + width + '.png';
      await screenshot(small, filename);
      filenames.push(filename);
      await small.close();
    }

    assert.deepEqual(errors, []);
    fs.writeFileSync(path.join(out, 'manifest.json'), JSON.stringify({
      seed: metadata.seed, sha256: metadata.sha256, browser: browser.version(), filenames, measurements, responsive,
      filter: '24–30 Oktober 2026, semua cabang dan kategori kecuali langkah uji filter',
      checks: ['6 rute','8 KPI','3 tugas teknis','persistensi filter','reset','pencarian',
        'ekspor CSV','word cloud dan workflow','peta dengan label tanpa ubin eksternal',
        'layout 390, 768, 1366, 1920'],
    }, null, 2) + '\n');
    console.log(JSON.stringify({ passed: true, measurements, responsive, filenames }, null, 2));
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
