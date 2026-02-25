"""
Expert agent definitions — each agent loads its dogma document as the system prompt.
All powered by Pydantic AI + OpenRouter, 2-tier FREE model routing:
  Trinity Large Preview (council, legal, editorial, principles, consistency, conversion)
  Nemotron Nano 12B 2 VL (mobile_ux, desktop_ux, seo) — receives actual screenshots.

Vision agents receive page screenshots as base64 image_url content parts
so the VL model can inspect layout, typography, spacing, and visual hierarchy.

Dogma files loaded from dogma/aitxpro/ with fallback to dogma/ root.
"""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path

from pydantic import ValidationError
from pydantic_ai import Agent, BinaryContent

from config import AGENT_MODELS, CONTEXT_DOCS, SITES, VISION_AGENTS
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
    Issue,
)

# Max screenshots per vision agent call (Nemotron VL limit is 10)
MAX_IMAGES_PER_BATCH = 8

# Output-type map: agent_key → Pydantic model class
OUTPUT_MODELS: dict[str, type] = {
    "legal":       LegalReport,
    "consistency": ConsistencyReport,
    "editorial":   EditorialReport,
    "principles":  PrinciplesReport,
    "mobile_ux":   MobileUXReport,
    "desktop_ux":  DesktopUXReport,
    "seo":         SEOReport,
    "conversion":  ConversionReport,
    "council":     CouncilReport,
}


def _json_schema_instruction(model_cls: type) -> str:
    """Return an instruction block telling the model to answer in JSON matching the schema."""
    schema = model_cls.model_json_schema()
    # Remove noisy $defs for brevity — keep just the top-level props
    compact = json.dumps(schema, indent=2)
    return (
        "\n\n---\n\n"
        "## RESPONSE FORMAT\n\n"
        "You MUST respond with a single JSON object (no markdown fences, no commentary "
        "before or after).  The JSON must conform to this schema:\n\n"
        f"```json\n{compact}\n```\n\n"
        "Return ONLY the JSON object. Do NOT wrap it in ```json fences.\n"
    )


def _extract_json(text: str) -> dict:
    """Pull the first JSON object out of a model response (tolerant of LLM quirks).

    Handles: markdown fences, trailing commas, single quotes, extra text.
    """
    # Strip markdown code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"```\s*$", "", text.strip())
    # Find first { ... } block
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
    raw_json = text[start:end]

    # Try strict parse first
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError:
        pass

    # Fix common LLM JSON issues:
    # 1. Trailing commas before } or ]
    fixed = re.sub(r",\s*([}\]])", r"\1", raw_json)
    # 2. Single-quoted strings → double-quoted
    # (only safe heuristic: replace ' at string boundaries)
    # 3. Unquoted property names
    fixed = re.sub(r"(?<=[\{,])\s*(\w+)\s*:", r' "\1":', fixed)
    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass

    # Last resort: try eval-safe approach
    try:
        # Replace single quotes with double quotes (naive but often works)
        fixed2 = raw_json.replace("'", '"')
        fixed2 = re.sub(r",\s*([}\]])", r"\1", fixed2)
        return json.loads(fixed2)
    except (json.JSONDecodeError, ValueError):
        raise ValueError(f"Could not parse JSON from model response (first 500 chars): {raw_json[:500]}")

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
    """Combine dogma + brand context + source content + QC findings + JSON schema into a system prompt."""
    dogma = _load_dogma(agent_key, site_name)
    parts = [dogma, "\n\n---\n\n## Brand & Product Context\n\n", brand_context]

    if qc_report_text:
        parts.append("\n\n---\n\n")
        parts.append(qc_report_text)

    if source_content:
        parts.append("\n\n---\n\n")
        parts.append(source_content)

    # Append JSON schema instruction so models that lack tool_choice still
    # return structured data we can parse.
    model_cls = OUTPUT_MODELS.get(agent_key)
    if model_cls:
        parts.append(_json_schema_instruction(model_cls))

    return "".join(parts)


# ── Helper to build page data for prompts ────────────────────────────────────

def _format_crawl_data(crawl_data: list[dict], viewport_filter: str = "") -> str:
    """Format crawl data into a readable TEXT prompt section (no images)."""
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

### Page Content (excerpt):
{item['page_text'][:1500]}
"""
        pages.append(page)
    return "\n---\n".join(pages)


def _build_vision_prompt(
    crawl_data: list[dict],
    viewport_filter: str = "",
    max_images: int = MAX_IMAGES_PER_BATCH,
    text_chars: int = 1500,
) -> list:
    """Build a multimodal message with text + BinaryContent screenshots for vision agents.

    Returns a list of (str | BinaryContent) suitable for Pydantic AI's agent.run().
    Limits to `max_images` screenshots to stay within provider limits.
    `text_chars` controls how much page text excerpt each page gets.
    """
    parts: list = []

    # Lead-in text
    parts.append(
        "Review the following website pages. For each page you will see its metadata, "
        "content excerpt, AND a full-page screenshot. Examine the screenshots carefully "
        "for visual issues: layout, spacing, typography, hierarchy, responsiveness, touch targets, "
        "broken images, colour contrast, CTA visibility, and overall design quality.\n\n"
    )

    img_count = 0
    for item in crawl_data:
        if viewport_filter and item.get("viewport") != viewport_filter:
            continue

        # Text metadata for this page
        page_text = f"""
---
## Page: {item['page_path']} ({item['viewport']}, {item.get('viewport_width', '?')}x{item.get('viewport_height', '?')})
URL: {item['full_url']}
Load time: {item['load_time_ms']}ms | Words: {item['word_count']} | Links: {item['link_count']} | Images: {item['image_count']}
Title: {item['meta']['title']}
H1: {', '.join(item['meta']['h1']) if item['meta']['h1'] else '(none)'}
H2: {', '.join(item['meta']['h2'][:6]) if item['meta']['h2'] else '(none)'}
Meta Description: {item['meta']['description']}
Console Errors: {len([c for c in item['console_logs'] if c['type'] == 'error'])}
Network Errors: {len(item['network_errors'])}
Broken Images: {item['broken_images'][:5]}

Page Content (excerpt):
{item['page_text'][:text_chars]}
"""
        parts.append(page_text)

        # Inline screenshot as BinaryContent (base64 → raw bytes)
        b64 = item.get("screenshot_b64", "")
        if b64 and img_count < max_images:
            img_bytes = base64.b64decode(b64)
            parts.append(BinaryContent(data=img_bytes, media_type="image/png"))
            img_count += 1
        elif b64:
            parts.append("[Screenshot omitted — batch limit reached]\n")
        else:
            parts.append(f"[Screenshot not available: {item.get('screenshot_path', '?')}]\n")

    return parts


def _chunk_crawl_data(
    crawl_data: list[dict],
    viewport_filter: str = "",
    chunk_size: int = MAX_IMAGES_PER_BATCH,
) -> list[list[dict]]:
    """Split crawl data into chunks of `chunk_size` for batched vision calls."""
    filtered = [
        item for item in crawl_data
        if not viewport_filter or item.get("viewport") == viewport_filter
    ]
    return [filtered[i:i + chunk_size] for i in range(0, len(filtered), chunk_size)]


# ═══════════════════════════════════════════════════════════════════════════════
#  EXPERT AGENTS — per-site initialization (no API key needed at import time)
# ═══════════════════════════════════════════════════════════════════════════════

_agents_cache: dict[str, dict[str, Agent]] = {}  # site_name -> {agent_key -> Agent}


def _get_agents(
    site_name: str = "aitxpro",
    source_content: str = "",
    qc_report_text: str = "",
) -> dict[str, Agent]:
    """Create all agents for a site on first call. Requires OPENROUTER_API_KEY.

    All agents use output_type=str so no tool_choice is sent to the provider.
    JSON structure is requested in the system prompt and parsed after.
    """
    cache_key = f"{site_name}|{bool(source_content)}|{bool(qc_report_text)}"
    if cache_key in _agents_cache:
        return _agents_cache[cache_key]

    BRAND_CONTEXT = _load_context_docs(site_name)

    # Size control: source content per agent role
    FULL_SOURCE_AGENTS = {"council", "consistency", "editorial", "principles", "legal"}

    agent_keys = list(OUTPUT_MODELS.keys())

    site_agents = {}
    for key in agent_keys:
        if key in FULL_SOURCE_AGENTS:
            # Cap at 40K chars — system prompt + user msg must fit 131K tokens
            agent_source = source_content[:40_000]
            if len(source_content) > 40_000:
                agent_source += "\n...(source truncated to fit context window)"
        elif source_content:
            agent_source = source_content[:20_000]
            if len(source_content) > 20_000:
                agent_source += "\n...(source truncated for this agent)"
        else:
            agent_source = ""

        retries = 3 if key == "council" else 2
        # All agents return raw str — we parse JSON ourselves.
        # This avoids tool_choice which free models don't support.
        site_agents[key] = Agent(
            model=AGENT_MODELS[key],
            output_type=str,
            retries=retries,
            system_prompt=_build_system_prompt(
                key, BRAND_CONTEXT, site_name,
                source_content=agent_source,
                qc_report_text=qc_report_text,
            ),
        )

    _agents_cache[cache_key] = site_agents
    return site_agents


def _parse_agent_output(raw: str, agent_key: str):
    """Parse raw JSON string from model into the appropriate Pydantic model.

    Tolerant of common LLM quirks: markdown fences, extra text, stringified lists.
    """
    model_cls = OUTPUT_MODELS[agent_key]
    data = _extract_json(raw)

    # Common LLM quirk: list fields returned as comma-separated strings
    # Walk through and fix any that the schema expects as list[str]
    _fix_string_lists(data)

    return model_cls.model_validate(data)


def _fix_string_lists(data: dict) -> None:
    """Recursively convert comma-separated strings to lists where expected."""
    if not isinstance(data, dict):
        return
    for key, val in data.items():
        if isinstance(val, str) and "," in val and key in (
            "what_works", "what_breaks", "missing_elements", "flow_path",
            "top_priorities", "missing_policies", "gdpr_issues",
            "ai_sounding_phrases", "missing_aha_moments", "readability_notes",
            "missing_principles", "scroll_depth_concerns", "whitespace_issues",
            "canonical_issues", "cross_cutting_themes", "strengths",
            "quick_wins", "trust_signal_gaps", "messaging_gaps",
            "related_issues", "broken_images",
        ):
            data[key] = [s.strip() for s in val.split(",") if s.strip()]
        elif isinstance(val, dict):
            _fix_string_lists(val)
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    _fix_string_lists(item)


# ═══════════════════════════════════════════════════════════════════════════════
#  RUNNER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def run_expert(
    agent_key: str,
    crawl_data: list[dict],
    viewport_filter: str = "",
    site_name: str = "aitxpro",
    source_content: str = "",
    qc_report_text: str = "",
) -> ExpertReport:
    """Run a single expert agent against crawl data.

    Vision agents (mobile_ux, desktop_ux, seo) receive screenshots as
    BinaryContent in batches of MAX_IMAGES_PER_BATCH to stay within
    provider limits.  Multiple batches are merged into one report.

    All agents return raw text (no tool_choice).  We parse the JSON
    ourselves with the appropriate Pydantic model.
    """
    agents = _get_agents(site_name, source_content=source_content, qc_report_text=qc_report_text)
    agent = agents[agent_key]

    if agent_key in VISION_AGENTS:
        # Batch vision calls to respect the provider's per-prompt image limit
        chunks = _chunk_crawl_data(crawl_data, viewport_filter, MAX_IMAGES_PER_BATCH)
        if not chunks:
            chunks = [crawl_data]  # fallback

        all_issues: list[Issue] = []
        last_report: ExpertReport | None = None

        for batch_idx, chunk in enumerate(chunks):
            # Reduce text per page to stay under 128K context
            text_chars = 1200 if len(chunks) > 1 else 1500
            vision_parts = _build_vision_prompt(
                chunk, viewport_filter="",  # already filtered by chunk
                max_images=MAX_IMAGES_PER_BATCH,
                text_chars=text_chars,
            )
            suffix = ""
            if len(chunks) > 1:
                suffix = f"\n\n(Batch {batch_idx + 1}/{len(chunks)} — review these pages and report issues for THIS batch only)\n"
            prompt = [
                f"Review the following website crawl data and produce your expert report:{suffix}\n\n",
                *vision_parts,
            ]
            try:
                result = await agent.run(prompt)
                report = _parse_agent_output(result.output, agent_key)
                all_issues.extend(report.issues)
                last_report = report
            except Exception as e:
                print(f"    ⚠️  {agent_key} batch {batch_idx + 1}/{len(chunks)} failed: {e}")
                continue  # skip this batch, try next

        # Merge batches: keep the last report's summary/score but union all issues
        if last_report and len(chunks) > 1:
            last_report.issues = all_issues
        if last_report is None:
            raise RuntimeError(f"{agent_key}: all vision batches failed")
        return last_report

    else:
        # Text-only prompt for reasoning agents
        formatted = _format_crawl_data(crawl_data, viewport_filter)
        prompt = f"Review the following website crawl data and produce your expert report:\n\n{formatted}"
        result = await agent.run(prompt, model_settings={"max_tokens": 8000})
        return _parse_agent_output(result.output, agent_key)


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
    council = _parse_agent_output(result.output, "council")
    council.expert_reports = expert_reports
    return council
