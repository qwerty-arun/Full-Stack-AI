from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional
import requests
import json

client = genai.Client(
    api_key=''
)

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    else:
        return f"Failed to fetch weather."

available_tools = {
    "get_weather": get_weather
}

SYSTEM_PROMPT = """
    You are an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN AND OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to be displayed to the user).
    - You can also call a tool if required from the list of available tools.
    - For every tool call wait for the observe step which is the output from the called tool.

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL" , "content": "string", "tool": "string", "input": "string"}

    Available Tools:
    - get_weather: Takes city name as an input string and returns the weatther info about the city.


    Example 1:
    START: Hey, can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": ,"content": "Seems like user is interested in maths problem"}
    PLAN: { "step": "PLAN": ,"content": "Looking at the problem, we should solve this using BODMAS method"}
    PLAN: { "step": "PLAN": ,"content": "Yes, the BODMAS is correct thing to be done here"}
    PLAN: { "step": "PLAN": ,"content": "First, we multiply 3 * 5 which is 15"}
    PLAN: { "step": "PLAN": ,"content": "Now, the new equation is 2 + 15 / 10"}
    PLAN: { "step": "PLAN": ,"content": "We must perform divide operation. That is 15/10 = 1.5"}
    PLAN: { "step": "PLAN": ,"content": "Now the new equation is 2 + 1.5"}
    PLAN: { "step": "PLAN": ,"content": "Now, we perform addition that gives us 3.5 as the final answer."}
    PLAN: { "step": "PLAN": ,"content": "The expression 2 + 3 * 5 / 10 = 3.5"}
    OUTPUT: {"step": "OUTPUT", "content": The final answer is 3.5}

    Example 2:
    START: What is the weather of Bengaluru? 
    PLAN: { "step": "PLAN": , "content": "Seems like user is interested in getting weather of Bengaluru in India"}
    PLAN: { "step": "PLAN": , "content": "Lets see if we have any available tool from the list of available tools"}
    PLAN: { "step": "PLAN": , "content": "Great, we have get_weather tool available for this query."}
    PLAN: { "step": "PLAN": , "content": "I need to call get_weather tool for bengaluru as input for city"}
    PLAN: { "step": "TOOL": , "tool": "get_weather", "input": "delhi"}
    PLAN: { "step": "OBSERVE": , "tool": "get_weather", "output": "The weather in bengaluru is cloudy with 20 degrees Celcius"}
    PLAN: { "step": "PLAN": , "content": "Great, I got the weather info about Bengaluru"}
    OUTPUT: {"step": "OUTPUT", "content": "The current weather in Bengaluru is 20C with some cloudy sky."}
"""

# response_schema = {
#     "type": "object",
#     "properties": {
#         "step": {"type": "string"},
#         "content": {"type": "string"},
#         "tool": {"type": "string"},
#         "input": {"type": "string"}
#     },
#     "required": ["step", "content"]
# }

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc.")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="Input params for the tool")



def format_message_history_as_text(messages):
    lines = []
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        # Format roles like SYSTEM:, USER:, ASSISTANT:
        lines.append(f"{role.upper()}: {content}")
    return "\n".join(lines)


print("\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]


while True:
    user_query = input("👉 ")
    message_history.append({"role": "user", "content": user_query})

    while True:
        prompt_text = format_message_history_as_text(message_history)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=MyOutputFormat
            )
        )

        # parsed_result = response.candidates[0].content.parts[0].parsed
        parsed_result = response.parsed
        message_history.append({"role": "assistant", "content": parsed_result})

        # Parse JSON string from model response
        # parsed_result = json.loads(raw_result)
        # content = parsed_result.content

        if parsed_result.step == 'START':
            print("🔥", parsed_result.content)
            continue

        if parsed_result.step == 'PLAN':
            print("🧠", parsed_result.content)
            continue
        
        if parsed_result.step == 'TOOL':
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            if not tool_to_call or tool_to_call not in available_tools:
                print(f"❌ Invalid or missing tool in response: {parsed_result}")
                break
            print(f"🔨: {tool_to_call} ({tool_input})")
            tool_response = available_tools[tool_to_call](tool_input)
            print(f"🔨: {tool_to_call} ({tool_input}) = {tool_response}")
            message_history.append({"role": "developer", "content": json.dumps(
                {
                    "step": "OBSERVE",
                    "tool": tool_to_call,
                    "input": tool_input,
                    "output": tool_response
                }
            )})
            continue

        if parsed_result.step == 'OUTPUT':
            print("🎂", parsed_result.content)
            break



    print("\n\n\n")
