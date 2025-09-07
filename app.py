import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import os, subprocess

# Auto-ingest if DB is empty
if not os.path.exists("db") or not os.listdir("db"):
    os.makedirs("db", exist_ok=True)
    try:
        subprocess.run(["python", "ingest.py"], check=True)
        print("Ingested docs automatically at startup.")
    except Exception as e:
        print("Ingestion failed:", e)


DB_DIR = "db"
COLLECTION_NAME = "docs"

@st.cache_resource
def get_retriever():
    client = chromadb.PersistentClient(path=DB_DIR)
    embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    col = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedder)
    return col

@st.cache_resource
def get_generator():
    model_name = "google/flan-t5-small"
    tok = AutoTokenizer.from_pretrained(model_name)
    mdl = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    gen = pipeline("text2text-generation", model=mdl, tokenizer=tok)
    return gen

def make_prompt(context, question):
    return (
        "Answer the question using ONLY the context below. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )

st.set_page_config(page_title="RAG: Chat with Your Docs", page_icon="💬")
st.title("💬 Chat with Your Documents (Local RAG)")

query = st.text_input("Ask a question about your documents:")
top_k = st.slider("Top K", min_value=2, max_value=10, value=4, step=1)

if st.button("Search & Answer") and query.strip():
    col = get_retriever()
    res = col.query(query_texts=[query], n_results=top_k)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]

    if not docs:
        st.warning("No results. Did you run `python ingest.py` after adding files to docs/?")
    else:
        context = "\n\n".join(docs)
        gen = get_generator()
        prompt = make_prompt(context, query)
        out = gen(prompt, max_new_tokens=256)[0]["generated_text"]

        st.subheader("Answer")
        st.write(out)

        st.subheader("Sources")
        for m in metas:
            st.write("-", m.get("source", "unknown"))
