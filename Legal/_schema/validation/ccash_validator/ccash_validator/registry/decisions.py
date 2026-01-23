"""
Decisions registry loader for [DECISION:*] and [RIGHT:*] markers.

Loads decision and right IDs from decisions_rights.md.
"""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import Field

from ccash_validator.models.enums import MarkerType
from ccash_validator.registry.base import Registry, RegistryEntry, RegistryLoader


class DecisionEntry(RegistryEntry):
    """A decision or right registry entry."""
    
    entry_type: str = Field(default="decision", description="Type: 'decision' or 'right'")
    description: str = Field(default="", description="Description")
    authority: str = Field(default="", description="Decision authority")
    stakeholder: str = Field(default="", description="Right holder")


class DecisionsRegistry(Registry[DecisionEntry]):
    """Registry of decision and right IDs."""
    
    marker_type: MarkerType = MarkerType.DECISION  # Also handles RIGHT


class DecisionsLoader(RegistryLoader):
    """
    Loader for decisions_rights.md.
    
    Extracts both DECISION and RIGHT IDs from the same file.
    Expected formats:
    - Table rows: | `COMPLIANCE-001` | Description | Authority |
    - [DECISION:ID] and [RIGHT:ID] markers
    - Inline code: `ID-001`
    """
    
    def __init__(self, schema_dir: Path, marker_type: MarkerType = MarkerType.DECISION):
        """
        Initialize loader.
        
        Args:
            schema_dir: Path to _schema directory
            marker_type: Whether loading for DECISION or RIGHT
        """
        super().__init__(schema_dir)
        self._marker_type = marker_type
    
    @property
    def marker_type(self) -> MarkerType:
        return self._marker_type
    
    @property
    def registry_filename(self) -> str:
        return "decisions_rights.md"
    
    def load(self) -> DecisionsRegistry:
        """
        Load decisions/rights from decisions_rights.md.
        """
        content = self._read_file()
        entries: list[DecisionEntry] = []
        seen: set[str] = set()
        
        # Patterns for extracting IDs
        patterns = [
            # [DECISION:ID] or [RIGHT:ID] markers
            r'\[(DECISION|RIGHT):([A-Za-z0-9_-]+)\]',
            # Table row: | `ID` | Description |
            r'^\|\s*`([A-Z]+-[A-Z]*-?[0-9]+)`\s*\|',
            # Inline code with ID format
            r'`([A-Z]+-[A-Z]*-?[0-9]+)`',
        ]
        
        # Track current section to determine entry type
        current_section = "decision"
        
        for line_num, line in enumerate(content.split("\n"), start=1):
            # Track section headers
            if re.match(r'^##\s+.*[Dd]ecision', line):
                current_section = "decision"
            elif re.match(r'^##\s+.*[Rr]ight', line):
                current_section = "right"
            
            # Check marker patterns
            for match in re.finditer(patterns[0], line):
                entry_type = match.group(1).lower()
                entry_id = match.group(2)
                
                if entry_id.lower() in seen:
                    continue
                seen.add(entry_id.lower())
                
                entries.append(DecisionEntry(
                    id=entry_id,
                    source_line=line_num,
                    entry_type=entry_type,
                ))
            
            # Check table and inline patterns
            for pattern in patterns[1:]:
                for match in re.finditer(pattern, line):
                    entry_id = match.group(1)
                    
                    if entry_id.lower() in seen:
                        continue
                    seen.add(entry_id.lower())
                    
                    # Try to extract description from table
                    description = ""
                    if "|" in line:
                        parts = line.split("|")
                        if len(parts) >= 3:
                            description = parts[2].strip()
                    
                    entries.append(DecisionEntry(
                        id=entry_id,
                        source_line=line_num,
                        entry_type=current_section,
                        description=description,
                    ))
        
        return DecisionsRegistry(
            marker_type=self._marker_type,
            source_file=str(self.registry_path),
            entries=entries,
        )


def load_decisions_registry(schema_dir: Path) -> DecisionsRegistry:
    """
    Convenience function to load decisions registry.
    
    Args:
        schema_dir: Path to _schema directory
        
    Returns:
        Populated DecisionsRegistry
    """
    loader = DecisionsLoader(schema_dir, MarkerType.DECISION)
    return loader.load()


def load_rights_registry(schema_dir: Path) -> DecisionsRegistry:
    """
    Convenience function to load rights registry.
    
    Args:
        schema_dir: Path to _schema directory
        
    Returns:
        Populated DecisionsRegistry (shared file with decisions)
    """
    loader = DecisionsLoader(schema_dir, MarkerType.RIGHT)
    return loader.load()
