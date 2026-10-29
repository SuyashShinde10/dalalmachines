const fs = require('fs');
['admin/dashboard.html', 'superadmin/dashboard.html', 'dev/index.html'].forEach(f => {
  const content = fs.readFileSync('d:/st.ourhtmldemo.com/' + f, 'utf8');
  const urls = [...content.matchAll(/https?:\/\/[^\s"'<>]+/gi)].map(m => m[0]);
  const domains = new Set();
  urls.forEach(u => {
    try { domains.add(new URL(u).origin); } catch (e) {}
  });
  console.log(f, Array.from(domains));
});
