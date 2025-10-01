from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

# 1. PDF path
pdf_path = Path(__file__).parent / "nodejs.pdf"

# 2. Load PDF
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()  # page by page

# 3. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)
chunks = text_splitter.split_documents(docs)

# 4. Embeddings model (Hugging Face)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 5. Qdrant vector store (recreate collection with correct dim)
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",   # Qdrant running locally
    collection_name="learning_rag_hf",
    force_recreate=True
)

print("✅ Indexing of documents done...")

# 6. Run a similarity search
query = "What is Node.js event loop?"
results = vector_store.similarity_search(query, k=3)

print("\n🔎 Top results:")
for i, doc in enumerate(results, 1):
    print(f"\nResult {i}:")
    print(doc.page_content[:300], "...")
