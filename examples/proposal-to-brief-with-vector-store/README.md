# Proposal to Brief with Vector Store

![Badge](https://img.shields.io/badge/Example-Persistent%20Retrieval-2563eb) ![Badge](https://img.shields.io/badge/Focus-Pinecone%20and%20Chroma-0f172a) ![Badge](https://img.shields.io/badge/Goal-Know%20When%20Persistence%20Wins-16a34a) ![Badge](https://img.shields.io/badge/Progress-3%2F6-0f172a)

## Goal
Learn the persistent-store version of the same retrieval problem:
1. store reusable proposal vectors
2. query by brief
3. rerank and judge the returned set

## Flow
```mermaid
flowchart LR
  A[Reusable proposal corpus] --> B[Vector store]
  B --> C[Metadata filter]
  C --> D[Vector query]
  D --> E[Optional hosted rerank]
  E --> F[Final LLM judge]
```

## What this example is
- A light scaffold for persistent retrieval.
- A place to compare Pinecone with a local Chroma setup.
- A companion to the in-memory batch example, not a replacement for it.

## File walkthrough order
1. `vector_store.py`
2. `matching.py`
3. `llm.py`
4. `sample_data/brief.json`
5. `sample_data/proposals.json`

## Why this example exists
This track answers a different question than bulk scoring:
- not "score this one batch now"
- but "store reusable proposal vectors and search them repeatedly"

That is the point where a persistent vector layer becomes worth discussing.

If you want the cleanest example of metadata filters narrowing the search space before similarity ranking, see [Metadata-Filtered Vector Search](../metadata-filtered-vector-search/README.md). That example stays local and focuses on the filter-first retrieval pattern itself.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Cookbook](https://img.shields.io/badge/Cookbook-Examples-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-Bulk%20Proposal%20Scoring-64748b)](../bulk-proposal-scoring/README.md)
[![Pattern](https://img.shields.io/badge/Pattern-11%20In--Memory%20vs%20Vector%20DB-2563eb)](../../patterns/11-in-memory-batch-scoring-vs-vector-db.md)
[![Pattern](https://img.shields.io/badge/Pattern-13%20Metadata%20Filters%20Before%20Vector%20Search-2563eb)](../../patterns/13-metadata-filters-before-vector-search.md)
[![Next](https://img.shields.io/badge/Next-Metadata--Filtered%20Vector%20Search-2563eb)](../metadata-filtered-vector-search/README.md)
