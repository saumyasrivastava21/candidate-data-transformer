# Multi-Source Candidate Data Transformer

This project converts messy candidate data from multiple sources into one clean canonical candidate profile.

## Problem

Recruiting systems receive candidate information from CSV files, ATS JSON blobs, resumes, GitHub profiles, LinkedIn profiles, and recruiter notes.

These sources can be incomplete, conflicting, duplicated, malformed, or unstructured.

## Goal

Generate one trustworthy canonical candidate profile with:

- normalized fields
- confidence scores
- provenance tracking
- configurable output schema

## Phase 0

Current features:

- CLI setup using Typer
- sample input files
- sample custom config
- output directory
- health command
- dummy pipeline execution

## Setup

```bash
conda activate candidate-transformer
pip install -r requirements.txt