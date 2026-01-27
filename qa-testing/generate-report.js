#!/usr/bin/env node
/**
 * Generate HTML Report from QA Results
 * With console logs and network requests per screenshot
 */

import fs from 'fs/promises';
import path from 'path';

const CONFIG = {
  reportsDir: './screenshots/reports',
  screenshotsDir: './screenshots'
};

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
  if (!text) return '';
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Shorten URL for display
 */
function shortenUrl(url) {
  if (!url) return '';
  try {
    const u = new URL(url);
    let path = u.pathname;
    if (path.length > 50) {
      path = '...' + path.slice(-47);
    }
    return u.host + path;
  } catch {
    return url.substring(0, 60);
  }
}

/**
 * Generate HTML report
 */
async function generateReport() {
  console.log('📝 Generating HTML Report...\n');
  
  // Load results
  let crawlerResults, reviewResults;
  
  try {
    crawlerResults = JSON.parse(
      await fs.readFile(path.join(CONFIG.reportsDir, 'crawler-results.json'), 'utf-8')
    );
  } catch (e) {
    console.error('❌ No crawler results found. Run: npm run test');
    process.exit(1);
  }
  
  try {
    reviewResults = JSON.parse(
      await fs.readFile(path.join(CONFIG.reportsDir, 'agent-review-results.json'), 'utf-8')
    );
  } catch (e) {
    reviewResults = null;
    console.log('⚠️  No review results found. Run: npm run review');
  }
  
  // Group screenshots by page and viewport
  const screenshotsByPage = {};
  for (const s of crawlerResults.screenshots) {
    if (!screenshotsByPage[s.page]) {
      screenshotsByPage[s.page] = {};
    }
    if (!screenshotsByPage[s.page][s.viewport]) {
      screenshotsByPage[s.page][s.viewport] = [];
    }
    screenshotsByPage[s.page][s.viewport].push(s);
  }
  
  // Get screenshot logs
  const screenshotLogs = crawlerResults.screenshotLogs || {};
  
  // Generate HTML
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sails.to QA Report - ${new Date().toLocaleDateString()}</title>
  <style>
    :root {
      --bg: #0a0a0a;
      --surface: #1a1a1a;
      --surface-2: #252525;
      --border: #333;
      --text: #f5f5f5;
      --text-dim: #888;
      --primary: #C9A227;
      --success: #22c55e;
      --warning: #f59e0b;
      --error: #ef4444;
      --info: #3b82f6;
      --purple: #8b5cf6;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 2rem;
    }
    
    .container { max-width: 1800px; margin: 0 auto; }
    
    h1 { font-size: 2rem; margin-bottom: 0.5rem; color: var(--primary); }
    h2 { font-size: 1.5rem; margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }
    h3 { font-size: 1.2rem; margin: 1.5rem 0 1rem; color: var(--text-dim); }
    
    .subtitle { color: var(--text-dim); margin-bottom: 2rem; }
    
    .summary-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 0.75rem;
      margin-bottom: 2rem;
    }
    
    .summary-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1rem;
    }
    
    .summary-card .label {
      font-size: 0.7rem;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    .summary-card .value {
      font-size: 1.5rem;
      font-weight: 700;
      margin-top: 0.25rem;
    }
    
    .summary-card.critical .value { color: var(--error); }
    .summary-card.warning .value { color: var(--warning); }
    .summary-card.success .value { color: var(--success); }
    .summary-card.info .value { color: var(--info); }
    .summary-card.purple .value { color: var(--purple); }
    
    .page-section {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.5rem;
      margin-bottom: 1.5rem;
    }
    
    .page-title { font-size: 1.25rem; margin-bottom: 1rem; }
    
    .viewport-tabs {
      display: flex;
      gap: 0.5rem;
      margin-bottom: 1rem;
      flex-wrap: wrap;
    }
    
    .viewport-tab {
      padding: 0.5rem 1rem;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 4px;
      cursor: pointer;
      color: var(--text);
      font-size: 0.875rem;
    }
    
    .viewport-tab:hover, .viewport-tab.active {
      background: var(--primary);
      color: var(--bg);
      border-color: var(--primary);
    }
    
    .screenshots-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
      gap: 1.5rem;
    }
    
    .screenshot-card {
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }
    
    .screenshot-card img {
      width: 100%;
      height: auto;
      display: block;
      cursor: pointer;
      transition: opacity 0.2s;
    }
    
    .screenshot-card img:hover { opacity: 0.9; }
    
    .screenshot-header {
      padding: 0.75rem;
      font-size: 0.875rem;
      color: var(--text-dim);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: var(--surface-2);
      border-bottom: 1px solid var(--border);
    }
    
    .screenshot-badges { display: flex; gap: 0.4rem; flex-wrap: wrap; }
    
    .badge {
      padding: 0.15rem 0.4rem;
      border-radius: 3px;
      font-size: 0.65rem;
      font-weight: 600;
    }
    
    .badge.network { background: var(--info); color: white; }
    .badge.console { background: var(--purple); color: white; }
    .badge.error { background: var(--error); color: white; }
    .badge.warn { background: var(--warning); color: black; }
    
    .logs-toggle {
      width: 100%;
      padding: 0.6rem;
      background: var(--surface-2);
      border: none;
      color: var(--text-dim);
      cursor: pointer;
      font-size: 0.8rem;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      border-top: 1px solid var(--border);
    }
    
    .logs-toggle:hover { background: var(--border); color: var(--text); }
    
    .screenshot-logs {
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.3s ease;
      background: var(--surface-2);
    }
    
    .screenshot-logs.expanded {
      max-height: 800px;
      overflow-y: auto;
    }
    
    .log-section {
      padding: 0.75rem;
      border-top: 1px solid var(--border);
    }
    
    .log-section:first-child { border-top: none; }
    
    .log-section-title {
      font-size: 0.7rem;
      color: var(--primary);
      text-transform: uppercase;
      margin-bottom: 0.5rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .log-count {
      background: var(--border);
      padding: 0.1rem 0.4rem;
      border-radius: 10px;
      font-size: 0.65rem;
    }
    
    .log-entry {
      font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
      font-size: 0.7rem;
      padding: 0.3rem 0.5rem;
      margin: 0.25rem 0;
      background: var(--bg);
      border-radius: 3px;
      word-break: break-all;
      border-left: 3px solid var(--border);
    }
    
    .log-entry.error { border-left-color: var(--error); background: rgba(239,68,68,0.1); }
    .log-entry.warning { border-left-color: var(--warning); background: rgba(245,158,11,0.1); }
    .log-entry.info { border-left-color: var(--info); }
    .log-entry.log { border-left-color: var(--text-dim); }
    .log-entry.debug { border-left-color: var(--purple); }
    
    .log-type {
      display: inline-block;
      min-width: 45px;
      color: var(--text-dim);
      font-weight: 600;
      margin-right: 0.5rem;
    }
    
    .network-entry {
      display: flex;
      gap: 0.5rem;
      align-items: center;
      font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
      font-size: 0.7rem;
      padding: 0.3rem 0.5rem;
      margin: 0.25rem 0;
      background: var(--bg);
      border-radius: 3px;
      border-left: 3px solid var(--purple);
    }
    
    .network-entry.failed {
      border-left-color: var(--error);
      background: rgba(239,68,68,0.1);
    }
    
    .network-method {
      background: var(--info);
      color: white;
      padding: 0.1rem 0.3rem;
      border-radius: 2px;
      font-size: 0.6rem;
      font-weight: 600;
    }
    
    .network-type {
      color: var(--text-dim);
      font-size: 0.6rem;
      min-width: 60px;
    }
    
    .network-url {
      color: var(--info);
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    
    .network-status {
      padding: 0.1rem 0.3rem;
      border-radius: 2px;
      font-size: 0.6rem;
      font-weight: 600;
    }
    
    .network-status.ok { background: var(--success); color: white; }
    .network-status.error { background: var(--error); color: white; }
    
    .performance-table {
      width: 100%;
      border-collapse: collapse;
      background: var(--surface);
      border-radius: 8px;
      overflow: hidden;
      margin-bottom: 2rem;
    }
    
    .performance-table th, .performance-table td {
      padding: 0.75rem 1rem;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }
    
    .performance-table th {
      background: var(--bg);
      font-weight: 600;
      color: var(--text-dim);
      font-size: 0.8rem;
      text-transform: uppercase;
    }
    
    .performance-table tr:last-child td { border-bottom: none; }
    
    .perf-good { color: var(--success); }
    .perf-ok { color: var(--warning); }
    .perf-bad { color: var(--error); }
    
    .issues-list {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
      margin-bottom: 2rem;
    }
    
    .issue-item {
      padding: 1rem 1.5rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      gap: 1rem;
      align-items: flex-start;
    }
    
    .issue-item:last-child { border-bottom: none; }
    
    .issue-severity {
      padding: 0.25rem 0.5rem;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      min-width: 60px;
      text-align: center;
    }
    
    .issue-severity.critical { background: var(--error); }
    .issue-severity.high { background: #dc2626; }
    .issue-severity.medium { background: var(--warning); color: #000; }
    .issue-severity.low { background: var(--info); }
    
    .issue-content { flex: 1; }
    .issue-type { font-weight: 600; font-size: 0.9rem; }
    .issue-description { color: var(--text-dim); margin-top: 0.25rem; font-size: 0.85rem; }
    .issue-meta { font-size: 0.8rem; color: var(--text-dim); margin-top: 0.5rem; }
    
    .lightbox {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.95);
      z-index: 1000;
      justify-content: center;
      align-items: center;
    }
    
    .lightbox.active { display: flex; }
    
    .lightbox img {
      max-width: 95%;
      max-height: 95%;
      object-fit: contain;
    }
    
    .lightbox-close {
      position: absolute;
      top: 1rem;
      right: 1rem;
      background: var(--error);
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      cursor: pointer;
      border-radius: 4px;
      font-size: 0.9rem;
    }
    
    .no-data {
      padding: 1rem;
      text-align: center;
      color: var(--text-dim);
      font-size: 0.8rem;
    }
    
    @media (max-width: 768px) {
      body { padding: 1rem; }
      .summary-grid { grid-template-columns: repeat(3, 1fr); }
      .screenshots-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🚀 Sails.to QA Report</h1>
    <p class="subtitle">Generated: ${new Date().toLocaleString()}</p>
    
    <!-- Summary Cards -->
    <div class="summary-grid">
      <div class="summary-card info">
        <div class="label">Pages</div>
        <div class="value">${crawlerResults.summary.totalPages}</div>
      </div>
      <div class="summary-card info">
        <div class="label">Screenshots</div>
        <div class="value">${crawlerResults.summary.totalScreenshots}</div>
      </div>
      <div class="summary-card purple">
        <div class="label">Network Reqs</div>
        <div class="value">${crawlerResults.summary.totalNetworkRequests || crawlerResults.networkRequests?.length || 0}</div>
      </div>
      <div class="summary-card ${(crawlerResults.consoleLogs?.length || 0) > 0 ? 'warning' : 'success'}">
        <div class="label">Console Logs</div>
        <div class="value">${crawlerResults.summary.totalConsoleMessages || crawlerResults.consoleLogs?.length || 0}</div>
      </div>
      <div class="summary-card ${(crawlerResults.networkErrors?.length || 0) > 0 ? 'critical' : 'success'}">
        <div class="label">Net Errors</div>
        <div class="value">${crawlerResults.summary.totalNetworkErrors || crawlerResults.networkErrors?.length || 0}</div>
      </div>
      <div class="summary-card ${crawlerResults.summary.totalIssues > 0 ? 'warning' : 'success'}">
        <div class="label">UI Issues</div>
        <div class="value">${crawlerResults.summary.totalIssues}</div>
      </div>
      ${reviewResults ? `
      <div class="summary-card info">
        <div class="label">UX Score</div>
        <div class="value">${reviewResults.summary.averageScore}/10</div>
      </div>
      ` : ''}
    </div>
    
    <!-- Network Errors Section -->
    ${(crawlerResults.networkErrors?.length || 0) > 0 ? `
      <h2>🔴 Network Errors (${crawlerResults.networkErrors.length})</h2>
      <div class="issues-list">
        ${crawlerResults.networkErrors.slice(0, 20).map(err => `
          <div class="issue-item">
            <span class="issue-severity critical">${err.status || 'FAIL'}</span>
            <div class="issue-content">
              <div class="issue-type">${err.resourceType || 'request'}</div>
              <div class="issue-description">${escapeHtml(err.url)}</div>
              <div class="issue-meta">Page: ${err.page} | ${err.failure || err.statusText || ''}</div>
            </div>
          </div>
        `).join('')}
      </div>
    ` : ''}
    
    <!-- Performance Metrics -->
    <h2>⚡ Performance Metrics</h2>
    <table class="performance-table">
      <thead>
        <tr>
          <th>Page</th>
          <th>Viewport</th>
          <th>DOM Ready</th>
          <th>Load</th>
          <th>FP</th>
          <th>FCP</th>
        </tr>
      </thead>
      <tbody>
        ${crawlerResults.performance.map(p => {
          const loadClass = p.loadComplete < 500 ? 'perf-good' : p.loadComplete < 2000 ? 'perf-ok' : 'perf-bad';
          return `
            <tr>
              <td>${p.page}</td>
              <td>${p.viewport}</td>
              <td>${p.domContentLoaded}ms</td>
              <td class="${loadClass}">${p.loadComplete}ms</td>
              <td>${Math.round(p.firstPaint)}ms</td>
              <td>${Math.round(p.firstContentfulPaint)}ms</td>
            </tr>
          `;
        }).join('')}
      </tbody>
    </table>
    
    <!-- Page Screenshots with Logs -->
    <h2>📸 Screenshots with Console & Network Logs</h2>
    ${Object.entries(screenshotsByPage).map(([pageName, viewports]) => `
      <div class="page-section">
        <h3 class="page-title">📄 ${pageName}</h3>
        <div class="viewport-tabs">
          ${Object.keys(viewports).map((v, i) => `<button class="viewport-tab ${i === 0 ? 'active' : ''}" data-viewport="${v}">${v}</button>`).join('')}
        </div>
        ${Object.entries(viewports).map(([viewport, screenshots], vi) => `
          <div class="screenshots-grid viewport-content" data-viewport="${viewport}" style="${vi === 0 ? '' : 'display:none'}">
            ${screenshots.map(s => {
              const logs = screenshotLogs[s.filename] || {};
              const consoleLogs = logs.consoleLogs || [];
              const networkReqs = logs.networkRequests || [];
              const networkErrors = logs.networkErrors || [];
              const allConsole = logs.allConsoleLogs || [];
              const allNetwork = logs.allNetworkRequests || [];
              
              const errorCount = consoleLogs.filter(l => l.type === 'error').length + networkErrors.length;
              const warnCount = consoleLogs.filter(l => l.type === 'warning').length;
              
              return `
              <div class="screenshot-card">
                <div class="screenshot-header">
                  <span>${s.scrollPosition}</span>
                  <div class="screenshot-badges">
                    ${allNetwork.length > 0 ? `<span class="badge network">${allNetwork.length} reqs</span>` : ''}
                    ${allConsole.length > 0 ? `<span class="badge console">${allConsole.length} logs</span>` : ''}
                    ${errorCount > 0 ? `<span class="badge error">${errorCount} err</span>` : ''}
                    ${warnCount > 0 ? `<span class="badge warn">${warnCount} warn</span>` : ''}
                  </div>
                </div>
                <img src="../${viewport}/${s.filename}" alt="${s.page} - ${viewport} - ${s.scrollPosition}" loading="lazy" onclick="openLightbox(this.src)">
                <button class="logs-toggle" onclick="toggleLogs(this)">
                  ▼ Show Console & Network Logs (${allConsole.length} logs, ${allNetwork.length} requests)
                </button>
                <div class="screenshot-logs">
                  ${allConsole.length > 0 ? `
                    <div class="log-section">
                      <div class="log-section-title">
                        Console Logs <span class="log-count">${allConsole.length}</span>
                      </div>
                      ${allConsole.map(log => `
                        <div class="log-entry ${log.type}">
                          <span class="log-type">[${log.type}]</span>
                          ${escapeHtml(log.text?.substring(0, 500))}
                        </div>
                      `).join('')}
                    </div>
                  ` : '<div class="log-section"><div class="no-data">No console logs</div></div>'}
                  
                  ${allNetwork.length > 0 ? `
                    <div class="log-section">
                      <div class="log-section-title">
                        Network Requests <span class="log-count">${allNetwork.length}</span>
                      </div>
                      ${allNetwork.map(req => `
                        <div class="network-entry">
                          <span class="network-method">${req.method}</span>
                          <span class="network-type">${req.resourceType}</span>
                          <span class="network-url" title="${escapeHtml(req.url)}">${escapeHtml(shortenUrl(req.url))}</span>
                        </div>
                      `).join('')}
                    </div>
                  ` : '<div class="log-section"><div class="no-data">No network requests captured at this position</div></div>'}
                  
                  ${networkErrors.length > 0 ? `
                    <div class="log-section">
                      <div class="log-section-title">
                        Network Errors <span class="log-count">${networkErrors.length}</span>
                      </div>
                      ${networkErrors.map(err => `
                        <div class="network-entry failed">
                          <span class="network-status error">${err.status || 'FAIL'}</span>
                          <span class="network-type">${err.resourceType || 'request'}</span>
                          <span class="network-url" title="${escapeHtml(err.url)}">${escapeHtml(shortenUrl(err.url))}</span>
                        </div>
                      `).join('')}
                    </div>
                  ` : ''}
                </div>
              </div>
              `;
            }).join('')}
          </div>
        `).join('')}
      </div>
    `).join('')}
    
    <!-- UI Issues -->
    ${crawlerResults.issues.length > 0 ? `
      <h2>⚠️ UI Issues (${crawlerResults.issues.length})</h2>
      <div class="issues-list">
        ${crawlerResults.issues.slice(0, 50).map(issue => `
          <div class="issue-item">
            <span class="issue-severity ${issue.severity}">${issue.severity}</span>
            <div class="issue-content">
              <div class="issue-type">${issue.type}</div>
              <div class="issue-description">${escapeHtml(issue.description || issue.element || issue.src || issue.text || '')}</div>
              <div class="issue-meta">Page: ${issue.page || 'N/A'} | Viewport: ${issue.viewport || 'N/A'}</div>
            </div>
          </div>
        `).join('')}
      </div>
    ` : '<div class="no-issues">✅ No UI issues found!</div>'}
    
  </div>
  
  <!-- Lightbox -->
  <div class="lightbox" id="lightbox" onclick="closeLightbox()">
    <button class="lightbox-close" onclick="closeLightbox()">✕ Close</button>
    <img id="lightbox-img" src="" alt="Full size screenshot">
  </div>
  
  <script>
    // Viewport tab switcher
    document.querySelectorAll('.page-section').forEach(section => {
      const tabs = section.querySelectorAll('.viewport-tab');
      const contents = section.querySelectorAll('.viewport-content');
      
      tabs.forEach(tab => {
        tab.addEventListener('click', () => {
          const viewport = tab.dataset.viewport;
          tabs.forEach(t => t.classList.remove('active'));
          tab.classList.add('active');
          contents.forEach(c => {
            c.style.display = c.dataset.viewport === viewport ? 'grid' : 'none';
          });
        });
      });
    });
    
    // Toggle logs
    function toggleLogs(btn) {
      const logs = btn.nextElementSibling;
      logs.classList.toggle('expanded');
      btn.textContent = logs.classList.contains('expanded') 
        ? '▲ Hide Console & Network Logs' 
        : btn.textContent.replace('▲', '▼').replace('Hide', 'Show');
    }
    
    // Lightbox
    function openLightbox(src) {
      document.getElementById('lightbox-img').src = src;
      document.getElementById('lightbox').classList.add('active');
    }
    
    function closeLightbox() {
      document.getElementById('lightbox').classList.remove('active');
    }
    
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeLightbox();
    });
  </script>
</body>
</html>`;

  const reportPath = path.join(CONFIG.reportsDir, 'qa-report.html');
  await fs.writeFile(reportPath, html);
  
  console.log(`✅ Report generated: ${reportPath}`);
  console.log(`\n📊 Summary:`);
  console.log(`   Screenshots: ${crawlerResults.summary.totalScreenshots}`);
  console.log(`   Network Requests: ${crawlerResults.summary.totalNetworkRequests || crawlerResults.networkRequests?.length || 0}`);
  console.log(`   Console Logs: ${crawlerResults.summary.totalConsoleMessages || crawlerResults.consoleLogs?.length || 0}`);
  console.log(`   Network Errors: ${crawlerResults.summary.totalNetworkErrors || crawlerResults.networkErrors?.length || 0}`);
  console.log(`\nOpen in browser: file://${path.resolve(reportPath)}`);
  
  return reportPath;
}

generateReport().catch(error => {
  console.error('❌ Report generation failed:', error);
  process.exit(1);
});
