#!/usr/bin/env python3
"""
HTML to Hugo Markdown Converter
Extracts content from HTML files and creates Markdown files for Hugo
Uses only built-in Python modules - no external dependencies
"""

import os
import re
from pathlib import Path

def extract_meta_tag(html_content, tag_name, attr_name='name'):
    """Extract content from meta tags"""
    pattern = f'<meta\\s+{attr_name}="([^"]*)"\\s+content="([^"]*)"'
    match = re.search(pattern, html_content, re.IGNORECASE)
    if match and match.group(1) == tag_name:
        return match.group(2)
    
    # Alternative pattern for property-based meta tags
    pattern = f'<meta\\s+property="([^"]*)"\\s+content="([^"]*)"'
    match = re.search(pattern, html_content, re.IGNORECASE)
    if match and match.group(1) == tag_name:
        return match.group(2)
    
    return None

def extract_frontmatter(html_content):
    """Extract metadata from HTML head"""
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    title_text = title_match.group(1) if title_match else "Page Title"
    
    # Remove the site name from title if present
    if ' | ' in title_text:
        title_text = title_text.split(' | ')[0]
    
    # Extract description
    description_match = re.search(
        r'<meta\s+name="description"\s+content="([^"]*)"',
        html_content,
        re.IGNORECASE
    )
    description = description_match.group(1) if description_match else ''
    
    # Extract OG image
    og_image_match = re.search(
        r'<meta\s+property="og:image"\s+content="([^"]*)"',
        html_content,
        re.IGNORECASE
    )
    og_image = og_image_match.group(1) if og_image_match else ''
    
    return {
        'title': title_text.strip(),
        'description': description.strip(),
        'og_image': og_image.strip() if og_image else ''
    }

def extract_stylesheets(html_content):
    """Extract stylesheet links from HTML"""
    stylesheets = []
    
    # Find all stylesheet links
    pattern = r'<link\s+rel="stylesheet"\s+href="([^"]*)"'
    matches = re.finditer(pattern, html_content, re.IGNORECASE)
    
    for match in matches:
        href = match.group(1)
        if href:
            # Normalize paths
            if href.startswith('assets/'):
                href = '/' + href
            elif href.startswith('./'):
                href = '/' + href[2:]
            elif not href.startswith('/'):
                href = '/' + href
            stylesheets.append(href)
    
    return stylesheets

def extract_body_content(html_content):
    """Extract content between nav and footer"""
    # Find nav end
    nav_match = re.search(r'</nav>', html_content, re.IGNORECASE)
    footer_match = re.search(r'<footer', html_content, re.IGNORECASE)
    
    if nav_match and footer_match:
        nav_end = nav_match.end()
        footer_start = footer_match.start()
        content = html_content[nav_end:footer_start].strip()
        
        # Remove HTML comments and extra whitespace
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        content = re.sub(r'\n\s*\n', '\n', content)
        
        return content
    
    return ""

def create_markdown_file(html_path, output_dir):
    """Convert HTML file to Markdown"""
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract metadata
        frontmatter = extract_frontmatter(html_content)
        stylesheets = extract_stylesheets(html_content)
        body_content = extract_body_content(html_content)
        
        # Determine output filename
        html_filename = Path(html_path).stem
        
        # Map specific filenames to their paths
        path_mapping = {
            'index': '_index.md',
            'issuers': 'issuers.md',
            'investors': 'investors.md',
            'brokers': 'brokers.md',
            'introducers': 'introducers.md',
            'regulated': 'regulated.md',
            'issuers-directory': 'issuers-directory.md',
            'whatsails': 'whatsails.md',
            'pricing': 'pricing.md',
            'signup': 'signup.md',
        }
        
        if html_filename in path_mapping:
            output_filename = path_mapping[html_filename]
        else:
            output_filename = f'{html_filename}.md'
        
        output_path = Path(output_dir) / output_filename
        
        # Create frontmatter
        frontmatter_str = '---\n'
        frontmatter_str += f'title: "{frontmatter["title"]}"\n'
        if frontmatter['description']:
            frontmatter_str += f'description: "{frontmatter["description"]}"\n'
        if stylesheets:
            frontmatter_str += 'stylesheets:\n'
            for sheet in stylesheets:
                frontmatter_str += f'  - "{sheet}"\n'
        frontmatter_str += '---\n\n'
        
        # Create markdown content
        markdown_content = frontmatter_str + body_content + '\n'
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return True, str(output_path)
    
    except Exception as e:
        return False, str(e)

def main():
    """Main conversion script"""
    drafts_dir = Path('/home/user/sailsto_website/drafts')
    hugo_content = Path('/home/user/sailsto_website/hugo-site/content')
    
    # Get all HTML files (excluding _source subdirectory)
    html_files = [f for f in drafts_dir.glob('*.html')]
    
    print(f"Found {len(html_files)} HTML files to convert\n")
    
    success_count = 0
    failed_files = []
    converted_files = []
    
    for html_file in sorted(html_files):
        print(f"Converting {html_file.name:30s}...", end=' ')
        success, result = create_markdown_file(str(html_file), hugo_content)
        
        if success:
            print(f"✅")
            success_count += 1
            converted_files.append(html_file.name)
        else:
            print(f"❌ {result}")
            failed_files.append((html_file.name, result))
    
    print(f"\n{'='*60}")
    print(f"Conversion complete!")
    print(f"Successfully converted: {success_count}/{len(html_files)}")
    
    if converted_files:
        print(f"\nConverted files:")
        for name in converted_files:
            print(f"  ✅ {name}")
    
    if failed_files:
        print(f"\nFailed conversions:")
        for filename, error in failed_files:
            print(f"  ❌ {filename}: {error}")

if __name__ == '__main__':
    main()

