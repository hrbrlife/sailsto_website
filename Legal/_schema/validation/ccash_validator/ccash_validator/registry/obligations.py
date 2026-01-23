"""
Obligations registry loader for [OBL:*] markers.

Loads obligation IDs from obligations.md.
"""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import Field

from ccash_validator.models.enums import MarkerType
from ccash_validator.registry.base import Registry, RegistryEntry, RegistryLoader


class ObligationEntry(RegistryEntry):
    """An obligation registry entry."""
    
    description: str = Field(default="", description="Obligation description")
    obligor: str = Field(default="", description="Party with the obligation")
    obligee: str = Field(default="", description="Party owed the obligation")
    source_doc: str = Field(default="", description="Source document")
    section: str = Field(default="", description="Section reference")


class ObligationsRegistry(Registry[ObligationEntry]):
    """Registry of obligation IDs."""
    
    marker_type: MarkerType = MarkerType.OBL


class ObligationsLoader(RegistryLoader):
    """
    Loader for obligations.md.
    
    Extracts obligation IDs from the ledger-style format.
    Expected formats:
    - Table rows: | `OBL-REG-001` | Description | ...
    - Ledger blocks with [OBL:ID] markers
    - Inline code: `REG-001`, `PARTNER-RESTRICT-001`
    """
    
    @property
    def marker_type(self) -> MarkerType:
        return MarkerType.OBL
    
    @property
    def registry_filename(self) -> str:
        return "obligations.md"
    
    def load(self) -> ObligationsRegistry:
        """
        Load obligations from obligations.md.
        
        The file uses a ledger-style format with obligation blocks.
        """
        content = self._read_file()
        entries: list[ObligationEntry] = []
        seen: set[str] = set()
        
        # Multiple patterns to catch different formats
        patterns = [
            # [OBL:ID] marker format
            r'\[OBL:([A-Za-z0-9_-]+)\]',
            # Table row: | `OBL-ID` |
            r'^\|\s*`(OBL-[A-Z]+-[0-9]{3})`\s*\|',
            # Table row: | `ID` | (without OBL- prefix)
            r'^\|\s*`([A-Z]+-[A-Z]*-?[0-9]{3})`\s*\|',
            # Inline code with ID format
            r'`([A-Z]+-[A-Z]+-[0-9]{3})`',
            # Header-style: ### OBL-ID
            r'^###\s+(OBL-[A-Z]+-[0-9]{3})',
        ]
        
        for line_num, line in enumerate(content.split("\n"), start=1):
            for pattern in patterns:
                for match in re.finditer(pattern, line):
                    obl_id = match.group(1)
                    
                    # Normalize: ensure consistent format
                    # Valid formats: OBL-REG-001, REG-001, PARTNER-RESTRICT-001
                    
                    # Skip duplicates
                    if obl_id.lower() in seen:
                        continue
                    seen.add(obl_id.lower())
                    
                    # Try to extract description from table format
                    description = ""
                    if "|" in line:
                        parts = line.split("|")
                        if len(parts) >= 3:
                            description = parts[2].strip()
                    
                    entries.append(ObligationEntry(
                        id=obl_id,
                        source_line=line_num,
                        description=description,
                    ))
        
        return ObligationsRegistry(
            marker_type=MarkerType.OBL,
            source_file=str(self.registry_path),
            entries=entries,
        )


def load_obligations_registry(schema_dir: Path) -> ObligationsRegistry:
    """
    Convenience function to load obligations registry.
    
    Args:
        schema_dir: Path to _schema directory
        
    Returns:
        Populated ObligationsRegistry
    """
    loader = ObligationsLoader(schema_dir)
    return loader.load()
