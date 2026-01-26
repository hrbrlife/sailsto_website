#!/bin/bash
# Sails.to Deployment Script
# Builds Hugo site and deploys to both GitHub and Sandstorm hosting

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HUGO_DIR="$SCRIPT_DIR/hugo-site"
DEPLOY_DIR="$SCRIPT_DIR/sailsto-deploy"
DEPLOY_REMOTE="https://nzatjbqc@api-f6411e4a4942c0b80d4b7ad39af36744.melusina-os.org/"

echo "🚀 Sails.to Deploy Script"
echo "========================="

# Step 1: Build Hugo site
echo ""
echo "📦 Building Hugo site..."
cd "$HUGO_DIR"
hugo --gc --minify
echo "✅ Hugo build complete"

# Step 2: Copy built files to deploy repo
echo ""
echo "📋 Copying files to deployment repo..."
cd "$DEPLOY_DIR"

# Clean old files (except .git)
find . -maxdepth 1 ! -name '.git' ! -name '.' -exec rm -rf {} +

# Copy new files
cp -r "$HUGO_DIR/public/"* .
echo "✅ Files copied"

# Step 3: Commit and push to Sandstorm (gw-pages)
echo ""
echo "🌐 Deploying to Sandstorm hosting..."
git add -A
if git diff --staged --quiet; then
    echo "ℹ️  No changes to deploy"
else
    COMMIT_MSG="Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "$COMMIT_MSG"
    git push -u origin gw-pages 2>&1
    echo "✅ Deployed to Sandstorm"
fi

# Step 4: Push main repo to GitHub (if configured)
echo ""
echo "📤 Pushing to GitHub..."
cd "$SCRIPT_DIR"
if git remote get-url origin &>/dev/null; then
    # Check if there are changes to commit
    if ! git diff --quiet || ! git diff --staged --quiet; then
        echo "⚠️  You have uncommitted changes. Please commit first."
    else
        git push origin main 2>&1 || git push origin master 2>&1 || echo "ℹ️  No GitHub remote or branch configured"
    fi
    echo "✅ GitHub push complete"
else
    echo "ℹ️  No GitHub remote configured. Skipping."
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Your site should be live at the Sandstorm public URL shortly."
