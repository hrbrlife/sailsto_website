"""Tests for Pydantic models."""

import pytest
from datetime import datetime

from llm_audit.models.findings import (
    AuditFinding,
    AgentAuditResult,
    AuditReport,
    ConsolidatedReport,
    AuditSeverity,
    AuditCategory,
)
from llm_audit.models.agents import (
    AgentRole,
    AgentConfig,
    AuditContext,
    OrchestratorConfig,
)


class TestAuditSeverity:
    """Tests for AuditSeverity enum."""

    def test_severity_values(self):
        assert AuditSeverity.CRITICAL.value == "critical"
        assert AuditSeverity.HIGH.value == "high"
        assert AuditSeverity.MEDIUM.value == "medium"
        assert AuditSeverity.LOW.value == "low"
        assert AuditSeverity.INFO.value == "info"

    def test_severity_weight(self):
        assert AuditSeverity.CRITICAL.weight == 100
        assert AuditSeverity.HIGH.weight == 50
        assert AuditSeverity.MEDIUM.weight == 20
        assert AuditSeverity.LOW.weight == 5
        assert AuditSeverity.INFO.weight == 1

    def test_severity_emoji(self):
        assert AuditSeverity.CRITICAL.emoji == "🚨"
        assert AuditSeverity.HIGH.emoji == "❌"


class TestAuditCategory:
    """Tests for AuditCategory enum."""

    def test_legal_categories(self):
        assert AuditCategory.LEGAL_STRUCTURE.value == "legal_structure"
        assert AuditCategory.CROSS_REFERENCE.value == "cross_reference"
        assert AuditCategory.CONTRACT_TERMS.value == "contract_terms"

    def test_compliance_categories(self):
        assert AuditCategory.BSA_AML.value == "bsa_aml"
        assert AuditCategory.FINCEN.value == "fincen"
        assert AuditCategory.MSB_REQUIREMENTS.value == "msb_requirements"


class TestAuditFinding:
    """Tests for AuditFinding model."""

    def test_minimal_finding(self):
        finding = AuditFinding(
            id="LEGAL-001",
            category=AuditCategory.CONTRACT_TERMS,
            severity=AuditSeverity.MEDIUM,
            title="Test finding title",
            description="Test finding description",
            location="Section 1.1",
            evidence="Some evidence text",
            recommendation="Fix this issue",
            agent_id="legal_auditor",
            confidence=0.8,
        )
        assert finding.id == "LEGAL-001"
        assert finding.severity == AuditSeverity.MEDIUM
        assert finding.confidence == 0.8
        assert finding.consolidated is False
        assert finding.disputed is False

    def test_to_markdown(self):
        finding = AuditFinding(
            id="TEST-001",
            category=AuditCategory.GOVERNANCE,
            severity=AuditSeverity.HIGH,
            title="Test Finding",
            description="Description here",
            location="Section 1",
            evidence="Evidence here",
            recommendation="Recommendation here",
            agent_id="test_agent",
            confidence=0.85,
        )
        markdown = finding.to_markdown()
        assert "TEST-001" in markdown
        assert "Test Finding" in markdown


class TestAgentAuditResult:
    """Tests for AgentAuditResult model."""

    def test_agent_audit_result(self):
        finding = AuditFinding(
            id="LEGAL-001",
            category=AuditCategory.CONTRACT_TERMS,
            severity=AuditSeverity.LOW,
            title="Minor issue",
            description="Minor issue in contract",
            location="Section 2.0",
            evidence="Issue here",
            recommendation="Fix it",
            agent_id="legal_auditor",
            confidence=0.7,
        )
        result = AgentAuditResult(
            agent_id="legal_auditor_01",
            agent_role="legal_auditor",
            document_path="/path/to/B1.md",
            findings=[finding],
            model_used="openrouter/anthropic/claude-3-haiku",
            tokens_used=1500,
        )
        assert result.agent_role == "legal_auditor"
        assert len(result.findings) == 1
        assert result.finding_count == 1


class TestConsolidatedReport:
    """Tests for ConsolidatedReport model."""

    def test_consolidated_report_passed(self):
        report = ConsolidatedReport(
            document_path="/path/to/B1.md",
            document_name="B1.md",
            document_code="B1",
            findings=[],
            overall_status="pass",
            summary="No issues found",
        )
        assert report.overall_status == "pass"
        assert len(report.findings) == 0


class TestAgentRole:
    """Tests for AgentRole enum."""

    def test_auditor_roles(self):
        assert AgentRole.LEGAL_AUDITOR.is_auditor is True
        assert AgentRole.COMPLIANCE_AUDITOR.is_auditor is True

    def test_pipeline_roles(self):
        assert AgentRole.CONSOLIDATOR.is_auditor is False
        assert AgentRole.SKEPTIC.is_auditor is False


class TestAgentConfig:
    """Tests for AgentConfig model."""

    def test_default_config(self):
        config = AgentConfig(role=AgentRole.LEGAL_AUDITOR)
        assert config.role == AgentRole.LEGAL_AUDITOR
        assert config.provider == "openrouter"
        assert config.enabled is True


class TestOrchestratorConfig:
    """Tests for OrchestratorConfig model."""

    def test_default_config(self):
        config = OrchestratorConfig()
        assert config.parallel_auditors is True
        assert config.enable_skeptic is True

    def test_get_enabled_auditors(self):
        config = OrchestratorConfig()
        auditors = config.get_enabled_auditors()
        assert len(auditors) == 6
        for auditor in auditors:
            assert auditor.role.is_auditor is True
