#!/usr/bin/env node

/**
 * ═══════════════════════════════════════════════════════════════
 *   SAILS.TO QC SUITE
 *   Comprehensive quality control for the Hugo site
 * ═══════════════════════════════════════════════════════════════
 * 
 * Runs all validation checks:
 *   • Glossary: term definitions, pages, and usage
 *   • Links: internal page links and static resources
 *   • Images: references, alt text, and unused files
 * 
 * Usage:
 *   node qc/run.js           Run all checks
 *   node qc/run.js glossary  Run only glossary checks
 *   node qc/run.js links     Run only link checks
 *   node qc/run.js images    Run only image checks
 *   node qc/run.js --help    Show help
 * 
 * Exit codes:
 *   0 = All checks passed (warnings OK)
 *   1 = One or more checks failed with errors
 */

const { validateGlossary } = require('./validate-glossary');
const { validateLinks } = require('./validate-links');
const { validateImages } = require('./validate-images');

// ANSI colors
const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const BLUE = '\x1b[34m';
const CYAN = '\x1b[36m';
const MAGENTA = '\x1b[35m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';

const VALIDATORS = {
    glossary: {
        name: 'Glossary Validation',
        description: 'Check term definitions, pages, and usage',
        fn: validateGlossary
    },
    links: {
        name: 'Link Validation',
        description: 'Check internal page links and static resources',
        fn: validateLinks
    },
    images: {
        name: 'Image Validation',
        description: 'Check image references, alt text, and unused files',
        fn: validateImages
    }
};

function showHelp() {
    console.log(`
${BOLD}SAILS.TO QC SUITE${RESET}
Comprehensive quality control for the Hugo site

${BOLD}USAGE:${RESET}
  node qc/run.js [command] [options]

${BOLD}COMMANDS:${RESET}
  ${CYAN}(none)${RESET}      Run all validation checks
  ${CYAN}glossary${RESET}    Run only glossary validation
  ${CYAN}links${RESET}       Run only link validation  
  ${CYAN}images${RESET}      Run only image validation
  ${CYAN}list${RESET}        List all available validators
  ${CYAN}help${RESET}        Show this help message

${BOLD}OPTIONS:${RESET}
  ${CYAN}--quiet${RESET}     Suppress detailed output (summary only)
  ${CYAN}--strict${RESET}    Treat warnings as errors

${BOLD}EXAMPLES:${RESET}
  node qc/run.js                    # Run all checks
  node qc/run.js links              # Check links only
  node qc/run.js glossary links     # Check glossary and links

${BOLD}EXIT CODES:${RESET}
  0 = All checks passed (warnings OK)
  1 = One or more checks failed with errors
`);
}

function showList() {
    console.log(`\n${BOLD}Available Validators:${RESET}\n`);
    for (const [key, validator] of Object.entries(VALIDATORS)) {
        console.log(`  ${CYAN}${key.padEnd(12)}${RESET} ${validator.description}`);
    }
    console.log();
}

function printBanner() {
    console.log(`
${MAGENTA}╔═══════════════════════════════════════════════════════════════╗${RESET}
${MAGENTA}║${RESET}                                                               ${MAGENTA}║${RESET}
${MAGENTA}║${RESET}   ${BOLD}⛵ SAILS.TO QC SUITE${RESET}                                      ${MAGENTA}║${RESET}
${MAGENTA}║${RESET}   ${DIM}Comprehensive quality control for the Hugo site${RESET}           ${MAGENTA}║${RESET}
${MAGENTA}║${RESET}                                                               ${MAGENTA}║${RESET}
${MAGENTA}╚═══════════════════════════════════════════════════════════════╝${RESET}
`);
}

function printDivider(title) {
    const padding = Math.max(0, 30 - Math.floor(title.length / 2));
    console.log(`\n${BLUE}${'─'.repeat(padding)} ${BOLD}${title}${RESET} ${BLUE}${'─'.repeat(padding)}${RESET}\n`);
}

async function runValidators(validatorKeys) {
    const results = {};
    let totalErrors = 0;
    let totalWarnings = 0;
    
    for (const key of validatorKeys) {
        const validator = VALIDATORS[key];
        if (!validator) {
            console.error(`${RED}Unknown validator: ${key}${RESET}`);
            continue;
        }
        
        printDivider(validator.name);
        
        try {
            const result = validator.fn();
            results[key] = result;
            totalErrors += result.errors || 0;
            totalWarnings += result.warnings || 0;
        } catch (error) {
            console.error(`${RED}Error running ${key} validator: ${error.message}${RESET}`);
            results[key] = { success: false, errors: 1, warnings: 0, error: error.message };
            totalErrors += 1;
        }
    }
    
    return { results, totalErrors, totalWarnings };
}

function printFinalSummary(results, totalErrors, totalWarnings) {
    console.log(`\n${MAGENTA}╔═══════════════════════════════════════════════════════════════╗${RESET}`);
    console.log(`${MAGENTA}║${RESET}                     ${BOLD}FINAL SUMMARY${RESET}                            ${MAGENTA}║${RESET}`);
    console.log(`${MAGENTA}╚═══════════════════════════════════════════════════════════════╝${RESET}\n`);
    
    // Per-validator results
    for (const [key, result] of Object.entries(results)) {
        const validator = VALIDATORS[key];
        const status = result.success 
            ? (result.warnings > 0 ? `${YELLOW}⚠${RESET}` : `${GREEN}✓${RESET}`)
            : `${RED}✗${RESET}`;
        const details = [];
        if (result.errors > 0) details.push(`${RED}${result.errors} error(s)${RESET}`);
        if (result.warnings > 0) details.push(`${YELLOW}${result.warnings} warning(s)${RESET}`);
        
        console.log(`  ${status} ${validator.name}${details.length ? ': ' + details.join(', ') : ''}`);
    }
    
    console.log();
    
    // Overall result
    if (totalErrors === 0 && totalWarnings === 0) {
        console.log(`${GREEN}${BOLD}  ✓ ALL CHECKS PASSED${RESET}`);
        console.log(`${DIM}    Site is ready for deployment${RESET}\n`);
    } else if (totalErrors === 0) {
        console.log(`${YELLOW}${BOLD}  ⚠ PASSED WITH WARNINGS${RESET}`);
        console.log(`${DIM}    ${totalWarnings} warning(s) - consider addressing before deployment${RESET}\n`);
    } else {
        console.log(`${RED}${BOLD}  ✗ CHECKS FAILED${RESET}`);
        console.log(`${DIM}    ${totalErrors} error(s), ${totalWarnings} warning(s) - fix before deployment${RESET}\n`);
    }
}

async function main() {
    const args = process.argv.slice(2);
    
    // Handle help/list commands
    if (args.includes('--help') || args.includes('help') || args.includes('-h')) {
        showHelp();
        process.exit(0);
    }
    
    if (args.includes('list')) {
        showList();
        process.exit(0);
    }
    
    // Parse options
    const options = {
        quiet: args.includes('--quiet'),
        strict: args.includes('--strict')
    };
    
    // Get validator keys (filter out options)
    let validatorKeys = args.filter(arg => !arg.startsWith('--'));
    
    // If no specific validators requested, run all
    if (validatorKeys.length === 0) {
        validatorKeys = Object.keys(VALIDATORS);
    }
    
    // Validate requested validators exist
    for (const key of validatorKeys) {
        if (!VALIDATORS[key]) {
            console.error(`${RED}Unknown validator: ${key}${RESET}`);
            console.log(`Run ${CYAN}node qc/run.js list${RESET} to see available validators`);
            process.exit(1);
        }
    }
    
    printBanner();
    console.log(`${DIM}Running ${validatorKeys.length} validator(s): ${validatorKeys.join(', ')}${RESET}`);
    
    const { results, totalErrors, totalWarnings } = await runValidators(validatorKeys);
    
    printFinalSummary(results, totalErrors, totalWarnings);
    
    // Exit with appropriate code
    if (options.strict) {
        process.exit(totalErrors + totalWarnings > 0 ? 1 : 0);
    } else {
        process.exit(totalErrors > 0 ? 1 : 0);
    }
}

main().catch(error => {
    console.error(`${RED}Fatal error: ${error.message}${RESET}`);
    process.exit(1);
});
