"""
Pipeline agents for consolidation, review, and quality control.

These agents run after the parallel auditors to merge,
challenge, and approve findings.

Now includes:
- Citation verification against knowledge base
- Online search capability for verification
- Domain-agnostic prompting
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from llm_audit.models.agents import AgentConfig, AgentRole, AuditContext
from llm_audit.models.findings import (
    AgentAuditResult,
    AuditFinding,
    AuditReport,
    ConsolidatedReport,
    AuditSeverity,
)
from llm_audit.providers import LLMProvider, ProviderError

import json


class ConsolidatorAgent:
    """
    Consolidates findings from multiple auditors.
    
    Responsibilities:
    - Merge duplicate findings
    - Resolve conflicts between auditors
    - Normalize severity ratings
    - Group related findings
    - Flag findings with missing citations
    """
    
    role = AgentRole.CONSOLIDATOR
    
    def __init__(
        self,
        config: AgentConfig,
        provider: LLMProvider,
        knowledge_base: Optional[Any] = None,
    ):
        self.config = config
        self.provider = provider
        self.knowledge_base = knowledge_base
    
    def get_system_prompt(self) -> str:
        return """You are a consolidation agent responsible for merging audit findings from multiple specialist auditors.

Your responsibilities:
1. Identify and merge duplicate findings (same issue, different wording)
2. Resolve conflicting severity ratings (take the higher severity if justified)
3. Remove false positives that appear when comparing across auditors
4. Group related findings that address the same root cause
5. Normalize descriptions for consistency
6. Preserve the most specific and actionable version of each finding
7. FLAG findings that make legal claims without [SOURCE:] citations

Rules:
- Never discard a CRITICAL finding
- Prefer findings with higher confidence scores AND valid citations
- Keep the most specific evidence and suggested_fix
- Maintain traceability to original auditor
- DOWNGRADE confidence for findings with uncited legal claims

Output: A consolidated JSON array of AuditFinding objects."""
    
    async def consolidate(
        self,
        agent_results: list[AgentAuditResult],
        context: AuditContext,
    ) -> list[AuditFinding]:
        """
        Consolidate findings from multiple auditors.
        
        Args:
            agent_results: Results from each auditor
            context: Audit context
            
        Returns:
            Consolidated list of findings
        """
        if not agent_results:
            return []
        
        # Flatten all findings for the prompt
        all_findings = []
        for ar in agent_results:
            for finding in ar.findings:
                all_findings.append({
                    "auditor": ar.agent_role,
                    "finding": finding.model_dump(exclude_none=True),
                })
        
        if not all_findings:
            return []
        
        prompt = f"""# Consolidation Task

Document: {context.document_name}

## Raw Findings from Auditors
```json
{json.dumps(all_findings, indent=2)}
```

## Instructions
1. Review all findings from the different auditors
2. Merge duplicates (same issue reported by multiple auditors)
3. Resolve any conflicting severity ratings
4. Remove likely false positives
5. Keep the best version of each unique finding
6. FLAG any findings that cite laws/regulations without [SOURCE:] markers

Return a JSON array of consolidated AuditFinding objects.
If all findings are false positives, return: []"""

        messages = [{"role": "user", "content": prompt}]
        
        try:
            consolidated = await self.provider.complete_list(
                agent_config=self.config,
                messages=messages,
                item_model=AuditFinding,
                system_prompt=self.get_system_prompt(),
            )
            return consolidated
        except ProviderError:
            # Fallback: return all findings without deduplication
            return [f for ar in agent_results for f in ar.findings]


class SkepticAgent:
    """
    Challenges consolidated findings to reduce false positives.
    
    Enhanced with:
    - Citation verification against knowledge base
    - Hallucination detection for legal claims
    - Online search for verification (when enabled)
    
    Responsibilities:
    - Question the validity of each finding
    - VERIFY [SOURCE:] citations exist in KB
    - REJECT findings citing non-existent sources
    - Challenge severity ratings
    - Identify missing findings
    """
    
    role = AgentRole.SKEPTIC
    
    def __init__(
        self,
        config: AgentConfig,
        provider: LLMProvider,
        knowledge_base: Optional[Any] = None,
        online_verifier_config: Optional[AgentConfig] = None,
    ):
        self.config = config
        self.provider = provider
        self.knowledge_base = knowledge_base
        self.online_config = online_verifier_config
        self._online_verifier = None  # Lazy-loaded
    
    def get_system_prompt(self) -> str:
        return """You are a skeptic agent responsible for challenging audit findings and verifying citations.

Your role is adversarial - your PRIMARY job is to CATCH HALLUCINATIONS:

## CITATION VERIFICATION (CRITICAL)

For EACH finding that makes a legal/regulatory claim, you MUST:

1. CHECK if finding has [SOURCE:filename] citations
2. If NO citation: Mark as "needs_citation", REDUCE confidence by 0.3
3. If citation provided: Verify the source file exists in the KB Index provided
4. If source NOT in KB: REJECT the finding as "hallucinated_source"

## COMMON HALLUCINATIONS TO CATCH

- State licensing requirements that don't exist (e.g., "Montana requires MTL")
- Made-up statute citations (e.g., "MCA Title 32, Chapter 9")
- Invented CFR sections not in the KB
- Regulatory requirements without KB backing

## For each finding, determine:

1. VALID: Has correct [SOURCE:] citation that exists in KB
2. NEEDS_CITATION: Makes legal claim but no citation - downgrade confidence
3. HALLUCINATED: Cites source not in KB - REJECT entirely
4. FALSE_POSITIVE: Not a real issue - remove from list

## Output Format

Respond with JSON:
```json
{
  "revised_findings": [...],  // Findings that pass verification
  "rejected_findings": [      // Findings rejected with reasons
    {"id": "...", "reason": "hallucinated_source", "details": "..."}
  ],
  "new_findings": [...]       // Any gaps you identified
}
```

Be AGGRESSIVE about catching hallucinated legal claims."""
    
    def _get_kb_index(self) -> str:
        """Get KB index for the prompt."""
        if self.knowledge_base:
            return self.knowledge_base.get_full_index()
        return "[No knowledge base loaded - cannot verify citations]"
    
    def _verify_citation(self, citation: str) -> tuple[bool, str]:
        """Verify a citation exists in KB."""
        if not self.knowledge_base:
            return True, "KB not loaded - cannot verify"
        
        is_valid, evidence = self.knowledge_base.verify_citation(citation)
        if is_valid:
            return True, f"Source verified: {evidence[:100]}..."
        return False, f"Source NOT FOUND in KB: {citation}"
    
    def _get_online_verifier(self) -> Optional['OnlineVerifierAgent']:
        """Lazy-load the online verifier if config provided."""
        if self._online_verifier is None and self.online_config:
            self._online_verifier = OnlineVerifierAgent(
                config=self.online_config,
                provider=self.provider,
            )
        return self._online_verifier
    
    async def _verify_finding_online(
        self, 
        finding: 'AuditFinding',
        context: 'AuditContext',
    ) -> dict[str, Any]:
        """
        Verify a finding's claims using online search.
        
        Called when KB verification fails but online fallback is enabled.
        
        Returns:
            Dict with verification result including 'verified', 'confidence', 'sources'
        """
        verifier = self._get_online_verifier()
        if not verifier:
            return {"verified": None, "error": "Online verifier not configured"}
        
        # Build the claim from the finding
        claim = f"{finding.title}: {finding.description}"
        if finding.source_citations:
            claim += f"\nCited sources: {', '.join(finding.source_citations)}"
        
        doc_context = f"Document: {context.document_name}\nCategory: {finding.category}"
        
        return await verifier.verify_claim(claim, doc_context)

    async def challenge(
        self,
        findings: list[AuditFinding],
        context: AuditContext,
    ) -> tuple[list[AuditFinding], list[AuditFinding], list[dict]]:
        """
        Challenge findings and verify citations.
        
        Args:
            findings: Consolidated findings to challenge
            context: Audit context with document
            
        Returns:
            Tuple of (revised_findings, new_findings, rejected_findings)
        """
        if not findings:
            return [], [], []
        
        findings_json = [f.model_dump(exclude_none=True) for f in findings]
        
        # Pre-verify citations
        citation_status = []
        for f in findings:
            finding_citations = f.source_citations or []
            if finding_citations:
                for cit in finding_citations:
                    is_valid, msg = self._verify_citation(cit)
                    citation_status.append({
                        "finding_id": f.id,
                        "citation": cit,
                        "valid": is_valid,
                        "message": msg,
                    })
        
        kb_index = self._get_kb_index()
        
        prompt = f"""# Skeptic Review Task - CITATION VERIFICATION REQUIRED

