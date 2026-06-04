import os

import chromadb
from pinecone import Pinecone


def get_pinecone_index():
    """Return a Pinecone index handle for a persistent production store."""
    client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    return client.Index(host=os.environ["PINECONE_INDEX_HOST"])


def upsert_proposals_to_pinecone(index, namespace, proposals, embed_text):
    """Upsert proposal vectors plus metadata into Pinecone."""
    vectors = []

    for proposal in proposals:
        vectors.append(
            {
                "id": proposal["proposal_id"],
                "values": embed_text(proposal["text"]),
                "metadata": {
                    "title": proposal["title"],
                    "region": proposal["region"],
                    "summary": proposal["summary"],
                    "text": proposal["text"],
                },
            }
        )

    index.upsert(vectors=vectors, namespace=namespace)


def query_pinecone(index, namespace, query_vector, region, top_k=10):
    """Query Pinecone with a vector and a simple region filter."""
    return index.query(
        namespace=namespace,
        vector=query_vector,
        filter={"region": {"$eq": region}},
        top_k=top_k,
        include_metadata=True,
    )


def get_local_chroma_collection(name="proposal_briefs"):
    """Return a local Chroma collection for development or small local testing."""
    client = chromadb.Client()
    return client.get_or_create_collection(name=name)


def upsert_proposals_to_chroma(collection, proposals):
    """Store proposal text locally in Chroma."""
    collection.add(
        ids=[proposal["proposal_id"] for proposal in proposals],
        documents=[proposal["text"] for proposal in proposals],
        metadatas=[
            {
                "title": proposal["title"],
                "region": proposal["region"],
                "summary": proposal["summary"],
            }
            for proposal in proposals
        ],
    )


def query_chroma(collection, brief_text, region, top_k=10):
    """Query the local Chroma collection by text."""
    return collection.query(
        query_texts=[brief_text],
        n_results=top_k,
        where={"region": region},
    )
