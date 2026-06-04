# Pattern 04: Reranker, When and Why

Rerankers are the precision layer that sits between retrieval and final decision-making.

They are useful when the right candidates are already being retrieved, but the ordering is not strong enough.

## What a Reranker Actually Does

Retrieval answers:

> Which items are probably relevant enough to consider?

Reranking answers:

> Among these candidates, which ones are most relevant in this exact query context?

That distinction matters.

Retrieval is usually optimized for recall.
Reranking is usually added for precision.

## Why Retrieval Alone Often Is Not Enough

Even good retrieval systems often have this pattern:

- the right answer is somewhere in the top 20 or top 50
- the order within that set is noisy
- near-matches and true matches are mixed together

That is often good enough for a reranker to help a lot.

It is not yet good enough for:

- a final user-facing ranking
- grounded LLM judging
- strict top-k downstream processing

## When a Reranker Helps Most

Use a reranker when:

- retrieval has decent recall but weak ordering
- semantically similar candidates need finer separation
- you only want the best few items passed downstream
- top-k quality matters more than raw recall

Typical examples:

- search results where the first 3 items matter more than the next 30
- candidate shortlisting before LLM judgment
- document matching where several near-matches look similar in embedding space
- RAG pipelines where context budget is limited

## When a Reranker Is Probably Not Worth It

Skip it when:

- the candidate set is already tiny
- the retrieval ranking is already strong enough
- latency or cost budget is very tight
- the downstream task does not care much about exact ordering

If your top 5 is already clean, adding a reranker may only add system weight.

## Reranker vs Embedding Similarity

A common confusion is treating reranking as just "better embeddings."

That is not quite the right mental model.

Embedding retrieval usually compresses query and candidate meaning into vector space for broad matching.

Rerankers usually evaluate the query-candidate pair more directly and score the relevance relationship with more precision.

That usually makes rerankers:

- slower than retrieval
- more accurate for final ordering
- best used on a narrowed candidate pool

## The Best Placement

The healthiest placement is usually:

```text
filter -> retrieve -> rerank -> final action
```

Where `final action` might be:

- show results to a user
- feed top chunks into RAG
- pass top documents into an LLM judge
- score top candidates against explicit criteria

Do not use a reranker across the entire corpus unless the corpus is tiny.

## How Reranking Changes Top-K Design

Without reranking, you may need a larger retrieved set just to avoid missing strong candidates.

With reranking, you can often:

- retrieve a wider candidate pool
- keep recall healthy
- then aggressively shrink to a smaller, higher-precision top-k

Example:

- retrieve top 50
- rerank those 50
- pass only top 5 or top 10 downstream

That is often much cheaper than passing 50 candidates into an LLM step.

## Good Signals That You Need One

You probably need a reranker if you see patterns like:

- the right result is usually in the retrieved set but not near the top
- semantically broad retrieval brings useful but badly ordered items
- users complain that relevant results exist but are buried
- the LLM downstream is doing too much sorting work on noisy candidates

## Signs You Should Fix Retrieval First

Do not use a reranker to hide a broken first stage.

Fix retrieval before adding reranking if:

- the right answer is often absent from the retrieved set
- hard constraints are being ignored
- abbreviation or lexical failures are common
- metadata filters are missing

Rerankers improve ranking inside the candidate set. They do not magically recover items you never retrieved.

## Cost and Latency Tradeoff

Rerankers are not free.

So the real question is not:

> Is reranking more accurate?

It usually is.

The real question is:

> Is the precision gain worth the extra stage?

That depends on:

- how expensive the downstream mistake is
- how large the candidate set is
- whether user-visible ranking quality matters
- whether an LLM step comes after reranking

If reranking lets you reduce LLM calls or context size later, it often pays for itself.

## Practical Defaults

Good defaults for many systems:

- retrieve broadly enough to protect recall
- rerank only the retrieved shortlist
- pass a much smaller final top-k into the next stage

A common healthy shape is:

```text
top 50 retrieval -> rerank -> top 5 downstream
```

Adjust the numbers based on your corpus size and quality targets.

## Common Mistakes

### 1. Using reranking before fixing hard filters

Exact constraints should usually be handled earlier.

### 2. Reranking too many items

That can destroy the latency advantage of your layered system.

### 3. Expecting reranking to solve recall failures

It cannot recover what retrieval never returned.

### 4. Keeping the downstream top-k too large anyway

If you still pass 30 noisy items to the LLM, the value of reranking is partly lost.

## Takeaway

Rerankers are not the first stage and not always necessary.

They are the precision tool you add when retrieval gets you close, but close is not good enough.
