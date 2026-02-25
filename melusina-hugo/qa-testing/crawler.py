"""
Playwright crawler – visits every page, captures screenshots, console logs,
network errors, meta tags, accessibility tree, and page HTML.
Produces a structured CrawlResult per page per viewport.

Screenshots are saved to disk AND base64-encoded into crawl data
so vision-capable agents (Nemotron VL) can inspect them directly.
"""

import asyncio
import base64
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

from playwright.async_api import async_playwright, Page, BrowserContext

from config import (
    SITES,
    VIEWPORTS,
    PLAYWRIGHT_TIMEOUT,
    SCREENSHOT_FULL_PAGE,
    SCREENSHOTS_DIR,
    CRAWL_DATA_DIR,
)


@dataclass
class MetaTags:
    title: str = ""
    description: str = ""
    og_title: str = ""
    og_description: str = ""
    og_image: str = ""
    canonical: str = ""
    viewport_meta: str = ""
    robots: str = ""
    h1: list[str] = field(default_factory=list)
    h2: list[str] = field(default_factory=list)
    lang: str = ""


@dataclass
class ConsoleEntry:
    type: str  # log, warning, error, info
    text: str
    url: str = ""


@dataclass
class NetworkError:
    url: str
    status: int
    status_text: str
    resource_type: str


@dataclass
class CrawlResult:
    site: str
    page_path: str
    full_url: str
    viewport: str
    viewport_width: int
    viewport_height: int
    screenshot_path: str
    screenshot_b64: str  # base64-encoded PNG for vision agents
    meta: MetaTags
    console_logs: list[ConsoleEntry] = field(default_factory=list)
    network_errors: list[NetworkError] = field(default_factory=list)
    page_text: str = ""  # visible text content
    html_snippet: str = ""  # first 5000 chars of body innerHTML
    load_time_ms: float = 0
    word_count: int = 0
    link_count: int = 0
    image_count: int = 0
    broken_images: list[str] = field(default_factory=list)


async def extract_meta(page: Page) -> MetaTags:
    """Extract SEO-relevant meta tags and headings."""
    meta = MetaTags()
    meta.title = await page.title()
    meta.lang = await page.evaluate("document.documentElement.lang || ''")

    selectors = {
        "description": "meta[name='description']",
        "og_title": "meta[property='og:title']",
        "og_description": "meta[property='og:description']",
        "og_image": "meta[property='og:image']",
        "robots": "meta[name='robots']",
        "viewport_meta": "meta[name='viewport']",
    }
    for attr, sel in selectors.items():
        el = await page.query_selector(sel)
        if el:
            setattr(meta, attr, await el.get_attribute("content") or "")

    canon = await page.query_selector("link[rel='canonical']")
    if canon:
        meta.canonical = await canon.get_attribute("href") or ""

    meta.h1 = await page.eval_on_selector_all("h1", "els => els.map(e => e.textContent.trim())")
    meta.h2 = await page.eval_on_selector_all("h2", "els => els.map(e => e.textContent.trim())")

    return meta


async def crawl_page(
    context: BrowserContext,
    site_name: str,
    base_url: str,
    page_path: str,
    viewport_name: str,
    vp: dict,
) -> CrawlResult:
    """Crawl a single page at a given viewport and collect all data."""
    page = await context.new_page()
    await page.set_viewport_size(vp)

    console_logs: list[ConsoleEntry] = []
    network_errors: list[NetworkError] = []

    page.on("console", lambda msg: console_logs.append(
        ConsoleEntry(type=msg.type, text=msg.text, url=msg.location.get("url", "") if msg.location else "")
    ))

    full_url = f"{base_url.rstrip('/')}{page_path}"

    # Track failed network requests
    async def handle_response(response):
        if response.status >= 400:
            network_errors.append(NetworkError(
                url=response.url,
                status=response.status,
                status_text=response.status_text,
                resource_type=response.request.resource_type,
            ))

    page.on("response", handle_response)

    import time
    start = time.monotonic()
    try:
        await page.goto(full_url, wait_until="networkidle", timeout=PLAYWRIGHT_TIMEOUT)
    except Exception:
        await page.goto(full_url, wait_until="load", timeout=PLAYWRIGHT_TIMEOUT)
    load_time = (time.monotonic() - start) * 1000

    # Wait a beat for JS rendering
    await page.wait_for_timeout(1500)

    # Screenshot — save to disk + base64 encode for vision agents
    slug = re.sub(r"[^a-z0-9]+", "-", page_path.strip("/").lower()) or "home"
    ss_path = SCREENSHOTS_DIR / site_name / viewport_name / f"{slug}.png"
    ss_path.parent.mkdir(parents=True, exist_ok=True)
    ss_bytes = await page.screenshot(full_page=SCREENSHOT_FULL_PAGE)
    ss_path.write_bytes(ss_bytes)
    ss_b64 = base64.b64encode(ss_bytes).decode("ascii")

    # Meta
    meta = await extract_meta(page)

    # Visible text
    page_text = await page.evaluate("document.body?.innerText || ''")
    word_count = len(page_text.split())

    # HTML snippet (first 5000 chars for AI inspection)
    html_snippet = await page.evaluate("(document.body?.innerHTML || '').substring(0, 5000)")

    # Links & images
    link_count = await page.eval_on_selector_all("a[href]", "els => els.length")
    image_count = await page.eval_on_selector_all("img", "els => els.length")

    # Broken images
    broken_images = await page.eval_on_selector_all(
        "img",
        """els => els.filter(e => !e.naturalWidth && e.src).map(e => e.src)"""
    )

    await page.close()

    return CrawlResult(
        site=site_name,
        page_path=page_path,
        full_url=full_url,
        viewport=viewport_name,
        viewport_width=vp["width"],
        viewport_height=vp["height"],
        screenshot_path=str(ss_path.relative_to(ss_path.parents[3])),
        screenshot_b64=ss_b64,
        meta=meta,
        console_logs=console_logs,
        network_errors=network_errors,
        page_text=page_text[:8000],  # cap for sanity
        html_snippet=html_snippet,
        load_time_ms=round(load_time, 1),
        word_count=word_count,
        link_count=link_count,
        image_count=image_count,
        broken_images=broken_images,
    )


async def crawl_site(site_name: str, site_cfg: dict) -> list[CrawlResult]:
    """Crawl all pages of a site at all viewports."""
    results = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context()

        for page_path in site_cfg["pages"]:
            for vp_name, vp in VIEWPORTS.items():
                print(f"  ↳ {site_name} {page_path} @ {vp_name}")
                result = await crawl_page(context, site_name, site_cfg["base_url"], page_path, vp_name, vp)
                results.append(result)

        await browser.close()
    return results


async def crawl_all() -> dict[str, list[CrawlResult]]:
    """Crawl all configured sites. Returns {site_name: [CrawlResult, ...]}."""
    all_results = {}
    for site_name, site_cfg in SITES.items():
        print(f"Crawling {site_name}...")
        all_results[site_name] = await crawl_site(site_name, site_cfg)
    return all_results


def save_crawl_data(all_results: dict[str, list[CrawlResult]]):
    """Save crawl results as JSON for agent consumption."""
    CRAWL_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for site_name, results in all_results.items():
        data = [asdict(r) for r in results]
        out = CRAWL_DATA_DIR / f"{site_name}.json"
        out.write_text(json.dumps(data, indent=2, default=str))
        print(f"  Saved {len(data)} crawl results → {out}")


if __name__ == "__main__":
    results = asyncio.run(crawl_all())
    save_crawl_data(results)
    total = sum(len(v) for v in results.values())
    print(f"\nDone: {total} pages crawled across {len(results)} sites.")
