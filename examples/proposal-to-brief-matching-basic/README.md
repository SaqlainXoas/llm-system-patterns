# Proposal to Brief Matching

![Badge](https://img.shields.io/badge/Example-Flagship%20Build-2563eb) ![Badge](https://img.shields.io/badge/Style-Service%20Files-0f172a) ![Badge](https://img.shields.io/badge/Goal-Pre--filter%20Then%20Semantic-16a34a)

## Goal
Learn the clean first-pass scoring flow used in this repo:
1. exact pre-filter first
2. semantic scoring second
3. final LLM validation last

## Flow
```mermaid
flowchart LR
  A[Load brief and proposals] --> B[Pre-filter]
  B --> C[Semantic scoring]
  C --> D[Shortlist]
  D --> E[Final LLM judge]
```

## What this example is
- A small public-safe version of the flagship scoring pipeline.
- Service-style files that are easy to copy into another project.
- A clean place to teach acronym handling such as `SOC 2`, `SSO`, and similar exact-term checks.

## What this example is not
- Not a full application shell.
- Not a framework demo.
- Not a vector-store example.

## File walkthrough order
1. `filters.py`
2. `matching.py`
3. `llm.py`
4. `sample_data/brief.json`
5. `sample_data/proposals.json`

## Why this shape comes first
This layout keeps the core lesson readable:
- use hard filters for required capabilities
- let embeddings recover meaning after that
- ask the LLM to compare only the best few proposals

The same idea also applies to skills filtering, acronym-heavy matching, and other exact-plus-semantic retrieval problems.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Pattern](https://img.shields.io/badge/Pattern-01%20Layered%20Pipeline-2563eb)](../../patterns/01-pre-filter-embed-llm-judge.md)
[![Next](https://img.shields.io/badge/Next-Bulk%20Proposal%20Scoring-2563eb)](../bulk-proposal-scoring/README.md)
