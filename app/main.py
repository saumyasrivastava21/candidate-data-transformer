import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from app.settings import INPUT_DIR, CONFIG_DIR, OUTPUT_DIR, DEFAULT_OUTPUT_PATH

app = typer.Typer(help="Multi-Source Candidate Data Transformer CLI")
console = Console()


@app.command()
def health():
    console.print("[green]Candidate Data Transformer is running successfully.[/green]")
    console.print(f"Input directory: {INPUT_DIR}")
    console.print(f"Config directory: {CONFIG_DIR}")
    console.print(f"Output directory: {OUTPUT_DIR}")


@app.command()
def run(
    input_dir: Path = typer.Option(INPUT_DIR, help="Directory containing source files"),
    config_path: Optional[Path] = typer.Option(None, help="Optional custom output config"),
    output_path: Path = typer.Option(DEFAULT_OUTPUT_PATH, help="Output JSON file path"),
):
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

    dummy_output = {
        "status": "phase_0_success",
        "message": "Project skeleton is working. Real pipeline starts from Phase 1.",
        "input_files_detected": [file.name for file in files],
        "custom_config_loaded": config_data is not None,
        "next_phase": "Canonical Pydantic models and schema validation"
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dummy_output, f, indent=2)

    console.print("[green]Pipeline completed successfully.[/green]")
    console.print(f"Output written to: {output_path}")


if __name__ == "__main__":
    app()