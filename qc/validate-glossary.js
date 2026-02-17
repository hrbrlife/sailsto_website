#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════
 *   GLOSSARY VALIDATOR — Hugo and Vite sites
 * ═══════════════════════════════════════════════════════════════
 *
 * Hugo mode (sails.to):
 *   1. data-term values in content ↔ glossary.json definitions
 *   2. glossary.json entries ↔ glossary page files
 *   3. Orphaned definitions (never used)
 *
 * Vite mode (kyclat, melusina, instakycapp):
 *   1. Glossary JSON files have required fields
 *   2. Bilingual consistency (en + fr)
 *   3. SEO metadata completeness
 *   4. Slug/filename consistency
 */

const fs = require('fs');
const path = require('path');
const { c, findFiles, getSiteFiles } = require('./utils');

// ─── Hugo Glossary ──────────────────────────────────────────

function validateHugoGlossary(site) {
    const glossaryJsonPath = site.glossary.json;
    const glossaryPagesDir = site.glossary.pagesDir;

    if (!fs.existsSync(glossaryJsonPath)) {
        console.log(`    ${c.RED}✗ glossary.json not found: ${glossaryJsonPath}${c.RESET}`);
        return { success: false, errors: 1, warnings: 0 };
    }

    const glossaryJson = JSON.parse(fs.readFileSync(glossaryJsonPath, 'utf8'));
    const definedTerms = new Set(Object.keys(glossaryJson));

    // Glossary pages
    const glossaryPages = new Set();
    if (fs.existsSync(glossaryPagesDir)) {
        for (const f of fs.readdirSync(glossaryPagesDir)) {
            if (f.endsWith('.md') && f !== '_index.md') glossaryPages.add(f.replace('.md', ''));
        }
    }

    // Extract data-term usage from all files
    const allFiles = getSiteFiles(site);
    const usedTerms = new Map();
    const dataTermRegex = /data-term="([^"]+)"/g;

    for (const file of allFiles) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        for (let i = 0; i < lines.length; i++) {
            let match;
            while ((match = dataTermRegex.exec(lines[i])) !== null) {
                if (!usedTerms.has(match[1])) usedTerms.set(match[1], []);
                usedTerms.get(match[1]).push({ file: path.relative(site.dir, file), line: i + 1 });
            }
        }
    }

    console.log(`    ${c.DIM}${definedTerms.size} definitions, ${glossaryPages.size} pages, ${usedTerms.size} terms used${c.RESET}`);

    let errors = 0;
    let warnings = 0;

    // CHECK 1: Used but not defined
    const undefined_ = [...usedTerms.keys()].filter(t => !definedTerms.has(t));
    if (undefined_.length > 0) {
        errors += undefined_.length;
        console.log(`    ${c.RED}✗ ${undefined_.length} term(s) used but not defined:${c.RESET}`);
        for (const t of undefined_.slice(0, 8)) {
            const loc = usedTerms.get(t)[0];
            console.log(`      ${c.RED}•${c.RESET} ${t}  ${c.DIM}(${loc.file}:${loc.line})${c.RESET}`);
        }
    } else {
        console.log(`    ${c.GREEN}✓ All used terms have definitions${c.RESET}`);
    }

    // CHECK 2: Defined without pages
    const noPage = [...definedTerms].filter(t => !glossaryPages.has(t));
    if (noPage.length > 0) {
        errors += noPage.length;
        console.log(`    ${c.RED}✗ ${noPage.length} term(s) missing glossary pages${c.RESET}`);
        for (const t of noPage.slice(0, 8)) console.log(`      ${c.RED}•${c.RESET} ${t}`);
    } else {
        console.log(`    ${c.GREEN}✓ All defined terms have pages${c.RESET}`);
    }

    // CHECK 3: Pages without definitions
    const orphanPages = [...glossaryPages].filter(p => !definedTerms.has(p));
    if (orphanPages.length > 0) {
        errors += orphanPages.length;
        console.log(`    ${c.RED}✗ ${orphanPages.length} glossary page(s) without definitions${c.RESET}`);
    }

    // CHECK 4: Orphaned definitions (warning only)
    const orphanDefs = [...definedTerms].filter(t => !usedTerms.has(t));
    if (orphanDefs.length > 0) {
        warnings += orphanDefs.length;
        console.log(`    ${c.YELLOW}⚠ ${orphanDefs.length} defined but unused term(s)${c.RESET}`);
    }

    return { success: errors === 0, errors, warnings };
}

// ─── Vite Glossary (JSON-per-file) ─────────────────────────

function validateViteGlossary(site) {
    const glossaryDir = site.glossary.contentDir;
    if (!fs.existsSync(glossaryDir)) {
        console.log(`    ${c.YELLOW}⚠ Glossary dir not found: ${glossaryDir}${c.RESET}`);
        return { success: true, errors: 0, warnings: 1 };
    }

    const files = fs.readdirSync(glossaryDir).filter(f => f.endsWith('.json'));
    if (files.length === 0) {
        console.log(`    ${c.YELLOW}⚠ No glossary JSON files found${c.RESET}`);
        return { success: true, errors: 0, warnings: 1 };
    }

    console.log(`    ${c.DIM}${files.length} glossary files${c.RESET}`);

    let errors = 0;
    let warnings = 0;
    const requiredFields = ['slug', 'term', 'shortDefinition', 'category'];

    for (const file of files) {
        try {
            const data = JSON.parse(fs.readFileSync(path.join(glossaryDir, file), 'utf8'));

            // Check required fields
            for (const field of requiredFields) {
                if (!data[field]) {
                    errors++;
                    console.log(`    ${c.RED}✗${c.RESET} ${file}: missing ${c.BOLD}${field}${c.RESET}`);
                }
            }

            // Check bilingual fields
            for (const field of ['term', 'shortDefinition']) {
                if (data[field]) {
                    if (!data[field].en) { warnings++; console.log(`    ${c.YELLOW}⚠${c.RESET} ${file}: ${field}.en empty`); }
                    if (!data[field].fr) { warnings++; console.log(`    ${c.YELLOW}⚠${c.RESET} ${file}: ${field}.fr empty`); }
                }
            }

            // Check slug matches filename
            const expectedSlug = file.replace('.json', '');
            if (data.slug && data.slug !== expectedSlug) {
                warnings++;
                console.log(`    ${c.YELLOW}⚠${c.RESET} ${file}: slug "${data.slug}" ≠ filename "${expectedSlug}"`);
            }

            // Check SEO metadata
            if (!data.metadata?.seo?.title?.en) {
                warnings++;
                console.log(`    ${c.YELLOW}⚠${c.RESET} ${file}: missing SEO title`);
            }
        } catch (e) {
            errors++;
            console.log(`    ${c.RED}✗${c.RESET} ${file}: invalid JSON — ${e.message}`);
        }
    }

    if (errors === 0 && warnings === 0) {
        console.log(`    ${c.GREEN}✓ All ${files.length} glossary entries valid${c.RESET}`);
    }

    return { success: errors === 0, errors, warnings };
}

// ─── Main entry point ───────────────────────────────────────

function validateGlossary(site) {
    if (!site.glossary) {
        return { success: true, errors: 0, warnings: 0, skipped: true };
    }

    if (site.glossary.json) {
        return validateHugoGlossary(site);
    } else if (site.glossary.contentDir) {
        return validateViteGlossary(site);
    }

    return { success: true, errors: 0, warnings: 0 };
}

if (require.main === module) {
    const { SITES } = require('./sites');
    const siteName = process.argv[2] || 'sailsto';
    const site = SITES[siteName];
    if (!site) { console.error('Unknown site:', siteName); process.exit(1); }
    const result = validateGlossary(site);
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateGlossary };
