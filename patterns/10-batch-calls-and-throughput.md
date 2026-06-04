# Pattern 10: Batch Calls and Throughput

![Badge](https://img.shields.io/badge/Pattern-Throughput-2563eb) ![Badge](https://img.shields.io/badge/Goal-Keep%20Jobs%20Moving-0f172a) ![Badge](https://img.shields.io/badge/Scale-Bulk%20Scoring-16a34a)

## Quick take
When the workload is large, the right question is not "can this score one document?" It is "can this score the whole batch without stalling the user or blowing up memory?"

```mermaid
flowchart LR
  A[Upload batch] --> B[Background worker]
  B --> C[Extract and pre-filter]
  C --> D[Embed one batch]
  D --> E[Keep top pool]
  E --> F[LLM on shortlist]
  F --> G[Webhook or stored result]
```

## Why batching matters
Single-item demos hide the real bottlenecks. Bulk scoring exposes them immediately:
- extraction gets expensive
- embeddings become repetitive
- the shortlist keeps growing unless you cap it
- long requests make the user wait too long

That is why bulk flows usually need a worker shape. Let the request create a job, let a background worker process batches, and return the final results through polling, stored status, or a webhook callback.

| If you keep it synchronous | What goes wrong |
|---|---|
| file batch is large | user waits too long |
| embeddings are slow | request thread stays blocked |
| final LLM stage is late | timeout pressure grows |
| many users upload at once | throughput collapses faster |

## A healthy worker shape
For proposal scoring, a practical first worker shape is:

```text
accept batch
-> hand work to Celery or another worker
-> extract one batch
-> pre-filter hard mismatches
-> embed only the current batch
-> keep a rolling top pool
-> run final LLM validation on the best few
-> save result and notify caller
```

This keeps the web layer responsive and stops one long scoring job from blocking everything else.

## What the stages usually mean
`background worker` means Celery, a queue consumer, or another async worker process. The point is not the tool name. The point is that long scoring jobs should not sit inside the request thread.

`embed one batch` means process a bounded chunk, score it, keep what matters, and move on. Do not keep every intermediate vector if the job is one-shot.

`keep a rolling top pool` means you do not need every document after scoring. If your final rerank window is 20, you may only need to retain the strongest 50 or 100 rows while later batches continue.

## Engineering rhythm

```text
queue job
-> open current batch only
-> score and trim
-> keep shortlist alive
-> release finished batch
-> continue
```

## Code shape
Keep the batch logic obvious:

```python
def process_batch_job(brief, proposals, embed_text):
    query_vector = embed_text(brief["summary"])
    best_rows = []

    for batch in chunked(proposals, size=25):
        filtered_batch = pre_filter_batch(brief, batch)
        scored_rows = score_one_batch(brief, filtered_batch, query_vector)
        best_rows.extend(scored_rows)
        best_rows.sort(key=lambda row: row["score"], reverse=True)
        best_rows = best_rows[:50]

    return best_rows[:10]
```

The exact numbers can change. The important part is the rhythm: batch, score, trim, continue.

## Why webhooks come up here
If the backend is separate from the UI, a webhook or stored-job result is often cleaner than making the caller wait. The user submits work once, your system processes it in the background, and the final result arrives when the job is complete.

That design is usually better than a giant synchronous request when:
- file extraction is slow
- the LLM stage is late in the pipeline
- many users may submit jobs at once

## Practical default

| Stage | Healthy default |
|---|---|
| request layer | queue the job |
| worker | process one batch at a time |
| scoring | keep only the rolling top pool |
| final step | let the LLM see the shortlist only |

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Prev](https://img.shields.io/badge/Prev-09%20Embeddings-64748b)](09-embedding-model-selection.md)
[![Example](https://img.shields.io/badge/Example-Bulk%20Proposal%20Scoring-16a34a)](../examples/bulk-proposal-scoring/README.md)
[![Next](https://img.shields.io/badge/Next-11%20In--Memory%20vs%20Vector%20DB-2563eb)](11-in-memory-batch-scoring-vs-vector-db.md)
