#!/bin/bash
# Hugo Site Build and Serve Script

echo "================================"
echo "Sails.to Hugo Site Manager"
echo "================================"
echo ""

# Check if Hugo is installed
if ! command -v hugo &> /dev/null; then
    echo "❌ Hugo is not installed!"
    echo ""
    echo "Install Hugo:"
    echo "  macOS:  brew install hugo"
    echo "  Linux:  snap install hugo"
    echo "  Windows: choco install hugo-extended"
    echo ""
    echo "Or download from: https://gohugo.io/installation/"
    exit 1
fi

echo "✅ Hugo found: $(hugo version)"
echo ""

# Function to display menu
show_menu() {
    echo "What would you like to do?"
    echo ""
    echo "1) Start development server (with drafts)"
    echo "2) Start development server (published only)"
    echo "3) Build for production"
    echo "4) Build and check output"
    echo "5) Clean build directory"
    echo "6) Exit"
    echo ""
    read -p "Enter choice [1-6]: " choice
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1)
            echo ""
            echo "🚀 Starting development server with drafts..."
            echo "   Visit: http://localhost:1313"
            echo "   Press Ctrl+C to stop"
            echo ""
            hugo server -D --bind 0.0.0.0
            ;;
        2)
            echo ""
            echo "🚀 Starting development server (published only)..."
            echo "   Visit: http://localhost:1313"
            echo "   Press Ctrl+C to stop"
            echo ""
            hugo server --bind 0.0.0.0
            ;;
        3)
            echo ""
            echo "🏗️  Building for production..."
            hugo --minify
            echo ""
            echo "✅ Build complete! Output in: public/"
            echo ""
            ;;
        4)
            echo ""
            echo "🏗️  Building and checking output..."
            hugo --minify
            echo ""
            echo "📊 Build Statistics:"
            echo "   Total files: $(find public -type f | wc -l)"
            echo "   HTML files: $(find public -name "*.html" | wc -l)"
            echo "   CSS files: $(find public -name "*.css" | wc -l)"
            echo "   JS files: $(find public -name "*.js" | wc -l)"
            echo ""
            ;;
        5)
            echo ""
            echo "🧹 Cleaning build directory..."
            rm -rf public resources .hugo_build.lock
            echo "✅ Clean complete!"
            echo ""
            ;;
        6)
            echo ""
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo ""
            echo "❌ Invalid choice. Please try again."
            echo ""
            ;;
    esac
done
