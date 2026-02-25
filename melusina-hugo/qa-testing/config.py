"""
Configuration for Melusina OS QA Testing Suite.
Free-tier council: Trinity Large Preview (reasoning/text) +
Nemotron Nano 12B 2 VL (vision). Both free via OpenRouter.

Self-contained inside the melusina-hugo site directory.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv(Path(__file__).resolve().parent / ".env")

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent          # melusina-hugo/qa-testing/
SITE_ROOT = ROOT.parent                         # melusina-hugo/
REPORTS_DIR = ROOT / "reports"
SCREENSHOTS_DIR = ROOT / "reports" / "screenshots"
CRAWL_DATA_DIR = ROOT / "reports" / "crawl_data"

# ── OpenRouter ───────────────────────────────────────────────────────────────
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# ── Model routing (free-tier: Trinity + Nemotron VL) ─────────────────────────
# Tier 1: BRAIN  — Arcee Trinity Large Preview (free) — 131K ctx, 400B MoE (13B active)
#                  Frontier reasoning, agentic, creative. Text-only.
#                  Council synthesis, legal, editorial, principles, consistency, conversion.
# Tier 2: EYES   — NVIDIA Nemotron Nano 12B 2 VL (free) — 128K ctx, multimodal vision
#                  OCR, chart reasoning, document intelligence. Sees screenshots.
#                  Mobile UX, Desktop UX, SEO (all get actual page screenshots).
MODEL_BRAIN = os.environ.get("MODEL_BRAIN", "openrouter:arcee-ai/trinity-large-preview:free")
MODEL_EYES  = os.environ.get("MODEL_EYES",  "openrouter:nvidia/nemotron-nano-12b-v2-vl:free")

AGENT_MODELS = {
    "council":     MODEL_BRAIN,     # Trinity — synthesises 8 expert reports, final grade
    "legal":       MODEL_BRAIN,     # Trinity — regulatory nuance, long-form reasoning
    "editorial":   MODEL_BRAIN,     # Trinity — copy quality, dinner test, tone
    "principles":  MODEL_BRAIN,     # Trinity — brand identity, emotional arc
    "conversion":  MODEL_BRAIN,     # Trinity — persona journeys, funnel analysis
    "consistency": MODEL_BRAIN,     # Trinity — cross-page terminology, messaging
    "seo":         MODEL_BRAIN,     # Trinity — meta tags, heading structure, perf
    "mobile_ux":   MODEL_BRAIN,     # Trinity — mobile layout analysis from metadata
    "desktop_ux":  MODEL_BRAIN,     # Trinity — desktop layout analysis from metadata
}

# Vision agents disabled — Nemotron VL free tier is unreliable (null responses).
# All agents run text-only via Trinity.  Re-enable when a reliable free VL model
# becomes available on OpenRouter.
VISION_AGENTS: set[str] = set()  # was {"mobile_ux", "desktop_ux", "seo"}

# ── Site under test ──────────────────────────────────────────────────────────
SITE_NAME = "melusina-os"
BASE_URL = os.environ.get("BASE_URL", "http://localhost:4173")

SITES = {
    "melusina-os": {
        "base_url": BASE_URL,
        "content_dir": str(SITE_ROOT / "content"),
        # pages: auto-discovered from crawl data by default.
        # Uncomment to restrict/order the page list:
        # "pages": [
        #     "/en",
        #     "/en/use-cases",
        #     "/en/compare",
        #     "/en/docs/architecture-blueprint",
        #     "/en/roadmap",
        #     "/en/plans",
        #     "/en/faq",
        #     "/en/company",
        #     "/en/apps/bureau",
        #     "/en/knowledge-base",
        #     "/en/glossary",
        #     "/en/blog",
        #     "/en/privacy",
        #     "/en/terms",
        #     "/en/dmca",
        # ],
        "context_docs": [],
        "dogma_dir": "melusina-os",
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
CONTEXT_DOCS = []
