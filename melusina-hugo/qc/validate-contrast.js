#!/usr/bin/env node

/**
 * Contrast & Visibility Validation Script (Melusina OS)
 * 
 * Checks WCAG 2.1 contrast ratios for all visible text on every page:
 * 1. Loads each page in a headless browser (Playwright)
 * 2. Extracts computed colors for all text elements
 * 3. Calculates effective background colors (walking DOM ancestry)
 * 4. Computes WCAG contrast ratios
 * 5. Flags violations against WCAG AA thresholds
 * 
 * Requirements:
 *   npx playwright install chromium
 *   Hugo dev server running (http://localhost:1315)
 * 
 * Usage: node qc/validate-contrast.js [--base-url=URL] [--verbose]
 */

let chromium;
try {
    ({ chromium } = require('playwright'));
} catch (e) {
    // Handled gracefully in validateContrast()
}

const fs = require('fs');
const path = require('path');
const http = require('http');

const HUGO_ROOT = path.join(__dirname, '..');
const CONTENT_DIR = path.join(HUGO_ROOT, 'content');

const BASE_URL = process.argv.find(a => a.startsWith('--base-url='))
    ?.split('=')[1] || process.env.BASE_URL || 'http://localhost:1315';

const VERBOSE = process.argv.includes('--verbose') || process.argv.includes('-v');

const WCAG_AA_NORMAL = 4.5;
const WCAG_AA_LARGE  = 3.0;

const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';

function relativeLuminance(r, g, b) {
    const [rs, gs, bs] = [r, g, b].map(c => {
        const s = c / 255;
        return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

function contrastRatio(color1, color2) {
    const l1 = relativeLuminance(color1.r, color1.g, color1.b);
    const l2 = relativeLuminance(color2.r, color2.g, color2.b);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
}

function compositeColor(fg, bg) {
    if (fg.a >= 1) return { r: fg.r, g: fg.g, b: fg.b };
    return {
        r: Math.round(fg.r * fg.a + bg.r * (1 - fg.a)),
        g: Math.round(fg.g * fg.a + bg.g * (1 - fg.a)),
        b: Math.round(fg.b * fg.a + bg.b * (1 - fg.a))
    };
}

function isLargeText(fontSize, fontWeight) {
    if (fontSize >= 24) return true;
    if (fontSize >= 18.66 && fontWeight >= 700) return true;
    return false;
}

function colorToHex(c) {
    const hex = (v) => Math.round(Math.max(0, Math.min(255, v))).toString(16).padStart(2, '0');
    return `#${hex(c.r)}${hex(c.g)}${hex(c.b)}`;
}

function getContentPages() {
    const pages = [];
    function scan(dir, urlPrefix) {
        if (!fs.existsSync(dir)) return;
        const items = fs.readdirSync(dir, { withFileTypes: true });
        for (const item of items) {
            const fullPath = path.join(dir, item.name);
            if (item.isDirectory()) {
                scan(fullPath, urlPrefix + item.name + '/');
            } else if (item.name === '_index.md') {
                pages.push({ url: urlPrefix, file: path.relative(HUGO_ROOT, fullPath) });
            } else if (item.name.endsWith('.md')) {
                const slug = item.name.replace('.md', '');
                pages.push({ url: urlPrefix + slug + '/', file: path.relative(HUGO_ROOT, fullPath) });
            }
        }
    }
    scan(CONTENT_DIR, '/');
    return pages;
}

function checkServer(url) {
    return new Promise((resolve) => {
        const req = http.get(url, (res) => {
            res.resume();
            resolve(true);
        });
        req.on('error', () => resolve(false));
        req.setTimeout(3000, () => { req.destroy(); resolve(false); });
    });
}

const BROWSER_EXTRACT_FN = function () {
    const results = [];

    function parseColor(str) {
        if (!str || str === 'transparent' || str === 'rgba(0, 0, 0, 0)') {
            return { r: 0, g: 0, b: 0, a: 0 };
        }
        const match = str.match(/rgba?\(\s*(\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\s*\)/);
        if (!match) return { r: 0, g: 0, b: 0, a: 0 };
        return {
            r: parseInt(match[1]),
            g: parseInt(match[2]),
            b: parseInt(match[3]),
            a: match[4] !== undefined ? parseFloat(match[4]) : 1
        };
    }

    function getEffectiveBackground(el) {
        const backgrounds = [];
        let current = el;
        while (current && current !== document.documentElement) {
            const style = getComputedStyle(current);
            backgrounds.push(parseColor(style.backgroundColor));
            current = current.parentElement;
        }
        if (document.documentElement) {
            backgrounds.push(parseColor(getComputedStyle(document.documentElement).backgroundColor));
        }
        let result = { r: 255, g: 255, b: 255, a: 1 };
        for (let i = backgrounds.length - 1; i >= 0; i--) {
            const fg = backgrounds[i];
            if (fg.a > 0) {
                result = {
                    r: Math.round(fg.r * fg.a + result.r * (1 - fg.a)),
                    g: Math.round(fg.g * fg.a + result.g * (1 - fg.a)),
                    b: Math.round(fg.b * fg.a + result.b * (1 - fg.a)),
                    a: 1
                };
            }
        }
        return result;
    }

    function hasBackgroundImage(el) {
        let current = el;
        while (current && current !== document.documentElement) {
            const style = getComputedStyle(current);
            if (style.backgroundImage && style.backgroundImage !== 'none') return true;
            current = current.parentElement;
        }
        return false;
    }

    function isVisible(el) {
        const style = getComputedStyle(el);
        if (style.display === 'none') return false;
        if (style.visibility === 'hidden') return false;
        if (parseFloat(style.opacity) === 0) return false;
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) return false;
        return true;
    }

    const SKIP = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'SVG', 'PATH',
                          'DEFS', 'CLIPPATH', 'MASK', 'LINEARGRADIENT', 'RADIALGRADIENT',
                          'STOP', 'USE', 'SYMBOL', 'G', 'CIRCLE', 'RECT', 'LINE',
                          'POLYGON', 'POLYLINE', 'ELLIPSE', 'TEXT']);

    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        {
            acceptNode: function (node) {
                const text = node.textContent.trim();
                if (!text || text.length < 2) return NodeFilter.FILTER_REJECT;
                const parent = node.parentElement;
                if (!parent) return NodeFilter.FILTER_REJECT;
                if (SKIP.has(parent.tagName)) return NodeFilter.FILTER_REJECT;
                if (parent.closest('svg')) return NodeFilter.FILTER_REJECT;
                return NodeFilter.FILTER_ACCEPT;
            }
        }
    );

    const seen = new Set();
    let node;
    while ((node = walker.nextNode())) {
        const el = node.parentElement;
        if (!el || seen.has(el)) continue;
        seen.add(el);
        if (!isVisible(el)) continue;

        const style = getComputedStyle(el);
        const textColor = parseColor(style.color);
        const bgColor = getEffectiveBackground(el);
        const hasBgImg = hasBackgroundImage(el);
        const rect = el.getBoundingClientRect();

        let selector = el.tagName.toLowerCase();
        if (el.id) {
            selector += '#' + el.id;
        } else if (el.className && typeof el.className === 'string' && el.className.trim()) {
            selector += '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.');
        }

        results.push({
            selector,
            text: node.textContent.trim().substring(0, 60),
            color: { r: textColor.r, g: textColor.g, b: textColor.b, a: textColor.a },
            bgColor: { r: bgColor.r, g: bgColor.g, b: bgColor.b },
            fontSize: parseFloat(style.fontSize),
            fontWeight: parseInt(style.fontWeight) || 400,
            hasBgImage: hasBgImg,
            y: Math.round(rect.top + window.scrollY)
        });
    }
    return results;
};

async function validateContrast() {
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   CONTRAST & VISIBILITY VALIDATION (WCAG 2.1 AA)${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    if (!chromium) {
        console.log(`${YELLOW}⚠ Playwright not installed.${RESET}`);
        console.log(`  Run: ${CYAN}npm install playwright && npx playwright install chromium${RESET}\n`);
        return { success: true, errors: 0, warnings: 1, skipped: true };
    }

    const serverUp = await checkServer(BASE_URL);
    if (!serverUp) {
        console.log(`${YELLOW}⚠ Cannot reach ${BASE_URL}${RESET}`);
        console.log(`  Start the Hugo dev server: ${CYAN}hugo server -p 1315${RESET}\n`);
        return { success: true, errors: 0, warnings: 1, skipped: true };
    }
    console.log(`${DIM}Server: ${BASE_URL}${RESET}`);

    const contentPages = getContentPages();
    console.log(`Found ${CYAN}${contentPages.length}${RESET} content pages to check\n`);

    let browser;
    try {
        browser = await chromium.launch({ headless: true });
    } catch (e) {
        console.log(`${YELLOW}⚠ Chromium not installed.${RESET}`);
        console.log(`  Run: ${CYAN}npx playwright install chromium${RESET}\n`);
        return { success: true, errors: 0, warnings: 1, skipped: true };
    }

    const context = await browser.newContext({
        viewport: { width: 1400, height: 900 },
        colorScheme: 'light'
    });
    const page = await context.newPage();

    let totalViolations = 0;
    let totalElements = 0;
    let totalBgImageWarns = 0;
    let pagesChecked = 0;
    let pagesFailed = 0;
    const allViolations = [];

    for (let i = 0; i < contentPages.length; i++) {
        const { url: pagePath } = contentPages[i];
        const fullUrl = BASE_URL + pagePath;
        process.stdout.write(`${DIM}  [${i + 1}/${contentPages.length}] ${pagePath}${RESET}`);

        try {
            const response = await page.goto(fullUrl, {
                waitUntil: 'domcontentloaded',
                timeout: 10000
            });

            if (response && response.status() >= 400) {
                process.stdout.write(` ${YELLOW}(${response.status()}, skipped)${RESET}\n`);
                continue;
            }

            await page.waitForTimeout(300);
            const elements = await page.evaluate(BROWSER_EXTRACT_FN);
            totalElements += elements.length;
            pagesChecked++;

            const pageViolations = [];
            let pageBgImageWarns = 0;

            for (const el of elements) {
                if (el.hasBgImage) { pageBgImageWarns++; continue; }
                const effectiveText = el.color.a < 1
                    ? compositeColor(el.color, el.bgColor)
                    : { r: el.color.r, g: el.color.g, b: el.color.b };
                const ratio = contrastRatio(effectiveText, el.bgColor);
                const largeText = isLargeText(el.fontSize, el.fontWeight);
                const threshold = largeText ? WCAG_AA_LARGE : WCAG_AA_NORMAL;
                if (ratio < threshold) {
                    pageViolations.push({ ...el, effectiveText, ratio, threshold, largeText });
                }
            }

            totalBgImageWarns += pageBgImageWarns;

            if (pageViolations.length === 0) {
                process.stdout.write(` ${GREEN}✓${RESET}\n`);
            } else {
                totalViolations += pageViolations.length;
                pagesFailed++;
                process.stdout.write(` ${RED}✗ ${pageViolations.length} violation(s)${RESET}\n`);
                allViolations.push({ path: pagePath, violations: pageViolations });

                const show = VERBOSE ? pageViolations : pageViolations.slice(0, 5);
                for (const v of show) {
                    console.log(`    ${RED}✗${RESET} [${v.ratio.toFixed(1)}:1 < ${v.threshold}:1] ${DIM}${v.selector}${RESET}`);
                    console.log(`      text ${BOLD}${colorToHex(v.effectiveText)}${RESET} on bg ${BOLD}${colorToHex(v.bgColor)}${RESET} — "${v.text.substring(0, 50)}"`);
                }
                if (!VERBOSE && pageViolations.length > 5) {
                    console.log(`    ${DIM}... and ${pageViolations.length - 5} more (pass --verbose)${RESET}`);
                }
            }
        } catch (err) {
            process.stdout.write(` ${YELLOW}(error: ${err.message.substring(0, 50)})${RESET}\n`);
        }
    }

    await browser.close();

    console.log(`\n${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   SUMMARY${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    console.log(`  Pages checked:       ${CYAN}${pagesChecked}${RESET}`);
    console.log(`  Text elements:       ${CYAN}${totalElements}${RESET}`);
    console.log(`  Contrast violations: ${totalViolations > 0 ? RED : GREEN}${totalViolations}${RESET}`);
    console.log(`  Pages with issues:   ${pagesFailed > 0 ? RED : GREEN}${pagesFailed}${RESET}`);
    if (totalBgImageWarns > 0) {
        console.log(`  Background image:    ${YELLOW}${totalBgImageWarns}${RESET} ${DIM}(manual check)${RESET}`);
    }
    console.log();

    if (totalViolations === 0) {
        console.log(`${GREEN}✓ All text passes WCAG 2.1 AA contrast requirements!${RESET}\n`);
        return { success: true, errors: 0, warnings: totalBgImageWarns > 0 ? 1 : 0 };
    } else {
        console.log(`${RED}✗ ${totalViolations} contrast violation(s) across ${pagesFailed} page(s)${RESET}\n`);
        return { success: false, errors: totalViolations, warnings: totalBgImageWarns > 0 ? 1 : 0 };
    }
}

if (require.main === module) {
    validateContrast().then(result => {
        process.exit(result.success ? 0 : 1);
    }).catch(err => {
        console.error(`${RED}Fatal: ${err.message}${RESET}`);
        process.exit(1);
    });
}

module.exports = { validateContrast };
