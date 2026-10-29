const fs = require('fs');
const path = require('path');

// 1. Clean index.html
const indexPath = path.join(__dirname, '..', 'new', 'dalalmachine', 'index.html');
let index = fs.readFileSync(indexPath, 'utf8');
index = index.replace(/\r?\n\s*<link href="css\/dalal-ai\.css\?v=3\.0" rel="stylesheet">/g, '');
index = index.replace(/\r?\n\s*<script src="js\/dalal-ai\.js\?v=4\.0"><\/script>/g, '');
fs.writeFileSync(indexPath, index, 'utf8');
console.log('Cleaned index.html');

// 2. Clean category.html
const catPath = path.join(__dirname, '..', 'new', 'dalalmachine', 'category.html');
let cat = fs.readFileSync(catPath, 'utf8');
cat = cat.replace(/\r?\n\s*<link href="css\/dalal-ai\.css\?v=3\.0" rel="stylesheet">/g, '');
cat = cat.replace(/\r?\n\s*<script src="js\/dalal-ai\.js\?v=4\.0"><\/script>/g, '');
// Remove ai-matchmaker-btn
cat = cat.replace(/\s*<button type="button" id="ai-matchmaker-btn"[\s\S]*?<\/button>/g, '');
fs.writeFileSync(catPath, cat, 'utf8');
console.log('Cleaned category.html');

// 3. Clean product.html
const prodPath = path.join(__dirname, '..', 'new', 'dalalmachine', 'product.html');
let prod = fs.readFileSync(prodPath, 'utf8');
prod = prod.replace(/\r?\n\s*<link href="css\/dalal-ai\.css\?v=3\.0" rel="stylesheet">/g, '');
prod = prod.replace(/\r?\n\s*<script src="js\/dalal-ai\.js\?v=4\.0"><\/script>/g, '');
fs.writeFileSync(prodPath, prod, 'utf8');
console.log('Cleaned product.html');

// 4. Neutralize dalal-ai.js completely with auto-destroy
const aiJsPath = path.join(__dirname, '..', 'new', 'dalalmachine', 'js', 'dalal-ai.js');
let aiJs = fs.readFileSync(aiJsPath, 'utf8');
if (!aiJs.includes('if (el) el.remove();\n    return;')) {
  aiJs = aiJs.replace(
    'function initDalalAI() {\n    const el = document.getElementById(\'dai-widget-container\');\n    if (el) el.remove();',
    'function initDalalAI() {\n    const el = document.getElementById(\'dai-widget-container\');\n    if (el) el.remove();\n    return;'
  );
  aiJs = aiJs.replace(
    'function initDalalAI() {\r\n    const el = document.getElementById(\'dai-widget-container\');\r\n    if (el) el.remove();',
    'function initDalalAI() {\r\n    const el = document.getElementById(\'dai-widget-container\');\r\n    if (el) el.remove();\r\n    return;'
  );
  fs.writeFileSync(aiJsPath, aiJs, 'utf8');
}
console.log('Neutralized dalal-ai.js');
