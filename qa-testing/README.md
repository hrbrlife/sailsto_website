# Sails.to QA Testing Suite

Automated UX/UI testing for the Sails.to CrossSecurities platform using multi-agent AI analysis.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Install Playwright browsers
npm run install:browsers

# Make sure Hugo dev server is running
cd ../hugo-site && hugo server -D &

# Run website analysis (default: critical + high priority pages)
npm run analyze

# Quick check (critical pages only)
npm run analyze -- --quick

# Full analysis (all tiers)
npm run analyze -- --full
```

## 🤖 Multi-Agent System

Two specialized AI agents analyze each page:

| Agent | Focus Areas |
|-------|-------------|
| 🎯 **UX Agent** | Trust & credibility, value proposition clarity, navigation, conversion path, mobile experience |
| 🎨 **UI Agent** | Visual hierarchy, design consistency, professional polish, whitespace, responsive quality |

### Models (via OpenRouter)

| Model | Best For |
|-------|----------|
| `deepseek/deepseek-r1t2-chimera` | **Default** - Strong reasoning, detailed analysis |
| `mistralai/devstral-2-2512` | Agentic tasks, 256K context |
| `qwen/qwen3-coder-480b-a35b` | Tool use, function calling |

## 📋 Scripts

| Command | Description |
|---------|-------------|
| `npm run analyze` | Analyze critical + high priority pages (10 pages) |
| `npm run analyze -- --quick` | Quick check - critical pages only (5 pages) |
| `npm run analyze -- --full` | Comprehensive - includes knowledge base (20+ pages) |
| `npm run analyze -- --all` | Everything including samples (25+ pages) |
| `npm run analyze:headless` | Run in headless mode (no browser window) |
| `npm run test` | Crawl site and capture screenshots |
| `npm run full-audit` | Run crawl + collages + review + report |

## 🎯 Page Tiers

Pages are organized by priority for testing:

### Tier 1: Critical (5 pages)
- Homepage, For Issuers, For Investors, Pricing, Signup

### Tier 2: High (5 pages)
- For Brokers, For Institutions, Introducers, How It Works, Issuers Directory

### Tier 3: Trust (7 pages)
- Security, Compliance, Oversight, Company Index, About, Contact, Legal

### Tier 4: Knowledge (8 pages)
- Knowledge Hub, FAQ, Roadmap, Glossary Index, Blog Index, Docs Index, Guides Index, Getting Started Guide

### Tier 5: Samples (11 pages)
- Sample glossary terms (CrossSecurities, Tokenization, Wyoming DAO, Security Token, ISIN, KYC)
- Sample blog posts (Security Tokens, Why Wyoming, Future of Tokenization)
- Sample docs (Platform Overview, Getting Started)

### Tier 6: Extended (17 pages)
- Additional glossary, blog, and docs pages for comprehensive audit

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```bash
# Required for AI analysis
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Model selection (optional)
OPENROUTER_MODEL=deepseek/deepseek-r1t2-chimera

# Site URL (optional, defaults to localhost:1313)
BASE_URL=http://localhost:1313

# Browser mode (optional)
HEADLESS=true

# Viewport: desktop, tablet, or mobile (optional)
VIEWPORT=desktop
```

### Get an API Key

1. Go to https://openrouter.ai/keys
2. Create a free account
3. Generate an API key
4. Add to `.env` file

## 📊 Output

After running analysis:

| File | Description |
|------|-------------|
| `WEBSITE_ANALYSIS_REPORT.md` | Full markdown report with scores, issues, and recommendations |
| `website-analysis.json` | Machine-readable JSON with all data |
| `screenshots/website-analysis/*.png` | Full-page screenshots of each analyzed page |

## 🎨 Scoring Rubric

Both agents use a 1-10 scale:

| Score | Meaning |
|-------|---------|
| 9-10 | Exceptional - Would convert skeptical finance professionals |
| 7-8 | Good - Works well, minor polish needed |
| 5-6 | Adequate - Gets the job done but not compelling |
| 3-4 | Needs Work - Confusing or unprofessional elements |
| 1-2 | Poor - Would erode trust or confuse visitors |

## 📁 Directory Structure

```
qa-testing/
├── .env                          # API key and config
├── .env.example                  # Template for .env
├── package.json                  # Dependencies and scripts
├── website-analyzer.js           # Main multi-agent analyzer
├── crawler.js                    # Screenshot crawler
├── agent-review.js               # Single-agent review
├── generate-collages.js          # Collage generator
├── generate-report.js            # HTML report generator
├── UX_STYLE_GUIDE.md            # UX standards reference
├── WEBSITE_ANALYSIS_REPORT.md   # Generated analysis report
├── website-analysis.json        # Generated JSON data
└── screenshots/
    └── website-analysis/        # Page screenshots
```

## 🔧 Advanced Usage

### Mobile Testing
```bash
VIEWPORT=mobile npm run analyze -- --quick
```

### Different Model
```bash
OPENROUTER_MODEL=mistralai/devstral-2-2512 npm run analyze
```

### Visible Browser (Debug)
```bash
HEADLESS=false npm run analyze -- --quick
```

### Production Site
```bash
BASE_URL=https://sails.to npm run analyze -- --quick
```
