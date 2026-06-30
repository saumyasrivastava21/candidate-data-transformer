# Candidate Data Transformer Architecture

## Pipeline

```text
                Input Sources
                     │
    ┌────────────────┼────────────────┐
    │                │                │
Recruiter CSV    ATS JSON        Notes TXT
    │                │                │
    └────────────ParserService────────┘
                     │
             CandidateFragment[]
                     │
          NormalizationService
                     │
      Normalized CandidateFragment[]
                     │
              MergeService
                     │
            CandidateProfile
                     │
          ProjectionService
                     │
             OutputValidator
                     │
          canonical_profile.json
```

---

### Components

ParserService

- Detects source
- Routes parser
- Produces CandidateFragment

NormalizationService

- Phone normalization
- Email normalization
- Skill normalization
- Text normalization

MergeService

- Deduplicate
- Conflict resolution
- Highest confidence wins

ProjectionService

- Runtime configurable output

OutputValidator

- Required field validation
- Output schema validation