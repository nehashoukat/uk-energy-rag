import os
import time

from dotenv import load_dotenv
from google import genai


# Load API key from .env
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODEL_NAME = "gemini-3.8-flash"

def generate_answer(question, context):
    """Generate an answer using retrieved document context."""

    prompt = f"""
You are an assistant answering questions about the UK's electricity
system using the provided NESO documents.

Answer the user's question using ONLY the information provided
in the context below.

If the context does not contain enough information to answer the
question, say that the documents do not provide enough information.

Do not invent facts.

Context:
{context}

Question:
{question}

Answer:
"""

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            return response.text

        except Exception as e:

            if "503" in str(e) and attempt < 2:

                wait_time = 10 * (attempt + 1)

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise