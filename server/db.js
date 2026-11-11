const fs = require('fs');
const path = require('path');
const bcrypt = require('bcryptjs');
const crypto = require('crypto');
const config = require('./config');
const cacheEngine = require('./performance/cacheEngine');
const { computeLogHash, verifyAuditChain } = require('./security/defenseInDepth');

// In-Memory High-Speed Indexing Engine for O(1) Lookups
const productIndex = new Map();

function rebuildProductIndex() {
  productIndex.clear();
  if (Array.isArray(db.products)) {
    for (const p of db.products) {
      if (p && p.id) {
        productIndex.set(p.id, p);
      }
    }
  }
}

// Ensure data directories exist
if (!fs.existsSync(config.DATA_DIR)) {
  fs.mkdirSync(config.DATA_DIR, { recursive: true });
}
if (!fs.existsSync(config.UPLOADS_DIR)) {
  fs.mkdirSync(config.UPLOADS_DIR, { recursive: true });
}

let db = {
  users: [],
  products: [],
  categories: [],
  inquiries: [],
  logs: [],
  settings: {
    siteName: "Dalal Machine Tools Agency Pvt. Ltd.",
    whatsappNumber: "+919820088888",
    contactEmail: "info@dalalmachines.com",
    ompiEnabled: true,
    currency: "INR",
    autoSyncCatalogJs: true,
    geminiApiKey: process.env.GEMINI_API_KEY || ""
  }
};

function saveDb() {
  try {
    const tmpPath = config.DB_FILE + '.tmp';
    fs.writeFileSync(tmpPath, JSON.stringify(db, null, 2), 'utf8');
    fs.renameSync(tmpPath, config.DB_FILE);
  } catch (err) {
    console.error('Error saving db.json:', err);
  }
}

function loadDb() {
  if (fs.existsSync(config.DB_FILE)) {
    try {
      const content = fs.readFileSync(config.DB_FILE, 'utf8');
      db = JSON.parse(content);
      rebuildProductIndex();
      return;
    } catch (err) {
      console.error('Error reading db.json, re-initializing...', err);
    }
  }

  // Seed Initial Database
  console.log('Seeding fresh database with users and existing catalog...');

  // 1. Initial Users
  const salt = bcrypt.genSaltSync(10);
  db.users = [
    {
      id: 'usr_superadmin_md',
      username: 'superadmin',
      email: 'superadmin@dalalmachines.com',
      passwordHash: bcrypt.hashSync('Dalal@Super2026', salt),
      role: 'superadmin',
      name: 'Super Admin (MD)',
      active: true,
      createdAt: new Date().toISOString(),
      lastLogin: null
    },
    {
      id: 'usr_superadmin',
      username: 'developer',
      email: 'developer@dalalmachines.com',
      passwordHash: bcrypt.hashSync('Developer@2026', salt),
      role: 'superadmin',
      name: 'System Developer',
      active: true,
      createdAt: new Date().toISOString(),
      lastLogin: null
    },
    {
      id: 'usr_admin',
      username: 'admin',
      email: 'admin@dalalmachines.com',
      passwordHash: bcrypt.hashSync('Dalal@Admin2026', salt),
      role: 'admin',
      name: 'Dalal Inventory Admin',
      active: true,
      createdAt: new Date().toISOString(),
      lastLogin: null
    }
  ];

  // 2. Seed Products from catalog-data.js
  if (fs.existsSync(config.CATALOG_JS_PATH)) {
    try {
      const content = fs.readFileSync(config.CATALOG_JS_PATH, 'utf8');
      const start = content.indexOf('[');
      const end = content.indexOf('];') + 1;
      if (start !== -1 && end > start) {
        const parsed = JSON.parse(content.substring(start, end));
        db.products = parsed.map((m, idx) => ({
          ...m,
          isCustom: m.isCustom || false,
          status: m.status || 'active',
          galleryImages: m.galleryImages || [m.image],
          createdAt: new Date(Date.now() - (parsed.length - idx) * 3600000).toISOString(),
          updatedAt: new Date().toISOString(),
          createdBy: 'system_import'
        }));
      }
    } catch (parseErr) {
      console.error('Failed to parse catalog-data.js for seeding:', parseErr);
      db.products = [];
    }
  }

  // 3. Extract Categories
  const categoryMap = {};
  db.products.forEach(p => {
    if (p.category && !categoryMap[p.category]) {
      categoryMap[p.category] = {
        slug: p.category,
        name: p.categoryName || p.category,
        section: p.section || 'forming',
        count: 0
      };
    }
    if (categoryMap[p.category]) {
      categoryMap[p.category].count++;
    }
  });
  db.categories = Object.values(categoryMap);

  // 4. Sample Inquiries
  db.inquiries = [
    {
      id: 'inq_sample_01',
      name: 'Rajesh Sharma',
      email: 'r.sharma@forgeind.com',
      phone: '+91 98234 11223',
      company: 'Precision Forgings Pune',
      machineId: 'P00007',
      machineName: '2500T RUSSIAN TMP-VORONEZH Hot Forging Press',
      message: 'Interested in CIF Nhava Sheva quote and inspection video under live power.',
      status: 'new',
      createdAt: new Date(Date.now() - 86400000).toISOString()
    }
  ];

  // 5. Initial Log
  db.logs = [
    {
      id: 'log_' + crypto.randomUUID().slice(0, 8),
      timestamp: new Date().toISOString(),
      userId: 'system',
      username: 'SYSTEM',
      role: 'system',
      action: 'SYSTEM_INIT',
      target: 'DATABASE',
      details: `Database initialized with ${db.products.length} machines and 2 default user accounts.`
    }
  ];

  saveDb();
  rebuildProductIndex();
}

// Write back to catalog-data.js so static client pages stay 100% updated
function syncToCatalogJs() {
  if (!db.settings.autoSyncCatalogJs) return;
  try {
    const activeProducts = db.products.filter(p => p.status === 'active');
    const jsHeader = `// Dalal Machine Tools Agency Pvt. Ltd. - Audited Inventory Database\n// Auto-synced from Dalal Admin Portal\nvar DALAL_MACHINES = ${JSON.stringify(activeProducts, null, 2)};\n\n// Helper: Filter machines\nfunction getMachines(filterOptions = {}) {\n  return DALAL_MACHINES.filter(m => {\n    if (filterOptions.category) {\n      if (m.category !== filterOptions.category) return false;\n    } else if (filterOptions.section) {\n      if (m.section !== filterOptions.section) return false;\n    }\n    if (filterOptions.location && !m.location.toLowerCase().includes(filterOptions.location.toLowerCase())) return false;\n    if (filterOptions.query) {\n      const q = filterOptions.query.toLowerCase();\n      const match = m.name.toLowerCase().includes(q) ||\n                    m.make.toLowerCase().includes(q) ||\n                    m.model.toLowerCase().includes(q) ||\n                    m.id.toLowerCase().includes(q) ||\n                    (m.categoryName && m.categoryName.toLowerCase().includes(q));\n      if (!match) return false;\n    }\n    return true;\n  });\n}\n`;
    fs.writeFileSync(config.CATALOG_JS_PATH, jsHeader, 'utf8');
  } catch (err) {
    console.error('Failed to sync to catalog-data.js:', err);
  }
}

// Initialize on module load
loadDb();

// DB API Methods
module.exports = {
  // Users
  getUsers: () => {
    return db.users.map(({ passwordHash, ...safeUser }) => safeUser);
  },
  getUserById: (id) => {
    return db.users.find(u => u.id === id);
  },
  getUserByUsernameOrEmail: (identifier) => {
    const lower = identifier.toLowerCase();
    return db.users.find(u => u.username.toLowerCase() === lower || u.email.toLowerCase() === lower);
  },
  createUser: (userData, actor) => {
    const salt = bcrypt.genSaltSync(10);
    const newUser = {
      id: 'usr_' + crypto.randomUUID().slice(0, 8),
      username: userData.username.trim().toLowerCase(),
      email: userData.email.trim().toLowerCase(),
      passwordHash: bcrypt.hashSync(userData.password, salt),
      role: userData.role === 'superadmin' ? 'superadmin' : 'admin',
      name: userData.name || userData.username,
      active: true,
      createdAt: new Date().toISOString(),
      lastLogin: null
    };
    db.users.push(newUser);
    saveDb();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'USER_CREATED',
      target: newUser.username,
      details: `Created user ${newUser.username} with role ${newUser.role}`
    });
    const { passwordHash, ...safe } = newUser;
    return safe;
  },
  updateUser: (id, updates, actor) => {
    const user = db.users.find(u => u.id === id);
    if (!user) return null;
    if (updates.name) user.name = updates.name;
    if (updates.email) user.email = updates.email.trim().toLowerCase();
    if (updates.role && ['admin', 'superadmin'].includes(updates.role)) user.role = updates.role;
    if (typeof updates.active === 'boolean') user.active = updates.active;
    if (updates.password) {
      user.passwordHash = bcrypt.hashSync(updates.password, 10);
    }
    saveDb();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'USER_UPDATED',
      target: user.username,
      details: `Updated user details for ${user.username}`
    });
    const { passwordHash, ...safe } = user;
    return safe;
  },
  deleteUser: (id, actor) => {
    const idx = db.users.findIndex(u => u.id === id);
    if (idx === -1) return false;
    const deletedUser = db.users[idx];
    db.users.splice(idx, 1);
    saveDb();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'USER_DELETED',
      target: deletedUser.username,
      details: `Deleted user ${deletedUser.username}`
    });
    return true;
  },
  updateUserLoginTimestamp: (id) => {
    const user = db.users.find(u => u.id === id);
    if (user) {
      user.lastLogin = new Date().toISOString();
      saveDb();
    }
  },

  // Developer Governance (Block/Unblock Admin & Superadmin - ZERO Client Data)
  getAdminAccountsForDev: () => {
    return db.users
      .filter(u => u.role === 'admin' || u.role === 'superadmin' || u.role === 'staff')
      .map(({ passwordHash, ...safe }) => ({
        id: safe.id,
        username: safe.username,
        name: safe.name,
        email: safe.email,
        role: safe.role,
        active: safe.active !== false,
        blockedByDeveloper: Boolean(safe.blockedByDeveloper),
        blockedReason: safe.blockedReason || '',
        blockedAt: safe.blockedAt || null,
        createdAt: safe.createdAt,
        lastLogin: safe.lastLogin
      }));
  },
  blockUserByDeveloper: (id, reason, actor = { id: 'usr_dev', username: 'developer_console', role: 'developer' }) => {
    const user = db.users.find(u => u.id === id);
    if (!user) return null;
    user.active = false;
    user.blockedByDeveloper = true;
    user.blockedReason = reason || 'Account suspended by Lead System Developer.';
    user.blockedAt = new Date().toISOString();
    saveDb();

    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: 'developer',
      action: 'USER_BLOCKED_BY_DEVELOPER',
      target: user.username,
      details: `Developer suspended ${user.role.toUpperCase()} [${user.username}]. Reason: ${user.blockedReason}`
    });

    const { passwordHash, ...safe } = user;
    return safe;
  },
  unblockUserByDeveloper: (id, actor = { id: 'usr_dev', username: 'developer_console', role: 'developer' }) => {
    const user = db.users.find(u => u.id === id);
    if (!user) return null;
    user.active = true;
    user.blockedByDeveloper = false;
    user.blockedReason = '';
    user.blockedAt = null;
    saveDb();

    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: 'developer',
      action: 'USER_UNBLOCKED_BY_DEVELOPER',
      target: user.username,
      details: `Developer unblocked/restored ${user.role.toUpperCase()} [${user.username}].`
    });

    const { passwordHash, ...safe } = user;
    return safe;
  },

  // Developer Google Doodle / Dashboard Banner
  getDeveloperBanner: () => {
    if (!db.developerBanner) {
      db.developerBanner = {
        active: false,
        style: 'doodle-gold',
        badgeText: '✨ DEVELOPER DOODLE SPOTLIGHT',
        title: 'Dalal Engineering Live Stockyard Milestone',
        message: 'High Seas import clearance and 4,000T Forging Press trial slots are now active across Pune and Ludhiana yards.',
        icon: 'fa-trophy',
        linkText: 'Explore Machines',
        linkUrl: '/admin/products.html',
        dismissable: true,
        updatedAt: new Date().toISOString()
      };
    }
    return db.developerBanner;
  },
  setDeveloperBanner: (bannerData, actor = { id: 'usr_dev', username: 'developer_console', role: 'developer' }) => {
    const current = module.exports.getDeveloperBanner();
    db.developerBanner = {
      ...current,
      ...bannerData,
      updatedAt: new Date().toISOString()
    };
    saveDb();

    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: 'developer',
      action: 'DEVELOPER_BANNER_UPDATED',
      target: 'DASHBOARD_BANNER',
      details: `Developer updated banner. Active: ${db.developerBanner.active}, Style: ${db.developerBanner.style}`
    });

    return db.developerBanner;
  },

  // Products
  getProducts: (filters = {}) => {
    let list = [...db.products];
    if (filters.section) {
      list = list.filter(p => p.section === filters.section);
    }
    if (filters.category) {
      list = list.filter(p => p.category === filters.category);
    }
    if (filters.location) {
      const loc = filters.location.toLowerCase();
      list = list.filter(p => p.location && p.location.toLowerCase().includes(loc));
    }
    if (filters.status) {
      list = list.filter(p => p.status === filters.status);
    }
    if (filters.query) {
      const q = filters.query.toLowerCase();
      list = list.filter(p =>
        (p.name && p.name.toLowerCase().includes(q)) ||
        (p.id && p.id.toLowerCase().includes(q)) ||
        (p.make && p.make.toLowerCase().includes(q)) ||
        (p.model && p.model.toLowerCase().includes(q)) ||
        (p.categoryName && p.categoryName.toLowerCase().includes(q))
      );
    }
    return list;
  },
  getProductById: (id) => {
    if (!id) return null;
    return productIndex.get(id) || db.products.find(p => p.id === id) || null;
  },
  createProduct: (productData, actor) => {
    // Generate machine ID if not provided
    let newId = productData.id ? productData.id.trim().toUpperCase() : '';
    if (!newId) {
      const prefix = productData.section === 'cutting' ? 'P000' : 'P000';
      const num = 100 + Math.floor(Math.random() * 900);
      newId = `${prefix}${num}${productData.isCustom ? '-CUST' : ''}`;
    }

    const newProduct = {
      id: newId,
      name: productData.name,
      section: productData.section || 'forming',
      category: productData.category || 'other-machinery',
      categoryName: productData.categoryName || 'Other Machinery',
      make: productData.make || 'Custom / Unspecified',
      model: productData.model || '-',
      year: parseInt(productData.year) || new Date().getFullYear(),
      tonnage: parseInt(productData.tonnage) || 0,
      location: productData.location || 'In Stock PUNE',
      condition: productData.condition || 'Operational',
      image: productData.image || 'images/dalal/cframe_press_pune.jpg',
      galleryImages: Array.isArray(productData.galleryImages) && productData.galleryImages.length > 0 
        ? productData.galleryImages 
        : [productData.image || 'images/dalal/cframe_press_pune.jpg'],
      specs: productData.specs || {},
      isCustom: Boolean(productData.isCustom),
      customBadges: productData.customBadges || [],
      priceText: productData.priceText || 'Price On Request',
      brochurePdf: productData.brochurePdf || null,
      status: productData.status || 'active',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      createdBy: actor.username
    };

    db.products.unshift(newProduct);
    saveDb();
    rebuildProductIndex();
    syncToCatalogJs();
    cacheEngine.invalidate('/api/products');

    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'PRODUCT_CREATED',
      target: newProduct.id,
      details: `Created machine ${newProduct.name} (${newProduct.isCustom ? 'Custom Machine' : 'Standard Machine'})`
    });

    return newProduct;
  },
  updateProduct: (id, updates, actor) => {
    const product = db.products.find(p => p.id === id);
    if (!product) return null;

    Object.assign(product, updates, {
      updatedAt: new Date().toISOString()
    });

    saveDb();
    rebuildProductIndex();
    syncToCatalogJs();
    cacheEngine.invalidate('/api/products');

    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'PRODUCT_UPDATED',
      target: product.id,
      details: `Updated details for machine ${product.name}`
    });

    return product;
  },
  deleteProduct: (id, actor) => {
    const idx = db.products.findIndex(p => p.id === id);
    if (idx === -1) return false;

    const deleted = db.products[idx];
    db.products.splice(idx, 1);
    saveDb();
    rebuildProductIndex();
    syncToCatalogJs();
    cacheEngine.invalidate('/api/products');

    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'PRODUCT_DELETED',
      target: deleted.id,
      details: `Deleted machine ${deleted.name}`
    });

    return true;
  },
  updateConfidentialPricing: (id, { procurementCost, floorPrice, targetPrice, inspectionVideos }, actor) => {
    const product = db.products.find(p => p.id === id);
    if (!product) return null;

    if (procurementCost !== undefined) product.procurementCost = parseFloat(procurementCost) || 0;
    if (floorPrice !== undefined) product.floorPrice = parseFloat(floorPrice) || 0;
    if (targetPrice !== undefined) product.targetPrice = parseFloat(targetPrice) || 0;
    if (Array.isArray(inspectionVideos)) product.inspectionVideos = inspectionVideos;
    product.updatedAt = new Date().toISOString();

    saveDb();
    rebuildProductIndex();

    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'CONFIDENTIAL_PRICING_UPDATED',
      target: product.id,
      details: `Superadmin updated confidential floor price (₹${product.floorPrice}) & procurement cost for ${product.name}`
    });

    return product;
  },

  // Categories
  getCategories: () => db.categories,

  // Inquiries & Pipeline Management
  getInquiries: () => db.inquiries,
  createInquiry: (data) => {
    const estVal = parseFloat(data.estimatedValue) || (data.tonnage ? data.tonnage * 12000 + 1500000 : 2500000);
    const createdAt = new Date().toISOString();
    const newInquiry = {
      id: 'inq_' + crypto.randomUUID().slice(0, 8),
      name: data.name || 'Anonymous',
      email: data.email || '',
      phone: data.phone || '',
      company: data.company || '',
      city: data.city || 'Mumbai',
      machineId: data.machineId || null,
      machineName: data.machineName || null,
      message: data.message || '',
      status: 'new',
      pipelineStage: 'new',
      estimatedValue: estVal,
      isVipDeal: estVal >= 5000000,
      assignedStaffId: data.assignedStaffId || 'usr_admin',
      assignedStaffName: data.assignedStaffName || 'Dalal Inventory Admin',
      slaDeadline: new Date(Date.now() + 24 * 3600 * 1000).toISOString(),
      inspectionVideoLinks: Array.isArray(data.inspectionVideoLinks) ? data.inspectionVideoLinks : [],
      notes: data.notes || '',
      createdAt
    };
    db.inquiries.unshift(newInquiry);
    saveDb();
    return newInquiry;
  },
  updateInquiryStatus: (id, status, actor) => {
    const inq = db.inquiries.find(i => i.id === id);
    if (!inq) return null;
    inq.status = status;
    inq.pipelineStage = status;
    saveDb();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'INQUIRY_STATUS_CHANGED',
      target: id,
      details: `Changed inquiry status to ${status}`
    });
    return inq;
  },
  updateInquiryPipeline: (id, updates, actor) => {
    const inq = db.inquiries.find(i => i.id === id);
    if (!inq) return null;

    if (updates.pipelineStage) {
      inq.pipelineStage = updates.pipelineStage;
      inq.status = updates.pipelineStage;
    }
    if (updates.estimatedValue !== undefined) {
      inq.estimatedValue = parseFloat(updates.estimatedValue) || 0;
      inq.isVipDeal = inq.estimatedValue >= 5000000;
    }
    if (updates.notes !== undefined) inq.notes = updates.notes;
    if (Array.isArray(updates.inspectionVideoLinks)) inq.inspectionVideoLinks = updates.inspectionVideoLinks;
    if (updates.isVipDeal !== undefined) inq.isVipDeal = Boolean(updates.isVipDeal);
    inq.lastFollowUpAt = new Date().toISOString();

    saveDb();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'INQUIRY_PIPELINE_UPDATED',
      target: id,
      details: `Updated pipeline for lead ${inq.name} (${inq.company || 'Direct'}): Stage=${inq.pipelineStage}, Deal Value=₹${inq.estimatedValue}`
    });
    return inq;
  },
  assignInquiry: (id, staffId, staffName, actor) => {
    const inq = db.inquiries.find(i => i.id === id);
    if (!inq) return null;
    inq.assignedStaffId = staffId;
    inq.assignedStaffName = staffName;
    saveDb();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'INQUIRY_ASSIGNED',
      target: id,
      details: `Assigned inquiry ${id} to ${staffName}`
    });
    return inq;
  },
  getExecutivePipelineMetrics: () => {
    const list = db.inquiries || [];
    const now = Date.now();
    let totalPipelineVal = 0;
    let closedRevenueVal = 0;
    let overdueCount = 0;
    let vipCount = 0;

    const stageCounts = {
      new: 0,
      power_trial_requested: 0,
      quotation_sent: 0,
      under_negotiation: 0,
      deal_closed: 0,
      deal_lost: 0
    };
    const stageValues = {
      new: 0,
      power_trial_requested: 0,
      quotation_sent: 0,
      under_negotiation: 0,
      deal_closed: 0,
      deal_lost: 0
    };

    const cityMap = {};
    const catMap = {
      'Mechanical Forming Presses': 0,
      'Hydraulic Forging Presses': 0,
      'Horizontal Boring Machines': 0,
      'Vertical Machining Centers (VMC)': 0,
      'Heavy Duty Lathes & Turning': 0
    };

    list.forEach(inq => {
      const stage = inq.pipelineStage || inq.status || 'new';
      const val = parseFloat(inq.estimatedValue) || 2500000;

      if (stageCounts[stage] !== undefined) {
        stageCounts[stage]++;
        stageValues[stage] += val;
      } else {
        stageCounts['new']++;
        stageValues['new'] += val;
      }

      if (stage === 'deal_closed') {
        closedRevenueVal += val;
      } else if (stage !== 'deal_lost') {
        totalPipelineVal += val;
      }

      if (inq.isVipDeal) vipCount++;

      // Check SLA overdue: if still new or power_trial_requested and past 24 hours
      if ((stage === 'new' || stage === 'power_trial_requested') && inq.slaDeadline) {
        if (new Date(inq.slaDeadline).getTime() < now) {
          overdueCount++;
        }
      }

      const city = inq.city || 'Mumbai';
      cityMap[city] = (cityMap[city] || 0) + 1;

      // Classify category from machineName or fallback
      const mName = (inq.machineName || '').toLowerCase();
      if (mName.includes('hydraulic') || mName.includes('forging')) {
        catMap['Hydraulic Forging Presses']++;
      } else if (mName.includes('boring') || mName.includes('btd') || mName.includes('horizontal')) {
        catMap['Horizontal Boring Machines']++;
      } else if (mName.includes('vmc') || mName.includes('machining center') || mName.includes('5-axis')) {
        catMap['Vertical Machining Centers (VMC)']++;
      } else if (mName.includes('lathe') || mName.includes('turning')) {
        catMap['Heavy Duty Lathes & Turning']++;
      } else {
        catMap['Mechanical Forming Presses']++;
      }
    });

    const geoDemand = Object.entries(cityMap)
      .map(([city, count]) => ({ city, count, percentage: Math.round((count / (list.length || 1)) * 100) }))
      .sort((a, b) => b.count - a.count);

    const categoryDemand = Object.entries(catMap)
      .map(([category, count]) => ({ category, count, percentage: Math.round((count / (list.length || 1)) * 100) }))
      .sort((a, b) => b.count - a.count);

    return {
      totalLeads: list.length,
      totalPipelineVal,
      closedRevenueVal,
      overdueCount,
      vipCount,
      stageCounts,
      stageValues,
      geoDemand,
      categoryDemand
    };
  },

  // High-Seas & Import Consignments
  getConsignments: () => db.consignments || [],
  getConsignmentById: (id) => (db.consignments || []).find(c => c.id === id) || null,
  createConsignment: (data, actor) => {
    if (!Array.isArray(db.consignments)) db.consignments = [];
    const newCsg = {
      id: 'csg_' + crypto.randomUUID().slice(0, 8),
      title: data.title || 'European Machinery Consignment',
      originPort: data.originPort || 'Hamburg, Germany',
      destinationPort: data.destinationPort || 'JNPT / Nhava Sheva, Mumbai',
      vesselName: data.vesselName || 'MSC CARGO',
      containerNumbers: Array.isArray(data.containerNumbers) ? data.containerNumbers : (data.containerNumbers ? [data.containerNumbers] : []),
      billOfLading: data.billOfLading || 'BL-DMTA-' + Date.now(),
      status: data.status || 'high_seas_transit',
      eta: data.eta || new Date(Date.now() + 14 * 86400000).toISOString().split('T')[0],
      totalMachines: parseInt(data.totalMachines, 10) || 1,
      valueInr: parseFloat(data.valueInr) || 5000000,
      updatedAt: new Date().toISOString()
    };
    db.consignments.unshift(newCsg);
    saveDb();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'CONSIGNMENT_CREATED',
      target: newCsg.id,
      details: `Created High-Seas shipment: ${newCsg.title} (${newCsg.vesselName})`
    });
    return newCsg;
  },
  updateConsignment: (id, updates, actor) => {
    if (!Array.isArray(db.consignments)) return null;
    const csg = db.consignments.find(c => c.id === id);
    if (!csg) return null;
    Object.assign(csg, updates, { updatedAt: new Date().toISOString() });
    saveDb();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'CONSIGNMENT_UPDATED',
      target: id,
      details: `Updated consignment ${csg.title} to status ${csg.status}`
    });
    return csg;
  },
  deleteConsignment: (id, actor) => {
    if (!Array.isArray(db.consignments)) return false;
    const idx = db.consignments.findIndex(c => c.id === id);
    if (idx === -1) return false;
    const deleted = db.consignments[idx];
    db.consignments.splice(idx, 1);
    saveDb();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'CONSIGNMENT_DELETED',
      target: id,
      details: `Deleted consignment ${deleted.title}`
    });
    return true;
  },

  // 2FA Management
  setUser2FA: (userId, { enabled, secret, recoveryCode }, actor) => {
    const user = db.users.find(u => u.id === userId);
    if (!user) return null;
    user.twoFactorEnabled = !!enabled;
    if (secret !== undefined) user.twoFactorSecret = secret;
    if (recoveryCode !== undefined) user.twoFactorRecoveryCode = recoveryCode;
    saveDb();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: enabled ? '2FA_ENABLED' : '2FA_DISABLED',
      target: user.username,
      details: `Superadmin ${user.username} ${enabled ? 'ACTIVATED' : 'DEACTIVATED'} RFC 6238 Two-Factor Authentication`
    });
    return { success: true, twoFactorEnabled: user.twoFactorEnabled };
  },

  // Activity Logs
  getLogs: (limit = 100) => {
    return db.logs.slice(0, limit);
  },
  addLog: ({ userId, username, role, action, target, details, ip }) => {
    const prevEntry = db.logs && db.logs.length > 0 ? db.logs[0] : null;
    const prevHash = prevEntry && prevEntry.hash ? prevEntry.hash : 'GENESIS_HASH_DMTA_2026';

    const entry = {
      id: 'log_' + crypto.randomUUID().slice(0, 8),
      timestamp: new Date().toISOString(),
      userId: userId || 'system',
      username: username || 'SYSTEM',
      role: role || 'admin',
      action,
      target: target || '-',
      details: details || '',
      ip: ip || '127.0.0.1',
      prevHash,
      hash: ''
    };
    entry.hash = computeLogHash(entry, prevHash);

    db.logs.unshift(entry);
    // Keep last 1000 logs
    if (db.logs.length > 1000) {
      db.logs = db.logs.slice(0, 1000);
    }
    saveDb();
    try {
      const realtime = require('./realtime');
      realtime.broadcastLogEntry(entry);
    } catch (e) {}
    return entry;
  },

  // Settings
  getSettings: () => db.settings,
  updateSettings: (newSettings, actor) => {
    Object.assign(db.settings, newSettings);
    saveDb();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'SETTINGS_UPDATED',
      target: 'SYSTEM',
      details: 'Updated system settings'
    });
    return db.settings;
  },

  // Developer / Backup Tools
  getBackup: () => db,
  restoreBackup: (backupData, actor) => {
    if (!backupData || !Array.isArray(backupData.products) || !Array.isArray(backupData.users)) {
      throw new Error('Invalid backup data format');
    }
    db = backupData;
    saveDb();
    syncToCatalogJs();
    module.exports.addLog({
      userId: actor.id,
      username: actor.username,
      role: actor.role,
      action: 'DATABASE_RESTORED',
      target: 'SYSTEM',
      details: `Restored database from JSON backup (${db.products.length} machines)`
    });
    return true;
  },
  verifyAuditIntegrity: () => verifyAuditChain(db.logs),
  rebuildProductIndex,
  syncToCatalogJs
};
