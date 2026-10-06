/**
 * Dalal Machine Tools Agency - Internal Test Suite Runner
 * Executes automated test cases covering:
 *  - Route & Static Assets Availability
 *  - Authentication & Role-Based Access Control (RBAC)
 *  - Inquiry / Lead Lifecycle
 *  - Product / Inventory CRUD Operations
 *  - Super Admin Master Controls & Backups
 */

const http = require('http');

const BASE_URL = 'http://localhost:5000';

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m'
};

let passedCount = 0;
let failedCount = 0;
const results = [];

function request(method, path, body = null, headers = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL);
    const reqHeaders = { ...headers };
    let requestData = null;

    if (body) {
      requestData = typeof body === 'string' ? body : JSON.stringify(body);
      if (!reqHeaders['Content-Type']) {
        reqHeaders['Content-Type'] = 'application/json';
      }
      reqHeaders['Content-Length'] = Buffer.byteLength(requestData);
    }

    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      method: method,
      headers: reqHeaders
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        let json = null;
        try {
          json = JSON.parse(data);
        } catch (e) {
          json = null;
        }
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          body: data,
          json: json
        });
      });
    });

    req.on('error', (err) => reject(err));
    if (requestData) req.write(requestData);
    req.end();
  });
}

async function runTestCase(id, name, testFn) {
  const startTime = Date.now();
  try {
    await testFn();
    const duration = Date.now() - startTime;
    passedCount++;
    results.push({ id, name, status: 'PASS', duration });
    console.log(`  ${colors.green}✔ PASS${colors.reset} [${id}] ${name} (${duration}ms)`);
  } catch (err) {
    const duration = Date.now() - startTime;
    failedCount++;
    results.push({ id, name, status: 'FAIL', duration, error: err.message });
    console.log(`  ${colors.red}✖ FAIL${colors.reset} [${id}] ${name} (${duration}ms)`);
    console.log(`         ${colors.red}Error: ${err.message}${colors.reset}`);
  }
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message || 'Assertion failed');
  }
}

