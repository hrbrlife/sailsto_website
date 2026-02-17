#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════
 *   IMAGE VALIDATOR — works with Hugo, Vite, and static sites
 * ═══════════════════════════════════════════════════════════════
 *
 * Checks:
 *  1. All img src references point to existing files
 *  2. All <img> tags have alt text (accessibility)
 *  3. Reports unused images in static/public directories
 */

const fs = require('fs');
const path = require('path');
const { c, findFiles, getSiteFiles } = require('./utils');

const IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico', '.avif'];

function getStaticImages(site) {
    const images = new Set();
    for (const dir of site.staticDirs || []) {
        const files = findFiles(dir, IMAGE_EXTENSIONS);
        for (const file of files) {
            const rel = '/' + path.relative(dir, file).replace(/\\/g, '/');
            images.add(rel);
        }
    }
    return images;
}

function extractImageRefs(files, rootDir) {
    const refs = [];

    for (const file of files) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        const relFile = path.relative(rootDir, file);

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];

            // <img> tags
            const imgRegex = /<img[^>]+>/gi;
            let imgMatch;
            while ((imgMatch = imgRegex.exec(line)) !== null) {
                const tag = imgMatch[0];
                const srcMatch = /src="([^"]+)"/.exec(tag);
                const altMatch = /alt="([^"]*)"/.exec(tag);
                if (srcMatch && srcMatch[1].startsWith('/') && !srcMatch[1].includes('{{')) {
                    refs.push({
                        url: srcMatch[1],
                        hasAlt: !!altMatch,
                        type: 'img',
                        file: relFile,
                        line: i + 1,
                    });
                }
            }

            // CSS url() references
            const cssRegex = /url\(['"]?([^'")\s]+\.(png|jpg|jpeg|gif|svg|webp|ico|avif))['"]?\)/gi;
            let cssMatch;
            while ((cssMatch = cssRegex.exec(line)) !== null) {
                if (cssMatch[1].startsWith('/') && !cssMatch[1].includes('{{')) {
                    refs.push({
                        url: cssMatch[1],
                        hasAlt: true, // N/A for CSS
                        type: 'css',
                        file: relFile,
                        line: i + 1,
                    });
                }
            }

            // Markdown images
            const mdRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
            let mdMatch;
            while ((mdMatch = mdRegex.exec(line)) !== null) {
                if (mdMatch[2].startsWith('/') && !mdMatch[2].includes('{{')) {
                    refs.push({
                        url: mdMatch[2],
                        hasAlt: !!mdMatch[1],
                        type: 'markdown',
                        file: relFile,
                        line: i + 1,
                    });
                }
            }
        }
    }

    return refs;
}

function validateImages(site) {
    const staticImages = getStaticImages(site);
    const allFiles = getSiteFiles(site);
    console.log(`    ${c.DIM}${staticImages.size} images, scanning ${allFiles.length} files${c.RESET}`);

    const refs = extractImageRefs(allFiles, site.dir);

    let errors = 0;
    let warnings = 0;

    // CHECK 1: Broken image references
    const broken = refs.filter(r =>
        IMAGE_EXTENSIONS.some(ext => r.url.toLowerCase().endsWith(ext)) &&
        !staticImages.has(r.url)
    );

    if (broken.length > 0) {
        errors += broken.length;
        const urls = [...new Set(broken.map(r => r.url))];
        console.log(`    ${c.RED}✗ ${urls.length} broken image ref(s):${c.RESET}`);
        for (const url of urls.slice(0, 10)) {
            const locs = broken.filter(r => r.url === url);
            console.log(`      ${c.RED}•${c.RESET} ${url}  ${c.DIM}(${locs[0].file}:${locs[0].line})${c.RESET}`);
        }
        if (urls.length > 10) console.log(`      ${c.DIM}... and ${urls.length - 10} more${c.RESET}`);
    } else {
        console.log(`    ${c.GREEN}✓ All image references valid${c.RESET}`);
    }

    // CHECK 2: Missing alt text
    const missingAlt = refs.filter(r => r.type === 'img' && !r.hasAlt);
    if (missingAlt.length > 0) {
        warnings += missingAlt.length;
        console.log(`    ${c.YELLOW}⚠ ${missingAlt.length} image(s) missing alt text${c.RESET}`);
        for (const ref of missingAlt.slice(0, 5)) {
            console.log(`      ${c.YELLOW}•${c.RESET} ${ref.url}  ${c.DIM}(${ref.file}:${ref.line})${c.RESET}`);
        }
    } else {
        console.log(`    ${c.GREEN}✓ All images have alt text${c.RESET}`);
    }

    // CHECK 3: Unused images
    const usedUrls = new Set(refs.map(r => r.url));
    const unused = [...staticImages].filter(img =>
        !usedUrls.has(img) &&
        !img.includes('favicon') &&
        !img.includes('apple-touch') &&
        !img.includes('og-') &&
        !img.includes('twitter-') &&
        !img.includes('android-chrome')
    );

    if (unused.length > 0) {
        console.log(`    ${c.YELLOW}⚠ ${unused.length} potentially unused image(s)${c.RESET}`);
        if (unused.length <= 8) {
            for (const img of unused) console.log(`      ${c.DIM}${img}${c.RESET}`);
        }
        warnings += 1; // Count as 1 warning, not per-image
    } else {
        console.log(`    ${c.GREEN}✓ All images appear used${c.RESET}`);
    }

    return { success: errors === 0, errors, warnings };
}

if (require.main === module) {
    const { SITES } = require('./sites');
    const siteName = process.argv[2] || 'sailsto';
    const site = SITES[siteName];
    if (!site) { console.error('Unknown site:', siteName); process.exit(1); }
    const result = validateImages(site);
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateImages };
