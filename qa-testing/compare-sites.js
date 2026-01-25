#!/usr/bin/env node
/**
 * Sails.to Site Comparison Tool
 * Compares pre-Hugo (drafts) site with Hugo-built site page by page
 * Uses AI vision models for section-by-section analysis
 */

import { chromium } from 'playwright';
import fs from 'fs/promises';
import path from 'path';
import sharp from 'sharp';

// Configuration
const CONFIG = {
  // Pre-Hugo site (static files from drafts folder)
  originalDir: path.resolve('../drafts'),
  originalPort: 8080,
  
  // Hugo site
  hugoDir: path.resolve('../hugo-site/public'),
  hugoPort: 1313,
  
  outputDir: './screenshots/comparison',
  reportsDir: './screenshots/reports',
  
  viewports: {
    desktop: { width: 1920, height: 1080, name: 'desktop' },
    mobile: { width: 375, height: 812, name: 'mobile' }
  },
  
  // Page mapping: original path -> hugo path
  // Full coverage of all matching pages between drafts and hugo
  pageMapping: [
    // Main pages
    { original: '/index.html', hugo: '/', name: 'home', priority: 'critical' },
    { original: '/issuers.html', hugo: '/issuers/', name: 'issuers', priority: 'critical' },
    { original: '/investors.html', hugo: '/investors/', name: 'investors', priority: 'critical' },
    { original: '/brokers.html', hugo: '/brokers/', name: 'brokers', priority: 'critical' },
    { original: '/introducers.html', hugo: '/introducers/', name: 'introducers', priority: 'high' },
    { original: '/regulated.html', hugo: '/regulated/', name: 'regulated', priority: 'high' },
    { original: '/issuers-directory.html', hugo: '/issuers-directory/', name: 'issuers-directory', priority: 'high' },
    { original: '/whatsails.html', hugo: '/whatsails/', name: 'whatsails', priority: 'critical' },
    { original: '/pricing.html', hugo: '/pricing/', name: 'pricing', priority: 'critical' },
    { original: '/signup.html', hugo: '/signup/', name: 'signup', priority: 'critical' },
    
    // Company pages
    { original: '/company/about.html', hugo: '/company/about/', name: 'company-about', priority: 'high' },
    { original: '/company/contact.html', hugo: '/company/contact/', name: 'company-contact', priority: 'high' },
    { original: '/company/legal.html', hugo: '/company/legal/', name: 'company-legal', priority: 'high' },
    
    // Knowledge hub
    { original: '/knowledge/index.html', hugo: '/knowledge/', name: 'knowledge-index', priority: 'medium' },
    { original: '/knowledge/faq.html', hugo: '/knowledge/faq/', name: 'knowledge-faq', priority: 'high' },
    { original: '/knowledge/roadmap.html', hugo: '/knowledge/roadmap/', name: 'knowledge-roadmap', priority: 'medium' },
    
    // Blog
    { original: '/knowledge/blog/index.html', hugo: '/knowledge/blog/', name: 'blog-index', priority: 'medium' },
    { original: '/knowledge/blog/security-tokens-explained.html', hugo: '/knowledge/blog/security-tokens-explained/', name: 'blog-security-tokens', priority: 'low' },
    { original: '/knowledge/blog/why-wyoming.html', hugo: '/knowledge/blog/why-wyoming/', name: 'blog-why-wyoming', priority: 'low' },
    { original: '/knowledge/blog/future-of-tokenized-securities.html', hugo: '/knowledge/blog/future-of-tokenized-securities/', name: 'blog-future-tokenized', priority: 'low' },
    
    // Glossary
    { original: '/knowledge/glossary/index.html', hugo: '/knowledge/glossary/', name: 'glossary-index', priority: 'medium' },
    { original: '/knowledge/glossary/security-token.html', hugo: '/knowledge/glossary/security-token/', name: 'glossary-security-token', priority: 'low' },
    { original: '/knowledge/glossary/kyc.html', hugo: '/knowledge/glossary/kyc/', name: 'glossary-kyc', priority: 'low' },
    { original: '/knowledge/glossary/isin.html', hugo: '/knowledge/glossary/isin/', name: 'glossary-isin', priority: 'low' },
    
    // Docs
    { original: '/knowledge/docs/index.html', hugo: '/knowledge/docs/', name: 'docs-index', priority: 'medium' },
    
    // Guides
    { original: '/knowledge/guides/getting-started.html', hugo: '/knowledge/guides/getting-started/', name: 'guides-getting-started', priority: 'medium' },
    { original: '/knowledge/guides/wyoming-dao-explained.html', hugo: '/knowledge/guides/wyoming-dao-explained/', name: 'guides-wyoming-dao', priority: 'low' }
  ],
  
  // Scroll positions for full page comparison
  scrollPositions: ['top', '50%', 'bottom'],
  
  // OpenRouter config - using more powerful models
  openrouterApiKey: process.env.OPENROUTER_API_KEY || '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',
  
  // Model selection - best free vision model with good rate limits
  models: {
    // Gemma 3 27B has vision and higher rate limits than Gemini
    best: 'google/gemma-3-27b-it:free'
  },
  
  // Which model tier to use
  modelTier: 'best'
};

const COMPARISON_PROMPT = `You are a QA engineer comparing two versions of the same webpage during a site migration.

LEFT SIDE: Original pre-migration site (source of truth)
RIGHT SIDE: New Hugo-built site (what we're testing)

Analyze these side-by-side screenshots and identify ALL differences:

## 1. CONTENT DIFFERENCES
- Missing text, headings, paragraphs
- Changed wording or copy
- Missing or added sections
- Different content order

## 2. VISUAL/STYLING DIFFERENCES  
- Font changes (family, size, weight)
- Color differences (text, backgrounds, accents)
- Spacing/padding/margin differences
- Border and shadow differences
- Button/link styling changes

## 3. LAYOUT DIFFERENCES
- Different grid/flex layouts
- Section ordering changes
- Width/alignment differences
- Missing or extra whitespace

## 4. MISSING ELEMENTS
- Icons, images, logos
- Navigation items
- Footer content
- Forms, buttons, CTAs

## 5. BROKEN ELEMENTS
- Raw HTML showing as text (code not rendering)
- Broken images
- Missing styles
- JavaScript not working

## 6. IMPROVEMENTS (if any)
- Things that look better in new version

Rate each issue severity: CRITICAL (blocks launch) | HIGH | MEDIUM | LOW

Respond with JSON:
{
  "pageName": "page name",
  "overallMatch": "percentage 0-100 of how similar they are",
  "launchReady": true/false,
  "issues": [
    {
      "category": "content|visual|layout|missing|broken|improvement",
      "severity": "critical|high|medium|low", 
      "description": "detailed description",
      "location": "where on page (e.g., 'hero section', 'footer', 'nav')",
      "original": "what it looks like in original (if applicable)",
      "hugo": "what it looks like in hugo version (if applicable)"
    }
  ],
  "summary": "Brief overall assessment"
}`;

let httpServers = [];

/**
 * Start static file server
 */
async function startServer(directory, port) {
  const { createServer } = await import('http');
  const { readFile, stat } = await import('fs/promises');
  const { extname, join } = await import('path');
  
  const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.webm': 'video/webm',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.eot': 'application/vnd.ms-fontobject'
  };
  
  const server = createServer(async (req, res) => {
    let filePath = join(directory, req.url === '/' ? 'index.html' : req.url);
    
    // Handle directory requests
    try {
      const stats = await stat(filePath);
      if (stats.isDirectory()) {
        filePath = join(filePath, 'index.html');
      }
    } catch {}
    
    try {
      const content = await readFile(filePath);
      const ext = extname(filePath).toLowerCase();
      res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
      res.end(content);
    } catch (e) {
      res.writeHead(404);
      res.end('Not Found');
    }
  });
  
  return new Promise((resolve, reject) => {
    server.listen(port, () => {
      console.log(`  📂 Serving ${directory} on port ${port}`);
      httpServers.push(server);
      resolve(server);
    });
    server.on('error', reject);
  });
}

/**
 * Setup directories
 */
async function setupDirectories() {
  await fs.mkdir(CONFIG.outputDir, { recursive: true });
  await fs.mkdir(path.join(CONFIG.outputDir, 'side-by-side'), { recursive: true });
  await fs.mkdir(path.join(CONFIG.outputDir, 'original'), { recursive: true });
  await fs.mkdir(path.join(CONFIG.outputDir, 'hugo'), { recursive: true });
  await fs.mkdir(CONFIG.reportsDir, { recursive: true });
}

/**
 * Scroll to position
 */
async function scrollToPosition(page, position) {
  await page.evaluate(async (pos) => {
    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
    let targetY = 0;
    switch (pos) {
      case 'top': targetY = 0; break;
      case '50%': targetY = scrollHeight * 0.5; break;
      case 'bottom': targetY = scrollHeight; break;
    }
    window.scrollTo({ top: targetY, behavior: 'instant' });
  }, position);
  await page.waitForTimeout(500);
}

/**
 * Capture full page screenshot
 */
async function captureFullPage(page, outputPath) {
  await page.screenshot({ path: outputPath, fullPage: true });
}

/**
 * Capture viewport screenshot
 */
async function captureViewport(page, outputPath) {
  await page.screenshot({ path: outputPath, fullPage: false });
}

/**
 * Create side-by-side comparison image
 */
async function createSideBySide(originalPath, hugoPath, outputPath, pageName) {
  const [originalImg, hugoImg] = await Promise.all([
    sharp(originalPath).metadata(),
    sharp(hugoPath).metadata()
  ]);
  
  const maxHeight = Math.max(originalImg.height, hugoImg.height);
  const totalWidth = originalImg.width + hugoImg.width + 20; // 20px gap
  
  // Create label
  const labelHeight = 40;
  const labelSvg = `
    <svg width="${totalWidth}" height="${labelHeight}">
      <rect width="100%" height="100%" fill="#1a1a1a"/>
      <text x="${originalImg.width / 2}" y="25" text-anchor="middle" fill="#C9A227" font-family="Arial" font-size="14" font-weight="bold">
        ORIGINAL (${pageName})
      </text>
      <text x="${originalImg.width + 10 + hugoImg.width / 2}" y="25" text-anchor="middle" fill="#22c55e" font-family="Arial" font-size="14" font-weight="bold">
        HUGO (${pageName})
      </text>
    </svg>
  `;
  
  // Extend images to same height
  const originalExtended = await sharp(originalPath)
    .extend({ bottom: maxHeight - originalImg.height, background: '#1a1a1a' })
    .toBuffer();
  
  const hugoExtended = await sharp(hugoPath)
    .extend({ bottom: maxHeight - hugoImg.height, background: '#1a1a1a' })
    .toBuffer();
  
  // Composite side by side
  await sharp({
    create: {
      width: totalWidth,
      height: maxHeight + labelHeight,
      channels: 4,
      background: '#1a1a1a'
    }
  })
    .composite([
      { input: Buffer.from(labelSvg), top: 0, left: 0 },
      { input: originalExtended, top: labelHeight, left: 0 },
      { input: hugoExtended, top: labelHeight, left: originalImg.width + 20 }
    ])
    .png()
    .toFile(outputPath);
  
  return { width: totalWidth, height: maxHeight + labelHeight };
}

/**
 * Call OpenRouter API with vision model - with retry logic
 */
async function callVisionModel(imageBase64, prompt, pageName, retries = 3) {
  const model = CONFIG.models[CONFIG.modelTier];
  console.log(`    🤖 Using model: ${model}`);
  
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${CONFIG.openrouterApiKey}`,
          'Content-Type': 'application/json',
          'HTTP-Referer': 'https://sails.to',
          'X-Title': 'Sails.to QA Comparison'
        },
        body: JSON.stringify({
          model: model,
          messages: [{
            role: 'user',
            content: [
              { type: 'text', text: `Page: ${pageName}\n\n${prompt}` },
              { type: 'image_url', image_url: { url: `data:image/png;base64,${imageBase64}` } }
            ]
          }],
          max_tokens: 4000,
          temperature: 0.2
        })
      });
      
      if (response.status === 429) {
        const waitTime = attempt * 10000; // 10s, 20s, 30s
        console.log(`    ⏳ Rate limited, waiting ${waitTime/1000}s (attempt ${attempt}/${retries})...`);
        await new Promise(r => setTimeout(r, waitTime));
        continue;
      }
      
      if (!response.ok) {
        const error = await response.text();
        throw new Error(`API error ${response.status}: ${error}`);
      }
      
      const data = await response.json();
      return data.choices[0]?.message?.content || '';
    } catch (e) {
      if (attempt === retries) throw e;
      console.log(`    ⚠️ Attempt ${attempt} failed, retrying...`);
      await new Promise(r => setTimeout(r, 5000));
    }
  }
}

/**
 * Parse AI response to JSON
 */
function parseResponse(response) {
  try {
    const match = response.match(/\{[\s\S]*\}/);
    if (match) return JSON.parse(match[0]);
  } catch (e) {
    console.log('    ⚠️ Failed to parse JSON, extracting manually');
  }
  return {
    pageName: 'unknown',
    overallMatch: 50,
    launchReady: false,
    issues: [{ category: 'other', severity: 'medium', description: response.substring(0, 1000) }],
    summary: 'Could not parse structured response',
    parseError: true
  };
}

/**
 * Main comparison flow
 */
async function runComparison() {
  console.log('🔄 Sails.to Site Comparison Tool');
  console.log('═'.repeat(60));
  console.log(`Comparing: Original (drafts) vs Hugo-built site`);
  console.log(`Model tier: ${CONFIG.modelTier} (${CONFIG.models[CONFIG.modelTier]})`);
  console.log('═'.repeat(60));
  
  await setupDirectories();
  
  // Start servers
  console.log('\n📡 Starting servers...');
  try {
    await startServer(CONFIG.originalDir, CONFIG.originalPort);
    await startServer(CONFIG.hugoDir, CONFIG.hugoPort);
  } catch (e) {
    console.error('❌ Failed to start servers:', e.message);
    process.exit(1);
  }
  
  const browser = await chromium.launch();
  const results = {
    timestamp: new Date().toISOString(),
    modelUsed: CONFIG.models[CONFIG.modelTier],
    pages: [],
    summary: {
      totalPages: 0,
      launchReady: 0,
      notReady: 0,
      criticalIssues: 0,
      highIssues: 0,
      averageMatch: 0
    }
  };
  
  let totalMatch = 0;
  
  console.log('\n📸 Capturing and comparing pages...\n');
  
  for (const pageMap of CONFIG.pageMapping) {
    console.log(`\n📄 ${pageMap.name}`);
    console.log(`   Original: ${pageMap.original}`);
    console.log(`   Hugo: ${pageMap.hugo}`);
    
    const context = await browser.newContext({
      viewport: CONFIG.viewports.desktop
    });
    
    try {
      // Capture original
      const originalPage = await context.newPage();
      await originalPage.goto(`http://localhost:${CONFIG.originalPort}${pageMap.original}`, {
        waitUntil: 'load',
        timeout: 15000
      });
      await originalPage.waitForTimeout(1500);
      
      const originalPath = path.join(CONFIG.outputDir, 'original', `${pageMap.name}.png`);
      await captureFullPage(originalPage, originalPath);
      console.log(`   ✓ Original captured`);
      
      // Capture Hugo
      const hugoPage = await context.newPage();
      await hugoPage.goto(`http://localhost:${CONFIG.hugoPort}${pageMap.hugo}`, {
        waitUntil: 'load',
        timeout: 15000
      });
      await hugoPage.waitForTimeout(1500);
      
      const hugoPath = path.join(CONFIG.outputDir, 'hugo', `${pageMap.name}.png`);
      await captureFullPage(hugoPage, hugoPath);
      console.log(`   ✓ Hugo captured`);
      
      // Create side-by-side
      const sideBySidePath = path.join(CONFIG.outputDir, 'side-by-side', `${pageMap.name}.png`);
      await createSideBySide(originalPath, hugoPath, sideBySidePath, pageMap.name);
      console.log(`   ✓ Side-by-side created`);
      
      // AI Analysis
      console.log(`   🔍 Analyzing differences...`);
      const imageBuffer = await fs.readFile(sideBySidePath);
      const base64 = imageBuffer.toString('base64');
      
      await new Promise(r => setTimeout(r, 8000)); // Rate limiting - 8s between requests
      
      const aiResponse = await callVisionModel(base64, COMPARISON_PROMPT, pageMap.name);
      const analysis = parseResponse(aiResponse);
      
      results.pages.push({
        name: pageMap.name,
        originalUrl: pageMap.original,
        hugoUrl: pageMap.hugo,
        screenshots: {
          original: originalPath,
          hugo: hugoPath,
          sideBySide: sideBySidePath
        },
        analysis
      });
      
      // Update summary
      results.summary.totalPages++;
      if (analysis.launchReady) {
        results.summary.launchReady++;
      } else {
        results.summary.notReady++;
      }
      
      const match = parseInt(analysis.overallMatch) || 50;
      totalMatch += match;
      
      if (analysis.issues) {
        results.summary.criticalIssues += analysis.issues.filter(i => i.severity === 'critical').length;
        results.summary.highIssues += analysis.issues.filter(i => i.severity === 'high').length;
      }
      
      console.log(`   📊 Match: ${analysis.overallMatch}% | Launch Ready: ${analysis.launchReady ? '✅' : '❌'}`);
      console.log(`   📝 Issues: ${analysis.issues?.length || 0} (${analysis.issues?.filter(i => i.severity === 'critical').length || 0} critical)`);
      
    } catch (e) {
      console.error(`   ❌ Error: ${e.message}`);
      results.pages.push({
        name: pageMap.name,
        error: e.message
      });
    }
    
    await context.close();
  }
  
  // Calculate average match
  results.summary.averageMatch = results.summary.totalPages > 0 
    ? (totalMatch / results.summary.totalPages).toFixed(1)
    : 0;
  
  // Save results
  const resultsPath = path.join(CONFIG.reportsDir, 'comparison-results.json');
  await fs.writeFile(resultsPath, JSON.stringify(results, null, 2));
  
  // Generate HTML report
  await generateComparisonReport(results);
  
  // Cleanup
  await browser.close();
  httpServers.forEach(s => s.close());
  
  // Print summary
  console.log('\n' + '═'.repeat(60));
  console.log('📊 COMPARISON SUMMARY');
  console.log('═'.repeat(60));
  console.log(`Total Pages: ${results.summary.totalPages}`);
  console.log(`Average Match: ${results.summary.averageMatch}%`);
  console.log(`Launch Ready: ${results.summary.launchReady}/${results.summary.totalPages}`);
  console.log(`Critical Issues: ${results.summary.criticalIssues}`);
  console.log(`High Issues: ${results.summary.highIssues}`);
  console.log(`\n📄 Report: ${path.join(CONFIG.reportsDir, 'comparison-report.html')}`);
  
  return results;
}

/**
 * Generate HTML comparison report
 */
async function generateComparisonReport(results) {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sails.to Site Comparison Report</title>
  <style>
    :root { --bg:#0a0a0a; --surface:#1a1a1a; --surface2:#252525; --border:#333; --text:#f5f5f5; --dim:#888; --primary:#C9A227; --success:#22c55e; --warning:#f59e0b; --error:#ef4444; --info:#3b82f6; }
    * { box-sizing:border-box; margin:0; padding:0; }
    body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; background:var(--bg); color:var(--text); line-height:1.6; padding:2rem; }
    .container { max-width:1600px; margin:0 auto; }
    h1 { font-size:2rem; color:var(--primary); margin-bottom:.5rem; }
    h2 { font-size:1.4rem; margin:2rem 0 1rem; border-bottom:1px solid var(--border); padding-bottom:.5rem; }
    .subtitle { color:var(--dim); margin-bottom:2rem; }
    
    .summary-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:1rem; margin-bottom:2rem; }
    .summary-card { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:1.25rem; text-align:center; }
    .summary-card .label { font-size:.75rem; color:var(--dim); text-transform:uppercase; letter-spacing:.05em; }
    .summary-card .value { font-size:2rem; font-weight:700; margin-top:.5rem; }
    .summary-card.success .value { color:var(--success); }
    .summary-card.warning .value { color:var(--warning); }
    .summary-card.error .value { color:var(--error); }
    .summary-card.info .value { color:var(--info); }
    .summary-card.primary .value { color:var(--primary); }
    
    .page-card { background:var(--surface); border:1px solid var(--border); border-radius:8px; margin-bottom:1.5rem; overflow:hidden; }
    .page-header { padding:1rem 1.5rem; background:var(--surface2); border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }
    .page-title { font-size:1.2rem; font-weight:600; }
    .page-meta { display:flex; gap:1rem; align-items:center; }
    .badge { padding:.25rem .75rem; border-radius:4px; font-size:.8rem; font-weight:600; }
    .badge.ready { background:var(--success); color:white; }
    .badge.not-ready { background:var(--error); color:white; }
    .badge.match { background:var(--surface); border:1px solid var(--border); }
    
    .page-content { padding:1.5rem; }
    .comparison-image { width:100%; max-height:600px; object-fit:contain; border-radius:4px; cursor:pointer; background:#000; }
    .comparison-image:hover { opacity:.95; }
    
    .issues-section { margin-top:1.5rem; }
    .issues-title { font-size:1rem; margin-bottom:1rem; color:var(--dim); }
    .issue { background:var(--surface2); border-left:3px solid var(--border); padding:1rem; margin-bottom:.75rem; border-radius:0 4px 4px 0; }
    .issue.critical { border-left-color:var(--error); }
    .issue.high { border-left-color:var(--warning); }
    .issue.medium { border-left-color:var(--info); }
    .issue.low { border-left-color:var(--dim); }
    .issue-header { display:flex; gap:.75rem; align-items:center; margin-bottom:.5rem; flex-wrap:wrap; }
    .issue-severity { font-size:.7rem; padding:.15rem .5rem; border-radius:3px; text-transform:uppercase; font-weight:600; }
    .issue-severity.critical { background:var(--error); color:white; }
    .issue-severity.high { background:var(--warning); color:black; }
    .issue-severity.medium { background:var(--info); color:white; }
    .issue-severity.low { background:var(--dim); color:white; }
    .issue-category { font-size:.75rem; color:var(--dim); }
    .issue-location { font-size:.75rem; color:var(--primary); }
    .issue-desc { font-size:.9rem; }
    .issue-comparison { display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:.75rem; font-size:.85rem; }
    .issue-comparison > div { background:var(--bg); padding:.75rem; border-radius:4px; }
    .issue-comparison .label { font-size:.7rem; color:var(--dim); margin-bottom:.25rem; }
    
    .summary-text { background:var(--surface2); padding:1rem; border-radius:4px; margin-top:1rem; font-style:italic; color:var(--dim); }
    
    .modal { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,.95); z-index:1000; cursor:zoom-out; }
    .modal img { max-width:95%; max-height:95%; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); }
    .modal.active { display:block; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🔄 Site Comparison Report</h1>
    <p class="subtitle">Original (drafts) vs Hugo-built site | Generated: ${results.timestamp} | Model: ${results.modelUsed}</p>
    
    <div class="summary-grid">
      <div class="summary-card primary">
        <div class="label">Average Match</div>
        <div class="value">${results.summary.averageMatch}%</div>
      </div>
      <div class="summary-card info">
        <div class="label">Total Pages</div>
        <div class="value">${results.summary.totalPages}</div>
      </div>
      <div class="summary-card success">
        <div class="label">Launch Ready</div>
        <div class="value">${results.summary.launchReady}</div>
      </div>
      <div class="summary-card error">
        <div class="label">Not Ready</div>
        <div class="value">${results.summary.notReady}</div>
      </div>
      <div class="summary-card error">
        <div class="label">Critical Issues</div>
        <div class="value">${results.summary.criticalIssues}</div>
      </div>
      <div class="summary-card warning">
        <div class="label">High Issues</div>
        <div class="value">${results.summary.highIssues}</div>
      </div>
    </div>
    
    <h2>Page-by-Page Comparison</h2>
    
    ${results.pages.map(page => {
      if (page.error) {
        return `
          <div class="page-card">
            <div class="page-header">
              <span class="page-title">${page.name}</span>
              <span class="badge not-ready">Error: ${page.error}</span>
            </div>
          </div>
        `;
      }
      
      const analysis = page.analysis || {};
      const issues = analysis.issues || [];
      
      return `
        <div class="page-card">
          <div class="page-header">
            <span class="page-title">${page.name}</span>
            <div class="page-meta">
              <span class="badge match">${analysis.overallMatch || '?'}% match</span>
              <span class="badge ${analysis.launchReady ? 'ready' : 'not-ready'}">${analysis.launchReady ? '✓ Launch Ready' : '✗ Not Ready'}</span>
            </div>
          </div>
          <div class="page-content">
            <img class="comparison-image" src="${page.screenshots?.sideBySide?.replace('./screenshots/', '../')}" alt="${page.name} comparison" onclick="openModal(this.src)">
            
            ${issues.length > 0 ? `
              <div class="issues-section">
                <div class="issues-title">Issues Found (${issues.length})</div>
                ${issues.map(issue => `
                  <div class="issue ${issue.severity || 'medium'}">
                    <div class="issue-header">
                      <span class="issue-severity ${issue.severity || 'medium'}">${issue.severity || 'medium'}</span>
                      <span class="issue-category">${issue.category || 'general'}</span>
                      ${issue.location ? `<span class="issue-location">📍 ${issue.location}</span>` : ''}
                    </div>
                    <div class="issue-desc">${issue.description || ''}</div>
                    ${(issue.original || issue.hugo) ? `
                      <div class="issue-comparison">
                        ${issue.original ? `<div><div class="label">Original</div>${issue.original}</div>` : ''}
                        ${issue.hugo ? `<div><div class="label">Hugo</div>${issue.hugo}</div>` : ''}
                      </div>
                    ` : ''}
                  </div>
                `).join('')}
              </div>
            ` : '<p style="color:var(--success);">✓ No issues found</p>'}
            
            ${analysis.summary ? `<div class="summary-text">${analysis.summary}</div>` : ''}
          </div>
        </div>
      `;
    }).join('')}
  </div>
  
  <div class="modal" id="modal" onclick="closeModal()">
    <img src="" alt="Full size">
  </div>
  
  <script>
    function openModal(src) {
      const modal = document.getElementById('modal');
      modal.querySelector('img').src = src;
      modal.classList.add('active');
    }
    function closeModal() {
      document.getElementById('modal').classList.remove('active');
    }
    document.addEventListener('keydown', e => { if(e.key === 'Escape') closeModal(); });
  </script>
</body>
</html>`;

  await fs.writeFile(path.join(CONFIG.reportsDir, 'comparison-report.html'), html);
  console.log('\n✅ Comparison report generated');
}

// Run
runComparison().catch(e => {
  console.error('❌ Fatal error:', e);
  httpServers.forEach(s => s.close());
  process.exit(1);
});
