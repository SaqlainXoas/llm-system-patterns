from llm import embed_text_with_gemini


def cosine_similarity(left_vector, right_vector):
    dot_product = 0.0
    left_size = 0.0
    right_size = 0.0

    for left_value, right_value in zip(left_vector, right_vector):
        dot_product += left_value * right_value
        left_size += left_value * left_value
        right_size += right_value * right_value

    if left_size == 0 or right_size == 0:
        return 0.0

    return dot_product / ((left_size ** 0.5) * (right_size ** 0.5))


def score_one_batch(brief, proposals, brief_vector):
    """Score only the current batch, then return ranked rows."""
    scored_rows = []

    for proposal in proposals:
        proposal_vector = embed_text_with_gemini(proposal["text"])
        semantic_score = cosine_similarity(brief_vector, proposal_vector)

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


def build_batch_shortlist(brief, proposal_batches):
    """Embed one batch at a time and keep only the strongest pool."""
    brief_vector = embed_text_with_gemini(brief["summary"])
    shortlist = []

    for batch in proposal_batches:
        shortlist.extend(score_one_batch(brief, batch, brief_vector))
        shortlist.sort(key=lambda row: row["score"], reverse=True)
        shortlist = shortlist[:40]

        # In the real worker flow, drop the finished batch here.
        del batch

    return shortlist[:10]
