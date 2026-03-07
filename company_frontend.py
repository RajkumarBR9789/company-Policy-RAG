import streamlit as st
import company_backend as brain
import os

# --- Page Config ---
st.set_page_config(
    page_title="Company Policy RAG",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Black & White Theme CSS ---
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #2a2a2a;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffffff !important;
    }

    /* Text area */
    .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        border: 1px solid #333333 !important;
        border-radius: 4px;
    }

    /* Buttons */
    .stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 4px;
        font-weight: 600;
        padding: 0.5rem 2rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #cccccc !important;
        color: #000000 !important;
    }

    /* File uploader */
    .stFileUploader {
        background-color: #1a1a1a;
        border: 1px dashed #333333;
        border-radius: 4px;
    }
    .stFileUploader section {
        background-color: #1a1a1a !important;
        color: #aaaaaa !important;
    }
    .stFileUploader section > button {
        background-color: #222222 !important;
        color: #cccccc !important;
        border: 1px solid #444444 !important;
    }
    .stFileUploader section > div {
        color: #888888 !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background-color: #141414 !important;
        border: 1px dashed #333333 !important;
        color: #888888 !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #222222 !important;
        color: #cccccc !important;
        border: 1px solid #444444 !important;
    }
    [data-testid="stFileUploaderDropzone"] small {
        color: #555555 !important;
    }
    [data-testid="stFileUploaderFile"] {
        background-color: #1a1a1a !important;
        color: #cccccc !important;
    }

    /* Top header bar */
    header[data-testid="stHeader"] {
        background-color: #0a0a0a !important;
        border-bottom: 1px solid #1a1a1a;
    }
    [data-testid="stToolbar"] {
        background-color: #0a0a0a !important;
    }
    [data-testid="stDecoration"] {
        display: none !important;
    }
    /* Deploy button */
    [data-testid="stToolbar"] button {
        color: #555555 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        background-color: #0a0a0a;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #333333;
        border-radius: 3px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #141414;
        border: 1px solid #2a2a2a;
        border-radius: 6px;
        padding: 12px 16px;
    }
    div[data-testid="stMetric"] label {
        color: #888888 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #141414 !important;
        color: #e0e0e0 !important;
        border: 1px solid #2a2a2a;
        border-radius: 4px;
    }

    /* Divider */
    hr {
        border-color: #2a2a2a !important;
    }

    /* Status box styles */
    .status-box {
        background-color: #141414;
        border: 1px solid #2a2a2a;
        border-radius: 6px;
        padding: 16px;
        margin: 8px 0;
    }
    .status-ready {
        border-left: 3px solid #ffffff;
    }
    .status-waiting {
        border-left: 3px solid #555555;
    }
    .answer-box {
        background-color: #141414;
        border: 1px solid #2a2a2a;
        border-radius: 6px;
        padding: 20px;
        margin: 12px 0;
        line-height: 1.6;
    }
    .source-box {
        background-color: #0f0f0f;
        border: 1px solid #222222;
        border-radius: 4px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 13px;
        color: #aaaaaa;
        font-family: monospace;
    }
    .header-line {
        width: 60px;
        height: 2px;
        background-color: #ffffff;
        margin: 4px 0 20px 0;
    }
    .sidebar-section-title {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #666666;
        margin-bottom: 12px;
    }
    .db-stat-row {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        border-bottom: 1px solid #1a1a1a;
        font-size: 13px;
    }
    .db-stat-label {
        color: #666666;
    }
    .db-stat-value {
        color: #ffffff;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'vector_index' not in st.session_state:
    st.session_state.vector_index = None
if 'db_stats' not in st.session_state:
    st.session_state.db_stats = None
if 'doc_name' not in st.session_state:
    st.session_state.doc_name = None

# =====================
#       SIDEBAR
# =====================
with st.sidebar:
    st.markdown("## Company Policy RAG")
    st.markdown('<div class="header-line"></div>', unsafe_allow_html=True)

    # --- Document Upload ---
    st.markdown('<div class="sidebar-section-title">Document Upload</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")

    if uploaded_file is not None:
        if st.session_state.doc_name != uploaded_file.name:
            with open("temp_pdf.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Processing document..."):
                index, stats = brain.company_pdf_from_file("temp_pdf.pdf")
                st.session_state.vector_index = index
                st.session_state.db_stats = stats
                st.session_state.doc_name = uploaded_file.name

    # --- Document Status ---
    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">Document Status</div>', unsafe_allow_html=True)

    if st.session_state.doc_name:
        st.markdown(f"""
        <div class="status-box status-ready">
            <div style="color:#ffffff; font-weight:600; margin-bottom:4px;">Loaded</div>
            <div style="color:#888888; font-size:13px;">{st.session_state.doc_name}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-box status-waiting">
            <div style="color:#888888; font-weight:600;">No document loaded</div>
            <div style="color:#555555; font-size:13px;">Upload a PDF to begin</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Vector Database Info ---
    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">Vector Database</div>', unsafe_allow_html=True)

    if st.session_state.db_stats:
        stats = st.session_state.db_stats
        st.markdown(f"""
        <div class="status-box status-ready">
            <div class="db-stat-row">
                <span class="db-stat-label">Index Type</span>
                <span class="db-stat-value">{stats['index_type']}</span>
            </div>
            <div class="db-stat-row">
                <span class="db-stat-label">Pages</span>
                <span class="db-stat-value">{stats['total_pages']}</span>
            </div>
            <div class="db-stat-row">
                <span class="db-stat-label">Chunks</span>
                <span class="db-stat-value">{stats['total_chunks']}</span>
            </div>
            <div class="db-stat-row">
                <span class="db-stat-label">Vectors</span>
                <span class="db-stat-value">{stats['vector_count']}</span>
            </div>
            <div class="db-stat-row">
                <span class="db-stat-label">Dimensions</span>
                <span class="db-stat-value">{stats['embedding_dim']}</span>
            </div>
            <div class="db-stat-row">
                <span class="db-stat-label">Embedding</span>
                <span class="db-stat-value">{stats['embedding_model']}</span>
            </div>
            <div class="db-stat-row">
                <span class="db-stat-label">Chunk Size</span>
                <span class="db-stat-value">{stats['chunk_size']}</span>
            </div>
            <div class="db-stat-row" style="border-bottom:none;">
                <span class="db-stat-label">Overlap</span>
                <span class="db-stat-value">{stats['chunk_overlap']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-box status-waiting">
            <div style="color:#555555; font-size:13px;">No vector database created</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Model Info ---
    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">Model</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="status-box" style="border-left: 3px solid #333333;">
        <div class="db-stat-row">
            <span class="db-stat-label">LLM</span>
            <span class="db-stat-value">LLaMA 3.3 70B</span>
        </div>
        <div class="db-stat-row" style="border-bottom:none;">
            <span class="db-stat-label">Provider</span>
            <span class="db-stat-value">Groq</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================
#      MAIN CONTENT
# =====================

# Header
st.markdown("# Company Policy Q&A")
st.markdown('<div class="header-line"></div>', unsafe_allow_html=True)

if st.session_state.vector_index is None:
    st.markdown("""
    <div class="status-box status-waiting" style="text-align:center; padding:40px;">
        <div style="color:#666666; font-size:16px; margin-bottom:8px;">Upload a document to get started</div>
        <div style="color:#444444; font-size:13px;">Use the sidebar to upload your company policy PDF</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Query input
    input_text = st.text_area(
        "Enter your question",
        placeholder="Type your question about the company policy...",
        label_visibility="collapsed",
        height=100
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        go_button = st.button("Ask", type="primary", use_container_width=True)

    if go_button and input_text:
        with st.spinner("Searching and generating answer..."):
            response_content, source_docs = brain.company_rag_response(
                index=st.session_state.vector_index,
                question=input_text
            )

        # Answer
        st.markdown("### Answer")
        st.markdown(f'<div class="answer-box">{response_content}</div>', unsafe_allow_html=True)

        # Retrieved Sources
        with st.expander("Retrieved Sources", expanded=False):
            for i, doc in enumerate(source_docs, 1):
                page = doc.metadata.get("page", "N/A")
                st.markdown(f"""
                <div class="source-box">
                    <span style="color:#666666;">Chunk {i} | Page {page}</span><br/>
                    {doc.page_content}
                </div>
                """, unsafe_allow_html=True)

    elif go_button and not input_text:
        st.warning("Please enter a question.")