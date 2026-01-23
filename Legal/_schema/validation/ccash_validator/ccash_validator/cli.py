"""
CLI interface for CCASH Document Validator.

Modern CLI using Typer with rich output.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from ccash_validator import __version__
from ccash_validator.config import load_config
from ccash_validator.models.enums import Severity, ValidationStatus
from ccash_validator.models.results import DocumentValidation, ValidationSummary
from ccash_validator.validator import DocumentValidator

# Create CLI app
app = typer.Typer(
    name="ccash-validate",
    help="CCASH Document Validator - Type-safe validation for legal documentation",
    add_completion=False,
)

console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"[bold blue]CCASH Validator[/bold blue] v{__version__}")
        raise typer.Exit()


@app.command()
def validate(
    document: Annotated[
        Optional[Path],
        typer.Argument(
            help="Document to validate (omit for --all)",
            exists=True,
            readable=True,
        ),
    ] = None,
    all_docs: Annotated[
        bool,
        typer.Option(
            "--all", "-a",
            help="Validate all documents in workspace",
        ),
    ] = False,
    patterns_file: Annotated[
        Optional[Path],
        typer.Option(
            "--patterns", "-p",
            help="Path to patterns.yaml",
            exists=True,
            readable=True,
        ),
    ] = None,
    check: Annotated[
        Optional[list[str]],
        typer.Option(
            "--check", "-c",
            help="Specific checks to run (metadata, markers, prohibited, required, semantic)",
        ),
    ] = None,
    enable_llm: Annotated[
        bool,
        typer.Option(
            "--llm",
            help="Enable LLM semantic analysis",
        ),
    ] = False,
    llm_provider: Annotated[
        str,
        typer.Option(
            "--llm-provider",
            help="LLM provider (mock, anthropic, openai)",
        ),
    ] = "mock",
    output_json: Annotated[
        bool,
        typer.Option(
            "--json", "-j",
            help="Output results as JSON",
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v",
            help="Verbose output with evidence",
        ),
    ] = False,
    errors_only: Annotated[
        bool,
        typer.Option(
            "--errors-only", "-e",
            help="Only show errors (not warnings or passes)",
        ),
    ] = False,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit",
        ),
    ] = None,
) -> None:
    """
    Validate CCASH legal documents against schema patterns.
    
    Examples:
    
        ccash-validate --all
        
        ccash-validate path/to/document.md
        
        ccash-validate --all --llm --llm-provider anthropic
        
        ccash-validate --all --check markers --check metadata
    """
    # Validate arguments
    if not document and not all_docs:
        console.print("[red]Error:[/red] Provide a document path or use --all")
        raise typer.Exit(1)
    
    # Find patterns file
    if patterns_file is None:
        candidates = [
            Path("patterns.yaml"),
            Path("_schema/validation/patterns.yaml"),
        ]
        for candidate in candidates:
            if candidate.exists():
                patterns_file = candidate
                break
        
        if patterns_file is None:
            console.print("[red]Error:[/red] Could not find patterns.yaml")
            console.print("Use --patterns to specify the path")
            raise typer.Exit(1)
    
    # Load configuration
    try:
        config = load_config(patterns_file)
    except Exception as e:
        console.print(f"[red]Error loading config:[/red] {e}")
        raise typer.Exit(1)
    
    # Create validator
    validator = DocumentValidator(
        config=config,
        enable_llm=enable_llm,
        llm_provider=llm_provider,
    )
    
    # Print header
    if not output_json:
        _print_header(enable_llm, llm_provider)
    
    # Run validation
    if all_docs:
        summary = validator.validate_all(checks=check)
        
        if output_json:
            console.print(json.dumps(summary.to_dict(), indent=2))
        else:
            _print_summary(summary, verbose, errors_only)
        
        # Exit with error code if there are errors
        if summary.total_errors > 0:
            raise typer.Exit(1)
    else:
        assert document is not None
        validation = validator.validate_document(document, checks=check)
        
        if output_json:
            console.print(json.dumps(validation.to_dict(), indent=2))
        else:
            _print_document_validation(validation, verbose, errors_only)
        
        if validation.has_errors:
            raise typer.Exit(1)


@app.command()
def list_registries(
    patterns_file: Annotated[
        Optional[Path],
        typer.Option(
            "--patterns", "-p",
            help="Path to patterns.yaml",
        ),
    ] = None,
) -> None:
    """
    List all loaded registry entries.
    
    Shows TERM, DOC, OBL, FLOW, DECISION, and RIGHT registries.
    """
    if patterns_file is None:
        patterns_file = Path("_schema/validation/patterns.yaml")
    
    try:
        config = load_config(patterns_file)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    
    from ccash_validator.models.enums import MarkerType
    from ccash_validator.validators.markers import MarkerValidator
    
    marker_validator = MarkerValidator(config.config, config.schema_dir)
    
    for marker_type in MarkerType:
        registry = marker_validator.get_registry(marker_type)
        if registry:
            table = Table(title=f"[bold]{marker_type}[/bold] Registry ({len(registry)} entries)")
            table.add_column("ID", style="cyan")
            table.add_column("Aliases", style="dim")
            
            for entry in registry.entries[:20]:  # Limit display
                aliases = ", ".join(entry.aliases) if entry.aliases else "-"
                table.add_row(entry.id, aliases)
            
            if len(registry.entries) > 20:
                table.add_row(f"... and {len(registry.entries) - 20} more", "")
            
            console.print(table)
            console.print()


@app.command()
def check_syntax(
    document: Annotated[
        Path,
        typer.Argument(
            help="Document to check",
            exists=True,
            readable=True,
        ),
    ],
) -> None:
    """
    Quick syntax check for a single document.
    
    Checks only metadata and marker syntax (not registry validation).
    """
    content = document.read_text()
    
    console.print(f"\n[bold]Syntax Check:[/bold] {document.name}\n")
    
    # Check effective date
    import re
    has_date = bool(re.search(r'Effective Date:', content, re.IGNORECASE))
    has_version = bool(re.search(r'Version:\s*\d+\.\d+', content, re.IGNORECASE))
    
    if has_date:
        console.print("  [green]✓[/green] Has effective date")
    else:
        console.print("  [red]✗[/red] Missing effective date")
    
    if has_version:
        console.print("  [green]✓[/green] Has version number")
    else:
        console.print("  [yellow]⚠[/yellow] Missing version number")
    
    # Check markers
    markers = {
        "TERM": re.findall(r'\[TERM:[^\]]+\]', content),
        "DOC": re.findall(r'\[DOC:[^\]]+\]', content),
        "OBL": re.findall(r'\[OBL:[^\]]+\]', content),
        "FLOW": re.findall(r'\[FLOW:[^\]]+\]', content),
    }
    
    console.print("\n[bold]Markers found:[/bold]")
    for marker_type, found in markers.items():
        if found:
            console.print(f"  {marker_type}: {len(found)}")


@app.command()
def populate(
    document: Annotated[
        Path,
        typer.Argument(
            help="Document to populate placeholders in",
            exists=True,
            readable=True,
        ),
    ],
    patterns_file: Annotated[
        Optional[Path],
        typer.Option(
            "--patterns", "-p",
            help="Path to patterns.yaml",
        ),
    ] = None,
    entity: Annotated[
        str,
        typer.Option(
            "--entity", "-e",
            help="Entity context for role resolution (company, p-1, c-001, etc.)",
        ),
    ] = "company",
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run", "-n",
            help="Show what would be changed without modifying file",
        ),
    ] = False,
    output_file: Annotated[
        Optional[Path],
        typer.Option(
            "--output", "-o",
            help="Write to different file instead of modifying in place",
        ),
    ] = None,
) -> None:
    """
    Populate [PERSON:*], [ROLE:*], [CONFIG:*] markers with registry data.
    
    Resolves markers to actual values from persons.md and assignments.md.
    Also replaces [________________] placeholders mapped in field_mappings.md.
    
    Examples:
    
        ccash populate Company/Formation/A1_Articles_of_Organization.md
        
        ccash populate document.md --entity p-1 --dry-run
        
        ccash populate document.md --output document-filled.md
    """
    import re
    
    if patterns_file is None:
        patterns_file = Path("_schema/validation/patterns.yaml")
    
    try:
        config = load_config(patterns_file)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    
    from ccash_validator.registry.persons import load_persons_registry, PersonEntry
    from ccash_validator.registry.assignments import load_assignments_registry
    
    schema_dir = config.schema_dir
    persons = load_persons_registry(schema_dir)
    assignments = load_assignments_registry(schema_dir)
    
    content = document.read_text(encoding="utf-8")
    original_content = content
    replacements: list[tuple[str, str]] = []
    
    # 1. Replace [PERSON:xxx] markers
    person_pattern = re.compile(r'\[PERSON:([A-Za-z0-9_.-]+)\]')
    for match in person_pattern.finditer(content):
        full_marker = match.group(0)
        value = match.group(1)
        
        # Split into ID and optional field path
        parts = value.split(".", 1)
        person_id = parts[0]
        field_path = parts[1] if len(parts) > 1 else "display_name"
        
        person = persons.get(person_id)
        if person and isinstance(person, PersonEntry):
            resolved = person.get_field(field_path)
            if resolved:
                replacements.append((full_marker, resolved))
                content = content.replace(full_marker, resolved, 1)
    
    # 2. Replace [ROLE:xxx] markers  
    role_pattern = re.compile(r'\[ROLE:([A-Za-z0-9_./-]+)\]')
    for match in role_pattern.finditer(content):
        full_marker = match.group(0)
        value = match.group(1)
        
        parts = value.split(".")
        if len(parts) < 2:
            continue
        
        entity_id = parts[0]
        role_type = parts[1]
        field_path = ".".join(parts[2:]) if len(parts) > 2 else "display_name"
        
        # Get the role assignment
        entity_assign = assignments.get_entity(entity_id)
        if entity_assign:
            role = entity_assign.get_role(role_type)
            if role:
                resolved = None
                
                # First check if field is on the assignment itself
                assignment_fields = ["ownership_percentage", "title", "abbreviation", "reports_to"]
                if field_path in assignment_fields:
                    resolved = role.get_field(field_path)
                
                # Otherwise resolve from the person record
                if not resolved:
                    person = persons.get(role.person_id)
                    if person and isinstance(person, PersonEntry):
                        resolved = person.get_field(field_path)
                
                if resolved:
                    replacements.append((full_marker, resolved))
                    content = content.replace(full_marker, resolved, 1)
    
    # 3. Replace [CONFIG:xxx] markers (basic implementation)
    config_pattern = re.compile(r'\[CONFIG:([A-Za-z0-9_./-]+)\]')
    # CONFIG markers would need a config registry - skip for now
    
    # Print results
    console.print()
    console.print(f"[bold]Populating:[/bold] {document.name}")
    console.print(f"[bold]Entity context:[/bold] {entity}")
    console.print()
    
    if replacements:
        table = Table(title="Replacements")
        table.add_column("Marker", style="cyan")
        table.add_column("Value", style="green")
        
        for marker, value in replacements[:20]:
            display_value = value[:50] + "..." if len(value) > 50 else value
            table.add_row(marker, display_value)
        
        if len(replacements) > 20:
            table.add_row(f"... and {len(replacements) - 20} more", "")
        
        console.print(table)
        console.print()
        console.print(f"[bold]Total replacements:[/bold] {len(replacements)}")
    else:
        console.print("[yellow]No markers found to replace[/yellow]")
    
    # Write output
    if not dry_run and replacements:
        output_path = output_file if output_file else document
        output_path.write_text(content, encoding="utf-8")
        console.print(f"\n[green]✓[/green] Written to {output_path}")
    elif dry_run:
        console.print("\n[dim]Dry run - no changes made[/dim]")


def _print_header(enable_llm: bool, llm_provider: str) -> None:
    """Print validation header."""
    console.print()
    console.print(Panel.fit(
        f"[bold blue]CCASH Document Validator[/bold blue] v{__version__}\n"
        f"LLM: {'[green]Enabled[/green] (' + llm_provider + ')' if enable_llm else '[dim]Disabled[/dim]'}",
        border_style="blue",
    ))
    console.print()


def _print_summary(summary: ValidationSummary, verbose: bool, errors_only: bool) -> None:
    """Print validation summary."""
    # Print per-document results
    for doc in summary.documents:
        if errors_only and doc.is_clean:
            continue
        _print_document_validation(doc, verbose, errors_only)
    
    # Print overall summary
    console.print()
    table = Table(title="[bold]Validation Summary[/bold]", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")
    
    table.add_row("Documents", str(summary.document_count))
    table.add_row("With Errors", str(summary.documents_with_errors))
    table.add_row("Clean", str(summary.documents_clean))
    table.add_row("─" * 15, "─" * 10)
    table.add_row("Total Checks", str(summary.total_checks))
    table.add_row("[green]Passed[/green]", str(summary.total_passed))
    table.add_row("[red]Errors[/red]", str(summary.total_errors))
    table.add_row("[yellow]Warnings[/yellow]", str(summary.total_warnings))
    
    console.print(table)
    console.print()
    
    if summary.is_passing:
        console.print("[bold green]✅ VALIDATION PASSED[/bold green]")
    else:
        console.print("[bold red]❌ VALIDATION FAILED[/bold red]")
    console.print()


def _print_document_validation(
    doc: DocumentValidation, 
    verbose: bool, 
    errors_only: bool
) -> None:
    """Print validation results for a single document."""
    # Document header
    status_icon = "✅" if doc.is_clean else "❌" if doc.has_errors else "⚠️"
    console.print(f"\n{status_icon} [bold]{doc.document_name}[/bold]")
    console.print(f"   [dim]{doc.document_path}[/dim]")
    
    # Filter results
    results = doc.results
    if errors_only:
        results = [r for r in results if r.is_failed]
    
    # Print results
    for result in results:
        _print_result(result, verbose)


def _print_result(result, verbose: bool) -> None:
    """Print a single validation result."""
    if result.status == ValidationStatus.PASS:
        if verbose:
            console.print(f"   [green]✓[/green] {result.rule_id}: {result.message}")
    elif result.status == ValidationStatus.FAIL:
        severity_color = "red" if result.severity == Severity.ERROR else "yellow"
        icon = result.severity.emoji
        llm_tag = " [dim][LLM][/dim]" if result.llm_assisted else ""
        
        console.print(f"   [{severity_color}]{icon}[/{severity_color}] {result.rule_id}: {result.message}{llm_tag}")
        
        if verbose and result.evidence:
            console.print(f"      [dim]Evidence: {result.evidence[:80]}...[/dim]" if len(result.evidence or "") > 80 
                         else f"      [dim]Evidence: {result.evidence}[/dim]")
        
        if verbose and result.line_number:
            console.print(f"      [dim]Line: {result.line_number}[/dim]")


if __name__ == "__main__":
    app()