Document: {context.document_name}

## Knowledge Base Index (AUTHORITATIVE SOURCE LIST)
{kb_index}

## Pre-Verification Results
```json
{json.dumps(citation_status, indent=2)}
```

## Document Content (excerpt)
```markdown
{context.document_content[:6000]}
```

## Findings to Challenge
```json
{json.dumps(findings_json, indent=2)}
```

## Instructions - BE AGGRESSIVE ABOUT HALLUCINATIONS

1. For EACH finding, check:
   - Does it make legal/regulatory claims?
   - Does it have [SOURCE:filename] citations?
   - Are those sources in the KB Index above?

2. REJECT findings that:
   - Cite sources NOT in the KB Index (HALLUCINATION)
   - Make legal claims without any [SOURCE:] citation (UNVERIFIED)
   - Cite non-existent laws/statutes (e.g., invented MCA sections)

3. KEEP findings that:
   - Have valid [SOURCE:] citations to files in the KB Index
   - Are purely technical/formatting issues (don't need legal citations)
   - Have appropriately low confidence for unverified claims

4. Adjust confidence:
   - 0.9+ : Fully cited and verified
   - 0.6-0.8: Partially verified
   - <0.5: Unverified claim (should be rare)

Respond with JSON:
```json
{{
  "revised_findings": [...],
  "rejected_findings": [{{"id": "...", "reason": "...", "details": "..."}}],
  "new_findings": [...]
}}
```"""

        messages = [{"role": "user", "content": prompt}]
        
        try:
            response = await self.provider.complete(
                agent_config=self.config,
                messages=messages,
                system_prompt=self.get_system_prompt(),
            )
            
            # Parse the response
            cleaned = response.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                start_idx = 1
                end_idx = len(lines)
                for i, line in enumerate(lines):
                    if line.startswith("```") and i > 0:
                        end_idx = i
                        break
                cleaned = "\n".join(lines[start_idx:end_idx])
            
            data = json.loads(cleaned)
            
            revised = [
                AuditFinding.model_validate(f) 
                for f in data.get("revised_findings", [])
            ]
            new = [
                AuditFinding.model_validate(f) 
                for f in data.get("new_findings", [])
            ]
            rejected = data.get("rejected_findings", [])
            
            # Online verification fallback for hallucination-rejected findings
            if self.online_config and rejected:
                rescued_findings = []
                final_rejected = []
                
                # Map findings by ID for lookup
                findings_by_id = {f.id: f for f in findings}
                
                for rej in rejected:
                    # Only attempt online rescue for hallucinated_source rejections
                    if rej.get("reason") == "hallucinated_source":
                        finding_id = rej.get("id")
                        original_finding = findings_by_id.get(finding_id)
                        
                        if original_finding:
                            print(f"    [Online] Verifying rejected finding {finding_id}...")
                            online_result = await self._verify_finding_online(
                                original_finding, context
                            )
                            
                            if online_result.get("verified") is True:
                                # Rescue the finding - it was verified online
                                original_finding.confidence = min(
                                    original_finding.confidence or 0.7,
                                    online_result.get("confidence", 0.7)
                                )
                                original_finding.citation_status = "online_verified"
                                original_finding.citation_warning = (
                                    f"Not in KB but verified online: {online_result.get('explanation', '')[:200]}"
                                )
                                # Add online sources if available
                                online_sources = online_result.get("sources", [])
                                if online_sources:
                                    if not original_finding.source_citations:
                                        original_finding.source_citations = []
                                    original_finding.source_citations.extend(
                                        [f"[ONLINE:{s}]" for s in online_sources[:3]]
                                    )
                                rescued_findings.append(original_finding)
                                print(f"    [Online] ✓ Rescued {finding_id} via online verification")
                            else:
                                # Still rejected - add online verification attempt note
                                rej["online_verified"] = False
                                rej["online_result"] = online_result.get("explanation", "Could not verify")
                                final_rejected.append(rej)
                                print(f"    [Online] ✗ {finding_id} not verified online either")
                        else:
                            final_rejected.append(rej)
                    else:
                        # Non-hallucination rejections pass through
                        final_rejected.append(rej)
                
                # Add rescued findings to revised list
                revised.extend(rescued_findings)
                rejected = final_rejected
            
            return revised, new, rejected
            
        except Exception as e:
            # Fallback: return original findings unchanged
            print(f"Skeptic parsing error: {e}")
            return findings, [], []


class OnlineVerifierAgent:
    """
    Uses online search to verify claims when KB is insufficient.
    
    Configured to use grok-4.1-fast:online or similar model with
    real-time web access.
    """
    
    role = AgentRole.SKEPTIC  # Sub-role of skeptic
    
    def __init__(
        self,
        config: AgentConfig,
        provider: LLMProvider,
    ):
        self.config = config
        self.provider = provider
    
    async def verify_claim(
        self,
        claim: str,
        context: str = "",
    ) -> dict[str, Any]:
        """
        Verify a specific claim using online search.
        
        Args:
            claim: The claim to verify
            context: Additional context
            
        Returns:
            Dict with verification result
        """
        prompt = f"""Verify this claim using current authoritative sources:

CLAIM: {claim}

CONTEXT: {context}

Search for:
1. Official government sources (.gov)
2. Official regulatory body websites
3. Current law/regulation text

Respond with JSON:
{{
  "verified": true/false,
  "confidence": 0.0-1.0,
  "sources": ["list of URLs"],
  "explanation": "Brief explanation",
  "current_as_of": "date checked"
}}

If you cannot verify, say so honestly."""

        try:
            response = await self.provider.complete(
                agent_config=self.config,
                messages=[{"role": "user", "content": prompt}],
                system_prompt="You are a fact-checker with real-time web access. Verify claims against authoritative sources.",
            )
            
            # Parse response
            cleaned = response.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                cleaned = "\n".join(lines[1:-1])
            
            return json.loads(cleaned)
            
        except Exception as e:
            return {
                "verified": None,
                "confidence": 0.0,
                "error": str(e),
            }


class ReviewerAgent:
    """
    Final reviewer that makes pass/fail decisions.
    
    Responsibilities:
    - Make final approval decision
    - Classify overall document status
    - Prioritize findings for remediation
    - Generate executive summary
    """
    
    role = AgentRole.REVIEWER
    
    def __init__(
        self,
        config: AgentConfig,
        provider: LLMProvider,
    ):
        self.config = config
        self.provider = provider
    
    def get_system_prompt(self) -> str:
        return """You are the final reviewer agent responsible for making audit decisions.

Your responsibilities:
1. Review all findings and make a pass/fail/conditional decision
2. Prioritize findings by remediation urgency
3. Generate an executive summary
4. Identify blocking issues vs. recommendations
5. Provide overall confidence assessment

Decision criteria:
- PASS: No CRITICAL or HIGH findings, or all are addressed
- CONDITIONAL: HIGH findings exist but have clear remediation path
- FAIL: CRITICAL findings exist, or systemic issues found

Output a JSON object with:
- decision: "pass", "conditional", or "fail"
- summary: Executive summary (2-3 sentences)
- blocking_findings: Array of finding IDs that block passing
- remediation_priority: Ordered list of finding IDs by urgency
- confidence: 0.0-1.0 confidence in the decision
- notes: Any additional reviewer notes"""
    
    async def review(
        self,
        findings: list[AuditFinding],
        context: AuditContext,
        original_count: int = 0,
        consolidated_count: int = 0,
        disputed_count: int = 0,
        citation_stats: Optional[dict[str, int]] = None,
    ) -> ConsolidatedReport:
        """
        Perform final review and generate consolidated report.
        
        Args:
            findings: Final findings list
            context: Audit context
            original_count: Original finding count before consolidation
            consolidated_count: Count after consolidation
            disputed_count: Count of disputed findings
            citation_stats: Stats on citation validation
            
        Returns:
            Complete ConsolidatedReport with decision
        """
        findings_json = [f.model_dump(exclude_none=True) for f in findings]
        
        # Count findings by severity
        severity_counts = {s.value: 0 for s in AuditSeverity}
        for f in findings:
            sev = f.final_severity or f.severity
            severity_counts[sev.value] += 1
        
        # Citation stats section
        citation_section = ""
        if citation_stats:
            citation_section = f"""
## Citation Verification Stats
- Total citations checked: {citation_stats.get('total', 0)}
- Valid (source in KB): {citation_stats.get('valid', 0)}
- Invalid/Hallucinated: {citation_stats.get('invalid', 0)}
"""
        
        prompt = f"""# Final Review Task

Document: {context.document_name}
Document Code: {context.document_code or 'Unknown'}

## Severity Summary
- CRITICAL: {severity_counts.get('critical', 0)}
- HIGH: {severity_counts.get('high', 0)}
- MEDIUM: {severity_counts.get('medium', 0)}
- LOW: {severity_counts.get('low', 0)}
- Total: {len(findings)}
{citation_section}
## All Findings
```json
{json.dumps(findings_json, indent=2)}
```

## Instructions
1. Review all findings
2. Make a pass/fail/conditional decision
3. Identify which findings block passing
4. Prioritize findings for remediation
5. Write an executive summary
6. Note any findings that may need additional verification (low citations)

Respond with a JSON object:
```json
{{
  "decision": "pass|conditional|fail",
  "summary": "Executive summary...",
  "blocking_issues": ["List of blocking issue descriptions"],
  "remediation_priority": ["FIN-001", "LEGAL-002"],
  "confidence": 0.85,
  "notes": "Additional notes..."
}}
```"""

        messages = [{"role": "user", "content": prompt}]
        
        try:
            response = await self.provider.complete(
                agent_config=self.config,
                messages=messages,
                system_prompt=self.get_system_prompt(),
            )
            
            # Parse response
            cleaned = response.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                start_idx = 1
                end_idx = len(lines)
                for i, line in enumerate(lines):
                    if line.startswith("```") and i > 0:
                        end_idx = i
                        break
                cleaned = "\n".join(lines[start_idx:end_idx])
            
            review_data = json.loads(cleaned)
            
        except Exception:
            # Fallback decision based on severity counts
            if severity_counts.get("critical", 0) > 0:
                decision = "fail"
                summary = f"Audit failed: {severity_counts.get('critical', 0)} critical findings."
            elif severity_counts.get("high", 0) > 0:
                decision = "needs_review"
                summary = f"Review needed: {severity_counts.get('high', 0)} high-severity findings require attention."
            else:
                decision = "pass"
                summary = f"Audit passed with {len(findings)} minor findings."
            
            review_data = {
                "decision": decision,
                "summary": summary,
                "confidence": 0.5,
                "blocking_issues": [],
            }
        
        return ConsolidatedReport(
            document_path=context.document_path,
            document_name=context.document_name,
            document_code=context.document_code,
            findings=findings,
            summary=review_data.get("summary", ""),
            overall_status=review_data.get("decision", "needs_review"),
            blocking_issues=review_data.get("blocking_issues", []),
            reviewer_decision=review_data.get("notes", ""),
            original_finding_count=original_count,
            deduplicated_count=consolidated_count,
            disputed_count=disputed_count,
            citation_stats=citation_stats,
            timestamp=datetime.utcnow(),
        )


# Pipeline agent registry
PIPELINE_AGENTS = {
    AgentRole.CONSOLIDATOR: ConsolidatorAgent,
    AgentRole.SKEPTIC: SkepticAgent,
    AgentRole.REVIEWER: ReviewerAgent,
}
