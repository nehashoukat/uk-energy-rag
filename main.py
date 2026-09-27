import json
import os

from src.ingestion import ingest_pdfs_from_folder
from src.chunking import chunk_documents
from src.embeddings import generate_embeddings


OUTPUT_FILE = "./outputs/embedded_chunks.json"


if __name__ == "__main__":

    # Step 1: Ingest PDFs
    raw_pages = ingest_pdfs_from_folder("./data")

    if raw_pages:

        # Step 2: Chunk documents
        processed_chunks = chunk_documents(
            raw_pages,
            chunk_size=500,
            chunk_overlap=50
        )

        total_chunks = len(processed_chunks)

        # Step 3: Check whether previous embeddings were saved
        embedded_chunks = []

        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
                embedded_chunks = json.load(file)

            print(
                f"\nFound existing embeddings: "
                f"{len(embedded_chunks)} / {total_chunks}"
            )

        # Step 4: Determine what still needs embedding
        completed = len(embedded_chunks)

        if completed >= total_chunks:
            print("\nAll chunks are already embedded!")
        else:
            remaining_chunks = processed_chunks[completed:]

            remaining_texts = [
                chunk["text"]
                for chunk in remaining_chunks
            ]

            print(
                f"Embedding remaining "
                f"{len(remaining_texts)} chunks..."
            )

            # Step 5: Generate remaining embeddings
            for start, batch_embeddings in generate_embeddings(
                remaining_texts
            ):

                batch_chunks = remaining_chunks[
                    start:start + len(batch_embeddings)
                ]

                for chunk, embedding in zip(
                    batch_chunks,
                    batch_embeddings
                ):
                    embedded_chunks.append({
                        "text": chunk["text"],
                        "metadata": chunk["metadata"],
                        "embedding": embedding
                    })

                # Save after every successful batch
                with open(
                    OUTPUT_FILE,
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(
                        embedded_chunks,
                        file
                    )

                print(
                    f"Saved {len(embedded_chunks)} / "
                    f"{total_chunks} embedded chunks."
                )

            # Step 6: Final confirmation
            print("\nEmbedding pipeline complete!")

            print(
                f"Total embedded chunks: "
                f"{len(embedded_chunks)}"
            )

            print(
                f"Vector dimensions: "
                f"{len(embedded_chunks[0]['embedding'])}"
            )

            print(
                f"Saved to: {OUTPUT_FILE}"
            )