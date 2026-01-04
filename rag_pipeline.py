from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def build_vectorstore(
    text: str,
    persist_dir: str = "vector_db",
    chunk_size: int = 500,
    chunk_overlap: int = 100
):
    """
    Builds a vector database for Retrieval-Augmented Generation (RAG).

    Parameters:
    - text (str): Raw text to be indexed (e.g., readme.htm or filing text)
    - persist_dir (str): Directory to store vector DB
    - chunk_size (int): Size of text chunks
    - chunk_overlap (int): Overlap between chunks

    Returns:
    - vectorstore (Chroma): Vector database object
    """

    # -----------------------------
    # 1. Chunk the text
    # -----------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_text(text)

    print(f"🔹 Total chunks created: {len(chunks)}")

    # -----------------------------
    # 2. Create embeddings
    # -----------------------------
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # -----------------------------
    # 3. Create / Load vector store
    # -----------------------------
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    vectorstore.persist()

    print(f"✅ Vector store created at '{persist_dir}'")

    return vectorstore
