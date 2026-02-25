#!/usr/bin/env node
/**
 * Sails.to QA Crawler
 * Crawls all pages, captures screenshots at multiple scroll positions
 * for both desktop and mobile viewports
 */

import { chromium } from 'playwright';
import fs from 'fs/promises';
import path from 'path';

// Configuration
const CONFIG = {
  baseUrl: process.env.BASE_URL || 'http://localhost:1313',
  outputDir: './screenshots',
  viewports: {
    desktop: { width: 1920, height: 1080, name: 'desktop' },
    tablet: { width: 768, height: 1024, name: 'tablet' },
    mobile: { width: 375, height: 812, name: 'mobile' }
  },
  // Pages to test - COMPREHENSIVE COVERAGE matching website-analyzer.js
  pages: [
    // ═══════════════════════════════════════════════════════════════════
    // TIER 1: CRITICAL - Conversion Pages
    // ═══════════════════════════════════════════════════════════════════
    { path: '/', name: 'home', tier: 'critical' },
    { path: '/issuers/', name: 'issuers', tier: 'critical' },
    { path: '/investors/', name: 'investors', tier: 'critical' },
    { path: '/pricing/', name: 'pricing', tier: 'critical' },
    { path: '/signup/', name: 'signup', tier: 'critical' },
    
    // ═══════════════════════════════════════════════════════════════════
    // TIER 2: HIGH - Audience & Product Pages
    // ═══════════════════════════════════════════════════════════════════
    { path: '/brokers/', name: 'brokers', tier: 'high' },
    { path: '/regulated/', name: 'regulated', tier: 'high' },
    { path: '/introducers/', name: 'introducers', tier: 'high' },
    { path: '/whatsails/', name: 'whatsails', tier: 'high' },
    { path: '/issuers-directory/', name: 'issuers-directory', tier: 'high' },
    
    // ═══════════════════════════════════════════════════════════════════
    // TIER 3: TRUST - Credibility Pages
    // ═══════════════════════════════════════════════════════════════════
    { path: '/security/', name: 'security', tier: 'trust' },
    { path: '/compliance/', name: 'compliance', tier: 'trust' },
    { path: '/oversight/', name: 'oversight', tier: 'trust' },
    { path: '/company/', name: 'company-index', tier: 'trust' },
    { path: '/company/about/', name: 'company-about', tier: 'trust' },
    { path: '/company/contact/', name: 'company-contact', tier: 'trust' },
    { path: '/company/legal/', name: 'company-legal', tier: 'trust' },
    
    // ═══════════════════════════════════════════════════════════════════
    // TIER 4: KNOWLEDGE - Educational Content
    // ═══════════════════════════════════════════════════════════════════
    { path: '/knowledge/', name: 'knowledge-index', tier: 'knowledge' },
    { path: '/knowledge/faq/', name: 'knowledge-faq', tier: 'knowledge' },
    { path: '/knowledge/roadmap/', name: 'knowledge-roadmap', tier: 'knowledge' },
    { path: '/knowledge/glossary/', name: 'glossary-index', tier: 'knowledge' },
    { path: '/knowledge/blog/', name: 'blog-index', tier: 'knowledge' },
    { path: '/knowledge/docs/', name: 'docs-index', tier: 'knowledge' },
    { path: '/knowledge/guides/', name: 'guides-index', tier: 'knowledge' },
    { path: '/knowledge/guides/getting-started/', name: 'guides-getting-started', tier: 'knowledge' },
    
    // ═══════════════════════════════════════════════════════════════════
    // TIER 5: SAMPLES - Spot Check Content Quality
    // ═══════════════════════════════════════════════════════════════════
    // Key glossary terms
    { path: '/knowledge/glossary/crosssecurities/', name: 'glossary-crosssecurities', tier: 'samples' },
    { path: '/knowledge/glossary/tokenization/', name: 'glossary-tokenization', tier: 'samples' },
    { path: '/knowledge/glossary/wyoming-dao-llc/', name: 'glossary-wyoming-dao', tier: 'samples' },
    { path: '/knowledge/glossary/security-token/', name: 'glossary-security-token', tier: 'samples' },
    { path: '/knowledge/glossary/isin/', name: 'glossary-isin', tier: 'samples' },
    { path: '/knowledge/glossary/kyc/', name: 'glossary-kyc', tier: 'samples' },
    // Key blog posts
    { path: '/knowledge/blog/security-tokens-explained/', name: 'blog-security-tokens', tier: 'samples' },
    { path: '/knowledge/blog/why-wyoming/', name: 'blog-why-wyoming', tier: 'samples' },
    { path: '/knowledge/blog/future-of-tokenized-securities/', name: 'blog-future-tokenized', tier: 'samples' },
    // Key docs
    { path: '/knowledge/docs/platform-overview/', name: 'docs-platform-overview', tier: 'samples' },
    { path: '/knowledge/docs/getting-started/', name: 'docs-getting-started', tier: 'samples' },
  ],
  scrollPositions: ['top', '25%', '50%', '75%', 'bottom'],
  waitTime: 500, // ms to wait after scroll for animations
  timeout: 30000
};

// Parse command line arguments
const args = process.argv.slice(2);
let selectedViewports = Object.keys(CONFIG.viewports);
if (args.includes('--viewport=desktop')) {
  selectedViewports = ['desktop'];
} else if (args.includes('--viewport=mobile')) {
  selectedViewports = ['mobile'];
} else if (args.includes('--viewport=tablet')) {
  selectedViewports = ['tablet'];
}

/**
 * Create output directories
 */
async function setupDirectories() {
  const dirs = [
    CONFIG.outputDir,
    `${CONFIG.outputDir}/desktop`,
    `${CONFIG.outputDir}/tablet`,
    `${CONFIG.outputDir}/mobile`,
    `${CONFIG.outputDir}/reports`
  ];
  
  for (const dir of dirs) {
    await fs.mkdir(dir, { recursive: true });
  }
  
  console.log('📁 Output directories created');
}

/**
 * Scroll to a specific position on the page
 */
async function scrollToPosition(page, position) {
  await page.evaluate(async (pos) => {
    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
    let targetY = 0;
    
    switch (pos) {
      case 'top':
        targetY = 0;
        break;
      case '25%':
        targetY = scrollHeight * 0.25;
        break;
      case '50%':
        targetY = scrollHeight * 0.5;
        break;
      case '75%':
        targetY = scrollHeight * 0.75;
        break;
      case 'bottom':
        targetY = scrollHeight;
        break;
      default:
        targetY = 0;
    }
    
    window.scrollTo({ top: targetY, behavior: 'instant' });
  }, position);
  
  // Wait for any animations or lazy-loaded content
  await page.waitForTimeout(CONFIG.waitTime);
}

/**
 * Capture screenshot with metadata
 */
async function captureScreenshot(page, pageInfo, viewport, position) {
  const filename = `${pageInfo.name}_${viewport}_${position.replace('%', 'pct')}.png`;
  const filepath = path.join(CONFIG.outputDir, viewport, filename);
  
  await page.screenshot({
    path: filepath,
    fullPage: false // Capture viewport only
  });
  
  return {
    filename,
    filepath,
    page: pageInfo.name,
    url: pageInfo.path,
    viewport,
    scrollPosition: position,
    timestamp: new Date().toISOString()
  };
}

/**
 * Setup comprehensive logging capture
 */
function setupPageCapture(page, pageInfo) {
  const capture = {
    consoleLogs: [],
    networkRequests: [],
    networkErrors: [],
    pageErrors: []
  };
  
  // Capture ALL console messages
  page.on('console', msg => {
    capture.consoleLogs.push({
      type: msg.type(),
      text: msg.text(),
      timestamp: Date.now(),
      page: pageInfo.name,
      url: pageInfo.path
    });
  });
  
  // Capture page errors
  page.on('pageerror', error => {
    capture.pageErrors.push({
      type: 'pageerror',
      text: error.message,
      stack: error.stack,
      timestamp: Date.now(),
      page: pageInfo.name,
      url: pageInfo.path
    });
  });
  
  // Capture network requests
  page.on('request', request => {
    capture.networkRequests.push({
      url: request.url(),
      method: request.method(),
      resourceType: request.resourceType(),
      timestamp: Date.now(),
      page: pageInfo.name
    });
  });
  
  // Capture network failures
  page.on('requestfailed', request => {
    capture.networkErrors.push({
      url: request.url(),
      method: request.method(),
      resourceType: request.resourceType(),
      failure: request.failure()?.errorText || 'Unknown error',
      timestamp: Date.now(),
      page: pageInfo.name
    });
  });
  
  // Capture response errors (4xx, 5xx)
  page.on('response', response => {
    if (response.status() >= 400) {
      capture.networkErrors.push({
        url: response.url(),
        status: response.status(),
        statusText: response.statusText(),
        resourceType: response.request().resourceType(),
        timestamp: Date.now(),
        page: pageInfo.name
      });
    }
  });
  
  return capture;
}

/**
 * Get snapshot of current logs at scroll position
 */
function snapshotLogs(capture, scrollPosition) {
  return {
    consoleLogs: [...capture.consoleLogs],
    networkRequests: [...capture.networkRequests],
    networkErrors: [...capture.networkErrors],
    pageErrors: [...capture.pageErrors],
    scrollPosition,
    snapshotTime: Date.now()
  };
}

/**
 * Test navigation functionality
 */
async function testNavigation(page, pageInfo) {
  const issues = [];
  
  try {
    // Check if nav exists
    const nav = await page.$('nav');
    if (!nav) {
      issues.push({
        type: 'missing-element',
        element: 'nav',
        page: pageInfo.name,
        severity: 'high'
      });
    }
    
    // Check mobile nav toggle
    const navToggle = await page.$('.nav-toggle');
    if (navToggle) {
      const isVisible = await navToggle.isVisible();
      if (isVisible) {
        // Test mobile nav toggle
        await navToggle.click();
        await page.waitForTimeout(300);
        
        const navLinks = await page.$('.nav-links');
        if (navLinks) {
          const linksVisible = await navLinks.isVisible();
          if (!linksVisible) {
            issues.push({
              type: 'interaction-failure',
              element: 'nav-toggle',
              description: 'Mobile nav toggle does not reveal menu',
              page: pageInfo.name,
              severity: 'high'
            });
          }
        }
        
        // Close nav
        await navToggle.click();
        await page.waitForTimeout(300);
      }
    }
    
    // Check footer exists
    const footer = await page.$('footer');
    if (!footer) {
      issues.push({
        type: 'missing-element',
        element: 'footer',
        page: pageInfo.name,
        severity: 'medium'
      });
    }
    
    // Check for broken images
    const images = await page.$$('img');
    for (const img of images) {
      const src = await img.getAttribute('src');
      const naturalWidth = await img.evaluate(el => el.naturalWidth);
      if (naturalWidth === 0) {
        issues.push({
          type: 'broken-image',
          src: src,
          page: pageInfo.name,
          severity: 'medium'
        });
      }
    }
    
    // Check for links
    const links = await page.$$('a[href]');
    for (const link of links) {
      const href = await link.getAttribute('href');
      const text = await link.textContent();
      if (!href || href === '#') {
        issues.push({
          type: 'empty-link',
          text: text?.trim().substring(0, 50),
          page: pageInfo.name,
          severity: 'low'
        });
      }
    }
    
  } catch (error) {
    issues.push({
      type: 'test-error',
      description: error.message,
      page: pageInfo.name,
      severity: 'high'
    });
  }
  
  return issues;
}

/**
 * Measure page performance
 */
async function measurePerformance(page, pageInfo) {
  const metrics = await page.evaluate(() => {
    const timing = performance.timing;
    const paint = performance.getEntriesByType('paint');
    
    return {
      domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
      loadComplete: timing.loadEventEnd - timing.navigationStart,
      firstPaint: paint.find(p => p.name === 'first-paint')?.startTime || 0,
      firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0
    };
  });
  
  return {
    ...metrics,
    page: pageInfo.name,
    url: pageInfo.path
  };
}

/**
 * Main crawler function
 */
async function crawlSite() {
  console.log('🚀 Starting Sails.to QA Crawler');
  console.log(`📍 Base URL: ${CONFIG.baseUrl}`);
  console.log(`📱 Viewports: ${selectedViewports.join(', ')}`);
  console.log(`📄 Pages to test: ${CONFIG.pages.length}`);
  console.log('');
  
  await setupDirectories();
  
  const browser = await chromium.launch({
    headless: true
  });
  
  const results = {
    screenshots: [],
    screenshotLogs: {}, // NEW: logs per screenshot
    issues: [],
    consoleLogs: [],
    networkRequests: [],
    networkErrors: [],
    performance: [],
    summary: {
      totalPages: CONFIG.pages.length,
      totalScreenshots: 0,
      totalIssues: 0,
      totalNetworkRequests: 0,
      totalConsoleMessages: 0,
      startTime: new Date().toISOString(),
      endTime: null
    }
  };
  
  try {
    for (const viewportName of selectedViewports) {
      const viewport = CONFIG.viewports[viewportName];
      console.log(`\n📐 Testing ${viewport.name} viewport (${viewport.width}x${viewport.height})`);
      console.log('─'.repeat(60));
      
      const context = await browser.newContext({
        viewport: { width: viewport.width, height: viewport.height },
        deviceScaleFactor: viewportName === 'mobile' ? 2 : 1,
        isMobile: viewportName === 'mobile',
        hasTouch: viewportName === 'mobile'
      });
      
      const page = await context.newPage();
      
      for (const pageInfo of CONFIG.pages) {
        const url = `${CONFIG.baseUrl}${pageInfo.path}`;
        console.log(`\n  📄 ${pageInfo.name}`);
        
        try {
          // Setup comprehensive capture (console, network, errors)
          const pageCapture = setupPageCapture(page, pageInfo);
          
          // Navigate to page
          const response = await page.goto(url, {
            waitUntil: 'networkidle',
            timeout: CONFIG.timeout
          });
          
          if (!response || response.status() >= 400) {
            results.issues.push({
              type: 'http-error',
              status: response?.status() || 'no response',
              page: pageInfo.name,
              url: pageInfo.path,
              viewport: viewport.name,
              severity: 'critical'
            });
            console.log(`     ❌ HTTP ${response?.status() || 'error'}`);
            continue;
          }
          
          // Wait for page to be fully loaded
          await page.waitForLoadState('domcontentloaded');
          
          // Measure performance
          const perfMetrics = await measurePerformance(page, pageInfo);
          results.performance.push({ ...perfMetrics, viewport: viewport.name });
          
          // Test navigation and UI elements
          const navIssues = await testNavigation(page, pageInfo);
          results.issues.push(...navIssues.map(i => ({ ...i, viewport: viewport.name })));
          
          // Capture screenshots at different scroll positions with associated logs
          let prevLogCount = 0;
          let prevNetworkCount = 0;
          
          for (const position of CONFIG.scrollPositions) {
            await scrollToPosition(page, position);
            const screenshotInfo = await captureScreenshot(page, pageInfo, viewport.name, position);
            
            // Snapshot logs at this scroll position
            const logSnapshot = snapshotLogs(pageCapture, position);
            
            // Calculate new logs since last position
            const newConsoleLogs = logSnapshot.consoleLogs.slice(prevLogCount);
            const newNetworkRequests = logSnapshot.networkRequests.slice(prevNetworkCount);
            
            // Store logs associated with this screenshot
            const screenshotKey = screenshotInfo.filename;
            results.screenshotLogs[screenshotKey] = {
              consoleLogs: newConsoleLogs,
              allConsoleLogs: logSnapshot.consoleLogs,
              networkRequests: newNetworkRequests,
              allNetworkRequests: logSnapshot.networkRequests,
              networkErrors: logSnapshot.networkErrors,
              pageErrors: logSnapshot.pageErrors,
              scrollPosition: position,
              viewport: viewport.name,
              page: pageInfo.name
            };
            
            // Add log counts to screenshot info
            screenshotInfo.consoleLogCount = newConsoleLogs.length;
            screenshotInfo.networkRequestCount = newNetworkRequests.length;
            screenshotInfo.errorCount = logSnapshot.networkErrors.length + logSnapshot.pageErrors.length;
            
            results.screenshots.push(screenshotInfo);
            results.summary.totalScreenshots++;
            
            prevLogCount = logSnapshot.consoleLogs.length;
            prevNetworkCount = logSnapshot.networkRequests.length;
          }
          
          // Collect all logs for summary
          results.consoleLogs.push(...pageCapture.consoleLogs);
          results.networkRequests.push(...pageCapture.networkRequests);
          results.networkErrors.push(...pageCapture.networkErrors);
          
          const issueCount = navIssues.length;
          const networkCount = pageCapture.networkRequests.length;
          const consoleCount = pageCapture.consoleLogs.length;
          const errorCount = pageCapture.networkErrors.length + pageCapture.pageErrors.length;
          
          const status = issueCount === 0 ? '✅' : `⚠️ ${issueCount}`;
          console.log(`     ${status} | ${CONFIG.scrollPositions.length} shots | ${networkCount} reqs | ${consoleCount} logs | ${errorCount} errs | ${perfMetrics.loadComplete}ms`);
          
        } catch (error) {
          results.issues.push({
            type: 'navigation-error',
            description: error.message,
            page: pageInfo.name,
            url: pageInfo.path,
            viewport: viewport.name,
            severity: 'critical'
          });
          console.log(`     ❌ Error: ${error.message.substring(0, 50)}`);
        }
      }
      
      await context.close();
    }
    
  } finally {
    await browser.close();
  }
  
  results.summary.endTime = new Date().toISOString();
  results.summary.totalIssues = results.issues.length;
  results.summary.totalNetworkRequests = results.networkRequests.length;
  results.summary.totalConsoleMessages = results.consoleLogs.length;
  results.summary.totalNetworkErrors = results.networkErrors.length;
  
  // Save results
  const resultsPath = path.join(CONFIG.outputDir, 'reports', 'crawler-results.json');
  await fs.writeFile(resultsPath, JSON.stringify(results, null, 2));
  
  // Print summary
  console.log('\n');
  console.log('═'.repeat(60));
  console.log('📊 CRAWL SUMMARY');
  console.log('═'.repeat(60));
  console.log(`  Total Pages:          ${results.summary.totalPages}`);
  console.log(`  Total Screenshots:    ${results.summary.totalScreenshots}`);
  console.log(`  Total Issues:         ${results.summary.totalIssues}`);
  console.log(`  Network Requests:     ${results.summary.totalNetworkRequests}`);
  console.log(`  Console Messages:     ${results.summary.totalConsoleMessages}`);
  console.log(`  Network Errors:       ${results.summary.totalNetworkErrors}`);
  console.log(`  Results saved to:     ${resultsPath}`);
  console.log(`  Results saved to:  ${resultsPath}`);
  console.log('═'.repeat(60));
  
  // Print issues if any
  if (results.issues.length > 0) {
    console.log('\n⚠️  ISSUES FOUND:');
    const criticalIssues = results.issues.filter(i => i.severity === 'critical');
    const highIssues = results.issues.filter(i => i.severity === 'high');
    const mediumIssues = results.issues.filter(i => i.severity === 'medium');
    
    if (criticalIssues.length > 0) {
      console.log(`\n  🔴 Critical (${criticalIssues.length}):`);
      criticalIssues.slice(0, 5).forEach(i => {
        console.log(`     - ${i.type}: ${i.page} - ${i.description || i.url || ''}`);
      });
    }
    
    if (highIssues.length > 0) {
      console.log(`\n  🟠 High (${highIssues.length}):`);
      highIssues.slice(0, 5).forEach(i => {
        console.log(`     - ${i.type}: ${i.page} - ${i.element || i.description || ''}`);
      });
    }
    
    if (mediumIssues.length > 0) {
      console.log(`\n  🟡 Medium (${mediumIssues.length}):`);
      mediumIssues.slice(0, 5).forEach(i => {
        console.log(`     - ${i.type}: ${i.page} - ${i.src || i.element || ''}`);
      });
    }
  }
  
  return results;
}

// Run crawler
crawlSite().catch(error => {
  console.error('❌ Crawler failed:', error);
  process.exit(1);
});
