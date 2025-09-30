from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
# import os
# import sentence_transformers

# INDEXING

# pdf_path = "D:\Full-Stack-AI/09_RAG_LangChain/nodejs.pdf"
pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load() # page by page loading

# print(docs[12]) # read any page

# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400 
)

chunks = text_splitter.split_documents(documents=docs)
# print(chunks[10]) # print out particular chunks

# Vector Embeddings
# embedding_model = GoogleGenerativeAIEmbeddings(
#     model="models/gemini-embedding-001",
#     google_api_key=""
#     # google_api_key=os.getenv("GOOGLE_API_KEY")
# )

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag_hf",         # same name will delete stuff
    force_recreate = True # now create 384-d vectors
)

print("Indexing of documents done...")