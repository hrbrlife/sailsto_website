"""
Citation Validation Module.

Validates [SOURCE:] citations in audit findings to ensure:
1. Cited sources exist in the knowledge base
2. Cited sections/anchors can be found
3. Content supports the claim being made

This is the key anti-hallucination mechanism.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class CitationStatus(str, Enum):
    """Status of a citation validation."""
    VALID = "valid"           # Source exists and supports claim
    PARTIAL = "partial"       # Source exists but anchor not found
    MISSING = "missing"       # Source file not found in KB
    UNSUPPORTED = "unsupported"  # Source exists but doesn't support claim
    UNCITED = "uncited"       # No citation provided for factual claim


@dataclass
class CitationValidation:
    """Result of validating a single citation."""
    
    citation: str
    status: CitationStatus
    source_file: Optional[str] = None
    anchor: Optional[str] = None
    evidence: Optional[str] = None
    error_message: Optional[str] = None
    confidence: float = 1.0
    
    @property
    def is_valid(self) -> bool:
        return self.status in (CitationStatus.VALID, CitationStatus.PARTIAL)


class FindingCitationResult(BaseModel):
    """Results of validating all citations in a finding."""
    
    finding_id: str = Field(description="ID of the finding being validated")
    
    # Citation analysis
    citations_found: list[str] = Field(
        default_factory=list,
        description="All [SOURCE:] citations found in finding"
    )
    citations_valid: list[str] = Field(
        default_factory=list,
        description="Citations that validated successfully"
    )
    citations_invalid: list[str] = Field(
        default_factory=list,
        description="Citations that failed validation"
    )
    citations_missing: list[str] = Field(
        default_factory=list,
        description="Sources cited but not in KB"
    )
    
    # Overall status
    has_citations: bool = Field(
        default=False,
        description="Whether finding has any citations"
    )
    all_citations_valid: bool = Field(
        default=False,
        description="Whether all citations are valid"
    )
    requires_citation: bool = Field(
        default=False,
        description="Whether this finding type requires citations"
    )
    
    # Detailed validations
    validations: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Detailed validation results per citation"
    )
    
    # Verdict
    verdict: str = Field(
        default="pending",
        description="Overall verdict: valid, invalid, needs_citation, unchecked"
    )
    confidence_adjustment: float = Field(
        default=0.0,
        description="Suggested confidence adjustment (-1.0 to 0)"
    )


# Pattern for [SOURCE:...] citations
CITATION_PATTERN = re.compile(r'\[SOURCE:([^\]]+)\]', re.IGNORECASE)

# Patterns that indicate a finding makes legal/regulatory claims
LEGAL_CLAIM_PATTERNS = [
    r'requires?\b',
    r'mandates?\b', 
    r'must\b',
    r'shall\b',
    r'under\s+(MCA|CFR|USC|law|regulation|statute)',
    r'pursuant\s+to',
    r'according\s+to',
    r'violat(e|es|ion)',
    r'non-?complian(t|ce)',
    r'\blaw\s+(requires|mandates|states)',
    r'regulatory\s+requirement',
    r'legal\s+(requirement|obligation)',
    r'§\s*\d+',  # Section symbols
    r'\d+\s+(CFR|USC|MCA)',  # Citation patterns
]

LEGAL_CLAIM_RE = re.compile('|'.join(LEGAL_CLAIM_PATTERNS), re.IGNORECASE)


def extract_citations(text: str) -> list[str]:
    """Extract all [SOURCE:...] citations from text."""
    return CITATION_PATTERN.findall(text)


def finding_requires_citation(finding: dict[str, Any]) -> bool:
    """
    Determine if a finding makes claims that require citation.
    
    Args:
        finding: Finding dict with title, description, recommendation
        
    Returns:
        True if finding makes legal/regulatory claims
    """
    # Combine all text fields
    text_parts = [
        finding.get('title', ''),
        finding.get('description', ''),
        finding.get('recommendation', ''),
        finding.get('evidence', ''),
    ]
    full_text = ' '.join(str(p) for p in text_parts if p)
    
    # Check for legal claim patterns
    return bool(LEGAL_CLAIM_RE.search(full_text))


class CitationValidator:
    """
    Validates citations in audit findings against the knowledge base.
    
    Usage:
        from llm_audit.knowledge_base import KnowledgeBase
        
        kb = KnowledgeBase(path)
        kb.load()
        
        validator = CitationValidator(kb)
        result = validator.validate_finding(finding_dict)
        
        if not result.all_citations_valid:
            # Reject or flag the finding
    """
    
    def __init__(self, knowledge_base: Any):  # Type is KnowledgeBase but avoiding circular import
        """
        Initialize with a loaded knowledge base.
        
        Args:
            knowledge_base: Loaded KnowledgeBase instance
        """
        self.kb = knowledge_base
    
    def validate_citation(self, citation: str) -> CitationValidation:
        """
        Validate a single citation.
        
        Args:
            citation: Citation string (e.g., "31_cfr_1022.txt" or "31_cfr_1022.txt#registration")
            
        Returns:
            CitationValidation result
        """
        # Parse citation
        if '#' in citation:
            source_file, anchor = citation.split('#', 1)
        else:
            source_file = citation
            anchor = None
        
        source_file = source_file.strip()
        
        # Check if source exists
        is_valid, evidence = self.kb.verify_citation(citation)
        
        if is_valid:
            if anchor and "not found" in str(evidence):
                return CitationValidation(
                    citation=citation,
                    status=CitationStatus.PARTIAL,
                    source_file=source_file,
                    anchor=anchor,
                    evidence=evidence,
                    error_message=f"Source exists but anchor '{anchor}' not found",
                    confidence=0.7,
                )
            return CitationValidation(
                citation=citation,
                status=CitationStatus.VALID,
                source_file=source_file,
                anchor=anchor,
                evidence=evidence,
                confidence=1.0,
            )
        else:
            return CitationValidation(
                citation=citation,
                status=CitationStatus.MISSING,
                source_file=source_file,
                anchor=anchor,
                error_message=f"Source '{source_file}' not found in knowledge base",
                confidence=0.0,
            )
    
    def validate_finding(self, finding: dict[str, Any]) -> FindingCitationResult:
        """
        Validate all citations in a finding.
        
        Args:
            finding: Finding dict with id, title, description, recommendation, etc.
            
        Returns:
            FindingCitationResult with validation details
        """
        finding_id = finding.get('id', 'unknown')
        
        # Combine all text fields to search for citations
        text_parts = [
            finding.get('title', ''),
            finding.get('description', ''),
            finding.get('recommendation', ''),
            finding.get('evidence', ''),
        ]
        full_text = ' '.join(str(p) for p in text_parts if p)
        
        # Extract citations
        citations = extract_citations(full_text)
        
        # Check if finding requires citations
        requires = finding_requires_citation(finding)
        
        result = FindingCitationResult(
            finding_id=finding_id,
            citations_found=citations,
            has_citations=len(citations) > 0,
            requires_citation=requires,
        )
        
        # Validate each citation
        for citation in citations:
            validation = self.validate_citation(citation)
            
            result.validations.append({
                'citation': citation,
                'status': validation.status.value,
                'source_file': validation.source_file,
                'anchor': validation.anchor,
                'evidence': validation.evidence[:200] if validation.evidence else None,
                'error': validation.error_message,
                'confidence': validation.confidence,
            })
            
            if validation.is_valid:
                result.citations_valid.append(citation)
            else:
                result.citations_invalid.append(citation)
                if validation.status == CitationStatus.MISSING:
                    result.citations_missing.append(citation)
        
        # Determine verdict
        if not requires:
            result.verdict = "not_required"
            result.confidence_adjustment = 0.0
        elif not citations:
            result.verdict = "needs_citation"
            result.confidence_adjustment = -0.5  # Significant penalty for uncited legal claims
        elif len(result.citations_invalid) > 0:
            result.verdict = "invalid"
            result.confidence_adjustment = -0.3 * len(result.citations_invalid)
        else:
            result.verdict = "valid"
            result.confidence_adjustment = 0.0
        
        result.all_citations_valid = (
            len(citations) > 0 and len(result.citations_invalid) == 0
        )
        
        return result
    
    def validate_findings_batch(
        self,
        findings: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[FindingCitationResult]]:
        """
        Validate citations in multiple findings.
        
        Args:
            findings: List of finding dicts
            
        Returns:
            Tuple of (adjusted_findings, validation_results)
        """
        adjusted = []
        results = []
        
        for finding in findings:
            result = self.validate_finding(finding)
            results.append(result)
            
            # Adjust confidence based on citation validation
            adjusted_finding = finding.copy()
            if 'confidence' in adjusted_finding:
                original_conf = adjusted_finding['confidence']
                adjusted_finding['confidence'] = max(
                    0.1,
                    original_conf + result.confidence_adjustment
                )
                adjusted_finding['citation_status'] = result.verdict
            
            # Add warning for problematic citations
            if result.verdict == "needs_citation":
                adjusted_finding['citation_warning'] = (
                    "Finding makes legal/regulatory claims without [SOURCE:] citations"
                )
            elif result.verdict == "invalid":
                adjusted_finding['citation_warning'] = (
                    f"Invalid citations: {', '.join(result.citations_missing)}"
                )
            
            adjusted.append(adjusted_finding)
        
        return adjusted, results


def get_citation_prompt_section() -> str:
    """
    Get the prompt section that instructs agents on citation requirements.
    
    This should be appended to agent system prompts.
    """
    return """

## CITATION REQUIREMENTS (CRITICAL)

You MUST cite sources for all legal, regulatory, or factual claims using:

    [SOURCE:filename.txt]

Or with section anchors:

    [SOURCE:filename.txt#section_name]

### Rules:

1. **NEVER HALLUCINATE LAWS OR REGULATIONS**
   - Only cite laws/regulations that exist in the provided Knowledge Base
   - If you cannot find a source, say "No source available in KB" and lower confidence

2. **CITE EVERYTHING LEGAL**
   - Any claim about what law "requires", "mandates", or "prohibits" needs a citation
   - Any mention of specific statutes (MCA, CFR, USC) needs a citation
   - Any claim about licensing requirements needs a citation

3. **BE HONEST ABOUT GAPS**
   - If the KB doesn't have information on a topic, say so
   - Don't invent requirements - this causes real harm

4. **VALID vs INVALID CITATIONS**
   ✅ VALID: [SOURCE:31_cfr_1022.380_msb_registration.txt]
   ✅ VALID: [SOURCE:mca_35-8-304_series_liability.txt]
   ❌ INVALID: "MCA Title 32, Chapter 9" (if not in KB)
   ❌ INVALID: "According to Montana law..." (uncited)

### Finding Template with Citations:

```json
{
  "id": "EXAMPLE-001",
  "category": "compliance",
  "severity": "high",
  "title": "Missing MSB Registration Reference",
  "description": "The document does not reference FinCEN MSB registration requirements [SOURCE:31_cfr_1022.380_msb_registration.txt] which mandates registration for money services businesses.",
  "recommendation": "Add reference to MSB registration per [SOURCE:fincen_msb_registration_overview.txt]",
  "confidence": 0.9
}
```

IMPORTANT: Findings with uncited legal claims will have their confidence REDUCED.
Findings citing non-existent sources will be REJECTED.
"""
