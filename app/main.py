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
def sample_model():
    """
    Create and print a sample validated CandidateProfile.
    """

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
        current_company=FieldValue(
            value="OralVis Healthcare",
            confidence=Confidence(score=0.9, reason="Found in multiple structured sources"),
            provenance=[
                Provenance(
                    source=SourceType.ATS_JSON,
                    source_file="ats.json",
                    field_path="company",
                    extraction_method="json_field_mapping",
                    raw_value="OralVis Healthcare",
                )
            ],
        ),
        current_title=FieldValue(
            value="AI Research Intern",
            confidence=Confidence(score=0.88, reason="Found in recruiter CSV"),
            provenance=[
                Provenance(
                    source=SourceType.RECRUITER_CSV,
                    source_file="recruiter.csv",
                    field_path="title",
                    extraction_method="csv_column_mapping",
                    raw_value="AI Research Intern",
                )
            ],
        ),
        skills=[
            Skill(value="Python", confidence=Confidence(score=0.95, reason="Detected in ATS skillsText")),
            Skill(value="YOLO", confidence=Confidence(score=0.95, reason="Detected in ATS skillsText")),
            Skill(value="Spring Boot", confidence=Confidence(score=0.9, reason="Detected in notes")),
        ],
        global_confidence=Confidence(score=0.93, reason="Strong identity and profile matches"),
        metadata={
            "phase": "1",
            "description": "Canonical Pydantic model validation successful",
        },
    )

    console.print_json(json.dumps(candidate.to_clean_dict(), indent=2))


@app.command()
def validate_sample():
    """
    Validate a sample candidate and print validation result.
    """

    candidate_data = {
        "candidate_id": "cand_001",
        "full_name": {
            "value": "Saumya Srivastava",
            "confidence": {
                "score": 0.98,
                "reason": "Name found in structured source"
            },
            "provenance": [
                {
                    "source": "recruiter_csv",
                    "source_file": "recruiter.csv",
                    "field_path": "name",
                    "extraction_method": "csv_column_mapping",
                    "raw_value": "Saumya Srivastava"
                }
            ]
        },
        "emails": [
            {
                "value": "saumya@example.com",
                "confidence": {
                    "score": 0.99,
                    "reason": "Email from structured source"
                }
            }
        ],
        "phones": [
            {
                "value": "+919876543210",
                "confidence": {
                    "score": 0.9,
                    "reason": "Phone from structured source"
                }
            }
        ],
        "skills": [
            {
                "value": "Python",
                "confidence": {
                    "score": 0.95,
                    "reason": "Skill from ATS"
                }
            }
        ]
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
    Phase 1 dummy pipeline with canonical validated candidate profile.
    """

    console.print("[blue]Starting Candidate Transformer Pipeline...[/blue]")

    if not input_dir.exists():
        raise typer.BadParameter(f"Input directory does not exist: {input_dir}")

    files = list(input_dir.iterdir())

    config_data = None
    if config_path:
        if not config_path.exists():
            raise typer.BadParameter(f"Config file does not exist: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

    candidate = CandidateProfile(
        candidate_id="cand_001",
        full_name=FieldValue(
            value="Saumya Srivastava",
            confidence=Confidence(score=0.98, reason="Sample Phase 1 validated name"),
            provenance=[
                Provenance(
                    source=SourceType.RECRUITER_CSV,
                    source_file="recruiter.csv",
                    field_path="name",
                    extraction_method="sample_phase_1_mapping",
                    raw_value="Saumya Srivastava",
                )
            ],
        ),
        emails=[
            Email(
                value="saumya@example.com",
                confidence=Confidence(score=0.99, reason="Sample Phase 1 email"),
            )
        ],
        phones=[
            Phone(
                value="+919876543210",
                confidence=Confidence(score=0.9, reason="Sample Phase 1 phone"),
            )
        ],
        skills=[
            Skill(value="Python", confidence=Confidence(score=0.95)),
            Skill(value="YOLO", confidence=Confidence(score=0.95)),
            Skill(value="Spring Boot", confidence=Confidence(score=0.9)),
        ],
        global_confidence=Confidence(score=0.93),
        metadata={
            "status": "phase_1_success",
            "input_files_detected": [file.name for file in files],
            "custom_config_loaded": config_data is not None,
            "next_phase": "Parsers for CSV, ATS JSON, notes, resume, and GitHub",
        },
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(candidate.to_clean_dict(), f, indent=2)

    console.print("[green]Pipeline completed successfully.[/green]")
    console.print(f"Output written to: {output_path}")

    table = Table(title="Phase 1 Candidate Summary")
    table.add_column("Field")
    table.add_column("Value")

    table.add_row("Candidate ID", candidate.candidate_id or "")
    table.add_row("Name", candidate.full_name.value if candidate.full_name else "")
    table.add_row("Primary Email", candidate.emails[0].value if candidate.emails else "")
    table.add_row("Primary Phone", candidate.phones[0].value if candidate.phones else "")
    table.add_row("Skills", ", ".join(skill.value for skill in candidate.skills))
    table.add_row("Global Confidence", str(candidate.global_confidence.score))

    console.print(table)


if __name__ == "__main__":
    app()