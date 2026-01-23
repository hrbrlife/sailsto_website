"""
Configuration loader for CCASH validator.

Loads and parses patterns.yaml configuration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ccash_validator.models.config import (
    LLMSemanticConfig,
    MarkerPatternConfig,
    MetadataPatternConfig,
    PatternsConfig,
    ProhibitedPatternConfig,
    RequiredPatternConfig,
)


class ValidatorConfig:
    """
    Configuration manager for the validator.
    
    Loads patterns.yaml and provides access to configuration.
    """
    
    def __init__(self, patterns_file: Path | str):
        """
        Initialize configuration from patterns.yaml.
        
        Args:
            patterns_file: Path to patterns.yaml
        """
        self.patterns_file = Path(patterns_file)
        self._raw_config: dict[str, Any] = {}
        self._config: PatternsConfig | None = None
        
        self._load()
    
    def _load(self) -> None:
        """Load and parse the patterns file."""
        if not self.patterns_file.exists():
            raise FileNotFoundError(f"Patterns file not found: {self.patterns_file}")
        
        with open(self.patterns_file, encoding="utf-8") as f:
            self._raw_config = yaml.safe_load(f) or {}
        
        self._config = self._parse_config()
    
    def _parse_config(self) -> PatternsConfig:
        """Parse raw config into typed models."""
        # Parse markers
        markers: dict[str, MarkerPatternConfig] = {}
        for name, data in self._raw_config.get("markers", {}).items():
            markers[name] = MarkerPatternConfig(**data)
        
        # Parse metadata
        metadata: dict[str, MetadataPatternConfig] = {}
        for name, data in self._raw_config.get("metadata", {}).items():
            metadata[name] = MetadataPatternConfig(**data)
        
        # Parse prohibited
        prohibited: dict[str, ProhibitedPatternConfig] = {}
        for name, data in self._raw_config.get("prohibited", {}).items():
            # Handle nested llm_semantic
            if "llm_semantic" in data and data["llm_semantic"]:
                data["llm_semantic"] = LLMSemanticConfig(**data["llm_semantic"])
            prohibited[name] = ProhibitedPatternConfig(**data)
        
        # Parse required
        required: dict[str, RequiredPatternConfig] = {}
        for name, data in self._raw_config.get("required", {}).items():
            # Handle nested llm_semantic
            if "llm_semantic" in data and data["llm_semantic"]:
                data["llm_semantic"] = LLMSemanticConfig(**data["llm_semantic"])
            required[name] = RequiredPatternConfig(**data)
        
        return PatternsConfig(
            version=self._raw_config.get("version", "2.0"),
            last_updated=self._raw_config.get("last_updated"),
            markers=markers,
            metadata=metadata,
            prohibited=prohibited,
            required=required,
            terminology=self._raw_config.get("terminology", {}),
            llm_prompts=self._raw_config.get("llm_prompts", {}),
            test_config=self._raw_config.get("test_config", {}),
        )
    
    @property
    def config(self) -> PatternsConfig:
        """Get the parsed configuration."""
        if self._config is None:
            raise RuntimeError("Configuration not loaded")
        return self._config
    
    @property
    def schema_dir(self) -> Path:
        """Get the schema directory (parent of validation folder)."""
        return self.patterns_file.parent.parent
    
    @property
    def docs_dir(self) -> Path:
        """Get the documents directory (parent of schema directory)."""
        return self.schema_dir.parent
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load()


def load_config(patterns_file: Path | str | None = None) -> ValidatorConfig:
    """
    Load validator configuration.
    
    Args:
        patterns_file: Path to patterns.yaml. If None, searches for it.
        
    Returns:
        ValidatorConfig instance
    """
    if patterns_file is None:
        # Try to find patterns.yaml
        candidates = [
            Path("patterns.yaml"),
            Path("_schema/validation/patterns.yaml"),
            Path(__file__).parent.parent / "patterns.yaml",
        ]
        
        for candidate in candidates:
            if candidate.exists():
                patterns_file = candidate
                break
        
        if patterns_file is None:
            raise FileNotFoundError("Could not find patterns.yaml")
    
    return ValidatorConfig(patterns_file)
