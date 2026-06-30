# Candidate Data Transformer

A production-style candidate data transformation pipeline.

This project ingests messy candidate data from multiple sources and produces one clean, validated JSON output.

---

## Problem Statement

Recruiting systems receive candidate information from many places:

- Recruiter CSV files
- ATS JSON exports
- Recruiter notes
- Resume text/PDF
- External profiles

These sources can be incomplete, duplicated, inconsistent, or conflicting.

The goal is to transform all available candidate data into a single canonical profile with:

- source detection
- extraction
- normalization
- deduplication
- conflict resolution
- confidence scoring
- provenance tracking
- configurable output projection
- output validation

---

## Supported Sources

This implementation supports:

| Source | Type | File |
|---|---|---|
| Recruiter CSV | Structured | `data/inputs/recruiter.csv` |
| ATS JSON | Structured | `data/inputs/ats.json` |
| Recruiter Notes | Unstructured text | `data/inputs/notes.txt` |

---

## Architecture

```txt
Raw Input Files
        |
        v
ParserService
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
Projected JSON
        |
        v
OutputValidator
        |
        v
Final JSON Output