const express = require('express');
const router = express.Router();
const aiService = require('../services/aiService');
const db = require('../db');
const { requireAdmin, requireSuperAdmin } = require('../middleware/auth');
const { rateLimit } = require('express-rate-limit');

// Rate limiter for public chat (prevent spam/abuse)
const chatLimiter = rateLimit({
  windowMs: 10 * 60 * 1000, // 10 minutes
  limit: 60, // 60 messages per 10 minutes per IP
  standardHeaders: 'draft-8',
  legacyHeaders: false,
  message: {
    success: false,
    message: 'AI assistant rate limit reached. Please wait a few moments or call us directly at +91 9821232131.'
  }
});

// GET /api/ai/status
router.get('/status', (req, res) => {
  const settings = db.getSettings() || {};
  const apiKey = settings.geminiApiKey || process.env.GEMINI_API_KEY || '';
  res.json({
    success: true,
    hasGeminiKey: Boolean(apiKey && apiKey.length > 10),
    activeEngine: (apiKey && apiKey.length > 10) ? 'Google Gemini 2.0 Flash' : 'Built-in Machinery Intelligence Engine',
    capabilities: [
      'Customer Catalog Advisory & Search',
      'Hinglish & Regional Language NLP',
      'High Seas Duty Savings Guidance',
      'Admin Operations Copilot',
      '1-Click Product Form Auto-Fill',
      'Smart Lead Scoring & WhatsApp Drafting'
    ]
  });
});

// POST /api/ai/chat (Public customer-facing chatbot)
router.post('/chat', chatLimiter, async (req, res) => {
  try {
    const { message, history, language } = req.body;
    if (!message || typeof message !== 'string' || message.trim() === '') {
      return res.status(400).json({ success: false, message: 'Message is required.' });
    }

    const result = await aiService.chatWithCustomer({
      message: message.trim(),
      history: Array.isArray(history) ? history : [],
      language: language || 'en'
    });

    res.json({
      success: true,
      reply: result.reply,
      matchedMachines: result.matchedMachines || [],
      chips: result.chips || []
    });
  } catch (err) {
    console.error('[AI Chat Route Error]:', err);
    res.status(500).json({
      success: false,
      message: 'Failed to process AI chat response: ' + err.message
    });
  }
});

// POST /api/ai/matchmaker (Enterprise AI Machinery Matchmaker & Technical Search)
router.post('/matchmaker', chatLimiter, async (req, res) => {
  try {
    const { query, options } = req.body;
    if (!query || typeof query !== 'string' || query.trim() === '') {
      return res.status(400).json({
        success: false,
        message: 'Industrial search query is required (e.g. "1600 ton forging press Pune").'
      });
    }

    const matchResult = aiService.matchMachinesTechnical(query.trim(), options);
    res.json({
      success: true,
      ...matchResult
    });
  } catch (err) {
    console.error('[AI Matchmaker Error]:', err);
    res.status(500).json({
      success: false,
      message: 'Failed to execute technical machine matchmaker: ' + err.message
    });
  }
});

// POST /api/ai/admin/copilot (Staff Admin & Superadmin Operations Assistant)
router.post('/admin/copilot', requireAdmin, async (req, res) => {
  try {
    const { message } = req.body;
    if (!message || typeof message !== 'string' || message.trim() === '') {
      return res.status(400).json({ success: false, message: 'Message is required.' });
    }

    const result = await aiService.chatWithAdminCopilot({
      message: message.trim(),
      user: req.user
    });

    res.json({
      success: true,
      reply: result.reply,
      stats: result.stats
    });
  } catch (err) {
    console.error('[AI Admin Copilot Error]:', err);
    res.status(500).json({
      success: false,
      message: 'Admin copilot error: ' + err.message
    });
  }
});

// POST /api/ai/parse-product (1-Click Machine Form Autofill)
router.post('/parse-product', requireAdmin, async (req, res) => {
  try {
    const { rawText } = req.body;
    if (!rawText || typeof rawText !== 'string' || rawText.trim() === '') {
      return res.status(400).json({ success: false, message: 'Raw machinery text or spec sheet is required.' });
    }

    const parsed = await aiService.parseProductText(rawText.trim());
    res.json({
      success: true,
      data: parsed
    });
  } catch (err) {
    console.error('[AI Parse Product Error]:', err);
    res.status(500).json({
      success: false,
      message: 'Failed to parse machinery text: ' + err.message
    });
  }
});

// POST /api/ai/score-inquiry (Inquiry Lead Scoring & WhatsApp reply)
router.post('/score-inquiry', requireAdmin, async (req, res) => {
  try {
    const { inquiry } = req.body;
    if (!inquiry) {
      return res.status(400).json({ success: false, message: 'Inquiry details are required.' });
    }

    const analysis = await aiService.scoreInquiry(inquiry);
    res.json({
      success: true,
      analysis
    });
  } catch (err) {
    console.error('[AI Score Inquiry Error]:', err);
    res.status(500).json({
      success: false,
      message: 'Failed to score inquiry: ' + err.message
    });
  }
});

// POST /api/ai/test-key (Superadmin test Gemini API Key)
router.post('/test-key', requireSuperAdmin, async (req, res) => {
  try {
    const { apiKey } = req.body;
    const keyToTest = apiKey || (db.getSettings() || {}).geminiApiKey;
    if (!keyToTest) {
      return res.status(400).json({ success: false, message: 'Please provide a Gemini API Key to test.' });
    }

    const testReply = await aiService.callGemini(
      keyToTest,
      'You are a testing assistant.',
      'Respond with exactly: "Dalal AI Connection Successful!"'
    );

    if (testReply) {
      res.json({
        success: true,
        message: 'Google Gemini API connection test passed successfully!',
        sampleResponse: testReply.trim()
      });
    } else {
      res.status(400).json({
        success: false,
        message: 'No response received from Gemini API. Please verify the key.'
      });
    }
  } catch (err) {
    res.status(400).json({
      success: false,
      message: 'Gemini API Key test failed: ' + err.message
    });
  }
});

module.exports = router;
