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


def semantic_score_with_gemini(query_text, document_text, embedding_cache):
    """Use Gemini embeddings first, then return one semantic score."""
    if query_text not in embedding_cache:
        embedding_cache[query_text] = embed_text_with_gemini(query_text)

    if document_text not in embedding_cache:
        embedding_cache[document_text] = embed_text_with_gemini(document_text)

    query_vector = embedding_cache[query_text]
    document_vector = embedding_cache[document_text]
    return _cosine_similarity(query_vector, document_vector)
