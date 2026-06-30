# Candidate Data Transformer

> Multi-Source Candidate Data Transformer for the Eightfold Engineering Intern Assignment.

---

## Overview

Recruiting systems receive candidate information from multiple independent sources. These sources may contain duplicated, incomplete, conflicting, malformed, or differently formatted information.

This project transforms heterogeneous candidate data into **one clean, canonical, validated JSON profile** that can be consumed safely by downstream recruiting systems.

The pipeline is deterministic, explainable, configurable at runtime, and robust to missing or malformed inputs.

---

## Key Capabilities

- Multi-source candidate data ingestion
- Structured source support
- Unstructured source support
- Canonical candidate schema
- Intermediate `CandidateFragment` model
- Email, phone, skill, name, company, and title normalization
- Deduplication across sources
- Conflict resolution using confidence scores
- Field-level provenance tracking
- Profile-level confidence scoring
- Runtime configurable output projection
- Output validation before writing JSON
- CLI-based input/output surface
- Automated tests

---

## Supported Input Sources

| Source | Category | File |
|---|---|---|
| Recruiter CSV | Structured | `data/inputs/recruiter.csv` |
| ATS JSON | Structured | `data/inputs/ats.json` |
| Recruiter Notes TXT | Unstructured | `data/inputs/notes.txt` |

This satisfies the requirement to handle at least one structured source and one unstructured source.

---

## Architecture

```text
                     Input Sources
                           |
       ------------------------------------------------
       |                      |                       |
 Recruiter CSV            ATS JSON              Notes TXT
       |                      |                       |
       ---------------- ParserService ----------------
                           |
                           v
                  CandidateFragment[]
                           |
                           v
                 NormalizationService
                           |
                           v
             Normalized CandidateFragment[]
                           |
                           v
                      MergeService
                           |
                           v
                    CandidateProfile
                           |
                           v
                   ProjectionService
                           |
                           v
                    OutputValidator
                           |
                           v
                 Final Canonical JSON
```

---

## Pipeline

```text
detect sources
    ↓
extract
    ↓
normalize
    ↓
merge
    ↓
confidence
    ↓
project-to-output
    ↓
validate
    ↓
emit JSON
```

Each step has a separate responsibility.

| Step | Purpose |
|---|---|
| Detect | Locate supported input files |
| Extract | Convert raw source data into `CandidateFragment` |
| Normalize | Standardize formats such as phone, email, skills |
| Merge | Resolve duplicates and conflicts |
| Confidence | Assign field-level and profile-level confidence |
| Project | Apply runtime output configuration |
| Validate | Check final JSON before writing |
| Emit | Save final JSON output |

---

## Project Structure

```text
candidate-data-transformer/
│
├── app/
│   ├── main.py
│   ├── settings.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── candidate.py
│   │
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base_parser.py
│   │   ├── csv_parser.py
│   │   ├── ats_parser.py
│   │   └── notes_parser.py
│   │
│   ├── normalizers/
│   │   ├── __init__.py
│   │   ├── email_normalizer.py
│   │   ├── phone_normalizer.py
│   │   ├── skill_normalizer.py
│   │   └── text_normalizer.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser_service.py
│   │   ├── normalization_service.py
│   │   ├── merge_service.py
│   │   ├── confidence_service.py
│   │   └── projection_service.py
│   │
│   └── validators/
│       ├── __init__.py
│       ├── candidate_validator.py
│       └── output_validator.py
│
├── data/
│   ├── inputs/
│   │   ├── recruiter.csv
│   │   ├── ats.json
│   │   └── notes.txt
│   │
│   ├── configs/
│   │   ├── custom_config.json
│   │   ├── minimal_config.json
│   │   ├── full_config.json
│   │   └── error_config.json
│   │
│   └── outputs/
│       └── canonical_profile.json
│
├── docs/
│   ├── one_page_design.md
│   └── images/
│
├── examples/
│   ├── input.csv
│   ├── ats.json
│   ├── notes.txt
│   └── output.json
│
├── tests/
│   └── test_phase0.py
│
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

---

## Technology Stack

| Area | Tool |
|---|---|
| Language | Python 3.12 |
| CLI | Typer |
| Console Output | Rich |
| Data Validation | Pydantic |
| CSV Parsing | Pandas |
| Phone Normalization | phonenumbers |
| Testing | Pytest |
| Configuration | JSON |
| Version Control | Git / GitHub |

---

## Installation

Clone the repository.

```bash
git clone https://github.com/saumyasrivastava21/candidate-data-transformer.git
cd candidate-data-transformer
```

Create and activate a Conda environment.

```bash
conda create -n candidate-transformer python=3.12 -y
conda activate candidate-transformer
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Run Commands

