#!/bin/bash
# CCASH Document Conversion Script - Simplified
# Converts Markdown documents to HTML and DOCX with dynamic numbering

BASE_DIR="/home/user/CCASH/Series Docs"
OUTPUT_DIR="$BASE_DIR/OUTPUT/Converted"

# Create output directories
mkdir -p "$OUTPUT_DIR/HTML"
mkdir -p "$OUTPUT_DIR/DOCX"

echo "=== CCASH Document Conversion ==="
echo "Output: $OUTPUT_DIR"
echo ""

# Create CSS for HTML output
cat > "$OUTPUT_DIR/style.css" << 'CSSEOF'
body {
    font-family: 'Times New Roman', serif;
    font-size: 12pt;
    line-height: 1.5;
    max-width: 8.5in;
    margin: 1in auto;
    padding: 0 0.5in;
}
h1, h2, h3, h4, h5, h6 {
    font-family: Arial, sans-serif;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}
h1 { font-size: 18pt; border-bottom: 2px solid black; padding-bottom: 0.3em; }
h2 { font-size: 16pt; }
h3 { font-size: 14pt; }
h4 { font-size: 12pt; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 11pt; }
th, td { border: 1px solid black; padding: 0.4em 0.6em; text-align: left; }
th { background-color: #E6E6E6; font-weight: bold; }
code { font-family: 'Courier New', monospace; font-size: 10pt; background: #F5F5F5; padding: 0.1em 0.3em; }
pre { background: #F5F5F5; border: 1px solid #DDD; padding: 1em; overflow-x: auto; }
blockquote { margin: 1em 2em; padding-left: 1em; border-left: 3px solid #CCC; font-style: italic; }
@media print { body { margin: 0; padding: 0; max-width: none; } }
CSSEOF

# Convert function
convert() {
    local src="$1"
    local name=$(basename "$src" .md)
    local rel="${src#$BASE_DIR/}"
    local dir=$(dirname "$rel")
    
    # Skip internal directories
    [[ "$rel" == _schema/* || "$rel" == OUTPUT/* || "$rel" == scripts/* ]] && return
    
    mkdir -p "$OUTPUT_DIR/HTML/$dir"
    mkdir -p "$OUTPUT_DIR/DOCX/$dir"
    
    echo "Converting: $name"
    
    # HTML with numbered sections and TOC
    pandoc "$src" \
        --from markdown \
        --to html5 \
        --standalone \
        --number-sections \
        --toc \
        --toc-depth=3 \
        --css="style.css" \
        --metadata title="$name" \
        -o "$OUTPUT_DIR/HTML/$dir/$name.html" 2>/dev/null
    
    # DOCX with numbered sections and TOC
    pandoc "$src" \
        --from markdown \
        --to docx \
        --number-sections \
        --toc \
        --toc-depth=3 \
        -o "$OUTPUT_DIR/DOCX/$dir/$name.docx" 2>/dev/null
    
    echo "  ✓ $name.html / $name.docx"
}

# Process all markdown files
count=0
for f in $(find "$BASE_DIR" -name "*.md" -type f ! -path "*/_schema/*" ! -path "*/OUTPUT/*" ! -path "*/scripts/*" ! -path "*/.git/*" | sort); do
    convert "$f"
    ((count++))
done

echo ""
echo "=== Done: $count documents converted ==="
echo "HTML: $OUTPUT_DIR/HTML/"
echo "DOCX: $OUTPUT_DIR/DOCX/"
