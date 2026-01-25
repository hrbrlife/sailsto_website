#!/usr/bin/env node
/**
 * Generate HTML Report with copyable logs and clickable full-res images
 */

import fs from 'fs/promises';
import path from 'path';

const CONFIG = {
  reportsDir: './screenshots/reports',
  screenshotsDir: './screenshots',
  collagesDir: './screenshots/collages'
};

function escapeHtml(text) {
  if (!text) return '';
  return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function shortenUrl(url) {
  if (!url) return '';
  try {
    const u = new URL(url);
    return u.host + (u.pathname.length > 40 ? '...' + u.pathname.slice(-37) : u.pathname);
  } catch { return url.substring(0, 50); }
}

async function generateReport() {
  console.log('📝 Generating HTML Report...\n');
  
  let crawlerResults, reviewResults, collagesIndex;
  
  try {
    crawlerResults = JSON.parse(await fs.readFile(path.join(CONFIG.reportsDir, 'crawler-results.json'), 'utf-8'));
  } catch (e) {
    console.error('❌ No crawler results. Run: npm run test');
    process.exit(1);
  }
  
  try {
    reviewResults = JSON.parse(await fs.readFile(path.join(CONFIG.reportsDir, 'agent-review-results.json'), 'utf-8'));
  } catch (e) { reviewResults = null; }
  
  try {
    collagesIndex = JSON.parse(await fs.readFile(path.join(CONFIG.collagesDir, 'collages-index.json'), 'utf-8'));
  } catch (e) { collagesIndex = null; }
  
  const screenshotsByPage = {};
  for (const s of crawlerResults.screenshots) {
    if (!screenshotsByPage[s.page]) screenshotsByPage[s.page] = {};
    if (!screenshotsByPage[s.page][s.viewport]) screenshotsByPage[s.page][s.viewport] = [];
    screenshotsByPage[s.page][s.viewport].push(s);
  }
  
  const screenshotLogs = crawlerResults.screenshotLogs || {};

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sails.to QA Report</title>
  <style>
    :root { --bg:#0a0a0a; --surface:#1a1a1a; --surface2:#252525; --border:#333; --text:#f5f5f5; --dim:#888; --primary:#C9A227; --success:#22c55e; --warning:#f59e0b; --error:#ef4444; --info:#3b82f6; --purple:#8b5cf6; }
    * { box-sizing:border-box; margin:0; padding:0; }
    body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; background:var(--bg); color:var(--text); line-height:1.6; padding:2rem; }
    .container { max-width:1800px; margin:0 auto; }
    h1 { font-size:2rem; color:var(--primary); margin-bottom:.5rem; }
    h2 { font-size:1.4rem; margin:2rem 0 1rem; border-bottom:1px solid var(--border); padding-bottom:.5rem; }
    h3 { font-size:1.1rem; color:var(--dim); margin:1rem 0; }
    .subtitle { color:var(--dim); margin-bottom:2rem; }
    .summary-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:.75rem; margin-bottom:2rem; }
    .summary-card { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:1rem; }
    .summary-card .label { font-size:.7rem; color:var(--dim); text-transform:uppercase; }
    .summary-card .value { font-size:1.4rem; font-weight:700; margin-top:.25rem; }
    .summary-card.critical .value { color:var(--error); }
    .summary-card.warning .value { color:var(--warning); }
    .summary-card.success .value { color:var(--success); }
    .summary-card.info .value { color:var(--info); }
    .summary-card.purple .value { color:var(--purple); }
    
    .collage-section { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:1.5rem; margin-bottom:1.5rem; }
    .collage-img { max-width:100%; height:auto; cursor:pointer; border-radius:4px; transition:opacity .2s; }
    .collage-img:hover { opacity:.9; }
    
    .page-section { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:1.5rem; margin-bottom:1.5rem; }
    .viewport-tabs { display:flex; gap:.5rem; margin-bottom:1rem; flex-wrap:wrap; }
    .viewport-tab { padding:.5rem 1rem; background:var(--bg); border:1px solid var(--border); border-radius:4px; cursor:pointer; color:var(--text); font-size:.875rem; }
    .viewport-tab:hover,.viewport-tab.active { background:var(--primary); color:var(--bg); border-color:var(--primary); }
    .screenshots-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(400px,1fr)); gap:1.5rem; }
    .screenshot-card { background:var(--bg); border:1px solid var(--border); border-radius:8px; overflow:hidden; }
    .screenshot-header { padding:.75rem; background:var(--surface2); border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; }
    .screenshot-badges { display:flex; gap:.4rem; flex-wrap:wrap; }
    .badge { padding:.15rem .4rem; border-radius:3px; font-size:.65rem; font-weight:600; }
    .badge.network { background:var(--info); color:white; }
    .badge.console { background:var(--purple); color:white; }
    .badge.error { background:var(--error); color:white; }
    .screenshot-card img { width:100%; height:auto; cursor:pointer; transition:opacity .2s; }
    .screenshot-card img:hover { opacity:.9; }
    
    .logs-toggle { width:100%; padding:.6rem; background:var(--surface2); border:none; color:var(--dim); cursor:pointer; font-size:.8rem; border-top:1px solid var(--border); }
    .logs-toggle:hover { background:var(--border); color:var(--text); }
    .screenshot-logs { max-height:0; overflow:hidden; transition:max-height .3s; background:var(--surface2); }
    .screenshot-logs.expanded { max-height:800px; overflow-y:auto; }
    
    .log-section { padding:.75rem; border-top:1px solid var(--border); }
    .log-section-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:.5rem; }
    .log-section-title { font-size:.7rem; color:var(--primary); text-transform:uppercase; font-weight:600; }
    .copy-btn { padding:.2rem .5rem; background:var(--info); color:white; border:none; border-radius:3px; cursor:pointer; font-size:.65rem; }
    .copy-btn:hover { background:#2563eb; }
    .copy-btn.copied { background:var(--success); }
    
    .log-box { font-family:'Monaco','Menlo',monospace; font-size:.7rem; background:var(--bg); border-radius:4px; padding:.5rem; max-height:300px; overflow-y:auto; white-space:pre-wrap; word-break:break-all; border:1px solid var(--border); }
    .log-entry { padding:.2rem 0; border-bottom:1px solid var(--border); }
    .log-entry:last-child { border-bottom:none; }
    .log-entry.error { color:#fca5a5; }
    .log-entry.warning { color:#fcd34d; }
    .log-entry.info { color:#93c5fd; }
    
    .performance-table { width:100%; border-collapse:collapse; background:var(--surface); border-radius:8px; overflow:hidden; margin-bottom:2rem; }
    .performance-table th,.performance-table td { padding:.75rem 1rem; text-align:left; border-bottom:1px solid var(--border); }
    .performance-table th { background:var(--bg); font-weight:600; color:var(--dim); font-size:.8rem; text-transform:uppercase; }
    .perf-good { color:var(--success); }
    .perf-ok { color:var(--warning); }
    .perf-bad { color:var(--error); }
    
    .issues-list { background:var(--surface); border:1px solid var(--border); border-radius:8px; overflow:hidden; margin-bottom:2rem; }
    .issue-item { padding:1rem 1.5rem; border-bottom:1px solid var(--border); display:flex; gap:1rem; }
    .issue-item:last-child { border-bottom:none; }
    .issue-severity { padding:.25rem .5rem; border-radius:4px; font-size:.7rem; font-weight:600; text-transform:uppercase; min-width:60px; text-align:center; }
    .issue-severity.critical { background:var(--error); }
    .issue-severity.high { background:#dc2626; }
    .issue-severity.medium { background:var(--warning); color:#000; }
    .issue-severity.low { background:var(--info); }
    .issue-content { flex:1; }
    .issue-type { font-weight:600; }
    .issue-description { color:var(--dim); margin-top:.25rem; font-size:.85rem; }
    
    .lightbox { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,.97); z-index:1000; justify-content:center; align-items:center; flex-direction:column; }
    .lightbox.active { display:flex; }
    .lightbox img { max-width:95%; max-height:90%; object-fit:contain; }
    .lightbox-close { position:absolute; top:1rem; right:1rem; background:var(--error); color:white; border:none; padding:.5rem 1rem; cursor:pointer; border-radius:4px; }
    .lightbox-info { color:var(--dim); margin-top:1rem; font-size:.9rem; }
    
    @media (max-width:768px) { body { padding:1rem; } .screenshots-grid { grid-template-columns:1fr; } }
  </style>
</head>
<body>
  <div class="container">
    <h1>🚀 Sails.to QA Report</h1>
    <p class="subtitle">Generated: ${new Date().toLocaleString()}</p>
    
    <div class="summary-grid">
      <div class="summary-card info"><div class="label">Pages</div><div class="value">${crawlerResults.summary.totalPages}</div></div>
      <div class="summary-card info"><div class="label">Screenshots</div><div class="value">${crawlerResults.summary.totalScreenshots}</div></div>
      <div class="summary-card purple"><div class="label">Network</div><div class="value">${crawlerResults.summary.totalNetworkRequests || crawlerResults.networkRequests?.length || 0}</div></div>
      <div class="summary-card ${(crawlerResults.consoleLogs?.length || 0) > 0 ? 'warning' : 'success'}"><div class="label">Console</div><div class="value">${crawlerResults.consoleLogs?.length || 0}</div></div>
      <div class="summary-card ${(crawlerResults.networkErrors?.length || 0) > 0 ? 'critical' : 'success'}"><div class="label">Errors</div><div class="value">${crawlerResults.networkErrors?.length || 0}</div></div>
      ${reviewResults ? `<div class="summary-card info"><div class="label">UX Score</div><div class="value">${reviewResults.summary?.averageScore || 'N/A'}/10</div></div>` : ''}
    </div>
    
    ${collagesIndex?.overview ? `
    <h2>🖼️ Overview Collage (Click for Full Size)</h2>
    <div class="collage-section">
      <img class="collage-img" src="../collages/overview-desktop-firstview.png" alt="Overview" onclick="openLightbox(this.src, 'Overview - All Desktop First Views')">
      <p style="color:var(--dim);margin-top:.5rem;font-size:.85rem;">All pages first view - identifies loading errors, 404s, blank pages</p>
    </div>
    ` : ''}
    
    ${reviewResults?.overview?.issues?.length > 0 ? `
    <h2>🔴 AI-Detected Issues (Overview)</h2>
    <div class="issues-list">
      ${reviewResults.overview.issues.map(i => `
        <div class="issue-item">
          <span class="issue-severity ${i.severity}">${i.severity}</span>
          <div class="issue-content">
            <div class="issue-type">${escapeHtml(i.type)}</div>
            <div class="issue-description">${escapeHtml(i.description)} ${i.location ? `(${escapeHtml(i.location)})` : ''}</div>
          </div>
        </div>
      `).join('')}
    </div>
    ` : ''}
    
    <h2>⚡ Performance</h2>
    <table class="performance-table">
      <thead><tr><th>Page</th><th>Viewport</th><th>DOM</th><th>Load</th><th>FCP</th></tr></thead>
      <tbody>
        ${crawlerResults.performance.map(p => `
          <tr>
            <td>${p.page}</td>
            <td>${p.viewport}</td>
            <td>${p.domContentLoaded}ms</td>
            <td class="${p.loadComplete < 500 ? 'perf-good' : p.loadComplete < 2000 ? 'perf-ok' : 'perf-bad'}">${p.loadComplete}ms</td>
            <td>${Math.round(p.firstContentfulPaint)}ms</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    
    <h2>📸 Screenshots by Page</h2>
    ${Object.entries(screenshotsByPage).map(([pageName, viewports]) => {
      const pageReview = reviewResults?.pages?.filter(p => p.page === pageName) || [];
      return `
      <div class="page-section">
        <h3>📄 ${pageName}</h3>
        <div class="viewport-tabs">
          ${Object.keys(viewports).map((v, i) => `<button class="viewport-tab ${i === 0 ? 'active' : ''}" data-viewport="${v}">${v}</button>`).join('')}
        </div>
        ${Object.entries(viewports).map(([viewport, screenshots], vi) => {
          const deviceReview = pageReview.find(r => r.device === viewport);
          return `
          <div class="screenshots-grid viewport-content" data-viewport="${viewport}" style="${vi === 0 ? '' : 'display:none'}">
            ${deviceReview?.issues?.length > 0 ? `
            <div style="grid-column:1/-1;background:var(--surface2);padding:1rem;border-radius:8px;margin-bottom:1rem;">
              <strong style="color:var(--warning);">AI Issues (${viewport}):</strong>
              ${deviceReview.issues.map(i => `<div style="margin-top:.5rem;font-size:.85rem;color:var(--dim);">• [${i.severity}] ${escapeHtml(i.description)}</div>`).join('')}
            </div>
            ` : ''}
            ${screenshots.map(s => {
              const logs = screenshotLogs[s.filename] || {};
              const allConsole = logs.allConsoleLogs || [];
              const allNetwork = logs.allNetworkRequests || [];
              const networkErrors = logs.networkErrors || [];
              
              const consoleText = allConsole.map(l => `[${l.type}] ${l.text}`).join('\\n');
              const networkText = allNetwork.map(r => `${r.method} ${r.resourceType} ${r.url}`).join('\\n');
              const errorsText = networkErrors.map(e => `[${e.status || 'FAIL'}] ${e.url}`).join('\\n');
              
              return `
              <div class="screenshot-card">
                <div class="screenshot-header">
                  <span>${s.scrollPosition}</span>
                  <div class="screenshot-badges">
                    ${allNetwork.length > 0 ? `<span class="badge network">${allNetwork.length} req</span>` : ''}
                    ${allConsole.length > 0 ? `<span class="badge console">${allConsole.length} log</span>` : ''}
                    ${networkErrors.length > 0 ? `<span class="badge error">${networkErrors.length} err</span>` : ''}
                  </div>
                </div>
                <img src="../${viewport}/${s.filename}" alt="${s.page} ${viewport} ${s.scrollPosition}" loading="lazy" onclick="openLightbox(this.src, '${s.page} - ${viewport} - ${s.scrollPosition}')">
                <button class="logs-toggle" onclick="toggleLogs(this)">▼ Show Logs (${allConsole.length} console, ${allNetwork.length} network)</button>
                <div class="screenshot-logs">
                  <div class="log-section">
                    <div class="log-section-header">
                      <span class="log-section-title">Console Logs (${allConsole.length})</span>
                      <button class="copy-btn" onclick="copyLogs(this, \`${escapeHtml(consoleText.replace(/`/g, '\\`'))}\`)">📋 Copy</button>
                    </div>
                    <div class="log-box">${allConsole.length > 0 ? allConsole.map(l => `<div class="log-entry ${l.type}">[${l.type}] ${escapeHtml(l.text?.substring(0, 300))}</div>`).join('') : '<div style="color:var(--dim)">No console logs</div>'}</div>
                  </div>
                  <div class="log-section">
                    <div class="log-section-header">
                      <span class="log-section-title">Network Requests (${allNetwork.length})</span>
                      <button class="copy-btn" onclick="copyLogs(this, \`${escapeHtml(networkText.replace(/`/g, '\\`'))}\`)">📋 Copy</button>
                    </div>
                    <div class="log-box">${allNetwork.length > 0 ? allNetwork.map(r => `<div class="log-entry">${r.method} [${r.resourceType}] ${escapeHtml(shortenUrl(r.url))}</div>`).join('') : '<div style="color:var(--dim)">No requests</div>'}</div>
                  </div>
                  ${networkErrors.length > 0 ? `
                  <div class="log-section">
                    <div class="log-section-header">
                      <span class="log-section-title" style="color:var(--error)">Network Errors (${networkErrors.length})</span>
                      <button class="copy-btn" onclick="copyLogs(this, \`${escapeHtml(errorsText.replace(/`/g, '\\`'))}\`)">📋 Copy</button>
                    </div>
                    <div class="log-box">${networkErrors.map(e => `<div class="log-entry error">[${e.status || 'FAIL'}] ${escapeHtml(e.url)}</div>`).join('')}</div>
                  </div>
                  ` : ''}
                </div>
              </div>
              `;
            }).join('')}
          </div>
          `;
        }).join('')}
      </div>
      `;
    }).join('')}
    
    ${crawlerResults.issues.length > 0 ? `
    <h2>⚠️ UI Issues (${crawlerResults.issues.length})</h2>
    <div class="issues-list">
      ${crawlerResults.issues.slice(0, 50).map(i => `
        <div class="issue-item">
          <span class="issue-severity ${i.severity}">${i.severity}</span>
          <div class="issue-content">
            <div class="issue-type">${i.type}</div>
            <div class="issue-description">${escapeHtml(i.description || i.text || i.src || '')}</div>
          </div>
        </div>
      `).join('')}
    </div>
    ` : ''}
  </div>
  
  <div class="lightbox" id="lightbox" onclick="if(event.target===this)closeLightbox()">
    <button class="lightbox-close" onclick="closeLightbox()">✕ Close (ESC)</button>
    <img id="lightbox-img" src="">
    <div class="lightbox-info" id="lightbox-info"></div>
  </div>
  
  <script>
    document.querySelectorAll('.page-section').forEach(section => {
      const tabs = section.querySelectorAll('.viewport-tab');
      const contents = section.querySelectorAll('.viewport-content');
      tabs.forEach(tab => {
        tab.addEventListener('click', () => {
          tabs.forEach(t => t.classList.remove('active'));
          tab.classList.add('active');
          contents.forEach(c => c.style.display = c.dataset.viewport === tab.dataset.viewport ? 'grid' : 'none');
        });
      });
    });
    
    function toggleLogs(btn) {
      const logs = btn.nextElementSibling;
      logs.classList.toggle('expanded');
      btn.textContent = logs.classList.contains('expanded') ? '▲ Hide Logs' : btn.textContent.replace('▲', '▼').replace('Hide', 'Show');
    }
    
    function copyLogs(btn, text) {
      navigator.clipboard.writeText(text.replace(/\\\\n/g, '\\n')).then(() => {
        btn.textContent = '✓ Copied!';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = '📋 Copy'; btn.classList.remove('copied'); }, 2000);
      });
    }
    
    function openLightbox(src, info) {
      document.getElementById('lightbox-img').src = src;
      document.getElementById('lightbox-info').textContent = info || '';
      document.getElementById('lightbox').classList.add('active');
    }
    
    function closeLightbox() { document.getElementById('lightbox').classList.remove('active'); }
    
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(); });
  </script>
</body>
</html>`;

  await fs.writeFile(path.join(CONFIG.reportsDir, 'qa-report.html'), html);
  console.log('✅ Report generated: screenshots/reports/qa-report.html');
  console.log(`   Screenshots: ${crawlerResults.summary.totalScreenshots}`);
  console.log(`   With collages: ${collagesIndex ? 'Yes' : 'No'}`);
  console.log(`   With AI review: ${reviewResults ? 'Yes' : 'No'}`);
}

generateReport().catch(e => { console.error('❌', e); process.exit(1); });
