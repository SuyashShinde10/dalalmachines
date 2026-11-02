// scratch/check_page_overflows.js
const http = require('http');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const EDGE_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const PORT = 9777;
const USER_DATA_DIR = path.join(__dirname, 'temp_edge_overflow_test');

const htmlPath = path.resolve('DALAL_AND_OMPI_57_PAGES_AND_MODULES_MASTER_SPECIFICATION.html').replace(/\\/g, '/');

const edge = spawn(EDGE_PATH, [
  '--headless=new',
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${USER_DATA_DIR}`,
  '--no-first-run',
  `file:///${htmlPath}`
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
        await new Promise(r => setTimeout(r, 2000));

        const report = await send('Runtime.evaluate', {
          expression: `(function() {
            var pages = document.querySelectorAll('.page');
            var results = [];
            for (var i = 0; i < pages.length; i++) {
              var p = pages[i];
              var content = p.querySelector('.page-content');
              var footer = p.querySelector('.footer-bar');
              var totalScroll = (content ? content.scrollHeight : 0) + (footer ? footer.offsetHeight : 0);
              var clientH = p.clientHeight;
              results.push({
                pageIndex: i + 1,
                clientH: clientH,
                totalScroll: totalScroll,
                overflowPx: totalScroll - clientH,
                isOverflowing: totalScroll > clientH
              });
            }
            return results;
          })()`,
          returnByValue: true
        });

        console.log("PAGE OVERFLOW AUDIT:");
        var overs = report.result.value.filter(r => r.isOverflowing);
        console.log("Total overflowing pages:", overs.length);
        overs.forEach(o => console.log(`Page ${o.pageIndex}: overflow by ${o.overflowPx}px (content: ${o.totalScroll}px > page: ${o.clientH}px)`));

        ws.close();
        edge.kill();
        try { fs.rmSync(USER_DATA_DIR, { recursive: true, force: true }); } catch (e) {}
        process.exit(0);
      });
    });
  });
}, 3000);
