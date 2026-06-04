import os

from google import genai


def embed_text_with_gemini(text):
    """Return one embedding vector for semantic comparison."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )
    return result.embeddings[0].values
