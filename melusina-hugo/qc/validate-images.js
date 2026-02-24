#!/usr/bin/env node

/**
 * Image Validation Script (Melusina OS)
 * 
 * Validates all images referenced in content:
 * 1. All img src references point to existing files
 * 2. All images have alt text for accessibility
 * 3. Reports unused images in static folder
 * 
 * Usage: node qc/validate-images.js
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

const IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico'];

function findFiles(dir, extensions = null, files = []) {
    if (!fs.existsSync(dir)) return files;
    const items = fs.readdirSync(dir, { withFileTypes: true });
    for (const item of items) {
        const fullPath = path.join(dir, item.name);
        if (item.isDirectory()) {
            findFiles(fullPath, extensions, files);
        } else if (!extensions || extensions.some(ext => item.name.toLowerCase().endsWith(ext))) {
            files.push(fullPath);
        }
    }
    return files;
}

function getStaticImages() {
    const images = new Set();
    const files = findFiles(STATIC_DIR, IMAGE_EXTENSIONS);
    for (const file of files) {
        const relativePath = '/' + path.relative(STATIC_DIR, file).replace(/\\/g, '/');
        images.add(relativePath);
    }
    return images;
}

function extractImageReferences(files) {
    const references = [];
    const patterns = [
        { regex: /src="([^"]+\.(png|jpg|jpeg|gif|svg|webp|ico))"/gi, type: 'src' },
        { regex: /url\(['"]?([^'")\s]+\.(png|jpg|jpeg|gif|svg|webp|ico))['"]?\)/gi, type: 'css' },
        { regex: /poster="([^"]+)"/gi, type: 'poster' },
        { regex: /!\[([^\]]*)\]\(([^)]+)\)/g, type: 'markdown' }
    ];

    for (const file of files) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        const relativeFile = path.relative(HUGO_ROOT, file);

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];

            // Check img tags for alt text
            const imgTagRegex = /<img[^>]+>/gi;
            let imgMatch;
            while ((imgMatch = imgTagRegex.exec(line)) !== null) {
                const imgTag = imgMatch[0];
                const srcMatch = /src="([^"]+)"/.exec(imgTag);
                const altMatch = /alt="([^"]*)"/.exec(imgTag);

                if (srcMatch) {
                    const src = srcMatch[1];
                    if (src.startsWith('/') && !src.includes('{{')) {
                        references.push({
                            url: src,
                            hasAlt: !!altMatch,
                            altText: altMatch ? altMatch[1] : null,
                            type: 'img',
                            file: relativeFile,
                            line: i + 1
                        });
                    }
                }
            }

            for (const { regex, type } of patterns) {
                let match;
                regex.lastIndex = 0;
                while ((match = regex.exec(line)) !== null) {
                    const url = type === 'markdown' ? match[2] : match[1];
                    if (url.startsWith('/') && !url.includes('{{')) {
                        references.push({
                            url,
                            hasAlt: type === 'markdown',
                            altText: type === 'markdown' ? match[1] : null,
                            type,
                            file: relativeFile,
                            line: i + 1
                        });
                    }
                }
            }
        }
    }
    return references;
}

function validateImages() {
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   IMAGE VALIDATION REPORT${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    const staticImages = getStaticImages();
    console.log(`Found ${CYAN}${staticImages.size}${RESET} images in static directory`);

    const sourceFiles = [
        ...findFiles(CONTENT_DIR, ['.md', '.html']),
        ...findFiles(LAYOUTS_DIR, ['.html'])
    ];
    console.log(`Scanning ${CYAN}${sourceFiles.length}${RESET} files for image references...\n`);

    const references = extractImageReferences(sourceFiles);
    const uniqueUrls = new Set(references.map(r => r.url));
    console.log(`Found ${CYAN}${references.length}${RESET} image references (${uniqueUrls.size} unique)\n`);

    let errors = 0;
    let warnings = 0;

    // CHECK 1: Broken image references
    console.log(`${BOLD}CHECK 1: Broken Image References${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const brokenImages = references.filter(ref => {
        if (IMAGE_EXTENSIONS.some(ext => ref.url.toLowerCase().endsWith(ext))) {
            return !staticImages.has(ref.url);
        }
        return false;
    });

    if (brokenImages.length === 0) {
        console.log(`${GREEN}✓ All image references are valid${RESET}\n`);
    } else {
        errors += brokenImages.length;
        console.log(`${RED}✗ ${brokenImages.length} broken image reference(s):${RESET}\n`);
        const byUrl = new Map();
        for (const ref of brokenImages) {
            if (!byUrl.has(ref.url)) byUrl.set(ref.url, []);
            byUrl.get(ref.url).push(ref);
        }
        for (const [url, refs] of byUrl) {
            console.log(`  ${RED}•${RESET} ${BOLD}${url}${RESET}`);
            for (const ref of refs.slice(0, 2)) console.log(`    ${DIM}${ref.file}:${ref.line}${RESET}`);
            if (refs.length > 2) console.log(`    ${DIM}... and ${refs.length - 2} more${RESET}`);
        }
        console.log();
    }

    // CHECK 2: Images without alt text
    console.log(`${BOLD}CHECK 2: Images Missing Alt Text (Accessibility)${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const missingAlt = references.filter(ref => ref.type === 'img' && !ref.hasAlt);
    if (missingAlt.length === 0) {
        console.log(`${GREEN}✓ All images have alt text${RESET}\n`);
    } else {
        warnings += missingAlt.length;
        console.log(`${YELLOW}⚠ ${missingAlt.length} image(s) missing alt text:${RESET}\n`);
        for (const ref of missingAlt.slice(0, 10)) {
            console.log(`  ${YELLOW}•${RESET} ${ref.url}`);
            console.log(`    ${DIM}${ref.file}:${ref.line}${RESET}`);
        }
        if (missingAlt.length > 10) console.log(`  ${DIM}... and ${missingAlt.length - 10} more${RESET}`);
        console.log();
    }

    // CHECK 3: Unused images
    console.log(`${BOLD}CHECK 3: Unused Images in Static Directory${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const usedUrls = new Set(references.map(r => r.url));
    const unusedImages = [...staticImages].filter(img => !usedUrls.has(img));
    const filteredUnused = unusedImages.filter(img =>
        !img.includes('favicon') &&
        !img.includes('apple-touch') &&
        !img.includes('og-') &&
        !img.includes('android-chrome')
    );

    if (filteredUnused.length === 0) {
        console.log(`${GREEN}✓ All images appear to be in use${RESET}\n`);
    } else if (filteredUnused.length <= 5) {
        console.log(`${YELLOW}⚠ ${filteredUnused.length} potentially unused image(s):${RESET}\n`);
        for (const img of filteredUnused) console.log(`  ${YELLOW}•${RESET} ${img}`);
        console.log(`\n  ${DIM}(These may be used dynamically or in external references)${RESET}\n`);
    } else {
        console.log(`${YELLOW}⚠ ${filteredUnused.length} potentially unused images${RESET}`);
        console.log(`  ${DIM}Run with --verbose to see full list${RESET}\n`);
    }

    // Summary
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   SUMMARY${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    if (errors === 0 && warnings === 0) {
        console.log(`${GREEN}✓ All image checks passed!${RESET}\n`);
        return { success: true, errors: 0, warnings: 0 };
    } else if (errors === 0) {
        console.log(`${YELLOW}⚠ ${warnings} warning(s) - accessibility improvements recommended${RESET}\n`);
        return { success: true, errors: 0, warnings };
    } else {
        console.log(`${RED}✗ ${errors} error(s), ${warnings} warning(s)${RESET}\n`);
        return { success: false, errors, warnings };
    }
}

if (require.main === module) {
    const result = validateImages();
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateImages };
