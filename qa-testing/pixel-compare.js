#!/usr/bin/env node
/**
 * Pixel-perfect comparison tool using actual image diffing
 * instead of unreliable AI vision models
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const PNG = require('pngjs').PNG;
const pixelmatch = require('pixelmatch');

const PAGES = [
    { name: 'home', original: '/index.html', hugo: '/' },
    { name: 'issuers', original: '/issuers.html', hugo: '/issuers/' },
    { name: 'investors', original: '/investors.html', hugo: '/investors/' },
    { name: 'brokers', original: '/brokers.html', hugo: '/brokers/' },
    { name: 'introducers', original: '/introducers.html', hugo: '/introducers/' },
    { name: 'regulated', original: '/regulated.html', hugo: '/regulated/' },
    { name: 'issuers-directory', original: '/issuers-directory.html', hugo: '/issuers-directory/' },
    { name: 'whatsails', original: '/whatsails.html', hugo: '/whatsails/' },
    { name: 'pricing', original: '/pricing.html', hugo: '/pricing/' },
    { name: 'signup', original: '/signup.html', hugo: '/signup/' },
    { name: 'company-about', original: '/company/about.html', hugo: '/company/about/' },
    { name: 'company-contact', original: '/company/contact.html', hugo: '/company/contact/' },
    { name: 'company-legal', original: '/company/legal.html', hugo: '/company/legal/' },
];

const ORIGINAL_URL = 'http://localhost:8080';
const HUGO_URL = 'http://localhost:1313';
const OUTPUT_DIR = 'screenshots/pixel-diff';

async function captureScreenshot(page, url, filename) {
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.waitForTimeout(500); // Wait for any animations
    const buffer = await page.screenshot({ fullPage: true });
    fs.writeFileSync(filename, buffer);
    return buffer;
}

function compareImages(img1Path, img2Path, diffPath) {
    const img1 = PNG.sync.read(fs.readFileSync(img1Path));
    const img2 = PNG.sync.read(fs.readFileSync(img2Path));
    
    // Images must be same size for comparison
    const width = Math.max(img1.width, img2.width);
    const height = Math.max(img1.height, img2.height);
    
    // Resize images if needed (pad with white)
    const canvas1 = new PNG({ width, height });
    const canvas2 = new PNG({ width, height });
    
    canvas1.data.fill(255); // White background
    canvas2.data.fill(255);
    
    PNG.bitblt(img1, canvas1, 0, 0, img1.width, img1.height, 0, 0);
    PNG.bitblt(img2, canvas2, 0, 0, img2.width, img2.height, 0, 0);
    
    const diff = new PNG({ width, height });
    
    const numDiffPixels = pixelmatch(
        canvas1.data,
        canvas2.data,
        diff.data,
        width,
        height,
        { threshold: 0.1 }
    );
    
    fs.writeFileSync(diffPath, PNG.sync.write(diff));
    
    const totalPixels = width * height;
    const matchPercentage = ((totalPixels - numDiffPixels) / totalPixels * 100).toFixed(2);
    
    return { numDiffPixels, totalPixels, matchPercentage, width, height };
}

async function main() {
    // Check if required packages are available
    try {
        require('pngjs');
        require('pixelmatch');
    } catch (e) {
        console.log('Installing required packages...');
        const { execSync } = require('child_process');
        execSync('npm install pngjs pixelmatch', { stdio: 'inherit' });
    }
    
    // Ensure output directories exist
    ['original', 'hugo', 'diff'].forEach(dir => {
        const fullPath = path.join(OUTPUT_DIR, dir);
        if (!fs.existsSync(fullPath)) {
            fs.mkdirSync(fullPath, { recursive: true });
        }
    });
    
    console.log('🔄 Sails.to Pixel-Perfect Comparison Tool');
    console.log('════════════════════════════════════════════════════════════');
    
    const browser = await chromium.launch();
    const context = await browser.newContext({
        viewport: { width: 1280, height: 900 }
    });
    
    const results = [];
    
    for (const pageDef of PAGES) {
        process.stdout.write(`📄 ${pageDef.name}... `);
        
        const page = await context.newPage();
        
        const originalPath = path.join(OUTPUT_DIR, 'original', `${pageDef.name}.png`);
        const hugoPath = path.join(OUTPUT_DIR, 'hugo', `${pageDef.name}.png`);
        const diffPath = path.join(OUTPUT_DIR, 'diff', `${pageDef.name}.png`);
        
        try {
            // Capture screenshots
            await captureScreenshot(page, `${ORIGINAL_URL}${pageDef.original}`, originalPath);
            await captureScreenshot(page, `${HUGO_URL}${pageDef.hugo}`, hugoPath);
            
            // Compare
            const comparison = compareImages(originalPath, hugoPath, diffPath);
            
            results.push({
                name: pageDef.name,
                ...comparison,
                status: comparison.matchPercentage >= 95 ? '✅' : '❌'
            });
            
            console.log(`${comparison.matchPercentage}% match ${comparison.matchPercentage >= 95 ? '✅' : '❌'}`);
        } catch (e) {
            console.log(`Error: ${e.message}`);
            results.push({
                name: pageDef.name,
                error: e.message,
                status: '⚠️'
            });
        }
        
        await page.close();
    }
    
    await browser.close();
    
    // Summary
    console.log('');
    console.log('════════════════════════════════════════════════════════════');
    console.log('📊 PIXEL COMPARISON SUMMARY');
    console.log('════════════════════════════════════════════════════════════');
    
    const validResults = results.filter(r => !r.error);
    if (validResults.length > 0) {
        const avgMatch = validResults.reduce((a, b) => a + parseFloat(b.matchPercentage), 0) / validResults.length;
        const perfect = validResults.filter(r => parseFloat(r.matchPercentage) >= 95).length;
        
        console.log(`Average Match: ${avgMatch.toFixed(2)}%`);
        console.log(`Perfect (≥95%): ${perfect}/${validResults.length}`);
        console.log('');
        
        console.log('Page Results:');
        results.forEach(r => {
            if (r.error) {
                console.log(`  ${r.status} ${r.name}: ${r.error}`);
            } else {
                console.log(`  ${r.status} ${r.name}: ${r.matchPercentage}% (${r.numDiffPixels.toLocaleString()} diff pixels)`);
            }
        });
    }
    
    // Save JSON report
    fs.writeFileSync(
        path.join(OUTPUT_DIR, 'pixel-comparison-results.json'),
        JSON.stringify({ timestamp: new Date().toISOString(), results }, null, 2)
    );
    
    console.log('');
    console.log(`📄 Diff images saved to: ${OUTPUT_DIR}/diff/`);
}

main().catch(console.error);
