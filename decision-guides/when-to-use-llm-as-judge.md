# Decision Guide: When to Use LLM-as-Judge

![Badge](https://img.shields.io/badge/Guide-LLM%20as%20Judge-2563eb) ![Badge](https://img.shields.io/badge/Rule-Use%20Late-16a34a)

## Quick take
Use LLM judgment after narrowing and grounding. Avoid it as the first or only decision layer, and prefer deterministic logic when the rule is exact and non-negotiable.

```mermaid
flowchart LR
  A[Hard filters] --> B[Retrieval or hybrid]
  B --> C[Optional rerank]
  C --> D[LLM judge on shortlist]
```

| Situation | Recommendation | Why |
|---|---|---|
| Nuanced comparison across a small shortlist | `Use LLM-as-judge` | This is where model reasoning adds value |
| Exact binary rule | `Use deterministic logic` | Cheaper and more reliable |
| Candidate set is still large | `Narrow first` | Full-scale LLM judgment is expensive and noisy |
| Grounded explanation with evidence is needed | `Use LLM-as-judge after narrowing` | The model can compare and explain if context is controlled |

## How to decide quickly
Do not ask whether an LLM can judge the task. Ask whether nuanced model reasoning is actually needed, or whether the system can decide with cheaper, more stable logic.

LLM judgment is strong when the task is comparative, the shortlist is already narrow, the criteria are explicit, and the evidence is actually in the prompt. It is weak when you want the model to search and judge at the same time, enforce hard rules, or behave with near-perfect consistency across uncontrolled contexts.

## Practical default
If you need nuanced final scoring, use this shape:

```text
hard filters
-> retrieval or hybrid retrieval
-> top-k narrowing
-> optional rerank
-> LLM judge on the final shortlist
```

That keeps the value of model reasoning without letting it take over the whole pipeline.

---
[![Home](https://img.shields.io/badge/Home-README-0f172a)](../README.md)
[![Pattern](https://img.shields.io/badge/Pattern-01%20Layered%20Pipeline-2563eb)](../patterns/01-pre-filter-embed-llm-judge.md)
[![Prev](https://img.shields.io/badge/Prev-Use%20a%20Reranker-64748b)](when-to-use-reranker.md)
