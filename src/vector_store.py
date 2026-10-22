import json

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct



client = QdrantClient(path="./outputs/qdrant_db")

COLLECTION_NAME = "neso_documents"



with open(
    "./outputs/embedded_chunks.json",
    "r",
    encoding="utf-8"
) as file:
    embedded_chunks = json.load(file)


print(f"Loaded {len(embedded_chunks)} embedded chunks.")



points = []

for index, chunk in enumerate(embedded_chunks):

    points.append(
        PointStruct(
            id=index,
            vector=chunk["embedding"],
            payload={
                "text": chunk["text"],
                "metadata": chunk["metadata"]
            }
        )
    )



client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)


print(
    f"Successfully inserted "
    f"{len(points)} vectors into Qdrant!"
)