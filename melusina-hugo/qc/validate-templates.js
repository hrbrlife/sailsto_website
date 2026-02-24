#!/usr/bin/env node

/**
 * Template Validation Script (Melusina OS)
 * 
 * Validates the Hugo template architecture:
 * 1. All partials called in layouts exist in layouts/partials/
 * 2. Data files referenced by templates exist
 * 3. Hugo build completes without errors
 * 
 * Note: Melusina has no shortcodes (empty shortcodes dir),
 * so this focuses on partials, data, and build integrity.
 * 
 * Usage: node qc/validate-templates.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const HUGO_ROOT = path.join(__dirname, '..');
const CONTENT_DIR = path.join(HUGO_ROOT, 'content');
const LAYOUTS_DIR = path.join(HUGO_ROOT, 'layouts');
const PARTIALS_DIR = path.join(LAYOUTS_DIR, 'partials');
const DATA_DIR = path.join(HUGO_ROOT, 'data');

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

/**
 * Get available partials (flat + nested in blocks/)
 */
function getAvailablePartials() {
    const partials = new Set();
    if (!fs.existsSync(PARTIALS_DIR)) return partials;

    function scan(dir, prefix = '') {
        const items = fs.readdirSync(dir, { withFileTypes: true });
        for (const item of items) {
            const fullPath = path.join(dir, item.name);
            if (item.isDirectory()) {
                scan(fullPath, prefix + item.name + '/');
            } else if (item.name.endsWith('.html')) {
                // Add with directory prefix (e.g., "blocks/hero.html")
                partials.add(prefix + item.name);
                // Also add without .html extension
                partials.add(prefix + item.name.replace('.html', ''));
            }
        }
    }

    scan(PARTIALS_DIR);
    return partials;
}

/**
 * Extract partial calls from layout files
 */
function extractPartialCalls(files) {
    const calls = new Map();
    const regex = /\{\{\s*partial\s+"([^"]+)"/g;

    for (const file of files) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        const relFile = path.relative(HUGO_ROOT, file);

        for (let i = 0; i < lines.length; i++) {
            let match;
            regex.lastIndex = 0;
            while ((match = regex.exec(lines[i])) !== null) {
                let name = match[1];
                if (!name.endsWith('.html')) name += '.html';
                if (!calls.has(name)) calls.set(name, []);
                calls.get(name).push({ file: relFile, line: i + 1 });
            }
        }
    }
    return calls;
}

/**
 * Extract data file references from templates
 */
function extractDataReferences(files) {
    const refs = new Map();
    const regex = /\.Site\.Data\.([a-zA-Z0-9_]+)/g;

    for (const file of files) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        const relFile = path.relative(HUGO_ROOT, file);

        for (let i = 0; i < lines.length; i++) {
            let match;
            regex.lastIndex = 0;
            while ((match = regex.exec(lines[i])) !== null) {
                const key = match[1];
                if (!refs.has(key)) refs.set(key, []);
                refs.get(key).push({ file: relFile, line: i + 1 });
            }
        }
    }
    return refs;
}

/**
 * Get available data keys (file names without extension + subdirectories)
 */
function getAvailableDataKeys() {
    const keys = new Set();
    if (!fs.existsSync(DATA_DIR)) return keys;
    const items = fs.readdirSync(DATA_DIR, { withFileTypes: true });
    for (const item of items) {
        if (item.isDirectory()) {
            keys.add(item.name); // e.g., "glossary", "pages", "authors"
        } else {
            const name = item.name.replace(/\.(json|yaml|yml|toml)$/, '');
            keys.add(name);
        }
    }
    return keys;
}

/**
 * Run Hugo build
 */
function checkHugoBuild() {
    try {
        const output = execSync('hugo --gc --minify 2>&1', {
            cwd: HUGO_ROOT,
            encoding: 'utf8',
            timeout: 60000
        });

        const pagesMatch = output.match(/Pages\s+\|\s+(\d+)\s+\|\s+(\d+)/);
        const timeMatch = output.match(/Total in (\d+ ms)/);

        return {
            success: true,
            enPages: pagesMatch ? parseInt(pagesMatch[1]) : 0,
            frPages: pagesMatch ? parseInt(pagesMatch[2]) : 0,
            buildTime: timeMatch ? timeMatch[1] : 'unknown',
            output
        };
    } catch (e) {
        return {
            success: false,
            error: e.stderr || e.message,
            output: e.stdout || ''
        };
    }
}

function validateTemplates() {
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   TEMPLATE VALIDATION REPORT${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    let totalErrors = 0;
    let totalWarnings = 0;

    const availablePartials = getAvailablePartials();
    const availableDataKeys = getAvailableDataKeys();

    console.log(`Available partials: ${CYAN}${availablePartials.size}${RESET}`);
    console.log(`Available data keys: ${CYAN}${[...availableDataKeys].join(', ')}${RESET}\n`);

    // ─── CHECK 1: Partial references ──────────────────────────────────
    console.log(`${BOLD}CHECK 1: Partial Calls in Layouts${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const layoutFiles = findFiles(LAYOUTS_DIR, ['.html']);
    const partialCalls = extractPartialCalls(layoutFiles);

    const missingPartials = [];
    for (const [name, locations] of partialCalls) {
        if (!availablePartials.has(name)) {
            missingPartials.push({ name, locations });
        }
    }

    if (missingPartials.length === 0) {
        console.log(`  ${GREEN}✓ All ${partialCalls.size} partial type(s) have templates${RESET}\n`);
    } else {
        totalErrors += missingPartials.length;
        console.log(`  ${RED}✗ ${missingPartials.length} missing partial template(s):${RESET}\n`);
        for (const { name, locations } of missingPartials) {
            console.log(`  ${RED}•${RESET} ${BOLD}${name}${RESET}`);
            for (const loc of locations.slice(0, 2)) {
                console.log(`    ${DIM}${loc.file}:${loc.line}${RESET}`);
            }
        }
        console.log();
    }

    // ─── CHECK 2: Data file references ────────────────────────────────
    console.log(`${BOLD}CHECK 2: Data File References in Templates${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const dataRefs = extractDataReferences(layoutFiles);

    const missingData = [];
    for (const [key, locations] of dataRefs) {
        if (!availableDataKeys.has(key)) {
            missingData.push({ key, locations });
        }
    }

    if (dataRefs.size === 0) {
        console.log(`  ${DIM}No data file references found${RESET}\n`);
    } else if (missingData.length === 0) {
        console.log(`  ${GREEN}✓ All ${dataRefs.size} data reference(s) resolve to existing files${RESET}\n`);
    } else {
        totalErrors += missingData.length;
        console.log(`  ${RED}✗ ${missingData.length} missing data file(s):${RESET}\n`);
        for (const { key, locations } of missingData) {
            console.log(`  ${RED}•${RESET} ${BOLD}.Site.Data.${key}${RESET}`);
            for (const loc of locations.slice(0, 2)) {
                console.log(`    ${DIM}${loc.file}:${loc.line}${RESET}`);
            }
        }
        console.log();
    }

    // ─── CHECK 3: Hugo build ──────────────────────────────────────────
    console.log(`${BOLD}CHECK 3: Hugo Build Verification${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const build = checkHugoBuild();
    if (build.success) {
        console.log(`  ${GREEN}✓ Build successful${RESET}`);
        console.log(`    EN pages: ${CYAN}${build.enPages}${RESET}, FR pages: ${CYAN}${build.frPages}${RESET}`);
        console.log(`    Build time: ${CYAN}${build.buildTime}${RESET}`);

        if (build.enPages < 40) {
            totalWarnings++;
            console.log(`  ${YELLOW}⚠ EN page count (${build.enPages}) seems low — check for missing content${RESET}`);
        }
    } else {
        totalErrors++;
        console.log(`  ${RED}✗ Build failed:${RESET}`);
        const errorLines = (build.error || '').split('\n').filter(l => l.trim());
        for (const line of errorLines.slice(0, 10)) {
            console.log(`    ${RED}${line}${RESET}`);
        }
    }
    console.log();

    // ─── Summary ──────────────────────────────────────────────────────
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   SUMMARY${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    if (totalErrors === 0 && totalWarnings === 0) {
        console.log(`${GREEN}✓ All template checks passed!${RESET}\n`);
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
    const result = validateTemplates();
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateTemplates };
