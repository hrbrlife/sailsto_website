#!/usr/bin/env python3
"""
QA Council — Main Orchestrator

Crawls the site with Playwright, runs expert AI agents in parallel,
convenes a council, and generates an HTML report.

Usage:
    export OPENROUTER_API_KEY="sk-or-..."
    python run.py                          # Full run: crawl + agents + report
    python run.py --crawl-only             # Just crawl, save data
    python run.py --agents-only            # Skip crawl, use saved data
    python run.py --site melusina-os       # Run for a specific site
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
from agents import (
    run_expert, run_council,
)
from report_generator import save_report


async def run_all_experts(crawl_data: list[dict]) -> list:
    """Run all expert agents in parallel against crawl data."""
    print("\n🤖 Running expert panel...")

    tasks = [
        ("Legal", run_expert("legal", crawl_data)),
        ("Consistency", run_expert("consistency", crawl_data)),
        ("Editorial", run_expert("editorial", crawl_data)),
        ("Principles", run_expert("principles", crawl_data)),
        ("Mobile UX", run_expert("mobile_ux", crawl_data, viewport_filter="mobile")),
        ("Desktop UX", run_expert("desktop_ux", crawl_data, viewport_filter="desktop")),
        ("SEO", run_expert("seo", crawl_data)),
        ("Conversion", run_expert("conversion", crawl_data)),
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
    parser = argparse.ArgumentParser(description="QA Council — Website Testing Suite")
    parser.add_argument("--crawl-only", action="store_true", help="Only crawl, skip agents")
    parser.add_argument("--agents-only", action="store_true", help="Skip crawl, use saved data")
    parser.add_argument("--site", type=str, default=None, help="Run for a specific site")
    args = parser.parse_args()

    if not args.crawl_only and not OPENROUTER_API_KEY:
        print("❌ Set OPENROUTER_API_KEY in your environment.")
        print("   export OPENROUTER_API_KEY='sk-or-...'")
        sys.exit(1)

    # Determine which sites to run
    sites = {args.site: SITES[args.site]} if args.site else SITES
    run_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    for site_name, site_cfg in sites.items():
        print(f"\n{'='*60}")
        print(f"  QA Council Session: {site_name}")
        print(f"  {run_date}")
        print(f"{'='*60}")

        # ── Phase 1: Crawl ──
        crawl_data_file = CRAWL_DATA_DIR / f"{site_name}.json"

        if args.agents_only and crawl_data_file.exists():
            print(f"\n📂 Loading saved crawl data from {crawl_data_file}")
            crawl_data = json.loads(crawl_data_file.read_text())
        else:
            print(f"\n🕷️  Crawling {site_name}...")
            from dataclasses import asdict
            results = await crawl_site(site_name, site_cfg)
            crawl_data = [asdict(r) for r in results]

            # Save crawl data
            CRAWL_DATA_DIR.mkdir(parents=True, exist_ok=True)
            crawl_data_file.write_text(json.dumps(crawl_data, indent=2, default=str))
            print(f"  Saved {len(crawl_data)} crawl results")

            if args.crawl_only:
                print(f"\n✅ Crawl complete. Data saved to {crawl_data_file}")
                continue

        # ── Phase 2: Expert Agents ──
        expert_reports = await run_all_experts(crawl_data)

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
        council = await run_council(expert_reports, site_name, run_date)
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
