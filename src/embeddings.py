import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-embedding-001"


def generate_embedding(text):
    """Convert one piece of text into a numerical embedding vector."""

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=text
    )

    return response.embeddings[0].values


def generate_embeddings(texts, batch_size=50):
    """Generate embeddings in batches and yield each completed batch."""

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]

        print(
            f"Embedding batch {start + 1}-"
            f"{min(start + batch_size, len(texts))} "
            f"of {len(texts)}..."
        )

        while True:
            try:
                response = client.models.embed_content(
                    model=MODEL_NAME,
                    contents=batch
                )

                batch_embeddings = [
                    embedding.values
                    for embedding in response.embeddings
                ]

                yield start, batch_embeddings
                break

            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print(
                        "Quota reached. "
                        "Waiting 35 seconds before retrying..."
                    )
                    time.sleep(35)
                else:
                    raise