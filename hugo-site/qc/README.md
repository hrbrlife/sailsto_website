# Sails.to QC Suite

Comprehensive quality control validators for the Hugo site.

## Quick Start

```bash
# Run all validators
node qc/run.js

# Run specific validator(s)
node qc/run.js glossary
node qc/run.js links
node qc/run.js images
node qc/run.js glossary links

# Show help
node qc/run.js --help
```

## Validators

### 📚 Glossary Validation (`glossary`)

Ensures consistency between glossary terms, definitions, and usage:

- **CHECK 1**: All `data-term="..."` values have definitions in `glossary.json`
- **CHECK 2**: All definitions in `glossary.json` have corresponding glossary pages
- **CHECK 3**: All glossary pages have JSON definitions
- **CHECK 4**: Reports orphaned definitions (defined but never used)

### 🔗 Link Validation (`links`)

Validates all internal links point to real content:

- **CHECK 1**: All `href="/..."` page links resolve to existing content
- **CHECK 2**: All `src="/..."` static resources exist in `static/`
- Handles query strings and anchor links correctly
- Scans both content (`.md`) and layout (`.html`) files

### 🖼️ Image Validation (`images`)

Checks image references and accessibility:

- **CHECK 1**: All image `src` references point to existing files
- **CHECK 2**: All `<img>` tags have `alt` text for accessibility
- **CHECK 3**: Reports potentially unused images in `static/`

## Exit Codes

- `0` — All checks passed (warnings are OK)
- `1` — One or more checks failed with errors

## Options

```bash
--quiet     # Suppress detailed output (summary only)
--strict    # Treat warnings as errors (exit 1 if any warnings)
```

## Integration

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
cd hugo-site
node qc/run.js --quiet || exit 1
```

### CI/CD

```yaml
# GitHub Actions example
- name: Run QC Suite
  run: |
    cd hugo-site
    node qc/run.js
```

### NPM Script

Add to `package.json`:

```json
{
  "scripts": {
    "qc": "node qc/run.js",
    "qc:glossary": "node qc/run.js glossary",
    "qc:links": "node qc/run.js links",
    "qc:images": "node qc/run.js images"
  }
}
```

## Adding New Validators

1. Create `qc/validate-{name}.js` with a `validate{Name}()` function
2. Return `{ success: boolean, errors: number, warnings: number }`
3. Add to `VALIDATORS` object in `qc/run.js`

Example template:

```javascript
function validateExample() {
    // ... validation logic ...
    return { 
        success: errors === 0, 
        errors, 
        warnings 
    };
}

module.exports = { validateExample };
```

## Files

```
qc/
├── run.js              # Main orchestrator
├── validate-glossary.js # Glossary term validation
├── validate-links.js    # Internal link validation
├── validate-images.js   # Image reference validation
└── README.md           # This file
```
