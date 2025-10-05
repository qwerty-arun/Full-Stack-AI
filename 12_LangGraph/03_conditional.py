from typing_extensions import TypedDict
from typing import Optional, Literal 
from langgraph.graph import StateGraph, START, END
from google import genai

client = genai.Client(
    api_key=""
)

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    print("\n\nChatbot State", state)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=state.get("user_query"),
    )

    state["llm_output"] = response.candidates[0].content.parts[0].text
    return state

def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:

    if False: # toggle and check the workflow
        return "endnode"
    return "chatbot_gemini"

def endnode(state: State):
    print("\n\nEnd Node", state)
    return state

def chatbot_gemini(state: State):
    print("\n\nChatbot Gemini State", state)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=state.get("user_query"),
    )
    state["llm_output"] = response.candidates[0].content.parts[0].text
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)
graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "Hey, What is 2 + 2?"}))
print(updated_state)