import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from app.models.candidate import CandidateProfile, Confidence, Email, FieldValue, Phone, Skill
from app.services.merge_service import MergeService
from app.services.normalization_service import NormalizationService
from app.services.parser_service import ParserService
from app.settings import CONFIG_DIR, DEFAULT_OUTPUT_PATH, INPUT_DIR, OUTPUT_DIR
from app.validators.candidate_validator import collect_validation_errors

app = typer.Typer(help="Multi-Source Candidate Data Transformer CLI")
console = Console()


@app.command()
def health():
    console.print("[green]Candidate Data Transformer is running successfully.[/green]")
    console.print(f"Input directory: {INPUT_DIR}")
    console.print(f"Config directory: {CONFIG_DIR}")
    console.print(f"Output directory: {OUTPUT_DIR}")


@app.command()
def parse_sources(
    input_dir: Path = typer.Option(INPUT_DIR, help="Directory containing source files"),
):
    parser_service = ParserService()
    fragments = parser_service.parse_input_directory(input_dir)

    console.print(f"[green]Parsed {len(fragments)} source fragments successfully.[/green]")

    table = Table(title="Parsed Candidate Fragments")
    table.add_column("Source")
    table.add_column("File")
    table.add_column("Name")
    table.add_column("Emails")
    table.add_column("Phones")
    table.add_column("Skills")

    for fragment in fragments:
        table.add_row(
            fragment.source.value,
            fragment.source_file or "",
            fragment.full_name.value if fragment.full_name else "",
            ", ".join(email.value for email in fragment.emails),
            ", ".join(phone.value for phone in fragment.phones),
            ", ".join(skill.value for skill in fragment.skills),
        )

    console.print(table)


@app.command()
def normalize_sources(
    input_dir: Path = typer.Option(INPUT_DIR, help="Directory containing source files"),
):
    parser_service = ParserService()
    normalization_service = NormalizationService()

    fragments = parser_service.parse_input_directory(input_dir)
    normalized_fragments = normalization_service.normalize_fragments(fragments)

    console.print("[green]Sources parsed and normalized successfully.[/green]")

    table = Table(title="Normalized Candidate Fragments")
    table.add_column("Source")
    table.add_column("Emails")
    table.add_column("Phones")
    table.add_column("Skills")

    for fragment in normalized_fragments:
        table.add_row(
            fragment.source.value,
            ", ".join(email.value for email in fragment.emails),
            ", ".join(phone.value for phone in fragment.phones),
            ", ".join(skill.value for skill in fragment.skills),
        )

    console.print(table)


@app.command()
def merge_sources(
    input_dir: Path = typer.Option(INPUT_DIR, help="Directory containing source files"),
):
    parser_service = ParserService()
    normalization_service = NormalizationService()
    merge_service = MergeService()

    fragments = parser_service.parse_input_directory(input_dir)
    normalized_fragments = normalization_service.normalize_fragments(fragments)
    candidate = merge_service.merge_fragments(normalized_fragments)

    console.print("[green]Sources parsed, normalized, and merged successfully.[/green]")

    table = Table(title="Merged Candidate Profile")
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("Candidate ID", candidate.candidate_id or "")
    table.add_row("Name", candidate.full_name.value if candidate.full_name else "")
    table.add_row("Emails", ", ".join(email.value for email in candidate.emails))
    table.add_row("Phones", ", ".join(phone.value for phone in candidate.phones))
    table.add_row("Company", candidate.current_company.value if candidate.current_company else "")
    table.add_row("Title", candidate.current_title.value if candidate.current_title else "")
    table.add_row("Skills", ", ".join(skill.value for skill in candidate.skills))
    table.add_row("Global Confidence", str(candidate.global_confidence.score))

    console.print(table)


@app.command()
def sample_model():
    candidate = CandidateProfile(
        candidate_id="cand_001",
        full_name=FieldValue(value="Saumya Srivastava"),
        emails=[Email(value="SAUMYA@example.com")],
        phones=[Phone(value="91 9876543210")],
        skills=[
            Skill(value="python", confidence=Confidence(score=0.95)),
            Skill(value="springboot", confidence=Confidence(score=0.9)),
        ],
        global_confidence=Confidence(score=0.93),
        metadata={
            "phase": "4",
            "description": "Merge engine added",
        },
    )

    console.print_json(json.dumps(candidate.to_clean_dict(), indent=2))


@app.command()
def validate_sample():
    candidate_data = {
        "candidate_id": "cand_001",
        "full_name": {"value": "Saumya Srivastava"},
        "emails": [{"value": "saumya@example.com"}],
        "phones": [{"value": "+919876543210"}],
        "skills": [{"value": "Python"}],
    }

    errors = collect_validation_errors(candidate_data)

    if errors:
        console.print("[red]Validation failed[/red]")
        for error in errors:
            console.print(error)
    else:
        console.print("[green]Validation successful[/green]")


@app.command()
def run(
    input_dir: Path = typer.Option(INPUT_DIR, help="Directory containing source files"),
    config_path: Optional[Path] = typer.Option(None, help="Optional custom output config"),
    output_path: Path = typer.Option(DEFAULT_OUTPUT_PATH, help="Output JSON file path"),
):
    console.print("[blue]Starting Candidate Transformer Pipeline...[/blue]")

    if not input_dir.exists():
        raise typer.BadParameter(f"Input directory does not exist: {input_dir}")

    config_data = None
    if config_path:
        if not config_path.exists():
            raise typer.BadParameter(f"Config file does not exist: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

    parser_service = ParserService()
    normalization_service = NormalizationService()
    merge_service = MergeService()

    fragments = parser_service.parse_input_directory(input_dir)

    if not fragments:
        raise typer.BadParameter("No supported input files found.")

    normalized_fragments = normalization_service.normalize_fragments(fragments)
    candidate = merge_service.merge_fragments(normalized_fragments)

    candidate.metadata["custom_config_loaded"] = config_data is not None

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(candidate.to_clean_dict(), f, indent=2)

    console.print("[green]Pipeline completed successfully.[/green]")
    console.print(f"Output written to: {output_path}")

    table = Table(title="Phase 4 Merge Summary")
    table.add_column("Metric")
    table.add_column("Value")

    table.add_row("Fragments Parsed", str(len(fragments)))
    table.add_row("Fragments Normalized", str(len(normalized_fragments)))
    table.add_row("Unique Emails", str(len(candidate.emails)))
    table.add_row("Unique Phones", str(len(candidate.phones)))
    table.add_row("Unique Skills", str(len(candidate.skills)))
    table.add_row("Global Confidence", str(candidate.global_confidence.score))

    console.print(table)


if __name__ == "__main__":
    app()