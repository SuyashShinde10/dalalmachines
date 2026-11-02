function formatSalutation(rawName, company) {
  const isGenericCompany = !company || /^(private|individual|n\/a|none|test|secops)/i.test(company.trim());
  const companyTitle = !isGenericCompany ? `Dear ${company.trim()} Team` : 'Namaste ji';

  if (!rawName || typeof rawName !== 'string') {
    return companyTitle;
  }
  let clean = rawName.trim();
  if (/^(test|machine|admin|demo|user|inquiry|customer|sample|security|auditor)/i.test(clean)) {
    return companyTitle;
  }
  const prefixMatch = clean.match(/^(?:mr\.|mr|mrs\.|mrs|ms\.|ms|dr\.|dr|shri)\s+(.*)$/i);
  if (prefixMatch && prefixMatch[1]) {
    const mainName = prefixMatch[1].trim();
    const firstName = mainName.split(/\s+/)[0];
    return `Namaste ${firstName} ji`;
  }
  const firstName = clean.split(/\s+/)[0];
  if (firstName && firstName.length >= 2) {
    return `Namaste ${firstName} ji`;
  }
  return 'Namaste ji';
}

console.log('Test 1 (Mr. Rajesh Verma):', formatSalutation('Mr. Rajesh Verma', 'Verma Forgings Ltd'));
console.log('Test 2 (Test Machine):', formatSalutation('Test Machine', 'Private Buyer'));
console.log('Test 3 (Security Audit Auditor):', formatSalutation('Security Audit Auditor', 'SecOps Global'));
console.log('Test 4 (Amit Sharma):', formatSalutation('Amit Sharma', 'Kalyani Forgings'));
console.log('Test 5 (Only Company):', formatSalutation('', 'Tata Motors Ltd'));
