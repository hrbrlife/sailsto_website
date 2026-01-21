#!/usr/bin/env python3
"""
Sails.to Template Builder

Bakes header/footer templates into static HTML files for production.
This eliminates the JS dependency and improves SEO/performance.

Usage:
    python3 build-templates.py              # Process all HTML files
    python3 build-templates.py file.html    # Process specific file
    python3 build-templates.py --list       # List files that would be processed
    python3 build-templates.py --reverse    # Convert back to placeholders
"""

import os
import re
import sys
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
TEMPLATES_DIR = SCRIPT_DIR / 'assets' / 'templates'

# Files/folders to skip
SKIP_PATTERNS = [
    'node_modules',
    'assets/templates',
    '_page-template.html',
    '.git',
    '__pycache__'
]


def load_template(name: str) -> str | None:
    """Load a template file."""
    template_path = TEMPLATES_DIR / f'{name}.html'
    if not template_path.exists():
        print(f'Template not found: {template_path}')
        return None
    return template_path.read_text(encoding='utf-8')


def get_relative_path(file_path: Path) -> str:
    """Calculate relative path to root from a file."""
    try:
        relative = file_path.parent.relative_to(SCRIPT_DIR)
        depth = len(relative.parts)
        return '../' * depth if depth > 0 else ''
    except ValueError:
        return ''


def process_template(template: str, base_path: str) -> str:
    """Process template placeholders."""
    return template.replace('{{ROOT}}', base_path)


def process_file(file_path: Path, header_template: str | None, footer_template: str | None) -> bool:
    """Process a single HTML file."""
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    base_path = get_relative_path(file_path)
    
    # Check for header placeholder
    if header_template and ('id="site-header"' in content or 'data-component="header"' in content):
        processed_header = process_template(header_template, base_path)
        
        # Replace placeholder div
        content = re.sub(
            r'<div\s+id="site-header"[^>]*>\s*</div>',
            processed_header,
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r'<[^>]+\s+data-component="header"[^>]*>\s*</[^>]+>',
            processed_header,
            content,
            flags=re.IGNORECASE
        )
    
    # Check for footer placeholder
    if footer_template and ('id="site-footer"' in content or 'data-component="footer"' in content):
        processed_footer = process_template(footer_template, base_path)
        
        # Replace placeholder div
        content = re.sub(
            r'<div\s+id="site-footer"[^>]*>\s*</div>',
            processed_footer,
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r'<[^>]+\s+data-component="footer"[^>]*>\s*</[^>]+>',
            processed_footer,
            content,
            flags=re.IGNORECASE
        )
    
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        relative_path = file_path.relative_to(SCRIPT_DIR)
        print(f'✓ Processed: {relative_path}')
        return True
    
    return False


def reverse_file(file_path: Path) -> bool:
    """Convert baked templates back to placeholders."""
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    # Replace nav with placeholder
    content = re.sub(
        r'<nav>[\s\S]*?</nav>',
        '<div id="site-header"></div>',
        content,
        count=1
    )
    
    # Replace footer with placeholder
    content = re.sub(
        r'<footer>[\s\S]*?</footer>',
        '<div id="site-footer"></div>',
        content,
        count=1
    )
    
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        relative_path = file_path.relative_to(SCRIPT_DIR)
        print(f'✓ Reversed: {relative_path}')
        return True
    
    return False


def find_html_files(directory: Path) -> list[Path]:
    """Find all HTML files recursively."""
    files = []
    
    for item in directory.rglob('*.html'):
        relative_path = str(item.relative_to(SCRIPT_DIR))
        
        # Skip certain paths
        if any(pattern in relative_path for pattern in SKIP_PATTERNS):
            continue
        
        files.append(item)
    
    return sorted(files)


def main():
    args = sys.argv[1:]
    
    print('🚢 Sails.to Template Builder\n')
    
    if '--help' in args or '-h' in args:
        print('Usage:')
        print('  python3 build-templates.py              # Process all HTML files')
        print('  python3 build-templates.py file.html    # Process specific file')
        print('  python3 build-templates.py --list       # List files that would be processed')
        print('  python3 build-templates.py --reverse    # Convert back to placeholders')
        return
    
    reverse_mode = '--reverse' in args
    if reverse_mode:
        args.remove('--reverse')
    
    # Load templates
    header_template = load_template('header')
    footer_template = load_template('footer')
    
    if not reverse_mode and not header_template and not footer_template:
        print('No templates found. Exiting.')
        sys.exit(1)
    
    if not reverse_mode:
        print('Templates loaded:')
        if header_template:
            print('  ✓ header.html')
        if footer_template:
            print('  ✓ footer.html')
        print('')
    
    # Determine files to process
    if args and not args[0].startswith('--'):
        # Process specific file
        file_path = Path(args[0]).resolve()
        if not file_path.exists():
            print(f'File not found: {args[0]}')
            sys.exit(1)
        files_to_process = [file_path]
    else:
        # Find all HTML files
        files_to_process = find_html_files(SCRIPT_DIR)
    
    if '--list' in args:
        print('Files that would be processed:')
        for f in files_to_process:
            print(f'  {f.relative_to(SCRIPT_DIR)}')
        return
    
    processed = 0
    for file_path in files_to_process:
        if reverse_mode:
            if reverse_file(file_path):
                processed += 1
        else:
            if process_file(file_path, header_template, footer_template):
                processed += 1
    
    action = 'Reversed' if reverse_mode else 'Processed'
    print(f'\n✨ Done! {action} {processed} file(s).')


if __name__ == '__main__':
    main()
