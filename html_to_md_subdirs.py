#!/usr/bin/env python3
"""
HTML to Hugo Markdown Converter - Subdirectories
Converts HTML files in subdirectories (company, knowledge, blog, docs, etc.)
"""

import re
from pathlib import Path

def extract_meta_tag(html_content, tag_name, attr_name='name'):
    """Extract content from meta tags"""
    pattern = f'<meta\\s+{attr_name}="([^"]*)"\\s+content="([^"]*)"'
    match = re.search(pattern, html_content, re.IGNORECASE)
    if match and match.group(1) == tag_name:
        return match.group(2)
    
    pattern = f'<meta\\s+property="([^"]*)"\\s+content="([^"]*)"'
    match = re.search(pattern, html_content, re.IGNORECASE)
    if match and match.group(1) == tag_name:
        return match.group(2)
    
    return None

def extract_frontmatter(html_content):
    """Extract metadata from HTML head"""
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    title_text = title_match.group(1) if title_match else "Page Title"
    
    if ' | ' in title_text:
        title_text = title_text.split(' | ')[0]
    
    description_match = re.search(
        r'<meta\s+name="description"\s+content="([^"]*)"',
        html_content,
        re.IGNORECASE
    )
    description = description_match.group(1) if description_match else ''
    
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
    pattern = r'<link\s+rel="stylesheet"\s+href="([^"]*)"'
    matches = re.finditer(pattern, html_content, re.IGNORECASE)
    
    for match in matches:
        href = match.group(1)
        if href:
            # Normalize paths - relative to content root
            # Since these are in subdirs, we need to go up levels
            if href.startswith('../'):
                href = href
            elif href.startswith('assets/'):
                href = '../' + href
            elif href == 'styles.css':
                href = '../styles.css'
            elif not href.startswith('/'):
                href = '../' + href
            stylesheets.append(href)
    
    return stylesheets

def extract_body_content(html_content):
    """Extract content between nav and footer"""
    nav_match = re.search(r'</nav>', html_content, re.IGNORECASE)
    footer_match = re.search(r'<footer', html_content, re.IGNORECASE)
    
    if nav_match and footer_match:
        nav_end = nav_match.end()
        footer_start = footer_match.start()
        content = html_content[nav_end:footer_start].strip()
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        content = re.sub(r'\n\s*\n', '\n', content)
        return content
    
    return ""

def create_markdown_file(html_path, output_dir):
    """Convert HTML file to Markdown"""
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        frontmatter = extract_frontmatter(html_content)
        stylesheets = extract_stylesheets(html_content)
        body_content = extract_body_content(html_content)
        
        html_filename = Path(html_path).stem
        
        # Index files become _index.md, others become name.md
        if html_filename == 'index':
            output_filename = '_index.md'
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
        
        markdown_content = frontmatter_str + body_content + '\n'
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return True, str(output_path)
    
    except Exception as e:
        return False, str(e)

def main():
    """Main conversion script for subdirectories"""
    base_dir = Path('/home/user/sailsto_website/drafts')
    hugo_content = Path('/home/user/sailsto_website/hugo-site/content')
    
    # Subdirectories to convert
    subdirs = ['company', 'knowledge', 'knowledge/blog', 'knowledge/docs', 'knowledge/glossary', 'knowledge/guides']
    
    total_count = 0
    success_count = 0
    failed_files = []
    
    for subdir in subdirs:
        src_dir = base_dir / subdir
        if not src_dir.exists():
            continue
        
        html_files = list(src_dir.glob('*.html'))
        if not html_files:
            continue
        
        print(f"\n{'='*60}")
        print(f"Converting {subdir.upper()}")
        print(f"Found {len(html_files)} files")
        print('='*60)
        
        for html_file in sorted(html_files):
            total_count += 1
            output_dir = hugo_content / subdir
            
            print(f"  {html_file.name:30s}...", end=' ')
            success, result = create_markdown_file(str(html_file), output_dir)
            
            if success:
                print(f"✅")
                success_count += 1
            else:
                print(f"❌ {result}")
                failed_files.append((f"{subdir}/{html_file.name}", result))
    
    print(f"\n{'='*60}")
    print(f"SUBDIRECTORY CONVERSION COMPLETE")
    print(f"Successfully converted: {success_count}/{total_count}")
    
    if failed_files:
        print(f"\nFailed conversions:")
        for filename, error in failed_files:
            print(f"  ❌ {filename}: {error}")

if __name__ == '__main__':
    main()
