import os
import glob
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

DOCS_DIR = "docs"
DB_DIR = "db"
COLLECTION_NAME = "docs"

def read_texts_from_docs():
    texts, metadatas = [], []
    # PDFs
    for pdf_path in glob.glob(os.path.join(DOCS_DIR, "*.pdf")):
        reader = PdfReader(pdf_path)
        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages)
        texts.append(text)
        metadatas.append({"source": os.path.basename(pdf_path)})
    # TXT / MD
    for txt_path in glob.glob(os.path.join(DOCS_DIR, "*.txt")) + glob.glob(os.path.join(DOCS_DIR, "*.md")):
        with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        texts.append(text)
        metadatas.append({"source": os.path.basename(txt_path)})
    return texts, metadatas

def chunk_text(text, chunk_size=700, overlap=120):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += max(1, chunk_size - overlap)
    return chunks

def main():
    os.makedirs(DB_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=DB_DIR)
    embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedder)

    texts, metas = read_texts_from_docs()
    if not texts:
        print(f"No docs found in '{DOCS_DIR}'. Add PDFs/TXTs and rerun.")
        return

    doc_id = 0
    for text, meta in zip(texts, metas):
        for chunk in chunk_text(text):
            collection.add(documents=[chunk], metadatas=[meta], ids=[f"doc-{doc_id}"])
            doc_id += 1

    print(f"Ingested {doc_id} chunks into Chroma at '{DB_DIR}'.")

if __name__ == "__main__":
    main()
