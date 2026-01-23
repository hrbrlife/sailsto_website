"""
Base validator class for CCASH validation.

Provides abstract interface for all validators.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from ccash_validator.models.results import ValidationResult

if TYPE_CHECKING:
    from ccash_validator.models.config import PatternsConfig


class BaseValidator(ABC):
    """
    Abstract base class for all validators.
    
    Each validator handles a specific type of check (metadata, markers, etc.)
    """
    
    def __init__(self, config: PatternsConfig, schema_dir: Path):
        """
        Initialize the validator.
        
        Args:
            config: Patterns configuration
            schema_dir: Path to _schema directory
        """
        self.config = config
        self.schema_dir = schema_dir
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable validator name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this validator checks."""
        pass
    
    @abstractmethod
    def validate(
        self, 
        content: str, 
        doc_code: str | None = None,
        doc_path: str | None = None,
    ) -> list[ValidationResult]:
        """
        Run validation checks on document content.
        
        Args:
            content: Document content to validate
            doc_code: Document code (e.g., "B1", "F1") for filtering rules
            doc_path: Path to document for context
            
        Returns:
            List of ValidationResult objects
        """
        pass
    
    def _create_pass(
        self,
        rule_id: str,
        rule_name: str,
        message: str,
        evidence: str | None = None,
    ) -> ValidationResult:
        """Create a passing validation result."""
        from ccash_validator.models.enums import Severity, ValidationStatus
        
        return ValidationResult(
            rule_id=rule_id,
            rule_name=rule_name,
            status=ValidationStatus.PASS,
            severity=Severity.INFO,
            message=message,
            evidence=evidence,
        )
    
    def _create_fail(
        self,
        rule_id: str,
        rule_name: str,
        message: str,
        severity: str = "ERROR",
        evidence: str | None = None,
        line_number: int | None = None,
    ) -> ValidationResult:
        """Create a failing validation result."""
        from ccash_validator.models.enums import Severity, ValidationStatus
        
        return ValidationResult(
            rule_id=rule_id,
            rule_name=rule_name,
            status=ValidationStatus.FAIL,
            severity=Severity(severity.lower()),
            message=message,
            evidence=evidence,
            line_number=line_number,
        )
