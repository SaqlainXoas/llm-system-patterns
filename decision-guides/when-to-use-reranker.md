# Decision Guide: When to Use a Reranker

Use this guide when retrieval is already "close" and you are deciding whether an extra precision layer is worth adding.

Short version:

- add a reranker when recall is decent but ordering is weak
- skip it when the candidate set is already small and clean
- do not use reranking to hide a broken retrieval stage

## Fast Decision Table

| Situation | Recommendation | Why |
|---|---|---|
| The right answer is usually in the retrieved set, but not near the top | Use a reranker | This is the classic reranker case |
| Retrieval results are already well ordered | Skip it | Extra cost with little gain |
| The candidate set is tiny | Usually skip it | There may be nothing meaningful to rerank |
| A downstream LLM step is too expensive on noisy top-k | Use a reranker | Better ordering can shrink the LLM workload |
| Retrieval often misses the right item entirely | Fix retrieval first | Reranking cannot recover missing candidates |

## The Core Question

Do not ask:

> Are rerankers more accurate?

They often are.

Ask:

> Is the precision gain worth the extra stage in this pipeline?

That is the real decision.

## Use a Reranker When

### 1. Retrieval recall is decent

The right item is usually somewhere in the retrieved set.

### 2. Ordering quality is the weak point

You are getting relevant candidates, but the best ones are buried among near-matches.

### 3. Top-k quality matters

This matters a lot when:

- only a few results are shown to users
- only a few chunks fit into context
- only a few candidates should reach the LLM judge stage

### 4. The candidate pool is still large after retrieval

If you retrieve top 30 or top 50 and need to narrow to the best 5, reranking can be very valuable.

## Skip a Reranker When

### 1. The retrieved set is already small and strong

If the top 5 is already clearly correct, reranking may add little.

### 2. Latency budget is extremely tight

Some systems care more about speed than small ranking gains.

### 3. Exact ordering is not very important

If downstream logic only needs a broad relevant pool, retrieval may be enough.

### 4. Retrieval quality is still fundamentally weak

Do not pay for ranking polish before fixing recall problems.

## Signs Retrieval Needs Work First

Fix retrieval first if:

- the correct item is often absent
- exact constraints are not being enforced
- abbreviations or IDs are being missed
- the semantic retrieval stage is too broad or poorly scoped

Rerankers improve order inside the candidate set.
They do not fix candidate generation failures.

## Strong Practical Use Cases

Rerankers are especially helpful in:

- search systems where the first few results matter most
- hybrid retrieval pipelines
- document or profile matching
- RAG systems with tight context budgets
- LLM-as-judge pipelines where top-k must be clean before final reasoning

## Cost and Latency Tradeoff

Rerankers add cost and latency, but that does not automatically make them a bad trade.

They can still reduce total pipeline cost if they help you:

- shrink the set passed into an LLM
- reduce prompt size
- improve precision enough to avoid repeated retries or follow-up search

The right comparison is total pipeline effect, not single-stage cost.

## A Good Default

If you suspect you need one, try:

```text
retrieve top 30-50
-> rerank
-> keep top 5-10
```

That structure is often strong enough to improve quality without making the system heavy.

## Takeaway

Use a reranker when retrieval gets you close, but not close enough.

If retrieval is already strong, skip it.
If retrieval is broken, fix that first.