async function main() {
  console.log(`\n${colors.bold}${colors.cyan}================================================================${colors.reset}`);
  console.log(`${colors.bold}${colors.cyan}   DALAL MACHINE TOOLS - INTERNAL AUTOMATED TEST SUITE          ${colors.reset}`);
  console.log(`${colors.bold}${colors.cyan}================================================================${colors.reset}\n`);

  let adminToken = '';
  let superAdminToken = '';
  let testInquiryId = '';
  let testProductId = '';

  // -------------------------------------------------------------
  // SUITE 1: Server Health & Static Routing
  // -------------------------------------------------------------
  console.log(`${colors.bold}${colors.yellow}[1] SERVER HEALTH & ROUTE DISCOVERY${colors.reset}`);

  await runTestCase('TC-SYS-01', 'API Health Check Endpoint returns 200 OK', async () => {
    const res = await request('GET', '/api/health');
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.json && res.json.status === 'ok', 'Status is not ok');
  });

  await runTestCase('TC-SYS-02', 'Customer Website Root (/new/dalalmachine/) returns 200 OK', async () => {
    const res = await request('GET', '/new/dalalmachine/');
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.body.includes('Dalal Machine') || res.body.includes('dalalmachine'), 'Missing expected title/content');
  });

  await runTestCase('TC-SYS-03', 'Customer Catalog (/new/dalalmachine/category.html) returns 200 OK', async () => {
    const res = await request('GET', '/new/dalalmachine/category.html');
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.body.includes('dalal-custom.css'), 'Missing custom CSS link');
  });

  await runTestCase('TC-SYS-04', 'Staff Admin Login (/admin/index.html) returns 200 OK', async () => {
    const res = await request('GET', '/admin/index.html');
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.body.includes('Staff Operations Portal'), 'Missing portal title');
  });

  await runTestCase('TC-SYS-05', 'Staff Admin Dashboard (/admin/dashboard.html) returns 200 OK', async () => {
    const res = await request('GET', '/admin/dashboard.html');
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.body.includes('admin-core.js'), 'Missing admin core script');
  });

  await runTestCase('TC-SYS-06', 'Super Admin Login (/superadmin/index.html) returns 200 OK', async () => {
    const res = await request('GET', '/superadmin/index.html');
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.body.includes('Master Executive Portal') || res.body.includes('Super Admin'), 'Missing Super Admin portal title');
  });

  await runTestCase('TC-SYS-07', 'Super Admin Dashboard (/superadmin/dashboard.html) returns 200 OK', async () => {
    const res = await request('GET', '/superadmin/dashboard.html');
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.body.includes('superadmin-core.js'), 'Missing super admin core script');
  });

  // -------------------------------------------------------------
  // SUITE 2: Authentication & RBAC (Role-Based Access Control)
  // -------------------------------------------------------------
  console.log(`\n${colors.bold}${colors.yellow}[2] AUTHENTICATION & ROLE-BASED ACCESS CONTROL (RBAC)${colors.reset}`);

  await runTestCase('TC-AUTH-01', 'Login with invalid password returns 401 Unauthorized', async () => {
    const res = await request('POST', '/api/auth/login', {
      identifier: 'admin',
      password: 'IncorrectPassword_999'
    });
    assert(res.statusCode === 401, `Expected 401, got ${res.statusCode}`);
    assert(res.json && res.json.success === false, 'Expected success=false');
  });

  await runTestCase('TC-AUTH-02', 'Staff Admin login succeeds with valid credentials', async () => {
    const res = await request('POST', '/api/auth/login', {
      identifier: 'admin',
      password: 'Dalal@Admin2026'
    });
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.json && res.json.token, 'Token missing in response');
    assert(res.json.user.role === 'admin', `Expected role=admin, got ${res.json.user.role}`);
    adminToken = res.json.token;
  });

  await runTestCase('TC-AUTH-03', 'Super Admin login succeeds with master credentials', async () => {
    const res = await request('POST', '/api/auth/login', {
      identifier: 'developer',
      password: 'Developer@2026'
    });
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.json && res.json.token, 'Token missing in response');
    assert(res.json.user.role === 'superadmin', `Expected role=superadmin, got ${res.json.user.role}`);
    superAdminToken = res.json.token;
  });

  await runTestCase('TC-AUTH-04', 'Staff Admin is FORBIDDEN (403) from accessing Super Admin users list', async () => {
    const res = await request('GET', '/api/users', null, {
      Authorization: `Bearer ${adminToken}`
    });
    assert(res.statusCode === 403, `Expected 403 Forbidden for staff admin, got ${res.statusCode}`);
  });

  await runTestCase('TC-AUTH-05', 'Staff Admin is FORBIDDEN (403) from accessing audit logs', async () => {
    const res = await request('GET', '/api/logs', null, {
      Authorization: `Bearer ${adminToken}`
    });
    assert(res.statusCode === 403, `Expected 403 Forbidden for staff admin, got ${res.statusCode}`);
  });

  await runTestCase('TC-AUTH-06', 'Super Admin can successfully access audit logs', async () => {
    const res = await request('GET', '/api/logs', null, {
      Authorization: `Bearer ${superAdminToken}`
    });
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.json && Array.isArray(res.json.logs), 'Expected logs array');
  });

  await runTestCase('TC-AUTH-07', 'Super Admin can successfully list system accounts', async () => {
    const res = await request('GET', '/api/users', null, {
      Authorization: `Bearer ${superAdminToken}`
    });
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.json && Array.isArray(res.json.users), 'Expected users array');
    assert(res.json.users.length >= 2, 'Expected at least admin and developer accounts');
  });

  // -------------------------------------------------------------
  // SUITE 3: Customer RFQ / Inquiry Lifecycle
  // -------------------------------------------------------------
  console.log(`\n${colors.bold}${colors.yellow}[3] CUSTOMER INQUIRY / LEAD LIFECYCLE${colors.reset}`);

  await runTestCase('TC-INQ-01', 'Public customer can submit a quotation request (POST /api/inquiries)', async () => {
    const payload = {
      name: 'Automated Test Client',
      email: 'qa-tester@dalaltest.com',
      phone: '+91 98000 11122',
      company: 'Test Precision Engg',
      machineName: 'DMTA High-Precision Press',
      message: 'Automated E2E test inquiry verifying pipeline responsiveness.'
    };
    const res = await request('POST', '/api/inquiries', payload);
    assert(res.statusCode === 201, `Expected 201 Created, got ${res.statusCode}`);
    assert(res.json && res.json.inquiryId, 'Missing inquiryId in response');
    testInquiryId = res.json.inquiryId;
  });

  await runTestCase('TC-INQ-02', 'Staff Admin can view inquiry list and find submitted lead', async () => {
    const res = await request('GET', '/api/inquiries', null, {
      Authorization: `Bearer ${adminToken}`
    });
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    const found = res.json.inquiries.find(i => i.id === testInquiryId);
    assert(found, `Submitted inquiry ${testInquiryId} not found in admin list`);
    assert(found.status === 'new', `Expected initial status 'new', got ${found.status}`);
  });

  await runTestCase('TC-INQ-03', 'Staff Admin can update inquiry status to "contacted"', async () => {
    const res = await request('PUT', `/api/inquiries/${testInquiryId}`, { status: 'contacted' }, {
      Authorization: `Bearer ${adminToken}`
    });
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.json.inquiry.status === 'contacted', `Expected status 'contacted', got ${res.json.inquiry.status}`);
  });

  // -------------------------------------------------------------
  // SUITE 4: Inventory / Machine Catalog Operations
  // -------------------------------------------------------------
  console.log(`\n${colors.bold}${colors.yellow}[4] INVENTORY & MACHINE SPECIFICATIONS CRUD${colors.reset}`);

  await runTestCase('TC-PROD-01', 'Staff Admin can create a new machine (POST /api/products)', async () => {
    const testMachine = {
      name: 'QA Test Auto-Lathe 400',
      section: 'cutting',
      category: 'CNC Lathes',
      manufacturer: 'DMTA Test Lab',
      year: '2024',
      price: '₹ 12,50,000',
      condition: 'Bench Tested',
      location: 'Pune Facility',
      status: 'active',
      isCustom: false,
      specs: {
        'Spindle Bore': '52 mm',
        'Bed Length': '1000 mm',
        'Motor Power': '7.5 kW'
      }
    };
    const res = await request('POST', '/api/products', testMachine, {
      Authorization: `Bearer ${adminToken}`
    });
    assert(res.statusCode === 201, `Expected 201 Created, got ${res.statusCode}`);
    assert(res.json && res.json.product && res.json.product.id, 'Missing created product');
    testProductId = res.json.product.id;
  });

  await runTestCase('TC-PROD-02', 'Public Catalog (GET /api/products) includes newly created machine', async () => {
    const res = await request('GET', '/api/products');
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    const found = res.json.products.find(p => p.id === testProductId);
    assert(found, `New machine ${testProductId} not found in public catalog`);
    assert(found.name === 'QA Test Auto-Lathe 400', 'Name mismatch');
  });

  await runTestCase('TC-PROD-03', 'Staff Admin can update machine details (PUT /api/products/:id)', async () => {
    const updatePayload = {
      price: '₹ 13,00,000',
      condition: 'Ready for Immediate Dispatch'
    };
    const res = await request('PUT', `/api/products/${testProductId}`, updatePayload, {
      Authorization: `Bearer ${adminToken}`
    });
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.json.product.price === '₹ 13,00,000', 'Price was not updated');
    assert(res.json.product.condition === 'Ready for Immediate Dispatch', 'Condition was not updated');
  });

  await runTestCase('TC-PROD-04', 'Staff Admin can clean up test machine (DELETE /api/products/:id)', async () => {
    const res = await request('DELETE', `/api/products/${testProductId}`, null, {
      Authorization: `Bearer ${adminToken}`
    });
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
  });

  await runTestCase('TC-PROD-05', 'Deleted machine is no longer retrieved (GET /api/products/:id returns 404)', async () => {
    const res = await request('GET', `/api/products/${testProductId}`);
    assert(res.statusCode === 404, `Expected 404 Not Found after deletion, got ${res.statusCode}`);
  });

  // -------------------------------------------------------------
  // SUITE 5: Super Admin Governance & Snapshot Backup
  // -------------------------------------------------------------
  console.log(`\n${colors.bold}${colors.yellow}[5] SUPER ADMIN GOVERNANCE & SNAPSHOT BACKUP${colors.reset}`);

  await runTestCase('TC-SYS-08', 'Super Admin can retrieve system telemetry & stats', async () => {
    const res = await request('GET', '/api/system/stats', null, {
      Authorization: `Bearer ${superAdminToken}`
    });
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.json && res.json.stats, 'Missing stats object');
    assert(typeof res.json.stats.totalMachines === 'number', 'Invalid machine count');
    assert(typeof res.json.stats.memoryUsageMB === 'number', 'Invalid memory usage metric');
  });

  await runTestCase('TC-SYS-09', 'Super Admin can export full JSON DB backup snapshot', async () => {
    const res = await request('GET', '/api/system/backup', null, {
      Authorization: `Bearer ${superAdminToken}`
    });
    assert(res.statusCode === 200, `Expected 200, got ${res.statusCode}`);
    assert(res.json && Array.isArray(res.json.products), 'Backup missing products table');
    assert(Array.isArray(res.json.users), 'Backup missing users table');
    assert(Array.isArray(res.json.inquiries), 'Backup missing inquiries table');
  });

  // -------------------------------------------------------------
  // Summary Report
  // -------------------------------------------------------------
  console.log(`\n${colors.bold}${colors.cyan}================================================================${colors.reset}`);
  console.log(`${colors.bold}${colors.cyan}                       TEST EXECUTION SUMMARY                   ${colors.reset}`);
  console.log(`${colors.bold}${colors.cyan}================================================================${colors.reset}`);
  console.log(`  Total Test Cases : ${results.length}`);
  console.log(`  ${colors.green}Passed           : ${passedCount}${colors.reset}`);
  console.log(`  ${failedCount > 0 ? colors.red : colors.green}Failed           : ${failedCount}${colors.reset}`);
  console.log(`  Success Rate     : ${Math.round((passedCount / results.length) * 100)}%`);
  console.log(`${colors.bold}${colors.cyan}================================================================${colors.reset}\n`);

  if (failedCount > 0) {
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Fatal Test Runner Error:', err);
  process.exit(1);
});
