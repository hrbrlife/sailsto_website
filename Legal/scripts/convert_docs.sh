#!/bin/bash
# CCASH Document Conversion Script
# Converts Markdown documents to HTML and DOCX with dynamic numbering
# Output styled like LibreOffice

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$BASE_DIR/OUTPUT/Converted"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create output directories
mkdir -p "$OUTPUT_DIR/HTML"
mkdir -p "$OUTPUT_DIR/DOCX"

echo "=== CCASH Document Conversion ==="
echo "Base directory: $BASE_DIR"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Create reference DOCX for LibreOffice-style formatting
create_reference_docx() {
    echo "Creating reference document for styling..."
    
    # We'll use Pandoc's default and customize via lua filter
    cat > "$OUTPUT_DIR/reference.docx.yaml" << 'EOF'
# Reference document settings (Pandoc will use defaults)
# For custom styling, generate with: pandoc -o reference.docx --print-default-data-file reference.docx
EOF
}

# Create Lua filter for dynamic numbering
create_lua_filter() {
    cat > "$OUTPUT_DIR/number-sections.lua" << 'LUAEOF'
-- Lua filter to add dynamic section numbering
-- Mimics LibreOffice outline numbering

local heading_counts = {0, 0, 0, 0, 0, 0}

function Header(el)
    local level = el.level
    
    -- Reset lower level counters
    for i = level + 1, 6 do
        heading_counts[i] = 0
    end
    
    -- Increment current level
    heading_counts[level] = heading_counts[level] + 1
    
    -- Build number string
    local num_parts = {}
    for i = 1, level do
        table.insert(num_parts, tostring(heading_counts[i]))
    end
    local num_str = table.concat(num_parts, ".")
    
    -- Don't number if heading starts with specific patterns
    local text = pandoc.utils.stringify(el.content)
    if text:match("^VERSION") or text:match("^SIGNATURE") or text:match("^EXHIBIT") then
        return el
    end
    
    -- Prepend number to heading
    local number = pandoc.Str(num_str .. " ")
    table.insert(el.content, 1, number)
    
    return el
end
LUAEOF
}

# Create CSS for HTML output (LibreOffice-like styling)
create_html_css() {
    cat > "$OUTPUT_DIR/libreoffice-style.css" << 'CSSEOF'
/* LibreOffice-style CSS for CCASH Documents */

@import url('https://fonts.googleapis.com/css2?family=Liberation+Serif&family=Liberation+Sans&display=swap');

:root {
    --text-color: #000000;
    --heading-color: #000000;
    --link-color: #0000EE;
    --border-color: #000000;
    --table-header-bg: #E6E6E6;
    --code-bg: #F5F5F5;
}

body {
    font-family: 'Liberation Serif', 'Times New Roman', serif;
    font-size: 12pt;
    line-height: 1.5;
    color: var(--text-color);
    max-width: 8.5in;
    margin: 1in auto;
    padding: 0 0.5in;
    background: white;
}

/* Headings - LibreOffice default outline numbering style */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Liberation Sans', 'Arial', sans-serif;
    color: var(--heading-color);
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    page-break-after: avoid;
}

h1 {
    font-size: 18pt;
    font-weight: bold;
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 0.3em;
}

h2 {
    font-size: 16pt;
    font-weight: bold;
}

h3 {
    font-size: 14pt;
    font-weight: bold;
}

h4 {
    font-size: 12pt;
    font-weight: bold;
}

h5, h6 {
    font-size: 12pt;
    font-weight: normal;
    font-style: italic;
}

/* Paragraphs */
p {
    margin: 0.5em 0;
    text-align: justify;
}

/* Lists - indented like LibreOffice */
ul, ol {
    margin: 0.5em 0;
    padding-left: 2em;
}

li {
    margin: 0.25em 0;
}

/* Nested lists */
ul ul, ol ol, ul ol, ol ul {
    margin: 0.25em 0;
}

/* Tables - LibreOffice default table style */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 11pt;
}

th, td {
    border: 1px solid var(--border-color);
    padding: 0.4em 0.6em;
    text-align: left;
    vertical-align: top;
}

th {
    background-color: var(--table-header-bg);
    font-weight: bold;
}

tr:nth-child(even) {
    background-color: #FAFAFA;
}

/* Code blocks */
code {
    font-family: 'Liberation Mono', 'Courier New', monospace;
    font-size: 10pt;
    background-color: var(--code-bg);
    padding: 0.1em 0.3em;
    border-radius: 2px;
}

pre {
    background-color: var(--code-bg);
    border: 1px solid #DDDDDD;
    padding: 1em;
    overflow-x: auto;
    font-size: 10pt;
    line-height: 1.4;
}

pre code {
    background: none;
    padding: 0;
}

/* Block quotes */
blockquote {
    margin: 1em 2em;
    padding-left: 1em;
    border-left: 3px solid #CCCCCC;
    color: #333333;
    font-style: italic;
}

/* Links */
a {
    color: var(--link-color);
    text-decoration: underline;
}

/* Horizontal rules */
hr {
    border: none;
    border-top: 1px solid var(--border-color);
    margin: 2em 0;
}

/* Definition lists */
dt {
    font-weight: bold;
    margin-top: 0.5em;
}

dd {
    margin-left: 2em;
    margin-bottom: 0.5em;
}

/* Print styles */
@media print {
    body {
        margin: 0;
        padding: 0;
        max-width: none;
    }
    
    h1, h2, h3 {
        page-break-after: avoid;
    }
    
    table, figure {
        page-break-inside: avoid;
    }
    
    a {
        color: var(--text-color);
        text-decoration: none;
    }
    
    a[href^="http"]:after {
        content: " (" attr(href) ")";
        font-size: 9pt;
        color: #666666;
    }
}

/* Document metadata header (schema comments become invisible) */
.comment {
    display: none;
}

/* Version history tables */
table:first-of-type {
    font-size: 10pt;
}

/* Signature blocks */
.signature {
    margin-top: 3em;
    page-break-inside: avoid;
}
CSSEOF
}

# Convert a single markdown file
convert_file() {
    local input_file="$1"
    local filename=$(basename "$input_file" .md)
    local rel_path="${input_file#$BASE_DIR/}"
    
    echo "Converting: $rel_path"
    
    # Skip schema and output directories
    if [[ "$rel_path" == _schema/* ]] || [[ "$rel_path" == OUTPUT/* ]] || [[ "$rel_path" == scripts/* ]]; then
        echo "  Skipping (schema/output/scripts)"
        return
    fi
    
    # Create subdirectory structure in output
    local subdir=$(dirname "$rel_path")
    mkdir -p "$OUTPUT_DIR/HTML/$subdir"
    mkdir -p "$OUTPUT_DIR/DOCX/$subdir"
    
    # Convert to HTML with CSS styling and section numbering
    pandoc "$input_file" \
        --from markdown \
        --to html5 \
        --standalone \
        --number-sections \
        --toc \
        --toc-depth=3 \
        --css="../../libreoffice-style.css" \
        --metadata title="$filename" \
        --lua-filter="$OUTPUT_DIR/number-sections.lua" \
        -o "$OUTPUT_DIR/HTML/$subdir/$filename.html" 2>/dev/null || {
            # Fallback without lua filter if it fails
            pandoc "$input_file" \
                --from markdown \
                --to html5 \
                --standalone \
                --number-sections \
                --toc \
                --toc-depth=3 \
                --css="../../libreoffice-style.css" \
                --metadata title="$filename" \
                -o "$OUTPUT_DIR/HTML/$subdir/$filename.html"
        }
    
    # Convert to DOCX with dynamic numbering
    pandoc "$input_file" \
        --from markdown \
        --to docx \
        --number-sections \
        --toc \
        --toc-depth=3 \
        --lua-filter="$OUTPUT_DIR/number-sections.lua" \
        -o "$OUTPUT_DIR/DOCX/$subdir/$filename.docx" 2>/dev/null || {
            # Fallback without lua filter if it fails
            pandoc "$input_file" \
                --from markdown \
                --to docx \
                --number-sections \
                --toc \
                --toc-depth=3 \
                -o "$OUTPUT_DIR/DOCX/$subdir/$filename.docx"
        }
    
    echo "  ✓ HTML: $OUTPUT_DIR/HTML/$subdir/$filename.html"
    echo "  ✓ DOCX: $OUTPUT_DIR/DOCX/$subdir/$filename.docx"
}

# Main conversion
main() {
    echo "Setting up conversion environment..."
    create_html_css
    create_lua_filter
    
    echo ""
    echo "Finding markdown documents..."
    
    local count=0
    
    # Find all markdown files (excluding schema, output, scripts)
    while IFS= read -r -d '' file; do
        convert_file "$file"
        ((count++))
    done < <(find "$BASE_DIR" -name "*.md" -type f \
        ! -path "*/_schema/*" \
        ! -path "*/OUTPUT/*" \
        ! -path "*/scripts/*" \
        ! -path "*/.git/*" \
        -print0 | sort -z)
    
    echo ""
    echo "=== Conversion Complete ==="
    echo "Documents converted: $count"
    echo ""
    echo "Output locations:"
    echo "  HTML: $OUTPUT_DIR/HTML/"
    echo "  DOCX: $OUTPUT_DIR/DOCX/"
    echo ""
    echo "To open in LibreOffice:"
    echo "  libreoffice $OUTPUT_DIR/DOCX/Company/Governance/B1_Master_Operating_Agreement.docx"
}

# Run with optional single file argument
if [ -n "$1" ]; then
    create_html_css
    create_lua_filter
    convert_file "$1"
else
    main
fi