### Health Check

```bash
python -m app.main health
```

Expected behavior:

```text
Candidate Data Transformer is running successfully.
```

---

### Parse Sources

```bash
python -m app.main parse-sources
```

This detects supported files and converts them into `CandidateFragment` objects.

---

### Normalize Sources

```bash
python -m app.main normalize-sources
```

This normalizes extracted values such as phones, emails, names, companies, titles, and skills.

---

### Merge Sources

```bash
python -m app.main merge-sources
```

This merges normalized fragments into one `CandidateProfile`.

---

### Project Output

```bash
python -m app.main project-sources
```

This applies the default custom configuration and prints projected JSON.

---

### Run Full Pipeline

```bash
python -m app.main run
```

This runs the complete pipeline and writes output to:

```text
data/outputs/canonical_profile.json
```

---

### Run With Custom Config

```bash
python -m app.main run --config-path data/configs/custom_config.json
```

---

### Validate Output

```bash
python -m app.main validate-output
```

---

### Run Tests

```bash
pytest
```

Expected result:

```text
19 passed
```

---

## Sample Inputs

### Recruiter CSV

File:

```text
data/inputs/recruiter.csv
```

```csv
candidate_id,name,email,phone,current_company,title
cand_001,Saumya Srivastava,saumya@example.com,+91 9876543210,OralVis Healthcare,AI Research Intern
```

---

### ATS JSON

File:

```text
data/inputs/ats.json
```

```json
{
  "candidateId": "cand_001",
  "candidateName": "Saumya Srivastava",
  "mail": "saumya@example.com",
  "mobile": "9876543210",
  "company": "OralVis Healthcare",
  "jobTitle": "Machine Learning Engineer Intern",
  "skillsText": "Python, YOLO, Computer Vision, FastAPI, Spring Boot"
}
```

---

### Recruiter Notes

File:

```text
data/inputs/notes.txt
```

```text
Candidate has strong experience in computer vision and healthcare AI.
Worked on YOLO-based dental disease detection.
Good Java and Spring Boot backend knowledge.
Strong DSA profile with 500+ problems solved.
```

---

## Produced Output

Running:

```bash
python -m app.main run --config-path data/configs/full_config.json
```

produces:

```json
{
  "candidate_id": "cand_001",
  "full_name": "Saumya Srivastava",
  "primary_email": "saumya@example.com",
  "primary_phone": "+919876543210",
  "current_company": "OralVis Healthcare",
  "current_title": "AI Research Intern",
  "skills": [
    "Python",
    "YOLO",
    "Computer Vision",
    "FastAPI",
    "Spring Boot",
    "Java",
    "Healthcare AI",
    "DSA"
  ],
  "confidence": 1.0
}
```

---

## Runtime Configurable Output

The pipeline separates the internal canonical profile from the output projection layer.

This means the same engine can produce different output shapes without code changes.

---

### Example: Custom Config

File:

```text
data/configs/custom_config.json
```

```json
{
  "fields": [
    {
      "path": "full_name",
      "type": "string",
      "required": true
    },
    {
      "path": "primary_email",
      "from": "emails[0]",
      "type": "string",
      "required": true
    },
    {
      "path": "phone",
      "from": "phones[0]",
      "type": "string",
      "normalize": "E164"
    },
    {
      "path": "skills",
      "from": "skills[].name",
      "type": "string[]",
      "normalize": "canonical"
    }
  ],
  "include_confidence": true,
  "include_provenance": true,
  "on_missing": "null"
}
```

Run:

```bash
python -m app.main run --config-path data/configs/custom_config.json
```

Output:

```json
{
  "full_name": "Saumya Srivastava",
  "primary_email": "saumya@example.com",
  "phone": "+919876543210",
  "skills": [
    "Python",
    "YOLO",
    "Computer Vision",
    "FastAPI",
    "Spring Boot",
    "Java",
    "Healthcare AI",
    "DSA"
  ]
}
```

---

### Minimal Config

File:

```text
data/configs/minimal_config.json
```

```json
{
  "fields": [
    {
      "path": "full_name",
      "type": "string",
      "required": true
    },
    {
      "path": "primary_email",
      "from": "emails[0]",
      "type": "string",
      "required": true
    }
  ],
  "include_confidence": false,
  "include_provenance": false,
  "on_missing": "null"
}
```

Run:

```bash
python -m app.main run --config-path data/configs/minimal_config.json
```

Output:

```json
{
  "full_name": "Saumya Srivastava",
  "primary_email": "saumya@example.com"
}
```

---

### Full Config

File:

```text
data/configs/full_config.json
```

```json
{
  "fields": [
    {
      "path": "candidate_id",
      "type": "string",
      "required": false
    },
    {
      "path": "full_name",
      "type": "string",
      "required": true
    },
    {
      "path": "primary_email",
      "from": "emails[0]",
      "type": "string",
      "required": true
    },
    {
      "path": "primary_phone",
      "from": "phones[0]",
      "type": "string",
      "required": false
    },
    {
      "path": "current_company",
      "type": "string",
      "required": false
    },
    {
      "path": "current_title",
      "type": "string",
      "required": false
    },
    {
      "path": "skills",
      "from": "skills[].name",
      "type": "string[]",
      "required": false
    },
    {
      "path": "confidence",
      "from": "global_confidence.score",
      "type": "number",
      "required": false
    }
  ],
  "include_confidence": false,
  "include_provenance": false,
  "on_missing": "null"
}
```

Run:

```bash
python -m app.main run --config-path data/configs/full_config.json
```

---

### Error Config

File:

```text
data/configs/error_config.json
```

```json
{
  "fields": [
    {
      "path": "missing_required_field",
      "from": "linkedin.url",
      "type": "string",
      "required": true
    }
  ],
  "include_confidence": false,
  "include_provenance": false,
  "on_missing": "error"
}
```

Run:

```bash
python -m app.main run --config-path data/configs/error_config.json
```

Expected behavior:

```text
Missing required field: linkedin.url
```

This demonstrates controlled failure for missing required projected fields.

---

## Canonical Internal Schema

The internal canonical model is represented by `CandidateProfile`.

Main fields:

| Field | Type |
|---|---|
| candidate_id | string |
| full_name | FieldValue |
| emails | Email[] |
| phones | Phone[] |
| current_company | FieldValue |
| current_title | FieldValue |
| skills | Skill[] |
| experience | Experience[] |
| education | Education[] |
| links | Links |
| global_confidence | Confidence |
| metadata | object |

Each important field can include:

- value
- confidence
- provenance

---

## Why CandidateFragment Exists

Each source may have different field names and structure.

For example:

- CSV uses `name`
- ATS JSON uses `candidateName`
- Notes are free text

Instead of parsing directly into the final profile, every parser creates a `CandidateFragment`.

This keeps the pipeline modular:

```text
Raw Source
    ↓
Parser
    ↓
CandidateFragment
    ↓
Normalization
    ↓
Merge
    ↓
CandidateProfile
```

Benefits:

- Parsers are independent
- Adding a new source is simpler
- Merge logic remains centralized
- Testing is easier
- Provenance is preserved

---

## Normalization Rules

### Email

```text
SAUMYA@Example.COM
```

becomes:

```text
saumya@example.com
```

---

### Phone

```text
9876543210
+91 9876543210
```

both become:

```text
+919876543210
```

Phone normalization follows E.164 format.

---

### Skills

```text
springboot
Spring Boot
SPRING_BOOT
```

become:

```text
Spring Boot
```

Other examples:

```text
ml → Machine Learning
cv → Computer Vision
```

---

### Company

Common suffixes are cleaned where applicable.

Example:

```text
Google LLC
```

becomes:

```text
Google
```

---

## Merge and Conflict Resolution Policy

### Match Keys

Candidate records are matched using:

1. Candidate ID
2. Normalized email
3. Normalized phone

---

### Scalar Fields

For scalar fields such as:

- full name
- company
- title

the value with the highest confidence wins.

Example:

```text
Recruiter CSV name confidence: 0.98
ATS JSON name confidence: 0.95
```

Winner:

```text
Recruiter CSV name
```

---

### List Fields

For list fields such as:

- emails
- phones
- skills

the policy is:

```text
normalize
    ↓
deduplicate
    ↓
merge provenance
    ↓
keep highest confidence
```

Example:

```text
9876543210
+91 9876543210
```

Final value:

```text
+919876543210
```

---

## Confidence Scoring

The project uses field-level confidence and profile-level confidence.

Profile-level confidence uses the following signals:

| Signal | Weight |
|---|---|
| Name present | 0.30 |
| Email present | 0.30 |
| Phone present | 0.20 |
| 3+ skills present | 0.20 |

