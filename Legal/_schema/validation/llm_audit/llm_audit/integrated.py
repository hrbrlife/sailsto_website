"""
Integrated audit orchestrator v3.

Enhanced pipeline optimized for Grok's 2M context window:
- Phase 0: Knowledge base loading (authoritative source grounding)
- Phase 1: Mechanical analysis (regex + dependency graph)
- Phase 2: Master summary (all docs -> 3000 word overview)
- Phase 3: Per-doc summaries (1000 words each with full context)
- Phase 4: Contextual audits (full related docs + master + summaries + KB)

Anti-Hallucination Design:
- Auditors receive relevant knowledge base context
- Legal/factual assertions require [SOURCE:] citations
- SkepticAgent verifies citations against knowledge base
- Findings with invalid citations are rejected
"""

from __future__ import annotations

import asyncio
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from llm_audit.cache import AuditCache, CacheManager, compute_file_hash
from llm_audit.models.agents import AgentRole, AuditContext, OrchestratorConfig, AgentConfig
from llm_audit.models.findings import AuditFinding, ConsolidatedReport, AuditSeverity
from llm_audit.providers import LLMProvider, create_provider_from_env
from llm_audit.agents.base import create_auditor
from llm_audit.agents.pipeline import ConsolidatorAgent, SkepticAgent, ReviewerAgent
from llm_audit.knowledge_base import KnowledgeBase
from llm_audit.citations import CitationValidator


class IntegratedOrchestrator:
    """
    Enhanced audit pipeline for Grok's massive context.
    
    Key improvements:
    - Knowledge base grounding to prevent hallucinations
    - Master summary generated from ALL docs at once
    - Rich 1000-word per-doc summaries with full context
    - Audits include full text of related docs (not truncated)
    - Citation validation for all legal/factual assertions
    - Hash-based caching with dependency awareness
    """
    
    def __init__(
        self,
        docs_dir: Path,
        schema_dir: Path,
        output_dir: Path,
        config: Optional[OrchestratorConfig] = None,
        provider: Optional[LLMProvider] = None,
        knowledge_base_dir: Optional[Path] = None,
    ):
        self.docs_dir = docs_dir
        self.schema_dir = schema_dir
        self.output_dir = output_dir
        self.config = config or OrchestratorConfig()
        self.provider = provider or create_provider_from_env()
        
        # Initialize cache
        self.cache_manager = CacheManager(output_dir)
        
        # Document paths keyed by doc_code
        self._doc_paths: dict[str, Path] = {}
        
        # Master summary (generated once, shared across all audits)
        self._master_summary: Optional[str] = None
        
        # Validation report text
        self._validation_report: str = ""
        
        # Knowledge base for grounding (anti-hallucination)
        self._knowledge_base: Optional[KnowledgeBase] = None
        self._citation_validator: Optional[CitationValidator] = None
        self._kb_dir = knowledge_base_dir or (schema_dir / "knowledge_base")
        self._research_outputs_dir = schema_dir / "research_outputs"
        
        # Load KB if directory exists
        if self._kb_dir.exists():
            self._knowledge_base = KnowledgeBase(self._kb_dir)
            self._knowledge_base.load()
            self._citation_validator = CitationValidator(self._knowledge_base)
            print(f"[KB] Loaded {len(self._knowledge_base.documents)} knowledge sources from {self._kb_dir}")
        else:
            print(f"[KB] Warning: Knowledge base directory not found at {self._kb_dir}")
        
        # Load research outputs as secondary sources (weight: 0.5)
        self._research_outputs: dict[str, str] = {}
        if self._research_outputs_dir.exists():
            for ro_file in self._research_outputs_dir.glob("*.md"):
                if ro_file.name not in ("README.md", "prompts.md"):
                    self._research_outputs[ro_file.stem] = ro_file.read_text(encoding="utf-8")
            print(f"[RO] Loaded {len(self._research_outputs)} research outputs (weight: 0.5)")
    
    @property
    def knowledge_base(self) -> Optional[KnowledgeBase]:
        """Get the loaded knowledge base."""
        return self._knowledge_base
    
    @property
    def citation_validator(self) -> Optional[CitationValidator]:
        """Get the citation validator."""
        return self._citation_validator
    
    @property
    def cache(self) -> AuditCache:
        return self.cache_manager.cache
    
    # ========== Document Discovery ==========
    
    def _extract_doc_code(self, filename: str) -> Optional[str]:
        """Extract document code from filename."""
        name = filename.replace(".md", "")
        
        # Standard codes: A1, B1, B11, F1, etc.
        match = re.match(r'^([A-Z][0-9]+[a-z]?)_', name)
        if match:
            return match.group(1)
        
        # Overview docs: 00_README, 00_Business_Model
        match = re.match(r'^(00_[A-Za-z_]+)', name)
        if match:
            return match.group(1)
        
        # Special docs
        match = re.match(r'^([A-Z]+[0-9]+)_', name)
        if match:
            return match.group(1)
        
        return name if name else None
    
    def _discover_documents(self) -> dict[str, Path]:
        """Discover all documents and their codes."""
        docs: dict[str, Path] = {}
        
        # Check for migrated layout
        subdirs = ["Company", "Client_Series", "Internal"]
        for subdir in subdirs:
            dir_path = self.docs_dir / subdir
            if dir_path.exists():
                for md_file in dir_path.rglob("*.md"):
                    doc_code = self._extract_doc_code(md_file.name)
                    if doc_code:
                        docs[doc_code] = md_file
        
        # Fallback to flat layout
        if not docs:
            for md_file in self.docs_dir.glob("*.md"):
                doc_code = self._extract_doc_code(md_file.name)
                if doc_code:
                    docs[doc_code] = md_file
        
        self._doc_paths = docs
        return docs
    
    def _scan_and_hash_documents(self) -> dict[str, bool]:
        """
        Scan all documents and update hashes.
        
        Returns:
            Dict of doc_code -> has_changed
        """
        docs = self._discover_documents()
        changes = {}
        
        for doc_code, doc_path in docs.items():
            content = doc_path.read_text(encoding="utf-8")
            rel_path = str(doc_path.relative_to(self.docs_dir))
            
            # Get old hash
            old_doc = self.cache.get_document(doc_code)
            old_hash = old_doc.content_hash if old_doc else None
            
            # Update hash
            new_doc = self.cache.update_document_hash(doc_code, rel_path, content)
            
            # Track if changed
            changes[doc_code] = (old_hash != new_doc.content_hash)
        
        return changes
    
    # ========== Phase 1: Mechanical Analysis ==========
    
    def _run_regex_validator(self) -> dict[str, Any]:
        """Run ccash-validate on all documents."""
        validator_venv = self.schema_dir / "validation" / "ccash_validator" / ".venv"
        patterns_file = self.schema_dir / "validation" / "patterns.yaml"
        
        if not patterns_file.exists():
            return {"error": "patterns.yaml not found"}
        
        python_path = validator_venv / "bin" / "python" if validator_venv.exists() else "python3"
        
        try:
            result = subprocess.run(
                [
                    str(python_path), "-m", "ccash_validator.cli",
                    "validate", "--all",
                    "--patterns", str(patterns_file),
                    "--json"
                ],
                cwd=str(self.docs_dir),
                capture_output=True,
                text=True,
                timeout=120,
            )
            
            if result.stdout:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return {"raw_output": result.stdout[:5000]}
        except Exception as e:
            return {"error": str(e)}
        
        return {}
    
    def _build_dependency_graph(self) -> dict[str, dict[str, list[str]]]:
        """Build document dependency graph from DOC markers."""
        doc_pattern = re.compile(r'\[DOC:([^\]]+)\]')
        
        graph: dict[str, dict[str, list[str]]] = {}
        
        for doc_code, doc_path in self._doc_paths.items():
            content = doc_path.read_text(encoding="utf-8")
            
            # Find all DOC references
            references = set()
            for match in doc_pattern.finditer(content):
                ref = match.group(1)
                # Normalize: strip anchors, section refs
                ref = re.sub(r'[#§].*$', '', ref).strip()
                ref = re.sub(r'\s.*$', '', ref).strip()
                if ref and ref != doc_code:
                    references.add(ref)
            
            graph[doc_code] = {
                "references": list(sorted(references)),
                "referenced_by": [],
            }
        
        # Build reverse references
        for doc_code, node in graph.items():
            for ref in node["references"]:
                if ref in graph:
                    graph[ref]["referenced_by"].append(doc_code)
        
        # Sort referenced_by lists
        for node in graph.values():
            node["referenced_by"] = list(sorted(node["referenced_by"]))
        
        self.cache.dependency_graph = graph
        return graph
    
    def _get_all_related_docs(self, doc_code: str) -> set[str]:
        """Get all documents related to doc_code (references + referenced_by)."""
        if doc_code not in self.cache.dependency_graph:
            return set()
        
        node = self.cache.dependency_graph[doc_code]
        return set(node["references"]) | set(node["referenced_by"])
    
    def _format_validation_report(self, results: dict[str, Any]) -> str:
        """Format validation results as readable text."""
        lines = [
            "# CCASH Document Validation Report",
            f"Generated: {datetime.utcnow().isoformat()}",
            "",
        ]
        
        if "error" in results:
            lines.append(f"**Error**: {results['error']}")
            return "\n".join(lines)
        
        # Summary stats
        total_errors = 0
        total_warnings = 0
        
        if "documents" in results:
            for doc in results["documents"]:
                total_errors += doc.get("error_count", 0)
                total_warnings += doc.get("warning_count", 0)
        
        lines.extend([
            "## Summary",
            f"- Total Errors: {total_errors}",
            f"- Total Warnings: {total_warnings}",
            "",
            "## Document Results",
            "",
        ])
        
        if "documents" in results:
            for doc in results["documents"]:
                doc_code = doc.get("document_code", "unknown")
                status = "✅" if doc.get("error_count", 0) == 0 else "❌"
                lines.append(f"### {status} {doc_code}")
                lines.append(f"- Errors: {doc.get('error_count', 0)}")
                lines.append(f"- Warnings: {doc.get('warning_count', 0)}")
                
                if doc.get("results"):
                    for r in doc["results"][:5]:  # Limit to 5 per doc
                        lines.append(f"  - {r.get('level', '?')}: {r.get('message', '')[:100]}")
                lines.append("")
        
        return "\n".join(lines)
    
    def _format_dependency_map(self) -> str:
        """Format dependency graph as readable text."""
        lines = [
            "# Document Dependency Map",
            "",
            "## Overview",
            f"Total Documents: {len(self.cache.dependency_graph)}",
            "",
            "## Document Relationships",
            "",
        ]
        
        for doc_code in sorted(self.cache.dependency_graph.keys()):
            node = self.cache.dependency_graph[doc_code]
            refs = node.get("references", [])
            ref_by = node.get("referenced_by", [])
            
            lines.append(f"### {doc_code}")
            if refs:
                lines.append(f"  References: {', '.join(refs)}")
            if ref_by:
                lines.append(f"  Referenced by: {', '.join(ref_by)}")
            if not refs and not ref_by:
                lines.append("  (No cross-references)")
            lines.append("")
        
        return "\n".join(lines)
    
    # ========== Phase 2: Master Summary ==========
    
    async def _generate_master_summary(self) -> str:
        """
        Generate comprehensive 3000-word master summary from ALL documents.
        
        This is fed to the model with ALL document content at once,
        leveraging Grok 4's massive 2M context window.
        """
        # Build mega-document with ALL content
        all_docs_content = []
        
        for doc_code in sorted(self._doc_paths.keys()):
            doc_path = self._doc_paths[doc_code]
            content = doc_path.read_text(encoding="utf-8")
            all_docs_content.append(f"{'='*60}\n# DOCUMENT: {doc_code}\n# File: {doc_path.name}\n{'='*60}\n\n{content}")
        
        mega_document = "\n\n".join(all_docs_content)
        
        # Add validation report and dependency map
        context = f"""
{self._validation_report}

{self._format_dependency_map()}

{'='*80}
FULL DOCUMENT CORPUS ({len(self._doc_paths)} documents)
{'='*80}

{mega_document}
"""
        
        system_prompt = """You are a legal document analyst creating a comprehensive overview of a document corpus.

Your task is to create a DETAILED 3000-word MASTER SUMMARY that maps out:

1. **BUSINESS OVERVIEW** (~500 words)
   - What is this business? (CCASH Money Services - a Montana Series LLC)
   - What services does it provide?
   - How is it structured (Series LLC with functional and client series)?
   - Who are the key parties?

2. **DOCUMENT ARCHITECTURE** (~500 words)
   - How are the documents organized?
   - What is the hierarchy (Articles → Operating Agreement → Policies → Agreements)?
   - Which documents are foundational vs. operational?
   - Key document dependencies and relationships

3. **REGULATORY FRAMEWORK** (~500 words)
   - Montana LLC law requirements (MCA 35-8)
   - Federal requirements (FinCEN MSB, BSA/AML)
   - State money transmitter considerations
   - Key compliance obligations

4. **OPERATIONAL STRUCTURE** (~500 words)
   - Officer roles and responsibilities (CEO, CTO, CMO, CFO, CCO)
   - Series structure and purpose of each series
   - Client onboarding and relationship model
   - Service delivery framework

5. **KEY DEFINED TERMS AND CONCEPTS** (~500 words)
   - Important defined terms and their meanings
   - Critical markers and cross-references
   - Standard document patterns

6. **DOCUMENT CROSS-REFERENCE MAP** (~500 words)
   - Which documents reference which others
   - Clusters of related documents
   - Key dependencies for each major document

DO NOT include issues, recommendations, or audit findings.
This is purely a FACTUAL DESCRIPTION of what exists.
Be precise and detailed. Use specific document codes (B1, F1, etc.) when referencing documents."""

        user_prompt = f"""Create a comprehensive 3000-word MASTER SUMMARY of the following document corpus.

This is the complete set of legal and operational documents for CCASH Money Services (US) Series LLC.

{context}"""

        config = AgentConfig(
            role=AgentRole.CONSOLIDATOR,
            model=self.config.default_model or "x-ai/grok-4.1-fast",
            provider=self.config.default_provider,
            temperature=0.3,
            max_tokens=6000,  # ~3000 words + formatting
            timeout_seconds=300,
            retry_count=2,
        )
        
        try:
            response = await self.provider.complete(
                agent_config=config,
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
            )
            return response.strip()
        except Exception as e:
            return f"[Master summary generation failed: {e}]"
    
    # ========== Phase 3: Per-Doc Summaries ==========
    
    async def _generate_doc_summary(self, doc_code: str) -> str:
        """
        Generate detailed 1000-word summary for a single document.
        
        Context includes:
        - The master summary
        - Validation results
        - All other documents (for cross-reference context)
        """
        if doc_code not in self._doc_paths:
            return ""
        
        doc_path = self._doc_paths[doc_code]
        content = doc_path.read_text(encoding="utf-8")
        
        # Build context with ALL docs (we can afford it with 2M context!)
        other_docs = []
        for other_code in sorted(self._doc_paths.keys()):
            if other_code != doc_code:
                other_path = self._doc_paths[other_code]
                other_content = other_path.read_text(encoding="utf-8")
                other_docs.append(f"### {other_code}\n{other_content[:10000]}")  # First 10K of each
        
        context = f"""
# MASTER SUMMARY (for context)
{self._master_summary or "[Not yet generated]"}

# VALIDATION REPORT
{self._validation_report}

# TARGET DOCUMENT: {doc_code}
{content}

# OTHER DOCUMENTS (for cross-reference context)
{"".join(other_docs[:20])}  # Limit to 20 for very large corpora
"""

        system_prompt = """You are a legal document summarizer creating a detailed summary of a specific document.

Create a 1000-word summary structured as:

1. **PURPOSE AND SCOPE** (~200 words)
   - What is this document for?
   - Who does it govern/apply to?
   - What legal function does it serve?

2. **KEY PARTIES AND ROLES** (~150 words)
   - Who are the parties involved?
   - What are their respective roles and responsibilities?
   - How do they relate to each other?

3. **MAIN OBLIGATIONS AND REQUIREMENTS** (~250 words)
   - What are the key obligations?
   - What must each party do?
   - What are the compliance requirements?

4. **CRITICAL DEFINED TERMS** (~150 words)
   - What terms are defined?
   - What do the key markers (TERM:, DOC:, etc.) reference?

5. **RELATIONSHIPS TO OTHER DOCUMENTS** (~150 words)
   - Which documents does this reference?
   - Which documents reference this one?
   - How does it fit in the document hierarchy?

6. **NOTABLE PROVISIONS** (~100 words)
   - Any unusual or critical clauses
   - Key protective provisions
   - Important limitations or conditions

DO NOT include issues, recommendations, or audit findings.
This is purely a FACTUAL DESCRIPTION of the document contents."""

        user_prompt = f"""Create a detailed 1000-word summary of document {doc_code}.

{context}"""

        config = AgentConfig(
            role=AgentRole.CONSOLIDATOR,
            model=self.config.default_model or "x-ai/grok-4.1-fast",
            provider=self.config.default_provider,
            temperature=0.3,
            max_tokens=2500,  # ~1000 words + formatting
            timeout_seconds=180,
            retry_count=2,
        )
        
        try:
            response = await self.provider.complete(
                agent_config=config,
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
            )
            return response.strip()
        except Exception as e:
            return f"[Summary generation failed: {e}]"
    
    async def _generate_doc_summaries(
        self,
        doc_codes: list[str],
        max_parallel: int = 3
    ) -> dict[str, str]:
        """Generate summaries for multiple documents."""
        semaphore = asyncio.Semaphore(max_parallel)
        results: dict[str, str] = {}
        
        async def generate_one(doc_code: str):
            async with semaphore:
                summary = await self._generate_doc_summary(doc_code)
                self.cache.mark_summary_done(doc_code, summary)
                results[doc_code] = summary
                # Save cache incrementally after each summary
                self.cache_manager.save()
                return doc_code
        
        tasks = [generate_one(code) for code in doc_codes]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    # ========== Phase 4: Contextual Audit ==========
    
    def _build_full_audit_context(self, doc_code: str) -> AuditContext:
        """
        Build comprehensive audit context for a document.
        
        Includes:
        - Target document in FULL
        - ALL related documents in FULL (from DOC markers)
        - Master summary
        - Validation results
        - Summaries of ALL non-related documents
        """
        if doc_code not in self._doc_paths:
            raise ValueError(f"Unknown document: {doc_code}")
        
        doc_path = self._doc_paths[doc_code]
        target_content = doc_path.read_text(encoding="utf-8")
        
        # Get related documents
        related_codes = self._get_all_related_docs(doc_code)
        
        # Build related documents (FULL TEXT, no truncation!)
        related_docs: dict[str, str] = {}
        for rel_code in related_codes:
            if rel_code in self._doc_paths:
                rel_content = self._doc_paths[rel_code].read_text(encoding="utf-8")
                related_docs[rel_code] = rel_content  # Full text!
        
        # Build summaries for non-related docs
        other_summaries = []
        for other_code in sorted(self.cache.summaries.keys()):
            if other_code != doc_code and other_code not in related_codes:
                summary = self.cache.summaries[other_code]
                other_summaries.append(f"### {other_code}\n{summary}")
        
        # Get validation results for this doc
        validation_text = ""
        if doc_code in self.cache.validation_results:
            val = self.cache.validation_results[doc_code]
            validation_text = json.dumps(val, indent=2)
        
        # Load schema context
        schema_context = self._load_schema_context()
        
        # Build the mega-context
        context_parts = [
            f"# COMPREHENSIVE AUDIT CONTEXT FOR {doc_code}",
            f"Generated: {datetime.utcnow().isoformat()}",
            "",
            "=" * 80,
            "# SECTION 1: MASTER SUMMARY",
            "=" * 80,
            "",
            self._master_summary or "[Not available]",
            "",
            "=" * 80,
            "# SECTION 2: MECHANICAL VALIDATION RESULTS",
            "=" * 80,
            "",
            f"## Validation for {doc_code}",
            validation_text or "No validation data available",
            "",
            "## Dependency Map",
            self._format_dependency_map(),
            "",
            "=" * 80,
            "# SECTION 3: TARGET DOCUMENT (FULL TEXT)",
            "=" * 80,
            "",
            f"## {doc_code} - {doc_path.name}",
            "",
            target_content,
            "",
        ]
        
        if related_docs:
            context_parts.extend([
                "=" * 80,
                "# SECTION 4: RELATED DOCUMENTS (FULL TEXT)",
                "=" * 80,
                "",
            ])
            for rel_code, rel_content in related_docs.items():
                rel_type = "references" if rel_code in self.cache.dependency_graph.get(doc_code, {}).get("references", []) else "referenced_by"
                context_parts.extend([
                    f"## {rel_code} ({rel_type})",
                    "",
                    rel_content,
                    "",
                ])
        
        if other_summaries:
            context_parts.extend([
                "=" * 80,
                "# SECTION 5: OTHER DOCUMENTS (SUMMARIES ONLY)",
                "=" * 80,
                "",
            ])
            context_parts.extend(other_summaries)
        
        full_context = "\n".join(context_parts)
        
        return AuditContext(
            document_path=str(doc_path),
            document_name=doc_path.name,
            document_code=doc_code,
            document_content=full_context,
            defined_terms=schema_context.get("defined_terms"),
            obligations=schema_context.get("obligations"),
            decisions=schema_context.get("decisions"),
            roles=schema_context.get("roles"),
            related_docs=related_docs,
        )
    
    def _load_schema_context(self) -> dict[str, str]:
        """Load schema files for context."""
        context = {}
        files = [
            ("defined_terms", "defined_terms.md"),
            ("obligations", "obligations.md"),
            ("decisions", "decisions_rights.md"),
            ("roles", "roles.md"),
        ]
        
        for key, filename in files:
            filepath = self.schema_dir / filename
            if filepath.exists():
                context[key] = filepath.read_text()
        
        return context
    
    async def _audit_single_document(
        self,
        doc_code: str,
        save_intermediates: bool = True,
    ) -> ConsolidatedReport:
        """Run full audit pipeline on a single document."""
        context = self._build_full_audit_context(doc_code)
        
        # Create output directory
        doc_output_dir = self.output_dir / doc_code
        doc_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save input context including KB stats
        if save_intermediates:
            kb_info = {}
            if self._knowledge_base:
                # Get unique domain tags across all documents
                all_tags = set()
                for doc in self._knowledge_base.documents.values():
                    all_tags.update(doc.domain_tags)
                kb_info = {
                    "kb_sources_loaded": len(self._knowledge_base.documents),
                    "kb_topics_available": list(sorted(all_tags)),
                }
            
            (doc_output_dir / "input_context.json").write_text(
                json.dumps({
                    "document_code": doc_code,
                    "document_path": context.document_path,
                    "timestamp": datetime.utcnow().isoformat(),
                    "context_length_chars": len(context.document_content),
                    "context_length_tokens_approx": len(context.document_content) // 4,
                    "related_docs": list(context.related_docs.keys()),
                    **kb_info,
                }, indent=2)
            )
            (doc_output_dir / "full_context.md").write_text(context.document_content)
        
        # Run auditors - with knowledge base injection
        auditor_configs = self.config.get_enabled_auditors()
        auditors = [
            create_auditor(cfg.role, cfg, self.provider, knowledge_base=self._knowledge_base) 
            for cfg in auditor_configs
        ]
        
        # Parallel execution
        semaphore = asyncio.Semaphore(self.config.max_parallel)
        
        async def run_auditor(auditor):
            async with semaphore:
                return await auditor.audit(context)
        
        agent_results = await asyncio.gather(
            *[run_auditor(a) for a in auditors],
            return_exceptions=True,
        )
        
        # Filter and save results
        valid_results = []
        for result in agent_results:
            if hasattr(result, 'findings'):
                valid_results.append(result)
                if save_intermediates:
                    agent_file = doc_output_dir / "agent_findings" / f"{result.agent_role}.json"
                    agent_file.parent.mkdir(exist_ok=True)
                    agent_file.write_text(json.dumps(result.model_dump(), indent=2, default=str))
        
        original_count = sum(len(ar.findings) for ar in valid_results)
        
        # Consolidate
        consolidator_config = self.config.get_agent_config(AgentRole.CONSOLIDATOR)
        consolidator = ConsolidatorAgent(consolidator_config, self.provider)
        consolidated = await consolidator.consolidate(valid_results, context)
        
        if save_intermediates:
            (doc_output_dir / "consolidated_findings.json").write_text(
                json.dumps([f.model_dump() for f in consolidated], indent=2, default=str)
            )
        
        # Skeptic - with knowledge base for citation validation
        disputed_count = 0
        rejected_findings = []
        citation_stats = {"total": 0, "valid": 0, "invalid": 0}
        if self.config.enable_skeptic:
            skeptic_config = self.config.get_agent_config(AgentRole.SKEPTIC)
            
            # Create online verifier config if KB is loaded and skeptic uses :online model
            # The :online suffix indicates the model has web search capabilities
            online_verifier_config = None
            if self._knowledge_base and ':online' in skeptic_config.model:
                online_verifier_config = AgentConfig(
                    role=AgentRole.SKEPTIC,  # Sub-role
                    model=skeptic_config.model,  # Use same online model
                    provider=skeptic_config.provider,
                    temperature=0.2,
                    max_tokens=2000,  # Online verification is more concise
                    timeout_seconds=30,
                )
                print("    [Online verification enabled for KB fallback]")
            
            skeptic = SkepticAgent(
                skeptic_config, 
                self.provider, 
                knowledge_base=self._knowledge_base,
                online_verifier_config=online_verifier_config,
            )
            revised, new_findings, rejected = await skeptic.challenge(consolidated, context)
            disputed_count = len(consolidated) - len(revised)
            final_findings = revised + new_findings
            rejected_findings = rejected
            
            # Calculate citation stats from rejected findings
            for rf in rejected:
                citation_stats["total"] += 1
                if rf.get("reason") == "hallucinated_source":
                    citation_stats["invalid"] += 1
                else:
                    citation_stats["valid"] += 1
            
            if save_intermediates:
                (doc_output_dir / "skeptic_review.json").write_text(
                    json.dumps({
                        "original_count": len(consolidated),
                        "disputed_count": disputed_count,
                        "new_findings": len(new_findings),
                        "rejected_findings": rejected_findings,
                        "citation_stats": citation_stats,
                        "final_findings": [f.model_dump() for f in final_findings],
                    }, indent=2, default=str)
                )
        else:
            final_findings = consolidated
        
        # Final review
        if self.config.require_reviewer_approval:
            reviewer_config = self.config.get_agent_config(AgentRole.REVIEWER)
            reviewer = ReviewerAgent(reviewer_config, self.provider)
            report = await reviewer.review(
                final_findings,
                context,
                original_count=original_count,
                consolidated_count=len(consolidated),
                disputed_count=disputed_count,
                citation_stats=citation_stats,
            )
        else:
            # Auto-evaluate
            critical = sum(1 for f in final_findings if (f.final_severity or f.severity) == AuditSeverity.CRITICAL)
            high = sum(1 for f in final_findings if (f.final_severity or f.severity) == AuditSeverity.HIGH)
            
            if critical > 0:
                status = "fail"
                summary = f"Audit failed: {critical} critical findings."
            elif high > 0:
                status = "needs_review"
                summary = f"Review needed: {high} high-severity findings."
            else:
                status = "pass"
                summary = f"Audit passed with {len(final_findings)} findings."
            
            report = ConsolidatedReport(
                document_path=context.document_path,
                document_name=context.document_name,
                document_code=doc_code,
                findings=final_findings,
                summary=summary,
                overall_status=status,
                original_finding_count=original_count,
                deduplicated_count=len(consolidated),
                disputed_count=disputed_count,
                citation_stats=citation_stats,
            )
        
        # Save final report
        if save_intermediates:
            (doc_output_dir / "final_report.json").write_text(
                json.dumps(report.model_dump(), indent=2, default=str)
            )
        
        # Mark audit complete
        self.cache.mark_audit_done(doc_code)
        
        return report
    
    # ========== Main Pipeline ==========
    
    async def run_full_audit(
        self,
        force: bool = False,
        progress_callback=None,
    ) -> dict[str, ConsolidatedReport]:
        """
        Run the complete 4-phase audit pipeline.
        
        Phase 1: Mechanical Analysis (regex + dependency graph)
        Phase 2: Master Summary (if any doc changed)
        Phase 3: Per-Doc Summaries (changed docs + their dependents)
        Phase 4: Contextual Audits
        """
        def log(msg: str):
            if progress_callback:
                progress_callback(msg)
            else:
                print(msg)
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # ===== PHASE 1: Mechanical Analysis =====
        log("=" * 60)
        log("PHASE 1: MECHANICAL ANALYSIS")
        log("=" * 60)
        
        log("\n  Scanning documents...")
        changes = self._scan_and_hash_documents()
        changed_docs = [code for code, changed in changes.items() if changed]
        log(f"  Found {len(self._doc_paths)} documents, {len(changed_docs)} changed")
        
        log("\n  Running regex validation...")
        validation_results = self._run_regex_validator()
        self._validation_report = self._format_validation_report(validation_results)
        
        # Store per-doc validation results
        if "documents" in validation_results:
            for doc_result in validation_results["documents"]:
                doc_code = doc_result.get("document_code")
                if doc_code:
                    self.cache.mark_validation_done(doc_code, doc_result)
        
        # Save validation report
        (self.output_dir / "validation_report.md").write_text(self._validation_report)
        (self.output_dir / "validation_report.json").write_text(
            json.dumps(validation_results, indent=2, default=str)
        )
        
        log("\n  Building dependency graph...")
        self._build_dependency_graph()
        (self.output_dir / "dependency_map.json").write_text(
            json.dumps(self.cache.dependency_graph, indent=2)
        )
        (self.output_dir / "dependency_map.md").write_text(self._format_dependency_map())
        log(f"  Graph built with {len(self.cache.dependency_graph)} nodes")
        
        # ===== PHASE 2: Master Summary =====
        log("\n" + "=" * 60)
        log("PHASE 2: MASTER SUMMARY")
        log("=" * 60)
        
        # Only regenerate if ANY doc changed or doesn't exist
        master_summary_file = self.output_dir / "master_summary.md"
        if force or changed_docs or not master_summary_file.exists():
            log("\n  Generating master summary (3000 words from ALL docs)...")
            self._master_summary = await self._generate_master_summary()
            master_summary_file.write_text(self._master_summary)
            log("  Master summary complete")
        else:
            log("\n  Loading existing master summary (no docs changed)...")
            self._master_summary = master_summary_file.read_text()
        
        # ===== PHASE 3: Per-Doc Summaries =====
        log("\n" + "=" * 60)
        log("PHASE 3: PER-DOC SUMMARIES")
        log("=" * 60)
        
        # Determine which docs need summaries
        # Changed docs + docs that reference them + docs they reference
        needs_summary = set(changed_docs) if not force else set(self._doc_paths.keys())
        
        for doc_code in list(changed_docs):
            related = self._get_all_related_docs(doc_code)
            needs_summary.update(related)
        
        # Also check cache for any without summaries
        for doc_code in self._doc_paths:
            if doc_code not in self.cache.summaries:
                needs_summary.add(doc_code)
        
        needs_summary_list = sorted(needs_summary)
        
        if needs_summary_list:
            log(f"\n  Generating summaries for {len(needs_summary_list)} documents...")
            await self._generate_doc_summaries(needs_summary_list, max_parallel=3)
            log("  Summaries complete")
        else:
            log("\n  All summaries up to date")
        
        # Save all summaries
        (self.output_dir / "summaries.json").write_text(
            json.dumps(self.cache.summaries, indent=2)
        )
        
        # Also save as markdown
        summaries_md = ["# Document Summaries", ""]
        for doc_code in sorted(self.cache.summaries.keys()):
            summaries_md.append(f"## {doc_code}")
            summaries_md.append("")
            summaries_md.append(self.cache.summaries[doc_code])
            summaries_md.append("")
        (self.output_dir / "summaries.md").write_text("\n".join(summaries_md))
        
        # ===== PHASE 4: Contextual Audits =====
        log("\n" + "=" * 60)
        log("PHASE 4: CONTEXTUAL AUDITS")
        log("=" * 60)
        
        # Determine what needs audit
        if force:
            needs_audit = list(self._doc_paths.keys())
        else:
            needs_audit = self.cache.get_documents_needing_audit()
            # Also audit docs whose related docs changed
            for doc_code in list(changed_docs):
                related = self._get_all_related_docs(doc_code)
                for rel in related:
                    if rel not in needs_audit and rel in self._doc_paths:
                        needs_audit.append(rel)
        
        needs_audit = sorted(set(needs_audit))
        
        reports: dict[str, ConsolidatedReport] = {}
        
        if needs_audit:
            log(f"\n  Auditing {len(needs_audit)} documents...")
            
            for i, doc_code in enumerate(needs_audit):
                log(f"\n  [{i+1}/{len(needs_audit)}] Auditing {doc_code}...")
                try:
                    report = await self._audit_single_document(doc_code)
                    reports[doc_code] = report
                    finding_count = len(report.findings)
                    status = report.overall_status
                    log(f"    ✓ {status}: {finding_count} findings")
                    
                    # Save cache incrementally after each successful audit
                    self.cache.mark_audit_done(doc_code)
                    self.cache_manager.save()
                    
                except Exception as e:
                    log(f"    ✗ Error: {e}")
                    reports[doc_code] = ConsolidatedReport(
                        document_path=str(self._doc_paths.get(doc_code, "")),
                        document_name=f"{doc_code}.md",
                        document_code=doc_code,
                        findings=[],
                        summary=f"Audit failed: {e}",
                        overall_status="error",
                    )
        else:
            log("\n  No documents need auditing")
        
        # ===== Generate Master Report =====
        log("\n" + "=" * 60)
        log("GENERATING MASTER REPORT")
        log("=" * 60)
        
        self._generate_master_report(reports)
        
        # Save cache
        self.cache.last_full_run = datetime.utcnow()
        self.cache_manager.save()
        
        log("\n" + "=" * 60)
        log("✅ AUDIT COMPLETE")
        log("=" * 60)
        log(f"\n  Total documents: {len(self._doc_paths)}")
        log(f"  Audited this run: {len(reports)}")
        log(f"  Results saved to: {self.output_dir}")
        
        return reports
    
    def _generate_master_report(self, reports: dict[str, ConsolidatedReport]) -> None:
        """Generate comprehensive master report."""
        # Aggregate stats
        total_docs = len(self._doc_paths)
        audited = len(reports)
        passed = sum(1 for r in reports.values() if r.overall_status == "pass")
        failed = sum(1 for r in reports.values() if r.overall_status == "fail")
        needs_review = sum(1 for r in reports.values() if r.overall_status == "needs_review")
        
        all_findings = []
        for doc_code, report in reports.items():
            for finding in report.findings:
                all_findings.append({
                    "document": doc_code,
                    **finding.model_dump(),
                })
        
        severity_counts = {
            "critical": sum(1 for f in all_findings if f.get("severity") == "critical" or f.get("final_severity") == "critical"),
            "high": sum(1 for f in all_findings if f.get("severity") == "high" or f.get("final_severity") == "high"),
            "medium": sum(1 for f in all_findings if f.get("severity") == "medium" or f.get("final_severity") == "medium"),
            "low": sum(1 for f in all_findings if f.get("severity") == "low" or f.get("final_severity") == "low"),
        }
        
        master_report = {
            "generated_at": datetime.utcnow().isoformat(),
            "pipeline_version": "2.0",
            "summary": {
                "total_documents": total_docs,
                "documents_audited": audited,
                "passed": passed,
                "failed": failed,
                "needs_review": needs_review,
                "total_findings": len(all_findings),
                "severity_breakdown": severity_counts,
            },
            "documents": {
                doc_code: {
                    "status": report.overall_status,
                    "finding_count": len(report.findings),
                    "summary": report.summary,
                }
                for doc_code, report in reports.items()
            },
            "all_findings": all_findings,
        }
        
        (self.output_dir / "master_report.json").write_text(
            json.dumps(master_report, indent=2, default=str)
        )
        
        # Human-readable markdown version
        md_lines = [
            "# CCASH Document Audit Report",
            f"Generated: {datetime.utcnow().isoformat()}",
            f"Pipeline Version: 2.0 (Grok 4 Optimized)",
            "",
            "## Executive Summary",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Documents | {total_docs} |",
            f"| Audited | {audited} |",
            f"| Passed | {passed} |",
            f"| Failed | {failed} |",
            f"| Needs Review | {needs_review} |",
            f"| Total Findings | {len(all_findings)} |",
            "",
            "## Findings by Severity",
            "",
            f"| Severity | Count |",
            f"|----------|-------|",
            f"| 🚨 Critical | {severity_counts['critical']} |",
            f"| ❌ High | {severity_counts['high']} |",
            f"| ⚠️ Medium | {severity_counts['medium']} |",
            f"| 💡 Low | {severity_counts['low']} |",
            "",
            "## Document Status",
            "",
        ]
        
        for doc_code in sorted(reports.keys()):
            report = reports[doc_code]
            icon = "✅" if report.overall_status == "pass" else "❌" if report.overall_status == "fail" else "⚠️"
            md_lines.append(f"### {icon} {doc_code}")
            md_lines.append(f"**Status**: {report.overall_status}")
            md_lines.append(f"**Findings**: {len(report.findings)}")
            md_lines.append(f"**Summary**: {report.summary}")
            md_lines.append("")
        
        if all_findings:
            md_lines.append("## All Findings")
            md_lines.append("")
            
            # Group by severity
            for severity in ["critical", "high", "medium", "low"]:
                sev_findings = [f for f in all_findings if (f.get("final_severity") or f.get("severity")) == severity]
                if sev_findings:
                    md_lines.append(f"### {severity.upper()} Findings ({len(sev_findings)})")
                    md_lines.append("")
                    for f in sev_findings:
                        md_lines.append(f"#### {f.get('title', 'Untitled')}")
                        md_lines.append(f"- **Document**: {f.get('document')}")
                        md_lines.append(f"- **Category**: {f.get('category')}")
                        md_lines.append(f"- **Location**: {f.get('location', 'N/A')}")
                        md_lines.append(f"- **Description**: {f.get('description', '')}")
                        md_lines.append(f"- **Recommendation**: {f.get('recommendation', '')}")
                        md_lines.append("")
        
        (self.output_dir / "master_report.md").write_text("\n".join(md_lines))
