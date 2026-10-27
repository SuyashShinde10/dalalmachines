const db = require('../db');

/**
 * Dalal Machine Tools - Enterprise AI Intelligence Engine
 * Handles customer machinery recommendations, WhatsApp RFQ generation,
 * High Seas advice, OMPI technical support, and Admin copilot operations.
 */

// Central Company Knowledge Base for AI System Instruction
const DALAL_KNOWLEDGE_BASE = `
You are the Official AI Machinery Sales & Technical Advisor for "Dalal Machine Tools Agency Pvt. Ltd." (founded by Mr. Dalal, technical partner OMPI India LLP).
Company Profile:
- Business: Leading Indian importer, stockist, and distributor of heavy industrial metal forming and metal cutting machinery.
- Major specializations: Hot Forging Presses (500T to 4000T, Russian Voronezh TMP, National, Eumuco, Hasenclever), Knuckle Joint Coining Presses, C-Frame Mechanical Presses, Hydraulic Deep Draw Presses, Horizontal Boring Machines (Skoda, TOS, Union), Heavy Duty Lathes, Gear Hobbing & Shaping Machines.
- Technical Partner: OMPI India LLP - world-class pneumatic and hydraulic clutch-brake units, retrofits for forging presses and stamping machines.
- Key USP: "High Seas Sales" - Direct import under customer's IEC code saving substantial customs duty, local cascading taxes, and port demurrage.
- Warehouses / Yards: Primary Indian yard in Pune (Maharashtra). Overseas inspection networks in Europe (Germany, Italy, Russia, Czech Republic), Thailand, and Vietnam.
- Contact info: Phone/WhatsApp: +91 9821232131 / +91 9820088888, Email: dalalmachine@gmail.com / info@dalalmachines.com.
- Communication Style: Professional, polite, technically sharp, industrial-savvy. Respond naturally in the language the user asks (Hinglish, Hindi, English, Gujarati).
`;

// Helper: Call Google Gemini REST API
async function callGemini(apiKey, systemInstruction, prompt) {
  if (!apiKey || apiKey.trim() === '') return null;

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey.trim()}`;
  const payload = {
    contents: [
      {
        role: 'user',
        parts: [{ text: `${systemInstruction}\n\nUser Request: ${prompt}` }]
      }
    ],
    generationConfig: {
      temperature: 0.4,
      maxOutputTokens: 1024
    }
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const errText = await response.text();
    console.warn(`[AI Engine] Gemini API error (${response.status}):`, errText);
    throw new Error(`Gemini API returned status ${response.status}`);
  }

  const data = await response.json();
  const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
  return text || null;
}

// Built-in Deterministic Search & Match Engine across db.products
function searchCatalog(query) {
  const products = db.getProducts({ all: 'true' }) || [];
  const q = (query || '').toLowerCase().trim();
  if (!q) return products.slice(0, 3);

  // Extract potential tonnage / numbers (e.g., 2500, 1000, 1600, 4000)
  const tonMatch = q.match(/(\d{3,4})\s*(?:t|ton|tons|tonne)?/i);
  const targetTonnage = tonMatch ? parseInt(tonMatch[1], 10) : null;

  const scored = products.map(p => {
    let score = 0;
    const name = (p.name || '').toLowerCase();
    const make = (p.make || '').toLowerCase();
    const model = (p.model || '').toLowerCase();
    const cat = (p.category || '').toLowerCase();
    const catName = (p.categoryName || '').toLowerCase();
    const loc = (p.location || '').toLowerCase();
    const condition = (p.condition || '').toLowerCase();

    // Check query tokens
    const tokens = q.split(/\s+/).filter(t => t.length > 2);
    tokens.forEach(tok => {
      if (name.includes(tok)) score += 5;
      if (cat.includes(tok) || catName.includes(tok)) score += 4;
      if (make.includes(tok)) score += 4;
      if (model.includes(tok)) score += 3;
      if (loc.includes(tok)) score += 2;
      if (condition.includes(tok)) score += 2;
    });

    // Tonnage exact/proximity matching
    if (targetTonnage && p.tonnage) {
      if (p.tonnage === targetTonnage) score += 10;
      else if (Math.abs(p.tonnage - targetTonnage) <= 500) score += 6;
      else if (Math.abs(p.tonnage - targetTonnage) <= 1000) score += 3;
    }

    // Specific keywords
    if ((q.includes('forging') || q.includes('press')) && (cat.includes('press') || name.includes('press'))) score += 3;
    if ((q.includes('boring') || q.includes('lathe') || q.includes('cutting')) && p.section === 'cutting') score += 3;
    if (q.includes('pune') && loc.includes('pune')) score += 4;
    if (q.includes('europe') && loc.includes('europe')) score += 4;
    if (q.includes('ompi') && (name.includes('ompi') || (p.specs && JSON.stringify(p.specs).toLowerCase().includes('ompi')))) score += 8;

    return { product: p, score };
  });

  scored.sort((a, b) => b.score - a.score);
  return scored.filter(s => s.score > 0).slice(0, 4).map(s => s.product);
}

/**
 * 1. Customer-Facing Chat (Multilingual: English default, Hinglish, Hindi, Gujarati, Marathi)
 */
async function chatWithCustomer({ message, history = [], language = 'en' }) {
  const settings = db.getSettings() || {};
  const apiKey = settings.geminiApiKey || process.env.GEMINI_API_KEY || '';
  const cleanMsg = (message || '').trim();
  const lowerMsg = cleanMsg.toLowerCase();
  const lang = (language || 'en').toLowerCase();

  const langMap = {
    en: 'English (Clear, professional industrial tone)',
    hinglish: 'Hinglish (Hindi written in English alphabet)',
    hi: 'Hindi (हिन्दी - Devanagari script)',
    gu: 'Gujarati (ગુજરાતી script)',
    mr: 'Marathi (मराठी script)'
  };
  const targetLanguageName = langMap[lang] || 'English';

  // Search catalog for relevant machines
  const matchedMachines = searchCatalog(cleanMsg);
  const matchedSummary = matchedMachines.map(m => 
    `ID: ${m.id} | Name: ${m.name} | Tonnage: ${m.tonnage || 'N/A'}T | Location: ${m.location} | Make: ${m.make}`
  ).join('\n');

  // Try calling Gemini if API key is provided
  if (apiKey) {
    try {
      const prompt = `
Context Catalog Products Available in Stock/Import:
${matchedSummary || 'Full catalog available online across 26 categories.'}

User Inquiry: "${cleanMsg}"

Language Requirement:
IMPORTANT: You MUST respond strictly in ${targetLanguageName}. If the requested language is English, answer entirely in polished, helpful English.

Instructions:
1. Provide a direct, helpful, and courteous answer in the requested language.
2. If relevant machines are matched, mention 1-2 top machines by name and invite them for a live power trial or video demonstration.
3. If they inquire about customs duty or High Seas Sales, explain that Dalal Machines facilitates direct B/L transfer under their IEC code to save cascading taxes.
4. Keep the response crisp (2 to 4 short paragraphs) and encourage an instant WhatsApp quote.
`;
      const aiReply = await callGemini(apiKey, DALAL_KNOWLEDGE_BASE, prompt);
      if (aiReply) {
        return {
          reply: aiReply,
          matchedMachines: matchedMachines.slice(0, 3),
          chips: generateChips(cleanMsg, lang)
        };
      }
    } catch (err) {
      console.warn('[AI Service] Gemini call failed, falling back to built-in rules:', err.message);
    }
  }

  // Built-in Intelligent Fallback Engine (No API key needed)
  let reply = '';
  const chips = generateChips(cleanMsg, lang);

  const isHighSeas = lowerMsg.includes('high sea') || lowerMsg.includes('custom') || lowerMsg.includes('tax') || lowerMsg.includes('duty') || lowerMsg.includes('iec');
  const isOMPI = lowerMsg.includes('ompi') || lowerMsg.includes('clutch') || lowerMsg.includes('brake');
  const isYard = lowerMsg.includes('pune') || lowerMsg.includes('yard') || lowerMsg.includes('visit') || lowerMsg.includes('trial') || lowerMsg.includes('inspection');
  const isQuote = lowerMsg.includes('quote') || lowerMsg.includes('price') || lowerMsg.includes('cost') || lowerMsg.includes('rfq');

  if (lang === 'hi') {
    // Hindi (Devanagari)
    if (isHighSeas) {
      reply = `**दलाल मशीन टूल्स हाई सीज सेल्स लाभ:**\n\n` +
        `जब आप हाई सीज सेल आधार पर आयातित मशीन खरीदते हैं, तो माल भारतीय बंदरगाह (न्हावा शेवा) पहुँचने से पहले बिल ऑफ लैडिंग (B/L) सीधे आपकी कंपनी के नाम एंडोर्स कर दिया जाता है।\n\n` +
        `**प्रमुख लाभ:**\n` +
        `• **कस्टम्स ड्यूटी और जीएसटी इनपुट क्रेडिट:** आपकी कंपनी के IEC कोड पर क्लीयरेंस होता है, जिससे आप शत-प्रतिशत इनपुट टैक्स क्रेडिट (ITC) ले सकते हैं।\n` +
        `• **अतिरिक्त मार्जिन की बचत:** बिचौलियों का स्थानीय मार्जिन बचता है।\n` +
        `• **शून्य पोर्ट डेमरेज:** हमारी लॉजिस्टिक्स टीम समय पूर्व एडवांस क्लीयरेंस कराती है।\n\n` +
        `क्या आप किसी विशेष मशीन का CIF कोटेशन चाहते हैं?`;
    } else if (isOMPI) {
      reply = `**OMPI India LLP - आधिकारिक तकनीकी पार्टनर:**\n\n` +
        `दलाल मशीन टूल्स OMPI India LLP के साथ जुड़ी है। हम न्यूमैटिक कंबाइंड क्लच-ब्रेक यूनिट्स और रेट्रोफिटिंग सॉल्यूशन प्रदान करते हैं।\n\n` +
        `• टॉर्क क्षमता: 500 Nm से 1,00,000+ Nm तक\n` +
        `• डुअल सेफ्टी वाल्व और सीई कंप्लायंस।`;
    } else if (isYard) {
      reply = `**पुणे मशीनरी यार्ड एवं ट्रायल सुविधा:**\n\n` +
        `हमारा मुख्य स्टॉकयार्ड **पुणे इंडस्ट्रियल जोन, महाराष्ट्र** में स्थित है।\n\n` +
        `• **लाइव पावर ट्रायल:** खरीदार मशीन को पावर कनेक्शन पर चलाकर लाइव टेस्ट कर सकते हैं।\n` +
        `• यूरोपियन स्टॉक के लिए लाइव वीडियो इंस्पेक्शन की सुविधा उपलब्ध है।`;
    } else if (matchedMachines.length > 0) {
      const top = matchedMachines[0];
      reply = `आपकी आवश्यकता के लिए हमारे पास सत्यापित मशीन उपलब्ध है: **${top.name}** (${top.location}).\n\n` +
        `• **मेक:** ${top.make || 'European / Asian Verified'}\n` +
        `• **क्षमता:** ${top.tonnage ? top.tonnage + ' टन' : 'हेवी ड्यूटी'}\n` +
        `• **कंडीशन:** ${top.condition || 'पावर पर जाँची गई'}\n\n` +
        `नीचे दिए गए कार्ड से आप टेक्निकल स्पेसिफिकेशन देख सकते हैं या व्हाट्सएप पर तत्काल कोटेशन मांग सकते हैं।`;
    } else {
      reply = `नमस्ते! मैं **दलाल मशीन टूल्स** का AI मशीनरी एडवाइजर हूँ।\n\n` +
        `मैं आपकी औद्योगिक आवश्यकता के अनुसार मेटल फॉर्मिंग (हॉट फोर्जिंग प्रेस, सी-फ्रेम, कॉइनिंग, हाइड्रोलिक) और मेटल कटिंग मशीनरी (लेथ, बोरिंग, गियर हॉबिंग) खोजने में मदद कर सकता हूँ।\n\n` +
        `आपको किस प्रकार की मशीन या क्षमता की आवश्यकता है?`;
    }
  } else if (lang === 'gu') {
    // Gujarati
    if (isHighSeas) {
      reply = `**દલાલ મશીન ટુલ્સ હાઇ સીઝ સેલ્સ લાભ:**\n\n` +
        `જ્યારે આપ હાઇ સીઝ સેલ દ્વારા આયાતી મશીન ખરીદો છો, ત્યારે શિપમેન્ટ બંદરે (ન્હાવા શેવા) પહોંચતા પહેલાં બિલ ઓફ લેડિંગ (B/L) સીધું તમારી કંપનીના નામે એન્ડોર્સ થાય છે.\n\n` +
        `• **સંપૂર્ણ GST ITC ક્રેડિટ:** આપના પોતાના IEC કોડ પર ક્લિયરન્સ.\n` +
        `• **વધારાના ટ્રેડિંગ માર્જિનની બચત.**\n\n` +
        `શું આપને કોઈ ચોક્કસ મશીનનું કોટેશન જોઈએ છે?`;
    } else if (matchedMachines.length > 0) {
      const top = matchedMachines[0];
      reply = `આપની જરૂરિયાત મુજબ ઉપલબ્ધ મશીન: **${top.name}** (${top.location}).\n\n` +
        `• **મેક:** ${top.make || 'European Verified'}\n` +
        `• **ક્ષમતા:** ${top.tonnage ? top.tonnage + ' ટન' : 'હેવી ડ્યુટી'}\n\n` +
        `નીચે આપેલા કાર્ડ પરથી ટેકનિકલ સ્પેક્સ ચકાસી શકો છો અથવા વોટ્સએપ પર ડાયરેક્ટ કોટેશન મેળવી શકો છો.`;
    } else {
      reply = `નમસ્તે! હું **દલાલ મશીન ટુલ્સ**નો AI મશીનરી એડવાઇઝર છું.\n\n` +
        `હું આપની ફેક્ટરી જરૂરિયાત મુજબ યોગ્ય ફોર્જિંગ પ્રેસ, સી-ફ્રેમ, લેથ અને બોરિંગ મશીનો શોધવામાં મદદ કરી શકું છું.\n\n` +
        `આપને કઈ મશીન અથવા ટનેજની જરૂર છે?`;
    }
  } else if (lang === 'mr') {
    // Marathi
    if (isHighSeas) {
      reply = `**दलाल मशीन टूल्स हाय सीज सेल्स फायदे:**\n\n` +
        `हाय सीज सेल अंतर्गत आयात केलेली मशीन खरेदी करताना बिल ऑफ लॅडिंग (B/L) थेट आपल्या कंपनीच्या नावावर केले जाते.\n\n` +
        `• **कस्टम ड्युटी आणि GST इनपुट क्रेडिट:** थेट आपल्या IEC कोडवर क्लिअरन्स.\n` +
        `• स्थानिक अतिरिक्त मार्जिन आणि पोर्ट डेमरेजची बचत.`;
    } else if (matchedMachines.length > 0) {
      const top = matchedMachines[0];
      reply = `आपल्या गरजेनुसार उपलब्ध मशीन: **${top.name}** (${top.location}).\n\n` +
        `• **मेक:** ${top.make || 'European Verified'}\n` +
        `• **क्षमता:** ${top.tonnage ? top.tonnage + ' टन' : 'हेवी ड्युटी'}\n\n` +
        `खालील कार्डवरून आपण सविस्तर माहिती पाहू शकता किंवा थेट व्हॉट्सॲपवर कोटेशन मागवू शकता.`;
    } else {
      reply = `नमस्कार! मी **दलाल मशीन टूल्स** चा AI मशीनरी सल्लागार आहे.\n\n` +
        `मी आपल्या कारखान्याच्या गरजेनुसार मेटल फॉर्मिंग आणि मेटल कटिंग मशीन्स शोधण्यात मदत करू शकतो.\n\n` +
        `आपल्याला कोणत्या प्रकारच्या मशीनची आवश्यकता आहे?`;
    }
  } else if (lang === 'hinglish') {
    // Hinglish
    if (isHighSeas) {
      reply = `**Dalal Machines High Seas Sales Advantage:**\n\n` +
        `Jab aap hamare through High Seas Sale basis par imported machine khareedte hain, to shipment Indian port (Nhava Sheva) pe pahunchne se pehle Bill of Lading (B/L) aapki company ke naam endorse ho jata hai.\n\n` +
        `**Key Benefits:**\n` +
        `• **Custom Duty & GST Benefit:** Custom duty clearance aapke IEC code par direct hoti hai jisse aap easily ITC (Input Tax Credit) claim kar sakte hain.\n` +
        `• **No Double Margins:** Intermediary holding cost aur local cascading margins bachte hain.\n` +
        `• **Zero Port Demurrage:** Hamari logistics team advance clearance file karti hai.\n\n` +
        `Aapko kisi specific machine ka CIF quote chahiye to batayein, hum turant quotation bana denge!`;
    } else if (isOMPI) {
      reply = `**OMPI India LLP - Official Technical Partner:**\n\n` +
        `Dalal Machine Tools OMPI India LLP ke sath closely associated hai. Hum standard mechanical presses aur heavy forging presses me modern **Pneumatic Combined Clutch-Brake Units** retrofit aur supply karte hain.\n\n` +
        `• **Dual Safety Valves & CE Compliance**\n` +
        `• **Torque Capacity:** 500 Nm se 1,00,000+ Nm tak\n` +
        `• **Retrofitting Service:** Pune yard aur on-site client facility par installation.\n\n` +
        `Kya aapko kisi purani press ke liye clutch replacement ya nayi machine me OMPI unit chahiye?`;
    } else if (isYard) {
      reply = `**Pune Machinery Yard & Inspection Facility:**\n\n` +
        `Hamara main machinery stockyard **Pune Industrial Machinery Zone, Maharashtra** me sthit hai.\n\n` +
        `• **Live Power Trial:** Hum buyers ko power connection ke sath live machine chala kar test karne ki suvidha dete hain.\n` +
        `• **Europe Stock Inspection:** Jo machines hamare Europe yards me hain, unke live inspection video calls provide kiye jaate hain.`;
    } else if (matchedMachines.length > 0) {
      const top = matchedMachines[0];
      reply = `Aapki requirement ke liye hamare paas verified inventory available hai! Jaise ki **${top.name}** (${top.location}).\n\n` +
        `• **Make:** ${top.make || 'European / Asian Verified'}\n` +
        `• **Capacity:** ${top.tonnage ? top.tonnage + ' Tons' : 'Standard Heavy Duty'}\n` +
        `• **Condition:** ${top.condition || 'Inspected under power'}\n\n` +
        `Niche diye gaye cards me aap iske technical specifications dekh sakte hain ya direct WhatsApp par instant RFQ bhej sakte hain.`;
    } else {
      reply = `Namaste! Main **Dalal Machine Tools** ka AI Machinery Advisor hoon.\n\n` +
        `Main aapki factory requirement ke mutabiq best metal forming (Forging Presses, C-Frame, Coining, Hydraulic) aur metal cutting machines (Lathes, Horizontal Boring, Gear Hobbing) recommend kar sakta hoon.\n\n` +
        `Aapko kis tonnage, make ya machine type ki talash hai?`;
    }
  } else {
    // English (DEFAULT)
    if (isHighSeas) {
      reply = `**Dalal Machine Tools - High Seas Sales Advantage:**\n\n` +
        `When procuring imported machinery on a High Seas Sale basis through Dalal Machine Tools, the original Bill of Lading (B/L) is legally endorsed to your company before the container vessel berths at Nhava Sheva Port.\n\n` +
        `**Key Commercial Benefits:**\n` +
        `• **100% Eligible GST & Duty Input Credit:** Customs clearance is filed directly under your company's Import Export Code (IEC), enabling full Input Tax Credit (ITC) utilization.\n` +
        `• **Zero Domestic Intermediary Margin:** Direct import pricing without domestic distributor markups.\n` +
        `• **Demurrage-Free Customs Clearance:** Advance filing executed by our in-house port logistics team.\n\n` +
        `Would you like a CIF Nhava Sheva proposal for any specific machinery in our catalog?`;
    } else if (isOMPI) {
      reply = `**OMPI India LLP - Official Technical Partner:**\n\n` +
        `Dalal Machine Tools works in close partnership with **OMPI India LLP** (world leader in pneumatic & hydraulic clutch-brake units).\n\n` +
        `• **Safety Standards:** Dual cross-flow safety solenoid valves, CE and OSHA compliant.\n` +
        `• **Torque Range:** 500 Nm to 100,000+ Nm for heavy stamping and forging presses.\n` +
        `• **Turnkey Retrofit:** Installation and commissioning at our Pune facility or on-site at your factory.\n\n` +
        `Are you seeking an OMPI retrofit for an existing press or a new machine installation?`;
    } else if (isYard) {
      reply = `**Pune Machinery Yard & Inspection Facilities:**\n\n` +
        `Our central heavy machinery stockyard is located in the **Pune Industrial Machinery Zone, Maharashtra**.\n\n` +
        `• **Live Power Demonstration:** Buyers can witness machines connected to live electric power and trial cycle tests.\n` +
        `• **Overseas Inspection:** For inventory located across our European or Asian network, high-definition live video inspections and technical audit ledgers are provided.\n\n` +
        `We welcome you to schedule a physical yard visit. Click the WhatsApp button below to coordinate timing.`;
    } else if (matchedMachines.length > 0) {
      const top = matchedMachines[0];
      reply = `We have verified machinery matching your specification available in our inventory: **${top.name}** (${top.location}).\n\n` +
        `• **Manufacturer:** ${top.make || 'European / Asian Verified'}\n` +
        `• **Nominal Capacity:** ${top.tonnage ? top.tonnage + ' Metric Tons' : 'Standard Heavy Duty'}\n` +
        `• **Condition:** ${top.condition || 'Inspected under live power'}\n\n` +
        `Please review the specification card below or tap **Get Quote** for an immediate formal WhatsApp RFQ.`;
    } else if (isQuote) {
      reply = `**Instant Machinery Quotation Service:**\n\n` +
        `We provide both CIF Nhava Sheva (Turnkey Port Delivery) and Ex-Pune Yard commercial proposals.\n\n` +
        `To receive a customized quote, please share your **Required Tonnage, Make Preference, and Delivery Location** in chat, or connect directly on WhatsApp (+91 9821232131).`;
    } else {
      reply = `Welcome to **Dalal Machine Tools Agency Pvt. Ltd.**! I am your AI Machinery Sales & Technical Advisor.\n\n` +
        `I can assist you in finding heavy metal forming machinery (Hot Forging Presses, Knuckle Joint Coining, C-Frame, Hydraulic Deep Draw) and heavy metal cutting machine tools (Heavy Duty Lathes, Horizontal Boring, Gear Hobbing).\n\n` +
        `What machinery specifications, capacity, or component application are you looking for?`;
    }
  }

  return {
    reply,
    matchedMachines: matchedMachines.slice(0, 3),
    chips
  };
}

// Generate context-aware quick suggestion chips
function generateChips(query = '', language = 'en') {
  const q = (query || '').toLowerCase();
  const lang = (language || 'en').toLowerCase();

  if (lang === 'hi') {
    return [
      '1000T - 2500T फोर्जिंग प्रेस',
      'हाई सीज कस्टम ड्यूटी बचत',
      'पुणे यार्ड उपलब्ध स्टॉक',
      'व्हाट्सएप कोटेशन'
    ];
  }
  if (lang === 'gu') {
    return [
      '1000T - 2500T ફોર્જિંગ પ્રેસ',
      'હાઇ સીઝ કસ્ટમ ડ્યુટી બચત',
      'પુણે યાર્ડ લાઇવ સ્ટોક',
      'વોટ્સએપ કોટેશન'
    ];
  }
  if (lang === 'mr') {
    return [
      '1000T - 2500T फोर्जिंग प्रेस',
      'हाय सीज कस्टम्स बचत',
      'पुणे यार्ड उपलब्ध स्टॉक',
      'व्हॉट्सॲप कोटेशन'
    ];
  }
  if (lang === 'hinglish') {
    return [
      'Find 1000T - 2500T Forging Press',
      'High Seas Customs Savings',
      'Pune Stock Live Trials',
      'OMPI Clutch & Brake Retrofit'
    ];
  }

  // Default: English
  if (q.includes('press') || q.includes('forg')) {
    return [
      '1000T - 2500T Hot Forging Press',
      'Knuckle Joint Coining Press',
      'Pune Yard In-Stock Units',
      'High Seas Duty Savings'
    ];
  }
  if (q.includes('boring') || q.includes('lathe') || q.includes('cutting')) {
    return [
      'Horizontal Boring Machines',
      'Heavy Duty CNC Lathes',
      'Gear Hobbing & Shaping',
      'Instant WhatsApp RFQ'
    ];
  }
  return [
    'Search 1000T - 2500T Forging Press',
    'High Seas Duty & Tax Savings',
    'Live Stock at Pune Yard',
    'OMPI Clutch & Brake Retrofit'
  ];
}

