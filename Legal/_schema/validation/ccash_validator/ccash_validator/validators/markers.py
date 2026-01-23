"""
Marker validator for schema marker checks.

Validates [TERM:*], [DOC:*], [OBL:*], [FLOW:*], [DECISION:*], [RIGHT:*],
[PERSON:*], [ROLE:*], [CONFIG:*] markers.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

from ccash_validator.models.enums import MarkerType, Severity, ValidationStatus
from ccash_validator.models.results import ValidationResult
from ccash_validator.registry.base import Registry
from ccash_validator.registry.terms import load_terms_registry
from ccash_validator.registry.documents import load_documents_registry, DocumentsLoader
from ccash_validator.registry.obligations import load_obligations_registry
from ccash_validator.registry.flows import load_flows_registry
from ccash_validator.registry.decisions import load_decisions_registry
from ccash_validator.registry.persons import load_persons_registry, PersonsRegistry, PersonEntry
from ccash_validator.registry.assignments import load_assignments_registry, AssignmentsRegistry
from ccash_validator.validators.base import BaseValidator

if TYPE_CHECKING:
    from ccash_validator.models.config import PatternsConfig


class MarkerValidator(BaseValidator):
    """
    Validator for schema markers.
    
    Checks:
    - Marker syntax validity
    - Marker values against registries
    - Cross-reference integrity
    """
    
    def __init__(self, config: PatternsConfig, schema_dir: Path):
        """
        Initialize marker validator with registries.
        
        Args:
            config: Patterns configuration
            schema_dir: Path to _schema directory
        """
        super().__init__(config, schema_dir)
        self._registries: dict[MarkerType, Registry] = {}
        self._load_registries()
    
    def _load_registries(self) -> None:
        """Load all registries."""
        try:
            self._registries[MarkerType.TERM] = load_terms_registry(self.schema_dir)
        except FileNotFoundError:
            pass
        
        try:
            self._registries[MarkerType.DOC] = load_documents_registry(self.schema_dir)
        except FileNotFoundError:
            pass
        
        try:
            self._registries[MarkerType.OBL] = load_obligations_registry(self.schema_dir)
        except FileNotFoundError:
            pass
        
        try:
            self._registries[MarkerType.FLOW] = load_flows_registry(self.schema_dir)
        except FileNotFoundError:
            pass
        
        try:
            self._registries[MarkerType.DECISION] = load_decisions_registry(self.schema_dir)
            self._registries[MarkerType.RIGHT] = self._registries[MarkerType.DECISION]
        except FileNotFoundError:
            pass
        
        try:
            self._registries[MarkerType.PERSON] = load_persons_registry(self.schema_dir)
        except FileNotFoundError:
            pass
        
        try:
            self._registries[MarkerType.ROLE] = load_assignments_registry(self.schema_dir)
        except FileNotFoundError:
            pass
        
        # CONFIG registry is loaded from entity_config.md if needed
        # For now, skip CONFIG validation as it requires custom handling
    
    @property
    def name(self) -> str:
        return "Marker Validator"
    
    @property
    def description(self) -> str:
        return "Validates schema markers ([TERM:*], [DOC:*], etc.) against registries"
    
    def validate(
        self,
        content: str,
        doc_code: str | None = None,
        doc_path: str | None = None,
    ) -> list[ValidationResult]:
        """
        Validate all markers in document content.
        
        Args:
            content: Document content
            doc_code: Document code (unused)
            doc_path: Document path for context
            
        Returns:
            List of validation results
        """
        results: list[ValidationResult] = []
        
        for marker_type_str, marker_config in self.config.markers.items():
            try:
                marker_type = MarkerType(marker_type_str)
            except ValueError:
                continue
            
            marker_results = self._validate_marker_type(
                content, marker_type, marker_config
            )
            results.extend(marker_results)
        
        return results
    
    def _validate_marker_type(
        self,
        content: str,
        marker_type: MarkerType,
        marker_config,  # MarkerPatternConfig
    ) -> list[ValidationResult]:
        """
        Validate markers of a specific type.
        
        Args:
            content: Document content
            marker_type: Type of marker to validate
            marker_config: Configuration for this marker type
            
        Returns:
            List of validation results
        """
        results: list[ValidationResult] = []
        extract_pattern = marker_config.extract_pattern
        validate_pattern = marker_config.validate_pattern
        
        # Extract all markers
        try:
            matches = list(re.finditer(extract_pattern, content))
        except re.error:
            return results
        
        if not matches:
            return results
        
        # Track unique values checked
        checked_values: set[str] = set()
        
        for match in matches:
            value = match.group(1) if match.groups() else match.group(0)
            
            # Skip duplicates
            if value.lower() in checked_values:
                continue
            checked_values.add(value.lower())
            
            # Find line number
            line_number = content[:match.start()].count('\n') + 1
            
            # Check syntax
            syntax_valid = bool(re.match(validate_pattern, value))
            if not syntax_valid:
                results.append(ValidationResult(
                    rule_id=f"MARKER-{marker_type}-SYNTAX",
                    rule_name=f"{marker_type}_syntax",
                    status=ValidationStatus.FAIL,
                    severity=Severity.ERROR,
                    message=f"Invalid {marker_type} marker syntax",
                    evidence=f"[{marker_type}:{value}]",
                    line_number=line_number,
                ))
                continue
            
            # Check against registry
            result = self._validate_against_registry(
                marker_type, value, marker_config, line_number
            )
            if result:
                results.append(result)
        
        return results
    
    def _validate_against_registry(
        self,
        marker_type: MarkerType,
        value: str,
        marker_config,
        line_number: int,
    ) -> ValidationResult | None:
        """
        Validate marker value against appropriate registry.
        
        Handles special cases for PERSON, ROLE, and CONFIG markers
        which use dot-notation for field access.
        """
        registry = self._registries.get(marker_type)
        if not registry:
            return None
        
        # Extract base ID and optional field path
        lookup_value = value
        field_path = None
        
        if marker_type == MarkerType.PERSON:
            # [PERSON:P001] or [PERSON:P001.display_name]
            parts = value.split(".", 1)
            lookup_value = parts[0]
            field_path = parts[1] if len(parts) > 1 else None
            
            if registry.contains(lookup_value):
                # Optionally validate field path exists
                if field_path and isinstance(registry, PersonsRegistry):
                    person = registry.get(lookup_value)
                    if person and not person.get_field(field_path):
                        return ValidationResult(
                            rule_id=f"MARKER-{marker_type}-FIELD",
                            rule_name=f"{marker_type}_field",
                            status=ValidationStatus.WARN,
                            severity=Severity.WARNING,
                            message=f"Person field '{field_path}' is empty",
                            evidence=f"[{marker_type}:{value}]",
                            line_number=line_number,
                        )
                return ValidationResult(
                    rule_id=f"MARKER-{marker_type}-REG",
                    rule_name=f"{marker_type}_registry",
                    status=ValidationStatus.PASS,
                    severity=Severity.INFO,
                    message=f"Valid {marker_type} reference",
                    evidence=f"[{marker_type}:{value}]",
                    line_number=line_number,
                )
            else:
                return ValidationResult(
                    rule_id=f"MARKER-{marker_type}-REG",
                    rule_name=f"{marker_type}_registry",
                    status=ValidationStatus.FAIL,
                    severity=Severity.ERROR,
                    message=f"Person '{lookup_value}' not found in registry",
                    evidence=f"[{marker_type}:{value}]",
                    line_number=line_number,
                )
        
        elif marker_type == MarkerType.ROLE:
            # [ROLE:company.ceo] or [ROLE:company.ceo.address_formatted]
            parts = value.split(".")
            if len(parts) < 2:
                return ValidationResult(
                    rule_id=f"MARKER-{marker_type}-SYNTAX",
                    rule_name=f"{marker_type}_syntax",
                    status=ValidationStatus.FAIL,
                    severity=Severity.ERROR,
                    message=f"ROLE marker requires entity.role format",
                    evidence=f"[{marker_type}:{value}]",
                    line_number=line_number,
                )
            
            entity_id = parts[0]
            role_type = parts[1]
            field_path = ".".join(parts[2:]) if len(parts) > 2 else None
            
            if isinstance(registry, AssignmentsRegistry):
                entity = registry.get_entity(entity_id)
                if not entity:
                    return ValidationResult(
                        rule_id=f"MARKER-{marker_type}-REG",
                        rule_name=f"{marker_type}_registry",
                        status=ValidationStatus.FAIL,
                        severity=Severity.ERROR,
                        message=f"Entity '{entity_id}' not found in assignments",
                        evidence=f"[{marker_type}:{value}]",
                        line_number=line_number,
                    )
                
                role_assignment = entity.get_role(role_type)
                if not role_assignment:
                    return ValidationResult(
                        rule_id=f"MARKER-{marker_type}-REG",
                        rule_name=f"{marker_type}_registry",
                        status=ValidationStatus.FAIL,
                        severity=Severity.ERROR,
                        message=f"Role '{role_type}' not assigned for '{entity_id}'",
                        evidence=f"[{marker_type}:{value}]",
                        line_number=line_number,
                    )
                
                return ValidationResult(
                    rule_id=f"MARKER-{marker_type}-REG",
                    rule_name=f"{marker_type}_registry",
                    status=ValidationStatus.PASS,
                    severity=Severity.INFO,
                    message=f"Valid {marker_type} reference",
                    evidence=f"[{marker_type}:{value}] → {role_assignment.person_id}",
                    line_number=line_number,
                )
        
        elif marker_type == MarkerType.CONFIG:
            # CONFIG markers are currently not validated against a registry
            # They will be resolved during document population
            return ValidationResult(
                rule_id=f"MARKER-{marker_type}-REG",
                rule_name=f"{marker_type}_registry",
                status=ValidationStatus.PASS,
                severity=Severity.INFO,
                message=f"CONFIG marker (validated at population time)",
                evidence=f"[{marker_type}:{value}]",
                line_number=line_number,
            )
        
        # Standard marker types (DOC, TERM, OBL, FLOW, DECISION, RIGHT)
        if marker_type == MarkerType.DOC:
            loader = DocumentsLoader(self.schema_dir)
            lookup_value = loader.normalize_doc_ref(value)
        
        if marker_type == MarkerType.FLOW:
            aliases = marker_config.aliases
            if value in aliases:
                lookup_value = aliases[value]
        
        if registry.contains(lookup_value):
            return ValidationResult(
                rule_id=f"MARKER-{marker_type}-REG",
                rule_name=f"{marker_type}_registry",
                status=ValidationStatus.PASS,
                severity=Severity.INFO,
                message=f"Valid {marker_type} reference",
                evidence=f"[{marker_type}:{value}]",
                line_number=line_number,
            )
        else:
            return ValidationResult(
                rule_id=f"MARKER-{marker_type}-REG",
                rule_name=f"{marker_type}_registry",
                status=ValidationStatus.FAIL,
                severity=Severity.ERROR,
                message=f"{marker_type} not found in registry",
                evidence=f"[{marker_type}:{value}] → '{lookup_value}' not in {marker_config.registry_file}",
                line_number=line_number,
            )
    
    def get_registry(self, marker_type: MarkerType) -> Registry | None:
        """Get a loaded registry by type."""
        return self._registries.get(marker_type)
