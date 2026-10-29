const http = require('http');

const domain = process.argv[2] || 'http://localhost:5000';
const parsedUrl = new URL(domain);

const sensitivePaths = [
  '/.env',
  '/.env.local',
  '/.env.production',
  '/.env.development',
  '/.env.backup',
  '/.env.bak',
  '/.env.old',
  '/.git/config',
  '/.git/HEAD',
  '/.gitignore',
  '/.DS_Store',
  '/.vscode/settings.json',
  '/.idea/workspace.xml',
  '/backup.zip',
  '/backup.tar.gz',
  '/db.sql',
  '/dump.sql',
  '/database.sql',
  '/database.sqlite',
  '/data.db',
  '/config.json',
  '/config.yml',
  '/docker-compose.yml',
  '/.npmrc',
  '/phpinfo.php',
  '/server-status',
  '/swagger.json',
  '/openapi.json',
  '/graphql'
];

function checkPath(path) {
  return new Promise((resolve) => {
    const req = http.request({
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
      path: path,
      method: 'GET',
      headers: { 'User-Agent': 'SecurityScanner-Check23/1.0' }
    }, (res) => {
      resolve({ path, status: res.statusCode });
    });
    req.on('error', (err) => resolve({ path, status: 'ERR', error: err.message }));
    req.end();
  });
}

async function runExposedCheck() {
  console.log(`================================================================`);
  console.log(` Check 23: Exposed Files & Information Leakage Audit`);
  console.log(` Target: ${domain}`);
  console.log(`================================================================\n`);

  let leaked = 0;
  let secured = 0;

  for (const p of sensitivePaths) {
    const result = await checkPath(p);
    const isSafe = result.status === 404 || result.status === 403;
    const statusText = isSafe ? `[SAFE ${result.status}]` : `[LEAK ${result.status}]`;
    console.log(`  ${statusText.padEnd(12)} ${p}`);
    if (isSafe) secured++;
    else leaked++;
  }

  console.log(`\n================================================================`);
  console.log(` Summary: ${secured}/${sensitivePaths.length} paths blocked (404/403). Leaks: ${leaked}`);
  console.log(`================================================================`);

  if (leaked > 0) process.exit(1);
}

runExposedCheck();

