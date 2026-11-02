const { spawn } = require('child_process');
const http = require('http');

const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const userDataDir = 'D:\\st.ourhtmldemo.com\\scratch\\temp_browser_profile';

console.log('Spawning Edge...');
const edge = spawn(edgePath, [
  '--headless=new',
  '--remote-debugging-port=9444',
  '--user-data-dir=' + userDataDir,
  '--no-first-run',
  'http://localhost:5000/'
]);

setTimeout(() => {
  http.get('http://127.0.0.1:9444/json', (res) => {
    let data = '';
    res.on('data', c => data += c);
    res.on('end', async () => {
      try {
        const list = JSON.parse(data);
        const target = list.find(t => t.type === 'page' && (t.url.includes('dalalmachine') || t.url === 'http://localhost:5000/')) || list[0];
        console.log('Chosen target:', target.url);

        const ws = new WebSocket(target.webSocketDebuggerUrl);
        let id = 1;
        const cbs = new Map();

        ws.addEventListener('open', async () => {
          const send = (method, params = {}) => new Promise(res => {
            const reqId = id++;
            cbs.set(reqId, res);
            ws.send(JSON.stringify({ id: reqId, method, params }));
          });

          ws.addEventListener('message', event => {
            const m = JSON.parse(event.data);
            if (cbs.has(m.id)) {
              const cb = cbs.get(m.id);
              cbs.delete(m.id);
              cb(m.result);
            }
          });

          await send('Runtime.enable');

          // Initial state
          const r0 = await send('Runtime.evaluate', {
            expression: `Array.from(document.querySelectorAll('.faq-minimal-item')).map(e => e.classList.contains('is-open'))`,
            returnByValue: true
          });
          console.log('Initial is-open states:', r0.result.value);

          // Click on 2nd question button
          console.log('Simulating normal click on 2nd FAQ button...');
          const r1 = await send('Runtime.evaluate', {
            expression: `(() => {
              const btn = document.querySelectorAll('.faq-minimal-btn')[1];
              btn.click();
              return Array.from(document.querySelectorAll('.faq-minimal-item')).map(e => e.classList.contains('is-open'));
            })()`,
            returnByValue: true
          });
          console.log('is-open states after clicking 2nd button:', r1.result.value);

          // Click on 3rd question CHEVRON directly
          console.log('Simulating normal click on 3rd FAQ CHEVRON icon...');
          const r2 = await send('Runtime.evaluate', {
            expression: `(() => {
              const chevron = document.querySelectorAll('.faq-minimal-btn')[2].querySelector('.faq-minimal-chevron');
              chevron.click();
              return Array.from(document.querySelectorAll('.faq-minimal-item')).map(e => e.classList.contains('is-open'));
            })()`,
            returnByValue: true
          });
          console.log('is-open states after clicking 3rd chevron:', r2.result.value);

          // Click on 3rd question again to CLOSE it
          console.log('Simulating click on 3rd FAQ to CLOSE it...');
          const r3 = await send('Runtime.evaluate', {
            expression: `(() => {
              const btn = document.querySelectorAll('.faq-minimal-btn')[2];
              btn.click();
              return Array.from(document.querySelectorAll('.faq-minimal-item')).map(e => e.classList.contains('is-open'));
            })()`,
            returnByValue: true
          });
          console.log('is-open states after clicking 3rd button again:', r3.result.value);

          ws.close();
          edge.kill();
          process.exit(0);
        });
      } catch (err) {
        console.error(err);
        edge.kill();
        process.exit(1);
      }
    });
  }).on('error', e => {
    console.error(e);
    edge.kill();
    process.exit(1);
  });
}, 3000);
