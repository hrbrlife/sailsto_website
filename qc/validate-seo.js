#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════
 *   SEO VALIDATOR — meta tags, OG, twitter cards, canonical
 * ═══════════════════════════════════════════════════════════════
 *
 * All sites: scans HTML output for essential SEO tags.
 * Vite sites: also checks content JSON for SEO metadata.
 */

const fs = require('fs');
const path = require('path');
const { c, findFiles, getSiteFiles } = require('./utils');

const META_REGEX = {
    title:       /<title>([^<]*)<\/title>/i,
    description: /<meta\s+name="description"\s+content="([^"]*)"/i,
    ogTitle:     /<meta\s+property="og:title"\s+content="([^"]*)"/i,
    ogDesc:      /<meta\s+property="og:description"\s+content="([^"]*)"/i,
    ogImage:     /<meta\s+property="og:image"\s+content="([^"]*)"/i,
    ogUrl:       /<meta\s+property="og:url"\s+content="([^"]*)"/i,
    twitterCard: /<meta\s+name="twitter:card"\s+content="([^"]*)"/i,
    canonical:   /<link\s+rel="canonical"\s+href="([^"]*)"/i,
};

function extractMeta(html) {
    const meta = {};
    for (const [key, regex] of Object.entries(META_REGEX)) {
        const match = html.match(regex);
        meta[key] = match ? match[1].trim() : null;
    }
    return meta;
}

function checkHtmlFile(file, site) {
    const content = fs.readFileSync(file, 'utf8');
    const relPath = path.relative(site.dir, file);
    const meta = extractMeta(content);
    const issues = [];

    // Must-haves (errors)
    if (!meta.title || meta.title.length === 0)
        issues.push({ level: 'error', msg: 'missing <title>' });
    if (meta.title && meta.title.length > 70)
        issues.push({ level: 'warn', msg: `title too long (${meta.title.length} chars, max 70)` });
    if (!meta.description)
        issues.push({ level: 'error', msg: 'missing meta description' });
    if (meta.description && meta.description.length > 160)
        issues.push({ level: 'warn', msg: `description too long (${meta.description.length} chars, max 160)` });

    // OG tags (warnings for non-index pages, errors for index)
    const isIndex = relPath.includes('index.html');
    const ogLevel = isIndex ? 'error' : 'warn';
    if (!meta.ogTitle)  issues.push({ level: ogLevel, msg: 'missing og:title' });
    if (!meta.ogDesc)   issues.push({ level: ogLevel, msg: 'missing og:description' });
    if (!meta.ogImage)  issues.push({ level: ogLevel, msg: 'missing og:image' });

    // Twitter card
    if (!meta.twitterCard)  issues.push({ level: 'warn', msg: 'missing twitter:card' });

    // Suspicious title content
    if (meta.title && /vite|react app|untitled|todo|test/i.test(meta.title))
        issues.push({ level: 'error', msg: `suspicious title: "${meta.title}"` });

    return { file: relPath, meta, issues };
}

// ─── Hugo site (check built public/) ────────────────────────

function validateHugoSeo(site) {
    const htmlFiles = findFiles(site.publicDir, ['.html']);
    if (htmlFiles.length === 0) {
        console.log(`    ${c.YELLOW}⚠ No HTML files in public dir (build first?)${c.RESET}`);
        return { success: true, errors: 0, warnings: 1 };
    }

    return checkHtmlFiles(htmlFiles, site);
}

// ─── Static site (hrbr-life) ────────────────────────────────

function validateStaticSeo(site) {
    const htmlFiles = findFiles(site.dir, ['.html']);
    return checkHtmlFiles(htmlFiles, site);
}

// ─── Vite site (check index.html + content JSON) ────────────

function validateViteSeo(site) {
    // Check root index.html
    const indexFile = path.join(site.dir, 'index.html');
    const results = [];

    if (fs.existsSync(indexFile)) {
        results.push(checkHtmlFile(indexFile, site));
    }

    // Check content JSON files for SEO metadata
    let contentWarnings = 0;
    for (const contentDir of site.contentDirs) {
        const jsonFiles = findFiles(contentDir, ['.json']);
        for (const file of jsonFiles) {
            try {
                const data = JSON.parse(fs.readFileSync(file, 'utf8'));
                const relPath = path.relative(site.dir, file);

                if (data.metadata?.seo) {
                    const seo = data.metadata.seo;
                    if (!seo.title?.en) { contentWarnings++; }
                    if (!seo.description?.en) { contentWarnings++; }
                }
            } catch (e) { /* skip invalid JSON */ }
        }
    }

    // Aggregate html results
    let errors = 0, warnings = 0;
    for (const r of results) {
        for (const issue of r.issues) {
            if (issue.level === 'error') errors++;
            else warnings++;
            const icon = issue.level === 'error' ? `${c.RED}✗` : `${c.YELLOW}⚠`;
            console.log(`    ${icon}${c.RESET} ${r.file}: ${issue.msg}`);
        }
    }

    if (contentWarnings > 0) {
        warnings += contentWarnings;
        console.log(`    ${c.YELLOW}⚠ ${contentWarnings} content JSON file(s) missing SEO metadata${c.RESET}`);
    }

    if (errors === 0 && warnings === 0) {
        console.log(`    ${c.GREEN}✓ SEO checks passed${c.RESET}`);
    }

    return { success: errors === 0, errors, warnings };
}

// ─── Shared HTML checker ────────────────────────────────────

function checkHtmlFiles(htmlFiles, site) {
    const results = htmlFiles.map(f => checkHtmlFile(f, site));
    let errors = 0, warnings = 0;

    const errorResults = results.filter(r => r.issues.some(i => i.level === 'error'));
    const warnResults = results.filter(r => r.issues.length > 0 && !r.issues.some(i => i.level === 'error'));

    for (const r of errorResults) {
        for (const issue of r.issues) {
            if (issue.level === 'error') { errors++; console.log(`    ${c.RED}✗${c.RESET} ${r.file}: ${issue.msg}`); }
            else { warnings++; console.log(`    ${c.YELLOW}⚠${c.RESET} ${r.file}: ${issue.msg}`); }
        }
    }

    // Only show first 10 warnings to avoid noise
    let shownWarns = 0;
    for (const r of warnResults) {
        for (const issue of r.issues) {
            warnings++;
            if (shownWarns < 10) { console.log(`    ${c.YELLOW}⚠${c.RESET} ${r.file}: ${issue.msg}`); shownWarns++; }
        }
    }
    if (shownWarns < warnings - errorResults.reduce((s, r) => s + r.issues.filter(i => i.level !== 'error').length, 0)) {
        console.log(`    ${c.DIM}  ... and ${warnings - shownWarns - errorResults.reduce((s, r) => s + r.issues.filter(i => i.level !== 'error').length, 0)} more warnings${c.RESET}`);
    }

    const clean = results.filter(r => r.issues.length === 0).length;
    if (clean > 0) console.log(`    ${c.GREEN}✓ ${clean}/${results.length} HTML files fully optimized${c.RESET}`);

    return { success: errors === 0, errors, warnings };
}

// ─── Main entry point ───────────────────────────────────────

function validateSeo(site) {
    switch (site.type) {
        case 'hugo':   return validateHugoSeo(site);
        case 'vite':   return validateViteSeo(site);
        case 'static': return validateStaticSeo(site);
        default:       return validateStaticSeo(site);
    }
}

if (require.main === module) {
    const { SITES } = require('./sites');
    const siteName = process.argv[2] || 'sailsto';
    const site = SITES[siteName];
    if (!site) { console.error('Unknown site:', siteName); process.exit(1); }
    const result = validateSeo(site);
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateSeo };
