from llm import embed_text_with_gemini, judge_shortlist, rerank_with_pinecone
from vector_store import query_chroma, query_pinecone


def search_with_pinecone(index, namespace, brief, top_k=10):
    """Search a persistent Pinecone index with the brief embedding."""
    query_vector = embed_text_with_gemini(brief["summary"])
    return query_pinecone(
        index=index,
        namespace=namespace,
        query_vector=query_vector,
        region=brief["region"],
        top_k=top_k,
    )


def search_with_chroma(collection, brief, top_k=10):
    """Search a local Chroma collection by text."""
    return query_chroma(
        collection=collection,
        brief_text=brief["summary"],
        region=brief["region"],
        top_k=top_k,
    )


def rerank_then_judge(brief, proposal_rows):
    """Use Pinecone rerank for the shortlist, then let Gemini do final judgment."""
    reranked_rows = rerank_with_pinecone(brief["summary"], proposal_rows)
    return judge_shortlist(brief, reranked_rows)
