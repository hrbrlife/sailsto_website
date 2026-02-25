"""
Per-page consilium agents — each agent evaluates ONE page at a time.

Architecture:
  Phase 2a: 8 experts × N pages = 8N calls (parallel per page, sequential across pages)
  Phase 2b: per-page council synthesizes 8 expert reports → PageConsilium
  Phase 3:  mega council synthesizes all PageConsiliums → MegaConsilium

All powered by Pydantic AI + OpenRouter using Trinity Large Preview (free tier).
Dogma files from dogma/aitxpro/ define each agent's character and evaluation criteria.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from pydantic_ai import Agent

from config import AGENT_MODELS
from models import (
    LegalReport,
    ConsistencyReport,
    EditorialReport,
    PrinciplesReport,
    MobileUXReport,
    DesktopUXReport,
    SEOReport,
    ConversionReport,
    ExpertReport,
    Issue,
    PageConsilium,
    MegaConsilium,
    CouncilDecision,
)

# ── Expert key → output model ────────────────────────────────────────────────

EXPERT_KEYS = [
    "legal", "consistency", "editorial", "principles",
    "mobile_ux", "desktop_ux", "seo", "conversion",
]

OUTPUT_MODELS: dict[str, type] = {
    "legal":        LegalReport,
    "consistency":  ConsistencyReport,
    "editorial":    EditorialReport,
    "principles":   PrinciplesReport,
    "mobile_ux":    MobileUXReport,
    "desktop_ux":   DesktopUXReport,
    "seo":          SEOReport,
    "conversion":   ConversionReport,
    "page_council": PageConsilium,
    "mega_council": MegaConsilium,
}

DOGMA_DIR = Path(__file__).resolve().parent / "dogma"


# ═══════════════════════════════════════════════════════════════════════════════
#  PROMPT UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def _json_schema_instruction(model_cls: type) -> str:
    """Append JSON schema specification to system prompt."""
    schema = model_cls.model_json_schema()
    compact = json.dumps(schema, indent=2)
    return (
        "\n\n---\n\n## RESPONSE FORMAT\n\n"
        "You MUST respond with a single JSON object (no markdown fences, no commentary "
        "before or after). The JSON must conform to this schema:\n\n"
        f"```json\n{compact}\n```\n\n"
        "Return ONLY the JSON object. Do NOT wrap it in ```json fences.\n"
    )


def _extract_json(text: str) -> dict:
    """Pull the first JSON object from model response with LLM-quirk tolerance."""
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"```\s*$", "", text.strip())
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object found in model response")
    depth = 0
    end = start
    for i, ch in enumerate(text[start:], start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    raw = text[start:end]

    # Strict parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Fix trailing commas + unquoted keys
    fixed = re.sub(r",\s*([}\]])", r"\1", raw)
    fixed = re.sub(r"(?<=[\{,])\s*(\w+)\s*:", r' "\1":', fixed)
    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass

    # Single quotes → double quotes (last resort)
    try:
        fixed2 = raw.replace("'", '"')
        fixed2 = re.sub(r",\s*([}\]])", r"\1", fixed2)
        return json.loads(fixed2)
    except (json.JSONDecodeError, ValueError):
        raise ValueError(f"Could not parse JSON (first 500 chars): {raw[:500]}")


def _fix_string_lists(data: dict) -> None:
    """Recursively convert comma-separated strings to lists where expected."""
    if not isinstance(data, dict):
        return
    LIST_FIELDS = {
        "what_works", "what_breaks", "missing_elements", "flow_path",
        "top_priorities", "missing_policies", "gdpr_issues",
        "ai_sounding_phrases", "missing_aha_moments", "readability_notes",
        "missing_principles", "scroll_depth_concerns", "whitespace_issues",
        "canonical_issues", "cross_cutting_themes", "strengths",
        "quick_wins", "trust_signal_gaps", "messaging_gaps",
        "related_issues", "broken_images", "top_recommendations",
        "site_wide_strengths",
    }
    for key, val in data.items():
        if isinstance(val, str) and "," in val and key in LIST_FIELDS:
            data[key] = [s.strip() for s in val.split(",") if s.strip()]
        elif isinstance(val, dict):
            _fix_string_lists(val)
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    _fix_string_lists(item)


def _load_dogma(agent_key: str, site_name: str = "") -> str:
    """Load dogma document, preferring site-specific version."""
    from config import SITES
    if site_name:
        site_cfg = SITES.get(site_name, {})
        dogma_subdir = site_cfg.get("dogma_dir", site_name)
        site_path = DOGMA_DIR / dogma_subdir / f"{agent_key}.md"
        if site_path.exists():
            return site_path.read_text()
    path = DOGMA_DIR / f"{agent_key}.md"
    if not path.exists():
        raise FileNotFoundError(f"Dogma file missing: {path}")
    return path.read_text()


def _parse_output(raw: str, agent_key: str):
    """Parse raw JSON string into the appropriate Pydantic model."""
    model_cls = OUTPUT_MODELS[agent_key]
    data = _extract_json(raw)
    _fix_string_lists(data)
    return model_cls.model_validate(data)


# ═══════════════════════════════════════════════════════════════════════════════
#  AGENT FACTORY — dogma-only system prompts, page data in user messages
# ═══════════════════════════════════════════════════════════════════════════════

_agents_cache: dict[str, dict[str, Agent]] = {}


def _get_page_agents(site_name: str = "aitxpro") -> dict[str, Agent]:
    """Create agents with dogma-only system prompts.

    Page-specific data goes in user messages, not system prompts.
    Agents are created once and reused across all pages.
    """
    if site_name in _agents_cache:
        return _agents_cache[site_name]

    agents = {}

    # Expert agents: dogma + JSON schema
    for key in EXPERT_KEYS:
        dogma = _load_dogma(key, site_name)
        model_cls = OUTPUT_MODELS[key]
        system = dogma + _json_schema_instruction(model_cls)
        agents[key] = Agent(
            model=AGENT_MODELS[key],
            output_type=str,
            retries=2,
            system_prompt=system,
        )

    # Per-page council agent
    page_council_system = _build_page_council_system(site_name)
    agents["page_council"] = Agent(
        model=AGENT_MODELS["council"],
        output_type=str,
        retries=2,
        system_prompt=page_council_system,
    )

    # Mega council agent: uses council.md dogma
    mega_dogma = _load_dogma("council", site_name)
    mega_system = mega_dogma + _json_schema_instruction(MegaConsilium)
    agents["mega_council"] = Agent(
        model=AGENT_MODELS["council"],
        output_type=str,
        retries=3,
        system_prompt=mega_system,
    )

    _agents_cache[site_name] = agents
    return agents


def _build_page_council_system(site_name: str) -> str:
    """Build system prompt for the per-page council agent."""
    instructions = """\
# Per-Page Consilium — Council Chair

You receive reports from up to 8 expert reviewers who have each evaluated a
SINGLE PAGE of the website. Your job is to synthesize their findings into
a unified per-page consilium report.

## Your Process

1. **Read every expert report** — don't skim
2. **Merge and deduplicate issues** — same issue found by multiple experts is stronger signal
3. **Score the page** — weighted average of expert scores, adjusted for critical issues
4. **Produce top recommendations** — specific, actionable, prioritized

## Conflict Resolution

- **Legal > Editorial**: compliance trumps style
- **Mobile > Desktop**: mobile-first
- **Consistency > Editorial**: brand vocabulary wins
- **Conversion > Principles**: but never sacrifice brand identity

## Output Fields

- **page_path**: the page being evaluated
- **executive_summary**: 2-3 sentences assessing this specific page
- **overall_score**: your composite assessment (1-10)
- **expert_scores**: record each expert's score {role: score}
- **critical_count**: number of critical issues across all experts
- **warning_count**: number of warning issues across all experts
- **top_issues**: the most important issues across ALL experts, merged and prioritized
- **strengths**: what this page does well
- **top_recommendations**: 3-5 specific fixes in priority order
"""
    return instructions + _json_schema_instruction(PageConsilium)


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE DATA FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════

def _format_crawl_item(item: dict) -> str:
    """Format a single crawl item (one viewport of one page) into text."""
    console_issues = [
        c for c in item.get("console_logs", [])
        if c.get("type") in ("error", "warning")
    ]
    network_errors = item.get("network_errors", [])
    meta = item.get("meta", {})

    return f"""\
