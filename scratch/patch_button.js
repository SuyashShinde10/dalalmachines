const fs = require('fs');
let code = fs.readFileSync('admin/inquiries.html', 'utf8');

const targetStr = `<button type="button" class="btn-sm" style="margin-top: 6px; background: rgba(248,157,19,0.12); color: #b45309; border: 1px solid rgba(248,157,19,0.3); border-radius: 4px; font-weight: 700; font-size: 11px; cursor: pointer; padding: 4px 6px; width: 100%; display: flex; align-items: center; justify-content: center; gap: 4px;" class="btn-sm btn-ai-score" data-inquiry-id="\${esc(i.id)}" onclick='openAILeadScore("\${esc(i.id)}")'>`;
const replacementStr = `<button type="button" class="btn-sm btn-ai-score" data-inquiry-id="\${esc(i.id)}" style="margin-top: 6px; background: rgba(248,157,19,0.12); color: #b45309; border: 1px solid rgba(248,157,19,0.3); border-radius: 4px; font-weight: 700; font-size: 11px; cursor: pointer; padding: 4px 6px; width: 100%; display: flex; align-items: center; justify-content: center; gap: 4px;" onclick='openAILeadScore("\${esc(i.id)}")'>`;

code = code.replace(targetStr, replacementStr);
fs.writeFileSync('admin/inquiries.html', code, 'utf8');
console.log('Button cleaned up successfully.');
