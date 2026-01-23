"""
Metadata validator for document metadata checks.

Validates effective date, version, placeholders, etc.
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


class MetadataValidator(BaseValidator):
    """
    Validator for document metadata.
    
    Checks:
    - BASE-001: Effective date presence
    - BASE-002: Version number presence
    - BASE-003: Unfilled placeholders
    """
    
    @property
    def name(self) -> str:
        return "Metadata Validator"
    
    @property
    def description(self) -> str:
        return "Validates document metadata (effective date, version, placeholders)"
    
    def validate(
        self,
        content: str,
        doc_code: str | None = None,
        doc_path: str | None = None,
    ) -> list[ValidationResult]:
        """
        Run metadata validation checks.
        
        Args:
            content: Document content
            doc_code: Document code (unused for metadata)
            doc_path: Document path (unused)
            
        Returns:
            List of validation results
        """
        results: list[ValidationResult] = []
        
        for check_name, config in self.config.metadata.items():
            result = self._check_metadata_pattern(content, check_name, config)
            results.append(result)
        
        return results
    
    def _check_metadata_pattern(
        self,
        content: str,
        check_name: str,
        config,  # MetadataPatternConfig
    ) -> ValidationResult:
        """
        Check a single metadata pattern.
        
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
        required = config.required
        invert = config.invert
        count = config.count
        
        # Handle count mode (for placeholders)
        if count:
            total_count = 0
            evidence_samples: list[str] = []
            
            for pattern in patterns:
                try:
                    matches = re.findall(pattern, content, re.MULTILINE)
                    total_count += len(matches)
                    evidence_samples.extend(matches[:3])  # Keep first 3 samples
                except re.error:
                    continue
            
            if invert:
                # Should NOT find these (like placeholders)
                if total_count > 0:
                    return ValidationResult(
                        rule_id=rule_id,
                        rule_name=check_name,
                        status=ValidationStatus.FAIL,
                        severity=severity,
                        message=f"Found {total_count} unfilled placeholders",
                        evidence=", ".join(evidence_samples[:3]) if evidence_samples else None,
                    )
                else:
                    return ValidationResult(
                        rule_id=rule_id,
                        rule_name=check_name,
                        status=ValidationStatus.PASS,
                        severity=severity,
                        message="No unfilled placeholders found",
                    )
            else:
                # Should find these
                if total_count > 0:
                    return ValidationResult(
                        rule_id=rule_id,
                        rule_name=check_name,
                        status=ValidationStatus.PASS,
                        severity=severity,
                        message=f"Found {total_count} occurrences",
                        evidence=", ".join(evidence_samples[:3]) if evidence_samples else None,
                    )
                else:
                    return ValidationResult(
                        rule_id=rule_id,
                        rule_name=check_name,
                        status=ValidationStatus.FAIL if required else ValidationStatus.PASS,
                        severity=severity,
                        message="No occurrences found",
                    )
        
        # Boolean mode - check for presence
        found = False
        evidence: str | None = None
        
        for pattern in patterns:
            try:
                match = re.search(pattern, content, re.MULTILINE)
                if match:
                    found = True
                    evidence = match.group(0)[:100] if match.group(0) else None
                    break
            except re.error:
                continue
        
        if invert:
            found = not found
        
        if found:
            return ValidationResult(
                rule_id=rule_id,
                rule_name=check_name,
                status=ValidationStatus.PASS,
                severity=severity,
                message=f"Found {check_name}",
                evidence=evidence,
            )
        elif required:
            return ValidationResult(
                rule_id=rule_id,
                rule_name=check_name,
                status=ValidationStatus.FAIL,
                severity=severity,
                message=f"Missing required {check_name}",
            )
        else:
            return ValidationResult(
                rule_id=rule_id,
                rule_name=check_name,
                status=ValidationStatus.PASS,
                severity=Severity.INFO,
                message=f"Optional {check_name} not found",
            )
