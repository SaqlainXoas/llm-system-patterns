import json

from llm import answer_with_gemini, embed_text_with_gemini


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


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


def chunk_documents(documents):
    """Keep chunking simple so the retrieval flow is easy to inspect."""
    chunks = []

    for document in documents:
        for index, paragraph in enumerate(document["paragraphs"], start=1):
            chunks.append(
                {
                    "chunk_id": f'{document["doc_id"]}-chunk-{index}',
                    "title": document["title"],
                    "text": paragraph,
                }
            )

    return chunks


def get_cached_embedding(cache, text):
    """Reuse embeddings inside one question run."""
    if text not in cache:
        cache[text] = embed_text_with_gemini(text)

    return cache[text]


def retrieve_top_chunks(question, chunks, top_k=3):
    """Retrieve the top evidence chunks for one question."""
    embedding_cache = {}
    question_vector = get_cached_embedding(embedding_cache, question)
    scored_rows = []

    for chunk in chunks:
        chunk_vector = get_cached_embedding(embedding_cache, chunk["text"])
        score = cosine_similarity(question_vector, chunk_vector)
        scored_rows.append(
            {
                "chunk": chunk,
                "score": score,
            }
        )

    scored_rows.sort(key=lambda row: row["score"], reverse=True)
    return scored_rows[:top_k]


def cleanup_scored_rows(scored_rows):
    """Trim the retrieval rows to the fields the final prompt actually needs."""
    cleaned_rows = []

    for row in scored_rows:
        cleaned_rows.append(
            {
                "chunk_id": row["chunk"]["chunk_id"],
                "title": row["chunk"]["title"],
                "text": row["chunk"]["text"],
                "score": row["score"],
            }
        )

    return cleaned_rows


def answer_question(question_text, documents):
    """Show the full no-framework RAG flow in one readable function."""
    chunks = chunk_documents(documents)
    scored_rows = retrieve_top_chunks(question_text, chunks)
    evidence_rows = cleanup_scored_rows(scored_rows)
    return answer_with_gemini(question_text, evidence_rows)
