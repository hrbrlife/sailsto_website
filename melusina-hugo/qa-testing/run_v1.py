#!/usr/bin/env python3
"""
QA Council — AiTX.pro Testing Suite

Crawls the site with Playwright, runs expert AI agents in parallel,
convenes a council, and generates an HTML report.

FREE-TIER models via OpenRouter:
  - Arcee Trinity Large Preview (text reasoning: council + experts)
  - NVIDIA Nemotron Nano 12B 2 VL (vision: UX + SEO with screenshots)

Usage:
    export OPENROUTER_API_KEY="sk-or-..."
    python run.py                          # Full run: crawl + agents + report
    python run.py --crawl-only             # Just crawl, save data
    python run.py --agents-only            # Skip crawl, use saved data
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
from crawler import crawl_all, crawl_site, save_crawl_data, CrawlResult
from content_loader import load_site_content, format_source_for_prompt
from qc_agents import run_all_qc
from agents import (
    run_expert, run_council,
)
from report_generator import save_report


async def run_all_experts(
    crawl_data: list[dict],
    site_name: str = "aitxpro",
    source_content: str = "",
    qc_report_text: str = "",
) -> list:
    """Run all expert agents in parallel against crawl data."""
    print("\n🤖 Running expert panel...")

    common = dict(
        site_name=site_name,
        source_content=source_content,
        qc_report_text=qc_report_text,
    )

    tasks = [
        ("Legal", run_expert("legal", crawl_data, viewport_filter="desktop", **common)),
        ("Consistency", run_expert("consistency", crawl_data, viewport_filter="desktop", **common)),
        ("Editorial", run_expert("editorial", crawl_data, viewport_filter="desktop", **common)),
        ("Principles", run_expert("principles", crawl_data, viewport_filter="desktop", **common)),
        ("Mobile UX", run_expert("mobile_ux", crawl_data, viewport_filter="mobile", **common)),
        ("Desktop UX", run_expert("desktop_ux", crawl_data, viewport_filter="desktop", **common)),
        ("SEO", run_expert("seo", crawl_data, viewport_filter="desktop", **common)),
        ("Conversion", run_expert("conversion", crawl_data, viewport_filter="desktop", **common)),
    ]

    # Run all agents in parallel
    results = await asyncio.gather(
        *(task for _, task in tasks),
        return_exceptions=True,
    )

    expert_reports = []
    for (name, _), result in zip(tasks, results):
        if isinstance(result, Exception):
            print(f"  ❌ {name} agent failed: {result}")
        else:
            print(f"  ✅ {name}: {result.overall_score}/10 — {len(result.issues)} issues")
            expert_reports.append(result)

    return expert_reports


async def main():
    parser = argparse.ArgumentParser(description="QA Council — AiTX.pro Testing Suite")
    parser.add_argument("--crawl-only", action="store_true", help="Only crawl, skip agents")
    parser.add_argument("--agents-only", action="store_true", help="Skip crawl, use saved data")
    parser.add_argument("--site", type=str, default="aitxpro", help="Site key (default: aitxpro)")
    args = parser.parse_args()

    if not args.crawl_only and not OPENROUTER_API_KEY:
        print("❌ Set OPENROUTER_API_KEY in your environment.")
        print("   export OPENROUTER_API_KEY='sk-or-...'")
        sys.exit(1)

    # Determine which site to run (only aitxpro in this module)
    sites = {args.site: SITES[args.site]}
    run_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    for site_name, site_cfg in sites.items():
        print(f"\n{'='*60}")
        print(f"  QA Council Session: {site_name}")
        print(f"  {run_date}")
        print(f"{'='*60}")

        # ── Phase 1: Crawl ──
        crawl_data_file = CRAWL_DATA_DIR / f"{site_name}.json"
        crawl_b64_file = CRAWL_DATA_DIR / f"{site_name}-screenshots.json"

        if args.agents_only and crawl_data_file.exists():
            print(f"\n📂 Loading saved crawl data from {crawl_data_file}")
            crawl_data = json.loads(crawl_data_file.read_text())
            # Re-attach base64 screenshots from separate file if available
            if crawl_b64_file.exists():
                b64_map = json.loads(crawl_b64_file.read_text())
                for item in crawl_data:
                    key = f"{item['page_path']}|{item['viewport']}"
                    item["screenshot_b64"] = b64_map.get(key, "")
                print(f"  Re-attached {len(b64_map)} screenshots from cache")
            else:
                # Fallback: read PNGs from disk and encode
                import base64
                for item in crawl_data:
                    ss_path = REPORTS_DIR / item.get("screenshot_path", "")
                    if ss_path.exists():
                        item["screenshot_b64"] = base64.b64encode(ss_path.read_bytes()).decode("ascii")
                    else:
                        item["screenshot_b64"] = ""
                print(f"  Re-encoded screenshots from disk PNGs")
        else:
            print(f"\n🕷️  Crawling {site_name}...")
            from dataclasses import asdict
            results = await crawl_site(site_name, site_cfg)
            crawl_data = [asdict(r) for r in results]

            # Save crawl data: slim JSON (no b64) + separate screenshot cache
            CRAWL_DATA_DIR.mkdir(parents=True, exist_ok=True)

            # Extract b64 screenshots into separate file (they're huge)
            b64_map = {}
            slim_data = []
            for item in crawl_data:
                key = f"{item['page_path']}|{item['viewport']}"
                b64_map[key] = item.get("screenshot_b64", "")
                slim = {k: v for k, v in item.items() if k != "screenshot_b64"}
                slim_data.append(slim)

            crawl_data_file.write_text(json.dumps(slim_data, indent=2, default=str))
            crawl_b64_file.write_text(json.dumps(b64_map))
            print(f"  Saved {len(crawl_data)} crawl results ({crawl_data_file.name} + screenshots cache)")

            if args.crawl_only:
                print(f"\n✅ Crawl complete. Data saved to {crawl_data_file}")
                continue

        # ── Phase 1b: Load MD source content ──
        print(f"\n📄 Loading source content for {site_name}...")
        corpus = load_site_content(site_name)
        if corpus.pages:
            print(f"  Loaded {corpus.total_files} files ({corpus.total_words:,} words)")
            source_content = format_source_for_prompt(corpus, max_chars=300_000)
        else:
            print(f"  ⚠️  No source content found (using crawl data only)")
            source_content = ""

        # ── Phase 1c: Pre-Processing QC ──
        qc_report_text = ""
        if corpus.pages:
            print(f"\n🔍 Running pre-processing QC checks...")
            qc_report = run_all_qc(corpus)
            print(f"  {qc_report.summary}")
            qc_report_text = qc_report.format_for_prompt()

            # Save QC report
            qc_dir = REPORTS_DIR / "qc" / site_name
            qc_dir.mkdir(parents=True, exist_ok=True)
            qc_file = qc_dir / "qc-report.txt"
            qc_file.write_text(qc_report_text)
            print(f"  Saved QC report to {qc_file}")

        # ── Phase 2: Expert Agents ──
        expert_reports = await run_all_experts(
            crawl_data, site_name=site_name,
            source_content=source_content,
            qc_report_text=qc_report_text,
        )

        if not expert_reports:
            print("  ❌ No expert reports generated. Check API key and model.")
            continue

        # Save individual expert reports
        experts_dir = REPORTS_DIR / "experts" / site_name
        experts_dir.mkdir(parents=True, exist_ok=True)
        for report in expert_reports:
            out = experts_dir / f"{report.expert_role}.json"
            out.write_text(report.model_dump_json(indent=2))

        # ── Phase 3: Council ──
        print(f"\n🏛️  Convening council with {len(expert_reports)} expert reports...")
        council = await run_council(
            expert_reports, site_name, run_date,
            source_content=source_content,
            qc_report_text=qc_report_text,
        )
        print(f"  Grade: {council.overall_grade}")
        print(f"  Decisions: {len(council.decisions)}")

        # Save council report as JSON
        council_json = REPORTS_DIR / f"council-{site_name}.json"
        council_json.write_text(council.model_dump_json(indent=2))

        # ── Phase 4: HTML Report ──
        print(f"\n📊 Generating HTML report...")
        report_path = save_report(council)

        print(f"\n{'='*60}")
        print(f"  ✅ QA Council Complete: {site_name}")
        print(f"  Grade: {council.overall_grade}")
        print(f"  Critical: {council.critical_issues_count} | Warnings: {council.warning_count}")
        print(f"  Report: {report_path}")
        print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
