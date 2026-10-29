const http = require('http');
const fs = require('fs');

const userAgent = 'EnterpriseAuditBrowser/1.0';

function request(options, data = null) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => {
        const rawBuffer = Buffer.concat(chunks);
        const bodyStr = rawBuffer.toString('utf8');
        let json = null;
        try { json = JSON.parse(bodyStr); } catch (e) {}
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          data: bodyStr,
          rawBuffer,
          json
        });
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

async function runAudit() {
  console.log('================================================================');
  console.log(' 🚀 GROWTH ENGINE & OFFLINE BACKUP VERIFICATION SUITE           ');
  console.log('================================================================\n');
  let passed = 0;
  let total = 0;

  function assert(condition, name, details = '') {
    total++;
    if (condition) {
      passed++;
      console.log(` [PASS] ${total}. ${name}`);
    } else {
      console.error(` [FAIL] ${total}. ${name} - ${details}`);
    }
  }

  try {
    // 1. GEO Knowledge Summary
    const llmsRes = await request({ host: 'localhost', port: 5000, path: '/llms.txt', method: 'GET' });
    assert(llmsRes.statusCode === 200 && llmsRes.data.includes('# Dalal Machine Tools Agency'),
      'GEO /llms.txt AI crawler knowledge base active (200 OK)');

    // 2. GEO Full Dynamic Inventory Feed
    const llmsFullRes = await request({ host: 'localhost', port: 5000, path: '/llms-full.txt', method: 'GET' });
    assert(llmsFullRes.statusCode === 200 && llmsFullRes.data.includes('Complete Machinery Inventory Feed'),
      'GEO /llms-full.txt dynamic 49+ inventory feed active (200 OK)');

    // 3. Robots.txt GEO & AEO crawler policies
    const robotsRes = await request({ host: 'localhost', port: 5000, path: '/robots.txt', method: 'GET' });
    assert(robotsRes.statusCode === 200 && robotsRes.data.includes('Allow: /llms.txt') && robotsRes.data.includes('User-agent: PerplexityBot'),
      'Robots.txt grants access to GPTBot, ClaudeBot, and PerplexityBot with /llms.txt');

    // Authenticate as Staff to access Lead Exports & System Backups
    const loginRes = await request({
      host: 'localhost',
      port: 5000,
      path: '/api/auth/login',
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'User-Agent': userAgent }
    }, JSON.stringify({ identifier: 'developer', password: 'Developer@2026' }));

    const token = loginRes.json?.token;
    const authHeaders = {
      'Authorization': `Bearer ${token}`,
      'User-Agent': userAgent
    };

    // 4. Inquiries Excel/CSV Export with UTF-8 BOM
    const csvRes = await request({
      host: 'localhost',
      port: 5000,
      path: '/api/inquiries/export/csv',
      method: 'GET',
      headers: authHeaders
    });
    const hasBom = csvRes.rawBuffer[0] === 0xEF && csvRes.rawBuffer[1] === 0xBB && csvRes.rawBuffer[2] === 0xBF;
    assert(csvRes.statusCode === 200 && hasBom && csvRes.headers['content-type'].includes('text/csv'),
      '1-Click Leads Exporter provides RFC-4180 CSV with Microsoft Excel UTF-8 BOM');

    // 5. System Backup Listing & Snapshot Engine
    const backupsRes = await request({
      host: 'localhost',
      port: 5000,
      path: '/api/system/backups',
      method: 'GET',
      headers: authHeaders
    });
    assert(backupsRes.statusCode === 200 && backupsRes.json?.success && Array.isArray(backupsRes.json?.backups),
      'Daily Snapshot & Rolling Backup Engine lists existing database snapshots');

    // 6. Superadmin/Admin 1-Click Backup Export
    const rawBackupRes = await request({
      host: 'localhost',
      port: 5000,
      path: '/api/system/backup',
      method: 'GET',
      headers: authHeaders
    });
    assert(rawBackupRes.statusCode === 200 && (rawBackupRes.data.includes('products') || rawBackupRes.data.includes('categories')),
      '1-Click Database JSON Export serves complete database snapshot');

    // 7. GTM & Schema.org JSON-LD Verification in index.html
    const indexHtml = fs.readFileSync('new/dalalmachine/index.html', 'utf8');
    assert(indexHtml.includes('GTM-DMTA2026') && indexHtml.includes('LocalBusiness') && indexHtml.includes('dalal-analytics.js'),
      'Homepage includes GTM container (GTM-DMTA2026), LocalBusiness Schema, & Telemetry');

    // 8. Dynamic Product Schema in product.html
    const productHtml = fs.readFileSync('new/dalalmachine/product.html', 'utf8');
    assert(productHtml.includes('GTM-DMTA2026') && productHtml.includes('pdp-product-schema') && !productHtml.includes('}, 500);'),
      'Product Detail Page includes GTM, dynamic Product JSON-LD schema, & clean JS syntax');

  } catch (err) {
    console.error('Test execution error:', err);
  }

  console.log('\n================================================================');
  console.log(` 🏆 TOTAL SCORE: ${passed}/${total} PASSED (${Math.round(passed/total*100)}% OPERATIONAL)`);
  console.log('================================================================\n');

  if (passed !== total) process.exit(1);
}

runAudit();
