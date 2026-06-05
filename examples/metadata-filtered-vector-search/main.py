import chromadb


def build_demo_documents():
    """Return a small set with one valid document and several invalid lookalikes."""
    return [
        {
            "document_id": "doc-1",
            "title": "US Published Delivery Refund Policy",
            "text": (
                "Published US policy for delayed delivery refunds. "
                "Customers can request a refund when delivery is delayed and the order arrives late."
            ),
            "region": "US",
            "document_type": "policy",
            "status": "published",
        },
        {
            "document_id": "doc-2",
            "title": "EU Published Delayed Delivery Refund Policy",
            "text": (
                "Published EU policy for delayed delivery refunds. "
                "This refund policy explains refund steps for delivery delays and late orders in the EU."
            ),
            "region": "EU",
            "document_type": "policy",
            "status": "published",
        },
        {
            "document_id": "doc-3",
            "title": "US Draft Refund Policy Update",
            "text": (
                "Draft US policy about delayed delivery refunds. "
                "The draft explains the refund policy for delayed shipments and delivery issues."
            ),
            "region": "US",
            "document_type": "policy",
            "status": "draft",
        },
        {
            "document_id": "doc-4",
            "title": "US Published Blog: Delivery Refund Tips",
            "text": (
                "Published US blog post about delayed delivery refund tips. "
                "It discusses refund policy ideas, delivery delays, and customer stories."
            ),
            "region": "US",
            "document_type": "blog",
            "status": "published",
        },
        {
            "document_id": "doc-5",
            "title": "US Published Security Policy",
            "text": "Published US security policy about account protection and audit logs.",
            "region": "US",
            "document_type": "policy",
            "status": "published",
        },
    ]


def get_collection():
    """Create a fresh local Chroma collection for the demo."""
    client = chromadb.Client()
    collection_name = "metadata_filter_demo"

    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    return client.get_or_create_collection(name=collection_name)


def load_documents(collection, documents):
    """Store documents plus metadata in Chroma."""
    collection.add(
        ids=[document["document_id"] for document in documents],
        documents=[document["text"] for document in documents],
        metadatas=[
            {
                "title": document["title"],
                "region": document["region"],
                "document_type": document["document_type"],
                "status": document["status"],
            }
            for document in documents
        ],
    )


def query_collection(collection, query, metadata_filter=None, top_k=3):
    """Run one Chroma text query, optionally with metadata filters."""
    query_options = {
        "query_texts": [query],
        "n_results": top_k,
    }

    if metadata_filter is not None:
        query_options["where"] = metadata_filter

    return collection.query(**query_options)


def run_demo():
    """Show naive search first, then the same query with a Chroma metadata filter."""
    documents = build_demo_documents()
    query = "What is the refund policy for delayed delivery?"
    metadata_filter = {
        "region": "US",
        "document_type": "policy",
        "status": "published",
    }
    collection = get_collection()

    load_documents(collection, documents)

    print(f"Query: {query}")
    print(f"Metadata filter: {metadata_filter}")
    print()

    print("Documents in Chroma:")
    for document in documents:
        print(
            f"- {document['title']} "
            f"[region={document['region']}, type={document['document_type']}, status={document['status']}]"
        )
    print()

    naive_results = query_collection(collection, query)
    print("Naive Chroma results across all documents:")
    for metadata, distance in zip(naive_results["metadatas"][0], naive_results["distances"][0]):
        print(
            f"- {metadata['title']} | distance={distance:.3f} "
            f"[region={metadata['region']}, type={metadata['document_type']}, status={metadata['status']}]"
        )
    print()

    filtered_results = query_collection(
        collection,
        query,
        metadata_filter=metadata_filter,
    )
    print("Filtered Chroma results inside the allowed subset:")
    for metadata, distance in zip(filtered_results["metadatas"][0], filtered_results["distances"][0]):
        print(
            f"- {metadata['title']} | distance={distance:.3f} "
            f"[region={metadata['region']}, type={metadata['document_type']}, status={metadata['status']}]"
        )
    print()

    zero_result_filter = {
        "region": "PK",
        "document_type": "policy",
        "status": "published",
    }
    zero_result_results = query_collection(
        collection,
        query,
        metadata_filter=zero_result_filter,
    )

    print(f"Zero-result filter: {zero_result_filter}")
    if not zero_result_results["ids"][0]:
        print(
            "No documents matched the metadata filter. "
            "Ask for clarification or relax non-critical filters."
        )


if __name__ == "__main__":
    run_demo()
