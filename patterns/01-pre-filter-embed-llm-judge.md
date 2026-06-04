# Pattern 01: Pre-filter -> Embed -> Rerank -> LLM Judge

This flagship pattern shows how to narrow the search space before asking an LLM to score or judge anything.

## What This Pattern Will Cover

- Why all-in-one prompting is expensive and unreliable
- Where deterministic filters should run first
- How embeddings widen recall after hard pruning
- When reranking improves precision before final judgment
- How to keep LLM reasoning grounded in a narrowed candidate set

## Planned Example

The first example will use a document scoring pipeline that moves from hard constraints to semantic retrieval and ends with a final grounded scoring step.
