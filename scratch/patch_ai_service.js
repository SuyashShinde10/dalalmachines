const fs = require('fs');

let code = fs.readFileSync('server/services/aiService.js', 'utf8');

const targetStr = `  // Deterministic Rule-Based Lead Scoring
  const msg = (inquiry.message || '').toLowerCase();
  let leadScore = 'WARM';
  let scoreReason = 'Valid contact details and specific machine inquiry submitted.';

  if (
    msg.includes('cif') || 
    msg.includes('urgent') || 
    msg.includes('inspection') || 
    msg.includes('buy') || 
    msg.includes('quote') || 
    msg.includes('immediate') || 
    (inquiry.company && inquiry.company.length > 5)
  ) {
    leadScore = 'HOT';
    scoreReason = 'High purchase intent: Buyer requested CIF price / live inspection trial with company credentials.';
  } else if (!inquiry.phone && !inquiry.company) {
    leadScore = 'GENERAL';
    scoreReason = 'Preliminary inquiry with limited technical requirements.';
  }

  const machineTitle = inquiry.machineName || 'requested machinery';
  const whatsappDraft = 
    \`Namaste \${inquiry.name} ji,\\n\\n\` +
    \`Thank you for contacting Dalal Machine Tools Agency Pvt. Ltd. regarding *\${machineTitle}*.\\n\\n\` +
    \`We have reviewed your inquiry and have ready options with complete inspection videos under live power.\\n\\n\` +
    \`Would you like us to share the detailed technical specification sheet and CIF Nhava Sheva / Ex-Pune Yard commercial proposal?\\n\\n\` +
    \`Warm regards,\\n\` +
    \`Sales Team | Dalal Machine Tools Agency Pvt. Ltd.\\n\` +
    \`Phone: +91 9821232131 / +91 9820088888\\n\` +
    \`Website: dalalmachines.com\`;

  return {
    leadScore,
    scoreReason,
    intentSummary: \`Quotation requested for \${machineTitle}\${inquiry.company ? ' by ' + inquiry.company : ''}.\`,
    suggestedWhatsAppReply: whatsappDraft,
    matchedMachines: matchedMachines.slice(0, 3)
  };
}`;

