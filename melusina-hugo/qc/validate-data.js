#!/usr/bin/env node

/**
 * Data File Validation Script (Melusina OS)
 * 
 * Validates JSON data files that drive the site's data-driven architecture:
 * 1. glossary_categories.json — structure, required fields
 * 2. roadmap_config.json — categories, statuses
 * 3. audiences.json — audience definitions
 * 4. Page data files — completeness, i18n (en/fr pairs)
 * 5. data/glossary/*.json — individual term files
 * 
 * Usage: node qc/validate-data.js
 */

const fs = require('fs');
const path = require('path');

const HUGO_ROOT = path.join(__dirname, '..');
const DATA_DIR = path.join(HUGO_ROOT, 'data');

const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';

/**
 * Safely parse a JSON file
 */
function loadJson(filePath) {
    if (!fs.existsSync(filePath)) return { exists: false };
    try {
        const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        return { exists: true, data };
    } catch (e) {
        return { exists: true, error: e.message };
    }
}

/**
 * Validate glossary_categories.json
 */
function validateGlossaryCategories(data) {
    const errors = [];
    const warnings = [];

    if (typeof data !== 'object' || Array.isArray(data)) {
        errors.push('Must be a JSON object (map of category-id → category)');
        return { errors, warnings };
    }

    const entries = Object.entries(data);
    for (const [key, cat] of entries) {
        if (!cat.label) errors.push(`${key}: missing "label"`);
        if (!cat.color) warnings.push(`${key}: missing "color"`);
        if (!cat.icon) warnings.push(`${key}: missing "icon"`);
        // Check for French label
        if (!cat.labelFr) warnings.push(`${key}: missing "labelFr" (i18n)`);
    }

    return { errors, warnings };
}

/**
 * Validate roadmap_config.json
 */
function validateRoadmapConfig(data) {
    const errors = [];
    const warnings = [];

    if (!data.categories || typeof data.categories !== 'object') {
        errors.push('Missing "categories" section');
    } else {
        for (const [key, cat] of Object.entries(data.categories)) {
            if (!cat.label) errors.push(`categories.${key}: missing "label"`);
            if (!cat.color) warnings.push(`categories.${key}: missing "color"`);
        }
    }

    if (!data.statuses && !data.phases) {
        warnings.push('No "statuses" or "phases" section found');
    }

    return { errors, warnings };
}

/**
 * Validate audiences.json
 */
function validateAudiences(data) {
    const errors = [];
    const warnings = [];

    if (!Array.isArray(data) && typeof data !== 'object') {
        errors.push('Must be a JSON array or object');
        return { errors, warnings };
    }

    const entries = Array.isArray(data) ? data : Object.values(data);
    for (let i = 0; i < entries.length; i++) {
        const audience = entries[i];
        const label = audience.id || audience.key || `[${i}]`;
        if (!audience.title && !audience.label && !audience.name) {
            warnings.push(`${label}: missing title/label/name`);
        }
    }

    return { errors, warnings };
}

/**
 * Check page data file pairs (en/fr)
 */
function checkPageDataPairs() {
    const pagesDir = path.join(DATA_DIR, 'pages');
    const errors = [];
    const warnings = [];

    if (!fs.existsSync(pagesDir)) {
        // Check root-level page data files
        const dataFiles = fs.readdirSync(DATA_DIR)
            .filter(f => f.endsWith('.json') && !f.startsWith('.'));

        // Find en/fr pairs
        const baseNames = new Set();
        const frFiles = new Set();

        for (const file of dataFiles) {
            const name = file.replace('.json', '');
            if (name.endsWith('_fr')) {
                frFiles.add(name.replace('_fr', ''));
            } else {
                baseNames.add(name);
            }
        }

        // Check for pages with EN but no FR
        const pageDataFiles = ['landing', 'architecture', 'compare', 'contact', 'plans', 'use-cases'];
        for (const page of pageDataFiles) {
            if (baseNames.has(page) && !frFiles.has(page)) {
                warnings.push(`${page}.json has no French translation (${page}_fr.json)`);
            }
        }

        return { errors, warnings, count: dataFiles.length };
    }

    const files = fs.readdirSync(pagesDir).filter(f => f.endsWith('.json'));
    return { errors, warnings, count: files.length };
}

/**
 * Main validation function
 */
function validateData() {
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   DATA FILE VALIDATION REPORT${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    let totalErrors = 0;
    let totalWarnings = 0;

    // ─── CHECK 1: glossary_categories.json ────────────────────────────
    console.log(`${BOLD}CHECK 1: data/glossary_categories.json${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const catResult = loadJson(path.join(DATA_DIR, 'glossary_categories.json'));
    if (!catResult.exists) {
        console.log(`${RED}✗ File not found${RESET}\n`);
        totalErrors++;
    } else if (catResult.error) {
        console.log(`${RED}✗ JSON parse error: ${catResult.error}${RESET}\n`);
        totalErrors++;
    } else {
        const entries = Object.keys(catResult.data);
        console.log(`  Categories: ${CYAN}${entries.join(', ')}${RESET}`);
        const v = validateGlossaryCategories(catResult.data);
        totalErrors += v.errors.length;
        totalWarnings += v.warnings.length;
        if (v.errors.length === 0 && v.warnings.length === 0) {
            console.log(`  ${GREEN}✓ All checks passed${RESET}\n`);
        } else {
            for (const e of v.errors) console.log(`  ${RED}✗ ${e}${RESET}`);
            for (const w of v.warnings) console.log(`  ${YELLOW}⚠ ${w}${RESET}`);
            console.log();
        }
    }

    // ─── CHECK 2: roadmap_config.json ─────────────────────────────────
    console.log(`${BOLD}CHECK 2: data/roadmap_config.json${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const rmResult = loadJson(path.join(DATA_DIR, 'roadmap_config.json'));
    if (!rmResult.exists) {
        console.log(`${YELLOW}⚠ File not found (optional)${RESET}\n`);
        totalWarnings++;
    } else if (rmResult.error) {
        console.log(`${RED}✗ JSON parse error: ${rmResult.error}${RESET}\n`);
        totalErrors++;
    } else {
        const v = validateRoadmapConfig(rmResult.data);
        totalErrors += v.errors.length;
        totalWarnings += v.warnings.length;
        if (v.errors.length === 0 && v.warnings.length === 0) {
            console.log(`  ${GREEN}✓ All checks passed${RESET}\n`);
        } else {
            for (const e of v.errors) console.log(`  ${RED}✗ ${e}${RESET}`);
            for (const w of v.warnings) console.log(`  ${YELLOW}⚠ ${w}${RESET}`);
            console.log();
        }
    }

    // ─── CHECK 3: audiences.json ──────────────────────────────────────
    console.log(`${BOLD}CHECK 3: data/audiences.json${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const audResult = loadJson(path.join(DATA_DIR, 'audiences.json'));
    if (!audResult.exists) {
        console.log(`${YELLOW}⚠ File not found (optional)${RESET}\n`);
        totalWarnings++;
    } else if (audResult.error) {
        console.log(`${RED}✗ JSON parse error: ${audResult.error}${RESET}\n`);
        totalErrors++;
    } else {
        const v = validateAudiences(audResult.data);
        totalErrors += v.errors.length;
        totalWarnings += v.warnings.length;
        if (v.errors.length === 0 && v.warnings.length === 0) {
            console.log(`  ${GREEN}✓ All checks passed${RESET}\n`);
        } else {
            for (const e of v.errors) console.log(`  ${RED}✗ ${e}${RESET}`);
            for (const w of v.warnings) console.log(`  ${YELLOW}⚠ ${w}${RESET}`);
            console.log();
        }
    }

    // ─── CHECK 4: Page data i18n pairs ────────────────────────────────
    console.log(`${BOLD}CHECK 4: Page Data Files (i18n Pairs)${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const pageResult = checkPageDataPairs();
    totalErrors += pageResult.errors.length;
    totalWarnings += pageResult.warnings.length;
    console.log(`  Found ${CYAN}${pageResult.count}${RESET} data files in data/pages/`);

    if (pageResult.errors.length === 0 && pageResult.warnings.length === 0) {
        console.log(`  ${GREEN}✓ All checks passed${RESET}\n`);
    } else {
        for (const e of pageResult.errors) console.log(`  ${RED}✗ ${e}${RESET}`);
        for (const w of pageResult.warnings) console.log(`  ${YELLOW}⚠ ${w}${RESET}`);
        console.log();
    }

    // ─── CHECK 5: Glossary data directory ─────────────────────────────
    console.log(`${BOLD}CHECK 5: data/glossary/ JSON Files${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const glossaryDir = path.join(DATA_DIR, 'glossary');
    if (!fs.existsSync(glossaryDir)) {
        console.log(`${RED}✗ Directory not found${RESET}\n`);
        totalErrors++;
    } else {
        const files = fs.readdirSync(glossaryDir).filter(f => f.endsWith('.json'));
        let parseOk = 0;
        let parseFail = 0;

        for (const file of files) {
            const result = loadJson(path.join(glossaryDir, file));
            if (result.error) {
                parseFail++;
                console.log(`  ${RED}✗ ${file}: ${result.error}${RESET}`);
            } else {
                parseOk++;
            }
        }

        totalErrors += parseFail;
        if (parseFail === 0) {
            console.log(`  ${GREEN}✓ All ${parseOk} glossary JSON files parse successfully${RESET}\n`);
        } else {
            console.log(`  ${RED}${parseFail} file(s) failed to parse${RESET}\n`);
        }
    }

    // ─── CHECK 6: version.json ────────────────────────────────────────
    console.log(`${BOLD}CHECK 6: data/version.json${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const verResult = loadJson(path.join(DATA_DIR, 'version.json'));
    if (!verResult.exists) {
        console.log(`${YELLOW}⚠ File not found (optional)${RESET}\n`);
        totalWarnings++;
    } else if (verResult.error) {
        console.log(`${RED}✗ JSON parse error: ${verResult.error}${RESET}\n`);
        totalErrors++;
    } else {
        if (!verResult.data.version) {
            totalWarnings++;
            console.log(`  ${YELLOW}⚠ Missing "version" field${RESET}\n`);
        } else {
            console.log(`  ${GREEN}✓ Version: ${verResult.data.version}${RESET}\n`);
        }
    }

    // ─── Summary ──────────────────────────────────────────────────────
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   SUMMARY${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    if (totalErrors === 0 && totalWarnings === 0) {
        console.log(`${GREEN}✓ All data file checks passed!${RESET}\n`);
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
    const result = validateData();
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateData };
