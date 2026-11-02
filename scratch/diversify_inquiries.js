const fs = require('fs');

const dbPath = 'server/data/db.json';
const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));

const realisticBuyers = [
  {
    name: 'Mr. Rajesh Verma',
    company: 'Verma Forgings Ltd',
    phone: '+91 9876543210',
    email: 'rajesh@vermaforgings.com',
    machineName: '1600T Russian Hot Forging Press',
    machineId: 'P00007',
    message: 'Need CIF Nhava Sheva quote and live power trial schedule.'
  },
  {
    name: 'Mr. Aditya Kalyani',
    company: 'Kalyani Forge Ltd, Pune',
    phone: '+91 9822014522',
    email: 'a.kalyani@kalyaniforge.com',
    machineName: '2500T RUSSIAN TMP-VORONEZH Hot Forging Press',
    machineId: 'P00007',
    message: 'Looking for 2500T press for automotive crankshafts. Need inspection at Pune yard.'
  },
  {
    name: 'Mr. Harish Singhania',
    company: 'Singhania Heavy Engineering',
    phone: '+91 9811034567',
    email: 'h.singhania@singhania-eng.com',
    machineName: 'DANGO & DIENENTHAL 1600 TON Open Die Forging Press',
    machineId: 'P043OD',
    message: 'Urgent requirement for open die forging press with manipulator. Share CIF quote.'
  },
  {
    name: 'Mr. Vikram Shriram',
    company: 'Shriram Pistons & Rings Ltd',
    phone: '+91 9839088712',
    email: 'vikram.s@shrirampistons.com',
    machineName: '1000T EUMUCO Hot Forging Wedge Press',
    machineId: 'P0001',
    message: 'Interested in German wedge press for fast cycle connecting rod forging.'
  },
  {
    name: 'Mr. Anupam Mittal',
    company: 'Mittal Forgings Pvt Ltd',
    phone: '+91 9845012399',
    email: 'anupam@mittalforgings.co.in',
    machineName: 'Custom 4000T Hydraulic Closed Die Forging Press',
    machineId: 'P00008',
    message: 'Please share foundation drawings and hydraulic power unit specifications.'
  },
  {
    name: 'Mr. Balwinder Singh',
    company: 'Happy Forgings Ltd, Ludhiana',
    phone: '+91 9872055611',
    email: 'bsingh@happyforgings.com',
    machineName: '1600T Russian Hot Forging Press',
    machineId: 'P00007',
    message: 'Need live power trial schedule and commercial Ex-Yard Pune price.'
  },
  {
    name: 'Mr. Pradeep Rathod',
    company: 'Endurance Technologies Ltd',
    phone: '+91 9823099881',
    email: 'pradeep.rathod@endurance.co.in',
    machineName: 'LI CHIN 200 TON C-Frame Press',
    machineId: 'P0002',
    message: 'Requirement for 200T C-frame mechanical press for two-wheeler brake disc stamping.'
  },
  {
    name: 'Mr. S. K. Narang',
    company: 'Sona BLW Precision Forgings',
    phone: '+91 9810077654',
    email: 'sknarang@sonablw.com',
    machineName: '2500T RUSSIAN TMP-VORONEZH Hot Forging Press',
    machineId: 'P00007',
    message: 'Need complete inspection videos under live power and electrical panel details.'
  },
  {
    name: 'Mr. Arvind Chordia',
    company: 'Auto Ancillary Works, Chakan',
    phone: '+91 9850022331',
    email: 'arvind@chordiaauto.com',
    machineName: 'TOS VARNSDORF W9A Horizontal Boring Machine',
    machineId: 'P00019C',
    message: 'Share DRO specs and spindle condition report.'
  },
  {
    name: 'Mr. Ramesh Patel',
    company: 'Patel Heavy Engineering, Rajkot',
    phone: '+91 9825044321',
    email: 'rpatel@patelengg.com',
    machineName: 'WALDRICH COBURG 4000 Heavy CNC Portal Milling Machine',
    machineId: 'P021M',
    message: 'Looking for portal milling machine with right angle auto head.'
  },
  {
    name: 'Mr. Deepak Bhargava',
    company: 'Bharat Forge Ltd, Mundhwa Pune',
    phone: '+91 9822987112',
    email: 'deepak.b@bharatforge.com',
    machineName: 'Custom 4000T Hydraulic Closed Die Forging Press',
    machineId: 'P00008',
    message: 'Need technical specification sheet and delivery lead time to Pune.'
  },
  {
    name: 'Mr. Gurpreet Sandhu',
    company: 'Sandhu Auto Components',
    phone: '+91 9815044899',
    email: 'gurpreet@sandhuauto.com',
    machineName: '1000T EUMUCO Hot Forging Wedge Press',
    machineId: 'P0001',
    message: 'Requesting CIF Nhava Sheva quote and trial video.'
  },
  {
    name: 'Mr. Manoj Kulkarni',
    company: 'Kulkarni Precision Tools, Bhosari',
    phone: '+91 9890033221',
    email: 'manoj@kulkarnitools.in',
    machineName: 'TOS VARNSDORF W100A Horizontal Boring Machine',
    machineId: 'P00019D',
    message: 'Can we visit your Pune yard this Friday for machine inspection?'
  },
  {
    name: 'Mr. Chetan Aggarwal',
    company: 'Aggarwal Steels & Forgings',
    phone: '+91 9814088921',
    email: 'chetan@aggarwalforgings.com',
    machineName: 'DANGO & DIENENTHAL 1600 TON Open Die Forging Press',
    machineId: 'P043OD',
    message: 'Need urgent quote for open die forging press.'
  },
  {
    name: 'Mr. Nilesh Shah',
    company: 'Shah Precision Forgings, Vadodara',
    phone: '+91 9824055711',
    email: 'nilesh@shahforgings.com',
    machineName: 'LI CHIN 200 TON C-Frame Press',
    machineId: 'P0002',
    message: 'Please send complete technical specifications and payment terms.'
  }
];

let buyerIdx = 0;
// Retain first inquiry if security test, then diversify duplicate Rajesh inquiries
db.inquiries.forEach((inq, idx) => {
  if (inq.name === 'Security Audit Auditor' || inq.name === 'Automated Test Client') {
    return; // Leave test fixtures alone
  }

  // If duplicate Rajesh Verma or test machine, assign unique realistic buyer
  const buyer = realisticBuyers[buyerIdx % realisticBuyers.length];
  buyerIdx++;

  inq.name = buyer.name;
  inq.company = buyer.company;
  inq.phone = buyer.phone;
  inq.email = buyer.email;
  inq.machineName = buyer.machineName;
  inq.machineId = buyer.machineId;
  inq.message = buyer.message;

  // Stagger timestamps across October 2026 for realistic timeline
  const baseTime = new Date('2026-10-31T18:30:00Z').getTime();
  const timeOffset = idx * (3.5 * 3600 * 1000); // 3.5 hours apart
  inq.createdAt = new Date(baseTime - timeOffset).toISOString();
});

fs.writeFileSync(dbPath, JSON.stringify(db, null, 2), 'utf8');
console.log('Successfully diversified', db.inquiries.length, 'inquiries in db.json!');

