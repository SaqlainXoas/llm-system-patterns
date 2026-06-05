# Metadata-Filtered Vector Search

![Badge](https://img.shields.io/badge/Example-Filter--First%20Retrieval-2563eb) ![Badge](https://img.shields.io/badge/Store-Local%20Chroma-0f172a) ![Badge](https://img.shields.io/badge/Goal-Hard%20Filters%20Before%20Ranking-16a34a) ![Badge](https://img.shields.io/badge/Progress-4%2F6-0f172a)

## Goal
Learn the clean filter-first retrieval shape used in persistent vector systems:
1. narrow the allowed document set with metadata
2. rank only that allowed set by similarity
3. avoid trusting top-k from the full index

The main idea is simple: do not run broad semantic search across your whole knowledge base or vector database if the answer must already come from a smaller allowed subset.

## Flow
```mermaid
flowchart LR
  A[Query] --> B[Metadata filter]
  B --> C[Allowed documents]
  C --> D[Similarity ranking]
  D --> E[Best valid matches]
```

## What this example shows
- a real vector retrieval flow
- one query across all documents
- the same query with a metadata filter
- why semantically similar but invalid documents can pollute top-k
- what to do when the filter returns zero documents

## Real retrieval flow
This is the production-shaped lesson behind the example:

```text
ingest documents
-> store each document with metadata
-> run a query across the collection
-> run the same query again with hard metadata filters
-> compare the returned top-k
-> handle the zero-match case safely
```

The important design rule is:
- metadata filters decide the allowed slice
- vector similarity ranks inside that slice

That is true no matter which vector database you use.

In other words:
- do not search the whole knowledge base first
- narrow the pool with metadata
- then let semantic search rank only inside that narrowed pool

## Generic query shape
Most vector stores end up looking roughly like this:

```python
vector_store.add(
    ids=[...],
    documents=[...],
    metadatas=[...],
)

naive_results = vector_store.query(
    query_text="What is the refund policy for delayed delivery?",
    top_k=3,
)

filtered_results = vector_store.query(
    query_text="What is the refund policy for delayed delivery?",
    top_k=3,
    filter={
        "region": "US",
        "document_type": "policy",
        "status": "published",
    },
)
```

The repo code uses a local store so the flow is runnable, but the retrieval pattern is meant to transfer to any vector DB with metadata filtering.

## Demo query and filters
Query:

```text
What is the refund policy for delayed delivery?
```

Metadata filter:

```python
{
    "region": "US",
    "document_type": "policy",
    "status": "published",
}
```

## How to run

```bash
pip install chromadb
python3 main.py
```

On first run, Chroma may download its default embedding model locally.

## What to look for in the output
- The naive query includes wrong-region, draft, or wrong-type documents because they use very similar language.
- The filtered query keeps only published US policy documents in the race.
- The zero-result example shows the safer fallback when no document matches the filter.

## File walkthrough order
1. `main.py`

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../../README.md)
[![Cookbook](https://img.shields.io/badge/Cookbook-Examples-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-Vector%20Store%20Track-64748b)](../proposal-to-brief-with-vector-store/README.md)
[![Pattern](https://img.shields.io/badge/Pattern-13%20Metadata%20Filters%20Before%20Vector%20Search-2563eb)](../../patterns/13-metadata-filters-before-vector-search.md)
[![Next](https://img.shields.io/badge/Next-Hybrid%20Search%20Pipeline-2563eb)](../hybrid-search-pipeline/README.md)
