# Decision Guide: RAG vs Fine-Tuning

![Badge](https://img.shields.io/badge/Guide-RAG%20vs%20Fine--Tuning-2563eb)

## Quick take
Prefer retrieval when the challenge is fresh or changing knowledge. Consider fine-tuning when the challenge is behavior, structure, or repeated task style rather than missing information.

```mermaid
flowchart TD
  A[What is broken?] --> B{Knowledge freshness?}
  B -->|Yes| C[RAG]
  B -->|No| D{Behavior or output style?}
  D -->|Yes| E[Fine-tuning]
  D -->|Both| F[Separate the two jobs]
```

## Why this matters
RAG solves the knowledge access problem. Fine-tuning solves the model behavior problem. Confusing the two usually leads to expensive systems that still do not address the real failure mode.

This guide will expand into clearer case splits, but the high-level rule is simple: do not fine-tune to memorize changing facts, and do not add retrieval when the real problem is stable task behavior or output format.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Pattern](https://img.shields.io/badge/Pattern-01%20Layered%20Pipeline-2563eb)](../patterns/01-pre-filter-embed-llm-judge.md)
