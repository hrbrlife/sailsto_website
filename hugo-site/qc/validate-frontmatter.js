#!/usr/bin/env node

/**
 * Frontmatter Validation Script
 * 
 * Validates frontmatter consistency across content files:
 * 1. Glossary files: category/tags/relatedTerms present and valid
 * 2. FAQ: faqItems have category field
 * 3. Content pages: scripts/stylesheets arrays reference existing files
 * 
 * Usage: node qc/validate-frontmatter.js
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Configuration
const HUGO_ROOT = path.join(__dirname, '..');
const CONTENT_DIR = path.join(HUGO_ROOT, 'content');
const STATIC_DIR = path.join(HUGO_ROOT, 'static');
const DATA_DIR = path.join(HUGO_ROOT, 'data');
const GLOSSARY_DIR = path.join(CONTENT_DIR, 'knowledge', 'glossary');
const FAQ_FILE = path.join(CONTENT_DIR, 'knowledge', 'faq.md');

// ANSI colors
const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';

/**
 * Parse frontmatter from a markdown file
 */
function parseFrontmatter(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return null;
    try {
        return yaml.load(match[1]);
    } catch (e) {
        return null;
    }
}

/**
 * Get all glossary page slugs
 */
function getGlossarySlugs() {
    if (!fs.existsSync(GLOSSARY_DIR)) return [];
    return fs.readdirSync(GLOSSARY_DIR)
        .filter(f => f.endsWith('.md') && f !== '_index.md')
        .map(f => f.replace('.md', ''));
}

/**
 * Recursively find all .md files in content/
 */
function findContentFiles(dir, files = []) {
    if (!fs.existsSync(dir)) return files;
    const items = fs.readdirSync(dir, { withFileTypes: true });
    for (const item of items) {
        const fullPath = path.join(dir, item.name);
        if (item.isDirectory()) {
            findContentFiles(fullPath, files);
        } else if (item.name.endsWith('.md')) {
            files.push(fullPath);
        }
    }
    return files;
}

/**
 * Check if a static-rooted path exists
 */
function staticFileExists(refPath) {
    // Strip leading slash and query strings, then check in static/
    const clean = refPath.replace(/^\//,  '').replace(/\?.*$/, '');
    return fs.existsSync(path.join(STATIC_DIR, clean));
}

/**
 * Main validation function
 */
function validateFrontmatter() {
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   FRONTMATTER VALIDATION REPORT${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    let totalErrors = 0;
    let totalWarnings = 0;

    // Load valid categories from data/categories.yaml
    let validGlossaryCategories = new Set();
    let validFaqCategories = new Set();
    const catPath = path.join(DATA_DIR, 'categories.yaml');
    if (fs.existsSync(catPath)) {
        try {
            const cats = yaml.load(fs.readFileSync(catPath, 'utf8'));
            if (cats.glossary_categories) validGlossaryCategories = new Set(Object.keys(cats.glossary_categories));
            if (cats.faq_categories) validFaqCategories = new Set(Object.keys(cats.faq_categories));
        } catch (e) { /* ignore */ }
    }

    // ─── CHECK 1: Glossary frontmatter ────────────────────────────────
    console.log(`${BOLD}CHECK 1: Glossary Frontmatter (category / tags / relatedTerms)${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const glossarySlugs = getGlossarySlugs();
    const slugSet = new Set(glossarySlugs);
    let missingCategory = [];
    let invalidCategory = [];
    let missingTags = [];
    let invalidRelated = [];

    for (const slug of glossarySlugs) {
        const filePath = path.join(GLOSSARY_DIR, `${slug}.md`);
        const fm = parseFrontmatter(filePath);
        if (!fm) {
            totalErrors++;
            missingCategory.push(slug);
            continue;
        }

        // Category check
        if (!fm.category) {
            missingCategory.push(slug);
        } else if (validGlossaryCategories.size > 0 && !validGlossaryCategories.has(fm.category)) {
            invalidCategory.push({ slug, category: fm.category });
        }

        // Tags check
        if (!fm.tags || !Array.isArray(fm.tags) || fm.tags.length === 0) {
            missingTags.push(slug);
        }

        // relatedTerms check — each must be a valid slug
        if (fm.relatedTerms && Array.isArray(fm.relatedTerms)) {
            for (const rel of fm.relatedTerms) {
                if (!slugSet.has(rel)) {
                    invalidRelated.push({ slug, related: rel });
                }
            }
        }
    }

    console.log(`  Scanned ${CYAN}${glossarySlugs.length}${RESET} glossary files`);
    if (validGlossaryCategories.size > 0) {
        console.log(`  Valid categories: ${CYAN}${[...validGlossaryCategories].join(', ')}${RESET}`);
    }

    if (missingCategory.length > 0) {
        totalErrors += missingCategory.length;
        console.log(`  ${RED}✗ ${missingCategory.length} file(s) missing "category":${RESET}`);
        for (const s of missingCategory.slice(0, 5)) console.log(`    ${RED}•${RESET} ${s}.md`);
        if (missingCategory.length > 5) console.log(`    ${DIM}... and ${missingCategory.length - 5} more${RESET}`);
    }
    if (invalidCategory.length > 0) {
        totalErrors += invalidCategory.length;
        console.log(`  ${RED}✗ ${invalidCategory.length} file(s) with invalid category:${RESET}`);
        for (const { slug, category } of invalidCategory.slice(0, 5)) {
            console.log(`    ${RED}•${RESET} ${slug}.md → "${category}"`);
        }
    }
    if (missingTags.length > 0) {
        totalWarnings += missingTags.length;
        console.log(`  ${YELLOW}⚠ ${missingTags.length} file(s) missing "tags":${RESET}`);
        for (const s of missingTags.slice(0, 5)) console.log(`    ${YELLOW}•${RESET} ${s}.md`);
        if (missingTags.length > 5) console.log(`    ${DIM}... and ${missingTags.length - 5} more${RESET}`);
    }
    if (invalidRelated.length > 0) {
        totalErrors += invalidRelated.length;
        console.log(`  ${RED}✗ ${invalidRelated.length} invalid relatedTerms reference(s):${RESET}`);
        for (const { slug, related } of invalidRelated.slice(0, 5)) {
            console.log(`    ${RED}•${RESET} ${slug}.md → "${related}" (no such glossary page)`);
        }
        if (invalidRelated.length > 5) console.log(`    ${DIM}... and ${invalidRelated.length - 5} more${RESET}`);
    }

    if (missingCategory.length === 0 && invalidCategory.length === 0 && missingTags.length === 0 && invalidRelated.length === 0) {
        console.log(`  ${GREEN}✓ All glossary frontmatter valid${RESET}`);
    }
    console.log();

    // ─── CHECK 2: FAQ frontmatter ─────────────────────────────────────
    console.log(`${BOLD}CHECK 2: FAQ Frontmatter (faqItems categories)${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    if (!fs.existsSync(FAQ_FILE)) {
        console.log(`  ${YELLOW}⚠ FAQ file not found: knowledge/faq.md${RESET}\n`);
        totalWarnings++;
    } else {
        const fm = parseFrontmatter(FAQ_FILE);
        if (!fm || !fm.faqItems || !Array.isArray(fm.faqItems)) {
            console.log(`  ${RED}✗ No faqItems found in frontmatter${RESET}\n`);
            totalErrors++;
        } else {
            let faqMissingCat = 0;
            let faqInvalidCat = 0;
            for (const item of fm.faqItems) {
                if (!item.category) {
                    faqMissingCat++;
                } else if (validFaqCategories.size > 0 && !validFaqCategories.has(item.category)) {
                    faqInvalidCat++;
                }
            }
            console.log(`  Scanned ${CYAN}${fm.faqItems.length}${RESET} FAQ items`);
            if (faqMissingCat > 0) {
                totalErrors += faqMissingCat;
                console.log(`  ${RED}✗ ${faqMissingCat} item(s) missing "category"${RESET}`);
            }
            if (faqInvalidCat > 0) {
                totalErrors += faqInvalidCat;
                console.log(`  ${RED}✗ ${faqInvalidCat} item(s) with invalid category${RESET}`);
            }
            if (faqMissingCat === 0 && faqInvalidCat === 0) {
                console.log(`  ${GREEN}✓ All FAQ items have valid categories${RESET}`);
            }
        }
    }
    console.log();

    // ─── CHECK 3: Script/stylesheet references ────────────────────────
    console.log(`${BOLD}CHECK 3: Script & Stylesheet References in Frontmatter${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const contentFiles = findContentFiles(CONTENT_DIR);
    let brokenScripts = [];
    let brokenStyles = [];
    let checkedFiles = 0;

    for (const file of contentFiles) {
        const fm = parseFrontmatter(file);
        if (!fm) continue;
        const relFile = path.relative(HUGO_ROOT, file);

        if (fm.scripts && Array.isArray(fm.scripts)) {
            checkedFiles++;
            for (const script of fm.scripts) {
                if (!staticFileExists(script)) {
                    brokenScripts.push({ file: relFile, ref: script });
                }
            }
        }

        if (fm.stylesheets && Array.isArray(fm.stylesheets)) {
            for (const style of fm.stylesheets) {
                if (!staticFileExists(style)) {
                    brokenStyles.push({ file: relFile, ref: style });
                }
            }
        }
    }

    console.log(`  Scanned ${CYAN}${contentFiles.length}${RESET} content files`);

    if (brokenScripts.length > 0) {
        totalErrors += brokenScripts.length;
        console.log(`  ${RED}✗ ${brokenScripts.length} broken script reference(s):${RESET}`);
        for (const { file, ref } of brokenScripts) {
            console.log(`    ${RED}•${RESET} ${ref}`);
            console.log(`      ${DIM}in ${file}${RESET}`);
        }
    }
    if (brokenStyles.length > 0) {
        totalErrors += brokenStyles.length;
        console.log(`  ${RED}✗ ${brokenStyles.length} broken stylesheet reference(s):${RESET}`);
        for (const { file, ref } of brokenStyles) {
            console.log(`    ${RED}•${RESET} ${ref}`);
            console.log(`      ${DIM}in ${file}${RESET}`);
        }
    }
    if (brokenScripts.length === 0 && brokenStyles.length === 0) {
        console.log(`  ${GREEN}✓ All script/stylesheet references valid${RESET}`);
    }
    console.log();

    // ─── Summary ──────────────────────────────────────────────────────
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   SUMMARY${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    if (totalErrors === 0 && totalWarnings === 0) {
        console.log(`${GREEN}✓ All frontmatter checks passed!${RESET}\n`);
        return { success: true, errors: 0, warnings: 0 };
    } else if (totalErrors === 0) {
        console.log(`${YELLOW}⚠ ${totalWarnings} warning(s)${RESET}\n`);
        return { success: true, errors: 0, warnings: totalWarnings };
    } else {
        console.log(`${RED}✗ ${totalErrors} error(s), ${totalWarnings} warning(s)${RESET}\n`);
        return { success: false, errors: totalErrors, warnings: totalWarnings };
    }
}

// Run if called directly
if (require.main === module) {
    const result = validateFrontmatter();
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateFrontmatter };
