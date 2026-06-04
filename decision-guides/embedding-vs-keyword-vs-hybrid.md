# Decision Guide: Embedding vs Keyword vs Hybrid

This guide is for the most common retrieval choice in practical LLM systems:

> Should I use keyword search, embeddings, or a hybrid of both?

The short answer is:

- use `keyword` when exact terms are the main truth signal
- use `embeddings` when wording varies and meaning matters more than phrasing
- use `hybrid` when your task needs both exactness and semantic flexibility

For many real production systems, `hybrid` is the safest default.

## Fast Decision Table

| Situation | Best starting point | Why |
|---|---|---|
| Exact terms are mandatory | Keyword | Hard lexical evidence matters more than paraphrase |
| Meaning matters more than wording | Embeddings | Semantic similarity covers phrasing variation |
| Both exact terms and related meaning matter | Hybrid | You need both lexical and semantic signals |
| Short tokens, acronyms, IDs, and required skills matter | Keyword or Hybrid | These often need exact support |
| The corpus is small and simple | Keyword or simple Hybrid | Full semantic complexity may be unnecessary |
| Result quality matters at the top of the ranking | Hybrid plus rerank | Better recall and better final ordering |

## Start With the Real Question

Do not ask:

> Which method is more advanced?

Ask:

> What kind of evidence proves relevance in this problem?

That is the better design question.

## Choose Keyword First When

Keyword retrieval is the better first choice when:

- exact phrase presence matters
- abbreviations are important
- required skills or certifications must literally appear
- IDs, codes, model names, or version names matter
- legal, policy, or compliance wording is strict

Examples:

- finding all documents that mention `SOC 2`
- matching exact product codes
- checking whether a policy contains a required clause
- filtering for hard skill terms before any broader scoring

### Strengths of Keyword Search

- precise for exact terms
- cheap and interpretable
- strong for abbreviations and codes
- easy to debug

### Weaknesses of Keyword Search

- weak on paraphrases
- misses broader meaning
- brittle when terminology varies

## Choose Embeddings First When

Embedding retrieval is the better first choice when:

- the same idea appears in many phrasings
- intent similarity matters more than exact words
- synonyms and related expressions are common
- user queries are natural language and underspecified

Examples:

- finding documents about `customer retention` even if the text says `reduce churn`
- matching a need description to related prior work
- retrieving conceptually similar support resolutions

### Strengths of Embeddings

- flexible on language variation
- strong on concept-level similarity
- useful for broader recall

### Weaknesses of Embeddings

- weaker on exact required terms
- can confuse near concepts with valid matches
- can miss short tokens and abbreviations

## Choose Hybrid When

Hybrid is the right start when:

- exact requirements exist alongside flexible phrasing
- keyword-only misses too much
- embedding-only returns too many soft false positives
- your domain mixes structured terms with natural language variation

Examples:

- role, profile, or document matching
- enterprise search
- policy lookup
- technical support knowledge systems
- RAG over domain-specific content

This is common enough that hybrid is often the most practical default.

## The Abbreviation Test

Ask this simple question:

> If the system misses a short acronym, code, or exact term, does the result become unacceptable?

If yes, do not rely on embeddings alone.

That is usually a strong signal for keyword or hybrid.

## The Paraphrase Test

Ask:

> If the exact words change but the meaning stays the same, should the system still match?

If yes, do not rely on keyword search alone.

That is usually a strong signal for embeddings or hybrid.

## Recommended Default by Problem Shape

### Search over strict terminology

Start with keyword.

### Search over fuzzy natural language

Start with embeddings.

### Search over documents with hard constraints and soft meaning

Start with hybrid.

### Large ranking pipeline before an LLM step

Start with hybrid, then consider reranking.

## Common Mistakes

### 1. Using embeddings because they feel more modern

Modern does not mean correct for the evidence your task needs.

### 2. Using keyword search when user phrasing varies heavily

This causes avoidable false negatives.

### 3. Calling a system hybrid when it only adds a tiny exact filter

True hybrid design should let both lexical and semantic signals influence the candidate set meaningfully.

### 4. Ignoring top-k quality

Even if retrieval type is right, bad ranking can still hurt the downstream system.

## A Practical Default Recommendation

If you are unsure, start here:

1. add cheap hard filters for mandatory constraints
2. use keyword and embedding retrieval together
3. merge the candidate sets
4. rerank only if ordering quality still feels weak

That path is usually easier to improve than an embedding-only design that never respected exactness.

## Takeaway

Keyword search proves explicit evidence.

Embeddings recover broader meaning.

Hybrid systems win when the task needs both, which is why so many serious LLM pipelines eventually move in that direction.
