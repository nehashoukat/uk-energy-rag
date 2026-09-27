from qdrant_client import QdrantClient

from src.embeddings import generate_embedding

# Connect to our local Qdrant database
client = QdrantClient(path="./outputs/qdrant_db")

COLLECTION_NAME = "neso_documents"


def search_documents(query, top_k=5):
    """Find the most relevant document chunks for a user query."""

    # Convert the user's question into an embedding
    query_vector = generate_embedding(query)

    # Search Qdrant for the closest vectors
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )

    return results.points


if __name__ == "__main__":

    query = "What is the NESO advice process and how does NESO provide advice to government?"
    results = search_documents(query, top_k=5)

    print(f"\nQuery: {query}")
    print(f"Retrieved {len(results)} chunks:\n")

    for i, result in enumerate(results, start=1):

        print(f"--- Result {i} ---")
        print(f"Similarity score: {result.score}")
        print(f"Source: {result.payload['metadata']['source']}")
        print(f"Page: {result.payload['metadata']['page']}")
        print(f"Chunk ID: {result.payload['metadata']['chunk_id']}")
        print(f"Text: {result.payload['text'][:500]}")
        print()
