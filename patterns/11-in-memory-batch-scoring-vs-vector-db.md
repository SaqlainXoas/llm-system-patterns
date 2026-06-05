# Pattern 11: In-Memory Batch Scoring vs Vector DB

![Badge](https://img.shields.io/badge/Pattern-Storage%20Decision-2563eb) ![Badge](https://img.shields.io/badge/Goal-Right%20Persistence-0f172a) ![Badge](https://img.shields.io/badge/Default-Decide%20Late-16a34a)

## Quick take
Do not reach for a vector DB just because embeddings exist. First ask whether the work is a one-run batch job or a persistent retrieval system.

```mermaid
flowchart LR
  A[One-run batch] --> B[In-memory]
  C[Reusable corpus] --> D[Vector DB]
```

## Why this decision matters
This is one of the most common architecture mistakes in LLM systems. People build a vector store first, then discover the real task was just "score this batch now."

If the data arrives, gets scored against one active brief, and then can be discarded, in-memory scoring is often the cleaner design:
- no indexing layer to maintain
- no extra write path
- easier cleanup
- easier debugging

If the same content must be searched again tomorrow, shared across users, filtered repeatedly, or updated over time, a vector DB becomes much more reasonable.

## Decision table

| Situation | Better fit | Why |
|---|---|---|
| One batch of proposals against one active brief | `In-memory` | Simple, cheap, no persistence tax |
| Frequent reuse of the same corpus | `Vector DB` | You pay indexing once and query many times |
| Multi-user retrieval service | `Vector DB` | Shared storage and filtering matter |
| Temporary scoring job with strong pre-filters | `In-memory` | Less moving infrastructure |
| Local experimentation | `Chroma` | Lightweight local option |
| Hosted production retrieval | `Pinecone` | Persistent managed service |

## In-memory flow
This is the strong fit for bulk proposal scoring:

```text
accept upload
-> parse one batch only
-> dedupe and pre-filter
-> embed brief once
-> embed current batch
-> keep rolling top pool
-> rerank or judge shortlist
-> drop finished batch from memory
```

That flow matches one-run scoring very well because the embeddings are useful immediately and disposable afterward.

## Why this pattern is strong
The engineering win is not just "skip the vector DB." The real win is:
- you do not build storage you do not need
- you keep the active batch small
- you can clean up after each batch
- the final LLM only sees the strongest rows

## Vector DB flow
This is better when the retrieval layer has to live beyond one run:

```text
parse and chunk documents
-> generate embeddings
-> upsert vectors and metadata
-> query by vector or text
-> rerank the returned set
-> reuse the store across many requests
```

This is where services like Pinecone start making sense, and where a local store like Chroma is helpful for development or small local workflows.

## Engineering comparison

| Question | `In-memory batch` | `Vector DB` |
|---|---|---|
| Same batch, same run? | strong fit | usually overkill |
| Reuse the corpus tomorrow? | weak fit | strong fit |
| Multi-user search service? | weak fit | strong fit |
| Easy cleanup after run? | very strong | more infra to manage |
| Fast local experimentation? | strong | Chroma can also be good |

## Code shape
The decision becomes easier when you write it this way:

```python
def choose_storage_mode(job_shape):
    if job_shape["one_run_batch"] and not job_shape["needs_reuse"]:
        return "in_memory"

    if job_shape["multi_user"] or job_shape["needs_reuse"]:
        return "vector_db"

    return "in_memory"
```

This is not about perfect theory. It is about protecting the system from unnecessary infrastructure.

## Practical recommendation

| Start with `in-memory` when | Move to `vector DB` when |
|---|---|
| the brief changes per run | the corpus persists |
| the batch is bounded | retrieval becomes a shared service |
| the results do not need long-term search | metadata filtering and reuse matter more than one-run simplicity |

Once that persistent retrieval system exists, the next design question becomes: how should the retrieval itself behave? Pattern 13 picks up from there and shows why metadata filters should narrow the allowed set before vector ranking takes over.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-10%20Batch%20Calls-64748b)](10-batch-calls-and-throughput.md)
[![Example](https://img.shields.io/badge/Example-Vector%20Store%20Track-16a34a)](../examples/proposal-to-brief-with-vector-store/README.md)
[![Deep%20Dive](https://img.shields.io/badge/Deep%20Dive-13%20Metadata%20Filters-2563eb)](13-metadata-filters-before-vector-search.md)
[![Next](https://img.shields.io/badge/Next-12%20Cleanup%20and%20Memory-2563eb)](12-cache-cleanup-and-memory-control.md)
