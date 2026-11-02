// scratch/test_live_faq.js
const http = require('http');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const EDGE_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const PORT = 9668;
const USER_DATA_DIR = path.join(__dirname, 'temp_edge_faq_test2');

const edge = spawn(EDGE_PATH, [
  '--headless=new',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${USER_DATA_DIR}`,
  '--no-first-run',
  'http://localhost:5000/'
]);

setTimeout(() => {
  http.get(`http://127.0.0.1:${PORT}/json`, (res) => {
    let d = ''; res.on('data', c => d += c);
    res.on('end', async () => {
      const list = JSON.parse(d);
      const target = list.find(t => t.type === 'page') || list[0];
      const ws = new WebSocket(target.webSocketDebuggerUrl);

      ws.addEventListener('open', async () => {
        let id = 1;
        const cbs = new Map();
        const send = (method, params = {}) => new Promise(r => {
          const reqId = id++; cbs.set(reqId, r);
          ws.send(JSON.stringify({ id: reqId, method, params }));
        });

        ws.addEventListener('message', ev => {
          const m = JSON.parse(ev.data);
          if (cbs.has(m.id)) {
            const cb = cbs.get(m.id); cbs.delete(m.id); cb(m.result);
          }
        });

        await send('Runtime.enable');
        // Wait 1.5s for page script & DOM to be completely initialized
        await new Promise(r => setTimeout(r, 1500));

        // Initial check: Q1 open, Q2-Q7 closed
        const state0 = await send('Runtime.evaluate', {
          expression: `Array.from(document.querySelectorAll('.faq-minimal-item')).map(i => i.classList.contains('is-open'))`,
          returnByValue: true
        });
        console.log('1. Initial State (Q1 open):', state0.result.value);

        // Click Question 2 button
        const clickQ2 = await send('Runtime.evaluate', {
          expression: `(function() {
            var btns = document.querySelectorAll('.faq-minimal-btn');
            btns[1].click();
            return Array.from(document.querySelectorAll('.faq-minimal-item')).map(i => i.classList.contains('is-open'));
          })()`,
          returnByValue: true
        });
        console.log('2. State After Clicking Q2:', clickQ2.result.value);

        // Click Question 3 question span
        const clickQ3Span = await send('Runtime.evaluate', {
          expression: `(function() {
            var spans = document.querySelectorAll('.faq-minimal-question');
            spans[2].click();
            return Array.from(document.querySelectorAll('.faq-minimal-item')).map(i => i.classList.contains('is-open'));
          })()`,
          returnByValue: true
        });
        console.log('3. State After Clicking Q3 Text Span:', clickQ3Span.result.value);

        // Click Question 6 chevron icon
        const clickQ6Chevron = await send('Runtime.evaluate', {
          expression: `(function() {
            var chevrons = document.querySelectorAll('.faq-minimal-chevron');
            chevrons[5].click();
            return Array.from(document.querySelectorAll('.faq-minimal-item')).map(i => i.classList.contains('is-open'));
          })()`,
          returnByValue: true
        });
        console.log('4. State After Clicking Q6 Chevron Icon:', clickQ6Chevron.result.value);

        // Re-click Question 6 to collapse it
        const reclickQ6 = await send('Runtime.evaluate', {
          expression: `(function() {
            var btns = document.querySelectorAll('.faq-minimal-btn');
            btns[5].click();
            return Array.from(document.querySelectorAll('.faq-minimal-item')).map(i => i.classList.contains('is-open'));
          })()`,
          returnByValue: true
        });
        console.log('5. State After Re-Clicking Q6 (Should Collapse All):', reclickQ6.result.value);

        ws.close();
        edge.kill();
        try { fs.rmSync(USER_DATA_DIR, { recursive: true, force: true }); } catch (e) {}
        process.exit(0);
      });
    });
  });
}, 3000);
