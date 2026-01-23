#!/usr/bin/env python3
"""
Knowledge Base File Cleaner

Extracts clean regulatory text from HTML-contaminated files.
Handles law.cornell.edu scrapes, Federal Register pages, and other sources.
"""

import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from typing import Optional


class TextExtractor(HTMLParser):
    """Extract text content from HTML, ignoring scripts, styles, and navigation."""
    
    def __init__(self):
        super().__init__()
        self.text_parts: list[str] = []
        self.skip_depth = 0
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'aside', 'noscript', 'iframe'}
        self.block_tags = {'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'tr', 'br', 'section', 'article'}
        
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_depth += 1
        elif tag in self.block_tags and self.text_parts and self.text_parts[-1] != '\n':
            self.text_parts.append('\n')
            
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_depth = max(0, self.skip_depth - 1)
        elif tag in self.block_tags and self.text_parts and self.text_parts[-1] != '\n':
            self.text_parts.append('\n')
    
    def handle_data(self, data):
        if self.skip_depth == 0:
            self.text_parts.append(data)
    
    def get_text(self) -> str:
        return ''.join(self.text_parts)


def is_html_contaminated(content: str) -> bool:
    """Check if content appears to be HTML rather than plain text."""
    indicators = [
        'window.dataLayer',
        'function gtag()',
        '<script',
        '<!DOCTYPE',
        '<html',
        'googleapis.com',
        'googletagservices',
        'BOOMR',
        'akamaihd.net',
        'Skip to main content',
    ]
    first_2000 = content[:2000]
    return any(ind in first_2000 for ind in indicators)


def clean_browser_text_dump(content: str, filename: str) -> str:
    """Clean browser text dump (not proper HTML, but raw text with JS noise)."""
    lines = content.split('\n')
    clean_lines = []
    
    # Patterns that indicate noise lines to skip
    noise_patterns = [
        r'^window\.',
        r'^function\s+\w+\(\)',
        r'gtag\(',
        r'dataLayer',
        r'BOOMR',
        r'akamaihd',
        r'googleapis',
        r'googletagservices',
        r'^!function',
        r'snippetExecuted',
        r'\.addEventListener',
        r'\.attachEvent',
        r'document\.createElement',
        r'performance\.setResourceTimingBufferSize',
        r'^var\s+\w+\s*=',
        r'^\s*if\s*\(\s*["\']',
        r'ak\.\w+',
        r'BOOMR_',
        r'^Here\'s how you know',
        r'^The \.gov means',
        r'^Federal government websites',
        r'^The site is secure',
        r'^The https://',
        r'^Skip to main content',
        r'^An official website of',
        r'^\s*Menu\s*$',
        r'^\s*Resources\s*$',
        r'^\s*About\s+\w+\s*$',
        r'^What We Do$',
        r'^Mission$',
        r'^Insignia$',
        r'^EEO$',
        r'^Contract Opportunities$',
        r'Alerts/Advisories/Notices',
        r'^Subscribe$',
        r'^Contact$',
        r'^Careers$',
        r'^Privacy Policy$',
        r'^Accessibility$',
        r'^USA.gov$',
        r'^FOIA$',
        r'^No Fear Act$',
        r'^Inspector General$',
        r'^\s*Search\s*$',
        r'^Follow us',
        r'^Share this page',
        r'^Email$',
        r'^Facebook$',
        r'^Twitter$',
        r'^LinkedIn$',
        r'^\s*Print$',
        r'Last Updated',
        # Additional navigation/menu items
        r'^Bank Secrecy Act Filing Information$',
        r'^Beneficial Ownership Information',
        r'^Financial Trend Analyses$',
        r'^Financial Institutions$',
        r'^FinCEN Exchange$',
        r'^Innovation$',
        r'^International$',
        r'^Law Enforcement$',
        r'^Ransomware$',
        r'^Residential Real Estate',
        r'^SAR Advisory Key Terms$',
        r'^SAR Stats$',
        r'^Scams$',
        r'^Statutes and Regulations$',
        r'^Advisories$',
        r'^News$',
        r'^Press Releases$',
        r'^Readouts$',
        r'^Speeches$',
        r'^Testimony$',
        r'^Enforcement Actions$',
        r'^SAR Technical Bulletins$',
        r'aria-expanded',
        r'aria-controls',
        r'usa-accordion',
        r'usa-banner',
    ]
    
    # Compile patterns for efficiency
    compiled_noise = [re.compile(p, re.IGNORECASE) for p in noise_patterns]
    
    # Track if we've found the main content
    found_content = False
    content_markers = [
        'Bank Secrecy Act',
        'FinCEN',
        'Financial Crimes',
        'Anti-Money Laundering',
        'BSA',
        'CFR',
        'USC',
        '§',
        'regulation',
        'compliance',
        'requirement',
    ]
    
    for line in lines:
        line = line.strip()
        
        # Strip any remaining HTML tags
        line = re.sub(r'<[^>]+>', '', line).strip()
        
        # Skip empty lines at the start
        if not line:
            if found_content and clean_lines and clean_lines[-1] != '':
                clean_lines.append('')
            continue
        
        # Skip lines matching noise patterns
        if any(p.search(line) for p in compiled_noise):
            continue
        
        # Skip very long lines without spaces (likely minified JS)
        if len(line) > 200 and line.count(' ') < 10:
            continue
        
        # Skip lines that are mostly special characters
        alpha_ratio = sum(1 for c in line if c.isalpha()) / max(len(line), 1)
        if alpha_ratio < 0.3 and len(line) > 20:
            continue
        
        # Check for content markers
        if any(marker.lower() in line.lower() for marker in content_markers):
            found_content = True
        
        # Accept lines that look like real content
        if len(line) > 30 or found_content:
            clean_lines.append(line)
            found_content = True
    
    text = '\n'.join(clean_lines)
    
    # Remove duplicate blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Add header
    header = f"# {filename.replace('.txt', '').replace('_', ' ').title()}\n"
    header += f"Source: Cleaned from browser text dump\n"
    header += f"Original file: {filename}\n"
    header += "---\n\n"
    
    return header + text.strip()


def extract_cfr_content(content: str) -> Optional[str]:
    """Extract CFR regulation text from law.cornell.edu HTML."""
    # Try to find the main content section
    patterns = [
        # LII CFR content pattern
        r'<div[^>]*class="[^"]*field-content[^"]*"[^>]*>(.*?)</div>',
        # Main body content
        r'<div[^>]*id="[^"]*content[^"]*"[^>]*>(.*?)</div>',
        # Article content
        r'<article[^>]*>(.*?)</article>',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None


def clean_cornell_law(content: str, filename: str) -> str:
    """Clean law.cornell.edu scraped content (browser text dumps)."""
    
    # Extract just the regulatory text using markers
    lines = content.split('\n')
    clean_lines = []
    
    # Patterns to identify regulatory content
    cfr_content_patterns = [
        r'^\s*\(\d+\)',  # (1), (2), etc.
        r'^\s*\([a-z]\)',  # (a), (b), etc.
        r'^\s*\([ivx]+\)',  # (i), (ii), etc.
        r'^§\s*\d+',  # § 1010.100
        r'^[A-Z][a-z]+ means',  # "Account means"
        r'^For (the )?purpose(s)? of',  # "For purposes of"
        r'^The term',  # "The term"
        r'^As used in',  # "As used in"
        r'means [a-z]',  # definition text
        r'^Except as',  # "Except as provided"
        r'^Subject to',  # "Subject to"
        r'^Notwithstanding',  # "Notwithstanding"
        r'^In general\.',  # "(a) In general."
        r'^Definitions\.',  # "Definitions."
        r'^Each\s+\w+',  # "Each financial institution"
        r'^No\s+\w+\s+(shall|may)',  # "No person shall"
        r'^A\s+\w+\s+(shall|must|may)',  # "A person shall"
        r'^Any\s+\w+',  # "Any person"
        r'shall (be|file|report|maintain|keep)',
        r'must (be|file|report|maintain|keep)',
        r'is required to',
    ]
    compiled_cfr = [re.compile(p, re.IGNORECASE) for p in cfr_content_patterns]
    
    # Noise patterns specific to Cornell
    noise_patterns = [
        r'googletag',
        r'adsbygoogle',
        r'SEARCH_URL',
        r'window\.',
        r'function\s*\(',
        r'\{.*@type.*\}',  # JSON-LD
        r'schema\.org',
        r'Toggle navigation',
        r'navbar',
        r'dropdown',
        r'btn btn-',
        r'form-control',
        r'aria-label',
        r'aria-expanded',
        r'aria-haspopup',
        r'aria-hidden',
        r'data-toggle',
        r'data-directive',
        r'data-crosslink',
        r'data-track',
        r'class=',
        r'href=',
        r'onclick=',
        r'img-responsive',
        r'glyphicon',
        r'cornell\.edu',
        r'Please help us improve',
        r'No thank you',
        r'Support Us',
        r'Donate',
        r'Search',
        r'Enter.*terms',
        r'Who We Are',
        r'Who Pays',
        r'Contact Us',
        r'law\</',  # HTML tag remnants
        r'^LII$',
        r'^e-CFR$',
        r'^CFR$',
        r'Legal Information Institute',
        r'Electronic Code of Federal Regulations',
        r'Cornell Law',
        r'Cornell University',
        r'img class',
        r'img width',
        r'alt=',
        r'src=',
        r'https?://',
        r'\.push\(',
        r'\.cmd',
        r'enableServices',
        r'enable_page_level_ads',
        r'eval\(',
        r'var\s+\w+\s*=',
        r'var \$elem',
        r'if\s*\(\s*width',
        r'return defs',
        r'else\s*\{',
        r'makeDefs',
        r'pubads',
        r'singleRequest',
        r'^\s*\{$',
        r'^\s*\};?$',
        r'^\s*\)$',
        r'^gads\.',
        r'^node\.parentNode',
        r'role="menuitem"',
        r'insertBefore',
        r'ui_508_compliant',
        r'login:',
        r'publid:',
        r'^style=',
        r'margin-bottom',
        r'margin-top',
        r'^\." />',  # HTML remnants
        r'^/>',
        r'div data-directive',
        r'jQuery\(',
    ]
    compiled_noise = [re.compile(p, re.IGNORECASE) for p in noise_patterns]
    
    # Additional exact match noise lines
    exact_noise = {
        'skip to main content',
        'lii',
        'e-cfr',
        'cfr',
        'federal rules of appellate procedure',
        'federal rules of civil procedure',
        'federal rules of criminal procedure',
        'federal rules of evidence',
        'federal rules of bankruptcy procedure',
        'join lawyer directory',
        'law about... articles from wex',
        'table of popular names',
        'parallel table of authorities',
    }
    
    # Find section title from content
    title_patterns = [
        r'§\s*([\d.]+)\s*[-–—]\s*([^|<\n]+)',  # § 1010.100 - General definitions
        r'(\d+)\s+U\.?S\.?C\.?\s*§?\s*(\d+)',  # 31 USC 5311
    ]
    section_title = filename.replace('.txt', '').replace('_', ' ')
    for pattern in title_patterns:
        match = re.search(pattern, content)
        if match:
            section_title = match.group(0).strip()
            break
    
    in_content = False
    
    for line in lines:
        line = line.strip()
        
        # Strip HTML tags
        line = re.sub(r'<[^>]+>', ' ', line)
        line = re.sub(r'&[a-z]+;', ' ', line)  # HTML entities
        line = re.sub(r'\s+', ' ', line).strip()
        
        if not line:
            if in_content and clean_lines and clean_lines[-1] != '':
                clean_lines.append('')
            continue
        
        # Skip exact noise matches
        if line.lower() in exact_noise:
            continue
        
        # Skip noise
        if any(p.search(line) for p in compiled_noise):
            continue
        
        # Skip short non-content lines
        if len(line) < 20 and not any(p.match(line) for p in compiled_cfr):
            continue
        
        # Check for CFR content markers
        if any(p.search(line) for p in compiled_cfr):
            in_content = True
        
        # Check if line looks like real regulatory text
        if in_content or (len(line) > 80 and line[0].isupper()):
            # Additional validation - must have reasonable alpha ratio
            alpha_ratio = sum(1 for c in line if c.isalpha()) / max(len(line), 1)
            if alpha_ratio > 0.5:
                clean_lines.append(line)
                in_content = True
    
    text = '\n'.join(clean_lines)
    
    # Post-processing: remove any remaining noise lines
    post_noise = [
        r'^\.?" />',
        r'^us improve our site!',
        r'^data_track_\w+:',
        r'^publid:',
        r'^login:',
        r'^ui_\d+_compliant:',
        r'^\s*(true|false),?\s*$',
        r'^gations for reports.*\." />',
    ]
    for pattern in post_noise:
        text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)
    
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Build header
    header = f"# {section_title}\n"
    header += f"Source: law.cornell.edu (cleaned)\n"
    header += f"Original file: {filename}\n"
    header += "---\n\n"
    
    return header + text.strip()


def clean_federal_register(content: str, filename: str) -> str:
    """Clean Federal Register HTML content."""
    # Federal Register has specific markers
    parser = TextExtractor()
    try:
        parser.feed(content)
        text = parser.get_text()
    except:
        text = re.sub(r'<[^>]+>', ' ', content)
    
    # Clean up
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    header = f"# {filename}\n"
    header += "Source: Federal Register (cleaned)\n"
    header += "---\n\n"
    
    return header + text


def clean_montana_sos(content: str, filename: str) -> str:
    """Clean Montana SOS content - usually already clean."""
    # These are typically form instructions, mostly clean
    # Just ensure proper markdown formatting
    
    if not is_html_contaminated(content):
        return content  # Already clean
    
    parser = TextExtractor()
    try:
        parser.feed(content)
        text = parser.get_text()
    except:
        text = re.sub(r'<[^>]+>', ' ', content)
    
    return text.strip()


def clean_fincen_content(content: str, filename: str) -> str:
    """Clean FinCEN content - handle browser text dumps."""
    if not is_html_contaminated(content):
        return content  # Already clean
    
    # Use browser text dump cleaner for FinCEN pages
    return clean_browser_text_dump(content, filename)


def clean_file(filepath: Path) -> tuple[bool, str]:
    """
    Clean a KB file.
    
    Returns:
        Tuple of (was_modified, cleaned_content)
    """
    content = filepath.read_text(encoding='utf-8', errors='replace')
    filename = filepath.name
    
    if not is_html_contaminated(content):
        return False, content
    
    # Route to appropriate cleaner based on filename patterns
    if any(x in filename for x in ['cfr', 'usc', '31_']):
        cleaned = clean_cornell_law(content, filename)
    elif 'federal_register' in filename.lower():
        cleaned = clean_federal_register(content, filename)
    elif filename.startswith('mt_'):
        cleaned = clean_montana_sos(content, filename)
    elif 'fincen' in filename.lower():
        cleaned = clean_fincen_content(content, filename)
    elif 'ofac' in filename.lower():
        cleaned = clean_fincen_content(content, filename)  # Similar structure
    else:
        # Generic HTML cleaning
        parser = TextExtractor()
        try:
            parser.feed(content)
            cleaned = parser.get_text()
        except:
            cleaned = re.sub(r'<[^>]+>', ' ', content)
        
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        cleaned = cleaned.strip()
    
    # Verify we got meaningful content
    if len(cleaned) < 100:
        print(f"  WARNING: Cleaned content very short ({len(cleaned)} chars), keeping original")
        return False, content
    
    return True, cleaned


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Clean KB files from HTML contamination')
    parser.add_argument('kb_dir', type=Path, help='Path to knowledge_base directory')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be cleaned without modifying')
    parser.add_argument('--backup', action='store_true', help='Create .bak files before cleaning')
    
    args = parser.parse_args()
    
    if not args.kb_dir.exists():
        print(f"ERROR: Directory not found: {args.kb_dir}")
        sys.exit(1)
    
    # Find all txt files (most likely to be HTML contaminated)
    files = list(args.kb_dir.glob('*.txt')) + list(args.kb_dir.glob('*.md'))
    
    print(f"Scanning {len(files)} files in {args.kb_dir}...\n")
    
    cleaned_count = 0
    skipped_count = 0
    
    for filepath in sorted(files):
        was_modified, cleaned_content = clean_file(filepath)
        
        if was_modified:
            cleaned_count += 1
            original_size = filepath.stat().st_size
            new_size = len(cleaned_content.encode('utf-8'))
            reduction = (1 - new_size/original_size) * 100 if original_size > 0 else 0
            
            print(f"✓ {filepath.name}")
            print(f"  {original_size:,} → {new_size:,} bytes ({reduction:.1f}% reduction)")
            
            if not args.dry_run:
                if args.backup:
                    backup_path = filepath.with_suffix(filepath.suffix + '.bak')
                    filepath.rename(backup_path)
                    print(f"  Backup: {backup_path.name}")
                
                filepath.write_text(cleaned_content, encoding='utf-8')
        else:
            skipped_count += 1
            print(f"- {filepath.name} (already clean)")
    
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Files cleaned: {cleaned_count}")
    print(f"  Files skipped: {skipped_count}")
    if args.dry_run:
        print(f"\n  (Dry run - no files were modified)")


if __name__ == '__main__':
    main()
