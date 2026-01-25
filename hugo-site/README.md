# Sails.to Hugo Website

This is the Hugo-powered version of the Sails.to website with complete 1:1 parity with the original HTML version.

## Structure

```
hugo-site/
├── content/           # Markdown content files
├── layouts/           # HTML templates
│   ├── _default/      # Default layouts
│   └── partials/      # Reusable components (nav, footer, head)
├── static/            # Static assets (CSS, JS, images)
├── hugo.toml          # Hugo configuration
└── public/            # Generated site (after build)
```

## Development

### Prerequisites
- Hugo Extended v0.120.0 or later

### Install Hugo
```bash
# macOS
brew install hugo

# Linux
snap install hugo

# Or download from https://gohugo.io/installation/
```

### Run Development Server
```bash
cd hugo-site
hugo server -D
```

Visit: http://localhost:1313

### Build for Production
```bash
hugo --minify
```

Output will be in `public/` directory.

## Content Organization

- **Main pages**: `content/*.md` (issuers, investors, brokers, etc.)
- **Knowledge**: `content/knowledge/` (faq, roadmap, etc.)
- **Blog**: `content/blog/`
- **Glossary**: `content/glossary/`
- **Company**: `content/company/` (about, contact, legal)

## Templates

- **Navigation**: `layouts/partials/nav.html` - Single source for all page navigation
- **Footer**: `layouts/partials/footer.html` - Single source for all page footers
- **Base**: `layouts/_default/baseof.html` - Main HTML wrapper

## Benefits

1. **Single Source**: Update nav/footer once, regenerates all pages
2. **Clean Content**: Markdown files are easy to edit
3. **Fast Builds**: Hugo is extremely fast
4. **Version Control**: Better diffs in Git
5. **Consistency**: Impossible to have mismatched nav/footers

## Next Steps

1. Copy assets from `drafts/assets/` to `static/assets/`
2. Convert HTML content to Markdown
3. Test build output matches original exactly
4. Set up deployment pipeline
