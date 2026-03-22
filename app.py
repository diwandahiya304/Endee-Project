import os
os.environ['no_proxy'] = '127.0.0.1,localhost'
os.environ['NO_PROXY'] = '127.0.0.1,localhost'

import streamlit as st
from pdf_utils import extract_text_from_pdf, chunk_text
from embedder import embed_texts, embed_single
from db_utils import create_index_if_not_exists, store_chunks, search_similar, delete_index
from qa_engine import answer_question

st.set_page_config(
    page_title="DocQA — Powered by Endee",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Document Q&A")
st.caption("Upload a PDF and ask any question about it — powered by Endee vector DB")

st.header("1. Upload your document")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    if st.button("Process Document"):
        with st.spinner("Reading and indexing your document..."):
            text = extract_text_from_pdf(uploaded_file)
            st.info(f"Extracted {len(text)} characters from the PDF.")
            chunks = chunk_text(text)
            st.info(f"Split into {len(chunks)} chunks.")
            embeddings = embed_texts(chunks)
            delete_index()
            create_index_if_not_exists()
            store_chunks(chunks, embeddings)
            st.session_state["doc_loaded"] = True
        st.success("Document indexed! You can now ask questions.")

if st.session_state.get("doc_loaded"):
    st.header("2. Ask a question")
    question = st.text_input("Type your question here...")

    if question:
        with st.spinner("Searching for relevant passages..."):
            q_embedding = embed_single(question)
            results = search_similar(q_embedding, top_k=5)

            retrieved_chunks = []
            for r in results:
                if isinstance(r, dict):
                    chunk_text_val = r.get('meta', {}).get('text', '')
                else:
                    chunk_text_val = r.meta.get('text', '') if hasattr(r, 'meta') else ''
                if chunk_text_val:
                    retrieved_chunks.append(chunk_text_val)

        with st.spinner("Generating answer..."):
            answer = answer_question(question, retrieved_chunks)

        st.subheader("Answer")
        st.write(answer)

        with st.expander("View source passages from document"):
            for i, chunk in enumerate(retrieved_chunks, 1):
                st.markdown(f"**Passage {i}:**")
                st.text(chunk[:300] + "..." if len(chunk) > 300 else chunk)
                st.divider()