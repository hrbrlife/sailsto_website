"""
CLI interface for LLM Audit system.

Provides commands for running audits on documents.
"""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.tree import Tree

from llm_audit.models.agents import OrchestratorConfig
from llm_audit.config import load_config as load_config_file, ConfigError
from llm_audit.models.findings import AuditSeverity
from llm_audit.integrated import IntegratedOrchestrator

app = typer.Typer(
    name="llm-audit",
    help="Multi-agent LLM audit system for CCASH legal documents.",
    no_args_is_help=True,
)
console = Console()


def load_config(config_path: Optional[Path]) -> OrchestratorConfig:
    """Load orchestrator config from file or return defaults."""
    if config_path:
        if not config_path.exists():
            console.print(f"[red]Config file not found: {config_path}[/red]")
            raise typer.Exit(1)
        try:
            return load_config_file(config_path)
        except ConfigError as e:
            console.print(f"[red]Invalid config: {e}[/red]")
            raise typer.Exit(1)
    return OrchestratorConfig()


def find_schema_dir(start_path: Path) -> Optional[Path]:
    """Find _schema directory by walking up from start path."""
    current = start_path.resolve()
    
    # First check if we're inside _schema
    for parent in [current] + list(current.parents):
        if parent.name == "_schema":
            return parent
        schema_path = parent / "_schema"
        if schema_path.is_dir():
            return schema_path
    
    return None


def severity_color(severity: AuditSeverity) -> str:
    """Get Rich color for severity level."""
    return {
        AuditSeverity.CRITICAL: "red bold",
        AuditSeverity.HIGH: "red",
        AuditSeverity.MEDIUM: "yellow",
        AuditSeverity.LOW: "blue",
    }.get(severity, "white")


@app.command()
def audit(
    paths: list[Path] = typer.Argument(
        ...,
        help="Paths to documents to audit (files or directories)",
        exists=True,
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config", "-c",
        help="Path to YAML config file",
    ),
    schema_dir: Optional[Path] = typer.Option(
        None,
        "--schema-dir", "-s",
        help="Path to _schema directory",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output JSON report to file",
    ),
    focus: Optional[str] = typer.Option(
        None,
        "--focus", "-f",
        help="Focus areas (comma-separated)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Verbose output",
    ),
    no_skeptic: bool = typer.Option(
        False,
        "--no-skeptic",
        help="Disable skeptic agent",
    ),
    no_reviewer: bool = typer.Option(
        False,
        "--no-reviewer",
        help="Disable reviewer agent (auto-evaluate)",
    ),
):
    """
    Audit documents using multi-agent LLM pipeline.
    
    Examples:
        llm-audit Company/Governance/B1_Master_Operating_Agreement.md
        llm-audit Company/ --output report.json
        llm-audit *.md --focus "BSA,compliance" --verbose
    """
    # Collect all document paths
    doc_paths: list[Path] = []
    
    for path in paths:
        if path.is_file():
            if path.suffix == ".md":
                doc_paths.append(path)
        elif path.is_dir():
            doc_paths.extend(path.rglob("*.md"))
    
    if not doc_paths:
        console.print("[red]No markdown documents found.[/red]")
        raise typer.Exit(1)
    
    # Filter out schema files
    doc_paths = [
        p for p in doc_paths 
        if "_schema" not in str(p) and not p.name.startswith(".")
    ]
    
    console.print(f"\n[bold]Found {len(doc_paths)} documents to audit[/bold]\n")
    
    # Find schema directory
    if not schema_dir:
        schema_dir = find_schema_dir(doc_paths[0])
        if schema_dir:
            console.print(f"Using schema directory: {schema_dir}")
    
    # Load config
    orchestrator_config = load_config(config)
    
    # Apply CLI overrides
    if no_skeptic:
        orchestrator_config.enable_skeptic = False
    if no_reviewer:
        orchestrator_config.require_reviewer_approval = False
    
    # Parse focus areas
    focus_areas = [f.strip() for f in focus.split(",")] if focus else None
    
    # Run audit
    async def run_audit():
        orchestrator = AuditOrchestrator(
            config=orchestrator_config,
            schema_dir=schema_dir,
        )
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running audit pipeline...", total=None)
            
            report = await orchestrator.audit_all(doc_paths, focus_areas)
            
            progress.update(task, completed=True)
        
        return report
    
    reports = asyncio.run(run_audit())
    
    # Aggregate summary
    documents_audited = len(reports)
    total_findings = sum(len(r.findings) for r in reports)
    passed = all(r.is_passing for r in reports)
    
    # Severity breakdown (using final findings)
    severity_counts: dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for r in reports:
        for f in r.findings:
            sev = (f.final_severity or f.severity).value
            if sev in severity_counts:
                severity_counts[sev] += 1
    
    # Display results
    console.print("\n")
    console.print(Panel.fit(
        f"[bold]Audit Complete[/bold]\n"
        f"Documents: {documents_audited}\n"
        f"Total Findings: {total_findings}\n"
        f"Status: {'[green]PASSED[/green]' if passed else '[red]FAILED[/red]'}",
        title="Summary",
    ))
    
    # Show severity breakdown
    severity_table = Table(title="Findings by Severity")
    severity_table.add_column("Severity")
    severity_table.add_column("Count", justify="right")
    
    for sev in ["critical", "high", "medium", "low"]:
        count = severity_counts.get(sev, 0)
        style = severity_color(AuditSeverity(sev))
        severity_table.add_row(sev.upper(), str(count), style=style)
    
    console.print(severity_table)
    
    # Show document details
    if verbose or not passed:
        console.print("\n[bold]Document Results:[/bold]\n")
        
        for audit in reports:
            status = "[green]✓[/green]" if audit.is_passing else "[red]✗[/red]"
            console.print(f"{status} {audit.document_name}")
            
            if audit.findings:
                tree = Tree(f"  Findings ({len(audit.findings)})")
                for finding in audit.findings:
                    style = severity_color(finding.severity)
                    tree.add(
                        f"[{style}]{finding.severity.value.upper()}[/{style}]: "
                        f"{finding.description[:80]}..."
                    )
                console.print(tree)
            
            if audit.summary:
                console.print(f"  [dim]{audit.summary}[/dim]")
            console.print()
    
    # Save report if requested
    if output:
        bundle = {
            "generated_at": datetime.utcnow().isoformat(),
            "documents_audited": documents_audited,
            "total_findings": total_findings,
            "passed": passed,
            "severity_counts": severity_counts,
            "audits": [r.model_dump(mode="json") for r in reports],
        }
        # Handle directory vs file
        if output.is_dir():
            output = output / "report.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w") as f:
            json.dump(bundle, f, indent=2, default=str)
        console.print(f"\n[green]Report saved to: {output}[/green]")
    
    # Exit with appropriate code
    if not passed:
        raise typer.Exit(1)


@app.command()
def check(
    path: Path = typer.Argument(
        ...,
        help="Path to a single document to quick-check",
        exists=True,
    ),
    schema_dir: Optional[Path] = typer.Option(
        None,
        "--schema-dir", "-s",
        help="Path to _schema directory",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config", "-c",
        help="Path to config YAML file",
    ),
):
    """
    Quick check a single document (simplified output).
    
    Example:
        llm-audit check B1_Master_Operating_Agreement.md
    """
    if not schema_dir:
        schema_dir = find_schema_dir(path)
    
    # Load config
    orchestrator_config = load_config(config)
    
    console.print(f"\n[bold]Quick audit: {path.name}[/bold]\n")
    
    # Create temp output dir
    import tempfile
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir)
        
        async def run():
            orchestrator = IntegratedOrchestrator(
                docs_dir=path.parent,
                schema_dir=schema_dir,
                output_dir=output_dir,
                config=orchestrator_config,
            )
            # Audit just this one document
            report = await orchestrator._audit_single_document(
                doc_code=path.stem,
                save_intermediates=False,
            )
            return report
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Auditing...", total=None)
            result = asyncio.run(run())
    
    # Simple output
    passed = result.overall_status == "PASS"
    if passed:
        console.print("[green]✓ PASSED[/green]")
    else:
        console.print("[red]✗ FAILED[/red]")
    
    console.print(f"Findings: {len(result.all_findings)}")
    
    if result.all_findings:
        for finding in result.all_findings[:10]:  # Show first 10
            style = severity_color(finding.severity)
            console.print(f"  [{style}]{finding.severity.value.upper()}[/{style}]: {finding.title}")
    
    if not passed:
        raise typer.Exit(1)


@app.command()
def agents():
    """List available audit agents and their descriptions."""
    from llm_audit.models.agents import AgentRole
    
    table = Table(title="Audit Agents")
    table.add_column("Role")
    table.add_column("Type")
    table.add_column("Description")
    table.add_column("Default Model")
    
    for role in AgentRole:
        role_type = "Auditor" if role.is_auditor else "Pipeline"
        table.add_row(
            role.value,
            role_type,
            role.description[:50] + "..." if len(role.description) > 50 else role.description,
            role.default_model,
        )
    
    console.print(table)


@app.command()
def init_config(
    output: Path = typer.Argument(
        Path("llm_audit_config.yaml"),
        help="Output path for config file",
    ),
):
    """Generate a default configuration file."""
    from llm_audit.models.agents import AgentRole
    
    config = {
        "# LLM Audit Configuration": None,
        "parallel_auditors": True,
        "max_parallel": 5,
        "enable_skeptic": True,
        "require_reviewer_approval": True,
        "default_provider": "openrouter",
        
        "providers": {
            "openrouter": {
                "# api_key": "set OPENROUTER_API_KEY env var",
            },
            "openai": {
                "# api_key": "set OPENAI_API_KEY env var",
            },
            "local": {
                "base_url": "http://localhost:8000/v1",
                "# api_key": "not-needed",
            },
        },
        
        "agents": {},
    }
    
    # Add agent configs
    for role in AgentRole:
        config["agents"][role.value] = {
            "enabled": True,
            "model": role.default_model,
            "temperature": 0.1,
            "max_tokens": 4096,
            "timeout_seconds": 120,
        }
    
    import yaml
    
    with open(output, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    console.print(f"[green]Config file created: {output}[/green]")
    console.print("\nEdit the file to customize agent settings and API keys.")


@app.command()
def auto(
    docs_dir: Path = typer.Argument(
        ...,
        help="Root directory containing documents (e.g., '.' or 'Company/')",
        exists=True,
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config", "-c",
        help="Path to YAML config file",
    ),
    schema_dir: Optional[Path] = typer.Option(
        None,
        "--schema-dir", "-s",
        help="Path to _schema directory",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output directory for reports (default: OUTPUT/)",
    ),
    force: bool = typer.Option(
        False,
        "--force", "-f",
        help="Force re-audit all documents (ignore cache)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Verbose output",
    ),
):
    """
    Fully automatic audit with caching and incremental updates.
    
    This is the recommended way to run audits. It will:
    
    1. Scan all documents and detect changes (via content hash)
    2. Run regex validation on changed documents
    3. Build document dependency graph
    4. Generate/update document summaries
    5. Audit only documents that have changed
    6. Save all intermediate data for audit trail
    7. Generate master report
    
    Examples:
    
        llm-audit auto .
        
        llm-audit auto . --force
        
        llm-audit auto Company/ --output reports/
    """
    # Find schema directory
    if not schema_dir:
        schema_dir = find_schema_dir(docs_dir)
        if not schema_dir:
            console.print("[red]Could not find _schema directory[/red]")
            console.print("Use --schema-dir to specify the path")
            raise typer.Exit(1)
    
    # Set default output directory
    if not output_dir:
        # Try to find OUTPUT dir relative to docs
        output_dir = docs_dir / "OUTPUT"
    
    # Load config
    orchestrator_config = load_config(config)
    
    console.print(Panel.fit(
        "[bold blue]CCASH Integrated Audit System[/bold blue]\n"
        f"Documents: {docs_dir}\n"
        f"Schema: {schema_dir}\n"
        f"Output: {output_dir}\n"
        f"Force: {force}",
        title="Configuration",
    ))
    
    # Run the integrated orchestrator
    async def run_audit():
        orchestrator = IntegratedOrchestrator(
            docs_dir=docs_dir,
            schema_dir=schema_dir,
            output_dir=output_dir,
            config=orchestrator_config,
        )
        
        def progress_callback(msg: str):
            if verbose or not msg.startswith("  "):
                console.print(msg)
        
        reports = await orchestrator.run_full_audit(
            force=force,
            progress_callback=progress_callback,
        )
        
        return reports

    reports = asyncio.run(run_audit())    # Print summary
    passed = sum(1 for r in reports.values() if r.overall_status == "pass")
    failed = sum(1 for r in reports.values() if r.overall_status == "fail")
    needs_review = sum(1 for r in reports.values() if r.overall_status == "needs_review")
    
    console.print()
    console.print(Panel.fit(
        f"[green]Passed[/green]: {passed}\n"
        f"[red]Failed[/red]: {failed}\n"
        f"[yellow]Needs Review[/yellow]: {needs_review}\n"
        f"\nReports saved to: {output_dir}",
        title="Audit Complete",
    ))
    
    # Exit with error code if any failures
    if failed > 0:
        raise typer.Exit(1)


@app.command()
def status(
    output_dir: Path = typer.Argument(
        Path("OUTPUT"),
        help="Output directory containing audit cache",
    ),
):
    """
    Show audit cache status and document states.
    """
    from llm_audit.cache import CacheManager
    
    cache_manager = CacheManager(output_dir)
    cache = cache_manager.cache
    
    if not cache.documents:
        console.print("[yellow]No audit cache found. Run 'llm-audit auto' first.[/yellow]")
        raise typer.Exit(0)
    
    # Build table
    table = Table(title="Document Audit Status")
    table.add_column("Doc Code", style="cyan")
    table.add_column("Summary", justify="center")
    table.add_column("Validated", justify="center")
    table.add_column("Audited", justify="center")
    table.add_column("Needs Update", justify="center")
    
    for doc_code in sorted(cache.documents.keys()):
        doc = cache.documents[doc_code]
        
        summary_ok = "✅" if not doc.needs_summary() else "❌"
        validation_ok = "✅" if not doc.needs_validation() else "❌"
        audit_ok = "✅" if not doc.needs_audit() else "❌"
        
        needs_update = "Yes" if (doc.needs_summary() or doc.needs_validation() or doc.needs_audit()) else "No"
        needs_style = "yellow" if needs_update == "Yes" else "green"
        
        table.add_row(
            doc_code,
            summary_ok,
            validation_ok,
            audit_ok,
            f"[{needs_style}]{needs_update}[/{needs_style}]",
        )
    
    console.print(table)
    
    # Summary
    needs_summary = len(cache.get_documents_needing_summary())
    needs_validation = len(cache.get_documents_needing_validation())
    needs_audit = len(cache.get_documents_needing_audit())
    
    console.print()
    console.print(f"Documents needing summary: {needs_summary}")
    console.print(f"Documents needing validation: {needs_validation}")
    console.print(f"Documents needing audit: {needs_audit}")
    
    if cache.last_full_run:
        console.print(f"\nLast full run: {cache.last_full_run}")


@app.command()
def clear_cache(
    output_dir: Path = typer.Argument(
        Path("OUTPUT"),
        help="Output directory containing audit cache",
    ),
    confirm: bool = typer.Option(
        False,
        "--yes", "-y",
        help="Skip confirmation prompt",
    ),
):
    """
    Clear the audit cache to force full re-processing.
    """
    from llm_audit.cache import CacheManager
    
    if not confirm:
        confirm = typer.confirm("Are you sure you want to clear the audit cache?")
    
    if confirm:
        cache_manager = CacheManager(output_dir)
        cache_manager.reset()
        console.print("[green]Cache cleared.[/green]")
    else:
        console.print("[yellow]Cancelled.[/yellow]")


@app.command()
def generate_kb_index(
    kb_dir: Path = typer.Argument(
        ...,
        help="Path to knowledge_base directory",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output path for relevance index JSON",
    ),
    report: Optional[Path] = typer.Option(
        None,
        "--report", "-r",
        help="Output path for human-readable report",
    ),
):
    """
    Generate KB relevance index mapping KB sources to document categories.
    
    This analyzes each KB file and determines which document types it is
    relevant to, creating an index that speeds up per-document audits.
    """
    import asyncio
    from llm_audit.kb_relevance import generate_relevance_index, export_relevance_report
    from llm_audit.providers import create_provider_from_env
    
    if not kb_dir.exists():
        console.print(f"[red]KB directory not found: {kb_dir}[/red]")
        raise typer.Exit(1)
    
    console.print(f"[cyan]Generating KB relevance index from {kb_dir}...[/cyan]")
    
    provider = create_provider_from_env()
    cache_path = output or (kb_dir.parent / "kb_relevance_index.json")
    
    async def run():
        return await generate_relevance_index(kb_dir, provider, cache_path)
    
    index = asyncio.run(run())
    
    console.print(f"[green]✓ Generated index with {len(index.kb_summaries)} sources[/green]")
    console.print(f"[green]✓ Categories mapped: {len(index.category_index)}[/green]")
    console.print(f"[green]✓ Saved to: {cache_path}[/green]")
    
    if report:
        export_relevance_report(index, report)
        console.print(f"[green]✓ Report saved to: {report}[/green]")


def main():
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
