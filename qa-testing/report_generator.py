"""
HTML Report Generator — produces beautiful, readable HTML reports
from CouncilReport data with embedded screenshots and navigation.
"""

from __future__ import annotations

import base64
import html
from datetime import datetime
from pathlib import Path
from typing import Optional

from models import CouncilReport, ExpertReport, Issue

from config import REPORTS_DIR, SCREENSHOTS_DIR


def _severity_color(severity: str) -> str:
    return {
        "critical": "#ff4444",
        "warning": "#ffaa00",
        "suggestion": "#44aaff",
        "praise": "#44cc44",
    }.get(severity, "#888888")


def _severity_badge(severity: str) -> str:
    color = _severity_color(severity)
    return f'<span class="badge" style="background:{color}">{severity.upper()}</span>'


def _grade_color(grade: str) -> str:
    return {
        "A": "#44cc44",
        "B": "#88cc44",
        "C": "#ffaa00",
        "D": "#ff6644",
        "F": "#ff4444",
    }.get(grade[0].upper() if grade else "C", "#888888")


def _screenshot_img(screenshot_path: str, reports_dir: Path) -> str:
    """Try to embed screenshot as base64 or link to it."""
    if not screenshot_path:
        return ""
    # Try relative to reports dir
    full_path = reports_dir / screenshot_path
    if not full_path.exists():
        full_path = reports_dir.parent / screenshot_path
    if not full_path.exists():
        return f'<p class="screenshot-missing">📷 {html.escape(screenshot_path)}</p>'

    try:
        data = base64.b64encode(full_path.read_bytes()).decode()
        return f'<img class="screenshot" src="data:image/png;base64,{data}" alt="{html.escape(screenshot_path)}" loading="lazy" />'
    except Exception:
        return f'<a href="{html.escape(screenshot_path)}">📷 View screenshot</a>'


def _render_issue(issue: Issue, reports_dir: Path) -> str:
    return f"""
    <div class="issue issue-{issue.severity}">
        <div class="issue-header">
            {_severity_badge(issue.severity)}
            <strong>{html.escape(issue.title)}</strong>
            <span class="issue-meta">{html.escape(issue.page)} · {html.escape(issue.viewport)}</span>
        </div>
        <p>{html.escape(issue.description)}</p>
        <div class="recommendation">💡 {html.escape(issue.recommendation)}</div>
        {"<div class='evidence'>📝 " + html.escape(issue.evidence) + "</div>" if issue.evidence else ""}
        {_screenshot_img(issue.screenshot_ref, reports_dir) if issue.screenshot_ref else ""}
    </div>"""


def _render_expert_section(report: ExpertReport, reports_dir: Path) -> str:
    issues_html = "\n".join(_render_issue(i, reports_dir) for i in report.issues)
    critical = sum(1 for i in report.issues if i.severity == "critical")
    warnings = sum(1 for i in report.issues if i.severity == "warning")
    suggestions = sum(1 for i in report.issues if i.severity == "suggestion")
    praises = sum(1 for i in report.issues if i.severity == "praise")

    return f"""
    <section class="expert-report" id="{html.escape(report.expert_role)}">
        <div class="expert-header">
            <h2>{html.escape(report.expert_name)}</h2>
            <div class="score-circle" style="border-color: {'#44cc44' if report.overall_score >= 7 else '#ffaa00' if report.overall_score >= 5 else '#ff4444'}">
                {report.overall_score}<span class="score-max">/10</span>
            </div>
        </div>
        <p class="expert-summary">{html.escape(report.summary)}</p>
        <div class="issue-stats">
            <span class="stat stat-critical">{critical} critical</span>
            <span class="stat stat-warning">{warnings} warnings</span>
            <span class="stat stat-suggestion">{suggestions} suggestions</span>
            <span class="stat stat-praise">{praises} praise</span>
        </div>
        <h3>Top Priorities</h3>
        <ol class="priorities">
            {"".join(f"<li>{html.escape(p)}</li>" for p in report.top_priorities)}
        </ol>
        <h3>All Findings ({len(report.issues)})</h3>
        <div class="issues-list">
            {issues_html}
        </div>
    </section>"""


def generate_html_report(council: CouncilReport, reports_dir: Optional[Path] = None) -> str:
    """Generate a complete HTML report from a CouncilReport."""
    if reports_dir is None:
        reports_dir = REPORTS_DIR

    grade_color = _grade_color(council.overall_grade)

    # Navigation tabs for expert sections
    nav_items = "".join(
        f'<a href="#{html.escape(r.expert_role)}" class="nav-tab">{html.escape(r.expert_name)} '
        f'<span class="nav-score">{r.overall_score}</span></a>'
        for r in council.expert_reports
    )

    # Expert sections
    expert_sections = "\n".join(
        _render_expert_section(r, reports_dir) for r in council.expert_reports
    )

    # Council decisions
    decisions_html = ""
    for d in council.decisions:
        p_color = {"P0": "#ff4444", "P1": "#ffaa00", "P2": "#44aaff"}.get(d.priority, "#888")
        decisions_html += f"""
        <div class="decision decision-{d.priority.lower()}">
            <div class="decision-header">
                <span class="priority-badge" style="background:{p_color}">{d.priority}</span>
                <span class="decision-category">{html.escape(d.category)}</span>
                <span class="decision-assignee">→ {html.escape(d.assigned_to)}</span>
            </div>
            <p class="decision-text"><strong>{html.escape(d.decision)}</strong></p>
            <p class="decision-rationale">{html.escape(d.rationale)}</p>
            {"<p class='decision-related'>Related: " + ", ".join(html.escape(r) for r in d.related_issues) + "</p>" if d.related_issues else ""}
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>QA Council Report — {html.escape(council.site_name)} — {html.escape(council.run_date)}</title>
<style>
:root {{
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1a1a25;
    --border: #2a2a3a;
    --text: #e0e0e8;
    --text-dim: #8888aa;
    --accent: #6c5ce7;
    --accent2: #00cec9;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding: 0;
}}
.container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}

/* Header */
.report-header {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    padding: 3rem 2rem;
    border-bottom: 1px solid var(--border);
    text-align: center;
}}
.report-header h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
.report-header .subtitle {{ color: var(--text-dim); font-size: 1.1rem; }}
.grade-display {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 80px; height: 80px;
    border-radius: 50%;
    font-size: 2.5rem;
    font-weight: 800;
    margin: 1.5rem 0;
    border: 3px solid;
}}

/* Stats bar */
.stats-bar {{
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 1.5rem 0;
}}
.stat-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    text-align: center;
    min-width: 120px;
}}
.stat-card .number {{ font-size: 2rem; font-weight: 700; }}
.stat-card .label {{ color: var(--text-dim); font-size: 0.85rem; }}

/* Navigation */
.nav-tabs {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
    position: sticky;
    top: 0;
    background: var(--bg);
    z-index: 100;
}}
.nav-tab {{
    padding: 0.5rem 1rem;
    border-radius: 8px;
    background: var(--surface);
    color: var(--text);
    text-decoration: none;
    font-size: 0.9rem;
    border: 1px solid var(--border);
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}
.nav-tab:hover {{ background: var(--surface2); border-color: var(--accent); }}
.nav-score {{
    background: var(--surface2);
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 0.8rem;
}}

/* Executive summary */
.executive {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
}}
.executive h2 {{ margin-bottom: 1rem; color: var(--accent2); }}
.strengths, .quick-wins, .cross-cutting {{
    margin: 1.5rem 0;
}}
.strengths li, .quick-wins li, .cross-cutting li {{
    padding: 0.3rem 0;
    margin-left: 1.5rem;
}}
.strengths li::marker {{ color: #44cc44; }}
.quick-wins li::marker {{ color: #ffaa00; }}

/* Expert sections */
.expert-report {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
}}
.expert-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}}
.expert-header h2 {{ font-size: 1.5rem; }}
.score-circle {{
    width: 60px; height: 60px;
    border-radius: 50%;
    border: 3px solid;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 700;
    flex-shrink: 0;
}}
.score-max {{ font-size: 0.7rem; color: var(--text-dim); }}
.expert-summary {{ color: var(--text-dim); margin-bottom: 1rem; font-style: italic; }}
.issue-stats {{ display: flex; gap: 1rem; margin: 1rem 0; flex-wrap: wrap; }}
.stat {{ padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; }}
.stat-critical {{ background: #ff444433; color: #ff6666; }}
.stat-warning {{ background: #ffaa0033; color: #ffcc44; }}
.stat-suggestion {{ background: #44aaff33; color: #66ccff; }}
.stat-praise {{ background: #44cc4433; color: #66ee66; }}
.priorities {{ margin: 0.5rem 0 1.5rem 1.5rem; }}
.priorities li {{ padding: 0.2rem 0; }}

/* Issues */
.issue {{
    border-left: 4px solid;
    background: var(--surface2);
    border-radius: 0 8px 8px 0;
    padding: 1rem;
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
.issue-meta {{ color: var(--text-dim); font-size: 0.8rem; }}
.badge {{
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 700;
    color: #fff;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.recommendation {{
    background: #6c5ce722;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: #b4a7ff;
}}
.evidence {{
    background: #ffffff08;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: var(--text-dim);
    font-style: italic;
}}
.screenshot {{
    max-width: 100%;
    border-radius: 8px;
    margin-top: 0.75rem;
    border: 1px solid var(--border);
}}
.screenshot-missing {{
    color: var(--text-dim);
    font-size: 0.85rem;
    font-style: italic;
}}

/* Council decisions */
.decisions-section {{
    margin: 2rem 0;
}}
.decisions-section h2 {{ margin-bottom: 1rem; color: var(--accent); }}
.decision {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
    margin: 0.75rem 0;
}}
.decision-header {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}}
.priority-badge {{
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
    color: #fff;
}}
.decision-category {{ color: var(--text-dim); font-size: 0.85rem; text-transform: uppercase; }}
.decision-assignee {{ color: var(--accent2); font-size: 0.85rem; margin-left: auto; }}
.decision-text {{ margin: 0.5rem 0; }}
.decision-rationale {{ color: var(--text-dim); font-size: 0.9rem; }}
.decision-related {{ color: var(--text-dim); font-size: 0.8rem; font-style: italic; margin-top: 0.5rem; }}

/* Expert scores overview */
.scores-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}}
.score-card {{
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}}
.score-card .score-val {{ font-size: 2rem; font-weight: 700; }}
.score-card .score-label {{ font-size: 0.8rem; color: var(--text-dim); }}

/* Footer */
.report-footer {{
    text-align: center;
    padding: 2rem;
    color: var(--text-dim);
    font-size: 0.85rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}}

@media (max-width: 768px) {{
    .container {{ padding: 1rem; }}
    .report-header {{ padding: 2rem 1rem; }}
    .expert-header {{ flex-direction: column; text-align: center; }}
    .issue-header {{ flex-direction: column; align-items: flex-start; }}
    .stats-bar {{ flex-direction: column; align-items: center; }}
    .nav-tabs {{ justify-content: center; }}
}}
</style>
</head>
<body>

<header class="report-header">
    <h1>🔍 QA Council Report</h1>
    <p class="subtitle">{html.escape(council.site_name)} — {html.escape(council.run_date)}</p>
    <div class="grade-display" style="color:{grade_color}; border-color:{grade_color}">
        {html.escape(council.overall_grade)}
    </div>
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
        {"".join(f'''<div class="score-card">
            <div class="score-val" style="color:{"#44cc44" if s >= 7 else "#ffaa00" if s >= 5 else "#ff4444"}">{s}</div>
            <div class="score-label">{html.escape(n)}</div>
        </div>''' for n, s in council.expert_scores.items())}
    </div>

    <!-- Executive Summary -->
    <div class="executive">
        <h2>📋 Executive Summary</h2>
        <p>{html.escape(council.executive_summary)}</p>

        <div class="strengths">
            <h3>✅ Strengths</h3>
            <ul>{"".join(f"<li>{html.escape(s)}</li>" for s in council.strengths)}</ul>
        </div>

        <div class="quick-wins">
            <h3>⚡ Quick Wins</h3>
            <ul>{"".join(f"<li>{html.escape(q)}</li>" for q in council.quick_wins)}</ul>
        </div>

        <div class="cross-cutting">
            <h3>🔗 Cross-Cutting Themes</h3>
            <ul>{"".join(f"<li>{html.escape(t)}</li>" for t in council.cross_cutting_themes)}</ul>
        </div>
    </div>

    <!-- Council Decisions -->
    <div class="decisions-section">
        <h2>🎯 Council Decisions ({len(council.decisions)})</h2>
        {decisions_html}
    </div>

    <!-- Navigation -->
    <nav class="nav-tabs">
        <a href="#executive-summary" class="nav-tab">Overview</a>
        {nav_items}
    </nav>

    <!-- Expert Reports -->
    {expert_sections}

</div>

<footer class="report-footer">
    Generated by QA Council · {html.escape(council.run_date)} · Powered by Pydantic AI + Playwright + OpenRouter
</footer>

</body>
</html>"""


def save_report(council: CouncilReport, output_dir: Optional[Path] = None) -> Path:
    """Save the HTML report and return the file path."""
    if output_dir is None:
        output_dir = REPORTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"qa-report-{council.site_name}-{timestamp}.html"
    filepath = output_dir / filename

    html_content = generate_html_report(council, output_dir)
    filepath.write_text(html_content)

    # Also save as latest
    latest = output_dir / f"qa-report-{council.site_name}-latest.html"
    latest.write_text(html_content)

    print(f"  Report saved → {filepath}")
    print(f"  Latest saved → {latest}")
    return filepath
