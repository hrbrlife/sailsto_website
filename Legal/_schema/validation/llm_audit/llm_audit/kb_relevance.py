"""
KB Relevance Mapping System

This module implements a 4-step relevance mapping system:
1. Generate summaries for each KB source file
2. Analyze which KB sources are relevant to which document types
3. Build a relevance index mapping KB → Documents
4. Integrate relevance into the audit pipeline
"""

import json
import hashlib
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
import logging

from .providers import make_completion
from .config import load_config

logger = logging.getLogger(__name__)


# Document type categories based on the workspace structure
DOCUMENT_CATEGORIES = {
    "formation": {
        "description": "LLC formation documents, articles of organization, amendments",
        "patterns": ["Articles_of", "Formation", "Exhibit_A", "Exhibit_B"],
        "examples": ["A1_Articles_of_Organization.md", "D1_Articles_of_Amendment_Add_Series.md"]
    },
    "governance": {
        "description": "Operating agreements, officer appointments, policies, succession",
        "patterns": ["Operating_Agreement", "Officer_", "Succession", "Governance"],
        "examples": ["B1_Master_Operating_Agreement.md", "B3_Officer_Rotation_Succession_Policy.md"]
    },
    "compliance_bsa_aml": {
        "description": "BSA/AML programs, suspicious activity, currency transaction reporting",
        "patterns": ["BSA_AML", "AML", "SAR", "CTR"],
        "examples": ["B5_BSA_AML_Program.md"]
    },
    "compliance_privacy": {
        "description": "Privacy policies, data protection, GLBA, CCPA compliance",
        "patterns": ["Privacy", "Data_Protection", "GLBA", "CCPA"],
        "examples": ["B8_Privacy_Data_Protection_Policy.md"]
    },
    "compliance_security": {
        "description": "IT security, incident response, business continuity, disaster recovery",
        "patterns": ["IT_Security", "Incident", "BCP", "DRP"],
        "examples": ["B6_IT_Security_Incident_BCP_DRP.md"]
    },
    "compliance_records": {
        "description": "Record keeping policies and procedures",
        "patterns": ["Record_Keeping", "Records"],
        "examples": ["B4_Record_Keeping_Policy.md"]
    },
    "compliance_screening": {
        "description": "Customer due diligence, fit and proper screening, OFAC checks",
        "patterns": ["Fit_and_Proper", "Screening", "CDD", "KYC", "OFAC"],
        "examples": ["B9_Fit_and_Proper_Screening_Policy.md"]
    },
    "client_agreements": {
        "description": "Client services agreements, licensing frameworks, terms of service",
        "patterns": ["Client_Services", "Licensing_Framework", "Terms"],
        "examples": ["F1_Client_Services_Agreement.md", "B11_Client_Services_and_Licensing_Framework.md"]
    },
    "msb_registration": {
        "description": "MSB registration, FinCEN filings, state licensing",
        "patterns": ["MSB", "FinCEN", "Registration", "ABN"],
        "examples": ["C1_ABN_Registration_CCASH.md", "N5_Client_FinCEN_Filing_Guide.md"]
    },
    "checklists": {
        "description": "Filing checklists, compliance checklists, procedural guides",
        "patterns": ["Checklist", "Filing", "Instructions"],
        "examples": ["E1_Filing_Checklist_and_Instructions.md", "E2_Securities_and_MTL_Checklist.md"]
    },
    "insurance_capital": {
        "description": "Insurance requirements, capital adequacy, bonding",
        "patterns": ["Insurance", "Capital", "Bond"],
        "examples": ["B10_Insurance_and_Capital_Policy.md"]
    },
    "research_secondary": {
        "description": "LLM-generated research memos (secondary sources, weight 0.5)",
        "patterns": ["research_outputs", "RO-"],
        "examples": ["01_mt_msb_licensing_federal_overlay.md", "04_series_llc_msb_structural_analysis.md"],
        "weight": 0.5
    }
}


@dataclass
class KBSourceSummary:
    """Summary of a single KB source file."""
    filename: str
    filepath: str
    content_hash: str
    summary: str
    key_topics: list[str]
    regulatory_citations: list[str]
    applicable_requirements: list[str]


@dataclass
class RelevanceMapping:
    """Mapping of KB source to document categories."""
    kb_filename: str
    relevant_categories: dict[str, str]  # category -> relevance explanation
    key_provisions: list[str]
    citation_anchors: list[str]  # Available anchors for citation


@dataclass
class KBRelevanceIndex:
    """Complete relevance index for all KB sources."""
    version: str
    generated_at: str
    kb_summaries: list[KBSourceSummary]
    relevance_mappings: list[RelevanceMapping]
    category_index: dict[str, list[str]]  # category -> list of relevant KB files
    

def compute_content_hash(content: str) -> str:
    """Compute hash of content for cache invalidation."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def load_kb_file(filepath: Path) -> tuple[str, str]:
    """Load KB file and compute its hash."""
    content = filepath.read_text(encoding='utf-8', errors='replace')
    content_hash = compute_content_hash(content)
    return content, content_hash


async def generate_kb_summary(
    filename: str,
    content: str,
    config: dict
) -> KBSourceSummary:
    """Generate a structured summary of a KB source file."""
    
    # Truncate very long content
    max_chars = 30000
    truncated = content[:max_chars] + ("..." if len(content) > max_chars else "")
    
    prompt = f"""Analyze this regulatory/legal knowledge base document and provide a structured summary.

DOCUMENT: {filename}

CONTENT:
{truncated}

Provide your analysis in the following JSON format:
{{
    "summary": "A 2-3 sentence summary of what this document covers",
    "key_topics": ["topic1", "topic2", ...],  // Main regulatory/legal topics covered
    "regulatory_citations": ["31 CFR 1010.100", ...],  // Specific regulation citations mentioned
    "applicable_requirements": ["requirement1", ...]  // Key compliance requirements defined
}}

Focus on:
- What regulatory framework does this cover (BSA, AML, CFR, USC, state law, etc.)?
- What types of entities does it apply to (MSBs, banks, money transmitters)?
- What specific compliance obligations does it define?
- What thresholds or deadlines are mentioned?

Respond ONLY with valid JSON."""

    response = await make_completion(
        config=config,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    try:
        result = json.loads(response)
        return KBSourceSummary(
            filename=filename,
            filepath=str(filename),
            content_hash=compute_content_hash(content),
            summary=result.get("summary", ""),
            key_topics=result.get("key_topics", []),
            regulatory_citations=result.get("regulatory_citations", []),
            applicable_requirements=result.get("applicable_requirements", [])
        )
    except json.JSONDecodeError:
        logger.error(f"Failed to parse summary for {filename}")
        return KBSourceSummary(
            filename=filename,
            filepath=str(filename),
            content_hash=compute_content_hash(content),
            summary="Failed to generate summary",
            key_topics=[],
            regulatory_citations=[],
            applicable_requirements=[]
        )


async def analyze_relevance(
    kb_summary: KBSourceSummary,
    document_categories: dict,
    config: dict
) -> RelevanceMapping:
    """Analyze which document categories a KB source is relevant to."""
    
    categories_desc = "\n".join([
        f"- {cat}: {info['description']}"
        for cat, info in document_categories.items()
    ])
    
    prompt = f"""Given this knowledge base source summary, determine which document categories it is relevant to.

KB SOURCE: {kb_summary.filename}
SUMMARY: {kb_summary.summary}
KEY TOPICS: {', '.join(kb_summary.key_topics)}
REGULATORY CITATIONS: {', '.join(kb_summary.regulatory_citations)}
REQUIREMENTS: {', '.join(kb_summary.applicable_requirements)}

DOCUMENT CATEGORIES:
{categories_desc}

Respond with JSON:
{{
    "relevant_categories": {{
        "category_name": "Brief explanation of why this KB source is relevant to this category",
        ...
    }},
    "key_provisions": ["provision1", ...],  // Key provisions that should be cited
    "citation_anchors": ["anchor1", ...]  // Suggested anchor IDs for citations (e.g., "definition-msb", "ctr-threshold")
}}

Only include categories where the KB source provides substantive guidance.
Respond ONLY with valid JSON."""

    response = await make_completion(
        config=config,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    try:
        result = json.loads(response)
        return RelevanceMapping(
            kb_filename=kb_summary.filename,
            relevant_categories=result.get("relevant_categories", {}),
            key_provisions=result.get("key_provisions", []),
            citation_anchors=result.get("citation_anchors", [])
        )
    except json.JSONDecodeError:
        logger.error(f"Failed to parse relevance for {kb_summary.filename}")
        return RelevanceMapping(
            kb_filename=kb_summary.filename,
            relevant_categories={},
            key_provisions=[],
            citation_anchors=[]
        )


def build_category_index(mappings: list[RelevanceMapping]) -> dict[str, list[str]]:
    """Build reverse index from categories to relevant KB files."""
    index = {}
    for mapping in mappings:
        for category in mapping.relevant_categories.keys():
            if category not in index:
                index[category] = []
            index[category].append(mapping.kb_filename)
    return index


async def generate_relevance_index(
    kb_dir: Path,
    config: dict,
    cache_path: Optional[Path] = None
) -> KBRelevanceIndex:
    """Generate complete relevance index for all KB sources."""
    from datetime import datetime
    
    # Load cache if exists
    cached_summaries = {}
    if cache_path and cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text())
            for summary in cached.get("kb_summaries", []):
                cached_summaries[summary["filename"]] = summary
        except:
            pass
    
    # Process all KB files
    kb_files = list(kb_dir.glob("*.txt")) + list(kb_dir.glob("*.md"))
    summaries = []
    mappings = []
    
    logger.info(f"Processing {len(kb_files)} KB files...")
    
    for filepath in kb_files:
        content, content_hash = load_kb_file(filepath)
        
        # Check cache
        cached = cached_summaries.get(filepath.name)
        if cached and cached.get("content_hash") == content_hash:
            summary = KBSourceSummary(**cached)
            logger.info(f"  Using cached summary: {filepath.name}")
        else:
            logger.info(f"  Generating summary: {filepath.name}")
            summary = await generate_kb_summary(filepath.name, content, config)
        
        summaries.append(summary)
        
        # Analyze relevance
        logger.info(f"  Analyzing relevance: {filepath.name}")
        mapping = await analyze_relevance(summary, DOCUMENT_CATEGORIES, config)
        mappings.append(mapping)
    
    # Build category index
    category_index = build_category_index(mappings)
    
    index = KBRelevanceIndex(
        version="1.0",
        generated_at=datetime.now().isoformat(),
        kb_summaries=summaries,
        relevance_mappings=mappings,
        category_index=category_index
    )
    
    # Save cache
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(asdict(index), indent=2))
    
    return index


def get_relevant_kb_context(
    document_path: Path,
    index: KBRelevanceIndex,
    kb_dir: Path
) -> str:
    """Get relevant KB context for a specific document being audited."""
    
    # Determine document category from filename/path
    doc_name = document_path.name.lower()
    doc_path_str = str(document_path).lower()
    
    matched_categories = []
    for category, info in DOCUMENT_CATEGORIES.items():
        for pattern in info["patterns"]:
            if pattern.lower() in doc_name or pattern.lower() in doc_path_str:
                matched_categories.append(category)
                break
    
    if not matched_categories:
        # Default to all categories if no match
        matched_categories = list(DOCUMENT_CATEGORIES.keys())
    
    # Collect relevant KB files
    relevant_files = set()
    for category in matched_categories:
        if category in index.category_index:
            relevant_files.update(index.category_index[category])
    
    if not relevant_files:
        return ""
    
    # Build context with summaries and key provisions
    context_parts = [
        "## Relevant Regulatory Context\n",
        f"Document categories: {', '.join(matched_categories)}\n",
        "---\n"
    ]
    
    for mapping in index.relevance_mappings:
        if mapping.kb_filename in relevant_files:
            # Find summary
            summary = next(
                (s for s in index.kb_summaries if s.filename == mapping.kb_filename),
                None
            )
            if summary:
                context_parts.append(f"\n### {mapping.kb_filename}\n")
                context_parts.append(f"{summary.summary}\n")
                if mapping.key_provisions:
                    context_parts.append(f"Key provisions: {', '.join(mapping.key_provisions[:5])}\n")
                if mapping.citation_anchors:
                    context_parts.append(f"Citation anchors: {', '.join(mapping.citation_anchors[:5])}\n")
                
                # Add relevance explanation for matched categories
                for cat in matched_categories:
                    if cat in mapping.relevant_categories:
                        context_parts.append(f"  → {cat}: {mapping.relevant_categories[cat]}\n")
    
    return "\n".join(context_parts)


def export_relevance_report(index: KBRelevanceIndex, output_path: Path):
    """Export a human-readable relevance report."""
    
    lines = [
        "# KB Relevance Mapping Report\n",
        f"Generated: {index.generated_at}\n",
        f"KB Sources: {len(index.kb_summaries)}\n",
        "---\n\n"
    ]
    
    # Category overview
    lines.append("## Category Overview\n\n")
    for category, files in sorted(index.category_index.items()):
        desc = DOCUMENT_CATEGORIES.get(category, {}).get("description", "")
        lines.append(f"### {category}\n")
        lines.append(f"{desc}\n\n")
        lines.append(f"Relevant KB sources ({len(files)}):\n")
        for f in sorted(files):
            lines.append(f"- {f}\n")
        lines.append("\n")
    
    # KB Source details
    lines.append("## KB Source Details\n\n")
    for summary in sorted(index.kb_summaries, key=lambda s: s.filename):
        lines.append(f"### {summary.filename}\n")
        lines.append(f"{summary.summary}\n\n")
        if summary.key_topics:
            lines.append(f"**Topics:** {', '.join(summary.key_topics)}\n\n")
        if summary.regulatory_citations:
            lines.append(f"**Citations:** {', '.join(summary.regulatory_citations)}\n\n")
        
        # Find mapping
        mapping = next(
            (m for m in index.relevance_mappings if m.kb_filename == summary.filename),
            None
        )
        if mapping and mapping.relevant_categories:
            lines.append("**Relevant to:**\n")
            for cat, reason in mapping.relevant_categories.items():
                lines.append(f"- {cat}: {reason}\n")
        lines.append("\n---\n\n")
    
    output_path.write_text("".join(lines))


# CLI interface
async def main():
    """CLI for generating relevance index."""
    import argparse
    import asyncio
    
    parser = argparse.ArgumentParser(description='Generate KB relevance index')
    parser.add_argument('kb_dir', type=Path, help='Path to knowledge_base directory')
    parser.add_argument('--output', '-o', type=Path, help='Output path for index JSON')
    parser.add_argument('--report', '-r', type=Path, help='Output path for human-readable report')
    parser.add_argument('--config', '-c', type=Path, help='Path to config file')
    
    args = parser.parse_args()
    
    # Load config
    config_path = args.config or Path(__file__).parent.parent / "llm_audit_config.yaml"
    config = load_config(config_path)
    
    # Generate index
    cache_path = args.output or (args.kb_dir.parent / "kb_relevance_index.json")
    index = await generate_relevance_index(args.kb_dir, config, cache_path)
    
    print(f"Generated relevance index with {len(index.kb_summaries)} sources")
    print(f"Categories mapped: {len(index.category_index)}")
    
    # Export report if requested
    if args.report:
        export_relevance_report(index, args.report)
        print(f"Report saved to: {args.report}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
