# Pattern 12: Cache, Cleanup, and Memory Control

![Badge](https://img.shields.io/badge/Pattern-System%20Hygiene-2563eb) ![Badge](https://img.shields.io/badge/Goal-Keep%20Runs%20Light-0f172a) ![Badge](https://img.shields.io/badge/Rule-Drop%20What%20You%20Do%20Not%20Need-16a34a)

## Quick take
Caching and cleanup are not afterthoughts. They are part of the pipeline design, especially when the system processes large files or large batches.

```mermaid
flowchart LR
  A[Parse batch] --> B[Cache reusable signals]
  B --> C[Score current batch]
  C --> D[Trim shortlist]
  D --> E[Drop temp data]
  E --> F[Move to next batch]
```

## What should usually be cached
Cache the things that repeat inside the same run:
- the brief embedding
- normalized keyword lists
- parsed metadata you will reuse across batches
- duplicate-file hashes

Do not cache everything blindly. If a value is large, rarely reused, or specific to one finished batch, cleanup is often better than caching.

## What should usually be cleaned up
Clean up the things that stop helping after a stage finishes:
- raw extracted text from discarded proposals
- embeddings for rows that did not survive the shortlist
- temporary files created during extraction
- large prompt payloads once the LLM result is saved

That is the difference between a flow that feels steady and one that slowly inflates during the run.

| Keep it | Drop it |
|---|---|
| brief embedding reused across all batches | raw text from discarded rows |
| shortlist rows still alive | embeddings for rows that lost early |
| duplicate hashes for the active run | temporary extraction directories |
| normalized metadata needed downstream | oversized prompt payloads after scoring |

## Code shape
Keep the cleanup points explicit:

```python
def process_batches(brief, proposal_batches, embed_text):
    brief_vector = embed_text(brief["summary"])
    shortlist = []

    for batch in proposal_batches:
        batch_rows = score_one_batch(brief, batch, brief_vector)
        shortlist.extend(batch_rows)
        shortlist.sort(key=lambda row: row["score"], reverse=True)
        shortlist = shortlist[:40]

        del batch_rows
        del batch

    return shortlist[:10]
```

This is intentionally plain. The point is to show that cleanup belongs in the flow, not in a forgotten TODO.

## Engineering instinct
Use cleanup as part of the design rhythm:

```text
extract current batch
-> normalize only needed fields
-> score and trim early
-> keep shortlist only
-> free finished batch
-> move forward
```

## Why this matters for extracted files
If the batch starts from PDFs or uploads, cleanup also means:
- delete temp extraction directories
- keep only the normalized fields the next stage needs
- avoid carrying entire file contents into the final prompt unless necessary

The system gets cheaper and easier to reason about when each stage hands forward only the minimum useful shape.

## Practical default
Use this instinct:

```text
cache reused signals
-> trim early
-> keep a bounded shortlist
-> drop stale intermediates
-> move to the next batch
```

That is not just performance tuning. It is part of building a pipeline that stays predictable under load.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-11%20In--Memory%20vs%20Vector%20DB-64748b)](11-in-memory-batch-scoring-vs-vector-db.md)
[![Example](https://img.shields.io/badge/Example-Bulk%20Proposal%20Scoring-16a34a)](../examples/bulk-proposal-scoring/README.md)
