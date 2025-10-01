from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from transformers import pipeline

# 1. Load embeddings model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Connect to existing Qdrant collection
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",   # Qdrant running locally
    collection_name="learning_rag_hf",
    embedding=embedding_model
)

# 3. Load a HuggingFace text generation model (choose a small one for local use)
# Example: distilgpt2 (small) OR "mistralai/Mistral-7B-Instruct" if you have GPU
generator = pipeline("text-generation", model="distilgpt2")

# 4. Take user input
user_query = input("Ask something: ")

# 5. Retrieve top matching chunks
search_results = vector_db.similarity_search(query=user_query, k=3)

# 6. Build context
context = "\n\n".join([res.page_content for res in search_results])

prompt = f"""
You are a helpful AI Assistant. Answer the question based only on the provided context.

Context:
{context}

Question: {user_query}

Answer:
"""

# 7. Generate answer using HuggingFace model
response = generator(prompt, max_length=512, do_sample=True, temperature=0.7)

print("\n🤖 Answer:")
print(response[0]["generated_text"])
