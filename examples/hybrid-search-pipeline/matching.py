import json

from llm import semantic_score_with_gemini


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def keyword_search(query, documents, top_k=3):
    """Find exact token hits first for abbreviations and must-have words."""
    scored_rows = []
    query_text = query["text"].lower()
    required_terms = [term.lower() for term in query.get("required_terms", [])]

    for document in documents:
        text = document["text"].lower()
        exact_matches = 0

        for term in required_terms:
            if term in text:
                exact_matches += 1

        if query_text in text:
            exact_matches += 1

        if exact_matches > 0:
            scored_rows.append(
                {
                    "document": document,
                    "keyword_score": exact_matches,
                }
            )

    scored_rows.sort(key=lambda row: row["keyword_score"], reverse=True)
    return scored_rows[:top_k]


def semantic_search(query, documents, top_k=3):
    """Find broader meaning matches with embeddings."""
    embedding_cache = {}
    scored_rows = []

    for document in documents:
        semantic_score = semantic_score_with_gemini(
            query["text"],
            document["text"],
            embedding_cache,
        )
        scored_rows.append(
            {
                "document": document,
                "semantic_score": semantic_score,
            }
        )

    scored_rows.sort(key=lambda row: row["semantic_score"], reverse=True)
    return scored_rows[:top_k]


def merge_hits(keyword_hits, semantic_hits):
    """Merge exact and semantic hits without losing either signal."""
    merged_rows = {}

    for row in keyword_hits:
        doc = row["document"]
        merged_rows[doc["doc_id"]] = {
            "document": doc,
            "keyword_score": row["keyword_score"],
            "semantic_score": 0.0,
        }

    for row in semantic_hits:
        doc = row["document"]
        current = merged_rows.get(doc["doc_id"])

        if current is None:
            merged_rows[doc["doc_id"]] = {
                "document": doc,
                "keyword_score": 0,
                "semantic_score": row["semantic_score"],
            }
        else:
            current["semantic_score"] = row["semantic_score"]

    merged_list = list(merged_rows.values())
    merged_list.sort(
        key=lambda row: (row["keyword_score"], row["semantic_score"]),
        reverse=True,
    )
    return merged_list


def run_hybrid_search(query, documents):
    """Show the full hybrid flow in one readable function."""
    keyword_hits = keyword_search(query, documents)
    semantic_hits = semantic_search(query, documents)
    return merge_hits(keyword_hits, semantic_hits)
