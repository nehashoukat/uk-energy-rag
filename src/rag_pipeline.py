from src.retrieval import search_documents
from src.generation import generate_answer


def answer_question(question, top_k=5):
    """Retrieve relevant documents and generate a grounded answer."""

    
    results = search_documents(question, top_k=top_k)

    
    context_parts = []

    for result in results:
        source = result.payload["metadata"]["source"]
        page = result.payload["metadata"]["page"]
        text = result.payload["text"]

        context_parts.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Text: {text}"
        )

    context = "\n\n---\n\n".join(context_parts)

    
    answer = generate_answer(question, context)

    return answer, results


if __name__ == "__main__":

    question = "What is the NESO advice process and how does NESO provide advice to government?"
    answer, results = answer_question(question)

    print("\nQUESTION:")
    print(question)

    print("\nANSWER:")
    print(answer)

    print("\nSOURCES:")

    for result in results:
        metadata = result.payload["metadata"]

        print(
            f"- {metadata['source']}, "
            f"page {metadata['page']}"
        )