from google import genai
from google.genai import types
import json

client = genai.Client(
    api_key=''
)


SYSTEM_PROMPT = """
    You are an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN AND OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to be displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

    Example:
    START: Hey, can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in maths problem"}
    PLAN: { "step": "PLAN": "content": "Looking at the problem, we should solve this using BODMAS method"}
    PLAN: { "step": "PLAN": "content": "Yes, the BODMAS is correct thing to be done here"}
    PLAN: { "step": "PLAN": "content": "First, we multiply 3 * 5 which is 15"}
    PLAN: { "step": "PLAN": "content": "Now, the new equation is 2 + 15 / 10"}
    PLAN: { "step": "PLAN": "content": "We must perform divide operation. That is 15/10 = 1.5"}
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5"}
    PLAN: { "step": "PLAN": "content": "Now, we perform addition that gives us 3.5 as the final answer."}
    PLAN: { "step": "PLAN": "content": "The expression 2 + 3 * 5 / 10 = 3.5"}
    OUTPUT: {"step": "OUTPUT", "content": The final answer is 3.5}

"""

response_schema = {
    "type": "object",
    "properties": {
        "step": {"type": "string"},
        "content": {"type": "string"}
    },
    "required": ["step", "content"]
}

plan_json_str = """
{"step": "PLAN", "content": "The user wants a JavaScript code snippet to add an arbitrary number of numbers. I will provide a function for this."}
{"step": "PLAN", "content": "I will define a JavaScript function that uses the rest parameter syntax (...) to accept any number of arguments."}
{"step": "PLAN", "content": "Inside the function, I will use the `reduce` method on the array of numbers to calculate their sum."}
"""

HUMAN_PROMPT = """
Hey, write a code to add n numbers in JS.
"""
# Append the JSON plan string to your prompt
FULL_PROMPT = HUMAN_PROMPT + "\n\n" + plan_json_str

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = FULL_PROMPT,
    config=types.GenerateContentConfig(
        system_instruction = SYSTEM_PROMPT,
        response_mime_type =  "application/json",
        response_schema=response_schema
    )
)

print(response.candidates[0].content.parts[0].text)