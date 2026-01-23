"""
Type-safe models for audit findings and reports.

All agent outputs must conform to these Pydantic models for type safety.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class AuditSeverity(str, Enum):
    """Severity levels for audit findings."""
    
    CRITICAL = "critical"      # Must fix before filing/execution
    HIGH = "high"              # Should fix, significant legal/compliance risk
    MEDIUM = "medium"          # Recommended fix, potential issues
    LOW = "low"                # Minor improvements, style/clarity
    INFO = "info"              # Informational, no action required
    
    @property
    def emoji(self) -> str:
        """Emoji representation for display."""
        return {
            self.CRITICAL: "🚨",
            self.HIGH: "❌",
            self.MEDIUM: "⚠️",
            self.LOW: "💡",
            self.INFO: "ℹ️",
        }[self]
    
    @property
    def weight(self) -> int:
        """Numeric weight for sorting/aggregation."""
        return {
            self.CRITICAL: 100,
            self.HIGH: 50,
            self.MEDIUM: 20,
            self.LOW: 5,
            self.INFO: 1,
        }[self]


class AuditCategory(str, Enum):
    """Categories of audit findings."""
    
    # Legal
    LEGAL_STRUCTURE = "legal_structure"
    CROSS_REFERENCE = "cross_reference"
    MONTANA_LLC_LAW = "montana_llc_law"
    CONTRACT_TERMS = "contract_terms"
    LIABILITY = "liability"
    
    # Compliance
    BSA_AML = "bsa_aml"
    FINCEN = "fincen"
    MSB_REQUIREMENTS = "msb_requirements"
    RECORD_KEEPING = "record_keeping"
    SANCTIONS = "sanctions"
    
    # Technical
    MARKER_SYNTAX = "marker_syntax"
    SCHEMA_CONFORMANCE = "schema_conformance"
    PLACEHOLDER = "placeholder"
    FORMATTING = "formatting"
    
    # Financial
    CAPITAL_REQUIREMENTS = "capital_requirements"
    INSURANCE = "insurance"
    FEE_STRUCTURE = "fee_structure"
    FINANCIAL_REPORTING = "financial_reporting"
    
    # Data Privacy
    GDPR = "gdpr"
    CCPA = "ccpa"
    DATA_HANDLING = "data_handling"
    CONSENT = "consent"
    
    # Operational
    OFFICER_DUTIES = "officer_duties"
    SERIES_SEPARATION = "series_separation"
    GOVERNANCE = "governance"
    SUCCESSION = "succession"


class AuditFinding(BaseModel):
    """
    A single audit finding from an agent.
    
    This is the core output unit - all agents produce these.
    """
    
    id: str = Field(
        description="Unique finding ID (e.g., 'LEGAL-001', 'BSA-042')"
    )
    category: AuditCategory = Field(
        description="Category of the finding"
    )
    severity: AuditSeverity = Field(
        description="Severity level"
    )
    title: str = Field(
        description="Short title (one line)",
        max_length=200,
    )
    description: str = Field(
        description="Detailed description of the finding"
    )
    location: str = Field(
        description="Where in the document (section, line, marker)"
    )
    evidence: str = Field(
        description="Specific text or marker that triggered the finding"
    )
    recommendation: str = Field(
        description="Recommended fix or action"
    )
    
    # Metadata
    agent_id: str = Field(
        description="ID of the agent that produced this finding"
    )
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Agent's confidence in this finding (0-1)"
    )
    references: list[str] = Field(
        default_factory=list,
        description="Related document markers, laws, or standards"
    )
    
    # Source citations (anti-hallucination)
    source_citations: list[str] = Field(
        default_factory=list,
        description="[SOURCE:filename] citations supporting this finding"
    )
    citation_status: Optional[str] = Field(
        default=None,
        description="Citation validation status: valid, invalid, needs_citation, not_required"
    )
    citation_warning: Optional[str] = Field(
        default=None,
        description="Warning message about citation issues"
    )
    
    # For consolidation
    consolidated: bool = Field(
        default=False,
        description="Whether this finding has been reviewed by consolidator"
    )
    disputed: bool = Field(
        default=False,
        description="Whether skeptic agent disputed this finding"
    )
    final_severity: Optional[AuditSeverity] = Field(
        default=None,
        description="Final severity after review (may differ from initial)"
    )
    
    model_config = {"frozen": False}
    
    def to_markdown(self) -> str:
        """Format finding as markdown."""
        severity = self.final_severity or self.severity
        return f"""### {severity.emoji} {self.id}: {self.title}

**Severity:** {severity.value.upper()}
**Category:** {self.category.value}
**Location:** {self.location}
**Confidence:** {self.confidence:.0%}

**Description:**
{self.description}

**Evidence:**
```
{self.evidence}
```

**Recommendation:**
{self.recommendation}

**References:** {', '.join(self.references) if self.references else 'None'}
"""


class AgentAuditResult(BaseModel):
    """Result from a single auditor agent."""
    
    agent_id: str = Field(description="Agent identifier")
    agent_role: str = Field(description="Agent role (e.g., 'legal_auditor')")
    document_path: str = Field(description="Document that was audited")
    
    findings: list[AuditFinding] = Field(
        default_factory=list,
        description="Findings from this agent"
    )
    
    # Execution metadata
    model_used: str = Field(description="Model that was used")
    tokens_used: int = Field(default=0, description="Total tokens consumed")
    execution_time_ms: int = Field(default=0, description="Execution time in ms")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Status
    success: bool = Field(default=True)
    error: Optional[str] = Field(default=None)
    
    @property
    def finding_count(self) -> int:
        return len(self.findings)
    
    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == AuditSeverity.CRITICAL)
    
    @property
    def high_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == AuditSeverity.HIGH)


class AuditReport(BaseModel):
    """
    Complete audit report for a single document.
    
    Contains results from all parallel auditors before consolidation.
    """
    
    document_path: str = Field(description="Path to audited document")
    document_name: str = Field(description="Document filename")
    document_code: Optional[str] = Field(
        default=None,
        description="Document code (e.g., 'B1', 'A1')"
    )
    
    # Raw results from all auditors
    agent_results: list[AgentAuditResult] = Field(
        default_factory=list,
        description="Results from each auditor agent"
    )
    
    # Aggregated
    all_findings: list[AuditFinding] = Field(
        default_factory=list,
        description="All findings from all agents (pre-consolidation)"
    )
    
    # Execution metadata
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)
    total_tokens: int = Field(default=0)
    
    @property
    def total_findings(self) -> int:
        return len(self.all_findings)
    
    @property
    def findings_by_severity(self) -> dict[AuditSeverity, int]:
        counts: dict[AuditSeverity, int] = {s: 0 for s in AuditSeverity}
        for f in self.all_findings:
            counts[f.severity] += 1
        return counts


class ConsolidatedReport(BaseModel):
    """
    Final consolidated audit report after all agent processing.
    
    This is the output of the full pipeline:
    Auditors → Consolidator → Skeptic → Reviewer
    """
    
    document_path: str
    document_name: str
    document_code: Optional[str] = None
    
    # Consolidated findings (deduplicated, reviewed)
    findings: list[AuditFinding] = Field(
        default_factory=list,
        description="Final reviewed findings"
    )
    
    # Summary
    summary: str = Field(
        default="",
        description="Executive summary of audit results"
    )
    
    # Verdicts
    overall_status: str = Field(
        default="pending",
        description="pass | fail | needs_review"
    )
    blocking_issues: list[str] = Field(
        default_factory=list,
        description="Issues that must be resolved before filing"
    )
    
    # Processing trace
    consolidator_notes: str = Field(
        default="",
        description="Notes from consolidator agent"
    )
    skeptic_challenges: list[str] = Field(
        default_factory=list,
        description="Challenges raised by skeptic agent"
    )
    reviewer_decision: str = Field(
        default="",
        description="Final decision from reviewer agent"
    )
    
    # Metrics
    original_finding_count: int = Field(default=0)
    deduplicated_count: int = Field(default=0)
    disputed_count: int = Field(default=0)
    severity_adjusted_count: int = Field(default=0)
    
    # Citation validation stats
    citation_stats: Optional[dict[str, int]] = Field(
        default=None,
        description="Stats from citation validation: total, valid, invalid"
    )
    
    # Rejected findings (hallucinations)
    rejected_findings: list[dict] = Field(
        default_factory=list,
        description="Findings rejected due to hallucinated citations"
    )
    
    # Execution
    total_tokens: int = Field(default=0)
    total_time_ms: int = Field(default=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def is_passing(self) -> bool:
        return self.overall_status == "pass"
    
    @property
    def critical_findings(self) -> list[AuditFinding]:
        return [f for f in self.findings 
                if (f.final_severity or f.severity) == AuditSeverity.CRITICAL]
    
    @property
    def high_findings(self) -> list[AuditFinding]:
        return [f for f in self.findings 
                if (f.final_severity or f.severity) == AuditSeverity.HIGH]
    
    def to_markdown(self) -> str:
        """Generate full markdown report."""
        status_emoji = {
            "pass": "✅",
            "fail": "❌",
            "needs_review": "⚠️",
        }.get(self.overall_status, "❓")
        
        report = f"""# Audit Report: {self.document_name}

**Document:** `{self.document_path}`
**Status:** {status_emoji} {self.overall_status.upper()}
**Generated:** {self.timestamp.isoformat()}

---

## Executive Summary

{self.summary}

---

## Metrics

| Metric | Value |
|--------|-------|
| Original Findings | {self.original_finding_count} |
| After Deduplication | {self.deduplicated_count} |
| Disputed by Skeptic | {self.disputed_count} |
| Severity Adjusted | {self.severity_adjusted_count} |
| Final Findings | {len(self.findings)} |
| Critical | {len(self.critical_findings)} |
| High | {len(self.high_findings)} |

---

## Blocking Issues

"""
        if self.blocking_issues:
            for issue in self.blocking_issues:
                report += f"- 🚨 {issue}\n"
        else:
            report += "_No blocking issues._\n"
        
        report += "\n---\n\n## Findings\n\n"
        
        # Group by severity
        for severity in [AuditSeverity.CRITICAL, AuditSeverity.HIGH, 
                         AuditSeverity.MEDIUM, AuditSeverity.LOW, AuditSeverity.INFO]:
            findings = [f for f in self.findings 
                       if (f.final_severity or f.severity) == severity]
            if findings:
                report += f"### {severity.emoji} {severity.value.upper()} ({len(findings)})\n\n"
                for finding in findings:
                    report += finding.to_markdown() + "\n---\n\n"
        
        report += f"""
## Processing Notes

### Consolidator Notes
{self.consolidator_notes or '_None_'}

### Skeptic Challenges
"""
        if self.skeptic_challenges:
            for challenge in self.skeptic_challenges:
                report += f"- {challenge}\n"
        else:
            report += "_None_\n"
        
        report += f"""
### Reviewer Decision
{self.reviewer_decision or '_Pending_'}

---

_Processed with {self.total_tokens:,} tokens in {self.total_time_ms:,}ms_
"""
        return report
