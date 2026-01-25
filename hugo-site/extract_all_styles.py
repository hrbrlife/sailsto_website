#!/usr/bin/env python3
"""
Extract embedded CSS and JS from ALL drafts HTML files and create separate files
for the Hugo site.
"""

import re
import os
from pathlib import Path

# Define directories
DRAFTS_DIR = Path("/home/user/sailsto_website/drafts")
HUGO_STATIC_CSS = Path("/home/user/sailsto_website/hugo-site/static/assets/css")
HUGO_STATIC_JS = Path("/home/user/sailsto_website/hugo-site/static/js")
HUGO_CONTENT = Path("/home/user/sailsto_website/hugo-site/content")

def extract_styles(html_content):
    """Extract content from <style> tags"""
    pattern = r'<style[^>]*>(.*?)</style>'
    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
    return '\n'.join(matches)

def extract_scripts(html_content):
    """Extract content from inline <script> tags (not external src scripts)"""
    pattern = r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>'
    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
    scripts = [s.strip() for s in matches if s.strip() and len(s.strip()) > 50]
    return '\n\n'.join(scripts)

def get_css_name(rel_path):
    """Convert relative path to CSS filename"""
    # company/legal.html -> company-legal.css
    name = str(rel_path).replace('/', '-').replace('.html', '.css')
    return name

def get_js_name(rel_path):
    """Convert relative path to JS filename"""
    name = str(rel_path).replace('/', '-').replace('.html', '.js')
    return name

def get_md_path(rel_path):
    """Convert HTML path to markdown path"""
    md_rel = str(rel_path).replace('.html', '.md')
    return HUGO_CONTENT / md_rel

def update_frontmatter_clean(md_path, css_file=None, js_file=None):
    """Update the frontmatter with proper formatting"""
    if not md_path.exists():
        print(f"  Warning: {md_path} does not exist")
        return
    
    with open(md_path, 'r') as f:
        content = f.read()
    
    if not content.startswith('---'):
        print(f"  Warning: {md_path} has no frontmatter")
        return
    
    # Find end of frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  Warning: Could not parse frontmatter in {md_path}")
        return
    
    frontmatter = parts[1].strip()
    body = parts[2]
    
    lines = frontmatter.split('\n')
    
    # Check if CSS already added
    css_path = f"/assets/css/{css_file}" if css_file else None
    js_path = f"/js/{js_file}" if js_file else None
    
    needs_css = css_path and css_path not in frontmatter
    needs_js = js_path and js_path not in frontmatter
    
    if not needs_css and not needs_js:
        print(f"  Frontmatter already up to date: {md_path.name}")
        return
    
    new_lines = []
    in_stylesheets = False
    in_scripts = False
    added_css = not needs_css
    added_js = not needs_js
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        if line.strip().startswith('stylesheets:'):
            in_stylesheets = True
            in_scripts = False
        elif line.strip().startswith('scripts:'):
            in_scripts = True
            in_stylesheets = False
        elif in_stylesheets and line.strip().startswith('-'):
            # Check if this is the last stylesheet entry
            next_idx = i + 1
            if next_idx >= len(lines) or (not lines[next_idx].strip().startswith('-') and lines[next_idx].strip()):
                if needs_css and not added_css:
                    new_lines.append(f'  - "{css_path}"')
                    added_css = True
                in_stylesheets = False
        elif in_scripts and line.strip().startswith('-'):
            next_idx = i + 1
            if next_idx >= len(lines) or (not lines[next_idx].strip().startswith('-') and lines[next_idx].strip()):
                if needs_js and not added_js:
                    new_lines.append(f'  - "{js_path}"')
                    added_js = True
                in_scripts = False
        elif (in_stylesheets or in_scripts) and line.strip() and not line.strip().startswith('-'):
            in_stylesheets = False
            in_scripts = False
    
    # If stylesheets section doesn't exist, add it
    if needs_css and not added_css:
        if 'stylesheets:' not in frontmatter:
            new_lines.append('stylesheets:')
            new_lines.append(f'  - "{css_path}"')
            added_css = True
    
    # If scripts section doesn't exist, add it
    if needs_js and not added_js:
        if 'scripts:' not in frontmatter:
            new_lines.append('scripts:')
            new_lines.append(f'  - "{js_path}"')
            added_js = True
    
    new_frontmatter = '\n'.join(new_lines)
    new_content = f'---\n{new_frontmatter}\n---{body}'
    
    with open(md_path, 'w') as f:
        f.write(new_content)
    
    print(f"  Updated frontmatter in {md_path.name}")

def find_html_files_with_styles():
    """Find all HTML files with embedded styles"""
    files = []
    for html_path in DRAFTS_DIR.rglob('*.html'):
        # Skip _source and other directories
        if '_source' in str(html_path) or 'dist' in str(html_path):
            continue
        
        with open(html_path, 'r') as f:
            content = f.read()
        
        if '<style' in content.lower():
            rel_path = html_path.relative_to(DRAFTS_DIR)
            files.append(rel_path)
    
    return sorted(files)

def process_page(rel_path):
    """Process a single HTML page"""
    html_path = DRAFTS_DIR / rel_path
    
    print(f"\nProcessing {rel_path}...")
    
    with open(html_path, 'r') as f:
        html_content = f.read()
    
    # Extract styles
    styles = extract_styles(html_content)
    css_file = None
    if styles.strip():
        css_file = get_css_name(rel_path)
        css_path = HUGO_STATIC_CSS / css_file
        
        if css_path.exists():
            print(f"  CSS file already exists: {css_file}")
        else:
            css_path.parent.mkdir(parents=True, exist_ok=True)
            with open(css_path, 'w') as f:
                f.write(f"/* Styles for {rel_path} */\n\n")
                f.write(styles)
            print(f"  Created CSS: {css_file} ({len(styles)} bytes)")
    
    # Extract scripts
    scripts = extract_scripts(html_content)
    js_file = None
    if scripts.strip():
        js_file = get_js_name(rel_path)
        js_path = HUGO_STATIC_JS / js_file
        
        if js_path.exists():
            print(f"  JS file already exists: {js_file}")
        else:
            js_path.parent.mkdir(parents=True, exist_ok=True)
            with open(js_path, 'w') as f:
                f.write(f"// Scripts for {rel_path}\n\n")
                f.write(scripts)
            print(f"  Created JS: {js_file} ({len(scripts)} bytes)")
    
    # Update markdown frontmatter
    md_path = get_md_path(rel_path)
    if css_file or js_file:
        update_frontmatter_clean(md_path, css_file, js_file)

def main():
    print("=" * 60)
    print("Extracting embedded CSS/JS from ALL drafts HTML files")
    print("=" * 60)
    
    HUGO_STATIC_CSS.mkdir(parents=True, exist_ok=True)
    HUGO_STATIC_JS.mkdir(parents=True, exist_ok=True)
    
    files = find_html_files_with_styles()
    print(f"\nFound {len(files)} HTML files with embedded styles")
    
    for rel_path in files:
        process_page(rel_path)
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()