Maximum score:

```text
1.0
```

---

## Provenance Tracking

Every extracted field can store where it came from.

Example:

```json
{
  "source": "recruiter_csv",
  "source_file": "recruiter.csv",
  "field_path": "email",
  "extraction_method": "csv_column_mapping",
  "raw_value": "saumya@example.com"
}
```

This makes the output explainable and traceable.

---

## Output Validation

Before writing the final JSON, the output is validated against the requested runtime config.

Validation checks:

- required fields
- expected types
- string fields
- string array fields
- number fields
- missing field behavior

Supported missing value behavior:

| Mode | Behavior |
|---|---|
| null | Put `null` when missing |
| omit | Remove field from output |
| error | Fail with clear validation error |

---

## Testing

Run:

```bash
pytest
```

Expected result:

```text
19 passed
```

The tests cover:

- directory setup
- sample input existence
- candidate model validation
- email validation
- parser service
- phone normalization
- email normalization
- skill normalization
- normalization service
- merge service
- conflict resolution
- projection service
- output validator
- missing field validation

---

## CLI Reference

| Command | Purpose |
|---|---|
| `health` | Check project setup |
| `parse-sources` | Parse supported input files |
| `normalize-sources` | Normalize parsed fragments |
| `merge-sources` | Merge fragments into canonical profile |
| `project-sources` | Generate configured projected output |
| `run` | Run full pipeline |
| `validate-output` | Validate generated output JSON |
| `validate-sample` | Validate sample candidate data |
| `sample-model` | Print sample model |

---

## Example End-to-End Run

```bash
python -m app.main health
python -m app.main parse-sources
python -m app.main normalize-sources
python -m app.main merge-sources
python -m app.main project-sources
python -m app.main run --config-path data/configs/full_config.json
python -m app.main validate-output --config-path data/configs/full_config.json
pytest
```

---

## Assumptions

- Candidate data is processed from local input files.
- The current sample represents one candidate.
- Indian phone numbers without a country code use India as the default region.
- Skills are canonicalized using a deterministic mapping.
- Unknown fields are not invented.
- Missing fields are handled according to the runtime config.
- Recruiter CSV and ATS JSON are treated as more reliable than recruiter notes.
- CLI is sufficient as the required input/output surface.

---

## Intentionally Left Out

The following were deliberately left out under time constraints:

- Full UI
- Database persistence
- LinkedIn scraping
- GitHub API integration
- Resume PDF parsing
- Authentication
- Multi-user dashboard
- Deployment setup

The core transformer engine was prioritized because the assignment emphasizes correctness, explainability, robust handling, and reasoning over UI polish.

---

## Robustness Behavior

The pipeline is designed so that:

- Missing supported files do not crash the entire design.
- Malformed or empty data is handled safely where possible.
- Unknown values remain null, omitted, or error based on config.
- Final output is validated before being written.

---

## Scalability Notes

The current implementation is stateless and file-based.

For thousands of candidates, the same design can be extended by:

- processing candidate files in batches
- running candidates independently
- parallelizing the pipeline
- streaming candidate records
- writing outputs to object storage or a database

The internal architecture already separates parsing, normalization, merging, projection, and validation, which makes batch execution straightforward.

---

## Future Work

Possible improvements:

- Resume PDF parser
- DOCX resume parser
- GitHub profile parser
- LinkedIn profile JSON parser
- HTML report generation
- Dockerfile
- GitHub Actions for automated tests
- Batch processing mode
- More advanced fuzzy matching for company names and skills

---

## Design Document

The one-page technical design is included separately as a PDF.

Expected filename format:

```text
SaumyaSrivastava_saumyasriv21@gmail.com_Eightfold.pdf
```

---

## Demo Video

The demo video should show:

1. Running the pipeline end-to-end
2. Showing the default output
3. Showing one custom config output
4. Explaining one design decision
5. Explaining one handled edge case

Suggested commands for demo:

```bash
python -m app.main health
python -m app.main run
python -m app.main run --config-path data/configs/full_config.json
python -m app.main validate-output --config-path data/configs/full_config.json
pytest
```

---

## Submission Contents

Final submission should include:

- Public GitHub repository link
- One-page design PDF
- README with exact run steps
- Produced output on sample inputs
- Tests
- Demo video link
- Assumptions and descoped items

---

## Author

**Saumya Srivastava**

Eightfold Engineering Intern Assignment  
Multi-Source Candidate Data Transformer
