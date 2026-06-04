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