/**
 * 2. Admin AI Copilot (Natural Language Operations Assistant)
 */
async function chatWithAdminCopilot({ message, user }) {
  const settings = db.getSettings() || {};
  const apiKey = settings.geminiApiKey || process.env.GEMINI_API_KEY || '';
  const cleanMsg = (message || '').trim();
  const lowerMsg = cleanMsg.toLowerCase();

  const products = db.getProducts({ all: 'true' }) || [];
  const inquiries = db.getInquiries() || [];
  const users = db.getUsers() || [];

  // Compute live operational telemetry
  const formingCount = products.filter(p => p.section === 'forming').length;
  const cuttingCount = products.filter(p => p.section === 'cutting').length;
  const puneStock = products.filter(p => (p.location || '').toLowerCase().includes('pune')).length;
  const europeStock = products.filter(p => (p.location || '').toLowerCase().includes('europe')).length;
  const newInquiries = inquiries.filter(i => i.status === 'new').length;
  const recentInquiries = inquiries.slice(0, 5);

  const contextData = {
    totalMachines: products.length,
    formingCount,
    cuttingCount,
    puneStock,
    europeStock,
    totalInquiries: inquiries.length,
    newInquiries,
    totalUsers: users.length,
    recentInquiriesSummary: recentInquiries.map(i => `${i.name} (${i.company || 'Private'}) inquired for: ${i.machineName || 'General'} | Status: ${i.status}`)
  };

  if (apiKey) {
    try {
      const prompt = `
System Telemetry & Live ERP Data:
${JSON.stringify(contextData, null, 2)}

Logged in Admin Operator: ${user.name} (${user.role})
Admin Question: "${cleanMsg}"

Instructions:
1. Provide a sharp, data-backed analytical response for the Dalal Machine Tools operations team.
2. If asked about stock, give exact counts and breakdowns.
3. If asked for recommendations or proposals, draft an executive summary.
4. Keep the tone professional, authoritative, and concise.
`;
      const aiReply = await callGemini(apiKey, DALAL_KNOWLEDGE_BASE, prompt);
      if (aiReply) {
        return { reply: aiReply, stats: contextData };
      }
    } catch (err) {
      console.warn('[AI Service Admin] Gemini failed, falling back to rule engine:', err.message);
    }
  }

  // Built-in Deterministic Admin Copilot Logic
  let reply = '';
  if (lowerMsg.includes('summary') || lowerMsg.includes('stat') || lowerMsg.includes('overview') || lowerMsg.includes('dashboard')) {
    reply = `### 📊 Dalal Machine Tools Operations Summary\n\n` +
      `• **Total Inventory:** **${products.length} Machines** active in database\n` +
      `  - Metal Forming: **${formingCount}** (Heavy Forging, C-Frame, Coining, Hydraulic)\n` +
      `  - Metal Cutting: **${cuttingCount}** (Boring, Lathes, Gear Machinery)\n` +
      `• **Yard Distribution:**\n` +
      `  - Pune Stockyard: **${puneStock} Machines** (Ready for Live Power Trial)\n` +
      `  - Overseas Yard (Europe/Asia): **${europeStock} Machines** (High Seas Sales Ready)\n` +
      `• **Customer RFQ Inquiries:**\n` +
      `  - Total Recorded: **${inquiries.length}**\n` +
      `  - Pending Action (NEW): **${newInquiries}** leads awaiting quotation`;
  } else if (lowerMsg.includes('inquir') || lowerMsg.includes('lead') || lowerMsg.includes('rfq')) {
    const listText = recentInquiries.map((inq, idx) => 
      `${idx + 1}. **${inq.name}** (${inq.company || inq.phone}) &bull; *${inq.machineName || 'Catalog'}* &bull; Status: \`${inq.status.toUpperCase()}\``
    ).join('\n');
    reply = `### 📬 Recent Customer Quotation Leads\n\n` +
      `Current Active Inbox has **${newInquiries} unaddressed inquiries** out of **${inquiries.length} total**:\n\n` +
      (listText || 'No inquiries recorded yet.') +
      `\n\n*Tip:* Use the Customer RFQs tab to review contact numbers and send 1-click WhatsApp quotes.`;
  } else if (lowerMsg.includes('pune') || lowerMsg.includes('stock')) {
    const puneMachines = products.filter(p => (p.location || '').toLowerCase().includes('pune')).slice(0, 6);
    const mList = puneMachines.map(m => `• **${m.name}** (${m.make || 'Make N/A'} - ${m.tonnage ? m.tonnage + 'T' : 'N/A'})`).join('\n');
    reply = `### 📍 Machines Available at Pune Yard (${puneStock} Total)\n\n` +
      (mList || 'No machines currently assigned to Pune yard.') +
      `\n\nAll listed Pune machines are physically stored and available for live power testing upon buyer arrival.`;
  } else if (lowerMsg.includes('europe') || lowerMsg.includes('import') || lowerMsg.includes('high sea')) {
    const europeMachines = products.filter(p => (p.location || '').toLowerCase().includes('europe')).slice(0, 6);
    const mList = europeMachines.map(m => `• **${m.name}** (${m.make || 'European'} - ${m.tonnage ? m.tonnage + 'T' : 'N/A'})`).join('\n');
    reply = `### 🚢 European Sourcing & High Seas Stock (${europeStock} Total)\n\n` +
      (mList || 'No machines tagged for European yards.') +
      `\n\nThese units are available for direct CIF Nhava Sheva shipment under the buyer's IEC code with full documentation.`;
  } else {
    reply = `Hello ${user.name || 'Admin'}! I am your **Dalal Operations Copilot**.\n\n` +
      `I can help you monitor inventory statistics, query machinery stock locations, analyze pending customer RFQs, and draft commercial quotation text.\n\n` +
      `Try asking:\n` +
      `• *"Show operations summary"*\n` +
      `• *"How many machines in Pune yard?"*\n` +
      `• *"Summarize new customer inquiries"*\n` +
      `• *"List hot forging presses over 1500 Tons"*`;
  }

  return { reply, stats: contextData };
}

