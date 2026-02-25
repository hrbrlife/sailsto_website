#!/usr/bin/env node
/**
 * AI Agent Review System using OpenRouter
 * Analyzes screenshots and collages for UX issues
 * Uses FREE models from OpenRouter
 */

import fs from 'fs/promises';
import path from 'path';
import { glob } from 'glob';

// Configuration
const CONFIG = {
  screenshotsDir: './screenshots',
  collagesDir: './screenshots/collages',
  reportsDir: './screenshots/reports',
  
  // OpenRouter settings
  openrouter: {
    apiKey: process.env.OPENROUTER_API_KEY,
    baseUrl: 'https://openrouter.ai/api/v1',
    
    // Free vision models on OpenRouter (as of 2024)
    freeVisionModels: [
      'meta-llama/llama-3.2-11b-vision-instruct:free',
      'qwen/qwen-2-vl-7b-instruct:free',
    ],
    
    // Free text models for analysis
    freeTextModels: [
      'google/gemma-2-9b-it:free',
      'meta-llama/llama-3.1-8b-instruct:free',
      'mistralai/mistral-7b-instruct:free',
    ],
    
    // Default model to use
    visionModel: 'meta-llama/llama-3.2-11b-vision-instruct:free',
    textModel: 'google/gemma-2-9b-it:free',
    
    // Rate limiting
    requestDelay: 2000, // ms between requests for free tier
    maxRetries: 3
  },
  
  // Local analysis fallback
  useLocalAnalysis: !process.env.OPENROUTER_API_KEY
};

/**
 * Sleep helper for rate limiting
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Make request to OpenRouter API
 */
async function callOpenRouter(messages, model, isVision = false) {
  if (!CONFIG.openrouter.apiKey) {
    throw new Error('OPENROUTER_API_KEY not set');
  }
  
  const response = await fetch(`${CONFIG.openrouter.baseUrl}/chat/completions`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${CONFIG.openrouter.apiKey}`,
      'Content-Type': 'application/json',
      'HTTP-Referer': 'https://sails.to',
      'X-Title': 'Sails.to QA Testing'
    },
    body: JSON.stringify({
      model: model,
      messages: messages,
      max_tokens: 2000,
      temperature: 0.3
    })
  });
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`OpenRouter API error: ${response.status} - ${error}`);
  }
  
  const data = await response.json();
  return data.choices[0].message.content;
}

/**
 * Analyze image with vision model
 */
async function analyzeImageWithVision(imagePath, prompt) {
  const imageBuffer = await fs.readFile(imagePath);
  const base64Image = imageBuffer.toString('base64');
  const mimeType = imagePath.endsWith('.png') ? 'image/png' : 'image/jpeg';
  
  const messages = [
    {
      role: 'user',
      content: [
        { type: 'text', text: prompt },
        {
          type: 'image_url',
          image_url: {
            url: `data:${mimeType};base64,${base64Image}`
          }
        }
      ]
    }
  ];
  
  return await callOpenRouter(messages, CONFIG.openrouter.visionModel, true);
}

/**
 * UX Review prompt for master collage
 */
function getMasterCollagePrompt() {
  return `You are a QA expert reviewing a collage of website screenshots. This collage shows the first view (top/above-fold) of every page on the site in DESKTOP view.

Analyze this collage and identify:

1. **LOADING ERRORS**: Any pages that appear blank, broken, or show error states (404, 500, etc.)
2. **VISUAL INCONSISTENCIES**: Pages that look different from others (wrong colors, fonts, layout issues)
3. **MISSING ELEMENTS**: Pages missing navigation, headers, or expected content
4. **OBVIOUS BUGS**: Any visual glitches, overlapping elements, or broken layouts

For each issue found, specify:
- Which page/thumbnail (describe its position or content)
- The type of issue
- Severity (critical/high/medium/low)

Respond in JSON format:
{
  "overallAssessment": "brief summary",
  "issuesFound": [
    {
      "page": "page identifier or description",
      "issueType": "loading-error|visual-inconsistency|missing-element|layout-bug",
      "severity": "critical|high|medium|low",
      "description": "what's wrong"
    }
  ],
  "pagesLookingGood": ["list of pages that look correct"],
  "recommendations": ["any general recommendations"]
}`;
}

/**
 * UX Review prompt for per-page collage
 */
function getPageCollagePrompt(pageName) {
  return `You are a UX expert reviewing screenshots of the "${pageName}" page across different devices and scroll positions.

This collage shows:
- Rows: Desktop, Tablet, Mobile viewports
- Columns: Different scroll positions (top, 25%, 50%, 75%, bottom)

Analyze for:

1. **RESPONSIVE ISSUES**: Content that doesn't adapt well between viewports
2. **LAYOUT PROBLEMS**: Elements that overlap, get cut off, or misalign
3. **READABILITY**: Text too small, poor contrast, or illegible on mobile
4. **NAVIGATION**: Menu accessibility issues on different devices
5. **CTA VISIBILITY**: Call-to-action buttons that are hard to find
6. **CONSISTENCY**: Elements that look different across viewports unexpectedly

Respond in JSON format:
{
  "page": "${pageName}",
  "overallScore": 1-10,
  "responsiveIssues": [
    {
      "viewport": "desktop|tablet|mobile",
      "scrollPosition": "top|25%|50%|75%|bottom",
      "issue": "description",
      "severity": "critical|high|medium|low"
    }
  ],
  "positives": ["things done well"],
  "recommendations": ["specific improvements needed"]
}`;
}

/**
 * Local image analysis (fallback when no API key)
 */
async function analyzeImageLocal(imagePath, metadata) {
  const issues = [];
  const filename = path.basename(imagePath);
  
  try {
    const sharp = (await import('sharp')).default;
    const image = sharp(imagePath);
    const stats = await image.stats();
    const meta = await image.metadata();
    
    // Check for mostly blank/white
    const avgBrightness = (stats.channels[0].mean + stats.channels[1].mean + stats.channels[2].mean) / 3;
    if (avgBrightness > 250) {
      issues.push({
        type: 'blank-page',
        severity: 'high',
        description: 'Page appears mostly blank/white - possible loading issue'
      });
    }
    
    // Check for mostly dark (possible CSS issue)
    if (avgBrightness < 15) {
      issues.push({
        type: 'dark-page',
        severity: 'medium',
        description: 'Page appears very dark - check for CSS loading'
      });
    }
    
    // Color variance check
    const colorVariance = stats.channels.reduce((sum, ch) => sum + ch.stdev, 0) / 3;
    if (colorVariance < 8) {
      issues.push({
        type: 'low-variance',
        severity: 'medium',
        description: 'Low visual variance - page may not be rendering correctly'
      });
    }
    
    // File size check
    const fileStats = await fs.stat(imagePath);
    if (fileStats.size < 5000) {
      issues.push({
        type: 'small-file',
        severity: 'high',
        description: 'Very small file size - page may be mostly empty'
      });
    }
    
  } catch (error) {
    issues.push({
      type: 'analysis-error',
      severity: 'low',
      description: `Analysis error: ${error.message}`
    });
  }
  
  return {
    screenshot: filename,
    issues,
    overallScore: issues.length === 0 ? 8 : Math.max(2, 8 - issues.length * 2),
    analysisType: 'local'
  };
}

/**
 * Analyze master collage
 */
async function analyzeMasterCollage() {
  const collagePath = path.join(CONFIG.collagesDir, 'master-overview.png');
  
  try {
    await fs.access(collagePath);
  } catch {
    console.log('   ⚠️ Master collage not found. Run: node generate-collages.js');
    return null;
  }
  
  console.log('   Analyzing master overview collage...');
  
  if (CONFIG.useLocalAnalysis) {
    return await analyzeImageLocal(collagePath, { type: 'master' });
  }
  
  try {
    const response = await analyzeImageWithVision(collagePath, getMasterCollagePrompt());
    
    // Try to parse JSON from response
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const result = JSON.parse(jsonMatch[0]);
      return {
        ...result,
        analysisType: 'ai-vision',
        model: CONFIG.openrouter.visionModel
      };
    }
    
    return {
      rawResponse: response,
      analysisType: 'ai-vision-raw',
      model: CONFIG.openrouter.visionModel
    };
  } catch (error) {
    console.log(`   ⚠️ AI analysis failed: ${error.message}`);
    console.log('   Falling back to local analysis...');
    return await analyzeImageLocal(collagePath, { type: 'master' });
  }
}

/**
 * Analyze per-page collages
 */
async function analyzePageCollages() {
  const pattern = path.join(CONFIG.collagesDir, 'pages', '*-collage.png');
  const collages = await glob(pattern);
  
  if (collages.length === 0) {
    console.log('   ⚠️ No page collages found. Run: node generate-collages.js');
    return [];
  }
  
  console.log(`   Found ${collages.length} page collages`);
  
  const results = [];
  
  for (const collagePath of collages) {
    const pageName = path.basename(collagePath).replace('-collage.png', '');
    process.stdout.write(`   ${pageName}: `);
    
    if (CONFIG.useLocalAnalysis) {
      const result = await analyzeImageLocal(collagePath, { page: pageName });
      result.page = pageName;
      results.push(result);
      console.log(`✅ (local)`);
      continue;
    }
    
    try {
      // Rate limiting for free tier
      await sleep(CONFIG.openrouter.requestDelay);
      
      const response = await analyzeImageWithVision(
        collagePath, 
        getPageCollagePrompt(pageName)
      );
      
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const result = JSON.parse(jsonMatch[0]);
        results.push({
          ...result,
          page: pageName,
          analysisType: 'ai-vision',
          model: CONFIG.openrouter.visionModel
        });
        console.log(`✅ (AI)`);
      } else {
        results.push({
          page: pageName,
          rawResponse: response,
          analysisType: 'ai-vision-raw'
        });
        console.log(`⚠️ (raw)`);
      }
    } catch (error) {
      console.log(`❌ ${error.message.substring(0, 30)}`);
      
      // Fallback to local
      const result = await analyzeImageLocal(collagePath, { page: pageName });
      result.page = pageName;
      results.push(result);
    }
  }
  
  return results;
}

/**
 * Analyze device overview collages
 */
async function analyzeDeviceCollages() {
  const viewports = ['desktop', 'tablet', 'mobile'];
  const results = [];
  
  for (const viewport of viewports) {
    const collagePath = path.join(CONFIG.collagesDir, `${viewport}-overview.png`);
    
    try {
      await fs.access(collagePath);
    } catch {
      continue;
    }
    
    process.stdout.write(`   ${viewport} overview: `);
    
    if (CONFIG.useLocalAnalysis) {
      const result = await analyzeImageLocal(collagePath, { viewport });
      result.viewport = viewport;
      results.push(result);
      console.log(`✅ (local)`);
      continue;
    }
    
    try {
      await sleep(CONFIG.openrouter.requestDelay);
      
      const prompt = `Analyze this ${viewport.toUpperCase()} overview collage showing all pages of a website. 
Identify any pages that look:
1. Broken or showing errors
2. Visually inconsistent with others
3. Missing expected content
4. Having layout issues

Respond in JSON: { "viewport": "${viewport}", "issues": [...], "overall": "summary" }`;
      
      const response = await analyzeImageWithVision(collagePath, prompt);
      
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        results.push({
          ...JSON.parse(jsonMatch[0]),
          viewport,
          analysisType: 'ai-vision'
        });
        console.log(`✅ (AI)`);
      } else {
        results.push({ viewport, rawResponse: response, analysisType: 'ai-raw' });
        console.log(`⚠️`);
      }
    } catch (error) {
      console.log(`❌`);
      const result = await analyzeImageLocal(collagePath, { viewport });
      result.viewport = viewport;
      results.push(result);
    }
  }
  
  return results;
}

/**
 * Main review function
 */
async function runReview() {
  console.log('🤖 Starting AI Agent UX Review');
  console.log('═'.repeat(60));
  
  if (CONFIG.openrouter.apiKey) {
    console.log(`📡 Using OpenRouter API`);
    console.log(`   Vision Model: ${CONFIG.openrouter.visionModel}`);
    console.log(`   Text Model: ${CONFIG.openrouter.textModel}`);
  } else {
    console.log(`📊 Using Local Analysis (no OPENROUTER_API_KEY set)`);
    console.log(`   Set OPENROUTER_API_KEY for AI-powered analysis`);
  }
  
  const allResults = {
    timestamp: new Date().toISOString(),
    analysisMode: CONFIG.useLocalAnalysis ? 'local' : 'openrouter',
    model: CONFIG.useLocalAnalysis ? 'local' : CONFIG.openrouter.visionModel,
    masterCollage: null,
    deviceCollages: [],
    pageCollages: [],
    summary: {
      totalIssues: 0,
      criticalIssues: 0,
      highIssues: 0,
      averageScore: 0
    }
  };
  
  // 1. Analyze master collage
  console.log('\n📊 Master Collage Analysis');
  console.log('─'.repeat(40));
  allResults.masterCollage = await analyzeMasterCollage();
  
  // 2. Analyze device collages
  console.log('\n📱 Device Collage Analysis');
  console.log('─'.repeat(40));
  allResults.deviceCollages = await analyzeDeviceCollages();
  
  // 3. Analyze per-page collages
  console.log('\n📄 Per-Page Collage Analysis');
  console.log('─'.repeat(40));
  allResults.pageCollages = await analyzePageCollages();
  
  // Calculate summary
  let totalScore = 0;
  let scoreCount = 0;
  
  // Count issues from master collage
  if (allResults.masterCollage?.issuesFound) {
    allResults.summary.totalIssues += allResults.masterCollage.issuesFound.length;
    allResults.masterCollage.issuesFound.forEach(i => {
      if (i.severity === 'critical') allResults.summary.criticalIssues++;
      if (i.severity === 'high') allResults.summary.highIssues++;
    });
  }
  
  // Count issues from page collages
  for (const page of allResults.pageCollages) {
    if (page.overallScore) {
      totalScore += page.overallScore;
      scoreCount++;
    }
    if (page.responsiveIssues) {
      allResults.summary.totalIssues += page.responsiveIssues.length;
      page.responsiveIssues.forEach(i => {
        if (i.severity === 'critical') allResults.summary.criticalIssues++;
        if (i.severity === 'high') allResults.summary.highIssues++;
      });
    }
    if (page.issues) {
      allResults.summary.totalIssues += page.issues.length;
    }
  }
  
  allResults.summary.averageScore = scoreCount > 0 
    ? (totalScore / scoreCount).toFixed(1) 
    : 'N/A';
  
  // Save results
  const resultsPath = path.join(CONFIG.reportsDir, 'agent-review-results.json');
  await fs.writeFile(resultsPath, JSON.stringify(allResults, null, 2));
  
  // Print summary
  console.log('\n');
  console.log('═'.repeat(60));
  console.log('📊 AI REVIEW SUMMARY');
  console.log('═'.repeat(60));
  console.log(`   Analysis Mode:     ${allResults.analysisMode}`);
  console.log(`   Model Used:        ${allResults.model}`);
  console.log(`   Pages Analyzed:    ${allResults.pageCollages.length}`);
  console.log(`   Total Issues:      ${allResults.summary.totalIssues}`);
  console.log(`   Critical Issues:   ${allResults.summary.criticalIssues}`);
  console.log(`   High Issues:       ${allResults.summary.highIssues}`);
  console.log(`   Average Score:     ${allResults.summary.averageScore}/10`);
  console.log(`\n   Results saved to:  ${resultsPath}`);
  console.log('═'.repeat(60));
  
  return allResults;
}

// Run review
runReview().catch(error => {
  console.error('❌ Review failed:', error);
  process.exit(1);
});