Viewport: {item.get('viewport', 'unknown')} ({item.get('viewport_width', '?')}x{item.get('viewport_height', '?')})
URL: {item.get('full_url', '')}
Load time: {item.get('load_time_ms', 0)}ms | Words: {item.get('word_count', 0)} | Links: {item.get('link_count', 0)} | Images: {item.get('image_count', 0)}

Title: {meta.get('title', '(none)')}
H1: {', '.join(meta.get('h1', [])) or '(none)'}
H2: {', '.join(meta.get('h2', [])[:10]) or '(none)'}
Meta Description: {meta.get('description', '(none)')}
OG Title: {meta.get('og_title', '')}
OG Description: {meta.get('og_description', '')}
Canonical: {meta.get('canonical', '')}
Robots: {meta.get('robots', '')}

Console Issues ({len(console_issues)}):
{chr(10).join(f'  [{c["type"]}] {c["text"][:200]}' for c in console_issues[:10]) or '  (none)'}

Network Errors ({len(network_errors)}):
{chr(10).join(f'  {e["status"]} {e["url"][:120]}' for e in network_errors[:5]) or '  (none)'}

Broken Images: {', '.join(str(b) for b in item.get('broken_images', [])[:5]) or '(none)'}

Page Text (rendered):
{item.get('page_text', '')[:3000]}"""


def build_page_expert_prompt(
    page_path: str,
    md_source: str,
    crawl_items: list[dict],
    qc_excerpt: str = "",
) -> str:
    """Build the user message for one expert evaluating one page.

    Includes: full MD source + desktop and mobile crawl data + QC notes.
    """
    parts = [
        f"# Evaluate this SINGLE page: {page_path}\n\n"
        f"Review this page thoroughly against your dogma and produce your expert report.\n\n"
    ]

    # Full MD source
    if md_source:
        parts.append("## Markdown Source Content\n\n")
        parts.append(md_source)
        parts.append("\n\n")

    # Crawl data for each viewport
    for item in crawl_items:
        viewport = item.get("viewport", "unknown")
        parts.append(f"## Crawl Data — {viewport.title()} Viewport\n\n")
        parts.append(_format_crawl_item(item))
        parts.append("\n\n")

    # QC notes
    if qc_excerpt:
        parts.append("## Pre-Processing QC Notes\n\n")
        parts.append(qc_excerpt[:5000])
        parts.append("\n\n")

    parts.append(
        f"Produce your expert report for page {page_path}. "
        "Focus on issues specific to THIS page. Be concrete and cite evidence."
    )

    return "".join(parts)


def build_page_council_prompt(
    page_path: str,
    page_title: str,
    expert_reports: list[ExpertReport],
) -> str:
    """Build the user message for the per-page council synthesis."""
    parts = [
        f"# Per-Page Consilium: {page_path}\n"
        f"**Title**: {page_title}\n\n"
        f"Below are findings from {len(expert_reports)} expert reviewers "
        f"for this specific page.\n"
        f"Synthesize them into a unified consilium.\n\n"
    ]

    for report in expert_reports:
        parts.append(f"{'='*60}\n")
        parts.append(f"EXPERT: {report.expert_name} ({report.expert_role})\n")
        parts.append(f"SCORE: {report.overall_score}/10\n")
        parts.append(f"SUMMARY: {report.summary}\n")
        parts.append(f"TOP PRIORITIES: {', '.join(report.top_priorities)}\n")
        parts.append(f"ISSUES ({len(report.issues)}):\n")
        for issue in report.issues:
            parts.append(f"  [{issue.severity}] {issue.title}: {issue.description}\n")
            parts.append(f"    -> {issue.recommendation}\n")
            if issue.evidence:
                parts.append(f"    Evidence: {issue.evidence}\n")
        parts.append("\n")

    return "".join(parts)


def build_mega_council_prompt(
    page_consiliums: list[PageConsilium],
    site_name: str,
    run_date: str,
) -> str:
    """Build the user message for the final mega council synthesis."""
    parts = [
        f"# Mega Consilium — Site-Wide Synthesis\n\n"
        f"**Site**: {site_name}\n"
        f"**Date**: {run_date}\n"
        f"**Pages evaluated**: {len(page_consiliums)}\n\n"
        f"Below are the consilium reports for every page on the site.\n"
        f"Produce a final site-wide mega consilium with overall grade, "
        f"cross-cutting themes, and prioritized decisions.\n\n"
    ]

    for pc in page_consiliums:
        parts.append(pc.format_for_mega_prompt())
        parts.append("\n---\n\n")

    return "".join(parts)


# ═══════════════════════════════════════════════════════════════════════════════
#  RUNNER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def run_page_expert(
    agent_key: str,
    page_path: str,
    md_source: str,
    crawl_items: list[dict],
    site_name: str = "aitxpro",
    qc_excerpt: str = "",
) -> ExpertReport:
    """Run one expert agent against one page.

    Returns the appropriate specialist ExpertReport subclass (LegalReport, etc.).
    """
    agents = _get_page_agents(site_name)
    agent = agents[agent_key]

    prompt = build_page_expert_prompt(page_path, md_source, crawl_items, qc_excerpt)
    result = await agent.run(prompt, model_settings={"max_tokens": 10000})
    report = _parse_output(result.output, agent_key)

    # Force correct expert_role key (LLM sometimes hallucinates different names)
    report.expert_role = agent_key

    # Ensure page field is set correctly on all issues
    for issue in report.issues:
        if not issue.page or issue.page == "various":
            issue.page = page_path

    return report


async def run_page_council(
    expert_reports: list[ExpertReport],
    page_path: str,
    page_title: str,
    page_url: str = "",
    site_name: str = "aitxpro",
) -> PageConsilium:
    """Synthesize 8 expert reports for one page into a PageConsilium."""
    agents = _get_page_agents(site_name)
    agent = agents["page_council"]

    prompt = build_page_council_prompt(page_path, page_title, expert_reports)
    result = await agent.run(prompt, model_settings={"max_tokens": 12000})
    consilium = _parse_output(result.output, "page_council")

    # Attach programmatic data
    consilium.page_path = page_path
    consilium.page_url = page_url
    consilium.page_title = page_title
    consilium.expert_reports = expert_reports

    # Always overwrite expert_scores from actual reports (LLM may use wrong keys)
    consilium.expert_scores = {
        r.expert_role: r.overall_score for r in expert_reports
    }

    return consilium


async def run_mega_council(
    page_consiliums: list[PageConsilium],
    site_name: str,
    run_date: str,
) -> MegaConsilium:
    """Final synthesis from all per-page consiliums into a MegaConsilium."""
    agents = _get_page_agents(site_name)
    agent = agents["mega_council"]

    prompt = build_mega_council_prompt(page_consiliums, site_name, run_date)
    result = await agent.run(prompt, model_settings={"max_tokens": 16000})
    mega = _parse_output(result.output, "mega_council")

    # Attach per-page consiliums
    mega.page_consiliums = page_consiliums

    return mega
