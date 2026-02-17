#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════
 *   HRBR.LIFE QC SUITE
 *   Centralized quality control for all portfolio sites
 * ═══════════════════════════════════════════════════════════════
 *
 * Usage:
 *   node qc/run.js --all                Run all checks on all sites
 *   node qc/run.js --site sailsto       Run all checks on one site
 *   node qc/run.js --all links          Run link checks on all sites
 *   node qc/run.js --site kyclat seo    Run SEO check on kyclat only
 *   node qc/run.js --site sailsto glossary links
 *   node qc/run.js list                 List sites and validators
 *   node qc/run.js --help               Show help
 *
 * Exit codes:
 *   0 = All checks passed (warnings OK)
 *   1 = One or more checks failed with errors
 */

const { SITES } = require('./sites');
const { validateLinks } = require('./validate-links');
const { validateImages } = require('./validate-images');
const { validateGlossary } = require('./validate-glossary');
const { validateSeo: validateSEO } = require('./validate-seo');
const { validateContent } = require('./validate-content');

const { c } = require('./utils');

// ─── Validator Registry ─────────────────────────────────────

const VALIDATORS = {
    links: {
        name: 'Link Validation',
        desc: 'Internal links and static resources',
        fn: validateLinks,
    },
    images: {
        name: 'Image Validation',
        desc: 'Image references, alt text, unused files',
        fn: validateImages,
    },
    glossary: {
        name: 'Glossary Validation',
        desc: 'Term definitions ↔ pages ↔ usage',
        fn: validateGlossary,
        filter: site => !!site.glossary,
    },
    seo: {
        name: 'SEO & Meta Validation',
        desc: 'Titles, descriptions, OG tags, canonical URLs',
        fn: validateSEO,
    },
    content: {
        name: 'Content Validation',
        desc: 'Vandalism, placeholder text, broken patterns',
        fn: validateContent,
    },
};

// ─── CLI ────────────────────────────────────────────────────

function showHelp() {
    console.log(`
${c.BOLD}HRBR.LIFE QC SUITE${c.RESET}
Centralized quality control for all portfolio sites

${c.BOLD}USAGE:${c.RESET}
  node qc/run.js --all [validators...]        Run on all sites
  node qc/run.js --site <name> [validators...]  Run on one site
  node qc/run.js list                          List sites & validators
  node qc/run.js --help                         Show this help

${c.BOLD}VALIDATORS:${c.RESET}`);

    for (const [key, v] of Object.entries(VALIDATORS)) {
        console.log(`  ${c.CYAN}${key.padEnd(12)}${c.RESET} ${v.desc}`);
    }

    console.log(`
${c.BOLD}EXAMPLES:${c.RESET}
  node qc/run.js --all                # All validators, all sites
  node qc/run.js --site sailsto       # All validators, one site
  node qc/run.js --all links seo      # Links + SEO on all sites
  node qc/run.js --site kyclat content # Content validator on kyclat

${c.BOLD}OPTIONS:${c.RESET}
  ${c.CYAN}--strict${c.RESET}   Treat warnings as errors
`);
}

function showList() {
    console.log(`\n${c.BOLD}Sites:${c.RESET}`);
    for (const [key, site] of Object.entries(SITES)) {
        console.log(`  ${c.CYAN}${key.padEnd(14)}${c.RESET} ${site.name.padEnd(18)} ${c.DIM}${site.type} · ${site.domain}${c.RESET}`);
    }
    console.log(`\n${c.BOLD}Validators:${c.RESET}`);
    for (const [key, v] of Object.entries(VALIDATORS)) {
        console.log(`  ${c.CYAN}${key.padEnd(14)}${c.RESET} ${v.desc}`);
    }
    console.log();
}

function printBanner() {
    console.log(`
${c.MAGENTA}╔═══════════════════════════════════════════════════════════════╗${c.RESET}
${c.MAGENTA}║${c.RESET}                                                               ${c.MAGENTA}║${c.RESET}
${c.MAGENTA}║${c.RESET}   ${c.BOLD}⚓ HRBR.LIFE QC SUITE${c.RESET}                                     ${c.MAGENTA}║${c.RESET}
${c.MAGENTA}║${c.RESET}   ${c.DIM}Centralized quality control — all portfolio sites${c.RESET}          ${c.MAGENTA}║${c.RESET}
${c.MAGENTA}║${c.RESET}                                                               ${c.MAGENTA}║${c.RESET}
${c.MAGENTA}╚═══════════════════════════════════════════════════════════════╝${c.RESET}
`);
}

// ─── Runner ─────────────────────────────────────────────────

async function runForSite(siteKey, site, validatorKeys) {
    console.log(`\n${c.MAGENTA}━━━ ${c.BOLD}${site.name}${c.RESET}${c.MAGENTA} (${site.domain}) ━━━${c.RESET}`);

    const results = {};
    let siteErrors = 0;
    let siteWarnings = 0;

    for (const key of validatorKeys) {
        const validator = VALIDATORS[key];
        if (!validator) continue;

        // Skip if validator has a filter and site doesn't qualify
        if (validator.filter && !validator.filter(site)) {
            console.log(`  ${c.DIM}⊘ ${validator.name} — not applicable${c.RESET}`);
            results[key] = { success: true, errors: 0, warnings: 0, skipped: true };
            continue;
        }

        console.log(`\n  ${c.BLUE}▸ ${validator.name}${c.RESET}`);

        try {
            const result = await validator.fn(site);
            results[key] = result;
            siteErrors += result.errors || 0;
            siteWarnings += result.warnings || 0;
        } catch (error) {
            console.error(`  ${c.RED}Error: ${error.message}${c.RESET}`);
            results[key] = { success: false, errors: 1, warnings: 0 };
            siteErrors += 1;
        }
    }

    return { results, errors: siteErrors, warnings: siteWarnings };
}

async function main() {
    const args = process.argv.slice(2);

    if (args.includes('--help') || args.includes('-h') || args.includes('help')) {
        showHelp();
        process.exit(0);
    }
    if (args.includes('list')) {
        showList();
        process.exit(0);
    }

    const strict = args.includes('--strict');
    const allSites = args.includes('--all');
    const siteIdx = args.indexOf('--site');
    const siteArg = siteIdx >= 0 ? args[siteIdx + 1] : null;

    if (!allSites && !siteArg) {
        console.error(`${c.RED}Specify --all or --site <name>. Run with --help for usage.${c.RESET}`);
        process.exit(1);
    }

    // Determine which sites to run
    let siteKeys;
    if (allSites) {
        siteKeys = Object.keys(SITES);
    } else {
        if (!SITES[siteArg]) {
            console.error(`${c.RED}Unknown site: ${siteArg}. Run 'list' to see available sites.${c.RESET}`);
            process.exit(1);
        }
        siteKeys = [siteArg];
    }

    // Determine which validators to run
    const flagArgs = new Set(['--all', '--site', '--strict', siteArg]);
    const requestedValidators = args.filter(a => !a.startsWith('--') && !flagArgs.has(a));
    const validatorKeys = requestedValidators.length > 0
        ? requestedValidators
        : Object.keys(VALIDATORS);

    // Validate requested validators
    for (const key of validatorKeys) {
        if (!VALIDATORS[key]) {
            console.error(`${c.RED}Unknown validator: ${key}. Run 'list' to see available validators.${c.RESET}`);
            process.exit(1);
        }
    }

    printBanner();
    console.log(`${c.DIM}Sites: ${siteKeys.join(', ')}${c.RESET}`);
    console.log(`${c.DIM}Validators: ${validatorKeys.join(', ')}${c.RESET}`);

    // Run
    const allResults = {};
    let grandErrors = 0;
    let grandWarnings = 0;

    for (const siteKey of siteKeys) {
        const site = SITES[siteKey];
        const { results, errors, warnings } = await runForSite(siteKey, site, validatorKeys);
        allResults[siteKey] = results;
        grandErrors += errors;
        grandWarnings += warnings;
    }

    // ─── Final Summary ──────────────────────────────────────

    console.log(`\n${c.MAGENTA}╔═══════════════════════════════════════════════════════════════╗${c.RESET}`);
    console.log(`${c.MAGENTA}║${c.RESET}                     ${c.BOLD}FINAL SUMMARY${c.RESET}                            ${c.MAGENTA}║${c.RESET}`);
    console.log(`${c.MAGENTA}╚═══════════════════════════════════════════════════════════════╝${c.RESET}\n`);

    for (const siteKey of siteKeys) {
        const site = SITES[siteKey];
        const siteResults = allResults[siteKey];
        const siteErrors = Object.values(siteResults).reduce((s, r) => s + (r.errors || 0), 0);
        const siteWarns = Object.values(siteResults).reduce((s, r) => s + (r.warnings || 0), 0);

        const icon = siteErrors > 0 ? `${c.RED}✗` : siteWarns > 0 ? `${c.YELLOW}⚠` : `${c.GREEN}✓`;
        const detail = [];
        if (siteErrors > 0) detail.push(`${c.RED}${siteErrors} error(s)${c.RESET}`);
        if (siteWarns > 0) detail.push(`${c.YELLOW}${siteWarns} warning(s)${c.RESET}`);

        console.log(`  ${icon}${c.RESET} ${c.BOLD}${site.name.padEnd(20)}${c.RESET}${detail.length ? detail.join(', ') : `${c.GREEN}all clear${c.RESET}`}`);

        for (const [vKey, vResult] of Object.entries(siteResults)) {
            if (vResult.skipped) continue;
            const vi = vResult.errors > 0 ? `${c.RED}✗` : vResult.warnings > 0 ? `${c.YELLOW}⚠` : `${c.GREEN}✓`;
            const vd = [];
            if (vResult.errors > 0) vd.push(`${c.RED}${vResult.errors}e${c.RESET}`);
            if (vResult.warnings > 0) vd.push(`${c.YELLOW}${vResult.warnings}w${c.RESET}`);
            console.log(`    ${vi}${c.RESET} ${VALIDATORS[vKey].name}${vd.length ? ' — ' + vd.join(', ') : ''}`);
        }
    }

    console.log();
    if (grandErrors === 0 && grandWarnings === 0) {
        console.log(`${c.GREEN}${c.BOLD}  ✓ ALL CHECKS PASSED${c.RESET}\n`);
    } else if (grandErrors === 0) {
        console.log(`${c.YELLOW}${c.BOLD}  ⚠ PASSED WITH ${grandWarnings} WARNING(S)${c.RESET}\n`);
    } else {
        console.log(`${c.RED}${c.BOLD}  ✗ ${grandErrors} ERROR(S), ${grandWarnings} WARNING(S)${c.RESET}\n`);
    }

    process.exit(strict ? (grandErrors + grandWarnings > 0 ? 1 : 0) : (grandErrors > 0 ? 1 : 0));
}

main().catch(err => {
    console.error(`${c.RED}Fatal: ${err.message}${c.RESET}`);
    process.exit(1);
});
