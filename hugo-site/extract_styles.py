#!/usr/bin/env python3
"""
Extract embedded CSS and JS from drafts HTML files and create separate files
for the Hugo site.
"""

import re
import os
from pathlib import Path

# Define source and target directories
DRAFTS_DIR = Path("/home/user/sailsto_website/drafts")
HUGO_STATIC_CSS = Path("/home/user/sailsto_website/hugo-site/static/assets/css")
HUGO_STATIC_JS = Path("/home/user/sailsto_website/hugo-site/static/js")
HUGO_CONTENT = Path("/home/user/sailsto_website/hugo-site/content")

# Pages with embedded styles
PAGES_WITH_STYLES = [
    "introducers.html",
    "issuers-directory.html",
    "brokers.html", 
    "signup.html",
    "pricing.html",
    "whatsails.html",
]

def extract_styles(html_content):
    """Extract content from <style> tags"""
    pattern = r'<style[^>]*>(.*?)</style>'
    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
    return '\n'.join(matches)

def extract_scripts(html_content):
    """Extract content from inline <script> tags (not external src scripts)"""
    # Match script tags that don't have src attribute
    pattern = r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>'
    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
    # Filter out empty scripts and scripts that are just nav.js type references
    scripts = [s.strip() for s in matches if s.strip() and len(s.strip()) > 50]
    return '\n\n'.join(scripts)

def get_markdown_name(html_name):
    """Convert HTML filename to markdown filename"""
    return html_name.replace('.html', '.md')

def update_frontmatter(md_path, css_file=None, js_file=None):
    """Update the frontmatter of a markdown file to include new css/js files"""
    if not md_path.exists():
        print(f"  Warning: {md_path} does not exist")
        return
    
    with open(md_path, 'r') as f:
        content = f.read()
    
    # Check if there's frontmatter
    if not content.startswith('---'):
        print(f"  Warning: {md_path} has no frontmatter")
        return
    
    # Find the end of frontmatter
    end_match = re.search(r'^---\s*$', content[3:], re.MULTILINE)
    if not end_match:
        print(f"  Warning: Could not find end of frontmatter in {md_path}")
        return
    
    end_pos = end_match.start() + 3
    frontmatter = content[3:end_pos]
    body = content[end_pos + 3:]  # Skip the closing ---
    
    # Add CSS file to stylesheets if not already there
    if css_file:
        css_path = f"/assets/css/{css_file}"
        if css_path not in frontmatter:
            # Find stylesheets section or add one
            if 'stylesheets:' in frontmatter:
                # Add to existing list
                lines = frontmatter.split('\n')
                new_lines = []
                in_stylesheets = False
                added = False
                for line in lines:
                    new_lines.append(line)
                    if 'stylesheets:' in line:
                        in_stylesheets = True
                    elif in_stylesheets and line.strip().startswith('-'):
                        # We're in the stylesheets list
                        pass
                    elif in_stylesheets and not line.strip().startswith('-'):
                        # End of stylesheets list
                        if not added:
                            # Insert before this line
                            new_lines.insert(-1, f'  - "{css_path}"')
                            added = True
                        in_stylesheets = False
                if in_stylesheets and not added:
                    new_lines.append(f'  - "{css_path}"')
                frontmatter = '\n'.join(new_lines)
            else:
                # Add new stylesheets section
                frontmatter += f'\nstylesheets:\n  - "{css_path}"'
    
    # Add JS file to scripts if not already there
    if js_file:
        js_path = f"/js/{js_file}"
        if js_path not in frontmatter:
            if 'scripts:' in frontmatter:
                # Add to existing list
                lines = frontmatter.split('\n')
                new_lines = []
                in_scripts = False
                added = False
                for line in lines:
                    new_lines.append(line)
                    if line.strip().startswith('scripts:'):
                        in_scripts = True
                    elif in_scripts and line.strip().startswith('-'):
                        pass
                    elif in_scripts and not line.strip().startswith('-'):
                        if not added:
                            new_lines.insert(-1, f'  - "{js_path}"')
                            added = True
                        in_scripts = False
                if in_scripts and not added:
                    new_lines.append(f'  - "{js_path}"')
                frontmatter = '\n'.join(new_lines)
            else:
                frontmatter += f'\nscripts:\n  - "{js_path}"'
    
    # Reconstruct the file
    new_content = '---' + frontmatter + '---' + body
    
    with open(md_path, 'w') as f:
        f.write(new_content)
    
    print(f"  Updated frontmatter in {md_path.name}")

def process_page(html_name):
    """Process a single HTML page"""
    html_path = DRAFTS_DIR / html_name
    base_name = html_name.replace('.html', '')
    
    print(f"\nProcessing {html_name}...")
    
    if not html_path.exists():
        print(f"  File not found: {html_path}")
        return
    
    with open(html_path, 'r') as f:
        html_content = f.read()
    
    # Extract styles
    styles = extract_styles(html_content)
    css_file = None
    if styles.strip():
        css_file = f"{base_name}.css"
        css_path = HUGO_STATIC_CSS / css_file
        
        # Check if file already exists and has same content
        if css_path.exists():
            with open(css_path, 'r') as f:
                existing = f.read()
            if existing.strip() == styles.strip():
                print(f"  CSS file already up to date: {css_file}")
            else:
                print(f"  CSS file exists but differs, skipping: {css_file}")
                css_file = None
        else:
            css_path.parent.mkdir(parents=True, exist_ok=True)
            with open(css_path, 'w') as f:
                f.write(f"/* Styles for {html_name} */\n\n")
                f.write(styles)
            print(f"  Created CSS: {css_file} ({len(styles)} bytes)")
    
    # Extract scripts
    scripts = extract_scripts(html_content)
    js_file = None
    if scripts.strip():
        js_file = f"{base_name}.js"
        js_path = HUGO_STATIC_JS / js_file
        
        if js_path.exists():
            with open(js_path, 'r') as f:
                existing = f.read()
            if existing.strip() == scripts.strip():
                print(f"  JS file already up to date: {js_file}")
            else:
                print(f"  JS file exists but differs, skipping: {js_file}")
                js_file = None
        else:
            js_path.parent.mkdir(parents=True, exist_ok=True)
            with open(js_path, 'w') as f:
                f.write(f"// Scripts for {html_name}\n\n")
                f.write(scripts)
            print(f"  Created JS: {js_file} ({len(scripts)} bytes)")
    
    # Update markdown frontmatter
    md_path = HUGO_CONTENT / get_markdown_name(html_name)
    if css_file or js_file:
        update_frontmatter(md_path, css_file, js_file)

def main():
    print("=" * 60)
    print("Extracting embedded CSS/JS from drafts HTML files")
    print("=" * 60)
    
    # Ensure directories exist
    HUGO_STATIC_CSS.mkdir(parents=True, exist_ok=True)
    HUGO_STATIC_JS.mkdir(parents=True, exist_ok=True)
    
    for page in PAGES_WITH_STYLES:
        process_page(page)
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()
