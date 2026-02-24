#!/bin/bash
# Melusina OS Hugo Site - Build & Dev Script

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   Melusina OS Hugo Site Builder      ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "  1) Dev server (with drafts)"
echo "  2) Dev server (published only)"
echo "  3) Production build (minified)"
echo "  4) Production build + stats"
echo "  5) Clean build artifacts"
echo ""
read -p "  Choose [1-5]: " choice

case $choice in
  1)
    echo "🚀 Starting dev server with drafts..."
    hugo server -D --bind 0.0.0.0 --port 1315 --disableFastRender
    ;;
  2)
    echo "🚀 Starting dev server..."
    hugo server --bind 0.0.0.0 --port 1315
    ;;
  3)
    echo "📦 Building for production..."
    hugo --gc --minify
    rm -rf public/admin
    echo "✅ Build complete → public/"
    ;;
  4)
    echo "📦 Building for production..."
    hugo --gc --minify
    rm -rf public/admin
    echo ""
    echo "📊 Build Stats:"
    echo "  HTML files: $(find public -name '*.html' | wc -l)"
    echo "  CSS files:  $(find public -name '*.css'  | wc -l)"
    echo "  JS files:   $(find public -name '*.js'   | wc -l)"
    echo "  Total size: $(du -sh public | cut -f1)"
    echo "✅ Build complete → public/"
    ;;
  5)
    echo "🧹 Cleaning..."
    rm -rf public/ resources/ .hugo_build.lock
    echo "✅ Clean"
    ;;
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac
