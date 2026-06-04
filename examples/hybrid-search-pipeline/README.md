# Hybrid Search Pipeline

![Badge](https://img.shields.io/badge/Example-Hybrid%20Retrieval-2563eb) ![Badge](https://img.shields.io/badge/Style-Framework--light-0f172a) ![Badge](https://img.shields.io/badge/Progress-4%2F5-0f172a)

## Quick take
This example combines exact matching and semantic retrieval in a clean implementation without hiding the retrieval logic inside heavy abstractions.

```mermaid
flowchart LR
  A[Query] --> B[Keyword search]
  A --> C[Semantic retrieval]
  B --> D[Merge]
  C --> D
  D --> E[Optional rerank]
```

## What this example is for
The focus here is keyword signals, semantic retrieval, score merging, and failure-case analysis. It will be the concrete companion to the hybrid retrieval docs so readers can see how lexical and semantic signals cooperate in code.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Cookbook](https://img.shields.io/badge/Cookbook-Examples-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-Vector%20Store%20Track-64748b)](../proposal-to-brief-with-vector-store/README.md)
[![Pattern](https://img.shields.io/badge/Pattern-02%20Hybrid%20Search-2563eb)](../../patterns/02-hybrid-search-keyword-semantic.md)
[![Next](https://img.shields.io/badge/Next-RAG%20Without%20Frameworks-2563eb)](../rag-without-frameworks/README.md)
