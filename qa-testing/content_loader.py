"""
Content loader — reads all markdown source files for a site and produces
a concatenated corpus for QC agents and expert panels.

Each site specifies its content_dir in config.py.
Files are read, stripped of Hugo front-matter, and indexed by page path.
"""

from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass, field

from config import SITES


@dataclass
class PageSource:
    """A single markdown source file with metadata."""
    rel_path: str           # e.g. "brokers.md" or "knowledge/glossary/isin.md"
    page_path: str          # e.g. "/brokers/" or "/knowledge/glossary/isin/"
    raw_content: str        # full file content including front matter
    body: str               # content with front matter stripped
    front_matter: dict      # parsed front matter (title, description, etc.)
    word_count: int = 0


@dataclass
class SiteCorpus:
    """All markdown source pages for a site."""
    site_name: str
    pages: list[PageSource] = field(default_factory=list)
    total_words: int = 0
    total_files: int = 0

    def full_text(self, max_chars: int = 0) -> str:
        """Concatenated text of all pages, optionally truncated."""
        parts = []
        total = 0
        for p in self.pages:
            header = f"\n{'='*60}\n## SOURCE: {p.page_path}\n{'='*60}\n"
            section = header + p.body
            if max_chars and total + len(section) > max_chars:
                remaining = max_chars - total
                if remaining > 200:
                    parts.append(section[:remaining] + "\n...(truncated)")
                break
            parts.append(section)
            total += len(section)
        return "\n".join(parts)

    def page_text(self, page_path: str) -> str | None:
        """Get body text for a specific page path."""
        for p in self.pages:
            if p.page_path == page_path or p.rel_path == page_path:
                return p.body
        return None


# ── Front-matter parsing ─────────────────────────────────────────────────────

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_front_matter(content: str) -> tuple[dict, str]:
    """Extract YAML front matter and return (fm_dict, body)."""
    m = _FM_RE.match(content)
    if not m:
        return {}, content

    fm_text = m.group(1)
    body = content[m.end():]

    # Simple key: value parser (no nested YAML needed)
    fm = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val:
                fm[key] = val
    return fm, body


def _rel_to_page_path(rel_path: str) -> str:
    """Convert a relative file path to a Hugo page path.

    Examples:
        _index.md          → /
        brokers.md         → /brokers/
        company/about.md   → /company/about/
        knowledge/glossary/_index.md → /knowledge/glossary/
    """
    # Remove .md extension
    p = rel_path.replace("\\", "/")
    if p.endswith(".md"):
        p = p[:-3]

    # Handle _index files
    if p.endswith("/_index") or p == "_index":
        p = p.replace("/_index", "").replace("_index", "")

    # Handle language-specific index (e.g. _index.fr)
    if p.endswith("/_index.fr") or p == "_index.fr":
        p = p.replace("/_index.fr", "").replace("_index.fr", "")

    # Ensure leading and trailing slashes
    if not p.startswith("/"):
        p = "/" + p
    if not p.endswith("/"):
        p = p + "/"

    return p


def load_site_content(site_name: str) -> SiteCorpus:
    """Load all markdown source files for a site.

    Returns a SiteCorpus with all pages indexed and parsed.
    """
    site_cfg = SITES.get(site_name)
    if not site_cfg:
        raise ValueError(f"Unknown site: {site_name}")

    content_dir = site_cfg.get("content_dir")
    if not content_dir:
        return SiteCorpus(site_name=site_name)

    content_path = Path(content_dir)
    if not content_path.exists():
        print(f"  ⚠️  Content dir not found: {content_path}")
        return SiteCorpus(site_name=site_name)

    corpus = SiteCorpus(site_name=site_name)
    md_files = sorted(content_path.rglob("*.md"))

    for md_file in md_files:
        rel_path = str(md_file.relative_to(content_path))
        raw = md_file.read_text(errors="replace")
        fm, body = _parse_front_matter(raw)
        page_path = _rel_to_page_path(rel_path)
        wc = len(body.split())

        corpus.pages.append(PageSource(
            rel_path=rel_path,
            page_path=page_path,
            raw_content=raw,
            body=body,
            front_matter=fm,
            word_count=wc,
        ))
        corpus.total_words += wc

    corpus.total_files = len(corpus.pages)
    return corpus


def format_source_for_prompt(corpus: SiteCorpus, max_chars: int = 200_000) -> str:
    """Format the corpus into a prompt-friendly string with clear page boundaries."""
    if not corpus.pages:
        return "(No source content available)"

    header = (
        f"## Markdown Source Content ({corpus.total_files} files, "
        f"{corpus.total_words:,} words)\n\n"
        f"Below is the raw markdown source for every page on the site. "
        f"Use this to verify terminology, capitalization, logic, and consistency.\n"
    )

    return header + corpus.full_text(max_chars=max_chars)
