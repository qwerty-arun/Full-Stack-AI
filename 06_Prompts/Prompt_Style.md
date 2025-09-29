# Prompt Styles

## Alpaca Prompting

- ### Instructions: <SYSTEM_PROMPT>\n
- ### Input: <USER_QUERY>
- ### Response:\n

## Chat ML (used by OpenAI, Gemini)
```
{
    "role": "system" | "user" | "assistant",
    "content": "string"
}
```

### INST Prompting (LLaMA-2)
- [INST] What is the time now? [/INST]