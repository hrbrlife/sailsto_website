#!/usr/bin/env python3
"""
QA Council — Per-Page Consilium Architecture

Phase 1: Crawl site + load MD source -> build per-page bundles
Phase 2: For each page: 8 experts (parallel) -> per-page consilium -> save
Phase 3: Mega consilium from all per-page reports -> final report
Phase 4: Generate HTML mega report

Usage:
    python run.py                         # Full run
    python run.py --crawl-only            # Crawl only, save data
    python run.py --agents-only           # Use cached crawl data
    python run.py --resume                # Resume from last completed page
    python run.py --page /otc-desk/       # Evaluate a single page only
    python run.py --delay 5               # Seconds between pages (default 3)
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Ensure qa-testing dir is on path
sys.path.insert(0, str(Path(__file__).parent))

from config import SITES, CRAWL_DATA_DIR, REPORTS_DIR, OPENROUTER_API_KEY
from crawler import crawl_site
from content_loader import load_site_content, SiteCorpus
from qc_agents import run_all_qc
from agents import (
    EXPERT_KEYS,
    run_page_expert,
    run_page_council,
    run_mega_council,
)
from report_generator import save_mega_report

# Delay between pages to respect free-tier rate limits (seconds)
PAGE_DELAY = 3.0
COUNCIL_DELAY = 2.0


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE BUNDLE BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_page_bundles(
    crawl_data: list[dict],
    corpus: SiteCorpus,
    site_cfg: dict,
) -> list[dict]:
    """Build per-page data bundles.

    Pages are discovered dynamically from crawl data.  If the site config
    contains a ``pages`` list it is used as a filter / ordering hint; otherwise
    every unique ``page_path`` found in the crawl results becomes a page bundle.

    Returns list of:
        {page_path, md_source, crawl_items, page_title, page_url}

    For Hugo pages where all content lives in templates (body is empty),
    md_source will contain the raw front matter so agents still see page config.
    The crawl data's page_text provides the rendered content.
    """
    # Index crawl data by page_path
    crawl_by_page: dict[str, list[dict]] = {}
    for item in crawl_data:
        pp = item.get("page_path", "")
        crawl_by_page.setdefault(pp, []).append(item)

    # Index MD source by page_path — use raw_content when body is empty
    md_by_page: dict[str, tuple[str, str]] = {}  # page_path -> (source, title)
    for page in corpus.pages:
        source = page.body if page.body.strip() else page.raw_content
        md_by_page[page.page_path] = (source, page.front_matter.get("title", ""))

    # ── Determine page list ──────────────────────────────────────────────────
    # Primary: derive from crawl data (unique page paths, sorted)
    crawled_pages = sorted(set(item.get("page_path", "") for item in crawl_data))
    crawled_pages = [p for p in crawled_pages if p]  # drop empty strings

    configured_pages = site_cfg.get("pages", [])
    if configured_pages:
        # Config pages act as a filter: only keep pages that were also crawled,
        # but preserve configured ordering.  Any crawled page NOT in config
        # is appended at the end so nothing discovered is lost.
        ordered = [p for p in configured_pages if p in crawl_by_page]
        extra = [p for p in crawled_pages if p not in set(configured_pages)]
        page_list = ordered + extra
        if extra:
            print(f"  [page-bundles] {len(extra)} extra page(s) discovered from crawl data")
    else:
        page_list = crawled_pages
        print(f"  [page-bundles] {len(page_list)} pages discovered from crawl data (no config list)")

    base_url = site_cfg.get("base_url", "")
    bundles = []
    for page_path in page_list:
        crawl_items = crawl_by_page.get(page_path, [])
        md_source, fm_title = md_by_page.get(page_path, ("", ""))

        # Fall back to crawl meta title if no front matter title
        title = fm_title
        if not title and crawl_items:
            title = crawl_items[0].get("meta", {}).get("title", "")

        bundles.append({
            "page_path": page_path,
            "md_source": md_source,
            "crawl_items": crawl_items,
            "page_title": title,
            "page_url": f"{base_url}{page_path}",
        })

    return bundles


# ═══════════════════════════════════════════════════════════════════════════════
#  PER-PAGE EVALUATION
# ═══════════════════════════════════════════════════════════════════════════════

async def evaluate_page(
    page_path: str,
    md_source: str,
    crawl_items: list[dict],
    site_name: str,
    qc_excerpt: str,
    page_title: str = "",
    page_url: str = "",
) -> tuple[list, object | None]:
    """Run all 8 experts on one page, then synthesize into a consilium.

    Returns (expert_reports, page_consilium).
    Consilium may be None if too few experts succeeded.
    """
    # Phase 2a: Run 8 experts in parallel
    tasks = []
    for key in EXPERT_KEYS:
        tasks.append((key, run_page_expert(
            agent_key=key,
            page_path=page_path,
            md_source=md_source,
            crawl_items=crawl_items,
            site_name=site_name,
            qc_excerpt=qc_excerpt,
        )))

    results = await asyncio.gather(
        *(task for _, task in tasks),
        return_exceptions=True,
    )

    expert_reports = []
    failed_keys = []
    for (key, _), result in zip(tasks, results):
        if isinstance(result, Exception):
            print(f"      x {key} failed: {result}")
            failed_keys.append(key)
        else:
            print(f"      + {key}: {result.overall_score}/10 ({len(result.issues)} issues)")
            expert_reports.append(result)

    # Retry failed experts once
    if failed_keys:
        print(f"      Retrying {len(failed_keys)} failed expert(s): {failed_keys}")
        await asyncio.sleep(3)
        retry_tasks = []
        for key in failed_keys:
            retry_tasks.append((key, run_page_expert(
                agent_key=key,
                page_path=page_path,
                md_source=md_source,
                crawl_items=crawl_items,
                site_name=site_name,
                qc_excerpt=qc_excerpt,
            )))
        retry_results = await asyncio.gather(
            *(task for _, task in retry_tasks),
            return_exceptions=True,
        )
        for (key, _), result in zip(retry_tasks, retry_results):
            if isinstance(result, Exception):
                print(f"      x {key} retry failed: {result}")
            else:
                print(f"      + {key} (retry): {result.overall_score}/10 ({len(result.issues)} issues)")
                expert_reports.append(result)

    if len(expert_reports) < 3:
        print(f"    !! Only {len(expert_reports)} experts succeeded — skipping consilium")
        return expert_reports, None

    # Phase 2b: Per-page council
    await asyncio.sleep(COUNCIL_DELAY)
    try:
        consilium = await run_page_council(
            expert_reports=expert_reports,
            page_path=page_path,
            page_title=page_title,
            page_url=page_url,
            site_name=site_name,
        )
        print(f"    => Consilium: {consilium.overall_score}/10 — "
              f"{consilium.critical_count} critical, {consilium.warning_count} warnings")
        return expert_reports, consilium
    except Exception as e:
        print(f"    !! Per-page consilium LLM failed: {e}")
        print(f"    -> Building consilium from expert data (fallback)...")
        # Build a programmatic consilium from expert reports
        from models import PageConsilium, Issue
        scores = {r.expert_role: r.overall_score for r in expert_reports}
        avg = sum(scores.values()) / len(scores) if scores else 5
        all_issues = []
        for r in expert_reports:
            all_issues.extend(r.issues)
        # Sort issues: critical first, then warnings
        sev_order = {"critical": 0, "warning": 1, "suggestion": 2, "praise": 3}
        all_issues.sort(key=lambda i: sev_order.get(i.severity, 9))
        crit = sum(1 for i in all_issues if i.severity == "critical")
        warn = sum(1 for i in all_issues if i.severity == "warning")
        consilium = PageConsilium(
            page_path=page_path,
            page_title=page_title,
            page_url=page_url,
            executive_summary=f"Programmatic synthesis from {len(expert_reports)} experts. Average score: {avg:.1f}/10.",
            overall_score=round(avg),
            expert_scores=scores,
            critical_count=crit,
            warning_count=warn,
            top_issues=all_issues[:10],
            strengths=[f"{r.expert_name}: {r.summary[:80]}" for r in expert_reports if r.overall_score >= 7],
            top_recommendations=[p for r in expert_reports for p in r.top_priorities[:1]],
            expert_reports=expert_reports,
        )
        print(f"    => Fallback consilium: {consilium.overall_score}/10 — "
              f"{crit} critical, {warn} warnings")
        return expert_reports, consilium


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

async def main():
    parser = argparse.ArgumentParser(description="QA Council — Per-Page Consilium")
    parser.add_argument("--crawl-only", action="store_true", help="Only crawl, skip agents")
    parser.add_argument("--agents-only", action="store_true", help="Use saved crawl data")
    parser.add_argument("--resume", action="store_true", help="Resume from last saved page")
    parser.add_argument("--site", default="aitxpro", help="Site key")
    parser.add_argument("--page", type=str, help="Evaluate a single page path only")
    parser.add_argument("--delay", type=float, default=PAGE_DELAY, help="Seconds between pages")
    args = parser.parse_args()

    if not args.crawl_only and not OPENROUTER_API_KEY:
        print("ERROR: Set OPENROUTER_API_KEY")
        sys.exit(1)

    page_delay = args.delay

    site_name = args.site
    site_cfg = SITES[site_name]
    run_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    print(f"\n{'='*60}")
    print(f"  Per-Page Consilium: {site_name}")
    print(f"  {run_date}")
    n_cfg = len(site_cfg.get("pages", []))
    print(f"  Config pages: {n_cfg or 'auto-discover from crawl'}")
    print(f"  Architecture: 8 experts x N pages -> consilium -> mega")
    print(f"{'='*60}")

    # ── Phase 1: Crawl ──────────────────────────────────────────────────────
    crawl_data_file = CRAWL_DATA_DIR / f"{site_name}.json"
    crawl_b64_file = CRAWL_DATA_DIR / f"{site_name}-screenshots.json"

    if args.agents_only and crawl_data_file.exists():
        print(f"\n[Phase 1] Loading cached crawl data...")
        crawl_data = json.loads(crawl_data_file.read_text())
        if crawl_b64_file.exists():
            b64_map = json.loads(crawl_b64_file.read_text())
            for item in crawl_data:
                key = f"{item['page_path']}|{item['viewport']}"
                item["screenshot_b64"] = b64_map.get(key, "")
        print(f"  Loaded {len(crawl_data)} crawl results")
    else:
        print(f"\n[Phase 1] Crawling {site_name}...")
        from dataclasses import asdict
        results = await crawl_site(site_name, site_cfg)
        crawl_data = [asdict(r) for r in results]

        CRAWL_DATA_DIR.mkdir(parents=True, exist_ok=True)
        b64_map = {}
        slim_data = []
        for item in crawl_data:
            key = f"{item['page_path']}|{item['viewport']}"
            b64_map[key] = item.get("screenshot_b64", "")
            slim = {k: v for k, v in item.items() if k != "screenshot_b64"}
            slim_data.append(slim)
        crawl_data_file.write_text(json.dumps(slim_data, indent=2, default=str))
        crawl_b64_file.write_text(json.dumps(b64_map))
        print(f"  Saved {len(crawl_data)} crawl results")

        if args.crawl_only:
            print(f"\n  Crawl complete. Data saved.")
            return

    # ── Phase 1b: Load source content ────────────────────────────────────────
    print(f"\n[Phase 1b] Loading source content...")
    corpus = load_site_content(site_name)
    print(f"  {corpus.total_files} files, {corpus.total_words:,} words")

    # ── Phase 1c: QC pre-processing ─────────────────────────────────────────
    qc_excerpt = ""
    if corpus.pages:
        print(f"\n[Phase 1c] Running QC checks...")
        qc_report = run_all_qc(corpus)
        print(f"  {qc_report.summary}")
        qc_excerpt = qc_report.format_for_prompt()
        qc_dir = REPORTS_DIR / "qc" / site_name
        qc_dir.mkdir(parents=True, exist_ok=True)
        (qc_dir / "qc-report.txt").write_text(qc_excerpt)

    # ── Phase 1d: Build page bundles ─────────────────────────────────────────
    bundles = build_page_bundles(crawl_data, corpus, site_cfg)
    print(f"\n[Phase 1d] Built {len(bundles)} page bundles")
    for b in bundles:
        md_len = len(b["md_source"])
        crawl_n = len(b["crawl_items"])
        print(f"  {b['page_path']:40s} MD:{md_len:>6,} chars  Crawl:{crawl_n} viewports")

    # Filter to single page if requested
    if args.page:
        bundles = [b for b in bundles if b["page_path"] == args.page]
        if not bundles:
            print(f"ERROR: Page not found: {args.page}")
            sys.exit(1)
        print(f"\n  Single page mode: {args.page}")

    # ── Phase 2: Per-page evaluation ─────────────────────────────────────────
    consilium_dir = REPORTS_DIR / "consiliums" / site_name
    consilium_dir.mkdir(parents=True, exist_ok=True)
    experts_dir = REPORTS_DIR / "experts" / site_name
    experts_dir.mkdir(parents=True, exist_ok=True)

    # Load previously completed consiliums if resuming
    completed_consiliums: list = []
    completed_pages: set[str] = set()
    if args.resume:
        from models import PageConsilium
        for f in sorted(consilium_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text())
                pc = PageConsilium.model_validate(data)
                completed_consiliums.append(pc)
                completed_pages.add(pc.page_path)
                print(f"  Resumed: {pc.page_path} ({pc.overall_score}/10)")
            except Exception as e:
                print(f"  Could not resume {f.name}: {e}")

    page_consiliums = list(completed_consiliums)
    total_pages = len(bundles)
    remaining = total_pages - len(completed_pages)

    print(f"\n[Phase 2] Evaluating {total_pages} pages "
          f"({len(completed_pages)} cached, {remaining} remaining)")
    print(f"  Estimated calls: {remaining * 9} "
          f"(8 experts + 1 council per page)")

    for idx, bundle in enumerate(bundles, 1):
        page_path = bundle["page_path"]

        if page_path in completed_pages:
            print(f"\n[{idx}/{total_pages}] >> {page_path} (cached)")
            continue

        print(f"\n[{idx}/{total_pages}] {page_path}")
        print(f"  Title: {bundle['page_title']}")
        print(f"  MD: {len(bundle['md_source']):,} chars | "
              f"Crawl: {len(bundle['crawl_items'])} viewports")

        expert_reports, consilium = await evaluate_page(
            page_path=page_path,
            md_source=bundle["md_source"],
            crawl_items=bundle["crawl_items"],
            site_name=site_name,
            qc_excerpt=qc_excerpt,
            page_title=bundle["page_title"],
            page_url=bundle["page_url"],
        )

        # Save expert reports for this page
        page_slug = page_path.strip("/").replace("/", "_") or "home"
        for report in expert_reports:
            out = experts_dir / f"{page_slug}_{report.expert_role}.json"
            out.write_text(report.model_dump_json(indent=2))

        # Save consilium
        if consilium:
            page_consiliums.append(consilium)
            out = consilium_dir / f"{page_slug}.json"
            out.write_text(consilium.model_dump_json(indent=2, exclude={"expert_reports"}))
            print(f"    Saved -> {out.name}")

        # Rate-limit delay between pages
        if idx < total_pages:
            print(f"    Waiting {page_delay}s...")
            await asyncio.sleep(page_delay)

    if not page_consiliums:
        print("ERROR: No page consiliums generated.")
        return

    # ── Phase 3: Mega consilium ──────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"[Phase 3] MEGA CONSILIUM — synthesizing {len(page_consiliums)} page reports...")
    print(f"{'='*60}")

    try:
        mega = await run_mega_council(page_consiliums, site_name, run_date)
        print(f"  Grade: {mega.overall_grade}")
        print(f"  Average: {mega.average_score:.1f}/10")
        print(f"  Decisions: {len(mega.prioritized_decisions)}")

        # Save mega consilium JSON
        mega_json = REPORTS_DIR / f"mega-consilium-{site_name}.json"
        mega_json.write_text(
            mega.model_dump_json(indent=2, exclude={"page_consiliums"})
        )
    except Exception as e:
        print(f"  Mega consilium failed: {e}")
        print("  Building report from per-page data only...")
        from models import MegaConsilium, CouncilDecision
        scores = [pc.overall_score for pc in page_consiliums]
        avg = sum(scores) / len(scores) if scores else 0
        total_crit = sum(pc.critical_count for pc in page_consiliums)
        total_warn = sum(pc.warning_count for pc in page_consiliums)

        # Sort pages by score for worst/best
        sorted_pcs = sorted(page_consiliums, key=lambda pc: pc.overall_score)
        worst_pages = [
            {"page_path": pc.page_path, "score": pc.overall_score,
             "reason": f"{pc.critical_count} critical, {pc.warning_count} warnings"}
            for pc in sorted_pcs[:5]
        ]
        best_pages = [
            {"page_path": pc.page_path, "score": pc.overall_score,
             "reason": next((s for s in pc.strengths[:1]), "Solid overall")}
            for pc in sorted_pcs[-5:][::-1]
        ]

        # Collect strengths that appear on 3+ pages
        from collections import Counter
        strength_phrases = Counter()
        for pc in page_consiliums:
            for s in pc.strengths:
                # Use first 60 chars as key for dedup
                key = s[:60].lower()
                strength_phrases[key] = s
        # Pick top 5 unique strengths from highest-scoring pages
        site_strengths = []
        seen = set()
        for pc in sorted_pcs[::-1]:  # best pages first
            for s in pc.strengths:
                k = s[:40].lower()
                if k not in seen:
                    site_strengths.append(s)
                    seen.add(k)
                if len(site_strengths) >= 5:
                    break
            if len(site_strengths) >= 5:
                break

        # Quick wins from top recommendations of worst pages
        quick_wins = []
        seen_qw = set()
        for pc in sorted_pcs:  # worst pages first
            for r in pc.top_recommendations[:2]:
                k = r[:40].lower()
                if k not in seen_qw:
                    quick_wins.append(r)
                    seen_qw.add(k)
                if len(quick_wins) >= 5:
                    break
            if len(quick_wins) >= 5:
                break

        # Cross-cutting themes: issues appearing on many pages
        theme_counter = Counter()
        for pc in page_consiliums:
            for iss in (pc.top_issues or []):
                title = getattr(iss, 'title', str(iss)) if not isinstance(iss, str) else iss
                theme_counter[title[:50].lower()] += 1
        cross_themes = [k.capitalize() for k, v in theme_counter.most_common(5) if v >= 2]
        if not cross_themes:
            cross_themes = ["Technical issues across multiple pages",
                           "Conversion optimization needed site-wide",
                           "Mobile UX improvements required"]

        # Build prioritized decisions from recurring critical issues
        decisions = []
        crit_issues = []
        for pc in page_consiliums:
            for iss in (pc.top_issues or []):
                sev = getattr(iss, 'severity', 'warning') if not isinstance(iss, str) else 'warning'
                if sev == 'critical':
                    crit_issues.append((pc.page_path, iss))
        # Deduplicate and take top 8
        seen_dec = set()
        for page_path, iss in crit_issues:
            title = getattr(iss, 'title', str(iss)) if not isinstance(iss, str) else iss
            desc = getattr(iss, 'description', '') if not isinstance(iss, str) else ''
            key = title[:40].lower()
            if key not in seen_dec:
                cat = getattr(iss, 'category', 'technical') if not isinstance(iss, str) else 'technical'
                decisions.append(CouncilDecision(
                    category=cat if isinstance(cat, str) else "technical",
                    decision=title,
                    rationale=f"Found on {page_path}: {desc[:100]}",
                    priority="P0" if len(decisions) < 3 else "P1",
                    assigned_to="dev" if "broken" in title.lower() or "404" in title.lower() else "content",
                ))
                seen_dec.add(key)
            if len(decisions) >= 8:
                break

        # Expert dimension summary
        expert_dim = {}
        for key in EXPERT_KEYS:
            expert_scores = [pc.expert_scores.get(key) for pc in page_consiliums
                            if pc.expert_scores.get(key) is not None]
            if expert_scores:
                eavg = sum(expert_scores) / len(expert_scores)
                expert_dim[key] = f"Average {eavg:.1f}/10 across {len(expert_scores)} pages"

        mega = MegaConsilium(
            site_name=site_name,
            run_date=run_date,
            executive_summary=(
                f"Site-wide QA evaluation of {len(page_consiliums)} pages found an average score of "
                f"{avg:.1f}/10 (Grade {'B' if avg >= 7 else 'C' if avg >= 5 else 'D' if avg >= 3 else 'F'}). "
                f"Identified {total_crit} critical issues and {total_warn} warnings. "
                f"Worst-performing areas: {sorted_pcs[0].page_path} ({sorted_pcs[0].overall_score}/10), "
                f"{sorted_pcs[1].page_path} ({sorted_pcs[1].overall_score}/10). "
                f"Best-performing: {sorted_pcs[-1].page_path} ({sorted_pcs[-1].overall_score}/10)."
            ),
            overall_grade="B" if avg >= 7 else "C" if avg >= 5 else "D" if avg >= 3 else "F",
            average_score=round(avg, 1),
            page_count=len(page_consiliums),
            total_critical=total_crit,
            total_warnings=total_warn,
            worst_pages=worst_pages,
            best_pages=best_pages,
            cross_cutting_themes=cross_themes,
            site_wide_strengths=site_strengths,
            prioritized_decisions=decisions,
            quick_wins=quick_wins,
            expert_dimension_summary=expert_dim,
            page_consiliums=page_consiliums,
        )

    # ── Phase 4: HTML report ─────────────────────────────────────────────────
    print(f"\n[Phase 4] Generating mega report...")
    report_path = save_mega_report(mega)

    print(f"\n{'='*60}")
    print(f"  Per-Page Consilium Complete: {site_name}")
    print(f"  Grade: {mega.overall_grade} | Average: {mega.average_score:.1f}/10")
    print(f"  Pages: {mega.page_count} | Critical: {mega.total_critical} | "
          f"Warnings: {mega.total_warnings}")
    print(f"  Report: {report_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
