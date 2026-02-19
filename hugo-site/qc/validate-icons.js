#!/usr/bin/env node

/**
 * Icon Sprite Validation Script
 * 
 * Validates SVG icon completeness:
 * 1. All <use href="#icon-*"> in content/layouts reference symbols
 *    that exist in the icon-sprite.html partial
 * 2. All <symbol> definitions in icon-sprite.html are used somewhere
 * 3. Roadmap data icon names have matching symbol definitions
 * 
 * Usage: node qc/validate-icons.js
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Configuration
const HUGO_ROOT = path.join(__dirname, '..');
const CONTENT_DIR = path.join(HUGO_ROOT, 'content');
const LAYOUTS_DIR = path.join(HUGO_ROOT, 'layouts');
const STATIC_DIR = path.join(HUGO_ROOT, 'static');
const ICON_SPRITE = path.join(LAYOUTS_DIR, 'partials', 'icon-sprite.html');
const ROADMAP_YAML = path.join(HUGO_ROOT, 'data', 'roadmap.yaml');

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
 * Extract all symbol IDs from the icon sprite partial
 */
function getDefinedIcons() {
    const icons = new Set();
    if (!fs.existsSync(ICON_SPRITE)) return icons;

    const content = fs.readFileSync(ICON_SPRITE, 'utf8');
    const regex = /id="(icon-[^"]+)"/g;
    let match;
    while ((match = regex.exec(content)) !== null) {
        icons.add(match[1]);
    }
    return icons;
}

/**
 * Extract all <use href="#icon-*"> references from source files
 */
function getUsedIcons(files) {
    const usages = new Map(); // icon-name -> [{file, line}]
    const regex = /href="#(icon-[^"]+)"/g;
    // Skip Hugo template expressions and placeholder names
    const skipPattern = /\{\{|icon-NAME/;

    for (const file of files) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n');
        const relFile = path.relative(HUGO_ROOT, file);

        for (let i = 0; i < lines.length; i++) {
            let match;
            regex.lastIndex = 0;
            while ((match = regex.exec(lines[i])) !== null) {
                const icon = match[1];
                // Skip Hugo template variables and placeholder names
                if (skipPattern.test(icon)) continue;
                if (!usages.has(icon)) usages.set(icon, []);
                usages.get(icon).push({ file: relFile, line: i + 1 });
            }
        }
    }
    return usages;
}

/**
 * Get icon names from roadmap data (these get turned into icon-{name} refs)
 */
function getRoadmapIcons() {
    if (!fs.existsSync(ROADMAP_YAML)) return new Set();
    try {
        const roadmap = yaml.load(fs.readFileSync(ROADMAP_YAML, 'utf8'));
        const icons = new Set();
        if (Array.isArray(roadmap.phases)) {
            for (const phase of roadmap.phases) {
                if (Array.isArray(phase.milestones)) {
                    for (const ms of phase.milestones) {
                        if (ms.icon) icons.add(`icon-${ms.icon}`);
                    }
                }
            }
        }
        return icons;
    } catch (e) {
        return new Set();
    }
}

/**
 * Main validation function
 */
function validateIcons() {
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   ICON SPRITE VALIDATION REPORT${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    let totalErrors = 0;
    let totalWarnings = 0;

    // Check sprite file exists
    if (!fs.existsSync(ICON_SPRITE)) {
        console.log(`${RED}✗ Icon sprite partial not found: layouts/partials/icon-sprite.html${RESET}\n`);
        return { success: false, errors: 1, warnings: 0 };
    }

    // Get defined icons
    const definedIcons = getDefinedIcons();
    console.log(`Found ${CYAN}${definedIcons.size}${RESET} icon symbols in icon-sprite.html`);

    // Get used icons from source files
    const sourceFiles = [
        ...findFiles(CONTENT_DIR, ['.md', '.html']),
        ...findFiles(LAYOUTS_DIR, ['.html'])
    ];
    const usedIcons = getUsedIcons(sourceFiles);
    console.log(`Found ${CYAN}${usedIcons.size}${RESET} unique icon references in source files`);

    // Get roadmap data icons
    const roadmapIcons = getRoadmapIcons();
    if (roadmapIcons.size > 0) {
        console.log(`Found ${CYAN}${roadmapIcons.size}${RESET} icon references in roadmap.yaml`);
    }

    // Merge all used icons (source + roadmap)
    const allUsed = new Map(usedIcons);
    for (const icon of roadmapIcons) {
        if (!allUsed.has(icon)) {
            allUsed.set(icon, [{ file: 'data/roadmap.yaml', line: 0 }]);
        }
    }

    console.log();

    // ─── CHECK 1: Used but not defined ────────────────────────────────
    console.log(`${BOLD}CHECK 1: Icons Used but NOT Defined in Sprite${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const undefinedIcons = [];
    for (const [icon, locations] of allUsed) {
        if (!definedIcons.has(icon)) {
            undefinedIcons.push({ icon, locations });
        }
    }

    if (undefinedIcons.length === 0) {
        console.log(`${GREEN}✓ All used icons have sprite definitions${RESET}\n`);
    } else {
        totalErrors += undefinedIcons.length;
        console.log(`${RED}✗ ${undefinedIcons.length} icon(s) used without definitions:${RESET}\n`);
        for (const { icon, locations } of undefinedIcons) {
            console.log(`  ${RED}•${RESET} ${BOLD}${icon}${RESET}`);
            for (const loc of locations.slice(0, 2)) {
                console.log(`    ${DIM}${loc.file}${loc.line ? ':' + loc.line : ''}${RESET}`);
            }
            if (locations.length > 2) console.log(`    ${DIM}... and ${locations.length - 2} more${RESET}`);
        }
        console.log();
    }

    // ─── CHECK 2: Defined but never used ──────────────────────────────
    console.log(`${BOLD}CHECK 2: Icons Defined but Never Used${RESET}`);
    console.log('────────────────────────────────────────────────────────────');

    const unusedIcons = [];
    for (const icon of definedIcons) {
        if (!allUsed.has(icon)) {
            unusedIcons.push(icon);
        }
    }

    if (unusedIcons.length === 0) {
        console.log(`${GREEN}✓ All defined icons are used${RESET}\n`);
    } else {
        totalWarnings += unusedIcons.length;
        console.log(`${YELLOW}⚠ ${unusedIcons.length} icon(s) defined but not currently used:${RESET}\n`);
        for (const icon of unusedIcons) {
            console.log(`  ${YELLOW}•${RESET} ${icon}`);
        }
        console.log(`  ${DIM}(These may be used in future content or via dynamic references)${RESET}\n`);
    }

    // ─── CHECK 3: Roadmap icons specifically ──────────────────────────
    if (roadmapIcons.size > 0) {
        console.log(`${BOLD}CHECK 3: Roadmap Data Icons${RESET}`);
        console.log('────────────────────────────────────────────────────────────');

        const missingRoadmap = [];
        for (const icon of roadmapIcons) {
            if (!definedIcons.has(icon)) {
                missingRoadmap.push(icon);
            }
        }

        if (missingRoadmap.length === 0) {
            console.log(`${GREEN}✓ All ${roadmapIcons.size} roadmap icons have definitions${RESET}\n`);
        } else {
            // Already counted in CHECK 1, just highlight
            console.log(`${RED}✗ ${missingRoadmap.length} roadmap icon(s) missing from sprite:${RESET}\n`);
            for (const icon of missingRoadmap) {
                console.log(`  ${RED}•${RESET} ${icon}`);
            }
            console.log();
        }
    }

    // ─── Summary ──────────────────────────────────────────────────────
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}`);
    console.log(`${BOLD}   SUMMARY${RESET}`);
    console.log(`${BOLD}═══════════════════════════════════════════════════════════════${RESET}\n`);

    if (totalErrors === 0 && totalWarnings === 0) {
        console.log(`${GREEN}✓ All icon checks passed!${RESET}\n`);
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
    const result = validateIcons();
    process.exit(result.success ? 0 : 1);
}

module.exports = { validateIcons };
