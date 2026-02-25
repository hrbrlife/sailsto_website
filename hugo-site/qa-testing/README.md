# QA Council — AiTX.pro Testing Suite

A panel of 7 AI expert agents reviews the AiTX.pro website from different
perspectives, then convenes a council to produce a unified, prioritized HTML report.

Uses **free-tier** OpenRouter models:
- **Arcee Trinity Large Preview** — text reasoning (council, legal, editorial, principles, consistency, conversion)
- **NVIDIA Nemotron Nano 12B 2 VL** — multimodal vision (mobile UX, desktop UX, SEO)

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
# 1. Install dependencies
make install

# 2. Set your OpenRouter API key (free at openrouter.ai)
export OPENROUTER_API_KEY="sk-or-..."

# 3. Start Hugo dev server in another terminal
cd .. && hugo server -p 4175

# 4. Full run: crawl + agents + report
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
```

## Output Structure

```
reports/
├── qa-report-aitxpro-latest.html   ← open this
├── qa-report-aitxpro-20260222.html
├── council-aitxpro.json
├── screenshots/
│   └── aitxpro/
│       ├── desktop/          ← full-page screenshots
│       └── mobile/
├── crawl_data/
│   └── aitxpro.json          ← raw crawl data
├── qc/
│   └── aitxpro/
│       └── qc-report.txt
└── experts/
    └── aitxpro/
        ├── legal.json
        ├── consistency.json
        ├── editorial.json
        ├── principles.json
        ├── mobile_ux.json
        ├── desktop_ux.json
        ├── conversion.json
        └── seo.json
```

## Tech Stack

- **Pydantic AI** — agent framework with first-class OpenRouter support
- **OpenRouter** — free-tier LLM gateway (Trinity + Nemotron VL)
- **Playwright** — browser automation for crawling + screenshots
- **Pydantic** — structured, validated agent outputs
