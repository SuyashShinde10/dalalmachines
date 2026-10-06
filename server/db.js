const fs = require('fs');
const path = require('path');
const bcrypt = require('bcryptjs');
const crypto = require('crypto');
const config = require('./config');

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
    autoSyncCatalogJs: true
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
    return db.products.find(p => p.id === id);
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
    syncToCatalogJs();

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
    syncToCatalogJs();

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
    syncToCatalogJs();

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

  // Categories
  getCategories: () => db.categories,

  // Inquiries
  getInquiries: () => db.inquiries,
  createInquiry: (data) => {
    const newInquiry = {
      id: 'inq_' + crypto.randomUUID().slice(0, 8),
      name: data.name || 'Anonymous',
      email: data.email || '',
      phone: data.phone || '',
      company: data.company || '',
      machineId: data.machineId || null,
      machineName: data.machineName || null,
      message: data.message || '',
      status: 'new',
      createdAt: new Date().toISOString()
    };
    db.inquiries.unshift(newInquiry);
    saveDb();
    return newInquiry;
  },
  updateInquiryStatus: (id, status, actor) => {
    const inq = db.inquiries.find(i => i.id === id);
    if (!inq) return null;
    inq.status = status;
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

  // Activity Logs
  getLogs: (limit = 100) => {
    return db.logs.slice(0, limit);
  },
  addLog: ({ userId, username, role, action, target, details, ip }) => {
    const entry = {
      id: 'log_' + crypto.randomUUID().slice(0, 8),
      timestamp: new Date().toISOString(),
      userId: userId || 'system',
      username: username || 'SYSTEM',
      role: role || 'admin',
      action,
      target: target || '-',
      details: details || '',
      ip: ip || '127.0.0.1'
    };
    db.logs.unshift(entry);
    // Keep last 1000 logs
    if (db.logs.length > 1000) {
      db.logs = db.logs.slice(0, 1000);
    }
    saveDb();
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
  syncToCatalogJs
};
