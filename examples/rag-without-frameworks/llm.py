import json
import os

from google import genai


def embed_text_with_gemini(text):
    """Return one embedding vector for retrieval scoring."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )
    return result.embeddings[0].values


def answer_with_gemini(question, evidence_chunks):
    """Answer only from the retrieved evidence."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = {
        "question": question,
        "evidence_chunks": evidence_chunks,
        "instructions": [
            "Answer only from the evidence chunks.",
            "If the evidence is missing, say that clearly.",
            "Do not invent unsupported details.",
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
                    "answer": {"type": "string"},
                    "used_chunk_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["answer", "used_chunk_ids"],
            },
        },
    )

    return json.loads(response.text)
