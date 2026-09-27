import streamlit as st


st.set_page_config(
    page_title="NESO Energy Knowledge Assistant",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ NESO Energy Knowledge Assistant")

st.write(
    "Ask questions about the UK's electricity system "
    "using information from NESO documents."
)

question = st.text_input(
    "Enter your question:",
    placeholder="e.g. What is the NESO advice process?"
)

if st.button("Ask"):

    if question.strip():

        from src.rag_pipeline import answer_question

        with st.spinner(
            "Searching NESO documents and generating an answer..."
        ):

            answer, results = answer_question(question)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources")

        for i, result in enumerate(results, start=1):

            metadata = result.payload["metadata"]

            source = metadata["source"]
            page = metadata["page"]
            score = result.score
            text = result.payload["text"]

            with st.expander(
                f"Source {i}: {source} — Page {page}"
            ):

                st.write(f"**Similarity score:** {score:.3f}")

                st.write("**Retrieved text:**")

                st.write(text)

    else:
        st.warning("Please enter a question.")