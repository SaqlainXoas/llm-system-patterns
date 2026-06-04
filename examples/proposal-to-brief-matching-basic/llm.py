import json
import os

from google import genai


def embed_text_with_gemini(text):
    """Return one Gemini embedding vector for the provided text."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )
    return result.embeddings[0].values


def judge_shortlist(brief, shortlist_rows):
    """Ask Gemini to score only the final shortlist as structured JSON."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = {
        "task": "Score proposal fit against the brief.",
        "brief": brief,
        "shortlist": [
            {
                "proposal_id": row["proposal"]["proposal_id"],
                "title": row["proposal"]["title"],
                "keyword_score": row["keyword_score"],
                "semantic_score": row["semantic_score"],
                "summary": row["proposal"]["summary"],
            }
            for row in shortlist_rows
        ],
        "instructions": [
            "Respect the required terms in the brief.",
            "Prefer grounded reasoning over generic praise.",
            "Return one winner plus short evidence for the ranking.",
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
                    "ranking_reason": {"type": "string"},
                    "scores": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "proposal_id": {"type": "string"},
                                "fit_score": {"type": "number"},
                                "evidence": {"type": "string"},
                            },
                            "required": ["proposal_id", "fit_score", "evidence"],
                        },
                    },
                },
                "required": ["winner_proposal_id", "ranking_reason", "scores"],
            },
        },
    )

    return json.loads(response.text)


# Swap Gemini for OpenAI or another provider if your stack prefers it.
# The important design rule is structured JSON on the final shortlist.
