#pip install groq
#pip install pypdf
#pip install faiss-cpu
#pip install python-dotenv
#pip install sentence-transformers

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS 
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq

load_dotenv()

# Get API key from Streamlit secrets (cloud) or .env (local)
try:
    import streamlit as st
    api_key = st.secrets.get("GROQ_API_KEY", None) or os.getenv("GROQ_API_KEY")
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
groq_client = None
if api_key:
    groq_client = Groq(api_key=api_key)

def company_pdf_from_file(file_path):
    """Load PDF from uploaded file and return index + stats"""
    data_load = PyPDFLoader(file_path)
    documents = data_load.load()
    
    pdf_split = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=1000,
        chunk_overlap=200
    )
    split_docs = pdf_split.split_documents(documents)
    
    pdf_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db_index = FAISS.from_documents(split_docs, pdf_embedding)
    
    # Return index and vector DB stats
    stats = {
        "total_pages": len(documents),
        "total_chunks": len(split_docs),
        "vector_count": db_index.index.ntotal,
        "embedding_dim": db_index.index.d,
        "index_type": "FAISS (Flat L2)",
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size": 1000,
        "chunk_overlap": 200,
    }
    return db_index, stats

def company_llm(context, question):
    """Use Groq API to generate response"""
    prompt = f"""You are a helpful assistant that answers questions based on the provided document context.

Document Context:
{context}

User Question: {question}

Instructions:
- Answer the question using ONLY the information from the document context above.
- If the context contains relevant information, provide a clear and detailed answer.
- If the context does not contain enough information to answer, say so.
- Be concise but thorough.

Answer:"""
    
    message = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return message.choices[0].message.content

def company_rag_response(index, question):
    relevant_docs = index.similarity_search(question, k=5)
    context = "\n\n---\n\n".join([doc.page_content for doc in relevant_docs])
    response = company_llm(context, question)
    return response, relevant_docs
