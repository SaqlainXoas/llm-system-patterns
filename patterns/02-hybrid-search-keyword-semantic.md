# Pattern 02: Hybrid Search, Keyword Plus Semantic

Hybrid retrieval is often the most practical default for real systems.

It exists because the two simple extremes both fail:

- keyword-only misses meaning
- embedding-only misses exactness

If your task contains both hard terms and flexible phrasing, hybrid is usually where the system starts becoming reliable.

## The Core Idea

Use keyword signals and semantic signals together instead of pretending one method fully replaces the other.

In practice, that often means:

- exact match, metadata filters, or BM25 for hard lexical evidence
- embeddings for meaning, paraphrase, and related language

## Why Keyword Search Still Matters

Keyword-style retrieval is still strong when:

- exact product names matter
- abbreviations are important
- IDs, codes, or version strings matter
- regulated terms must be present
- you care about explicit phrases, not just related meaning

Examples:

- `SOC 2`
- `GDPR`
- `C++`
- `S3`
- `RN`
- exact jurisdiction names

Embedding models may blur, weaken, or miss these signals, especially when the token is short or domain-specific.

## Why Semantic Retrieval Still Matters

Keyword systems struggle when language varies.

Examples:

- `customer churn` vs `retention risk`
- `resume parser` vs `candidate profile extractor`
- `fraud review` vs `transaction abuse detection`
- `incident postmortem` vs `root-cause writeup`

This is where embeddings shine:

- paraphrases
- related concepts
- looser phrasing
- broader contextual similarity

## Why Embedding-Only Is Not Enough

An embedding-only pipeline often looks smart in demos and weak in edge cases.

Common failure modes:

- missing a mandatory exact term
- overvaluing conceptually related but invalid content
- mixing up short abbreviations
- failing to distinguish required versus merely similar

Semantic similarity is not the same as task validity.

## What Hybrid Actually Looks Like

There is no single hybrid architecture.

Common patterns include:

### Keyword pre-filter plus embedding retrieval

Use exact filters first, then semantic retrieval on the remaining pool.

Good when:

- mandatory terms must be enforced
- semantic recall still matters after pruning

### Parallel keyword and embedding retrieval

Retrieve from both methods independently, then merge and score.

Good when:

- you want recall from both worlds
- neither method alone is trustworthy enough

### BM25 plus vector similarity plus rerank

Generate a broader candidate set, then let a reranker clean up the ordering.

Good when:

- the corpus is large
- candidate ordering matters
- the system can afford one more precision stage

## A Simple Mental Model

Think of keyword search as answering:

> Did the text say the important thing?

Think of semantic retrieval as answering:

> Did the text mean the important thing, even if phrased differently?

Real systems often need both answers.

## When Hybrid Is the Right Default

Start with hybrid when:

- exact requirements and broader meaning both matter
- users phrase the same concept in many ways
- abbreviations or hard terms appear alongside natural language variation
- false positives from semantic-only retrieval are costly
- false negatives from keyword-only retrieval are also costly

This is very common in:

- enterprise search
- profile or document matching
- support knowledge retrieval
- policy and compliance lookup
- long-tail terminology domains

## When Hybrid May Be Overkill

Use simpler retrieval if the problem is narrow enough.

Keyword-first may be enough when:

- all key terms are explicit
- terminology is controlled
- exact phrase presence is the main goal

Embedding-first may be enough when:

- language variation is high
- hard constraints are minimal
- exact wording matters less than intent similarity

## Common Design Mistakes

### 1. Treating embeddings as a full replacement for lexical search

This usually fails when exactness matters.

### 2. Merging scores without understanding what they mean

BM25 and cosine similarity are different signals. Combining them blindly can create unstable ranking.

### 3. Using hybrid when the corpus is tiny

If you only have a small candidate set, simple filtering and direct comparison may be enough.

### 4. Forgetting the abbreviation problem

Short tokens and domain acronyms often need exact support.

## Practical Implementation Options

Start with the simplest viable version:

### Option A: Filter first, then semantic search

Best early default when hard constraints are clear.

### Option B: Retrieve keyword top-k and embedding top-k, then union them

Best when recall is the top concern.

### Option C: Hybrid retrieval plus reranking

Best when result ordering quality matters and you can afford one extra stage.

## Recommended Default

For many production-minded systems, this is a strong default:

```text
hard filters
-> keyword top-k
-> embedding top-k
-> merge
-> rerank
-> final downstream task
```

If that feels too heavy, simplify to:

```text
hard filters
-> embedding retrieval
with exact-term boosting or keyword fallback
```

## Takeaway

Keyword search and semantic retrieval are not enemies.

They solve different failure modes.

When a system needs both exactness and meaning, hybrid retrieval is usually the design that behaves like an engineering solution instead of a demo.
