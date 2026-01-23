"""
Person registry loader for CCASH validation.

Parses persons.md to load person data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field

from ccash_validator.models.enums import MarkerType
from ccash_validator.registry.base import Registry, RegistryEntry, RegistryLoader


class PersonAddress(BaseModel):
    """Person address data."""
    
    street1: str = ""
    street2: Optional[str] = None
    city: str = ""
    state: str = ""
    zip: str = ""
    country: str = "USA"
    
    @property
    def formatted(self) -> str:
        """Return formatted address string."""
        parts = [self.street1]
        if self.street2:
            parts.append(self.street2)
        parts.append(f"{self.city}, {self.state} {self.zip}")
        return ", ".join(parts)


class PersonLegalName(BaseModel):
    """Person legal name components."""
    
    first: str = ""
    middle: Optional[str] = None
    last: str = ""
    suffix: Optional[str] = None
    
    @property
    def full(self) -> str:
        """Return full name."""
        parts = [self.first]
        if self.middle:
            parts.append(self.middle)
        parts.append(self.last)
        if self.suffix:
            parts.append(self.suffix)
        return " ".join(parts)


class PersonEntry(RegistryEntry):
    """A person in the registry."""
    
    person_type: str = Field(default="individual", description="individual or entity")
    status: str = Field(default="active", description="active, inactive, pending")
    display_name: str = Field(default="", description="Display name")
    entity_name: Optional[str] = Field(default=None, description="Entity name if type=entity")
    legal_name: PersonLegalName = Field(default_factory=PersonLegalName)
    address: PersonAddress = Field(default_factory=PersonAddress)
    address_formatted: str = Field(default="", description="Pre-formatted address")
    phone: str = Field(default="", description="Phone number")
    email: str = Field(default="", description="Email address")
    signature_name: str = Field(default="", description="Name for signature block")
    notes: str = Field(default="", description="Notes about person")
    
    model_config = {"frozen": False}
    
    def get_field(self, field_path: str) -> str:
        """
        Get a field value by dot-notation path.
        
        Args:
            field_path: Field path like 'display_name' or 'legal_name.first'
            
        Returns:
            Field value as string, or empty string if not found
        """
        parts = field_path.split(".")
        obj: Any = self
        
        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                return ""
        
        if obj is None:
            return ""
        return str(obj)


class PersonsRegistry(Registry[PersonEntry]):
    """Registry of persons."""
    
    marker_type: MarkerType = Field(default=MarkerType.PERSON)


def load_persons_registry(schema_dir: Path) -> PersonsRegistry:
    """
    Load persons registry from persons.md.
    
    Args:
        schema_dir: Path to _schema directory
        
    Returns:
        PersonsRegistry with all persons loaded
    """
    persons_file = schema_dir / "persons.md"
    
    if not persons_file.exists():
        return PersonsRegistry(
            marker_type=MarkerType.PERSON,
            source_file=str(persons_file),
            entries=[],
        )
    
    content = persons_file.read_text(encoding="utf-8")
    entries = _parse_persons_md(content)
    
    return PersonsRegistry(
        marker_type=MarkerType.PERSON,
        source_file=str(persons_file),
        entries=entries,
    )


def _parse_persons_md(content: str) -> list[PersonEntry]:
    """
    Parse persons.md content into PersonEntry objects.
    
    Extracts YAML blocks for each person.
    """
    entries = []
    
    # Find all person sections (### P001 - Name or ### RA001 - Name)
    person_pattern = re.compile(
        r'^### ([A-Z0-9]+(?:-[A-Z0-9]+)*)\s*[-–]\s*(.+?)$',
        re.MULTILINE
    )
    
    # Find YAML code blocks
    yaml_pattern = re.compile(
        r'```yaml\n(.*?)```',
        re.DOTALL
    )
    
    matches = list(person_pattern.finditer(content))
    
    for i, match in enumerate(matches):
        person_id = match.group(1)
        person_name = match.group(2).strip()
        
        # Get content between this section and the next
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section_content = content[start:end]
        
        # Find YAML block in section
        yaml_match = yaml_pattern.search(section_content)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            entry = _parse_person_yaml(person_id, yaml_content, match.start())
            if entry:
                entries.append(entry)
    
    return entries


def _parse_person_yaml(person_id: str, yaml_content: str, line_num: int) -> Optional[PersonEntry]:
    """Parse a single person's YAML block."""
    
    def get_value(pattern: str, default: str = "") -> str:
        match = re.search(pattern, yaml_content, re.MULTILINE)
        if match:
            value = match.group(1).strip().strip('"\'')
            # Skip placeholder values
            if value.startswith("[__") or value == "null":
                return default
            return value
        return default
    
    def get_nested_value(parent: str, child: str, default: str = "") -> str:
        # Look for indented child under parent
        pattern = rf'{parent}:\s*\n(?:.*?\n)*?\s+{child}:\s*["\']?([^"\'\n]+)'
        match = re.search(pattern, yaml_content, re.MULTILINE)
        if match:
            value = match.group(1).strip().strip('"\'')
            if value.startswith("[__") or value == "null":
                return default
            return value
        return default
    
    person_type = get_value(r'^type:\s*(.+)$', "individual")
    status = get_value(r'^status:\s*(.+)$', "active")
    display_name = get_value(r'^display_name:\s*(.+)$', "")
    entity_name = get_value(r'^entity_name:\s*(.+)$', "")
    
    # Legal name
    legal_name = PersonLegalName(
        first=get_nested_value("legal_name", "first"),
        middle=get_nested_value("legal_name", "middle") or None,
        last=get_nested_value("legal_name", "last"),
        suffix=get_nested_value("legal_name", "suffix") or None,
    )
    
    # Address
    address = PersonAddress(
        street1=get_nested_value("address", "street1"),
        street2=get_nested_value("address", "street2") or None,
        city=get_nested_value("address", "city"),
        state=get_nested_value("address", "state"),
        zip=get_nested_value("address", "zip"),
        country=get_nested_value("address", "country") or "USA",
    )
    
    address_formatted = get_value(r'^address_formatted:\s*(.+)$', "")
    if not address_formatted and address.street1:
        address_formatted = address.formatted
    
    phone = get_value(r'^phone:\s*(.+)$', "")
    email = get_value(r'^email:\s*(.+)$', "")
    
    # Signature block
    signature_name = get_nested_value("signature_block", "name_line")
    if not signature_name:
        signature_name = display_name
    
    notes = get_value(r'^notes:\s*(.+)$', "")
    
    # Use entity_name as display_name for entities
    if person_type == "entity" and entity_name and not display_name:
        display_name = entity_name
    
    return PersonEntry(
        id=person_id,
        person_type=person_type,
        status=status,
        display_name=display_name,
        entity_name=entity_name,
        legal_name=legal_name,
        address=address,
        address_formatted=address_formatted,
        phone=phone,
        email=email,
        signature_name=signature_name,
        notes=notes,
        source_line=line_num,
    )
