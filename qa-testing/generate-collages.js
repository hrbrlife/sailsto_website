#!/usr/bin/env node
/**
 * Generate Collages from Screenshots
 * 1. Overview collage: All desktop first-view (top) screenshots
 * 2. Per-page collages: All viewports for each page
 */

import fs from 'fs/promises';
import path from 'path';
import sharp from 'sharp';

const CONFIG = {
  screenshotsDir: './screenshots',
  outputDir: './screenshots/collages',
  viewports: ['desktop', 'tablet', 'mobile'],
  thumbnailWidth: 400,
  overviewThumbWidth: 300,
  padding: 10,
  labelHeight: 30,
  backgroundColor: '#1a1a1a',
  labelColor: '#C9A227',
  textColor: '#ffffff'
};

/**
 * Get all screenshots grouped by page
 */
async function getScreenshotsByPage() {
  const screenshots = {};
  
  for (const viewport of CONFIG.viewports) {
    const dir = path.join(CONFIG.screenshotsDir, viewport);
    try {
      const files = await fs.readdir(dir);
      for (const file of files) {
        if (!file.endsWith('.png')) continue;
        
        const parts = file.replace('.png', '').split('_');
        const position = parts.pop();
        const vp = parts.pop();
        const pageName = parts.join('_');
        
        if (!screenshots[pageName]) screenshots[pageName] = {};
        if (!screenshots[pageName][viewport]) screenshots[pageName][viewport] = {};
        screenshots[pageName][viewport][position] = path.join(dir, file);
      }
    } catch (e) {
      console.error(`Error reading ${dir}:`, e.message);
    }
  }
  
  return screenshots;
}

/**
 * Create a labeled thumbnail
 */
async function createLabeledThumbnail(imagePath, label, width) {
  const image = sharp(imagePath);
  const metadata = await image.metadata();
  const height = Math.round((metadata.height / metadata.width) * width);
  
  const resized = await image
    .resize(width, height, { fit: 'contain', background: CONFIG.backgroundColor })
    .toBuffer();
  
  const labelSvg = `
    <svg width="${width}" height="${CONFIG.labelHeight}">
      <rect width="100%" height="100%" fill="${CONFIG.backgroundColor}"/>
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" 
            fill="${CONFIG.labelColor}" font-family="Arial, sans-serif" font-size="12" font-weight="bold">
        ${label}
      </text>
    </svg>
  `;
  
  const labeled = await sharp({
    create: { width, height: height + CONFIG.labelHeight, channels: 4, background: CONFIG.backgroundColor }
  })
    .composite([
      { input: Buffer.from(labelSvg), top: 0, left: 0 },
      { input: resized, top: CONFIG.labelHeight, left: 0 }
    ])
    .png()
    .toBuffer();
  
  return { buffer: labeled, width, height: height + CONFIG.labelHeight };
}

/**
 * Create overview collage (all desktop top screenshots)
 */
async function createOverviewCollage(screenshotsByPage) {
  console.log('\n📸 Creating Overview Collage (Desktop First-View)...');
  
  const pages = Object.keys(screenshotsByPage).sort();
  const thumbnails = [];
  
  for (const page of pages) {
    const topScreenshot = screenshotsByPage[page]?.desktop?.top;
    if (topScreenshot) {
      try {
        const thumb = await createLabeledThumbnail(topScreenshot, page, CONFIG.overviewThumbWidth);
        thumbnails.push({ ...thumb, page });
        console.log(`  ✓ ${page}`);
      } catch (e) {
        console.error(`  ✗ ${page}: ${e.message}`);
      }
    }
  }
  
  if (thumbnails.length === 0) return null;
  
  const cols = Math.ceil(Math.sqrt(thumbnails.length));
  const rows = Math.ceil(thumbnails.length / cols);
  const maxThumbHeight = Math.max(...thumbnails.map(t => t.height));
  
  const totalWidth = cols * (CONFIG.overviewThumbWidth + CONFIG.padding) + CONFIG.padding;
  const totalHeight = rows * (maxThumbHeight + CONFIG.padding) + CONFIG.padding + 50;
  
  const titleSvg = `
    <svg width="${totalWidth}" height="50">
      <rect width="100%" height="100%" fill="${CONFIG.backgroundColor}"/>
      <text x="50%" y="30" dominant-baseline="middle" text-anchor="middle" 
            fill="${CONFIG.textColor}" font-family="Arial, sans-serif" font-size="20" font-weight="bold">
        Desktop Overview - All Pages First View (${thumbnails.length} pages)
      </text>
    </svg>
  `;
  
  const composites = [{ input: Buffer.from(titleSvg), top: 0, left: 0 }];
  
  thumbnails.forEach((thumb, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    composites.push({
      input: thumb.buffer,
      top: 50 + CONFIG.padding + row * (maxThumbHeight + CONFIG.padding),
      left: CONFIG.padding + col * (CONFIG.overviewThumbWidth + CONFIG.padding)
    });
  });
  
  const outputPath = path.join(CONFIG.outputDir, 'overview-desktop-firstview.png');
  await sharp({
    create: { width: totalWidth, height: totalHeight, channels: 4, background: CONFIG.backgroundColor }
  }).composite(composites).png().toFile(outputPath);
  
  console.log(`  ✅ Created: overview-desktop-firstview.png (${totalWidth}x${totalHeight})`);
  return outputPath;
}

/**
 * Create device-specific collages per page
 */
async function createDeviceCollage(pageName, pageScreenshots, device) {
  const positions = ['top', '25pct', '50pct', '75pct', 'bottom'];
  const deviceScreenshots = pageScreenshots[device];
  if (!deviceScreenshots) return null;
  
  const thumbnails = [];
  const thumbWidth = device === 'desktop' ? 500 : device === 'tablet' ? 350 : 250;
  
  for (const position of positions) {
    const screenshot = deviceScreenshots[position];
    if (screenshot) {
      try {
        const thumb = await createLabeledThumbnail(screenshot, position, thumbWidth);
        thumbnails.push(thumb);
      } catch (e) {}
    }
  }
  
  if (thumbnails.length === 0) return null;
  
  const totalWidth = thumbWidth + CONFIG.padding * 2;
  const totalHeight = thumbnails.reduce((sum, t) => sum + t.height + CONFIG.padding, CONFIG.padding + 40);
  
  const titleSvg = `
    <svg width="${totalWidth}" height="40">
      <rect width="100%" height="100%" fill="${CONFIG.backgroundColor}"/>
      <text x="50%" y="25" dominant-baseline="middle" text-anchor="middle" 
            fill="${CONFIG.labelColor}" font-family="Arial, sans-serif" font-size="14" font-weight="bold">
        ${pageName} - ${device}
      </text>
    </svg>
  `;
  
  const composites = [{ input: Buffer.from(titleSvg), top: 0, left: 0 }];
  let y = 40 + CONFIG.padding;
  for (const thumb of thumbnails) {
    composites.push({ input: thumb.buffer, top: y, left: CONFIG.padding });
    y += thumb.height + CONFIG.padding;
  }
  
  const outputPath = path.join(CONFIG.outputDir, `${pageName}-${device}.png`);
  await sharp({
    create: { width: totalWidth, height: totalHeight, channels: 4, background: CONFIG.backgroundColor }
  }).composite(composites).png().toFile(outputPath);
  
  return outputPath;
}

/**
 * Main function
 */
async function generateCollages() {
  console.log('🎨 Generating Screenshot Collages');
  console.log('═'.repeat(50));
  
  await fs.mkdir(CONFIG.outputDir, { recursive: true });
  
  const screenshotsByPage = await getScreenshotsByPage();
  const pages = Object.keys(screenshotsByPage);
  
  console.log(`\n📊 Found ${pages.length} pages with screenshots`);
  
  const results = { overview: null, pageCollages: [], deviceCollages: [] };
  
  results.overview = await createOverviewCollage(screenshotsByPage);
  
  console.log('\n📱 Creating Device-Specific Collages...');
  for (const page of pages) {
    for (const device of CONFIG.viewports) {
      const collagePath = await createDeviceCollage(page, screenshotsByPage[page], device);
      if (collagePath) {
        results.deviceCollages.push({ page, device, path: collagePath });
        console.log(`  ✓ ${page} (${device})`);
      }
    }
  }
  
  await fs.writeFile(path.join(CONFIG.outputDir, 'collages-index.json'), JSON.stringify(results, null, 2));
  
  console.log('\n═'.repeat(50));
  console.log('📊 COLLAGE GENERATION COMPLETE');
  console.log('═'.repeat(50));
  console.log(`  Overview Collage:     1`);
  console.log(`  Device Collages:      ${results.deviceCollages.length}`);
  console.log(`  Output Directory:     ${CONFIG.outputDir}`);
  
  return results;
}

generateCollages().catch(error => {
  console.error('❌ Collage generation failed:', error);
  process.exit(1);
});
