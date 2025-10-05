import os
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from google import genai

# --- Initialize Gemini client ---
client = genai.Client(api_key="")


# --- Define the state structure ---
class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

# --- Node 1: Ask Gemini a question ---
def chatbot(state: State):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=state["user_query"],
    )
    output = response.candidates[0].content.parts[0].text
    state["llm_output"] = output
    print(f"💬 Chatbot (gemini-2.0-flash) output: {output}")
    return state

# --- Decision node: Check if Gemini’s response is good ---
def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    output = (state.get("llm_output") or "").lower()
    # output = "5"

    # Simple logic: if the response seems correct for a math query, we stop
    if "4" in output or "four" in output:
        print("✅ Response seems correct — ending flow.")
        state["is_good"] = True
        return "endnode"
    
    # Otherwise, try again with another prompt
    print("⚠️ Response not confident — retrying with gemini-2.5-flash")
    state["is_good"] = False
    return "chatbot_gemini"

# --- Node 2: Retry or enhance response ---
def chatbot_gemini(state: State):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Be more clear and accurate: {state['user_query']}",
    )
    output = response.candidates[0].content.parts[0].text
    state["llm_output"] = output
    print(f"🔁 Refined output (gemini-2.5-flash): {output}")
    return state

# --- End node ---
def endnode(state: State):
    print("🏁 Flow ended.")
    return state

# --- Build graph ---
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)
graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

# --- Run graph ---
updated_state = graph.invoke(State({"user_query": "Hey, what is 2 + 2?"}))
print("\nFinal state:", updated_state)
