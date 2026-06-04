# Pattern 07: Cost and Latency Budgeting

Cost and latency are not cleanup topics.

They are architecture topics.

If you ignore them until late, you often discover that the "best" pipeline is too slow, too expensive, or too unstable to run at the scale you actually need.

## The Core Rule

Push expensive work as late as possible.

That usually means:

- cheap filters first
- retrieval before generation
- narrowing before comparison
- LLM reasoning only on the final shortlist

This is one of the most important habits in production-minded LLM design.

## Why Budgeting Must Happen Early

A design can look correct in a notebook and still fail in practice because:

- each request calls the model too many times
- too much text is sent per request
- broad candidate sets are processed unnecessarily
- repeated work is not cached
- throughput collapses under batch use

The fix is rarely just "use a cheaper model."

Usually the better fix is to reduce how much expensive work reaches the model at all.

## Think in Four Budgets

### 1. Cost budget

How much are you willing to spend per request, per batch, or per day?

### 2. Latency budget

How long can a user wait, or how long can an offline pipeline take per item?

### 3. Context budget

How much text can you afford to pass into the model before quality, latency, or cost degrade?

### 4. Error budget

How often can the system be wrong before the pipeline becomes unusable or risky?

All four interact.

## Expensive Work Should Come Last

This repo repeats one idea often because it matters often:

> Narrow first. Reason last.

Bad order:

```text
LLM compare everything -> then try to clean up the result
```

Better order:

```text
hard filters -> retrieval -> rerank -> LLM only on top-k
```

That ordering usually reduces both latency and cost while improving stability.

## Where the Biggest Wins Usually Come From

### Deterministic pruning

Remove impossible candidates before any semantic or LLM stage.

### Top-k narrowing

Do not pass 100 candidates into a stage that only needs 5.

### Batching

Process compatible work together when the workflow and provider support it.

### Caching

Avoid recomputing repeated embeddings, repeated extraction, repeated normalization, or repeated scoring inputs when nothing changed.

### Better chunking

Smaller, better-shaped candidate units often reduce waste downstream.

## Cost vs Latency Is Not the Same Tradeoff

Some teams treat cost and latency as the same thing. They overlap, but they are not identical.

Examples:

- A smaller model may reduce cost and improve latency.
- A reranker may add latency but reduce total cost by shrinking the LLM workload.
- More aggressive retrieval may improve quality while slightly increasing latency.
- More caching may improve latency without changing model quality at all.

Design decisions should be judged on total pipeline effect, not single-stage intuition.

## Online vs Offline Budgeting

### Online systems

Prioritize:

- response time
- predictable tail latency
- graceful fallback behavior
- bounded context size

### Offline or batch pipelines

Prioritize:

- throughput
- cost per item
- memory use
- recoverability after failures

The same architecture may need different defaults depending on whether it serves a live user or a background batch.

## Where Caching Helps

Caching is strongest when inputs repeat.

Good caching targets:

- embeddings for stable documents
- normalized metadata
- parsed document sections
- retrieval results for repeated queries when freshness needs allow

Caching is weaker when:

- prompts change constantly
- the source data changes frequently
- the expensive step depends on highly dynamic context

## Practical Questions To Ask Early

Before going too far, answer:

- What is the maximum acceptable cost per request?
- What is the maximum acceptable latency?
- Which stages can run in parallel?
- Which artifacts can be cached safely?
- Which stage dominates runtime?
- Which stage dominates spend?

These answers usually shape architecture more than model branding does.

## A Simple Example

Imagine a scoring pipeline over many documents.

Expensive version:

- send each document directly to an LLM
- ask for full scoring and explanation

Better version:

- extract and normalize once
- filter invalid documents
- retrieve top candidates
- rerank if needed
- ask the LLM to score only the final shortlist

The second design often wins on all three fronts:

- cheaper
- faster
- easier to debug

## Common Budgeting Mistakes

### 1. Designing for quality only

A pipeline that is too slow or too expensive is not actually high quality in production.

### 2. Letting the LLM do filtering work

That is one of the most common sources of avoidable cost.

### 3. Ignoring long-tail latency

Average latency can look fine while worst-case latency is unacceptable.

### 4. Skipping measurement

If you do not track stage-level timing and spend, you cannot improve the right part.

## Recommended Default Mindset

Treat each stage like it must earn its place.

Ask:

- does this stage improve recall?
- does it improve precision?
- does it reduce downstream cost?
- does it make the final decision more reliable?

If the answer is no, the stage may be unnecessary.

## Takeaway

Strong LLM systems are not just accurate.

They are accurate within a cost, latency, and operational budget that the real system can survive.
