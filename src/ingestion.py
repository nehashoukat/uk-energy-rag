import os
import fitz  # PyMuPDF

def ingest_pdfs_from_folder(folder_path="./data"):
    """Reads all PDF files in the target folder and extracts their text page by page."""
    print(f"Starting Ingestion Pipeline looking at: '{folder_path}'")
    
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return []
        
    all_documents = []
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_name}")
            
            try:
                doc = fitz.open(file_path)
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    page_text = page.get_text("text")
                    clean_text = " ".join(page_text.split())
                    
                    if clean_text:
                        all_documents.append({
                            "text": clean_text,
                            "metadata": {
                                "source": file_name,
                                "page": page_num + 1
                            }
                        })
                print(f"Successfully ingested {len(doc)} pages from {file_name}")
            except Exception as e:
                print(f"Failed to process {file_name}. Error: {e}")
                
    print(f"Pipeline Ingestion complete. Total system pages loaded: {len(all_documents)}")
    return all_documents
