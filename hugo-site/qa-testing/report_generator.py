"""
HTML Mega Report Generator — produces detailed per-page consilium reports
from MegaConsilium data with page-level drill-down and executive overview.

Report structure:
  1. Header: site grade, stats, date
  2. Page score heatmap table (all pages × all expert dimensions)
     — each score cell links to the individual expert report
  3. Executive summary + cross-cutting themes
  4. QC / Technical report section
  5. Prioritized decisions (P0/P1/P2)
  6. Per-page consilium sections (collapsed, expandable)
     — with links to individual expert reports and consilium JSONs
  7. Footer
"""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from models import MegaConsilium, PageConsilium, ExpertReport, Issue, CouncilDecision
from config import REPORTS_DIR


# ── Expert display config ────────────────────────────────────────────────────

EXPERT_ORDER = [
    "legal", "editorial", "principles", "consistency",
    "seo", "mobile_ux", "desktop_ux", "conversion",
]

EXPERT_SHORT = {
    "legal": "Legal", "editorial": "Edit", "principles": "Prin",
    "consistency": "Cons", "seo": "SEO", "mobile_ux": "M-UX",
    "desktop_ux": "D-UX", "conversion": "Conv",
}

EXPERT_ICON = {
    "legal": "&#9878;", "editorial": "&#9997;", "principles": "&#129517;",
    "consistency": "&#128279;", "seo": "&#128269;", "mobile_ux": "&#128241;",
    "desktop_ux": "&#128421;", "conversion": "&#128200;",
}

EXPERT_FULL = {
    "legal": "Legal & Regulatory", "editorial": "Editorial & Copy",
    "principles": "Brand Principles", "consistency": "Cross-Page Consistency",
    "seo": "SEO & Performance", "mobile_ux": "Mobile UX",
    "desktop_ux": "Desktop UX", "conversion": "Conversion & Funnel",
}


# ── Colour helpers ───────────────────────────────────────────────────────────

def _severity_color(severity: str) -> str:
    return {"critical": "#ff4444", "warning": "#ffaa00",
            "suggestion": "#44aaff", "praise": "#44cc44"}.get(severity, "#888")


def _severity_icon(severity: str) -> str:
    return {"critical": "&#128308;", "warning": "&#128992;",
            "suggestion": "&#128309;", "praise": "&#128994;"}.get(severity, "&#9898;")


def _grade_color(grade: str) -> str:
    g = grade[0].upper() if grade else "C"
    return {"A": "#44cc44", "B": "#88cc44", "C": "#ffaa00",
            "D": "#ff6644", "F": "#ff4444"}.get(g, "#888")


def _score_color(score: int) -> str:
    if score >= 8:
        return "#44cc44"
    elif score >= 6:
        return "#88cc44"
    elif score >= 4:
        return "#ffaa00"
    else:
        return "#ff4444"


def _score_bg(score: int) -> str:
    """Background colour for heatmap cells."""
    if score >= 8:
        return "rgba(68,204,68,0.2)"
    elif score >= 6:
        return "rgba(136,204,68,0.15)"
    elif score >= 4:
        return "rgba(255,170,0,0.15)"
    else:
        return "rgba(255,68,68,0.15)"


# ── Badge / icon helpers ─────────────────────────────────────────────────────

def _severity_badge(severity: str) -> str:
    color = _severity_color(severity)
    icon = _severity_icon(severity)
    return (f'<span class="badge" style="background:{color}">'
            f'{icon} {html.escape(severity.upper())}</span>')


def _page_slug(page_path: str) -> str:
    return page_path.strip("/").replace("/", "-") or "home"


def _screenshot_filename(page_path: str) -> str:
    """Convert page path to screenshot filename matching crawler convention."""
    slug = page_path.strip("/").replace("/", "-") or "home"
    return f"{slug}.png"


def _render_screenshots(page_path: str, site_name: str) -> str:
    """Render desktop + mobile screenshot side-by-side for a page."""
    fname = _screenshot_filename(page_path)
    desktop_path = REPORTS_DIR / "screenshots" / site_name / "desktop" / fname
    mobile_path = REPORTS_DIR / "screenshots" / site_name / "mobile" / fname

    # Build relative paths from reports/ root
    desktop_rel = f"screenshots/{site_name}/desktop/{fname}"
    mobile_rel = f"screenshots/{site_name}/mobile/{fname}"

    has_desktop = desktop_path.exists()
    has_mobile = mobile_path.exists()

    if not has_desktop and not has_mobile:
        return ""

    parts = ['<div class="screenshots-row">']
    if has_desktop:
        parts.append(
            f'<div class="screenshot-col">'
            f'<div class="screenshot-label">&#128421; Desktop (1440&times;900)</div>'
            f'<img class="page-screenshot" src="{html.escape(desktop_rel)}" '
            f'alt="Desktop screenshot of {html.escape(page_path)}" loading="lazy" />'
            f'</div>'
        )
    if has_mobile:
        parts.append(
            f'<div class="screenshot-col screenshot-col-mobile">'
            f'<div class="screenshot-label">&#128241; Mobile (390&times;844)</div>'
            f'<img class="page-screenshot" src="{html.escape(mobile_rel)}" '
            f'alt="Mobile screenshot of {html.escape(page_path)}" loading="lazy" />'
            f'</div>'
        )
    parts.append('</div>')
    return "\n".join(parts)


# ── Expert report file helpers ───────────────────────────────────────────────

def _expert_report_filename(page_path: str, expert_key: str) -> str:
    """Return the filename for an individual expert report HTML page."""
    slug = page_path.strip("/").replace("/", "_") or "home"
    return f"expert-{slug}-{expert_key}.html"


def _consilium_json_filename(page_path: str) -> str:
    """Return the filename for a consilium JSON (as saved by run.py)."""
    slug = page_path.strip("/").replace("/", "_") or "home"
    return f"{slug}.json"


def _expert_json_filename(page_path: str, expert_key: str) -> str:
    """Return the filename for an expert JSON (as saved by run.py)."""
    slug = page_path.strip("/").replace("/", "_") or "home"
    return f"{slug}_{expert_key}.json"


def _generate_expert_report_html(
    expert_data: dict,
    page_path: str,
    expert_key: str,
    site_name: str,
    back_link: str = "../mega-report-{site}-latest.html",
) -> str:
    """Generate a standalone HTML page for one expert's report on one page."""
    score = expert_data.get("overall_score", "?")
    expert_name = expert_data.get("expert_name", EXPERT_FULL.get(expert_key, expert_key))
    summary = expert_data.get("summary", "")
    issues = expert_data.get("issues", [])
    top_priorities = expert_data.get("top_priorities", [])
    icon = EXPERT_ICON.get(expert_key, "&#128202;")
    sc = _score_color(int(score)) if isinstance(score, (int, float)) else "#888"

    # Issues HTML
    issues_html_parts = []
    for iss in issues:
        sev = iss.get("severity", "suggestion")
        badge = _severity_badge(sev)
        title = html.escape(str(iss.get("title", "")))
        desc = html.escape(str(iss.get("description", "")))
        rec = html.escape(str(iss.get("recommendation", "")))
        evidence = iss.get("evidence", "")
        ev_html = f'<div class="evidence">&#128221; {html.escape(evidence)}</div>' if evidence else ""
        pg = html.escape(str(iss.get("page", page_path)))
        vp = html.escape(str(iss.get("viewport", "all")))
        issues_html_parts.append(f"""\
        <div class="issue issue-{sev}">
            <div class="issue-header">{badge} <strong>{title}</strong>
                <span class="issue-meta">{pg} &middot; {vp}</span>
            </div>
            <p class="issue-desc">{desc}</p>
            <div class="recommendation">&#128161; {rec}</div>
            {ev_html}
        </div>""")
    issues_html = "\n".join(issues_html_parts) if issues_html_parts else "<p>No issues found.</p>"

    # Top priorities
    prio_html = ""
    if top_priorities:
        items = "\n".join(f"<li>{html.escape(str(p))}</li>" for p in top_priorities)
        prio_html = f"<h3>&#127919; Top Priorities</h3><ol>{items}</ol>"

    # Expert-specific sections (five_second_test, persona_journeys, etc.)
    extra_html = ""
    for section_key in ["five_second_test", "persona_journeys", "funnel_leaks",
                        "dead_ends", "cta_issues", "meta_tags", "heading_structure",
                        "schema_markup", "layout_analysis", "typography", "navigation",
                        "touch_targets", "regulatory_flags", "required_disclosures",
                        "cross_site_gaps"]:
        val = expert_data.get(section_key)
        if val and val != [] and val != {}:
            pretty = json.dumps(val, indent=2, default=str) if isinstance(val, (dict, list)) else str(val)
            label = section_key.replace("_", " ").title()
            extra_html += (
                f'<details class="extra-section"><summary>{html.escape(label)}</summary>'
                f'<pre>{html.escape(pretty)}</pre></details>'
            )

    back_url = back_link.replace("{site}", site_name)

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(expert_name)} — {html.escape(page_path)} — Expert Report</title>
<style>
{REPORT_CSS}
.back-link {{ display: inline-block; padding: 0.5rem 1rem; margin-bottom: 1rem;
    background: var(--surface2); border: 1px solid var(--border); border-radius: 8px;
    color: var(--accent2); text-decoration: none; font-size: 0.9rem; }}
.back-link:hover {{ background: var(--surface3); }}
.expert-header {{ display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }}
.expert-score-big {{ font-size: 2.5rem; font-weight: 800; }}
.extra-section {{ margin: 0.75rem 0; }}
.extra-section summary {{ cursor: pointer; color: var(--accent); font-weight: 600; padding: 0.5rem 0; }}
.extra-section pre {{ background: var(--surface2); padding: 1rem; border-radius: 8px;
    overflow-x: auto; font-size: 0.85rem; color: var(--text); white-space: pre-wrap; }}
.json-link {{ display: inline-block; padding: 3px 10px; margin-left: 0.5rem;
    background: var(--surface2); border: 1px solid var(--border); border-radius: 6px;
    color: var(--accent2); text-decoration: none; font-size: 0.8rem; }}
.json-link:hover {{ background: var(--surface3); }}
</style>
</head>
<body>
<div class="container">
    <a href="{html.escape(back_url)}#page-{_page_slug(page_path)}" class="back-link">&larr; Back to Report</a>
    <a href="../experts/{site_name}/{_expert_json_filename(page_path, expert_key)}" class="json-link">RAW JSON</a>

    <header class="report-header" style="text-align:left; padding: 2rem">
        <div class="expert-header">
            <span style="font-size:2rem">{icon}</span>
            <div>
                <h1>{html.escape(expert_name)}</h1>
                <p class="subtitle">{html.escape(page_path)}</p>
            </div>
            <span class="expert-score-big" style="color:{sc};margin-left:auto">{score}/10</span>
        </div>
    </header>

    <div class="executive" style="margin-top:1.5rem">
        <h2>Summary</h2>
        <p>{html.escape(summary)}</p>
    </div>

    {prio_html}

    <div class="section" style="margin-top:1.5rem">
        <h2>Issues ({len(issues)})</h2>
        {issues_html}
    </div>

    {extra_html}
</div>
</body>
</html>"""


def _generate_all_expert_pages(mega: MegaConsilium, output_dir: Path) -> dict[str, dict[str, str]]:
    """Generate individual expert HTML pages for every page/expert combination.

    Returns a nested dict: {page_path: {expert_key: relative_filename}} for linking.
    Reads saved expert JSONs from reports/experts/{site_name}/.
    """
    site_name = mega.site_name
    experts_json_dir = REPORTS_DIR / "experts" / site_name
    expert_html_dir = output_dir / "expert-reports"
    expert_html_dir.mkdir(parents=True, exist_ok=True)

    link_map: dict[str, dict[str, str]] = {}

    for pc in mega.page_consiliums:
        page_path = pc.page_path
        slug = page_path.strip("/").replace("/", "_") or "home"
        link_map[page_path] = {}

        for expert_key in EXPERT_ORDER:
            json_file = experts_json_dir / f"{slug}_{expert_key}.json"
            if not json_file.exists():
                continue

            try:
                expert_data = json.loads(json_file.read_text())
            except Exception:
                continue

            fname = _expert_report_filename(page_path, expert_key)
            expert_html = _generate_expert_report_html(
                expert_data, page_path, expert_key, site_name,
            )
            (expert_html_dir / fname).write_text(expert_html)
            link_map[page_path][expert_key] = f"expert-reports/{fname}"

    return link_map


# ── Render helpers ───────────────────────────────────────────────────────────

def _render_issue(issue: Issue) -> str:
    evidence = ""
    if issue.evidence:
        evidence = (f'<div class="evidence">&#128221; '
                    f'{html.escape(issue.evidence)}</div>')
    return f"""\
    <div class="issue issue-{issue.severity}">
        <div class="issue-header">
            {_severity_badge(issue.severity)}
            <strong>{html.escape(issue.title)}</strong>
            <span class="issue-meta">{html.escape(issue.page)} &middot; {html.escape(issue.viewport)}</span>
        </div>
        <p class="issue-desc">{html.escape(issue.description)}</p>
        <div class="recommendation">&#128161; {html.escape(issue.recommendation)}</div>
        {evidence}
    </div>"""


def _render_decision(d: CouncilDecision, idx: int) -> str:
    color = {"P0": "#ff4444", "P1": "#ffaa00", "P2": "#44aaff"}.get(d.priority, "#888")
    related = ""
    if d.related_issues:
        related = (f'<p class="decision-related">Related: '
                   f'{", ".join(html.escape(r) for r in d.related_issues)}</p>')
    return f"""\
    <div class="decision">
        <div class="decision-header">
            <span class="priority-badge" style="background:{color}">{html.escape(d.priority)}</span>
            <span class="decision-idx">#{idx}</span>
            <span class="decision-category">{html.escape(d.category)}</span>
            <span class="decision-assignee">&rarr; {html.escape(d.assigned_to)}</span>
        </div>
        <p class="decision-text"><strong>{html.escape(d.decision)}</strong></p>
        <p class="decision-rationale">{html.escape(d.rationale)}</p>
        {related}
    </div>"""


def _render_page_score_table(
    consiliums: list[PageConsilium],
    expert_links: dict[str, dict[str, str]] | None = None,
) -> str:
    """Render the page × expert heatmap score table.

    If *expert_links* is provided, each score cell becomes a clickable link
    to the individual expert report HTML page.
    """
    if not consiliums:
        return "<p>No page data available.</p>"

    if expert_links is None:
        expert_links = {}

    # Header row
    headers = "".join(
        f'<th title="{html.escape(EXPERT_FULL.get(k, k))}">{html.escape(EXPERT_SHORT.get(k, k))}</th>'
        for k in EXPERT_ORDER
    )

    rows = []
    for pc in sorted(consiliums, key=lambda c: c.overall_score):
        slug = _page_slug(pc.page_path)
        sc = _score_color(pc.overall_score)
        page_links = expert_links.get(pc.page_path, {})

        cells = ""
        for k in EXPERT_ORDER:
            s = pc.expert_scores.get(k)
            bg = _score_bg(s) if s is not None else "transparent"
            col = _score_color(s) if s is not None else "#555"
            display = str(s) if s is not None else "-"
            link = page_links.get(k)
            if link and s is not None:
                cells += (f'<td style="background:{bg}"><a href="{html.escape(link)}" '
                          f'style="color:{col};font-weight:600;text-decoration:none" '
                          f'title="View {EXPERT_FULL.get(k,k)} report for {html.escape(pc.page_path)}">'
                          f'{display}</a></td>')
            else:
                cells += f'<td style="background:{bg};color:{col};font-weight:600">{display}</td>'

        # Consilium JSON link
        consilium_json = f"consiliums/{pc.page_path.strip('/').replace('/', '_') or 'home'}.json"
        consilium_link_exists = (REPORTS_DIR / consilium_json.replace("consiliums/", f"consiliums/{pc.page_path and '' or ''}")).exists() if False else True

        rows.append(
            f'<tr>'
            f'<td class="page-name"><a href="#page-{slug}">{html.escape(pc.page_path)}</a></td>'
            f'<td class="page-score" style="color:{sc};font-weight:700">{pc.overall_score}</td>'
            f'{cells}'
            f'<td style="color:#ff6666">{pc.critical_count}</td>'
            f'<td style="color:#ffcc44">{pc.warning_count}</td>'
            f'</tr>'
        )

    return f"""\
    <div class="table-wrap">
    <table class="score-table">
        <thead>
            <tr>
                <th class="col-page">Page</th>
                <th class="col-score">Score</th>
                {headers}
                <th>Crit</th>
                <th>Warn</th>
            </tr>
        </thead>
        <tbody>
            {"".join(rows)}
        </tbody>
    </table>
    </div>"""


def _render_page_section(
    pc: PageConsilium,
    idx: int,
    expert_links: dict[str, str] | None = None,
    site_name: str = "aitxpro",
) -> str:
    """Render one per-page consilium section (collapsed by default).

    *expert_links*: {expert_key: relative_html_path} for this page.
    """
    if expert_links is None:
        expert_links = {}

    slug = _page_slug(pc.page_path)
    sc = _score_color(pc.overall_score)
    is_open = "open" if pc.overall_score <= 4 else ""  # Auto-expand bad pages

    # Expert score badges — now clickable when links exist
    score_badges = ""
    for k in EXPERT_ORDER:
        s = pc.expert_scores.get(k)
        col = _score_color(s) if s is not None else "#555"
        label = EXPERT_SHORT.get(k, k)
        link = expert_links.get(k)
        if link and s is not None:
            score_badges += (
                f'<a href="{html.escape(link)}" class="expert-badge" '
                f'style="border-color:{col};text-decoration:none" '
                f'title="View full {EXPERT_FULL.get(k,k)} report">'
                f'<span class="eb-label">{html.escape(label)}</span>'
                f'<span class="eb-score" style="color:{col}">{s if s is not None else "-"}</span>'
                f'</a>'
            )
        else:
            score_badges += (
                f'<span class="expert-badge" style="border-color:{col}">'
                f'<span class="eb-label">{html.escape(label)}</span>'
                f'<span class="eb-score" style="color:{col}">{s if s is not None else "-"}</span>'
                f'</span>'
            )

    # Data files links bar
    file_slug = pc.page_path.strip("/").replace("/", "_") or "home"
    data_links = f'<div class="data-links">&#128193; '
    consilium_json = REPORTS_DIR / "consiliums" / site_name / f"{file_slug}.json"
    if consilium_json.exists():
        data_links += f'<a href="consiliums/{site_name}/{file_slug}.json" class="json-link">Consilium JSON</a> '
    for k in EXPERT_ORDER:
        expert_json = REPORTS_DIR / "experts" / site_name / f"{file_slug}_{k}.json"
        link = expert_links.get(k)
        if expert_json.exists() and link:
            data_links += f'<a href="{html.escape(link)}" class="json-link">{EXPERT_SHORT.get(k,k)}</a> '
    data_links += '</div>'

    # Strengths
    strengths_html = ""
    if pc.strengths:
        items = "\n".join(f"<li>{html.escape(s)}</li>" for s in pc.strengths)
        strengths_html = f'<div class="page-strengths"><h4>&#9989; Strengths</h4><ul>{items}</ul></div>'

    # Recommendations
    recs_html = ""
    if pc.top_recommendations:
        items = "\n".join(f"<li>{html.escape(r)}</li>" for r in pc.top_recommendations)
        recs_html = f'<div class="page-recs"><h4>&#128161; Top Recommendations</h4><ol>{items}</ol></div>'

    # Issues
    issues_html = ""
    if pc.top_issues:
        issue_items = "\n".join(_render_issue(i) for i in pc.top_issues)
        issues_html = f"""\
        <details class="issues-detail">
            <summary>All Issues ({len(pc.top_issues)})</summary>
            <div class="issues-list">{issue_items}</div>
        </details>"""

    # Screenshots
    screenshots_html = _render_screenshots(pc.page_path, site_name)

    return f"""\
    <details class="page-consilium" id="page-{slug}" {is_open}>
        <summary class="page-summary-bar">
            <span class="page-num">#{idx}</span>
            <span class="page-path">{html.escape(pc.page_path)}</span>
            <span class="page-title-text">{html.escape(pc.page_title)}</span>
            <span class="page-score-badge" style="color:{sc};border-color:{sc}">{pc.overall_score}/10</span>
            <span class="page-issues-count">
                <span style="color:#ff6666">{pc.critical_count}C</span> /
                <span style="color:#ffcc44">{pc.warning_count}W</span>
            </span>
        </summary>
        <div class="page-body">
            <p class="page-exec-summary">{html.escape(pc.executive_summary)}</p>
            <div class="expert-badges-row">{score_badges}</div>
            {data_links}
            <details class="screenshots-detail">
                <summary>&#128247; Screenshots</summary>
                {screenshots_html}
            </details>
            {strengths_html}
            {recs_html}
            {issues_html}
        </div>
    </details>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════════════════════════

REPORT_CSS = """\
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {
    --bg: #0a0a0f; --surface: #12121a; --surface2: #1a1a25; --surface3: #222233;
    --border: #2a2a3a; --text: #e0e0e8; --text-dim: #8888aa;
    --accent: #6c5ce7; --accent2: #00cec9; --radius: 12px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.6; padding: 0;
}
.container { max-width: 1200px; margin: 0 auto; padding: 2rem 1.5rem; }

/* Header */
.report-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 3rem 2rem; border-bottom: 2px solid var(--border); text-align: center;
}
.report-header h1 { font-size: 1.8rem; margin-bottom: 0.3rem; font-weight: 800; letter-spacing: -0.02em; }
.report-header .subtitle { color: var(--text-dim); font-size: 1rem; margin-bottom: 1rem; }
.grade-display {
    display: inline-flex; align-items: center; justify-content: center;
    width: 90px; height: 90px; border-radius: 50%; font-size: 2.8rem; font-weight: 800;
    margin: 1rem 0; border: 4px solid; background: rgba(0,0,0,0.3);
}
.stats-bar {
    display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin: 1.5rem 0 0.5rem;
}
.stat-card {
    background: rgba(0,0,0,0.25); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 0.75rem 1.25rem; text-align: center; min-width: 100px;
}
.stat-card .number { font-size: 1.8rem; font-weight: 700; }
.stat-card .label { color: var(--text-dim); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }

/* Score table / heatmap */
.table-wrap { overflow-x: auto; margin: 1.5rem 0; }
.score-table {
    width: 100%; border-collapse: collapse; font-size: 0.85rem;
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
}
.score-table th, .score-table td { padding: 0.5rem 0.6rem; text-align: center; border-bottom: 1px solid var(--border); }
.score-table th { background: var(--surface2); color: var(--text-dim); font-weight: 600; font-size: 0.75rem; text-transform: uppercase; white-space: nowrap; }
.score-table .col-page { text-align: left; min-width: 160px; }
.score-table .page-name { text-align: left; }
.score-table .page-name a { color: var(--accent2); text-decoration: none; }
.score-table .page-name a:hover { text-decoration: underline; }
.score-table tbody tr:hover { background: rgba(108,92,231,0.08); }

/* Section headings */
.section { margin-bottom: 2rem; }
.section > h2 { font-size: 1.3rem; margin-bottom: 1rem; color: var(--accent2); }

/* Executive summary */
.executive {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 2rem; margin-bottom: 2rem;
}
.executive h2 { margin-bottom: 1rem; color: var(--accent2); font-size: 1.3rem; }
.executive p { margin-bottom: 1rem; line-height: 1.7; }
.exec-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1.5rem; }
.exec-columns h3 { font-size: 1rem; margin-bottom: 0.75rem; }
.exec-columns li { padding: 0.3rem 0; margin-left: 1.5rem; }
.strengths li::marker { color: #44cc44; }
.quick-wins li::marker { color: #ffaa00; }
.themes li::marker { color: #6c5ce7; }

/* Dimension summary */
.dim-summary { margin-top: 1.5rem; }
.dim-card {
    background: var(--surface2); border: 1px solid var(--border); border-radius: 8px;
    padding: 0.75rem 1rem; margin-bottom: 0.5rem;
}
.dim-card strong { color: var(--accent2); }
.dim-card p { color: var(--text-dim); font-size: 0.9rem; margin-top: 0.25rem; }

/* Decisions */
.decision {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 1.25rem; margin-bottom: 0.75rem;
}
.decision-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem; flex-wrap: wrap; }
.priority-badge { padding: 3px 9px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; color: #fff; }
.decision-idx { color: var(--text-dim); font-size: 0.8rem; }
.decision-category { color: var(--text-dim); font-size: 0.85rem; text-transform: uppercase; }
.decision-assignee { color: var(--accent2); font-size: 0.85rem; margin-left: auto; }
.decision-text { margin: 0.5rem 0; line-height: 1.5; }
.decision-rationale { color: var(--text-dim); font-size: 0.9rem; line-height: 1.5; }
.decision-related { color: var(--text-dim); font-size: 0.8rem; font-style: italic; margin-top: 0.5rem; }

/* Per-page consilium */
.page-consilium {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); margin-bottom: 0.75rem;
}
.page-summary-bar {
    display: flex; align-items: center; gap: 0.75rem; padding: 0.85rem 1.25rem;
    cursor: pointer; list-style: none; flex-wrap: wrap;
}
.page-summary-bar::-webkit-details-marker { display: none; }
.page-num { color: var(--text-dim); font-size: 0.8rem; min-width: 2rem; }
.page-path { font-weight: 600; font-size: 0.95rem; min-width: 180px; }
.page-title-text { color: var(--text-dim); font-size: 0.85rem; flex: 1; }
.page-score-badge {
    font-weight: 700; font-size: 1rem; border: 2px solid; border-radius: 8px;
    padding: 2px 10px; background: rgba(0,0,0,0.2);
}
.page-issues-count { font-size: 0.8rem; color: var(--text-dim); white-space: nowrap; }
.page-body { padding: 0 1.25rem 1.25rem; }
.page-exec-summary { color: var(--text-dim); font-style: italic; margin-bottom: 1rem; line-height: 1.6; }

/* Expert badges row */
.expert-badges-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
.expert-badge {
    display: inline-flex; flex-direction: column; align-items: center;
    border: 1px solid var(--border); border-radius: 6px; padding: 4px 8px;
    background: var(--surface2); min-width: 50px;
}
.eb-label { font-size: 0.65rem; color: var(--text-dim); text-transform: uppercase; }
.eb-score { font-size: 1.1rem; font-weight: 700; }

/* Page strengths + recs */
.page-strengths, .page-recs { margin-bottom: 0.75rem; }
.page-strengths h4, .page-recs h4 { font-size: 0.9rem; margin-bottom: 0.4rem; }
.page-strengths ul, .page-recs ol { margin-left: 1.5rem; }
.page-strengths li, .page-recs li { padding: 0.2rem 0; font-size: 0.9rem; }

/* Screenshots */
.screenshots-detail { margin-bottom: 1rem; }
.screenshots-detail summary { cursor: pointer; color: var(--accent2); font-weight: 600; padding: 0.5rem 0; }
.screenshots-row { display: flex; gap: 1rem; margin-top: 0.75rem; flex-wrap: wrap; }
.screenshot-col { flex: 1; min-width: 300px; }
.screenshot-col-mobile { max-width: 220px; flex: 0 0 220px; }
.screenshot-label { font-size: 0.8rem; color: var(--text-dim); margin-bottom: 0.3rem; }
.page-screenshot {
    max-width: 100%; border-radius: 8px; border: 1px solid var(--border);
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

/* Issues */
.issues-detail { margin-top: 0.75rem; }
.issues-detail summary { cursor: pointer; color: var(--accent); font-weight: 600; padding: 0.5rem 0; }
.issue {
    border-left: 4px solid; background: var(--surface2); border-radius: 0 8px 8px 0;
    padding: 1rem 1.25rem; margin: 0.75rem 0;
}
.issue-critical { border-left-color: #ff4444; }
.issue-warning { border-left-color: #ffaa00; }
.issue-suggestion { border-left-color: #44aaff; }
.issue-praise { border-left-color: #44cc44; }
.issue-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem; flex-wrap: wrap; }
.issue-meta { color: var(--text-dim); font-size: 0.8rem; margin-left: auto; }
.issue-desc { margin-bottom: 0.5rem; line-height: 1.5; }
.badge {
    padding: 3px 9px; border-radius: 4px; font-size: 0.7rem; font-weight: 700;
    color: #fff; text-transform: uppercase; white-space: nowrap;
}
.recommendation {
    background: #6c5ce715; border: 1px solid #6c5ce733; border-radius: 6px;
    padding: 0.6rem 0.85rem; margin-top: 0.5rem; font-size: 0.9rem; color: #b4a7ff;
}
.evidence {
    background: #ffffff08; border-radius: 6px; padding: 0.6rem 0.85rem;
    margin-top: 0.5rem; font-size: 0.85rem; color: var(--text-dim); font-style: italic;
    border-left: 2px solid var(--border);
}

/* Nav */
.nav-tabs {
    display: flex; gap: 0.5rem; flex-wrap: wrap; padding: 0.75rem 0;
    border-bottom: 1px solid var(--border); border-top: 1px solid var(--border);
    margin: 1.5rem 0; position: sticky; top: 0; background: var(--bg); z-index: 100;
}
.nav-tab {
    padding: 0.5rem 0.85rem; border-radius: 8px; background: var(--surface);
    color: var(--text); text-decoration: none; font-size: 0.85rem;
    border: 1px solid var(--border); transition: all 0.2s;
}
.nav-tab:hover { background: var(--surface2); border-color: var(--accent); }

/* Footer */
.report-footer {
    text-align: center; padding: 2rem; color: var(--text-dim); font-size: 0.85rem;
    border-top: 1px solid var(--border); margin-top: 2rem;
}

/* Data file links */
.data-links { margin-bottom: 1rem; display: flex; gap: 0.4rem; flex-wrap: wrap; align-items: center; font-size: 0.85rem; color: var(--text-dim); }
.json-link { display: inline-block; padding: 3px 10px; background: var(--surface2); border: 1px solid var(--border); border-radius: 6px;
    color: var(--accent2); text-decoration: none; font-size: 0.75rem; white-space: nowrap; }
.json-link:hover { background: var(--surface3); border-color: var(--accent2); }

/* Clickable expert badges */
a.expert-badge { cursor: pointer; transition: all 0.2s; }
a.expert-badge:hover { background: var(--surface3); transform: translateY(-1px); }

/* Score table clickable cells */
.score-table td a { display: block; width: 100%; height: 100%; padding: 2px; }
.score-table td a:hover { text-decoration: underline !important; }

/* QC Report */
.qc-report { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; }
.qc-heading { font-size: 1.1rem; margin: 0.5rem 0; color: var(--accent2); }
.qc-subheading { font-size: 0.95rem; margin: 1rem 0 0.5rem; color: var(--text); }
.qc-finding { padding: 0.4rem 0.75rem; margin: 0.3rem 0; border-radius: 6px; font-size: 0.85rem; line-height: 1.5; }
.qc-error { background: rgba(255,68,68,0.08); border-left: 3px solid #ff4444; }
.qc-warning { background: rgba(255,170,0,0.08); border-left: 3px solid #ffaa00; }
.qc-info { background: rgba(68,170,255,0.08); border-left: 3px solid #44aaff; }
.qc-text { color: var(--text-dim); font-size: 0.9rem; margin: 0.3rem 0; }

/* Responsive */
@media (max-width: 768px) {
    .container { padding: 1rem; }
    .report-header { padding: 2rem 1rem; }
    .report-header h1 { font-size: 1.4rem; }
    .exec-columns { grid-template-columns: 1fr; }
    .page-summary-bar { font-size: 0.85rem; gap: 0.5rem; }
    .page-path { min-width: auto; }
    .score-table { font-size: 0.75rem; }
    .decision-header { flex-direction: column; align-items: flex-start; }
    .decision-assignee { margin-left: 0; }
}"""


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN REPORT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def _render_qc_section(site_name: str) -> str:
    """Render the QC / Technical Report section from saved qc-report.txt."""
    qc_file = REPORTS_DIR / "qc" / site_name / "qc-report.txt"
    if not qc_file.exists():
        return ""

    raw = qc_file.read_text().strip()
    if not raw:
        return ""

    # Parse the structured text into styled HTML
    lines = raw.split("\n")
    parts = ['<div class="qc-report">']
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            parts.append(f'<h3 class="qc-heading">{html.escape(stripped[3:])}</h3>')
        elif stripped.startswith("### "):
            parts.append(f'<h4 class="qc-subheading">{html.escape(stripped[4:])}</h4>')
        elif stripped.startswith("- [error]"):
            text = stripped[len("- [error] "):]
            parts.append(
                f'<div class="qc-finding qc-error">'
                f'<span class="badge" style="background:#ff4444">ERROR</span> '
                f'{html.escape(text)}</div>'
            )
        elif stripped.startswith("- [warning]"):
            text = stripped[len("- [warning] "):]
            parts.append(
                f'<div class="qc-finding qc-warning">'
                f'<span class="badge" style="background:#ffaa00">WARNING</span> '
                f'{html.escape(text)}</div>'
            )
        elif stripped.startswith("- [info]"):
            text = stripped[len("- [info] "):]
            parts.append(
                f'<div class="qc-finding qc-info">'
                f'<span class="badge" style="background:#44aaff">INFO</span> '
                f'{html.escape(text)}</div>'
            )
        elif stripped:
            parts.append(f'<p class="qc-text">{html.escape(stripped)}</p>')
    parts.append('</div>')
    return "\n".join(parts)


def generate_mega_report(
    mega: MegaConsilium,
    expert_links: dict[str, dict[str, str]] | None = None,
) -> str:
    """Generate complete HTML report from a MegaConsilium.

    *expert_links*: {page_path: {expert_key: relative_html_path}} for clickable drill-down.
    """
    consiliums = mega.page_consiliums
    grade_color = _grade_color(mega.overall_grade)
    if expert_links is None:
        expert_links = {}

    # ── Stats ────────────────────────────────────────────────────────────────
    total_issues = sum(
        len(pc.top_issues) for pc in consiliums
    )

    # ── Navigation tabs ──────────────────────────────────────────────────────
    nav_html = (
        '<a href="#score-table" class="nav-tab">&#128202; Score Table</a>'
        '<a href="#executive-summary" class="nav-tab">&#128203; Summary</a>'
        '<a href="#qc-section" class="nav-tab">&#128295; Technical QC</a>'
        '<a href="#decisions" class="nav-tab">&#127919; Decisions</a>'
        '<a href="#pages-section" class="nav-tab">&#128196; Pages</a>'
    )

    # ── Score table (with clickable cells) ───────────────────────────────────
    score_table_html = _render_page_score_table(consiliums, expert_links)

    # ── Executive summary ────────────────────────────────────────────────────
    strengths_items = "\n".join(
        f"<li>{html.escape(s)}</li>" for s in mega.site_wide_strengths
    ) if mega.site_wide_strengths else "<li>(none identified)</li>"

    quickwins_items = "\n".join(
        f"<li>{html.escape(q)}</li>" for q in mega.quick_wins
    ) if mega.quick_wins else "<li>(none identified)</li>"

    themes_items = "\n".join(
        f"<li>{html.escape(t)}</li>" for t in mega.cross_cutting_themes
    ) if mega.cross_cutting_themes else "<li>(none identified)</li>"

    # Expert dimension summaries
    dim_html = ""
    if mega.expert_dimension_summary:
        cards = ""
        for role, summary in mega.expert_dimension_summary.items():
            icon = EXPERT_ICON.get(role, "&#128202;")
            label = EXPERT_SHORT.get(role, role)
            cards += (
                f'<div class="dim-card"><strong>{icon} {html.escape(label)}</strong>'
                f'<p>{html.escape(summary)}</p></div>'
            )
        dim_html = f'<div class="dim-summary"><h3>Expert Dimension Summaries</h3>{cards}</div>'

    # Best / worst pages
    best_worst_html = ""
    if mega.best_pages or mega.worst_pages:
        bw_parts = []
        if mega.worst_pages:
            bw_parts.append("<h3 style='color:#ff6666'>&#128308; Worst Pages</h3><ul>")
            for p in mega.worst_pages:
                name = html.escape(str(p.get("page_path", p.get("page", "?"))))
                score = p.get("score", "?")
                reason = html.escape(str(p.get("reason", "")))
                bw_parts.append(f"<li><strong>{name}</strong> ({score}/10) — {reason}</li>")
            bw_parts.append("</ul>")
        if mega.best_pages:
            bw_parts.append("<h3 style='color:#44cc44'>&#128994; Best Pages</h3><ul>")
            for p in mega.best_pages:
                name = html.escape(str(p.get("page_path", p.get("page", "?"))))
                score = p.get("score", "?")
                reason = html.escape(str(p.get("reason", "")))
                bw_parts.append(f"<li><strong>{name}</strong> ({score}/10) — {reason}</li>")
            bw_parts.append("</ul>")
        best_worst_html = "\n".join(bw_parts)

    # ── QC / Technical Report ────────────────────────────────────────────────
    qc_html = _render_qc_section(mega.site_name)

    # ── Decisions ────────────────────────────────────────────────────────────
    decisions = mega.prioritized_decisions
    p0 = [d for d in decisions if d.priority == "P0"]
    p1 = [d for d in decisions if d.priority == "P1"]
    p2 = [d for d in decisions if d.priority == "P2"]

    def render_group(items, label, color):
        if not items:
            return ""
        cards = "\n".join(_render_decision(d, i+1) for i, d in enumerate(items))
        return (f'<div class="decision-group">'
                f'<h3 style="color:{color}">{label} ({len(items)})</h3>'
                f'{cards}</div>')

    decisions_html = (
        render_group(p0, "&#128680; P0 — Fix Immediately", "#ff4444")
        + render_group(p1, "&#9888;&#65039; P1 — This Sprint", "#ffaa00")
        + render_group(p2, "&#128161; P2 — Backlog", "#44aaff")
    )

    # ── Per-page sections (with expert links) ────────────────────────────────
    pages_html = "\n".join(
        _render_page_section(pc, idx+1, expert_links.get(pc.page_path, {}), mega.site_name)
        for idx, pc in enumerate(
            sorted(consiliums, key=lambda c: c.overall_score)
        )
    )

    # ── QC section HTML block ────────────────────────────────────────────────
    qc_section_html = ""
    if qc_html:
        qc_section_html = f"""\
    <!-- QC / Technical Report -->
    <div class="section" id="qc-section">
        <h2>&#128295; Technical QC Report</h2>
        <p style="color:var(--text-dim);margin-bottom:1rem">
            Pre-processing checks on source content: terminology, capitalisation,
            structure, and logic consistency.
        </p>
        {qc_html}
    </div>"""

    # ── Assemble ─────────────────────────────────────────────────────────────
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mega Consilium — {html.escape(mega.site_name)} — {html.escape(mega.run_date)}</title>
<style>
{REPORT_CSS}
</style>
</head>
<body>

<header class="report-header">
    <h1>Per-Page Consilium Report</h1>
    <p class="subtitle">{html.escape(mega.site_name)} &mdash; {html.escape(mega.run_date)}</p>
    <div class="grade-display" style="color:{grade_color}; border-color:{grade_color}">
        {html.escape(mega.overall_grade)}
    </div>
    <p class="subtitle">Average: {mega.average_score:.1f}/10 across {mega.page_count} pages</p>
    <div class="stats-bar">
        <div class="stat-card">
            <div class="number">{mega.page_count}</div>
            <div class="label">Pages</div>
        </div>
        <div class="stat-card">
            <div class="number" style="color:#ff6666">{mega.total_critical}</div>
            <div class="label">Critical</div>
        </div>
        <div class="stat-card">
            <div class="number" style="color:#ffcc44">{mega.total_warnings}</div>
            <div class="label">Warnings</div>
        </div>
        <div class="stat-card">
            <div class="number" style="color:#66ccff">{total_issues}</div>
            <div class="label">Total Issues</div>
        </div>
    </div>
</header>

<div class="container">

    <!-- Navigation -->
    <nav class="nav-tabs">
        {nav_html}
    </nav>

    <!-- Score Heatmap -->
    <div class="section" id="score-table">
        <h2>&#128202; Page Score Matrix</h2>
        <p style="color:var(--text-dim);margin-bottom:0.5rem;font-size:0.85rem">
            Click any score to view the full expert report for that page.
        </p>
        {score_table_html}
    </div>

    <!-- Executive Summary -->
    <div class="executive" id="executive-summary">
        <h2>&#128203; Executive Summary</h2>
        <p>{html.escape(mega.executive_summary)}</p>

        {best_worst_html}

        <div class="exec-columns">
            <div class="strengths">
                <h3>&#9989; Site-Wide Strengths</h3>
                <ul>{strengths_items}</ul>
            </div>
            <div class="quick-wins">
                <h3>&#9889; Quick Wins</h3>
                <ul>{quickwins_items}</ul>
            </div>
        </div>

        <div class="themes" style="margin-top:1.5rem">
            <h3>&#128279; Cross-Cutting Themes</h3>
            <ul>{themes_items}</ul>
        </div>

        {dim_html}
    </div>

    {qc_section_html}

    <!-- Decisions -->
    <div class="section" id="decisions">
        <h2>&#127919; Prioritized Decisions ({len(decisions)})</h2>
        {decisions_html if decisions_html else "<p>No decisions generated.</p>"}
    </div>

    <!-- Per-Page Consiliums -->
    <div class="section" id="pages-section">
        <h2>&#128196; Per-Page Consiliums ({len(consiliums)})</h2>
        <p style="color:var(--text-dim);margin-bottom:1rem">
            Pages sorted by score (worst first). Click to expand.
            <span style="color:#ff6666">Red pages</span> auto-expand.
            Expert badges link to individual reports.
        </p>
        {pages_html}
    </div>

</div>

<footer class="report-footer">
    Generated by Per-Page Consilium Engine &middot; {html.escape(mega.run_date)}<br>
    Architecture: 8 experts &times; {mega.page_count} pages &rarr; per-page consilium &rarr; mega consilium<br>
    Powered by Pydantic AI + Playwright + OpenRouter (Trinity Large Preview)
</footer>

</body>
</html>"""


def save_mega_report(
    mega: MegaConsilium,
    output_dir: Optional[Path] = None,
) -> Path:
    """Save the HTML report and return the file path.

    Also generates individual expert report HTML pages and links them from the
    main report's score matrix and per-page sections.
    """
    if output_dir is None:
        output_dir = REPORTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate individual expert report pages first
    print(f"  Generating individual expert report pages...")
    expert_links = _generate_all_expert_pages(mega, output_dir)
    n_pages = sum(len(v) for v in expert_links.values())
    print(f"  Generated {n_pages} expert report pages")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"mega-report-{mega.site_name}-{timestamp}.html"
    filepath = output_dir / filename

    html_content = generate_mega_report(mega, expert_links)
    filepath.write_text(html_content)

    # Also save as latest
    latest = output_dir / f"mega-report-{mega.site_name}-latest.html"
    latest.write_text(html_content)

    print(f"  Report saved -> {filepath}")
    print(f"  Latest saved -> {latest}")
    return filepath
