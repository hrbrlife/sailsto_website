"""
Configuration for the QA testing suite.
Opus 4 + xAI Grok swarm: Opus 4 (council), Grok 4.1 Fast (expert agents),
Grok 3 Mini (UX viewport checks). All via OpenRouter.
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

# ── Model routing (Opus + xAI Grok) ─────────────────────────────────────────
# Tier 1: BOSS    — Claude Opus 4         — council synthesis (deep reasoning)
# Tier 2: SENIOR  — xAI Grok 4.1 Fast     — expert agents (SEO #1, Legal #3, 2M context)
# Tier 3: WORKER  — xAI Grok 3 Mini       — UX viewport analysis (lightweight)
MODEL_BOSS    = os.environ.get("MODEL_BOSS",    "openrouter:anthropic/claude-opus-4")
MODEL_SENIOR  = os.environ.get("MODEL_SENIOR",  "openrouter:x-ai/grok-4.1-fast")
MODEL_WORKER  = os.environ.get("MODEL_WORKER",  "openrouter:x-ai/grok-3-mini")

AGENT_MODELS = {
    "council":     MODEL_BOSS,      # Opus 4 — synthesises 8 expert reports, final grade
    "legal":       MODEL_SENIOR,    # Grok 4.1 Fast — regulatory nuance (#3 Legal)
    "editorial":   MODEL_SENIOR,    # Grok 4.1 Fast — copy quality, dinner test
    "principles":  MODEL_SENIOR,    # Grok 4.1 Fast — brand identity, emotional arc
    "conversion":  MODEL_SENIOR,    # Grok 4.1 Fast — persona journeys, funnel analysis
    "consistency": MODEL_SENIOR,    # Grok 4.1 Fast — cross-page terminology, tone
    "seo":         MODEL_SENIOR,    # Grok 4.1 Fast — meta tags, structured data (#1 SEO)
    "mobile_ux":   MODEL_WORKER,    # Grok 3 Mini — mechanical viewport checks
    "desktop_ux":  MODEL_WORKER,    # Grok 3 Mini — mechanical viewport checks
}

# ── Sites to test ────────────────────────────────────────────────────────────
BASE_URL = os.environ.get("BASE_URL", "http://localhost:4173")

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
            "/en/privacy",
            "/en/terms",
            "/en/dmca",
        ],
        "context_docs": [
            ROOT.parent / "melusina-os" / "REVIEW-PROMPT.md",
        ],
        "dogma_dir": "melusina-os",
    },
    "sails-to": {
        "base_url": os.environ.get("SAILSTO_BASE_URL", "http://localhost:4174"),
        "pages": [
            # ── Core / Landing ──
            "/",
            "/whatsails/",
            "/compare/",
            "/players/",
            # ── Audience pages ──
            "/brokers/",
            "/investors/",
            "/issuers/",
            "/introducers/",
            "/trustees/",
            "/regulated/",
            "/issuers-directory/",
            # ── Product / Commercial ──
            "/pricing/",
            "/signup/",
            "/compliance/",
            "/security/",
            "/oversight/",
            # ── Company ──
            "/company/about/",
            "/company/contact/",
            "/company/legal/",
            # ── Knowledge Hub ──
            "/knowledge/",
            "/knowledge/faq/",
            "/knowledge/roadmap/",
            "/knowledge/blog/",
            "/knowledge/docs/",
            "/knowledge/glossary/",
            # ── Key Docs (sample) ──
            "/knowledge/docs/platform-overview/",
            "/knowledge/docs/getting-started/",
            "/knowledge/docs/hybrid-architecture/",
            "/knowledge/docs/compliance-framework/",
            # ── Key Guides (sample) ──
            "/knowledge/guides/tokenization-101/",
            "/knowledge/guides/wyoming-dao-explained/",
            # ── Key Glossary (sample) ──
            "/knowledge/glossary/crosssecurities/",
            "/knowledge/glossary/crossconversion/",
            "/knowledge/glossary/security-token/",
        ],
        "context_docs": [
            ROOT / "SAILSTO-REVIEW-PROMPT.md",
        ],
        "dogma_dir": "sails-to",
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
# Per-site context docs are now in SITES[site]["context_docs"].
# Legacy fallback for backward compatibility:
CONTEXT_DOCS = [
    ROOT.parent / "melusina-os" / "REVIEW-PROMPT.md",
]
