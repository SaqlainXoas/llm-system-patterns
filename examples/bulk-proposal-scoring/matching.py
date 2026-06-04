from llm import embed_text_with_gemini, semantic_score_with_gemini


def get_cached_embedding(cache, text):
    """Reuse embeddings inside one run instead of recomputing the same text."""
    if text not in cache:
        cache[text] = embed_text_with_gemini(text)

    return cache[text]


def score_one_batch(brief, proposals, brief_vector, embedding_cache):
    """Score only the current batch, then return ranked rows."""
    scored_rows = []

    for proposal in proposals:
        semantic_score = semantic_score_with_gemini(
            brief_vector,
            proposal["text"],
            embedding_cache,
        )

        score = semantic_score
        for term in brief["preferred_terms"]:
            if term.lower() in proposal["text"].lower():
                score += 1

        scored_rows.append(
            {
                "proposal": proposal,
                "semantic_score": semantic_score,
                "score": score,
            }
        )

    scored_rows.sort(key=lambda row: row["score"], reverse=True)
    return scored_rows


def cleanup_finished_batch(batch_rows):
    """Keep only the minimal fields needed after a batch has been scored."""
    cleaned_rows = []

    for row in batch_rows:
        cleaned_rows.append(
            {
                "proposal": row["proposal"],
                "semantic_score": row["semantic_score"],
                "score": row["score"],
            }
        )

    return cleaned_rows


def build_batch_shortlist(brief, proposal_batches, rolling_pool_size=40, top_k=10):
    """Embed one batch at a time and keep only the strongest pool."""
    embedding_cache = {}
    brief_vector = get_cached_embedding(embedding_cache, brief["summary"])
    shortlist = []

    for batch in proposal_batches:
        batch_rows = score_one_batch(brief, batch, brief_vector, embedding_cache)
        shortlist.extend(cleanup_finished_batch(batch_rows))
        shortlist.sort(key=lambda row: row["score"], reverse=True)
        shortlist = shortlist[:rolling_pool_size]

        # In the real worker flow, drop the finished batch here.
        del batch_rows
        del batch

    return shortlist[:top_k]


def run_bulk_scoring_job(brief, proposals, batcher, dedupe_fn, pre_filter_fn):
    """Show the full engineering flow in one readable function."""
    unique_proposals = dedupe_fn(proposals)
    proposal_batches = []

    for batch in batcher(unique_proposals, size=2):
        filtered_batch = pre_filter_fn(brief, batch)
        if filtered_batch:
            proposal_batches.append(filtered_batch)

    return build_batch_shortlist(brief, proposal_batches)
