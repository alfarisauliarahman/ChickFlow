const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '../..');
const origin = process.env.CHICKFLOW_URL || 'http://127.0.0.1:8516';
const executablePath = process.env.CHICKFLOW_CHROME;
const profiles = [
  { id:'SIM-01', role:'Pengguna baru', viewport:{width:1366,height:768}, method:'menu' },
  { id:'SIM-02', role:'Manajer operasional', viewport:{width:1920,height:1080}, method:'alert' },
  { id:'SIM-03', role:'Staf persediaan', viewport:{width:1024,height:768}, method:'menu', criticalOnly:true },
  { id:'SIM-04', role:'Pengguna keyboard', viewport:{width:1366,height:768}, method:'keyboard' },
  { id:'SIM-05', role:'Pemilik melalui ponsel', viewport:{width:390,height:844}, method:'alert', mobile:true },
];

const tasks = [
  { id:'A', module:'Dapur', action:'Cek dapur', heading:'Waktu persiapan dapur',
    route:'/kitchen', frame:'Kitchen Performance' },
  { id:'B', module:'Stok', action:'Cek stok', heading:'Persediaan bahan',
    route:'/inventory', frame:'Inventory' },
  { id:'C', module:'Biaya dan laba', action:'Cek margin', heading:'Biaya dan laba menu',
    route:'/profit', frame:'Food Cost & Profit' },
];

function figcraftWalkthrough() {
  const filename = path.join(root, 'reports/design/ChickFlow-Prototype.figcraft');
  const document = JSON.parse(execFileSync('unzip', ['-p', filename, 'document.json'],
    { encoding:'utf8', maxBuffer:8 * 1024 * 1024 }));
  const nodes = document.nodes;
  const canvas = nodes[document.pages[0]];
  const frames = Object.fromEntries(canvas.children.map(id => [nodes[id].name, nodes[id]]));
  const content = name => frames[name].children.map(id => nodes[id]);
  const text = (name, value) => content(name).some(node => node.characters === value);
  const link = (from, label, to) => content(from).some(node =>
    node.characters === label && (node.interactions || []).some(interaction =>
      interaction.actions.some(action => action.type === 'navigate' && nodes[action.dest].name === to)));
  const results = [];
  for (const profile of profiles) {
    const home = profile.mobile ? 'Overview · Mobile' : 'Overview';
    for (const task of tasks) {
      const label = profile.mobile ? ({ A:'Dapur', B:'Cek stok', C:'Laba' }[task.id]) :
        profile.method === 'alert' ? task.action : task.module;
      const primary = link(home, label, task.frame);
      const detail = task.id === 'B' ? 'Inventory · Riwayat mutasi' :
        task.id === 'C' ? 'Profit · Biaya resep' : null;
      const detailLabel = task.id === 'B' ? 'Lihat riwayat stok' : 'Cek biaya resep';
      const answer = task.id === 'A' ? text('Overview','22,4%') && text('Overview','Payakumbuh') :
        task.id === 'B' ? content(task.frame).some(node => /48 ml tersisa.+103 ml/.test(node.characters || '')) :
        text(detail,'Family Feast Box') && text(detail,'Rp58.320');
      results.push({ profile:profile.id, task:task.id, start_frame:home, action:label, module:task.frame,
        detail, linked:primary && (!detail || link(task.frame, detailLabel, detail)),
        answer_present:answer, destination_width:frames[task.frame].width });
    }
  }
  return results;
}

async function openOverview(page) {
  await page.goto(origin);
  await page.getByRole('heading',{name:'Ringkasan operasional',exact:true}).waitFor();
  await page.getByRole('link',{name:'Cek margin',exact:true}).waitFor();
}

async function keyActivate(page, locator) {
  await locator.waitFor();
  for (let i=0; i<70; i++) {
    if (await locator.evaluate(el => el === document.activeElement || el.contains(document.activeElement))) {
      await page.keyboard.press('Enter');
      return i;
    }
    await page.keyboard.press('Tab');
  }
  throw new Error('Kontrol belum tercapai setelah 70 langkah Tab.');
}

async function activate(page, profile, locator) {
  if (profile.method === 'keyboard') return keyActivate(page, locator);
  await locator.click();
  return null;
}

async function firstScreen(page) {
  const height = page.viewportSize().height;
  const observed = {};
  for (const label of ['Perlu diperiksa','Cek stok','Cek dapur','Cek margin']) {
    const locator = label === 'Perlu diperiksa' ? page.getByRole('heading',{name:label,exact:true}) :
      page.getByRole('link',{name:label,exact:true});
    const box = await locator.boundingBox();
    observed[label] = box ? { y:Math.round(box.y), fully_visible:box.y >= 0 && box.y+box.height <= height } : null;
  }
  return observed;
}

