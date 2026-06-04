import json
import os

from google import genai


def embed_text_with_gemini(text):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )
    return result.embeddings[0].values


def _cosine_similarity(left_vector, right_vector):
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


def semantic_score_with_gemini(brief_vector, proposal_text, embedding_cache):
    """Use Gemini embeddings first, then return one semantic score."""
    if proposal_text not in embedding_cache:
        embedding_cache[proposal_text] = embed_text_with_gemini(proposal_text)

    proposal_vector = embedding_cache[proposal_text]
    return _cosine_similarity(brief_vector, proposal_vector)


def judge_final_pool(brief, shortlist_rows):
    """Late-stage LLM validation for the final shortlist only."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = {
        "brief": brief,
        "shortlist": [
            {
                "proposal_id": row["proposal"]["proposal_id"],
                "title": row["proposal"]["title"],
                "score": row["score"],
                "summary": row["proposal"]["summary"],
            }
            for row in shortlist_rows
        ],
        "instructions": [
            "Rank the shortlist only.",
            "Use the brief as the truth source.",
            "Return concise JSON for downstream systems.",
        ],
    }

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=json.dumps(prompt, indent=2),
        config={
            "response_mime_type": "application/json",
            "response_json_schema": {
                "type": "object",
                "properties": {
                    "winner_proposal_id": {"type": "string"},
                    "top_reasons": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "ranked_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["winner_proposal_id", "top_reasons", "ranked_ids"],
            },
        },
    )

    return json.loads(response.text)


# The same flow works with OpenAI or another provider.
# Keep the model late and keep the output structured.
