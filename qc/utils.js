/**
 * ═══════════════════════════════════════════════════════════════
 *   SHARED UTILITIES
 * ═══════════════════════════════════════════════════════════════
 */

const fs = require('fs');
const path = require('path');

// ANSI colors
const c = {
    RED: '\x1b[31m',
    GREEN: '\x1b[32m',
    YELLOW: '\x1b[33m',
    BLUE: '\x1b[34m',
    CYAN: '\x1b[36m',
    MAGENTA: '\x1b[35m',
    RESET: '\x1b[0m',
    BOLD: '\x1b[1m',
    DIM: '\x1b[2m',
};

/**
 * Recursively find all files with given extensions in a directory
 */
function findFiles(dir, extensions, files = []) {
    if (!fs.existsSync(dir)) return files;

    const items = fs.readdirSync(dir, { withFileTypes: true });
    for (const item of items) {
        const fullPath = path.join(dir, item.name);
        if (item.isDirectory()) {
            // Skip node_modules, .git, dist, build
            if (['node_modules', '.git', 'dist', 'build', '.next', '.cache'].includes(item.name)) continue;
            findFiles(fullPath, extensions, files);
        } else if (!extensions || extensions.length === 0 || extensions.some(ext => item.name.endsWith(ext))) {
            files.push(fullPath);
        }
    }
    return files;
}

/**
 * Gather all scannable files for a site
 */
function getSiteFiles(site) {
    const files = [];
    for (const dir of [...(site.contentDirs || []), ...(site.layoutDirs || [])]) {
        findFiles(dir, site.fileExtensions, files);
    }
    // Deduplicate
    return [...new Set(files)];
}

/**
 * Print a divider with title
 */
function divider(title) {
    const padding = Math.max(0, 30 - Math.floor(title.length / 2));
    console.log(`\n${c.BLUE}${'─'.repeat(padding)} ${c.BOLD}${title}${c.RESET} ${c.BLUE}${'─'.repeat(padding)}${c.RESET}\n`);
}

module.exports = { c, findFiles, getSiteFiles, divider };
