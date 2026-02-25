#!/usr/bin/env node
/**
 * Generate image collages for QA review
 * 1. Master collage: All desktop "top" screenshots for quick overview
 * 2. Per-page collages: All viewports/positions for each page
 */

import sharp from 'sharp';
import fs from 'fs/promises';
import path from 'path';
import { glob } from 'glob';

const CONFIG = {
  screenshotsDir: './screenshots',
  collagesDir: './screenshots/collages',
  reportsDir: './screenshots/reports',
  
  // Master collage settings (all pages, desktop, top view)
  masterCollage: {
    columns: 5,
    thumbWidth: 384,
    thumbHeight: 216,
    padding: 4,
    labelHeight: 24,
    backgroundColor: '#0a0a0a',
    labelColor: '#C9A227',
    borderColor: '#333'
  },
  
  // Per-page collage settings (all viewports, all positions)
  pageCollage: {
    viewportOrder: ['desktop', 'tablet', 'mobile'],
    positionOrder: ['top', '25%', '50%', '75%', 'bottom'],
    thumbWidth: 300,
    padding: 3,
    labelHeight: 20,
    backgroundColor: '#1a1a1a',
    labelColor: '#f5f5f5'
  }
};

/**
 * Ensure output directories exist
 */
async function setupDirs() {
  await fs.mkdir(CONFIG.collagesDir, { recursive: true });
  await fs.mkdir(path.join(CONFIG.collagesDir, 'pages'), { recursive: true });
  console.log('📁 Collage directories created');
}

/**
 * Create a text label image
 */
async function createLabel(text, width, height, bgColor, textColor) {
  // Create SVG with text
  const svg = `
    <svg width="${width}" height="${height}">
      <rect width="100%" height="100%" fill="${bgColor}"/>
      <text 
        x="50%" 
        y="50%" 
        text-anchor="middle" 
        dominant-baseline="middle" 
        font-family="Arial, sans-serif" 
        font-size="12" 
        font-weight="bold"
        fill="${textColor}"
      >${text}</text>
    </svg>
  `;
  return sharp(Buffer.from(svg)).png().toBuffer();
}

/**
 * Create thumbnail with border
 */
async function createThumbnail(imagePath, width, height, borderColor) {
  try {
    const image = sharp(imagePath);
    const meta = await image.metadata();
    
    // Calculate aspect-ratio-preserving dimensions
    const aspectRatio = meta.width / meta.height;
    let resizeWidth = width;
    let resizeHeight = Math.round(width / aspectRatio);
    
    if (resizeHeight > height) {
      resizeHeight = height;
      resizeWidth = Math.round(height * aspectRatio);
    }
    
    // Resize and add border
    return await image
      .resize(resizeWidth, resizeHeight, { fit: 'inside' })
      .extend({
        top: 1,
        bottom: 1,
        left: 1,
        right: 1,
        background: borderColor
      })
      .png()
      .toBuffer();
  } catch (error) {
    console.error(`Error processing ${imagePath}:`, error.message);
    // Return placeholder
    return await sharp({
      create: {
        width: width,
        height: height,
        channels: 4,
        background: { r: 50, g: 50, b: 50, alpha: 1 }
      }
    }).png().toBuffer();
  }
}

/**
 * Generate master collage (all desktop top screenshots)
 */
async function generateMasterCollage() {
  console.log('\n🖼️  Generating master collage (all pages, desktop, top view)...');
  
  const config = CONFIG.masterCollage;
  
  // Find all desktop top screenshots
  const pattern = path.join(CONFIG.screenshotsDir, 'desktop', '*_desktop_top.png');
  const files = await glob(pattern);
  files.sort();
  
  if (files.length === 0) {
    console.log('   ⚠️ No desktop top screenshots found');
    return null;
  }
  
  console.log(`   Found ${files.length} pages`);
  
  const rows = Math.ceil(files.length / config.columns);
  const cellWidth = config.thumbWidth + config.padding * 2;
  const cellHeight = config.thumbHeight + config.labelHeight + config.padding * 2;
  
  const canvasWidth = cellWidth * config.columns;
  const canvasHeight = cellHeight * rows;
  
  // Create base canvas
  const canvas = sharp({
    create: {
      width: canvasWidth,
      height: canvasHeight,
      channels: 4,
      background: config.backgroundColor
    }
  });
  
  // Prepare composite operations
  const composites = [];
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const pageName = path.basename(file).replace('_desktop_top.png', '');
    
    const col = i % config.columns;
    const row = Math.floor(i / config.columns);
    const x = col * cellWidth + config.padding;
    const y = row * cellHeight + config.padding;
    
    // Create thumbnail
    const thumb = await createThumbnail(
      file, 
      config.thumbWidth, 
      config.thumbHeight,
      config.borderColor
    );
    
    composites.push({
      input: thumb,
      left: x,
      top: y
    });
    
    // Create label
    const label = await createLabel(
      pageName,
      config.thumbWidth,
      config.labelHeight,
      config.backgroundColor,
      config.labelColor
    );
    
    composites.push({
      input: label,
      left: x,
      top: y + config.thumbHeight + 2
    });
  }
  
  // Composite all images
  const outputPath = path.join(CONFIG.collagesDir, 'master-overview.png');
  await canvas
    .composite(composites)
    .png({ quality: 90 })
    .toFile(outputPath);
  
  console.log(`   ✅ Master collage: ${outputPath}`);
  console.log(`   📐 Size: ${canvasWidth}x${canvasHeight}px (${files.length} pages)`);
  
  return outputPath;
}

/**
 * Generate collage for a single page (all viewports, all positions)
 */
async function generatePageCollage(pageName) {
  const config = CONFIG.pageCollage;
  
  // Collect all screenshots for this page
  const screenshots = {};
  
  for (const viewport of config.viewportOrder) {
    screenshots[viewport] = [];
    
    for (const position of config.positionOrder) {
      const posFile = position.replace('%', 'pct');
      const filename = `${pageName}_${viewport}_${posFile}.png`;
      const filepath = path.join(CONFIG.screenshotsDir, viewport, filename);
      
      try {
        await fs.access(filepath);
        screenshots[viewport].push({ position, filepath });
      } catch {
        // File doesn't exist
      }
    }
  }
  
  // Calculate dimensions
  const numViewports = config.viewportOrder.length;
  const numPositions = config.positionOrder.length;
  
  // Viewport-specific thumb heights (maintain aspect ratio)
  const viewportHeights = {
    desktop: Math.round(config.thumbWidth * (1080 / 1920)),
    tablet: Math.round(config.thumbWidth * (1024 / 768)),
    mobile: Math.round(config.thumbWidth * (812 / 375))
  };
  
  const maxHeight = Math.max(...Object.values(viewportHeights));
  const cellWidth = config.thumbWidth + config.padding * 2;
  const cellHeight = maxHeight + config.labelHeight + config.padding * 2;
  
  const canvasWidth = cellWidth * numPositions + 80; // Extra for viewport labels
  const canvasHeight = (cellHeight + config.labelHeight) * numViewports + 40; // Extra for header
  
  // Create base canvas
  const canvas = sharp({
    create: {
      width: canvasWidth,
      height: canvasHeight,
      channels: 4,
      background: config.backgroundColor
    }
  });
  
  const composites = [];
  
  // Add page title
  const titleLabel = await createLabel(
    `📄 ${pageName}`,
    canvasWidth,
    30,
    config.backgroundColor,
    '#C9A227'
  );
  composites.push({ input: titleLabel, left: 0, top: 5 });
  
  // Add position headers
  for (let p = 0; p < numPositions; p++) {
    const posLabel = await createLabel(
      config.positionOrder[p],
      config.thumbWidth,
      18,
      config.backgroundColor,
      '#888'
    );
    composites.push({
      input: posLabel,
      left: 80 + p * cellWidth,
      top: 35
    });
  }
  
  // Add screenshots
  for (let v = 0; v < numViewports; v++) {
    const viewport = config.viewportOrder[v];
    const viewportY = 55 + v * (cellHeight + config.labelHeight);
    
    // Viewport label (rotated effect with simple text)
    const vpLabel = await createLabel(
      viewport.toUpperCase(),
      70,
      cellHeight,
      '#252525',
      '#C9A227'
    );
    composites.push({
      input: vpLabel,
      left: 5,
      top: viewportY
    });
    
    // Screenshots for this viewport
    const viewportScreenshots = screenshots[viewport];
    
    for (let p = 0; p < numPositions; p++) {
      const posName = config.positionOrder[p];
      const ss = viewportScreenshots.find(s => s.position === posName);
      
      const x = 80 + p * cellWidth + config.padding;
      const y = viewportY + config.padding;
      
      if (ss) {
        const thumb = await createThumbnail(
          ss.filepath,
          config.thumbWidth - 4,
          viewportHeights[viewport] - 4,
          '#444'
        );
        composites.push({ input: thumb, left: x, top: y });
      } else {
        // Missing screenshot placeholder
        const placeholder = await sharp({
          create: {
            width: config.thumbWidth - 4,
            height: viewportHeights[viewport] - 4,
            channels: 4,
            background: { r: 30, g: 30, b: 30, alpha: 1 }
          }
        }).png().toBuffer();
        composites.push({ input: placeholder, left: x, top: y });
      }
    }
  }
  
  // Save collage
  const outputPath = path.join(CONFIG.collagesDir, 'pages', `${pageName}-collage.png`);
  await canvas
    .composite(composites)
    .png({ quality: 90 })
    .toFile(outputPath);
  
  return outputPath;
}

/**
 * Generate all page collages
 */
async function generateAllPageCollages() {
  console.log('\n🖼️  Generating per-page collages (all viewports, all positions)...');
  
  // Get list of unique page names
  const pattern = path.join(CONFIG.screenshotsDir, 'desktop', '*_desktop_top.png');
  const files = await glob(pattern);
  
  const pageNames = files.map(f => 
    path.basename(f).replace('_desktop_top.png', '')
  ).sort();
  
  console.log(`   Found ${pageNames.length} pages to process`);
  
  const results = [];
  
  for (const pageName of pageNames) {
    process.stdout.write(`   Processing: ${pageName}... `);
    try {
      const collagePath = await generatePageCollage(pageName);
      results.push({ page: pageName, path: collagePath, success: true });
      console.log('✅');
    } catch (error) {
      results.push({ page: pageName, error: error.message, success: false });
      console.log(`❌ ${error.message}`);
    }
  }
  
  return results;
}

/**
 * Generate per-device collages (all pages for each device)
 */
async function generateDeviceCollages() {
  console.log('\n🖼️  Generating per-device collages...');
  
  const viewports = ['desktop', 'tablet', 'mobile'];
  const results = [];
  
  for (const viewport of viewports) {
    console.log(`   Processing ${viewport}...`);
    
    const pattern = path.join(CONFIG.screenshotsDir, viewport, `*_${viewport}_top.png`);
    const files = await glob(pattern);
    files.sort();
    
    if (files.length === 0) {
      console.log(`   ⚠️ No ${viewport} screenshots found`);
      continue;
    }
    
    const config = CONFIG.masterCollage;
    const columns = viewport === 'mobile' ? 6 : 5;
    
    const rows = Math.ceil(files.length / columns);
    const cellWidth = config.thumbWidth + config.padding * 2;
    const cellHeight = config.thumbHeight + config.labelHeight + config.padding * 2;
    
    const canvasWidth = cellWidth * columns;
    const canvasHeight = cellHeight * rows + 40;
    
    const canvas = sharp({
      create: {
        width: canvasWidth,
        height: canvasHeight,
        channels: 4,
        background: config.backgroundColor
      }
    });
    
    const composites = [];
    
    // Title
    const title = await createLabel(
      `${viewport.toUpperCase()} - All Pages (Top View)`,
      canvasWidth,
      35,
      config.backgroundColor,
      '#C9A227'
    );
    composites.push({ input: title, left: 0, top: 0 });
    
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const pageName = path.basename(file).replace(`_${viewport}_top.png`, '');
      
      const col = i % columns;
      const row = Math.floor(i / columns);
      const x = col * cellWidth + config.padding;
      const y = 40 + row * cellHeight + config.padding;
      
      const thumb = await createThumbnail(
        file,
        config.thumbWidth,
        config.thumbHeight,
        config.borderColor
      );
      
      composites.push({ input: thumb, left: x, top: y });
      
      const label = await createLabel(
        pageName.substring(0, 20),
        config.thumbWidth,
        config.labelHeight,
        config.backgroundColor,
        config.labelColor
      );
      
      composites.push({
        input: label,
        left: x,
        top: y + config.thumbHeight + 2
      });
    }
    
    const outputPath = path.join(CONFIG.collagesDir, `${viewport}-overview.png`);
    await canvas.composite(composites).png({ quality: 90 }).toFile(outputPath);
    
    results.push({ viewport, path: outputPath, pages: files.length });
    console.log(`   ✅ ${viewport}: ${outputPath} (${files.length} pages)`);
  }
  
  return results;
}

/**
 * Main function
 */
async function main() {
  console.log('🎨 Generating QA Collages');
  console.log('═'.repeat(50));
  
  await setupDirs();
  
  // 1. Master overview collage
  const masterPath = await generateMasterCollage();
  
  // 2. Per-device collages
  const deviceResults = await generateDeviceCollages();
  
  // 3. Per-page collages
  const pageResults = await generateAllPageCollages();
  
  // Summary
  console.log('\n');
  console.log('═'.repeat(50));
  console.log('📊 COLLAGE GENERATION COMPLETE');
  console.log('═'.repeat(50));
  console.log(`\n  Master Overview:    ${masterPath || 'N/A'}`);
  console.log(`  Device Collages:    ${deviceResults.length}`);
  console.log(`  Page Collages:      ${pageResults.filter(r => r.success).length}`);
  console.log(`\n  Output Directory:   ${path.resolve(CONFIG.collagesDir)}`);
  console.log('═'.repeat(50));
  
  // Save manifest
  const manifest = {
    generated: new Date().toISOString(),
    master: masterPath,
    devices: deviceResults,
    pages: pageResults
  };
  
  await fs.writeFile(
    path.join(CONFIG.collagesDir, 'manifest.json'),
    JSON.stringify(manifest, null, 2)
  );
  
  return manifest;
}

main().catch(error => {
  console.error('❌ Collage generation failed:', error);
  process.exit(1);
});
