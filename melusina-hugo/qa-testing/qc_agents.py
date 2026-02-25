"""
Pre-processing QC agents — run BEFORE the expert panel.

These agents scan the raw markdown source corpus for mechanical issues
that don't require domain expertise:

1. TerminologyQC  — inconsistent term usage, wrong casing of product names
2. ConsistencyQC  — capitalization mismatches, number/stat contradictions
3. StructureQC    — broken links, missing front matter, orphan pages

Their reports are injected into the expert agent prompts so the panel
can focus on higher-order judgement calls.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from content_loader import SiteCorpus, PageSource

# ═══════════════════════════════════════════════════════════════════════════════
#  QC REPORT MODELS
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class QCFinding:
    """A single QC finding."""
    category: str       # terminology | capitalization | stat | structure | link
    severity: str       # error | warning | info
    page: str           # page_path where found
    text: str           # the exact offending text
    context: str        # surrounding context (± 60 chars)
    recommendation: str # what to fix


@dataclass
class QCReport:
    """Aggregated QC report from all pre-processing checks."""
    site_name: str
    total_pages: int = 0
    total_words: int = 0
    findings: list[QCFinding] = field(default_factory=list)
    term_frequency: dict[str, int] = field(default_factory=dict)
    summary: str = ""

    @property
    def error_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")

    def format_for_prompt(self) -> str:
        """Format QC findings as a prompt section for expert agents."""
        if not self.findings:
            return "## Pre-Processing QC Report\n\nNo issues found. All terminology and formatting checks passed.\n"

        lines = [
            f"## Pre-Processing QC Report ({len(self.findings)} findings)\n",
            f"Scanned {self.total_pages} source files ({self.total_words:,} words).\n",
            f"Errors: {self.error_count} | Warnings: {self.warning_count}\n",
        ]

        # Group by category
        by_cat: dict[str, list[QCFinding]] = defaultdict(list)
        for f in self.findings:
            by_cat[f.category].append(f)

        for cat, items in sorted(by_cat.items()):
            lines.append(f"\n### {cat.upper()} ({len(items)} issues)")
            for item in items[:30]:  # Cap per category to avoid prompt bloat
                lines.append(
                    f"- [{item.severity}] **{item.page}**: `{item.text}` "
                    f"→ {item.recommendation}"
                )
            if len(items) > 30:
                lines.append(f"  ... and {len(items) - 30} more")

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
#  TERMINOLOGY QC
# ═══════════════════════════════════════════════════════════════════════════════

# Canonical terms → wrong variants (case-sensitive matching)
DEFAULT_TERM_RULES: dict[str, list[str]] = {
    "CrossSecurities": ["cross securities", "cross-securities",
                        "crosssecurities", "Crosssecurities", "Cross Securities",
                        "Cross-Securities", "CROSSSECURITIES"],
    "CrossConversion": ["cross conversion", "cross-conversion", "Crossconversion",
                        "crossconversion", "Cross Conversion", "Cross-Conversion",
                        "CROSSCONVERSION"],
    "CrossBonds": ["cross bonds", "Crossbonds", "crossbonds", "Cross Bonds",
                   "Cross-Bonds", "cross-bonds", "CROSSBONDS"],
    "CrossShares": ["cross shares", "Crossshares", "crossshares", "Cross Shares",
                    "Cross-Shares", "cross-shares", "CROSSSHARES"],
    "CrossRWA": ["cross RWA", "CrossRwa", "crossrwa", "Cross RWA", "Cross-RWA",
                 "cross-rwa", "CROSSRWA", "Crossrwa"],
    "OTC network": ["OTC Network", "otc network", "OTC exchange",
                    "OTC Exchange"],
    "broker-mediated": ["peer-to-peer", "P2P trading", "direct trading"],
    "Clearstream": ["clearstream", "CLEARSTREAM", "Clear Stream", "clear stream"],
    "Vienna MTF": ["vienna mtf", "Vienna exchange", "vienna exchange",
                   "Vienna Exchange", "ViennaMTF", "vienna MTF"],
    "soulbound": ["soul-bound", "soul bound", "Soul Bound", "Soul-Bound",
                  "Soulbound"],
    "Reg D": ["RegD", "Reg-D", "reg d", "reg D", "REG D"],
    "Reg S": ["RegS", "Reg-S", "reg s", "reg S", "REG S"],
    "DAO LLC": ["DAO-LLC", "dao llc", "dao LLC", "Dao LLC", "Dao Llc"],
    "ISIN": ["isin", "Isin", "I.S.I.N."],
    "Solana": ["solana", "SOLANA", "Sol chain"],
}

# Site-specific term rules loaded from dogma
SITE_TERM_RULES: dict[str, dict[str, list[str]]] = {
    "sails-to": {
        **DEFAULT_TERM_RULES,
        "private testing": ["coming soon", "launching soon", "available now",
                           "now live", "publicly available", "live"],
        "professional investor": ["retail investor", "general public",
                                  "anyone can invest"],
        "credential token": ["KYC NFT", "identity token", "ID token"],
        "technology infrastructure provider": ["exchange", "dealer",
                                                "broker-dealer platform"],
    },
    "melusina-os": {
        **DEFAULT_TERM_RULES,
        "Melusina OS": ["melusina os", "MelusinaOS", "melusina OS",
                        "MELUSINA OS", "Melusina-OS", "melusina-os"],
    },
    "aitxpro": {
        **DEFAULT_TERM_RULES,
        "AiTX.pro": ["AITX.pro", "aitx.pro", "Aitx.pro", "AiTx.pro",
                      "AITX PRO", "aitxpro", "AiTXpro", "Ai TX pro",
                      "AiTX Pro", "AiTX.Pro"],
        "MetaTrader 5": ["Metatrader 5", "metatrader 5", "MetaTrader5",
                         "MT5", "metatrader5", "Meta Trader 5"],
        "FSC": ["fsc", "Fsc", "F.S.C."],
        "Investment Dealer": ["investment dealer", "Investment dealer",
                              "investment Dealer", "INVESTMENT DEALER"],
        "B2B Prime Services EU": ["B2B Prime", "b2b prime", "B2B prime",
                                   "B2B Prime Services", "b2b prime services eu"],
        "Mauritius": ["mauritius", "MAURITIUS"],
        "intelligent brokerage infrastructure": ["smart brokerage",
                                                  "AI brokerage platform"],
        "multi-asset brokerage": ["multi asset brokerage",
                                   "multiasset brokerage"],
    },
}


def _find_context(text: str, pos: int, radius: int = 60) -> str:
    """Extract surrounding context around a match position."""
    start = max(0, pos - radius)
    end = min(len(text), pos + radius)
    ctx = text[start:end].replace("\n", " ").strip()
    if start > 0:
        ctx = "..." + ctx
    if end < len(text):
        ctx = ctx + "..."
    return ctx


def _is_in_html_attr_or_code(text: str, pos: int) -> bool:
    """Check if position is inside an HTML attribute, code block, or URL."""
    # Look backward for context
    lookback = text[max(0, pos - 150):pos]
    # Inside an HTML tag attribute (data-term=", class=", href=", etc.)
    if re.search(r'<[^>]*(?:data-\w+|class|id|href|src|alt)\s*=\s*["\'][^"\']*$',
                 lookback, re.IGNORECASE):
        return True
    # Inside <code>...</code> tags
    if re.search(r'<code>[^<]*$', lookback):
        return True
    # Inside a code fence
    before = text[:pos]
    open_fences = before.count("```")
    if open_fences % 2 == 1:  # odd number = inside a code block
        return True
    # Inside inline code
    line_start = text.rfind("\n", 0, pos)
    line_before = text[line_start:pos]
    if line_before.count("`") % 2 == 1:
        return True
    # Inside a URL
    if re.search(r'https?://[^\s]*$', lookback):
        return True
    return False


def run_terminology_qc(corpus: SiteCorpus) -> list[QCFinding]:
    """Scan all pages for wrong term variants."""
    findings = []
    rules = SITE_TERM_RULES.get(corpus.site_name, DEFAULT_TERM_RULES)

    for page in corpus.pages:
        text = page.body
        for canonical, wrong_variants in rules.items():
            for wrong in wrong_variants:
                # Case-sensitive search for exact wrong variant
                idx = 0
                while True:
                    pos = text.find(wrong, idx)
                    if pos == -1:
                        break
                    # Skip false positives inside HTML attributes, code, URLs
                    if not _is_in_html_attr_or_code(text, pos):
                        findings.append(QCFinding(
                            category="terminology",
                            severity="error" if canonical in (
                                "CrossSecurities", "CrossConversion",
                                "CrossBonds", "CrossShares", "CrossRWA",
                            ) else "warning",
                            page=page.page_path,
                            text=wrong,
                            context=_find_context(text, pos),
                            recommendation=f"Use '{canonical}' instead of '{wrong}'",
                        ))
                    idx = pos + len(wrong)

    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  CAPITALIZATION & NUMBER CONSISTENCY QC
# ═══════════════════════════════════════════════════════════════════════════════

# Numbers that should be consistent across all pages
CANONICAL_NUMBERS: dict[str, list[str]] = {
    "sails-to": {
        "0.75%": ["conversion fee", "CrossConversion fee"],
        "$150,000": ["minimum investment", "minimum"],
        "3%": ["security deposit", "guarantee"],
        "$600K": ["minimum issuance", "minimum raise"],
        "€3-5k": ["Vienna MTF", "MTF listing"],
    },
    "melusina-os": {},
    "aitxpro": {
        "GB21026537": ["FSC licence", "licence number", "license number"],
        "IDB/ATS": ["licence category", "dealer category"],
    },
}


def run_consistency_qc(corpus: SiteCorpus) -> list[QCFinding]:
    """Scan for capitalization inconsistencies and number mismatches."""
    findings = []

    # ── Capitalization of headings ──
    for page in corpus.pages:
        lines = page.body.split("\n")
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Check markdown headings for consistency
            if stripped.startswith("#"):
                heading = stripped.lstrip("#").strip()
                # Flag ALL-CAPS headings (except short acronyms)
                words = heading.split()
                if len(words) > 2 and all(w.isupper() and len(w) > 3 for w in words):
                    findings.append(QCFinding(
                        category="capitalization",
                        severity="warning",
                        page=page.page_path,
                        text=heading,
                        context=f"Line {i+1}: {stripped[:80]}",
                        recommendation="Use title case for headings, not ALL CAPS",
                    ))

    # ── Number consistency ──
    site_numbers = CANONICAL_NUMBERS.get(corpus.site_name, {})
    number_occurrences: dict[str, list[tuple[str, str]]] = defaultdict(list)

    for page in corpus.pages:
        text = page.body
        for canonical_num, contexts in site_numbers.items():
            for ctx_word in contexts:
                # Find the number near the context word
                for m in re.finditer(re.escape(ctx_word), text, re.IGNORECASE):
                    # Look for numbers in ±100 chars around the context word
                    region = text[max(0, m.start()-100):m.end()+100]
                    nums = re.findall(r'[\$€]?[\d,]+\.?\d*%?[KkMm]?', region)
                    for n in nums:
                        if n and len(n) > 1:
                            number_occurrences[ctx_word].append((n, page.page_path))

    # Check for inconsistent numbers for the same concept
    for concept, occurrences in number_occurrences.items():
        unique_nums = set(n for n, _ in occurrences)
        if len(unique_nums) > 1:
            findings.append(QCFinding(
                category="stat_mismatch",
                severity="error",
                page="(cross-page)",
                text=f"'{concept}' has inconsistent numbers: {unique_nums}",
                context="; ".join(f"{n} on {p}" for n, p in occurrences[:5]),
                recommendation=f"Standardize the number for '{concept}' across all pages",
            ))

    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  STRUCTURAL QC
# ═══════════════════════════════════════════════════════════════════════════════

def run_structure_qc(corpus: SiteCorpus) -> list[QCFinding]:
    """Check for structural issues: missing front matter, broken internal links, etc."""
    findings = []
    all_paths = {p.page_path for p in corpus.pages}

    for page in corpus.pages:
        # ── Missing required front matter ──
        if not page.front_matter.get("title"):
            findings.append(QCFinding(
                category="structure",
                severity="error",
                page=page.page_path,
                text="Missing title in front matter",
                context=page.raw_content[:120],
                recommendation="Add 'title:' to the YAML front matter",
            ))

        if not page.front_matter.get("description"):
            findings.append(QCFinding(
                category="structure",
                severity="warning",
                page=page.page_path,
                text="Missing description in front matter",
                context=page.raw_content[:120],
                recommendation="Add 'description:' for SEO meta description",
            ))

        # ── Internal broken links ──
        # Match markdown links like [text](/path/) or [text](path/)
        for m in re.finditer(r'\[([^\]]+)\]\((/[^)]+)\)', page.body):
            link_text, link_target = m.group(1), m.group(2)
            # Normalize: strip anchors and query params
            target = link_target.split("#")[0].split("?")[0]
            if not target.endswith("/"):
                target += "/"
            # Only check internal links (starting with /)
            if target.startswith("/") and target not in all_paths:
                # Could be a valid URL but not a content page (static asset, etc.)
                if not any(target.endswith(ext) for ext in
                           (".png", ".jpg", ".svg", ".css", ".js", ".pdf")):
                    findings.append(QCFinding(
                        category="broken_link",
                        severity="warning",
                        page=page.page_path,
                        text=f"[{link_text}]({link_target})",
                        context=_find_context(page.body, m.start()),
                        recommendation=f"Internal link to '{target}' — no matching content file found",
                    ))

    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  CROSS-PAGE LOGIC QC
# ═══════════════════════════════════════════════════════════════════════════════

def run_logic_qc(corpus: SiteCorpus) -> list[QCFinding]:
    """Detect logical contradictions and claim mismatches across pages."""
    findings = []

    # Collect all claims about specific topics
    claims: dict[str, list[tuple[str, str]]] = defaultdict(list)  # topic → [(claim, page)]

    for page in corpus.pages:
        text = page.body.lower()

        # Check for contradictory status claims
        if "coming soon" in text and corpus.site_name == "sails-to":
            findings.append(QCFinding(
                category="logic",
                severity="error",
                page=page.page_path,
                text="'coming soon' — all products should be 'private testing'",
                context=_find_context(page.body,
                                      page.body.lower().find("coming soon")),
                recommendation="Replace 'coming soon' with 'private testing' "
                               "per approved status",
            ))

        if "now live" in text or "publicly available" in text:
            findings.append(QCFinding(
                category="logic",
                severity="error",
                page=page.page_path,
                text="Claims product is live/publicly available",
                context=_find_context(page.body,
                                      max(page.body.lower().find("now live"),
                                          page.body.lower().find("publicly available"))),
                recommendation="All products are in 'private testing'",
            ))

        # Check for blockchain references that shouldn't be there
        if "ton " in text or "ton blockchain" in text or "toncoin" in text:
            if corpus.site_name == "sails-to":
                pos = max(
                    text.find("ton "),
                    text.find("ton blockchain"),
                    text.find("toncoin"),
                )
                findings.append(QCFinding(
                    category="logic",
                    severity="error",
                    page=page.page_path,
                    text="References TON blockchain",
                    context=_find_context(page.body, pos),
                    recommendation="Sails.to is Solana only. Remove TON references.",
                ))

        # Check for "exchange" used to describe sails.to itself
        for m in re.finditer(r'\b(exchange|dex|decentralized exchange)\b',
                             text):
            # Skip if in HTML attribute, code, or comparison context
            if _is_in_html_attr_or_code(page.body, m.start()):
                continue
            ctx = text[max(0, m.start()-80):m.end()+80]
            if ("not an" not in ctx and "isn't" not in ctx
                    and "versus" not in ctx and "compared" not in ctx
                    and "unlike" not in ctx and "traditional" not in ctx
                    and "vienna" not in ctx):
                if corpus.site_name == "sails-to":
                    findings.append(QCFinding(
                        category="logic",
                        severity="warning",
                        page=page.page_path,
                        text=m.group(0),
                        context=_find_context(page.body, m.start()),
                        recommendation="Sails.to is an OTC network, NOT an exchange/DEX. "
                                       "Check if this usage is describing sails.to vs. comparing.",
                    ))

    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_qc(corpus: SiteCorpus) -> QCReport:
    """Run all QC checks and produce an aggregated report."""
    report = QCReport(
        site_name=corpus.site_name,
        total_pages=corpus.total_files,
        total_words=corpus.total_words,
    )

    # Collect term frequency
    all_text = corpus.full_text()
    for term in ("CrossSecurities", "CrossConversion", "CrossBonds",
                 "CrossShares", "CrossRWA", "OTC", "broker", "ISIN",
                 "Clearstream", "Solana", "credential", "soulbound",
                 "Reg D", "Reg S", "DAO LLC", "private testing"):
        count = all_text.lower().count(term.lower())
        if count:
            report.term_frequency[term] = count

    # Run all checks
    print("  📋 Terminology QC...")
    report.findings.extend(run_terminology_qc(corpus))

    print("  📋 Consistency QC...")
    report.findings.extend(run_consistency_qc(corpus))

    print("  📋 Structure QC...")
    report.findings.extend(run_structure_qc(corpus))

    print("  📋 Logic QC...")
    report.findings.extend(run_logic_qc(corpus))

    # Sort by severity
    severity_order = {"error": 0, "warning": 1, "info": 2}
    report.findings.sort(key=lambda f: severity_order.get(f.severity, 9))

    report.summary = (
        f"QC scanned {report.total_pages} files ({report.total_words:,} words): "
        f"{report.error_count} errors, {report.warning_count} warnings."
    )

    return report
