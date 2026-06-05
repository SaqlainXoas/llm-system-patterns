# RAG Without Frameworks

![Badge](https://img.shields.io/badge/Example-RAG%20Without%20Frameworks-2563eb) ![Badge](https://img.shields.io/badge/Style-Plain%20Python-0f172a) ![Badge](https://img.shields.io/badge/Progress-6%2F6-0f172a)

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

## File walkthrough order
1. `retrieval.py`
2. `llm.py`
3. `sample_data/question.json`
4. `sample_data/knowledge_base.json`

## What the code teaches
- how to chunk and score evidence without a framework
- how to keep only the top evidence window
- how to build a grounded prompt
- where small retrieval caches and cleanup points belong

## Flow shape
```text
chunk knowledge
-> score chunks
-> keep top evidence
-> build grounded prompt
-> answer from evidence only
```

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Cookbook](https://img.shields.io/badge/Cookbook-Examples-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-Hybrid%20Search%20Pipeline-64748b)](../hybrid-search-pipeline/README.md)
[![Pattern](https://img.shields.io/badge/Pattern-01%20Layered%20Pipeline-2563eb)](../../patterns/01-pre-filter-embed-llm-judge.md)