const replacementStr = `  // Helper for human-grade professional salutation
  function formatSalutation(rawName, company) {
    const isGenericCompany = !company || /^(private|individual|n\\/a|none|test|secops)/i.test(company.trim());
    const companyTitle = !isGenericCompany ? \`Dear \${company.trim()} Team\` : 'Namaste ji';

    if (!rawName || typeof rawName !== 'string') return companyTitle;
    let clean = rawName.trim();
    if (/^(test|machine|admin|demo|user|inquiry|customer|sample|security|auditor)/i.test(clean)) {
      return companyTitle;
    }
    const prefixMatch = clean.match(/^(?:mr\\.|mr|mrs\\.|mrs|ms\\.|ms|dr\\.|dr|shri)\\s+(.*)$/i);
    if (prefixMatch && prefixMatch[1]) {
      const mainName = prefixMatch[1].trim();
      const firstName = mainName.split(/\\s+/)[0];
      return \`Namaste \${firstName} ji\`;
    }
    const firstName = clean.split(/\\s+/)[0];
    if (firstName && firstName.length >= 2) {
      return \`Namaste \${firstName} ji\`;
    }
    return 'Namaste ji';
  }

  // Multi-Factor Quantitative Lead Scoring Engine (0 - 100 points)
  let scorePoints = 0;
  const factors = [];

  const msg = (inquiry.message || '').toLowerCase();
  const machineName = (inquiry.machineName || '').trim();
  const company = (inquiry.company || '').trim();
  const phone = (inquiry.phone || '').trim();

  // 1. Technical Precision: Specific Machine / Model / Tonnage (+35 pts)
  if (machineName && !/general/i.test(machineName)) {
    scorePoints += 35;
    factors.push('Specific machine model specified (' + machineName + ')');
  } else if (/\\b(\\d{3,4}\\s*t|\\d{3,4}\\s*ton|press|forging|milling|lathe|boring)\\b/i.test(msg)) {
    scorePoints += 25;
    factors.push('Technical tonnage/process keywords identified');
  }

  // 2. Commercial Procurement Cues (+30 pts)
  const commercialKeywords = ['cif', 'quote', 'quotation', 'price', 'pricing', 'cost', 'urgent', 'immediate', 'inspection', 'trial', 'budget', 'nhava sheva', 'ready stock', 'buy', 'purchase'];
  const matchedKeywords = commercialKeywords.filter(k => msg.includes(k));
  if (matchedKeywords.length >= 2) {
    scorePoints += 30;
    factors.push('Commercial purchase cues: ' + matchedKeywords.slice(0, 3).join(', '));
  } else if (matchedKeywords.length === 1) {
    scorePoints += 20;
    factors.push('Commercial cue: ' + matchedKeywords[0]);
  }

  // 3. Corporate Credibility (+20 pts)
  if (company && company.length > 3 && !/individual|private/i.test(company)) {
    scorePoints += 20;
    factors.push('Enterprise buyer (' + company + ')');
  }

  // 4. Direct Communication Channel (+15 pts)
  if (phone && phone.replace(/[^0-9]/g, '').length >= 10) {
    scorePoints += 15;
    factors.push('Verified phone/WhatsApp contact');
  }

  let leadScore = 'WARM';
  let scoreReason = '';

  if (scorePoints >= 65) {
    leadScore = 'HOT';
    scoreReason = \`High Procurement Intent (\${scorePoints}/100): \${factors.join(' • ')}. Buyer is actively sourcing with immediate purchase/inspection readiness.\`;
  } else if (scorePoints >= 35) {
    leadScore = 'WARM';
    scoreReason = \`Active Evaluation (\${scorePoints}/100): \${factors.join(' • ')}. Buyer evaluating technical specifications and stock availability.\`;
  } else {
    leadScore = 'GENERAL';
    scoreReason = \`General Inquiry (\${scorePoints}/100): Preliminary request requiring technical requirement gathering and contact qualification.\`;
  }

  const salutation = formatSalutation(inquiry.name, inquiry.company);
  const machineTitle = machineName ? \`*\${machineName}*\` : 'heavy industrial machinery';
  const companyMention = company && !/individual|private/i.test(company) ? \` for \${company}\` : '';

  let whatsappDraft = '';
  if (leadScore === 'HOT') {
    whatsappDraft = 
      \`\${salutation},\\n\\n\` +
      \`Thank you for reaching out to Dalal Machine Tools Agency regarding \${machineTitle}\${companyMention}.\\n\\n\` +
      \`We have verified options available with complete operational inspection videos under live power, inspected abroad by our engineering team.\\n\\n\` +
      \`Shall I share the full technical specification sheet along with our commercial CIF Nhava Sheva / Ex-Pune Yard quotation?\\n\\n\` +
      \`We can also coordinate a live video demonstration or an on-site yard trial at your convenience.\\n\\n\` +
      \`Warm regards,\\n\` +
      \`Sales & Procurement Desk | Dalal Machine Tools Agency Pvt. Ltd.\\n\` +
      \`📍 Commerce Centre, Tardeo, Mumbai\\n\` +
      \`📞 +91 9821232131 / +91 9820088888\\n\` +
      \`🌐 dalalmachines.com\`;
  } else if (leadScore === 'WARM') {
    whatsappDraft = 
      \`\${salutation},\\n\\n\` +
      \`Thank you for your interest in Dalal Machine Tools Agency regarding \${machineTitle}\${companyMention}.\\n\\n\` +
      \`We have multiple options available in this category ready for immediate delivery from our Pune Yard as well as European partner stock.\\n\\n\` +
      \`Would you like me to share our latest catalog and technical specifications over WhatsApp for your engineering team to review?\\n\\n\` +
      \`Best regards,\\n\` +
      \`Sales Team | Dalal Machine Tools Agency Pvt. Ltd.\\n\` +
      \`📍 Commerce Centre, Tardeo, Mumbai\\n\` +
      \`📞 +91 9821232131 / +91 9820088888\\n\` +
      \`🌐 dalalmachines.com\`;
  } else {
    whatsappDraft = 
      \`\${salutation},\\n\\n\` +
      \`Thank you for connecting with Dalal Machine Tools Agency Pvt. Ltd.\\n\\n\` +
      \`We received your inquiry regarding industrial machinery. Please let us know your required tonnage, bed size, or application so we can suggest the best matching machines currently in stock.\\n\\n\` +
      \`You can also browse our live inventory anytime at dalalmachines.com.\\n\\n\` +
      \`Best regards,\\n\` +
      \`Dalal Machine Tools Agency Pvt. Ltd.\\n\` +
      \`📍 Commerce Centre, Tardeo, Mumbai\\n\` +
      \`📞 +91 9821232131\`;
  }

  return {
    leadScore,
    scoreReason,
    intentSummary: \`Quotation requested for \${machineName || 'machinery'}\${company ? ' by ' + company : ''}.\`,
    suggestedWhatsAppReply: whatsappDraft,
    matchedMachines: matchedMachines.slice(0, 3)
  };
}`;

if (!code.includes(targetStr)) {
  console.error('Target string not found in aiService.js! Check line endings.');
  // normalize CRLF
  const normCode = code.replace(/\r\n/g, '\n');
  const normTarget = targetStr.replace(/\r\n/g, '\n');
  if (normCode.includes(normTarget)) {
    const updated = normCode.replace(normTarget, replacementStr);
    fs.writeFileSync('server/services/aiService.js', updated, 'utf8');
    console.log('Successfully updated aiService.js with normalized newlines!');
  } else {
    console.error('Still not found even after newline normalization.');
  }
} else {
  code = code.replace(targetStr, replacementStr);
  fs.writeFileSync('server/services/aiService.js', code, 'utf8');
  console.log('Successfully updated aiService.js!');
}

