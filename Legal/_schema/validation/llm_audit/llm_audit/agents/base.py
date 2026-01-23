"""
Base auditor agent class.

Provides the foundation for all specialist auditor implementations.
Now includes knowledge base integration and citation requirements.
"""

from __future__ import annotations

import abc
import re
import uuid
from datetime import datetime
from typing import Any, Optional

from llm_audit.models.agents import AgentConfig, AgentRole, AuditContext
from llm_audit.models.findings import (
    AgentAuditResult,
    AuditFinding,
    AuditCategory,
    AuditSeverity,
)
from llm_audit.providers import LLMProvider, ProviderError


# Citation pattern for extraction
SOURCE_CITATION_PATTERN = re.compile(r'\[SOURCE:([^\]]+)\]', re.IGNORECASE)


class BaseAuditor(abc.ABC):
    """
    Abstract base class for auditor agents.
    
    Subclasses implement specific auditor logic for different domains
    (legal, compliance, technical, etc.).
    
    Now includes:
    - Knowledge base context injection
    - Citation requirements for legal/factual claims
    - Domain-agnostic prompting
    
    Usage:
        class ComplianceAuditor(BaseAuditor):
            role = AgentRole.COMPLIANCE_AUDITOR
            
            def get_system_prompt(self) -> str:
                return "You are a compliance auditor..."
        
        auditor = ComplianceAuditor(config, provider)
        result = await auditor.audit(context)
    """
    
    # Subclasses must set these
    role: AgentRole
    
    # Default finding categories for this auditor type
    default_categories: list[AuditCategory] = []
    
    # Domain topics for KB retrieval (subclasses can override)
    knowledge_topics: list[str] = []
    
    def __init__(
        self,
        config: AgentConfig,
        provider: LLMProvider,
        knowledge_base: Optional[Any] = None,  # KnowledgeBase type
    ):
        """
        Initialize auditor.
        
        Args:
            config: Agent configuration
            provider: LLM provider for completions
            knowledge_base: Optional loaded KnowledgeBase for grounding
        """
        self.config = config
        self.provider = provider
        self.knowledge_base = knowledge_base
    
    @abc.abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this auditor.
        
        Returns:
            System prompt string
        """
        ...
    
    def get_citation_instructions(self) -> str:
        """Get citation requirement instructions."""
        return """

## CITATION REQUIREMENTS (MANDATORY)

When making legal, regulatory, or factual assertions, you MUST:

1. **CITE SOURCES** using: [SOURCE:filename.txt] or [SOURCE:filename.txt#section]

2. **NO HALLUCINATION**: Only cite laws/regulations present in the Knowledge Base
   - If a requirement is NOT in the KB, say "No KB source available"
   - Do NOT invent statutes, CFR sections, or state requirements

3. **CONFIDENCE ADJUSTMENT**:
   - High confidence (0.8+): Claim fully supported by KB source
   - Medium confidence (0.5-0.7): Claim partially supported or inferred
   - Low confidence (<0.5): No KB source, based on general knowledge

4. **EXAMPLES**:
   ✅ "MSB registration required per [SOURCE:31_cfr_1022.380_msb_registration.txt]"
   ✅ "Series liability protected under [SOURCE:mca_35-8-304_series_liability.txt]"
   ❌ "Montana requires MTL under MCA Title 32" (if not in KB - DON'T MAKE THIS UP)

FINDINGS WITH UNCITED LEGAL CLAIMS WILL BE PENALIZED.
FINDINGS CITING NON-EXISTENT SOURCES WILL BE REJECTED.
"""
    
    def get_knowledge_base_context(self, max_chars: int = 80000) -> str:
        """
        Get relevant knowledge base content for this auditor.
        
        Args:
            max_chars: Maximum characters to include
            
        Returns:
            Formatted KB context string
        """
        if not self.knowledge_base:
            return ""
        
        # Get topics for this auditor (can be overridden by subclasses)
        topics = self.knowledge_topics or self._get_default_topics()
        
        context = self.knowledge_base.get_context_for_topics(topics, max_chars)
        
        if context:
            return f"""

## AUTHORITATIVE KNOWLEDGE BASE

The following are authoritative sources. Use [SOURCE:filename] to cite them.
{context}

{self.knowledge_base.get_full_index()}
"""
        return ""
    
    def _get_default_topics(self) -> list[str]:
        """Get default KB topics based on role."""
        role_topics = {
            AgentRole.LEGAL_AUDITOR: ["llc", "montana", "contract", "liability"],
            AgentRole.COMPLIANCE_AUDITOR: ["bsa", "aml", "fincen", "msb", "sar", "ctr"],
            AgentRole.TECHNICAL_AUDITOR: ["schema", "marker", "validation"],
            AgentRole.FINANCIAL_AUDITOR: ["capital", "insurance", "fee"],
            AgentRole.DATA_PRIVACY_AUDITOR: ["privacy", "gdpr", "ccpa", "glba"],
            AgentRole.OPERATIONAL_AUDITOR: ["governance", "officer", "succession"],
        }
        return role_topics.get(self.role, [])
    
    def get_audit_prompt(self, context: AuditContext) -> str:
        """
        Build the audit prompt from context.
        
        Override for custom prompt formatting.
        
        Args:
            context: Audit context with document and schema info
            
        Returns:
            Prompt string for the user message
        """
        prompt_parts = [
            f"# Document to Audit: {context.document_name}",
            "",
            "## Document Content",
            "```markdown",
            context.document_content,
            "```",
        ]
        
        # Add schema context if available
        if context.defined_terms:
            prompt_parts.extend([
                "",
                "## Available Defined Terms (from defined_terms.md)",
                "```markdown",
                context.defined_terms[:4000],  # Truncate if too long
                "```",
            ])
        
        if context.obligations:
            prompt_parts.extend([
                "",
                "## Obligations Registry (from obligations.md)",
                "```markdown",
                context.obligations[:4000],
                "```",
            ])
        
        if context.roles:
            prompt_parts.extend([
                "",
                "## Roles Registry (from roles.md)",
                "```markdown",
                context.roles[:4000],
                "```",
            ])
        
        # Add Knowledge Base context
        kb_context = self.get_knowledge_base_context()
        if kb_context:
            prompt_parts.append(kb_context)
        
        # Add focus areas if specified
        if context.focus_areas:
            prompt_parts.extend([
                "",
                f"## Focus Areas: {', '.join(context.focus_areas)}",
                "",
            ])
        
        prompt_parts.extend([
            "",
            "## Task",
            "Audit this document according to your role. Return a JSON array of findings.",
            "Each finding must have: id, category, severity, title, description, location, evidence, recommendation, confidence.",
            "",
            "**IMPORTANT**: Include [SOURCE:filename] citations for all legal/regulatory claims.",
            "",
            "If no issues found, return an empty array: []",
        ])
        
        return "\n".join(prompt_parts)
    
    def _extract_citations(self, text: str) -> list[str]:
        """Extract [SOURCE:...] citations from text."""
        return SOURCE_CITATION_PATTERN.findall(text)
    
    async def audit(self, context: AuditContext) -> AgentAuditResult:
        """
        Perform audit on the document.
        
        Args:
            context: Audit context with document and schema info
            
        Returns:
            AgentAuditResult with all findings from this auditor
        """
        base_system_prompt = self.get_system_prompt()
        citation_instructions = self.get_citation_instructions()
        system_prompt = base_system_prompt + citation_instructions
        
        user_prompt = self.get_audit_prompt(context)
        
        messages = [
            {"role": "user", "content": user_prompt},
        ]
        
        start_time = datetime.utcnow()
        
        try:
            findings = await self.provider.complete_list(
                agent_config=self.config,
                messages=messages,
                item_model=AuditFinding,
                system_prompt=system_prompt,
            )
            
            # Post-process findings
            for finding in findings:
                # Ensure agent_id is set
                finding.agent_id = self.role.value
                
                # Set default category if not set
                if not finding.category and self.default_categories:
                    finding.category = self.default_categories[0]
                
                # Extract citations from finding text
                all_text = f"{finding.description} {finding.recommendation} {finding.evidence}"
                finding.source_citations = self._extract_citations(all_text)
            
            end_time = datetime.utcnow()
            execution_ms = int((end_time - start_time).total_seconds() * 1000)
            
            return AgentAuditResult(
                agent_id=str(uuid.uuid4())[:8],
                agent_role=self.role.value,
                document_path=context.document_path,
                findings=findings,
                model_used=self.config.get_full_model_id(),
                execution_time_ms=execution_ms,
                timestamp=start_time,
                success=True,
            )
            
        except ProviderError as e:
            # Return error result
            end_time = datetime.utcnow()
            execution_ms = int((end_time - start_time).total_seconds() * 1000)
            
            return AgentAuditResult(
                agent_id=str(uuid.uuid4())[:8],
                agent_role=self.role.value,
                document_path=context.document_path,
                findings=[],
                model_used=self.config.get_full_model_id(),
                execution_time_ms=execution_ms,
                timestamp=start_time,
                success=False,
                error=str(e),
            )
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(role={self.role.value})"


class LegalAuditor(BaseAuditor):
    """
    Legal auditor for contract structure and jurisdictional compliance.
    Domain-agnostic: Works for any legal document corpus.
    """
    
    role = AgentRole.LEGAL_AUDITOR
    default_categories = [AuditCategory.LEGAL_STRUCTURE, AuditCategory.CONTRACT_TERMS]
    knowledge_topics = ["llc", "corporation", "contract", "liability", "statute", "law"]
    
    def get_system_prompt(self) -> str:
        return """You are an expert legal auditor specializing in contract structure and jurisdictional compliance.

Your responsibilities:
1. Verify contract structure follows proper legal formatting
2. Check cross-references between documents are valid
3. Validate jurisdictional law compliance (state formation, governing law)
4. Review defined terms are used consistently
5. Identify ambiguous or contradictory provisions
6. Verify all required sections are present

For each issue found, return a finding with:
- id: Unique identifier like "LEGAL-001"
- category: One of legal_structure, cross_reference, montana_llc_law, contract_terms, liability
- severity: critical, high, medium, low, or info
- title: Short one-line title
- description: Detailed explanation WITH [SOURCE:] citations
- location: Section or marker where found
- evidence: Quote from the document
- recommendation: Recommended fix WITH [SOURCE:] citations
- confidence: 0.0-1.0 (lower if no KB source available)

**CRITICAL**: Use [SOURCE:filename] for all legal claims. Do NOT invent statutes."""
    
    def get_audit_prompt(self, context: AuditContext) -> str:
        base_prompt = super().get_audit_prompt(context)
        
        legal_additions = """

## Legal Focus Areas
- Jurisdictional law compliance (check KB for applicable statutes)
- Entity formation requirements (verify against KB sources)
- Operating agreement required provisions
- Officer authority and limitations
- Member voting rights consistency
- Indemnification provisions validity
- Amendment procedure adequacy
- Dissolution provisions clarity

**REMEMBER**: Only cite laws that are in the Knowledge Base. If a requirement isn't there, say so.
"""
        
        return base_prompt + legal_additions


class ComplianceAuditor(BaseAuditor):
    """
    Compliance auditor for regulatory requirements.
    Domain-agnostic: Works for BSA/AML, HIPAA, SOX, or any regulatory framework.
    """
    
    role = AgentRole.COMPLIANCE_AUDITOR
    default_categories = [AuditCategory.BSA_AML, AuditCategory.FINCEN]
    knowledge_topics = ["bsa", "aml", "fincen", "msb", "compliance", "regulatory", "sar", "ctr", "cfr"]
    
    def get_system_prompt(self) -> str:
        return """You are an expert compliance auditor specializing in regulatory requirements.

Your responsibilities:
1. Verify compliance program elements are complete
2. Check regulatory registration references
3. Validate identification and verification procedures
4. Review suspicious activity reporting procedures
5. Check record retention requirements
6. Verify licensing compliance
7. Review sanctions screening references

For each issue found, return a finding with:
- id: Unique identifier like "COMP-001"
- category: One of bsa_aml, fincen, msb_requirements, record_keeping, sanctions
- severity: critical, high, medium, low, or info
- title: Short one-line title
- description: Detailed explanation WITH [SOURCE:filename] citations
- location: Section or marker where found
- evidence: Quote from the document
- recommendation: Recommended fix WITH [SOURCE:filename] and regulation cite
- confidence: 0.0-1.0 (lower if no KB source)

**CRITICAL**: Only cite regulations in the Knowledge Base. Do NOT hallucinate requirements.
Example valid: [SOURCE:31_cfr_1022.380_msb_registration.txt]
Example INVALID: "MCA Title 32 requires..." (if not in KB)"""
    
    def get_audit_prompt(self, context: AuditContext) -> str:
        base_prompt = super().get_audit_prompt(context)
        
        compliance_additions = """

## Compliance Focus Areas
- Verify program elements against KB sources
- Registration requirements (cite specific KB files)
- State licensing (ONLY if documented in KB)
- Identification requirements (cite CFR if in KB)
- Reporting thresholds and procedures
- Sanctions screening requirements
- Record retention periods
- Compliance officer designation
- Training program requirements

**WARNING**: Do NOT claim a state requires a license unless the KB confirms it.
Many states do NOT require money transmitter licenses. Check the KB first.
"""
        
        return base_prompt + compliance_additions


class TechnicalAuditor(BaseAuditor):
    """
    Technical auditor for marker syntax and schema conformance.
    Domain-agnostic: Works for any document schema system.
    """
    
    role = AgentRole.TECHNICAL_AUDITOR
    default_categories = [AuditCategory.MARKER_SYNTAX, AuditCategory.SCHEMA_CONFORMANCE]
    knowledge_topics = ["schema", "marker", "validation", "format"]
    
    def get_system_prompt(self) -> str:
        return """You are a technical auditor for document marker syntax and schema validation.

Your responsibilities:
1. Verify all [MARKER:reference] syntax is correct
2. Check marker references resolve to valid targets
3. Validate document follows required structure
4. Identify orphaned or broken cross-references
5. Check markdown formatting consistency
6. Verify required sections are present
7. Find placeholder text that needs completion

Marker types to validate:
- [TERM:term_id] - Defined term references
- [DOC:doc_code] - Document cross-references
- [OBL:obligation_id] - Obligation references
- [FLOW:flow_id] - Flow/process references
- [DECISION:decision_id] - Decision right references
- [RIGHT:right_id] - Rights references
- [ROLE:role.field] - Role field references
- [PERSON:person.field] - Person field references
- [SOURCE:filename] - Knowledge base citations

For each issue found, return a finding with:
- id: Unique identifier like "TECH-001"
- category: One of marker_syntax, schema_conformance, placeholder, formatting
- severity: critical for broken refs, medium for syntax issues, low for formatting
- title: Short one-line title
- description: Clear explanation
- location: Section or line where found
- evidence: The problematic text
- recommendation: Corrected marker syntax or fix
- confidence: 0.0-1.0

Focus on structural and syntactical correctness. No citations needed for syntax issues."""
    
    def get_audit_prompt(self, context: AuditContext) -> str:
        base_prompt = super().get_audit_prompt(context)
        
        technical_additions = """

## Technical Focus Areas
- Marker syntax: [TYPE:reference] or [TYPE:reference.field]
- Valid marker types: TERM, DOC, OBL, FLOW, DECISION, RIGHT, ROLE, PERSON, CONFIG, SOURCE
- Cross-reference targets exist in schema files
- Document code format: Letter+Number (e.g., B1, A2, N3)
- Required metadata sections at document start
- Consistent markdown heading hierarchy
- Table formatting consistency
- Placeholder text like [________________] or TBD
"""
        
        return base_prompt + technical_additions


class FinancialAuditor(BaseAuditor):
    """
    Financial auditor for capital, insurance, and fee provisions.
    Domain-agnostic: Works for any business entity documents.
    """
    
    role = AgentRole.FINANCIAL_AUDITOR
    default_categories = [AuditCategory.CAPITAL_REQUIREMENTS, AuditCategory.INSURANCE]
    knowledge_topics = ["capital", "insurance", "fee", "financial", "surety", "bond"]
    
    def get_system_prompt(self) -> str:
        return """You are a financial auditor specializing in capital requirements, insurance provisions, and fee structures.

Your responsibilities:
1. Verify capital contribution requirements are clear
2. Check insurance requirements are adequate
3. Review fee structures for consistency
4. Validate profit/loss allocation formulas
5. Check distribution provisions
6. Review financial reporting requirements

For each issue found, return a finding with:
- id: Unique identifier like "FIN-001"
- category: One of capital_requirements, insurance, fee_structure, financial_reporting
- severity: critical, high, medium, low, or info
- title: Short one-line title
- description: Clear explanation WITH [SOURCE:] if citing requirements
- location: Section where found
- evidence: Quote from the document
- recommendation: Recommended correction WITH [SOURCE:] if citing requirements
- confidence: 0.0-1.0 (lower if no KB source for requirement)

Be thorough about capital adequacy and insurance gaps. Cite KB sources for requirements."""


class DataPrivacyAuditor(BaseAuditor):
    """
    Data privacy auditor for GDPR, CCPA, and data handling provisions.
    Domain-agnostic: Works for any privacy regulation framework.
    """
    
    role = AgentRole.DATA_PRIVACY_AUDITOR
    default_categories = [AuditCategory.DATA_HANDLING, AuditCategory.CONSENT]
    knowledge_topics = ["privacy", "gdpr", "ccpa", "glba", "data", "consent", "pii"]
    
    def get_system_prompt(self) -> str:
        return """You are a data privacy auditor specializing in privacy regulations and data protection requirements.

Your responsibilities:
1. Verify data collection disclosures
2. Check data retention policies
3. Review consent mechanisms
4. Validate data subject rights provisions
5. Check cross-border transfer provisions
6. Review data processing agreements
7. Verify security requirements

For each issue found, return a finding with:
- id: Unique identifier like "PRIV-001"
- category: One of gdpr, ccpa, data_handling, consent
- severity: critical, high, medium, low, or info
- title: Short one-line title
- description: Clear explanation WITH [SOURCE:filename] citations
- location: Section where found
- evidence: Quote from the document
- recommendation: Recommended correction WITH [SOURCE:filename] and regulation cite
- confidence: 0.0-1.0 (lower if no KB source)

Be strict about consent and data subject rights. Cite KB sources for requirements."""


class OperationalAuditor(BaseAuditor):
    """
    Operational auditor for governance, succession, and procedures.
    Domain-agnostic: Works for any organizational documents.
    """
    
    role = AgentRole.OPERATIONAL_AUDITOR
    default_categories = [AuditCategory.GOVERNANCE, AuditCategory.OFFICER_DUTIES]
    knowledge_topics = ["governance", "officer", "succession", "operations", "procedure"]
    
    def get_system_prompt(self) -> str:
        return """You are an operational auditor specializing in governance, succession planning, and operational procedures.

Your responsibilities:
1. Verify officer duties are clearly defined
2. Check succession procedures are adequate
3. Review voting and decision procedures
4. Validate entity separation provisions
5. Check meeting and notice requirements
6. Review amendment procedures
7. Verify record-keeping requirements

For each issue found, return a finding with:
- id: Unique identifier like "OPS-001"
- category: One of officer_duties, series_separation, governance, succession
- severity: critical, high, medium, low, or info
- title: Short one-line title
- description: Clear explanation (cite [SOURCE:] for legal requirements)
- location: Section where found
- evidence: Quote from the document
- recommendation: Recommended correction (cite [SOURCE:] for legal requirements)
- confidence: 0.0-1.0 (lower if no KB source for legal claims)

Focus on operational clarity and completeness."""


# Registry of all auditor classes
AUDITOR_CLASSES: dict[AgentRole, type[BaseAuditor]] = {
    AgentRole.LEGAL_AUDITOR: LegalAuditor,
    AgentRole.COMPLIANCE_AUDITOR: ComplianceAuditor,
    AgentRole.TECHNICAL_AUDITOR: TechnicalAuditor,
    AgentRole.FINANCIAL_AUDITOR: FinancialAuditor,
    AgentRole.DATA_PRIVACY_AUDITOR: DataPrivacyAuditor,
    AgentRole.OPERATIONAL_AUDITOR: OperationalAuditor,
}


def create_auditor(
    role: AgentRole,
    config: AgentConfig,
    provider: LLMProvider,
    knowledge_base: Optional[Any] = None,
) -> BaseAuditor:
    """
    Factory function to create an auditor by role.
    
    Args:
        role: Agent role
        config: Agent configuration
        provider: LLM provider
        knowledge_base: Optional loaded KnowledgeBase for grounding
        
    Returns:
        Configured auditor instance
        
    Raises:
        ValueError: If role is not an auditor role
    """
    if role not in AUDITOR_CLASSES:
        raise ValueError(f"No auditor class for role: {role}")
    
    cls = AUDITOR_CLASSES[role]
    return cls(config, provider, knowledge_base)
