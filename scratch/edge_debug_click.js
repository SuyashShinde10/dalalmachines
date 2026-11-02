const http = require('http');
const { spawn } = require('child_process');

const edge = spawn('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', [
  '--headless=new',
  '--remote-debugging-port=9666',
  '--user-data-dir=D:\\st.ourhtmldemo.com\\scratch\\temp_browser_profile3',
  '--no-first-run',
  'http://localhost:5000/'
]);

setTimeout(() => {
  http.get('http://127.0.0.1:9666/json', (res) => {
    let d = ''; res.on('data', c => d += c);
    res.on('end', async () => {
      const list = JSON.parse(d);
      const target = list.find(t => t.type === 'page' && (t.url.includes('dalalmachine') || t.url === 'http://localhost:5000/')) || list[0];
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
            console.log('[Browser Console]', m.params.args.map(a => a.value || a.description).join(' '));
          }
          if (m.method === 'Runtime.exceptionThrown') {
            console.log('[Browser Exception]', m.params.exceptionDetails);
          }
          if (cbs.has(m.id)) {
            const cb = cbs.get(m.id); cbs.delete(m.id); cb(m.result);
          }
        });

        await send('Runtime.enable');

        const debugRes = await send('Runtime.evaluate', {
          expression: `(function() {
            var btn = document.querySelectorAll('.faq-minimal-btn')[1];
            var fired = false;
            var targetTag = '';
            document.addEventListener('click', function(e) {
              fired = true;
              targetTag = e.target.tagName;
            });
            btn.click();
            return {
              fired: fired,
              targetTag: targetTag,
              btnTag: btn ? btn.tagName : 'NULL',
              btnClass: btn ? btn.className : 'NULL',
              itemClass: btn ? btn.closest('.faq-minimal-item').className : 'NULL'
            };
          })()`,
          returnByValue: true
        });
        console.log('Debug result:', debugRes.result.value);

        ws.close();
        edge.kill();
        process.exit(0);
      });
    });
  });
}, 3000);

