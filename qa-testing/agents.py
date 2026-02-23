"""
Expert agent definitions — each agent loads its dogma document as the system prompt.
All powered by Pydantic AI + OpenRouter, 4-tier model routing:
  Opus 4 (council + legal) → Sonnet 4 (editorial/principles/conversion) →
  Gemini 2.5 Pro (consistency/seo) → Gemini 2.5 Flash (UX viewports).

Supports per-site dogma directories:
  dogma/melusina-os/legal.md, dogma/sails-to/legal.md, etc.
  Falls back to dogma/legal.md if site-specific file doesn't exist.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic_ai import Agent

from config import AGENT_MODELS, CONTEXT_DOCS, SITES
from content_loader import SiteCorpus, format_source_for_prompt
from qc_agents import QCReport
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


def _load_dogma(agent_key: str, site_name: str = "") -> str:
    """Load the dogma document for an agent, preferring site-specific version."""
    # Try site-specific dogma first
    if site_name:
        site_cfg = SITES.get(site_name, {})
        dogma_subdir = site_cfg.get("dogma_dir", site_name)
        site_path = DOGMA_DIR / dogma_subdir / f"{agent_key}.md"
        if site_path.exists():
            return site_path.read_text()

    # Fall back to root dogma
    path = DOGMA_DIR / f"{agent_key}.md"
    if not path.exists():
        raise FileNotFoundError(f"Dogma file missing: {path}")
    return path.read_text()


def _load_context_docs(site_name: str = "") -> str:
    """Load grounding documents — per-site if available, else legacy fallback."""
    # Try per-site context docs
    doc_paths = []
    if site_name and site_name in SITES:
        doc_paths = SITES[site_name].get("context_docs", [])

    # Legacy fallback
    if not doc_paths:
        doc_paths = CONTEXT_DOCS

    parts = []
    for p in doc_paths:
        if p.exists():
            parts.append(f"--- {p.name} ---\n{p.read_text()[:30000]}")
    return "\n\n".join(parts) if parts else "(No context documents found)"


def _build_system_prompt(
    agent_key: str,
    brand_context: str,
    site_name: str = "",
    source_content: str = "",
    qc_report_text: str = "",
) -> str:
    """Combine dogma + brand context + source content + QC findings into a system prompt."""
    dogma = _load_dogma(agent_key, site_name)
    parts = [dogma, "\n\n---\n\n## Brand & Product Context\n\n", brand_context]

    if qc_report_text:
        parts.append("\n\n---\n\n")
        parts.append(qc_report_text)

    if source_content:
        parts.append("\n\n---\n\n")
        parts.append(source_content)

    return "".join(parts)


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
{item['page_text'][:6000]}
"""
        pages.append(page)
    return "\n---\n".join(pages)


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERT AGENTS — per-site initialization (no API key needed at import time)
# ═══════════════════════════════════════════════════════════════════════════════

_agents_cache: dict[str, dict[str, Agent]] = {}  # site_name -> {agent_key -> Agent}


def _get_agents(
    site_name: str = "melusina-os",
    source_content: str = "",
    qc_report_text: str = "",
) -> dict[str, Agent]:
    """Create all agents for a site on first call. Requires OPENROUTER_API_KEY.

    When source_content or qc_report_text change we invalidate the cache
    so agents get the fresh system prompt.
    """
    # Build a cache key that includes whether we have source/QC data
    cache_key = f"{site_name}|{bool(source_content)}|{bool(qc_report_text)}"
    if cache_key in _agents_cache:
        return _agents_cache[cache_key]

    BRAND_CONTEXT = _load_context_docs(site_name)

    # Size control: source content per agent role
    # Council + consistency + editorial + principles get full source
    # Others get a truncated version to save tokens
    FULL_SOURCE_AGENTS = {"council", "consistency", "editorial", "principles", "legal"}

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

    site_agents = {}
    for key, output_type in agent_defs:
        # Full source for content-heavy agents, truncated for others
        if key in FULL_SOURCE_AGENTS:
            agent_source = source_content
        elif source_content:
            # Give UX/SEO/conversion a shorter excerpt (first 60K chars)
            agent_source = source_content[:60_000]
            if len(source_content) > 60_000:
                agent_source += "\n...(source truncated for this agent)"
        else:
            agent_source = ""

        retries = 3 if key == "council" else 1
        site_agents[key] = Agent(
            model=AGENT_MODELS[key],
            output_type=output_type,
            retries=retries,
            system_prompt=_build_system_prompt(
                key, BRAND_CONTEXT, site_name,
                source_content=agent_source,
                qc_report_text=qc_report_text,
            ),
        )

    _agents_cache[cache_key] = site_agents
    return site_agents


# ═══════════════════════════════════════════════════════════════════════════════
#  RUNNER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def run_expert(
    agent_key: str,
    crawl_data: list[dict],
    viewport_filter: str = "",
    site_name: str = "melusina-os",
    source_content: str = "",
    qc_report_text: str = "",
) -> ExpertReport:
    """Run a single expert agent against crawl data."""
    agents = _get_agents(site_name, source_content=source_content, qc_report_text=qc_report_text)
    agent = agents[agent_key]
    formatted = _format_crawl_data(crawl_data, viewport_filter)
    prompt = f"Review the following website crawl data and produce your expert report:\n\n{formatted}"
    result = await agent.run(prompt)
    return result.output


async def run_council(
    expert_reports: list[ExpertReport],
    site_name: str,
    run_date: str,
    source_content: str = "",
    qc_report_text: str = "",
) -> CouncilReport:
    """Run the council agent to synthesize all expert reports."""
    agents = _get_agents(site_name, source_content=source_content, qc_report_text=qc_report_text)
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
