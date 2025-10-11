import os
from dotenv import load_dotenv
from google import genai
from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct, VectorParams, Distance,
    Filter, FieldCondition, MatchValue, Vector, SearchRequest
)
from neo4j import GraphDatabase
from qdrant_client import models

# ---------------------------
# 🔧 LOAD ENVIRONMENT
# ---------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD", "password")

COLLECTION_NAME = "user_memories"

# ---------------------------
# 🔧 INITIALIZE CLIENTS
# ---------------------------

# Google GenAI
genai_client = genai.Client(api_key=GOOGLE_API_KEY)

# Qdrant
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Delete collection if exists (to avoid vector size mismatch)
if COLLECTION_NAME in [col.name for col in qdrant.get_collections().collections]:
    qdrant.delete_collection(collection_name=COLLECTION_NAME)
    print(f"Deleted existing collection '{COLLECTION_NAME}'.")

# Create collection with vector size 768 - matches your embedding size
qdrant.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)
print(f"Created collection '{COLLECTION_NAME}' with vector size 768.")

# Neo4j
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

# ---------------------------
# 🧠 FUNCTIONS
# ---------------------------

def get_embedding(text: str):
    """Generate embedding using Google GenAI"""
    response = genai_client.models.embed_content(
        model="text-embedding-004",
        contents=[text]
    )
    return response.embeddings[0].values

def add_memory_to_qdrant(user_id, memory_text):
    embedding = get_embedding(memory_text)
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=None,
                vector=embedding,
                payload={"user_id": user_id, "memory": memory_text}
            )
        ]
    )
    return embedding

def search_memory_from_qdrant(user_id, query_text, limit=5):
    query_vector = get_embedding(query_text)
    
    search_request = SearchRequest(
        vector=Vector(values=query_vector),
        filter=Filter(
            must=[FieldCondition(key="user_id", match=MatchValue(value=user_id))]
        ),
        limit=limit
    )
    results = qdrant.search(collection_name=COLLECTION_NAME, search_request=search_request)
    return [point.payload for point in results.points]

def store_memory_in_neo4j(user_id, query_text, response_text):
    with neo4j_driver.session() as session:
        session.run("""
            MERGE (u:User {id: $user_id})
            CREATE (m:Memory {query: $query, response: $response, timestamp: timestamp()})
            MERGE (u)-[:HAS_MEMORY]->(m)
        """, user_id=user_id, query=query_text, response=response_text)

def retrieve_user_memory_graph(user_id, limit=5):
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (u:User {id: $user_id})-[:HAS_MEMORY]->(m:Memory)
            RETURN m.query AS query, m.response AS response
            ORDER BY m.timestamp DESC
            LIMIT $limit
        """, user_id=user_id, limit=limit)
        return [{"query": r["query"], "response": r["response"]} for r in result]

# ---------------------------
# 💬 MAIN LOOP
# ---------------------------

USER_ID = "arun"
print("System Ready — Neo4j + Qdrant + Google GenAI Connected.\n")

while True:
    user_query = input("> ")

    # 1️⃣ Search similar memories from Qdrant
    qdrant_results = search_memory_from_qdrant(USER_ID, user_query)
    qdrant_context = "\n".join([f"- {m['memory']}" for m in qdrant_results])

    # 2️⃣ Retrieve latest memories from Neo4j
    neo4j_results = retrieve_user_memory_graph(USER_ID)
    neo4j_context = "\n".join([f"Q: {m['query']} → A: {m['response']}" for m in neo4j_results])

    # 3️⃣ Prepare system prompt
    SYSTEM_PROMPT = f"""
The user has these past memories (from vector + graph):

[Vector Memory]
{qdrant_context}

[Graph Memory]
{neo4j_context}
"""

    # 4️⃣ Ask Gemini LLM
    response = genai_client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            {"role": "system", "parts": [SYSTEM_PROMPT]},
            {"role": "user", "parts": [user_query]}
        ]
    )

    ai_response = response.text
    print("AI:", ai_response, "\n")

    # 5️⃣ Save memory in Qdrant + Neo4j
    add_memory_to_qdrant(USER_ID, f"{user_query} -> {ai_response}")
    store_memory_in_neo4j(USER_ID, user_query, ai_response)

    print("Memory updated in Qdrant + Neo4j ✅\n")
