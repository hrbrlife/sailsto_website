#!/usr/bin/env node
/**
 * Sails.to Template Builder
 * 
 * Bakes header/footer templates into static HTML files for production.
 * This eliminates the JS dependency and improves SEO/performance.
 * 
 * Usage:
 *   node build-templates.js              # Process all HTML files
 *   node build-templates.js --watch      # Watch for changes
 *   node build-templates.js file.html    # Process specific file
 * 
 * The script will:
 * 1. Find all HTML files with <div id="site-header"></div> or <div id="site-footer"></div>
 * 2. Replace them with the actual template content
 * 3. Adjust paths based on file depth
 */

const fs = require('fs');
const path = require('path');

const TEMPLATES_DIR = path.join(__dirname, 'assets', 'templates');
const ROOT_DIR = __dirname;

// Files/folders to skip
const SKIP_PATTERNS = [
    'node_modules',
    'assets/templates',
    '_page-template.html',
    '.git'
];

// Load a template file
function loadTemplate(name) {
    const templatePath = path.join(TEMPLATES_DIR, `${name}.html`);
    if (!fs.existsSync(templatePath)) {
        console.error(`Template not found: ${templatePath}`);
        return null;
    }
    return fs.readFileSync(templatePath, 'utf8');
}

// Calculate relative path to root from a file
function getRelativePath(filePath) {
    const relativePath = path.relative(ROOT_DIR, path.dirname(filePath));
    if (!relativePath) return '';
    
    const depth = relativePath.split(path.sep).length;
    return '../'.repeat(depth);
}

// Process template placeholders
function processTemplate(template, basePath) {
    return template.replace(/\{\{ROOT\}\}/g, basePath);
}

// Process a single HTML file
function processFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    const basePath = getRelativePath(filePath);
    
    // Check for header placeholder
    if (content.includes('id="site-header"') || content.includes('data-component="header"')) {
        const headerTemplate = loadTemplate('header');
        if (headerTemplate) {
            const processedHeader = processTemplate(headerTemplate, basePath);
            
            // Replace placeholder div
            content = content.replace(
                /<div\s+id="site-header"[^>]*>\s*<\/div>/gi,
                processedHeader
            );
            content = content.replace(
                /<[^>]+\s+data-component="header"[^>]*>\s*<\/[^>]+>/gi,
                processedHeader
            );
            modified = true;
        }
    }
    
    // Check for footer placeholder
    if (content.includes('id="site-footer"') || content.includes('data-component="footer"')) {
        const footerTemplate = loadTemplate('footer');
        if (footerTemplate) {
            const processedFooter = processTemplate(footerTemplate, basePath);
            
            // Replace placeholder div
            content = content.replace(
                /<div\s+id="site-footer"[^>]*>\s*<\/div>/gi,
                processedFooter
            );
            content = content.replace(
                /<[^>]+\s+data-component="footer"[^>]*>\s*<\/[^>]+>/gi,
                processedFooter
            );
            modified = true;
        }
    }
    
    if (modified) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`✓ Processed: ${path.relative(ROOT_DIR, filePath)}`);
        return true;
    }
    
    return false;
}

// Find all HTML files recursively
function findHtmlFiles(dir, files = []) {
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
        const fullPath = path.join(dir, item);
        const relativePath = path.relative(ROOT_DIR, fullPath);
        
        // Skip certain paths
        if (SKIP_PATTERNS.some(pattern => relativePath.includes(pattern))) {
            continue;
        }
        
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
            findHtmlFiles(fullPath, files);
        } else if (item.endsWith('.html')) {
            files.push(fullPath);
        }
    }
    
    return files;
}

// Main execution
function main() {
    const args = process.argv.slice(2);
    
    console.log('🚢 Sails.to Template Builder\n');
    
    if (args.includes('--help') || args.includes('-h')) {
        console.log('Usage:');
        console.log('  node build-templates.js              # Process all HTML files');
        console.log('  node build-templates.js file.html    # Process specific file');
        console.log('  node build-templates.js --list       # List files that would be processed');
        return;
    }
    
    // Load templates
    const headerTemplate = loadTemplate('header');
    const footerTemplate = loadTemplate('footer');
    
    if (!headerTemplate && !footerTemplate) {
        console.error('No templates found. Exiting.');
        process.exit(1);
    }
    
    console.log('Templates loaded:');
    if (headerTemplate) console.log('  ✓ header.html');
    if (footerTemplate) console.log('  ✓ footer.html');
    console.log('');
    
    let filesToProcess = [];
    
    if (args.length > 0 && !args[0].startsWith('--')) {
        // Process specific file
        const filePath = path.resolve(args[0]);
        if (fs.existsSync(filePath)) {
            filesToProcess = [filePath];
        } else {
            console.error(`File not found: ${args[0]}`);
            process.exit(1);
        }
    } else {
        // Find all HTML files
        filesToProcess = findHtmlFiles(ROOT_DIR);
    }
    
    if (args.includes('--list')) {
        console.log('Files that would be processed:');
        filesToProcess.forEach(f => console.log(`  ${path.relative(ROOT_DIR, f)}`));
        return;
    }
    
    let processed = 0;
    for (const file of filesToProcess) {
        if (processFile(file)) {
            processed++;
        }
    }
    
    console.log(`\n✨ Done! Processed ${processed} file(s).`);
}

main();
