# RAG Without Frameworks

![Badge](https://img.shields.io/badge/Example-RAG%20Without%20Frameworks-2563eb) ![Badge](https://img.shields.io/badge/Style-Plain%20Python-0f172a)

## Quick take
This example is a minimal retrieval pipeline built with plain Python and direct API usage rather than heavy orchestration tooling.

```mermaid
flowchart LR
  A[Question] --> B[Retrieve]
  B --> C[Select evidence]
  C --> D[Grounded prompt]
  D --> E[Answer]
```

## What this example is for
The focus is lightweight setup, direct retrieval steps, grounded prompting, and evaluation basics. It is the repo's "show the moving parts clearly" track for readers who want the system without a framework layer.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Pattern](https://img.shields.io/badge/Pattern-01%20Layered%20Pipeline-2563eb)](../../patterns/01-pre-filter-embed-llm-judge.md)
