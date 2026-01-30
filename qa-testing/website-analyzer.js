#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════════════════════════════
 * SAILS.TO WEBSITE MULTI-AGENT ANALYZER
 * ═══════════════════════════════════════════════════════════════════════════════════════
 * 
 * Production-ready QA suite for the Sails.to CrossSecurities platform website.
 * 
 * TWO AI AGENTS:
 * 🎯 UX AGENT - User experience, messaging clarity, conversion optimization
 * 🎨 UI AGENT - Visual design, consistency, responsive layout
 * 
 * SITE STRUCTURE:
 * - Landing pages (Issuers, Investors, Brokers, Institutions)
 * - Core pages (Pricing, How It Works, Security, Compliance, Oversight)
 * - Knowledge base (Glossary, Docs, Guides, Blog, FAQ)
 * - Company (About, Contact, Legal)
 * - Conversion (Signup, Issuers Directory)
 * 
 * Model: DeepSeek R1T2 Chimera via OpenRouter (configurable)
 * ═══════════════════════════════════════════════════════════════════════════════════════
 */

import { chromium } from 'playwright';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ═══════════════════════════════════════════════════════════════════════════════════════
// SITE MAP - ALL SAILS.TO PAGES CATEGORIZED
// ═══════════════════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════════════════
// SITE OVERVIEW - SHARED CONTEXT FOR ALL AGENTS
// ═══════════════════════════════════════════════════════════════════════════════════════

const SITE_OVERVIEW = `
## SAILS.TO PLATFORM OVERVIEW

Sails.to is a CrossSecurities platform enabling companies to issue regulated security tokens
(tokenized bonds, equity, revenue share agreements) using Wyoming DAO LLC legal structures
with Solana blockchain infrastructure and TradFi integration via Clearstream for ISINs.

### TARGET AUDIENCES:
1. **Issuers** - Companies raising capital ($1M-$50M via bonds/securities)
2. **Investors** - Professional & accredited investors (high net worth individuals)
3. **Brokers** - Licensed securities dealers seeking digital asset offerings
4. **Institutions** - Trust companies, VCs, MFOs, family offices
5. **Introducers** - Referral partners earning commissions

### KEY VALUE PROPOSITIONS:
- Regulatory compliance (Wyoming DAO LLC + SEC Reg D/S frameworks)
- TradFi bridge (ISIN numbers, Clearstream settlement)
- Lower costs vs traditional securities issuance
- Self-custody hybrid model (investors control their own tokens)
- Secondary trading capability via compliant ATS partnerships

### SITE STRUCTURE:
- **Landing Pages**: Audience-specific (Issuers, Investors, Brokers, Institutions, Introducers)
- **Core Pages**: Pricing, How It Works, Signup, Issuers Directory
- **Trust Pages**: Security, Compliance, Oversight
- **Company**: About, Contact, Legal
- **Knowledge Base**: FAQ, Roadmap, Blog, Glossary, Docs, Guides

### BRAND VOICE:
- Professional financial services (not crypto-bro)
- Authoritative but accessible
- Trust-building through transparency
- Technical accuracy with plain-language explanations
`;

// ═══════════════════════════════════════════════════════════════════════════════════════
// SITE MAP - ALL SAILS.TO PAGES CATEGORIZED BY PRIORITY
// ═══════════════════════════════════════════════════════════════════════════════════════

const SITE_MAP = {
  // TIER 1: Critical conversion pages - highest traffic & revenue impact
  critical: [
    { path: '/', name: 'Homepage', desc: 'Main landing - must convert visitors to leads, establish credibility in 5 seconds' },
    { path: '/issuers/', name: 'For Issuers', desc: 'Primary audience - companies wanting to raise capital via tokenized securities' },
    { path: '/investors/', name: 'For Investors', desc: 'Investor audience - accredited/professional investors seeking opportunities' },
    { path: '/pricing/', name: 'Pricing', desc: 'Revenue page - must be crystal clear on costs vs. value' },
    { path: '/signup/', name: 'Signup', desc: 'Conversion endpoint - minimize friction, maximize trust signals' },
  ],
  
  // TIER 2: High-value pages - key audience segments & product understanding
  high: [
    { path: '/brokers/', name: 'For Brokers', desc: 'Licensed securities dealers - partnership/white-label opportunity' },
    { path: '/regulated/', name: 'For Institutions', desc: 'Trust companies, VCs, MFOs - institutional-grade compliance messaging' },
    { path: '/introducers/', name: 'For Introducers', desc: 'Referral partners - commission structure & easy onboarding' },
    { path: '/whatsails/', name: 'How It Works', desc: 'Deep-dive explainer - builds understanding and trust' },
    { path: '/issuers-directory/', name: 'Issuers Directory', desc: 'Live offerings showcase - social proof & discovery' },
  ],
  
  // TIER 3: Trust & credibility pages - essential for regulated finance
  trust: [
    { path: '/security/', name: 'Security', desc: 'Infrastructure security - SOC2, encryption, custody model' },
    { path: '/compliance/', name: 'Compliance', desc: 'Regulatory framework - SEC, Wyoming DAO, KYC/AML' },
    { path: '/oversight/', name: 'Oversight', desc: 'Governance, monitoring, audit trails' },
    { path: '/company/', name: 'Company Index', desc: 'Company section hub' },
    { path: '/company/about/', name: 'About Us', desc: 'Team, mission, company credibility' },
    { path: '/company/contact/', name: 'Contact', desc: 'Accessibility signal - multiple contact methods' },
    { path: '/company/legal/', name: 'Legal', desc: 'Terms, privacy, legal disclosures' },
  ],
  
  // TIER 4: Knowledge base - educational content & SEO
  knowledge: [
    { path: '/knowledge/', name: 'Knowledge Hub', desc: 'Central resource hub - navigation to all educational content' },
    { path: '/knowledge/faq/', name: 'FAQ', desc: 'Common questions - reduces support burden, builds confidence' },
    { path: '/knowledge/roadmap/', name: 'Roadmap', desc: 'Product direction transparency - shows commitment' },
    { path: '/knowledge/glossary/', name: 'Glossary Index', desc: 'Securities/crypto term definitions hub' },
    { path: '/knowledge/blog/', name: 'Blog Index', desc: 'Content marketing hub - thought leadership' },
    { path: '/knowledge/docs/', name: 'Docs Index', desc: 'Technical documentation for integration partners' },
    { path: '/knowledge/guides/', name: 'Guides Index', desc: 'Step-by-step tutorials' },
    { path: '/knowledge/guides/getting-started/', name: 'Getting Started Guide', desc: 'Onboarding tutorial for new users' },
  ],
  
  // TIER 5: Key content samples - spot check quality of dynamic content
  samples: [
    // Core glossary terms
    { path: '/knowledge/glossary/crosssecurities/', name: 'Glossary: CrossSecurities', desc: 'Core product term - must be clear' },
    { path: '/knowledge/glossary/tokenization/', name: 'Glossary: Tokenization', desc: 'Fundamental concept explanation' },
    { path: '/knowledge/glossary/wyoming-dao-llc/', name: 'Glossary: Wyoming DAO LLC', desc: 'Legal structure explanation' },
    { path: '/knowledge/glossary/security-token/', name: 'Glossary: Security Token', desc: 'Core product definition' },
    { path: '/knowledge/glossary/isin/', name: 'Glossary: ISIN', desc: 'TradFi bridge concept' },
    { path: '/knowledge/glossary/reg-d/', name: 'Glossary: Reg D', desc: 'Regulatory framework term' },
    // Key blog posts
    { path: '/knowledge/blog/security-tokens-explained/', name: 'Blog: Security Tokens', desc: 'Educational pillar content' },
    { path: '/knowledge/blog/why-wyoming/', name: 'Blog: Why Wyoming', desc: 'Legal structure rationale' },
    { path: '/knowledge/blog/future-of-tokenized-securities/', name: 'Blog: Future of Tokenization', desc: 'Thought leadership' },
    // Key docs
    { path: '/knowledge/docs/platform-overview/', name: 'Docs: Platform Overview', desc: 'Technical architecture intro' },
    { path: '/knowledge/docs/getting-started/', name: 'Docs: Getting Started', desc: 'Developer onboarding' },
  ],
  
  // TIER 6: Extended content - comprehensive audit (use with --all flag)
  extended: [
    // Additional glossary terms
    { path: '/knowledge/glossary/accredited-investor/', name: 'Glossary: Accredited Investor', desc: 'Investor qualification' },
    { path: '/knowledge/glossary/aml/', name: 'Glossary: AML', desc: 'Anti-money laundering' },
    { path: '/knowledge/glossary/kyc/', name: 'Glossary: KYC', desc: 'Know Your Customer' },
    { path: '/knowledge/glossary/spv/', name: 'Glossary: SPV', desc: 'Special Purpose Vehicle' },
    { path: '/knowledge/glossary/custody/', name: 'Glossary: Custody', desc: 'Asset custody model' },
    { path: '/knowledge/glossary/solana/', name: 'Glossary: Solana', desc: 'Blockchain infrastructure' },
    { path: '/knowledge/glossary/tradfi-bridge/', name: 'Glossary: TradFi Bridge', desc: 'Traditional finance integration' },
    // Additional blog posts
    { path: '/knowledge/blog/hybrid-custody-explained/', name: 'Blog: Hybrid Custody', desc: 'Custody model explanation' },
    { path: '/knowledge/blog/institutional-adoption/', name: 'Blog: Institutional Adoption', desc: 'Market trends' },
    { path: '/knowledge/blog/kyc-compliance-guide/', name: 'Blog: KYC Guide', desc: 'Compliance process' },
    { path: '/knowledge/blog/real-estate-tokenization/', name: 'Blog: Real Estate Tokenization', desc: 'Use case example' },
    { path: '/knowledge/blog/solana-for-securities/', name: 'Blog: Solana for Securities', desc: 'Technology rationale' },
    // Additional docs
    { path: '/knowledge/docs/api-reference/', name: 'Docs: API Reference', desc: 'Technical API documentation' },
    { path: '/knowledge/docs/compliance-framework/', name: 'Docs: Compliance Framework', desc: 'Regulatory integration' },
    { path: '/knowledge/docs/kyc-integration/', name: 'Docs: KYC Integration', desc: 'KYC API documentation' },
    { path: '/knowledge/docs/token-standard/', name: 'Docs: Token Standard', desc: 'CrossSecurities token spec' },
    // Additional guides
    { path: '/knowledge/guides/tokenization-101/', name: 'Guide: Tokenization 101', desc: 'Beginner tutorial' },
    { path: '/knowledge/guides/investor-eligibility/', name: 'Guide: Investor Eligibility', desc: 'Qualification requirements' },
    { path: '/knowledge/guides/wyoming-dao-explained/', name: 'Guide: Wyoming DAO', desc: 'Legal structure guide' },
  ]
};

