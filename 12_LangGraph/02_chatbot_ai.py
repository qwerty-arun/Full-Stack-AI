import os
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model

os.environ["GOOGLE_API_KEY"] = ""

llm = init_chat_model("google_genai:gemini-2.0-flash")

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}

def sample_node(state: State):
    print("\n\nInside smaple_node node", state)
    return {"messages": ["Sample message appended"]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample_node", sample_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sample_node")
graph_builder.add_edge("sample_node", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi, Arun Here!"]}))
print("\n\nupdated_state", updated_state)

# (START -> chatbot -> sample_node -> END)

# state = { "messages" : ["Hey there"]}
# node runs: chatbot(state: ["Hey There"]) -> ["Hi, this is a message from ChatBot Node"]
# state = { "messages" : ["Hey there", "Hi, this a message from ChatBot Node"]}
# state = { "messages" : ["Hey there", "Hi, this a message from ChatBot Node", "Sample message appended"]}