/**
 * 3. 1-Click Machine Product Text Parser (Form Auto-Fill)
 */
async function parseProductText(rawText) {
  if (!rawText || rawText.trim() === '') {
    throw new Error('Please provide text description or spec sheet to parse.');
  }

  const settings = db.getSettings() || {};
  const apiKey = settings.geminiApiKey || process.env.GEMINI_API_KEY || '';

  if (apiKey) {
    try {
      const prompt = `
Extract structured machinery information from this raw text:
"""
${rawText}
"""

Return ONLY a valid JSON object with EXACTLY this structure (no markdown fences, just pure JSON):
{
  "name": "Full descriptive machine title",
  "section": "forming" or "cutting",
  "category": "one of: hot-forging-press, c-frame-press, knuckle-joint-press, hydraulic-deep-draw, horizontal-boring-machine, heavy-duty-lathe, gear-hobbing-machine, other-machinery",
  "make": "Manufacturer name",
  "model": "Model code or series",
  "year": 1995 (integer or null),
  "tonnage": 2500 (integer capacity in tons or 0),
  "location": "one of: In Stock PUNE, Ready in Europe, Thailand, Vietnam, Nhava Sheva Port",
  "condition": "Descriptive condition (e.g. Excellent - Inspected under live power)",
  "priceText": "Pricing note or leave empty",
  "specs": [
    { "label": "Capacity", "val": "2500 Tons" },
    { "label": "Slide Stroke", "val": "400 mm" }
  ]
}
`;
      const aiReply = await callGemini(apiKey, 'You are an industrial machinery data parser. Output valid JSON only.', prompt);
      if (aiReply) {
        const cleanJson = aiReply.replace(/```json/gi, '').replace(/```/g, '').trim();
        const parsed = JSON.parse(cleanJson);
        return parsed;
      }
    } catch (err) {
      console.warn('[AI Parse Product] Gemini failed, using local NLP parser:', err.message);
    }
  }

  // Built-in NLP Specification Parser
  const text = rawText.trim();
  const lines = text.split('\n').map(l => l.trim()).filter(Boolean);

  let section = 'forming';
  let category = 'hot-forging-press';
  const lower = text.toLowerCase();

  if (lower.includes('lathe') || lower.includes('turning')) {
    section = 'cutting';
    category = 'heavy-duty-lathe';
  } else if (lower.includes('boring') || lower.includes('milling') || lower.includes('tos') || lower.includes('skoda')) {
    section = 'cutting';
    category = 'horizontal-boring-machine';
  } else if (lower.includes('gear') || lower.includes('hobbing') || lower.includes('shaping')) {
    section = 'cutting';
    category = 'gear-hobbing-machine';
  } else if (lower.includes('knuckle') || lower.includes('coining')) {
    section = 'forming';
    category = 'knuckle-joint-press';
  } else if (lower.includes('c-frame') || lower.includes('c frame') || lower.includes('inclinable')) {
    section = 'forming';
    category = 'c-frame-press';
  } else if (lower.includes('hydraulic') || lower.includes('deep draw')) {
    section = 'forming';
    category = 'hydraulic-deep-draw';
  }

  // Tonnage extraction
  const tonMatch = text.match(/(\d{3,4})\s*(?:t|ton|tons|tonne|tonnes|tn)\b/i);
  const tonnage = tonMatch ? parseInt(tonMatch[1], 10) : 0;

  // Year extraction
  const yearMatch = text.match(/\b(19\d\d|20[0-2]\d)\b/);
  const year = yearMatch ? parseInt(yearMatch[1], 10) : null;

  // Make extraction
  let make = '';
  if (lower.includes('voronezh') || lower.includes('tmp')) make = 'TMP Voronezh (Russia)';
  else if (lower.includes('national')) make = 'National Machinery (USA)';
  else if (lower.includes('eumuco')) make = 'Eumuco (Germany)';
  else if (lower.includes('hasenclever')) make = 'Hasenclever (SMS Group Germany)';
  else if (lower.includes('schuler')) make = 'Schuler Presses (Germany)';
  else if (lower.includes('skoda')) make = 'Skoda Machine Tools (Czech)';
  else if (lower.includes('tos')) make = 'TOS Varnsdorf';
  else if (lower.includes('hmt')) make = 'HMT Machine Tools (India)';

  // Model extraction
  let model = '';
  const modelMatch = text.match(/\b(?:model|type|series|k|kb)[\s:]*([a-z0-9\-\/]+)/i);
  if (modelMatch) model = modelMatch[1].toUpperCase();

  // Location
  let location = 'Ready in Europe';
  if (lower.includes('pune')) location = 'In Stock PUNE';
  else if (lower.includes('thailand')) location = 'Thailand';
  else if (lower.includes('vietnam')) location = 'Vietnam';
  else if (lower.includes('nhava') || lower.includes('port')) location = 'Nhava Sheva Port';

  // Extract specs from lines containing colons or dashes
  const specs = [];
  lines.forEach(line => {
    const parts = line.split(/[:=\t]/);
    if (parts.length >= 2) {
      const k = parts[0].replace(/^[\-\*\•\d\.]+\s*/, '').trim();
      const v = parts.slice(1).join(':').trim();
      if (k.length > 2 && v.length > 0 && k.length < 40) {
        specs.push({ label: k, val: v });
      }
    }
  });

  // Default specs if none extracted from lines
  if (specs.length === 0) {
    if (section === 'forming') {
      specs.push({ label: 'Capacity / Tonnage', val: tonnage ? `${tonnage} Tons` : '2000 Tons' });
      specs.push({ label: 'Slide Stroke', val: '350 mm' });
      specs.push({ label: 'Shut Height', val: '950 mm' });
      specs.push({ label: 'Bed Bolster Dimensions', val: '2200 x 1400 mm' });
    } else {
      specs.push({ label: 'Spindle Diameter', val: '130 mm' });
      specs.push({ label: 'Table Size', val: '1600 x 1400 mm' });
      specs.push({ label: 'X/Y/Z Axis Travel', val: '2000 x 1600 x 1200 mm' });
    }
  }

  // Name construction
  let name = lines[0] || '';
  if (name.length < 10) {
    const parts = [];
    if (tonnage) parts.push(`${tonnage}T`);
    if (make) parts.push(make);
    if (model) parts.push(model);
    parts.push(category.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '));
    name = parts.join(' ');
  }

  return {
    name: name.replace(/^[\-\*\#\s]+/, '').slice(0, 100),
    section,
    category,
    make,
    model,
    year,
    tonnage,
    location,
    condition: 'Excellent - Inspected Under Live Power Abroad',
    priceText: 'CIF Nhava Sheva / Ready for Import',
    specs
  };
}

/**
 * 4. Smart Inquiry Lead Scoring & WhatsApp Reply Drafter
 */
async function scoreInquiry(inquiry) {
  if (!inquiry) throw new Error('Inquiry data is required');

  const settings = db.getSettings() || {};
  const apiKey = settings.geminiApiKey || process.env.GEMINI_API_KEY || '';

  const matchedMachines = searchCatalog(inquiry.machineName || inquiry.message || '');
  const topMatched = matchedMachines[0] || null;

  if (apiKey) {
    try {
      const prompt = `
Analyze this customer machinery quotation request:
Customer Name: ${inquiry.name}
Company: ${inquiry.company || 'Not mentioned'}
Phone: ${inquiry.phone || 'N/A'}
Email: ${inquiry.email || 'N/A'}
Machine Inquired: ${inquiry.machineName || 'N/A'}
Message: "${inquiry.message || ''}"

Return ONLY a JSON object:
{
  "leadScore": "HOT" or "WARM" or "GENERAL",
  "scoreReason": "Why this lead was scored this way (budget clarity, urgency, company stature)",
  "intentSummary": "1-line summary of what the buyer needs",
  "suggestedWhatsAppReply": "A polite, professional WhatsApp message draft ready to send to the customer with machine details and invite for inspection."
}
`;
      const aiReply = await callGemini(apiKey, DALAL_KNOWLEDGE_BASE, prompt);
      if (aiReply) {
        const clean = aiReply.replace(/```json/gi, '').replace(/```/g, '').trim();
        const parsed = JSON.parse(clean);
        return {
          ...parsed,
          matchedMachines: matchedMachines.slice(0, 3)
        };
      }
    } catch (err) {
      console.warn('[AI Score Inquiry] Gemini call failed, using rule engine:', err.message);
    }
  }

  // Deterministic Rule-Based Lead Scoring
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
    `Namaste ${inquiry.name} ji,\n\n` +
    `Thank you for contacting Dalal Machine Tools Agency Pvt. Ltd. regarding *${machineTitle}*.\n\n` +
    `We have reviewed your inquiry and have ready options with complete inspection videos under live power.\n\n` +
    `Would you like us to share the detailed technical specification sheet and CIF Nhava Sheva / Ex-Pune Yard commercial proposal?\n\n` +
    `Warm regards,\n` +
    `Sales Team | Dalal Machine Tools Agency Pvt. Ltd.\n` +
    `Phone: +91 9821232131 / +91 9820088888\n` +
    `Website: dalalmachines.com`;

  return {
    leadScore,
    scoreReason,
    intentSummary: `Quotation requested for ${machineTitle}${inquiry.company ? ' by ' + inquiry.company : ''}.`,
    suggestedWhatsAppReply: whatsappDraft,
    matchedMachines: matchedMachines.slice(0, 3)
  };
}

module.exports = {
  chatWithCustomer,
  chatWithAdminCopilot,
  parseProductText,
  scoreInquiry,
  callGemini,
  searchCatalog
};
