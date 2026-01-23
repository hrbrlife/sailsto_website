"""
Base registry classes for CCASH validation.

Provides abstract base for all registry loaders.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from ccash_validator.models.enums import MarkerType


class RegistryEntry(BaseModel):
    """A single entry in a registry."""
    
    id: str = Field(..., description="Primary identifier")
    aliases: list[str] = Field(default_factory=list, description="Alternative names/aliases")
    source_line: int = Field(default=0, description="Line number in source file")
    metadata: dict[str, str] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = {"frozen": True}
    
    def matches(self, value: str, case_sensitive: bool = False) -> bool:
        """Check if a value matches this entry (id or any alias)."""
        if case_sensitive:
            return value == self.id or value in self.aliases
        else:
            lower_value = value.lower()
            return (
                lower_value == self.id.lower() or 
                any(lower_value == alias.lower() for alias in self.aliases)
            )


T = TypeVar("T", bound=RegistryEntry)


class Registry(BaseModel, Generic[T]):
    """
    A type-safe registry of entries.
    
    Provides efficient lookup by ID or alias.
    """
    
    marker_type: MarkerType = Field(..., description="Type of marker this registry validates")
    source_file: str = Field(..., description="Path to source registry file")
    entries: list[T] = Field(default_factory=list, description="All registry entries")
    
    # Lookup caches (populated on first access)
    _id_index: dict[str, T] | None = None
    _alias_index: dict[str, T] | None = None
    
    model_config = {"arbitrary_types_allowed": True}
    
    def _build_indices(self) -> None:
        """Build lookup indices if not already built."""
        if self._id_index is None:
            self._id_index = {}
            self._alias_index = {}
            for entry in self.entries:
                # Index by ID (case-insensitive)
                self._id_index[entry.id.lower()] = entry
                # Index by aliases
                for alias in entry.aliases:
                    self._alias_index[alias.lower()] = entry
    
    def lookup(self, value: str) -> T | None:
        """
        Look up an entry by ID or alias.
        
        Args:
            value: The value to look up
            
        Returns:
            Matching entry or None
        """
        self._build_indices()
        assert self._id_index is not None
        assert self._alias_index is not None
        
        lower_value = value.lower()
        
        # Try direct ID match first
        if lower_value in self._id_index:
            return self._id_index[lower_value]
        
        # Try alias match
        if lower_value in self._alias_index:
            return self._alias_index[lower_value]
        
        return None
    
    def contains(self, value: str) -> bool:
        """Check if a value exists in the registry."""
        return self.lookup(value) is not None
    
    def get(self, value: str) -> T | None:
        """Alias for lookup() - get an entry by ID or alias."""
        return self.lookup(value)
    
    def all_ids(self) -> list[str]:
        """Get all primary IDs in the registry."""
        return [entry.id for entry in self.entries]
    
    def all_values(self) -> set[str]:
        """Get all valid values (IDs and aliases)."""
        values: set[str] = set()
        for entry in self.entries:
            values.add(entry.id)
            values.update(entry.aliases)
        return values
    
    def __len__(self) -> int:
        return len(self.entries)
    
    def __contains__(self, value: str) -> bool:
        return self.contains(value)


class RegistryLoader(ABC):
    """
    Abstract base class for registry loaders.
    
    Each marker type has its own loader that knows how to parse its registry file.
    """
    
    def __init__(self, schema_dir: Path):
        """
        Initialize the loader.
        
        Args:
            schema_dir: Path to the _schema directory
        """
        self.schema_dir = schema_dir
    
    @property
    @abstractmethod
    def marker_type(self) -> MarkerType:
        """The marker type this loader handles."""
        pass
    
    @property
    @abstractmethod
    def registry_filename(self) -> str:
        """Filename of the registry file relative to schema_dir."""
        pass
    
    @property
    def registry_path(self) -> Path:
        """Full path to the registry file."""
        return self.schema_dir / self.registry_filename
    
    @abstractmethod
    def load(self) -> Registry:
        """
        Load and parse the registry file.
        
        Returns:
            Populated Registry instance
        """
        pass
    
    def _read_file(self) -> str:
        """Read the registry file contents."""
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry file not found: {self.registry_path}")
        return self.registry_path.read_text(encoding="utf-8")
    
    def _extract_with_pattern(
        self, 
        content: str, 
        pattern: str,
        group: int = 1
    ) -> list[tuple[str, int]]:
        """
        Extract values using a regex pattern.
        
        Args:
            content: File content to search
            pattern: Regex pattern with capture group
            group: Which capture group to extract (default: 1)
            
        Returns:
            List of (value, line_number) tuples
        """
        results: list[tuple[str, int]] = []
        compiled = re.compile(pattern, re.MULTILINE)
        
        for line_num, line in enumerate(content.split("\n"), start=1):
            for match in compiled.finditer(line):
                if match.groups():
                    value = match.group(group)
                    results.append((value, line_num))
        
        return results
