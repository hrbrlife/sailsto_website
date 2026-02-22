"""
Configuration for the QA testing suite.
Per-agent model routing: critical → Opus 4.6, mid-tier → Sonnet 4.6,
UX → Kimi K2.5, mechanical → Grok 4.1 Fast. All via OpenRouter.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv(Path(__file__).resolve().parent / ".env")

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
REPORTS_DIR = ROOT / "reports"
SCREENSHOTS_DIR = ROOT / "reports" / "screenshots"
CRAWL_DATA_DIR = ROOT / "reports" / "crawl_data"

# ── OpenRouter ───────────────────────────────────────────────────────────────
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# ── Model routing (2 tiers) ─────────────────────────────────────────────────
# Boss  = Opus 4.6 ($5/$25)  — legal + council (critical thinking)
# Slave = Gemini 2.5 Flash ($0.30/$2.50) — everything else
# TEST MODE: all agents use cheapest model to validate pipeline
MODEL_BOSS  = os.environ.get("MODEL_BOSS",  "openrouter:google/gemini-2.5-flash")
MODEL_SLAVE = os.environ.get("MODEL_SLAVE", "openrouter:google/gemini-2.5-flash")

AGENT_MODELS = {
    "legal":       MODEL_BOSS,
    "council":     MODEL_BOSS,
    "conversion":  MODEL_BOSS,
    "consistency": MODEL_SLAVE,
    "editorial":   MODEL_SLAVE,
    "principles":  MODEL_SLAVE,
    "mobile_ux":   MODEL_SLAVE,
    "desktop_ux":  MODEL_SLAVE,
    "seo":         MODEL_SLAVE,
}

# ── Sites to test ────────────────────────────────────────────────────────────
BASE_URL = os.environ.get("BASE_URL", "https://melusina-os.org")

SITES = {
    "melusina-os": {
        "base_url": BASE_URL,
        "pages": [
            "/en",
            "/en/use-cases",
            "/en/compare",
            "/en/docs/architecture-blueprint",
            "/en/roadmap",
            "/en/plans",
            "/en/faq",
            "/en/company",
            "/en/apps/bureau",
            "/en/knowledge-base",
            "/en/glossary",
            "/en/blog",
        ],
    },
}

# ── Viewports ────────────────────────────────────────────────────────────────
VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "mobile": {"width": 390, "height": 844},  # iPhone 14 Pro
}

# ── Playwright ───────────────────────────────────────────────────────────────
PLAYWRIGHT_TIMEOUT = 30_000  # ms per page load
SCREENSHOT_FULL_PAGE = True

# ── Context document paths (fed to agents for grounding) ────────────────────
CONTEXT_DOCS = [
    ROOT.parent / "melusina-os" / "REVIEW-PROMPT.md",
]
