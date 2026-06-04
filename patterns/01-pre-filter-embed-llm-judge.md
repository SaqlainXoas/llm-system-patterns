# Pattern 01: Pre-filter -> Embed -> Rerank -> LLM Judge

This is the flagship pattern of the repo.

It teaches one practical rule:

> Do the cheap, reliable narrowing first. Ask the LLM to reason only after the candidate set is already small.

If you skip that rule, the system usually becomes slower, more expensive, and less reliable than it needs to be.

## Why This Pattern Matters

Many LLM application designs start in the wrong place:

- send the full problem directly to an LLM
- ask it to search, compare, rank, and explain everything at once
- hope prompting alone will keep the result stable

That works for small demos, but it breaks down quickly when:

- the candidate pool is large
- some constraints are non-negotiable
- exact terms, IDs, certifications, or abbreviations matter
- cost and latency start to matter in production

This pattern fixes that by turning one expensive fuzzy decision into a layered system.

## The Core Flow

```text
pre-filter -> semantic retrieval -> optional rerank -> final LLM judgment
```

Each stage has a different job:

1. `Pre-filter`
   Remove clearly invalid candidates with deterministic logic.
2. `Semantic retrieval`
   Pull in the most meaningfully related candidates.
3. `Rerank`
   Improve ordering when retrieval is broad but imprecise.
4. `LLM judge`
   Compare only the narrowed set and produce a grounded final score or explanation.

## What Each Layer Is Good At

### Stage 1: Pre-filter

Use deterministic logic first when the constraint is hard.

Good examples:

- required language
- must-have certifications
- exact region or jurisdiction
- explicit product family
- mandatory compliance tags
- minimum years threshold when it can be extracted safely

Why this stage matters:

- it is cheap
- it is fast
- it is explainable
- it prevents waste in later stages

This is where regex, exact keywords, metadata filters, rule checks, and structured fields still win.

### Stage 2: Semantic retrieval

After hard pruning, use embeddings or hybrid retrieval to widen recall.

This stage helps when the wording differs:

- `software engineer` vs `backend developer`
- `fraud prevention` vs `risk controls`
- `HIPAA compliance` vs `healthcare privacy work`

Its job is not to make the final decision.

Its job is to produce a good candidate pool for later stages.

### Stage 3: Rerank

Retrieval often finds relevant items but orders them imperfectly.

A reranker is useful when:

- the right answer is somewhere in the top results
- near-duplicate candidates need better separation
- semantic retrieval is broad enough to be useful but still noisy

If retrieval quality is already strong and the candidate set is small, you may skip this stage.

### Stage 4: LLM judge

The LLM should come last.

At this point, the model is no longer being asked to search the universe. It is being asked to reason over a narrowed shortlist.

That makes the LLM stage:

- cheaper
- more grounded
- easier to prompt
- easier to evaluate

## Example Framing: Document Scoring Pipeline

One clean example is document scoring.

Imagine you need to score documents against a target brief:

- proposals against a requirements sheet
- profiles against a role definition
- internal knowledge entries against a task need
- policy documents against a compliance checklist

The wrong design is:

> Give all documents to the LLM and ask it to choose.

The better design is:

1. Filter out documents that fail hard constraints.
2. Retrieve semantically related content.
3. Rerank the top candidates if ordering quality matters.
4. Ask the LLM to score only the shortlisted items against explicit criteria.

## Why This Beats LLM-First Design

### Lower cost

The expensive model sees fewer candidates.

### Lower latency

Cheap pruning removes work before the slowest stage.

### Better reliability

Hard constraints are enforced deterministically instead of being "remembered" by the prompt.

### Better debugging

When results are bad, you can inspect which stage failed:

- pre-filter too strict
- retrieval too weak
- reranker not helping
- judge prompt poorly defined

## Failure Modes This Pattern Prevents

### 1. Hard requirements get ignored

If the LLM is asked to judge everything at once, it may overvalue semantic fit and underweight a mandatory requirement.

### 2. Abbreviations get missed

Short or domain-specific tokens can be weak in embedding space, so exact matching still matters before or alongside semantic search.

### 3. Cost explodes with scale

An LLM-first pipeline may be acceptable on 20 items and unacceptable on 20,000.

### 4. Explanations sound smart but are poorly grounded

When the model sees too much broad context, it may produce plausible but weakly supported comparisons.

## When To Use This Pattern

Use it when:

- you are searching or scoring across many candidates
- some requirements are exact and non-negotiable
- semantic similarity matters but is not enough alone
- you need good explanations without paying for full-set LLM comparisons

It is especially useful for:

- retrieval pipelines
- matching systems
- ranking workflows
- grounded evaluation tasks
- production-minded RAG systems

## When You Might Simplify It

You do not always need all four stages.

Use a lighter version when:

- the candidate set is already tiny
- exact filters alone solve most of the task
- the ranking need is weak
- LLM explanation is optional

Common lighter variants:

- `pre-filter -> hybrid retrieval`
- `pre-filter -> retrieval -> LLM judge`
- `keyword search -> rerank`

## Design Checklist

Before implementing this pattern, decide:

- what counts as a hard filter versus a soft preference
- what fields are structured versus extracted from text
- whether retrieval is keyword, embedding, or hybrid
- how large the candidate pool should be before reranking
- whether the LLM is scoring, validating, or explaining
- what evidence the judge prompt must cite

## Grounding Rules For The Judge Step

If you use an LLM judge, keep it disciplined:

- only pass the narrowed top candidates
- provide explicit scoring criteria
- require evidence from the candidate text
- separate score from explanation
- avoid asking the model to invent missing facts

Good prompt role:

> Compare these shortlisted candidates against the criteria using only the provided evidence.

Bad prompt role:

> Figure out the best answer from everything and use your judgment.

## Practical Default

If you need a good default architecture, start here:

```text
metadata / regex filters
-> hybrid retrieval
-> top-k narrowing
-> rerank top 20
-> LLM judge top 5
```

That default is not universal, but it reflects a healthy production instinct:

- deterministic first
- semantic second
- expensive reasoning last

## Takeaway

The strongest LLM systems are usually not the ones that ask the biggest model to do everything.

They are the ones that break the task into layers and let each method do the part it is best at.
