# LLM System Patterns

<p align="center">
  <img alt="Docs: Markdown-first" src="https://img.shields.io/badge/Docs-Markdown--first-0f172a?logo=markdown&logoColor=fff" />
  <img alt="Focus: Retrieval and ranking" src="https://img.shields.io/badge/Focus-Retrieval%20%2B%20Ranking-2563eb" />
  <img alt="Approach: Layered systems" src="https://img.shields.io/badge/Approach-Layered%20Systems-0891b2" />
  <img alt="Status: Phase 1 drafted" src="https://img.shields.io/badge/Status-Phase%201%20Drafted-16a34a" />
</p>

<p align="center">
  <img src="assets/llm_system_mascot.svg" alt="Pipeline bot mascot holding a filter funnel" width="170">
</p>

> Practical patterns for building reliable LLM systems with retrieval, ranking, scoring, guardrails, and production-minded engineering tradeoffs.

<p align="center">
  <img src="assets/svg/llm_system_hero_v4_fixed.svg" alt="LLM system pipeline diagram showing deterministic filters, retrieval, reranking, and final LLM judgment" width="980">
</p>

## What You'll Learn Fast

- When keyword search beats embeddings
- When embeddings help and where they fail
- Why hybrid retrieval is often the safer default
- When reranking is worth the extra stage
- Why LLM judgment belongs late, not first
- How cost, latency, and evaluation shape the architecture itself

## System Map

```mermaid
flowchart LR
  A[Corpus or candidates] --> B[Hard filters]
  B --> C[Keyword and semantic retrieval]
  C --> D[Top-k narrowing]
  D --> E[Optional rerank]
  E --> F[LLM judge or grounded answer]
```

Most LLM projects start with "send everything to the model." This repo is the opposite instinct: narrow first, reason last, and keep each stage honest about what it is good at.

## Start Here

1. [Pattern 01](patterns/01-pre-filter-embed-llm-judge.md) for the flagship layered pipeline.
2. [Embedding vs Keyword vs Hybrid](decision-guides/embedding-vs-keyword-vs-hybrid.md) for the retrieval decision.
3. [Pattern 04](patterns/04-reranker-when-and-why.md) for precision tradeoffs.
4. [Document Scoring Pipeline](examples/document-scoring-pipeline/README.md) for the first end-to-end build path.

For orchestration-heavy agent workflows, see [langgraph-design-patterns](https://github.com/SaqlainXoas/langgraph-design-patterns).

## Read By Job

| If you need | Start here | Then follow with |
|---|---|---|
| A full layered mental model | [Pattern 01](patterns/01-pre-filter-embed-llm-judge.md) | [Pattern 04](patterns/04-reranker-when-and-why.md) |
| Retrieval choice help | [Embedding vs Keyword vs Hybrid](decision-guides/embedding-vs-keyword-vs-hybrid.md) | [Pattern 02](patterns/02-hybrid-search-keyword-semantic.md) |
| Better top-k quality | [When to Use a Reranker](decision-guides/when-to-use-reranker.md) | [Pattern 04](patterns/04-reranker-when-and-why.md) |
| Final LLM scoring guidance | [When to Use LLM-as-Judge](decision-guides/when-to-use-llm-as-judge.md) | [Pattern 01](patterns/01-pre-filter-embed-llm-judge.md) |
| A practical build path | [Document Scoring Pipeline](examples/document-scoring-pipeline/README.md) | [Scaled Document Scoring](examples/scaled-document-scoring/README.md) |

## Pattern Map

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

## Repo Family

- `langgraph-design-patterns`: orchestration, routing, memory, workflow control, human review loops
- `ai-research-notes`: papers, ideas, experiments, and concept-first research summaries
- `llm-system-patterns`: retrieval, ranking, scoring, reliability, and production-minded system tradeoffs

Together they form a cleaner path from concept to system shape to orchestration.

## Current Status

The repo now has:

- a stable identity and visual system
- the flagship retrieval and ranking docs in place
- decision guides that point readers to the right pattern faster
- example tracks shaped around real implementation paths

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

The next phase is to expand the remaining pages and start the first plain-Python implementation track.
