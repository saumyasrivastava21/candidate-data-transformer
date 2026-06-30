import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from app.models.candidate import (
    CandidateProfile,
    Confidence,
    Email,
    FieldValue,
    Phone,
    Provenance,
    Skill,
    SourceType,
)
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
    """
    Parse raw input files into CandidateFragment objects.
    """

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
def sample_model():
    candidate = CandidateProfile(
        candidate_id="cand_001",
        full_name=FieldValue(
            value="Saumya Srivastava",
            confidence=Confidence(score=0.98, reason="Name found in recruiter CSV and ATS JSON"),
            provenance=[
                Provenance(
                    source=SourceType.RECRUITER_CSV,
                    source_file="recruiter.csv",
                    field_path="name",
                    extraction_method="csv_column_mapping",
                    raw_value="Saumya Srivastava",
                )
            ],
        ),
        emails=[
            Email(
                value="SAUMYA@example.com",
                confidence=Confidence(score=0.99, reason="Email from structured CSV"),
                provenance=[
                    Provenance(
                        source=SourceType.RECRUITER_CSV,
                        source_file="recruiter.csv",
                        field_path="email",
                        extraction_method="csv_column_mapping",
                        raw_value="SAUMYA@example.com",
                    )
                ],
            )
        ],
        phones=[
            Phone(
                value="91 9876543210",
                confidence=Confidence(score=0.85, reason="Phone from recruiter CSV"),
                provenance=[
                    Provenance(
                        source=SourceType.RECRUITER_CSV,
                        source_file="recruiter.csv",
                        field_path="phone",
                        extraction_method="csv_column_mapping",
                        raw_value="+91 9876543210",
                    )
                ],
            )
        ],
        current_company=FieldValue(value="OralVis Healthcare"),
        current_title=FieldValue(value="AI Research Intern"),
        skills=[
            Skill(value="Python", confidence=Confidence(score=0.95)),
            Skill(value="YOLO", confidence=Confidence(score=0.95)),
            Skill(value="Spring Boot", confidence=Confidence(score=0.9)),
        ],
        global_confidence=Confidence(score=0.93, reason="Strong identity and profile matches"),
        metadata={
            "phase": "2",
            "description": "CandidateFragment parser architecture added",
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
    """
    Phase 2 pipeline:
    Raw files -> CandidateFragment list -> temporary CandidateProfile.
    """

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
    fragments = parser_service.parse_input_directory(input_dir)

    if not fragments:
        raise typer.BadParameter("No supported input files found.")

    primary_fragment = fragments[0]

    all_emails = []
    all_phones = []
    all_skills = []

    for fragment in fragments:
        all_emails.extend(fragment.emails)
        all_phones.extend(fragment.phones)
        all_skills.extend(fragment.skills)

    candidate = CandidateProfile(
        candidate_id=primary_fragment.candidate_id,
        full_name=primary_fragment.full_name,
        emails=all_emails,
        phones=all_phones,
        current_company=primary_fragment.current_company,
        current_title=primary_fragment.current_title,
        skills=all_skills,
        global_confidence=Confidence(score=0.80, reason="Temporary profile built from parsed fragments"),
        metadata={
            "status": "phase_2_success",
            "fragments_parsed": len(fragments),
            "sources": [fragment.source.value for fragment in fragments],
            "custom_config_loaded": config_data is not None,
            "next_phase": "Normalization engine for phones, skills, dates, duplicates",
        },
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(candidate.to_clean_dict(), f, indent=2)

    console.print("[green]Pipeline completed successfully.[/green]")
    console.print(f"Output written to: {output_path}")

    table = Table(title="Phase 2 Parser Summary")
    table.add_column("Metric")
    table.add_column("Value")

    table.add_row("Fragments Parsed", str(len(fragments)))
    table.add_row("Sources", ", ".join(fragment.source.value for fragment in fragments))
    table.add_row("Emails Extracted", str(len(all_emails)))
    table.add_row("Phones Extracted", str(len(all_phones)))
    table.add_row("Skills Extracted", str(len(all_skills)))

    console.print(table)


if __name__ == "__main__":
    app()