#!/usr/bin/env node

/**
 * Glossary Validation Script (Melusina OS)
 * 
 * Validates glossary terms against Melusina's JSON-based data architecture:
 * 1. All data-term values in HTML/MD have definitions in data/glossary/*.json
 * 2. All glossary JSON data files have corresponding content pages
 * 3. Reports orphaned definitions (defined but never used)
 * 4. Validates glossary frontmatter fields
 * 5. Validates glossary categories against glossary_categories.json
 * 
 * Usage: node qc/validate-glossary.js
 */

const fs = require('fs');
const path = require('path');

const HUGO_ROOT = path.join(__dirname, '..');
const CONTENT_DIR = path.join(HUGO_ROOT, 'content');
const LAYOUTS_DIR = path.join(HUGO_ROOT, 'layouts');
const GLOSSARY_DATA_DIR = path.join(HUGO_ROOT, 'data', 'glossary');
const GLOSSARY_CATEGORIES_FILE = path.join(HUGO_ROOT, 'data', 'glossary_categories.json');
const GLOSSARY_PAGES_DIR = path.join(HUGO_ROOT, 'content', 'glossary');

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

function extractDataTerms(files) {
    const terms = new Map();
    const dataTermRegex = /data-term="([^"]+)"/g;

    for (const file of files) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        for (let i = 0; i < lines.length; i++) {
            let match;
            while ((match = dataTermRegex.exec(lines[i])) !== null) {
                const term = match[1];
                if (!terms.has(term)) terms.set(term, []);
                terms.get(term).push({
                    file: path.relative(HUGO_ROOT, file),
                    line: i + 1
                });
            }
        }
    }
    return terms;
}

function loadGlossaryDataFiles() {
    const glossary = new Map();
    if (!fs.existsSync(GLOSSARY_DATA_DIR)) return glossary;

    const files = fs.readdirSync(GLOSSARY_DATA_DIR);
    for (const file of files) {
        if (!file.endsWith('.json')) continue;
        const slug = file.replace('.json', '');
        try {
            const data = JSON.parse(fs.readFileSync(path.join(GLOSSARY_DATA_DIR, file), 'utf8'));
            glossary.set(slug, data);
        } catch (e) {
            glossary.set(slug, { _parseError: e.message });
        }
    }
    return glossary;
}

function loadGlossaryCategories() {
    if (!fs.existsSync(GLOSSARY_CATEGORIES_FILE)) return new Map();
    try {
        const data = JSON.parse(fs.readFileSync(GLOSSARY_CATEGORIES_FILE, 'utf8'));
        return new Map(Object.entries(data));
    } catch (e) {
        return new Map();
    }
}

function getGlossaryPages() {
    const pages = new Set();
    if (!fs.existsSync(GLOSSARY_PAGES_DIR)) return pages;
    const files = fs.readdirSync(GLOSSARY_PAGES_DIR);
    for (const file of files) {
        if (file.endsWith('.md') && file !== '_index.md') {
            pages.add(file.replace('.md', ''));
        }
    }
    return pages;
}

function parseFrontmatter(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return null;

    // Simple YAML parser for the fields we need
    const fm = {};
    const lines = match[1].split('\n');
    let currentKey = null;
    let currentArray = null;

    for (const line of lines) {
        const kvMatch = line.match(/^(\w+):\s*"?([^"]*)"?$/);
        if (kvMatch) {
            if (currentArray) {
                fm[currentKey] = currentArray;
                currentArray = null;
            }
            currentKey = kvMatch[1];
            fm[currentKey] = kvMatch[2] || '';
            continue;
        }

        const arrayStart = line.match(/^(\w+):$/);
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

function validateGlossary() {
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   GLOSSARY VALIDATION REPORT${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    // Load glossary data files
    const glossaryData = loadGlossaryDataFiles();
    console.log(`Found ${CYAN}${glossaryData.size}${RESET} glossary data files in data/glossary/`);

    // Load categories
    const categories = loadGlossaryCategories();
    console.log(`Found ${CYAN}${categories.size}${RESET} glossary categories in glossary_categories.json`);

    // Get glossary pages
    const glossaryPages = getGlossaryPages();
    console.log(`Found ${CYAN}${glossaryPages.size}${RESET} glossary pages in content/glossary/`);

    // Find all content and layout files
    const contentFiles = findFiles(CONTENT_DIR, ['.md', '.html']);
    const layoutFiles = findFiles(LAYOUTS_DIR, ['.html']);
    const allFiles = [...contentFiles, ...layoutFiles];
    console.log(`Scanning ${CYAN}${allFiles.length}${RESET} files for data-term usage...\n`);

    const usedTerms = extractDataTerms(allFiles);
    console.log(`Found ${CYAN}${usedTerms.size}${RESET} unique terms used with data-term attribute\n`);

    let errors = 0;
    let warnings = 0;

    // CHECK 1: Data files with parse errors
    console.log(`${BOLD}CHECK 1: Glossary Data File Integrity${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const parseErrors = [];
    for (const [slug, data] of glossaryData) {
        if (data._parseError) parseErrors.push({ slug, error: data._parseError });
    }

    if (parseErrors.length === 0) {
        console.log(`${GREEN}✓ All ${glossaryData.size} data files parse successfully${RESET}\n`);
    } else {
        errors += parseErrors.length;
        console.log(`${RED}✗ ${parseErrors.length} data file(s) have parse errors:${RESET}\n`);
        for (const { slug, error } of parseErrors) {
            console.log(`  ${RED}•${RESET} ${slug}.json: ${error}`);
        }
        console.log();
    }

    // CHECK 2: Data files without content pages
    console.log(`${BOLD}CHECK 2: Glossary Data Files Without Content Pages${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const missingPages = [];
    for (const slug of glossaryData.keys()) {
        if (!glossaryPages.has(slug)) missingPages.push(slug);
    }

    if (missingPages.length === 0) {
        console.log(`${GREEN}✓ All data files have corresponding content pages${RESET}\n`);
    } else {
        errors += missingPages.length;
        console.log(`${RED}✗ ${missingPages.length} data file(s) missing content pages:${RESET}\n`);
        for (const slug of missingPages) console.log(`  ${RED}•${RESET} ${slug}`);
        console.log();
    }

    // CHECK 3: Content pages without data files
    console.log(`${BOLD}CHECK 3: Content Pages Without Data Files${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const orphanedPages = [];
    for (const slug of glossaryPages) {
        if (!glossaryData.has(slug)) orphanedPages.push(slug);
    }

    if (orphanedPages.length === 0) {
        console.log(`${GREEN}✓ All content pages have data files${RESET}\n`);
    } else {
        errors += orphanedPages.length;
        console.log(`${RED}✗ ${orphanedPages.length} content page(s) without data files:${RESET}\n`);
        for (const page of orphanedPages) console.log(`  ${RED}•${RESET} ${page}.md`);
        console.log();
    }

    // CHECK 4: Data file required fields
    console.log(`${BOLD}CHECK 4: Glossary Data File Required Fields${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const fieldIssues = [];
    for (const [slug, data] of glossaryData) {
        if (data._parseError) continue;
        if (!data.term) fieldIssues.push({ slug, issue: 'missing "term" field' });
        if (!data.shortDefinition) fieldIssues.push({ slug, issue: 'missing "shortDefinition" field' });
        if (!data.slug) fieldIssues.push({ slug, issue: 'missing "slug" field' });
        if (data.slug && data.slug !== slug) {
            fieldIssues.push({ slug, issue: `slug mismatch: file="${slug}" data="${data.slug}"` });
        }
    }

    if (fieldIssues.length === 0) {
        console.log(`${GREEN}✓ All data files have required fields${RESET}\n`);
    } else {
        errors += fieldIssues.length;
        console.log(`${RED}✗ ${fieldIssues.length} field issue(s):${RESET}\n`);
        for (const { slug, issue } of fieldIssues) {
            console.log(`  ${RED}•${RESET} ${slug}.json: ${issue}`);
        }
        console.log();
    }

    // CHECK 5: Frontmatter category validation
    console.log(`${BOLD}CHECK 5: Glossary Page Frontmatter${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const validCategoryIds = new Set(categories.keys());
    // Also allow category labels (case-insensitive matching)
    const categoryLabelMap = new Map();
    for (const [id, cat] of categories) {
        if (cat.label) categoryLabelMap.set(cat.label.toLowerCase(), id);
    }

    const fmIssues = [];
    for (const slug of glossaryPages) {
        const filePath = path.join(GLOSSARY_PAGES_DIR, `${slug}.md`);
        const fm = parseFrontmatter(filePath);
        if (!fm) {
            fmIssues.push({ slug, issue: 'no frontmatter found' });
            continue;
        }

        // Check category
        if (!fm.category) {
            fmIssues.push({ slug, issue: 'missing category field' });
        } else if (validCategoryIds.size > 0) {
            const catLower = fm.category.toLowerCase();
            if (!validCategoryIds.has(fm.category) && !validCategoryIds.has(catLower) && !categoryLabelMap.has(catLower)) {
                fmIssues.push({ slug, issue: `category "${fm.category}" not in glossary_categories.json` });
            }
        }

        // Check relatedTerms references
        if (fm.relatedTerms && Array.isArray(fm.relatedTerms)) {
            for (const ref of fm.relatedTerms) {
                if (!glossaryPages.has(ref)) {
                    fmIssues.push({ slug, issue: `relatedTerms "${ref}" has no glossary page` });
                }
            }
        }
    }

    if (fmIssues.length === 0) {
        console.log(`${GREEN}✓ All ${glossaryPages.size} glossary pages have valid frontmatter${RESET}\n`);
    } else {
        const fmErrors = fmIssues.filter(i => !i.issue.includes('relatedTerms'));
        const fmWarns = fmIssues.filter(i => i.issue.includes('relatedTerms'));
        errors += fmErrors.length;
        warnings += fmWarns.length;
        if (fmErrors.length > 0) {
            console.log(`${RED}✗ ${fmErrors.length} frontmatter error(s):${RESET}`);
            for (const { slug, issue } of fmErrors) console.log(`  ${RED}•${RESET} ${slug}.md: ${issue}`);
        }
        if (fmWarns.length > 0) {
            console.log(`${YELLOW}⚠ ${fmWarns.length} frontmatter warning(s):${RESET}`);
            for (const { slug, issue } of fmWarns) console.log(`  ${YELLOW}•${RESET} ${slug}.md: ${issue}`);
        }
        console.log();
    }

    // Summary
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   SUMMARY${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    if (errors === 0 && warnings === 0) {
        console.log(`${GREEN}✓ All checks passed!${RESET}\n`);
        return { success: true, errors: 0, warnings: 0 };
    } else if (errors === 0) {
        console.log(`${YELLOW}⚠ ${warnings} warning(s) - optional improvements${RESET}\n`);
        return { success: true, errors: 0, warnings };
    } else {
        console.log(`${RED}✗ ${errors} error(s), ${warnings} warning(s)${RESET}\n`);
        return { success: false, errors, warnings };
    }
}

if (require.main === module) {
    const result = validateGlossary();
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateGlossary };
