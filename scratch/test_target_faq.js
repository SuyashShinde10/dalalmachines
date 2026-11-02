// scratch/test_target_faq.js
const http = require('http');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const edge = spawn("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", [
  '--headless=new',
  '--remote-debugging-port=9670',
  '--user-data-dir=D:\\st.ourhtmldemo.com\\scratch\\temp_browser_profile_target',
  '--no-first-run',
  'http://localhost:5000/'
]);

setTimeout(() => {
  http.get('http://127.0.0.1:9670/json', (res) => {
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
          if (m.method === 'Runtime.consoleAPICalled') {
            console.log('[Browser Console]', m.params.type, m.params.args.map(a => a.value || a.description).join(' '));
          }
          if (m.method === 'Runtime.exceptionThrown') {
            console.error('[Browser Exception]', JSON.stringify(m.params.exceptionDetails));
          }
          if (cbs.has(m.id)) {
            const cb = cbs.get(m.id); cbs.delete(m.id); cb(m.result);
          }
        });

        await send('Runtime.enable');
        // Wait 4 seconds for full load
        await new Promise(r => setTimeout(r, 4000));

        const testRes = await send('Runtime.evaluate', {
          expression: `(function() {
            var fnExists = typeof window.toggleDalalSplitFaq;
            var items = document.querySelectorAll('.faq-minimal-item');
            var btn2 = items[1] ? items[1].querySelector('.faq-minimal-btn') : null;
            
            var beforeClasses = Array.from(items).map(i => i.className);
            
            if (btn2) {
              btn2.click();
            }
            
            var afterClasses = Array.from(items).map(i => i.className);
            
            // Now test direct call if click didn't trigger
            var directCallResult = null;
            if (btn2 && typeof window.toggleDalalSplitFaq === 'function') {
              window.toggleDalalSplitFaq(btn2);
              directCallResult = Array.from(items).map(i => i.className);
            }
            
            return {
              fnExists: fnExists,
              itemsCount: items.length,
              btn2Found: !!btn2,
              beforeClasses: beforeClasses,
              afterClasses: afterClasses,
              directCallResult: directCallResult
            };
          })()`,
          returnByValue: true
        });

        console.log("TEST EVAL RESULT:\n", JSON.stringify(testRes.result.value, null, 2));

        ws.close();
        edge.kill();
        process.exit(0);
      });
    });
  });
}, 3000);

