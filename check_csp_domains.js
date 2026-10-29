const fs = require('fs');
const content = fs.readFileSync('d:/st.ourhtmldemo.com/new/dalalmachine/index.html', 'utf8');

// Find all external URLs in script, link, img, iframe
const urls = [...content.matchAll(/https?:\/\/[^\s"'<>]+/gi)].map(m => m[0]);
const domains = new Set();
urls.forEach(u => {
  try {
    const d = new URL(u).origin;
    domains.add(d);
  } catch (e) {}
});
console.log('Public site external domains:', Array.from(domains));
