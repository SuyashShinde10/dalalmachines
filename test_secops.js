const http = require('http');

function makeRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          body: data
        });
      });
    });
    req.on('error', reject);
    if (postData) {
      req.write(postData);
    }
    req.end();
  });
}

async function runSecOpsTestSuite() {
  console.log('===============================================================');
  console.log(' 🛡️ RUNNING COMPREHENSIVE SECOPS & INTRUSION DEFENSE TEST SUITE');
  console.log('===============================================================');

  let passed = 0;
  let total = 0;

  function assert(testName, condition, detail = '') {
    total++;
    if (condition) {
      passed++;
      console.log(`[PASS] ${testName}`);
    } else {
      console.error(`[FAIL] ${testName} -> ${detail}`);
    }
  }

  try {
    // 1. Public website must load 200 OK
    const resPublic = await makeRequest({
      hostname: '127.0.0.1',
      port: 5000,
      path: '/',
      method: 'GET'
    });
    assert('1. Public Homepage Accessible (200 OK)', resPublic.statusCode === 200);

    // 2. Unauthenticated probe on /admin must return 404 (Cloaked Decoy)
    const resAdmin404 = await makeRequest({
      hostname: '127.0.0.1',
      port: 5000,
      path: '/admin',
      method: 'GET'
    });
    assert('2. Unauthenticated /admin Cloaked as 404 Not Found', resAdmin404.statusCode === 404, `Got ${resAdmin404.statusCode}`);

    // 3. Unauthenticated probe on /dev must return 404
    const resDev404 = await makeRequest({
      hostname: '127.0.0.1',
      port: 5000,
      path: '/dev',
      method: 'GET'
    });
    assert('3. Unauthenticated /dev Cloaked as 404 Not Found', resDev404.statusCode === 404, `Got ${resDev404.statusCode}`);

    // 4. Unauthenticated probe on /superadmin/dashboard.html must return 404
    const resSuper404 = await makeRequest({
      hostname: '127.0.0.1',
      port: 5000,
      path: '/superadmin/dashboard.html',
      method: 'GET'
    });
    assert('4. Unauthenticated /superadmin/dashboard.html Cloaked as 404', resSuper404.statusCode === 404, `Got ${resSuper404.statusCode}`);

    // 5. Honeypot Trap probe on /wp-admin
    const resHoneypot = await makeRequest({
      hostname: '127.0.0.1',
      port: 5000,
      path: '/wp-admin/setup-config.php',
      method: 'GET',
      headers: { 'User-Agent': 'Sqlmap/1.4.7#stable' }
    });
    assert('5. Honeypot Trap /wp-admin catches scanner & returns 404', resHoneypot.statusCode === 404);

    // 6. Invalid Gateway key probe must return 404
    const resInvalidGate = await makeRequest({
      hostname: '127.0.0.1',
      port: 5000,
      path: '/portal-gate?key=wrong_passcode_xyz',
      method: 'GET'
    });
    assert('6. Invalid Portal Gateway Key Cloaked as 404', resInvalidGate.statusCode === 404);

    // 7. Authorized Gateway Entry with valid key
    const resValidGate = await makeRequest({
      hostname: '127.0.0.1',
      port: 5000,
      path: '/portal-gate?key=dmta-ops-2026&to=admin',
      method: 'GET'
    });
    const setCookie = resValidGate.headers['set-cookie'] || [];
    const hasGateCookie = setCookie.some(c => c.includes('dmta_gate_pass='));
    assert('7. Valid Gateway Key Issues Signed dmta_gate_pass Cookie & Redirects (302)', resValidGate.statusCode === 302 && hasGateCookie);

    // Extract cookie
    let gateCookieVal = '';
    for (const c of setCookie) {
      if (c.includes('dmta_gate_pass=')) {
        gateCookieVal = c.split(';')[0];
        break;
      }
    }

    // 8. With Gateway Cookie, access to /admin/ and login page is unlocked (200 OK)
    const resAdminUnlocked = await makeRequest({
      hostname: '127.0.0.1',
      port: 5000,
      path: '/admin/',
      method: 'GET',
      headers: { 'Cookie': gateCookieVal }
    });
    assert('8. Carrying Gateway Cookie Unlocks Admin Portal (200 OK)', resAdminUnlocked.statusCode === 200, `Got ${resAdminUnlocked.statusCode}`);

    // 9. With Gateway Cookie, developer console /dev/ is accessible
    const resDevUnlocked = await makeRequest({
      hostname: '127.0.0.1',
      port: 5000,
      path: '/dev/',
      method: 'GET',
      headers: { 'Cookie': gateCookieVal }
    });
    assert('9. Carrying Gateway Cookie Unlocks Developer Console (200 OK)', resDevUnlocked.statusCode === 200, `Got ${resDevUnlocked.statusCode}`);

    // 10. Check Security Status API from Developer Console
    const resSecApi = await makeRequest({
      hostname: '127.0.0.1',
      port: 5000,
      path: '/api/dev/security/status',
      method: 'GET',
      headers: { 'Cookie': gateCookieVal }
    });
    const secData = JSON.parse(resSecApi.body);
    assert('10. /api/dev/security/status returns live telemetry', secData.success === true && secData.totalEvents > 0, `Total events: ${secData.totalEvents}`);

    console.log('===============================================================');
    console.log(` 🛡️ TEST RESULTS: ${passed}/${total} PASSED (${Math.round(passed/total * 100)}%)`);
    console.log('===============================================================');

    if (passed === total) {
      console.log('ALL SECOPS DEFENSES VERIFIED 100% OPERATIONAL!');
      process.exit(0);
    } else {
      process.exit(1);
    }
  } catch (err) {
    console.error('Test execution error:', err);
    process.exit(1);
  }
}

runSecOpsTestSuite();
