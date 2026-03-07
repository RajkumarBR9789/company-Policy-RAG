# Company Policy RAG - Q&A Bot

An AI-powered Question & Answer application that lets you upload company policy documents (PDF) and ask questions about them using Retrieval-Augmented Generation (RAG).

**Live Demo:** [company-policy-rag.streamlit.app](https://company-policy-rag.streamlit.app/)

---

## Demo

https://github.com/RajkumarBR9789/company-Policy-RAG/raw/main/rag.mp4

---

## Architecture

```
PDF Upload --> PDF Loader --> Text Splitter --> Embeddings --> FAISS Vector DB
                                                                    |
User Question --> Embedding --> Similarity Search (FAISS) --> Top-K Chunks
                                                                    |
                                                         Groq LLaMA 3.3 70B
                                                                    |
                                                              Answer + Sources
```

---

## Tech Stack

| Component         | Technology                        |
|-------------------|-----------------------------------|
| Frontend          | Streamlit                         |
| LLM               | LLaMA 3.3 70B (via Groq API)      |
| Embeddings        | HuggingFace all-MiniLM-L6-v2      |
| Vector Database   | FAISS (Facebook AI Similarity Search) |
| Document Loader   | LangChain PyPDFLoader             |
| Text Splitting    | RecursiveCharacterTextSplitter    |
| Deployment        | Streamlit Community Cloud         |

---

## Features

- **PDF Upload** -- Upload any company policy document in PDF format
- **RAG Pipeline** -- Retrieval-Augmented Generation for accurate, context-based answers
- **Vector Database Display** -- Real-time stats showing pages, chunks, vectors, dimensions, and embedding model
- **Source Attribution** -- View the exact document chunks used to generate each answer
- **Dark Theme UI** -- Clean black and white minimal interface
- **Groq-Powered** -- Ultra-fast inference using Groq's LPU hardware

---

## Project Structure

```
company-Policy-RAG/
├── company_backend.py      # RAG pipeline: PDF processing, embeddings, FAISS, Groq LLM
├── company_frontend.py     # Streamlit UI: upload, query, display results
├── requirements.txt        # Python dependencies
├── .env                    # Local environment variables (not in repo)
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

---

## How It Works

1. **Document Processing** -- The uploaded PDF is parsed and split into chunks (1000 chars, 200 overlap)
2. **Embedding Generation** -- Each chunk is converted to a 384-dimensional vector using HuggingFace's all-MiniLM-L6-v2
3. **Vector Storage** -- Vectors are stored in a FAISS index for fast similarity search
4. **Query Processing** -- User's question is embedded and matched against stored vectors
5. **Answer Generation** -- Top 5 matching chunks are sent as context to LLaMA 3.3 70B via Groq API
6. **Response Display** -- Answer is shown with expandable source chunks and page numbers

---

## Setup (Local)

### Prerequisites

- Python 3.10+
- Groq API Key ([Get one here](https://console.groq.com/keys))

### Installation

```bash
# Clone the repository
git clone https://github.com/RajkumarBR9789/company-Policy-RAG.git
cd company-Policy-RAG

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_groq_api_key_here > .env

# Run the application
streamlit run company_frontend.py
```

The app will open at `http://localhost:8501`

---

## Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set **Main file path** to `company_frontend.py`
5. Add `GROQ_API_KEY` in **Settings > Secrets**
6. Deploy

---

## Configuration

| Parameter       | Value                  | Description                          |
|-----------------|------------------------|--------------------------------------|
| Chunk Size      | 1000 characters        | Size of each text chunk              |
| Chunk Overlap   | 200 characters         | Overlap between consecutive chunks   |
| Top-K Results   | 5                      | Number of similar chunks retrieved   |
| Max Tokens      | 1024                   | Maximum response length from LLM     |
| Embedding Model | all-MiniLM-L6-v2       | 384-dim sentence embeddings          |
| LLM Model       | llama-3.3-70b-versatile| Groq-hosted LLaMA model              |

---

## Screenshots

### Main Interface
> Upload a PDF and ask questions about company policies.

### Vector Database Stats
> Real-time display of FAISS index statistics in the sidebar.

### Answer with Sources
> AI-generated answers with expandable retrieved source chunks.

---

## Author

**Rajkumar BR**
- GitHub: [@RajkumarBR9789](https://github.com/RajkumarBR9789)

---

## License

This project is open source and available under the [MIT License](LICENSE).
