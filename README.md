# NESO Energy Knowledge Assistant

A retrieval augmented generation (RAG) system for answering questions about the UK's electricity system using NESO (National Energy System Operator) documents.

The project combines document processing, semantic embeddings, vector search, and large language model generation to produce answers grounded in the underlying source documents, with document and page metadata for traceability.

The project also includes a Streamlit interface for interactive question answering and a retrieval evaluation script for testing document-level retrieval relevance.

## Overview

Large energy system reports contain substantial amounts of technical information that can be difficult to search efficiently.

This project builds a domain specific question-answering system that allows users to ask natural language questions about NESO documents.

The system follows a retrieval augmented generation architecture:

```text
NESO PDF Documents
        │
        ▼
   PDF Ingestion
      PyMuPDF
        │
        ▼
     Chunking
  500 characters
   50 overlap
        │
        ▼
 Gemini Embeddings
        │
        ▼
 Qdrant Vector Database
        │
        │
 User Question
        ▼
 Query Embedding
        │
        ▼
 Semantic Retrieval
        │
        ▼
 Relevant Document Chunks
        │
        ▼
 Gemini Generation
        │
        ▼
 Grounded Answer
 + Source References
```

## Documents

The initial knowledge base contains three NESO publications:

* `NESO-Advice-Process-Document.pdf`
* `Forward-Work-Programme-2026-to-2027.pdf`
* `clean-flexibility-roadmap.pdf`

Together, these documents contain 120 pages of material.

The source PDFs are kept locally in:

```text
data/
```

They are not included in the GitHub repository.

## Technical Stack

* **Python** - application and data-processing logic
* **PyMuPDF** - PDF text extraction
* **Google Gemini** - text embeddings and answer generation
* **Qdrant** - local vector database
* **Streamlit** - interactive question-answering interface
* **python-dotenv** - environment variable management
* **JSON** - intermediate storage of generated embeddings

## RAG Pipeline

### 1. Document Ingestion

PDF files are read page by page using PyMuPDF.

For each page, the system extracts text and stores metadata including:

* source filename
* page number

This allows retrieved information to be traced back to the original document.

### 2. Text Chunking

Long page level text is divided into smaller chunks.

Current configuration:

```text
Chunk size: 500 characters
Overlap:    50 characters
```

The overlap helps preserve context when information spans the boundary between two chunks.

The 120 source pages produced:

```text
688 chunks
```

### 3. Embedding Generation

Each chunk is converted into a numerical vector using Google's Gemini embedding model.

The resulting embeddings have:

```text
3072 dimensions
```

The embedding pipeline is resumable. Generated embeddings are saved incrementally so that an interrupted run does not require previously completed embeddings to be regenerated.

### 4. Vector Storage

The embeddings are stored in a local Qdrant database.

Each vector contains:

* embedding
* document text
* source metadata
* page number
* chunk ID

### 5. Semantic Retrieval

When a user asks a question, the question is converted into an embedding using the same embedding model.

Qdrant then searches for the most semantically similar document chunks.

The current retrieval configuration returns the top 5 chunks.

### 6. Answer Generation

The retrieved chunks are passed to Gemini together with the user's question.

The generation prompt instructs the model to:

* answer using only the retrieved context
* avoid inventing information
* state when the available documents do not contain enough information

This creates a grounded generation step rather than asking the language model to answer entirely from its general knowledge.

## Streamlit Interface

The project includes a Streamlit interface for interactive question answering.

Run:

```bash
streamlit run app.py
```

The interface allows users to:

* enter natural-language questions
* view the generated answer
* inspect the retrieved source documents
* view similarity scores
* expand individual sources to view the retrieved text

This provides visibility into the retrieval step rather than presenting the generated answer as a black box.

## Project Structure

```text
RAG/
│
├── data/
│   └── NESO source PDFs
│
├── outputs/
│   ├── embedded_chunks.json
│   └── qdrant_db/
│
├── src/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retrieval.py
│   ├── generation.py
│   └── rag_pipeline.py
│
├── app.py
├── evaluation.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

Generated files in `outputs/` and environment secrets are excluded from version control.

## Installation

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

### macOS / Linux

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`:

```text
GEMINI_API_KEY=your_api_key_here
```

Add the NESO PDF documents to:

```text
data/
```

## Running the Pipeline

Generate document embeddings:

```bash
python main.py
```

The pipeline saves completed embeddings incrementally to:

```text
outputs/embedded_chunks.json
```

Build the Qdrant vector database:

```bash
python -m src.vector_store
```

## Testing Retrieval

Run:

```bash
python -m src.retrieval
```

This retrieves the most relevant chunks for the test question and displays:

* similarity score
* source document
* page number
* chunk ID
* retrieved text

## Running the RAG Pipeline

Run:

```bash
python -m src.rag_pipeline
```

The system retrieves relevant document chunks and passes them to Gemini to generate a grounded answer.

The output includes the generated answer and the source documents/pages used for retrieval.

## Evaluation

A small retrieval evaluation set was created using six questions covering the three source documents, plus one out of scope question.

The six in scope questions were evaluated against their expected source documents.

Evaluation result:

```text
Expected-document retrieval: 6/6
Out-of-scope question tested: Yes
```

The six in scope questions all returned the expected document as the top retrieved source during the evaluation run.

The out of scope test demonstrated that semantic retrieval can still return moderately similar document chunks even when the question is unrelated to the knowledge base. This highlights the importance of evaluating retrieval relevance and adding stronger confidence or relevance controls in future versions.

The evaluation measures document level retrieval relevance. It does not claim that generated answers are automatically factually correct.

Run the evaluation with:

```bash
python evaluation.py
```

## Example

Example question:

> What is the NESO advice process and how does NESO provide advice to government?

The system retrieves relevant sections from the NESO advice process document and uses those retrieved passages as context for answer generation.

The Streamlit interface displays the generated answer together with the retrieved source documents, pages, similarity scores, and retrieved text.

## Limitations

This is a portfolio-scale RAG system rather than a production deployment.

Current limitations include:

* The knowledge base is limited to three documents.
* The vector database is stored locally.
* Retrieval currently uses a fixed top-k semantic search.
* No external web search is performed during answering.
* The system does not currently use reranking or hybrid keyword/vector retrieval.
* Semantic retrieval can return moderately similar chunks for questions outside the knowledge base.
* Answer quality depends partly on the quality and coverage of the retrieved chunks.
* The application has not been designed as a production-scale multi-user service.

## Future Improvements

Potential extensions include:

* Hybrid keyword and semantic retrieval
* Reranking retrieved documents
* Improved chunking strategies
* Stronger retrieval and generation evaluation
* Improved citation display
* Confidence or relevance thresholds for out-of-scope questions
* Cloud-hosted vector storage
* Automated evaluation of retrieval and generation quality
* Deployment as a hosted application

## Key Learning Outcomes

This project demonstrates practical experience with:

* Retrieval-augmented generation
* Document processing
* Text chunking
* Vector embeddings
* Semantic search
* Vector databases
* LLM prompting
* API integration
* Metadata-based source tracing
* Resumable data-processing pipelines
* Interactive application development with Streamlit
* Retrieval evaluation
* Environment-variable and API-key management


