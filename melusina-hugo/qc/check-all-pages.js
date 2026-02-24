#!/usr/bin/env node
/**
 * QC: Check all pages for console errors and 404 network requests
 * Usage: node check-all-pages.js
 * Requires: playwright (npx playwright install chromium)
 */

const BASE = 'http://localhost:1315/melusina-site';

const PAGES = [
  '/',
  '/architecture/',
  '/bureau/',
  '/company/',
  '/compare/',
  '/docs/',
  '/docs/api-integration/',
  '/docs/architecture-blueprint/',
  '/docs/case-chat-guide/',
  '/docs/getting-started/',
  '/docs/screening-providers/',
  '/docs/security-best-practices/',
  '/docs/wallet-verification/',
  '/faq/',
  '/for/',
  '/for/daos/',
  '/for/family-offices/',
  '/for/introducers/',
  '/for/private-banks/',
  '/for/regulated/',
  '/for/trust-companies/',
  '/for/vasps/',
  '/glossary/',
  '/glossary/aml/',
  '/glossary/anonymous-identity/',
  '/glossary/bureau/',
  '/glossary/capability-url/',
  '/glossary/capnproto/',
  '/glossary/due-diligence/',
  '/glossary/grapple/',
  '/glossary/kyc/',
  '/glossary/mermail/',
  '/glossary/panel-builder/',
  '/glossary/pearl/',
  '/glossary/process-catalog/',
  '/glossary/pwa/',
  '/glossary/repeatable-group/',
  '/glossary/static-store/',
  '/glossary/template-compiler/',
  '/glossary/visiblewhen/',
  '/knowledge-base/',
  '/plans/',
  '/privacy/',
  '/roadmap/',
  '/terms/',
  '/use-cases/',
  '/fr/',
  '/fr/architecture/',
  '/fr/company/',
];

async function main() {
  const { chromium } = await import('playwright');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  
  const results = [];
  let totalErrors = 0;
  let total404s = 0;
  
  for (const path of PAGES) {
    const url = BASE + path;
    const page = await context.newPage();
    
    const errors = [];
    const failed = [];
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    page.on('response', response => {
      if (response.status() === 404) {
        failed.push(response.url());
      }
    });
    
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });
    } catch (e) {
      errors.push(`Navigation error: ${e.message}`);
    }
    
    const status = (errors.length === 0 && failed.length === 0) ? '✓' : '✗';
    
    if (errors.length > 0 || failed.length > 0) {
      console.log(`${status} ${path}`);
      errors.forEach(e => console.log(`  ERROR: ${e}`));
      failed.forEach(f => console.log(`  404: ${f}`));
      totalErrors += errors.length;
      total404s += failed.length;
    } else {
      console.log(`${status} ${path}`);
    }
    
    await page.close();
  }
  
  console.log(`\n=== SUMMARY ===`);
  console.log(`Pages checked: ${PAGES.length}`);
  console.log(`Console errors: ${totalErrors}`);
  console.log(`404 resources: ${total404s}`);
  
  await browser.close();
  process.exit(totalErrors + total404s > 0 ? 1 : 0);
}

main().catch(console.error);
