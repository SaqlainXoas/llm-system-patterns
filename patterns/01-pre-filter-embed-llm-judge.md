# Pattern 01: Pre-filter -> Embed -> Rerank -> LLM Judge

![Badge](https://img.shields.io/badge/Pattern-Flagship-2563eb) ![Badge](https://img.shields.io/badge/Goal-Narrow%20First-0f172a) ![Badge](https://img.shields.io/badge/LLM-Last-16a34a)

## Quick take
Do the cheap, reliable narrowing first. Ask the LLM to reason only after the candidate set is already small.

```mermaid
flowchart LR
  A[Candidate pool] --> B[Pre-filter]
  B --> C[Semantic or hybrid retrieval]
  C --> D[Optional rerank]
  D --> E[LLM judge]
```

## Why this pattern exists
Many systems start by asking one big model to search, compare, rank, and explain everything at once. That can work for a small demo, but it starts failing when the pool is large, some constraints are non-negotiable, abbreviations matter, or cost and latency finally become visible.

This pattern splits the work by job instead of by hype. Deterministic logic handles hard rules. Retrieval handles recall. Reranking handles precision. The LLM handles the final reasoning over a small, grounded shortlist.

| Stage | Job | Why it belongs there |
|---|---|---|
| `Pre-filter` | Remove clearly invalid candidates | Cheapest place to enforce hard constraints |
| `Semantic retrieval` | Recover meaning across different wording | Best stage for recall, not final judgment |
| `Rerank` | Clean up ordering inside the shortlist | Useful when retrieval is close but noisy |
| `LLM judge` | Compare the narrowed set and explain | Strongest when the context is bounded |

## How the flow works
Use `pre-filter` first for things that should never be fuzzy: required language, mandatory certifications, exact region, compliance tags, product family, or safe numeric thresholds. This stage is cheap, fast, and explainable, so it should absorb as much hard logic as possible.

Use `semantic retrieval` or `hybrid retrieval` after that to recover meaning across phrasing differences such as `software engineer` versus `backend developer` or `fraud prevention` versus `risk controls`. Retrieval is there to produce a good pool, not the final answer.

Add `rerank` only when the right answer is already in the retrieved set but the ordering is still weak. Then let the `LLM judge` compare only the narrowed shortlist against explicit criteria. At that point the model is no longer searching the universe; it is reading a well-shaped problem.

## Practical example
Document scoring is a clean fit for this pattern. Imagine scoring proposals against a requirements sheet, profiles against a role definition, or policy documents against a compliance checklist.

The weak version is: give everything to the LLM and ask it to choose. The stronger version is: filter hard mismatches, retrieve by meaning, rerank if top-k quality still feels soft, and ask the model to score only the final few candidates using evidence from the provided text.

That structure lowers cost, lowers latency, enforces hard rules deterministically, and makes debugging easier because you can inspect which stage failed.

## Implementation blueprint
For a resume-to-JD matcher or document scorer, think in four small functions:

```python
def pre_filter(items, query):
    return [
        item for item in items
        if item["country"] == query["country"]
        and query["must_have_skill"] in item["text"]
    ]

def retrieve(items, query_embedding, embed_fn, top_k=50):
    scored = []
    for item in items:
        score = cosine_similarity(query_embedding, embed_fn(item["text"]))
        scored.append((item, score))
    return [item for item, _ in sorted(scored, key=lambda x: x[1], reverse=True)[:top_k]]

def rerank(query_text, candidates, reranker_fn, top_k=10):
    scored = reranker_fn(query_text, [c["text"] for c in candidates])
    ranked = sorted(zip(candidates, scored), key=lambda x: x[1], reverse=True)
    return [item for item, _ in ranked[:top_k]]

def judge(shortlist, criteria, llm_fn):
    return llm_fn(shortlist=shortlist, criteria=criteria)
```

The point is not the exact library. The point is the sequence: hard checks first, semantic narrowing second, precision cleanup third, expensive reasoning last.

## What the stages usually look like
`metadata / regex filters` usually means country checks, exact skill names, explicit compliance tags, document type checks, or numeric thresholds that should not be left to the LLM.

`hybrid retrieval` usually means keyword top-k plus embedding top-k merged into one candidate set. This is especially useful when the system must respect abbreviations like `RN`, `SOC 2`, or `C++` but still recover paraphrases and related meaning.

`top-k narrowing` means setting a hard cap before the next expensive stage. For example, retrieve top 50, rerank top 20, then let the LLM judge only top 5. Those numbers are not magic. They are there to keep cost and noise bounded.

## Practical default
If you want a healthy default shape, start here:

```text
metadata / regex filters
-> hybrid retrieval
-> top-k narrowing
-> rerank top 20
-> LLM judge top 5
```

This is not universal, but it reflects the right instinct: deterministic first, semantic second, expensive reasoning last.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Decision](https://img.shields.io/badge/Decision-Hybrid%20vs%20Keyword-2563eb)](../decision-guides/embedding-vs-keyword-vs-hybrid.md)
[![Example](https://img.shields.io/badge/Example-Document%20Scoring-16a34a)](../examples/document-scoring-pipeline/README.md)
[![Next](https://img.shields.io/badge/Next-02%20Hybrid%20Search-2563eb)](02-hybrid-search-keyword-semantic.md)
