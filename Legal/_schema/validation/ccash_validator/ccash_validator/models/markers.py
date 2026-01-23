"""
Marker models for CCASH validation.

Defines type-safe representations of schema markers like [TERM:Company], [DOC:B1], etc.
"""

from __future__ import annotations

import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from ccash_validator.models.enums import MarkerType


class Marker(BaseModel):
    """
    A schema marker extracted from a document.
    
    Examples:
        - [TERM:Company] -> Marker(type=TERM, value="Company")
        - [DOC:B1 §5.2] -> Marker(type=DOC, value="B1 §5.2", raw_value="B1", section="5.2")
        - [OBL:REG-001] -> Marker(type=OBL, value="REG-001")
    """
    
    type: MarkerType = Field(..., description="Type of marker (TERM, DOC, OBL, etc.)")
    value: str = Field(..., description="The marker value as extracted")
    raw_value: str = Field(default="", description="Normalized value for registry lookup")
    section: Optional[str] = Field(default=None, description="Section reference if present")
    line_number: int = Field(default=0, description="Line number in source document")
    column: int = Field(default=0, description="Column position in source line")
    
    model_config = {"frozen": True}
    
    def __init__(self, **data):
        """Initialize marker with automatic raw_value normalization."""
        if not data.get("raw_value"):
            data["raw_value"] = data.get("value", "")
        super().__init__(**data)
    
    @field_validator("value")
    @classmethod
    def validate_value_not_empty(cls, v: str) -> str:
        """Ensure marker value is not empty."""
        if not v.strip():
            raise ValueError("Marker value cannot be empty")
        return v.strip()
    
    @property
    def full_marker(self) -> str:
        """Return the full marker string as it appears in documents."""
        return f"[{self.type}:{self.value}]"
    
    def normalize(self, normalization_rules: list[dict[str, str]] | None = None) -> str:
        """
        Normalize the value for registry lookup.
        
        Args:
            normalization_rules: List of {pattern, replacement} dicts
            
        Returns:
            Normalized value string
        """
        result = self.value
        
        if normalization_rules:
            for rule in normalization_rules:
                pattern = rule.get("pattern", "")
                replacement = rule.get("replacement", "")
                result = re.sub(pattern, replacement, result)
        
        return result.strip()


class MarkerMatch(BaseModel):
    """
    Result of matching a marker against a pattern or registry.
    """
    
    marker: Marker = Field(..., description="The marker that was matched")
    is_valid_syntax: bool = Field(default=True, description="Whether syntax is valid")
    is_in_registry: bool = Field(default=False, description="Whether found in registry")
    registry_entry: Optional[str] = Field(default=None, description="Matched registry entry")
    error_message: Optional[str] = Field(default=None, description="Error if invalid")
    
    @property
    def is_valid(self) -> bool:
        """Marker is valid if syntax and registry checks pass."""
        return self.is_valid_syntax and self.is_in_registry


class MarkerConfig(BaseModel):
    """
    Configuration for a marker type from patterns.yaml.
    """
    
    description: str = Field(default="", description="Human-readable description")
    extract_pattern: str = Field(..., description="Regex to extract markers from text")
    validate_pattern: str = Field(default=".*", description="Regex to validate marker value")
    registry_file: str = Field(..., description="Registry file to validate against")
    registry_extract: Optional[str] = Field(default=None, description="Regex to extract from registry")
    registry_extract_mode: Optional[str] = Field(default=None, description="Special extraction mode")
    normalize: list[dict[str, str]] = Field(default_factory=list, description="Normalization rules")
    aliases: dict[str, str] = Field(default_factory=dict, description="Value aliases")
    
    model_config = {"extra": "allow"}
    
    @field_validator("extract_pattern", "validate_pattern")
    @classmethod
    def validate_regex(cls, v: str) -> str:
        """Ensure regex patterns are valid."""
        try:
            re.compile(v)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
        return v
    
    def extract_markers(self, content: str) -> list[Marker]:
        """
        Extract all markers of this type from content.
        
        Args:
            content: Document content to search
            
        Returns:
            List of extracted Marker objects
        """
        markers: list[Marker] = []
        pattern = re.compile(self.extract_pattern)
        
        for line_num, line in enumerate(content.split("\n"), start=1):
            for match in pattern.finditer(line):
                value = match.group(1) if match.groups() else match.group(0)
                markers.append(Marker(
                    type=MarkerType(self.description.split()[0]) if self.description else MarkerType.TERM,
                    value=value,
                    line_number=line_num,
                    column=match.start(),
                ))
        
        return markers
    
    def validate_marker(self, marker: Marker) -> MarkerMatch:
        """
        Validate a marker's syntax against the validation pattern.
        
        Args:
            marker: Marker to validate
            
        Returns:
            MarkerMatch with validation result
        """
        is_valid = bool(re.match(self.validate_pattern, marker.value))
        
        return MarkerMatch(
            marker=marker,
            is_valid_syntax=is_valid,
            error_message=None if is_valid else f"Value '{marker.value}' does not match pattern {self.validate_pattern}",
        )
