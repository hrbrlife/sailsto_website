#!/bin/bash
# Sails.to Deployment Script
# Builds Hugo site and deploys to both GitHub and Sandstorm hosting
# Generates version.json from git for cache busting and version tracking

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HUGO_DIR="$SCRIPT_DIR/hugo-site"
DEPLOY_DIR="$SCRIPT_DIR/sailsto-deploy"
DEPLOY_REMOTE="${DEPLOY_REMOTE:-}" # Set via environment variable, e.g. export DEPLOY_REMOTE="https://user@host/"

echo "🚀 Sails.to Deploy Script"
echo "========================="

# Step 0: Generate version.json from git
echo ""
echo "🔖 Generating version info..."
cd "$SCRIPT_DIR"

GIT_HASH=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
GIT_HASH_SHORT=$(git rev-parse --short HEAD 2>/dev/null || echo "dev")
GIT_DATE=$(git log -1 --format=%cI 2>/dev/null || date -Iseconds)
GIT_MSG=$(git log -1 --format=%s 2>/dev/null | sed 's/"/\\"/g' || echo "no message")
GIT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
BUILD_NUM=$(git rev-list --count HEAD 2>/dev/null || echo "0")

cat > "$HUGO_DIR/data/version.json" << VEOF
{
  "hash": "${GIT_HASH}",
  "hashShort": "${GIT_HASH_SHORT}",
  "date": "${GIT_DATE}",
  "message": "${GIT_MSG}",
  "tag": "${GIT_TAG}",
  "buildNumber": ${BUILD_NUM}
}
VEOF

echo "  Commit: ${GIT_HASH_SHORT} (build #${BUILD_NUM})"
echo "  Date:   ${GIT_DATE}"
echo "  Tag:    ${GIT_TAG:-none}"
echo "✅ Version info generated"

# Step 1: Build Hugo site
echo ""
echo "📦 Building Hugo site..."
cd "$HUGO_DIR"
hugo --gc --minify
# Remove TinaCMS admin panel (dev-only, points at localhost:4001)
rm -rf "$HUGO_DIR/public/admin"
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

# Step 5: Publish to website-publish branch (GitHub Pages)
# Uses a temp directory since hugo-site/public/ is gitignored
echo ""
echo "🌍 Publishing to website-publish branch..."
cd "$SCRIPT_DIR"
if git remote get-url origin &>/dev/null; then
    ORIGIN_URL=$(git remote get-url origin)
    TMPDIR=$(mktemp -d)
    cp -r "$HUGO_DIR/public/"* "$TMPDIR/"
    touch "$TMPDIR/.nojekyll"
    cd "$TMPDIR"
    git init -b website-publish
    git add -A
    git commit -m "Deploy: ${GIT_HASH_SHORT} build #${BUILD_NUM} — $(date '+%Y-%m-%d %H:%M')"
    git remote add origin "$ORIGIN_URL"
    git push origin website-publish --force 2>&1
    cd "$SCRIPT_DIR"
    rm -rf "$TMPDIR"
    echo "✅ Published to website-publish branch"
else
    echo "ℹ️  No GitHub remote configured. Skipping."
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Version: ${GIT_HASH_SHORT} (build #${BUILD_NUM})"
echo "Your site should be live at the Sandstorm public URL shortly."
