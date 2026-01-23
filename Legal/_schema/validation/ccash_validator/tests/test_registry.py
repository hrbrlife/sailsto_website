"""
Tests for the registry module.
"""

import pytest
from pathlib import Path

from ccash_validator.models.enums import MarkerType
from ccash_validator.registry.base import Registry, RegistryEntry


class TestRegistryEntry:
    """Tests for RegistryEntry."""
    
    def test_entry_creation(self):
        """Test basic entry creation."""
        entry = RegistryEntry(
            id="Company",
            aliases=["CCASH", "CCASH LLC"],
            source_line=10,
        )
        assert entry.id == "Company"
        assert len(entry.aliases) == 2
    
    def test_entry_matches(self):
        """Test matching by id or alias."""
        entry = RegistryEntry(
            id="Company",
            aliases=["CCASH"],
        )
        
        assert entry.matches("Company")
        assert entry.matches("company")  # Case-insensitive
        assert entry.matches("CCASH")
        assert not entry.matches("Other")
    
    def test_entry_matches_case_sensitive(self):
        """Test case-sensitive matching."""
        entry = RegistryEntry(id="Company")
        
        assert entry.matches("Company", case_sensitive=True)
        assert not entry.matches("company", case_sensitive=True)


class TestRegistry:
    """Tests for Registry base class."""
    
    def test_registry_lookup(self):
        """Test registry lookup by ID."""
        entries = [
            RegistryEntry(id="Term1"),
            RegistryEntry(id="Term2", aliases=["Alias2"]),
        ]
        
        registry = Registry(
            marker_type=MarkerType.TERM,
            source_file="test.md",
            entries=entries,
        )
        
        assert registry.lookup("Term1") is not None
        assert registry.lookup("term1") is not None  # Case-insensitive
        assert registry.lookup("Term2") is not None
        assert registry.lookup("Alias2") is not None  # By alias
        assert registry.lookup("NotFound") is None
    
    def test_registry_contains(self):
        """Test registry contains check."""
        entries = [RegistryEntry(id="Test")]
        registry = Registry(
            marker_type=MarkerType.TERM,
            source_file="test.md",
            entries=entries,
        )
        
        assert registry.contains("Test")
        assert "Test" in registry
        assert not registry.contains("Other")
    
    def test_registry_all_ids(self):
        """Test getting all IDs."""
        entries = [
            RegistryEntry(id="A"),
            RegistryEntry(id="B"),
            RegistryEntry(id="C"),
        ]
        registry = Registry(
            marker_type=MarkerType.TERM,
            source_file="test.md",
            entries=entries,
        )
        
        ids = registry.all_ids()
        assert ids == ["A", "B", "C"]
    
    def test_registry_all_values(self):
        """Test getting all values including aliases."""
        entries = [
            RegistryEntry(id="A", aliases=["X", "Y"]),
            RegistryEntry(id="B"),
        ]
        registry = Registry(
            marker_type=MarkerType.TERM,
            source_file="test.md",
            entries=entries,
        )
        
        values = registry.all_values()
        assert values == {"A", "B", "X", "Y"}
    
    def test_registry_len(self):
        """Test registry length."""
        entries = [RegistryEntry(id="A"), RegistryEntry(id="B")]
        registry = Registry(
            marker_type=MarkerType.TERM,
            source_file="test.md",
            entries=entries,
        )
        assert len(registry) == 2


class TestRegistryIntegration:
    """Integration tests with actual registry files."""
    
    @pytest.fixture
    def real_schema_dir(self) -> Path:
        """Get real schema directory if it exists."""
        test_dir = Path(__file__).parent
        schema_dir = test_dir.parent.parent.parent  # tests -> ccash_validator -> validation -> _schema
        if schema_dir.exists() and (schema_dir / "defined_terms.md").exists():
            return schema_dir
        pytest.skip("Schema directory not available")
    
    def test_load_terms_registry(self, real_schema_dir):
        """Test loading real terms registry."""
        from ccash_validator.registry.terms import load_terms_registry
        
        registry = load_terms_registry(real_schema_dir)
        assert len(registry) > 0
        
        # Should have common terms
        assert registry.contains("Company") or registry.contains("Client")
    
    def test_load_documents_registry(self, real_schema_dir):
        """Test loading real documents registry."""
        from ccash_validator.registry.documents import load_documents_registry
        
        registry = load_documents_registry(real_schema_dir)
        assert len(registry) > 0
        
        # Should have standard document codes
        assert registry.contains("B1") or registry.contains("F1")
    
    def test_load_obligations_registry(self, real_schema_dir):
        """Test loading real obligations registry."""
        from ccash_validator.registry.obligations import load_obligations_registry
        
        registry = load_obligations_registry(real_schema_dir)
        # May or may not have entries depending on file content
        assert registry is not None
