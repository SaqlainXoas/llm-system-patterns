from llm import embed_text_with_gemini


def cosine_similarity(left_vector, right_vector):
    """Return cosine similarity for two embedding vectors."""
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


def count_keyword_matches(brief, proposal):
    """Count preferred capability terms that appear exactly in the proposal text."""
    proposal_text = proposal["text"].lower()
    matches = 0

    for term in brief["preferred_terms"]:
        if term.lower() in proposal_text:
            matches += 1

    return matches


def score_proposals(brief, proposals):
    """Score proposals with exact-term support plus semantic similarity."""
    brief_vector = embed_text_with_gemini(brief["summary"])
    scored_rows = []

    for proposal in proposals:
        proposal_vector = embed_text_with_gemini(proposal["text"])
        semantic_score = cosine_similarity(brief_vector, proposal_vector)
        keyword_score = count_keyword_matches(brief, proposal)

        scored_rows.append(
            {
                "proposal": proposal,
                "keyword_score": keyword_score,
                "semantic_score": semantic_score,
                "final_score": keyword_score + semantic_score,
            }
        )

    scored_rows.sort(key=lambda row: row["final_score"], reverse=True)
    return scored_rows


def build_shortlist(brief, proposals, top_k=3):
    """Return the strongest proposals after pre-filtering and semantic scoring."""
    scored_rows = score_proposals(brief, proposals)
    return scored_rows[:top_k]
