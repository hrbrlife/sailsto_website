"""
HTML Report Generator — produces beautiful, readable HTML reports
from CouncilReport data with linked screenshots and navigation.
"""

from __future__ import annotations

import base64
import html
from datetime import datetime
from pathlib import Path
from typing import Optional
import shutil

from models import CouncilReport, ExpertReport, Issue

from config import REPORTS_DIR, SCREENSHOTS_DIR


def _severity_color(severity: str) -> str:
    return {
        "critical": "#ff4444",
        "warning": "#ffaa00",
        "suggestion": "#44aaff",
        "praise": "#44cc44",
    }.get(severity, "#888888")


def _severity_icon(severity: str) -> str:
    return {
        "critical": "🔴",
        "warning": "🟡",
        "suggestion": "🔵",
        "praise": "🟢",
    }.get(severity, "⚪")


def _severity_badge(severity: str) -> str:
    color = _severity_color(severity)
    icon = _severity_icon(severity)
    return f'<span class="badge" style="background:{color}">{icon} {severity.upper()}</span>'


def _grade_color(grade: str) -> str:
    return {
        "A": "#44cc44",
        "B": "#88cc44",
        "C": "#ffaa00",
        "D": "#ff6644",
        "F": "#ff4444",
    }.get(grade[0].upper() if grade else "C", "#888888")


def _score_color(score: int) -> str:
    if score >= 8:
        return "#44cc44"
    elif score >= 6:
        return "#ffaa00"
    else:
        return "#ff4444"


def _expert_icon(role: str) -> str:
    return {
        "legal": "⚖️",
        "consistency": "🔗",
        "editorial": "✍️",
        "principles": "🧭",
        "mobile_ux": "📱",
        "desktop_ux": "🖥️",
        "seo": "🔍",
        "conversion": "📈",
    }.get(role, "📊")


def _screenshot_img(screenshot_path: str, reports_dir: Path, assets_dir: Path | None = None) -> str:
    """Link to screenshot file (copied to assets dir) instead of base64 embedding."""
    if not screenshot_path:
        return ""

    # Find the source file
    full_path = reports_dir / screenshot_path
    if not full_path.exists():
        full_path = reports_dir.parent / screenshot_path
    if not full_path.exists():
        return f'<p class="screenshot-missing">📷 {html.escape(screenshot_path)}</p>'

    # Copy to assets dir if provided
    if assets_dir:
        assets_dir.mkdir(parents=True, exist_ok=True)
        dest = assets_dir / full_path.name
        if not dest.exists():
            try:
                shutil.copy2(full_path, dest)
            except Exception:
                pass
        rel_path = f"assets/{full_path.name}"
    else:
        rel_path = screenshot_path

    return f'''<details class="screenshot-details">
        <summary>📷 View Screenshot</summary>
        <img class="screenshot" src="{html.escape(rel_path)}" alt="{html.escape(screenshot_path)}" loading="lazy" />
    </details>'''


def _render_issue(issue: Issue, reports_dir: Path, assets_dir: Path | None = None) -> str:
    return f"""
    <div class="issue issue-{issue.severity}">
        <div class="issue-header">
            {_severity_badge(issue.severity)}
            <strong>{html.escape(issue.title)}</strong>
            <span class="issue-meta">{html.escape(issue.page)} · {html.escape(issue.viewport)}</span>
        </div>
        <p class="issue-desc">{html.escape(issue.description)}</p>
        <div class="recommendation">💡 {html.escape(issue.recommendation)}</div>
        {"<div class='evidence'>📝 " + html.escape(issue.evidence) + "</div>" if issue.evidence else ""}
        {_screenshot_img(issue.screenshot_ref, reports_dir, assets_dir) if issue.screenshot_ref else ""}
    </div>"""


