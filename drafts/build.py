#!/usr/bin/env python3
"""
Sails.to Static Site Builder

Builds HTML files from _source/ by:
1. Replacing {{NAV}} with nav.html include (paths adjusted for depth)
2. Replacing {{FOOTER}} with footer.html include (paths adjusted for depth)
3. Replacing {{ROOT}} with correct relative path

Usage:
    python3 build.py              # Build all source files to output
    python3 build.py --init       # Create _source/ files from existing HTML (normalizes nav/footer)
    python3 build.py --verify     # Compare built output to existing files
    python3 build.py file.html    # Build a single file
"""

import os
import re
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
SOURCE_DIR = SCRIPT_DIR / '_source'
INCLUDES_DIR = SOURCE_DIR / '_includes'
OUTPUT_DIR = SCRIPT_DIR

# Files with completely different structure (skip entirely)
STANDALONE_FILES = {'whatsails.html', 'exec_summ.html', 'pitchdeck.html'}

# Directories to skip
SKIP_PATTERNS = ['_source', 'node_modules', '.git', 'diagrams']


def should_skip(path: Path) -> bool:
    """Check if path should be skipped."""
    path_str = str(path)
    return any(pattern in path_str for pattern in SKIP_PATTERNS)


def get_root_path(rel_path: Path) -> str:
    """Calculate relative path to root from file location."""
    depth = len(rel_path.parts) - 1
    return '../' * depth if depth > 0 else ''


def load_include(name: str) -> str:
    """Load an include template."""
    path = INCLUDES_DIR / f'{name}.html'
    if not path.exists():
        raise FileNotFoundError(f"Include not found: {path}")
    return path.read_text()


def process_content(content: str, root_path: str) -> str:
    """Replace placeholders with includes."""
    nav = load_include('nav').replace('{{ROOT}}', root_path)
    footer = load_include('footer').replace('{{ROOT}}', root_path)
    
    content = content.replace('{{NAV}}', nav)
    content = content.replace('{{FOOTER}}', footer)
    content = content.replace('{{ROOT}}', root_path)
    
    return content


def build_file(source_path: Path) -> tuple[Path, str]:
    """Build single file. Returns (output_path, status)."""
    rel_path = source_path.relative_to(SOURCE_DIR)
    output_path = OUTPUT_DIR / rel_path
    root_path = get_root_path(rel_path)
    
    content = source_path.read_text()
    built = process_content(content, root_path)
    
    # Compare to existing
    status = 'new'
    if output_path.exists():
        existing = output_path.read_text()
        if existing == built:
            return output_path, 'unchanged'
        status = 'updated'
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(built)
    return output_path, status


def build_all():
    """Build all source files."""
    if not SOURCE_DIR.exists():
        print(f"Error: {SOURCE_DIR} not found. Run --init first.")
        return 1
    
    print(f"Building from: {SOURCE_DIR}")
    print(f"Output to: {OUTPUT_DIR}")
    print()
    
    stats = {'new': 0, 'updated': 0, 'unchanged': 0}
    
    for source_path in sorted(SOURCE_DIR.rglob('*.html')):
        if '_includes' in source_path.parts:
            continue
        
        rel_path = source_path.relative_to(SOURCE_DIR)
        _, status = build_file(source_path)
        stats[status] += 1
        
        icon = {'new': '+', 'updated': '✓', 'unchanged': '·'}[status]
        print(f"  {icon} {rel_path}")
    
    print()
    print(f"Done: {stats['new']} new, {stats['updated']} updated, {stats['unchanged']} unchanged")
    return 0


def init_source():
    """
    Create _source/ files from existing HTML.
    Normalizes nav/footer by replacing with {{NAV}} and {{FOOTER}} placeholders.
    """
    print("Initializing source files...")
    print("This will normalize nav/footer across all files.")
    print()
    
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    INCLUDES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Regex patterns to match nav and footer blocks
    nav_pattern = re.compile(
        r'^([ \t]*)<nav>.*?</nav>',
        re.MULTILINE | re.DOTALL
    )
    footer_pattern = re.compile(
        r'^([ \t]*)<footer>.*?</footer>',
        re.MULTILINE | re.DOTALL
    )
    
    created = 0
    skipped = 0
    
    for html_path in sorted(OUTPUT_DIR.rglob('*.html')):
        if should_skip(html_path):
            continue
        if html_path.name in STANDALONE_FILES:
            skipped += 1
            continue
        
        rel_path = html_path.relative_to(OUTPUT_DIR)
        content = html_path.read_text()
        
        # Replace nav with placeholder
        nav_match = nav_pattern.search(content)
        if nav_match:
            indent = nav_match.group(1)
            content = nav_pattern.sub(f'{indent}{{{{NAV}}}}', content)
        
        # Replace footer with placeholder
        footer_match = footer_pattern.search(content)
        if footer_match:
            indent = footer_match.group(1)
            content = footer_pattern.sub(f'{indent}{{{{FOOTER}}}}', content)
        
        # Write source file
        source_path = SOURCE_DIR / rel_path
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_text(content)
        
        created += 1
        print(f"  + _source/{rel_path}")
    
    print()
    print(f"Created {created} source files, skipped {skipped} standalone files")
    print()
    print("Next: Run 'python3 build.py' to build normalized output")
    return 0


def verify_build():
    """Build and compare to existing files."""
    if not SOURCE_DIR.exists():
        print(f"Error: {SOURCE_DIR} not found")
        return 1
    
    print("Verifying build output matches existing files...")
    print()
    
    matches = 0
    differs = 0
    
    for source_path in sorted(SOURCE_DIR.rglob('*.html')):
        if '_includes' in source_path.parts:
            continue
        
        rel_path = source_path.relative_to(SOURCE_DIR)
        output_path = OUTPUT_DIR / rel_path
        root_path = get_root_path(rel_path)
        
        content = source_path.read_text()
        built = process_content(content, root_path)
        
        if not output_path.exists():
            print(f"  ? {rel_path} (no existing file)")
            differs += 1
            continue
        
        existing = output_path.read_text()
        
        if built == existing:
            print(f"  ✓ {rel_path}")
            matches += 1
        else:
            print(f"  ✗ {rel_path}")
            differs += 1
            
            # Find first difference
            for i, (a, b) in enumerate(zip(built, existing)):
                if a != b:
                    line = built[:i].count('\n') + 1
                    col = i - built[:i].rfind('\n')
                    print(f"      Line {line}, col {col}")
                    print(f"      Built: {repr(built[max(0,i-20):i+30])}")
                    print(f"      Exist: {repr(existing[max(0,i-20):i+30])}")
                    break
    
    print()
    if differs == 0:
        print(f"SUCCESS: All {matches} files match")
        return 0
    else:
        print(f"DIFFERS: {differs} files differ, {matches} match")
        return 1


def main():
    if len(sys.argv) < 2:
        return build_all()
    
    cmd = sys.argv[1]
    
    if cmd == '--init':
        return init_source()
    elif cmd == '--verify':
        return verify_build()
    elif cmd == '--help':
        print(__doc__)
        return 0
    elif cmd.endswith('.html'):
        source_path = SOURCE_DIR / cmd
        if not source_path.exists():
            print(f"Error: {source_path} not found")
            return 1
        output_path, status = build_file(source_path)
        print(f"{status}: {output_path}")
        return 0
    else:
        print(f"Unknown command: {cmd}")
        print("Use --help for usage")
        return 1


if __name__ == '__main__':
    sys.exit(main())
