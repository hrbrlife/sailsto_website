#!/usr/bin/env node
/**
 * AI Agent Review using OpenRouter Free Models
 */

import fs from 'fs/promises';
import path from 'path';

const CONFIG = {
  collagesDir: './screenshots/collages',
  reportsDir: './screenshots/reports',
  openrouterApiKey: process.env.OPENROUTER_API_KEY || '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',
  visionModel: 'google/gemma-3-27b-it:free'
};

const UX_PROMPT = `Analyze this website screenshot collage for UX issues:

1. LOADING ERRORS: Blank pages, 404s, broken images, missing CSS
2. VISUAL CONSISTENCY: Colors, typography, spacing, button styles
3. RESPONSIVE: Content fits, readable text, proper scaling
4. NAVIGATION: Clear structure, visible CTAs, proper hierarchy
5. ACCESSIBILITY: Color contrast, text size, interactive elements

Respond with JSON only:
{"issues":[{"type":"category","severity":"critical|high|medium|low","description":"issue","location":"where"}],"score":1-10,"summary":"assessment"}`;

async function callOpenRouter(imageBase64, prompt) {
  const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${CONFIG.openrouterApiKey}`,
      'Content-Type': 'application/json',
      'HTTP-Referer': 'https://sails.to',
      'X-Title': 'Sails.to QA'
    },
    body: JSON.stringify({
      model: CONFIG.visionModel,
      messages: [{
        role: 'user',
        content: [
          { type: 'text', text: prompt },
          { type: 'image_url', image_url: { url: `data:image/png;base64,${imageBase64}` } }
        ]
      }],
      max_tokens: 2000,
      temperature: 0.3
    })
  });
  
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  const data = await response.json();
  return data.choices[0]?.message?.content || '';
}

function parseResponse(response) {
  try {
    const match = response.match(/\{[\s\S]*\}/);
    if (match) return JSON.parse(match[0]);
  } catch (e) {}
  return { issues: [], score: 5, summary: response.substring(0, 500), parseError: true };
}

async function analyzeLocal(imagePath) {
  const sharp = (await import('sharp')).default;
  const stats = await sharp(imagePath).stats();
  const issues = [];
  const avg = (stats.channels[0].mean + stats.channels[1].mean + stats.channels[2].mean) / 3;
  
  if (avg > 250) issues.push({ type: 'loading-error', severity: 'critical', description: 'Page appears blank', location: 'entire page' });
  if (avg < 20) issues.push({ type: 'loading-error', severity: 'medium', description: 'Page very dark', location: 'entire page' });
  
  return { issues, score: issues.length === 0 ? 8 : Math.max(1, 8 - issues.length * 2), summary: `${issues.length} issues found`, analysisType: 'local' };
}

async function runReview() {
  console.log('🤖 AI Agent UX Review (OpenRouter)');
  console.log('═'.repeat(50));
  console.log(`Model: ${CONFIG.visionModel}\n`);
  
  let collagesIndex;
  try {
    collagesIndex = JSON.parse(await fs.readFile(path.join(CONFIG.collagesDir, 'collages-index.json'), 'utf-8'));
  } catch (e) {
    console.error('❌ No collages found. Run: npm run collages');
    process.exit(1);
  }
  
  const results = { overview: null, pages: [], summary: { totalAnalyzed: 0, totalIssues: 0, criticalIssues: 0, averageScore: 0 } };
  let totalScore = 0, scoredCount = 0;
  
  // Analyze overview
  if (collagesIndex.overview) {
    console.log('🔍 Analyzing Overview Collage...');
    try {
      const base64 = (await fs.readFile(collagesIndex.overview)).toString('base64');
      const response = await callOpenRouter(base64, `This shows ALL pages first view. Find loading errors, 404s, blank pages, broken layouts.\n\n${UX_PROMPT}`);
      results.overview = { type: 'overview', ...parseResponse(response) };
      console.log(`  Score: ${results.overview.score}/10, Issues: ${results.overview.issues?.length || 0}`);
      results.summary.totalAnalyzed++;
      results.summary.totalIssues += results.overview.issues?.length || 0;
    } catch (e) {
      console.log(`  ❌ ${e.message}`);
      results.overview = await analyzeLocal(collagesIndex.overview);
    }
  }
  
  // Analyze device collages
  console.log('\n📱 Analyzing Page Collages...');
  for (const collage of collagesIndex.deviceCollages || []) {
    await new Promise(r => setTimeout(r, 1500)); // Rate limit
    process.stdout.write(`  ${collage.page}/${collage.device}: `);
    
    try {
      const base64 = (await fs.readFile(collage.path)).toString('base64');
      const response = await callOpenRouter(base64, `Page "${collage.page}" on ${collage.device} at different scroll positions.\n\n${UX_PROMPT}`);
      const result = { type: 'page', page: collage.page, device: collage.device, ...parseResponse(response) };
      results.pages.push(result);
      
      console.log(`${result.score}/10, ${result.issues?.length || 0} issues`);
      results.summary.totalAnalyzed++;
      results.summary.totalIssues += result.issues?.length || 0;
      results.summary.criticalIssues += (result.issues || []).filter(i => i.severity === 'critical').length;
      if (result.score) { totalScore += result.score; scoredCount++; }
    } catch (e) {
      console.log(`❌ ${e.message}`);
      const local = await analyzeLocal(collage.path);
      results.pages.push({ type: 'page', page: collage.page, device: collage.device, ...local });
    }
  }
  
  results.summary.averageScore = scoredCount > 0 ? (totalScore / scoredCount).toFixed(1) : 'N/A';
  
  await fs.writeFile(path.join(CONFIG.reportsDir, 'agent-review-results.json'), JSON.stringify(results, null, 2));
  
  console.log('\n═'.repeat(50));
  console.log('📊 AI REVIEW SUMMARY');
  console.log(`  Analyzed: ${results.summary.totalAnalyzed} | Issues: ${results.summary.totalIssues} | Critical: ${results.summary.criticalIssues} | Score: ${results.summary.averageScore}/10`);
  
  return results;
}

runReview().catch(e => { console.error('❌', e); process.exit(1); });
