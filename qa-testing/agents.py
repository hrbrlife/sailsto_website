"""
Expert agent definitions — each agent loads its dogma document as the system prompt.
All powered by Pydantic AI + OpenRouter, 4-tier model routing:
  Opus 4 (council + legal) → Sonnet 4 (editorial/principles/conversion) →
  Gemini 2.5 Pro (consistency/seo) → Gemini 2.5 Flash (UX viewports).
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic_ai import Agent

from config import AGENT_MODELS, CONTEXT_DOCS
from models import (
    LegalReport,
    ConsistencyReport,
    EditorialReport,
    PrinciplesReport,
    MobileUXReport,
    DesktopUXReport,
    SEOReport,
    ConversionReport,
    CouncilReport,
    ExpertReport,
)

DOGMA_DIR = Path(__file__).resolve().parent / "dogma"


def _load_dogma(agent_key: str) -> str:
    """Load the dogma document for an agent."""
    path = DOGMA_DIR / f"{agent_key}.md"
    if not path.exists():
        raise FileNotFoundError(f"Dogma file missing: {path}")
    return path.read_text()


def _load_context_docs() -> str:
    """Load grounding documents (REVIEW-PROMPT.md etc.)."""
    parts = []
    for p in CONTEXT_DOCS:
        if p.exists():
            parts.append(f"--- {p.name} ---\n{p.read_text()[:6000]}")
    return "\n\n".join(parts) if parts else "(No context documents found)"


def _build_system_prompt(agent_key: str, brand_context: str) -> str:
    """Combine dogma + brand context into a system prompt."""
    dogma = _load_dogma(agent_key)
    return f"{dogma}\n\n---\n\n## Brand & Product Context\n\n{brand_context}"


# ── Helper to build page data for prompts ────────────────────────────────────

def _format_crawl_data(crawl_data: list[dict], viewport_filter: str = "") -> str:
    """Format crawl data into a readable prompt section."""
    pages = []
    for item in crawl_data:
        if viewport_filter and item.get("viewport") != viewport_filter:
            continue
        page = f"""
## Page: {item['page_path']} ({item['viewport']})
URL: {item['full_url']}
Load time: {item['load_time_ms']}ms | Words: {item['word_count']} | Links: {item['link_count']} | Images: {item['image_count']}

### Title: {item['meta']['title']}
### H1: {', '.join(item['meta']['h1']) if item['meta']['h1'] else '(none)'}
### H2: {', '.join(item['meta']['h2'][:8]) if item['meta']['h2'] else '(none)'}
### Meta Description: {item['meta']['description']}
### OG Title: {item['meta']['og_title']}
### OG Description: {item['meta']['og_description']}
### Canonical: {item['meta']['canonical']}
### Robots: {item['meta']['robots']}

### Console Errors: {len([c for c in item['console_logs'] if c['type'] == 'error'])}
{chr(10).join(f"  - [{c['type']}] {c['text'][:200]}" for c in item['console_logs'] if c['type'] in ('error','warning'))[:1000]}

### Network Errors: {len(item['network_errors'])}
{chr(10).join(f"  - {e['status']} {e['url'][:100]}" for e in item['network_errors'])[:500]}

### Broken Images: {item['broken_images'][:5]}

### Screenshot: {item['screenshot_path']}

### Page Content (excerpt):
{item['page_text'][:3000]}
"""
        pages.append(page)
    return "\n---\n".join(pages)


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERT AGENTS — lazy initialization (no API key needed at import time)
# ═══════════════════════════════════════════════════════════════════════════════

_agents_cache: dict[str, Agent] = {}


def _get_agents() -> dict[str, Agent]:
    """Create all agents on first call. Requires OPENROUTER_API_KEY."""
    if _agents_cache:
        return _agents_cache

    BRAND_CONTEXT = _load_context_docs()

    # Agent key → output type mapping
    agent_defs: list[tuple[str, type]] = [
        ("legal",       LegalReport),
        ("consistency", ConsistencyReport),
        ("editorial",   EditorialReport),
        ("principles",  PrinciplesReport),
        ("mobile_ux",   MobileUXReport),
        ("desktop_ux",  DesktopUXReport),
        ("seo",         SEOReport),
        ("conversion",  ConversionReport),
        ("council",     CouncilReport),
    ]

    for key, output_type in agent_defs:
        _agents_cache[key] = Agent(
            model=AGENT_MODELS[key],
            output_type=output_type,
            system_prompt=_build_system_prompt(key, BRAND_CONTEXT),
        )

    return _agents_cache


# ═══════════════════════════════════════════════════════════════════════════════
#  RUNNER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def run_expert(agent_key: str, crawl_data: list[dict], viewport_filter: str = "") -> ExpertReport:
    """Run a single expert agent against crawl data."""
    agents = _get_agents()
    agent = agents[agent_key]
    formatted = _format_crawl_data(crawl_data, viewport_filter)
    prompt = f"Review the following website crawl data and produce your expert report:\n\n{formatted}"
    result = await agent.run(prompt)
    return result.output


async def run_council(expert_reports: list[ExpertReport], site_name: str, run_date: str) -> CouncilReport:
    """Run the council agent to synthesize all expert reports."""
    agents = _get_agents()
    reports_text = ""
    for report in expert_reports:
        reports_text += f"\n\n{'='*60}\n"
        reports_text += f"EXPERT: {report.expert_name} ({report.expert_role})\n"
        reports_text += f"SCORE: {report.overall_score}/10\n"
        reports_text += f"SUMMARY: {report.summary}\n"
        reports_text += f"TOP PRIORITIES: {', '.join(report.top_priorities)}\n"
        reports_text += f"ISSUES ({len(report.issues)}):\n"
        for issue in report.issues:
            reports_text += f"  [{issue.severity}] {issue.title}: {issue.description}\n"
            reports_text += f"    → {issue.recommendation}\n"
            if issue.evidence:
                reports_text += f"    Evidence: {issue.evidence}\n"

    prompt = f"""Site: {site_name}
Date: {run_date}

Below are the complete findings from our panel of {len(expert_reports)} expert reviewers.
Synthesize them into a unified council report with prioritized decisions.

{reports_text}"""

    result = await agents["council"].run(prompt, model_settings={"max_tokens": 16000})
    council = result.output
    council.expert_reports = expert_reports
    return council
