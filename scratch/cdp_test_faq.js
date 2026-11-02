const http = require('http');

http.get('http://127.0.0.1:9333/json', async (res) => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', async () => {
    const list = JSON.parse(data);
    const target = list.find(t => t.type === 'page' && t.url.includes('5000')) || list[0];
    console.log('Target URL:', target.url);

    const ws = new WebSocket(target.webSocketDebuggerUrl);
    let msgId = 1;
    const callbacks = new Map();

    ws.on('open', () => {
      function send(method, params = {}) {
        return new Promise((resolve) => {
          const id = msgId++;
          callbacks.set(id, resolve);
          ws.send(JSON.stringify({ id, method, params }));
        });
      }

      ws.on('message', (raw) => {
        const msg = JSON.parse(raw);
        if (msg.method === 'Runtime.consoleAPICalled') {
          console.log('[Browser Console]', msg.params.type, msg.params.args.map(a => a.value || a.description).join(' '));
        }
        if (msg.method === 'Runtime.exceptionThrown') {
          console.log('[Browser Exception]', msg.params.exceptionDetails.text, msg.params.exceptionDetails.exception?.description);
        }
        if (callbacks.has(msg.id)) {
          const cb = callbacks.get(msg.id);
          callbacks.delete(msg.id);
          cb(msg.result);
        }
      });

      async function run() {
        await send('Runtime.enable');
        await send('Log.enable');

        // Check typeof toggleDalalSplitFaq
        const r1 = await send('Runtime.evaluate', { expression: 'typeof window.toggleDalalSplitFaq' });
        console.log('typeof window.toggleDalalSplitFaq:', r1.result.value);

        // Check initial state of items
        const r2 = await send('Runtime.evaluate', {
          expression: `(() => {
            return Array.from(document.querySelectorAll('.faq-minimal-item')).map((el, i) => ({
              idx: i,
              isOpen: el.classList.contains('is-open'),
              q: el.querySelector('.faq-minimal-question') ? el.querySelector('.faq-minimal-question').textContent.trim().slice(0, 35) : ''
            }));
          })()`,
          returnByValue: true
        });
        console.log('Initial items:', JSON.stringify(r2.result.value, null, 2));

        // Click the 2nd button
        console.log('Clicking 2nd FAQ button...');
        const r3 = await send('Runtime.evaluate', {
          expression: `(() => {
            const btns = document.querySelectorAll('.faq-minimal-btn');
            console.log('Found buttons:', btns.length);
            if (btns[1]) {
              btns[1].click();
            }
            return Array.from(document.querySelectorAll('.faq-minimal-item')).map((el, i) => ({
              idx: i,
              isOpen: el.classList.contains('is-open'),
              maxHeight: window.getComputedStyle(el.querySelector('.faq-minimal-answer')).maxHeight,
              opacity: window.getComputedStyle(el.querySelector('.faq-minimal-answer')).opacity
            }));
          })()`,
          returnByValue: true
        });
        console.log('State after clicking 2nd button:', JSON.stringify(r3.result.value, null, 2));

        // Now test clicking on Question 1 to see if it toggles
        console.log('Clicking 1st FAQ button (which was closed)...');
        const r4 = await send('Runtime.evaluate', {
          expression: `(() => {
            const btns = document.querySelectorAll('.faq-minimal-btn');
            if (btns[0]) btns[0].click();
            return Array.from(document.querySelectorAll('.faq-minimal-item')).map((el, i) => ({
              idx: i,
              isOpen: el.classList.contains('is-open')
            }));
          })()`,
          returnByValue: true
        });
        console.log('State after clicking 1st button:', JSON.stringify(r4.result.value, null, 2));

        ws.close();
        process.exit(0);
      }

      run().catch(e => { console.error(e); process.exit(1); });
    });
  });
});