// ═══════════════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════════════

const CONFIG = {
  // API
  openRouterApiKey: process.env.OPENROUTER_API_KEY || '',
  model: process.env.OPENROUTER_MODEL || 'deepseek/deepseek-r1t2-chimera',
  
  // Site
  baseUrl: process.env.BASE_URL || 'http://localhost:1313',
  
  // What to test (CLI args or default to critical + high)
  testTiers: process.argv.includes('--all') 
    ? ['critical', 'high', 'trust', 'knowledge', 'samples', 'extended']
    : process.argv.includes('--full')
      ? ['critical', 'high', 'trust', 'knowledge', 'samples']
      : process.argv.includes('--quick')
        ? ['critical']
        : ['critical', 'high'],
  
  // Output
  outputDir: path.join(__dirname, 'screenshots', 'website-analysis'),
  reportFile: path.join(__dirname, 'WEBSITE_ANALYSIS_REPORT.md'),
  jsonFile: path.join(__dirname, 'website-analysis.json'),
  
  // Timing
  pageLoadTimeout: 30000,
  waitAfterLoad: 800,
  
  // Viewports
  viewports: {
    desktop: { width: 1400, height: 900 },
    tablet: { width: 768, height: 1024 },
    mobile: { width: 390, height: 844 }
  },
  
  // Test mode
  headless: process.env.HEADLESS !== 'false',
  viewport: process.env.VIEWPORT || 'desktop'
};

// ═══════════════════════════════════════════════════════════════════════════════════════
// AGENT PROMPTS - SAILS.TO SPECIFIC WITH FULL SITE CONTEXT
// ═══════════════════════════════════════════════════════════════════════════════════════

const AGENT_PROMPTS = {
  ux: {
    name: 'UX Agent',
    emoji: '🎯',
    systemPrompt: `You are a SENIOR UX EXPERT reviewing Sails.to - a platform for issuing tokenized securities (CrossSecurities).

${SITE_OVERVIEW}

## YOUR ROLE
You are analyzing ONE PAGE within the context of this larger site. Consider how this page fits into the overall user journey and information architecture.

## TARGET AUDIENCE: Sophisticated but not necessarily crypto-native users
- Issuers: Companies wanting to raise capital via bonds/securities (CFOs, founders)
- Investors: Professional/accredited investors (high net worth individuals, family offices)
- Brokers: Licensed securities dealers seeking digital asset offerings
- Institutions: Trust companies, VCs, MFOs seeking compliant tokenization

## CRITICAL UX PRINCIPLES FOR FINANCIAL PLATFORMS

### 1. TRUST & CREDIBILITY (Most Important for Finance)
- Does the page feel legitimate and professional?
- Are there appropriate trust signals (regulated, audited, established)?
- Is the tone authoritative but accessible?
- Would a CFO/compliance officer feel comfortable?
- Does it avoid crypto/meme coin aesthetics?

### 2. CLARITY OF VALUE PROPOSITION
- Within 5 seconds, can a visitor understand what this page offers?
- Is the benefit clear before features are listed?
- Is financial/legal jargon explained when used?
- Are complex concepts broken down appropriately for the audience?

### 3. NAVIGATION & INFORMATION ARCHITECTURE
- Can users find what they need quickly?
- Is the navigation logical for the audience?
- Are related pages linked appropriately?
- Is the content hierarchy sensible?
- Are there clear pathways to conversion?

### 4. CONVERSION PATH
- Is the next step obvious on every page?
- Are CTAs clear, specific, and compelling?
- Is friction minimized (forms, steps, confusion)?
- Is there a logical funnel (learn → trust → convert)?
- Does the page guide users toward signup/contact?

### 5. MOBILE EXPERIENCE
- Does the page work well on phone/tablet?
- Are touch targets adequate (min 44px)?
- Is content readable without zooming?
- Does navigation work on mobile?

## SCORING RUBRIC
- 9-10: Exceptional - Clear, trustworthy, would convert skeptical finance professional
- 7-8: Good - Works well, minor polish needed
- 5-6: Adequate - Gets the job done but not compelling
- 3-4: Needs Work - Confusing or unprofessional elements
- 1-2: Poor - Would erode trust or confuse visitors

RESPOND WITH JSON ONLY:
{
  "score": <1-10>,
  "headline": "<one compelling sentence summary>",
  "trustScore": <1-10>,
  "clarityScore": <1-10>,
  "conversionScore": <1-10>,
  "strengths": ["<strength 1>", "<strength 2>"],
  "issues": [
    {"severity": "high|medium|low", "issue": "<description>", "fix": "<specific suggestion>"}
  ],
  "quickWins": ["<easy fix 1>", "<easy fix 2>"]
}`
  },
  
  ui: {
    name: 'UI Agent',
    emoji: '🎨',
    systemPrompt: `You are a SENIOR UI DESIGNER reviewing Sails.to - a financial services platform for tokenized securities.

${SITE_OVERVIEW}

## YOUR ROLE
You are analyzing ONE PAGE within the context of this larger site. Consider visual consistency with the overall brand and design system.

## BRAND CONTEXT:
- Professional financial services aesthetic (think Bloomberg, Carta, AngelList)
- Modern but not flashy (NOT a crypto meme site)
- Trust-building design language
- Primary audience: CFOs, investors, compliance officers
- Color palette: Deep purples, professional blues, clean whites
- Typography: Clean, readable, professional sans-serif

## VISUAL DESIGN CRITERIA

### 1. VISUAL HIERARCHY
- Does the most important content stand out?
- Are headings properly weighted (H1 > H2 > H3)?
- Is there clear distinction between sections?
- Do the eyes flow naturally down the page?
- Are CTAs visually prominent?

### 2. CONSISTENCY (Critical for Trust)
- Are colors consistent with brand (purples, blues)?
- Are fonts consistent throughout?
- Do similar elements look similar?
- Are spacings predictable and rhythmic?
- Does this page match other pages on the site?

### 3. PROFESSIONAL POLISH
- Does this look like a legitimate financial platform?
- Are there any amateur design tells (bad alignment, inconsistent spacing)?
- Is imagery appropriate and high quality?
- Do icons and illustrations fit the brand?
- Are there any visual bugs or glitches?

### 4. WHITESPACE & BREATHING ROOM
- Is content crowded or well-spaced?
- Do sections have clear boundaries?
- Is text readable with good line height?
- Is there sufficient padding around elements?

### 5. RESPONSIVE QUALITY
- Does the layout adapt gracefully?
- Are elements properly sized for the viewport?
- Do cards/grids reorganize sensibly?
- No horizontal scrolling?

### 6. INTERACTIVE ELEMENTS
- Are buttons clearly buttons (not flat text)?
- Are links distinguishable from regular text?
- Are hover states appropriate?
- Are forms well-designed with clear labels?

## SCORING RUBRIC
- 9-10: Polished - Production-ready, would impress institutional clients
- 7-8: Good - Professional, minor refinements possible
- 5-6: Adequate - Functional but needs design attention
- 3-4: Rough - Inconsistent or unprofessional
- 1-2: Poor - Would undermine credibility

RESPOND WITH JSON ONLY:
{
  "score": <1-10>,
  "headline": "<one sentence design assessment>",
  "hierarchyScore": <1-10>,
  "consistencyScore": <1-10>,
  "polishScore": <1-10>,
  "strengths": ["<design strength 1>", "<design strength 2>"],
  "issues": [
    {"severity": "high|medium|low", "issue": "<design problem>", "fix": "<specific CSS/design fix>"}
  ],
  "quickWins": ["<easy design fix 1>", "<easy design fix 2>"]
}`
  }
};

// ═══════════════════════════════════════════════════════════════════════════════════════
// LOGGING
// ═══════════════════════════════════════════════════════════════════════════════════════

const LOG = {
  banner: () => console.log(`
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🚀  SAILS.TO WEBSITE ANALYZER                                               ║
║                                                                               ║
║   Multi-Agent UX/UI Analysis Suite                                            ║
║   Model: ${CONFIG.model.padEnd(45)}║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
`),
  header: (msg) => console.log(`\n${'═'.repeat(75)}\n  ${msg}\n${'═'.repeat(75)}`),
  tier: (name) => console.log(`\n${'─'.repeat(60)}\n  📂 TIER: ${name.toUpperCase()}\n${'─'.repeat(60)}`),
  page: (name, path) => console.log(`\n  📄 ${name} (${path})`),
  info: (msg) => console.log(`     ${msg}`),
  score: (agent, score, headline) => console.log(`     ${agent} Score: ${score}/10 - ${headline}`),
  success: (msg) => console.log(`     ✅ ${msg}`),
  warn: (msg) => console.log(`     ⚠️  ${msg}`),
  error: (msg) => console.log(`     ❌ ${msg}`),
  done: () => console.log(`\n${'═'.repeat(75)}\n  ✨ ANALYSIS COMPLETE\n${'═'.repeat(75)}\n`)
};

// ═══════════════════════════════════════════════════════════════════════════════════════
// AI CLIENT
// ═══════════════════════════════════════════════════════════════════════════════════════

class AIClient {
  constructor() {
    this.apiKey = CONFIG.openRouterApiKey;
    this.model = CONFIG.model;
    this.enabled = !!this.apiKey;
    this.requestCount = 0;
  }
  
  async analyze(systemPrompt, pageContext) {
    if (!this.enabled) {
      return { score: 'N/A', headline: 'Set OPENROUTER_API_KEY in .env', strengths: [], issues: [], quickWins: [] };
    }
    
    this.requestCount++;
    
    try {
      const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
          'HTTP-Referer': 'https://sails.to',
          'X-Title': 'Sails.to QA Analyzer'
        },
        body: JSON.stringify({
          model: this.model,
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: `Analyze this page and respond with JSON only:\n\n${pageContext}` }
          ],
          temperature: 0.2,
          max_tokens: 1500
        })
      });
      
      if (!response.ok) {
        const err = await response.text();
        throw new Error(`API ${response.status}: ${err.substring(0, 200)}`);
      }
      
      const data = await response.json();
      const content = data.choices[0]?.message?.content || '';
      
      // Extract JSON
      const jsonMatch = content.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      
      return { score: 5, headline: 'Could not parse AI response', raw: content.substring(0, 500) };
      
    } catch (error) {
      LOG.error(`AI: ${error.message}`);
      return { score: 'ERR', headline: error.message.substring(0, 80), strengths: [], issues: [], quickWins: [] };
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════════════
// WEBSITE ANALYZER
// ═══════════════════════════════════════════════════════════════════════════════════════

class WebsiteAnalyzer {
  constructor() {
    this.browser = null;
    this.page = null;
    this.ai = new AIClient();
    this.results = [];
    this.startTime = Date.now();
  }
  
  async init() {
    LOG.banner();
    LOG.info(`Base URL: ${CONFIG.baseUrl}`);
    LOG.info(`Tiers: ${CONFIG.testTiers.join(', ')}`);
    LOG.info(`Viewport: ${CONFIG.viewport}`);
    LOG.info(`AI Enabled: ${this.ai.enabled ? 'Yes' : 'No (set OPENROUTER_API_KEY)'}`);
    
    await fs.mkdir(CONFIG.outputDir, { recursive: true });
    
    this.browser = await chromium.launch({ headless: CONFIG.headless });
    this.context = await this.browser.newContext({
      viewport: CONFIG.viewports[CONFIG.viewport] || CONFIG.viewports.desktop
    });
    this.page = await this.context.newPage();
  }
  
  async screenshot(name) {
    const safeName = name.replace(/[^a-z0-9-]/gi, '_').toLowerCase();
    const filepath = path.join(CONFIG.outputDir, `${safeName}.png`);
    await this.page.screenshot({ path: filepath, fullPage: true });
    return filepath;
  }
  
  async extractPageData() {
    return await this.page.evaluate(() => {
      const $ = (sel) => document.querySelector(sel);
      const $$ = (sel) => Array.from(document.querySelectorAll(sel));
      const text = (sel) => $(sel)?.textContent?.trim() || '';
      const texts = (sel) => $$(sel).map(el => el.textContent.trim()).filter(Boolean);
      
      return {
        title: document.title,
        url: window.location.href,
        h1: text('h1'),
        heroText: text('.page-hero, .hero, [class*="hero"]'),
        h2s: texts('h2').slice(0, 8),
        h3s: texts('h3').slice(0, 6),
        navItems: texts('nav a, header a').slice(0, 12),
        footerLinks: texts('footer a').slice(0, 10),
        buttons: texts('button, .btn, [class*="btn"]').slice(0, 8),
        links: texts('main a, article a').slice(0, 10),
        forms: $('form') ? 'Yes' : 'No',
        images: $$('img').length,
        cards: $$('[class*="card"], [class*="feature"]').length,
        bodyPreview: document.body?.innerText?.substring(0, 2500) || ''
      };
    });
  }
  
  formatPageContext(data, pageInfo) {
    return `
═══════════════════════════════════════════════════════════════════════════
PAGE: ${pageInfo.name}
URL: ${data.url}
PURPOSE: ${pageInfo.desc}
═══════════════════════════════════════════════════════════════════════════

TITLE: ${data.title}
H1: ${data.h1}
HERO TEXT: ${data.heroText}

HEADINGS (H2): ${data.h2s.join(' | ')}
HEADINGS (H3): ${data.h3s.join(' | ')}

NAVIGATION: ${data.navItems.join(' | ')}
BUTTONS/CTAs: ${data.buttons.join(' | ')}
LINKS IN CONTENT: ${data.links.join(' | ')}

STRUCTURE:
- Images: ${data.images}
- Cards/Features: ${data.cards}
- Has Form: ${data.forms}

BODY CONTENT (Preview):
${data.bodyPreview}
═══════════════════════════════════════════════════════════════════════════`;
  }
  
  async analyzePage(pageInfo, tierName) {
    const url = `${CONFIG.baseUrl}${pageInfo.path}`;
    LOG.page(pageInfo.name, pageInfo.path);
    
    try {
      // Load page
      await this.page.goto(url, { waitUntil: 'networkidle', timeout: CONFIG.pageLoadTimeout });
      await this.page.waitForTimeout(CONFIG.waitAfterLoad);
      
      // Screenshot
      const screenshotPath = await this.screenshot(pageInfo.name);
      LOG.info(`📸 Screenshot saved`);
      
      // Extract data
      const pageData = await this.extractPageData();
      const pageContext = this.formatPageContext(pageData, pageInfo);
      
      // Run AI agents
      LOG.info(`🎯 UX Agent analyzing...`);
      const uxResult = await this.ai.analyze(AGENT_PROMPTS.ux.systemPrompt, pageContext);
      LOG.score('🎯 UX', uxResult.score, uxResult.headline || '');
      
      LOG.info(`🎨 UI Agent analyzing...`);
      const uiResult = await this.ai.analyze(AGENT_PROMPTS.ui.systemPrompt, pageContext);
      LOG.score('🎨 UI', uiResult.score, uiResult.headline || '');
      
      // Calculate combined
      const uxScore = typeof uxResult.score === 'number' ? uxResult.score : 0;
      const uiScore = typeof uiResult.score === 'number' ? uiResult.score : 0;
      const combined = uxScore && uiScore ? ((uxScore + uiScore) / 2).toFixed(1) : 'N/A';
      
      return {
        tier: tierName,
        page: pageInfo.name,
        path: pageInfo.path,
        desc: pageInfo.desc,
        url,
        screenshot: screenshotPath,
        ux: uxResult,
        ui: uiResult,
        combined
      };
      
    } catch (error) {
      LOG.error(`Failed: ${error.message}`);
      return {
        tier: tierName,
        page: pageInfo.name,
        path: pageInfo.path,
        error: error.message
      };
    }
  }
  
  async run() {
    await this.init();
    
    // Process each tier
    for (const tierName of CONFIG.testTiers) {
      const pages = SITE_MAP[tierName];
      if (!pages) continue;
      
      LOG.tier(tierName);
      
      for (const pageInfo of pages) {
        const result = await this.analyzePage(pageInfo, tierName);
        this.results.push(result);
      }
    }
    
    // Generate reports
    await this.generateMarkdownReport();
    await this.generateJsonReport();
    
    // Cleanup
    await this.browser.close();
    
    LOG.done();
    LOG.info(`Report: ${CONFIG.reportFile}`);
    LOG.info(`JSON: ${CONFIG.jsonFile}`);
    LOG.info(`Screenshots: ${CONFIG.outputDir}`);
    LOG.info(`Total API calls: ${this.ai.requestCount}`);
    LOG.info(`Duration: ${((Date.now() - this.startTime) / 1000).toFixed(1)}s`);
  }
  
  async generateMarkdownReport() {
    const timestamp = new Date().toISOString();
    const duration = ((Date.now() - this.startTime) / 1000).toFixed(1);
    
    let md = `# 🚀 Sails.to Website Analysis Report

**Generated:** ${timestamp}  
**Model:** ${CONFIG.model}  
**Duration:** ${duration}s  
**Pages Analyzed:** ${this.results.length}  
**Tiers:** ${CONFIG.testTiers.join(', ')}

---

## 📊 Summary Scores

| Tier | Page | UX | UI | Combined |
|------|------|----|----|----------|
`;
    
    for (const r of this.results) {
      if (r.error) {
        md += `| ${r.tier} | ${r.page} | ❌ | ❌ | Error |\n`;
      } else {
        const uxScore = r.ux?.score || 'N/A';
        const uiScore = r.ui?.score || 'N/A';
        md += `| ${r.tier} | [${r.page}](${r.path}) | ${uxScore} | ${uiScore} | **${r.combined}** |\n`;
      }
    }
    
    // High priority issues
    md += `\n---\n\n## 🚨 High Priority Issues\n\n`;
    
    let hasHighIssues = false;
    for (const r of this.results) {
      if (r.error) continue;
      
      const highIssues = [
        ...(r.ux?.issues || []).filter(i => i.severity === 'high').map(i => ({ ...i, agent: 'UX' })),
        ...(r.ui?.issues || []).filter(i => i.severity === 'high').map(i => ({ ...i, agent: 'UI' }))
      ];
      
      if (highIssues.length > 0) {
        hasHighIssues = true;
        md += `### ${r.page}\n\n`;
        for (const issue of highIssues) {
          md += `- **[${issue.agent}]** ${issue.issue}\n`;
          if (issue.fix) md += `  - 💡 Fix: ${issue.fix}\n`;
        }
        md += '\n';
      }
    }
    
    if (!hasHighIssues) {
      md += `No high-priority issues detected! 🎉\n\n`;
    }
    
    // Quick wins
    md += `---\n\n## ⚡ Quick Wins\n\n`;
    
    const allQuickWins = [];
    for (const r of this.results) {
      if (r.error) continue;
      const wins = [
        ...(r.ux?.quickWins || []).map(w => ({ page: r.page, win: w, agent: 'UX' })),
        ...(r.ui?.quickWins || []).map(w => ({ page: r.page, win: w, agent: 'UI' }))
      ];
      allQuickWins.push(...wins);
    }
    
    if (allQuickWins.length > 0) {
      for (const qw of allQuickWins.slice(0, 15)) {
        md += `- **${qw.page}** [${qw.agent}]: ${qw.win}\n`;
      }
    } else {
      md += `No quick wins identified.\n`;
    }
    
    // Detailed analysis per page
    md += `\n---\n\n## 📋 Detailed Analysis\n\n`;
    
    for (const r of this.results) {
      md += `### ${r.page}\n\n`;
      md += `**Path:** \`${r.path}\`  \n`;
      md += `**Purpose:** ${r.desc}  \n`;
      
      if (r.error) {
        md += `**Status:** ❌ Error - ${r.error}\n\n---\n\n`;
        continue;
      }
      
      md += `**Combined Score:** ${r.combined}/10\n\n`;
      
      // UX
      md += `#### 🎯 UX Analysis (${r.ux?.score || 'N/A'}/10)\n\n`;
      md += `> ${r.ux?.headline || 'No summary'}\n\n`;
      
      if (r.ux?.strengths?.length) {
        md += `**Strengths:**\n`;
        for (const s of r.ux.strengths) md += `- ✅ ${s}\n`;
        md += '\n';
      }
      
      if (r.ux?.issues?.length) {
        md += `**Issues:**\n`;
        for (const i of r.ux.issues) {
          md += `- [${(i.severity || 'medium').toUpperCase()}] ${i.issue}\n`;
          if (i.fix) md += `  - 💡 ${i.fix}\n`;
        }
        md += '\n';
      }
      
      // UI
      md += `#### 🎨 UI Analysis (${r.ui?.score || 'N/A'}/10)\n\n`;
      md += `> ${r.ui?.headline || 'No summary'}\n\n`;
      
      if (r.ui?.strengths?.length) {
        md += `**Strengths:**\n`;
        for (const s of r.ui.strengths) md += `- ✅ ${s}\n`;
        md += '\n';
      }
      
      if (r.ui?.issues?.length) {
        md += `**Issues:**\n`;
        for (const i of r.ui.issues) {
          md += `- [${(i.severity || 'medium').toUpperCase()}] ${i.issue}\n`;
          if (i.fix) md += `  - 💡 ${i.fix}\n`;
        }
        md += '\n';
      }
      
      md += `---\n\n`;
    }
    
    await fs.writeFile(CONFIG.reportFile, md);
  }
  
  async generateJsonReport() {
    const report = {
      meta: {
        generated: new Date().toISOString(),
        model: CONFIG.model,
        baseUrl: CONFIG.baseUrl,
        tiers: CONFIG.testTiers,
        totalPages: this.results.length,
        apiCalls: this.ai.requestCount
      },
      summary: {
        avgUxScore: this.calcAvg(this.results, r => r.ux?.score),
        avgUiScore: this.calcAvg(this.results, r => r.ui?.score),
        avgCombined: this.calcAvg(this.results, r => parseFloat(r.combined)),
        highIssueCount: this.results.reduce((acc, r) => {
          const uxHigh = (r.ux?.issues || []).filter(i => i.severity === 'high').length;
          const uiHigh = (r.ui?.issues || []).filter(i => i.severity === 'high').length;
          return acc + uxHigh + uiHigh;
        }, 0)
      },
      pages: this.results
    };
    
    await fs.writeFile(CONFIG.jsonFile, JSON.stringify(report, null, 2));
  }
  
  calcAvg(arr, fn) {
    const values = arr.map(fn).filter(v => typeof v === 'number' && !isNaN(v));
    if (values.length === 0) return 'N/A';
    return (values.reduce((a, b) => a + b, 0) / values.length).toFixed(1);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════════════
// CLI HELP
// ═══════════════════════════════════════════════════════════════════════════════════════

if (process.argv.includes('--help') || process.argv.includes('-h')) {
  console.log(`
Sails.to Website Analyzer

Usage: node website-analyzer.js [options]

Options:
  --quick     Only test critical pages (5 pages)
  --full      Test critical + high + trust + knowledge (20+ pages)
  --all       Test everything including samples (25+ pages)
  --help      Show this help

Environment:
  OPENROUTER_API_KEY   Required for AI analysis
  OPENROUTER_MODEL     Model to use (default: deepseek/deepseek-r1t2-chimera)
  BASE_URL             Site URL (default: http://localhost:1313)
  HEADLESS             Set to 'false' to see browser
  VIEWPORT             'desktop', 'tablet', or 'mobile'

Examples:
  npm run analyze              # Default (critical + high tiers)
  npm run analyze -- --quick   # Quick check (critical only)
  npm run analyze -- --full    # Comprehensive test
  VIEWPORT=mobile npm run analyze -- --quick   # Mobile quick test
`);
  process.exit(0);
}

// ═══════════════════════════════════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════════════════════════════════

const analyzer = new WebsiteAnalyzer();
analyzer.run().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
