#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════
 *   LINK VALIDATOR — works with Hugo, Vite, and static sites
 * ═══════════════════════════════════════════════════════════════
 *
 * Checks:
 *  1. Internal href="/..." links point to real pages or files
 *  2. src="/..." resources exist in static/public dirs
 *  3. Markdown [text](/path) links resolve
 */

const fs = require('fs');
const path = require('path');
const { c, findFiles, getSiteFiles } = require('./utils');

const STATIC_EXTENSIONS = new Set([
    '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.webm',
    '.woff', '.woff2', '.ttf', '.eot', '.ico', '.pdf', '.json', '.xml',
    '.mp4', '.mp3', '.zip', '.gz', '.map', '.txt', '.wasm',
]);

/**
 * Get valid content page paths for a site (Hugo or Vite)
 */
function getValidPages(site) {
    const pages = new Set(['/']);

    if (site.type === 'hugo') {
        // Hugo: content files map to URL paths
        const contentDir = site.contentDirs[0];
        if (!contentDir || !fs.existsSync(contentDir)) return pages;

        const files = findFiles(contentDir, ['.md', '.html']);
        for (const file of files) {
            let rel = path.relative(contentDir, file)
                .replace(/\\/g, '/')
                .replace(/_index\.(md|html)$/, '')
                .replace(/\.(md|html)$/, '/');
            if (!rel.startsWith('/')) rel = '/' + rel;
            if (!rel.endsWith('/')) rel += '/';
            pages.add(rel);
            pages.add(rel.slice(0, -1)); // without trailing slash
        }
    } else if (site.type === 'vite') {
        // Vite SPA: routes are defined in source, not easily statically resolved.
        // We check what content JSON files exist which imply routes, plus common routes.
        const contentDir = site.contentDirs[0];
        if (contentDir && fs.existsSync(contentDir)) {
            const files = findFiles(contentDir, ['.json', '.md']);
            for (const file of files) {
                let rel = path.relative(contentDir, file)
                    .replace(/\\/g, '/')
                    .replace(/\.(json|md)$/, '');
                // Handle language suffixes like landing.fr.json
                rel = rel.replace(/\.[a-z]{2}$/, '');
                pages.add('/' + rel);
                pages.add('/' + rel + '/');
            }
        }
        // Scan TSX/TS for route definitions
        for (const srcDir of site.layoutDirs || []) {
            const srcFiles = findFiles(srcDir, ['.tsx', '.ts']);
            for (const file of srcFiles) {
                const content = fs.readFileSync(file, 'utf8');
                const routeMatches = content.matchAll(/path:\s*['"]([^'"]+)['"]/g);
                for (const m of routeMatches) {
                    pages.add(m[1]);
                }
            }
        }
    } else {
        // Static: each .html file is a page
        for (const dir of site.contentDirs) {
            const files = findFiles(dir, ['.html']);
            for (const file of files) {
                let rel = path.relative(dir, file).replace(/\\/g, '/');
                if (rel === 'index.html') rel = '/';
                else rel = '/' + rel.replace(/\.html$/, '');
                pages.add(rel);
                pages.add(rel + '/');
            }
        }
    }

    return pages;
}

/**
 * Get all static file paths
 */
function getStaticFiles(site) {
    const paths = new Set();
    for (const dir of site.staticDirs || []) {
        const files = findFiles(dir, null); // all files
        for (const file of files) {
            const rel = '/' + path.relative(dir, file).replace(/\\/g, '/');
            paths.add(rel);
        }
    }
    return paths;
}

/**
 * Extract all internal links from files
 */
function extractLinks(files, rootDir) {
    const links = [];

    const patterns = [
        { regex: /href="(\/[^"#?]*)[?]?([^"#]*)(#[^"]*)?"/g, type: 'href' },
        { regex: /src="(\/[^"]+)"/g, type: 'src' },
        { regex: /\[([^\]]+)\]\((\/[^)#?]+)[?]?([^)#]*)(#[^)]*)?\)/g, type: 'markdown' },
    ];

    for (const file of files) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        const relFile = path.relative(rootDir, file);

        for (let i = 0; i < lines.length; i++) {
            for (const { regex, type } of patterns) {
                regex.lastIndex = 0;
                let match;
                while ((match = regex.exec(lines[i])) !== null) {
                    const url = type === 'markdown' ? match[2] : match[1];
                    if (url.includes('{{') || url.startsWith('//') || url.startsWith('data:')) continue;
                    links.push({ url, type, file: relFile, line: i + 1 });
                }
            }
        }
    }

    return links;
}

function categorize(url) {
    const ext = path.extname(url).toLowerCase();
    return STATIC_EXTENSIONS.has(ext) ? 'static' : 'page';
}

/**
 * Main validator — takes a site config object
 */
function validateLinks(site) {
    const validPages = getValidPages(site);
    const validStatic = getStaticFiles(site);

    const allFiles = getSiteFiles(site);
    console.log(`    ${c.DIM}${validPages.size} pages, ${validStatic.size} static files, scanning ${allFiles.length} files${c.RESET}`);

    const links = extractLinks(allFiles, site.dir);

    const brokenPages = [];
    const brokenStatic = [];

    for (const link of links) {
        const cat = categorize(link.url);
        if (cat === 'page') {
            let norm = link.url;
            if (!norm.endsWith('/') && !path.extname(norm)) norm += '/';
            if (!validPages.has(norm) && !validPages.has(link.url)) {
                brokenPages.push(link);
            }
        } else {
            if (!validStatic.has(link.url)) {
                brokenStatic.push(link);
            }
        }
    }

    // Report
    let errors = 0;
    if (brokenPages.length > 0) {
        errors += brokenPages.length;
        const byUrl = groupBy(brokenPages, 'url');
        console.log(`    ${c.RED}✗ ${byUrl.size} broken page link(s):${c.RESET}`);
        for (const [url, refs] of byUrl) {
            console.log(`      ${c.RED}•${c.RESET} ${url}  ${c.DIM}(${refs.map(r => r.file + ':' + r.line).slice(0, 2).join(', ')})${c.RESET}`);
        }
    } else {
        console.log(`    ${c.GREEN}✓ All page links valid${c.RESET}`);
    }

    if (brokenStatic.length > 0) {
        errors += brokenStatic.length;
        const byUrl = groupBy(brokenStatic, 'url');
        console.log(`    ${c.RED}✗ ${byUrl.size} broken static resource(s):${c.RESET}`);
        for (const [url, refs] of byUrl) {
            console.log(`      ${c.RED}•${c.RESET} ${url}  ${c.DIM}(${refs.map(r => r.file + ':' + r.line).slice(0, 2).join(', ')})${c.RESET}`);
        }
    } else {
        console.log(`    ${c.GREEN}✓ All static resources valid${c.RESET}`);
    }

    return { success: errors === 0, errors, warnings: 0 };
}

function groupBy(arr, key) {
    const map = new Map();
    for (const item of arr) {
        if (!map.has(item[key])) map.set(item[key], []);
        map.get(item[key]).push(item);
    }
    return map;
}

if (require.main === module) {
    const { SITES } = require('./sites');
    const siteName = process.argv[2] || 'sailsto';
    const site = SITES[siteName];
    if (!site) { console.error('Unknown site:', siteName); process.exit(1); }
    const result = validateLinks(site);
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateLinks };
