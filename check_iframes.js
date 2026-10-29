const fs = require('fs');
GetHtmlFiles = (dir) => {
  let res = [];
  fs.readdirSync(dir).forEach(f => {
    const full = dir + '/' + f;
    if (fs.statSync(full).isDirectory()) res = res.concat(GetHtmlFiles(full));
    else if (f.endsWith('.html')) res.push(full);
  });
  return res;
};

const allFiles = GetHtmlFiles('d:/st.ourhtmldemo.com');
allFiles.forEach(f => {
  const c = fs.readFileSync(f, 'utf8');
  const m = c.match(/<iframe[^>]*src=["']([^"']+)["']/i);
  if (m) console.log(f.replace('d:/st.ourhtmldemo.com/', ''), 'iframe src:', m[1]);
});
