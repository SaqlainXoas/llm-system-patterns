# Document Scoring Pipeline

![Badge](https://img.shields.io/badge/Example-Flagship%20Build-2563eb) ![Badge](https://img.shields.io/badge/Style-Plain%20Python-0f172a) ![Badge](https://img.shields.io/badge/Goal-Layered%20Scoring-16a34a)

## Quick take
This is the first end-to-end build path for the repo. It shows how to score documents with a layered system instead of an LLM-first shortcut.

```mermaid
flowchart LR
  A[Load documents] --> B[Normalize fields]
  B --> C[Deterministic pre-checks]
  C --> D[Retrieval]
  D --> E[Optional rerank]
  E --> F[Grounded scoring]
```

## Why this example comes first
Document scoring naturally contains exact constraints, semantic similarity, ordering problems, cost tradeoffs, and grounded evaluation needs. That makes it the cleanest place to turn the repo's core philosophy into code.

The point is not to showcase a framework. The point is to show system shape and engineering judgment in a form that readers can follow stage by stage.

## What this build will teach
The implementation path is intentionally simple: load and normalize documents, remove obvious hard mismatches, retrieve the most relevant candidates, optionally rerank if the ordering is still soft, and ask the model to score only the final shortlist against explicit criteria.

When the code lands, readers should be able to inspect what got filtered out, what got retrieved, whether reranking helped, what evidence the final score used, and where cost or latency concentrate.

## Planned repo shape

```text
examples/document-scoring-pipeline/
├── README.md
├── app.py
├── scorer.py
├── retrieval.py
├── filters.py
├── prompts.py
└── sample_data/
```

The first version should stay plain: small sample data, explicit stage outputs, and no premature framework dependency.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Pattern](https://img.shields.io/badge/Pattern-01%20Layered%20Pipeline-2563eb)](../../patterns/01-pre-filter-embed-llm-judge.md)
[![Next](https://img.shields.io/badge/Next-Scaled%20Document%20Scoring-2563eb)](../scaled-document-scoring/README.md)
