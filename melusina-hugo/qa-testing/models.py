"""
Pydantic models for all agent outputs.
Every expert agent returns a typed, validated structure.
"""

from __future__ import annotations
import json
from pydantic import BaseModel, Field, model_validator


# ── Shared primitives ────────────────────────────────────────────────────────

class Issue(BaseModel):
    """A single finding from any expert agent."""
    severity: str = Field(description="critical | warning | suggestion | praise")
    page: str = Field(description="Page path where the issue was found, e.g. /en")
    viewport: str = Field(default="both", description="desktop | mobile | both")
    title: str = Field(description="Short issue title, max 10 words")
    description: str = Field(description="Concrete description of the problem")
    recommendation: str = Field(description="Specific fix recommendation")
    screenshot_ref: str = Field(default="", description="Screenshot filename if relevant")
    evidence: str = Field(default="", description="Quote or data supporting the finding")


class ExpertReport(BaseModel):
    """Base report returned by every expert agent."""
    expert_name: str
    expert_role: str
    summary: str = Field(description="2-3 sentence executive summary of findings")
    overall_score: int = Field(ge=1, le=10, description="Overall score 1-10")
    issues: list[Issue] = Field(default_factory=list)
    top_priorities: list[str] = Field(description="Top 3 things to fix, in order")


# ── Specialist report extensions ─────────────────────────────────────────────

class LegalReport(ExpertReport):
    """Legal compliance expert findings."""
    missing_policies: list[str] = Field(default_factory=list, description="Required legal pages missing")
    gdpr_issues: list[str] = Field(default_factory=list)
    cookie_compliance: str = Field(default="", description="Cookie consent status")
    terms_quality: str = Field(default="", description="Assessment of terms/privacy if present")


class ConsistencyReport(ExpertReport):
    """Brand & messaging consistency findings."""
    terminology_conflicts: list[dict] = Field(default_factory=list, description="Terms used inconsistently")
    tone_shifts: list[dict] = Field(default_factory=list, description="Pages where tone changes")
    messaging_gaps: list[str] = Field(default_factory=list, description="Key messages missing from pages")
    repeated_content: list[dict] = Field(default_factory=list, description="Content repeated across pages")


class EditorialReport(ExpertReport):
    """Copy quality and Made to Stick findings."""
    jargon_instances: list[dict] = Field(default_factory=list, description="Jargon found with location")
    ai_sounding_phrases: list[str] = Field(default_factory=list, description="Phrases that sound AI-generated")
    missing_aha_moments: list[str] = Field(default_factory=list, description="Pages without a clear aha moment")
    word_count_by_page: dict[str, int] = Field(default_factory=dict)
    readability_notes: list[str] = Field(default_factory=list)


class PrinciplesReport(ExpertReport):
    """Alignment with REVIEW-PROMPT.md principles and brand identity."""
    dinner_test_failures: list = Field(default_factory=list, description="Sentences that fail the dinner test")
    missing_principles: list[str] = Field(default_factory=list, description="Core principles not reflected")
    audience_alignment: dict[str, str] = Field(default_factory=dict, description="Per-page audience targeting assessment")


class MobileUXReport(ExpertReport):
    """Mobile UX expert findings."""
    touch_target_issues: list[dict] = Field(default_factory=list)
    scroll_depth_concerns: list[str] = Field(default_factory=list)
    text_readability: list[dict] = Field(default_factory=list, description="Text too small or cramped")
    layout_breaks: list[dict] = Field(default_factory=list, description="Layout issues at mobile width")


class DesktopUXReport(ExpertReport):
    """Desktop UX expert findings."""
    visual_hierarchy: list[dict] = Field(default_factory=list, description="Hierarchy issues per page")
    whitespace_issues: list[str] = Field(default_factory=list)
    navigation_flow: list[dict] = Field(default_factory=list)
    cta_visibility: list[dict] = Field(default_factory=list)
    five_second_test: dict = Field(default_factory=dict, description="Per-page 5-second test result")


class SEOReport(ExpertReport):
    """SEO and meta tag quality findings."""
    missing_meta: list[dict] = Field(default_factory=list, description="Pages with missing/poor meta tags")
    heading_hierarchy: list[dict] = Field(default_factory=list, description="H1/H2 structure issues")
    canonical_issues: list[str] = Field(default_factory=list)
    open_graph_issues: list[dict] = Field(default_factory=list)
    performance_notes: list[dict] = Field(default_factory=list, description="Load time concerns")


