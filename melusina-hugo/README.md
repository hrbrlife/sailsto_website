# Melusina OS Website

Hugo static site for [melusina-os.org](https://melusina-os.org) — migrated from React/Vite SPA to Hugo for instant load times and full SEO.

## Architecture

Same pattern as [sails.to](https://sails.to):

- **Hugo v0.139+** with data-driven templates
- **Bootstrap 5.3** compiled CSS (no runtime JS framework)
- **JSON data files** in `data/` drive all page content
- **Block partials** (`layouts/partials/blocks/`) for reusable sections
- **Per-page layouts** (`layouts/page/`) for each route
- **Full SEO**: JSON-LD schemas, OG/Twitter cards, sitemap, robots.txt
- **i18n ready**: EN + FR with hreflang tags

## Quick Start

```bash
# Dev server with drafts
hugo server -D --port 1315

# Production build
hugo --gc --minify

# Or use the interactive build script
./build.sh
```

## Structure

```
content/           # Markdown content files (frontmatter-driven)
data/              # JSON data (pages, glossary, audiences, config)
layouts/
  _default/        # baseof.html, single.html, list.html
  page/            # Per-page templates (landing, compare, plans, etc.)
  partials/        # Shared partials (head, nav, footer, blocks/)
  glossary-term/   # Glossary term detail template
  doc/             # Documentation single + list templates
static/
  css/             # Compiled main.css + page-specific CSS
  js/              # Vanilla JS (nav, page filters)
  fonts/           # Self-hosted web fonts (Inter, DM Serif Display, etc.)
i18n/              # Translation strings (en.toml, fr.toml)
```

## Pages (53 EN)

| Route | Layout | Data Source |
|-------|--------|-------------|
| `/` | index.html | `data/pages/landing.json` |
| `/use-cases/` | page/use-cases | `data/pages/use-cases.json` |
| `/compare/` | page/compare | `data/pages/compare.json` |
| `/plans/` | page/plans | `data/pages/plans.json` |
| `/roadmap/` | page/roadmap | `data/pages/roadmap.json` |
| `/faq/` | page/faq | `data/pages/faq.json` |
| `/bureau/` | page/bureau | `data/pages/bureau.json` |
| `/architecture/` | page/architecture | `data/pages/architecture.json` |
| `/company/` | page/company | `data/pages/contact.json` |
| `/knowledge-base/` | page/knowledge-base | — |
| `/for/{audience}/` | page/audience | `data/audiences.json` |
| `/glossary/` | page/glossary | `data/glossary/*.json` |
| `/glossary/{term}/` | glossary-term/single | `data/glossary/{term}.json` |
| `/docs/{slug}/` | doc/single | Markdown content |
| `/privacy/`, `/terms/` | page/legal | Markdown content |

## SEO Features

- **JSON-LD schemas**: Organization, SoftwareApplication, WebSite, WebPage, BreadcrumbList, FAQPage, Article, DefinedTerm
- **Open Graph + Twitter Cards** on every page
- **Canonical URLs** with hreflang alternates
- **Dynamic robots.txt** with AI bot rules
- **XML Sitemap** (46+ URLs)
- **Self-hosted fonts** (no external requests)
- **No JavaScript framework** — pure static HTML

## Build Performance

- **Build time**: ~200ms (53 pages)
- **Page load**: Instant (static HTML, no hydration)
- **Lighthouse**: 100 Performance target

## Design System

Cyberpunk dark theme:
- Background: `#0A0A1A` / `#0F0F23`
- Cyan accent: `#00E5FF`
- Green accent: `#00FFB2`
- Orange accent: `#FF6B35`
- Purple accent: `#9B59FF`
- Fonts: DM Serif Display (headings), Inter (body), JetBrains Mono (code), Orbitron (brand)
