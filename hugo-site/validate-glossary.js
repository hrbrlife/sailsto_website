#!/usr/bin/env node

/**
 * Glossary Validation Script
 * 
 * Performs mechanical checks on glossary terms:
 * 1. All data-term values used in HTML/MD have definitions in glossary.json
 * 2. All glossary.json definitions have corresponding glossary pages
 * 3. Reports orphaned definitions (defined but never used)
 * 
 * Usage: node validate-glossary.js
 */

const fs = require('fs');
const path = require('path');

// Configuration
const HUGO_ROOT = __dirname;
const GLOSSARY_JSON = path.join(HUGO_ROOT, 'static/assets/content/glossary.json');
const CONTENT_DIR = path.join(HUGO_ROOT, 'content');
const LAYOUTS_DIR = path.join(HUGO_ROOT, 'layouts');
const GLOSSARY_PAGES_DIR = path.join(HUGO_ROOT, 'content/knowledge/glossary');

// ANSI colors for output
const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const BLUE = '\x1b[34m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';

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
function validate() {
    console.log(`\n${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   GLOSSARY VALIDATION REPORT${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);
    
    let errorCount = 0;
    let warningCount = 0;
    
    // 1. Load glossary definitions
    const glossaryJson = loadGlossaryJson();
    if (!glossaryJson) {
        return 1;
    }
    const definedTerms = new Set(Object.keys(glossaryJson));
    console.log(`${BLUE}Found ${definedTerms.size} definitions in glossary.json${RESET}`);
    
    // 2. Get glossary pages
    const glossaryPages = getGlossaryPages();
    console.log(`${BLUE}Found ${glossaryPages.size} glossary pages in content/knowledge/glossary/${RESET}`);
    
    // 3. Find all content and layout files
    const contentFiles = findFiles(CONTENT_DIR, ['.md', '.html']);
    const layoutFiles = findFiles(LAYOUTS_DIR, ['.html']);
    const allFiles = [...contentFiles, ...layoutFiles];
    console.log(`${BLUE}Scanning ${allFiles.length} files for data-term usage...${RESET}\n`);
    
    // 4. Extract all data-term values used in templates/content
    const usedTerms = extractDataTerms(allFiles);
    console.log(`${BLUE}Found ${usedTerms.size} unique terms used with data-term attribute${RESET}\n`);
    
    // ═══════════════════════════════════════════════════════════════
    // CHECK 1: Terms used but not defined in glossary.json
    // ═══════════════════════════════════════════════════════════════
    console.log(`${BOLD}CHECK 1: Terms used but NOT defined in glossary.json${RESET}`);
    console.log('─'.repeat(60));
    
    const undefinedTerms = [];
    for (const [term, usages] of usedTerms) {
        if (!definedTerms.has(term)) {
            undefinedTerms.push({ term, usages });
        }
    }
    
    if (undefinedTerms.length === 0) {
        console.log(`${GREEN}✓ All used terms have definitions${RESET}\n`);
    } else {
        console.log(`${RED}✗ ${undefinedTerms.length} terms are MISSING definitions:${RESET}\n`);
        for (const { term, usages } of undefinedTerms) {
            console.log(`  ${RED}• ${term}${RESET}`);
            for (const usage of usages.slice(0, 3)) {
                console.log(`    ${YELLOW}→ ${usage.file}:${usage.line}${RESET}`);
            }
            if (usages.length > 3) {
                console.log(`    ${YELLOW}  ... and ${usages.length - 3} more usages${RESET}`);
            }
        }
        errorCount += undefinedTerms.length;
        console.log();
    }
    
    // ═══════════════════════════════════════════════════════════════
    // CHECK 2: Terms defined in JSON but no glossary page exists
    // ═══════════════════════════════════════════════════════════════
    console.log(`${BOLD}CHECK 2: Terms in glossary.json without glossary pages${RESET}`);
    console.log('─'.repeat(60));
    
    const missingPages = [];
    for (const term of definedTerms) {
        if (!glossaryPages.has(term)) {
            missingPages.push(term);
        }
    }
    
    if (missingPages.length === 0) {
        console.log(`${GREEN}✓ All defined terms have glossary pages${RESET}\n`);
    } else {
        console.log(`${YELLOW}⚠ ${missingPages.length} terms need glossary pages:${RESET}\n`);
        for (const term of missingPages.sort()) {
            console.log(`  ${YELLOW}• ${term}${RESET}`);
        }
        warningCount += missingPages.length;
        console.log();
    }
    
    // ═══════════════════════════════════════════════════════════════
    // CHECK 3: Glossary pages that don't have JSON definitions
    // ═══════════════════════════════════════════════════════════════
    console.log(`${BOLD}CHECK 3: Glossary pages without JSON definitions${RESET}`);
    console.log('─'.repeat(60));
    
    const pagesWithoutDefs = [];
    for (const page of glossaryPages) {
        if (!definedTerms.has(page)) {
            pagesWithoutDefs.push(page);
        }
    }
    
    if (pagesWithoutDefs.length === 0) {
        console.log(`${GREEN}✓ All glossary pages have JSON definitions${RESET}\n`);
    } else {
        console.log(`${RED}✗ ${pagesWithoutDefs.length} glossary pages need JSON definitions:${RESET}\n`);
        for (const page of pagesWithoutDefs.sort()) {
            console.log(`  ${RED}• ${page}${RESET} (content/knowledge/glossary/${page}.md exists)`);
        }
        errorCount += pagesWithoutDefs.length;
        console.log();
    }
    
    // ═══════════════════════════════════════════════════════════════
    // CHECK 4: Orphaned definitions (defined but never used)
    // ═══════════════════════════════════════════════════════════════
    console.log(`${BOLD}CHECK 4: Orphaned definitions (defined but never used)${RESET}`);
    console.log('─'.repeat(60));
    
    const orphanedTerms = [];
    for (const term of definedTerms) {
        if (!usedTerms.has(term)) {
            orphanedTerms.push(term);
        }
    }
    
    if (orphanedTerms.length === 0) {
        console.log(`${GREEN}✓ All defined terms are used somewhere${RESET}\n`);
    } else {
        console.log(`${YELLOW}⚠ ${orphanedTerms.length} terms are defined but never used:${RESET}\n`);
        for (const term of orphanedTerms.sort()) {
            console.log(`  ${YELLOW}• ${term}${RESET}`);
        }
        warningCount += orphanedTerms.length;
        console.log();
    }
    
    // ═══════════════════════════════════════════════════════════════
    // SUMMARY
    // ═══════════════════════════════════════════════════════════════
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   SUMMARY${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);
    
    if (errorCount === 0 && warningCount === 0) {
        console.log(`${GREEN}${BOLD}✓ All checks passed!${RESET}\n`);
        return 0;
    }
    
    if (errorCount > 0) {
        console.log(`${RED}${BOLD}✗ ${errorCount} error(s)${RESET} - these MUST be fixed`);
    }
    if (warningCount > 0) {
        console.log(`${YELLOW}${BOLD}⚠ ${warningCount} warning(s)${RESET} - optional improvements`);
    }
    
    // Print actionable list of missing definitions
    if (undefinedTerms.length > 0) {
        console.log(`\n${BOLD}Add these to static/assets/content/glossary.json:${RESET}`);
        console.log('```json');
        for (const { term } of undefinedTerms.sort((a, b) => a.term.localeCompare(b.term))) {
            console.log(`  "${term}": {`);
            console.log(`    "term": "${term.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}",`);
            console.log(`    "shortDefinition": "TODO: Add definition",`);
            console.log(`    "longDefinition": "TODO: Add detailed definition",`);
            console.log(`    "category": "TODO",`);
            console.log(`    "relatedTerms": []`);
            console.log(`  },`);
        }
        console.log('```');
    }
    
    console.log();
    return errorCount > 0 ? 1 : 0;
}

// Run validation
const exitCode = validate();
process.exit(exitCode);
