"""
Prohibited language validator.

Detects prohibited language patterns like white-label, rent-a-license, etc.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

from ccash_validator.models.enums import Severity, ValidationStatus
from ccash_validator.models.results import ValidationResult
from ccash_validator.validators.base import BaseValidator

if TYPE_CHECKING:
    from ccash_validator.models.config import PatternsConfig


class ProhibitedValidator(BaseValidator):
    """
    Validator for prohibited language.
    
    Checks:
    - MSB-001: White-label language
    - MSB-002: Rent-a-license language
    - Other prohibited patterns
    """
    
    @property
    def name(self) -> str:
        return "Prohibited Language Validator"
    
    @property
    def description(self) -> str:
        return "Detects prohibited language (white-label, rent-a-license, etc.)"
    
    def validate(
        self,
        content: str,
        doc_code: str | None = None,
        doc_path: str | None = None,
    ) -> list[ValidationResult]:
        """
        Check for prohibited language patterns.
        
        Args:
            content: Document content
            doc_code: Document code for filtering applicable rules
            doc_path: Document path (unused)
            
        Returns:
            List of validation results
        """
        results: list[ValidationResult] = []
        
        for check_name, config in self.config.prohibited.items():
            # Check if this rule applies to this document
            applies_to = config.applies_to
            if applies_to and doc_code and doc_code not in applies_to:
                continue
            
            result = self._check_prohibited_pattern(content, check_name, config)
            results.append(result)
        
        return results
    
    def _check_prohibited_pattern(
        self,
        content: str,
        check_name: str,
        config,  # ProhibitedPatternConfig
    ) -> ValidationResult:
        """
        Check for a single prohibited pattern.
        
        Args:
            content: Document content
            check_name: Name of the check
            config: Pattern configuration
            
        Returns:
            ValidationResult
        """
        rule_id = config.rule_id
        severity = Severity(config.severity.lower())
        patterns = config.patterns
        case_insensitive = config.case_insensitive
        
        flags = re.IGNORECASE if case_insensitive else 0
        
        # Check each pattern
        found = False
        evidence: str | None = None
        line_number: int | None = None
        
        for pattern in patterns:
            try:
                match = re.search(pattern, content, flags)
                if match:
                    found = True
                    evidence = match.group(0)
                    # Find line number
                    line_number = content[:match.start()].count('\n') + 1
                    break
            except re.error:
                continue
        
        if found:
            return ValidationResult(
                rule_id=rule_id,
                rule_name=check_name,
                status=ValidationStatus.FAIL,
                severity=severity,
                message=f"Prohibited language found: {check_name}",
                evidence=evidence,
                line_number=line_number,
            )
        else:
            return ValidationResult(
                rule_id=rule_id,
                rule_name=check_name,
                status=ValidationStatus.PASS,
                severity=severity,
                message=f"No {check_name} found",
            )
