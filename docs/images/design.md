# Design Decisions

## Why CandidateFragment?

Every source has different structure.

Instead of directly creating CandidateProfile,
every parser produces CandidateFragment.

Benefits

- Independent parsers
- Easier testing
- Easy to add new sources

---

## Why separate Normalization?

Normalization should never merge data.

Responsibilities

Parser
↓

Normalization

↓

Merge

↓

Projection

↓

Validation

Single Responsibility Principle.

---

## Merge Policy

Scalar values

Highest confidence wins.

Collections

Normalize
↓

Deduplicate

↓

Merge provenance

↓

Keep highest confidence

---

## Projection

Output schema is runtime configurable.

No code changes required.

---

## Validation

Output validated before writing JSON.

Prevents invalid output.