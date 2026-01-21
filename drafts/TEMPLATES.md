# Sails.to Template System

Single source of truth for headers, footers, and other reusable components.

## Quick Start

### Option 1: Dynamic Loading (Development)

Add placeholders to your HTML and include the components script:

```html
<body>
    <!-- Header placeholder -->
    <div id="site-header"></div>

    <!-- Your page content -->
    <main>...</main>

    <!-- Footer placeholder -->
    <div id="site-footer"></div>

    <!-- Load components -->
    <script src="assets/js/components.js"></script>
</body>
```

### Option 2: Static Build (Production)

Bake templates directly into HTML files:

```bash
# Using Python
python3 build-templates.py

# Using Node.js
node build-templates.js
```

## Template Files

Located in `assets/templates/`:

| File | Description |
|------|-------------|
| `header.html` | Main navigation bar |
| `footer.html` | Site footer with links |
| `_page-template.html` | Starter template for new pages |

## Path Handling

Templates use `{{ROOT}}` placeholder for paths, which automatically resolves to:

| Page Location | `{{ROOT}}` Value |
|--------------|------------------|
| `/index.html` | `` (empty) |
| `/company/about.html` | `../` |
| `/knowledge/blog/post.html` | `../../` |

## Creating New Pages

1. Copy `assets/templates/_page-template.html` to your desired location
2. Update the `<title>`, meta tags, and content
3. The header/footer will load automatically

## Dark Navigation

For pages with dark hero sections, add `data-nav-dark="true"` to the body:

```html
<body data-nav-dark="true">
```

The nav will automatically switch to light text on scroll.

## Build Commands

```bash
# Process all files
python3 build-templates.py

# Process specific file
python3 build-templates.py company/about.html

# List files without processing
python3 build-templates.py --list

# Convert back to placeholders (for development)
python3 build-templates.py --reverse
```

## Events (Dynamic Loading)

When using `components.js`, you can hook into the load event:

```javascript
document.addEventListener('componentsLoaded', function(e) {
    console.log('Header loaded:', e.detail.header);
    console.log('Footer loaded:', e.detail.footer);
    // Initialize your page code here
});
```

## Modifying Templates

1. Edit files in `assets/templates/`
2. For dynamic loading: Changes apply immediately on page refresh
3. For static builds: Re-run the build script

## File Structure

```
drafts/
├── assets/
│   ├── js/
│   │   ├── components.js      # Dynamic loader
│   │   └── glossary.js        # Tooltip system
│   └── templates/
│       ├── header.html        # Nav template
│       ├── footer.html        # Footer template
│       └── _page-template.html # Starter template
├── build-templates.js         # Node.js build script
├── build-templates.py         # Python build script
└── TEMPLATES.md               # This file
```
