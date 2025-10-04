from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",   # Qdrant running locally
    collection_name="learning_rag_hf",
    embedding=embedding_model
)

def process_query(query: str):
    print("Searching Chunks", query)
    search_results = vector_db.similarity_search(query=query, k=3)
    print(f"🤖: {search_results}")
    return search_results