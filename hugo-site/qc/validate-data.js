#!/usr/bin/env node

/**
 * Data File Validation Script
 * 
 * Validates YAML data files that drive the site's data-driven architecture:
 * 1. data/categories.yaml — structure, i18n completeness, required sections
 * 2. data/roadmap.yaml — phases, milestones, cross-references to categories
 * 
 * Usage: node qc/validate-data.js
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Configuration
const HUGO_ROOT = path.join(__dirname, '..');
const DATA_DIR = path.join(HUGO_ROOT, 'data');

// ANSI colors
const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';

const LANGS = ['en', 'fr'];

/**
 * Check that an object has both en/fr keys
 */
function checkI18n(obj, label, errors, warnings) {
    if (!obj || typeof obj !== 'object') {
        errors.push(`${label}: missing or not an object`);
        return false;
    }
    let ok = true;
    for (const lang of LANGS) {
        if (!obj[lang]) {
            errors.push(`${label}: missing "${lang}" translation`);
            ok = false;
        }
    }
    return ok;
}

/**
 * Validate categories.yaml
 */
function validateCategories(cats) {
    const errors = [];
    const warnings = [];

    // Required top-level sections
    const requiredSections = [
        'content_types',
        'glossary_categories',
        'content_categories',
        'roadmap_statuses',
        'tags',
        'faq_categories'
    ];

    for (const section of requiredSections) {
        if (!cats[section]) {
            errors.push(`Missing required section: ${section}`);
            continue;
        }
        if (typeof cats[section] !== 'object') {
            errors.push(`Section "${section}" must be a map`);
            continue;
        }

        // Check each entry in the section has i18n
        for (const [key, entry] of Object.entries(cats[section])) {
            checkI18n(entry, `${section}.${key}`, errors, warnings);
        }
    }

    // Roadmap statuses need extra fields
    if (cats.roadmap_statuses) {
        for (const [key, status] of Object.entries(cats.roadmap_statuses)) {
            if (!status.icon) warnings.push(`roadmap_statuses.${key}: missing "icon"`);
            if (!status.css_class) errors.push(`roadmap_statuses.${key}: missing "css_class"`);
        }
    }

    // Glossary categories need color
    if (cats.glossary_categories) {
        for (const [key, cat] of Object.entries(cats.glossary_categories)) {
            if (!cat.color) warnings.push(`glossary_categories.${key}: missing "color"`);
        }
    }

    // Content categories need color
    if (cats.content_categories) {
        for (const [key, cat] of Object.entries(cats.content_categories)) {
            if (!cat.color) warnings.push(`content_categories.${key}: missing "color"`);
        }
    }

    return { errors, warnings };
}

/**
 * Validate roadmap.yaml against categories.yaml
 */
function validateRoadmap(roadmap, cats) {
    const errors = [];
    const warnings = [];

    // Top-level required fields
    if (!roadmap.current_status) errors.push('Missing "current_status"');
    if (!roadmap.hero) errors.push('Missing "hero"');
    if (!roadmap.phases) errors.push('Missing "phases"');
    if (!roadmap.vision) errors.push('Missing "vision"');
    if (!roadmap.cta) warnings.push('Missing "cta" section');

    // Hero i18n
    if (roadmap.hero) {
        if (roadmap.hero.title) checkI18n(roadmap.hero.title, 'hero.title', errors, warnings);
        if (roadmap.hero.description) checkI18n(roadmap.hero.description, 'hero.description', errors, warnings);
    }

    // Vision i18n
    if (roadmap.vision) {
        if (roadmap.vision.title) checkI18n(roadmap.vision.title, 'vision.title', errors, warnings);
        if (roadmap.vision.paragraphs && Array.isArray(roadmap.vision.paragraphs)) {
            roadmap.vision.paragraphs.forEach((p, i) => {
                checkI18n(p, `vision.paragraphs[${i}]`, errors, warnings);
            });
        }
    }

    // Valid statuses from categories
    const validStatuses = cats.roadmap_statuses ? new Set(Object.keys(cats.roadmap_statuses)) : new Set();

    // Phases
    if (Array.isArray(roadmap.phases)) {
        const phaseIds = new Set();
        const milestoneIds = new Set();

        for (const phase of roadmap.phases) {
            // Required phase fields
            if (!phase.id) { errors.push('Phase missing "id"'); continue; }
            if (phaseIds.has(phase.id)) errors.push(`Duplicate phase id: "${phase.id}"`);
            phaseIds.add(phase.id);

            if (!phase.number) errors.push(`Phase "${phase.id}": missing "number"`);
            if (phase.title) checkI18n(phase.title, `phase.${phase.id}.title`, errors, warnings);
            if (phase.date) checkI18n(phase.date, `phase.${phase.id}.date`, errors, warnings);

            // Phase status must reference valid status
            if (phase.status && validStatuses.size > 0 && !validStatuses.has(phase.status)) {
                errors.push(`Phase "${phase.id}": status "${phase.status}" not in roadmap_statuses (valid: ${[...validStatuses].join(', ')})`);
            }

            // Milestones
            if (!Array.isArray(phase.milestones) || phase.milestones.length === 0) {
                warnings.push(`Phase "${phase.id}": no milestones defined`);
                continue;
            }

            for (const ms of phase.milestones) {
                if (!ms.id) { errors.push(`Phase "${phase.id}": milestone missing "id"`); continue; }
                if (milestoneIds.has(ms.id)) errors.push(`Duplicate milestone id: "${ms.id}"`);
                milestoneIds.add(ms.id);

                if (ms.title) checkI18n(ms.title, `milestone.${ms.id}.title`, errors, warnings);
                if (ms.description) checkI18n(ms.description, `milestone.${ms.id}.description`, errors, warnings);

                if (ms.status && validStatuses.size > 0 && !validStatuses.has(ms.status)) {
                    errors.push(`Milestone "${ms.id}": status "${ms.status}" not in roadmap_statuses`);
                }

                if (!ms.icon) warnings.push(`Milestone "${ms.id}": missing "icon"`);
                if (!ms.category) warnings.push(`Milestone "${ms.id}": missing "category"`);
                if (!ms.tags || !Array.isArray(ms.tags) || ms.tags.length === 0) {
                    warnings.push(`Milestone "${ms.id}": no tags defined`);
                }
            }
        }
    }

    // CTA buttons
    if (roadmap.cta && roadmap.cta.buttons) {
        for (const btn of roadmap.cta.buttons) {
            if (!btn.href && !btn.url) errors.push('CTA button missing "href" or "url"');
            if (btn.label) checkI18n(btn.label, 'cta.button.label', errors, warnings);
        }
    }

    return { errors, warnings };
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

    // ─── categories.yaml ──────────────────────────────────────────────
    console.log(`${BOLD}CHECK 1: data/categories.yaml${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const catPath = path.join(DATA_DIR, 'categories.yaml');
    if (!fs.existsSync(catPath)) {
        console.log(`${RED}✗ File not found: data/categories.yaml${RESET}\n`);
        totalErrors++;
    } else {
        let cats;
        try {
            cats = yaml.load(fs.readFileSync(catPath, 'utf8'));
        } catch (e) {
            console.log(`${RED}✗ YAML parse error: ${e.message}${RESET}\n`);
            totalErrors++;
            cats = null;
        }

        if (cats) {
            const sections = Object.keys(cats);
            console.log(`  Sections: ${CYAN}${sections.join(', ')}${RESET}`);

            const catResult = validateCategories(cats);
            totalErrors += catResult.errors.length;
            totalWarnings += catResult.warnings.length;

            if (catResult.errors.length === 0 && catResult.warnings.length === 0) {
                console.log(`  ${GREEN}✓ All checks passed${RESET}\n`);
            } else {
                for (const e of catResult.errors) console.log(`  ${RED}✗ ${e}${RESET}`);
                for (const w of catResult.warnings) console.log(`  ${YELLOW}⚠ ${w}${RESET}`);
                console.log();
            }
        }
    }

    // ─── roadmap.yaml ─────────────────────────────────────────────────
    console.log(`${BOLD}CHECK 2: data/roadmap.yaml${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const roadmapPath = path.join(DATA_DIR, 'roadmap.yaml');
    if (!fs.existsSync(roadmapPath)) {
        console.log(`${RED}✗ File not found: data/roadmap.yaml${RESET}\n`);
        totalErrors++;
    } else {
        let roadmap;
        try {
            roadmap = yaml.load(fs.readFileSync(roadmapPath, 'utf8'));
        } catch (e) {
            console.log(`${RED}✗ YAML parse error: ${e.message}${RESET}\n`);
            totalErrors++;
            roadmap = null;
        }

        if (roadmap) {
            const phaseCount = Array.isArray(roadmap.phases) ? roadmap.phases.length : 0;
            const milestoneCount = Array.isArray(roadmap.phases)
                ? roadmap.phases.reduce((sum, p) => sum + (Array.isArray(p.milestones) ? p.milestones.length : 0), 0)
                : 0;
            console.log(`  Phases: ${CYAN}${phaseCount}${RESET}, Milestones: ${CYAN}${milestoneCount}${RESET}`);

            // Load categories for cross-reference validation
            let cats = {};
            try {
                cats = yaml.load(fs.readFileSync(catPath, 'utf8')) || {};
            } catch (e) { /* already reported */ }

            const rmResult = validateRoadmap(roadmap, cats);
            totalErrors += rmResult.errors.length;
            totalWarnings += rmResult.warnings.length;

            if (rmResult.errors.length === 0 && rmResult.warnings.length === 0) {
                console.log(`  ${GREEN}✓ All checks passed${RESET}\n`);
            } else {
                for (const e of rmResult.errors) console.log(`  ${RED}✗ ${e}${RESET}`);
                for (const w of rmResult.warnings) console.log(`  ${YELLOW}⚠ ${w}${RESET}`);
                console.log();
            }
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

// Run if called directly
if (require.main === module) {
    const result = validateData();
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateData };
