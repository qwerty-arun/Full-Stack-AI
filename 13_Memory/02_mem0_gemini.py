import os
from mem0 import Memory

os.environ["OPENAI_API_KEY"] = ""  # Used for embedding model
os.environ["GOOGLE_API_KEY"] = ""

config = {
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-2.0-flash-001",
            "temperature": 0.2,
            "max_tokens": 2000,
            "top_p": 1.0
        }
    }
}

m = Memory.from_config(config)

messages = [
    {"role": "user", "content": "I'm planning to watch a movie tonight. Any recommendations?"},
    {"role": "assistant", "content": "How about thriller movies? They can be quite engaging."},
    {"role": "user", "content": "I’m not a big fan of thrillers, but I love sci-fi movies."},
    {"role": "assistant", "content": "Got it! I'll avoid thrillers and suggest sci-fi movies instead."}
]

m.add(messages, user_id="alice", metadata={"category": "movies"})