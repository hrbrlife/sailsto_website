"""
Configuration models for CCASH validation patterns.

These models represent the structure of patterns.yaml.
"""

from __future__ import annotations

import re
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class LLMSemanticConfig(BaseModel):
    """Configuration for LLM semantic analysis fallback."""
    
    enabled: bool = Field(default=False, description="Whether LLM analysis is enabled")
    prompt: str = Field(default="", description="Prompt for LLM analysis")
    min_confidence: float = Field(default=0.8, ge=0.0, le=1.0, description="Minimum confidence threshold")
    
    model_config = {"extra": "allow"}


class MetadataPatternConfig(BaseModel):
    """Configuration for metadata validation (effective_date, version, etc.)."""
    
    description: str = Field(default="", description="Human-readable description")
    rule_id: str = Field(..., description="Rule identifier (e.g., BASE-001)")
    patterns: list[str] = Field(default_factory=list, description="Regex patterns to match")
    required: bool = Field(default=True, description="Whether this metadata is required")
    severity: str = Field(default="ERROR", description="Severity if check fails")
    invert: bool = Field(default=False, description="Invert the check (should NOT match)")
    count: bool = Field(default=False, description="Count occurrences instead of boolean")
    
    model_config = {"extra": "allow"}
    
    @field_validator("patterns")
    @classmethod
    def validate_patterns(cls, v: list[str]) -> list[str]:
        """Ensure all patterns are valid regex."""
        for pattern in v:
            try:
                re.compile(pattern)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{pattern}': {e}")
        return v


class ProhibitedPatternConfig(BaseModel):
    """Configuration for prohibited language detection."""
    
    description: str = Field(default="", description="Human-readable description")
    rule_id: str = Field(..., description="Rule identifier (e.g., MSB-001)")
    patterns: list[str] = Field(default_factory=list, description="Regex patterns to detect")
    case_insensitive: bool = Field(default=False, description="Case-insensitive matching")
    severity: str = Field(default="ERROR", description="Severity if prohibited language found")
    applies_to: list[str] = Field(default_factory=list, description="Document codes this applies to")
    llm_semantic: Optional[LLMSemanticConfig] = Field(default=None, description="LLM fallback config")
    
    model_config = {"extra": "allow"}
    
    @field_validator("patterns")
    @classmethod
    def validate_patterns(cls, v: list[str]) -> list[str]:
        """Ensure all patterns are valid regex."""
        for pattern in v:
            try:
                re.compile(pattern)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{pattern}': {e}")
        return v


class RequiredPatternConfig(BaseModel):
    """Configuration for required language verification."""
    
    description: str = Field(default="", description="Human-readable description")
    rule_id: str = Field(..., description="Rule identifier (e.g., MSB-003)")
    patterns: list[str] = Field(default_factory=list, description="Regex patterns that must match")
    anti_patterns: list[str] = Field(default_factory=list, description="Patterns that should NOT match")
    case_insensitive: bool = Field(default=False, description="Case-insensitive matching")
    severity: str = Field(default="ERROR", description="Severity if required language missing")
    applies_to: list[str] = Field(default_factory=list, description="Document codes this applies to")
    llm_semantic: Optional[LLMSemanticConfig] = Field(default=None, description="LLM fallback config")
    
    model_config = {"extra": "allow"}
    
    @field_validator("patterns", "anti_patterns")
    @classmethod
    def validate_patterns(cls, v: list[str]) -> list[str]:
        """Ensure all patterns are valid regex."""
        for pattern in v:
            try:
                re.compile(pattern)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{pattern}': {e}")
        return v


class MarkerPatternConfig(BaseModel):
    """Configuration for a marker type (TERM, DOC, OBL, etc.)."""
    
    description: str = Field(default="", description="Human-readable description")
    extract_pattern: str = Field(..., description="Regex to extract markers")
    validate_pattern: str = Field(default=".*", description="Regex to validate marker values")
    registry_file: str = Field(..., description="Registry file for validation")
    registry_extract: Optional[str] = Field(default=None, description="Regex to extract from registry")
    registry_extract_mode: Optional[str] = Field(default=None, description="Special extraction mode")
    registry_modes: Optional[list[dict[str, str]]] = Field(default=None, description="Multiple registry modes")
    normalize: list[dict[str, str]] = Field(default_factory=list, description="Normalization rules")
    aliases: dict[str, str] = Field(default_factory=dict, description="Value aliases")
    examples: dict[str, Any] = Field(default_factory=dict, description="Example values")
    
    model_config = {"extra": "allow"}
    
    @field_validator("extract_pattern", "validate_pattern")
    @classmethod
    def validate_regex(cls, v: str) -> str:
        """Ensure regex is valid."""
        try:
            re.compile(v)
        except re.error as e:
            raise ValueError(f"Invalid regex: {e}")
        return v


class TerminologyConfig(BaseModel):
    """Configuration for terminology consistency checking."""
    
    description: str = Field(default="", description="Human-readable description")
    canonical: str = Field(..., description="Canonical form of the term")
    doc_code: Optional[str] = Field(default=None, description="Associated document code")
    alternatives: list[dict[str, str]] = Field(default_factory=list, description="Alternative forms with severities")
    
    model_config = {"extra": "allow"}


class LLMPromptConfig(BaseModel):
    """Configuration for an LLM analysis prompt."""
    
    description: str = Field(default="", description="Human-readable description")
    prompt: str = Field(..., description="The prompt text")
    
    model_config = {"extra": "allow"}


class PatternsConfig(BaseModel):
    """
    Root configuration model for patterns.yaml.
    
    This represents the complete structure of the patterns configuration file.
    """
    
    version: str = Field(default="2.0", description="Configuration version")
    last_updated: Optional[str] = Field(default=None, description="Last update date")
    
    markers: dict[str, MarkerPatternConfig] = Field(
        default_factory=dict, 
        description="Marker type configurations"
    )
    metadata: dict[str, MetadataPatternConfig] = Field(
        default_factory=dict,
        description="Metadata pattern configurations"
    )
    prohibited: dict[str, ProhibitedPatternConfig] = Field(
        default_factory=dict,
        description="Prohibited language configurations"
    )
    required: dict[str, RequiredPatternConfig] = Field(
        default_factory=dict,
        description="Required language configurations"
    )
    terminology: dict[str, TerminologyConfig] = Field(
        default_factory=dict,
        description="Terminology consistency configurations"
    )
    llm_prompts: dict[str, LLMPromptConfig] = Field(
        default_factory=dict,
        description="LLM prompt configurations"
    )
    test_config: dict[str, Any] = Field(
        default_factory=dict,
        description="Test framework configuration"
    )
    
    model_config = {"extra": "allow"}
    
    def get_marker_config(self, marker_type: str) -> MarkerPatternConfig | None:
        """Get configuration for a specific marker type."""
        return self.markers.get(marker_type)
    
    def get_applicable_prohibited(self, doc_code: str) -> list[tuple[str, ProhibitedPatternConfig]]:
        """Get prohibited patterns applicable to a document code."""
        result = []
        for name, config in self.prohibited.items():
            if not config.applies_to or doc_code in config.applies_to:
                result.append((name, config))
        return result
    
    def get_applicable_required(self, doc_code: str) -> list[tuple[str, RequiredPatternConfig]]:
        """Get required patterns applicable to a document code."""
        result = []
        for name, config in self.required.items():
            if not config.applies_to or doc_code in config.applies_to:
                result.append((name, config))
        return result
