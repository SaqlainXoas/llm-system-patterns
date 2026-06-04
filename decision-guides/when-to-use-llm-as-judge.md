# Decision Guide: When to Use LLM-as-Judge

Use this guide when you are deciding whether final scoring, validation, or comparison should be done by an LLM or by simpler methods.

Short version:

- use LLM judgment after narrowing and grounding
- avoid it as the first or only decision layer
- prefer deterministic logic when the rule is exact and non-negotiable

## Fast Decision Table

| Situation | Recommendation | Why |
|---|---|---|
| The task needs nuanced comparison across a small shortlist | Use LLM-as-judge | This is where the model adds real value |
| The rule is exact and binary | Use deterministic logic | Exact checks are cheaper and more reliable |
| The candidate set is very large | Narrow first | LLM judgment is too expensive and noisy at full scale |
| You need grounded explanation with evidence | Use LLM-as-judge after narrowing | The model can compare and explain if context is controlled |
| The evaluation must be perfectly consistent | Prefer deterministic or tightly structured evaluation | LLM outputs can drift |

## The Core Question

Do not ask:

> Can an LLM judge this?

Ask:

> Is nuanced model reasoning actually needed here, or can the system decide with cheaper, more stable logic?

That is the better architecture question.

## Use LLM-as-Judge When

### 1. The task is comparative, not just exact

Examples:

- compare shortlisted documents against criteria
- decide which candidate best satisfies a brief
- score the quality of evidence among a small set of candidates

### 2. The candidate set is already narrow

The model should judge a shortlist, not the whole corpus.

### 3. The decision needs interpretation

An LLM is useful when the task involves:

- balancing multiple soft signals
- summarizing tradeoffs
- generating a reasoned explanation from provided evidence

### 4. The judgment can be grounded

The model should have:

- explicit criteria
- bounded context
- the relevant candidate text
- instructions to cite or reference evidence

## Do Not Use LLM-as-Judge When

### 1. The decision is a hard rule

Examples:

- required field exists or not
- exact phrase is present or not
- numeric threshold is met or not

These are better handled deterministically.

### 2. The model would need to inspect too much broad context

If the candidate set is too large, the model becomes expensive and easier to mislead.

### 3. You want the LLM to do retrieval and judging at the same time

That usually produces a pipeline that is both costly and hard to debug.

### 4. You need near-perfect consistency

LLM judgments can vary with prompt shape, evidence ordering, and context differences.

## Best Placement In a Pipeline

The healthiest placement is usually:

```text
filter -> retrieve -> optional rerank -> LLM judge
```

That order matters because it gives the model a smaller, better-shaped problem.

## What the LLM Should Be Asked To Do

Good jobs for an LLM judge:

- compare shortlisted options
- score relevance against explicit criteria
- explain tradeoffs between strong candidates
- validate whether retrieved evidence supports a claim

Bad jobs for an LLM judge:

- search the full corpus
- enforce hard filters
- guess missing facts
- act as the only trust layer in a high-stakes system

## Grounding Checklist

Before adding an LLM judge, make sure you can answer yes to most of these:

- Is the candidate set already narrow?
- Are the criteria explicit?
- Is the evidence included in the prompt?
- Can the output be structured?
- Can you review where the judgment came from?

If most answers are no, the stage is probably too early or poorly defined.

## Common Mistakes

### 1. Using the LLM as the first stage

This wastes cost and hides too much logic in a single prompt.

### 2. Asking for judgment without evidence

That encourages plausible but weakly grounded outputs.

### 3. Mixing hard constraints with soft reasoning

Hard rules should usually be applied before the LLM step.

### 4. Overtrusting the explanation

A confident explanation is not the same thing as a reliable decision.

## A Good Default

If you need nuanced final scoring, use this shape:

```text
hard filters
-> retrieval or hybrid retrieval
-> top-k narrowing
-> optional rerank
-> LLM judge on the final shortlist
```

That pattern preserves the value of model reasoning without letting it take over the whole pipeline.

## Takeaway

LLM-as-judge is strongest as a late-stage reasoning layer.

Use it when the system needs nuanced comparison over a small, grounded shortlist.
Do not use it where exact, deterministic logic is enough.
