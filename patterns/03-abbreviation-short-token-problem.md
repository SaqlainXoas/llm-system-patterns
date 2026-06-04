# Pattern 03: The Abbreviation and Short-Token Problem

![Badge](https://img.shields.io/badge/Pattern-Lexical%20Edge%20Cases-2563eb) ![Badge](https://img.shields.io/badge/Risk-Short%20Tokens-0f172a)

## Quick take
Short tokens, acronyms, IDs, and domain abbreviations are common failure cases for semantic matching. If missing a tiny token makes the result unacceptable, embeddings alone are usually the wrong trust layer.

```mermaid
flowchart LR
  A[Short token: SOC 2 / S3 / RN] --> B[Exact lexical support]
  B --> C[Hybrid retrieval]
  C --> D[Safer candidate set]
```

## Why this matters
Embedding systems are built to capture broader meaning, which is exactly why they can weaken or blur tiny but critical signals. A short acronym may carry all the business truth, but the vector signal may treat it as a faint hint instead of a hard requirement.

That is why dictionaries, exact matching, metadata checks, or keyword support still matter. Hybrid retrieval is often the repair layer because it keeps semantic flexibility without dropping the exact lexical anchor.

## Where to use it
This pattern matters in compliance, skills matching, technical search, regulated domains, and any workflow where codes, versions, acronyms, or required skill names must not be missed.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-02%20Hybrid%20Search-64748b)](02-hybrid-search-keyword-semantic.md)
[![Decision](https://img.shields.io/badge/Decision-Hybrid%20vs%20Keyword-2563eb)](../decision-guides/embedding-vs-keyword-vs-hybrid.md)
[![Next](https://img.shields.io/badge/Next-04%20Reranker-2563eb)](04-reranker-when-and-why.md)
