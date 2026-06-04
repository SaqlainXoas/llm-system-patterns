import json
import os

from google import genai
from pinecone import Pinecone


def embed_text_with_gemini(text):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )
    return result.embeddings[0].values


def rerank_with_pinecone(query_text, proposal_rows, top_n=5):
    """Use Pinecone hosted reranking on the returned shortlist."""
    client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    result = client.inference.rerank(
        model="bge-reranker-v2-m3",
        query=query_text,
        documents=[
            {
                "id": row["proposal_id"],
                "text": row["text"],
            }
            for row in proposal_rows
        ],
        top_n=top_n,
        return_documents=True,
    )

    reranked_rows = []
    for row in result.data:
        document = row.document

        if hasattr(document, "get"):
            proposal_id = document.get("id")
            text = document.get("text")
        else:
            proposal_id = getattr(document, "id", None)
            text = getattr(document, "text", None)

        reranked_rows.append(
            {
                "proposal_id": proposal_id,
                "text": text,
                "rerank_score": row.score,
            }
        )

    return reranked_rows


def judge_shortlist(brief, shortlist_rows):
    """Final LLM comparison after retrieval and reranking."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = {
        "brief": brief,
        "shortlist": shortlist_rows,
        "instructions": [
            "Pick the strongest fit for the brief.",
            "Use concise evidence grounded in the shortlist text.",
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
                    "reason": {"type": "string"},
                },
                "required": ["winner_proposal_id", "reason"],
            },
        },
    )

    return json.loads(response.text)