class QCImprovementReport(ExpertReport):
    """QC Improvement Advisor findings — suggests improvements to automated QC tests."""
    proposed_checks: list[dict] = Field(default_factory=list, description="New checks to add [{name, pattern, implementation, priority}]")
    coverage_gaps: list[str] = Field(default_factory=list, description="Categories the current QC misses entirely")
    false_positive_patterns: list[str] = Field(default_factory=list, description="Current QC checks that produce false positives")
    automation_ready: list[dict] = Field(default_factory=list, description="Issues AI experts found that code could catch [{issue, regex_or_logic}]")


class PersonaJourney(BaseModel):
    """Assessment of a single persona's journey through the site."""
    persona: str = Field(description="Persona name, e.g. 'Trust Companies', 'Issuers'")
    journey_score: int = Field(ge=1, le=10, description="How complete/effective is this persona's journey")
    flow_path: list[str] = Field(default_factory=list, description="Pages in the persona's expected flow")
    what_works: list[str] = Field(default_factory=list, description="What's effective for this persona")
    what_breaks: list[str] = Field(default_factory=list, description="Where the journey fails or has friction")
    missing_elements: list[str] = Field(default_factory=list, description="What's missing for this persona")

    @model_validator(mode="before")
    @classmethod
    def _split_comma_strings(cls, data: dict) -> dict:
        """LLMs sometimes return list[str] fields as comma-separated strings."""
        if not isinstance(data, dict):
            return data
        for field in ("flow_path", "what_works", "what_breaks", "missing_elements"):
            val = data.get(field)
            if isinstance(val, str):
                data[field] = [s.strip() for s in val.split(",") if s.strip()]
        return data


class ConversionReport(ExpertReport):
    """Conversion & online marketing specialist findings."""
    persona_journeys: list[PersonaJourney] = Field(default_factory=list, description="Per-persona journey assessments")
    dead_ends: list = Field(default_factory=list, description="Pages with no clear next action")
    cta_issues: list = Field(default_factory=list, description="CTA problems: missing, weak, competing")
    cross_site_gaps: list = Field(default_factory=list, description="Missing cross-links to sails.to or related sites")
    funnel_leaks: list = Field(default_factory=list, description="Points where users likely drop out of the funnel")
    trust_signal_gaps: list[str] = Field(default_factory=list, description="Missing social proof, credibility signals")


# ── Council synthesis ─────────────────────────────────────────────────────────

class CouncilDecision(BaseModel):
    """A decision made by the council after reviewing all expert reports."""
    category: str = Field(description="legal | ux | editorial | seo | consistency | principles | conversion")
    decision: str = Field(description="What to do")
    rationale: str = Field(description="Why, referencing which expert(s) raised it")
    priority: str = Field(description="P0 (now) | P1 (this sprint) | P2 (backlog)")
    assigned_to: str = Field(default="content", description="content | design | dev | legal")
    related_issues: list[str] = Field(default_factory=list, description="Issue titles from expert reports")


class CouncilReport(BaseModel):
    """The unified council report synthesizing all expert findings."""
    site_name: str
    run_date: str
    executive_summary: str = Field(description="3-5 sentence overall assessment")
    overall_grade: str = Field(description="A/B/C/D/F overall site grade")
    expert_scores: dict[str, int] = Field(description="Score from each expert")
    critical_issues_count: int
    warning_count: int
    suggestion_count: int
    praise_count: int
    decisions: list[CouncilDecision] = Field(description="Prioritized action items")
    cross_cutting_themes: list[str] = Field(description="Issues raised by multiple experts")
    strengths: list[str] = Field(description="Things the site does well")
    quick_wins: list[str] = Field(description="Easy fixes with high impact")
    expert_reports: list[ExpertReport] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _parse_stringified_fields(cls, data: dict) -> dict:
        """LLMs sometimes return list/dict fields as JSON strings — parse them."""
        if not isinstance(data, dict):
            return data
        list_fields = ["decisions", "cross_cutting_themes", "strengths", "quick_wins"]
        for field in list_fields:
            val = data.get(field)
            if isinstance(val, str):
                try:
                    data[field] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    pass
        dict_fields = ["expert_scores"]
        for field in dict_fields:
            val = data.get(field)
            if isinstance(val, str):
                try:
                    data[field] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    pass
        return data


# ── Per-page consilium ───────────────────────────────────────────────────────

class PageConsilium(BaseModel):
    """Council synthesis for a single page — all experts' views unified.

    Produced by the per-page council agent after reading 8 expert reports.
    The page_url and expert_reports fields are attached programmatically.
    """
    page_path: str = Field(description="Page being evaluated, e.g. /otc-desk/")
    page_title: str = Field(default="", description="Page title from front matter or meta")
    executive_summary: str = Field(description="2-3 sentence assessment of this specific page")
    overall_score: int = Field(ge=1, le=10, description="Composite page quality score 1-10")
    expert_scores: dict[str, int] = Field(default_factory=dict, description="expert_role → score for this page")
    critical_count: int = Field(default=0)
    warning_count: int = Field(default=0)
    top_issues: list[Issue] = Field(default_factory=list, description="Top 5-8 issues merged and prioritized across all experts")
    strengths: list[str] = Field(default_factory=list, description="What this page does well")
    top_recommendations: list[str] = Field(default_factory=list, description="Top 3-5 fixes in priority order")

    # Attached programmatically (not from LLM)
    page_url: str = Field(default="")
    expert_reports: list[ExpertReport] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _parse_stringified(cls, data: dict) -> dict:
        if not isinstance(data, dict):
            return data
        for field in ("top_issues", "strengths", "top_recommendations"):
            val = data.get(field)
            if isinstance(val, str):
                try:
                    data[field] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    if field != "top_issues" and "," in val:
                        data[field] = [s.strip() for s in val.split(",") if s.strip()]
        if isinstance(data.get("expert_scores"), str):
            try:
                data["expert_scores"] = json.loads(data["expert_scores"])
            except (json.JSONDecodeError, TypeError):
                pass
        return data

    def format_for_mega_prompt(self, max_issues: int = 5) -> str:
        """Format this consilium for the mega council prompt."""
        issues_text = "\n".join(
            f"  [{i.severity}] {i.title}: {i.description}"
            for i in self.top_issues[:max_issues]
        )
        recs_text = "\n".join(
            f"  {idx+1}. {r}" for idx, r in enumerate(self.top_recommendations[:5])
        )
        return (
            f"## Page: {self.page_path} — Score: {self.overall_score}/10\n"
            f"Title: {self.page_title}\n"
            f"{self.executive_summary}\n"
            f"Expert scores: {self.expert_scores}\n"
            f"Critical: {self.critical_count}, Warnings: {self.warning_count}\n"
            f"Strengths: {', '.join(self.strengths[:5])}\n"
            f"Top issues:\n{issues_text}\n"
            f"Recommendations:\n{recs_text}\n"
        )


class MegaConsilium(BaseModel):
    """Final site-wide consilium synthesizing all per-page reports.

    Produced by the mega council agent after reading all PageConsiliums.
    The page_consiliums list is attached programmatically.
    """
    site_name: str
    run_date: str
    executive_summary: str = Field(description="3-5 sentence site-wide assessment")
    overall_grade: str = Field(description="A/B/C/D/F overall site grade")
    average_score: float = Field(description="Mean score across all pages")
    page_count: int
    total_critical: int = Field(default=0)
    total_warnings: int = Field(default=0)
    worst_pages: list[dict] = Field(default_factory=list, description="3-5 worst pages [{page_path, score, reason}]")
    best_pages: list[dict] = Field(default_factory=list, description="3-5 best pages [{page_path, score, reason}]")
    cross_cutting_themes: list[str] = Field(default_factory=list)
    site_wide_strengths: list[str] = Field(default_factory=list)
    prioritized_decisions: list[CouncilDecision] = Field(default_factory=list, description="Site-wide action items")
    quick_wins: list[str] = Field(default_factory=list)
    expert_dimension_summary: dict[str, str] = Field(default_factory=dict, description="Per-expert-role summary across all pages")

    # Attached programmatically
    page_consiliums: list[PageConsilium] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _parse_stringified(cls, data: dict) -> dict:
        if not isinstance(data, dict):
            return data
        for field in ("worst_pages", "best_pages", "cross_cutting_themes",
                      "site_wide_strengths", "prioritized_decisions", "quick_wins"):
            val = data.get(field)
            if isinstance(val, str):
                try:
                    data[field] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    if field in ("cross_cutting_themes", "site_wide_strengths", "quick_wins") and "," in str(val):
                        data[field] = [s.strip() for s in val.split(",") if s.strip()]
        if isinstance(data.get("expert_dimension_summary"), str):
            try:
                data["expert_dimension_summary"] = json.loads(data["expert_dimension_summary"])
            except (json.JSONDecodeError, TypeError):
                pass
        return data
