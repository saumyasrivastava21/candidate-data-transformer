# Candidate Data Transformer - One Page Design

## Objective

Build a configurable pipeline that converts messy candidate data from multiple sources into one clean, validated JSON profile.

## Supported Inputs

| Source | Type | Example |
|---|---|---|
| Recruiter CSV | Structured | recruiter.csv |
| ATS JSON | Structured | ats.json |
| Recruiter Notes | Unstructured | notes.txt |

## Pipeline

Raw Inputs
→ ParserService
→ CandidateFragment[]
→ NormalizationService
→ MergeService
→ CandidateProfile
→ ProjectionService
→ OutputValidator
→ Final JSON

## Core Components

### ParserService
Detects source files and converts raw data into CandidateFragment objects.

### NormalizationService
Normalizes emails, phones, names, companies, titles, and skills.

### MergeService
Deduplicates values and resolves conflicts using confidence scores.

### ProjectionService
Applies runtime config to select, rename, and reshape output fields.

### OutputValidator
Validates projected JSON before writing final output.

## Merge Policy

- Scalar fields: highest confidence wins.
- List fields: normalize, deduplicate, merge provenance, keep highest confidence.
- Missing fields: handled by runtime config using null, omit, or error.

## Output Example

```json
{
  "full_name": "Saumya Srivastava",
  "primary_email": "saumya@example.com",
  "phone": "+919876543210",
  "skills": ["Python", "YOLO", "Spring Boot"]
}