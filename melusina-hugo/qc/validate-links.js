#!/usr/bin/env node

/**
 * Link Validation Script (Melusina OS)
 * 
 * Validates all internal links in content and layouts:
 * 1. All href="/..." links point to existing pages
 * 2. All src="/..." resources exist in static/
 * 
 * Usage: node qc/validate-links.js
 */

const fs = require('fs');
const path = require('path');

const HUGO_ROOT = path.join(__dirname, '..');
const CONTENT_DIR = path.join(HUGO_ROOT, 'content');
const LAYOUTS_DIR = path.join(HUGO_ROOT, 'layouts');
const STATIC_DIR = path.join(HUGO_ROOT, 'static');

const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';

function findFiles(dir, extensions, files = []) {
    if (!fs.existsSync(dir)) return files;
    const items = fs.readdirSync(dir, { withFileTypes: true });
    for (const item of items) {
        const fullPath = path.join(dir, item.name);
        if (item.isDirectory()) {
            findFiles(fullPath, extensions, files);
        } else if (extensions.some(ext => item.name.endsWith(ext))) {
            files.push(fullPath);
        }
    }
    return files;
}

function getValidContentPaths() {
    const paths = new Set();
    paths.add('/');

    const contentFiles = findFiles(CONTENT_DIR, ['.md', '.html']);
    for (const file of contentFiles) {
        let relativePath = path.relative(CONTENT_DIR, file);
        relativePath = relativePath
            .replace(/\\/g, '/')
            .replace(/_index\.(md|html)$/, '')
            .replace(/\.(md|html)$/, '/');

        if (!relativePath.startsWith('/')) relativePath = '/' + relativePath;
        if (!relativePath.endsWith('/')) relativePath += '/';

        paths.add(relativePath);
        paths.add(relativePath.slice(0, -1));
    }
    return paths;
}

function getValidStaticPaths() {
    const paths = new Set();
    const staticFiles = findFiles(STATIC_DIR, ['']);
    for (const file of staticFiles) {
        let relativePath = path.relative(STATIC_DIR, file);
        relativePath = '/' + relativePath.replace(/\\/g, '/');
        paths.add(relativePath);
    }
    return paths;
}

function extractLinks(files) {
    const links = [];
    const patterns = [
        { regex: /href="(\/[^"#?]*)[?]?([^"#]*)(#[^"]*)?"/g, type: 'href' },
        { regex: /src="(\/[^"]+)"/g, type: 'src' },
        { regex: /\[([^\]]+)\]\((\/[^)#?]+)[?]?([^)#]*)(#[^)]*)?\)/g, type: 'markdown' }
    ];

    for (const file of files) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        const relativeFile = path.relative(HUGO_ROOT, file);

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            for (const { regex, type } of patterns) {
                let match;
                regex.lastIndex = 0;
                while ((match = regex.exec(line)) !== null) {
                    const url = type === 'markdown' ? match[2] : match[1];
                    if (url.includes('{{') || url.startsWith('//') || url.startsWith('data:')) continue;
                    links.push({
                        url,
                        type,
                        file: relativeFile,
                        line: i + 1
                    });
                }
            }
        }
    }
    return links;
}

function categorizeUrl(url) {
    const staticExtensions = [
        '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.webm',
        '.woff', '.woff2', '.ttf', '.eot', '.ico', '.pdf', '.json', '.xml'
    ];
    const ext = path.extname(url).toLowerCase();
    return staticExtensions.includes(ext) ? 'static' : 'page';
}

function validateLinks() {
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   LINK VALIDATION REPORT${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    const validPages = getValidContentPaths();
    const validStatic = getValidStaticPaths();

    console.log(`Found ${CYAN}${validPages.size}${RESET} valid content pages`);
    console.log(`Found ${CYAN}${validStatic.size}${RESET} static files`);

    const sourceFiles = [
        ...findFiles(CONTENT_DIR, ['.md', '.html']),
        ...findFiles(LAYOUTS_DIR, ['.html'])
    ];
    console.log(`Scanning ${CYAN}${sourceFiles.length}${RESET} files for links...\n`);

    const links = extractLinks(sourceFiles);
    console.log(`Found ${CYAN}${links.length}${RESET} internal links to validate\n`);

    const brokenPages = [];
    const brokenStatic = [];

    for (const link of links) {
        const category = categorizeUrl(link.url);
        if (category === 'page') {
            let normalizedUrl = link.url;
            if (!normalizedUrl.endsWith('/') && !path.extname(normalizedUrl)) {
                normalizedUrl += '/';
            }
            if (!validPages.has(normalizedUrl) && !validPages.has(link.url)) {
                const withIndex = link.url + (link.url.endsWith('/') ? 'index.html' : '/index.html');
                if (!validStatic.has(withIndex)) {
                    brokenPages.push(link);
                }
            }
        } else {
            if (!validStatic.has(link.url)) {
                brokenStatic.push(link);
            }
        }
    }

    console.log(`${BOLD}CHECK 1: Broken Page Links${RESET}`);
    console.log('────────────────────────────────────────────────────────────');
    if (brokenPages.length === 0) {
        console.log(`${GREEN}✓ All page links are valid${RESET}\n`);
    } else {
        console.log(`${RED}✗ ${brokenPages.length} broken page link(s) found:${RESET}\n`);
        const byUrl = new Map();
        for (const link of brokenPages) {
            if (!byUrl.has(link.url)) byUrl.set(link.url, []);
            byUrl.get(link.url).push(link);
        }
        for (const [url, occurrences] of byUrl) {
            console.log(`  ${RED}•${RESET} ${BOLD}${url}${RESET}`);
            for (const occ of occurrences.slice(0, 3)) {
                console.log(`    ${DIM}${occ.file}:${occ.line}${RESET}`);
            }
            if (occurrences.length > 3) console.log(`    ${DIM}... and ${occurrences.length - 3} more${RESET}`);
        }
        console.log();
    }

    console.log(`${BOLD}CHECK 2: Broken Static Resources${RESET}`);
    console.log('────────────────────────────────────────────────────────────');
    if (brokenStatic.length === 0) {
        console.log(`${GREEN}✓ All static resource links are valid${RESET}\n`);
    } else {
        console.log(`${RED}✗ ${brokenStatic.length} broken static resource(s) found:${RESET}\n`);
        const byUrl = new Map();
        for (const link of brokenStatic) {
            if (!byUrl.has(link.url)) byUrl.set(link.url, []);
            byUrl.get(link.url).push(link);
        }
        for (const [url, occurrences] of byUrl) {
            console.log(`  ${RED}•${RESET} ${BOLD}${url}${RESET}`);
            for (const occ of occurrences.slice(0, 3)) {
                console.log(`    ${DIM}${occ.file}:${occ.line}${RESET}`);
            }
            if (occurrences.length > 3) console.log(`    ${DIM}... and ${occurrences.length - 3} more${RESET}`);
        }
        console.log();
    }

    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   SUMMARY${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    const totalErrors = brokenPages.length + brokenStatic.length;
    if (totalErrors === 0) {
        console.log(`${GREEN}✓ All ${links.length} links validated successfully!${RESET}\n`);
        return { success: true, errors: 0, warnings: 0 };
    } else {
        console.log(`${RED}✗ ${totalErrors} broken link(s) found${RESET}`);
        if (brokenPages.length > 0) console.log(`  • ${brokenPages.length} broken page link(s)`);
        if (brokenStatic.length > 0) console.log(`  • ${brokenStatic.length} broken static resource(s)`);
        console.log();
        return { success: false, errors: totalErrors, warnings: 0 };
    }
}

if (require.main === module) {
    const result = validateLinks();
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateLinks };
