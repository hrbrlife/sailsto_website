#!/usr/bin/env node

/**
 * Shortcode & Template Validation Script
 * 
 * Validates the Hugo template architecture:
 * 1. All shortcodes called in content ({{< name >}}) exist in layouts/shortcodes/
 * 2. All partials called in layouts ({{ partial "name" }}) exist in layouts/partials/
 * 3. Data files referenced by shortcodes/partials exist
 * 4. Hugo build completes without errors
 * 
 * Usage: node qc/validate-shortcodes.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const HUGO_ROOT = path.join(__dirname, '..');
const CONTENT_DIR = path.join(HUGO_ROOT, 'content');
const LAYOUTS_DIR = path.join(HUGO_ROOT, 'layouts');
const SHORTCODES_DIR = path.join(LAYOUTS_DIR, 'shortcodes');
const PARTIALS_DIR = path.join(LAYOUTS_DIR, 'partials');
const DATA_DIR = path.join(HUGO_ROOT, 'data');

// ANSI colors
const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';

/**
 * Recursively find all files with given extensions
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
 * Get available shortcodes
 */
function getAvailableShortcodes() {
    const shortcodes = new Set();
    if (!fs.existsSync(SHORTCODES_DIR)) return shortcodes;
    const files = fs.readdirSync(SHORTCODES_DIR);
    for (const file of files) {
        if (file.endsWith('.html')) {
            shortcodes.add(file.replace('.html', ''));
        }
    }
    return shortcodes;
}

/**
 * Get available partials
 */
function getAvailablePartials() {
    const partials = new Set();
    if (!fs.existsSync(PARTIALS_DIR)) return partials;
    const files = fs.readdirSync(PARTIALS_DIR);
    for (const file of files) {
        if (file.endsWith('.html')) {
            partials.add(file);
        }
    }
    return partials;
}

/**
 * Extract shortcode calls from content files
 */
function extractShortcodeCalls(files) {
    const calls = new Map(); // name -> [{file, line}]
    // Match both {{< name >}} and {{< name args >}} and {{< name >}}...{{< /name >}}
    const regex = /\{\{[<%]\s*\/?\s*([a-zA-Z0-9_-]+)/g;

    for (const file of files) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        const relFile = path.relative(HUGO_ROOT, file);

        for (let i = 0; i < lines.length; i++) {
            let match;
            regex.lastIndex = 0;
            while ((match = regex.exec(lines[i])) !== null) {
                const name = match[1];
                // Skip closing tags ({{< /name >}})
                if (lines[i].substring(match.index).match(/\{\{[<%]\s*\//)) continue;
                if (!calls.has(name)) calls.set(name, []);
                calls.get(name).push({ file: relFile, line: i + 1 });
            }
        }
    }
    return calls;
}

/**
 * Extract partial calls from layout files
 */
function extractPartialCalls(files) {
    const calls = new Map(); // filename -> [{file, line}]
    // Match {{ partial "name.html" . }} and {{ partial "name" . }}
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
                // Ensure .html extension
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
    const refs = new Map(); // data key -> [{file, line}]
    // Match .Site.Data.something or $.Site.Data.something
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
 * Get available data files
 */
function getAvailableDataKeys() {
    const keys = new Set();
    if (!fs.existsSync(DATA_DIR)) return keys;
    const files = fs.readdirSync(DATA_DIR);
    for (const file of files) {
        if (file.endsWith('.yaml') || file.endsWith('.yml') || file.endsWith('.json') || file.endsWith('.toml')) {
            keys.add(file.replace(/\.(yaml|yml|json|toml)$/, ''));
        }
    }
    return keys;
}

/**
 * Run Hugo build and check for errors
 */
function checkHugoBuild() {
    try {
        const output = execSync('hugo --gc --minify 2>&1', {
            cwd: HUGO_ROOT,
            encoding: 'utf8',
            timeout: 60000
        });

        // Parse output for page counts
        const pagesMatch = output.match(/Pages\s+\|\s+(\d+)\s+\|\s+(\d+)/);
        const timeMatch = output.match(/Total in (\d+ ms)/);

        return {
            success: true,
            enPages: pagesMatch ? parseInt(pagesMatch[1]) : 0,
            frPages: pagesMatch ? parseInt(pagesMatch[2]) : 0,
            buildTime: timeMatch ? timeMatch[1] : 'unknown',
            output: output
        };
    } catch (e) {
        return {
            success: false,
            error: e.stderr || e.message,
            output: e.stdout || ''
        };
    }
}

/**
 * Main validation function
 */
function validateShortcodes() {
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   SHORTCODE & TEMPLATE VALIDATION REPORT${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    let totalErrors = 0;
    let totalWarnings = 0;

    // Get available templates
    const availableShortcodes = getAvailableShortcodes();
    const availablePartials = getAvailablePartials();
    const availableDataKeys = getAvailableDataKeys();

    console.log(`Available shortcodes: ${CYAN}${[...availableShortcodes].join(', ')}${RESET}`);
    console.log(`Available partials: ${CYAN}${availablePartials.size}${RESET}`);
    console.log(`Available data files: ${CYAN}${[...availableDataKeys].join(', ')}${RESET}\n`);

    // ─── CHECK 1: Shortcode references ────────────────────────────────
    console.log(`${BOLD}CHECK 1: Shortcode Calls in Content${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const contentFiles = findFiles(CONTENT_DIR, ['.md', '.html']);
    const shortcodeCalls = extractShortcodeCalls(contentFiles);

    const missingShortcodes = [];
    for (const [name, locations] of shortcodeCalls) {
        if (!availableShortcodes.has(name)) {
            missingShortcodes.push({ name, locations });
        }
    }

    if (shortcodeCalls.size === 0) {
        console.log(`  ${DIM}No shortcode calls found${RESET}\n`);
    } else if (missingShortcodes.length === 0) {
        console.log(`  ${GREEN}✓ All ${shortcodeCalls.size} shortcode type(s) have templates${RESET}\n`);
    } else {
        totalErrors += missingShortcodes.length;
        console.log(`  ${RED}✗ ${missingShortcodes.length} missing shortcode template(s):${RESET}\n`);
        for (const { name, locations } of missingShortcodes) {
            console.log(`  ${RED}•${RESET} ${BOLD}{{< ${name} >}}${RESET}`);
            for (const loc of locations.slice(0, 2)) {
                console.log(`    ${DIM}${loc.file}:${loc.line}${RESET}`);
            }
        }
        console.log();
    }

    // ─── CHECK 2: Partial references ──────────────────────────────────
    console.log(`${BOLD}CHECK 2: Partial Calls in Layouts${RESET}`);
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

    // ─── CHECK 3: Data file references ────────────────────────────────
    console.log(`${BOLD}CHECK 3: Data File References in Templates${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const allTemplateFiles = [
        ...layoutFiles,
        ...findFiles(SHORTCODES_DIR, ['.html'])
    ];
    const dataRefs = extractDataReferences(allTemplateFiles);

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
            console.log(`  ${RED}•${RESET} ${BOLD}.Site.Data.${key}${RESET} → data/${key}.yaml not found`);
            for (const loc of locations.slice(0, 2)) {
                console.log(`    ${DIM}${loc.file}:${loc.line}${RESET}`);
            }
        }
        console.log();
    }

    // ─── CHECK 4: Hugo build ──────────────────────────────────────────
    console.log(`${BOLD}CHECK 4: Hugo Build Verification${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const build = checkHugoBuild();
    if (build.success) {
        console.log(`  ${GREEN}✓ Build successful${RESET}`);
        console.log(`    EN pages: ${CYAN}${build.enPages}${RESET}, FR pages: ${CYAN}${build.frPages}${RESET}`);
        console.log(`    Build time: ${CYAN}${build.buildTime}${RESET}`);

        // Warn if page count seems low
        if (build.enPages < 100) {
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

// Run if called directly
if (require.main === module) {
    const result = validateShortcodes();
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateShortcodes };
