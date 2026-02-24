#!/usr/bin/env node

/**
 * Frontmatter Validation Script (Melusina OS)
 * 
 * Validates frontmatter consistency across content files:
 * 1. Glossary files: category/relatedTerms present and valid
 * 2. Content pages: scripts/stylesheets reference existing files
 * 3. All pages: required fields (title, description)
 * 
 * Usage: node qc/validate-frontmatter.js
 */

const fs = require('fs');
const path = require('path');

const HUGO_ROOT = path.join(__dirname, '..');
const CONTENT_DIR = path.join(HUGO_ROOT, 'content');
const STATIC_DIR = path.join(HUGO_ROOT, 'static');
const DATA_DIR = path.join(HUGO_ROOT, 'data');
const GLOSSARY_DIR = path.join(CONTENT_DIR, 'glossary');

const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';

/**
 * Simple YAML frontmatter parser
 */
function parseFrontmatter(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return null;

    const fm = {};
    const lines = match[1].split('\n');
    let currentKey = null;
    let currentArray = null;

    for (const line of lines) {
        const kvMatch = line.match(/^(\w[\w-]*):\s*"?([^"]*)"?$/);
        if (kvMatch) {
            if (currentArray) { fm[currentKey] = currentArray; currentArray = null; }
            currentKey = kvMatch[1];
            fm[currentKey] = kvMatch[2] || '';
            continue;
        }
        const arrayStart = line.match(/^(\w[\w-]*):\s*$/);
        if (arrayStart) {
            if (currentArray) fm[currentKey] = currentArray;
            currentKey = arrayStart[1];
            currentArray = [];
            continue;
        }
        const arrayItem = line.match(/^\s+-\s+"?([^"]*)"?$/);
        if (arrayItem && currentArray !== null) {
            currentArray.push(arrayItem[1]);
        }
    }
    if (currentArray) fm[currentKey] = currentArray;

    return fm;
}

/**
 * Get glossary page slugs
 */
function getGlossarySlugs() {
    if (!fs.existsSync(GLOSSARY_DIR)) return [];
    return fs.readdirSync(GLOSSARY_DIR)
        .filter(f => f.endsWith('.md') && f !== '_index.md')
        .map(f => f.replace('.md', ''));
}

/**
 * Recursively find all .md files
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

function staticFileExists(refPath) {
    const clean = refPath.replace(/^\//, '').replace(/\?.*$/, '');
    return fs.existsSync(path.join(STATIC_DIR, clean));
}

function validateFrontmatter() {
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   FRONTMATTER VALIDATION REPORT${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    let totalErrors = 0;
    let totalWarnings = 0;

    // Load valid glossary categories
    let validCategories = new Set();
    const catPath = path.join(DATA_DIR, 'glossary_categories.json');
    if (fs.existsSync(catPath)) {
        try {
            const cats = JSON.parse(fs.readFileSync(catPath, 'utf8'));
            validCategories = new Set(Object.keys(cats));
            // Also add labels for case-insensitive matching
            for (const cat of Object.values(cats)) {
                if (cat.label) validCategories.add(cat.label.toLowerCase());
            }
        } catch (e) { /* ignore */ }
    }

    // ─── CHECK 1: Glossary frontmatter ────────────────────────────────
    console.log(`${BOLD}CHECK 1: Glossary Frontmatter (category / relatedTerms)${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const glossarySlugs = getGlossarySlugs();
    const slugSet = new Set(glossarySlugs);
    let missingCategory = [];
    let invalidCategory = [];
    let invalidRelated = [];

    for (const slug of glossarySlugs) {
        const filePath = path.join(GLOSSARY_DIR, `${slug}.md`);
        const fm = parseFrontmatter(filePath);
        if (!fm) {
            totalErrors++;
            missingCategory.push(slug);
            continue;
        }

        if (!fm.category) {
            missingCategory.push(slug);
        } else if (validCategories.size > 0) {
            const catLower = fm.category.toLowerCase();
            if (!validCategories.has(fm.category) && !validCategories.has(catLower)) {
                invalidCategory.push({ slug, category: fm.category });
            }
        }

        if (fm.relatedTerms && Array.isArray(fm.relatedTerms)) {
            for (const rel of fm.relatedTerms) {
                if (!slugSet.has(rel)) {
                    invalidRelated.push({ slug, related: rel });
                }
            }
        }
    }

    console.log(`  Scanned ${CYAN}${glossarySlugs.length}${RESET} glossary files`);
    if (validCategories.size > 0) {
        console.log(`  Valid categories: ${CYAN}${[...new Set(Object.keys(JSON.parse(fs.readFileSync(catPath, 'utf8'))))].join(', ')}${RESET}`);
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
    if (invalidRelated.length > 0) {
        totalWarnings += invalidRelated.length;
        console.log(`  ${YELLOW}⚠ ${invalidRelated.length} invalid relatedTerms reference(s):${RESET}`);
        for (const { slug, related } of invalidRelated.slice(0, 5)) {
            console.log(`    ${YELLOW}•${RESET} ${slug}.md → "${related}" (no such glossary page)`);
        }
        if (invalidRelated.length > 5) console.log(`    ${DIM}... and ${invalidRelated.length - 5} more${RESET}`);
    }

    if (missingCategory.length === 0 && invalidCategory.length === 0 && invalidRelated.length === 0) {
        console.log(`  ${GREEN}✓ All glossary frontmatter valid${RESET}`);
    }
    console.log();

    // ─── CHECK 2: All content pages have basic frontmatter ────────────
    console.log(`${BOLD}CHECK 2: Content Pages - Required Fields${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const contentFiles = findContentFiles(CONTENT_DIR);
    let missingTitle = [];
    let missingDescription = [];

    for (const file of contentFiles) {
        const fm = parseFrontmatter(file);
        const relFile = path.relative(HUGO_ROOT, file);
        if (!fm) continue;

        if (!fm.title) missingTitle.push(relFile);
        if (!fm.description) missingDescription.push(relFile);
    }

    console.log(`  Scanned ${CYAN}${contentFiles.length}${RESET} content files`);

    if (missingTitle.length > 0) {
        totalWarnings += missingTitle.length;
        console.log(`  ${YELLOW}⚠ ${missingTitle.length} file(s) missing "title":${RESET}`);
        for (const f of missingTitle.slice(0, 5)) console.log(`    ${YELLOW}•${RESET} ${f}`);
        if (missingTitle.length > 5) console.log(`    ${DIM}... and ${missingTitle.length - 5} more${RESET}`);
    }
    if (missingDescription.length > 0) {
        totalWarnings += missingDescription.length;
        console.log(`  ${YELLOW}⚠ ${missingDescription.length} file(s) missing "description":${RESET}`);
        for (const f of missingDescription.slice(0, 5)) console.log(`    ${YELLOW}•${RESET} ${f}`);
        if (missingDescription.length > 5) console.log(`    ${DIM}... and ${missingDescription.length - 5} more${RESET}`);
    }

    if (missingTitle.length === 0 && missingDescription.length === 0) {
        console.log(`  ${GREEN}✓ All content pages have required fields${RESET}`);
    }
    console.log();

    // ─── CHECK 3: Script/stylesheet references ────────────────────────
    console.log(`${BOLD}CHECK 3: Script & Stylesheet References in Frontmatter${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    let brokenScripts = [];
    let brokenStyles = [];

    for (const file of contentFiles) {
        const fm = parseFrontmatter(file);
        if (!fm) continue;
        const relFile = path.relative(HUGO_ROOT, file);

        if (fm.scripts && Array.isArray(fm.scripts)) {
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

if (require.main === module) {
    const result = validateFrontmatter();
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateFrontmatter };
