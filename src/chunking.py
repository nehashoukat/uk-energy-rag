def chunk_documents(documents, chunk_size=500, chunk_overlap=50):
    """Splits large page texts into small, uniform paragraphs (chunks)."""
    print(f"\nStarting Text Chunking Pipeline (Size: {chunk_size}, Overlap: {chunk_overlap})...")
    all_chunks = []
    
    for doc in documents:
        text = doc["text"]
        metadata = doc["metadata"]
        
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_id"] = chunk_index
            
            all_chunks.append({
                "text": chunk_text,
                "metadata": chunk_metadata
            })
            
            start += (chunk_size - chunk_overlap)
            chunk_index += 1
            
    print(f"Chunking complete. Split {len(documents)} pages into {len(all_chunks)} unique vector chunks!")
    return all_chunks
