#!/usr/bin/env node

/**
 * Glossary Validation Script
 * 
 * Performs mechanical checks on glossary terms:
 * 1. All data-term values used in HTML/MD have definitions in glossary.json
 * 2. All glossary.json definitions have corresponding glossary pages
 * 3. Reports orphaned definitions (defined but never used)
 * 
 * Usage: node qc/validate-glossary.js
 */

const fs = require('fs');
const path = require('path');

// Configuration
const HUGO_ROOT = path.join(__dirname, '..');
const GLOSSARY_JSON = path.join(HUGO_ROOT, 'static/assets/content/glossary.json');
const CONTENT_DIR = path.join(HUGO_ROOT, 'content');
const LAYOUTS_DIR = path.join(HUGO_ROOT, 'layouts');
const GLOSSARY_PAGES_DIR = path.join(HUGO_ROOT, 'content/knowledge/glossary');

// ANSI colors for output
const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const BLUE = '\x1b[34m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';

/**
 * Recursively find all files with given extensions in a directory
 */
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

/**
 * Extract all data-term values from files
 */
function extractDataTerms(files) {
    const terms = new Map(); // term -> [{ file, line, context }]
    const dataTermRegex = /data-term="([^"]+)"/g;
    
    for (const file of files) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            let match;
            while ((match = dataTermRegex.exec(line)) !== null) {
                const term = match[1];
                if (!terms.has(term)) {
                    terms.set(term, []);
                }
                terms.get(term).push({
                    file: path.relative(HUGO_ROOT, file),
                    line: i + 1,
                    context: line.trim().substring(0, 100)
                });
            }
        }
    }
    return terms;
}

/**
 * Load glossary JSON definitions
 */
function loadGlossaryJson() {
    if (!fs.existsSync(GLOSSARY_JSON)) {
        console.error(`${RED}Error: glossary.json not found at ${GLOSSARY_JSON}${RESET}`);
        return null;
    }
    const content = fs.readFileSync(GLOSSARY_JSON, 'utf8');
    return JSON.parse(content);
}

/**
 * Get list of glossary page slugs from content/knowledge/glossary
 */
function getGlossaryPages() {
    const pages = new Set();
    if (!fs.existsSync(GLOSSARY_PAGES_DIR)) {
        console.warn(`${YELLOW}Warning: Glossary pages directory not found at ${GLOSSARY_PAGES_DIR}${RESET}`);
        return pages;
    }
    
    const files = fs.readdirSync(GLOSSARY_PAGES_DIR);
    for (const file of files) {
        if (file.endsWith('.md') && file !== '_index.md') {
            pages.add(file.replace('.md', ''));
        }
    }
    return pages;
}

/**
 * Main validation function
 */
function validateGlossary() {
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   GLOSSARY VALIDATION REPORT${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);
    
    // Load glossary definitions
    const glossaryJson = loadGlossaryJson();
    if (!glossaryJson) {
        return { success: false, errors: 1, warnings: 0 };
    }
    
    const definedTerms = new Set(Object.keys(glossaryJson));
    console.log(`Found ${CYAN}${definedTerms.size}${RESET} definitions in glossary.json`);
    
    // Get glossary pages
    const glossaryPages = getGlossaryPages();
    console.log(`Found ${CYAN}${glossaryPages.size}${RESET} glossary pages in content/knowledge/glossary/`);
    
    // Find all content and layout files
    const contentFiles = findFiles(CONTENT_DIR, ['.md', '.html']);
    const layoutFiles = findFiles(LAYOUTS_DIR, ['.html']);
    const allFiles = [...contentFiles, ...layoutFiles];
    console.log(`Scanning ${CYAN}${allFiles.length}${RESET} files for data-term usage...\n`);
    
    // Extract used terms
    const usedTerms = extractDataTerms(allFiles);
    console.log(`Found ${CYAN}${usedTerms.size}${RESET} unique terms used with data-term attribute\n`);
    
    let errors = 0;
    let warnings = 0;
    
    // CHECK 1: Terms used but not defined
    console.log(`${BOLD}CHECK 1: Terms used but NOT defined in glossary.json${RESET}`);
    console.log('────────────────────────────────────────────────────────────');
    
    const undefinedTerms = [];
    for (const term of usedTerms.keys()) {
        if (!definedTerms.has(term)) {
            undefinedTerms.push(term);
        }
    }
    
    if (undefinedTerms.length === 0) {
        console.log(`${GREEN}✓ All used terms have definitions${RESET}\n`);
    } else {
        errors += undefinedTerms.length;
        console.log(`${RED}✗ ${undefinedTerms.length} term(s) missing definitions:${RESET}\n`);
        for (const term of undefinedTerms) {
            const usages = usedTerms.get(term);
            console.log(`  ${RED}•${RESET} ${BOLD}${term}${RESET}`);
            for (const usage of usages.slice(0, 2)) {
                console.log(`    ${DIM}${usage.file}:${usage.line}${RESET}`);
            }
            if (usages.length > 2) {
                console.log(`    ${DIM}... and ${usages.length - 2} more usages${RESET}`);
            }
        }
        console.log();
    }
    
    // CHECK 2: Definitions without glossary pages
    console.log(`${BOLD}CHECK 2: Terms in glossary.json without glossary pages${RESET}`);
    console.log('────────────────────────────────────────────────────────────');
    
    const missingPages = [];
    for (const term of definedTerms) {
        if (!glossaryPages.has(term)) {
            missingPages.push(term);
        }
    }
    
    if (missingPages.length === 0) {
        console.log(`${GREEN}✓ All defined terms have glossary pages${RESET}\n`);
    } else {
        errors += missingPages.length;
        console.log(`${RED}✗ ${missingPages.length} term(s) missing glossary pages:${RESET}\n`);
        for (const term of missingPages) {
            console.log(`  ${RED}•${RESET} ${term}`);
        }
        console.log();
    }
    
    // CHECK 3: Glossary pages without definitions
    console.log(`${BOLD}CHECK 3: Glossary pages without JSON definitions${RESET}`);
    console.log('────────────────────────────────────────────────────────────');
    
    const orphanedPages = [];
    for (const page of glossaryPages) {
        if (!definedTerms.has(page)) {
            orphanedPages.push(page);
        }
    }
    
    if (orphanedPages.length === 0) {
        console.log(`${GREEN}✓ All glossary pages have JSON definitions${RESET}\n`);
    } else {
        errors += orphanedPages.length;
        console.log(`${RED}✗ ${orphanedPages.length} glossary page(s) without definitions:${RESET}\n`);
        for (const page of orphanedPages) {
            console.log(`  ${RED}•${RESET} ${page}.md`);
        }
        console.log();
    }
    
    // CHECK 4: Orphaned definitions (defined but never used)
    console.log(`${BOLD}CHECK 4: Orphaned definitions (defined but never used)${RESET}`);
    console.log('────────────────────────────────────────────────────────────');
    
    const orphanedDefs = [];
    for (const term of definedTerms) {
        if (!usedTerms.has(term)) {
            orphanedDefs.push(term);
        }
    }
    
    if (orphanedDefs.length === 0) {
        console.log(`${GREEN}✓ All defined terms are used somewhere${RESET}\n`);
    } else {
        warnings += orphanedDefs.length;
        console.log(`${YELLOW}⚠ ${orphanedDefs.length} terms are defined but never used:${RESET}\n`);
        for (const term of orphanedDefs) {
            console.log(`  ${YELLOW}•${RESET} ${term}`);
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

// Run if called directly
if (require.main === module) {
    const result = validateGlossary();
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateGlossary };
