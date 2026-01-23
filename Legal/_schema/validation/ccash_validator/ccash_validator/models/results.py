"""
Validation result models for CCASH validation.

Type-safe representations of validation outcomes.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ccash_validator.models.enums import Severity, ValidationStatus


class ValidationResult(BaseModel):
    """
    Result of a single validation check.
    
    Examples:
        - BASE-001: Missing effective date (FAIL, ERROR)
        - MSB-003: Found independent MSB language (PASS, ERROR)
        - MARKER-TERM: Invalid format for [TERM:] (FAIL, ERROR)
    """
    
    rule_id: str = Field(..., description="Unique rule identifier (e.g., BASE-001, MSB-003)")
    rule_name: str = Field(..., description="Human-readable rule name")
    status: ValidationStatus = Field(..., description="Pass/Fail/Skip status")
    severity: Severity = Field(default=Severity.ERROR, description="Severity if failed")
    message: str = Field(default="", description="Detailed message about the check")
    evidence: Optional[str] = Field(default=None, description="Supporting evidence/quote")
    line_number: Optional[int] = Field(default=None, description="Line number if applicable")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score (1.0 = certain)")
    llm_assisted: bool = Field(default=False, description="Whether LLM was used for this check")
    
    model_config = {"frozen": True}
    
    @property
    def is_passed(self) -> bool:
        """Check passed successfully."""
        return self.status == ValidationStatus.PASS
    
    @property
    def is_failed(self) -> bool:
        """Check failed."""
        return self.status == ValidationStatus.FAIL
    
    @property
    def is_error(self) -> bool:
        """Check failed with error severity."""
        return self.is_failed and self.severity == Severity.ERROR
    
    @property
    def is_warning(self) -> bool:
        """Check failed with warning severity."""
        return self.is_failed and self.severity == Severity.WARNING
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "status": self.status.value,
            "severity": self.severity.value,
            "message": self.message,
            "evidence": self.evidence,
            "line_number": self.line_number,
            "confidence": self.confidence,
            "llm_assisted": self.llm_assisted,
        }


class DocumentValidation(BaseModel):
    """
    Complete validation results for a single document.
    """
    
    document_path: str = Field(..., description="Path to the validated document")
    document_code: Optional[str] = Field(default=None, description="Extracted document code (e.g., B1, F1)")
    validated_at: datetime = Field(default_factory=datetime.now, description="Validation timestamp")
    results: list[ValidationResult] = Field(default_factory=list, description="Individual check results")
    
    @computed_field
    @property
    def document_name(self) -> str:
        """Extract document filename."""
        return Path(self.document_path).name
    
    @computed_field
    @property
    def error_count(self) -> int:
        """Count of failed checks with ERROR severity."""
        return sum(1 for r in self.results if r.is_error)
    
    @computed_field
    @property
    def warning_count(self) -> int:
        """Count of failed checks with WARNING severity."""
        return sum(1 for r in self.results if r.is_warning)
    
    @computed_field
    @property
    def passed_count(self) -> int:
        """Count of passed checks."""
        return sum(1 for r in self.results if r.is_passed)
    
    @computed_field
    @property
    def total_count(self) -> int:
        """Total number of checks run."""
        return len(self.results)
    
    @computed_field
    @property
    def has_errors(self) -> bool:
        """Document has at least one error."""
        return self.error_count > 0
    
    @computed_field
    @property
    def has_warnings(self) -> bool:
        """Document has at least one warning."""
        return self.warning_count > 0
    
    @computed_field
    @property
    def is_clean(self) -> bool:
        """Document passed all checks."""
        return not self.has_errors and not self.has_warnings
    
    def get_failures(self) -> list[ValidationResult]:
        """Get all failed results."""
        return [r for r in self.results if r.is_failed]
    
    def get_errors(self) -> list[ValidationResult]:
        """Get all error-severity failures."""
        return [r for r in self.results if r.is_error]
    
    def get_warnings(self) -> list[ValidationResult]:
        """Get all warning-severity failures."""
        return [r for r in self.results if r.is_warning]
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "document_path": self.document_path,
            "document_code": self.document_code,
            "document_name": self.document_name,
            "validated_at": self.validated_at.isoformat(),
            "summary": {
                "total": self.total_count,
                "passed": self.passed_count,
                "errors": self.error_count,
                "warnings": self.warning_count,
            },
            "results": [r.to_dict() for r in self.results],
        }


class ValidationSummary(BaseModel):
    """
    Aggregate summary of validation across multiple documents.
    """
    
    documents: list[DocumentValidation] = Field(default_factory=list, description="Individual document results")
    started_at: datetime = Field(default_factory=datetime.now, description="Validation start time")
    completed_at: Optional[datetime] = Field(default=None, description="Validation end time")
    llm_enabled: bool = Field(default=False, description="Whether LLM analysis was enabled")
    llm_provider: Optional[str] = Field(default=None, description="LLM provider if enabled")
    
    @computed_field
    @property
    def document_count(self) -> int:
        """Total documents validated."""
        return len(self.documents)
    
    @computed_field
    @property
    def total_errors(self) -> int:
        """Total errors across all documents."""
        return sum(d.error_count for d in self.documents)
    
    @computed_field
    @property
    def total_warnings(self) -> int:
        """Total warnings across all documents."""
        return sum(d.warning_count for d in self.documents)
    
    @computed_field
    @property
    def total_passed(self) -> int:
        """Total passed checks across all documents."""
        return sum(d.passed_count for d in self.documents)
    
    @computed_field
    @property
    def total_checks(self) -> int:
        """Total checks run across all documents."""
        return sum(d.total_count for d in self.documents)
    
    @computed_field
    @property
    def documents_with_errors(self) -> int:
        """Count of documents with at least one error."""
        return sum(1 for d in self.documents if d.has_errors)
    
    @computed_field
    @property
    def documents_clean(self) -> int:
        """Count of documents with no issues."""
        return sum(1 for d in self.documents if d.is_clean)
    
    @computed_field
    @property
    def is_passing(self) -> bool:
        """Overall validation is passing (no errors)."""
        return self.total_errors == 0
    
    def complete(self) -> None:
        """Mark validation as complete."""
        self.completed_at = datetime.now()
    
    def add_document(self, doc: DocumentValidation) -> None:
        """Add a document validation result."""
        self.documents.append(doc)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "summary": {
                "documents": self.document_count,
                "documents_with_errors": self.documents_with_errors,
                "documents_clean": self.documents_clean,
                "total_checks": self.total_checks,
                "passed": self.total_passed,
                "errors": self.total_errors,
                "warnings": self.total_warnings,
                "is_passing": self.is_passing,
            },
            "meta": {
                "started_at": self.started_at.isoformat(),
                "completed_at": self.completed_at.isoformat() if self.completed_at else None,
                "llm_enabled": self.llm_enabled,
                "llm_provider": self.llm_provider,
            },
            "documents": [d.to_dict() for d in self.documents],
        }
