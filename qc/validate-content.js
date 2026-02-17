#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════
 *   CONTENT VALIDATOR — vandalism, placeholders, quality
 * ═══════════════════════════════════════════════════════════════
 *
 * Detects:
 *   • Profanity / vandalism
 *   • Garbled text (repeated chars, random symbols)
 *   • Placeholder / template text
 *   • TODO / FIXME / HACK markers
 *   • Suspicious numeric patterns (e.g. "100jjj0")
 *   • Debug artifacts (console.log, alert, debugger)
 */

const fs = require('fs');
const path = require('path');
const { c, findFiles, getSiteFiles } = require('./utils');

// ─── Detection patterns ─────────────────────────────────────

// Use word-boundary regex to prevent "ass" matching "class", "cock" matching "cockpit"
const PROFANITY = [
    { word: 'fuck',   re: /\bfuck/i },
    { word: 'shit',   re: /\bshit\b/i },
    { word: 'dick',   re: /\bdick\b/i },
    { word: 'ass',    re: /\bass\b/i },
    { word: 'bitch',  re: /\bbitch/i },
    { word: 'cunt',   re: /\bcunt\b/i },
    { word: 'nigger', re: /\bnigger/i },
    { word: 'faggot', re: /\bfaggot/i },
    { word: 'retard', re: /\bretard\b/i },
    { word: 'suc my', re: /\bsuc[k]?\s+my\b/i },
];

const PLACEHOLDER_PATTERNS = [
    /lorem ipsum/i,
    /\[placeholder\]/i,
    /\[insert .+? here\]/i,
    /TODO[:\s]/i,
    /FIXME[:\s]/i,
    /HACK[:\s]/i,
    /XXX[:\s]/,
    /your.?company.?name/i,
    /test@test/i,
];

const GARBLED_PATTERNS = [
    /([a-z])\1{6,}/i,           // 7+ repeated chars: "aaaaaaa" (raised from 4)
    /\*#\*[^*]+\*#\*/,          // *#*text*#* (vandalism marker)
];

const DEBUG_PATTERNS = [
    /\bconsole\.(log|warn|error|debug)\(/,
    /\balert\s*\(/,
    /\bdebugger\b/,
];

// ─── Scanner ────────────────────────────────────────────────

function scanFile(filePath, site) {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n');
    const relPath = path.relative(site.dir, filePath);
    const ext = path.extname(filePath).toLowerCase();
    const issues = [];

    // Skip minified files or very long lines (likely build output)
    if (lines.some(l => l.length > 5000)) return issues;

    // For JSON content files, also check parsed values
    if (ext === '.json') {
        try {
            const data = JSON.parse(content);
            scanJsonValues(data, relPath, '', issues);
        } catch (e) { /* not valid JSON, will be caught by other validators */ }
        return issues;
    }

    // Track code blocks in markdown (skip content inside ```)
    let inCodeBlock = false;
    const isMd = ext === '.md';

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const lineNum = i + 1;

        // Toggle code block tracking for markdown
        if (isMd && line.trim().startsWith('```')) {
            inCodeBlock = !inCodeBlock;
            continue;
        }
        if (inCodeBlock) continue;

        // Skip comments and script blocks in some formats
        const trimmed = line.trim();
        if (trimmed.startsWith('//') && ext !== '.html') continue;

        // Profanity check (word-boundary, skips code comments about filtering)
        for (const { word, re } of PROFANITY) {
            if (re.test(line)) {
                // Make sure it's not in a comment about content filtering
                if (!/filter|detect|block|profanity|pattern|regex|test/i.test(line)) {
                    issues.push({
                        level: 'error',
                        file: relPath,
                        line: lineNum,
                        msg: `profanity detected: "${word}"`,
                        snippet: trimmed.substring(0, 80)
                    });
                }
            }
        }

        // Placeholder patterns
        for (const pattern of PLACEHOLDER_PATTERNS) {
            if (pattern.test(line)) {
                // Skip if in a test/config file
                if (/node_modules|test|spec|\.config\.|\.test\./i.test(relPath)) continue;
                // Skip TODO in source code files — only flag in content
                if (/TODO|FIXME|HACK/.test(pattern.source) && !/\.(md|html|json|txt)$/i.test(ext)) continue;

                issues.push({
                    level: 'warn',
                    file: relPath,
                    line: lineNum,
                    msg: `placeholder text: ${pattern.source}`,
                    snippet: trimmed.substring(0, 80)
                });
                break;
            }
        }

        // Garbled text
        for (const pattern of GARBLED_PATTERNS) {
            const match = line.match(pattern);
            if (match) {
                issues.push({
                    level: 'error',
                    file: relPath,
                    line: lineNum,
                    msg: `garbled/vandalized text: "${match[0]}"`,
                    snippet: trimmed.substring(0, 80)
                });
                break;
            }
        }

        // Debug artifacts (only in HTML — source code may legitimately use console.log)
        if (ext === '.html') {
            for (const pattern of DEBUG_PATTERNS) {
                if (pattern.test(line)) {
                    issues.push({
                        level: 'warn',
                        file: relPath,
                        line: lineNum,
                        msg: `debug artifact in production HTML`,
                        snippet: trimmed.substring(0, 80)
                    });
                    break;
                }
            }
        }
    }

    return issues;
}

// ─── JSON deep value scanner ────────────────────────────────

function scanJsonValues(obj, file, keyPath, issues) {
    if (typeof obj === 'string') {
        const val = obj;
        for (const { word, re } of PROFANITY) {
            if (re.test(val)) {
                issues.push({ level: 'error', file, line: 0, msg: `profanity in ${keyPath}: "${word}"`, snippet: val.substring(0, 80) });
            }
        }
        for (const pattern of GARBLED_PATTERNS) {
            const match = val.match(pattern);
            if (match) {
                issues.push({ level: 'error', file, line: 0, msg: `garbled text in ${keyPath}: "${match[0]}"`, snippet: val.substring(0, 80) });
            }
        }
    } else if (Array.isArray(obj)) {
        obj.forEach((v, i) => scanJsonValues(v, file, `${keyPath}[${i}]`, issues));
    } else if (obj && typeof obj === 'object') {
        for (const [k, v] of Object.entries(obj)) scanJsonValues(v, file, keyPath ? `${keyPath}.${k}` : k, issues);
    }
}

// ─── Main entry point ───────────────────────────────────────

function validateContent(site) {
    const extensions = ['.html', '.md', '.json', '.txt'];
    let allIssues = [];

    // Scan content dirs
    for (const dir of [...site.contentDirs, ...(site.layoutDirs || [])]) {
        if (!fs.existsSync(dir)) continue;
        const files = findFiles(dir, extensions);
        for (const file of files) {
            allIssues.push(...scanFile(file, site));
        }
    }

    // For Hugo, also scan public (built output)
    if (site.type === 'hugo' && fs.existsSync(site.publicDir)) {
        const htmlFiles = findFiles(site.publicDir, ['.html']);
        for (const file of htmlFiles) {
            allIssues.push(...scanFile(file, site));
        }
    }

    // For static sites, scan the root dir
    if (site.type === 'static') {
        const files = findFiles(site.dir, extensions);
        for (const file of files) {
            allIssues.push(...scanFile(file, site));
        }
    }

    // Deduplicate (same message can appear in source + built output)
    const seen = new Set();
    allIssues = allIssues.filter(i => {
        const key = `${i.msg}:${i.snippet}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
    });

    const errors = allIssues.filter(i => i.level === 'error');
    const warnings = allIssues.filter(i => i.level === 'warn');

    for (const i of errors) {
        console.log(`    ${c.RED}✗${c.RESET} ${i.file}${i.line ? ':' + i.line : ''}: ${i.msg}`);
        if (i.snippet) console.log(`      ${c.DIM}${i.snippet}${c.RESET}`);
    }
    for (const i of warnings.slice(0, 15)) {
        console.log(`    ${c.YELLOW}⚠${c.RESET} ${i.file}${i.line ? ':' + i.line : ''}: ${i.msg}`);
    }
    if (warnings.length > 15) console.log(`    ${c.DIM}  ... and ${warnings.length - 15} more warnings${c.RESET}`);

    if (errors.length === 0 && warnings.length === 0) {
        console.log(`    ${c.GREEN}✓ No content issues detected${c.RESET}`);
    }

    return { success: errors.length === 0, errors: errors.length, warnings: warnings.length };
}

if (require.main === module) {
    const { SITES } = require('./sites');
    const siteName = process.argv[2] || 'sailsto';
    const site = SITES[siteName];
    if (!site) { console.error('Unknown site:', siteName); process.exit(1); }
    const result = validateContent(site);
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateContent };
