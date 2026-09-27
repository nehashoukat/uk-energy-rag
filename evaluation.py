from src.retrieval import search_documents


TEST_CASES = [
    {
        "question": "What is the NESO advice process?",
        "expected_source": "NESO-Advice-Process-Document.pdf",
    },
    {
        "question": "What role does NESO play in providing advice to government?",
        "expected_source": "NESO-Advice-Process-Document.pdf",
    },
    {
        "question": "What is the purpose of the Forward Work Programme?",
        "expected_source": "Forward-Work-Programme-2026-to-2027.pdf",
    },
    {
        "question": "What is clean flexibility and why is it important?",
        "expected_source": "clean-flexibility-roadmap.pdf",
    },
    {
        "question": "What does NESO say about flexibility in the electricity system?",
        "expected_source": "clean-flexibility-roadmap.pdf",
    },
    {
        "question": "What is the role of flexibility in managing the electricity system?",
        "expected_source": "clean-flexibility-roadmap.pdf",
    },
]


OUT_OF_SCOPE_QUESTION = (
    "Who is the current Prime Minister of the United Kingdom?"
)


if __name__ == "__main__":

    print("NESO RAG Retrieval Evaluation")
    print("=" * 60)

    passed_tests = 0

    for i, test_case in enumerate(TEST_CASES, start=1):

        question = test_case["question"]
        expected_source = test_case["expected_source"]

        print(f"\nTest {i}")
        print(f"Question: {question}")

        results = search_documents(question, top_k=5)

        top_result = results[0]
        top_source = top_result.payload["metadata"]["source"]

        if top_source == expected_source:
            passed_tests += 1
            status = "PASS"
        else:
            status = "CHECK"

        print(f"Expected source: {expected_source}")
        print(f"Top retrieved source: {top_source}")
        print(f"Top similarity score: {top_result.score:.3f}")
        print(f"Status: {status}")

        print("\nTop retrieved sources:")

        for rank, result in enumerate(results, start=1):

            metadata = result.payload["metadata"]

            print(
                f"{rank}. "
                f"{metadata['source']} "
                f"(page {metadata['page']}) "
                f"score={result.score:.3f}"
            )

    print("\n" + "=" * 60)
    print("Out-of-scope test")
    print(f"Question: {OUT_OF_SCOPE_QUESTION}")

    results = search_documents(
        OUT_OF_SCOPE_QUESTION,
        top_k=5
    )

    print("\nTop retrieved result:")

    top_result = results[0]
    metadata = top_result.payload["metadata"]

    print(
        f"{metadata['source']} "
        f"(page {metadata['page']}) "
        f"score={top_result.score:.3f}"
    )

    print("\n" + "=" * 60)
    print("Evaluation Summary")
    print("=" * 60)

    print(
        f"Expected-document retrieval: "
        f"{passed_tests}/{len(TEST_CASES)}"
    )

    print("Out-of-scope question tested: Yes")

    print(
        "\nNote: This evaluation measures retrieval relevance "
        "based on expected source documents. It does not "
        "measure the factual accuracy of generated answers."
    )