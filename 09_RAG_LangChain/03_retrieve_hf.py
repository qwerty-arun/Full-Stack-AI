from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

# 1. Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Connect to existing Qdrant collection
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",   # Qdrant running locally
    collection_name="learning_rag_hf",
    embedding=embedding_model
)

# 3. Take user input
user_query = input("Ask something: ")

# 4. Perform similarity search
search_results = vector_db.similarity_search(query=user_query, k=3)

# 5. Show results directly
print("\n🔎 Top matching chunks:\n")
for i, result in enumerate(search_results, 1):
    print(f"Result {i}:")
    print(f"Page Number: {result.metadata.get('page_label')}")
    print(f"Source File: {result.metadata.get('source')}")
    print(f"Content:\n{result.page_content[:500]}...\n")
