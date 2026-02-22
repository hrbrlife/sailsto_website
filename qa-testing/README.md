# QA Council — Multi-Agent Website Testing Suite

A panel of 7 AI expert agents reviews your website from different perspectives,
then convenes a council to produce a unified, prioritized HTML report.

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                  Playwright Crawler                   │
│  Visits every page at desktop + mobile viewports      │
│  Captures: screenshots, console logs, meta tags,      │
│  network errors, page text, broken images              │
└──────────────────┬───────────────────────────────────┘
                   │ crawl_data.json
                   ▼
┌──────────────────────────────────────────────────────┐
│              Expert Agent Panel (parallel)             │
│                                                        │
│  🔒 Legal          — GDPR, privacy, compliance         │
│  🔄 Consistency    — terminology, tone, messaging      │
│  ✍️  Editorial      — Made to Stick, jargon, clarity    │
│  🎯 Principles     — core identity, dinner test        │
│  📱 Mobile UX      — touch, readability, layout        │
│  🖥️  Desktop UX     — hierarchy, CTAs, 5-second test    │
│  🔍 SEO            — meta, headers, performance        │
└──────────────────┬───────────────────────────────────┘
                   │ 7 expert reports
                   ▼
┌──────────────────────────────────────────────────────┐
│                   QA Council Chair                     │
│  Reads all reports, resolves conflicts, prioritizes    │
│  Produces: grade, decisions, quick wins, themes        │
└──────────────────┬───────────────────────────────────┘
                   │ council report
                   ▼
┌──────────────────────────────────────────────────────┐
│               HTML Report Generator                    │
│  Beautiful dark-themed report with:                    │
│  - Overall grade + stats                              │
│  - Executive summary                                  │
│  - Prioritized decisions (P0/P1/P2)                   │
│  - Per-expert findings with screenshots               │
│  - Issue cards with severity badges                   │
└──────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Set your OpenRouter API key
export OPENROUTER_API_KEY="sk-or-..."

# 2. Full run: crawl + agents + report
make run

# Or step-by-step:
make crawl          # Just crawl (no API key needed)
make agents         # Run agents on saved crawl data
```

## Files

| File | Purpose |
|------|---------|
| `run.py` | Main orchestrator — CLI entry point |
| `crawler.py` | Playwright crawler — screenshots, console logs, meta tags |
| `agents.py` | 7 expert agents + council agent (Pydantic AI + OpenRouter) |
| `models.py` | Pydantic models for all agent outputs |
| `report_generator.py` | HTML report with embedded screenshots |
| `config.py` | Sites, viewports, model, paths |

## Commands

```bash
python run.py                    # Full run
python run.py --crawl-only       # Just crawl, save data
python run.py --agents-only      # Skip crawl, use saved data
python run.py --site melusina-os # Run for specific site
```

## Adding Sites

Edit `config.py`:

```python
SITES = {
    "melusina-os": {
        "base_url": "https://melusina-os.org",
        "pages": ["/en", "/en/use-cases", ...],
    },
    "kyclat": {
        "base_url": "https://kyclat.com",
        "pages": ["/en", "/en/pricing", ...],
    },
}
```

## Changing the AI Model

Edit `config.py`:

```python
MODEL = "anthropic/claude-sonnet-4"     # default
MODEL = "google/gemini-2.5-pro"           # alternative
MODEL = "openai/gpt-4o"                   # another option
```

## Output Structure

```
reports/
├── qa-report-melusina-os-latest.html   ← open this
├── qa-report-melusina-os-20260222.html
├── council-melusina-os.json
├── screenshots/
│   └── melusina-os/
│       ├── desktop/          ← full-page screenshots
│       └── mobile/
├── crawl_data/
│   └── melusina-os.json      ← raw crawl data
└── experts/
    └── melusina-os/
        ├── legal.json
        ├── consistency.json
        ├── editorial.json
        ├── principles.json
        ├── mobile_ux.json
        ├── desktop_ux.json
        └── seo.json
```

## Tech Stack

- **Pydantic AI** — agent framework with first-class OpenRouter support
- **OpenRouter** — LLM API gateway (Claude, GPT-4, Gemini, etc.)
- **Playwright** — browser automation for crawling + screenshots
- **Pydantic** — structured, validated agent outputs
