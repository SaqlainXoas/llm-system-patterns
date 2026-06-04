# LLM System Patterns

<p align="center">
  <img src="assets/llm_system_mascot.svg" alt="Pipeline bot mascot holding a filter funnel" width="170">
</p>

> Practical patterns for building reliable LLM systems with retrieval, ranking, scoring, guardrails, and production-minded engineering tradeoffs.

<p align="center">
  <img src="assets/svg/llm_system_hero_v4_fixed.svg" alt="LLM system pipeline diagram showing deterministic filters, retrieval, reranking, and final LLM judgment" width="980">
</p>

## Why This Repo Exists

Most LLM projects look simple at the start: send a prompt, get an answer, and hope it behaves well enough in production.

Real systems are not that simple.

Reliable LLM applications usually need layers:

- deterministic filters for hard constraints
- keyword and semantic retrieval for recall
- reranking for precision
- grounded LLM reasoning only after the candidate set is narrow
- cost, latency, and evaluation thinking from the beginning

This repository is being built as a practical engineering playbook for those layers.

## What You Will Learn

- When keyword search beats embeddings
- When embeddings help and where they fail
- Why hybrid retrieval is often the better default
- When a reranker is worth the extra cost
- How to use LLMs late in the pipeline instead of first
- How to think about batching, caching, latency, and reliability together

## Who This Is For

- Engineers building LLM applications beyond basic prompting
- Learners moving from demos to production-minded system design
- Developers comparing retrieval, reranking, and LLM scoring choices
- Reviewers who want to see applied GenAI engineering judgment, not only API usage

## Repo Philosophy

This repo is not a framework showcase and not a random collection of notes.

It is meant to teach one core idea clearly:

> Build the system in layers. Use deterministic logic where it is strongest, use semantic methods where they help, add precision controls before expensive reasoning, and optimize only after the pipeline is sound.

## Start Here

1. Read [Pattern 01](patterns/01-pre-filter-embed-llm-judge.md) to understand the flagship multi-stage pipeline.
2. Read [Embedding vs Keyword vs Hybrid](decision-guides/embedding-vs-keyword-vs-hybrid.md) for the core retrieval decision.
3. Read [Reranker: When and Why](patterns/04-reranker-when-and-why.md) to understand precision tradeoffs.
4. Explore [Document Scoring Pipeline](examples/document-scoring-pipeline/README.md) for the first end-to-end example direction.

For orchestration-heavy agent workflows, see [langgraph-design-patterns](https://github.com/SaqlainXoas/langgraph-design-patterns).

## Learning Path

### Core Patterns

- [01. Pre-filter -> Embed -> Rerank -> LLM Judge](patterns/01-pre-filter-embed-llm-judge.md)
- [02. Hybrid Search: Keyword + Semantic](patterns/02-hybrid-search-keyword-semantic.md)
- [03. The Abbreviation and Short-Token Problem](patterns/03-abbreviation-short-token-problem.md)
- [04. Reranker: When and Why](patterns/04-reranker-when-and-why.md)
- [05. Chunking Strategies](patterns/05-chunking-strategies.md)
- [06. Prompt Injection Defense](patterns/06-prompt-injection-defense.md)
- [07. Cost and Latency Budgeting](patterns/07-cost-latency-budgeting.md)
- [08. LLM-as-Judge Reliability](patterns/08-llm-as-judge-reliability.md)
- [09. Embedding Model Selection](patterns/09-embedding-model-selection.md)

### Decision Guides

- [Embedding vs Keyword vs Hybrid](decision-guides/embedding-vs-keyword-vs-hybrid.md)
- [When to Use a Reranker](decision-guides/when-to-use-reranker.md)
- [When to Use LLM-as-Judge](decision-guides/when-to-use-llm-as-judge.md)
- [RAG vs Fine-Tuning](decision-guides/rag-vs-fine-tuning.md)

### Example Tracks

- [Document Scoring Pipeline](examples/document-scoring-pipeline/README.md)
- [Scaled Document Scoring](examples/scaled-document-scoring/README.md)
- [Hybrid Search Pipeline](examples/hybrid-search-pipeline/README.md)
- [RAG Without Frameworks](examples/rag-without-frameworks/README.md)

## Initial Structure

```text
llm-system-patterns/
├── README.md
├── patterns/
├── decision-guides/
├── examples/
│   ├── document-scoring-pipeline/
│   ├── scaled-document-scoring/
│   ├── hybrid-search-pipeline/
│   └── rag-without-frameworks/
└── assets/
    ├── diagrams/
    └── svg/
```

## Relationship to the Other Repos

This project sits beside two related repositories with a different job:

- `langgraph-design-patterns`: orchestration, routing, memory, workflow control, human review loops
- `ai-research-notes`: papers, ideas, experiments, and concept-first research summaries
- `llm-system-patterns`: retrieval, ranking, scoring, reliability, and production-minded system tradeoffs

Together, they form a cleaner map from concepts to systems to orchestration.

## Current Status

The repo now has a strong first phase in place:

- repo identity and scope are defined
- the hero visuals are in place
- the first flagship pattern docs are now drafted
- the first decision and example paths are now shaped around a real layered pipeline

The next phase is to expand the remaining guides and start the first plain-Python example implementation.
