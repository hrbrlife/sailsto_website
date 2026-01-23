"""
Required language validator.

Verifies presence of required language patterns.
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


class RequiredValidator(BaseValidator):
    """
    Validator for required language.
    
    Checks:
    - MSB-003: Independent MSB model language
    - MSB-004: Client own EIN requirement
    - MSB-005: FinCEN registration requirement
    - FINCEN-001: Biennial renewal language
    """
    
    @property
    def name(self) -> str:
        return "Required Language Validator"
    
    @property
    def description(self) -> str:
        return "Verifies presence of required compliance language"
    
    def validate(
        self,
        content: str,
        doc_code: str | None = None,
        doc_path: str | None = None,
    ) -> list[ValidationResult]:
        """
        Check for required language patterns.
        
        Args:
            content: Document content
            doc_code: Document code for filtering applicable rules
            doc_path: Document path (unused)
            
        Returns:
            List of validation results
        """
        results: list[ValidationResult] = []
        
        for check_name, config in self.config.required.items():
            # Check if this rule applies to this document
            applies_to = config.applies_to
            if applies_to and doc_code and doc_code not in applies_to:
                continue
            
            result = self._check_required_pattern(content, check_name, config)
            results.append(result)
        
        return results
    
    def _check_required_pattern(
        self,
        content: str,
        check_name: str,
        config,  # RequiredPatternConfig
    ) -> ValidationResult:
        """
        Check for a single required pattern.
        
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
        anti_patterns = config.anti_patterns
        case_insensitive = config.case_insensitive
        
        flags = re.IGNORECASE if case_insensitive else 0
        
        # First check anti-patterns (things that should NOT be present)
        for anti_pattern in anti_patterns:
            try:
                match = re.search(anti_pattern, content, flags)
                if match:
                    line_number = content[:match.start()].count('\n') + 1
                    return ValidationResult(
                        rule_id=rule_id,
                        rule_name=check_name,
                        status=ValidationStatus.FAIL,
                        severity=severity,
                        message=f"Found prohibited variant for {check_name}",
                        evidence=match.group(0),
                        line_number=line_number,
                    )
            except re.error:
                continue
        
        # Check for required patterns
        found = False
        evidence: str | None = None
        line_number: int | None = None
        
        for pattern in patterns:
            try:
                match = re.search(pattern, content, flags)
                if match:
                    found = True
                    evidence = match.group(0)
                    line_number = content[:match.start()].count('\n') + 1
                    break
            except re.error:
                continue
        
        if found:
            return ValidationResult(
                rule_id=rule_id,
                rule_name=check_name,
                status=ValidationStatus.PASS,
                severity=severity,
                message=f"Found required language: {check_name}",
                evidence=evidence,
                line_number=line_number,
            )
        else:
            return ValidationResult(
                rule_id=rule_id,
                rule_name=check_name,
                status=ValidationStatus.FAIL,
                severity=severity,
                message=f"Missing required: {check_name}",
            )