async function execute(page, profile, task) {
  const label = profile.method === 'alert' ? task.action : task.module;
  const entryTabs = await activate(page, profile, page.getByRole('link',{name:label,exact:true}));
  await page.getByRole('heading',{name:task.heading,exact:true}).waitFor();
  assert.equal(new URL(page.url()).pathname, task.route);
  let observed;
  let detailTabs = null;
  if (task.id === 'A') {
    await page.getByText('Payakumbuh tertinggi',{exact:true}).waitFor();
    await page.getByText(/22,4% \(49 dari 219 pesanan\)/).waitFor();
    observed = 'Payakumbuh · 22,4% (49 dari 219 pesanan)';
  } else if (task.id === 'B') {
    await page.getByRole('heading',{name:'Saus teriyaki, Payakumbuh',exact:true}).waitFor();
    await page.getByText('48 ml tersisa · batas 103 ml',{exact:true}).waitFor();
    if (profile.criticalOnly) {
      await page.getByText('Hanya bahan kritis',{exact:true}).click();
      await page.waitForFunction(() =>
        document.querySelector('input[aria-label="Hanya bahan kritis"]')?.checked ||
        [...document.querySelectorAll('[data-testid="stCheckbox"]')].some(el =>
          el.textContent.includes('Hanya bahan kritis') && el.querySelector('input')?.checked));
    }
    detailTabs = await activate(page, profile, page.getByRole('button',{name:'Lihat riwayat stok',exact:true}));
    await page.getByRole('heading',{name:'Riwayat stok',exact:true}).waitFor();
    await page.getByRole('heading',{name:'Saus teriyaki · Payakumbuh',exact:true}).waitFor();
    observed = 'Saus teriyaki · Payakumbuh · 48 ml dari batas 103 ml; riwayat terbuka';
  } else {
    await page.getByText('Family Feast Box',{exact:true}).waitFor();
    detailTabs = await activate(page, profile, page.getByRole('button',{name:'Cek biaya resep',exact:true}));
    await page.getByRole('heading',{name:'Bahan dan kemasan',exact:true}).waitFor();
    await page.getByText('Biaya resep per unit · Rp58.320',{exact:true}).waitFor();
    observed = 'Family Feast Box · biaya resep Rp58.320 per unit';
  }
  assert.equal(await page.locator('[data-testid="stException"]').count(),0);
  return { task:task.id, passed:true, entry:label, observed, entry_tabs:entryTabs, detail_tabs:detailTabs };
}

(async () => {
  const figcraft = figcraftWalkthrough();
  const browser = await chromium.launch({headless:true, ...(executablePath ? {executablePath} : {})});
  try {
    const attempts = [];
    for (const profile of profiles) {
      const context = await browser.newContext({viewport:profile.viewport, hasTouch:!!profile.mobile, locale:'id-ID'});
      const profileResults = [];
      let startView;
      for (const task of tasks) {
        const page = await context.newPage();
        page.setDefaultTimeout(8000);
        try {
          await openOverview(page);
          if (!startView) startView = await firstScreen(page);
          profileResults.push(await execute(page, profile, task));
        } catch (error) {
          profileResults.push({task:task.id,passed:false,error:error.message.split('\n')[0]});
        } finally {
          await page.close();
        }
      }
      await context.close();
      attempts.push({...profile, initial_view:startView, streamlit:profileResults});
      console.log(profile.id, profileResults.map(result =>
        result.task+':'+(result.passed?'lulus':result.error)).join(' '));
    }
    const date = new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Jakarta'}).format(new Date());
    const archive = { method:'evaluasi AI berbasis skenario', human_participants:0, assessment_date:date,
      scope:'24–30 Oktober 2026, semua cabang dan kategori, seed 20261001',
      browser:browser.version(), figcraft_structural_check:figcraft, scenarios:attempts };
    const output = process.env.CHICKFLOW_WALKTHROUGH_OUTPUT ||
      path.join(root,'reports/prototype/walkthrough-ai-retest.json');
    fs.writeFileSync(output, JSON.stringify(archive,null,2)+'\n');
    console.log('FigCraft:', figcraft.filter(row=>row.linked&&row.answer_present).length+'/'+figcraft.length, 'jalur/bukti.');
    console.log('Streamlit:', attempts.flatMap(row=>row.streamlit).filter(row=>row.passed).length+'/15', 'jalur UI.');
  } finally {
    await browser.close();
  }
})().catch(error=>{console.error(error); process.exit(1)});