def _render_expert_section(report: ExpertReport, reports_dir: Path, assets_dir: Path | None = None) -> str:
    issues_html = "\n".join(_render_issue(i, reports_dir, assets_dir) for i in report.issues)
    critical = sum(1 for i in report.issues if i.severity == "critical")
    warnings = sum(1 for i in report.issues if i.severity == "warning")
    suggestions = sum(1 for i in report.issues if i.severity == "suggestion")
    praises = sum(1 for i in report.issues if i.severity == "praise")
    icon = _expert_icon(report.expert_role)
    score_color = _score_color(report.overall_score)

    return f"""
    <section class="expert-report" id="{html.escape(report.expert_role)}">
        <div class="expert-header">
            <h2>{icon} {html.escape(report.expert_name)}</h2>
            <div class="score-circle" style="border-color: {score_color}; color: {score_color}">
                {report.overall_score}<span class="score-max">/10</span>
            </div>
        </div>
        <p class="expert-summary">{html.escape(report.summary)}</p>
        <div class="issue-stats">
            <span class="stat stat-critical">🔴 {critical} critical</span>
            <span class="stat stat-warning">🟡 {warnings} warnings</span>
            <span class="stat stat-suggestion">🔵 {suggestions} suggestions</span>
            <span class="stat stat-praise">🟢 {praises} praise</span>
        </div>
        <h3>Top Priorities</h3>
        <ol class="priorities">
            {"".join(f"<li>{html.escape(p)}</li>" for p in report.top_priorities)}
        </ol>
        <details open>
            <summary class="findings-toggle"><h3 style="display:inline">All Findings ({len(report.issues)})</h3></summary>
            <div class="issues-list">
                {issues_html}
            </div>
        </details>
    </section>"""


def generate_html_report(council: CouncilReport, reports_dir: Optional[Path] = None, assets_dir: Optional[Path] = None) -> str:
    """Generate a complete HTML report from a CouncilReport."""
    if reports_dir is None:
        reports_dir = REPORTS_DIR

    grade_color = _grade_color(council.overall_grade)

    # Navigation tabs for expert sections
    nav_items = "\n        ".join(
        f'<a href="#{html.escape(r.expert_role)}" class="nav-tab">'
        f'{_expert_icon(r.expert_role)} {html.escape(r.expert_name)} '
        f'<span class="nav-score" style="color:{_score_color(r.overall_score)}">{r.overall_score}</span></a>'
        for r in council.expert_reports
    )

    # Expert sections
    expert_sections = "\n".join(
        _render_expert_section(r, reports_dir, assets_dir) for r in council.expert_reports
    )

    # Score cards — use expert_reports if available, else fall back to expert_scores dict
    if council.expert_reports:
        score_cards = "\n            ".join(
            f'<div class="score-card">\n'
            f'                <div class="score-val" style="color:{_score_color(r.overall_score)}">{r.overall_score}</div>\n'
            f'                <div class="score-label">{_expert_icon(r.expert_role)} {html.escape(r.expert_name)}</div>\n'
            f'            </div>'
            for r in council.expert_reports
        )
    else:
        score_cards = "\n            ".join(
            f'<div class="score-card">\n'
            f'                <div class="score-val" style="color:{_score_color(s)}">{s}</div>\n'
            f'                <div class="score-label">{_expert_icon(n)} {html.escape(n)}</div>\n'
            f'            </div>'
            for n, s in council.expert_scores.items()
        )

    # Compute average score
    all_scores = [r.overall_score for r in council.expert_reports] if council.expert_reports else list(council.expert_scores.values())
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

    # Council decisions grouped by priority
    p0_decisions = [d for d in council.decisions if d.priority == "P0"]
    p1_decisions = [d for d in council.decisions if d.priority == "P1"]
    p2_decisions = [d for d in council.decisions if d.priority == "P2"]

    def render_decision_group(decisions, label, color):
        if not decisions:
            return ""
        items = "\n        ".join(
            f"""<div class="decision decision-{d.priority.lower()}">
            <div class="decision-header">
                <span class="priority-badge" style="background:{color}">{d.priority}</span>
                <span class="decision-category">{html.escape(d.category)}</span>
                <span class="decision-assignee">→ {html.escape(d.assigned_to)}</span>
            </div>
            <p class="decision-text"><strong>{html.escape(d.decision)}</strong></p>
            <p class="decision-rationale">{html.escape(d.rationale)}</p>
            {"<p class='decision-related'>Related: " + ", ".join(html.escape(r) for r in d.related_issues) + "</p>" if d.related_issues else ""}
        </div>"""
            for d in decisions
        )
        return f"""
        <div class="decision-group">
            <h3 class="decision-group-label" style="color:{color}">{label} ({len(decisions)})</h3>
            {items}
        </div>"""

    decisions_html = (
        render_decision_group(p0_decisions, "🚨 P0 — Fix Immediately", "#ff4444")
        + render_decision_group(p1_decisions, "⚠️ P1 — This Sprint", "#ffaa00")
        + render_decision_group(p2_decisions, "💡 P2 — Backlog", "#44aaff")
    )

    # Strengths + Quick wins + Cross-cutting with proper line breaks
    strengths_items = "\n                ".join(f"<li>{html.escape(s)}</li>" for s in council.strengths)
    quickwins_items = "\n                ".join(f"<li>{html.escape(q)}</li>" for q in council.quick_wins)
    crosscut_items = "\n                ".join(f"<li>{html.escape(t)}</li>" for t in council.cross_cutting_themes)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>QA Report — {html.escape(council.site_name)} — {html.escape(council.run_date)}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {{
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1a1a25;
    --surface3: #222233;
    --border: #2a2a3a;
    --text: #e0e0e8;
    --text-dim: #8888aa;
    --accent: #6c5ce7;
    --accent2: #00cec9;
    --radius: 12px;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding: 0;
}}
.container {{ max-width: 1100px; margin: 0 auto; padding: 2rem 1.5rem; }}

/* ── Header ── */
.report-header {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 3rem 2rem;
    border-bottom: 2px solid var(--border);
    text-align: center;
}}
.report-header h1 {{
    font-size: 1.8rem;
    margin-bottom: 0.3rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}}
.report-header .subtitle {{
    color: var(--text-dim);
    font-size: 1rem;
    margin-bottom: 1rem;
}}
.grade-display {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 90px; height: 90px;
    border-radius: 50%;
    font-size: 2.8rem;
    font-weight: 800;
    margin: 1rem 0;
    border: 4px solid;
    background: rgba(0,0,0,0.3);
}}
.grade-sub {{
    font-size: 0.9rem;
    color: var(--text-dim);
    margin-top: 0.25rem;
}}

/* ── Stats bar ── */
.stats-bar {{
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 1.5rem 0 0.5rem;
}}
.stat-card {{
    background: rgba(0,0,0,0.25);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.75rem 1.25rem;
    text-align: center;
    min-width: 100px;
}}
.stat-card .number {{ font-size: 1.8rem; font-weight: 700; }}
.stat-card .label {{ color: var(--text-dim); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }}

/* ── Scores grid ── */
.scores-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 0.75rem;
    margin: 1.5rem 0;
}}
.score-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 0.75rem;
    text-align: center;
    transition: border-color 0.2s;
}}
.score-card:hover {{ border-color: var(--accent); }}
.score-card .score-val {{ font-size: 2rem; font-weight: 700; }}
.score-card .score-label {{ font-size: 0.75rem; color: var(--text-dim); margin-top: 0.25rem; }}

/* ── Navigation ── */
.nav-tabs {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--border);
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
    position: sticky;
    top: 0;
    background: var(--bg);
    z-index: 100;
}}
.nav-tab {{
    padding: 0.5rem 0.85rem;
    border-radius: 8px;
    background: var(--surface);
    color: var(--text);
    text-decoration: none;
    font-size: 0.85rem;
    border: 1px solid var(--border);
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    white-space: nowrap;
}}
.nav-tab:hover {{ background: var(--surface2); border-color: var(--accent); }}
.nav-score {{
    background: var(--surface2);
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 0.8rem;
}}

/* ── Executive summary ── */
.executive {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem;
    margin-bottom: 2rem;
}}
.executive h2 {{ margin-bottom: 1rem; color: var(--accent2); font-size: 1.3rem; }}
.executive > p {{ margin-bottom: 1.25rem; line-height: 1.7; }}
.exec-columns {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-top: 1.5rem;
}}
.strengths h3, .quick-wins h3, .cross-cutting h3 {{
    font-size: 1rem;
    margin-bottom: 0.75rem;
}}
.strengths li, .quick-wins li, .cross-cutting li {{
    padding: 0.35rem 0;
    margin-left: 1.5rem;
    line-height: 1.5;
}}
.strengths li::marker {{ color: #44cc44; }}
.quick-wins li::marker {{ color: #ffaa00; }}
.cross-cutting li::marker {{ color: #6c5ce7; }}

/* ── Expert sections ── */
.expert-report {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem;
    margin-bottom: 1.5rem;
}}
.expert-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    gap: 1rem;
}}
.expert-header h2 {{ font-size: 1.4rem; }}
.score-circle {{
    width: 56px; height: 56px;
    border-radius: 50%;
    border: 3px solid;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    font-weight: 700;
    flex-shrink: 0;
    background: rgba(0,0,0,0.2);
}}
.score-max {{ font-size: 0.6rem; color: var(--text-dim); }}
.expert-summary {{ color: var(--text-dim); margin-bottom: 1rem; font-style: italic; line-height: 1.6; }}
.issue-stats {{ display: flex; gap: 0.75rem; margin: 1rem 0; flex-wrap: wrap; }}
.stat {{ padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; }}
.stat-critical {{ background: #ff444422; color: #ff6666; }}
.stat-warning {{ background: #ffaa0022; color: #ffcc44; }}
.stat-suggestion {{ background: #44aaff22; color: #66ccff; }}
.stat-praise {{ background: #44cc4422; color: #66ee66; }}
.priorities {{ margin: 0.5rem 0 1.25rem 1.5rem; }}
.priorities li {{ padding: 0.25rem 0; }}
.findings-toggle {{ cursor: pointer; list-style: none; padding: 0.5rem 0; }}
.findings-toggle::-webkit-details-marker {{ display: none; }}
.findings-toggle h3 {{ font-size: 1rem; color: var(--accent); display: inline; }}

/* ── Issues ── */
.issue {{
    border-left: 4px solid;
    background: var(--surface2);
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
}}
.issue-critical {{ border-left-color: #ff4444; }}
.issue-warning {{ border-left-color: #ffaa00; }}
.issue-suggestion {{ border-left-color: #44aaff; }}
.issue-praise {{ border-left-color: #44cc44; }}
.issue-header {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
    flex-wrap: wrap;
}}
.issue-meta {{ color: var(--text-dim); font-size: 0.8rem; margin-left: auto; }}
.issue-desc {{ margin-bottom: 0.5rem; line-height: 1.5; }}
.badge {{
    padding: 3px 9px;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 700;
    color: #fff;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
}}
.recommendation {{
    background: #6c5ce715;
    border: 1px solid #6c5ce733;
    border-radius: 6px;
    padding: 0.6rem 0.85rem;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: #b4a7ff;
    line-height: 1.5;
}}
.evidence {{
    background: #ffffff08;
    border-radius: 6px;
    padding: 0.6rem 0.85rem;
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: var(--text-dim);
    font-style: italic;
    line-height: 1.5;
    border-left: 2px solid var(--border);
}}
.screenshot-details {{ margin-top: 0.75rem; }}
.screenshot-details summary {{ cursor: pointer; color: var(--accent2); font-size: 0.85rem; }}
.screenshot {{
    max-width: 100%;
    border-radius: 8px;
    margin-top: 0.5rem;
    border: 1px solid var(--border);
}}
.screenshot-missing {{
    color: var(--text-dim);
    font-size: 0.85rem;
    font-style: italic;
}}

/* ── Council decisions ── */
.decisions-section {{
    margin-bottom: 2rem;
}}
.decisions-section > h2 {{ margin-bottom: 1.25rem; color: var(--accent); font-size: 1.3rem; }}
.decision-group {{ margin-bottom: 1.5rem; }}
.decision-group-label {{ font-size: 1rem; margin-bottom: 0.75rem; }}
.decision {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem;
    margin-bottom: 0.75rem;
}}
.decision-header {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
    flex-wrap: wrap;
}}
.priority-badge {{
    padding: 3px 9px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
    color: #fff;
    white-space: nowrap;
}}
.decision-category {{ color: var(--text-dim); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; }}
.decision-assignee {{ color: var(--accent2); font-size: 0.85rem; margin-left: auto; }}
.decision-text {{ margin: 0.5rem 0; line-height: 1.5; }}
.decision-rationale {{ color: var(--text-dim); font-size: 0.9rem; line-height: 1.5; }}
.decision-related {{ color: var(--text-dim); font-size: 0.8rem; font-style: italic; margin-top: 0.5rem; }}

/* ── Footer ── */
.report-footer {{
    text-align: center;
    padding: 2rem;
    color: var(--text-dim);
    font-size: 0.85rem;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
}}

/* ── Responsive ── */
@media (max-width: 768px) {{
    .container {{ padding: 1rem; }}
    .report-header {{ padding: 2rem 1rem; }}
    .report-header h1 {{ font-size: 1.4rem; }}
    .expert-header {{ flex-direction: column; text-align: center; gap: 0.5rem; }}
    .issue-header {{ flex-direction: column; align-items: flex-start; }}
    .issue-meta {{ margin-left: 0; }}
    .stats-bar {{ gap: 0.5rem; }}
    .stat-card {{ min-width: 80px; padding: 0.5rem 0.75rem; }}
    .stat-card .number {{ font-size: 1.3rem; }}
    .scores-grid {{ grid-template-columns: repeat(auto-fit, minmax(90px, 1fr)); }}
    .nav-tabs {{ gap: 0.3rem; }}
    .nav-tab {{ font-size: 0.75rem; padding: 0.4rem 0.6rem; }}
    .exec-columns {{ grid-template-columns: 1fr; }}
    .decision-header {{ flex-direction: column; align-items: flex-start; }}
    .decision-assignee {{ margin-left: 0; }}
}}
</style>
</head>
<body>

<header class="report-header">
    <h1>QA Council Report</h1>
    <p class="subtitle">{html.escape(council.site_name)} &mdash; {html.escape(council.run_date)}</p>
    <div class="grade-display" style="color:{grade_color}; border-color:{grade_color}">
        {html.escape(council.overall_grade)}
    </div>
    <p class="grade-sub">Average: {avg_score:.1f}/10 across {len(all_scores)} experts</p>
    <div class="stats-bar">
        <div class="stat-card">
            <div class="number" style="color:#ff6666">{council.critical_issues_count}</div>
            <div class="label">Critical</div>
        </div>
        <div class="stat-card">
            <div class="number" style="color:#ffcc44">{council.warning_count}</div>
            <div class="label">Warnings</div>
        </div>
        <div class="stat-card">
            <div class="number" style="color:#66ccff">{council.suggestion_count}</div>
            <div class="label">Suggestions</div>
        </div>
        <div class="stat-card">
            <div class="number" style="color:#66ee66">{council.praise_count}</div>
            <div class="label">Praise</div>
        </div>
    </div>
</header>

<div class="container">

    <!-- Expert Scores Overview -->
    <div class="scores-grid">
            {score_cards}
    </div>

    <!-- Navigation -->
    <nav class="nav-tabs">
        <a href="#executive-summary" class="nav-tab">📋 Overview</a>
        <a href="#decisions" class="nav-tab">🎯 Decisions</a>
        {nav_items}
    </nav>

    <!-- Executive Summary -->
    <div class="executive" id="executive-summary">
        <h2>📋 Executive Summary</h2>
        <p>{html.escape(council.executive_summary)}</p>

        <div class="exec-columns">
            <div class="strengths">
                <h3>✅ Strengths</h3>
                <ul>
                {strengths_items}
                </ul>
            </div>
            <div class="quick-wins">
                <h3>⚡ Quick Wins</h3>
                <ul>
                {quickwins_items}
                </ul>
            </div>
        </div>

        <div class="cross-cutting" style="margin-top: 1.5rem;">
            <h3>🔗 Cross-Cutting Themes</h3>
            <ul>
                {crosscut_items}
            </ul>
        </div>
    </div>

    <!-- Council Decisions -->
    <div class="decisions-section" id="decisions">
        <h2>🎯 Council Decisions ({len(council.decisions)})</h2>
        {decisions_html}
    </div>

    <!-- Expert Reports -->
    {expert_sections}

</div>

<footer class="report-footer">
    Generated by QA Council &middot; {html.escape(council.run_date)}<br>
    Powered by Pydantic AI + Playwright + OpenRouter
</footer>

</body>
</html>"""


def save_report(council: CouncilReport, output_dir: Optional[Path] = None) -> Path:
    """Save the HTML report and return the file path."""
    if output_dir is None:
        output_dir = REPORTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create assets directory for screenshots
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"qa-report-{council.site_name}-{timestamp}.html"
    filepath = output_dir / filename

    html_content = generate_html_report(council, output_dir, assets_dir)
    filepath.write_text(html_content)

    # Also save as latest
    latest = output_dir / f"qa-report-{council.site_name}-latest.html"
    latest.write_text(html_content)

    print(f"  Report saved → {filepath}")
    print(f"  Latest saved → {latest}")
    return filepath
