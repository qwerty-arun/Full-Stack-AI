import os
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

os.environ["GOOGLE_API_KEY"] = ""

llm = init_chat_model("google_genai:gemini-2.0-flash")

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

DB_URI = "mongodb://admin:admin@localhost:27017"

with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)

    # change the thread and see what happens
    config = {
        "configurable": {
            "thread_id": "arun" # we can have multiple users
        }
    }

    for chunk in graph_with_checkpointer.stream(
        State({"messages": ["Hey, what am I learning now?"]}),
        config,
        stream_mode="values",
        ):
        chunk["messages"][-1].pretty_print()

# START -> (chatbot) -> END
# checkpointer (arun) = Hey, my name is Arun
# Restart App
# START -> "What is my name?"
# Response (expected): "You name is Arun."