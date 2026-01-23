"""
Knowledge Base Integration Module.

Provides domain-agnostic loading, indexing, and retrieval of authoritative
source documents for grounding LLM auditors in factual information.

Design Principles:
- Domain-agnostic: Works for MSB, healthcare, legal, or any document corpus
- Citation-first: Enables [SOURCE:filename#section] markers
- RAG-ready: Supports chunking for large files, full injection for small
- Verifiable: All assertions must be traceable to sources
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field


@dataclass
class KnowledgeDocument:
    """A single document in the knowledge base."""
    
    filename: str
    filepath: Path
    content: str
    content_hash: str
    size_bytes: int
    line_count: int
    
    # Extracted metadata
    title: Optional[str] = None
    domain_tags: list[str] = field(default_factory=list)
    
    # Chunking for large files
    chunks: list[str] = field(default_factory=list)
    chunk_count: int = 0
    
    @property
    def is_large(self) -> bool:
        """Whether this document exceeds the large file threshold."""
        return self.line_count > 1000 or self.size_bytes > 50_000
    
    def get_excerpt(self, max_lines: int = 200) -> str:
        """Get first N lines as excerpt."""
        lines = self.content.split('\n')
        return '\n'.join(lines[:max_lines])
    
    def search(self, query: str, context_lines: int = 5) -> list[dict[str, Any]]:
        """
        Search document for query string.
        
        Returns list of matches with surrounding context.
        """
        matches = []
        lines = self.content.split('\n')
        query_lower = query.lower()
        
        for i, line in enumerate(lines):
            if query_lower in line.lower():
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                matches.append({
                    'line_number': i + 1,
                    'match_line': line,
                    'context': '\n'.join(lines[start:end]),
                    'filename': self.filename,
                })
        
        return matches


class KnowledgeBaseConfig(BaseModel):
    """Configuration for knowledge base integration."""
    
    # Paths
    knowledge_base_dir: str = Field(
        default="_schema/knowledge_base",
        description="Path to knowledge base directory relative to workspace"
    )
    
    # File patterns
    include_patterns: list[str] = Field(
        default=["*.txt", "*.md"],
        description="Glob patterns for files to include"
    )
    exclude_patterns: list[str] = Field(
        default=["README.md", "*.tmp"],
        description="Glob patterns for files to exclude"
    )
    
    # Injection settings
    max_full_inject_lines: int = Field(
        default=500,
        description="Max lines for full document injection into context"
    )
    max_full_inject_bytes: int = Field(
        default=30_000,
        description="Max bytes for full document injection"
    )
    
    # Chunking for large files
    chunk_size_lines: int = Field(
        default=200,
        description="Number of lines per chunk for large files"
    )
    chunk_overlap_lines: int = Field(
        default=20,
        description="Overlap between chunks for context continuity"
    )
    
    # Context injection
    max_kb_context_tokens: int = Field(
        default=50_000,
        description="Maximum tokens to inject from KB into auditor context"
    )
    
    # Citation settings
    require_citations: bool = Field(
        default=True,
        description="Whether to require [SOURCE:] citations for legal/factual claims"
    )
    citation_pattern: str = Field(
        default=r'\[SOURCE:([^\]]+)\]',
        description="Regex pattern for source citations"
    )
    
    # Online fallback settings
    allow_online_fallback: bool = Field(
        default=True,
        description="Allow online verification when KB citation fails"
    )
    online_search_timeout: int = Field(
        default=30,
        description="Timeout in seconds for online verification requests"
    )
    
    model_config = {"extra": "allow"}


class KnowledgeBase:
    """
    Domain-agnostic knowledge base for grounding LLM auditors.
    
    Usage:
        kb = KnowledgeBase(Path("/workspace/_schema/knowledge_base"))
        kb.load()
        
        # Get relevant context for an audit
        context = kb.get_context_for_topic("BSA/AML", max_tokens=10000)
        
        # Verify a citation
        valid, evidence = kb.verify_citation("31_cfr_1022.380_msb_registration.txt")
        
        # Search for specific content
        results = kb.search("money transmitter license")
    """
    
    def __init__(
        self,
        base_path: Path,
        config: Optional[KnowledgeBaseConfig] = None,
    ):
        self.base_path = base_path
        self.config = config or KnowledgeBaseConfig()
        
        # Document index
        self.documents: dict[str, KnowledgeDocument] = {}
        
        # Metadata
        self.total_lines = 0
        self.total_bytes = 0
        self.loaded = False
    
    def load(self) -> None:
        """Load all documents from the knowledge base directory."""
        if not self.base_path.exists():
            raise FileNotFoundError(f"Knowledge base directory not found: {self.base_path}")
        
        self.documents.clear()
        self.total_lines = 0
        self.total_bytes = 0
        
        # Find all matching files
        for pattern in self.config.include_patterns:
            for filepath in self.base_path.glob(pattern):
                # Check exclusions
                if any(filepath.match(exc) for exc in self.config.exclude_patterns):
                    continue
                
                self._load_document(filepath)
        
        self.loaded = True
    
    def _load_document(self, filepath: Path) -> None:
        """Load a single document."""
        try:
            content = filepath.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")
            return
        
        lines = content.split('\n')
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        doc = KnowledgeDocument(
            filename=filepath.name,
            filepath=filepath,
            content=content,
            content_hash=content_hash,
            size_bytes=len(content.encode('utf-8')),
            line_count=len(lines),
            title=self._extract_title(content),
            domain_tags=self._extract_domain_tags(filepath.name, content),
        )
        
        # Chunk large files
        if doc.is_large:
            doc.chunks = self._chunk_content(content)
            doc.chunk_count = len(doc.chunks)
        
        self.documents[filepath.name] = doc
        self.total_lines += doc.line_count
        self.total_bytes += doc.size_bytes
    
    def _extract_title(self, content: str) -> Optional[str]:
        """Extract title from document content."""
        # Look for markdown title
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Look for first non-empty line
        for line in content.split('\n')[:10]:
            line = line.strip()
            if line and not line.startswith(('#', '/', '*', '-')):
                return line[:100]
        
        return None
    
    def _extract_domain_tags(self, filename: str, content: str) -> list[str]:
        """Extract domain tags from filename and content."""
        tags = []
        
        # Filename-based tags
        name_lower = filename.lower()
        
        # Generic domain detection (extensible)
        domain_keywords = {
            'bsa': ['bsa', 'bank_secrecy', 'aml', 'anti_money'],
            'fincen': ['fincen', 'financial_crimes'],
            'msb': ['msb', 'money_service', 'money_transmit'],
            'cfr': ['cfr', 'code_of_federal'],
            'usc': ['usc', 'united_states_code'],
            'ofac': ['ofac', 'sanctions', 'sdn'],
            'privacy': ['privacy', 'gdpr', 'ccpa', 'glba'],
            'state': ['montana', 'mt_', 'state_'],
            'irs': ['irs', 'form_8300', 'tax'],
            'ffiec': ['ffiec'],
        }
        
        for tag, keywords in domain_keywords.items():
            if any(kw in name_lower for kw in keywords):
                tags.append(tag)
        
        return tags
    
    def _chunk_content(self, content: str) -> list[str]:
        """Split content into overlapping chunks."""
        lines = content.split('\n')
        chunks = []
        
        chunk_size = self.config.chunk_size_lines
        overlap = self.config.chunk_overlap_lines
        
        i = 0
        while i < len(lines):
            end = min(i + chunk_size, len(lines))
            chunk = '\n'.join(lines[i:end])
            chunks.append(chunk)
            i += chunk_size - overlap
        
        return chunks
    
    def get_document(self, filename: str) -> Optional[KnowledgeDocument]:
        """Get a specific document by filename."""
        return self.documents.get(filename)
    
    def search(
        self,
        query: str,
        max_results: int = 10,
        domain_filter: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        """
        Search all documents for a query string.
        
        Args:
            query: Search string (case-insensitive)
            max_results: Maximum results to return
            domain_filter: Only search documents with these domain tags
            
        Returns:
            List of match dicts with context
        """
        all_matches = []
        
        for doc in self.documents.values():
            # Apply domain filter
            if domain_filter:
                if not any(tag in doc.domain_tags for tag in domain_filter):
                    continue
            
            matches = doc.search(query)
            all_matches.extend(matches)
        
        # Sort by relevance (number of query terms in match)
        query_terms = query.lower().split()
        all_matches.sort(
            key=lambda m: sum(t in m['match_line'].lower() for t in query_terms),
            reverse=True
        )
        
        return all_matches[:max_results]
    
    def verify_citation(self, citation: str) -> tuple[bool, Optional[str]]:
        """
        Verify a [SOURCE:filename] or [SOURCE:filename#anchor] citation.
        
        Args:
            citation: Citation string (filename or filename#anchor)
            
        Returns:
            Tuple of (is_valid, evidence_text)
        """
        # Parse citation
        if '#' in citation:
            filename, anchor = citation.split('#', 1)
        else:
            filename = citation
            anchor = None
        
        # Normalize filename
        filename = filename.strip()
        
        # Check if document exists
        doc = self.documents.get(filename)
        if not doc:
            # Try partial match
            for name, d in self.documents.items():
                if filename in name or name in filename:
                    doc = d
                    break
        
        if not doc:
            return False, None
        
        # If anchor specified, search for it
        if anchor:
            # Try exact match first
            matches = doc.search(anchor, context_lines=10)
            if matches:
                return True, matches[0]['context']
            
            # Try with spaces (Article12 -> Article 12)
            import re
            spaced_anchor = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', anchor)
            if spaced_anchor != anchor:
                matches = doc.search(spaced_anchor, context_lines=10)
                if matches:
                    return True, matches[0]['context']
            
            # Try removing common prefixes (Section1.2 -> 1.2)
            for prefix in ['Section', 'Article', 'Part', 'Chapter']:
                if anchor.startswith(prefix):
                    remainder = anchor[len(prefix):]
                    matches = doc.search(f"{prefix} {remainder}", context_lines=10)
                    if matches:
                        return True, matches[0]['context']
            
            return False, f"Document exists but anchor '{anchor}' not found"
        
        # Return excerpt as evidence
        return True, doc.get_excerpt(50)
    
    def get_context_for_topics(
        self,
        topics: list[str],
        max_chars: int = 100_000,
    ) -> str:
        """
        Get relevant KB content for specified topics.
        
        Args:
            topics: List of topic keywords to search for
            max_chars: Maximum characters to return
            
        Returns:
            Formatted context string with source citations
        """
        context_parts = []
        used_chars = 0
        seen_files = set()
        
        # First, include small files that match domain tags
        for doc in self.documents.values():
            if used_chars >= max_chars:
                break
            
            # Check if any topic matches domain tags or filename
            topic_match = any(
                t.lower() in doc.filename.lower() or
                any(t.lower() in tag for tag in doc.domain_tags)
                for t in topics
            )
            
            if topic_match and not doc.is_large:
                if doc.filename not in seen_files:
                    header = f"\n{'='*60}\n[SOURCE:{doc.filename}]\n{'='*60}\n"
                    context_parts.append(header + doc.content)
                    used_chars += len(doc.content) + len(header)
                    seen_files.add(doc.filename)
        
        # Then, add search results from remaining docs
        for topic in topics:
            if used_chars >= max_chars:
                break
            
            results = self.search(topic, max_results=5)
            for result in results:
                if result['filename'] not in seen_files:
                    doc = self.documents[result['filename']]
                    if doc.is_large:
                        # For large files, just include relevant chunks
                        header = f"\n{'='*60}\n[SOURCE:{doc.filename}] (excerpt)\n{'='*60}\n"
                        context_parts.append(header + result['context'])
                        used_chars += len(result['context']) + len(header)
                    else:
                        # Include full small file
                        header = f"\n{'='*60}\n[SOURCE:{doc.filename}]\n{'='*60}\n"
                        context_parts.append(header + doc.content)
                        used_chars += len(doc.content) + len(header)
                    seen_files.add(doc.filename)
        
        return '\n'.join(context_parts)
    
    def get_full_index(self) -> str:
        """Get formatted index of all documents in KB."""
        lines = [
            "# Knowledge Base Index",
            f"Total Documents: {len(self.documents)}",
            f"Total Lines: {self.total_lines:,}",
            f"Total Size: {self.total_bytes:,} bytes",
            "",
            "## Documents",
            "",
        ]
        
        for filename in sorted(self.documents.keys()):
            doc = self.documents[filename]
            tags = ', '.join(doc.domain_tags) if doc.domain_tags else 'general'
            size_indicator = "📄" if not doc.is_large else "📚"
            lines.append(f"- {size_indicator} `{filename}` ({doc.line_count} lines) [{tags}]")
        
        return '\n'.join(lines)
    
    def get_citation_instructions(self) -> str:
        """Get instructions for citing sources."""
        return """
## Citation Requirements

When making factual or legal assertions, you MUST cite your sources using:

    [SOURCE:filename.txt]

For specific sections, use anchors:

    [SOURCE:filename.txt#section_name]

### Available Sources

""" + self.get_full_index() + """

### Citation Rules

1. **REQUIRED**: All legal/regulatory assertions must cite a source
2. **NO HALLUCINATION**: Do not cite statutes, regulations, or requirements not in the knowledge base
3. **VERIFY**: If a claim cannot be cited to a source, state "No source available" and lower confidence
4. **BE SPECIFIC**: Cite the most specific source available

### Invalid Citation Examples

❌ "MCA Title 32, Chapter 9 requires..." (if not in KB)
❌ "According to federal law..." (too vague)
❌ "Montana requires MTL..." (unless KB confirms)

### Valid Citation Examples

✅ [SOURCE:31_cfr_1022.380_msb_registration.txt] requires MSB registration
✅ [SOURCE:mca_35-8-304_series_liability.txt] addresses series liability
✅ "No KB source found for Montana MTL requirements" (if truly not present)
"""


def load_knowledge_base(
    workspace_root: Path,
    config: Optional[KnowledgeBaseConfig] = None,
) -> KnowledgeBase:
    """
    Load knowledge base from workspace.
    
    Args:
        workspace_root: Root of the workspace
        config: Optional configuration
        
    Returns:
        Loaded KnowledgeBase instance
    """
    config = config or KnowledgeBaseConfig()
    kb_path = workspace_root / config.knowledge_base_dir
    
    kb = KnowledgeBase(kb_path, config)
    kb.load()
    
    return kb
